# 08. Namespace 机制详解

## 📑 目录

- [08. Namespace 机制详解](#08-namespace-机制详解)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 核心概念](#11-核心概念)
    - [1.2 与容器化的关系](#12-与容器化的关系)
  - [2 Namespace 基础](#2-namespace-基础)
    - [2.1 Namespace 类型](#21-namespace-类型)
    - [2.2 Namespace 数据结构](#22-namespace-数据结构)
  - [3 Namespace 类型详解](#3-namespace-类型详解)
    - [3.1 PID Namespace](#31-pid-namespace)
    - [3.2 Network Namespace](#32-network-namespace)
    - [3.3 Mount Namespace](#33-mount-namespace)
    - [3.4 User Namespace](#34-user-namespace)
    - [3.5 UTS Namespace](#35-uts-namespace)
    - [3.6 IPC Namespace](#36-ipc-namespace)
  - [4 Namespace API](#4-namespace-api)
    - [4.1 clone() 系统调用](#41-clone-系统调用)
    - [4.2 unshare() 系统调用](#42-unshare-系统调用)
    - [4.3 setns() 系统调用](#43-setns-系统调用)
  - [5 内核实现机制](#5-内核实现机制)
    - [5.1 Namespace 创建流程](#51-namespace-创建流程)
    - [5.2 Namespace 查找机制](#52-namespace-查找机制)
    - [5.3 Namespace 引用计数](#53-namespace-引用计数)
  - [6 容器中的应用](#6-容器中的应用)
    - [6.1 Docker 中的 Namespace 使用](#61-docker-中的-namespace-使用)
    - [6.2 runc 中的实现](#62-runc-中的实现)
  - [7 性能与限制](#7-性能与限制)
    - [7.1 性能特点](#71-性能特点)
    - [7.2 限制](#72-限制)
  - [8 相关文档](#8-相关文档)
    - [8.1 实现细节](#81-实现细节)
    - [8.2 架构分析](#82-架构分析)
    - [8.3 理论分析](#83-理论分析)
  - [9 2025 年最新实践](#9-2025-年最新实践)
    - [9.1 Linux 6.1+ Namespace 增强（2025）](#91-linux-61-namespace-增强2025)
    - [9.2 containerd 2.0+ Namespace 管理（2025）](#92-containerd-20-namespace-管理2025)
    - [9.3 Kubernetes 1.30+ Namespace 支持（2025）](#93-kubernetes-130-namespace-支持2025)
  - [10 实际应用案例](#10-实际应用案例)
    - [案例 1：多租户容器隔离](#案例-1多租户容器隔离)
    - [案例 2：高性能网络应用](#案例-2高性能网络应用)
    - [案例 3：容器化 CI/CD 系统](#案例-3容器化-cicd-系统)

---

## 1 概述

**Namespace** 是 Linux 内核提供的进程隔离机制，允许不同进程组拥有独立的系统资源视图，这是容器化技术的基础。

### 1.1 核心概念

- **隔离边界**：每个 Namespace 提供独立的资源视图
- **进程组织**：进程可以属于多个不同类型的 Namespace
- **层次结构**：某些 Namespace 支持嵌套（如 PID Namespace）
- **轻量级**：相比虚拟化，Namespace 开销极小

### 1.2 与容器化的关系

Namespace 是容器化的核心机制之一：

- **进程隔离**：PID Namespace 提供独立的进程树
- **网络隔离**：Network Namespace 提供独立的网络栈
- **文件系统隔离**：Mount Namespace 提供独立的挂载点视图
- **用户隔离**：User Namespace 提供独立的用户 ID 映射

---

## 2 Namespace 基础

### 2.1 Namespace 类型

Linux 内核支持以下 Namespace 类型：

| Namespace | 标志位 | 隔离内容 | 内核版本 |
|-----------|--------|----------|----------|
| **PID** | CLONE_NEWPID | 进程 ID | 2.6.24+ |
| **Network** | CLONE_NEWNET | 网络栈 | 2.6.29+ |
| **Mount** | CLONE_NEWNS | 挂载点 | 2.4.19+ |
| **UTS** | CLONE_NEWUTS | 主机名和域名 | 2.6.19+ |
| **IPC** | CLONE_NEWIPC | 进程间通信 | 2.6.19+ |
| **User** | CLONE_NEWUSER | 用户和组 ID | 3.8+ |
| **Cgroup** | CLONE_NEWCGROUP | Cgroup 视图 | 4.6+ |
| **Time** | CLONE_NEWTIME | 系统时间 | 5.6+ |

### 2.2 Namespace 数据结构

内核中的 Namespace 数据结构（简化）：

```c
// include/linux/nsproxy.h
struct nsproxy {
    atomic_t count;
    struct uts_namespace *uts_ns;
    struct ipc_namespace *ipc_ns;
    struct pid_namespace *pid_ns_for_children;
    struct net *net_ns;
    struct cgroup_namespace *cgroup_ns;
    struct time_namespace *time_ns;
    struct time_namespace *time_ns_for_children;
    struct mnt_namespace *mnt_ns;
    struct user_namespace *user_ns;
};
```

每个进程的 `task_struct` 包含一个 `nsproxy` 指针，指向其所属的 Namespace 集合。

---

## 3 Namespace 类型详解

### 3.1 PID Namespace

**功能**：隔离进程 ID，每个 PID Namespace 有独立的进程 ID 空间。

**内核实现**：

```c
// include/linux/pid_namespace.h
struct pid_namespace {
    struct idr idr;
    struct rcu_head rcu;
    unsigned int pid_allocated;
    struct task_struct *child_reaper;
    struct kmem_cache *pid_cachep;
    unsigned int level;
    struct pid_namespace *parent;
    // ...
};
```

**特性**：

- **层次结构**：支持嵌套，子 Namespace 可以看到父 Namespace 的进程
- **init 进程**：每个 PID Namespace 有自己的 init 进程（PID 1）
- **进程树**：每个 Namespace 维护独立的进程树

**示例**：

```bash
# 创建新的 PID Namespace
unshare --pid --fork /bin/bash

# 在新 Namespace 中，PID 1 是当前 shell
echo $$
# 输出：1
```

### 3.2 Network Namespace

**功能**：隔离网络栈，每个 Network Namespace 有独立的网络接口、路由表、防火墙规则。

**内核实现**：

```c
// include/net/net_namespace.h
struct net {
    refcount_t      count;
    spinlock_t      rules_mod_lock;
    struct list_head list;
    struct list_head cleanup_list;
    struct list_head exit_list;
    struct proc_dir_entry *proc_net;
    struct proc_dir_entry *proc_net_stat;
    struct ctl_table_set sysctls;
    // ...
};
```

**特性**：

- **独立网络栈**：每个 Namespace 有独立的网络设备、路由表、iptables 规则
- **veth 对**：通过 veth pair 连接不同 Network Namespace
- **网络隔离**：不同 Namespace 的网络完全隔离

**示例**：

```bash
# 创建新的 Network Namespace
ip netns add mynetns

# 在 Namespace 中创建 veth 对
ip link add veth0 type veth peer name veth1
ip link set veth1 netns mynetns

# 配置网络
ip addr add 10.0.0.1/24 dev veth0
ip netns exec mynetns ip addr add 10.0.0.2/24 dev veth1
```

### 3.3 Mount Namespace

**功能**：隔离文件系统挂载点，每个 Mount Namespace 有独立的挂载点视图。

**内核实现**：

```c
// include/linux/mnt_namespace.h
struct mnt_namespace {
    atomic_t        count;
    struct ns_common ns;
    struct mount *  root;
    struct list_head list;
    struct user_namespace *user_ns;
    struct ucounts *ucounts;
    u64 seq;
    // ...
};
```

**特性**：

- **挂载传播**：支持 shared、private、slave、unbindable 等传播类型
- **根文件系统**：每个 Namespace 可以有独立的根文件系统视图
- **容器根文件系统**：容器通过 Mount Namespace 实现文件系统隔离

**示例**：

```bash
# 创建新的 Mount Namespace
unshare --mount --fork /bin/bash

# 在新 Namespace 中挂载文件系统
mount -t tmpfs tmpfs /tmp
# 这个挂载只在当前 Namespace 中可见
```

### 3.4 User Namespace

**功能**：隔离用户和组 ID，允许在容器内以 root 身份运行，但在宿主机上映射为非特权用户。

**内核实现**：

```c
// include/linux/user_namespace.h
struct user_namespace {
    struct uid_gid_map uid_map;
    struct uid_gid_map gid_map;
    struct uid_gid_map projid_map;
    atomic_t count;
    struct user_namespace *parent;
    int level;
    // ...
};
```

**特性**：

- **UID/GID 映射**：容器内的 UID 映射到宿主机的不同 UID
- **权限隔离**：容器内的 root 不等于宿主机的 root
- **安全增强**：减少容器逃逸的风险

**示例**：

```bash
# 创建新的 User Namespace
unshare --user --map-root-user --fork /bin/bash

# 在新 Namespace 中，当前用户是 root
id
# 输出：uid=0(root) gid=0(root) groups=0(root)

# 但在宿主机上，仍然是普通用户
```

### 3.5 UTS Namespace

**功能**：隔离主机名和域名。

**内核实现**：

```c
// include/linux/utsname.h
struct uts_namespace {
    struct kref kref;
    struct new_utsname name;
    struct user_namespace *user_ns;
    struct ucounts *ucounts;
    struct ns_common ns;
};
```

**示例**：

```bash
# 创建新的 UTS Namespace
unshare --uts --fork /bin/bash

# 设置主机名
hostname mycontainer
# 这个主机名只在当前 Namespace 中可见
```

### 3.6 IPC Namespace

**功能**：隔离进程间通信对象（消息队列、信号量、共享内存）。

**内核实现**：

```c
// include/linux/ipc_namespace.h
struct ipc_namespace {
    struct kref kref;
    struct idr ids[3];
    int sem_ctls[4];
    int used_sems;
    unsigned int msg_ctlmax;
    unsigned int msg_ctlmnb;
    unsigned int msg_ctlmni;
    // ...
};
```

---

## 4 Namespace API

### 4.1 clone() 系统调用

创建新进程时指定 Namespace：

```c
#include <sched.h>

pid_t clone(int (*fn)(void *), void *stack, int flags, void *arg, ...);
```

**flags 参数**：

- `CLONE_NEWPID`：创建新的 PID Namespace
- `CLONE_NEWNET`：创建新的 Network Namespace
- `CLONE_NEWNS`：创建新的 Mount Namespace
- `CLONE_NEWUTS`：创建新的 UTS Namespace
- `CLONE_NEWIPC`：创建新的 IPC Namespace
- `CLONE_NEWUSER`：创建新的 User Namespace
- `CLONE_NEWCGROUP`：创建新的 Cgroup Namespace
- `CLONE_NEWTIME`：创建新的 Time Namespace

**示例**：

```c
#define STACK_SIZE (1024 * 1024)
static char child_stack[STACK_SIZE];

int child_main(void *arg) {
    printf("Child PID: %d\n", getpid());
    system("hostname mycontainer");
    execv("/bin/bash", (char *[]){"/bin/bash", NULL});
    return 0;
}

int main() {
    pid_t pid = clone(child_main,
                      child_stack + STACK_SIZE,
                      CLONE_NEWPID | CLONE_NEWUTS | SIGCHLD,
                      NULL);
    waitpid(pid, NULL, 0);
    return 0;
}
```

### 4.2 unshare() 系统调用

将当前进程移到新的 Namespace：

```c
#include <sched.h>

int unshare(int flags);
```

**示例**：

```c
// 创建新的 PID 和 UTS Namespace
unshare(CLONE_NEWPID | CLONE_NEWUTS);
```

### 4.3 setns() 系统调用

将当前进程加入已存在的 Namespace：

```c
#include <sched.h>

int setns(int fd, int nstype);
```

**fd**：通过 `/proc/[pid]/ns/` 目录下的文件描述符获取。

**示例**：

```c
// 打开目标进程的 Network Namespace
int fd = open("/proc/1234/ns/net", O_RDONLY);
// 加入该 Namespace
setns(fd, CLONE_NEWNET);
close(fd);
```

---

## 5 内核实现机制

### 5.1 Namespace 创建流程

1. **用户空间调用**：`clone()`、`unshare()` 或 `setns()`
2. **系统调用入口**：进入内核空间
3. **权限检查**：检查是否有权限创建/加入 Namespace
4. **Namespace 创建**：分配并初始化 Namespace 结构
5. **进程关联**：将进程的 `nsproxy` 指向新的 Namespace
6. **资源初始化**：初始化 Namespace 相关的资源

### 5.2 Namespace 查找机制

内核通过 `task_struct->nsproxy` 查找进程所属的 Namespace：

```c
// 获取进程的 PID Namespace
struct pid_namespace *task_active_pid_ns(struct task_struct *tsk) {
    return ns_of_pid(task_pid(tsk));
}
```

### 5.3 Namespace 引用计数

每个 Namespace 使用引用计数管理生命周期：

```c
// 增加引用计数
get_nsproxy(old_nsproxy);

// 减少引用计数
put_nsproxy(nsproxy);
```

当引用计数为 0 时，Namespace 被销毁。

---

## 6 容器中的应用

### 6.1 Docker 中的 Namespace 使用

Docker 为每个容器创建以下 Namespace：

- **PID Namespace**：容器内进程树隔离
- **Network Namespace**：容器网络隔离
- **Mount Namespace**：容器文件系统隔离
- **UTS Namespace**：容器主机名隔离
- **IPC Namespace**：容器 IPC 隔离
- **User Namespace**：容器用户隔离（可选）

### 6.2 runc 中的实现

runc 通过 `clone()` 系统调用创建容器进程：

```go
// 设置 clone flags
cloneFlags := syscall.CLONE_NEWPID | syscall.CLONE_NEWNS |
              syscall.CLONE_NEWNET | syscall.CLONE_NEWUTS |
              syscall.CLONE_NEWIPC

// 创建容器进程
cmd := exec.Command("/proc/self/exe", "init")
cmd.SysProcAttr = &syscall.SysProcAttr{
    Cloneflags: cloneFlags,
}
```

---

## 7 性能与限制

### 7.1 性能特点

- **低开销**：Namespace 切换开销极小（纳秒级）
- **内存占用**：每个 Namespace 占用少量内存
- **无额外延迟**：不影响进程调度和系统调用性能

### 7.2 限制

- **内核共享**：所有容器共享同一个内核
- **内核漏洞影响**：内核漏洞可能影响所有容器
- **资源竞争**：虽然隔离，但仍共享底层硬件资源

---

## 8 相关文档

### 8.1 实现细节

- **[Namespace 配置示例](../../ARCHITECTURE/01-implementation/02-containerization/namespace-examples.md)** - 实际配置示例
- **[容器化实现](../../ARCHITECTURE/01-implementation/02-containerization/)** - 容器化技术实现

### 8.2 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 隔离机制层次分析
- **[容器化架构视角](../../ARCHITECTURE/02-views/02-virtualization-containerization-sandboxing/)** - 容器化抽象层

### 8.3 理论分析

- **[隔离模型](../../COGNITIVE/05-decision-analysis/decision-models/01-theory-models/02-isolation-models.md)** - 隔离机制的理论分析

## 9 2025 年最新实践

### 9.1 Linux 6.1+ Namespace 增强（2025）

**最新内核版本**：Linux 6.1+（2025 年）

**新特性**：

- **Time Namespace 增强**：支持更精确的时间隔离
- **User Namespace 改进**：更好的安全性和性能
- **PID Namespace 优化**：减少嵌套 Namespace 的开销
- **Network Namespace 性能提升**：更快的网络栈初始化

**内核版本要求**：

```bash
# 检查内核版本
uname -r
# 推荐：6.1+ 或 5.15 LTS

# 检查 Namespace 支持
ls /proc/self/ns/
# 应该看到：pid, net, mnt, uts, ipc, user, cgroup, time
```

### 9.2 containerd 2.0+ Namespace 管理（2025）

**containerd 2.0+ 新特性**：

- **统一 Namespace 管理**：更好的 Namespace 生命周期管理
- **性能优化**：减少 Namespace 创建和销毁的开销
- **安全增强**：默认启用 User Namespace

**配置示例**：

```toml
# /etc/containerd/config.toml
version = 2

[plugins."io.containerd.grpc.v1.cri"]
  # 启用 User Namespace（2025 推荐）
  enable_userns = true

  # Namespace 配置
  [plugins."io.containerd.grpc.v1.cri".containerd]
    default_runtime_name = "runc"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
      runtime_type = "io.containerd.runc.v2"
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
        # 启用所有 Namespace
        SystemdCgroup = true
```

### 9.3 Kubernetes 1.30+ Namespace 支持（2025）

**Kubernetes 1.30+ 新特性**：

- **User Namespace 支持**：Pod 级别的 User Namespace
- **Network Namespace 共享**：支持 Pod 内容器共享 Network Namespace
- **PID Namespace 共享**：支持 Pod 内容器共享 PID Namespace

**配置示例**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: shared-ns-pod
spec:
  shareProcessNamespace: true  # 共享 PID Namespace
  containers:
  - name: app1
    image: nginx
  - name: app2
    image: nginx
```

## 10 实际应用案例

### 案例 1：多租户容器隔离

**场景**：在 Kubernetes 集群中实现多租户隔离

**实现方案**：

```yaml
# 使用 User Namespace 实现租户隔离
apiVersion: v1
kind: Pod
metadata:
  name: tenant-a-app
  namespace: tenant-a
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
  containers:
  - name: app
    image: nginx
    securityContext:
      # 移除不必要的 Capabilities
      capabilities:
        drop:
          - ALL
        add:
          - NET_BIND_SERVICE
```

**效果**：

- 租户隔离：每个租户有独立的 User Namespace
- 安全性：减少容器逃逸风险
- 资源隔离：通过 Namespace 实现资源隔离

### 案例 2：高性能网络应用

**场景**：部署高性能网络应用，需要独立的 Network Namespace

**实现方案**：

```bash
# 创建独立的 Network Namespace
ip netns add app-ns

# 配置网络接口
ip link add veth0 type veth peer name veth1
ip link set veth0 netns app-ns
ip netns exec app-ns ip addr add 10.0.0.1/24 dev veth0
ip netns exec app-ns ip link set veth0 up

# 在 Network Namespace 中运行应用
ip netns exec app-ns /usr/bin/myapp
```

**效果**：

- 网络隔离：应用有独立的网络栈
- 性能优化：减少网络干扰
- 安全性：网络流量隔离

### 案例 3：容器化 CI/CD 系统

**场景**：在容器中运行 CI/CD 任务，需要隔离的进程树

**实现方案**：

```yaml
# Kubernetes Job 配置
apiVersion: batch/v1
kind: Job
metadata:
  name: ci-job
spec:
  template:
    spec:
      # 使用独立的 PID Namespace
      shareProcessNamespace: false
      containers:
      - name: builder
        image: build-tool:latest
        securityContext:
          # 移除不必要的 Capabilities
          capabilities:
            drop:
              - ALL
```

**效果**：

- 进程隔离：每个 CI/CD 任务有独立的进程树
- 安全性：任务之间完全隔离
- 资源控制：通过 Cgroup 限制资源使用

---

**最后更新**：2025-11-15
**文档状态**：✅ 完整 | 📊 包含内核实现分析、2025 年最新实践、实际应用案例 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
