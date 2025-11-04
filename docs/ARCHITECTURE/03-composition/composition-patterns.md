# 组合模式与实践

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 核心思想](#11-核心思想)
- [2. 组合模式概述](#2-组合模式概述)
  - [核心原则](#核心原则)
- [2. 组合模式分类](#2-组合模式分类)
- [3. Adapter / Bridge 模式](#3-adapter--bridge-模式)
  - [3.1 跨技术边界](#31-跨技术边界)
  - [3.2 典型案例](#32-典型案例)
- [4. Facade / API Gateway 模式](#4-facade--api-gateway-模式)
  - [4.1 聚合多服务](#41-聚合多服务)
  - [4.2 典型案例](#42-典型案例)
- [5. Composite 模式](#5-composite-模式)
  - [5.1 递归聚合](#51-递归聚合)
  - [5.2 典型案例](#52-典型案例)
- [6. Pipeline / Orchestration 模式](#6-pipeline--orchestration-模式)
  - [6.1 流程编排](#61-流程编排)
  - [6.2 典型案例](#62-典型案例)
- [7. Service Mesh 模式](#7-service-mesh-模式)
  - [7.1 通讯治理](#71-通讯治理)
  - [7.2 典型案例](#72-典型案例)
- [8. Observability 模式](#8-observability-模式)
  - [8.1 统一监控](#81-统一监控)
  - [8.2 典型案例](#82-典型案例)
- [9. 组合模式的最佳实践](#9-组合模式的最佳实践)
  - [9.1 边界清晰](#91-边界清晰)
  - [9.2 契约优先](#92-契约优先)
  - [9.3 无缝替换](#93-无缝替换)
  - [9.4 监控/治理](#94-监控治理)
- [10. 组合模式的形式化](#10-组合模式的形式化)
  - [10.1 组合函数](#101-组合函数)
  - [10.2 范畴论视角](#102-范畴论视角)
- [12. 2025 年 11 月最新趋势](#12-2025-年-11-月最新趋势)
  - [12.1 组合模式趋势](#121-组合模式趋势)
  - [12.2 工具趋势](#122-工具趋势)
  - [12.3 架构趋势](#123-架构趋势)
- [13. 参考资源](#13-参考资源)

---

## 1. 概述

本文档阐述架构设计的核心：**组合模式**，通过组合模式把拆解后的子结构"拼接"成最终
应用，实现关注点分离和持续演进。

### 1.1 核心思想

> **组合模式通过接口统一、安全与治理、弹性等原则，将拆解后的组件组合成最终应用，
> 实现关注点分离和持续演进**

---

## 2. 组合模式概述

组合模式是架构设计的核心，通过**组合模式**把拆解后的子结构"拼接"成最终应用。

### 核心原则

1. **接口统一**：无论是 VM、容器还是沙箱，所有外部调用都通过 **Gateway/Facade**
2. **安全与治理**：在**服务网格**和**沙箱**层统一施行安全策略，避免在业务层散布
   安全细节
3. **弹性**：**Pipeline/Orchestration** 把业务流程与底层技术解耦，支持快速迭代

## 2. 组合模式分类

| 组合模式                     | 作用           | 典型技术/工具                 | 典型场景               |
| ---------------------------- | -------------- | ----------------------------- | ---------------------- |
| **Adapter / Bridge**         | 兼容不同技术栈 | gRPC‑to‑REST, JDBC‑to‑JPA     | 把传统服务迁移到容器中 |
| **Facade / API‑Gateway**     | 聚合多服务     | Kong, Istio Gateway           | 简化外部调用、统一鉴权 |
| **Composite**                | 递归聚合       | Service‑Mesh 组合、聚合微服务 | 支持业务树形结构       |
| **Pipeline / Orchestration** | 流程编排       | Temporal, Argo Workflows      | 事务、Saga、事件驱动   |
| **Service‑Mesh**             | 通讯治理       | Envoy, Istio                  | 负载均衡、熔断、MTLS   |
| **Observability**            | 监控与追踪     | OpenTelemetry, Prometheus     | 统一度量、日志、追踪   |

## 3. Adapter / Bridge 模式

### 3.1 跨技术边界

**场景**：传统服务迁移到容器化环境

```text
传统服务 (REST) → Adapter → 容器化服务 (gRPC)
    ↓
统一接口，平滑迁移
```

**技术实现**：

- **gRPC ↔ REST**：Envoy gRPC-Web，API Gateway
- **JDBC ↔ JPA**：数据访问层适配器
- **Docker ↔ K8s**：容器运行时接口（CRI）

### 3.2 典型案例

**支付网关适配**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: legacy-payment
spec:
  hosts:
    - legacy-payment.example.com
  ports:
    - number: 443
      name: https
      protocol: HTTPS
  location: MESH_EXTERNAL
  resolution: DNS
```

## 4. Facade / API Gateway 模式

### 4.1 聚合多服务

**场景**：单一入口聚合内部 API

```text
Client → API Gateway → [Service A, Service B, Service C]
    ↓
统一认证、限流、路由
```

**技术实现**：

- **Istio Gateway**：统一入口，流量管理
- **Kong**：API 网关，插件系统
- **Spring Cloud Gateway**：Java 生态网关

### 4.2 典型案例

**Istio Gateway 配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: api-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - api.example.com
```

## 5. Composite 模式

### 5.1 递归聚合

**场景**：服务网格组合、聚合微服务

```text
Service Mesh (Istio) + NSM (vWire) + OPA (策略)
    ↓
多层次组合，统一治理
```

**技术实现**：

- **Service Mesh**：流量治理
- **NSM**：网络服务聚合
- **OPA**：策略决策

### 5.2 典型案例

**多层组合**：

```yaml
# Service Mesh
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: composite-service
spec:
  hosts:
    - service-a
    - service-b
  http:
    - route:
        - destination:
            host: service-a
          weight: 50
        - destination:
            host: service-b
          weight: 50
```

## 6. Pipeline / Orchestration 模式

### 6.1 流程编排

**场景**：长事务、订单处理

```text
订单创建 → 支付 → 库存 → 物流 → 通知
    ↓
Saga 模式，分布式事务
```

**技术实现**：

- **Temporal**：工作流引擎，可靠性保证
- **Argo Workflows**：Kubernetes 工作流
- **Camunda**：BPMN 流程引擎

### 6.2 典型案例

**Temporal 工作流**：

```go
func OrderWorkflow(ctx workflow.Context, order Order) error {
    // 1. 创建订单
    err := workflow.ExecuteActivity(ctx, CreateOrderActivity, order).Get(ctx, nil)
    if err != nil {
        return err
    }

    // 2. 支付
    err = workflow.ExecuteActivity(ctx, PaymentActivity, order).Get(ctx, nil)
    if err != nil {
        // 补偿：取消订单
        workflow.ExecuteActivity(ctx, CancelOrderActivity, order).Get(ctx, nil)
        return err
    }

    // 3. 库存
    err = workflow.ExecuteActivity(ctx, InventoryActivity, order).Get(ctx, nil)
    if err != nil {
        // 补偿：退款 + 取消订单
        workflow.ExecuteActivity(ctx, RefundActivity, order).Get(ctx, nil)
        workflow.ExecuteActivity(ctx, CancelOrderActivity, order).Get(ctx, nil)
        return err
    }

    return nil
}
```

## 7. Service Mesh 模式

### 7.1 通讯治理

**场景**：负载均衡、熔断、MTLS

```text
Service A → Sidecar (Envoy) → Sidecar (Envoy) → Service B
    ↓
统一流量治理，安全通信
```

**技术实现**：

- **Istio**：Envoy 代理，控制平面
- **Linkerd**：轻量级 Service Mesh
- **Consul Connect**：服务发现集成

### 7.2 典型案例

**Istio 流量管理**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews
spec:
  host: reviews
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutiveErrors: 3
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

## 8. Observability 模式

### 8.1 统一监控

**场景**：统一度量、日志、追踪

```text
应用 → OpenTelemetry → Prometheus → Grafana
    ↓
统一可观测性，全链路追踪
```

**技术实现**：

- **OpenTelemetry**：统一标准，自动检测
- **Prometheus**：指标收集和存储
- **Grafana**：可视化面板
- **Tempo**：分布式追踪

### 8.2 典型案例

**OpenTelemetry 配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-config
data:
  otel-collector-config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
    processors:
      batch:
        timeout: 1s
        send_batch_size: 1024
    exporters:
      prometheus:
        endpoint: "0.0.0.0:8889"
      logging:
        loglevel: debug
    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [batch]
          exporters: [logging]
        metrics:
          receivers: [otlp]
          processors: [batch]
          exporters: [prometheus]
```

## 9. 组合模式的最佳实践

### 9.1 边界清晰

- **不要让一个服务承担多种职责**
- **接口优先**：接口（API、事件）先写，业务再写

### 9.2 契约优先

- **统一接口**：API Gateway、Service Mesh
- **版本管理**：接口版本化，向后兼容

### 9.3 无缝替换

- **Service Registry**：Eureka、Consul 实现动态发现
- **健康检查**：自动故障转移

### 9.4 监控/治理

- **在每一层都加上日志、指标、追踪**
- **统一身份**：OpenID Connect
- **统一授权**：OPA/Gatekeeper

## 10. 组合模式的形式化

### 10.1 组合函数

```text
组合 = f(g(h(x)))
```

其中：

- h：底层抽象（虚拟化）
- g：中层抽象（容器化）
- f：上层抽象（服务网格）

### 10.2 范畴论视角

- **对象**：VM、Container、Service
- **态射**：组合函数
- **函子**：抽象层映射

## 12. 2025 年 11 月最新趋势

### 12.1 组合模式趋势

- **Service Mesh 成熟**：Istio、Linkerd 大规模应用
- **NSM 兴起**：跨域网络服务聚合
- **OPA 普及**：策略即代码成为标准实践

### 12.2 工具趋势

- **GitOps 成熟**：ArgoCD、Flux 成为标准
- **可观测性统一**：OpenTelemetry 成为事实标准
- **自动化增强**：AI 辅助的组合模式优化

### 12.3 架构趋势

- **事件驱动架构**：事件溯源和 CQRS 的普及
- **微服务细化**：从服务拆分到功能拆分
- **领域驱动设计**：DDD 在云原生架构中的应用

---

## 13. 参考资源

- **"Patterns of Enterprise Application Architecture" (Martin
  Fowler)**：<https://martinfowler.com/books/eaa.html>
- **"Design Patterns: Elements of Reusable Object-Oriented Software" (Gang of
  Four)**：<https://en.wikipedia.org/wiki/Design_Patterns>
- **Istio 文档**：<https://istio.io/latest/docs/>
- **Temporal 文档**：<https://docs.temporal.io/>
- **相关文档**：
  - `03-composition/adapter-bridge-pattern.md` - Adapter/Bridge 模式详细说明
  - `03-composition/facade-gateway-pattern.md` - Facade/Gateway 模式详细说明
  - `03-composition/pipeline-orchestration.md` - Pipeline/Orchestration 模式详细
    说明
  - `08-composition-patterns/` - 组合模式详细文档

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第 4 节
，组合模式部分
