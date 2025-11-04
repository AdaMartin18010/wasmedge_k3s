# 概念属性关系矩阵

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
- [2. 核心概念定义](#2-核心概念定义)
  - [2.1 计算单元概念](#21-计算单元概念)
  - [2.2 网络概念](#22-网络概念)
  - [2.3 策略概念](#23-策略概念)
- [3. 属性矩阵](#3-属性矩阵)
  - [3.1 隔离属性矩阵](#31-隔离属性矩阵)
  - [3.2 资源属性矩阵](#32-资源属性矩阵)
  - [3.3 安全属性矩阵](#33-安全属性矩阵)
- [4. 关系图谱](#4-关系图谱)
  - [4.1 包含关系](#41-包含关系)
  - [4.2 组合关系](#42-组合关系)
  - [4.3 依赖关系](#43-依赖关系)
- [5. 概念属性关系表](#5-概念属性关系表)
  - [5.1 VM 概念属性关系](#51-vm-概念属性关系)
  - [5.2 Container 概念属性关系](#52-container-概念属性关系)
  - [5.3 Sandbox 概念属性关系](#53-sandbox-概念属性关系)
- [6. 组合关系图谱](#6-组合关系图谱)
  - [6.1 计算单元组合](#61-计算单元组合)
  - [6.2 网络组合](#62-网络组合)
  - [6.3 策略组合](#63-策略组合)
- [7. 属性传递关系](#7-属性传递关系)
  - [7.1 隔离属性传递](#71-隔离属性传递)
  - [7.2 安全属性传递](#72-安全属性传递)
  - [7.3 可观测性属性传递](#73-可观测性属性传递)
- [8. 概念演进关系](#8-概念演进关系)
  - [8.1 历史演进](#81-历史演进)
  - [8.2 技术演进](#82-技术演进)
  - [8.3 架构演进](#83-架构演进)
- [9. 形式化关系定义](#9-形式化关系定义)
  - [9.1 包含关系](#91-包含关系)
  - [9.2 组合关系](#92-组合关系)
  - [9.3 依赖关系](#93-依赖关系)
- [10. 2025 年 11 月最新趋势](#10-2025-年-11-月最新趋势)
  - [10.1 概念演进](#101-概念演进)
  - [10.2 属性演进](#102-属性演进)
  - [10.3 关系演进](#103-关系演进)
- [11. 参考资源](#11-参考资源)

---

## 1. 概述

本文档从概念、属性、关系的角度系统梳理虚拟化、容器化、沙盒化、Service
Mesh、NSM、OPA 等云原生架构技术的概念属性关系。

---

## 2. 核心概念定义

### 2.1 计算单元概念

| 概念          | 定义                       | 形式化描述                                    |
| ------------- | -------------------------- | --------------------------------------------- |
| **VM**        | 虚拟机，完整模拟物理硬件   | VM = ⟨vCPU, vMEM, vIO⟩                        |
| **Container** | 容器，共享内核的进程集合   | C = ⟨processes, namespaces, cgroups⟩          |
| **Sandbox**   | 沙盒，细粒度安全隔离的进程 | S = ⟨process, filters, eBPF programs⟩         |
| **Pod**       | Kubernetes 最小调度单元    | P = {Container₁, Container₂, ..., Containerₙ} |

### 2.2 网络概念

| 概念             | 定义                       | 形式化描述                               |
| ---------------- | -------------------------- | ---------------------------------------- |
| **Service**      | Kubernetes 服务，虚拟 IP   | Svc = ⟨name, selector, port⟩             |
| **Service Mesh** | 服务网格，流量治理         | SM = ⟨dataPlane, controlPlane, policies⟩ |
| **NSM**          | 网络服务网格，跨域网络聚合 | NS = ⟨vL3, vWire, endpoints⟩             |
| **vWire**        | 虚拟线路，逻辑隧道         | vWire = ⟨client, endpoint, policy⟩       |

### 2.3 策略概念

| 概念           | 定义               | 形式化描述                         |
| -------------- | ------------------ | ---------------------------------- |
| **OPA**        | 开放策略代理       | OPA = ⟨PDP, PEP, Bundle, Policy⟩   |
| **Policy**     | 策略，访问控制规则 | P = ⟨condition, action, effect⟩    |
| **Constraint** | 约束，资源限制规则 | C = ⟨resource, limit, enforcement⟩ |

---

## 3. 属性矩阵

### 3.1 隔离属性矩阵

| 概念             | 隔离级别 | 隔离粒度 | 隔离方式    | 隔离保证   |
| ---------------- | -------- | -------- | ----------- | ---------- |
| **VM**           | 硬件级   | 完整 OS  | VT-x/SVM    | 强隔离     |
| **Container**    | OS 级    | 进程     | namespace   | 中等隔离   |
| **Sandbox**      | 进程级   | 系统调用 | seccomp-bpf | 细粒度隔离 |
| **Service Mesh** | 网络级   | 流量     | mTLS        | 网络隔离   |

### 3.2 资源属性矩阵

| 概念             | 资源开销 | 启动时间 | 内存占用   | CPU 开销 |
| ---------------- | -------- | -------- | ---------- | -------- |
| **VM**           | 高       | 10-30s   | 2-3× RAM   | 5-10%    |
| **Container**    | 中       | <1s      | 共享内核   | 1-2%     |
| **Sandbox**      | 低       | <1s      | 与容器同级 | 0.5-1%   |
| **Service Mesh** | 中       | <1s      | 50-100MB   | 2-5%     |

### 3.3 安全属性矩阵

| 概念          | 安全模型      | 安全边界 | 安全保证 | 合规支持 |
| ------------- | ------------- | -------- | -------- | -------- |
| **VM**        | 隔离+快照     | 硬件边界 | 强       | 高       |
| **Container** | 隔离+Overlay  | OS 边界  | 中       | 中       |
| **Sandbox**   | 最小权限+eBPF | 进程边界 | 强       | 高       |
| **OPA**       | 策略即代码    | 策略边界 | 可证明   | 高       |

---

## 4. 关系图谱

### 4.1 包含关系

```text
VM ⊃ Container ⊃ Sandbox
│
├─ VM 包含完整 OS
├─ Container 在 VM 或物理机上运行
└─ Sandbox 在 Container 内运行
```

### 4.2 组合关系

```text
Pod ──> Container ──> Runtime ──> Kernel
 │        │            │           │
 └─ Service ──> Service Mesh ──> NSM ──> Network
```

### 4.3 依赖关系

```text
Application ──> Service Mesh ──> NSM ──> Container ──> Kernel ──> Hardware
     │              │            │           │            │           │
     └─ OPA ──> Policy ──> Constraint ──> Security ──> Isolation ──> Trust
```

---

## 5. 概念属性关系表

### 5.1 VM 概念属性关系

| 属性         | 值     | 关系        | 说明                             |
| ------------ | ------ | ----------- | -------------------------------- |
| **隔离级别** | 硬件级 | ⊃ Container | VM 提供比容器更强的隔离          |
| **资源开销** | 高     | > Container | VM 占用更多资源                  |
| **启动时间** | 10-30s | > Container | VM 启动更慢                      |
| **安全保证** | 强     | = Sandbox   | VM 和 Sandbox 提供相似的安全保证 |
| **可移植性** | 高     | = Container | VM 和 Container 都支持跨平台     |

### 5.2 Container 概念属性关系

| 属性         | 值    | 关系            | 说明                              |
| ------------ | ----- | --------------- | --------------------------------- |
| **隔离级别** | OS 级 | ⊂ VM, ⊃ Sandbox | Container 介于 VM 和 Sandbox 之间 |
| **资源开销** | 中    | < VM, > Sandbox | Container 资源开销适中            |
| **启动时间** | <1s   | < VM, ≈ Sandbox | Container 启动快速                |
| **安全保证** | 中    | < VM, < Sandbox | Container 安全保证中等            |
| **可组合性** | 高    | > VM            | Container 支持更好的组合          |

### 5.3 Sandbox 概念属性关系

| 属性         | 值     | 关系              | 说明                         |
| ------------ | ------ | ----------------- | ---------------------------- |
| **隔离级别** | 进程级 | ⊂ Container       | Sandbox 在 Container 内运行  |
| **资源开销** | 低     | < Container       | Sandbox 资源开销低           |
| **启动时间** | <1s    | ≈ Container       | Sandbox 启动快速             |
| **安全保证** | 强     | ≥ VM              | Sandbox 提供强安全保证       |
| **可编程性** | 高     | > VM, > Container | Sandbox 支持 eBPF 可编程策略 |

---

## 6. 组合关系图谱

### 6.1 计算单元组合

```text
Hardware
    │
    ├─ VT-x/SVM ──> Hypervisor ──> VM
    │
    ├─ cgroup/namespace ──> Kernel ──> Container
    │
    └─ seccomp-bpf ──> Sandbox Runtime ──> Sandbox
```

### 6.2 网络组合

```text
Container ──> Service ──> Service Mesh ──> NSM ──> vWire ──> Endpoint
    │            │             │            │         │
    └─ CNI ──> Network ──> Envoy ──> vL3 ──> Policy
```

### 6.3 策略组合

```text
Application ──> OPA ──> Policy ──> Constraint ──> Enforcement
    │            │        │             │
    └─ Service Mesh ──> Authorization ──> Access Control
```

---

## 7. 属性传递关系

### 7.1 隔离属性传递

```text
Hardware Isolation
    │
    ├─ VT-x/SVM ──> VM Isolation
    │
    ├─ namespace ──> Container Isolation
    │
    └─ seccomp-bpf ──> Sandbox Isolation
```

### 7.2 安全属性传递

```text
Hardware Trust (TPM/SGX)
    │
    ├─ Hypervisor Security ──> VM Security
    │
    ├─ Kernel Security ──> Container Security
    │
    └─ eBPF Security ──> Sandbox Security
```

### 7.3 可观测性属性传递

```text
Hardware Metrics
    │
    ├─ Hypervisor Metrics ──> VM Metrics
    │
    ├─ Kernel Metrics ──> Container Metrics
    │
    └─ eBPF Metrics ──> Sandbox Metrics
         │
         └─ OpenTelemetry ──> Service Mesh Metrics
```

---

## 8. 概念演进关系

### 8.1 历史演进

```text
裸机 (1970s)
    │
    ├─ 虚拟化 (2000s) ──> VM
    │
    ├─ 容器化 (2010s) ──> Container
    │
    └─ 沙盒化 (2020s) ──> Sandbox
```

### 8.2 技术演进

```text
传统架构
    │
    ├─ 虚拟化 ──> 云原生
    │
    ├─ 容器化 ──> Kubernetes
    │
    └─ 沙盒化 ──> Serverless
```

### 8.3 架构演进

```text
单体架构
    │
    ├─ 微服务 ──> Service Mesh
    │
    ├─ 多集群 ──> NSM
    │
    └─ 边缘计算 ──> Edge Computing
```

---

## 9. 形式化关系定义

### 9.1 包含关系

**VM ⊃ Container ⊃ Sandbox**:

**形式化**：

**∀ Container c, ∃ VM v, c ∈ v** **∀ Sandbox s, ∃ Container c, s ∈ c**

### 9.2 组合关系

**Compose(Container, Service Mesh) → Service**:

**形式化**：

**Compose: C × SM → S**:

### 9.3 依赖关系

**Application → Service Mesh → NSM → Container → Kernel**:

**形式化**：

**Depends: App → SM → NSM → C → K**:

---

## 10. 2025 年 11 月最新趋势

### 10.1 概念演进

- **机密计算**：从 VM 到机密容器的演进
- **边缘计算**：从 Container 到边缘容器的演进
- **Serverless**：从 Sandbox 到无服务器函数的演进

### 10.2 属性演进

- **隔离属性**：从硬件级到进程级的细粒度演进
- **资源属性**：从高开销到低开销的优化演进
- **安全属性**：从隔离到可证明安全的演进

### 10.3 关系演进

- **组合关系**：从单一组合到多维度组合的演进
- **依赖关系**：从强耦合到松耦合的演进
- **演进关系**：从传统架构到云原生架构的演进

---

## 11. 参考资源

- **概念定义**：CNCF 云原生术语表
- **属性矩阵**：Kubernetes 官方文档
- **关系图谱**：C4 Model 架构图
- **形式化定义**：范畴论和类型论
- **相关文档**：
  - `08-concepts-relations/concept-definitions.md` - 概念定义
  - `08-concepts-relations/property-relations.md` - 属性关系
  - `08-concepts-relations/relationship-graph.md` - 关系图谱

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 概念属
性矩阵部分
