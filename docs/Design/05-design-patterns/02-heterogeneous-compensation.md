# 7.2 异构补偿机制

> **文档版本**：v1.0 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [7.2 异构补偿机制](#72-异构补偿机制)
  - [📑 目录](#-目录)
  - [概述](#概述)
  - [异构补偿机制矩阵](#异构补偿机制矩阵)
  - [关键技术分析](#关键技术分析)
    - [1. 启动速度差异](#1-启动速度差异)
    - [2. 状态粒度差异](#2-状态粒度差异)
    - [3. 热迁移差异](#3-热迁移差异)
    - [4. GuestOS 感知差异](#4-guestos-感知差异)
    - [5. 硬件直通差异](#5-硬件直通差异)
  - [相关文档](#相关文档)

---

## 概述

本文档分析虚拟化容器化集群管理 API 中的异构补偿机制，展示如何通过补偿方案解决容
器和虚拟机之间的差异。

## 异构补偿机制矩阵

| **差异点**       | **补偿方案**       | **API 设计**                              |
| ---------------- | ------------------ | ----------------------------------------- |
| **启动速度**     | 预分配资源池       | VirtualMachinePool CRD                    |
| **状态粒度**     | 更细状态机         | Stopped/Paused/Running vs Pending/Running |
| **热迁移**       | 新增控制器         | Migration CRD                             |
| **GuestOS 感知** | Agent 扩展         | Guest Agent 协议                          |
| **硬件直通**     | Device Plugin 扩展 | KubeVirt Device Plugin                    |

---

## 关键技术分析

### 1. 启动速度差异

**差异点**：虚拟机启动速度慢（30-60 秒），容器启动速度快（秒级）

**补偿方案**：预分配资源池

**API 设计**：VirtualMachinePool CRD

```yaml
apiVersion: pool.kubevirt.io/v1
kind: VirtualMachinePool
metadata:
  name: fast-start-pool
spec:
  size: 10
  template:
    spec:
      domain:
        resources:
          requests:
            memory: "2Gi"
            cpu: "2"
      volumes:
        - name: bootdisk
          containerDisk:
            image: ubuntu:22.04
  autoReplenish: true
  minAvailable: 5
```

**说明**：

- 预分配资源池提前创建虚拟机，减少启动时间
- VirtualMachinePool CRD 管理资源池生命周期
- 自动补充机制确保资源池始终有可用虚拟机

### 2. 状态粒度差异

**差异点**：虚拟机状态粒度更细（Stopped/Paused/Running），容器状态粒度较粗
（Pending/Running）

**补偿方案**：更细状态机

**API 设计**：Stopped/Paused/Running vs Pending/Running

```yaml
# 容器状态机
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
status:
  phase: Running
  conditions:
    - type: Ready
      status: "True"

# 虚拟机状态机（更细粒度）
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
status:
  phase: Running
  conditions:
    - type: Ready
      status: "True"
  # 虚拟机特有状态
  - type: Paused
    status: "False"
  - type: Stopped
    status: "False"
```

**说明**：

- 虚拟机状态机更细粒度，支持 Stopped/Paused/Running 状态
- 容器状态机较粗粒度，仅支持 Pending/Running 状态
- 状态机差异通过 CRD 扩展字段补偿

### 3. 热迁移差异

**差异点**：虚拟机支持热迁移，容器不支持热迁移

**补偿方案**：新增控制器

**API 设计**：Migration CRD

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstanceMigration
metadata:
  name: test-vmi-migration
spec:
  vmiName: test-vmi
status:
  phase: Running
  migrationState:
    startTimestamp: "2025-11-07T10:00:00Z"
    endTimestamp: null
    targetNode: "node-2"
    targetPod: "virt-launcher-test-vmi-xxxxx"
    sourceNode: "node-1"
    sourcePod: "virt-launcher-test-vmi-yyyyy"
    completed: false
    failed: false
```

**说明**：

- 虚拟机支持热迁移，通过 Migration CRD 实现
- 容器不支持热迁移，只能通过删除并重新创建 Pod 实现迁移
- 热迁移功能是虚拟机的特有功能

### 4. GuestOS 感知差异

**差异点**：虚拟机需要 GuestOS 感知，容器不需要 GuestOS 感知

**补偿方案**：Agent 扩展

**API 设计**：Guest Agent 协议

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    devices:
      channels:
        - type: unix
          target:
            name: org.qemu.guest_agent.0
          source:
            name: guest-agent
    resources:
      requests:
        memory: "1Gi"
        cpu: "1"
```

**说明**：

- 虚拟机需要 Guest Agent 感知 GuestOS 状态
- 容器不需要 Guest Agent，容器直接运行在宿主机上
- Guest Agent 协议通过 virt-handler 代理，统一上报到 API Server

### 5. 硬件直通差异

**差异点**：虚拟机支持硬件直通（GPU/FPGA），容器支持有限

**补偿方案**：Device Plugin 扩展

**API 设计**：KubeVirt Device Plugin

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    devices:
      gpus:
        - deviceName: nvidia.com/gpu
          name: gpu1
      hostDevices:
        - deviceName: pci_0000_01_00_0
          name: fpga1
    resources:
      requests:
        memory: "1Gi"
        cpu: "1"
        nvidia.com/gpu: "1"
```

**说明**：

- 虚拟机支持硬件直通，通过 Device Plugin 扩展实现
- 容器支持有限的硬件直通，主要通过 Device Plugin 实现
- 硬件直通功能通过 Device Plugin 统一管理

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [同构设计原则](../05-design-patterns/01-isomorphic-principles.md) - 同构设计原
  则
- [实时迁移功能扩展](../03-dynamic-management/03-live-migration.md) - 实时迁移功
  能

---

**最后更新**：2025-11-10 **维护者**：项目团队
