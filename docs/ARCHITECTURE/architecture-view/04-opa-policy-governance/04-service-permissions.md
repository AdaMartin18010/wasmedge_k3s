# 服务间权限：把"服务间权限"组合化

## 1. 概述

本文档详细阐述如何通过 **Service Mesh + OPA** 实现**服务间权限**的组合化管理。

### 1.1 核心思想

> **通过 Service Mesh + OPA 实现服务间权限的组合化，同一策略可附加到任意
> <source, destination> 对，实现可证明、可版本化的权限控制**

## 2. Service Mesh + OPA 组合

### 2.1 场景描述

**Service Mesh + OPA**：

- **身份** = SPIFFE ID
- **流量属性** = HTTP method, path, header
- **OPA 作为外部授权服务**（Envoy ext_authz）

### 2.2 架构设计

```text
Client Pod
├── Istio Sidecar
└── OPA Agent (PDP)
    └── Decision: allow / deny / rate-limit / routing
```

## 3. OPA 服务间权限策略

### 3.1 Rego 策略示例

**服务间权限策略**：

```rego
package mesh.authz

import rego.v1

default allow = false

# 允许前端访问订单服务
allow {
  input.attributes.destination.principal == "spiffe://A/ns/default/sa/frontend"
  input.attributes.source.principal == "spiffe://B/ns/default/sa/order-service"
  input.attributes.request.http.method == "GET"
  input.attributes.request.http.path == "/orders"
}

# 允许后端访问支付服务
allow {
  input.attributes.destination.principal == "spiffe://A/ns/default/sa/order-service"
  input.attributes.source.principal == "spiffe://B/ns/default/sa/payment-service"
  input.attributes.request.http.method == "POST"
  input.attributes.request.http.path == "/payments"
}

# 允许监控服务访问 metrics 端点
allow {
  input.attributes.request.http.path == "/metrics"
  input.attributes.source.principal == "spiffe://A/ns/default/sa/prometheus"
}
```

### 3.2 组合性

**同一策略可附加到任意 <source, destination> 对**：

```rego
# 通用权限策略
allow {
  source_allowed[input.attributes.source.principal]
  destination_allowed[input.attributes.destination.principal]
  method_allowed[input.attributes.request.http.method]
  path_allowed[input.attributes.request.http.path]
}

# 允许的服务列表
source_allowed = {
  "spiffe://A/ns/default/sa/frontend",
  "spiffe://A/ns/default/sa/order-service",
  "spiffe://A/ns/default/sa/payment-service"
}

destination_allowed = {
  "spiffe://B/ns/default/sa/order-service",
  "spiffe://B/ns/default/sa/payment-service",
  "spiffe://B/ns/default/sa/inventory-service"
}

method_allowed = {
  "GET",
  "POST"
}

path_allowed = {
  "/orders",
  "/payments",
  "/inventory",
  "/metrics"
}
```

## 4. Istio AuthorizationPolicy 集成

### 4.1 AuthorizationPolicy 配置

**Istio AuthorizationPolicy**：

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: order-service-policy
  namespace: default
spec:
  selector:
    matchLabels:
      app: order-service
  action: CUSTOM
  provider:
    name: opa
  rules:
    - to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/orders", "/orders/*"]
```

### 4.2 OPA Provider 配置

**OPA Provider**：

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: opa-provider
spec:
  provider:
    name: opa
    config:
      opa:
        endpoint: http://opa:8181/v1/data/mesh/authz/allow
```

## 5. 服务间权限组合模式

### 5.1 组合模式类型

| 组合模式     | 说明                        | 典型实现       |
| ------------ | --------------------------- | -------------- |
| **基于身份** | 根据 SPIFFE ID 授权         | OPA + SPIFFE   |
| **基于路径** | 根据 HTTP path 授权         | OPA + Envoy    |
| **基于方法** | 根据 HTTP method 授权       | OPA + Envoy    |
| **基于标签** | 根据 Kubernetes labels 授权 | OPA + K8s      |
| **基于时间** | 根据时间范围授权            | OPA + 时间策略 |
| **基于条件** | 根据复杂条件授权            | OPA + Rego     |

### 5.2 组合示例

**基于身份 + 路径 + 方法**：

```rego
package mesh.authz

import rego.v1

default allow = false

allow {
  # 身份验证
  source.principal == "spiffe://A/ns/default/sa/frontend"
  destination.principal == "spiffe://B/ns/default/sa/order-service"

  # 路径验证
  request.http.path == "/orders"

  # 方法验证
  request.http.method == "GET"
}
```

## 6. 权限组合的归纳收益

### 6.1 组合性

**同一策略可附加到任意 <source, destination> 对**：

- 策略可以组合和重用
- 支持复杂的权限规则

### 6.2 可证明性

**Rego → AST → SAT，可在 CI 中跑 tautology check**：

- 策略决策等价于 SAT 问题
- 可自动验证策略的正确性

### 6.3 版本一致性

**策略与镜像共用 Git SHA，回滚即 git revert**：

- 策略与代码同步版本化
- 支持快速回滚

## 7. 典型场景

### 7.1 微服务权限管理

**场景**：管理微服务间的访问权限

**策略**：

```rego
package mesh.authz

import rego.v1

default allow = false

# 允许服务访问
allow {
  source_service := input.attributes.source.principal
  destination_service := input.attributes.destination.principal
  allowed_routes[source_service][destination_service]
}

# 允许的路由
allowed_routes = {
  "spiffe://A/ns/default/sa/frontend": {
    "spiffe://B/ns/default/sa/order-service": ["GET", "POST"],
    "spiffe://B/ns/default/sa/payment-service": ["POST"]
  },
  "spiffe://A/ns/default/sa/order-service": {
    "spiffe://B/ns/default/sa/payment-service": ["POST"],
    "spiffe://B/ns/default/sa/inventory-service": ["GET", "POST"]
  }
}
```

### 7.2 多租户权限管理

**场景**：多租户 SaaS 应用的权限管理

**策略**：

```rego
package mesh.authz

import rego.v1

default allow = false

# 允许租户访问自己的资源
allow {
  source_tenant := input.attributes.source.labels["tenant"]
  destination_tenant := input.attributes.destination.labels["tenant"]
  source_tenant == destination_tenant
}
```

## 8. 形式化定义

### 8.1 服务间权限定义

```text
服务间权限 P = ⟨source, destination, method, path, policy⟩
其中：
- source: 源服务身份（SPIFFE ID）
- destination: 目标服务身份（SPIFFE ID）
- method: HTTP 方法
- path: HTTP 路径
- policy: 权限策略（OPA Rego）
```

### 8.2 权限决策定义

```text
权限决策 D = OPA(source, destination, method, path)
其中：
- D ∈ {allow, deny}
- OPA: OPA 决策函数
```

### 8.3 权限组合定义

```text
权限组合 C = P₁ ∘ P₂ ∘ ... ∘ Pₙ
其中：
- Pᵢ: 权限策略
- ∘: 组合操作
```

## 9. 总结

通过**服务间权限**，OPA + Service Mesh 实现了：

1. **组合性**：同一策略可附加到任意 <source, destination> 对
2. **可证明性**：策略决策等价于 SAT 问题，可自动验证
3. **版本一致性**：策略与代码同步版本化
4. **灵活性**：支持复杂的权限规则和组合模式
5. **可审计性**：所有权限决策可审计和追溯

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
2028-2056 行，服务间权限部分
