# 物理资源模型与权衡

## 📑 目录

- [物理资源模型与权衡](#物理资源模型与权衡)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
  - [2 CPU 资源模型与权衡](#2-cpu-资源模型与权衡)
    - [2.1 CPU 调度模型对比](#21-cpu-调度模型对比)
    - [2.2 CPU 开销数学模型](#22-cpu-开销数学模型)
      - [虚拟化 CPU 开销模型](#虚拟化-cpu-开销模型)
      - [半虚拟化 CPU 开销模型](#半虚拟化-cpu-开销模型)
      - [容器化 CPU 开销模型](#容器化-cpu-开销模型)
      - [沙盒化 CPU 开销模型](#沙盒化-cpu-开销模型)
    - [2.3 CPU 资源权衡决策](#23-cpu-资源权衡决策)
  - [3 内存资源模型与权衡](#3-内存资源模型与权衡)
    - [3.1 内存管理模型对比](#31-内存管理模型对比)
    - [3.2 内存开销数学模型](#32-内存开销数学模型)
      - [虚拟化内存开销模型](#虚拟化内存开销模型)
      - [半虚拟化内存开销模型](#半虚拟化内存开销模型)
      - [容器化内存开销模型](#容器化内存开销模型)
      - [沙盒化内存开销模型](#沙盒化内存开销模型)
    - [3.3 内存资源权衡决策](#33-内存资源权衡决策)
  - [4 IO 资源模型与权衡](#4-io-资源模型与权衡)
    - [4.1 IO 模型对比](#41-io-模型对比)
    - [4.2 IO 性能模型](#42-io-性能模型)
      - [虚拟化 IO 性能](#虚拟化-io-性能)
      - [半虚拟化 IO 性能](#半虚拟化-io-性能)
      - [容器化 IO 性能](#容器化-io-性能)
      - [沙盒化 IO 性能](#沙盒化-io-性能)
    - [4.3 IO 资源权衡决策](#43-io-资源权衡决策)
  - [5 网络资源模型与权衡](#5-网络资源模型与权衡)
    - [5.1 网络模型对比](#51-网络模型对比)
    - [5.2 网络延迟模型](#52-网络延迟模型)
      - [虚拟化网络延迟](#虚拟化网络延迟)
      - [半虚拟化网络延迟](#半虚拟化网络延迟)
      - [容器化网络延迟](#容器化网络延迟)
      - [沙盒化网络延迟](#沙盒化网络延迟)
    - [5.3 网络资源权衡决策](#53-网络资源权衡决策)
  - [6 存储资源模型与权衡](#6-存储资源模型与权衡)
    - [6.1 存储模型对比](#61-存储模型对比)
    - [6.2 存储 IO 模型](#62-存储-io-模型)
    - [6.3 存储资源权衡决策](#63-存储资源权衡决策)
  - [7 综合资源权衡决策矩阵](#7-综合资源权衡决策矩阵)
  - [8 参考](#8-参考)

---

## 1 概述

**物理资源是技术选择的根本约束**。虚拟化、容器化、沙盒化的差异本质上来自于对物理
资源的不同使用方式。

本文档深入分析 CPU、内存、IO、网络、存储等物理资源的权衡模型，提供数学模型和决策
依据。

**核心问题**：

- 为什么虚拟化、容器化、沙盒化在资源利用率上有差异？
- 不同范式对 CPU、内存、IO、网络、存储的影响是什么？
- 如何根据资源约束选择合适的技术范式？

---

## 2 CPU 资源模型与权衡

### 2.1 CPU 调度模型对比

**CPU 调度模型**是虚拟化、容器化、沙盒化的核心差异之一。

| 范式         | CPU 调度模型                      | 上下文切换开销          | CPU 利用率 | 开销来源                          |
| ------------ | --------------------------------- | ----------------------- | ---------- | --------------------------------- |
| **虚拟化**   | 两级调度（Hypervisor + Guest OS） | 高（> 1000 cycles）     | 70-80%     | 特权指令陷阱、VM Exit             |
| **半虚拟化** | 协作调度（Hypervisor + Guest OS） | 中高（800-1200 cycles） | 75-85%     | Hypercall、协作优化、减少 VM Exit |
| **容器化**   | 单级调度（Host OS）               | 中（~500 cycles）       | 85-95%     | Namespace 切换、Cgroup 更新       |
| **沙盒化**   | 应用级调度（Runtime）             | 低（< 100 cycles）      | 90-98%     | 函数调用、轻量隔离                |

**CPU 调度路径对比**：

1. **虚拟化（全虚拟化）**：

   ```text
   Guest App → Guest Kernel → Hypervisor → Host Kernel → CPU
   ```

   - **两级调度**：Guest OS 调度 + Hypervisor 调度
   - **VM Exit**：特权指令触发 VM Exit，切换到 Hypervisor
   - **开销**：上下文切换开销高（> 1000 CPU cycles）

2. **半虚拟化**：

   ```text
   Guest App → Guest Kernel (Hypercall) → Hypervisor → Host Kernel → CPU
   ```

   - **协作调度**：Guest OS 通过 Hypercall 与 Hypervisor 协作
   - **Hypercall**：Guest OS 直接调用 Hypervisor 接口，减少 VM Exit
   - **开销**：上下文切换开销中高（800-1200 CPU cycles，通过协作优化减少）

3. **容器化**：

   ```text
   Container App → Host Kernel → CPU
   ```

   - **单级调度**：Host OS 统一调度
   - **Namespace**：进程在隔离的 Namespace 中运行
   - **开销**：上下文切换开销中等（~500 CPU cycles）

4. **沙盒化**：

   ```text
   Wasm Module → Runtime → Host Kernel → CPU
   ```

   - **应用级调度**：Runtime 直接调度
   - **轻量隔离**：函数调用级别的隔离
   - **开销**：上下文切换开销低（< 100 CPU cycles）

### 2.2 CPU 开销数学模型

**CPU 开销通用模型**：

设 CPU 总开销为 $C_{\text{total}}$，则：

$$C_{\text{total}} = C_{\text{workload}} + C_{\text{isolation}} + C_{\text{overhead}}$$

其中：

- $C_{\text{workload}}$：工作负载 CPU 开销
- $C_{\text{isolation}}$：隔离机制 CPU 开销
- $C_{\text{overhead}}$：管理开销

**各范式 CPU 开销模型**：

#### 虚拟化 CPU 开销模型

$$C_{\text{VM}} = C_{\text{workload}} + C_{\text{vmexit}} + C_{\text{emulation}} + C_{\text{hypervisor}}$$

其中：

- $C_{\text{vmexit}}$：VM Exit 开销（特权指令陷阱）
  - 触发频率：约每 1000 条指令触发 1 次
  - 开销：约 1000-5000 CPU cycles
- $C_{\text{emulation}}$：指令模拟开销
  - 不可虚拟化的指令需要 Hypervisor 模拟
  - 开销：约 100-500 CPU cycles/指令
- $C_{\text{hypervisor}}$：Hypervisor 调度开销
  - 虚拟 CPU 调度开销
  - 开销：约 50-200 CPU cycles

**虚拟化 CPU 利用率**：

$$\text{CPU}_{\text{utilization}} = \frac{C_{\text{workload}}}{C_{\text{VM}}} \approx 70-80\%$$

#### 半虚拟化 CPU 开销模型

$$C_{\text{PV}} = C_{\text{workload}} + C_{\text{hypercall}} + C_{\text{collaboration}} + C_{\text{hypervisor}}$$

其中：

- $C_{\text{hypercall}}$：Hypercall 开销（协作接口）
  - Guest OS 通过 Hypercall 调用 Hypervisor，减少 VM Exit
  - 开销：约 100-300 CPU cycles（比 VM Exit 低）
- $C_{\text{collaboration}}$：协作优化开销
  - 前端/后端驱动协作，减少模拟开销
  - 开销：约 50-150 CPU cycles
- $C_{\text{hypervisor}}$：Hypervisor 调度开销
  - 虚拟 CPU 调度开销（类似全虚拟化）
  - 开销：约 50-200 CPU cycles

**半虚拟化 CPU 利用率**：

$$\text{CPU}_{\text{utilization}} = \frac{C_{\text{workload}}}{C_{\text{PV}}} \approx 75-85\%$$

#### 容器化 CPU 开销模型

$$C_{\text{Container}} = C_{\text{workload}} + C_{\text{namespace}} + C_{\text{cgroup}} + C_{\text{runtime}}$$

其中：

- $C_{\text{namespace}}$：Namespace 切换开销
  - 进程在不同 Namespace 间切换
  - 开销：约 10-50 CPU cycles
- $C_{\text{cgroup}}$：Cgroup 更新开销
  - 资源限制更新开销
  - 开销：约 5-20 CPU cycles
- $C_{\text{runtime}}$：容器运行时开销
  - containerd、runc 等运行时开销
  - 开销：约 10-30 CPU cycles

**容器化 CPU 利用率**：

$$\text{CPU}_{\text{utilization}} = \frac{C_{\text{workload}}}{C_{\text{Container}}} \approx 85-95\%$$

#### 沙盒化 CPU 开销模型

$$C_{\text{Sandbox}} = C_{\text{workload}} + C_{\text{runtime}} + C_{\text{syscall}}$$

其中：

- $C_{\text{runtime}}$：运行时开销（最小化）
  - WasmEdge、Wasmtime 等运行时开销
  - 开销：约 5-15 CPU cycles
- $C_{\text{syscall}}$：系统调用拦截开销
  - WASI 系统调用拦截（函数调用）
  - 开销：约 1-5 CPU cycles

**沙盒化 CPU 利用率**：

$$\text{CPU}_{\text{utilization}} = \frac{C_{\text{workload}}}{C_{\text{Sandbox}}} \approx 90-98\%$$

### 2.3 CPU 资源权衡决策

**决策规则**：

- **CPU 密集型应用** → 容器化（CPU 利用率 85-95%，开销适中）
- **低延迟要求** → 沙盒化（上下文切换快，< 100 cycles）
- **多 OS 需求 + 高性能** → 半虚拟化（CPU 利用率 75-85%，协作优化）
- **多 OS 需求** → 虚拟化（需要 Guest OS，可接受 CPU 开销）

**量化对比**：

| 场景           | 推荐范式 | CPU 利用率 | 上下文切换开销  | 理由                      |
| -------------- | -------- | ---------- | --------------- | ------------------------- |
| CPU 密集型     | 容器化   | 85-95%     | ~500 cycles     | 平衡性能与开销            |
| 低延迟关键     | 沙盒化   | 90-98%     | < 100 cycles    | 最快响应                  |
| 多 OS + 高性能 | 半虚拟化 | 75-85%     | 800-1200 cycles | 协作优化，减少 VM Exit    |
| 多 OS 支持     | 虚拟化   | 70-80%     | > 1000 cycles   | 唯一支持多 OS（无需修改） |
| 资源受限       | 沙盒化   | 90-98%     | < 100 cycles    | 最高资源利用率            |
| 大规模部署     | 容器化   | 85-95%     | ~500 cycles     | 平衡性能与成本            |

---

## 3 内存资源模型与权衡

### 3.1 内存管理模型对比

**内存管理模型**决定了不同范式的内存开销和共享机制。

| 范式         | 内存模型     | 内存开销              | 共享机制                | 隔离粒度           |
| ------------ | ------------ | --------------------- | ----------------------- | ------------------ |
| **虚拟化**   | 独立物理内存 | 高（Guest OS + 应用） | 无（完全隔离）          | 物理内存页         |
| **半虚拟化** | 协作物理内存 | 高（Guest OS + 应用） | 共享内存（Grant Table） | 物理内存页（协作） |
| **容器化**   | 共享内核内存 | 中（仅应用内存）      | 内核内存、文件系统      | 进程地址空间       |
| **沙盒化**   | 应用级内存   | 低（仅运行时）        | 共享主机内存            | 应用内存空间       |

**内存路径对比**：

1. **虚拟化（全虚拟化）**：

   ```text
   Guest App → Guest Memory → Hypervisor → Host Memory → Physical Memory
   ```

   - **独立物理内存**：每个 VM 分配独立的物理内存页
   - **Guest OS 开销**：每个 VM 需要运行完整的 Guest OS（通常 256MB-2GB）
   - **无内存共享**：VM 之间完全隔离，无法共享内存

2. **半虚拟化**：

   ```text
   Guest App → Guest Memory (Grant Table) → Hypervisor → Host Memory → Physical Memory
   ```

   - **协作物理内存**：通过 Grant Table 机制共享内存页
   - **Guest OS 开销**：每个 VM 需要运行完整的 Guest OS（通常 256MB-2GB）
   - **共享内存**：通过 Grant Table 实现 Guest OS 与 Hypervisor 之间的内存共享
   - **内存效率**：通过协作机制优化内存访问，减少内存复制开销

3. **容器化**：

   ```text
   Container App → Process Address Space → Host Kernel → Physical Memory
   ```

   - **共享内核内存**：多个容器共享 Host 内核内存
   - **进程地址空间隔离**：每个容器有独立的进程地址空间
   - **内存共享**：可以共享只读文件系统、共享库等

4. **沙盒化**：

   ```text
   Wasm Module → Runtime Memory → Host Memory → Physical Memory
   ```

   - **应用级内存**：仅包含 Wasm 模块内存和运行时内存
   - **零 rootfs**：无需文件系统镜像
   - **内存共享**：共享主机内存，最小内存占用

### 3.2 内存开销数学模型

**内存开销通用模型**：

设总内存开销为 $M_{\text{total}}$，则：

$$M_{\text{total}} = M_{\text{workload}} + M_{\text{isolation}} + M_{\text{overhead}}$$

其中：

- $M_{\text{workload}}$：工作负载内存开销
- $M_{\text{isolation}}$：隔离机制内存开销
- $M_{\text{overhead}}$：管理开销

**各范式内存开销模型**：

#### 虚拟化内存开销模型

$$M_{\text{VM}} = M_{\text{guest\_os}} + M_{\text{workload}} + M_{\text{hypervisor}}$$

其中：

- $M_{\text{guest\_os}}$：Guest OS 内存（通常 256MB-2GB）
  - 最小化 Linux 发行版：256MB-512MB
  - 标准 Linux 发行版：512MB-2GB
  - Windows 系统：2GB-4GB
- $M_{\text{workload}}$：工作负载内存
- $M_{\text{hypervisor}}$：Hypervisor 开销（通常 < 100MB）

**虚拟化内存开销示例**：

- **最小 VM**：Guest OS (256MB) + Workload (128MB) + Hypervisor (50MB) =
  **434MB**
- **标准 VM**：Guest OS (1GB) + Workload (512MB) + Hypervisor (100MB) =
  **1.6GB**

#### 半虚拟化内存开销模型

$$M_{\text{PV}} = M_{\text{guest\_os}} + M_{\text{workload}} + M_{\text{hypervisor}} + M_{\text{grant\_table}}$$

其中：

- $M_{\text{guest\_os}}$：Guest OS 内存（通常 256MB-2GB，类似全虚拟化）
- $M_{\text{workload}}$：工作负载内存
- $M_{\text{hypervisor}}$：Hypervisor 开销（通常 < 100MB）
- $M_{\text{grant\_table}}$：Grant Table 开销（内存共享机制，通常 < 10MB）

**半虚拟化内存开销示例**：

- **最小 PV VM**：Guest OS (256MB) + Workload (128MB) + Hypervisor (50MB) +
  Grant Table (5MB) = **439MB**
- **标准 PV VM**：Guest OS (1GB) + Workload (512MB) + Hypervisor (100MB) + Grant
  Table (10MB) = **1.62GB**

**内存效率**：通过 Grant Table 机制，可以减少内存复制开销，提高 IO 性能（约
10-20% 提升）

#### 容器化内存开销模型

$$M_{\text{Container}} = M_{\text{workload}} + M_{\text{namespace}} + M_{\text{runtime}}$$

其中：

- $M_{\text{workload}}$：工作负载内存（主要开销）
- $M_{\text{namespace}}$：Namespace 开销（可忽略，通常 < 1MB）
- $M_{\text{runtime}}$：运行时开销（通常 < 50MB）

**容器化内存开销示例**：

- **最小容器**：Workload (128MB) + Runtime (20MB) = **148MB**
- **标准容器**：Workload (512MB) + Runtime (50MB) = **562MB**

#### 沙盒化内存开销模型

$$M_{\text{Wasm}} = M_{\text{wasm\_module}} + M_{\text{runtime}} + M_{\text{memory}}$$

其中：

- $M_{\text{wasm\_module}}$：Wasm 模块内存（通常 < 10MB）
  - 编译后的 Wasm 二进制文件
  - 通常只有几百 KB 到几 MB
- $M_{\text{runtime}}$：运行时开销（通常 < 10MB）
  - WasmEdge、Wasmtime 等运行时
  - 通常 < 10MB
- $M_{\text{memory}}$：线性内存（按需分配）
  - Wasm 线性内存，按需分配
  - 默认 64KB，可扩展

**沙盒化内存开销示例**：

- **最小 Wasm**：Module (2MB) + Runtime (5MB) + Memory (64KB) = **约 7MB**
- **标准 Wasm**：Module (5MB) + Runtime (10MB) + Memory (1MB) = **约 16MB**

**内存开销对比**：

| 范式         | 最小内存开销 | 标准内存开销 | 内存效率             |
| ------------ | ------------ | ------------ | -------------------- |
| **虚拟化**   | 434MB        | 1.6GB        | 低                   |
| **半虚拟化** | 439MB        | 1.62GB       | 低（但 IO 性能优化） |
| **容器化**   | 148MB        | 562MB        | 中                   |
| **沙盒化**   | 7MB          | 16MB         | 极高                 |

### 3.3 内存资源权衡决策

**决策规则**：

- **内存受限场景** → 沙盒化（内存开销最小，7-16MB）
- **资源充足场景** → 虚拟化（强隔离，可接受内存开销）
- **资源共享场景** → 容器化（内存共享，平衡开销与隔离）

**量化对比**：

| 场景       | 推荐范式 | 内存开销 | 内存共享 | 理由               |
| ---------- | -------- | -------- | -------- | ------------------ |
| 内存受限   | 沙盒化   | 7-16MB   | 共享     | 最小内存占用       |
| 资源充足   | 虚拟化   | 434MB+   | 无       | 强隔离，可接受开销 |
| 资源共享   | 容器化   | 148MB+   | 部分共享 | 平衡开销与隔离     |
| 大规模部署 | 容器化   | 148MB+   | 部分共享 | 成本效益高         |
| 极致轻量   | 沙盒化   | 7-16MB   | 共享     | 最小资源占用       |

---

## 4 IO 资源模型与权衡

### 4.1 IO 模型对比

**IO 模型**决定了不同范式的 IO 性能和开销。

| 范式       | IO 模型            | IO 开销 | 虚拟化层              | 性能损失 |
| ---------- | ------------------ | ------- | --------------------- | -------- |
| **虚拟化** | 虚拟设备（VirtIO） | 高      | Hypervisor + Guest OS | 10-30%   |
| **容器化** | 直接 IO（syscall） | 低      | Host OS               | < 5%     |
| **沙盒化** | 拦截 IO（WASI）    | 极低    | Runtime 拦截          | < 1%     |

**IO 路径对比**：

1. **虚拟化（全虚拟化）**：

   ```text
   Guest App → Guest Kernel → 模拟设备 → Hypervisor → Host Kernel → Hardware
   ```

   - **设备模拟**：完全模拟硬件设备，需要 Hypervisor 拦截所有 IO
   - **IO 拦截**：所有 IO 请求都需要经过 Hypervisor 模拟
   - **上下文切换**：Guest → Hypervisor → Host
   - **性能损失**：10-30%

2. **半虚拟化**：

   ```text
   Guest App → Guest Kernel (前端驱动) → VirtIO/PV → Hypervisor (后端驱动) → Host Kernel → Hardware
   ```

   - **前端/后端驱动**：Guest OS 前端驱动与 Hypervisor 后端驱动协作
   - **VirtIO 或 PV 驱动**：通过 Hypercall 和共享内存减少 IO 拦截开销
   - **协作优化**：减少设备模拟开销，提高 IO 性能
   - **上下文切换**：Guest (Hypercall) → Hypervisor → Host
   - **性能损失**：5-15%（相比全虚拟化性能提升约 50%）

3. **容器化**：

   ```text
   Container App → Host Kernel → Hardware
   ```

   - **直接 IO**：直接系统调用，无需虚拟化
   - **Namespace 过滤**：仅过滤 Namespace
   - **上下文切换**：Container → Host
   - **性能损失**：< 5%

4. **沙盒化**：

   ```text
   Wasm Module → WASI Runtime → Host Kernel → Hardware
   ```

   - **WASI 拦截**：系统调用拦截（函数调用）
   - **轻量拦截**：无需虚拟化，仅函数调用
   - **上下文切换**：Wasm → Host（函数调用）
   - **性能损失**：< 1%

### 4.2 IO 性能模型

**IO 性能通用模型**：

设 IO 性能为 $P_{\text{io}}$，则：

$$P_{\text{io}} = \frac{\text{IO Throughput}}{\text{IO Latency}}$$

其中：

- **IO Throughput**：IO 吞吐量（MB/s 或 IOPS）
- **IO Latency**：IO 延迟（ms）

**各范式 IO 性能模型**：

#### 虚拟化 IO 性能

$$P_{\text{VM\_io}} = \frac{T_{\text{raw}} \times (1 - L_{\text{vm}})}{L_{\text{raw}} + L_{\text{vm}} + L_{\text{emulation}}}$$

其中：

- $T_{\text{raw}}$：原始 IO 吞吐量
- $L_{\text{raw}}$：原始 IO 延迟
- $L_{\text{vm}}$：VM Exit 延迟（约 10-50μs）
- $L_{\text{emulation}}$：设备模拟延迟（约 5-20μs）

**性能损失**：约 10-30%

#### 半虚拟化 IO 性能

$$P_{\text{PV\_io}} = \frac{T_{\text{raw}} \times (1 - L_{\text{pv}})}{L_{\text{raw}} + L_{\text{hypercall}} + L_{\text{collaboration}}}$$

其中：

- $T_{\text{raw}}$：原始 IO 吞吐量
- $L_{\text{raw}}$：原始 IO 延迟
- $L_{\text{hypercall}}$：Hypercall 延迟（约 1-5μs，比 VM Exit 低）
- $L_{\text{collaboration}}$：协作延迟（前端/后端驱动协作，约 2-8μs）

**性能损失**：约 5-15%（相比全虚拟化性能提升约 50%）

#### 容器化 IO 性能

$$P_{\text{Container\_io}} = \frac{T_{\text{raw}} \times (1 - L_{\text{container}})}{L_{\text{raw}} + L_{\text{namespace}}}$$

其中：

- $L_{\text{container}}$：容器开销（约 1-3%）
- $L_{\text{namespace}}$：Namespace 过滤延迟（约 0.1-1μs）

**性能损失**：< 5%

#### 沙盒化 IO 性能

$$P_{\text{Wasm\_io}} = \frac{T_{\text{raw}} \times (1 - L_{\text{wasm}})}{L_{\text{raw}} + L_{\text{wasi}}}$$

其中：

- $L_{\text{wasm}}$：Wasm 运行时开销（约 0.1-0.5%）
- $L_{\text{wasi}}$：WASI 拦截延迟（< 0.1μs，函数调用）

**性能损失**：< 1%

**IO 性能对比**：

| 范式         | IO 吞吐量损失 | IO 延迟增加 | 总体性能损失 |
| ------------ | ------------- | ----------- | ------------ |
| **虚拟化**   | 10-30%        | 10-50μs     | 10-30%       |
| **半虚拟化** | 5-15%         | 3-13μs      | 5-15%        |
| **容器化**   | < 5%          | 0.1-1μs     | < 5%         |
| **沙盒化**   | < 1%          | < 0.1μs     | < 1%         |

### 4.3 IO 资源权衡决策

**决策规则**：

- **高 IO 性能要求** → 沙盒化（IO 路径最短，性能损失 < 1%）
- **IO 密集型应用** → 容器化（性能损失小，< 5%）
- **多设备支持** → 虚拟化（设备虚拟化，可接受性能损失）

**量化对比**：

| 场景       | 推荐范式 | IO 性能损失 | 理由             |
| ---------- | -------- | ----------- | ---------------- |
| 高 IO 性能 | 沙盒化   | < 1%        | 最小性能损失     |
| IO 密集型  | 容器化   | < 5%        | 性能与兼容性平衡 |
| 多设备支持 | 虚拟化   | 10-30%      | 设备虚拟化支持   |
| 极致性能   | 沙盒化   | < 1%        | 最优 IO 性能     |

---

## 5 网络资源模型与权衡

### 5.1 网络模型对比

**网络模型**决定了不同范式的网络延迟和吞吐量。

| 范式         | 网络模型                   | 网络开销 | 虚拟化层                   | 延迟开销 |
| ------------ | -------------------------- | -------- | -------------------------- | -------- |
| **虚拟化**   | 虚拟网卡（模拟网卡）       | 高       | Hypervisor + Guest OS      | 10-50μs  |
| **半虚拟化** | 半虚拟化网卡（VirtIO Net） | 中高     | Hypervisor + Guest OS 协作 | 5-25μs   |
| **容器化**   | 网络 Namespace             | 中       | Host OS Network Stack      | 1-10μs   |
| **沙盒化**   | Socket 拦截                | 低       | Runtime + Host OS          | < 1μs    |

**网络路径对比**：

1. **虚拟化**：

   ```text
   Guest App → Guest Kernel → vNIC → Hypervisor → Host Kernel → Network
   ```

   - **虚拟网卡**：需要 Hypervisor 虚拟化网卡
   - **网络栈**：Guest OS 和 Host OS 两层网络栈
   - **延迟开销**：10-50μs

2. **容器化**：

   ```text
   Container App → Host Kernel → Network
   ```

   - **网络 Namespace**：进程级别的网络隔离
   - **单层网络栈**：共享 Host OS 网络栈
   - **延迟开销**：1-10μs

3. **沙盒化**：

   ```text
   Wasm Module → WASI Socket → Host Kernel → Network
   ```

   - **Socket 拦截**：WASI socket 函数调用拦截
   - **轻量拦截**：函数调用级别，无虚拟化
   - **延迟开销**：< 1μs

### 5.2 网络延迟模型

**网络延迟通用模型**：

设网络延迟为 $L_{\text{net}}$，则：

$$L_{\text{net}} = L_{\text{hardware}} + L_{\text{software}} + L_{\text{isolation}}$$

其中：

- $L_{\text{hardware}}$：硬件延迟（物理网络）
- $L_{\text{software}}$：软件栈延迟（内核、协议栈）
- $L_{\text{isolation}}$：隔离层延迟（虚拟化开销）

**各范式网络延迟模型**：

#### 虚拟化网络延迟

$$L_{\text{VM}} = L_{\text{hardware}} + L_{\text{host\_kernel}} + L_{\text{hypervisor}} + L_{\text{guest\_kernel}}$$

其中：

- $L_{\text{hypervisor}}$：Hypervisor 网络虚拟化（10-30μs）
- $L_{\text{guest\_kernel}}$：Guest OS 网络栈（5-10μs）

**总延迟开销**：15-40μs

#### 半虚拟化网络延迟

$$L_{\text{PV}} = L_{\text{hardware}} + L_{\text{host\_kernel}} + L_{\text{hypervisor}} + L_{\text{hypercall}} + L_{\text{guest\_kernel}}$$

其中：

- $L_{\text{hypervisor}}$：Hypervisor 网络虚拟化（5-15μs，通过 VirtIO 优化）
- $L_{\text{hypercall}}$：Hypercall 延迟（1-3μs，比 VM Exit 低）
- $L_{\text{guest\_kernel}}$：Guest OS 网络栈（5-10μs）

**总延迟开销**：11-28μs（相比全虚拟化减少约 30-50%）

#### 容器化网络延迟

$$L_{\text{Container}} = L_{\text{hardware}} + L_{\text{host\_kernel}} + L_{\text{namespace}}$$

其中：

- $L_{\text{namespace}}$：Namespace 过滤（1-5μs）

**总延迟开销**：1-5μs

#### 沙盒化网络延迟

$$L_{\text{Wasm}} = L_{\text{hardware}} + L_{\text{host\_kernel}} + L_{\text{wasi}}$$

其中：

- $L_{\text{wasi}}$：WASI socket 拦截（< 1μs，函数调用）

**总延迟开销**：< 1μs

**网络延迟对比**：

| 范式         | 延迟开销 | 网络吞吐量损失 | 总体性能 |
| ------------ | -------- | -------------- | -------- |
| **虚拟化**   | 15-40μs  | 10-20%         | 中等     |
| **半虚拟化** | 11-28μs  | 5-12%          | 中高     |
| **容器化**   | 1-5μs    | < 5%           | 较高     |
| **沙盒化**   | < 1μs    | < 1%           | 最高     |

### 5.3 网络资源权衡决策

**决策规则**：

- **低延迟要求** → 沙盒化（延迟最小，< 1μs）
- **网络密集型** → 容器化（性能损失小，1-5μs）
- **多网卡支持** → 虚拟化（虚拟网卡，可接受延迟）

**量化对比**：

| 场景       | 推荐范式 | 延迟开销 | 理由             |
| ---------- | -------- | -------- | ---------------- |
| 低延迟关键 | 沙盒化   | < 1μs    | 最小延迟         |
| 网络密集型 | 容器化   | 1-5μs    | 性能与兼容性平衡 |
| 多网卡支持 | 虚拟化   | 15-40μs  | 设备虚拟化支持   |

---

## 6 存储资源模型与权衡

### 6.1 存储模型对比

**存储模型**决定了不同范式的存储 IO 性能和开销。

| 范式       | 存储模型            | 存储开销         | 共享机制    | IO 性能 |
| ---------- | ------------------- | ---------------- | ----------- | ------- |
| **虚拟化** | 虚拟磁盘（VirtIO）  | 高（Guest FS）   | 无          | 中等    |
| **容器化** | 镜像层（OverlayFS） | 中（层共享）     | 镜像层共享  | 较高    |
| **沙盒化** | 零 rootfs           | 低（无文件系统） | 共享主机 FS | 最高    |

**存储路径对比**：

1. **虚拟化**：

   ```text
   Guest App → Guest FS → VirtIO Block → Hypervisor → Host FS → Hardware
   ```

   - **虚拟磁盘**：VirtIO Block 设备虚拟化
   - **文件系统虚拟化**：Guest 文件系统 + Host 文件系统
   - **性能损失**：15-25%

2. **容器化**：

   ```text
   Container App → OverlayFS → Host FS → Hardware
   ```

   - **镜像层**：OverlayFS 联合文件系统
   - **层共享**：多个容器共享镜像层
   - **性能损失**：5-10%

3. **沙盒化**：

   ```text
   Wasm Module → WASI FS → Host FS → Hardware
   ```

   - **零 rootfs**：无需文件系统镜像
   - **WASI FS**：直接访问主机文件系统
   - **性能损失**：< 2%

### 6.2 存储 IO 模型

**存储 IO 通用模型**：

设存储 IO 性能为 $P_{\text{storage}}$，则：

$$P_{\text{storage}} = \frac{\text{IOPS} \times \text{Throughput}}{\text{Latency}}$$

其中：

- **IOPS**：每秒 IO 操作数
- **Throughput**：吞吐量（MB/s）
- **Latency**：延迟（ms）

**各范式存储性能**：

| 范式       | IOPS 损失 | 吞吐量损失 | 延迟增加 | 总体性能损失 |
| ---------- | --------- | ---------- | -------- | ------------ |
| **虚拟化** | 15-25%    | 15-25%     | 10-30μs  | 15-25%       |
| **容器化** | 5-10%     | 5-10%      | 1-5μs    | 5-10%        |
| **沙盒化** | < 2%      | < 2%       | < 1μs    | < 2%         |

### 6.3 存储资源权衡决策

**决策规则**：

- **高 IOPS 要求** → 沙盒化（存储路径最短，性能损失 < 2%）
- **镜像共享需求** → 容器化（镜像层共享，性能损失 5-10%）
- **多文件系统** → 虚拟化（支持任意 Guest FS，可接受性能损失）

**量化对比**：

| 场景         | 推荐范式 | 存储性能损失 | 理由           |
| ------------ | -------- | ------------ | -------------- |
| 高 IOPS 要求 | 沙盒化   | < 2%         | 最优存储性能   |
| 镜像共享     | 容器化   | 5-10%        | 镜像层共享优势 |
| 多文件系统   | 虚拟化   | 15-25%       | 设备虚拟化支持 |

---

## 7 综合资源权衡决策矩阵

**综合资源权衡矩阵**：

| 资源维度       | 虚拟化             | 半虚拟化                | 容器化            | 沙盒化           | 最佳选择 |
| -------------- | ------------------ | ----------------------- | ----------------- | ---------------- | -------- |
| **CPU 利用率** | 70-80%             | 75-85%                  | 85-95%            | 90-98%           | 沙盒化   |
| **内存开销**   | 高（+Guest OS）    | 高（+Guest OS + Grant） | 中（仅应用）      | 低（最小）       | 沙盒化   |
| **IO 性能**    | 中等（10-30%损失） | 中高（5-15%损失）       | 较高（< 5%损失）  | 最高（< 1%损失） | 沙盒化   |
| **网络延迟**   | 高（10-50μs）      | 中高（11-28μs）         | 中（1-10μs）      | 低（< 1μs）      | 沙盒化   |
| **存储 IO**    | 中等（15-25%损失） | 中高（8-18%损失）       | 较高（5-10%损失） | 最高（< 2%损失） | 沙盒化   |
| **隔离强度**   | 最高（硬件级）     | 高（内核级）            | 中等（进程级）    | 较低（应用级）   | 虚拟化   |
| **兼容性**     | 最高（多 OS）      | 高（需修改 Guest OS）   | 高（Linux）       | 低（应用特定）   | 虚拟化   |

**资源权衡决策规则**：

```text
if 资源受限 and 性能要求高:
    return 沙盒化
elif 隔离要求高 and 兼容性要求高 and Guest OS 可修改:
    return 半虚拟化（性能优于全虚拟化）
elif 隔离要求高 and 兼容性要求高:
    return 虚拟化（全虚拟化，无需修改 Guest OS）
elif 资源共享需求 and 标准化需求:
    return 容器化
```

---

## 8 参考

**关联文档**：

- **[隔离模型](02-isolation-models.md)** - 隔离机制理论模型
- **[安全模型](03-security-models.md)** - 安全机制理论模型
- **[分布式系统模型](04-distributed-models.md)** - 分布式系统理论模型
- **[主文档](../decision-models.md)** - 完整技术决策模型文档

**外部参考**：

- [CPU Virtualization](https://en.wikipedia.org/wiki/Hardware_virtualization)
- [Memory Management](https://en.wikipedia.org/wiki/Memory_management)
- [IO Virtualization](https://en.wikipedia.org/wiki/Input/output_virtualization)
- [Network Virtualization](https://en.wikipedia.org/wiki/Network_virtualization)

---

---

## 2025 年最新实践

### 物理资源模型应用最佳实践（2025）

**2025 年趋势**：物理资源模型在资源优化和性能分析中的深度应用

**实践要点**：

- **资源建模**：使用物理资源模型进行资源建模和优化
- **性能分析**：使用数学模型进行性能分析和预测
- **权衡决策**：使用权衡决策矩阵进行资源权衡

**代码示例**：

```python
# 2025 年物理资源模型工具
class ResourceModelTool:
    def __init__(self):
        self.cpu_model = CPUResourceModel()
        self.memory_model = MemoryResourceModel()
        self.io_model = IOResourceModel()
        self.network_model = NetworkResourceModel()

    def model_resources(self, workload_config):
        """资源建模"""
        cpu_usage = self.cpu_model.model(workload_config)
        memory_usage = self.memory_model.model(workload_config)
        io_usage = self.io_model.model(workload_config)
        network_usage = self.network_model.model(workload_config)

        return {
            'cpu': cpu_usage,
            'memory': memory_usage,
            'io': io_usage,
            'network': network_usage
        }

    def analyze_performance(self, resource_model):
        """性能分析"""
        return self.cpu_model.analyze_performance(resource_model)

    def make_tradeoff(self, requirements):
        """权衡决策"""
        return self.cpu_model.make_tradeoff(requirements)
```

## 实际应用案例

### 案例 1：资源优化决策（2025）

**场景**：使用物理资源模型进行资源优化决策

**实现方案**：

```python
# 资源优化决策
workload_config = {
    'type': 'container',
    'cpu_requests': '2',
    'memory_requests': '4Gi',
    'io_requirements': 'high',
    'network_requirements': 'medium'
}

tool = ResourceModelTool()
resource_model = tool.model_resources(workload_config)
performance = tool.analyze_performance(resource_model)
tradeoff = tool.make_tradeoff(workload_config)

print(f"资源模型: {resource_model}")
print(f"性能分析: {performance}")
print(f"权衡决策: {tradeoff}")
```

**效果**：

- 资源建模：使用物理资源模型进行资源建模和优化
- 性能分析：使用数学模型进行性能分析和预测
- 权衡决策：使用权衡决策矩阵进行资源权衡

---

**最后更新**：2025-11-15
**文档状态**：✅ 完整 | 📊 包含 2025 年最新趋势
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../../../../TECHNICAL/10-reference-trends/2025-trends/2025-trends.md)
