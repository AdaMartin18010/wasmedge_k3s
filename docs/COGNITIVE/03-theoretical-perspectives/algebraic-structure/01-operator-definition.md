# 算子定义：20 个一元算子

## 📑 目录

- [算子定义：20 个一元算子](#算子定义20-个一元算子)
  - [📑 目录](#-目录)
  - [1 算子概述](#1-算子概述)
  - [2 20 个一元算子详解](#2-20-个一元算子详解)
    - [2.1 虚拟化算子（V）](#21-虚拟化算子v)
    - [2.2 镜像打包算子（I）](#22-镜像打包算子i)
    - [2.3 容器化算子（C）](#23-容器化算子c)
    - [2.4 沙盒化算子（S）](#24-沙盒化算子s)
    - [2.5 服务网格算子（M）](#25-服务网格算子m)
    - [2.6 其他算子](#26-其他算子)
      - [Kc：Kata-runtime](#kckata-runtime)
      - [G：gVisor](#ggvisor)
      - [F：Firecracker](#ffirecracker)
      - [W：WasmEdge](#wwasmedge)
      - [Am：Ambient Mesh](#amambient-mesh)
      - [P：eBPF](#pebpf)
      - [Otel：OpenTelemetry](#otelopentelemetry)
      - [Gk：Gatekeeper](#gkgatekeeper)
      - [Cc：Confidential Container](#ccconfidential-container)
  - [3 算子三元组解构](#3-算子三元组解构)
  - [4 算子映射关系](#4-算子映射关系)
  - [5 参考](#5-参考)

---

## 1 算子概述

**算子（Operator）** 是一元变换，将一种技术对象转换为另一种技术对象。

**核心特征**：

- **一元变换**：`ω: Ω → Ω'`，将对象 `x` 转换为对象 `x'`
- **生成子结构**：每个算子都能"生成"一种更高级的技术对象
- **代数属性**：满足幂等、交换、结合等代数性质

**算子分类**：

| 类别       | 算子            | 作用域        | 生成对象               |
| ---------- | --------------- | ------------- | ---------------------- |
| **虚拟化** | V, Kc, F, G, Cc | 物理 → 虚拟   | VM, MicroVM            |
| **打包**   | I               | 二进制 → 镜像 | Image                  |
| **运行时** | C, W, We        | 镜像 → 运行时 | Container, WasmRuntime |
| **安全**   | S, P, Ns, Cg    | 运行时 → 沙盒 | Sandbox, eBPF Program  |
| **网络**   | M, Am, E, Ist   | 运行时 → 网格 | Mesh Container         |
| **观测**   | Otel            | 运行时 → 观测 | Telemetry              |
| **策略**   | Gk              | 运行时 → 策略 | Policy                 |

## 2 20 个一元算子详解

### 2.1 虚拟化算子（V）

**符号**：`V`

**名称**：Virtualization（虚拟化）

**作用**：`V: Binary → VM`

**典型实现**：

- KVM（Linux 内核态）
- Xen（裸机）
- Hyper-V（微软）
- bhyve（FreeBSD）

**生成对象**：VM（虚拟机）

**三元组解构**：

- **Σ（状态空间）**：VMCS, EPT, VT-x
- **Δ（迁移规则）**：VM-Exit/Entry
- **Λ（观测函数）**：perf, KVM trace

**代数属性**：

- **幂等性**：V² ≠ I（嵌套虚拟化需硬件解锁）
- **交换性**：V∘C ≠ C∘V（页表深度不同）

**2025 年更新**：

- 支持嵌套虚拟化（Intel VT-x/AMD-V）
- 支持机密计算（SGX/SEV）
- 支持 IOMMU 设备直通

### 2.2 镜像打包算子（I）

**符号**：`I`

**名称**：Image-packing（镜像打包）

**作用**：`I: Binary → Image`

**典型实现**：

- OCI Image Spec
- Image Index（多架构）
- Layer blob（分层存储）

**生成对象**：Image（镜像）

**三元组解构**：

- **Σ（状态空间）**：tar+gzip, OCI, layer-hash
- **Δ（迁移规则）**：docker build, commit
- **Λ（观测函数）**：docker history, cosign

**代数属性**：

- **幂等性**：I² = I（镜像幂等）
- **交换性**：I∘C = C∘I（可与容器交换）

**2025 年更新**：

- 支持多架构镜像（arm64, amd64, riscv64）
- 支持 SBOM（软件物料清单）
- 支持 cosign 签名和 attestation

### 2.3 容器化算子（C）

**符号**：`C`

**名称**：Containerization（容器化）

**作用**：`C: Image → Container`

**典型实现**：

- runc（OCI 标准）
- crun（C 语言实现，更快）
- youki（Rust 实现）
- Kata-runtime（VM 级容器）

**生成对象**：Container（容器）

**三元组解构**：

- **Σ（状态空间）**：namespace, cgroup, seccomp
- **Δ（迁移规则）**：clone(), setns()
- **Λ（观测函数）**：/proc, cadvisor, runc events

**代数属性**：

- **幂等性**：C² = C（容器理想）
- **交换性**：C∘S = S∘C（可与沙盒交换）

**2025 年更新**：

- 支持 WasmEdge 运行时
- 支持 eBPF 增强
- 支持 cgroup v2

### 2.4 沙盒化算子（S）

**符号**：`S`

**名称**：Sandbox（沙盒化）

**作用**：`S: Container → Sandbox Container`

**典型实现**：

- seccomp-bpf（系统调用过滤）
- Landlock（文件系统沙盒）
- AppArmor, SELinux（MAC）

**生成对象**：Sandbox Container（沙盒容器）

**三元组解构**：

- **Σ（状态空间）**：seccomp-BPF, Landlock, rlimit
- **Δ（迁移规则）**：syscall filter
- **Λ（观测函数）**：auditd, Falco

**代数属性**：

- **幂等性**：S² = S（沙盒商对象）
- **交换性**：S∘C = C∘S（可与容器交换）
- **短正合列**：`0 → Ker(S) → Ω → Im(S) → 0`

**2025 年更新**：

- 支持 Landlock（Linux 5.13+）
- 支持 eBPF LSM（Linux 5.7+）
- 支持 Capsicum（FreeBSD）

### 2.5 服务网格算子（M）

**符号**：`M`

**名称**：Mesh-inject（服务网格注入）

**作用**：`M: Container → Mesh Container`

**典型实现**：

- Istio sidecar（Envoy 代理）
- Linkerd proxy
- Cilium Service Mesh（eBPF 加速）
- Istio Ambient Mesh（无 Sidecar 模式）

**生成对象**：Mesh Container（带服务网格的容器）

**三元组解构**：

- **Σ（状态空间）**：xDS, Envoy config, cluster, VirtualService, DestinationRule
- **Δ（迁移规则）**：RDS/CDS update, sidecar injection, traffic routing
- **Λ（观测函数）**：Prometheus metrics, OpenTelemetry traces, Envoy access logs

**代数属性**：

- **幂等性**：M² = M（服务网格幂等，多次注入等于一次注入）
- **交换性**：M∘C = C∘M（可与容器交换），M∘S = S∘M（可与沙盒交换）
- **组合性**：M∘Am ≃ M（Ambient Mesh 是 M 的特殊形式）

**技术背景**：

根据 Wikipedia（as of 2025-11-04），**Service Mesh（服务网格）**是用于处理服务间
通信的基础设施层：

> "A service mesh is a dedicated infrastructure layer for handling
> service-to-service communication. It is typically composed of lightweight
> network proxies that are deployed alongside application code, without the
> application needing to be aware."

**2025 年更新**：

- **Istio Ambient Mesh**（2022 年引入，2025 年成熟）：

  - 无 Sidecar 模式，资源占用 20MB/服务
  - 延迟开销 < 0.3ms（相比 Sidecar 模式的 0.5ms）
  - 通过 ztunnel（L4）和 waypoint proxy（L7）实现

- **Cilium Service Mesh**（2024 年 GA，2025 年成熟）：

  - 基于 eBPF 的 L4/L7 负载均衡
  - 延迟开销 < 10μs（L4），< 50μs（L7）
  - 资源占用 15MB（系统级，非每 Pod）

- **Wasm 插件热加载**（2025 年新特性）：
  - Envoy Wasm 插件支持热加载
  - WasmEdge 集成，支持边缘计算场景

**组件详解**：

1. **控制平面（Control Plane）**：

   - **Istiod**：Istio 控制平面，管理配置和策略
   - **xDS API**：配置发现协议（CDS, EDS, LDS, RDS）
   - **配置模型**：VirtualService, DestinationRule, Gateway, PeerAuthentication

2. **数据平面（Data Plane）**：

   - **Sidecar 模式**：每个 Pod 注入 Envoy 代理（50-200MB/Pod）
   - **Ambient 模式**：节点级 ztunnel（L4）+ 按需 waypoint proxy（L7）
   - **Envoy 代理**：L4/L7 代理，支持 HTTP/gRPC/WebSocket 等协议

3. **功能组件**：
   - **流量治理**：负载均衡、路由、灰度发布、A/B 测试
   - **零信任安全**：自动 mTLS、服务间认证、授权策略
   - **可观测性**：自动生成 Trace/Metric/Log，无需应用埋点

**使用场景**：

- **微服务架构**：服务数量 >50，需要统一的服务间通信治理
- **多云环境**：跨云、跨集群的服务发现和路由
- **边缘计算**：边缘节点的服务间通信治理（Cilium Service Mesh）

**组合与聚合**：

- **M∘C**：容器 + 服务网格（标准组合）
- **M∘S**：沙盒 + 服务网格（高安全场景）
- **M∘Am**：Ambient Mesh（无 Sidecar，资源优化）
- **M∘Otel**：服务网格 + OpenTelemetry（完整可观测性）

**权威引用**：

1. **Wikipedia（2025-11-04）**：

   - [Service Mesh](https://en.wikipedia.org/wiki/Service_mesh)
   - [Istio](https://en.wikipedia.org/wiki/Istio)
   - [Envoy Proxy](https://en.wikipedia.org/wiki/Envoy_Proxy)

2. **学术研究**：
   - NIST Service Mesh Proxy Models（2023）
   - MIT 服务网格架构研究（2024）
   - Stanford 服务网格性能评估（2025）

**性能指标**（2025 年基准）：

| 模式        | 延迟开销（p50） | 延迟开销（p99） | 资源占用       | 适用场景           |
| ----------- | --------------- | --------------- | -------------- | ------------------ |
| **无 Mesh** | 0ms             | 0ms             | 0MB            | 单机应用           |
| **Sidecar** | 0.5ms           | 1.2ms           | 50-200MB/Pod   | 中大规模集群       |
| **Ambient** | 0.3ms           | 0.8ms           | 20MB/服务      | 大规模集群（推荐） |
| **Cilium**  | < 10μs（L4）    | < 50μs（L7）    | 15MB（系统级） | 高性能场景         |

- Cilium Service Mesh

**生成对象**：Mesh Container（网格容器）

**三元组解构**：

- **Σ（状态空间）**：xDS, Envoy config, cluster
- **Δ（迁移规则）**：RDS/CDS update
- **Λ（观测函数）**：Prometheus, OTLP

**代数属性**：

- **幂等性**：M² = M（网格吸收）
- **交换性**：M∘C = C∘M（可与容器交换）
- **交换性**：M∘W = W∘M（可与 WasmEdge 交换）

**2025 年更新**：

- 支持 Istio Ambient Mesh（无 Sidecar）
- 支持 Wasm 插件热加载
- 支持 OTLP 统一遥测

### 2.6 其他算子

#### Kc：Kata-runtime

- **作用**：`Kc: Binary → Kata-VM-Container`
- **特点**：VM 级容器，强隔离

#### G：gVisor

- **作用**：`G: Binary → User-Kernel Container`
- **特点**：用户态内核，轻量隔离

#### F：Firecracker

- **作用**：`F: Binary → microVM`
- **特点**：极轻量 VM，冷启动 < 2ms

#### W：WasmEdge

- **作用**：`W: Binary → Wasm Runtime`
- **特点**：冷启动 < 10ms，内存 < 50MB

#### Am：Ambient Mesh

- **作用**：`Am: Container → Ambient Mesh`
- **特点**：无 Sidecar，资源占用 20MB/服务

#### P：eBPF

- **作用**：`P: Kernel → eBPF Program`
- **特点**：内核可编程，零开销观测

#### Otel：OpenTelemetry

- **作用**：`Otel: Runtime → Telemetry`
- **特点**：统一遥测标准，OTLP 协议

#### Gk：Gatekeeper

- **作用**：`Gk: Runtime → Policy`
- **特点**：OPA 准入控制，策略即代码

#### Cc：Confidential Container

- **作用**：`Cc: Container → Confidential Container`
- **特点**：SGX/SEV 机密计算，硬件级隔离

## 3 算子三元组解构

每个算子都可以拆解为三元组 `⟨Σ, Δ, Λ⟩`：

| 算子  | Σ（状态空间）              | Δ（迁移规则）        | Λ（观测函数）          |
| ----- | -------------------------- | -------------------- | ---------------------- |
| **V** | VMCS, EPT, VT-x            | VM-Exit/Entry        | perf, KVM trace        |
| **I** | tar+gzip, OCI, layer-hash  | docker build, commit | docker history, cosign |
| **C** | namespace, cgroup, seccomp | clone(), setns()     | /proc, cadvisor        |
| **S** | seccomp-BPF, Landlock      | syscall filter       | auditd, Falco          |
| **M** | xDS, Envoy config, cluster | RDS/CDS update       | Prometheus, OTLP       |

## 4 算子映射关系

**对象全集**：Ω = {Binary, Image, Container, Pod, Sidecar, Mesh, VM, HW, Kernel,
Syscall}

**算子映射**：

```text
V: Binary → VM
I: Binary → Image
C: Image → Container
S: Container → Sandbox Container
M: Container → Mesh Container
```

**复合映射**：

```text
I∘C: Binary → Image → Container
C∘S: Container → Sandbox Container
C∘M: Container → Mesh Container
I∘C∘S∘M: Binary → Image → Container → Sandbox → Mesh
```

## 5 参考

**关联文档**：

- **[算子定义](./01-operator-definition.md)** - 20 个一元算子详解
- **[代数结构](./02-algebraic-structure.md)** - 代数结构 Σ = ⟨Ω, ℱ, 𝒫, ℒ⟩
- **[公理体系](./03-axioms.md)** - 公理 A1-A7
- **[复合运算表](./04-composition-table.md)** - 20×20 运算表

**外部参考**：

- [Virtualization (Wikipedia)](https://en.wikipedia.org/wiki/Virtualization)
- [Containerization (Wikipedia)](https://en.wikipedia.org/wiki/Containerization)
- [Service Mesh (CNCF)](https://www.cncf.io/blog/2017/04/25/service-mesh/)
- [OCI Image Spec](https://github.com/opencontainers/image-spec)
- [WasmEdge](https://wasmedge.org/)

---

**最后更新**：2025-11-04 **维护者**：项目团队
