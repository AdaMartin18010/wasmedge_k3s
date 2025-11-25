# 概念定义：VM、Container、Sandbox、Service Mesh、OPA

## 📑 目录

- [概念定义：VM、Container、Sandbox、Service Mesh、OPA](#概念定义vmcontainersandboxservice-meshopa)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 核心思想](#11-核心思想)
  - [2 核心概念定义](#2-核心概念定义)
    - [2.1 VM（虚拟机）](#21-vm虚拟机)
    - [2.2 Container（容器）](#22-container容器)
    - [2.3 Sandbox（沙盒）](#23-sandbox沙盒)
    - [2.4 Service（服务）](#24-service服务)
    - [2.5 VirtualNode（虚拟节点）](#25-virtualnode虚拟节点)
    - [2.6 Edge（边）](#26-edge边)
    - [2.7 Policy（策略）](#27-policy策略)
  - [3 Service Mesh 概念](#3-service-mesh-概念)
    - [3.1 Service Mesh](#31-service-mesh)
    - [3.2 NSM（Network Service Mesh）](#32-nsmnetwork-service-mesh)
  - [4 OPA 概念](#4-opa-概念)
    - [4.1 OPA（Open Policy Agent）](#41-opaopen-policy-agent)
    - [4.2 Policy（策略）](#42-policy策略)
  - [5 概念关系代数](#5-概念关系代数)
    - [5.1 关系代数定义](#51-关系代数定义)
    - [5.2 关系定义](#52-关系定义)
  - [6 形式化定义](#6-形式化定义)
    - [6.1 概念定义](#61-概念定义)
    - [6.2 关系定义](#62-关系定义)
    - [6.3 属性定义](#63-属性定义)
  - [7 概念属性映射](#7-概念属性映射)
    - [7.1 属性映射表](#71-属性映射表)
    - [7.2 形式化映射](#72-形式化映射)
  - [8 总结](#8-总结)

---

## 1 概述

本文档详细定义**虚拟化、容器化、沙盒化、Service Mesh、OPA**等核心概念，建立概念
属性关系的基础。

### 1.1 核心思想

> **通过形式化定义核心概念，建立概念属性关系的基础，支持后续的矩阵分析和关系图构
> 建**

## 2 核心概念定义

### 2.1 VM（虚拟机）

**定义**：VM = ⟨vCPU, vMEM, vIO, vNetwork, config⟩

**属性**：

- **vCPU**：虚拟 CPU 核心集合
- **vMEM**：虚拟内存
- **vIO**：虚拟 I/O 设备
- **vNetwork**：虚拟网络设备
- **config**：VM 配置（镜像、快照、迁移策略）

**关系**：

- **运行于**：Hypervisor（KVM、Xen、Hyper-V）
- **包含**：Container（VM 可以运行容器）
- **抽象自**：物理硬件

### 2.2 Container（容器）

**定义**：Container = ⟨image, namespace, cgroup, runtime⟩

**属性**：

- **image**：容器镜像（OCI Image）
- **namespace**：命名空间（pid, mnt, net, ipc, uts, user）
- **cgroup**：资源限制（CPU、内存、I/O）
- **runtime**：容器运行时（runc、containerd）

**关系**：

- **由 Runtime 创建**：containerd、CRI-O
- **包含**：Sandbox（容器可以运行沙盒）
- **抽象自**：VM 或物理硬件

### 2.3 Sandbox（沙盒）

**定义**：Sandbox = ⟨seccomp, filesystem, network, capability, runtime⟩

**属性**：

- **seccomp**：系统调用过滤规则
- **filesystem**：文件系统访问控制
- **network**：网络策略
- **capability**：Linux Capability 集合
- **runtime**：沙盒运行时（gVisor、Firecracker、WasmEdge）

**关系**：

- **由 Sandbox Runtime 创建**：gVisor、Firecracker
- **抽象自**：Container

### 2.4 Service（服务）

**定义**：Service = ⟨name, label, port, endpoints⟩

**属性**：

- **name**：服务名称
- **label**：标签集合
- **port**：端口号
- **endpoints**：端点集合（Pod IP:Port）

**关系**：

- **指向**：Pod 集合
- **抽象自**：Pod IP:Port

### 2.5 VirtualNode（虚拟节点）

**定义**：VirtualNode = ⟨identity, labels, endpoints⟩

**属性**：

- **identity**：SPIFFE ID
- **labels**：标签集合
- **endpoints**：端点集合

**关系**：

- **映射到**：U 子集（VM/Container/Sandbox）
- **抽象自**：物理节点

### 2.6 Edge（边）

**定义**：Edge = ⟨source, destination, weight, policy⟩

**属性**：

- **source**：源节点
- **destination**：目标节点
- **weight**：权重（流量分配）
- **policy**：策略配置（安全、限流、熔断）

**关系**：

- **连接**：VirtualNode → VirtualNode
- **抽象自**：物理网络连接

### 2.7 Policy（策略）

**定义**：Policy = ⟨type, rules, version⟩

**属性**：

- **type**：策略类型（elastic, security, observability）
- **rules**：规则集合（Rego 规则）
- **version**：版本信息（Git SHA）

**关系**：

- **附加到**：Edge
- **抽象自**：安全基线、运维规则

## 3 Service Mesh 概念

### 3.1 Service Mesh

**定义**：ServiceMesh = ⟨sidecars, controlPlane, policies⟩

**属性**：

- **sidecars**：侧车代理集合（Envoy）
- **controlPlane**：控制平面（Istio Pilot、Linkerd Control Plane）
- **policies**：策略配置（VirtualService、DestinationRule）

**关系**：

- **包含**：Sidecar、Control Plane
- **抽象自**：网络代理

### 3.2 NSM（Network Service Mesh）

**定义**：NSM = ⟨vL3, vWire, endpoints, clients⟩

**属性**：

- **vL3**：虚拟 L3 网络
- **vWire**：虚拟隧道集合
- **endpoints**：端点集合
- **clients**：客户端集合

**关系**：

- **包含**：vL3、vWire、Endpoints
- **抽象自**：物理网络

## 4 OPA 概念

### 4.1 OPA（Open Policy Agent）

**定义**：OPA = ⟨PDP, PEP, OCP, Bundle, DecisionLog⟩

**属性**：

- **PDP**：策略决策点
- **PEP**：策略执行点集合
- **OCP**：OPA 控制平面
- **Bundle**：策略包集合
- **DecisionLog**：决策日志

**关系**：

- **包含**：PDP、PEP、OCP
- **抽象自**：策略引擎

### 4.2 Policy（策略）

**定义**：Policy = ⟨rego, data, version⟩

**属性**：

- **rego**：Rego 规则
- **data**：数据集合
- **version**：版本信息（Git SHA）

**关系**：

- **包含在**：Bundle
- **抽象自**：安全基线

## 5 概念关系代数

### 5.1 关系代数定义

**关系代数 ℳ** = ⟨U, Svc, Vn, e, p⟩

**满足**：

- U ⊆ (U_vm ∪ U_c ∪ U_s)
- e ⊆ Vn × Vn × ℝ⁺ (weight)
- p : e → Policy DSL

### 5.2 关系定义

| 关系                      | 定义                                              | 典型属性                       | 例子                       |
| ------------------------- | ------------------------------------------------- | ------------------------------ | -------------------------- |
| **虚拟化 ⊃ 容器化**       | VM 提供完整 OS，容器在其上共享内核                | 隔离级别由 VM → OS → Namespace | KVM + Docker               |
| **容器化 ⊃ 沙盒化**       | 容器提供进程隔离，沙盒在此基础上加细粒度安全      | 安全边界由 Namespace → eBPF    | Docker + seccomp           |
| **沙盒化 ↔ 服务网格**     | 沙盒控制进程，服务网格控制流量                    | 统一安全：最小权限 + mTLS      | Istio + seccomp            |
| **服务网格 ↔ NSM**        | 服务网格为侧车，NSM 为网络抽象                    | 统一网络治理：vWire            | Istio + NSM                |
| **NSM ↔ 分布式系统**      | NSM 通过 vWire 把跨域节点聚合，分布式系统提供共识 | 可聚合多域                     | Kubernetes + NSM + Raft    |
| **动态运维 ↔ 以上所有层** | GitOps、监控、弹性伸缩在每层提供自适应机制        | 自动化                         | Argo CD + Prometheus + HPA |

## 6 形式化定义

### 6.1 概念定义

```text
概念 C = ⟨name, type, properties, relations⟩
其中：
- name: 概念名称
- type: 概念类型
- properties: 属性集合
- relations: 关系集合
```

### 6.2 关系定义

```text
关系 R = ⟨source, target, type, properties⟩
其中：
- source: 源概念
- target: 目标概念
- type: 关系类型（⊃, ↔, →）
- properties: 关系属性
```

### 6.3 属性定义

```text
属性 P = ⟨name, type, value, constraints⟩
其中：
- name: 属性名称
- type: 属性类型
- value: 属性值
- constraints: 约束条件
```

## 7 概念属性映射

### 7.1 属性映射表

**属性映射**：

```text
- 可组合：所有层都实现接口化（API, gRPC, BPF program）
- 弹性：每层支持动态扩容/缩容（VM Live‑Migrate, Container HPA, Service‑Mesh Traffic Shaping）
- 安全：从硬件隔离到进程过滤，最终到流量加密
- 可观测：从容器内部的 metrics（cAdvisor）到 Mesh 级别的 tracing（OpenTelemetry）
```

### 7.2 形式化映射

```text
同态 φ: (Ω,∘) → ℝ³
其中：
- ℝ³ = (Latency↑, Security↓, Observability→)
- φ 将每个概念映射到性能/安全/观测三元组
```

## 8 总结

通过**概念定义**，我们建立了：

1. **核心概念**：VM、Container、Sandbox、Service Mesh、OPA 的形式化定义
2. **概念属性**：每个概念都有明确的属性定义
3. **概念关系**：概念之间的关系通过关系代数定义
4. **形式化框架**：建立了完整的形式化框架
5. **属性映射**：建立了属性到三元组的映射

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
1153-1169 行，概念定义部分
