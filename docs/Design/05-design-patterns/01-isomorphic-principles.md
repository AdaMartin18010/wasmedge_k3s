# 7.1 同构设计原则

> **文档版本**：v1.0 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [📑 目录](#-目录)
- [概述](#概述)
- [同构设计原则](#同构设计原则)
  - [1 CRD 扩展优先](#1-crd-扩展优先)
  - [2 控制器模式复用](#2-控制器模式复用)
  - [3 资源模型对齐](#3-资源模型对齐)
  - [4 调度器复用](#4-调度器复用)
  - [5 网络存储共享](#5-网络存储共享)
  - [6 运维工具统一](#6-运维工具统一)
- [关键技术分析](#关键技术分析)
  - [1 CRD 扩展机制](#1-crd-扩展机制)
  - [2 控制器模式](#2-控制器模式)
  - [3 资源模型对齐](#3-资源模型对齐-1)
- [相关文档](#相关文档)

---

## 概述

本文档总结虚拟化容器化集群管理 API 中的同构设计原则，展示如何通过统一的设计模式
实现容器和虚拟机的统一管理。

## 同构设计原则

### 1. CRD 扩展优先

**原则**：所有虚拟化功能通过 CRD 表达，不修改 Kubernetes 核心

**实现方式**：

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: virtualmachines.kubevirt.io
spec:
  group: kubevirt.io
  versions:
    - name: v1
      served: true
      storage: true
  scope: Namespaced
  names:
    plural: virtualmachines
    singular: virtualmachine
    kind: VirtualMachine
```

**说明**：

- 所有虚拟化功能通过 CRD 扩展实现
- 不修改 Kubernetes 核心代码
- 保持与 Kubernetes 原生 API 的兼容性

### 2. 控制器模式复用

**原则**：遵循声明式 API 和控制器循环模式

**实现方式**：

```go
// 控制器循环模式
func (c *Controller) sync(key string) error {
    // 1. 获取期望状态（Spec）
    desired, err := c.getDesiredState(key)
    if err != nil {
        return err
    }

    // 2. 获取实际状态（Status）
    actual, err := c.getActualState(key)
    if err != nil {
        return err
    }

    // 3. 计算差异（Delta）
    delta := c.computeDelta(desired, actual)

    // 4. 执行调谐（Reconcile）
    return c.reconcile(delta)
}
```

**说明**：

- 所有控制器都遵循声明式 API 和控制器循环模式
- 期望状态（Spec）与实际状态（Status）分离
- 控制器负责调谐（Reconcile），实现期望状态

### 3. 资源模型对齐

**原则**：VMI ↔ Pod, DataVolume ↔ PVC, VMIRS ↔ ReplicaSet

**实现方式**：

```yaml
# Pod 资源模型
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test
      image: nginx:alpine

# VMI 资源模型（对齐 Pod）
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    resources:
      requests:
        memory: "1Gi"
        cpu: "1"
```

**说明**：

- VMI 资源模型与 Pod 资源模型对齐
- DataVolume 资源模型与 PVC 资源模型对齐
- VMIRS 资源模型与 ReplicaSet 资源模型对齐

### 4. 调度器复用

**原则**：kube-scheduler 统一调度，通过预选/优选策略区分负载

**实现方式**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  schedulerName: default-scheduler
  containers:
    - name: test
      image: nginx:alpine

# VMI 通过 virt-launcher Pod 复用调度器
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  # VMI 通过 virt-launcher Pod 复用 kube-scheduler
  domain:
    resources:
      requests:
        memory: "1Gi"
        cpu: "1"
```

**说明**：

- kube-scheduler 统一调度容器和虚拟机
- 通过预选/优选策略区分容器和虚拟机负载
- 调度器复用，无需单独实现虚拟机调度器

### 5. 网络存储共享

**原则**：完全复用 CNI/CSI 生态，避免重复建设

**实现方式**：

```yaml
# 网络：复用 CNI 生态
apiVersion: k8s.cni.cncf.io/v1
kind: NetworkAttachmentDefinition
metadata:
  name: macvlan-conf
spec:
  config: |
    {
      "cniVersion": "0.3.1",
      "type": "macvlan",
      "master": "eth0",
      "mode": "bridge",
      "ipam": {
        "type": "host-local",
        "subnet": "10.56.0.0/16"
      }
    }

# 存储：复用 CSI 生态
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 10Gi
```

**说明**：

- 完全复用 CNI 生态，虚拟机通过 Multus 复用 CNI 插件
- 完全复用 CSI 生态，虚拟机通过 DataVolume 复用 CSI 驱动
- 网络存储共享，避免重复建设

### 6. 运维工具统一

**原则**：kubectl + virtctl 作为统一 CLI 入口

**实现方式**：

```bash
# 容器管理：kubectl
kubectl get pods
kubectl create -f pod.yaml
kubectl delete pod test-pod

# 虚拟机管理：virtctl
virtctl start test-vm
virtctl stop test-vm
virtctl pause test-vm
virtctl restart test-vm

# 统一管理：kubectl
kubectl get virtualmachines
kubectl create -f vm.yaml
kubectl delete virtualmachine test-vm
```

**说明**：

- kubectl 统一管理容器和虚拟机资源
- virtctl 提供虚拟机特有的操作（启动、停止、暂停、重启）
- 运维工具统一，降低学习成本

---

## 关键技术分析

### 1. CRD 扩展机制

**优势**：

- 不修改 Kubernetes 核心代码
- 保持与 Kubernetes 原生 API 的兼容性
- 支持版本升级和向后兼容

**实现**：

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: virtualmachines.kubevirt.io
spec:
  group: kubevirt.io
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                running:
                  type: boolean
            status:
              type: object
              properties:
                phase:
                  type: string
  scope: Namespaced
  names:
    plural: virtualmachines
    singular: virtualmachine
    kind: VirtualMachine
```

### 2. 控制器模式

**优势**：

- 声明式 API 设计，易于理解和使用
- 控制器循环模式，自动调谐期望状态
- 支持事件驱动和定时同步

**实现**：

```go
// 控制器接口
type Controller interface {
    // 同步资源
    Sync(key string) error

    // 处理事件
    OnAdd(obj interface{})
    OnUpdate(oldObj, newObj interface{})
    OnDelete(obj interface{})
}

// 控制器实现
type VirtualMachineController struct {
    client    kubernetes.Interface
    informer  cache.SharedInformer
    workqueue workqueue.RateLimitingInterface
}

func (c *VirtualMachineController) Sync(key string) error {
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

### 3. 资源模型对齐

**优势**：

- 资源模型对齐，降低学习成本
- 统一资源抽象，简化管理复杂度
- 支持资源转换和映射

**实现**：

```yaml
# Pod 资源模型
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test
      image: nginx:alpine
      resources:
        requests:
          memory: "1Gi"
          cpu: "1"
        limits:
          memory: "2Gi"
          cpu: "2"

# VMI 资源模型（对齐 Pod）
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    resources:
      requests:
        memory: "1Gi"
        cpu: "1"
      limits:
        memory: "2Gi"
        cpu: "2"
```

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [异构补偿机制](../05-design-patterns/02-heterogeneous-compensation.md) - 异构
  补偿机制
- [监控指标统一采集](../04-operations-monitoring/01-unified-monitoring.md) - 监
  控指标采集

---

**最后更新**：2025-11-10 **维护者**：项目团队
