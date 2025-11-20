# 11. Seccomp 安全机制

## 📑 目录

- [11. Seccomp 安全机制](#11-seccomp-安全机制)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 核心概念](#11-核心概念)
    - [1.2 与容器化的关系](#12-与容器化的关系)
  - [2 Seccomp 基础](#2-seccomp-基础)
    - [2.1 Seccomp 模式](#21-seccomp-模式)
    - [2.2 Seccomp 历史](#22-seccomp-历史)
    - [2.3 Seccomp 优势](#23-seccomp-优势)
  - [3 Seccomp 模式详解](#3-seccomp-模式详解)
    - [3.1 Strict 模式](#31-strict-模式)
    - [3.2 Filter 模式](#32-filter-模式)
    - [3.3 BPF 过滤器](#33-bpf-过滤器)
  - [4 Seccomp BPF 过滤器](#4-seccomp-bpf-过滤器)
    - [4.1 BPF 指令](#41-bpf-指令)
    - [4.2 过滤器编写](#42-过滤器编写)
    - [4.3 过滤器示例](#43-过滤器示例)
  - [5 内核实现机制](#5-内核实现机制)
    - [5.1 Seccomp 数据结构](#51-seccomp-数据结构)
    - [5.2 系统调用过滤](#52-系统调用过滤)
    - [5.3 过滤器执行](#53-过滤器执行)
  - [6 容器中的应用](#6-容器中的应用)
    - [6.1 Docker 中的 Seccomp](#61-docker-中的-seccomp)
    - [6.2 Kubernetes 中的 Seccomp](#62-kubernetes-中的-seccomp)
    - [6.3 runc 中的实现](#63-runc-中的实现)
  - [7 安全最佳实践](#7-安全最佳实践)
    - [7.1 最小系统调用集](#71-最小系统调用集)
    - [7.2 过滤器配置](#72-过滤器配置)
    - [7.3 性能考虑](#73-性能考虑)
  - [8 相关文档](#8-相关文档)
    - [8.1 详细机制文档](#81-详细机制文档)
    - [8.2 容器化基础机制](#82-容器化基础机制)
    - [8.3 架构分析](#83-架构分析)

---

## 1 概述

**Seccomp（Secure Computing Mode）** 是 Linux 内核提供的系统调用过滤机制，允许进程限制可以调用的系统调用，从而减少攻击面，增强安全性。

### 1.1 核心概念

- **系统调用过滤**：限制进程可以调用的系统调用
- **BPF 过滤器**：使用 BPF（Berkeley Packet Filter）编写过滤规则
- **最小权限**：只允许进程调用必要的系统调用
- **安全增强**：减少系统调用滥用和攻击面

### 1.2 与容器化的关系

Seccomp 在容器化中起到关键作用：

- **系统调用限制**：容器只能调用允许的系统调用
- **攻击面减少**：减少容器逃逸的风险
- **安全加固**：与 Capabilities、Namespace 配合使用
- **最小权限**：容器只获得运行所需的最小系统调用集

---

## 2 Seccomp 基础

### 2.1 Seccomp 模式

**Seccomp 模式**：

1. **SECCOMP_MODE_DISABLED**：禁用 Seccomp（默认）
2. **SECCOMP_MODE_STRICT**：严格模式，只允许 read、write、exit、sigreturn
3. **SECCOMP_MODE_FILTER**：过滤模式，使用 BPF 过滤器自定义规则

### 2.2 Seccomp 历史

**版本演进**：

- **Linux 2.6.12（2005）**：引入 Seccomp Strict 模式
- **Linux 3.5（2012）**：引入 Seccomp Filter 模式（BPF 过滤器）
- **Linux 4.14（2017）**：支持 Seccomp 用户通知

### 2.3 Seccomp 优势

**安全优势**：

- **攻击面减少**：限制可用的系统调用
- **权限控制**：细粒度的系统调用控制
- **性能开销小**：BPF 过滤器执行效率高
- **灵活性**：可以自定义过滤规则

---

## 3 Seccomp 模式详解

### 3.1 Strict 模式

**Strict 模式**：

- 只允许 4 个系统调用：`read`、`write`、`exit`、`sigreturn`
- 其他系统调用会导致进程被 SIGKILL 杀死
- 适用于沙盒环境

**Strict 模式使用**：

```c
#include <sys/prctl.h>
#include <linux/seccomp.h>

// 启用 Strict 模式
prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT);
```

**内核实现**：

```c
// kernel/seccomp.c
static long seccomp_set_mode_strict(void) {
    const unsigned long seccomp_mode = SECCOMP_MODE_STRICT;
    long ret = -EINVAL;

    spin_lock_irq(&current->sighand->siglock);

    if (!seccomp_may_assign_mode(seccomp_mode))
        goto out;

    current->seccomp.mode = seccomp_mode;
    current->seccomp.filter = NULL;
    set_tsk_thread_flag(current, TIF_SECCOMP);

out:
    spin_unlock_irq(&current->sighand->siglock);
    return ret;
}
```

### 3.2 Filter 模式

**Filter 模式**：

- 使用 BPF 过滤器自定义系统调用规则
- 可以允许、拒绝或记录特定的系统调用
- 支持参数检查

**Filter 模式使用**：

```c
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>

// 创建 BPF 过滤器
struct sock_fprog prog = {
    .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
    .filter = filter,
};

// 启用 Filter 模式
prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
```

### 3.3 BPF 过滤器

**BPF 过滤器结构**：

```c
// include/linux/filter.h
struct sock_filter {
    __u16 code;    // BPF 指令码
    __u8 jt;      // 跳转真
    __u8 jf;      // 跳转假
    __u32 k;      // 立即数
};

struct sock_fprog {
    unsigned short len;
    struct sock_filter *filter;
};
```

**BPF 指令类型**：

- **BPF_LD**：加载数据
- **BPF_JMP**：跳转
- **BPF_RET**：返回
- **BPF_ALU**：算术运算

---

## 4 Seccomp BPF 过滤器

### 4.1 BPF 指令

**常用 BPF 指令**：

```c
// 加载系统调用编号
BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr))

// 比较系统调用编号
BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_read, 0, 1)

// 允许系统调用
BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW)

// 拒绝系统调用
BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | (EPERM & SECCOMP_RET_DATA))

// 记录系统调用
BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_TRACE)
```

### 4.2 过滤器编写

**过滤器编写步骤**：

1. **加载系统调用编号**：从 `seccomp_data.nr` 加载
2. **比较系统调用**：与允许的系统调用编号比较
3. **返回结果**：允许、拒绝或记录

**过滤器示例**：

```c
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <sys/prctl.h>

// 只允许 read、write、exit 系统调用
struct sock_filter filter[] = {
    // 加载系统调用编号
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),

    // 检查是否为 read
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_read, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

    // 检查是否为 write
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_write, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

    // 检查是否为 exit
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_exit, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

    // 其他系统调用拒绝
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | (EPERM & SECCOMP_RET_DATA)),
};

struct sock_fprog prog = {
    .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
    .filter = filter,
};

// 启用 Seccomp Filter
prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
```

### 4.3 过滤器示例

**参数检查示例**：

```c
// 只允许 open 打开特定文件
struct sock_filter filter[] = {
    // 加载系统调用编号
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),

    // 检查是否为 open
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_open, 0, 5),

    // 加载第一个参数（文件路径指针）
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, args[0])),

    // 检查文件路径（简化示例）
    // 实际应用中需要更复杂的检查

    // 允许 open
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

    // 其他系统调用拒绝
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ERRNO | (EPERM & SECCOMP_RET_DATA)),
};
```

---

## 5 内核实现机制

### 5.1 Seccomp 数据结构

**Seccomp 数据结构**：

```c
// include/linux/seccomp.h
struct seccomp_filter {
    refcount_t refs;
    struct seccomp_filter *prev;
    struct bpf_prog *prog;
    struct notification *notif;
    struct mutex notify_lock;
    wait_queue_head_t wqh;
};

struct seccomp {
    int mode;
    struct seccomp_filter *filter;
};
```

**task_struct 中的 Seccomp**：

```c
// include/linux/sched.h
struct task_struct {
    // ...
    struct seccomp seccomp;
    // ...
};
```

### 5.2 系统调用过滤

**系统调用过滤流程**：

```c
// kernel/seccomp.c
// 在系统调用入口检查 Seccomp
static int __seccomp_filter(struct seccomp_data *sd) {
    struct seccomp_filter *match = NULL;
    int data = 0;
    u32 result;

    // 执行 BPF 过滤器
    result = seccomp_run_filters(sd, &match);
    data = result & SECCOMP_RET_DATA;
    result &= SECCOMP_RET_ACTION;

    switch (result) {
    case SECCOMP_RET_ALLOW:
        return 0;
    case SECCOMP_RET_ERRNO:
        return -data;
    case SECCOMP_RET_TRACE:
        // 通知 ptrace
        return 0;
    case SECCOMP_RET_KILL_PROCESS:
    case SECCOMP_RET_KILL_THREAD:
        // 杀死进程或线程
        seccomp_send_sigsys(sd->nr, data);
        return -1;
    default:
        return -1;
    }
}
```

### 5.3 过滤器执行

**BPF 过滤器执行**：

```c
// kernel/seccomp.c
static u32 seccomp_run_filters(const struct seccomp_data *sd,
                               struct seccomp_filter **match) {
    u32 ret = SECCOMP_RET_ALLOW;
    struct seccomp_filter *f;

    // 遍历过滤器链
    for (f = current->seccomp.filter; f; f = f->prev) {
        u32 cur_ret = BPF_PROG_RUN(f->prog, sd);

        if ((cur_ret & SECCOMP_RET_ACTION) < (ret & SECCOMP_RET_ACTION)) {
            ret = cur_ret;
            *match = f;
        }
    }

    return ret;
}
```

---

## 6 容器中的应用

### 6.1 Docker 中的 Seccomp

**Docker Seccomp 配置**：

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": ["read", "write", "open", "close"],
      "action": "SCMP_ACT_ALLOW"
    },
    {
      "names": ["clone"],
      "action": "SCMP_ACT_ALLOW",
      "args": [
        {
          "index": 0,
          "value": 2114060288,
          "op": "SCMP_CMP_MASKED_EQ"
        }
      ]
    }
  ]
}
```

**Docker 使用 Seccomp**：

```bash
# 使用默认 Seccomp 配置
docker run --security-opt seccomp=default.json ubuntu:20.04

# 禁用 Seccomp（不推荐）
docker run --security-opt seccomp=unconfined ubuntu:20.04

# 使用自定义 Seccomp 配置
docker run --security-opt seccomp=my-seccomp.json ubuntu:20.04
```

### 6.2 Kubernetes 中的 Seccomp

**Kubernetes Seccomp 配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: seccomp-pod
  annotations:
    seccomp.security.alpha.kubernetes.io/pod: "localhost/my-seccomp-profile"
spec:
  containers:
  - name: test-container
    image: nginx:1.21
    securityContext:
      seccompProfile:
        type: Localhost
        localhostProfile: my-seccomp-profile.json
```

**Kubernetes Seccomp 类型**：

- **RuntimeDefault**：使用容器运行时的默认配置
- **Localhost**：使用节点上的本地配置文件
- **Unconfined**：禁用 Seccomp（不推荐）

### 6.3 runc 中的实现

**runc Seccomp 实现**：

```go
// libcontainer/seccomp/seccomp_linux.go
func setupSeccomp(config *configs.Seccomp) error {
    if config == nil {
        return nil
    }

    // 编译 BPF 过滤器
    filter, err := compileFilter(config)
    if err != nil {
        return err
    }

    // 设置 Seccomp Filter
    if err := prctl.SetSeccomp(filter); err != nil {
        return err
    }

    return nil
}
```

---

## 7 安全最佳实践

### 7.1 最小系统调用集

**最小权限原则**：

- **只允许必要的系统调用**：分析应用实际使用的系统调用
- **定期审查**：定期检查系统调用使用情况
- **测试验证**：在测试环境中验证 Seccomp 配置

**系统调用分析工具**：

```bash
# 使用 strace 分析系统调用
strace -c -e trace=all ./myapp

# 使用 auditd 记录系统调用
auditctl -a always,exit -S all -F pid=1234
```

### 7.2 过滤器配置

**过滤器配置建议**：

- **白名单模式**：默认拒绝，只允许必要的系统调用
- **参数检查**：对关键系统调用进行参数检查
- **版本兼容**：考虑不同架构的系统调用编号差异
- **错误处理**：合理处理被拒绝的系统调用

### 7.3 性能考虑

**性能影响**：

- **BPF 过滤器开销**：每个系统调用都会执行过滤器
- **优化建议**：
  - 将常用的系统调用放在过滤器前面
  - 使用高效的 BPF 指令
  - 避免复杂的参数检查

**性能测试**：

```bash
# 测试 Seccomp 性能影响
perf stat -e syscalls:sys_enter_* ./myapp
```

---

## 8 相关文档

### 8.1 详细机制文档

- **[系统调用机制](07-syscall.md)** - 系统调用详解
- **[Capabilities 机制](10-capabilities.md)** - 权限控制机制
- **[Namespace 机制详解](08-namespace.md)** - 进程隔离机制

### 8.2 容器化基础机制

- **[Capabilities 机制](10-capabilities.md)** - 权限控制
- **[Namespace 机制详解](08-namespace.md)** - 进程隔离
- **[Cgroup 机制详解](09-cgroup.md)** - 资源限制

### 8.3 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 隔离机制层次分析
- **[容器化架构视角](../../ARCHITECTURE/02-views/02-virtualization-containerization-sandboxing/)** - 容器化抽象层

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核实现分析 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
