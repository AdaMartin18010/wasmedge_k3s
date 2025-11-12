# 11.1 声明式 API 设计模式

> **文档版本**：v1.0 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [📑 目录](#-目录)
- [概述](#概述)
- [核心原则](#核心原则)
  - [声明式 API 设计模式示例](#声明式-api-设计模式示例)
- [设计模式对比](#设计模式对比)
- [关键技术分析](#关键技术分析)
  - [1 声明式设计](#1-声明式设计)
  - [2 命令式设计](#2-命令式设计)
  - [3 控制器模式](#3-控制器模式)
  - [4 状态机](#4-状态机)
  - [5 事件驱动](#5-事件驱动)
- [相关文档](#相关文档)

---

## 概述

本文档深入解析声明式 API 设计模式，展示如何通过期望状态（Spec）与实际状态
（Status）分离实现声明式 API 设计。

## 核心原则

**核心原则**：期望状态（Spec）与实际状态（Status）分离，控制器负责调谐
（Reconcile）。

### 声明式 API 设计模式示例

```yaml
# 声明式API设计模式
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: web-server-vm
spec: # 期望状态
  running: true
  template:
    spec:
      domain:
        resources:
          requests:
            memory: "2Gi"
            cpu: "2"
status: # 实际状态（只读，由控制器更新）
  phase: Running
  conditions:
    - type: Ready
      status: "True"
      lastProbeTime: "2025-11-07T10:00:00Z"
```

---

## 设计模式对比

| **模式**       | **容器实现**          | **虚拟机实现**     | **API 一致性**          |
| -------------- | --------------------- | ------------------ | ----------------------- |
| **声明式**     | Pod Spec/Status       | VM Spec/Status     | 完全一致                |
| **命令式**     | kubectl create/apply  | virtctl start/stop | CLI 工具统一            |
| **控制器模式** | ReplicaSet Controller | VMIRS Controller   | 相同的 Reconcile 循环   |
| **状态机**     | Pod Phase             | VMI Phase          | 状态语义对齐            |
| **事件驱动**   | Watch API             | Watch API          | 完全复用 K8s Watch 机制 |

---

## 关键技术分析

### 1. 声明式设计

**容器实现**：Pod Spec/Status

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec: # 期望状态
  containers:
    - name: test
      image: nginx:alpine
status: # 实际状态（只读）
  phase: Running
  conditions:
    - type: Ready
      status: "True"
```

**虚拟机实现**：VM Spec/Status

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: test-vm
spec: # 期望状态
  running: true
  template:
    spec:
      domain:
        resources:
          requests:
            memory: "1Gi"
            cpu: "1"
status: # 实际状态（只读）
  phase: Running
  conditions:
    - type: Ready
      status: "True"
```

**API 一致性**：完全一致

- 容器和虚拟机都使用 Spec/Status 分离设计
- 期望状态（Spec）由用户定义
- 实际状态（Status）由控制器更新

### 2. 命令式设计

**容器实现**：kubectl create/apply

```bash
# 创建 Pod
kubectl create -f pod.yaml

# 更新 Pod
kubectl apply -f pod.yaml
```

**虚拟机实现**：virtctl start/stop

```bash
# 启动虚拟机
virtctl start test-vm

# 停止虚拟机
virtctl stop test-vm
```

**CLI 工具统一**：

- kubectl 统一管理容器和虚拟机资源
- virtctl 提供虚拟机特有的操作
- CLI 工具统一，降低学习成本

### 3. 控制器模式

**容器实现**：ReplicaSet Controller

```go
// ReplicaSet Controller 循环
func (c *ReplicaSetController) sync(key string) error {
    // 1. 获取期望状态
    desired := c.getDesiredState(key)

    // 2. 获取实际状态
    actual := c.getActualState(key)

    // 3. 计算差异
    delta := c.computeDelta(desired, actual)

    // 4. 执行调谐
    return c.reconcile(delta)
}
```

**虚拟机实现**：VMIRS Controller

```go
// VMIRS Controller 循环
func (c *VMIRSController) sync(key string) error {
    // 1. 获取期望状态
    desired := c.getDesiredState(key)

    // 2. 获取实际状态
    actual := c.getActualState(key)

    // 3. 计算差异
    delta := c.computeDelta(desired, actual)

    // 4. 执行调谐
    return c.reconcile(delta)
}
```

**相同的 Reconcile 循环**：

- 容器和虚拟机控制器都使用相同的 Reconcile 循环
- 期望状态与实际状态分离
- 控制器负责调谐，实现期望状态

### 4. 状态机

**容器实现**：Pod Phase

```yaml
apiVersion: v1
kind: Pod
status:
  phase: Running
  # Pod Phase: Pending, Running, Succeeded, Failed, Unknown
```

**虚拟机实现**：VMI Phase

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
status:
  phase: Running
  # VMI Phase: Pending, Scheduling, Scheduled, Running, Succeeded, Failed, Unknown
```

**状态语义对齐**：

- Pod Phase 和 VMI Phase 状态语义对齐
- 状态机设计统一，降低理解成本
- 状态转换逻辑一致

### 5. 事件驱动

**容器实现**：Watch API

```go
// Watch Pod 变化
watcher, err := client.CoreV1().Pods(namespace).Watch(ctx, metav1.ListOptions{})
for event := range watcher.ResultChan() {
    switch event.Type {
    case watch.Added:
        c.OnAdd(event.Object)
    case watch.Modified:
        c.OnUpdate(event.Object)
    case watch.Deleted:
        c.OnDelete(event.Object)
    }
}
```

**虚拟机实现**：Watch API

```go
// Watch VirtualMachine 变化
watcher, err := client.KubevirtV1().VirtualMachines(namespace).Watch(ctx, metav1.ListOptions{})
for event := range watcher.ResultChan() {
    switch event.Type {
    case watch.Added:
        c.OnAdd(event.Object)
    case watch.Modified:
        c.OnUpdate(event.Object)
    case watch.Deleted:
        c.OnDelete(event.Object)
    }
}
```

**完全复用 K8s Watch 机制**：

- 容器和虚拟机都使用 Kubernetes Watch API
- 事件驱动机制统一，降低实现复杂度
- Watch API 提供实时事件通知

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [适配器模式：统一异构运行时](../07-api-design-patterns/02-adapter-pattern.md) -
  适配器模式
- [策略模式：多租户配额策略](../07-api-design-patterns/03-strategy-pattern.md) -
  策略模式
- [观察者模式：统一事件通知](../07-api-design-patterns/04-observer-pattern.md) -
  观察者模式

---

**最后更新**：2025-11-10 **维护者**：项目团队
