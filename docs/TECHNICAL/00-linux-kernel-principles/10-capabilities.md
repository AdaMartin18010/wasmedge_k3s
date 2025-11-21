# 10. Capabilities 机制

## 📑 目录

- [10. Capabilities 机制](#10-capabilities-机制)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 核心概念](#11-核心概念)
    - [1.2 与容器化的关系](#12-与容器化的关系)
  - [2 Capabilities 基础](#2-capabilities-基础)
    - [2.1 传统权限模型的问题](#21-传统权限模型的问题)
    - [2.2 Capabilities 模型](#22-capabilities-模型)
    - [2.3 Capabilities 集合](#23-capabilities-集合)
  - [3 Capabilities 类型](#3-capabilities-类型)
    - [3.1 进程 Capabilities](#31-进程-capabilities)
    - [3.2 文件 Capabilities](#32-文件-capabilities)
    - [3.3 有效 Capabilities](#33-有效-capabilities)
  - [4 主要 Capabilities](#4-主要-capabilities)
    - [4.1 网络相关](#41-网络相关)
    - [4.2 系统管理相关](#42-系统管理相关)
    - [4.3 文件系统相关](#43-文件系统相关)
    - [4.4 其他重要 Capabilities](#44-其他重要-capabilities)
  - [5 内核实现机制](#5-内核实现机制)
    - [5.1 Capabilities 数据结构](#51-capabilities-数据结构)
    - [5.2 Capabilities 检查](#52-capabilities-检查)
    - [5.3 Capabilities 传递](#53-capabilities-传递)
  - [6 容器中的应用](#6-容器中的应用)
    - [6.1 Docker 中的 Capabilities](#61-docker-中的-capabilities)
    - [6.2 Kubernetes 中的 Capabilities](#62-kubernetes-中的-capabilities)
  - [7 安全最佳实践](#7-安全最佳实践)
    - [7.1 最小权限原则](#71-最小权限原则)
    - [7.2 Capabilities 配置](#72-capabilities-配置)
  - [8 相关文档](#8-相关文档)
    - [8.1 实现细节](#81-实现细节)
    - [8.2 架构分析](#82-架构分析)
    - [8.3 理论分析](#83-理论分析)
  - [9 2025 年最新实践](#9-2025-年最新实践)
    - [9.1 安全加固最佳实践（2025）](#91-安全加固最佳实践2025)
    - [9.2 Kubernetes Pod Security Standards（2025）](#92-kubernetes-pod-security-standards2025)
    - [9.3 Docker 24.0+ Capabilities 管理（2025）](#93-docker-240-capabilities-管理2025)
  - [10 实际应用案例](#10-实际应用案例)
    - [案例 1：Web 服务器安全加固](#案例-1web-服务器安全加固)
    - [案例 2：网络工具容器](#案例-2网络工具容器)
    - [案例 3：容器运行时安全配置](#案例-3容器运行时安全配置)

---

## 1 概述

**Capabilities** 是 Linux 内核提供的细粒度权限控制机制，将传统的 root 权限分解为多个独立的权限单元，实现最小权限原则。

### 1.1 核心概念

- **权限分解**：将 root 权限分解为多个独立的 Capability
- **细粒度控制**：进程只需要获得执行特定操作所需的 Capability
- **最小权限**：遵循最小权限原则，只授予必要的权限
- **安全增强**：减少权限滥用和攻击面

### 1.2 与容器化的关系

Capabilities 在容器化中起到关键作用：

- **权限隔离**：容器内的 root 不等于宿主机的 root
- **安全加固**：通过移除不必要的 Capabilities 增强安全性
- **最小权限**：容器只获得运行所需的最小权限集
- **攻击面减少**：减少容器逃逸的风险

---

## 2 Capabilities 基础

### 2.1 传统权限模型的问题

**传统 root 权限模型**：

- 进程要么是 root（拥有所有权限），要么是普通用户（权限受限）
- root 权限过于宽泛，容易造成安全风险
- 无法实现细粒度的权限控制

**问题示例**：

```bash
# 一个只需要绑定 80 端口的 Web 服务器
# 在传统模型中，需要 root 权限
# 但实际上只需要 CAP_NET_BIND_SERVICE 这一个 Capability
```

### 2.2 Capabilities 模型

**Capabilities 模型**：

- 将 root 权限分解为多个独立的 Capability
- 进程可以拥有部分 Capability，而不需要完整的 root 权限
- 每个 Capability 对应特定的系统操作权限

**优势**：

- **细粒度控制**：精确控制进程可以执行的操作
- **最小权限**：只授予必要的权限
- **安全增强**：减少权限滥用风险

### 2.3 Capabilities 集合

每个进程有三个 Capabilities 集合：

1. **Effective（有效集）**：内核检查权限时使用的集合
2. **Permitted（允许集）**：进程可以获得的 Capability 上限
3. **Inheritable（可继承集）**：可以传递给子进程的 Capability

**Capabilities 传递规则**：

- 子进程的 Permitted = (父进程的 Inheritable ∩ 文件的 Permitted) ∪ (文件的 Inheritable)
- 子进程的 Effective = 子进程的 Permitted（如果文件设置了 Effective 标志）
- 子进程的 Inheritable = 父进程的 Inheritable

---

## 3 Capabilities 类型

### 3.1 进程 Capabilities

进程的 Capabilities 存储在 `task_struct` 中：

```c
// include/linux/sched.h
struct task_struct {
    // ...
    struct cred *cred;
    // ...
};

// include/linux/cred.h
struct cred {
    // ...
    kernel_cap_t cap_inheritable;  // 可继承集
    kernel_cap_t cap_permitted;    // 允许集
    kernel_cap_t cap_effective;    // 有效集
    kernel_cap_t cap_bset;         // 边界集（系统级限制）
    kernel_cap_t cap_ambient;      // 环境集（Linux 4.3+）
    // ...
};
```

### 3.2 文件 Capabilities

文件可以设置 Capabilities，当执行该文件时，进程会获得这些 Capability：

```bash
# 设置文件的 Capabilities
setcap cap_net_bind_service=+ep /usr/bin/myapp

# 查看文件的 Capabilities
getcap /usr/bin/myapp
# 输出：/usr/bin/myapp = cap_net_bind_service+ep
```

**文件 Capabilities 标志**：

- `e`：Effective（执行时生效）
- `p`：Permitted（允许集）
- `i`：Inheritable（可继承集）

### 3.3 有效 Capabilities

有效 Capabilities 是内核实际检查的权限集：

```c
// 检查 Capability
bool capable(int cap) {
    return ns_capable(current_user_ns(), cap);
}

// 使用示例
if (capable(CAP_NET_BIND_SERVICE)) {
    // 允许绑定特权端口
    bind(sock, addr, addrlen);
} else {
    // 权限不足
    return -EPERM;
}
```

---

## 4 主要 Capabilities

Linux 内核定义了约 40 个 Capabilities，以下是常用的：

### 4.1 网络相关

| Capability | 权限 | 说明 |
|------------|------|------|
| **CAP_NET_BIND_SERVICE** | 绑定特权端口 | 绑定 < 1024 的端口 |
| **CAP_NET_RAW** | 原始套接字 | 创建原始套接字（如 ping） |
| **CAP_NET_ADMIN** | 网络管理 | 配置网络接口、路由表等 |
| **CAP_NET_BROADCAST** | 网络广播 | 发送广播数据包 |

**示例**：

```c
// 需要 CAP_NET_BIND_SERVICE 才能绑定 80 端口
if (bind(sock, &addr, sizeof(addr)) < 0) {
    // 如果没有 CAP_NET_BIND_SERVICE，会失败
    perror("bind");
}
```

### 4.2 系统管理相关

| Capability | 权限 | 说明 |
|------------|------|------|
| **CAP_SYS_ADMIN** | 系统管理 | 广泛的系统管理权限 |
| **CAP_SYS_TIME** | 系统时间 | 修改系统时间 |
| **CAP_SYS_MODULE** | 内核模块 | 加载/卸载内核模块 |
| **CAP_SYS_RAWIO** | 原始 IO | 直接访问硬件端口 |
| **CAP_SYS_CHROOT** | 改变根目录 | 使用 chroot() |

### 4.3 文件系统相关

| Capability | 权限 | 说明 |
|------------|------|------|
| **CAP_DAC_OVERRIDE** | 绕过文件权限 | 忽略文件权限检查 |
| **CAP_DAC_READ_SEARCH** | 绕过读/搜索权限 | 忽略读和搜索权限检查 |
| **CAP_FOWNER** | 文件所有者 | 忽略文件所有者检查 |
| **CAP_FSETID** | 设置文件 ID | 设置文件的 setuid/setgid |
| **CAP_MKNOD** | 创建设备文件 | 创建特殊设备文件 |

### 4.4 其他重要 Capabilities

| Capability | 权限 | 说明 |
|------------|------|------|
| **CAP_SETUID** | 设置用户 ID | 使用 setuid() |
| **CAP_SETGID** | 设置组 ID | 使用 setgid() |
| **CAP_KILL** | 发送信号 | 向其他进程发送信号 |
| **CAP_SYS_PTRACE** | 进程跟踪 | 使用 ptrace() 跟踪进程 |
| **CAP_SYS_NICE** | 进程优先级 | 修改进程优先级 |

---

## 5 内核实现机制

### 5.1 Capabilities 数据结构

内核使用位图（bitmap）存储 Capabilities：

```c
// include/linux/capability.h
typedef struct kernel_cap_struct {
    __u32 cap[_KERNEL_CAPABILITY_U32S];
} kernel_cap_t;

// Capability 定义
#define CAP_CHOWN            0
#define CAP_DAC_OVERRIDE     1
#define CAP_DAC_READ_SEARCH  2
#define CAP_FOWNER           3
#define CAP_FSETID           4
#define CAP_KILL             5
#define CAP_SETGID           6
#define CAP_SETUID           7
// ... 更多 Capabilities
```

### 5.2 Capabilities 检查

内核在关键操作前检查 Capabilities：

```c
// kernel/capability.c
bool ns_capable(struct user_namespace *ns, int cap) {
    if (unlikely(!cap_valid(cap))) {
        pr_crit("capable() called with invalid cap=%u\n", cap);
        BUG();
    }

    if (security_capable(current_cred(), ns, cap, CAP_OPT_NONE) == 0) {
        return true;
    }

    return false;
}

// 检查示例：绑定特权端口
int inet_bind(struct socket *sock, struct sockaddr *uaddr, int addr_len) {
    // ...
    if (snum && snum < PROT_SOCK && !ns_capable(net->user_ns, CAP_NET_BIND_SERVICE)) {
        return -EACCES;
    }
    // ...
}
```

### 5.3 Capabilities 传递

Capabilities 在进程创建时传递：

```c
// kernel/fork.c
static int copy_creds(struct task_struct *p, unsigned long clone_flags) {
    struct cred *new;
    // ...
    // 计算子进程的 Capabilities
    new->cap_inheritable = p->cred->cap_inheritable;
    new->cap_permitted = cap_intersect(new->cap_permitted,
                                       cap_combine(old->cap_permitted,
                                                   old->cap_inheritable));
    new->cap_effective = new->cap_permitted;
    // ...
}
```

---

## 6 容器中的应用

### 6.1 Docker 中的 Capabilities

Docker 默认移除大部分 Capabilities，只保留必要的：

**默认 Capabilities**：

```bash
# Docker 默认保留的 Capabilities
CAP_CHOWN
CAP_DAC_OVERRIDE
CAP_FOWNER
CAP_FSETID
CAP_KILL
CAP_SETGID
CAP_SETUID
CAP_SETPCAP
CAP_NET_BIND_SERVICE
CAP_NET_RAW
CAP_SYS_CHROOT
CAP_MKNOD
CAP_AUDIT_WRITE
CAP_SETFCAP
```

**配置示例**：

```yaml
# docker-compose.yml
services:
  app:
    image: nginx
    cap_add:
      - CAP_NET_BIND_SERVICE  # 添加绑定特权端口的权限
    cap_drop:
      - ALL                   # 移除所有 Capabilities
      - CAP_SYS_ADMIN         # 移除系统管理权限
```

**命令行示例**：

```bash
# 添加 Capability
docker run --cap-add=CAP_NET_BIND_SERVICE nginx

# 移除 Capability
docker run --cap-drop=CAP_SYS_ADMIN nginx

# 使用所有 Capabilities（不推荐）
docker run --privileged nginx
```

### 6.2 Kubernetes 中的 Capabilities

Kubernetes 通过 SecurityContext 配置 Capabilities：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: app
    image: nginx
    securityContext:
      capabilities:
        add:
          - NET_BIND_SERVICE    # 添加 Capability
        drop:
          - ALL                 # 移除所有 Capabilities
          - SYS_ADMIN           # 移除特定 Capability
```

**Kubernetes Capabilities 命名**：

- Kubernetes 使用大写命名（如 `NET_BIND_SERVICE`）
- 对应内核的 `CAP_NET_BIND_SERVICE`

---

## 7 安全最佳实践

### 7.1 最小权限原则

**原则**：

- 只授予进程运行所需的最小权限集
- 移除所有不必要的 Capabilities
- 定期审查和更新 Capabilities 配置

**示例**：

```yaml
# 好的实践：只添加必要的 Capability
securityContext:
  capabilities:
    add:
      - NET_BIND_SERVICE
    drop:
      - ALL

# 不好的实践：使用所有 Capabilities
securityContext:
  capabilities:
    add:
      - ALL  # 危险！
```

### 7.2 Capabilities 配置

**配置检查清单**：

- [ ] 是否移除了 `CAP_SYS_ADMIN`（除非绝对必要）
- [ ] 是否移除了 `CAP_SYS_MODULE`（防止加载内核模块）
- [ ] 是否移除了 `CAP_SYS_RAWIO`（防止直接访问硬件）
- [ ] 是否只添加了必要的 Capabilities
- [ ] 是否使用了 `drop: ALL` 然后只添加需要的

**常见场景的 Capabilities 需求**：

| 场景 | 需要的 Capabilities |
|------|---------------------|
| Web 服务器（绑定 80/443） | `NET_BIND_SERVICE` |
| 网络工具（ping） | `NET_RAW` |
| 容器运行时 | `SYS_CHROOT`, `SETUID`, `SETGID` |
| 系统监控 | `SYS_PTRACE`（谨慎使用） |

---

## 8 相关文档

### 8.1 实现细节

- **[Seccomp 配置示例](../../ARCHITECTURE/01-implementation/03-sandboxing/seccomp-examples.md)** - Seccomp 与 Capabilities 配合使用
- **[沙盒化实现](../../ARCHITECTURE/01-implementation/03-sandboxing/)** - 沙盒化技术实现

### 8.2 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 隔离机制层次分析
- **[安全模型](../../COGNITIVE/05-decision-analysis/decision-models/01-theory-models/03-security-models.md)** - 安全机制的理论分析

### 8.3 理论分析

- **[安全模型](../../COGNITIVE/05-decision-analysis/decision-models/01-theory-models/03-security-models.md)** - 安全机制的理论分析
- **[隔离模型](../../COGNITIVE/05-decision-analysis/decision-models/01-theory-models/02-isolation-models.md)** - 隔离机制的理论分析

## 9 2025 年最新实践

### 9.1 安全加固最佳实践（2025）

**2025 年安全趋势**：最小权限原则成为标准

**推荐配置**：

```yaml
# Kubernetes Pod 安全配置（2025 推荐）
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    # 移除所有 Capabilities，然后只添加需要的
    capabilities:
      drop:
        - ALL
    runAsNonRoot: true
    runAsUser: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
        add:
          - NET_BIND_SERVICE  # 只添加必要的 Capability
```

### 9.2 Kubernetes Pod Security Standards（2025）

**Kubernetes 1.25+ Pod Security Standards**：

- **Restricted**：最严格的安全策略（推荐）
- **Baseline**：基本安全策略
- **Privileged**：无限制（不推荐）

**配置示例**：

```yaml
# Namespace 级别 Pod Security
apiVersion: v1
kind: Namespace
metadata:
  name: secure-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### 9.3 Docker 24.0+ Capabilities 管理（2025）

**Docker 24.0+ 新特性**：

- **默认 Capabilities 减少**：默认只保留必要的 Capabilities
- **安全扫描增强**：自动检测不安全的 Capabilities 配置
- **策略模板**：提供安全策略模板

**配置示例**：

```yaml
# docker-compose.yml（2025 推荐）
version: '3.8'
services:
  app:
    image: nginx
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
```

## 10 实际应用案例

### 案例 1：Web 服务器安全加固

**场景**：部署 Web 服务器，需要绑定 80/443 端口

**实现方案**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
    - containerPort: 443
    securityContext:
      # 只添加绑定端口所需的 Capability
      capabilities:
        drop:
          - ALL
        add:
          - NET_BIND_SERVICE
      runAsNonRoot: true
      runAsUser: 101  # nginx 用户
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
```

**效果**：

- 最小权限：只拥有绑定端口权限
- 安全加固：移除所有不必要的 Capabilities
- 攻击面减少：减少容器逃逸风险

### 案例 2：网络工具容器

**场景**：运行网络诊断工具（如 ping），需要网络相关 Capabilities

**实现方案**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: network-tool
spec:
  containers:
  - name: ping
    image: busybox:latest
    command: ["ping", "8.8.8.8"]
    securityContext:
      capabilities:
        drop:
          - ALL
        add:
          - NET_RAW  # ping 需要 RAW socket
      runAsNonRoot: true
      allowPrivilegeEscalation: false
```

**效果**：

- 精确权限：只添加网络工具所需的 Capability
- 安全隔离：其他操作被禁止
- 功能完整：ping 功能正常工作

### 案例 3：容器运行时安全配置

**场景**：配置容器运行时（如 containerd）的安全策略

**实现方案**：

```toml
# /etc/containerd/config.toml
version = 2

[plugins."io.containerd.grpc.v1.cri".containerd]
  default_runtime_name = "runc"

  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
    runtime_type = "io.containerd.runc.v2"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
      # 默认移除所有 Capabilities
      SystemdCgroup = true
      # 安全配置
      NoNewPrivileges = true
      # 默认 Capabilities（空列表）
      DefaultCapabilities = []
```

**效果**：

- 默认安全：所有容器默认无特权
- 最小权限：需要显式添加 Capabilities
- 安全审计：便于安全审计和合规

---

**最后更新**：2025-11-15
**文档状态**：✅ 完整 | 📊 包含内核实现分析、2025 年最新实践、实际应用案例 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
