# API 多区域部署规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 多区域架构](#11-多区域架构)
- [2. 区域架构](#2-区域架构)
  - [2.1 区域配置](#21-区域配置)
  - [2.2 区域标签](#22-区域标签)
- [3. 流量路由](#3-流量路由)
  - [3.1 基于地理位置的路由](#31-基于地理位置的路由)
  - [3.2 基于延迟的路由](#32-基于延迟的路由)
- [4. 数据同步](#4-数据同步)
  - [4.1 数据库复制](#41-数据库复制)
  - [4.2 缓存同步](#42-缓存同步)
- [5. 故障切换](#5-故障切换)
  - [5.1 自动故障切换](#51-自动故障切换)
  - [5.2 手动故障切换](#52-手动故障切换)
- [6. 延迟优化](#6-延迟优化)
  - [6.1 CDN 集成](#61-cdn-集成)
  - [6.2 边缘计算](#62-边缘计算)
- [7. 成本优化](#7-成本优化)
  - [7.1 区域成本对比](#71-区域成本对比)
  - [7.2 成本优化策略](#72-成本优化策略)
- [8. 相关文档](#8-相关文档)

---

## 1. 概述

API 多区域部署规范定义了 API 在多区域环境下的部署策略和配置，从区域架构到流量路
由，从数据同步到故障切换。

### 1.1 多区域架构

```text
主区域（Primary Region）
  ↓
次区域（Secondary Region）
  ↓
边缘区域（Edge Regions）
  ↓
全局负载均衡（Global Load Balancer）
```

---

## 2. 区域架构

### 2.1 区域配置

**多区域部署配置**：

```yaml
apiVersion: api.example.com/v1
kind: APIMultiRegion
metadata:
  name: payment-api-multiregion
spec:
  regions:
    - name: us-east-1
      role: primary
      replicas: 6
      resources:
        requests:
          cpu: "500m"
          memory: "512Mi"
    - name: us-west-2
      role: secondary
      replicas: 3
      resources:
        requests:
          cpu: "500m"
          memory: "512Mi"
    - name: eu-west-1
      role: edge
      replicas: 2
      resources:
        requests:
          cpu: "200m"
          memory: "256Mi"
```

### 2.2 区域标签

**区域标签配置**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-api-us-east-1
spec:
  replicas: 6
  template:
    metadata:
      labels:
        app: payment-api
        region: us-east-1
        role: primary
    spec:
      nodeSelector:
        topology.kubernetes.io/region: us-east-1
```

---

## 3. 流量路由

### 3.1 基于地理位置的路由

**Istio 地理位置路由**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-api-vs
spec:
  hosts:
    - payment-api
  http:
    - match:
        - headers:
            x-forwarded-for:
              regex: ".*\\.(us|ca)\\..*"
      route:
        - destination:
            host: payment-api-us-east-1
          weight: 100
    - match:
        - headers:
            x-forwarded-for:
              regex: ".*\\.(eu|uk|de)\\..*"
      route:
        - destination:
            host: payment-api-eu-west-1
          weight: 100
    - route:
        - destination:
            host: payment-api-us-east-1
          weight: 70
        - destination:
            host: payment-api-us-west-2
          weight: 30
```

### 3.2 基于延迟的路由

**基于延迟的路由配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-api-dr
spec:
  host: payment-api
  trafficPolicy:
    loadBalancer:
      localityLbSetting:
        enabled: true
        distribute:
          - from: us-east-1/*
            to:
              "us-east-1/*": 70
              "us-west-2/*": 30
```

---

## 4. 数据同步

### 4.1 数据库复制

**PostgreSQL 主从复制**：

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: payment-db
spec:
  instances: 3
  postgresql:
    parameters:
      max_connections: "200"
  primaryUpdateStrategy: unsupervised
  replication:
    syncReplicaElectionConstraint:
      enabled: true
```

### 4.2 缓存同步

**Redis 主从复制**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
data:
  redis.conf: |
    replicaof redis-master 6379
    replica-read-only yes
```

---

## 5. 故障切换

### 5.1 自动故障切换

**故障切换配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-api-dr-failover
spec:
  host: payment-api
  trafficPolicy:
    outlierDetection:
      consecutiveErrors: 3
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
        http2MaxRequests: 100
```

### 5.2 手动故障切换

**故障切换步骤**：

```bash
# 1. 检查主区域状态
kubectl get pods -l region=us-east-1,app=payment-api

# 2. 切换到次区域
kubectl patch virtualservice payment-api-vs \
  --type merge \
  -p '{"spec":{"http":[{"route":[{"destination":{"host":"payment-api-us-west-2"},"weight":100}]}]}}'

# 3. 验证切换
kubectl get virtualservice payment-api-vs
```

---

## 6. 延迟优化

### 6.1 CDN 集成

**CDN 配置**：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: payment-api-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: payment-api
                port:
                  number: 8080
```

### 6.2 边缘计算

**边缘节点部署**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-api-edge
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: payment-api
        tier: edge
    spec:
      nodeSelector:
        node-role.kubernetes.io/edge: "true"
      containers:
        - name: app
          image: payment-api-wasm:latest
          resources:
            requests:
              memory: "64Mi"
              cpu: "50m"
```

---

## 7. 成本优化

### 7.1 区域成本对比

**区域成本矩阵**：

| 区域          | 实例成本 | 数据传输成本 | 总成本  |
| ------------- | -------- | ------------ | ------- |
| **us-east-1** | $100/月  | $10/月       | $110/月 |
| **us-west-2** | $120/月  | $15/月       | $135/月 |
| **eu-west-1** | $130/月  | $20/月       | $150/月 |

### 7.2 成本优化策略

**成本优化配置**：

```yaml
apiVersion: api.example.com/v1
kind: APIMultiRegion
metadata:
  name: payment-api-cost-optimized
spec:
  costOptimization:
    enabled: true
    strategy: "use-cheapest-region"
    regions:
      - name: us-east-1
        cost: 110
        priority: 1
      - name: us-west-2
        cost: 135
        priority: 2
```

---

## 8. 相关文档

- **[API 故障恢复](../32-api-disaster-recovery/api-disaster-recovery.md)** - 故
  障切换
- **[API 成本优化](../21-api-cost-optimization/api-cost-optimization.md)** - 成
  本优化
- **[API 性能优化](../14-api-performance/api-performance.md)** - 延迟优化
- **[最佳实践](../08-best-practices/best-practices.md)** - 多区域部署最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新**：2025-11-07 **维护者**：项目团队
