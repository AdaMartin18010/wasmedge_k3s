# Service Mesh 模式：侧车与代理

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 核心思想](#11-核心思想)
- [2 Service Mesh 模式定义](#2-service-mesh-模式定义)
  - [2.1 Service Mesh 模式概念](#21-service-mesh-模式概念)
  - [2.2 Service Mesh 模式结构](#22-service-mesh-模式结构)
  - [2.3 Service Mesh 模式特点](#23-service-mesh-模式特点)
- [3 架构中的应用](#3-架构中的应用)
  - [3.1 Istio Service Mesh](#31-istio-service-mesh)
  - [3.2 Linkerd Service Mesh](#32-linkerd-service-mesh)
- [4 Service Mesh 模式实现](#4-service-mesh-模式实现)
  - [4.1 Istio 配置示例](#41-istio-配置示例)
  - [4.2 Linkerd 配置示例](#42-linkerd-配置示例)
- [5 Service Mesh 模式优势](#5-service-mesh-模式优势)
  - [5.1 透明治理](#51-透明治理)
  - [5.2 统一控制](#52-统一控制)
  - [5.3 可观测性](#53-可观测性)
- [6 Service Mesh 模式与其他模式](#6-service-mesh-模式与其他模式)
  - [6.1 Service Mesh vs API Gateway](#61-service-mesh-vs-api-gateway)
  - [6.2 Service Mesh vs Sidecar](#62-service-mesh-vs-sidecar)
- [7 形式化定义](#7-形式化定义)
  - [7.1 Service Mesh 模式定义](#71-service-mesh-模式定义)
  - [7.2 Sidecar 定义](#72-sidecar-定义)
  - [7.3 Control Plane 定义](#73-control-plane-定义)
- [8 相关文档](#8-相关文档)
  - [8.1 组合模式文档](#81-组合模式文档)
  - [8.2 参考资源](#82-参考资源)
- [9 总结](#9-总结)

---

## 1 概述

本文档详细阐述**Service Mesh 模式**在架构设计中的应用，通过侧车和代理实现流量治
理。

### 1.1 核心思想

> **通过 Service Mesh 模式将流量治理从应用中分离出来，通过侧车代理实现统一治理**

## 2 Service Mesh 模式定义

### 2.1 Service Mesh 模式概念

**Service Mesh 模式**是一种架构模式，通过侧车代理实现流量治理。

### 2.2 Service Mesh 模式结构

```text
Application Pod
├── Application Container
└── Sidecar Container (Envoy)
    ├── Control Plane (Istio)
    ├── Traffic Management
    ├── Security (mTLS)
    └── Observability (Metrics/Tracing)
```

### 2.3 Service Mesh 模式特点

**Service Mesh 模式特点**：

- **侧车代理**：每个 Pod 都有侧车代理
- **透明治理**：流量治理对应用透明
- **统一控制**：通过控制平面统一控制
- **可观测性**：自动注入遥测数据

## 3 架构中的应用

### 3.1 Istio Service Mesh

**Istio Service Mesh 架构**：

```text
Application Pod
├── Application Container
└── Istio Sidecar (Envoy)
    ├── Istio Control Plane
    │   ├── Pilot (配置管理)
    │   ├── Citadel (安全)
    │   └── Galley (配置验证)
    ├── Traffic Management
    │   ├── VirtualService
    │   ├── DestinationRule
    │   └── Gateway
    ├── Security
    │   ├── mTLS
    │   └── AuthorizationPolicy
    └── Observability
        ├── Prometheus (Metrics)
        ├── Tempo (Tracing)
        └── Grafana (Visualization)
```

**Istio Service Mesh 特点**：

- **侧车注入**：自动注入 Envoy sidecar
- **配置驱动**：通过 CRD 配置流量治理
- **统一控制**：通过控制平面统一控制
- **可观测性**：自动注入遥测数据

### 3.2 Linkerd Service Mesh

**Linkerd Service Mesh 架构**：

```text
Application Pod
├── Application Container
└── Linkerd Sidecar (Linkerd Proxy)
    ├── Linkerd Control Plane
    │   ├── Destination (服务发现)
    │   ├── Identity (安全)
    │   └── Public API
    ├── Traffic Management
    │   ├── ServiceProfile
    │   └── TrafficSplit
    ├── Security
    │   ├── mTLS
    │   └── Authorization
    └── Observability
        ├── Metrics
        └── Tracing
```

**Linkerd Service Mesh 特点**：

- **轻量级**：Linkerd Proxy 更轻量
- **Rust 实现**：性能更好
- **易于使用**：配置更简单
- **可观测性**：自动注入遥测数据

## 4 Service Mesh 模式实现

### 4.1 Istio 配置示例

**VirtualService 配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
    - order-service
  http:
    - match:
        - headers:
            version:
              exact: v1
      route:
        - destination:
            host: order-service
            subset: v1
    - route:
        - destination:
            host: order-service
            subset: v2
          weight: 10
        - destination:
            host: order-service
            subset: v1
          weight: 90
```

**DestinationRule 配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: order-service
spec:
  host: order-service
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
```

**AuthorizationPolicy 配置**：

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: order-service-policy
spec:
  selector:
    matchLabels:
      app: order-service
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/default/sa/frontend"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/orders"]
```

### 4.2 Linkerd 配置示例

**ServiceProfile 配置**：

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: order-service
  namespace: default
spec:
  routes:
    - name: GET /orders
      condition:
        method: GET
        pathRegex: /orders
      isRetryable: true
      timeout: 30s
```

**TrafficSplit 配置**：

```yaml
apiVersion: split.smi-spec.io/v1alpha1
kind: TrafficSplit
metadata:
  name: order-service-split
spec:
  service: order-service
  backends:
    - service: order-service-v1
      weight: 90
    - service: order-service-v2
      weight: 10
```

## 5 Service Mesh 模式优势

### 5.1 透明治理

**Service Mesh 模式优势**：

- **应用无感知**：流量治理对应用透明
- **无需修改代码**：应用无需修改代码
- **统一治理**：通过控制平面统一治理

### 5.2 统一控制

**Service Mesh 模式优势**：

- **配置驱动**：通过 CRD 配置流量治理
- **统一控制**：通过控制平面统一控制
- **动态更新**：配置可以动态更新

### 5.3 可观测性

**Service Mesh 模式优势**：

- **自动注入**：自动注入遥测数据
- **统一遥测**：统一的遥测标准
- **可视化**：通过 Grafana 可视化

## 6 Service Mesh 模式与其他模式

### 6.1 Service Mesh vs API Gateway

**Service Mesh vs API Gateway**：

| 模式             | 特点               | 使用场景       |
| ---------------- | ------------------ | -------------- |
| **Service Mesh** | 侧车代理，透明治理 | 微服务内部通信 |
| **API Gateway**  | 入口网关，统一入口 | 外部访问入口   |

### 6.2 Service Mesh vs Sidecar

**Service Mesh vs Sidecar**：

| 模式             | 特点               | 使用场景       |
| ---------------- | ------------------ | -------------- |
| **Service Mesh** | 完整的流量治理平台 | 微服务架构     |
| **Sidecar**      | 单个侧车代理       | 特定场景的代理 |

## 7 形式化定义

### 7.1 Service Mesh 模式定义

```text
Service Mesh M = ⟨sidecars, controlPlane, policies, observability⟩
其中：
- sidecars: 侧车代理集合
- controlPlane: 控制平面
- policies: 策略配置集合
- observability: 可观测性组件集合
```

### 7.2 Sidecar 定义

```text
Sidecar S = ⟨proxy, policies, metrics, tracing⟩
其中：
- proxy: 代理组件
- policies: 策略配置
- metrics: 指标收集
- tracing: 追踪收集
```

### 7.3 Control Plane 定义

```text
Control Plane C = ⟨config, discovery, security, observability⟩
其中：
- config: 配置管理
- discovery: 服务发现
- security: 安全管理
- observability: 可观测性管理
```

## 8 相关文档

### 8.1 组合模式文档

- **[组合模式文档集](README.md)** - 组合模式文档集说明
- **[Service Mesh Patterns](./04-service-mesh-pattern.md)** - Service Mesh 模式
  （本文件）
- **[Service Aggregation 模式](./05-nsm-pattern.md#service-aggregation)** -
  Service Aggregation 模式（在本目录中）
- **[Service Mesh 与 NSM](../03-service-mesh-nsm/)** - Service Mesh 和 NSM 的组
  合模式

### 8.2 参考资源

- **[REFERENCES.md](../../REFERENCES.md)** - 参考标准、框架、工具和资源
- **[ACADEMIC-REFERENCES.md](../../ACADEMIC-REFERENCES.md)** - Wikipedia、大学课
  程、学术论文等学术资源

## 9 总结

通过**Service Mesh 模式**，我们实现了：

1. **侧车代理**：每个 Pod 都有侧车代理，实现透明治理
2. **统一控制**：通过控制平面统一控制流量治理
3. **配置驱动**：通过 CRD 配置流量治理，无需修改代码
4. **可观测性**：自动注入遥测数据，实现统一可观测性
5. **安全性**：通过 mTLS 和 AuthorizationPolicy 实现安全治理

**相关模式**：Service Mesh 模式可以与 Service Aggregation 模式结合使用，Service
Mesh 负责流量治理，Service Aggregation 负责服务聚合。详细内容请参考
[Service Aggregation 模式](./05-nsm-pattern.md#service-aggregation)。

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
914-983 行，Service Mesh 模式部分
