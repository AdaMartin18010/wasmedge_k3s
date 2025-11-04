# Hypervisor/Kernel 层架构视图

## 目录

- [1. 概述](#1-概述)
- [2. 层级定位](#2-层级定位)
- [3. 核心技术组件](#3-核心技术组件)
- [4. 组合模式](#4-组合模式)
- [5. 形式化描述](#5-形式化描述)
- [6. 与上层的关系](#6-与上层的关系)
- [7. 2025 年 11 月最新趋势](#7-2025-年-11-月最新趋势)
- [8. 参考资源](#8-参考资源)

---

## 1. 概述

Hypervisor/Kernel 层位于硬件/固件层之上，负责资源调度、隔离和系统调用过滤。本文
档从架构视角分析 Hypervisor/Kernel 层的职责、接口和组合方式。

---

## 2. 层级定位

```text
┌────────────────────────────────────────────────────────────┐
│ 2. Hypervisor/Kernel 层                                    │
│    └─ KVM, Xen, seccomp-bpf, eBPF, cgroup, namespace       │
└────────────────────────────────────────────────────────────┘
                    ▲
┌────────────────────────────────────────────────────────────┐
│ 3. 编排层 (Orchestration Layer)                            │
│    └─ Kubernetes, Pod, Deployment, Service                 │
└────────────────────────────────────────────────────────────┘
```

### 2.1 职责边界

| 职责             | 说明                         | 典型实现                   |
| ---------------- | ---------------------------- | -------------------------- |
| **VM 调度**      | 虚拟机的创建、销毁和资源分配 | KVM, Xen, Hyper-V          |
| **资源隔离**     | CPU、内存、I/O 的资源隔离    | cgroup, namespace          |
| **系统调用过滤** | 进程系统调用的细粒度控制     | seccomp-bpf, eBPF          |
| **网络策略**     | 网络流量的策略控制           | eBPF, iptables             |
| **文件系统隔离** | 文件系统的访问控制           | overlayfs, mount namespace |

### 2.2 接口契约

Hypervisor/Kernel 层向上层提供的接口包括：

1. **虚拟化接口**

   - KVM API：Linux 内核虚拟化接口
   - Xen API：Xen Hypervisor 接口
   - Hyper-V API：Windows Hyper-V 接口

2. **容器接口**

   - cgroup v2：资源控制接口
   - namespace：命名空间隔离接口
   - seccomp：系统调用过滤接口

3. **网络接口**
   - eBPF：可编程网络策略
   - iptables：传统防火墙规则
   - netfilter：网络过滤框架

---

## 3. 核心技术组件

### 3.1 Hypervisor

| 技术        | 特点              | 典型实现          |
| ----------- | ----------------- | ----------------- |
| **KVM**     | Linux 内核虚拟化  | KVM/QEMU          |
| **Xen**     | Type-1 Hypervisor | Xen Project       |
| **Hyper-V** | Windows 虚拟化    | Microsoft Hyper-V |
| **bhyve**   | FreeBSD 虚拟化    | FreeBSD bhyve     |

**2025 年 11 月更新**：

- **KVM 6.9**：增强的嵌套虚拟化支持
- **Xen 4.19**：更好的 ARM 支持
- **Hyper-V 2025**：增强的机密计算支持

### 3.2 资源隔离

| 技术          | 特点                   | 典型实现                      |
| ------------- | ---------------------- | ----------------------------- |
| **cgroup v2** | 统一资源控制接口       | Linux cgroup v2               |
| **namespace** | 命名空间隔离           | pid, mnt, net, ipc, uts, user |
| **cgroup v1** | 传统资源控制（已废弃） | Linux cgroup v1               |

**2025 年 11 月更新**：

- **cgroup v2 默认启用**：所有新 Linux 发行版默认使用 cgroup v2
- **统一控制器**：CPU、内存、I/O 统一管理
- **性能优化**：cgroup v2 性能提升 20%

### 3.3 系统调用过滤

| 技术            | 特点                    | 典型实现       |
| --------------- | ----------------------- | -------------- |
| **seccomp-bpf** | 基于 BPF 的系统调用过滤 | Linux seccomp  |
| **eBPF**        | 可编程内核过滤器        | Linux eBPF     |
| **Landlock**    | 文件系统访问控制        | Linux Landlock |
| **AppArmor**    | 应用级访问控制          | AppArmor       |

**2025 年 11 月更新**：

- **eBPF 5.20**：Linux 内核 6.7+ 支持更多 eBPF 功能
- **Landlock 3.0**：增强的文件系统访问控制
- **seccomp 增强**：支持更细粒度的系统调用过滤

---

## 4. 组合模式

### 4.1 Hypervisor 组合

Hypervisor 与硬件层组合，提供虚拟化能力：

```text
Hardware ──> Hypervisor ──> VM
              │
              ├─ VT-x/SVM (硬件虚拟化)
              ├─ IOMMU (I/O 虚拟化)
              └─ TPM/SGX (安全虚拟化)
```

### 4.2 容器运行时组合

内核与容器运行时组合，提供容器隔离：

```text
Kernel ──> cgroup/namespace ──> Container
          │
          ├─ cgroup v2 (资源控制)
          ├─ namespace (隔离)
          └─ seccomp (安全过滤)
```

### 4.3 eBPF 组合

eBPF 与内核组合，提供可编程策略：

```text
Kernel ──> eBPF ──> Policy
         │
         ├─ 网络策略 (Cilium)
         ├─ 安全监控 (Falco)
         └─ 可观测性 (Pixie)
```

---

## 5. 形式化描述

### 5.1 Hypervisor 状态模型

Hypervisor 状态可以表示为：

**H = ⟨VMs, Resources, Policies⟩**:

其中：

- **VMs** = {vm₁, vm₂, ..., vmₙ}
- **Resources** = ⟨CPU, Memory, I/O⟩
- **Policies** = ⟨Scheduling, Isolation, Security⟩

### 5.2 资源调度模型

资源调度可以表示为：

**Schedule(VM, Resources) → Allocation**:

其中：

- **VM**: 虚拟机请求
- **Resources**: 可用资源
- **Allocation**: 资源分配结果

### 5.3 隔离模型

隔离可以表示为：

**Isolate(Process, Namespace) → IsolatedProcess**:

其中：

- **Process**: 原始进程
- **Namespace**: 命名空间配置
- **IsolatedProcess**: 隔离后的进程

---

## 6. 与上层的关系

### 6.1 向上层提供的接口

Hypervisor/Kernel 层向上层（编排层）提供：

1. **虚拟化接口**：VM 的创建和管理
2. **容器接口**：容器的创建和管理
3. **资源控制接口**：CPU、内存、I/O 的资源限制
4. **安全接口**：系统调用过滤和访问控制

### 6.2 组合方式

Hypervisor/Kernel 层与编排层的组合方式：

1. **CRI 接口**：容器运行时接口（Container Runtime Interface）
2. **CNI 接口**：容器网络接口（Container Network Interface）
3. **CSI 接口**：容器存储接口（Container Storage Interface）

---

## 7. 2025 年 11 月最新趋势

### 7.1 eBPF 生态成熟

- **更多内核功能**：eBPF 5.20 支持更多内核功能
- **工具链完善**：BCC、bpftrace 工具链完善
- **云原生集成**：Cilium、Falco 等工具在 Kubernetes 中的广泛应用

### 7.2 cgroup v2 普及

- **默认启用**：所有新 Linux 发行版默认使用 cgroup v2
- **性能提升**：cgroup v2 性能提升 20%
- **统一管理**：CPU、内存、I/O 统一管理

### 7.3 安全增强

- **Landlock 3.0**：增强的文件系统访问控制
- **seccomp 增强**：支持更细粒度的系统调用过滤
- **机密计算支持**：KVM 6.9 增强的机密计算支持

---

## 8. 参考资源

- **Linux Kernel Documentation**：Linux 内核文档
- **KVM Documentation**：KVM 虚拟化文档
- **eBPF Documentation**：eBPF 编程文档
- **cgroup v2 Documentation**：cgroup v2 资源控制文档

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md`
Hypervisor/Kernel 层部分
