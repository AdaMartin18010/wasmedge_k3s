# 虚拟化/半虚拟化/容器化/沙盒化严格定义与技术层级分析

## 目录

- [目录](#目录)
- [01. 文档定位](#01-文档定位)
- [02. 严格定义](#02-严格定义)
  - [02.1 虚拟化（Full Virtualization）严格定义](#021-虚拟化full-virtualization严格定义)
  - [02.2 半虚拟化（Para-virtualization）严格定义](#022-半虚拟化para-virtualization严格定义)
  - [02.3 容器化（Containerization）严格定义](#023-容器化containerization严格定义)
  - [02.4 沙盒化（Sandboxing）严格定义](#024-沙盒化sandboxing严格定义)
- [03. 技术层级分析](#03-技术层级分析)
  - [03.1 硬件层技术名称与概念](#031-硬件层技术名称与概念)
  - [03.2 驱动/OS 层技术名称与概念](#032-驱动os-层技术名称与概念)
  - [03.3 OS 层技术名称与概念](#033-os-层技术名称与概念)
  - [03.4 OS 进程内技术名称与概念](#034-os-进程内技术名称与概念)
- [04. 多维度对比矩阵](#04-多维度对比矩阵)
  - [04.1 技术层级对比矩阵](#041-技术层级对比矩阵)
  - [04.2 支持层级对比矩阵](#042-支持层级对比矩阵)
  - [04.3 隔离机制对比矩阵](#043-隔离机制对比矩阵)
  - [04.4 性能特性对比矩阵](#044-性能特性对比矩阵)
  - [04.5 安全性对比矩阵](#045-安全性对比矩阵)
  - [04.6 适用场景对比矩阵](#046-适用场景对比矩阵)
- [05. 技术层级思维导图](#05-技术层级思维导图)
  - [05.1 技术层级关系图](#051-技术层级关系图)
  - [05.2 支持层级关系图](#052-支持层级关系图)
  - [05.3 技术栈分层图](#053-技术栈分层图)
- [06. 参考](#06-参考)

---

## 01. 文档定位

本文档专门从**技术层级和支持层级**角度，严格定义**虚拟化（全虚拟化）、半虚拟化、
容器化、沙盒化**四个技术范式，提供各层级的技术名称、概念、多维度对比矩阵和思维导
图，明确区分各范式的技术边界和支持范围。

**核心内容**：

1. **严格定义**：从技术层级和支持层级角度严格定义四个技术范式
2. **技术层级分析**：硬件层、驱动/OS 层、OS 层、OS 进程内各层级的技术名称和概念
3. **多维度对比矩阵**：技术层级、支持层级、隔离机制、性能特性、安全性、适用场景
   等维度的对比
4. **技术层级思维导图**：技术层级关系图、支持层级关系图、技术栈分层图

**关键区分**：

- **虚拟化（全虚拟化）**：硬件支持的复用（硬件层虚拟化）
- **半虚拟化**：硬件 + 驱动/OS 支持的复用（硬件层虚拟化 + 驱动/OS 层协作）
- **容器化**：OS 支持的复用（操作系统层虚拟化）
- **沙盒化**：OS 进程内支持的复用（应用层隔离）

---

## 02. 严格定义

### 02.1 虚拟化（Full Virtualization）严格定义

**虚拟化（Full Virtualization）严格定义**：

虚拟化（全虚拟化）是一种**硬件支持的复用**技术，通过在物理硬件之上创建
Hypervisor 层，将物理硬件资源抽象为虚拟硬件资源，允许多个虚拟机（VM）完全独立地
运行在物理硬件上。

**关键特征**：

1. **支持层级**：**硬件层**（Hardware Layer）

   - **硬件虚拟化支持**：Intel VT-x、AMD-V 等硬件虚拟化扩展
   - **不需要 Guest OS 修改**：Guest OS 无需感知虚拟化环境
   - **硬件指令直接执行**：部分指令直接在硬件上执行，特权指令通过 Hypervisor 拦
     截

2. **技术层级**：**硬件抽象层**（Hardware Abstraction Layer）

   - **Hypervisor（虚拟机监控器）**：运行在硬件之上，管理虚拟硬件资源
   - **虚拟硬件**：虚拟 CPU、虚拟内存、虚拟 IO 设备
   - **Guest OS**：运行在虚拟硬件上的完整操作系统

3. **隔离级别**：**硬件级隔离**（Hardware-Level Isolation）

   - **隔离边界**：物理硬件边界
   - **隔离机制**：Hypervisor + 硬件虚拟化扩展
   - **隔离强度**：最强（硬件级完全隔离）

4. **复用机制**：**硬件虚拟化复用**（Hardware Virtualization Multiplexing）
   - **CPU 复用**：多个 vCPU 共享物理 CPU，通过硬件虚拟化扩展实现
   - **内存复用**：多个虚拟机共享物理内存，通过 EPT/NPT 实现内存虚拟化
   - **IO 复用**：多个虚拟机共享物理 IO 设备，通过虚拟设备实现

**技术实现**：

- **Type 1 Hypervisor（裸机 Hypervisor）**：直接运行在物理硬件上（如 VMware
  ESXi、Xen、Hyper-V）
- **Type 2 Hypervisor（托管 Hypervisor）**：运行在 Host OS 之上（如 VMware
  Workstation、VirtualBox、QEMU）
- **硬件辅助虚拟化**：Intel VT-x、AMD-V、Intel VT-d（IOMMU）

### 02.2 半虚拟化（Para-virtualization）严格定义

**半虚拟化（Para-virtualization）严格定义**：

半虚拟化是一种**硬件 + 驱动/OS 支持的复用**技术，通过在物理硬件之上创建
Hypervisor 层，并要求 Guest OS 进行修改以配合 Hypervisor，通过协作方式提高虚拟化
性能。

**关键特征**：

1. **支持层级**：**硬件层 + 驱动/OS 层**（Hardware Layer + Driver/OS Layer）

   - **硬件虚拟化支持**：硬件虚拟化扩展（可选，但通常使用）
   - **需要 Guest OS 修改**：Guest OS 需要修改以支持半虚拟化接口（Hypercall）
   - **驱动层协作**：虚拟设备驱动与 Hypervisor 协作（如前端/后端驱动模型）

2. **技术层级**：**硬件抽象层 + 驱动抽象层**（Hardware Abstraction Layer +
   Driver Abstraction Layer）

   - **Hypervisor（虚拟机监控器）**：运行在硬件之上，提供半虚拟化接口
   - **半虚拟化接口**：Hypercall、事件通道、共享内存等
   - **Guest OS 修改**：Guest OS 内核需要修改以支持半虚拟化接口

3. **隔离级别**：**内核级隔离**（Kernel-Level Isolation）

   - **隔离边界**：Guest 内核边界
   - **隔离机制**：Hypervisor + Guest OS 协作
   - **隔离强度**：强（内核级隔离，但需要 Guest OS 配合）

4. **复用机制**：**硬件 + 驱动协作复用**（Hardware + Driver Collaborative
   Multiplexing）
   - **CPU 复用**：多个 vCPU 共享物理 CPU，通过 Hypercall 协作
   - **内存复用**：多个虚拟机共享物理内存，通过协作的内存管理
   - **IO 复用**：多个虚拟机共享物理 IO 设备，通过前端/后端驱动模型

**技术实现**：

- **Xen 半虚拟化**：Xen Hypervisor + 修改后的 Linux 内核（如 Xen PV Guest）
- **Hypercall 接口**：Guest OS 通过 Hypercall 与 Hypervisor 通信
- **前端/后端驱动**：Guest OS 中的前端驱动与 Hypervisor 中的后端驱动协作

### 02.3 容器化（Containerization）严格定义

**容器化（Containerization）严格定义**：

容器化是一种**OS 支持的复用**技术，通过在操作系统层面利用 Namespace、Cgroup 等内
核特性，使多个容器进程共享同一 Host OS 内核，实现进程级隔离和资源限制。

**关键特征**：

1. **支持层级**：**OS 层**（Operating System Layer）

   - **OS 内核支持**：Linux 内核的 Namespace、Cgroup、Capabilities 等特性
   - **不需要 Guest OS**：容器直接运行在 Host OS 之上，共享 Host OS 内核
   - **进程级隔离**：通过 Namespace 实现进程、网络、文件系统等隔离

2. **技术层级**：**操作系统层**（Operating System Layer）

   - **Container Runtime**：容器运行时（如 runc、crun、containerd）
   - **Namespace**：进程命名空间、网络命名空间、挂载命名空间等
   - **Cgroup**：资源限制和控制组（CPU、内存、IO 等）

3. **隔离级别**：**进程级隔离**（Process-Level Isolation）

   - **隔离边界**：进程地址空间、Namespace 边界
   - **隔离机制**：Namespace + Cgroup + Capabilities
   - **隔离强度**：中等（进程级隔离，但共享内核）

4. **复用机制**：**OS 内核复用**（OS Kernel Multiplexing）
   - **内核复用**：多个容器共享同一 Host OS 内核
   - **进程复用**：多个容器进程共享 Host OS 进程调度器
   - **资源复用**：多个容器共享 Host OS 资源，通过 Cgroup 限制

**技术实现**：

- **Linux Namespace**：PID、Network、Mount、UTS、IPC、User 命名空间
- **Linux Cgroup**：CPU、Memory、IO、Device、Network 控制组
- **Container Runtime**：Docker（runc）、containerd、CRI-O
- **容器镜像**：OCI 镜像格式、OverlayFS 文件系统

### 02.4 沙盒化（Sandboxing）严格定义

**沙盒化（Sandboxing）严格定义**：

沙盒化是一种**OS 进程内支持的复用**技术，通过在操作系统进程内部创建受限的执行环
境，使多个应用在同一个进程空间内运行，但通过系统调用拦截、能力限制等方式实现应用
级隔离。

**关键特征**：

1. **支持层级**：**OS 进程内层**（OS Process-Internal Layer）

   - **进程内支持**：在单个 OS 进程内创建多个应用执行环境
   - **不需要独立进程**：多个应用可以在同一进程空间内运行
   - **系统调用拦截**：通过系统调用拦截限制应用的资源访问

2. **技术层级**：**应用运行时层**（Application Runtime Layer）

   - **Sandbox Runtime**：沙盒运行时（如 Wasm Runtime、gVisor、Firecracker）
   - **系统调用拦截**：拦截和重定向系统调用
   - **能力限制**：限制应用的资源访问能力（文件系统、网络等）

3. **隔离级别**：**应用级隔离**（Application-Level Isolation）

   - **隔离边界**：应用运行时边界
   - **隔离机制**：系统调用拦截 + 能力限制 + 资源限制
   - **隔离强度**：较弱（应用级隔离，共享进程空间）

4. **复用机制**：**进程内复用**（Process-Internal Multiplexing）
   - **Runtime 复用**：多个应用共享同一 Runtime 实例
   - **进程空间复用**：多个应用在同一进程空间内运行
   - **资源复用**：多个应用共享进程资源，通过能力限制隔离

**技术实现**：

- **WebAssembly（Wasm）**：Wasm Runtime（WasmEdge、Wasmtime）+ WASI 接口
- **gVisor**：用户空间内核（Userspace Kernel）+ 系统调用拦截
- **Firecracker**：轻量级虚拟机（MicroVM）+ VMM 精简
- **进程沙盒**：seccomp、AppArmor、SELinux

---

## 03. 技术层级分析

### 03.1 硬件层技术名称与概念

**硬件层技术名称与概念（虚拟化、半虚拟化）**：

| 技术名称           | 技术层级   | 支持层级   | 关键概念                                              | 技术实现                             |
| ------------------ | ---------- | ---------- | ----------------------------------------------------- | ------------------------------------ |
| **Hypervisor**     | 硬件抽象层 | 硬件层     | 虚拟机监控器，运行在硬件之上                          | Type 1 Hypervisor、Type 2 Hypervisor |
| **硬件虚拟化扩展** | 硬件层     | 硬件层     | CPU 硬件虚拟化支持                                    | Intel VT-x、AMD-V、Intel VT-d        |
| **EPT/NPT**        | 硬件层     | 硬件层     | 扩展页表/嵌套页表，硬件辅助内存虚拟化                 | Intel EPT、AMD NPT                   |
| **IOMMU**          | 硬件层     | 硬件层     | IO 内存管理单元，硬件辅助 IO 虚拟化                   | Intel VT-d、AMD-Vi                   |
| **vCPU**           | 虚拟硬件层 | 硬件层     | 虚拟 CPU，通过硬件虚拟化扩展实现                      | vCPU 调度、硬件辅助执行              |
| **虚拟内存**       | 虚拟硬件层 | 硬件层     | 虚拟内存，通过 EPT/NPT 实现                           | Guest 物理内存 → Host 物理内存       |
| **虚拟设备**       | 虚拟硬件层 | 硬件层     | 虚拟 IO 设备，通过 Hypervisor 模拟                    | 虚拟网卡、虚拟磁盘、虚拟 GPU         |
| **Hypercall**      | 驱动/OS 层 | 驱动/OS 层 | 半虚拟化接口，Guest OS 与 Hypervisor 通信             | Xen Hypercall、KVM Hypercall         |
| **前端/后端驱动**  | 驱动/OS 层 | 驱动/OS 层 | 半虚拟化驱动模型，Guest OS 前端与 Hypervisor 后端协作 | Xen PV 驱动、VirtIO 驱动             |

**硬件层关键技术概念**：

1. **Hypervisor（虚拟机监控器）**：

   - **定义**：运行在物理硬件之上的软件层，负责虚拟机的创建、管理和资源分配
   - **技术层级**：硬件抽象层
   - **支持层级**：硬件层
   - **类型**：Type 1（裸机）、Type 2（托管）

2. **硬件虚拟化扩展（Hardware Virtualization Extensions）**：

   - **定义**：CPU 硬件提供的虚拟化支持（Intel VT-x、AMD-V）
   - **技术层级**：硬件层
   - **支持层级**：硬件层
   - **作用**：提高虚拟化性能，减少 Hypervisor 开销

3. **EPT/NPT（扩展页表/嵌套页表）**：

   - **定义**：硬件辅助的内存虚拟化技术，直接翻译 Guest 物理地址到 Host 物理地址
   - **技术层级**：硬件层
   - **支持层级**：硬件层
   - **作用**：减少内存虚拟化开销，提高性能

4. **IOMMU（IO 内存管理单元）**：
   - **定义**：硬件辅助的 IO 虚拟化技术，实现设备直接分配给虚拟机
   - **技术层级**：硬件层
   - **支持层级**：硬件层
   - **作用**：支持设备透传，提高 IO 性能

### 03.2 驱动/OS 层技术名称与概念

**驱动/OS 层技术名称与概念（半虚拟化）**：

| 技术名称                        | 技术层级   | 支持层级   | 关键概念                               | 技术实现                               |
| ------------------------------- | ---------- | ---------- | -------------------------------------- | -------------------------------------- |
| **Hypercall**                   | 驱动/OS 层 | 驱动/OS 层 | 半虚拟化接口，Guest OS 调用 Hypervisor | Xen Hypercall、KVM Hypercall           |
| **事件通道（Event Channel）**   | 驱动/OS 层 | 驱动/OS 层 | 半虚拟化事件通知机制                   | Xen Event Channel                      |
| **共享内存（Shared Memory）**   | 驱动/OS 层 | 驱动/OS 层 | Guest OS 与 Hypervisor 共享内存        | Xen Grant Table                        |
| **VirtIO**                      | 驱动/OS 层 | 驱动/OS 层 | 半虚拟化设备标准接口                   | VirtIO 网络、VirtIO 块设备、VirtIO GPU |
| **前端驱动（Frontend Driver）** | 驱动/OS 层 | 驱动/OS 层 | Guest OS 中的虚拟设备驱动              | Xen PV 前端驱动                        |
| **后端驱动（Backend Driver）**  | 驱动/OS 层 | 驱动/OS 层 | Hypervisor 或 Host OS 中的设备驱动     | Xen PV 后端驱动                        |

**驱动/OS 层关键技术概念**：

1. **Hypercall（超级调用）**：

   - **定义**：Guest OS 直接调用 Hypervisor 的接口，类似系统调用
   - **技术层级**：驱动/OS 层
   - **支持层级**：驱动/OS 层
   - **作用**：提高虚拟化性能，减少模拟开销

2. **VirtIO（虚拟 IO 标准）**：
   - **定义**：半虚拟化设备标准接口，提供前端/后端驱动模型
   - **技术层级**：驱动/OS 层
   - **支持层级**：驱动/OS 层
   - **作用**：标准化半虚拟化设备接口，提高性能和兼容性

### 03.3 OS 层技术名称与概念

**OS 层技术名称与概念（容器化）**：

| 技术名称                               | 技术层级 | 支持层级 | 关键概念                        | 技术实现                            |
| -------------------------------------- | -------- | -------- | ------------------------------- | ----------------------------------- |
| **Namespace**                          | OS 层    | OS 层    | Linux 命名空间，实现进程隔离    | PID、Network、Mount、UTS、IPC、User |
| **Cgroup**                             | OS 层    | OS 层    | Linux 控制组，实现资源限制      | CPU、Memory、IO、Device、Network    |
| **Capabilities**                       | OS 层    | OS 层    | Linux 能力，实现权限控制        | CAP_NET_ADMIN、CAP_SYS_ADMIN 等     |
| **Container Runtime**                  | OS 层    | OS 层    | 容器运行时，管理容器生命周期    | runc、crun、containerd              |
| **Container Image**                    | OS 层    | OS 层    | 容器镜像，包含应用和依赖        | OCI 镜像格式、OverlayFS             |
| **OverlayFS**                          | OS 层    | OS 层    | 联合文件系统，实现镜像层复用    | Docker OverlayFS、Overlay2          |
| **OCI（Open Container Initiative）**   | OS 层    | OS 层    | 容器标准化规范                  | OCI 镜像、OCI 运行时规范            |
| **CRI（Container Runtime Interface）** | OS 层    | OS 层    | 容器运行时接口，用于 Kubernetes | CRI-O、containerd CRI               |

**OS 层关键技术概念**：

1. **Namespace（命名空间）**：

   - **定义**：Linux 内核特性，实现进程、网络、文件系统等资源的隔离
   - **技术层级**：OS 层
   - **支持层级**：OS 层
   - **作用**：提供进程级隔离，使容器看起来拥有独立的资源视图

2. **Cgroup（控制组）**：

   - **定义**：Linux 内核特性，实现资源限制和优先级控制
   - **技术层级**：OS 层
   - **支持层级**：OS 层
   - **作用**：限制容器的 CPU、内存、IO 等资源使用

3. **Container Runtime（容器运行时）**：
   - **定义**：管理容器生命周期的组件，创建、启动、停止、删除容器
   - **技术层级**：OS 层
   - **支持层级**：OS 层
   - **作用**：实现容器的创建和管理，提供容器与 Host OS 的接口

### 03.4 OS 进程内技术名称与概念

**OS 进程内技术名称与概念（沙盒化）**：

| 技术名称                                 | 技术层级     | 支持层级    | 关键概念                           | 技术实现                     |
| ---------------------------------------- | ------------ | ----------- | ---------------------------------- | ---------------------------- |
| **Wasm Runtime**                         | 应用运行时层 | OS 进程内层 | WebAssembly 运行时，执行 Wasm 模块 | WasmEdge、Wasmtime、V8       |
| **WASI（WebAssembly System Interface）** | 应用运行时层 | OS 进程内层 | Wasm 系统接口，限制资源访问        | WASI Filesystem、WASI Socket |
| **系统调用拦截（Syscall Interception）** | 应用运行时层 | OS 进程内层 | 拦截和重定向系统调用               | seccomp、ptrace、gVisor      |
| **用户空间内核（Userspace Kernel）**     | 应用运行时层 | OS 进程内层 | 用户空间实现的内核，拦截系统调用   | gVisor                       |
| **MicroVM（微虚拟机）**                  | 应用运行时层 | OS 进程内层 | 轻量级虚拟机，最小化 VMM           | Firecracker                  |
| **seccomp（Secure Computing）**          | OS 进程内层  | OS 进程内层 | Linux 系统调用过滤机制             | seccomp-bpf                  |
| **AppArmor**                             | OS 进程内层  | OS 进程内层 | Linux 应用程序安全框架             | AppArmor profiles            |
| **SELinux**                              | OS 进程内层  | OS 进程内层 | Linux 安全增强框架                 | SELinux policies             |

**OS 进程内关键技术概念**：

1. **Wasm Runtime（WebAssembly 运行时）**：

   - **定义**：执行 WebAssembly 模块的运行时环境
   - **技术层级**：应用运行时层
   - **支持层级**：OS 进程内层
   - **作用**：提供沙盒执行环境，通过 WASI 限制资源访问

2. **WASI（WebAssembly System Interface）**：

   - **定义**：Wasm 系统接口，提供受限的系统资源访问
   - **技术层级**：应用运行时层
   - **支持层级**：OS 进程内层
   - **作用**：限制 Wasm 模块的文件系统、网络等资源访问

3. **系统调用拦截（Syscall Interception）**：
   - **定义**：拦截应用程序的系统调用，进行安全检查或重定向
   - **技术层级**：应用运行时层
   - **支持层级**：OS 进程内层
   - **作用**：限制应用的系统资源访问，提高安全性

---

## 04. 多维度对比矩阵

### 04.1 技术层级对比矩阵

**技术层级对比矩阵**：

| 维度              | 虚拟化（全虚拟化）     | 半虚拟化                   | 容器化                       | 沙盒化                        |
| ----------------- | ---------------------- | -------------------------- | ---------------------------- | ----------------------------- |
| **技术层级**      | 硬件抽象层             | 硬件抽象层 + 驱动抽象层    | 操作系统层                   | 应用运行时层                  |
| **支持层级**      | 硬件层                 | 硬件层 + 驱动/OS 层        | OS 层                        | OS 进程内层                   |
| **实现位置**      | Hypervisor（硬件之上） | Hypervisor + Guest OS 驱动 | Container Runtime（OS 之上） | Sandbox Runtime（进程内）     |
| **Guest OS 需求** | 无需修改（完整 OS）    | 需要修改（支持 Hypercall） | 无需 OS（共享 Host OS）      | 无需 OS（应用层）             |
| **硬件需求**      | 硬件虚拟化扩展（必需） | 硬件虚拟化扩展（可选）     | 无需硬件支持                 | 无需硬件支持                  |
| **内核共享**      | 否（每个 VM 独立内核） | 否（每个 VM 独立内核）     | 是（共享 Host OS 内核）      | 是（共享 Host OS 内核和进程） |

### 04.2 支持层级对比矩阵

**支持层级对比矩阵**：

| 维度             | 虚拟化（全虚拟化）        | 半虚拟化                 | 容器化                      | 沙盒化                  |
| ---------------- | ------------------------- | ------------------------ | --------------------------- | ----------------------- |
| **硬件层支持**   | ✅ 必需（硬件虚拟化扩展） | ✅ 可选（通常使用）      | ❌ 不需要                   | ❌ 不需要               |
| **驱动层支持**   | ❌ 不需要                 | ✅ 必需（前端/后端驱动） | ❌ 不需要                   | ❌ 不需要               |
| **OS 层支持**    | ❌ 不需要                 | ✅ 必需（Guest OS 修改） | ✅ 必需（Host OS 内核特性） | ❌ 不需要               |
| **进程内支持**   | ❌ 不需要                 | ❌ 不需要                | ❌ 不需要                   | ✅ 必需（Runtime 支持） |
| **支持层级总结** | 硬件层                    | 硬件层 + 驱动/OS 层      | OS 层                       | OS 进程内层             |

**支持层级详细说明**：

1. **虚拟化（全虚拟化）**：

   - **硬件层支持**：Intel VT-x、AMD-V（必需）
   - **驱动层支持**：不需要（Guest OS 驱动直接使用虚拟设备）
   - **OS 层支持**：不需要（Guest OS 无需感知虚拟化）
   - **支持层级**：仅硬件层

2. **半虚拟化**：

   - **硬件层支持**：Intel VT-x、AMD-V（可选，但通常使用）
   - **驱动层支持**：前端/后端驱动（必需）
   - **OS 层支持**：Guest OS 内核修改（必需，支持 Hypercall）
   - **支持层级**：硬件层 + 驱动/OS 层

3. **容器化**：

   - **硬件层支持**：不需要
   - **驱动层支持**：不需要
   - **OS 层支持**：Host OS 内核特性（必需，Namespace、Cgroup）
   - **支持层级**：仅 OS 层

4. **沙盒化**：
   - **硬件层支持**：不需要
   - **驱动层支持**：不需要
   - **OS 层支持**：不需要（系统调用拦截在进程内）
   - **进程内支持**：Sandbox Runtime（必需）
   - **支持层级**：仅 OS 进程内层

### 04.3 隔离机制对比矩阵

**隔离机制对比矩阵**：

| 维度           | 虚拟化（全虚拟化）      | 半虚拟化                           | 容器化                      | 沙盒化                          |
| -------------- | ----------------------- | ---------------------------------- | --------------------------- | ------------------------------- |
| **隔离级别**   | 硬件级隔离              | 内核级隔离                         | 进程级隔离                  | 应用级隔离                      |
| **隔离边界**   | 物理硬件边界            | Guest 内核边界                     | 进程地址空间边界            | 应用运行时边界                  |
| **隔离机制**   | Hypervisor + 硬件虚拟化 | Hypervisor + Guest OS 协作         | Namespace + Cgroup          | 系统调用拦截 + 能力限制         |
| **隔离强度**   | 最强（5/5）             | 强（4/5）                          | 中等（3/5）                 | 较弱（2/5）                     |
| **攻击面**     | 最小（Hypervisor 漏洞） | 较小（Hypervisor + Guest OS 漏洞） | 中等（内核漏洞）            | 较大（应用漏洞 + 系统调用漏洞） |
| **跨隔离通信** | 不可能（硬件隔离）      | 困难（需要通过 Hypervisor）        | 受限（通过 Namespace 隔离） | 容易（共享进程空间）            |

### 04.4 性能特性对比矩阵

**性能特性对比矩阵**：

| 维度         | 虚拟化（全虚拟化）           | 半虚拟化                            | 容器化                 | 沙盒化                      |
| ------------ | ---------------------------- | ----------------------------------- | ---------------------- | --------------------------- |
| **CPU 性能** | 70-95%（硬件辅助）           | 80-95%（协作优化）                  | 95-99%（接近原生）     | 80-95%（Runtime 开销）      |
| **内存性能** | 70-90%（EPT/NPT 开销）       | 80-95%（协作优化）                  | 95-99%（接近原生）     | 85-98%（Runtime 开销）      |
| **IO 性能**  | 50-80%（虚拟设备模拟）       | 70-90%（前端/后端驱动）             | 90-98%（接近原生）     | 70-90%（系统调用拦截开销）  |
| **启动时间** | 慢（分钟级，需要启动 OS）    | 较慢（分钟级，需要启动修改后的 OS） | 快（秒级，共享内核）   | 很快（毫秒级，无需启动 OS） |
| **资源开销** | 高（每个 VM 独立 OS）        | 高（每个 VM 独立 OS）               | 低（共享内核）         | 最低（共享进程空间）        |
| **内存占用** | 高（每个 VM 独立内核和驱动） | 高（每个 VM 独立内核和驱动）        | 低（共享内核，仅应用） | 最低（共享进程空间）        |
| **CPU 开销** | 5-30%（Hypervisor 开销）     | 2-10%（协作优化）                   | <5%（接近原生）        | 5-20%（Runtime 开销）       |

### 04.5 安全性对比矩阵

**安全性对比矩阵**：

| 维度               | 虚拟化（全虚拟化）                   | 半虚拟化                                 | 容器化                  | 沙盒化                         |
| ------------------ | ------------------------------------ | ---------------------------------------- | ----------------------- | ------------------------------ |
| **隔离强度**       | 最强（硬件级隔离）                   | 强（内核级隔离）                         | 中等（进程级隔离）      | 较弱（应用级隔离）             |
| **攻击面大小**     | 最小（仅 Hypervisor）                | 较小（Hypervisor + Guest OS）            | 中等（Host OS 内核）    | 较大（应用层 + 系统调用层）    |
| **逃逸风险**       | 低（硬件隔离，需要 Hypervisor 漏洞） | 中低（需要 Hypervisor 或 Guest OS 漏洞） | 中（需要内核漏洞）      | 中高（需要应用或系统调用漏洞） |
| **侧信道攻击风险** | 中（虚拟化侧信道）                   | 中（虚拟化侧信道）                       | 高（共享内核）          | 高（共享进程空间）             |
| **权限控制**       | 强（硬件级权限）                     | 强（硬件级权限）                         | 中（Capabilities 限制） | 弱（应用级权限限制）           |
| **审计能力**       | 中（Hypervisor 级别）                | 中（Hypervisor + Guest OS 级别）         | 高（内核级别）          | 高（Runtime 级别）             |

### 04.6 适用场景对比矩阵

**适用场景对比矩阵**：

| 维度               | 虚拟化（全虚拟化）   | 半虚拟化                       | 容器化                | 沙盒化                  |
| ------------------ | -------------------- | ------------------------------ | --------------------- | ----------------------- |
| **多操作系统支持** | ✅ 是（完全独立 OS） | ✅ 是（完全独立 OS，但需修改） | ❌ 否（仅 Linux）     | ❌ 否（仅应用层）       |
| **强隔离需求**     | ✅ 是（硬件级隔离）  | ✅ 是（内核级隔离）            | ⚠️ 部分（进程级隔离） | ❌ 否（应用级隔离）     |
| **高性能需求**     | ⚠️ 部分（有开销）    | ✅ 是（协作优化）              | ✅ 是（接近原生）     | ⚠️ 部分（Runtime 开销） |
| **快速启动需求**   | ❌ 否（分钟级）      | ❌ 否（分钟级）                | ✅ 是（秒级）         | ✅ 是（毫秒级）         |
| **资源效率需求**   | ❌ 否（高开销）      | ❌ 否（高开销）                | ✅ 是（低开销）       | ✅ 是（最低开销）       |
| **云原生应用**     | ❌ 否                | ❌ 否                          | ✅ 是（Kubernetes）   | ✅ 是（Serverless）     |
| **边缘计算**       | ❌ 否（资源消耗大）  | ❌ 否（资源消耗大）            | ⚠️ 部分（K3s）        | ✅ 是（轻量级）         |
| **多租户环境**     | ✅ 是（强隔离）      | ✅ 是（强隔离）                | ⚠️ 部分（中等隔离）   | ❌ 否（弱隔离）         |

---

## 05. 技术层级思维导图

### 05.1 技术层级关系图

**技术层级关系图（从硬件到应用）**：

```text
┌─────────────────────────────────────────────────────────────┐
│                    应用层（Application Layer）                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  沙盒化（Sandboxing）                                    │ │
│  │  ├── Wasm Runtime（OS 进程内支持）                       │ │
│  │  ├── gVisor（用户空间内核）                              │ │
│  │  ├── Firecracker（MicroVM）                             │ │
│  │  └── seccomp/AppArmor/SELinux（系统调用拦截）           │ │
│  └────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                  操作系统层（OS Layer）                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  容器化（Containerization）                              │ │
│  │  ├── Container Runtime（OS 层支持）                     │ │
│  │  ├── Namespace（进程隔离）                               │ │
│  │  ├── Cgroup（资源限制）                                  │ │
│  │  └── Capabilities（权限控制）                             │ │
│  └────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│             驱动/OS层（Driver/OS Layer）                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  半虚拟化（Para-virtualization）                         │ │
│  │  ├── Hypercall（驱动/OS 层支持）                         │ │
│  │  ├── VirtIO（前端/后端驱动）                             │ │
│  │  ├── 事件通道（Event Channel）                           │ │
│  │  └── 共享内存（Shared Memory）                            │ │
│  └────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                  硬件抽象层（Hardware Abstraction Layer）      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  虚拟化（Full Virtualization）                           │ │
│  │  ├── Hypervisor（硬件层支持）                            │ │
│  │  ├── Type 1 Hypervisor（裸机）                           │ │
│  │  ├── Type 2 Hypervisor（托管）                           │ │
│  │  └── 硬件虚拟化扩展（VT-x、AMD-V）                       │ │
│  └────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    硬件层（Hardware Layer）                    │
│  ├── CPU（Intel VT-x、AMD-V）                                │
│  ├── 内存（EPT/NPT）                                         │
│  ├── IO（IOMMU、VT-d）                                       │
│  └── 物理硬件资源                                            │
└─────────────────────────────────────────────────────────────┘
```

### 05.2 支持层级关系图

**支持层级关系图（从硬件到进程内）**：

```text
支持层级关系（Support Layer Hierarchy）：

硬件层支持（Hardware Layer Support）
    ├── 虚拟化（全虚拟化）✅
    │   └── Intel VT-x、AMD-V、EPT/NPT、IOMMU
    │
    └── 半虚拟化 ✅（可选，但通常使用）
        └── Intel VT-x、AMD-V（可选）

驱动/OS层支持（Driver/OS Layer Support）
    └── 半虚拟化 ✅
        ├── Hypercall 接口
        ├── VirtIO 前端/后端驱动
        ├── 事件通道（Event Channel）
        └── Guest OS 内核修改

OS层支持（OS Layer Support）
    └── 容器化 ✅
        ├── Linux Namespace（PID、Network、Mount 等）
        ├── Linux Cgroup（CPU、Memory、IO 等）
        ├── Linux Capabilities
        └── Container Runtime（runc、containerd 等）

OS进程内支持（OS Process-Internal Support）
    └── 沙盒化 ✅
        ├── Wasm Runtime（WasmEdge、Wasmtime）
        ├── WASI 接口
        ├── 系统调用拦截（seccomp、ptrace）
        └── 用户空间内核（gVisor）
```

### 05.3 技术栈分层图

**技术栈分层图（完整技术栈视角）**：

```text
技术栈分层（Technology Stack Layering）：

┌──────────────────────────────────────────────────────────┐
│  应用层（Application Layer）                             │
│  ├── 应用程序（App）                                      │
│  └── 沙盒化层（Sandboxing Layer）                        │
│      ├── Wasm Module                                    │
│      ├── Wasm Runtime                                   │
│      └── WASI API                                       │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│  操作系统层（Operating System Layer）                     │
│  ├── Host OS 内核（Host OS Kernel）                      │
│  │   ├── Namespace（容器化）                              │
│  │   ├── Cgroup（容器化）                                 │
│  │   └── Capabilities（容器化）                           │
│  ├── Container Runtime（容器化）                         │
│  │   └── Container Process                               │
│  └── 沙盒 Runtime 进程（Sandboxing）                      │
│      └── Wasm Runtime Process                            │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│  Guest OS 层（Guest OS Layer）                           │
│  ├── Guest OS 内核（半虚拟化需要修改）                    │
│  │   ├── Hypercall 接口（半虚拟化）                       │
│  │   └── VirtIO 前端驱动（半虚拟化）                      │
│  └── Guest OS 应用（虚拟化、半虚拟化）                    │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│  Hypervisor 层（Hypervisor Layer）                        │
│  ├── Type 1 Hypervisor（虚拟化、半虚拟化）                 │
│  │   ├── vCPU 调度                                       │
│  │   ├── 虚拟内存管理（EPT/NPT）                          │
│  │   ├── 虚拟设备模拟（虚拟化）                           │
│  │   └── VirtIO 后端驱动（半虚拟化）                      │
│  └── Type 2 Hypervisor（虚拟化、半虚拟化）                 │
│      └── Host OS（托管 Hypervisor）                       │
└──────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────┐
│  硬件层（Hardware Layer）                                 │
│  ├── CPU（硬件虚拟化扩展：VT-x、AMD-V）                    │
│  ├── 内存（EPT/NPT）                                       │
│  ├── IO（IOMMU、VT-d）                                     │
│  └── 物理硬件资源                                          │
└──────────────────────────────────────────────────────────┘

复用机制（Multiplexing Mechanisms）：

虚拟化：     硬件虚拟化复用（Hardware Virtualization Multiplexing）
半虚拟化：   硬件 + 驱动协作复用（Hardware + Driver Collaborative Multiplexing）
容器化：     OS 内核复用（OS Kernel Multiplexing）
沙盒化：     进程内复用（Process-Internal Multiplexing）
```

**技术栈分层说明**：

1. **硬件层**：

   - **虚拟化/半虚拟化**：需要硬件虚拟化扩展（VT-x、AMD-V、EPT/NPT、IOMMU）
   - **容器化/沙盒化**：不需要硬件支持

2. **Hypervisor 层**（仅虚拟化/半虚拟化）：

   - **虚拟化**：Type 1 或 Type 2 Hypervisor，硬件虚拟化支持
   - **半虚拟化**：Hypervisor + Guest OS 协作，Hypercall 接口

3. **Guest OS 层**（仅虚拟化/半虚拟化）：

   - **虚拟化**：完整的 Guest OS，无需修改
   - **半虚拟化**：修改后的 Guest OS，支持 Hypercall

4. **Host OS 层**（仅容器化/沙盒化）：

   - **容器化**：Host OS 内核特性（Namespace、Cgroup）
   - **沙盒化**：Host OS 进程空间（Runtime 进程）

5. **应用层**：
   - **容器化**：容器应用进程
   - **沙盒化**：Wasm Module 或其他沙盒应用

---

## 06. 参考

**关联文档**：

- **[技术名词概念论证](technical-concepts-explanation.md)** - 技术名词概念论证
- **[隔离模型](../01-theory-models/02-isolation-models.md)** - 隔离模型理论
- **[复用机制全面分析](10-multiplexing-mechanisms-analysis.md)** - 复用机制分析

**外部参考（Wikipedia，as of 2025-11-02）**：

- [Virtualization](https://en.wikipedia.org/wiki/Virtualization) -
  Virtualization
- [Hardware Virtualization](https://en.wikipedia.org/wiki/Hardware_virtualization) -
  Hardware Virtualization
- [Hypervisor](https://en.wikipedia.org/wiki/Hypervisor) - Hypervisor
- [Para-virtualization](https://en.wikipedia.org/wiki/Para-virtualization) -
  Para-virtualization
- [Xen](https://en.wikipedia.org/wiki/Xen) - Xen Hypervisor
- [Container](<https://en.wikipedia.org/wiki/Container_(computing)>) - Container
- [Linux Namespaces](https://en.wikipedia.org/wiki/Linux_namespaces) - Linux
  Namespaces
- [Cgroups](https://en.wikipedia.org/wiki/Cgroups) - Cgroups
- [Sandbox (Computer Security)](<https://en.wikipedia.org/wiki/Sandbox_(computer_security)>) -
  Sandbox
- [WebAssembly](https://en.wikipedia.org/wiki/WebAssembly) - WebAssembly
- [WASI](https://en.wikipedia.org/wiki/WebAssembly_System_Interface) -
  WebAssembly System Interface

**技术标准参考**：

- [Intel Virtualization Technology](https://www.intel.com/content/www/us/en/virtualization/virtualization-technology/intel-virtualization-technology.html) -
  Intel VT-x
- [AMD-V](https://www.amd.com/en/technologies/virtualization) - AMD-V
- [OCI Specification](https://github.com/opencontainers/runtime-spec) - Open
  Container Initiative
- [CRI Specification](https://github.com/kubernetes/cri-api) - Container Runtime
  Interface
- [WebAssembly Specification](https://webassembly.org/specs/) - WebAssembly Core
  Specification
- [WASI Specification](https://github.com/WebAssembly/WASI) - WebAssembly System
  Interface

---

**文档版本**：v1.0 **最后更新**：2025-01 **维护者**：文档维护团队

---

_本文档为虚拟化/半虚拟化/容器化/沙盒化严格定义与技术层级分析的核心文档，持续更新
和完善中。_
