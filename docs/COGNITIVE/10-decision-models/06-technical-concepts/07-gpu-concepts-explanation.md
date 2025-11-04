# GPU 概念与技术名词论证

## 目录

- [目录](#目录)
- [01. 文档定位](#01-文档定位)
- [02. GPU 拓扑结构](#02-gpu-拓扑结构)
  - [02.1 物理 GPU 拓扑](#021-物理-gpu-拓扑)
    - [02.1.1 物理 GPU 拓扑定义](#0211-物理-gpu-拓扑定义)
    - [02.1.2 物理 GPU 拓扑在技术栈中的作用](#0212-物理-gpu-拓扑在技术栈中的作用)
  - [02.2 逻辑 GPU 拓扑](#022-逻辑-gpu-拓扑)
    - [02.2.1 逻辑 GPU 拓扑定义](#0221-逻辑-gpu-拓扑定义)
    - [02.2.2 逻辑 GPU 拓扑在技术栈中的作用](#0222-逻辑-gpu-拓扑在技术栈中的作用)
  - [02.3 GPU 拓扑映射](#023-gpu-拓扑映射)
    - [02.3.1 物理 GPU 拓扑与逻辑 GPU 拓扑映射](#0231-物理-gpu-拓扑与逻辑-gpu-拓扑映射)
    - [02.3.2 各范式 GPU 拓扑结构映射](#0232-各范式-gpu-拓扑结构映射)
- [03. GPU 执行模式](#03-gpu-执行模式)
  - [03.1 GPU 计算模式](#031-gpu-计算模式)
    - [03.1.1 GPU 计算模式定义](#0311-gpu-计算模式定义)
    - [03.1.2 GPU 计算模式在各范式中的应用](#0312-gpu-计算模式在各范式中的应用)
  - [03.2 GPU 调度模式](#032-gpu-调度模式)
    - [03.2.1 GPU 调度模式定义](#0321-gpu-调度模式定义)
    - [03.2.2 GPU 调度模式在各范式中的应用](#0322-gpu-调度模式在各范式中的应用)
  - [03.3 GPU 执行模式映射](#033-gpu-执行模式映射)
    - [03.3.1 GPU 执行模式对比矩阵](#0331-gpu-执行模式对比矩阵)
    - [03.3.2 各范式 GPU 执行模式映射](#0332-各范式-gpu-执行模式映射)
- [04. GPU 通道模型](#04-gpu-通道模型)
  - [04.1 物理 GPU 通道](#041-物理-gpu-通道)
    - [04.1.1 物理 GPU 通道定义](#0411-物理-gpu-通道定义)
    - [04.1.2 物理 GPU 通道在技术栈中的作用](#0412-物理-gpu-通道在技术栈中的作用)
  - [04.2 逻辑 GPU 通道](#042-逻辑-gpu-通道)
    - [04.2.1 逻辑 GPU 通道定义](#0421-逻辑-gpu-通道定义)
    - [04.2.2 逻辑 GPU 通道在技术栈中的作用](#0422-逻辑-gpu-通道在技术栈中的作用)
  - [04.3 GPU 通道映射](#043-gpu-通道映射)
    - [04.3.1 物理 GPU 通道与逻辑 GPU 通道映射](#0431-物理-gpu-通道与逻辑-gpu-通道映射)
    - [04.3.2 各范式 GPU 通道模型映射](#0432-各范式-gpu-通道模型映射)
- [05. GPU 设备模型](#05-gpu-设备模型)
  - [05.1 物理 GPU](#051-物理-gpu)
    - [05.1.1 物理 GPU 定义](#0511-物理-gpu-定义)
    - [05.1.2 物理 GPU 在技术栈中的作用](#0512-物理-gpu-在技术栈中的作用)
  - [05.2 虚拟 GPU (vGPU)](#052-虚拟-gpu-vgpu)
    - [05.2.1 虚拟 GPU 定义](#0521-虚拟-gpu-定义)
    - [05.2.2 虚拟 GPU 在技术栈中的作用](#0522-虚拟-gpu-在技术栈中的作用)
  - [05.3 逻辑 GPU](#053-逻辑-gpu)
    - [05.3.1 逻辑 GPU 定义](#0531-逻辑-gpu-定义)
    - [05.3.2 逻辑 GPU 在技术栈中的作用](#0532-逻辑-gpu-在技术栈中的作用)
  - [05.4 GPU 设备模型映射](#054-gpu-设备模型映射)
    - [05.4.1 GPU 设备模型对比矩阵](#0541-gpu-设备模型对比矩阵)
    - [05.4.2 各范式 GPU 设备模型映射](#0542-各范式-gpu-设备模型映射)
- [06. GPU 协议栈](#06-gpu-协议栈)
  - [06.1 GPU 协议栈模型](#061-gpu-协议栈模型)
    - [06.1.1 GPU 协议栈定义](#0611-gpu-协议栈定义)
    - [06.1.2 GPU 协议栈在各范式中的映射](#0612-gpu-协议栈在各范式中的映射)
  - [06.2 GPU 接口标准](#062-gpu-接口标准)
    - [06.2.1 GPU 接口标准定义](#0621-gpu-接口标准定义)
    - [06.2.2 GPU 接口标准在各范式中的应用](#0622-gpu-接口标准在各范式中的应用)
  - [06.3 各范式 GPU 栈对比](#063-各范式-gpu-栈对比)
    - [06.3.1 GPU 协议栈对比矩阵](#0631-gpu-协议栈对比矩阵)
- [07. 虚拟化 GPU 架构](#07-虚拟化-gpu-架构)
  - [07.1 虚拟化 GPU 拓扑](#071-虚拟化-gpu-拓扑)
    - [07.1.1 虚拟化 GPU 拓扑结构](#0711-虚拟化-gpu-拓扑结构)
  - [07.2 虚拟化 GPU 设备模型](#072-虚拟化-gpu-设备模型)
    - [07.2.1 虚拟化 GPU 设备架构](#0721-虚拟化-gpu-设备架构)
  - [07.3 虚拟化 GPU 隔离](#073-虚拟化-gpu-隔离)
    - [07.3.1 虚拟化 GPU 隔离机制](#0731-虚拟化-gpu-隔离机制)
- [08. 容器化 GPU 架构](#08-容器化-gpu-架构)
  - [08.1 容器化 GPU 拓扑](#081-容器化-gpu-拓扑)
    - [08.1.1 容器化 GPU 拓扑结构](#0811-容器化-gpu-拓扑结构)
  - [08.2 容器化 GPU 设备模型](#082-容器化-gpu-设备模型)
    - [08.2.1 容器化 GPU 设备架构](#0821-容器化-gpu-设备架构)
  - [08.3 容器化 GPU 隔离](#083-容器化-gpu-隔离)
    - [08.3.1 容器化 GPU 隔离机制](#0831-容器化-gpu-隔离机制)
- [09. 沙盒化 GPU 架构](#09-沙盒化-gpu-架构)
  - [09.1 沙盒化 GPU 拓扑](#091-沙盒化-gpu-拓扑)
    - [09.1.1 沙盒化 GPU 拓扑结构](#0911-沙盒化-gpu-拓扑结构)
  - [09.2 沙盒化 GPU 设备模型](#092-沙盒化-gpu-设备模型)
    - [09.2.1 沙盒化 GPU 设备架构](#0921-沙盒化-gpu-设备架构)
  - [09.3 沙盒化 GPU 隔离](#093-沙盒化-gpu-隔离)
    - [09.3.1 沙盒化 GPU 隔离机制](#0931-沙盒化-gpu-隔离机制)
- [10. GPU 架构对比矩阵](#10-gpu-架构对比矩阵)
  - [10.1 GPU 拓扑对比矩阵](#101-gpu-拓扑对比矩阵)
  - [10.2 GPU 执行模式对比矩阵](#102-gpu-执行模式对比矩阵)
  - [10.3 GPU 通道模型对比矩阵](#103-gpu-通道模型对比矩阵)
  - [10.4 GPU 设备模型对比矩阵](#104-gpu-设备模型对比矩阵)
  - [10.5 GPU 协议栈对比矩阵](#105-gpu-协议栈对比矩阵)
- [11. 参考](#11-参考)

---

## 01. 文档定位

本文档系统化解释**虚拟化、容器化、沙盒化**的 GPU 概念、拓扑结构、执行模式、通道
模型、设备模型，提供详细的 GPU 架构论证和技术名词对应关系。

**核心内容**：

1. **GPU 拓扑结构**：物理 GPU 拓扑 vs 逻辑 GPU 拓扑的映射关系
2. **GPU 执行模式**：GPU 计算模式、GPU 调度模式的实现机制
3. **GPU 通道模型**：物理 GPU 通道 vs 逻辑 GPU 通道的抽象关系
4. **GPU 设备模型**：物理 GPU、虚拟 GPU、逻辑 GPU 的技术实现
5. **GPU 协议栈**：各范式在 GPU 协议栈中的位置和作用
6. **GPU 架构对比**：虚拟化、容器化、沙盒化的 GPU 架构全面对比

**与其他文档的关系**：

- **GPU/IO 设备概念论证**：GPU/IO 设备的综合讨论
- **IO 设备概念论证**：IO 设备的专门讨论
- **本文档**：专门的 GPU 概念论证，更详细和系统化

---

## 02. GPU 拓扑结构

### 02.1 物理 GPU 拓扑

#### 02.1.1 物理 GPU 拓扑定义

**物理 GPU 拓扑（Physical GPU Topology）定义**：

物理 GPU 拓扑是指 GPU 卡、GPU 核心、GPU 内存、GPU 互连在硬件上的实际布局和连接关
系。

**物理 GPU 拓扑类型**：

1. **单 GPU 架构（Single GPU）**：

   - **结构**：单个 GPU 卡，通过 PCIe 连接到 CPU
   - **特征**：独立 GPU 内存、CUDA 核心、Tensor 核心
   - **应用**：工作站、小型服务器、个人开发

2. **多 GPU 架构（Multi-GPU）**：

   - **结构**：多个 GPU 卡，通过 PCIe 连接到 CPU，GPU 间通过 NVLink 互连
   - **特征**：GPU 间高速互连（NVLink 2.0/3.0: 300-600 GB/s）、统一内存空间、GPU
     间通信
   - **应用**：深度学习训练、HPC、大规模并行计算

3. **GPU 集群架构（GPU Cluster）**：

   - **结构**：多个服务器节点，每个节点有多个 GPU，节点间通过高速网络互连
   - **特征**：跨节点 GPU 通信（InfiniBand/Ethernet: 200 Gbps+）、分布式训练、大
     规模并行
   - **应用**：大规模深度学习、超算中心、AI 训练集群

4. **GPU 内存层次结构**：

   - **全局内存（Global Memory）**：GPU 显存，所有线程共享（8-80GB）
   - **共享内存（Shared Memory）**：SM（流多处理器）内共享（48-164 KB/SM）
   - **寄存器（Registers）**：每个线程私有（65536/线程）
   - **常量内存（Constant Memory）**：只读缓存（64 KB）
   - **纹理内存（Texture Memory）**：只读缓存（与全局内存共享）
   - **特征**：延迟递增、容量递增、访问模式不同

#### 02.1.2 物理 GPU 拓扑在技术栈中的作用

**物理 GPU 拓扑映射**：

```text
物理 GPU 拓扑结构:

单 GPU 架构:
├── GPU Card 0
│   ├── GPU 核心 (GPU Core)
│   │   ├── SM (Streaming Multiprocessor) 0-7
│   │   │   ├── CUDA 核心 (CUDA Cores): 2048-10496
│   │   │   ├── Tensor 核心 (Tensor Cores): 64-640
│   │   │   ├── RT 核心 (RT Cores): 0-80 (光线追踪)
│   │   │   └── 共享内存 (Shared Memory): 48-164 KB/SM
│   │   ├── GPU 内存层次结构
│   │   │   ├── 全局内存 (Global Memory): 8-80 GB
│   │   │   ├── 共享内存 (Shared Memory): 48-164 KB/SM
│   │   │   ├── 寄存器 (Registers): 65536/线程
│   │   │   ├── 常量内存 (Constant Memory): 64 KB
│   │   │   └── 纹理内存 (Texture Memory): 与全局内存共享
│   │   └── GPU 缓存
│   │       ├── L1 Cache: 128 KB/SM
│   │       ├── L2 Cache: 4-80 MB
│   │       └── 纹理缓存 (Texture Cache)
│   └── PCIe 接口
│       ├── PCIe 3.0 x16: 16 GB/s (单方向)
│       ├── PCIe 4.0 x16: 32 GB/s (单方向)
│       └── PCIe 5.0 x16: 64 GB/s (单方向)
└── CPU 连接
    └── PCIe 总线
        ├── CPU ↔ GPU 数据传输
        └── 命令和控制

多 GPU 架构:
├── GPU Card 0
│   ├── GPU 核心
│   ├── GPU 内存: 16-80 GB
│   └── NVLink 接口 (GPU 间互连)
│       ├── NVLink 2.0: 25 GB/s (单方向)/链路
│       └── NVLink 3.0: 50 GB/s (单方向)/链路
├── GPU Card 1
│   ├── GPU 核心
│   ├── GPU 内存: 16-80 GB
│   └── NVLink 接口 (GPU 间互连)
├── GPU Card 2-7 (可选)
│   └── NVLink 互连
└── NVLink 互连拓扑
    ├── Mesh 拓扑: 所有 GPU 互连
    ├── Ring 拓扑: GPU 环形连接
    └── 带宽: 300-600 GB/s (总带宽)

GPU 集群架构:
├── Node 0
│   ├── GPU Card 0-7 (每节点)
│   │   ├── 本地 NVLink 互连
│   │   └── PCIe 连接到 CPU
│   ├── CPU 0-N (每节点)
│   └── InfiniBand 网络接口
│       ├── InfiniBand 200 Gbps (HDR)
│       └── InfiniBand 400 Gbps (NDR)
├── Node 1-N
│   └── 相同结构
└── 高速网络互连
    ├── InfiniBand 网络
    │   ├── 200 Gbps/400 Gbps 带宽
    │   ├── 跨节点 GPU 通信
    │   └── RDMA 支持
    ├── Ethernet 网络
    │   ├── 100 Gbps/200 Gbps 带宽
    │   └── RoCE (RDMA over Converged Ethernet)
    └── GPU Direct RDMA
        ├── GPU 直接访问网络
        └── 零拷贝 GPU 通信
```

**物理 GPU 拓扑特性**：

| 特性             | 单 GPU           | 多 GPU               | GPU 集群                               |
| ---------------- | ---------------- | -------------------- | -------------------------------------- |
| **GPU 数量**     | 1                | 2-8                  | 数十到数百                             |
| **GPU 间互连**   | N/A              | NVLink 2.0/3.0       | NVLink（节点内）+ InfiniBand（节点间） |
| **统一内存空间** | 否               | 是（NVLink）         | 否（分布式）                           |
| **通信带宽**     | PCIe 16-32 GB/s  | NVLink 300-600 GB/s  | InfiniBand 200-400 Gbps                |
| **典型应用**     | 工作站、个人开发 | HPC、AI 训练         | 大规模 AI 训练、超算中心               |
| **扩展性**       | 低               | 中                   | 高                                     |
| **延迟**         | PCIe 延迟 (~1μs) | NVLink 延迟 (~100ns) | 网络延迟 (~5-10μs)                     |

### 02.2 逻辑 GPU 拓扑

#### 02.2.1 逻辑 GPU 拓扑定义

**逻辑 GPU 拓扑（Logical GPU Topology）定义**：

逻辑 GPU 拓扑是指操作系统或虚拟化层对 GPU 资源的逻辑抽象和映射关系，包括 GPU 设
备抽象、CUDA 设备、GPU 调度等。

**逻辑 GPU 拓扑类型**：

1. **GPU 设备抽象**：

   - **结构**：操作系统将 GPU 作为设备抽象（如 `/dev/nvidia0`、`/dev/nvidia1`）
   - **特征**：设备节点、设备驱动、设备管理
   - **应用**：GPU 设备访问、资源管理、设备控制

2. **CUDA 设备抽象**：

   - **结构**：CUDA Runtime 识别的逻辑 GPU 设备（cudaDevice）
   - **特征**：CUDA 设备 ID、设备属性（Compute Capability、Memory
     Size、Multi-Processor Count）、设备选择
   - **应用**：CUDA 应用开发、多 GPU 编程、GPU 资源管理

3. **GPU 调度抽象**：

   - **结构**：GPU 调度器管理的 GPU 资源队列
   - **特征**：GPU 任务队列、GPU 时间片分配、GPU 优先级、多任务 GPU 共享
   - **应用**：多任务 GPU 共享、GPU 资源调度、GPU QoS

#### 02.2.2 逻辑 GPU 拓扑在技术栈中的作用

**逻辑 GPU 拓扑映射**：

```text
逻辑 GPU 拓扑结构:

操作系统逻辑拓扑:
├── GPU 设备节点 (/dev)
│   ├── /dev/nvidia0 (GPU 0)
│   │   ├── 设备节点
│   │   ├── 设备权限
│   │   └── 设备控制接口
│   ├── /dev/nvidia1 (GPU 1)
│   ├── /dev/nvidiactl (GPU 控制节点)
│   └── /dev/nvidia-modeset (GPU 模式设置)
├── GPU 驱动
│   ├── NVIDIA Driver
│   │   ├── 内核模块 (nvidia.ko)
│   │   ├── 用户空间库 (libnvidia.so)
│   │   └── GPU 设备管理
│   └── GPU 驱动接口
│       ├── CUDA Driver API
│       ├── OpenCL Driver API
│       └── Vulkan Driver API
├── GPU 调度器
│   ├── GPU 任务队列
│   │   ├── GPU 上下文队列
│   │   ├── GPU 命令队列
│   │   └── GPU 内存队列
│   ├── GPU 时间片分配
│   │   ├── 时间片调度
│   │   ├── 优先级调度
│   │   └── 抢占式调度
│   └── GPU 资源管理
│       ├── GPU 内存管理
│       ├── GPU 计算资源管理
│       └── GPU QoS
└── GPU 文件系统 (sysfs)
    ├── /sys/class/drm/card0 (GPU 设备信息)
    └── /sys/devices/pci0000:00/0000:00:01.0 (GPU PCIe 信息)

CUDA 逻辑拓扑:
├── CUDA Device 0
│   ├── Device ID: 0
│   ├── Device Properties
│   │   ├── Compute Capability: 7.0/8.0/9.0
│   │   ├── Memory Size: 16-80 GB
│   │   ├── Multi-Processor Count: 64-128
│   │   ├── CUDA Cores: 2048-10496
│   │   ├── Tensor Cores: 64-640
│   │   └── Max Threads per Block: 1024
│   ├── CUDA Runtime 管理
│   │   ├── CUDA Context 创建
│   │   ├── CUDA Stream 管理
│   │   └── CUDA Event 管理
│   └── CUDA Memory 管理
│       ├── Global Memory
│       ├── Shared Memory
│       └── Constant Memory
├── CUDA Device 1-N (多 GPU)
│   └── 相同结构
└── CUDA Multi-GPU
    ├── Peer-to-Peer (P2P) 访问
    ├── Unified Memory (统一内存)
    └── Multi-GPU 编程

OpenCL 逻辑拓扑:
├── OpenCL Platform
│   ├── OpenCL Device 0 (GPU)
│   │   ├── Device ID: 0
│   │   ├── Device Properties
│   │   └── OpenCL Runtime 管理
│   └── OpenCL Device 1-N
└── OpenCL Context
    ├── OpenCL Command Queue
    └── OpenCL Memory

虚拟化逻辑拓扑:
├── vGPU 设备抽象
│   ├── vGPU 0 → 物理 GPU 0 (部分资源)
│   │   ├── vGPU 内存分配 (2-16 GB)
│   │   ├── vGPU 计算资源分配 (部分 SM)
│   │   └── vGPU 调度
│   ├── vGPU 1 → 物理 GPU 0 (部分资源)
│   └── vGPU 分区
│       ├── GPU MIG (Multi-Instance GPU)
│       │   ├── GPU 硬件分区
│       │   ├── 独立 GPU 实例
│       │   └── 硬件级隔离
│       └── GPU 时间片分区
│           ├── GPU 时间片调度
│           └── GPU 资源共享
└── Guest OS GPU 设备
    ├── Guest OS 识别 vGPU
    │   ├── Guest OS GPU 设备节点
    │   └── Guest OS GPU 驱动
    └── Guest OS CUDA 支持
        └── Guest OS CUDA Runtime
```

### 02.3 GPU 拓扑映射

#### 02.3.1 物理 GPU 拓扑与逻辑 GPU 拓扑映射

**映射关系**：

```text
物理 GPU 拓扑 → 逻辑 GPU 拓扑映射:

物理层:
├── GPU Card 0 (物理)
│   ├── GPU 核心 (物理)
│   │   ├── SM 0-63 (物理)
│   │   └── CUDA Cores: 2048-10496 (物理)
│   ├── GPU 内存 16-80 GB (物理)
│   │   ├── 全局内存 (物理)
│   │   └── 内存层次结构 (物理)
│   └── PCIe 3.0/4.0 x16 (物理)
└── GPU Card 1-N (物理，多 GPU)
    └── NVLink 互连 (物理)

逻辑层:
├── 操作系统视图
│   ├── /dev/nvidia0 (逻辑设备)
│   │   ├── GPU 设备节点
│   │   └── GPU 驱动管理
│   ├── GPU 调度器 (逻辑)
│   │   ├── GPU 任务队列
│   │   └── GPU 时间片分配
│   └── GPU 文件系统 (逻辑)
│       └── /sys/class/drm/card0
└── CUDA 视图
    ├── CUDA Device 0 (逻辑设备)
    │   ├── Device ID: 0
    │   ├── Device Properties
    │   └── CUDA Runtime 管理
    ├── CUDA Context (逻辑)
    │   ├── GPU 上下文创建
    │   └── GPU 内存管理
    └── CUDA Multi-GPU (逻辑)
        ├── Peer-to-Peer 访问
        └── Unified Memory
```

#### 02.3.2 各范式 GPU 拓扑结构映射

**各范式 GPU 拓扑映射矩阵**：

| 维度              | 虚拟化                       | 容器化                   | 沙盒化                       |
| ----------------- | ---------------------------- | ------------------------ | ---------------------------- |
| **物理 GPU 拓扑** | 直接访问或透传（SR-IOV/MIG） | 直接访问                 | 间接访问（通过 Host）        |
| **逻辑 GPU 拓扑** | Guest OS 独立 GPU 抽象       | Host OS 共享 GPU 抽象    | Runtime GPU 抽象（有限）     |
| **GPU 抽象**      | vGPU (虚拟 GPU)              | GPU 设备绑定             | GPU API 调用（WebGPU/WebGL） |
| **GPU 调度**      | Hypervisor GPU 调度          | Host OS GPU 调度         | Runtime GPU 调度（有限）     |
| **多 GPU 支持**   | 支持（vGPU 分配）            | 支持（GPU 设备绑定）     | 有限（Runtime 抽象）         |
| **GPU 内存管理**  | Guest OS GPU 内存管理        | Host OS GPU 内存管理     | Runtime GPU 内存管理（有限） |
| **CUDA 支持**     | 支持（Guest OS CUDA）        | 支持（Host OS CUDA）     | 有限（Runtime API）          |
| **GPU MIG**       | 支持（硬件级 GPU 分区）      | 支持（GPU MIG 设备绑定） | 不支持                       |
| **GPU 共享**      | 支持（vGPU 共享）            | 支持（GPU 设备共享）     | 不支持（API 限制）           |
| **GPU 性能**      | 中等（虚拟化开销）           | 高（直接访问）           | 低（API 抽象开销）           |

---

## 03. GPU 执行模式

### 03.1 GPU 计算模式

#### 03.1.1 GPU 计算模式定义

**GPU 计算模式（GPU Computing Mode）定义**：

GPU 计算模式是指 GPU 执行计算任务的方式，包括 CUDA 计算、OpenCL 计算、图形渲染等
。

**GPU 计算模式类型**：

1. **CUDA 计算模式**：

   - **结构**：NVIDIA CUDA 并行计算模型
   - **特征**：线程网格（Grid）、线程块（Block）、线程（Thread）、共享内存、全局
     内存
   - **应用**：深度学习、科学计算、并行计算

2. **OpenCL 计算模式**：

   - **结构**：跨平台并行计算标准
   - **特征**：工作项（Work-item）、工作组（Work-group）、设备抽象
   - **应用**：跨平台 GPU 计算

3. **图形渲染模式**：

   - **结构**：GPU 图形渲染管线（Graphics Pipeline）
   - **特征**：顶点着色器、片元着色器、光栅化
   - **应用**：图形渲染、游戏、可视化

#### 03.1.2 GPU 计算模式在各范式中的应用

**GPU 计算模式架构**：

```text
GPU 计算模式架构:

CUDA 计算模式:
├── CUDA 内核（Kernel）
│   ├── 线程网格（Grid）
│   │   ├── 线程块（Block）
│   │   │   ├── 线程（Thread）
│   │   │   └── 共享内存（Shared Memory）
│   │   └── 全局内存（Global Memory）
│   └── 常量内存（Constant Memory）
├── CUDA Runtime
│   ├── 设备管理
│   ├── 内存管理
│   └── 流管理（Stream）
└── GPU 硬件执行
    ├── SM (Streaming Multiprocessor)
    └── CUDA 核心执行

虚拟化 GPU 计算:
├── Guest OS CUDA Runtime
│   └── Guest OS GPU 驱动
├── vGPU 计算资源
│   └── 虚拟 GPU 内存、核心
└── Hypervisor GPU 调度
    └── vGPU → 物理 GPU 映射

容器化 GPU 计算:
├── Host OS CUDA Runtime
│   └── Host OS GPU 驱动
├── Container GPU 访问
│   ├── GPU 设备绑定
│   └── GPU 资源限制
└── Host OS GPU 调度
    └── 直接 GPU 访问

沙盒化 GPU 计算:
├── Runtime GPU API
│   ├── WebGPU API (WASM)
│   └── GPU API 抽象
├── Runtime GPU 资源管理
│   └── GPU 内存、计算资源抽象
└── Host OS GPU 访问
    └── Runtime → Host OS GPU 驱动
```

### 03.2 GPU 调度模式

#### 03.2.1 GPU 调度模式定义

**GPU 调度模式（GPU Scheduling Mode）定义**：

GPU 调度模式是指 GPU 资源在多任务或多虚拟机间的分配和调度方式，包括独占调度、时
间片调度、资源分区调度等。

**GPU 调度模式类型**：

1. **独占调度（Exclusive）**：

   - **结构**：GPU 被单个任务或虚拟机独占使用
   - **特征**：GPU 独占、无资源竞争、高性能
   - **应用**：高性能计算、专用 GPU 任务

2. **时间片调度（Time-Slice）**：

   - **结构**：GPU 资源通过时间片分配给多个任务
   - **特征**：GPU 资源共享、时间片切换、多任务支持
   - **应用**：多任务 GPU 共享、虚拟化环境

3. **资源分区调度（Resource Partitioning）**：

   - **结构**：GPU 资源被分区分配给多个任务（GPU MIG）
   - **特征**：GPU 硬件分区、独立 GPU 实例、硬件级隔离
   - **应用**：多租户 GPU 共享、云 GPU 服务

#### 03.2.2 GPU 调度模式在各范式中的应用

**GPU 调度模式架构**：

```text
GPU 调度模式架构:

独占调度:
├── GPU 独占访问
│   ├── 单任务独占 GPU
│   └── 无资源竞争
└── GPU 性能
    └── 最高性能

时间片调度:
├── GPU 时间片分配
│   ├── 任务 A 时间片
│   ├── 任务 B 时间片
│   └── 任务 C 时间片
├── GPU 上下文切换
│   ├── 上下文保存
│   ├── 上下文恢复
│   └── 上下文切换开销
└── GPU 资源共享
    └── 多任务 GPU 共享

资源分区调度 (GPU MIG):
├── GPU MIG 分区
│   ├── GPU Instance 0 (1/7 GPU)
│   │   ├── 独立 GPU 实例
│   │   ├── 独立 GPU 内存
│   │   └── 独立 SM 分区
│   ├── GPU Instance 1 (1/7 GPU)
│   └── GPU Instance 2-6
├── 硬件级隔离
│   ├── 独立 GPU 实例
│   ├── 独立内存空间
│   └── 独立计算资源
└── 多租户 GPU 共享
    └── 硬件级 GPU 分区

虚拟化 GPU 调度:
├── Hypervisor GPU 调度
│   ├── vGPU 时间片调度
│   ├── vGPU 资源分配
│   └── vGPU 优先级调度
└── Guest OS GPU 调度
    └── Guest OS GPU 任务队列

容器化 GPU 调度:
├── Host OS GPU 调度
│   ├── GPU 设备绑定
│   ├── GPU 资源限制 (cgroup)
│   └── GPU 时间片分配
└── Container GPU 访问
    └── 容器直接 GPU 访问

沙盒化 GPU 调度:
├── Runtime GPU 调度
│   ├── GPU API 调用队列
│   └── GPU 资源抽象
└── Host OS GPU 调度
    └── Runtime → Host OS GPU 驱动
```

### 03.3 GPU 执行模式映射

#### 03.3.1 GPU 执行模式对比矩阵

**GPU 执行模式对比矩阵**：

| 维度           | 独占调度             | 时间片调度           | 资源分区调度（GPU MIG）      |
| -------------- | -------------------- | -------------------- | ---------------------------- |
| **调度方式**   | GPU 独占             | GPU 时间片分配       | GPU 硬件分区                 |
| **GPU 共享**   | 不支持               | 支持（时间片共享）   | 支持（硬件分区共享）         |
| **GPU 性能**   | 高（独占访问）       | 中等（时间片开销）   | 高（硬件分区，无开销）       |
| **GPU 隔离**   | 物理隔离             | 时间隔离             | 硬件级隔离（GPU MIG）        |
| **上下文切换** | 无                   | 有（上下文切换开销） | 无（硬件分区）               |
| **适用场景**   | 高性能计算、专用任务 | 多任务 GPU 共享      | 多租户 GPU 共享、云 GPU 服务 |
| **GPU MIG**    | 不支持               | 不支持               | 支持（硬件级 GPU 分区）      |

#### 03.3.2 各范式 GPU 执行模式映射

**各范式 GPU 执行模式映射矩阵**：

| 维度             | 虚拟化                      | 容器化                   | 沙盒化                   |
| ---------------- | --------------------------- | ------------------------ | ------------------------ |
| **GPU 计算模式** | Guest OS CUDA/OpenCL        | Host OS CUDA/OpenCL      | Runtime GPU API（有限）  |
| **GPU 调度模式** | Hypervisor GPU 调度（vGPU） | Host OS GPU 调度         | Runtime GPU 调度（有限） |
| **GPU 共享**     | 支持（vGPU 共享）           | 支持（GPU 设备共享）     | 不支持（API 限制）       |
| **GPU MIG**      | 支持（硬件级 GPU 分区）     | 支持（GPU MIG 设备绑定） | 不支持                   |
| **GPU 性能**     | 中等（虚拟化开销）          | 高（直接访问）           | 低（API 抽象开销）       |
| **GPU 隔离**     | 硬件级隔离（vGPU）          | 逻辑隔离（设备绑定）     | 应用级隔离（API 限制）   |
| **GPU 透传**     | 支持（GPU 透传）            | 支持（GPU 设备绑定）     | 不支持                   |

---

## 04. GPU 通道模型

### 04.1 物理 GPU 通道

#### 04.1.1 物理 GPU 通道定义

**物理 GPU 通道（Physical GPU Channel）定义**：

物理 GPU 通道是指 GPU 与 CPU、内存、其他 GPU 之间的物理连接和数据传输通道，包括
PCIe 通道、NVLink 通道、InfiniBand 通道等。

**物理 GPU 通道类型**：

1. **PCIe 通道**：

   - **结构**：GPU 通过 PCIe 连接到 CPU（PCIe 3.0/4.0/5.0 x16）
   - **特征**：点对点连接、高带宽（16-64 GB/s）、低延迟（~1-2μs）
   - **应用**：GPU 与 CPU 通信、GPU 数据传输、GPU 初始化

2. **NVLink 通道**：

   - **结构**：GPU 间高速互连（NVIDIA NVLink）
   - **特征**：GPU 间点对点连接、超高带宽（NVLink 2.0: 25 GB/s/链路，NVLink 3.0:
     50 GB/s/链路）、低延迟（~100ns）
   - **应用**：多 GPU 并行计算、GPU 内存共享、GPU 间数据传输

3. **InfiniBand 通道**：

   - **结构**：跨节点 GPU 通信（GPU 集群）
   - **特征**：高速网络、高带宽（200-400 Gbps）、低延迟（~5-10μs）
   - **应用**：分布式 GPU 训练、跨节点 GPU 通信、GPU Direct RDMA

#### 04.1.2 物理 GPU 通道在技术栈中的作用

**物理 GPU 通道映射**：

```text
物理 GPU 通道结构:

PCIe 通道:
├── GPU Card 0
│   └── PCIe 3.0/4.0/5.0 x16 → CPU
│       ├── 带宽: 16-64 GB/s (单方向)
│       ├── 延迟: ~1-2μs
│       └── 点对点连接
├── GPU Card 1-N (多 GPU)
│   └── PCIe 3.0/4.0/5.0 x16 → CPU
│       └── 各自独立 PCIe 连接
└── GPU 与 CPU 通信
    ├── CPU → GPU 数据传输
    ├── GPU → CPU 数据传输
    ├── GPU 命令传输
    └── GPU 内存映射

NVLink 通道:
├── GPU Card 0
│   └── NVLink 接口
│       ├── NVLink 2.0: 25 GB/s (单方向)/链路
│       └── NVLink 3.0: 50 GB/s (单方向)/链路
├── GPU Card 1
│   └── NVLink 接口
├── NVLink 互连拓扑
│   ├── Mesh 拓扑: 所有 GPU 互连
│   │   ├── GPU 0 ↔ GPU 1
│   │   ├── GPU 0 ↔ GPU 2
│   │   └── GPU 1 ↔ GPU 2
│   ├── Ring 拓扑: GPU 环形连接
│   │   ├── GPU 0 → GPU 1 → GPU 2 → GPU 0
│   │   └── 环形通信路径
│   └── 总带宽: 300-600 GB/s (多链路聚合)
└── GPU 间通信
    ├── GPU 间数据传输
    ├── GPU 内存共享
    └── Peer-to-Peer (P2P) 访问

InfiniBand 通道:
├── Node 0
│   ├── GPU Card 0-7
│   └── InfiniBand 网卡
│       ├── InfiniBand 200 Gbps (HDR)
│       └── InfiniBand 400 Gbps (NDR)
├── Node 1-N
│   └── 相同结构
└── 跨节点 GPU 通信
    ├── InfiniBand 网络
    │   ├── 高带宽: 200-400 Gbps
    │   ├── 低延迟: ~5-10μs
    │   └── RDMA 支持
    ├── GPU Direct RDMA
    │   ├── GPU 直接访问网络
    │   └── 零拷贝 GPU 通信
    └── 分布式 GPU 训练
        ├── 跨节点 GPU 同步
        └── 分布式模型训练
```

**物理 GPU 通道特性**：

| 特性         | PCIe 通道            | NVLink 通道               | InfiniBand 通道             |
| ------------ | -------------------- | ------------------------- | --------------------------- |
| **连接方式** | 点对点（CPU ↔ GPU）  | 点对点（GPU ↔ GPU）       | 网络（节点 ↔ 节点）         |
| **带宽**     | 16-64 GB/s           | 300-600 GB/s（总带宽）    | 200-400 Gbps                |
| **延迟**     | ~1-2μs               | ~100ns                    | ~5-10μs                     |
| **距离**     | 主板内（~10cm）      | 主板内（~10cm）           | 跨节点（网络距离）          |
| **典型应用** | GPU 初始化、数据传输 | 多 GPU 并行、GPU 内存共享 | 分布式训练、跨节点 GPU 通信 |
| **扩展性**   | 低（PCIe 插槽限制）  | 中（NVLink 端口限制）     | 高（网络扩展）              |

### 04.2 逻辑 GPU 通道

#### 04.2.1 逻辑 GPU 通道定义

**逻辑 GPU 通道（Logical GPU Channel）定义**：

逻辑 GPU 通道是指操作系统或虚拟化层对 GPU 通信通道的逻辑抽象，包括 CUDA 流、GPU
命令队列、GPU 内存传输等。

**逻辑 GPU 通道类型**：

1. **CUDA 流（CUDA Stream）**：

   - **结构**：CUDA 任务执行队列（GPU 任务队列）
   - **特征**：异步执行、任务排队、流同步
   - **应用**：CUDA 并行计算、多任务 GPU 执行

2. **GPU 命令队列（GPU Command Queue）**：

   - **结构**：GPU 命令执行队列（命令缓冲区）
   - **特征**：命令排队、命令执行、命令同步
   - **应用**：GPU 命令管理、GPU 任务调度

3. **GPU 内存传输通道**：

   - **结构**：CPU ↔ GPU 内存传输通道（DMA、零拷贝）
   - **特征**：内存传输、零拷贝、GPU Direct 内存访问
   - **应用**：大数据传输、GPU 内存管理

#### 04.2.2 逻辑 GPU 通道在技术栈中的作用

**逻辑 GPU 通道映射**：

```text
逻辑 GPU 通道结构:

操作系统逻辑 GPU 通道:
├── CUDA 流 (CUDA Stream)
│   ├── Stream 0
│   │   ├── 任务队列
│   │   ├── 异步执行
│   │   └── 流同步
│   ├── Stream 1-N
│   └── 多流并行执行
├── GPU 命令队列 (Command Queue)
│   ├── 命令缓冲区
│   ├── 命令排队
│   ├── 命令执行
│   └── 命令同步
└── GPU 内存传输通道
    ├── CPU → GPU 传输
    │   ├── DMA 传输
    │   ├── 零拷贝传输
    │   └── Unified Memory
    ├── GPU → CPU 传输
    │   └── 相同机制
    └── GPU → GPU 传输 (P2P)
        ├── NVLink P2P
        └── PCIe P2P

虚拟化逻辑 GPU 通道:
├── 虚拟 CUDA 流 (vCUDA Stream)
│   ├── Guest OS CUDA 流
│   └── Hypervisor GPU 调度
├── 虚拟 GPU 命令队列 (vGPU Command Queue)
│   ├── Guest OS GPU 命令队列
│   └── Hypervisor GPU 命令管理
└── 虚拟 GPU 内存传输
    ├── Guest OS GPU 内存传输
    └── Hypervisor GPU 内存映射

容器化逻辑 GPU 通道:
├── Host OS CUDA 流
│   └── 容器直接使用 Host OS CUDA 流
├── Host OS GPU 命令队列
│   └── 容器直接使用 Host OS GPU 命令队列
└── Host OS GPU 内存传输
    └── 容器直接使用 Host OS GPU 内存传输

沙盒化逻辑 GPU 通道:
├── Runtime GPU API 调用
│   ├── WebGPU API (WASM)
│   └── GPU API 抽象
├── Runtime GPU 命令队列
│   └── Runtime 管理的 GPU 命令队列
└── Runtime GPU 内存传输
    └── Runtime 转发的 GPU 内存传输
```

### 04.3 GPU 通道映射

#### 04.3.1 物理 GPU 通道与逻辑 GPU 通道映射

**映射关系**：

```text
物理 GPU 通道 → 逻辑 GPU 通道映射:

物理层:
├── PCIe 通道 (物理)
│   ├── GPU ↔ CPU
│   └── 点对点连接
├── NVLink 通道 (物理)
│   ├── GPU ↔ GPU
│   └── GPU 间互连
└── InfiniBand 通道 (物理)
    └── 跨节点 GPU

逻辑层:
├── CUDA 流 (逻辑)
│   ├── GPU 任务队列
│   └── 异步执行
├── GPU 命令队列 (逻辑)
│   ├── GPU 命令执行
│   └── 命令同步
└── GPU 内存传输 (逻辑)
    ├── CPU ↔ GPU 数据传输
    └── GPU → GPU 数据传输 (P2P)
```

#### 04.3.2 各范式 GPU 通道模型映射

**各范式 GPU 通道映射矩阵**：

| 维度              | 虚拟化                   | 容器化                  | 沙盒化                       |
| ----------------- | ------------------------ | ----------------------- | ---------------------------- |
| **物理 GPU 通道** | 直接访问或透传           | 直接访问                | 间接访问（通过 Host）        |
| **逻辑 GPU 通道** | Guest OS CUDA 流         | Host OS CUDA 流         | Runtime GPU API（有限）      |
| **GPU 内存传输**  | Guest OS GPU 内存传输    | Host OS GPU 内存传输    | Runtime GPU 内存传输（有限） |
| **GPU 命令队列**  | Guest OS GPU 命令队列    | Host OS GPU 命令队列    | Runtime GPU 命令（有限）     |
| **CUDA 流管理**   | Guest OS CUDA 流管理     | Host OS CUDA 流管理     | Runtime GPU API 管理（有限） |
| **GPU P2P**       | 支持（Guest OS GPU P2P） | 支持（Host OS GPU P2P） | 不支持（API 限制）           |
| **通道性能**      | 中等（虚拟化开销）       | 高（直接访问）          | 低（API 抽象开销）           |
| **通道隔离**      | 硬件级隔离（透传）       | 逻辑隔离（设备绑定）    | 应用级隔离（API 限制）       |

---

## 05. GPU 设备模型

### 05.1 物理 GPU

#### 05.1.1 物理 GPU 定义

**物理 GPU（Physical GPU）定义**：

物理 GPU 是实际存在的硬件 GPU 设备，包括 GPU 卡、GPU 核心、GPU 内存等硬件组件。

**物理 GPU 特征**：

1. **硬件实现**：

   - **GPU 卡**：PCIe GPU 卡（NVIDIA/AMD/Intel）
   - **GPU 核心**：SM（流多处理器）、CUDA 核心、Tensor 核心、RT 核心
   - **GPU 内存**：全局内存（8-80 GB）、共享内存、寄存器、缓存

2. **功能特性**：

   - **并行计算**：大规模并行计算、CUDA/OpenCL 支持
   - **图形渲染**：图形管线、光线追踪、实时渲染
   - **深度学习**：Tensor 核心、混合精度计算、AI 推理

#### 05.1.2 物理 GPU 在技术栈中的作用

**物理 GPU 位置**：

```text
物理 GPU 在技术栈中的位置:

物理硬件层:
├── GPU Card 0
│   ├── GPU 核心 (GPU Core)
│   │   ├── SM 0-63 (流多处理器)
│   │   │   ├── CUDA Cores: 2048-10496
│   │   │   ├── Tensor Cores: 64-640
│   │   │   ├── RT Cores: 0-80 (光线追踪)
│   │   │   └── Shared Memory: 48-164 KB/SM
│   │   ├── GPU 内存层次结构
│   │   │   ├── Global Memory: 8-80 GB
│   │   │   ├── Shared Memory: 48-164 KB/SM
│   │   │   ├── Registers: 65536/线程
│   │   │   ├── Constant Memory: 64 KB
│   │   │   └── Texture Memory: 与全局内存共享
│   │   └── GPU 缓存
│   │       ├── L1 Cache: 128 KB/SM
│   │       ├── L2 Cache: 4-80 MB
│   │       └── Texture Cache
│   └── PCIe 接口
│       ├── PCIe 3.0/4.0/5.0 x16
│       └── GPU 间互连 (NVLink)
└── GPU Card 1-N (多 GPU)
    └── 相同结构

操作系统层:
├── GPU 设备驱动程序
│   ├── NVIDIA Driver
│   │   ├── 内核模块 (nvidia.ko)
│   │   ├── 用户空间库 (libnvidia.so)
│   │   └── GPU 设备管理
│   └── GPU 驱动接口
│       ├── CUDA Driver API
│       ├── OpenCL Driver API
│       └── Vulkan Driver API
└── GPU 设备抽象
    ├── 设备节点 (/dev/nvidia0)
    └── 设备文件系统 (sysfs)
```

### 05.2 虚拟 GPU (vGPU)

#### 05.2.1 虚拟 GPU 定义

**虚拟 GPU（vGPU - Virtual GPU）定义**：

虚拟 GPU 是指 Hypervisor 为虚拟机创建的虚拟 GPU 抽象，通过 GPU 虚拟化技术将物理
GPU 资源分配给虚拟机。

**虚拟 GPU 类型**：

1. **软件虚拟化 GPU（Software vGPU）**：

   - **结构**：Hypervisor 软件模拟 GPU（QEMU、VMware）
   - **特征**：完全软件模拟、兼容性好、性能开销大
   - **应用**：基础 GPU 虚拟化

2. **硬件辅助虚拟化 GPU（Hardware-Assisted vGPU）**：

   - **结构**：硬件支持的 GPU 虚拟化（NVIDIA vGPU、AMD MxGPU）
   - **特征**：硬件加速、高性能、硬件级隔离
   - **应用**：企业 GPU 虚拟化、云 GPU 服务

3. **GPU MIG（Multi-Instance GPU）**：

   - **结构**：GPU 硬件分区（NVIDIA A100/H100）
   - **特征**：GPU 硬件级分区、独立 GPU 实例、硬件级隔离
   - **应用**：多租户 GPU 共享、GPU 资源分区

#### 05.2.2 虚拟 GPU 在技术栈中的作用

**虚拟 GPU 映射**：

```text
虚拟化 GPU 设备模型:

Hypervisor 层:
├── 物理 GPU
│   ├── GPU Card 0
│   └── GPU Card 1-N
├── GPU 虚拟化层
│   ├── NVIDIA vGPU
│   │   ├── vGPU 管理器
│   │   ├── vGPU 调度器
│   │   └── vGPU 资源分配
│   ├── GPU MIG
│   │   ├── GPU 硬件分区
│   │   ├── GPU Instance 创建
│   │   └── GPU Instance 管理
│   └── GPU 时间片调度
│       ├── vGPU 时间片分配
│       └── vGPU 上下文切换
└── 虚拟 GPU 设备
    ├── vGPU 0 → 物理 GPU 0 (部分资源)
    │   ├── vGPU 内存分配 (2-16 GB)
    │   ├── vGPU 计算资源分配 (部分 SM)
    │   └── vGPU 调度
    ├── vGPU 1 → 物理 GPU 0 (部分资源)
    └── vGPU 2-N → 物理 GPU 0 (部分资源)

Guest OS 层:
├── 虚拟 GPU 设备驱动
│   ├── Guest OS GPU 驱动
│   │   ├── NVIDIA vGPU 驱动
│   │   └── Guest OS CUDA 支持
│   └── Guest OS GPU 设备抽象
│       ├── Guest OS GPU 设备节点
│       └── Guest OS CUDA Device
└── Guest OS GPU 应用
    ├── Guest OS CUDA 应用
    └── Guest OS GPU 计算任务

映射关系:
├── vGPU 0 → 物理 GPU 0 (部分资源)
├── vGPU 1 → 物理 GPU 0 (部分资源)
└── vGPU N → 物理 GPU 0 (部分资源)
    └── 或多个物理 GPU (GPU MIG)
```

### 05.3 逻辑 GPU

#### 05.3.1 逻辑 GPU 定义

**逻辑 GPU（Logical GPU）定义**：

逻辑 GPU 是指操作系统或容器层对 GPU 资源的逻辑抽象，包括 GPU 设备节点、CUDA 设备
等。

**逻辑 GPU 类型**：

1. **GPU 设备节点抽象**：

   - **结构**：操作系统将 GPU 抽象为设备节点（如 `/dev/nvidia0`）
   - **特征**：设备文件、设备驱动、设备管理
   - **应用**：GPU 设备访问、GPU 资源管理

2. **CUDA 设备抽象**：

   - **结构**：CUDA Runtime 识别的逻辑 GPU 设备（cudaDevice）
   - **特征**：CUDA 设备 ID、设备属性、设备选择
   - **应用**：CUDA 应用开发、多 GPU 编程

3. **容器 GPU 抽象**：

   - **结构**：容器层对 GPU 资源的逻辑抽象
   - **特征**：GPU 设备绑定、GPU 资源限制、GPU 命名空间隔离
   - **应用**：容器 GPU 访问、容器 GPU 管理

#### 05.3.2 逻辑 GPU 在技术栈中的作用

**逻辑 GPU 映射**：

```text
容器化 GPU 设备模型:

Host OS 层:
├── 物理 GPU
│   ├── GPU Card 0
│   └── GPU Card 1-N
├── GPU 设备节点 (/dev)
│   ├── /dev/nvidia0 (GPU 0)
│   ├── /dev/nvidia1 (GPU 1)
│   └── /dev/nvidiactl (GPU 控制节点)
├── GPU 驱动
│   ├── NVIDIA Driver
│   └── GPU 设备管理
└── CUDA Runtime
    ├── CUDA Device 0
    └── CUDA Device 1-N

容器层:
├── 容器 GPU 映射
│   ├── Host /dev/nvidia0 → 容器 /dev/nvidia0
│   ├── Host /dev/nvidia1 → 容器 /dev/nvidia1
│   └── GPU 设备权限映射
├── 容器 GPU 访问
│   ├── 直接访问 Host GPU
│   └── GPU 设备命名空间隔离
└── 容器 GPU 资源管理
    ├── GPU 设备绑定
    ├── GPU 资源限制 (cgroup)
    └── GPU 权限控制

沙盒化 GPU 设备模型:

Host OS 层:
├── 物理 GPU
│   └── GPU Card 0-N
├── GPU 驱动
│   └── NVIDIA Driver
└── CUDA Runtime
    └── CUDA Device 0-N

Runtime 层:
├── Wasm Runtime
│   ├── GPU API 实现 (WebGPU)
│   ├── Runtime GPU 管理
│   └── Runtime GPU 抽象
└── Runtime GPU 接口
    ├── WebGPU API
    └── GPU API 抽象

Wasm Module 层:
├── Wasm Module
│   ├── GPU API 调用 (WebGPU)
│   └── Wasm GPU 应用
└── Wasm GPU 抽象
    ├── WebGPU API
    └── GPU 计算抽象
```

### 05.4 GPU 设备模型映射

#### 05.4.1 GPU 设备模型对比矩阵

**GPU 设备模型对比矩阵**：

| 维度         | 物理 GPU       | 虚拟 GPU (vGPU)              | 逻辑 GPU                 |
| ------------ | -------------- | ---------------------------- | ------------------------ |
| **抽象层级** | 硬件物理资源   | Hypervisor 虚拟抽象          | 操作系统逻辑抽象         |
| **资源隔离** | 物理隔离       | 硬件级隔离（vGPU 分区、MIG） | 逻辑隔离（设备绑定）     |
| **GPU 访问** | 直接访问       | Hypervisor GPU 调度          | Host OS GPU 调度         |
| **GPU 性能** | 高（直接访问） | 中等（虚拟化开销）           | 高（直接访问）           |
| **GPU 共享** | 不支持         | 支持（vGPU 分区、MIG）       | 支持（设备绑定）         |
| **GPU MIG**  | 不支持         | 支持（硬件级 GPU 分区）      | 支持（GPU MIG 设备绑定） |
| **典型应用** | 物理服务器     | 虚拟化                       | 容器化                   |

#### 05.4.2 各范式 GPU 设备模型映射

**各范式 GPU 设备模型映射矩阵**：

| 维度           | 虚拟化                  | 容器化                   | 沙盒化                   |
| -------------- | ----------------------- | ------------------------ | ------------------------ |
| **物理 GPU**   | 直接访问或透传          | 直接访问                 | 间接访问（通过 Host）    |
| **虚拟 GPU**   | 支持（vGPU/vGPU MIG）   | 不支持                   | 不支持                   |
| **逻辑 GPU**   | Guest OS GPU 抽象       | Host OS GPU 抽象         | Runtime GPU 抽象（有限） |
| **GPU 抽象层** | 虚拟 GPU 层             | 无（直接访问）           | Runtime GPU API 层       |
| **GPU 隔离**   | 硬件级隔离              | 逻辑隔离                 | 应用级隔离               |
| **GPU 共享**   | 支持（vGPU 共享）       | 支持（GPU 设备共享）     | 不支持（API 限制）       |
| **GPU MIG**    | 支持（硬件级 GPU 分区） | 支持（GPU MIG 设备绑定） | 不支持                   |
| **GPU 透传**   | 支持（GPU 透传）        | 支持（GPU 设备绑定）     | 不支持                   |
| **典型应用**   | 企业虚拟化、云 GPU 服务 | 容器编排、GPU 容器       | Wasm GPU 应用、边缘计算  |

---

## 06. GPU 协议栈

### 06.1 GPU 协议栈模型

#### 06.1.1 GPU 协议栈定义

**GPU 协议栈（GPU Protocol Stack）定义**：

GPU 协议栈是指操作系统或虚拟化层管理 GPU 的软件栈，包括硬件层、驱动层、运行时层
、应用层等。

**GPU 协议栈层级**：

1. **硬件层**：

   - **物理 GPU**：GPU 卡、GPU 核心、GPU 内存、GPU 接口
   - **物理接口**：PCIe、NVLink、InfiniBand
   - **硬件协议**：PCIe 协议、NVLink 协议、GPU 硬件命令

2. **驱动层**：

   - **GPU 驱动**：NVIDIA Driver、AMD Driver、Intel Driver
   - **驱动接口**：CUDA Driver API、OpenCL Driver API、Vulkan Driver API
   - **驱动管理**：驱动加载、设备初始化、中断处理

3. **运行时层**：

   - **CUDA Runtime**：CUDA Runtime API、CUDA Context、CUDA Stream
   - **OpenCL Runtime**：OpenCL Runtime API、OpenCL Context、OpenCL Command
     Queue
   - **图形运行时**：OpenGL、Vulkan、DirectX

4. **应用层**：

   - **CUDA 应用**：CUDA 内核、CUDA 内存管理、CUDA 流管理
   - **OpenCL 应用**：OpenCL 内核、OpenCL 内存管理、OpenCL 命令队列
   - **图形应用**：图形渲染、游戏、可视化

#### 06.1.2 GPU 协议栈在各范式中的映射

**虚拟化 GPU 协议栈**：

```text
虚拟化 GPU 协议栈:

应用层:
├── Guest OS GPU 应用
│   ├── Guest OS CUDA 应用
│   ├── Guest OS OpenCL 应用
│   └── Guest OS 图形应用
└── Guest OS GPU 抽象
    ├── Guest OS CUDA Runtime
    ├── Guest OS OpenCL Runtime
    └── Guest OS 图形运行时

运行时层:
├── Guest OS CUDA Runtime
│   ├── Guest OS CUDA Context
│   ├── Guest OS CUDA Stream
│   └── Guest OS CUDA Memory
├── Guest OS OpenCL Runtime
│   ├── Guest OS OpenCL Context
│   ├── Guest OS OpenCL Command Queue
│   └── Guest OS OpenCL Memory
└── Guest OS 图形运行时
    ├── Guest OS OpenGL
    └── Guest OS Vulkan

驱动层:
├── Guest OS GPU 驱动
│   ├── Guest OS NVIDIA vGPU 驱动
│   ├── Guest OS GPU 驱动接口
│   └── Guest OS CUDA Driver API
└── Guest OS GPU 设备抽象
    ├── Guest OS GPU 设备节点
    └── Guest OS CUDA Device

虚拟化层:
├── Hypervisor GPU 管理
│   ├── vGPU 管理器
│   ├── vGPU 调度器
│   └── vGPU 资源分配
└── 虚拟 GPU 抽象
    ├── vGPU 0-N
    └── vGPU 队列管理

驱动层（Host）:
├── Host OS GPU 驱动
│   ├── Host OS NVIDIA Driver
│   ├── Host OS GPU 设备管理
│   └── Host OS CUDA Driver API
└── 物理 GPU 驱动接口
    ├── PCIe 驱动
    └── GPU 硬件接口

硬件层:
├── 物理 GPU
│   ├── GPU Card 0
│   ├── GPU 核心
│   ├── GPU 内存
│   └── GPU 接口
└── 物理接口
    ├── PCIe 总线
    ├── NVLink 互连
    └── InfiniBand 网络
```

**容器化 GPU 协议栈**：

```text
容器化 GPU 协议栈:

应用层:
├── Container GPU 应用
│   ├── Container CUDA 应用
│   ├── Container OpenCL 应用
│   └── Container 图形应用
└── Container GPU 抽象
    ├── Container CUDA Runtime
    └── Container OpenCL Runtime

运行时层:
├── Host OS CUDA Runtime
│   ├── Host OS CUDA Context
│   ├── Host OS CUDA Stream
│   └── Host OS CUDA Memory
├── Host OS OpenCL Runtime
│   ├── Host OS OpenCL Context
│   ├── Host OS OpenCL Command Queue
│   └── Host OS OpenCL Memory
└── Host OS 图形运行时
    ├── Host OS OpenGL
    └── Host OS Vulkan

驱动层:
├── Host OS GPU 驱动
│   ├── Host OS NVIDIA Driver
│   ├── Host OS GPU 设备管理
│   └── Host OS CUDA Driver API
└── 容器 GPU 设备抽象
    ├── 容器 GPU 设备映射
    └── 容器 GPU 设备访问

硬件层:
├── 物理 GPU
│   ├── GPU Card 0
│   ├── GPU 核心
│   ├── GPU 内存
│   └── GPU 接口
└── 物理接口
    ├── PCIe 总线
    ├── NVLink 互连
    └── InfiniBand 网络
```

**沙盒化 GPU 协议栈**：

```text
沙盒化 GPU 协议栈:

应用层:
├── Wasm GPU 应用
│   ├── Wasm GPU 计算应用
│   └── Wasm GPU 图形应用
└── Wasm GPU 抽象
    ├── WebGPU API
    └── GPU API 抽象

Runtime 层:
├── Wasm Runtime
│   ├── GPU API 实现 (WebGPU)
│   ├── Runtime GPU 管理
│   └── Runtime GPU 抽象
└── Runtime GPU 接口
    ├── WebGPU API
    └── GPU API 抽象

运行时层:
├── Host OS CUDA Runtime（可选）
│   └── Runtime 通过 Host OS CUDA Runtime
└── Host OS 图形运行时（可选）
    └── Runtime 通过 Host OS 图形运行时

驱动层:
├── Host OS GPU 驱动
│   ├── Host OS NVIDIA Driver
│   └── Host OS GPU 设备管理
└── Host OS GPU 设备抽象
    └── Host OS GPU 设备节点

硬件层:
├── 物理 GPU（Host）
│   ├── GPU Card 0
│   ├── GPU 核心
│   └── GPU 内存
└── 物理接口
    ├── PCIe 总线
    └── NVLink 互连
```

### 06.2 GPU 接口标准

#### 06.2.1 GPU 接口标准定义

**GPU 接口标准（GPU Interface Standard）定义**：

GPU 接口标准是指操作系统或虚拟化层提供的 GPU 访问接口标准，包括 CUDA API、OpenCL
API、图形 API 等。

**GPU 接口标准类型**：

1. **CUDA API**：

   - **CUDA Runtime API**：`cudaMalloc()`、`cudaMemcpy()`、`cudaLaunchKernel()`
   - **CUDA Driver API**：`cuDeviceGet()`、`cuCtxCreate()`、`cuMemAlloc()`
   - **应用**：NVIDIA GPU 编程、深度学习、科学计算

2. **OpenCL API**：

   - **OpenCL Runtime
     API**：`clCreateBuffer()`、`clEnqueueNDRangeKernel()`、`clEnqueueReadBuffer()`
   - **OpenCL Driver
     API**：`clGetDeviceIDs()`、`clCreateContext()`、`clCreateCommandQueue()`
   - **应用**：跨平台 GPU 编程、异构计算

3. **图形 API**：

   - **OpenGL API**：`glBindTexture()`、`glDrawArrays()`、`glBufferData()`
   - **Vulkan API**：`vkCreateBuffer()`、`vkCmdDraw()`、`vkQueueSubmit()`
   - **应用**：图形渲染、游戏、可视化

4. **WebGPU API**：

   - **WebGPU Runtime
     API**：`gpu.createBuffer()`、`gpu.createCommandEncoder()`、`gpu.createComputePipeline()`
   - **应用**：Web GPU 编程、Wasm GPU 应用、边缘计算

#### 06.2.2 GPU 接口标准在各范式中的应用

**虚拟化中的 GPU 接口**：

- **Guest OS CUDA API**：Guest OS 应用通过 Guest OS CUDA API 访问虚拟 GPU
- **Guest OS OpenCL API**：Guest OS 应用通过 Guest OS OpenCL API 访问虚拟 GPU
- **Guest OS 图形 API**：Guest OS 应用通过 Guest OS 图形 API 访问虚拟 GPU

**容器化中的 GPU 接口**：

- **Host OS CUDA API**：容器应用通过 Host OS CUDA API 访问物理 GPU
- **Host OS OpenCL API**：容器应用通过 Host OS OpenCL API 访问物理 GPU
- **Host OS 图形 API**：容器应用通过 Host OS 图形 API 访问物理 GPU

**沙盒化中的 GPU 接口**：

- **WebGPU API**：Wasm 应用通过 WebGPU API 访问 GPU（通过 Runtime）
- **Runtime GPU API**：Wasm Runtime 提供 GPU 抽象接口
- **Host OS GPU API**：Runtime 通过 Host OS GPU API 访问物理 GPU

### 06.3 各范式 GPU 栈对比

#### 06.3.1 GPU 协议栈对比矩阵

**GPU 协议栈对比矩阵**：

| 维度                 | 虚拟化                                      | 容器化                       | 沙盒化                                 |
| -------------------- | ------------------------------------------- | ---------------------------- | -------------------------------------- |
| **协议栈层级**       | Hypervisor + Guest OS（两级）               | Host OS（单级）              | Runtime + Host OS（应用级+单级）       |
| **GPU 驱动层级**     | Guest OS 驱动 + Hypervisor 驱动（两级）     | Host OS 驱动（单级）         | Runtime API + Host OS 驱动             |
| **GPU Runtime 层级** | Guest OS CUDA Runtime + Hypervisor GPU 管理 | Host OS CUDA Runtime（单级） | Runtime GPU API + Host OS CUDA Runtime |
| **性能开销**         | 高（两级协议栈开销）                        | 低（单级协议栈开销）         | 中等（Runtime + Host OS）              |
| **GPU 隔离**         | 硬件级隔离（vGPU/MIG）                      | 逻辑隔离（设备绑定）         | 应用级隔离（API 限制）                 |
| **GPU 共享**         | 支持（vGPU 共享）                           | 支持（GPU 设备共享）         | 不支持（API 限制）                     |
| **GPU 透传**         | 支持（GPU 透传）                            | 支持（GPU 设备绑定）         | 不支持                                 |
| **GPU MIG**          | 支持（硬件级 GPU 分区）                     | 支持（GPU MIG 设备绑定）     | 不支持                                 |
| **典型应用**         | 企业虚拟化、云 GPU 服务                     | 容器编排、GPU 容器           | Wasm GPU 应用、边缘计算                |

---

## 07. 虚拟化 GPU 架构

### 07.1 虚拟化 GPU 拓扑

#### 07.1.1 虚拟化 GPU 拓扑结构

**虚拟化 GPU 拓扑结构**：

```text
虚拟化 GPU 拓扑:

物理层:
├── 物理 GPU
│   ├── GPU Card 0
│   └── GPU Card 1-N
└── PCIe 接口
    └── PCIe 3.0/4.0/5.0 x16

Hypervisor 层:
├── GPU 虚拟化层
│   ├── NVIDIA vGPU
│   │   ├── vGPU 管理器
│   │   ├── vGPU 调度器
│   │   └── vGPU 资源分配
│   ├── GPU MIG
│   │   ├── GPU 硬件分区
│   │   ├── GPU Instance 创建
│   │   └── GPU Instance 管理
│   └── GPU 时间片调度
│       ├── vGPU 时间片分配
│       └── vGPU 上下文切换
└── 虚拟 GPU 设备
    ├── vGPU 0 → 物理 GPU 0 (部分资源)
    ├── vGPU 1 → 物理 GPU 0 (部分资源)
    └── vGPU 2-N → 物理 GPU 0 (部分资源)

Guest OS 层:
├── Guest OS GPU 设备抽象
│   ├── Guest OS GPU 设备节点
│   └── Guest OS CUDA Device
└── Guest OS GPU 驱动
    ├── Guest OS NVIDIA vGPU 驱动
    └── Guest OS CUDA 支持
```

### 07.2 虚拟化 GPU 设备模型

#### 07.2.1 虚拟化 GPU 设备架构

**虚拟化 GPU 设备架构**：

```text
虚拟化 GPU 设备架构:

设备抽象层:
├── 虚拟 GPU (vGPU)
│   ├── NVIDIA vGPU
│   │   ├── vGPU 硬件加速
│   │   ├── vGPU 内存分配
│   │   ├── vGPU 计算资源分配
│   │   └── vGPU 调度
│   ├── GPU MIG
│   │   ├── GPU Instance 0 (1/7 GPU)
│   │   │   ├── 独立 GPU 实例
│   │   │   ├── 独立 GPU 内存
│   │   │   └── 独立 SM 分区
│   │   ├── GPU Instance 1 (1/7 GPU)
│   │   └── GPU Instance 2-6
│   └── GPU 时间片分区
│       ├── vGPU 时间片调度
│       └── GPU 资源共享
├── Guest OS GPU 设备驱动
│   ├── Guest OS NVIDIA vGPU 驱动
│   ├── Guest OS CUDA 支持
│   └── Guest OS GPU 设备抽象
└── Guest OS GPU 应用
    ├── Guest OS CUDA 应用
    └── Guest OS GPU 计算任务

设备映射层:
├── vGPU 0 → 物理 GPU 0 (部分资源)
│   ├── vGPU 内存: 2-16 GB
│   ├── vGPU SM: 部分 SM
│   └── vGPU 调度
├── vGPU 1 → 物理 GPU 0 (部分资源)
└── vGPU N → 物理 GPU 0 (部分资源)
    └── 或多个物理 GPU (GPU MIG)
```

### 07.3 虚拟化 GPU 隔离

#### 07.3.1 虚拟化 GPU 隔离机制

**虚拟化 GPU 隔离**：

1. **硬件级隔离**：

   - **GPU MIG 隔离**：GPU 硬件级分区，每个 GPU Instance 独立隔离
   - **vGPU 隔离**：Hypervisor vGPU 资源隔离，每个 vGPU 独立资源
   - **GPU 透传隔离**：GPU 透传到虚拟机，硬件级隔离（IOMMU）

2. **虚拟设备隔离**：

   - **vGPU 抽象**：每个虚拟机拥有独立的虚拟 GPU
   - **GPU 资源分配**：Hypervisor 分配 GPU 资源给虚拟机
   - **GPU QoS**：支持 GPU QoS（服务质量）控制

3. **GPU MIG 隔离**：

   - **硬件分区**：GPU 硬件级分区（NVIDIA A100/H100）
   - **独立 GPU 实例**：每个 GPU Instance 独立隔离
   - **硬件级隔离**：GPU 内存、计算资源硬件级隔离

---

## 08. 容器化 GPU 架构

### 08.1 容器化 GPU 拓扑

#### 08.1.1 容器化 GPU 拓扑结构

**容器化 GPU 拓扑结构**：

```text
容器化 GPU 拓扑:

物理层:
├── 物理 GPU
│   ├── GPU Card 0
│   └── GPU Card 1-N
└── PCIe 接口
    └── PCIe 3.0/4.0/5.0 x16

Host OS 层:
├── GPU 设备节点 (/dev)
│   ├── /dev/nvidia0 (GPU 0)
│   ├── /dev/nvidia1 (GPU 1)
│   └── /dev/nvidiactl (GPU 控制节点)
├── GPU 驱动
│   ├── NVIDIA Driver
│   └── GPU 设备管理
└── CUDA Runtime
    ├── CUDA Device 0
    └── CUDA Device 1-N

容器层:
├── 容器 GPU 映射
│   ├── Host /dev/nvidia0 → 容器 /dev/nvidia0
│   ├── Host /dev/nvidia1 → 容器 /dev/nvidia1
│   └── GPU 设备权限映射
└── 容器 GPU 访问
    ├── 直接访问 Host GPU
    └── GPU 设备命名空间隔离
```

### 08.2 容器化 GPU 设备模型

#### 08.2.1 容器化 GPU 设备架构

**容器化 GPU 设备架构**：

```text
容器化 GPU 设备架构:

设备抽象层:
├── 容器 GPU 映射
│   ├── GPU 设备绑定
│   │   ├── Host /dev/nvidia0 → 容器 /dev/nvidia0
│   │   ├── Host /dev/nvidia1 → 容器 /dev/nvidia1
│   │   └── GPU MIG 设备绑定
│   │       ├── Host /dev/nvidia0:0 → 容器 /dev/nvidia0
│   │       └── Host /dev/nvidia0:1 → 容器 /dev/nvidia1
│   ├── GPU 设备权限映射
│   │   ├── GPU 设备权限控制
│   │   └── GPU 设备访问限制
│   └── GPU 设备命名空间隔离
│       ├── 容器 GPU 设备命名空间
│       └── GPU 设备访问隔离
├── 容器 GPU 资源管理
│   ├── GPU 设备绑定
│   ├── GPU 资源限制 (cgroup)
│   │   ├── GPU 内存限制
│   │   ├── GPU 计算资源限制
│   │   └── GPU 时间片分配
│   └── GPU 权限控制
│       ├── GPU 设备访问权限
│       └── GPU 设备访问审计
└── 容器 GPU 应用
    ├── 容器 CUDA 应用
    └── 容器 GPU 计算任务

设备共享层:
├── 容器 GPU 共享
│   ├── 多个容器共享物理 GPU
│   ├── GPU 设备命名空间隔离
│   └── GPU 权限控制
└── 容器 GPU 资源管理
    ├── GPU 资源分配
    └── GPU 资源限制
```

### 08.3 容器化 GPU 隔离

#### 08.3.1 容器化 GPU 隔离机制

**容器化 GPU 隔离**：

1. **设备命名空间隔离**：

   - **GPU 设备命名空间**：每个容器拥有独立的 GPU 设备命名空间
   - **GPU 设备节点隔离**：容器内的 GPU 设备节点与 Host OS 隔离
   - **GPU 权限隔离**：通过 GPU 权限控制实现 GPU 隔离

2. **GPU 访问控制**：

   - **cgroup GPU 控制**：通过 cgroup 控制容器 GPU 访问
   - **GPU 权限管理**：限制容器 GPU 访问权限
   - **GPU 访问审计**：记录容器 GPU 访问日志

3. **GPU 设备绑定隔离**：

   - **GPU 设备绑定**：容器绑定特定 GPU 设备节点
   - **GPU 权限映射**：Host GPU 权限映射到容器
   - **GPU 共享隔离**：多个容器共享 GPU 时进行权限隔离

---

## 09. 沙盒化 GPU 架构

### 09.1 沙盒化 GPU 拓扑

#### 09.1.1 沙盒化 GPU 拓扑结构

**沙盒化 GPU 拓扑结构**：

```text
沙盒化 GPU 拓扑:

物理层:
├── 物理 GPU（Host）
│   ├── GPU Card 0
│   └── GPU Card 1-N
└── PCIe 接口
    └── PCIe 3.0/4.0/5.0 x16

Host OS 层:
├── GPU 设备节点 (/dev)
│   ├── /dev/nvidia0 (GPU 0)
│   └── /dev/nvidia1 (GPU 1)
├── GPU 驱动
│   ├── NVIDIA Driver
│   └── GPU 设备管理
└── CUDA Runtime
    └── CUDA Device 0-N

Runtime 层:
├── Wasm Runtime
│   ├── GPU API 实现 (WebGPU)
│   ├── Runtime GPU 管理
│   └── Runtime GPU 抽象
└── Runtime GPU 接口
    ├── WebGPU API
    └── GPU API 抽象

Wasm Module 层:
├── Wasm Module
│   ├── GPU API 调用 (WebGPU)
│   └── Wasm GPU 应用
└── Wasm GPU 抽象
    ├── WebGPU API
    └── GPU 计算抽象
```

### 09.2 沙盒化 GPU 设备模型

#### 09.2.1 沙盒化 GPU 设备架构

**沙盒化 GPU 设备架构**：

```text
沙盒化 GPU 设备架构:

设备抽象层:
├── WebGPU API
│   ├── GPU 设备抽象
│   │   ├── GPU 设备选择
│   │   ├── GPU 设备属性
│   │   └── GPU 设备访问
│   ├── GPU 内存抽象
│   │   ├── GPU Buffer
│   │   ├── GPU Texture
│   │   └── GPU 内存管理
│   ├── GPU 计算抽象
│   │   ├── GPU Compute Pipeline
│   │   ├── GPU Compute Shader
│   │   └── GPU 计算任务
│   └── GPU 图形抽象
│       ├── GPU Render Pipeline
│       ├── GPU Vertex Shader
│       ├── GPU Fragment Shader
│       └── GPU 图形渲染
├── Runtime GPU 管理
│   ├── Runtime GPU 设备管理
│   ├── Runtime GPU 内存管理
│   └── Runtime GPU 任务调度
└── Runtime GPU API 接口
    ├── WebGPU API → Host OS GPU Driver
    └── Runtime GPU 调用转发

设备访问层:
├── Runtime GPU 接口
│   ├── WebGPU API → Host OS CUDA Runtime
│   ├── WebGPU API → Host OS OpenCL Runtime
│   └── WebGPU API → Host OS 图形运行时
└── Host OS GPU 访问
    ├── Runtime 转发 GPU 调用
    ├── Runtime 转发 GPU 内存操作
    └── Runtime 转发 GPU 计算任务
```

### 09.3 沙盒化 GPU 隔离

#### 09.3.1 沙盒化 GPU 隔离机制

**沙盒化 GPU 隔离**：

1. **GPU API 隔离**：

   - **API 限制**：Wasm 模块只能通过 WebGPU API 访问 GPU
   - **权限控制**：通过 Runtime GPU 权限控制设备访问
   - **最小权限原则**：只授予必要的 GPU 权限

2. **GPU 调用拦截**：

   - **GPU API 拦截**：Runtime 拦截 WebGPU API 调用
   - **权限检查**：在 API 层面进行权限检查
   - **访问控制**：限制 Wasm 模块的 GPU 访问范围

3. **GPU 资源抽象隔离**：

   - **GPU 资源抽象**：每个 Wasm 模块拥有独立的 GPU 资源抽象
   - **GPU 内存隔离**：Wasm 模块的 GPU 内存与 Host OS 隔离
   - **GPU 访问控制**：限制 Wasm 模块的 GPU 访问范围

---

## 10. GPU 架构对比矩阵

### 10.1 GPU 拓扑对比矩阵

**GPU 拓扑对比**：

| 拓扑维度        | 虚拟化                       | 容器化                   | 沙盒化                   |
| --------------- | ---------------------------- | ------------------------ | ------------------------ |
| **物理拓扑**    | 直接访问或透传（SR-IOV/MIG） | 直接访问                 | 间接访问（通过 Host）    |
| **逻辑拓扑**    | Guest OS 独立 GPU 抽象       | Host OS 共享 GPU 抽象    | Runtime GPU 抽象（有限） |
| **GPU 抽象**    | vGPU (虚拟 GPU)              | GPU 设备绑定             | GPU API 调用（WebGPU）   |
| **GPU 调度**    | Hypervisor GPU 调度          | Host OS GPU 调度         | Runtime GPU 调度（有限） |
| **多 GPU 支持** | 支持（vGPU 分配）            | 支持（GPU 设备绑定）     | 有限（Runtime 抽象）     |
| **GPU MIG**     | 支持（硬件级 GPU 分区）      | 支持（GPU MIG 设备绑定） | 不支持                   |
| **GPU 隔离**    | 硬件级隔离（vGPU/MIG）       | 逻辑隔离（设备绑定）     | 应用级隔离（API 限制）   |
| **GPU 共享**    | 支持（vGPU 共享）            | 支持（GPU 设备共享）     | 不支持（API 限制）       |

### 10.2 GPU 执行模式对比矩阵

**GPU 执行模式对比**：

| 执行模式     | 虚拟化                      | 容器化                   | 沙盒化                   |
| ------------ | --------------------------- | ------------------------ | ------------------------ |
| **计算模式** | Guest OS CUDA/OpenCL        | Host OS CUDA/OpenCL      | Runtime GPU API（有限）  |
| **调度模式** | Hypervisor GPU 调度（vGPU） | Host OS GPU 调度         | Runtime GPU 调度（有限） |
| **GPU 共享** | 支持（vGPU 共享）           | 支持（GPU 设备共享）     | 不支持（API 限制）       |
| **GPU MIG**  | 支持（硬件级 GPU 分区）     | 支持（GPU MIG 设备绑定） | 不支持                   |
| **GPU 性能** | 中等（虚拟化开销）          | 高（直接访问）           | 低（API 抽象开销）       |
| **GPU 隔离** | 硬件级隔离（vGPU）          | 逻辑隔离（设备绑定）     | 应用级隔离（API 限制）   |
| **GPU 透传** | 支持（GPU 透传）            | 支持（GPU 设备绑定）     | 不支持                   |

### 10.3 GPU 通道模型对比矩阵

**GPU 通道模型对比**：

| 通道类型         | 虚拟化                        | 容器化                  | 沙盒化                       |
| ---------------- | ----------------------------- | ----------------------- | ---------------------------- |
| **物理通道**     | PCIe/NVLink（直接访问或透传） | PCIe/NVLink（直接访问） | 间接访问（通过 Host）        |
| **逻辑通道**     | Guest OS CUDA 流              | Host OS CUDA 流         | Runtime GPU API（有限）      |
| **GPU 内存传输** | Guest OS GPU 内存传输         | Host OS GPU 内存传输    | Runtime GPU 内存传输（有限） |
| **GPU 命令队列** | Guest OS GPU 命令队列         | Host OS GPU 命令队列    | Runtime GPU 命令（有限）     |
| **CUDA 流管理**  | Guest OS CUDA 流管理          | Host OS CUDA 流管理     | Runtime GPU API 管理（有限） |
| **GPU P2P**      | 支持（Guest OS GPU P2P）      | 支持（Host OS GPU P2P） | 不支持（API 限制）           |
| **通道性能**     | 中等（虚拟化开销）            | 高（直接访问）          | 低（API 抽象开销）           |
| **通道隔离**     | 硬件级隔离（透传）            | 逻辑隔离（设备绑定）    | 应用级隔离（API 限制）       |

### 10.4 GPU 设备模型对比矩阵

**GPU 设备模型对比**：

| 设备类型     | 虚拟化                         | 容器化                         | 沙盒化                     |
| ------------ | ------------------------------ | ------------------------------ | -------------------------- |
| **设备模型** | 虚拟 GPU（vGPU/vGPU MIG）      | 逻辑 GPU（设备绑定）           | Runtime GPU 抽象（WebGPU） |
| **实现方式** | NVIDIA vGPU、GPU MIG           | GPU 设备绑定、GPU MIG 设备绑定 | WebGPU API                 |
| **性能**     | 中等（虚拟化开销）或高（透传） | 高（直接访问）                 | 低（API 抽象开销）         |
| **隔离强度** | 硬件级隔离                     | 逻辑隔离                       | 应用级隔离                 |
| **GPU 共享** | 支持（vGPU 共享）              | 支持（GPU 设备共享）           | 不支持（API 限制）         |
| **GPU MIG**  | 支持（硬件级 GPU 分区）        | 支持（GPU MIG 设备绑定）       | 不支持                     |
| **GPU 透传** | 支持（GPU 透传）               | 支持（GPU 设备绑定）           | 不支持                     |

### 10.5 GPU 协议栈对比矩阵

**GPU 协议栈对比**：

| 协议栈层次     | 虚拟化                        | 容器化               | 沙盒化                           |
| -------------- | ----------------------------- | -------------------- | -------------------------------- |
| **应用层**     | Guest OS GPU App              | Container GPU App    | Wasm GPU Module                  |
| **Runtime 层** | Guest OS CUDA Runtime         | Host OS CUDA Runtime | Runtime GPU API (WebGPU)         |
| **驱动层**     | Guest OS 驱动 + Hypervisor    | Host OS 驱动         | Runtime API + Host OS 驱动       |
| **硬件层**     | 物理 GPU                      | 物理 GPU（共享）     | 物理 GPU（共享，通过 Host）      |
| **协议栈层级** | Hypervisor + Guest OS（两级） | Host OS（单级）      | Runtime + Host OS（应用级+单级） |
| **性能开销**   | 高（两级协议栈开销）          | 低（单级协议栈开销） | 中等（Runtime + Host OS）        |
| **GPU 隔离**   | 硬件级隔离（vGPU/MIG）        | 逻辑隔离（设备绑定） | 应用级隔离（API 限制）           |
| **GPU 共享**   | 支持（vGPU 共享）             | 支持（GPU 设备共享） | 不支持（API 限制）               |

---

## 11. 参考

**关联文档**：

- **[理论模型](../01-theory-models/)** - 技术范式背后的理论模型
- **[技术名词概念论证](technical-concepts-explanation.md)** - 技术名词概念论证
- **[网络概念论证](02-network-concepts-explanation.md)** - 网络架构论证
- **[存储概念论证](03-storage-concepts-explanation.md)** - 存储架构论证
- **[CPU/内存概念论证](04-cpu-memory-concepts-explanation.md)** - CPU/内存架构论
  证
- **[GPU/IO 设备概念论证](05-gpu-io-concepts-explanation.md)** - GPU/IO 设备综合
  论证
- **[IO 设备概念论证](06-io-device-concepts-explanation.md)** - IO 设备专门论证

**外部参考**：

- [NVIDIA CUDA](https://developer.nvidia.com/cuda-zone)
- [NVIDIA vGPU](https://www.nvidia.com/en-us/data-center/virtualization/)
- [NVIDIA MIG](https://www.nvidia.com/en-us/technologies/multi-instance-gpu/)
- [NVLink](https://www.nvidia.com/en-us/data-center/nvlink/)
- [WebGPU](https://www.w3.org/TR/webgpu/)
- [OpenCL](https://www.khronos.org/opencl/)
- [GPU Passthrough](https://wiki.archlinux.org/title/PCI_passthrough_via_OVMF)

---

**文档版本**：v1.0 **最后更新**：2025-11-03 **维护者**：文档维护团队

---

_本文档为 GPU 概念与技术名词论证的核心文档，持续更新和完善中。_
