# 2. 存储功能同构矩阵

> **文档版本**：v1.0 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [📑 目录](#-目录)
- [概述](#概述)
- [存储功能同构矩阵](#存储功能同构矩阵)
- [架构特点](#架构特点)
  - [关键设计要点](#关键设计要点)
- [关键技术分析](#关键技术分析)
  - [1 持久化存储](#1-持久化存储)
  - [2 块存储](#2-块存储)
  - [3 镜像管理](#3-镜像管理)
  - [4 动态供应](#4-动态供应)
  - [5 快照克隆](#5-快照克隆)
  - [6 热插拔](#6-热插拔)
  - [7 数据导入](#7-数据导入)
- [相关文档](#相关文档)

---

## 概述

本文档分析虚拟化容器化集群管理 API 中存储功能的同构性设计，对比容器和虚拟机在存
储功能实现上的统一性和差异性。

## 存储功能同构矩阵

| **能力**       | **容器实现**    | **虚拟机实现**    | **API 统一性**      | **关键技术**      |
| -------------- | --------------- | ----------------- | ------------------- | ----------------- |
| **持久化存储** | PVC             | DataVolume        | DataVolume 封装 PVC | CSI 标准          |
| **块存储**     | Block PV        | 虚拟机磁盘        | 统一块设备          | VolumeMode: Block |
| **镜像管理**   | Container Image | VMImage           | CDI 导入器          | QCOW2/ISO 格式    |
| **动态供应**   | StorageClass    | 复用 StorageClass | 完全一致            | CSI Provisioner   |
| **快照克隆**   | VolumeSnapshot  | VM 快照           | CRD 扩展            | 存储驱动支持      |
| **热插拔**     | Volume 挂载     | 磁盘热插拔        | 类似操作            | libvirt 支持      |
| **数据导入**   | 镜像拉取        | CDI 导入          | 异步处理            | CDI Controller    |

---

## 架构特点

`Containerized Data Importer (CDI)` 项目将虚拟机磁盘作为特殊容器镜像处理，通过
`DataVolume` CRD 统一容器和虚拟机的数据管理接口。

### 关键设计要点

1. **CDI 统一数据管理**：通过 CDI 项目统一管理容器和虚拟机的数据导入
2. **DataVolume 封装 PVC**：DataVolume CRD 封装 PVC，提供统一的数据管理接口
3. **CSI 标准复用**：容器和虚拟机都使用 CSI 标准进行存储管理
4. **异步处理机制**：数据导入通过 CDI Controller 异步处理

---

## 关键技术分析

### 1. 持久化存储

**容器实现**：PVC

```yaml
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

**虚拟机实现**：DataVolume

```yaml
apiVersion: cdi.kubevirt.io/v1beta1
kind: DataVolume
metadata:
  name: test-dv
spec:
  source:
    pvc:
      name: source-pvc
      namespace: default
  pvc:
    accessModes:
      - ReadWriteOnce
    storageClassName: fast-ssd
    resources:
      requests:
        storage: 10Gi
```

**API 统一性**：DataVolume 封装 PVC

- DataVolume CRD 封装 PVC，提供统一的数据管理接口
- 容器和虚拟机都使用 CSI 标准进行存储管理
- 存储配置通过 CRD 统一描述

### 2. 块存储

**容器实现**：Block PV

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: block-pvc
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Block
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 10Gi
```

**虚拟机实现**：虚拟机磁盘

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    devices:
      disks:
        - name: datavolumedisk1
          disk:
            bus: virtio
          volumeName: datavolumedisk1
    volumes:
      - name: datavolumedisk1
        persistentVolumeClaim:
          claimName: block-pvc
```

**API 统一性**：统一块设备

- 容器和虚拟机都使用 Block PV 模式
- VolumeMode: Block 统一块设备管理
- 块设备通过 CSI 驱动统一管理

### 3. 镜像管理

**容器实现**：Container Image

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

**虚拟机实现**：VMImage

```yaml
apiVersion: cdi.kubevirt.io/v1beta1
kind: DataVolume
metadata:
  name: test-dv
spec:
  source:
    registry:
      url: docker://registry.example.com/vm-images/ubuntu:22.04
  pvc:
    accessModes:
      - ReadWriteOnce
    storageClassName: fast-ssd
    resources:
      requests:
        storage: 10Gi
```

**API 统一性**：CDI 导入器

- CDI 导入器统一管理容器镜像和虚拟机镜像
- QCOW2/ISO 格式通过 CDI 导入器处理
- 镜像管理通过 DataVolume CRD 统一描述

### 4. 动态供应

**容器实现**：StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: csi.example.com
parameters:
  type: ssd
  replication: "3"
```

**虚拟机实现**：复用 StorageClass

```yaml
apiVersion: cdi.kubevirt.io/v1beta1
kind: DataVolume
metadata:
  name: test-dv
spec:
  pvc:
    storageClassName: fast-ssd
    resources:
      requests:
        storage: 10Gi
```

**API 统一性**：完全一致

- 容器和虚拟机都使用 StorageClass 进行动态供应
- CSI Provisioner 统一处理存储动态供应
- 存储配置通过 StorageClass 统一描述

### 5. 快照克隆

**容器实现**：VolumeSnapshot

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: test-snapshot
spec:
  source:
    persistentVolumeClaimName: test-pvc
```

**虚拟机实现**：VM 快照

```yaml
apiVersion: snapshot.kubevirt.io/v1alpha1
kind: VirtualMachineSnapshot
metadata:
  name: test-vm-snapshot
spec:
  source:
    apiGroup: kubevirt.io
    kind: VirtualMachine
    name: test-vm
```

**API 统一性**：CRD 扩展

- 容器使用 VolumeSnapshot CRD 进行快照管理
- 虚拟机使用 VirtualMachineSnapshot CRD 进行快照管理
- 快照功能通过 CRD 扩展实现

### 6. 热插拔

**容器实现**：Volume 挂载

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test
      image: nginx:alpine
      volumeMounts:
        - name: data
          mountPath: /data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: test-pvc
```

**虚拟机实现**：磁盘热插拔

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    devices:
      disks:
        - name: datavolumedisk1
          disk:
            bus: virtio
          volumeName: datavolumedisk1
    volumes:
      - name: datavolumedisk1
        persistentVolumeClaim:
          claimName: test-pvc
```

**API 统一性**：类似操作

- 容器通过 Volume 挂载实现存储热插拔
- 虚拟机通过磁盘热插拔实现存储热插拔
- libvirt 支持虚拟机磁盘热插拔

### 7. 数据导入

**容器实现**：镜像拉取

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test
      image: nginx:alpine
      # 镜像拉取由 kubelet 自动处理
```

**虚拟机实现**：CDI 导入

```yaml
apiVersion: cdi.kubevirt.io/v1beta1
kind: DataVolume
metadata:
  name: test-dv
spec:
  source:
    http:
      url: https://example.com/vm-images/ubuntu.qcow2
  pvc:
    accessModes:
      - ReadWriteOnce
    storageClassName: fast-ssd
    resources:
      requests:
        storage: 10Gi
```

**API 统一性**：异步处理

- 容器镜像拉取由 kubelet 自动处理
- 虚拟机数据导入由 CDI Controller 异步处理
- 数据导入通过 DataVolume CRD 统一描述

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [网络功能同构矩阵](../02-isomorphic-functions/01-network-isomorphism.md) - 网
  络功能同构分析
- [多租户与配额同构](../02-isomorphic-functions/03-multi-tenant-quota.md) - 多租
  户配额同构分析
- [运行时管理同构](../02-isomorphic-functions/04-runtime-management.md) - 运行时
  管理同构分析

---

**最后更新**：2025-11-10 **维护者**：项目团队
