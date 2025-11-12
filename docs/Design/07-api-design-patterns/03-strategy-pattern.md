# 11.3 策略模式：多租户配额策略

> **文档版本**：v1.0 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [📑 目录](#-目录)
- [概述](#概述)
- [场景描述](#场景描述)
- [策略模式实现](#策略模式实现)
  - [策略模式：配额策略 CRD](#策略模式配额策略-crd)
- [策略实现矩阵](#策略实现矩阵)
- [关键技术分析](#关键技术分析)
  - [1 公平共享策略](#1-公平共享策略)
  - [2 优先级抢占策略](#2-优先级抢占策略)
  - [3 预留保证策略](#3-预留保证策略)
  - [4 动态超售策略](#4-动态超售策略)
- [相关文档](#相关文档)

---

## 概述

本文档分析策略模式在多租户配额策略中的应用，展示如何通过策略模式实现不同租户的资
源分配策略。

## 场景描述

**场景**：不同租户需要不同的资源分配策略（公平共享、优先级抢占、预留保证）。

**需求**：

1. **公平共享**：多租户平等使用资源
2. **优先级抢占**：关键业务优先使用资源
3. **预留保证**：SLA 保证的资源预留
4. **动态超售**：成本优化的资源超售

## 策略模式实现

### 策略模式：配额策略 CRD

```yaml
# 策略模式：配额策略CRD
apiVersion: quota.kubevirt.io/v1
kind: QuotaPolicy
metadata:
  name: tenant-a-policy
  namespace: tenant-a
spec:
  strategy: PriorityPreemption # 策略类型
  rules:
    - priority: 100 # 高优先级
      guaranteed:
        cpu: "10"
        memory: 20Gi
    - priority: 50 # 中优先级
      burstable:
        cpu: "20"
        memory: 40Gi
    - priority: 10 # 低优先级
      bestEffort:
        cpu: "40"
        memory: 80Gi
```

---

## 策略实现矩阵

| **策略类型**   | **适用场景**   | **API 设计**               | **性能影响**   |
| -------------- | -------------- | -------------------------- | -------------- |
| **公平共享**   | 多租户平等使用 | ResourceQuota 硬限制       | 无额外开销     |
| **优先级抢占** | 关键业务优先   | PriorityClass + Preemption | 调度延迟+5%    |
| **预留保证**   | SLA 保证       | ReservedQuota CRD          | 资源利用率-10% |
| **动态超售**   | 成本优化       | OvercommitRatio 配置       | 风险可控       |

---

## 关键技术分析

### 1. 公平共享策略

**适用场景**：多租户平等使用资源

**API 设计**：ResourceQuota 硬限制

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-a-quota
  namespace: tenant-a
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    count/pods: "20"
    count/virtualmachines.kubevirt.io: "5"
```

**性能影响**：无额外开销

- ResourceQuota 硬限制直接生效
- 无需额外的策略计算
- 性能开销最小

### 2. 优先级抢占策略

**适用场景**：关键业务优先使用资源

**API 设计**：PriorityClass + Preemption

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
preemptionPolicy: PreemptLowerPriority
---
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: critical-vm
spec:
  priorityClassName: high-priority
  template:
    spec:
      domain:
        resources:
          requests:
            memory: "2Gi"
            cpu: "2"
```

**性能影响**：调度延迟+5%

- PriorityClass 需要额外的调度计算
- Preemption 机制需要驱逐低优先级工作负载
- 调度延迟增加约 5%

### 3. 预留保证策略

**适用场景**：SLA 保证的资源预留

**API 设计**：ReservedQuota CRD

```yaml
apiVersion: quota.kubevirt.io/v1
kind: ReservedQuota
metadata:
  name: tenant-a-reserved
  namespace: tenant-a
spec:
  reserved:
    cpu: "5"
    memory: 10Gi
  guaranteed:
    cpu: "10"
    memory: 20Gi
```

**性能影响**：资源利用率-10%

- 预留资源无法被其他租户使用
- 资源利用率降低约 10%
- 但保证了 SLA 要求

### 4. 动态超售策略

**适用场景**：成本优化的资源超售

**API 设计**：OvercommitRatio 配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: overcommit-config
  namespace: kube-system
data:
  config.yaml: |
    overcommit:
      cpu: 2.0
      memory: 1.5
      enabled: true
```

**性能影响**：风险可控

- 超售比例可配置
- 风险可控，但需要监控资源使用情况
- 成本优化效果明显

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [声明式 API 设计模式](../07-api-design-patterns/01-declarative-api.md) - 声明
  式 API
- [适配器模式：统一异构运行时](../07-api-design-patterns/02-adapter-pattern.md) -
  适配器模式
- [观察者模式：统一事件通知](../07-api-design-patterns/04-observer-pattern.md) -
  观察者模式
- [多租户与配额同构](../02-isomorphic-functions/03-multi-tenant-quota.md) - 多租
  户配额同构分析

---

**最后更新**：2025-11-10 **维护者**：项目团队
