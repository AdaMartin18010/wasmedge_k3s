# 弹性伸缩：自动横向扩缩与渐进式交付

## 📑 目录

- [弹性伸缩：自动横向扩缩与渐进式交付](#弹性伸缩自动横向扩缩与渐进式交付)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 核心思想](#11-核心思想)
  - [2 弹性伸缩类型](#2-弹性伸缩类型)
    - [2.1 弹性伸缩类型概览](#21-弹性伸缩类型概览)
    - [2.2 弹性伸缩对比](#22-弹性伸缩对比)
  - [3 HPA（水平自动伸缩）](#3-hpa水平自动伸缩)
    - [3.1 HPA 定义](#31-hpa-定义)
    - [3.2 HPA 配置](#32-hpa-配置)
    - [3.3 HPA 工作原理](#33-hpa-工作原理)
    - [3.4 HPA 指标类型](#34-hpa-指标类型)
  - [4 VPA（垂直自动伸缩）](#4-vpa垂直自动伸缩)
    - [4.1 VPA 定义](#41-vpa-定义)
    - [4.2 VPA 配置](#42-vpa-配置)
    - [4.3 VPA 工作原理](#43-vpa-工作原理)
    - [4.4 VPA 更新模式](#44-vpa-更新模式)
  - [5 Knative（Serverless 自动伸缩）](#5-knativeserverless-自动伸缩)
    - [5.1 Knative 定义](#51-knative-定义)
    - [5.2 Knative 配置](#52-knative-配置)
    - [5.3 Knative 工作原理](#53-knative-工作原理)
    - [5.4 Knative 伸缩策略](#54-knative-伸缩策略)
  - [6 Argo Rollouts（渐进式交付）](#6-argo-rollouts渐进式交付)
    - [6.1 Argo Rollouts 定义](#61-argo-rollouts-定义)
    - [6.2 金丝雀部署配置](#62-金丝雀部署配置)
    - [6.3 蓝绿部署配置](#63-蓝绿部署配置)
    - [6.4 Argo Rollouts 工作原理](#64-argo-rollouts-工作原理)
  - [7 弹性伸缩组合](#7-弹性伸缩组合)
    - [7.1 HPA + VPA](#71-hpa--vpa)
    - [7.2 HPA + Argo Rollouts](#72-hpa--argo-rollouts)
    - [7.3 Knative + Service Mesh](#73-knative--service-mesh)
  - [8 形式化定义](#8-形式化定义)
    - [8.1 弹性伸缩定义](#81-弹性伸缩定义)
    - [8.2 HPA 定义](#82-hpa-定义)
    - [8.3 VPA 定义](#83-vpa-定义)
  - [9 最佳实践](#9-最佳实践)
    - [9.1 HPA 最佳实践](#91-hpa-最佳实践)
    - [9.2 VPA 最佳实践](#92-vpa-最佳实践)
    - [9.3 Argo Rollouts 最佳实践](#93-argo-rollouts-最佳实践)
  - [10 总结](#10-总结)
    - [10.1 相关文档](#101-相关文档)

---

## 1 概述

本文档详细阐述**弹性伸缩**的实现方法，通过 **HPA、VPA、Knative、Argo Rollouts**
等技术实现自动横向扩缩和渐进式交付。

### 1.1 核心思想

> **通过自动弹性伸缩实现资源的动态分配，通过渐进式交付实现安全的部署和回滚**

## 2 弹性伸缩类型

### 2.1 弹性伸缩类型概览

| 类型              | 定义                             | 典型工具           | 适用场景 |
| ----------------- | -------------------------------- | ------------------ | -------- |
| **HPA**           | 水平自动伸缩：增加/减少 Pod 数量 | Kubernetes HPA     | 负载变化 |
| **VPA**           | 垂直自动伸缩：调整 Pod 资源      | Kubernetes VPA     | 资源优化 |
| **Knative**       | Serverless 自动伸缩              | Knative Autoscaler | 事件驱动 |
| **Argo Rollouts** | 渐进式交付：蓝绿/金丝雀部署      | Argo Rollouts      | 安全部署 |

### 2.2 弹性伸缩对比

| 类型              | 伸缩方向 | 伸缩粒度 | 响应时间 | 适用场景 |
| ----------------- | -------- | -------- | -------- | -------- |
| **HPA**           | 水平     | Pod 级别 | 秒级     | 负载变化 |
| **VPA**           | 垂直     | Pod 级别 | 分钟级   | 资源优化 |
| **Knative**       | 水平     | Pod 级别 | 秒级     | 事件驱动 |
| **Argo Rollouts** | 渐进     | 版本级别 | 分钟级   | 安全部署 |

## 3 HPA（水平自动伸缩）

### 3.1 HPA 定义

**HPA** 是水平自动伸缩，通过增加/减少 Pod 数量来应对负载变化。

### 3.2 HPA 配置

**HPA 配置示例**：

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### 3.3 HPA 工作原理

**HPA 工作流程**：

```text
1. 收集指标（Prometheus）
    ↓
2. 计算目标副本数
    ↓
3. 调整 Deployment 副本数
    ↓
4. Pod 自动创建/删除
```

### 3.4 HPA 指标类型

**HPA 指标类型**：

- **Resource**：CPU、内存使用率
- **Pod**：Pod 级别指标
- **Object**：对象级别指标
- **External**：外部指标

## 4 VPA（垂直自动伸缩）

### 4.1 VPA 定义

**VPA** 是垂直自动伸缩，通过调整 Pod 资源（CPU、内存）来优化资源使用。

### 4.2 VPA 配置

**VPA 配置示例**：

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: order-service-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
      - containerName: order-service
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 2
          memory: 2Gi
```

### 4.3 VPA 工作原理

**VPA 工作流程**：

```text
1. 收集历史资源使用数据
    ↓
2. 计算推荐资源值
    ↓
3. 调整 Pod 资源请求/限制
    ↓
4. Pod 重启应用新资源
```

### 4.4 VPA 更新模式

**VPA 更新模式**：

- **Auto**：自动更新 Pod 资源
- **Recreate**：重新创建 Pod 应用新资源
- **Off**：仅推荐，不自动更新

## 5 Knative（Serverless 自动伸缩）

### 5.1 Knative 定义

**Knative** 是 Serverless 平台，提供自动伸缩功能。

### 5.2 Knative 配置

**Knative Service 配置**：

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: order-service
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "10"
        autoscaling.knative.dev/target: "70"
    spec:
      containers:
        - image: order-service:latest
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
```

### 5.3 Knative 工作原理

**Knative 工作流程**：

```text
1. 请求到达（事件触发）
    ↓
2. 计算目标副本数（基于请求数）
    ↓
3. 自动扩容（从 0 到目标副本数）
    ↓
4. 请求处理
    ↓
5. 自动缩容（从目标副本数到 0）
```

### 5.4 Knative 伸缩策略

**Knative 伸缩策略**：

- **基于请求数**：根据请求数自动伸缩
- **基于并发数**：根据并发数自动伸缩
- **基于 CPU**：根据 CPU 使用率自动伸缩

## 6 Argo Rollouts（渐进式交付）

### 6.1 Argo Rollouts 定义

**Argo Rollouts** 是渐进式交付工具，支持蓝绿部署、金丝雀部署。

### 6.2 金丝雀部署配置

**金丝雀部署配置**：

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: order-service
spec:
  replicas: 5
  strategy:
    canary:
      steps:
        - setWeight: 10
        - pause: {}
        - setWeight: 20
        - pause: { duration: 10m }
        - setWeight: 40
        - pause: { duration: 10m }
        - setWeight: 60
        - pause: { duration: 10m }
        - setWeight: 80
        - pause: { duration: 10m }
      canaryService: order-service-canary
      stableService: order-service-stable
      trafficRouting:
        istio:
          virtualService:
            name: order-service-vs
            routes:
              - primary
```

### 6.3 蓝绿部署配置

**蓝绿部署配置**：

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: order-service
spec:
  replicas: 5
  strategy:
    blueGreen:
      activeService: order-service-active
      previewService: order-service-preview
      autoPromotionEnabled: false
      scaleDownDelaySeconds: 30
```

### 6.4 Argo Rollouts 工作原理

**Argo Rollouts 工作流程**：

```text
1. 创建新版本 Pod
    ↓
2. 逐步增加流量（金丝雀）
    ↓
3. 监控指标（Prometheus）
    ↓
4. 自动回滚（如果指标异常）
    ↓
5. 完成部署（如果指标正常）
```

## 7 弹性伸缩组合

### 7.1 HPA + VPA

**HPA + VPA 组合**：

```text
HPA: 水平伸缩（增加/减少 Pod）
    +
VPA: 垂直伸缩（调整 Pod 资源）
    =
优化资源使用 + 应对负载变化
```

### 7.2 HPA + Argo Rollouts

**HPA + Argo Rollouts 组合**：

```text
HPA: 自动伸缩（应对负载变化）
    +
Argo Rollouts: 渐进式交付（安全部署）
    =
自动伸缩 + 安全部署
```

### 7.3 Knative + Service Mesh

**Knative + Service Mesh 组合**：

```text
Knative: Serverless 自动伸缩
    +
Service Mesh: 流量治理
    =
Serverless + 流量治理
```

## 8 形式化定义

### 8.1 弹性伸缩定义

```text
弹性伸缩 A = ⟨type, metrics, policy, actions⟩
其中：
- type ∈ {HPA, VPA, Knative, ArgoRollouts}
- metrics: 指标集合
- policy: 伸缩策略
- actions: 伸缩动作集合
```

### 8.2 HPA 定义

```text
HPA = ⟨target, minReplicas, maxReplicas, metrics⟩
其中：
- target: 目标 Deployment/StatefulSet
- minReplicas: 最小副本数
- maxReplicas: 最大副本数
- metrics: 指标集合
```

### 8.3 VPA 定义

```text
VPA = ⟨target, updateMode, resourcePolicy⟩
其中：
- target: 目标 Deployment/StatefulSet
- updateMode: 更新模式（Auto/Recreate/Off）
- resourcePolicy: 资源策略
```

## 9 最佳实践

### 9.1 HPA 最佳实践

**HPA 最佳实践**：

- **合理设置指标**：使用 CPU、内存等核心指标
- **合理设置范围**：minReplicas 和 maxReplicas
- **监控伸缩行为**：监控 HPA 的伸缩行为

### 9.2 VPA 最佳实践

**VPA 最佳实践**：

- **合理设置资源范围**：minAllowed 和 maxAllowed
- **使用 Off 模式学习**：先使用 Off 模式学习资源使用
- **逐步启用 Auto 模式**：学习完成后启用 Auto 模式

### 9.3 Argo Rollouts 最佳实践

**Argo Rollouts 最佳实践**：

- **逐步增加流量**：从 10% 逐步增加到 100%
- **监控关键指标**：监控错误率、延迟等关键指标
- **自动回滚**：配置自动回滚策略

## 10 总结

通过**弹性伸缩**，我们实现了：

1. **自动横向扩缩**：通过 HPA 自动应对负载变化
2. **自动垂直扩缩**：通过 VPA 优化资源使用
3. **Serverless 自动伸缩**：通过 Knative 实现 Serverless 自动伸缩
4. **渐进式交付**：通过 Argo Rollouts 实现安全的部署和回滚
5. **组合使用**：HPA + VPA + Argo Rollouts 组合使用

### 10.1 相关文档

**扩展阅读**：

- **[eBPF/OTLP 架构视角](../09-multi-perspectives/07-ebpf-otlp-perspective.md)**
  ⭐ - 横纵耦合的可观测性驱动架构
  - **自动伸缩：从响应式到预测式的演进**（5.2 章节）
  - 细粒度指标驱动（Socket 队列积压、goroutine 阻塞数、JVM 老年代分配速率、TCP
    重传率）
  - 实时反馈控制回路（eBPF 采集 → OTLP Metrics → HPA 决策）
  - 智能容量规划（基于 eBPF 的记帐机制 + OTLP 成本关联模型）
- **[可观测性文档](../07-dynamic-operations/02-observability.md)** - 统一遥测与
  监控
- **[32. eBPF/OTLP 扩展技术分析](../../../TECHNICAL/32-ebpf-otlp-analysis/ebpf-otlp-analysis.md)**
  ⭐ - eBPF/OTLP 扩展技术分析文档

---

**更新时间**：2025-11-07 **版本**：v1.1 **参考**：`architecture_view.md` 第
1320-1330 行，弹性伸缩部分
