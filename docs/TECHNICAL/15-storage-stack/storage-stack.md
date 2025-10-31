# 24. 存储技术规格堆栈：全面梳理

## 目录

- [目录](#目录)
- [24.1 文档定位](#241-文档定位)
- [24.2 存储技术栈全景](#242-存储技术栈全景)
  - [24.2.1 存储层次结构](#2421-存储层次结构)
  - [24.2.2 技术组件矩阵](#2422-技术组件矩阵)
  - [24.2.3 技术栈组合](#2423-技术栈组合)
- [24.3 CSI 插件技术规格](#243-csi-插件技术规格)
  - [24.3.1 CSI 规范](#2431-csi-规范)
  - [24.3.2 NFS CSI 规格](#2432-nfs-csi-规格)
  - [24.3.3 Ceph CSI 规格](#2433-ceph-csi-规格)
  - [24.3.4 Longhorn CSI 规格](#2434-longhorn-csi-规格)
  - [24.3.5 本地存储 CSI 规格](#2435-本地存储-csi-规格)
  - [24.3.6 云存储 CSI 规格](#2436-云存储-csi-规格)
  - [24.3.7 CSI 插件对比](#2437-csi-插件对比)
- [24.4 存储类型技术规格](#244-存储类型技术规格)
  - [24.4.1 块存储规格](#2441-块存储规格)
  - [24.4.2 文件存储规格](#2442-文件存储规格)
  - [24.4.3 对象存储规格](#2443-对象存储规格)
  - [24.4.4 存储类型对比](#2444-存储类型对比)
- [24.5 PV/PVC 技术规格](#245-pvpvc-技术规格)
  - [24.5.1 PersistentVolume 规格](#2451-persistentvolume-规格)
  - [24.5.2 PersistentVolumeClaim 规格](#2452-persistentvolumeclaim-规格)
  - [24.5.3 StorageClass 规格](#2453-storageclass-规格)
  - [24.5.4 动态供给规格](#2454-动态供给规格)
  - [24.5.5 静态供给规格](#2455-静态供给规格)
- [24.6 存储卷模式技术规格](#246-存储卷模式技术规格)
  - [24.6.1 Filesystem 模式](#2461-filesystem-模式)
  - [24.6.2 Block 模式](#2462-block-模式)
  - [24.6.3 存储卷模式对比](#2463-存储卷模式对比)
- [24.7 存储访问模式技术规格](#247-存储访问模式技术规格)
  - [24.7.1 ReadWriteOnce](#2471-readwriteonce)
  - [24.7.2 ReadOnlyMany](#2472-readonlymany)
  - [24.7.3 ReadWriteMany](#2473-readwritemany)
  - [24.7.4 ReadWriteOncePod](#2474-readwriteoncepod)
  - [24.7.5 访问模式对比](#2475-访问模式对比)
- [24.8 存储拓扑技术规格](#248-存储拓扑技术规格)
  - [24.8.1 单节点存储拓扑](#2481-单节点存储拓扑)
  - [24.8.2 多节点存储拓扑](#2482-多节点存储拓扑)
  - [24.8.3 分布式存储拓扑](#2483-分布式存储拓扑)
  - [24.8.4 边缘存储拓扑](#2484-边缘存储拓扑)
- [24.9 存储性能规格](#249-存储性能规格)
  - [24.9.1 IOPS 规格](#2491-iops-规格)
  - [24.9.2 吞吐量规格](#2492-吞吐量规格)
  - [24.9.3 延迟规格](#2493-延迟规格)
  - [24.9.4 性能对比](#2494-性能对比)
- [24.10 存储技术栈组合方案](#2410-存储技术栈组合方案)
  - [24.10.1 小规模集群组合](#24101-小规模集群组合)
  - [24.10.2 大规模集群组合](#24102-大规模集群组合)
  - [24.10.3 边缘计算组合](#24103-边缘计算组合)
  - [24.10.4 高性能组合](#24104-高性能组合)
  - [24.10.5 云原生组合](#24105-云原生组合)
- [24.11 存储接口规范](#2411-存储接口规范)
  - [24.11.1 CSI 接口规范](#24111-csi-接口规范)
  - [24.11.2 Storage API 规范](#24112-storage-api-规范)
  - [24.11.3 VolumeSnapshot API 规范](#24113-volumesnapshot-api-规范)
- [24.12 参考](#2412-参考)

---

## 24.1 文档定位

本文档全面梳理云原生容器技术栈中的存储技术、规格和堆栈组合方案，包括 CSI 插件
、PV/PVC、StorageClass、存储类型、存储卷模式、访问模式等存储技术的详细规格和技术
栈组合方案。

**文档结构**：

- **存储技术栈全景**：存储层次结构、技术组件矩阵、技术栈组合
- **CSI 插件技术规格**：NFS、Ceph、Longhorn、本地存储、云存储等 CSI 插件的详细规
  格
- **存储类型技术规格**：块存储、文件存储、对象存储的详细规格
- **PV/PVC 技术规格**：PersistentVolume、PersistentVolumeClaim、StorageClass 规
  格
- **存储卷模式技术规格**：Filesystem、Block 模式规格
- **存储访问模式技术规
  格**：ReadWriteOnce、ReadOnlyMany、ReadWriteMany、ReadWriteOncePod
- **存储拓扑技术规格**：单节点、多节点、分布式、边缘存储拓扑
- **存储性能规格**：IOPS、吞吐量、延迟、性能对比
- **存储技术栈组合方案**：不同场景的存储技术栈组合
- **存储接口规范**：CSI、Storage API、VolumeSnapshot API 规范

## 24.2 存储技术栈全景

### 24.2.1 存储层次结构

**存储层次结构**：

```mermaid
graph TB
    A[应用层] --> B[PVC<br/>存储声明]
    B --> C[PV<br/>持久化卷]
    C --> D[StorageClass<br/>存储类]
    D --> E[CSI Driver<br/>CSI 驱动]
    E --> F[存储后端<br/>NFS/Ceph/Local/Cloud]

    subgraph "存储类型"
        F1[块存储<br/>Block Storage]
        F2[文件存储<br/>File Storage]
        F3[对象存储<br/>Object Storage]
    end

    F --> F1
    F --> F2
    F --> F3

    style B fill:#e1f5ff
    style C fill:#e1f5ff
    style D fill:#fff4e1
    style E fill:#e6ffe6
    style F fill:#ffe6e6
```

**存储层次定义**：

| 层次       | 定义         | 技术                       | 功能                   |
| ---------- | ------------ | -------------------------- | ---------------------- |
| **应用层** | 应用使用存储 | PVC                        | 存储请求声明           |
| **编排层** | 存储编排     | PV、StorageClass           | 存储资源管理和动态分配 |
| **驱动层** | 存储驱动     | CSI Driver                 | 存储后端接口实现       |
| **存储层** | 存储后端     | NFS、Ceph、Local、Cloud    | 实际存储提供           |
| **类型层** | 存储类型     | 块存储、文件存储、对象存储 | 不同存储访问模式       |

### 24.2.2 技术组件矩阵

**存储技术组件矩阵**：

| 组件类别     | 技术           | 定位                    | 成熟度     | 生产验证   |
| ------------ | -------------- | ----------------------- | ---------- | ---------- |
| **CSI 驱动** | NFS CSI        | 文件存储 CSI 驱动       | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   |
|              | Ceph CSI       | 分布式存储 CSI 驱动     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Longhorn CSI   | 轻量分布式存储 CSI 驱动 | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   |
|              | Local Path     | 本地路径存储 CSI 驱动   | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   |
|              | AWS EBS CSI    | AWS 块存储 CSI 驱动     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Azure Disk CSI | Azure 块存储 CSI 驱动   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | GCP PD CSI     | GCP 块存储 CSI 驱动     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **存储类型** | 块存储         | Block Storage           | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | 文件存储       | File Storage            | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | 对象存储       | Object Storage          | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   |
| **存储后端** | NFS            | 网络文件系统            | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Ceph           | 分布式存储系统          | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | GlusterFS      | 分布式文件系统          | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   |
|              | Longhorn       | 轻量分布式存储          | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   |
|              | Local Disk     | 本地磁盘存储            | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Cloud Storage  | 云存储服务              | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 24.2.3 技术栈组合

**存储技术栈组合方案**：

| 场景           | 存储类型   | CSI 驱动       | 存储后端    | 特点                     |
| -------------- | ---------- | -------------- | ----------- | ------------------------ |
| **小规模集群** | 文件存储   | NFS CSI        | NFS Server  | 简单易用、配置简单       |
| **大规模集群** | 分布式存储 | Ceph CSI       | Ceph        | 高性能、高可用、可扩展   |
| **边缘计算**   | 本地存储   | Local Path     | Local Disk  | 轻量级、低延迟           |
| **高性能场景** | 块存储     | Cloud CSI/本地 | SSD/NVMe    | 高性能、低延迟           |
| **云原生场景** | 云存储     | Cloud CSI      | EBS/PD/Disk | 与云平台集成、自动化管理 |

## 24.3 CSI 插件技术规格

### 24.3.1 CSI 规范

**CSI（Container Storage Interface）规范**：

**定义**：CSI 是容器编排系统（如 Kubernetes）与存储系统之间的标准化接口，用于解
耦存储实现和编排系统。

**核心组件**：

1. **CSI Driver**：存储驱动的实现，运行在 Kubernetes 集群中
2. **CSI Node Plugin**：节点插件，处理节点级别的存储操作
3. **CSI Controller Plugin**：控制器插件，处理集群级别的存储操作

**CSI 操作**：

| 操作                    | 功能           | 调用组件   |
| ----------------------- | -------------- | ---------- |
| **CreateVolume**        | 创建存储卷     | Controller |
| **DeleteVolume**        | 删除存储卷     | Controller |
| **NodePublishVolume**   | 在节点上挂载卷 | Node       |
| **NodeUnpublishVolume** | 在节点上卸载卷 | Node       |
| **NodeStageVolume**     | 在节点上准备卷 | Node       |
| **NodeUnstageVolume**   | 在节点上清理卷 | Node       |

**CSI 规范版本**：

- **CSI v1.0**：2019 年发布，基础 CSI 规范
- **CSI v1.1**：增加快照支持
- **CSI v1.2**：增加克隆支持
- **CSI v1.3**：增加存储容量跟踪
- **CSI v1.5**：增加存储卷健康监控
- **CSI v1.8**：增加存储卷服务（2024 年最新）

### 24.3.2 NFS CSI 规格

**NFS CSI Driver 规格**：

**技术特点**：

- ✅ 支持动态供给和静态供给
- ✅ 支持 ReadWriteMany 访问模式
- ✅ 支持存储卷快照和克隆
- ✅ 支持存储卷扩展

**版本信息**：

- **最新版本**：v4.0.0+（2024）
- **GitHub Stars**：500+
- **生产验证**：✅ 广泛使用

**配置示例**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-storage
provisioner: nfs.csi.k8s.io
parameters:
  server: nfs-server.example.com
  share: /exports
  mountOptions: "nfsvers=4.1"
allowVolumeExpansion: true
```

**适用场景**：

- ✅ 小规模集群
- ✅ 共享存储需求
- ✅ 多 Pod 读写同一存储

### 24.3.3 Ceph CSI 规格

**Ceph CSI Driver 规格**：

**技术特点**：

- ✅ 支持 RBD（块存储）和 CephFS（文件存储）
- ✅ 支持动态供给和静态供给
- ✅ 支持存储卷快照和克隆
- ✅ 支持存储卷扩展
- ✅ 支持多后端存储

**版本信息**：

- **最新版本**：v3.10.0+（2024）
- **GitHub Stars**：1.5K+
- **生产验证**：✅ 大规模生产使用

**配置示例**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ceph-rbd
provisioner: rbd.csi.ceph.com
parameters:
  clusterID: ceph-cluster
  pool: k8s-pool
  imageFormat: "2"
  imageFeatures: layering
allowVolumeExpansion: true
```

**适用场景**：

- ✅ 大规模集群
- ✅ 高性能需求
- ✅ 高可用需求
- ✅ 分布式存储场景

### 24.3.4 Longhorn CSI 规格

**Longhorn CSI Driver 规格**：

**技术特点**：

- ✅ 轻量级分布式存储
- ✅ 支持动态供给
- ✅ 支持存储卷快照和备份
- ✅ 支持存储卷复制
- ✅ 易于部署和管理

**版本信息**：

- **最新版本**：v1.6.0+（2024）
- **GitHub Stars**：5K+
- **生产验证**：✅ 中等规模生产使用

**配置示例**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: longhorn
provisioner: driver.longhorn.io
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: Immediate
```

**适用场景**：

- ✅ 中小规模集群
- ✅ 边缘计算场景
- ✅ 简单分布式存储需求

### 24.3.5 本地存储 CSI 规格

**Local Path Provisioner 规格**：

**技术特点**：

- ✅ 使用节点本地磁盘
- ✅ 支持动态供给
- ✅ 轻量级部署
- ✅ 低延迟

**版本信息**：

- **最新版本**：v0.0.24+（2024）
- **GitHub Stars**：1K+
- **生产验证**：✅ 边缘场景广泛使用

**配置示例**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-path
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
```

**适用场景**：

- ✅ 边缘计算
- ✅ 单节点存储
- ✅ 低延迟需求
- ✅ K3s 场景

### 24.3.6 云存储 CSI 规格

**云存储 CSI Driver 规格**：

**AWS EBS CSI**：

- ✅ 支持 EBS 块存储
- ✅ 动态供给和快照
- ✅ 最新版本：v1.29.0+（2024）

**Azure Disk CSI**：

- ✅ 支持 Azure Managed Disk
- ✅ 动态供给和快照
- ✅ 最新版本：v1.29.0+（2024）

**GCP PD CSI**：

- ✅ 支持 Persistent Disk
- ✅ 动态供给和快照
- ✅ 最新版本：v1.16.0+（2024）

**配置示例（AWS EBS）**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
allowVolumeExpansion: true
```

**适用场景**：

- ✅ 云原生应用
- ✅ 与云平台深度集成
- ✅ 自动化存储管理

### 24.3.7 CSI 插件对比

**CSI 插件对比矩阵**：

| CSI 驱动        | 存储类型 | 访问模式支持 | 快照支持 | 克隆支持 | 扩展支持 | 成熟度     | 推荐场景         |
| --------------- | -------- | ------------ | -------- | -------- | -------- | ---------- | ---------------- |
| **NFS CSI**     | 文件存储 | RWO/RWX/ROX  | ✅       | ✅       | ✅       | ⭐⭐⭐⭐   | 小规模、共享存储 |
| **Ceph CSI**    | 块/文件  | RWO/RWX      | ✅       | ✅       | ✅       | ⭐⭐⭐⭐⭐ | 大规模、高性能   |
| **Longhorn**    | 块存储   | RWO          | ✅       | ✅       | ✅       | ⭐⭐⭐⭐   | 中小规模、简单   |
| **Local Path**  | 本地存储 | RWO          | ❌       | ❌       | ❌       | ⭐⭐⭐⭐   | 边缘、单节点     |
| **AWS EBS CSI** | 块存储   | RWO          | ✅       | ✅       | ✅       | ⭐⭐⭐⭐⭐ | AWS 云原生       |
| **Azure Disk**  | 块存储   | RWO          | ✅       | ✅       | ✅       | ⭐⭐⭐⭐⭐ | Azure 云原生     |
| **GCP PD CSI**  | 块存储   | RWO          | ✅       | ✅       | ✅       | ⭐⭐⭐⭐⭐ | GCP 云原生       |

## 24.4 存储类型技术规格

### 24.4.1 块存储规格

**块存储（Block Storage）规格**：

**定义**：块存储是将存储划分为固定大小的块，通过块设备接口访问的存储类型。

**特点**：

- ✅ 高性能、低延迟
- ✅ 支持 ReadWriteOnce 访问模式
- ✅ 适合数据库、高性能应用
- ❌ 不支持多 Pod 同时读写

**典型实现**：

- **Ceph RBD**：Ceph 块设备
- **AWS EBS**：AWS 弹性块存储
- **Azure Disk**：Azure 托管磁盘
- **GCP PD**：GCP 持久化磁盘
- **Longhorn**：Longhorn 块存储

**性能规格**：

| 存储后端          | IOPS      | 吞吐量          | 延迟    |
| ----------------- | --------- | --------------- | ------- |
| **Ceph RBD**      | 10K-100K+ | 500MB/s-1GB/s+  | 0.1-1ms |
| **AWS EBS gp3**   | 3K-16K    | 125MB/s-1GB/s   | < 1ms   |
| **Azure Premium** | 500-20K   | 60MB/s-500MB/s  | < 1ms   |
| **GCP PD SSD**    | 750-30K   | 48MB/s-480MB/s  | < 1ms   |
| **Longhorn**      | 1K-10K    | 100MB/s-500MB/s | 1-5ms   |

### 24.4.2 文件存储规格

**文件存储（File Storage）规格**：

**定义**：文件存储是通过文件系统接口访问的存储类型，支持多个客户端同时访问。

**特点**：

- ✅ 支持 ReadWriteMany 访问模式
- ✅ 支持多 Pod 同时读写
- ✅ 适合共享存储、内容管理
- ⚠️ 性能相对块存储较低

**典型实现**：

- **NFS**：网络文件系统
- **CephFS**：Ceph 文件系统
- **GlusterFS**：Gluster 文件系统

**性能规格**：

| 存储后端      | IOPS      | 吞吐量        | 延迟   |
| ------------- | --------- | ------------- | ------ |
| **NFS v4**    | 1K-10K    | 100MB/s-1GB/s | 1-10ms |
| **CephFS**    | 10K-100K+ | 500MB/s-5GB/s | 1-5ms  |
| **GlusterFS** | 5K-50K    | 200MB/s-2GB/s | 2-10ms |

### 24.4.3 对象存储规格

**对象存储（Object Storage）规格**：

**定义**：对象存储是通过 HTTP/HTTPS API 访问的存储类型，以对象为单位存储数据。

**特点**：

- ✅ 高可扩展性
- ✅ 适合大数据、归档存储
- ✅ 支持版本控制和生命周期管理
- ⚠️ 不适合频繁读写场景

**典型实现**：

- **AWS S3**：AWS 对象存储
- **Azure Blob**：Azure 对象存储
- **GCP GCS**：GCP 对象存储
- **MinIO**：开源对象存储
- **Ceph RGW**：Ceph 对象网关

**性能规格**：

| 存储后端     | 请求延迟 | 吞吐量         | 适用场景       |
| ------------ | -------- | -------------- | -------------- |
| **AWS S3**   | 10-100ms | 100MB/s-5GB/s  | 大数据、归档   |
| **MinIO**    | 5-50ms   | 500MB/s-10GB/s | 私有云、边缘   |
| **Ceph RGW** | 10-100ms | 1GB/s-10GB/s+  | 大规模对象存储 |

### 24.4.4 存储类型对比

**存储类型对比矩阵**：

| 特性         | 块存储     | 文件存储    | 对象存储    |
| ------------ | ---------- | ----------- | ----------- |
| **访问模式** | RWO        | RWO/RWX/ROX | 通过 API    |
| **性能**     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐    | ⭐⭐⭐      |
| **延迟**     | 最低       | 中等        | 较高        |
| **扩展性**   | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐  |
| **多客户端** | ❌         | ✅          | ✅          |
| **典型场景** | 数据库     | 共享存储    | 大数据归档  |
| **CSI 支持** | ✅         | ✅          | ⚠️ 部分支持 |

## 24.5 PV/PVC 技术规格

### 24.5.1 PersistentVolume 规格

**PersistentVolume（PV）规格**：

**定义**：PV 是集群级别的存储资源，由管理员预先配置或通过 StorageClass 动态创建
。

**PV 状态**：

| 状态          | 说明   | 转换条件       |
| ------------- | ------ | -------------- |
| **Available** | 可用   | 创建后或释放后 |
| **Bound**     | 已绑定 | 被 PVC 绑定    |
| **Released**  | 已释放 | PVC 删除后     |
| **Failed**    | 失败   | 存储后端错误   |
| **Pending**   | 等待中 | 动态创建中     |

**PV 配置示例**：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: nfs-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs-storage
  nfs:
    server: nfs-server.example.com
    path: /exports/data
```

### 24.5.2 PersistentVolumeClaim 规格

**PersistentVolumeClaim（PVC）规格**：

**定义**：PVC 是用户对存储的请求，Kubernetes 会根据 PVC 的要求绑定或创建 PV。

**PVC 绑定模式**：

| 模式                     | 说明                 | 适用场景          |
| ------------------------ | -------------------- | ----------------- |
| **Immediate**            | 立即绑定             | 存储已就绪        |
| **WaitForFirstConsumer** | 等待首个消费者       | 需要 Pod 调度决定 |
| **VolumeBindingMode**    | 卷绑定模式（已弃用） | -                 |

**PVC 配置示例**：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 20Gi
```

### 24.5.3 StorageClass 规格

**StorageClass 规格**：

**定义**：StorageClass 是存储类的抽象，定义了存储的动态供给策略和参数。

**StorageClass 参数**：

- **provisioner**：CSI 驱动名称
- **parameters**：存储驱动特定参数
- **allowVolumeExpansion**：是否允许卷扩展
- **reclaimPolicy**：回收策略（Delete/Retain）
- **volumeBindingMode**：绑定模式

**StorageClass 配置示例**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "4000"
  throughput: "500"
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```

### 24.5.4 动态供给规格

**动态供给（Dynamic Provisioning）规格**：

**定义**：动态供给是通过 StorageClass 自动创建 PV 的机制。

**工作流程**：

1. 用户创建 PVC，指定 StorageClass
2. StorageClass 触发 CSI Driver 创建存储
3. CSI Driver 创建 PV 并绑定到 PVC
4. Pod 使用 PVC 挂载存储

**优势**：

- ✅ 自动化存储管理
- ✅ 无需预先配置 PV
- ✅ 灵活的资源分配

### 24.5.5 静态供给规格

**静态供给（Static Provisioning）规格**：

**定义**：静态供给是管理员预先创建 PV，然后由 PVC 绑定的机制。

**工作流程**：

1. 管理员创建 PV
2. 用户创建 PVC，要求匹配 PV 规格
3. Kubernetes 匹配 PV 和 PVC 并绑定
4. Pod 使用 PVC 挂载存储

**优势**：

- ✅ 精确控制存储资源
- ✅ 适合特殊存储需求
- ✅ 可预测的资源分配

## 24.6 存储卷模式技术规格

### 24.6.1 Filesystem 模式

**Filesystem 模式规格**：

**定义**：Filesystem 模式将存储卷格式化为文件系统后挂载到 Pod。

**特点**：

- ✅ 支持文件系统操作
- ✅ 支持目录和文件管理
- ✅ 适合大多数应用场景
- ✅ 支持大多数访问模式

**使用场景**：

- ✅ Web 应用
- ✅ 内容管理
- ✅ 日志存储
- ✅ 配置文件存储

### 24.6.2 Block 模式

**Block 模式规格**：

**定义**：Block 模式将存储卷作为原始块设备挂载到 Pod。

**特点**：

- ✅ 高性能、低延迟
- ✅ 适合数据库、高性能应用
- ⚠️ 需要应用自行管理文件系统
- ⚠️ 仅支持 ReadWriteOnce

**使用场景**：

- ✅ 数据库（MySQL、PostgreSQL）
- ✅ 高性能计算
- ✅ 块设备直接访问场景

### 24.6.3 存储卷模式对比

**存储卷模式对比**：

| 特性         | Filesystem 模式 | Block 模式 |
| ------------ | --------------- | ---------- |
| **性能**     | ⭐⭐⭐⭐        | ⭐⭐⭐⭐⭐ |
| **延迟**     | 中等            | 最低       |
| **易用性**   | ⭐⭐⭐⭐⭐      | ⭐⭐⭐     |
| **访问模式** | RWO/RWX/ROX     | RWO        |
| **典型场景** | 大多数应用      | 数据库     |
| **文件系统** | 自动格式化      | 需应用管理 |

## 24.7 存储访问模式技术规格

### 24.7.1 ReadWriteOnce

**ReadWriteOnce（RWO）规格**：

**定义**：RWO 表示存储卷可以被单个节点以读写模式挂载。

**特点**：

- ✅ 支持单 Pod 读写
- ✅ 高性能、低延迟
- ✅ 适合数据库、高性能应用
- ❌ 不支持多 Pod 同时挂载

**支持存储类型**：

- ✅ 块存储（Ceph RBD、AWS EBS、Azure Disk、GCP PD）
- ✅ 本地存储（Local Path）
- ✅ 大多数 CSI 驱动

### 24.7.2 ReadOnlyMany

**ReadOnlyMany（ROX）规格**：

**定义**：ROX 表示存储卷可以被多个节点以只读模式挂载。

**特点**：

- ✅ 支持多 Pod 只读访问
- ✅ 适合配置共享、内容分发
- ❌ 不支持写入操作

**支持存储类型**：

- ✅ 文件存储（NFS、CephFS）
- ⚠️ 部分块存储（需驱动支持）

### 24.7.3 ReadWriteMany

**ReadWriteMany（RWX）规格**：

**定义**：RWX 表示存储卷可以被多个节点以读写模式挂载。

**特点**：

- ✅ 支持多 Pod 同时读写
- ✅ 适合共享存储、内容管理
- ⚠️ 性能相对较低
- ⚠️ 需要存储后端支持并发访问

**支持存储类型**：

- ✅ 文件存储（NFS、CephFS、GlusterFS）
- ❌ 块存储不支持（除特殊实现）

### 24.7.4 ReadWriteOncePod

**ReadWriteOncePod（RWOP）规格**：

**定义**：RWOP 表示存储卷可以被单个 Pod 以读写模式挂载（Kubernetes 1.22+）。

**特点**：

- ✅ 确保存储卷只能被一个 Pod 使用
- ✅ 适合需要独占存储的场景
- ✅ 防止意外共享存储

**支持版本**：

- ✅ Kubernetes 1.22+
- ✅ 需要 CSI 驱动支持

### 24.7.5 访问模式对比

**存储访问模式对比**：

| 访问模式 | 挂载节点数 | 读写权限 | 性能       | 典型场景 |
| -------- | ---------- | -------- | ---------- | -------- |
| **RWO**  | 1          | 读写     | ⭐⭐⭐⭐⭐ | 数据库   |
| **ROX**  | 多个       | 只读     | ⭐⭐⭐⭐   | 配置共享 |
| **RWX**  | 多个       | 读写     | ⭐⭐⭐     | 共享存储 |
| **RWOP** | 1 Pod      | 读写     | ⭐⭐⭐⭐⭐ | 独占存储 |

## 24.8 存储拓扑技术规格

### 24.8.1 单节点存储拓扑

**单节点存储拓扑规格**：

**定义**：存储卷只能挂载到特定节点，通常是本地存储。

**特点**：

- ✅ 低延迟、高性能
- ✅ 适合边缘计算
- ❌ 不可迁移、不可扩展

**典型实现**：

- **Local Path Provisioner**：本地路径存储
- **HostPath**：主机路径存储

**适用场景**：

- ✅ 边缘计算
- ✅ 单节点集群
- ✅ 临时数据存储

### 24.8.2 多节点存储拓扑

**多节点存储拓扑规格**：

**定义**：存储卷可以在多个节点之间迁移，但同一时间只能挂载到一个节点。

**特点**：

- ✅ 支持 Pod 迁移
- ✅ 适合有状态应用
- ✅ 适合动态调度

**典型实现**：

- **Ceph RBD**：Ceph 块设备
- **AWS EBS**：AWS 弹性块存储
- **Azure Disk**：Azure 托管磁盘

### 24.8.3 分布式存储拓扑

**分布式存储拓扑规格**：

**定义**：存储卷可以在多个节点同时访问，支持并发读写。

**特点**：

- ✅ 高可用、可扩展
- ✅ 支持多 Pod 访问
- ⚠️ 性能可能受网络影响

**典型实现**：

- **NFS**：网络文件系统
- **CephFS**：Ceph 文件系统
- **GlusterFS**：Gluster 文件系统

### 24.8.4 边缘存储拓扑

**边缘存储拓扑规格**：

**定义**：在边缘节点上使用本地存储，支持离线访问。

**特点**：

- ✅ 低延迟、高性能
- ✅ 支持离线访问
- ✅ 适合边缘计算
- ⚠️ 容量受限

**典型实现**：

- **Local Path Provisioner**：K3s 内置
- **HostPath**：主机路径
- **边缘存储设备**：USB、SD 卡等

## 24.9 存储性能规格

### 24.9.1 IOPS 规格

**IOPS（Input/Output Operations Per Second）规格**：

**定义**：IOPS 是存储系统每秒能处理的输入输出操作数。

**IOPS 对比**：

| 存储类型        | 典型 IOPS 范围 | 最佳场景     |
| --------------- | -------------- | ------------ |
| **本地 SSD**    | 10K-100K+      | 高性能数据库 |
| **Ceph RBD**    | 10K-100K+      | 分布式存储   |
| **AWS EBS gp3** | 3K-16K         | 云原生应用   |
| **NFS v4**      | 1K-10K         | 共享存储     |
| **Longhorn**    | 1K-10K         | 中小规模集群 |

### 24.9.2 吞吐量规格

**吞吐量（Throughput）规格**：

**定义**：吞吐量是存储系统每秒能传输的数据量，通常以 MB/s 或 GB/s 表示。

**吞吐量对比**：

| 存储类型        | 典型吞吐量范围  | 最佳场景     |
| --------------- | --------------- | ------------ |
| **本地 SSD**    | 500MB/s-5GB/s+  | 大数据处理   |
| **CephFS**      | 500MB/s-5GB/s+  | 分布式文件   |
| **AWS EBS gp3** | 125MB/s-1GB/s   | 云原生应用   |
| **NFS v4**      | 100MB/s-1GB/s   | 共享存储     |
| **Longhorn**    | 100MB/s-500MB/s | 中小规模集群 |

### 24.9.3 延迟规格

**延迟（Latency）规格**：

**定义**：延迟是存储操作从发起到完成的响应时间。

**延迟对比**：

| 存储类型        | 典型延迟范围 | 最佳场景     |
| --------------- | ------------ | ------------ |
| **本地 SSD**    | 0.1-1ms      | 低延迟应用   |
| **Ceph RBD**    | 0.1-1ms      | 分布式块存储 |
| **AWS EBS gp3** | < 1ms        | 云原生应用   |
| **NFS v4**      | 1-10ms       | 共享存储     |
| **Longhorn**    | 1-5ms        | 中小规模集群 |

### 24.9.4 性能对比

**存储性能综合对比**：

| 存储方案        | IOPS       | 吞吐量     | 延迟       | 综合评分   |
| --------------- | ---------- | ---------- | ---------- | ---------- |
| **本地 SSD**    | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Ceph RBD**    | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **AWS EBS gp3** | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐   |
| **NFS v4**      | ⭐⭐⭐     | ⭐⭐⭐     | ⭐⭐⭐     | ⭐⭐⭐     |
| **Longhorn**    | ⭐⭐⭐     | ⭐⭐⭐     | ⭐⭐⭐⭐   | ⭐⭐⭐     |

## 24.10 存储技术栈组合方案

### 24.10.1 小规模集群组合

**小规模集群存储组合**：

**技术栈**：

- **存储类型**：文件存储
- **CSI 驱动**：NFS CSI
- **存储后端**：NFS Server
- **StorageClass**：nfs-storage

**配置示例**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-storage
provisioner: nfs.csi.k8s.io
parameters:
  server: nfs-server.example.com
  share: /exports
reclaimPolicy: Delete
allowVolumeExpansion: true
```

**特点**：

- ✅ 简单易用、配置简单
- ✅ 支持多 Pod 共享存储
- ✅ 成本低
- ⚠️ 性能相对较低

### 24.10.2 大规模集群组合

**大规模集群存储组合**：

**技术栈**：

- **存储类型**：分布式存储
- **CSI 驱动**：Ceph CSI
- **存储后端**：Ceph 集群
- **StorageClass**：ceph-rbd、cephfs

**配置示例**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ceph-rbd
provisioner: rbd.csi.ceph.com
parameters:
  clusterID: ceph-cluster
  pool: k8s-pool
  imageFormat: "2"
  imageFeatures: layering
allowVolumeExpansion: true
```

**特点**：

- ✅ 高性能、高可用
- ✅ 可扩展性强
- ✅ 支持快照和克隆
- ⚠️ 配置相对复杂

### 24.10.3 边缘计算组合

**边缘计算存储组合**：

**技术栈**：

- **存储类型**：本地存储
- **CSI 驱动**：Local Path Provisioner
- **存储后端**：本地磁盘
- **StorageClass**：local-path

**配置示例**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-path
provisioner: rancher.io/local-path
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
```

**特点**：

- ✅ 低延迟、高性能
- ✅ 轻量级部署
- ✅ 适合边缘场景
- ⚠️ 不支持跨节点迁移

### 24.10.4 高性能组合

**高性能存储组合**：

**技术栈**：

- **存储类型**：块存储
- **CSI 驱动**：Cloud CSI 或 Ceph CSI
- **存储后端**：SSD/NVMe
- **StorageClass**：fast-ssd

**配置示例**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "16000"
  throughput: "1000"
allowVolumeExpansion: true
```

**特点**：

- ✅ 超高性能、超低延迟
- ✅ 适合数据库、高性能应用
- ⚠️ 成本较高

### 24.10.5 云原生组合

**云原生存储组合**：

**技术栈**：

- **存储类型**：云存储
- **CSI 驱动**：云厂商 CSI（AWS EBS、Azure Disk、GCP PD）
- **存储后端**：云存储服务
- **StorageClass**：云存储类

**配置示例（AWS EBS）**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

**特点**：

- ✅ 与云平台深度集成
- ✅ 自动化管理
- ✅ 高可用、可扩展
- ✅ 按需付费

## 24.11 存储接口规范

### 24.11.1 CSI 接口规范

**CSI 接口规范**：

**定义**：CSI（Container Storage Interface）是容器编排系统与存储系统之间的标准化
接口。

**核心接口**：

- **Identity Service**：身份服务
- **Controller Service**：控制器服务
- **Node Service**：节点服务

**最新规范**：

- **CSI v1.8**：2024 年最新版本
- **支持特性**：快照、克隆、扩展、健康监控、卷服务

### 24.11.2 Storage API 规范

**Storage API 规范**：

**Kubernetes Storage API**：

- **PersistentVolume**：v1 API
- **PersistentVolumeClaim**：v1 API
- **StorageClass**：storage.k8s.io/v1 API
- **VolumeSnapshot**：snapshot.storage.k8s.io/v1 API（需要 CSI 驱动支持）

### 24.11.3 VolumeSnapshot API 规范

**VolumeSnapshot API 规范**：

**定义**：VolumeSnapshot API 用于创建和管理存储卷快照。

**核心资源**：

- **VolumeSnapshotClass**：快照类，定义快照策略
- **VolumeSnapshot**：快照对象
- **VolumeSnapshotContent**：快照内容

**配置示例**：

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: ceph-snapshot-class
driver: rbd.csi.ceph.com
deletionPolicy: Delete
```

## 24.12 参考

- [Kubernetes 存储文档](https://kubernetes.io/docs/concepts/storage/)
- [CSI 规范](https://github.com/container-storage-interface/spec)
- [NFS CSI Driver](https://github.com/kubernetes-csi/csi-driver-nfs)
- [Ceph CSI Driver](https://github.com/ceph/ceph-csi)
- [Longhorn 文档](https://longhorn.io/docs/)
- [Local Path Provisioner](https://github.com/rancher/local-path-provisioner)
- [AWS EBS CSI Driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)
- [Azure Disk CSI Driver](https://github.com/kubernetes-sigs/azuredisk-csi-driver)
- [GCP PD CSI Driver](https://github.com/kubernetes-sigs/gcp-compute-persistent-disk-csi-driver)
