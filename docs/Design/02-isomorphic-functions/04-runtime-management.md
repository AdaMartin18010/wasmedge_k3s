# 4. 运行时管理同构

> **文档版本**：v1.0 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [📑 目录](#-目录)
- [概述](#概述)
- [运行时管理同构矩阵](#运行时管理同构矩阵)
- [关键设计](#关键设计)
  - [关键设计要点](#关键设计要点)
- [关键技术分析](#关键技术分析)
  - [1. 创建操作](#1-创建操作)
  - [2. 启动操作](#2-启动操作)
  - [3. 停止操作](#3-停止操作)
  - [4. 暂停操作](#4-暂停操作)
  - [5. 重启操作](#5-重启操作)
  - [6. 删除操作](#6-删除操作)
  - [7. 迁移操作](#7-迁移操作)
  - [8. 扩缩容操作](#8-扩缩容操作)
- [相关文档](#相关文档)

---

## 概述

本文档分析虚拟化容器化集群管理 API 中运行时管理的同构性设计，对比容器和虚拟机在
运行时管理上的统一性和差异性。

## 运行时管理同构矩阵

| **操作**   | **容器 API** | **虚拟机 API**        | **状态机对齐**            |
| ---------- | ------------ | --------------------- | ------------------------- |
| **创建**   | POST /pods   | POST /virtualmachines | Pending→Running           |
| **启动**   | N/A          | virtctl start         | Stopped→Running           |
| **停止**   | DELETE /pods | virtctl stop          | Running→Stopped           |
| **暂停**   | N/A          | virtctl pause         | Running→Paused            |
| **重启**   | Pod 重建     | virtctl restart       | 状态重置                  |
| **删除**   | DELETE       | DELETE                | 级联删除                  |
| **迁移**   | N/A          | Migration CRD         | Running→Migrating→Running |
| **扩缩容** | HPA/Scale    | VMIRS/Scale           | 副本数调整                |

---

## 关键设计

虚拟机生命周期通过 `VirtualMachineInstance (VMI)` CRD 表达，与 Pod 生命周期状态
机保持映射关系，`virt-launcher` Pod 作为 VMI 的 1:1 载体，实现 kubelet 统一调度
。

### 关键设计要点

1. **状态机对齐**：VMI 状态机与 Pod 状态机保持映射关系
2. **Pod 映射**：每个 VMI 对应一个 virt-launcher Pod，实现 1:1 映射
3. **统一调度**：kubelet 统一调度容器和虚拟机
4. **生命周期管理**：通过 CRD 统一管理容器和虚拟机的生命周期

---

## 关键技术分析

### 1. 创建操作

**容器实现**：POST /pods

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test
      image: nginx:alpine
```

**虚拟机实现**：POST /virtualmachines

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: test-vm
spec:
  running: true
  template:
    spec:
      domain:
        resources:
          requests:
            memory: "1Gi"
            cpu: "1"
```

**状态机对齐**：Pending→Running

- 容器创建后进入 Pending 状态，然后进入 Running 状态
- 虚拟机创建后进入 Pending 状态，然后进入 Running 状态
- 状态机对齐确保容器和虚拟机的生命周期管理一致性

### 2. 启动操作

**容器实现**：N/A（容器创建后自动启动）

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test
      image: nginx:alpine
      # 容器创建后自动启动
```

**虚拟机实现**：virtctl start

```bash
# 启动虚拟机
virtctl start test-vm
```

**状态机对齐**：Stopped→Running

- 容器创建后自动启动，无需单独启动操作
- 虚拟机可以处于 Stopped 状态，需要 virtctl start 启动
- 启动后虚拟机进入 Running 状态

### 3. 停止操作

**容器实现**：DELETE /pods

```bash
# 删除 Pod（停止容器）
kubectl delete pod test-pod
```

**虚拟机实现**：virtctl stop

```bash
# 停止虚拟机
virtctl stop test-vm
```

**状态机对齐**：Running→Stopped

- 容器删除后立即停止，无法恢复
- 虚拟机停止后进入 Stopped 状态，可以重新启动
- 停止操作确保容器和虚拟机的生命周期管理一致性

### 4. 暂停操作

**容器实现**：N/A（容器不支持暂停操作）

```yaml
# 容器不支持暂停操作
# 只能通过删除 Pod 停止容器
```

**虚拟机实现**：virtctl pause

```bash
# 暂停虚拟机
virtctl pause test-vm
```

**状态机对齐**：Running→Paused

- 容器不支持暂停操作，只能删除 Pod
- 虚拟机支持暂停操作，进入 Paused 状态
- 暂停操作是虚拟机的特有功能

### 5. 重启操作

**容器实现**：Pod 重建

```bash
# 重启容器（删除并重新创建 Pod）
kubectl delete pod test-pod
kubectl create -f test-pod.yaml
```

**虚拟机实现**：virtctl restart

```bash
# 重启虚拟机
virtctl restart test-vm
```

**状态机对齐**：状态重置

- 容器重启需要删除并重新创建 Pod
- 虚拟机重启通过 virtctl restart 实现
- 重启操作确保容器和虚拟机的生命周期管理一致性

### 6. 删除操作

**容器实现**：DELETE

```bash
# 删除 Pod
kubectl delete pod test-pod
```

**虚拟机实现**：DELETE

```bash
# 删除虚拟机
kubectl delete virtualmachine test-vm
```

**状态机对齐**：级联删除

- 容器删除后立即停止，无法恢复
- 虚拟机删除后级联删除 VMI 和 virt-launcher Pod
- 删除操作确保容器和虚拟机的生命周期管理一致性

### 7. 迁移操作

**容器实现**：N/A（容器不支持迁移操作）

```yaml
# 容器不支持迁移操作
# 只能通过删除并重新创建 Pod 实现迁移
```

**虚拟机实现**：Migration CRD

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstanceMigration
metadata:
  name: test-vm-migration
spec:
  vmiName: test-vm
```

**状态机对齐**：Running→Migrating→Running

- 容器不支持迁移操作，只能删除并重新创建 Pod
- 虚拟机支持实时迁移，通过 Migration CRD 实现
- 迁移操作是虚拟机的特有功能

### 8. 扩缩容操作

**容器实现**：HPA/Scale

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: test-hpa
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
```

**虚拟机实现**：VMIRS/Scale

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

**状态机对齐**：副本数调整

- 容器通过 HPA 实现自动扩缩容
- 虚拟机通过 VMIRS 实现手动扩缩容
- 扩缩容操作确保容器和虚拟机的生命周期管理一致性

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [网络功能同构矩阵](../02-isomorphic-functions/01-network-isomorphism.md) - 网
  络功能同构分析
- [存储功能同构矩阵](../02-isomorphic-functions/02-storage-isomorphism.md) - 存
  储功能同构分析
- [多租户与配额同构](../02-isomorphic-functions/03-multi-tenant-quota.md) - 多租
  户配额同构分析

---

**最后更新**：2025-11-10 **维护者**：项目团队
