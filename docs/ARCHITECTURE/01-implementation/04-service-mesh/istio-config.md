# Istio 配置示例

## 📑 目录

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

---

**更新时间**：2025-11-04 **版本**：v1.0 **状态**：✅ 基础示例已创建
