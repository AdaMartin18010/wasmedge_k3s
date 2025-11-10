# 1. 扩缩容机制对比

> **文档版本**：v1.0 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [📑 目录](#-目录)
- [概述](#概述)
- [扩缩容机制对比矩阵](#扩缩容机制对比矩阵)
- [实现方式](#实现方式)
  - [容器 HPA 实现](#容器-hpa-实现)
  - [虚拟机 VMIRS 实现](#虚拟机-vmirs-实现)
- [关键技术分析](#关键技术分析)
  - [1. 指标源](#1-指标源)
  - [2. 触发器](#2-触发器)
  - [3. 缩放对象](#3-缩放对象)
  - [4. 缩放策略](#4-缩放策略)
  - [5. 最小副本](#5-最小副本)
- [相关文档](#相关文档)

---

## 概述

本文档对比容器和虚拟机在扩缩容机制上的统一性和差异性，分析 HPA 和 VMIRS 的实现方
式和设计要点。

## 扩缩容机制对比矩阵

| **维度**     | **容器 HPA**           | **虚拟机 VMIRS**            | **同构程度** |
| ------------ | ---------------------- | --------------------------- | ------------ |
| **指标源**   | metrics-server         | metrics-server+GuestOS 指标 | 部分扩展     |
| **触发器**   | CPU/内存/自定义        | CPU/内存/业务指标           | 基本一致     |
| **缩放对象** | Deployment/StatefulSet | VirtualMachine              | 类似模式     |
| **缩放策略** | 快速启停               | 冷启动/热添加               | 性能差异     |
| **最小副本** | 0（serverless）        | 0（stopped 状态）           | 语义对齐     |

---

## 实现方式

### 容器 HPA 实现

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: container-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: test-deployment
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

### 虚拟机 VMIRS 实现

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: vm-hpa
spec:
  scaleTargetRef:
    apiVersion: kubevirt.io/v1
    kind: VirtualMachineInstanceReplicaSet
    name: test-vmirs
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

---

## 关键技术分析

### 1. 指标源

**容器实现**：metrics-server

```yaml
apiVersion: v1
kind: Service
metadata:
  name: metrics-server
  namespace: kube-system
spec:
  selector:
    k8s-app: metrics-server
  ports:
    - port: 443
      targetPort: 4443
```

**虚拟机实现**：metrics-server+GuestOS 指标

```yaml
apiVersion: v1
kind: Service
metadata:
  name: metrics-server
  namespace: kube-system
spec:
  selector:
    k8s-app: metrics-server
  ports:
    - port: 443
      targetPort: 4443
---
apiVersion: v1
kind: Service
metadata:
  name: guest-metrics
  namespace: kube-system
spec:
  selector:
    k8s-app: guest-metrics
  ports:
    - port: 8080
      targetPort: 8080
```

**同构程度**：部分扩展

- 容器使用 metrics-server 采集 Pod 指标
- 虚拟机使用 metrics-server 采集 virt-launcher Pod 指标，同时通过 Guest Agent 采
  集 GuestOS 指标
- 指标源部分扩展，支持 GuestOS 指标采集

### 2. 触发器

**容器实现**：CPU/内存/自定义

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: container-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: test-deployment
  minReplicas: 1
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
    - type: Pods
      pods:
        metric:
          name: custom-metric
        target:
          type: AverageValue
          averageValue: "100"
```

**虚拟机实现**：CPU/内存/业务指标

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vm-hpa
spec:
  scaleTargetRef:
    apiVersion: kubevirt.io/v1
    kind: VirtualMachineInstanceReplicaSet
    name: test-vmirs
  minReplicas: 1
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
    - type: Pods
      pods:
        metric:
          name: guest-metric
        target:
          type: AverageValue
          averageValue: "100"
```

**同构程度**：基本一致

- 容器和虚拟机都支持 CPU/内存/自定义指标触发扩缩容
- 虚拟机通过 Guest Agent 采集业务指标，支持更细粒度的扩缩容控制
- 触发器基本一致，支持多种指标类型

### 3. 缩放对象

**容器实现**：Deployment/StatefulSet

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: test
  template:
    metadata:
      labels:
        app: test
    spec:
      containers:
        - name: test
          image: nginx:alpine
```

**虚拟机实现**：VirtualMachine

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstanceReplicaSet
metadata:
  name: test-vmirs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: test
  template:
    metadata:
      labels:
        app: test
    spec:
      domain:
        resources:
          requests:
            memory: "1Gi"
            cpu: "1"
```

**同构程度**：类似模式

- 容器使用 Deployment/StatefulSet 管理副本
- 虚拟机使用 VirtualMachineInstanceReplicaSet 管理副本
- 缩放对象类似，都支持副本管理

### 4. 缩放策略

**容器实现**：快速启停

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: container-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: test-deployment
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
```

**虚拟机实现**：冷启动/热添加

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vm-hpa
spec:
  scaleTargetRef:
    apiVersion: kubevirt.io/v1
    kind: VirtualMachineInstanceReplicaSet
    name: test-vmirs
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 600
      policies:
        - type: Percent
          value: 25
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
        - type: Pods
          value: 2
          periodSeconds: 60
      selectPolicy: Max
```

**同构程度**：性能差异

- 容器启动速度快，支持快速启停策略
- 虚拟机启动速度慢，需要更长的稳定窗口和更保守的缩放策略
- 缩放策略需要考虑性能差异，虚拟机需要更保守的策略

### 5. 最小副本

**容器实现**：0（serverless）

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: container-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: test-deployment
  minReplicas: 0
  maxReplicas: 10
```

**虚拟机实现**：0（stopped 状态）

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vm-hpa
spec:
  scaleTargetRef:
    apiVersion: kubevirt.io/v1
    kind: VirtualMachineInstanceReplicaSet
    name: test-vmirs
  minReplicas: 0
  maxReplicas: 10
```

**同构程度**：语义对齐

- 容器支持最小副本为 0，实现 serverless 模式
- 虚拟机支持最小副本为 0，虚拟机处于 stopped 状态
- 最小副本语义对齐，都支持缩放到 0

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [负载均衡统一架构](../03-dynamic-management/02-load-balancing.md) - 负载均衡架
  构
- [实时迁移功能扩展](../03-dynamic-management/03-live-migration.md) - 实时迁移功
  能

---

**最后更新**：2025-11-10 **维护者**：项目团队
