# Istio 配置示例

## 📑 目录

- [Istio 配置示例](#istio-配置示例)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 理论基础](#11-理论基础)
  - [2 Istio 安装配置](#2-istio-安装配置)
    - [2.1 Istio 安装](#21-istio-安装)
    - [2.2 命名空间自动注入](#22-命名空间自动注入)
    - [2.3 Istio Operator 配置](#23-istio-operator-配置)
  - [3 VirtualService 配置](#3-virtualservice-配置)
    - [3.1 基础路由配置](#31-基础路由配置)
    - [3.2 金丝雀发布配置](#32-金丝雀发布配置)
    - [3.3 流量镜像配置](#33-流量镜像配置)
  - [4 DestinationRule 配置](#4-destinationrule-配置)
    - [4.1 负载均衡配置](#41-负载均衡配置)
    - [4.2 熔断配置](#42-熔断配置)
    - [4.3 子集配置](#43-子集配置)
  - [5 Gateway 配置](#5-gateway-配置)
    - [5.1 入口网关配置](#51-入口网关配置)
    - [5.2 TLS 配置](#52-tls-配置)
  - [6 相关文档](#6-相关文档)
    - [6.1 理论论证](#61-理论论证)
    - [6.2 架构视角](#62-架构视角)
    - [6.3 技术文档](#63-技术文档)
  - [7 2025 年最新实践](#7-2025-年最新实践)
    - [7.1 Istio 1.22+ 新特性（2025）](#71-istio-122-新特性2025)
    - [7.2 Ambient Mesh 模式（2025）](#72-ambient-mesh-模式2025)
    - [7.3 Wasm 插件支持（2025）](#73-wasm-插件支持2025)
  - [8 实际应用案例](#8-实际应用案例)
    - [案例 1：微服务流量管理](#案例-1微服务流量管理)
    - [案例 2：服务间安全通信](#案例-2服务间安全通信)
    - [案例 3：多集群 Service Mesh](#案例-3多集群-service-mesh)

---

## 1 概述

本文档提供 **Istio Service Mesh 的实际配置示例**，包含可直接使用的 YAML 配置。

### 1.1 理论基础

Service Mesh 实现基于以下理论论证：

- **公理 A3（网络异步交付）**：消息传递语义 ≥ 共享内存语义
- **归纳映射 Ψ₄（网络抽象层）**：将 IP:Port 抽象为 ServiceName
- **定理 T1（身份-路由等价）**：身份-路由等价，路由函数 R(e) = v 是双射

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2 Istio 安装配置

### 2.1 Istio 安装

```bash
# 下载 Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*

# 安装 Istio
istioctl install --set profile=default

# 验证安装
istioctl verify-install
```

### 2.2 命名空间自动注入

```yaml
# 启用命名空间自动注入
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    istio-injection: enabled
```

### 2.3 Istio Operator 配置

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: control-plane
spec:
  profile: default
  components:
    pilot:
      k8s:
        resources:
          requests:
            cpu: 500m
            memory: 1024Mi
```

---

## 3 VirtualService 配置

### 3.1 基础路由配置

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
    - myapp
  http:
    - route:
        - destination:
            host: myapp
            subset: v1
```

### 3.2 金丝雀发布配置

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
    - reviews
  http:
    - match:
        - headers:
            end-user:
              exact: jason
      route:
        - destination:
            host: reviews
            subset: v2
    - route:
        - destination:
            host: reviews
            subset: v1
          weight: 90
        - destination:
            host: reviews
            subset: v2
          weight: 10
```

### 3.3 流量镜像配置

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
    - myapp
  http:
    - match:
        - uri:
            prefix: /
      route:
        - destination:
            host: myapp
            subset: v1
      mirror:
        host: myapp
        subset: v2
      mirrorPercentage:
        value: 100
```

---

## 4 DestinationRule 配置

### 4.1 负载均衡配置

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
        http2MaxRequests: 10
```

### 4.2 熔断配置

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  trafficPolicy:
    outlierDetection:
      consecutiveErrors: 3
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 50
```

### 4.3 子集配置

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

---

## 5 Gateway 配置

### 5.1 入口网关配置

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: myapp-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - myapp.example.com
```

### 5.2 TLS 配置

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: myapp-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: myapp-tls
      hosts:
        - myapp.example.com
```

---

## 6 相关文档

### 6.1 理论论证

- **`../../00-theory/02-induction-proof/psi4-network.md`** - 网络抽象层归纳映射
- **`../../00-theory/01-axioms/A3-network-async.md`** - 网络异步交付公理
- **`../../00-theory/05-lemmas-theorems/T1-identity-routing.md`** - 身份-路由等
  价定理

### 6.2 架构视角

- **`../../02-views/10-quick-views/service-mesh-view.md`** - Service Mesh 架构视
  角

### 6.3 技术文档

- **`../../../TECHNICAL/06-advanced-features/service-mesh/service-mesh.md`** - Service Mesh 技术文
  档

## 7 2025 年最新实践

### 7.1 Istio 1.22+ 新特性（2025）

**最新版本**：Istio 1.22+（2025 年 11 月）

**新特性**：

- **Ambient Mesh**：无 Sidecar 的 Service Mesh 模式
- **性能优化**：减少延迟和资源消耗
- **Telemetry API**：统一的遥测 API
- **Wasm 插件支持**：支持 Wasm 扩展

**安装最新版本**：

```bash
# 安装 Istio 1.22
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.22.0 sh -
cd istio-1.22.0
./bin/istioctl install --set profile=default
```

### 7.2 Ambient Mesh 模式（2025）

**Ambient Mesh 优势**：

- **无 Sidecar**：不需要在每个 Pod 中注入 Sidecar
- **性能提升**：减少延迟和资源消耗
- **简化运维**：减少 Sidecar 管理复杂度

**启用 Ambient Mesh**：

```bash
# 安装 Ambient Mesh
istioctl install --set profile=ambient

# 标记命名空间使用 Ambient Mesh
kubectl label namespace default istio.io/dataplane-mode=ambient
```

### 7.3 Wasm 插件支持（2025）

**Istio Wasm 插件**：

- **动态扩展**：无需重启即可加载 Wasm 插件
- **性能优化**：Wasm 插件执行效率高
- **安全隔离**：Wasm 插件提供安全隔离

**配置示例**：

```yaml
apiVersion: extensions.istio.io/v1alpha1
kind: WasmPlugin
metadata:
  name: my-wasm-plugin
spec:
  selector:
    matchLabels:
      app: myapp
  url: oci://myregistry.com/wasm-plugins/my-plugin:v1.0.0
  phase: AUTHN
```

## 8 实际应用案例

### 案例 1：微服务流量管理

**场景**：管理微服务之间的流量路由和负载均衡

**实现方案**：

```yaml
# VirtualService：流量路由
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        end-user:
          exact: jason
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
      weight: 50
    - destination:
        host: reviews
        subset: v3
      weight: 50

---
# DestinationRule：负载均衡策略
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews
spec:
  host: reviews
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
  - name: v3
    labels:
      version: v3
```

**效果**：

- 流量路由：根据用户和权重进行流量路由
- 负载均衡：使用最少连接负载均衡策略
- 金丝雀发布：支持渐进式发布

### 案例 2：服务间安全通信

**场景**：实现服务间的 mTLS 通信

**实现方案**：

```yaml
# PeerAuthentication：启用 mTLS
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT

---
# AuthorizationPolicy：访问控制
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-frontend
  namespace: production
spec:
  selector:
    matchLabels:
      app: backend
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/production/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
```

**效果**：

- mTLS 加密：所有服务间通信自动加密
- 访问控制：基于服务身份的访问控制
- 安全加固：减少中间人攻击风险

### 案例 3：多集群 Service Mesh

**场景**：跨多个 Kubernetes 集群的 Service Mesh

**实现方案**：

```bash
# 安装 Istio 多集群
istioctl install --set profile=multicluster

# 配置多集群网络
istioctl create-remote-secret \
  --name=cluster-1 \
  --context=cluster-1-context | \
  kubectl apply -f - --context=cluster-2-context
```

**效果**：

- 跨集群通信：实现跨集群的服务通信
- 统一管理：统一管理多个集群的流量
- 故障隔离：集群间故障隔离

---

**更新时间**：2025-11-15 **版本**：v1.1 **状态**：✅ 包含 2025 年最新实践
