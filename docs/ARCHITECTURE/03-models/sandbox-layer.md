# 沙盒层架构

**版本**：v1.0 **最后更新：2025-11-15 **维护者**：项目团队

## 📑 目录

- [沙盒层架构](#沙盒层架构)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
  - [2 核心职责](#2-核心职责)
    - [2.1. 系统调用过滤](#21-系统调用过滤)
    - [2.2. 进程隔离](#22-进程隔离)
    - [2.3. 资源限制](#23-资源限制)
    - [2.4. 安全模型](#24-安全模型)
  - [3 架构层次](#3-架构层次)
  - [4 技术实现](#4-技术实现)
    - [4.1. seccomp-bpf](#41-seccomp-bpf)
    - [4.2. gVisor (用户态内核)](#42-gvisor-用户态内核)
    - [4.3. Firecracker (轻量级 MicroVM)](#43-firecracker-轻量级-microvm)
    - [4.4. WasmEdge (WebAssembly 运行时)](#44-wasmedge-webassembly-运行时)
  - [5 对比矩阵](#5-对比矩阵)
  - [6 安全模型](#6-安全模型)
    - [6.1. 能力闭包（Capability Closure）](#61-能力闭包capability-closure)
    - [6.2. 最小权限原则](#62-最小权限原则)
    - [6.3. 可编程策略](#63-可编程策略)
  - [7 与其他层的关系](#7-与其他层的关系)
    - [7.1. 与容器运行时层](#71-与容器运行时层)
    - [7.2. 与服务网格层](#72-与服务网格层)
    - [7.3. 与 OPA 策略层](#73-与-opa-策略层)
  - [8 演进路径](#8-演进路径)
    - [8.1. 第一阶段：基础隔离（2010-2015）](#81-第一阶段基础隔离2010-2015)
    - [8.2. 第二阶段：系统调用过滤（2015-2020）](#82-第二阶段系统调用过滤2015-2020)
    - [8.3. 第三阶段：用户态内核（2020-2025）](#83-第三阶段用户态内核2020-2025)
    - [8.4. 第四阶段：WebAssembly 沙盒（2025-）](#84-第四阶段webassembly-沙盒2025-)
  - [9 最佳实践](#9-最佳实践)
    - [9.1. 最小权限原则](#91-最小权限原则)
    - [9.2. 分层防御](#92-分层防御)
    - [9.3. 策略即代码](#93-策略即代码)
    - [9.4. 可观测性](#94-可观测性)
  - [10 参考资源](#10-参考资源)

---

## 1 概述

沙盒层（Sandbox Layer）是在容器运行时层之上，对容器内部进程进行进一步安全隔离的
抽象层。它通过系统调用过滤、文件系统隔离、网络策略等技术，将容器内进程抽象为"安
全进程"。

## 2 核心职责

### 2.1. 系统调用过滤

- **seccomp-bpf**：基于 eBPF 的系统调用过滤
- **Landlock**：文件系统访问控制
- **AppArmor/SELinux**：强制访问控制（MAC）

### 2.2. 进程隔离

- **用户命名空间**：UID/GID 映射
- **PID 命名空间**：进程树隔离
- **网络命名空间**：网络栈隔离

### 2.3. 资源限制

- **cgroup v2**：统一资源控制器
- **内存限制**：OOM 保护
- **CPU 限制**：公平调度

### 2.4. 安全模型

- **最小权限原则**：只允许必要的系统调用
- **能力边界**：Capability 控制
- **动态策略**：可编程的安全策略

## 3 架构层次

```text
┌─────────────────────────────────────┐
│      Application Layer              │
│  (业务逻辑、业务代码)                │
└─────────────────────────────────────┘
                 ▲
┌─────────────────────────────────────┐
│      Sandbox Layer                  │
│  ├─ seccomp-bpf (系统调用过滤)      │
│  ├─ Landlock (文件系统隔离)         │
│  ├─ eBPF (可编程过滤器)             │
│  ├─ User Namespace (UID/GID映射)    │
│  └─ Capability (权限控制)           │
└─────────────────────────────────────┘
                 ▲
┌─────────────────────────────────────┐
│      Container Runtime Layer        │
│  (runc, Kata, gVisor, Firecracker)  │
└─────────────────────────────────────┘
```

## 4 技术实现

### 4.1. seccomp-bpf

```yaml
# seccomp 配置文件示例
apiVersion: v1
kind: Pod
metadata:
  name: sandboxed-pod
spec:
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: profiles/restrictive.json
  containers:
    - name: app
      image: nginx:latest
```

### 4.2. gVisor (用户态内核)

- **Sentry**：Go 实现的用户态内核
- **Gofer**：文件系统代理
- **隔离级别**：介于容器和 VM 之间

### 4.3. Firecracker (轻量级 MicroVM)

- **内存占用**：< 5 MB
- **启动时间**：< 125 ms
- **适用场景**：Serverless、边缘计算

### 4.4. WasmEdge (WebAssembly 运行时)

- **沙盒隔离**：WASI 安全模型
- **启动速度**：< 1 ms
- **资源占用**：极低

## 5 对比矩阵

| 属性         | seccomp-bpf    | gVisor       | Firecracker | WasmEdge      |
| ------------ | -------------- | ------------ | ----------- | ------------- |
| **隔离级别** | 系统调用过滤   | 用户态内核   | 轻量级 VM   | WASI 沙盒     |
| **资源开销** | 极低           | 低           | 中          | 极低          |
| **启动时间** | < 1 ms         | < 50 ms      | < 125 ms    | < 1 ms        |
| **安全模型** | 系统调用白名单 | 完整内核隔离 | VM 隔离     | WASI 能力模型 |
| **适用场景** | 容器内进程隔离 | 多租户 SaaS  | Serverless  | 边缘计算      |

## 6 安全模型

### 6.1. 能力闭包（Capability Closure）

**定义**：沙盒的能力闭包 = 所有允许的系统调用的交集

```text
Capability(S) = ∩{Syscall_i | process needs Syscall_i}
```

**形式化**：

- 对于任意进程 p，其能力集 `Cap(p) ⊆ Syscall_set`
- 最小权限原则：`|Cap(p)| ≤ 35`（Google 生产数据）

### 6.2. 最小权限原则

**公理 A5**：能力闭包公理

> ∀u∈U, Capability(u) ⊆ ∩{Syscall_i | u needs Syscall_i}

**实现**：

- 只允许必要的系统调用
- 动态调整权限
- 审计和监控

### 6.3. 可编程策略

**OPA + seccomp**：

- 策略即代码（Rego）
- 动态调整
- 版本化治理

## 7 与其他层的关系

### 7.1. 与容器运行时层

```text
Container Runtime ──> Sandbox
  (进程隔离)          (系统调用过滤)
```

### 7.2. 与服务网格层

```text
Sandbox ──> Service Mesh
  (进程安全)    (流量安全)
```

### 7.3. 与 OPA 策略层

```text
Sandbox ──> OPA
  (运行时隔离)  (策略决策)
```

## 8 演进路径

### 8.1. 第一阶段：基础隔离（2010-2015）

- **技术**：Linux namespaces、cgroups
- **特点**：进程级隔离

### 8.2. 第二阶段：系统调用过滤（2015-2020）

- **技术**：seccomp、AppArmor
- **特点**：细粒度权限控制

### 8.3. 第三阶段：用户态内核（2020-2025）

- **技术**：gVisor、Firecracker
- **特点**：完整内核隔离

### 8.4. 第四阶段：WebAssembly 沙盒（2025-）

- **技术**：WasmEdge、WASI
- **特点**：极轻量、快速启动

## 9 最佳实践

### 9.1. 最小权限原则

- 只允许必要的系统调用
- 使用 seccomp 白名单
- 定期审计权限

### 9.2. 分层防御

- 容器层：进程隔离
- 沙盒层：系统调用过滤
- 服务网格层：流量安全

### 9.3. 策略即代码

- 使用 OPA 管理安全策略
- 版本化策略配置
- CI/CD 集成

### 9.4. 可观测性

- 监控系统调用
- 审计权限变更
- 追踪安全事件

## 10 参考资源

- **seccomp**：<https://www.kernel.org/doc/Documentation/prctl/seccomp_filter.txt>
- **gVisor**：<https://gvisor.dev/>
- **Firecracker**：<https://firecracker-microvm.github.io/>
- **WasmEdge**：<https://wasmedge.org/>
- **OPA**：<https://www.openpolicyagent.org/>

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 沙盒层
部分
