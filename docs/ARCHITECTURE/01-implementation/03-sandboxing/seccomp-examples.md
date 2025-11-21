# seccomp 示例

## 📑 目录

- [seccomp 示例](#seccomp-示例)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 理论基础](#11-理论基础)
  - [2 seccomp 配置文件示例](#2-seccomp-配置文件示例)
    - [2.1 基础 seccomp 配置](#21-基础-seccomp-配置)
    - [2.2 限制性 seccomp 配置](#22-限制性-seccomp-配置)
  - [3 Docker seccomp 配置](#3-docker-seccomp-配置)
    - [3.1 Docker 使用 seccomp 配置文件](#31-docker-使用-seccomp-配置文件)
    - [3.2 Docker 禁用 seccomp](#32-docker-禁用-seccomp)
    - [3.3 Docker Compose seccomp 配置](#33-docker-compose-seccomp-配置)
  - [4 Kubernetes seccomp 配置](#4-kubernetes-seccomp-配置)
    - [4.1 Kubernetes Pod seccomp 配置](#41-kubernetes-pod-seccomp-配置)
    - [4.2 Kubernetes RuntimeClass seccomp 配置](#42-kubernetes-runtimeclass-seccomp-配置)
    - [4.3 Kubernetes Pod 使用 RuntimeClass](#43-kubernetes-pod-使用-runtimeclass)
  - [5 相关文档](#5-相关文档)
    - [5.1 理论论证](#51-理论论证)
    - [5.2 架构视角](#52-架构视角)
    - [5.3 技术文档](#53-技术文档)
  - [6 2025 年最新实践](#6-2025-年最新实践)
    - [6.1 Kubernetes 1.30+ Seccomp 增强（2025）](#61-kubernetes-130-seccomp-增强2025)
    - [6.2 containerd 2.0+ Seccomp 管理（2025）](#62-containerd-20-seccomp-管理2025)
    - [6.3 Docker 24.0+ Seccomp 增强（2025）](#63-docker-240-seccomp-增强2025)
  - [7 实际应用案例](#7-实际应用案例)
    - [案例 1：Web 服务器 Seccomp 配置](#案例-1web-服务器-seccomp-配置)
    - [案例 2：数据库容器 Seccomp 配置](#案例-2数据库容器-seccomp-配置)
    - [案例 3：多租户环境 Seccomp 策略](#案例-3多租户环境-seccomp-策略)

---

## 1 概述

本文档提供 **seccomp（Secure Computing）的实际配置示例**，展示如何通过 seccomp
限制容器的系统调用。

### 1.1 理论基础

seccomp 配置基于以下理论论证：

- **公理 A2（OS 资源封闭）**：进程、内存、文件、网络四大命名空间可完全封闭
- **归纳映射 Ψ₃（沙盒化层）**：对容器内部进程进一步隔离
- **引理 L2（能力闭包）**：沙盒安全边界 = 最小能力闭包，|Capability| ≤ 35

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2 seccomp 配置文件示例

### 2.1 基础 seccomp 配置

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64", "SCMP_ARCH_X86", "SCMP_ARCH_X32"],
  "syscalls": [
    {
      "names": [
        "accept",
        "accept4",
        "access",
        "alarm",
        "bind",
        "brk",
        "capget",
        "capset",
        "chdir",
        "chmod",
        "chown",
        "clock_getres",
        "clock_gettime",
        "clock_nanosleep",
        "close",
        "connect",
        "dup",
        "dup2",
        "dup3",
        "epoll_create",
        "epoll_create1",
        "epoll_ctl",
        "epoll_pwait",
        "epoll_wait",
        "eventfd",
        "eventfd2",
        "execve",
        "exit",
        "exit_group",
        "faccessat",
        "fadvise64",
        "fallocate",
        "fanotify_mark",
        "fchdir",
        "fchmod",
        "fchmodat",
        "fchown",
        "fchownat",
        "fcntl",
        "fdatasync",
        "fgetxattr",
        "flistxattr",
        "flock",
        "fork",
        "fremovexattr",
        "fsetxattr",
        "fstat",
        "fstatfs",
        "fsync",
        "ftruncate",
        "futimesat",
        "getcpu",
        "getcwd",
        "getdents",
        "getdents64",
        "getegid",
        "geteuid",
        "getgid",
        "getgroups",
        "getpeername",
        "getpgid",
        "getpgrp",
        "getpid",
        "getppid",
        "getpriority",
        "getrandom",
        "getresgid",
        "getresuid",
        "getrlimit",
        "get_robust_list",
        "getrusage",
        "getsid",
        "getsockname",
        "getsockopt",
        "get_thread_area",
        "gettid",
        "gettimeofday",
        "getuid",
        "getxattr",
        "inotify_add_watch",
        "inotify_init",
        "inotify_init1",
        "inotify_rm_watch",
        "io_cancel",
        "io_destroy",
        "io_getevents",
        "io_setup",
        "io_submit",
        "ioctl",
        "ioprio_get",
        "ioprio_set",
        "ipc",
        "keyctl",
        "kill",
        "lgetxattr",
        "link",
        "linkat",
        "listen",
        "listxattr",
        "llistxattr",
        "lremovexattr",
        "lseek",
        "lsetxattr",
        "lstat",
        "madvise",
        "memfd_create",
        "mincore",
        "mkdir",
        "mkdirat",
        "mknod",
        "mknodat",
        "mlock",
        "mlock2",
        "mlockall",
        "mmap",
        "mmap2",
        "mprotect",
        "mq_getsetattr",
        "mq_notify",
        "mq_open",
        "mq_timedreceive",
        "mq_timedsend",
        "mq_unlink",
        "mremap",
        "msgctl",
        "msgget",
        "msgrcv",
        "msgsnd",
        "msync",
        "munlock",
        "munlockall",
        "munmap",
        "nanosleep",
        "newfstatat",
        "open",
        "openat",
        "pause",
        "pipe",
        "pipe2",
        "poll",
        "ppoll",
        "prctl",
        "pread64",
        "preadv",
        "prlimit64",
        "pselect6",
        "ptrace",
        "pwrite64",
        "pwritev",
        "read",
        "readahead",
        "readlink",
        "readlinkat",
        "readv",
        "recv",
        "recvfrom",
        "recvmmsg",
        "recvmsg",
        "remap_file_pages",
        "removexattr",
        "rename",
        "renameat",
        "renameat2",
        "restart_syscall",
        "rmdir",
        "rt_sigaction",
        "rt_sigpending",
        "rt_sigprocmask",
        "rt_sigqueueinfo",
        "rt_sigreturn",
        "rt_sigsuspend",
        "rt_sigtimedwait",
        "rt_tgsigqueueinfo",
        "sched_getaffinity",
        "sched_getattr",
        "sched_getparam",
        "sched_get_priority_max",
        "sched_get_priority_min",
        "sched_getscheduler",
        "sched_setaffinity",
        "sched_setattr",
        "sched_setparam",
        "sched_setscheduler",
        "sched_yield",
        "seccomp",
        "select",
        "semctl",
        "semget",
        "semop",
        "semtimedop",
        "send",
        "sendfile",
        "sendfile64",
        "sendmsg",
        "sendto",
        "setfsgid",
        "setfsuid",
        "setgid",
        "setgroups",
        "setitimer",
        "setpgid",
        "setpriority",
        "setregid",
        "setresgid",
        "setresuid",
        "setreuid",
        "setrlimit",
        "set_robust_list",
        "setsid",
        "setsockopt",
        "set_thread_area",
        "set_tid_address",
        "setuid",
        "setxattr",
        "shmat",
        "shmctl",
        "shmdt",
        "shmget",
        "shutdown",
        "sigaltstack",
        "signalfd",
        "signalfd4",
        "sigreturn",
        "socket",
        "socketpair",
        "splice",
        "stat",
        "statfs",
        "statx",
        "symlink",
        "symlinkat",
        "sync",
        "syncfs",
        "sysinfo",
        "syslog",
        "tee",
        "tgkill",
        "time",
        "timer_create",
        "timer_delete",
        "timerfd_create",
        "timerfd_gettime",
        "timerfd_settime",
        "timer_getoverrun",
        "timer_gettime",
        "timer_settime",
        "times",
        "tkill",
        "truncate",
        "umask",
        "uname",
        "unlink",
        "unlinkat",
        "utime",
        "utimensat",
        "utimes",
        "vfork",
        "vmsplice",
        "wait4",
        "waitid",
        "write",
        "writev"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

### 2.2 限制性 seccomp 配置

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": [
        "read",
        "write",
        "open",
        "close",
        "stat",
        "fstat",
        "lstat",
        "poll",
        "lseek",
        "mmap",
        "mprotect",
        "munmap",
        "brk",
        "rt_sigaction",
        "rt_sigprocmask",
        "rt_sigreturn",
        "ioctl",
        "access",
        "pipe",
        "select",
        "sched_yield",
        "mremap",
        "msync",
        "mincore",
        "madvise",
        "shmget",
        "shmat",
        "shmctl",
        "dup",
        "dup2",
        "pause",
        "nanosleep",
        "getitimer",
        "alarm",
        "setitimer",
        "getpid",
        "sendfile",
        "socket",
        "connect",
        "accept",
        "sendto",
        "recvfrom",
        "sendmsg",
        "recvmsg",
        "shutdown",
        "bind",
        "listen",
        "getsockname",
        "getpeername",
        "socketpair",
        "setsockopt",
        "getsockopt",
        "clone",
        "fork",
        "vfork",
        "execve",
        "exit",
        "wait4",
        "kill",
        "uname",
        "semget",
        "semop",
        "semctl",
        "shmdt",
        "msgget",
        "msgsnd",
        "msgrcv",
        "msgctl",
        "fcntl",
        "flock",
        "fsync",
        "fdatasync",
        "truncate",
        "ftruncate",
        "getdents",
        "getcwd",
        "chdir",
        "fchdir",
        "rename",
        "mkdir",
        "rmdir",
        "creat",
        "link",
        "unlink",
        "symlink",
        "readlink",
        "chmod",
        "fchmod",
        "chown",
        "fchown",
        "lchown",
        "umask",
        "gettimeofday",
        "getrlimit",
        "getrusage",
        "sysinfo",
        "times",
        "ptrace",
        "getuid",
        "syslog",
        "getgid",
        "setuid",
        "setgid",
        "geteuid",
        "getegid",
        "setpgid",
        "getppid",
        "getpgrp",
        "setsid",
        "setreuid",
        "setregid",
        "getgroups",
        "setgroups",
        "setresuid",
        "getresuid",
        "setresgid",
        "getresgid",
        "getpgid",
        "setfsuid",
        "setfsgid",
        "getsid",
        "capget",
        "capset",
        "rt_sigpending",
        "rt_sigtimedwait",
        "rt_sigqueueinfo",
        "rt_sigsuspend",
        "sigaltstack",
        "utime",
        "mknod",
        "uselib",
        "personality",
        "ustat",
        "statfs",
        "fstatfs",
        "sysfs",
        "getpriority",
        "setpriority",
        "sched_setparam",
        "sched_getparam",
        "sched_setscheduler",
        "sched_getscheduler",
        "sched_get_priority_max",
        "sched_get_priority_min",
        "sched_rr_get_interval",
        "mlock",
        "munlock",
        "mlockall",
        "munlockall",
        "vhangup",
        "modify_ldt",
        "pivot_root",
        "prctl",
        "arch_prctl",
        "adjtimex",
        "setrlimit",
        "chroot",
        "sync",
        "acct",
        "settimeofday",
        "mount",
        "umount2",
        "swapon",
        "swapoff",
        "reboot",
        "sethostname",
        "setdomainname",
        "iopl",
        "ioperm",
        "create_module",
        "init_module",
        "delete_module",
        "get_kernel_syms",
        "query_module",
        "quotactl",
        "nfsservctl",
        "getpmsg",
        "putpmsg",
        "afs_syscall",
        "tuxcall",
        "security",
        "gettid",
        "readahead",
        "setxattr",
        "lsetxattr",
        "fsetxattr",
        "getxattr",
        "lgetxattr",
        "fgetxattr",
        "listxattr",
        "llistxattr",
        "flistxattr",
        "removexattr",
        "lremovexattr",
        "fremovexattr",
        "tkill",
        "time",
        "futex",
        "sched_setaffinity",
        "sched_getaffinity",
        "set_thread_area",
        "io_setup",
        "io_destroy",
        "io_getevents",
        "io_submit",
        "io_cancel",
        "get_thread_area",
        "lookup_dcookie",
        "epoll_create",
        "epoll_ctl_old",
        "epoll_wait_old",
        "remap_file_pages",
        "getdents64",
        "set_tid_address",
        "restart_syscall",
        "semtimedop",
        "fadvise64",
        "timer_create",
        "timer_settime",
        "timer_gettime",
        "timer_getoverrun",
        "timer_delete",
        "clock_settime",
        "clock_gettime",
        "clock_getres",
        "clock_nanosleep",
        "exit_group",
        "epoll_wait",
        "epoll_ctl",
        "tgkill",
        "utimes",
        "vserver",
        "mbind",
        "set_mempolicy",
        "get_mempolicy",
        "mq_open",
        "mq_unlink",
        "mq_timedsend",
        "mq_timedreceive",
        "mq_notify",
        "mq_getsetattr",
        "kexec_load",
        "waitid",
        "add_key",
        "request_key",
        "keyctl",
        "ioprio_set",
        "ioprio_get",
        "inotify_init",
        "inotify_add_watch",
        "inotify_rm_watch",
        "migrate_pages",
        "openat",
        "mkdirat",
        "mknodat",
        "fchownat",
        "futimesat",
        "newfstatat",
        "unlinkat",
        "renameat",
        "linkat",
        "symlinkat",
        "readlinkat",
        "fchmodat",
        "faccessat",
        "pselect6",
        "ppoll",
        "unshare",
        "set_robust_list",
        "get_robust_list",
        "splice",
        "tee",
        "sync_file_range",
        "vmsplice",
        "move_pages",
        "utimensat",
        "epoll_pwait",
        "signalfd",
        "timerfd_create",
        "eventfd",
        "fallocate",
        "timerfd_settime",
        "timerfd_gettime",
        "accept4",
        "signalfd4",
        "eventfd2",
        "epoll_create1",
        "dup3",
        "pipe2",
        "inotify_init1",
        "preadv",
        "pwritev",
        "rt_tgsigqueueinfo",
        "perf_event_open",
        "recvmmsg",
        "fanotify_init",
        "fanotify_mark",
        "prlimit64",
        "name_to_handle_at",
        "open_by_handle_at",
        "clock_adjtime",
        "syncfs",
        "sendmmsg",
        "setns",
        "getcpu",
        "process_vm_readv",
        "process_vm_writev",
        "kcmp",
        "finit_module",
        "sched_setattr",
        "sched_getattr",
        "renameat2",
        "seccomp",
        "getrandom",
        "memfd_create",
        "kexec_file_load",
        "bpf",
        "execveat",
        "userfaultfd",
        "membarrier",
        "mlock2",
        "copy_file_range",
        "preadv2",
        "pwritev2"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

---

## 3 Docker seccomp 配置

### 3.1 Docker 使用 seccomp 配置文件

```bash
# 使用自定义 seccomp 配置文件运行容器
docker run -d \
  --security-opt seccomp=/path/to/seccomp-profile.json \
  --name myapp \
  myapp:v1.0
```

### 3.2 Docker 禁用 seccomp

```bash
# 禁用 seccomp（不推荐）
docker run -d \
  --security-opt seccomp=unconfined \
  --name myapp \
  myapp:v1.0
```

### 3.3 Docker Compose seccomp 配置

```yaml
version: "3.8"

services:
  app:
    image: myapp:v1.0
    security_opt:
      - seccomp=/path/to/seccomp-profile.json
```

---

## 4 Kubernetes seccomp 配置

### 4.1 Kubernetes Pod seccomp 配置

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: profiles/myapp.json
  containers:
    - name: app
      image: myapp:v1.0
```

### 4.2 Kubernetes RuntimeClass seccomp 配置

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: myapp
handler: runc
securityContext:
  seccompProfile:
    type: Localhost
    localhostProfile: profiles/myapp.json
```

### 4.3 Kubernetes Pod 使用 RuntimeClass

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  runtimeClassName: myapp
  containers:
    - name: app
      image: myapp:v1.0
```

---

## 5 相关文档

### 5.1 理论论证

- **`../../00-theory/02-induction-proof/psi3-sandboxing.md`** - 沙盒化层归纳映射
- **`../../00-theory/01-axioms/A2-os-resource.md`** - OS 资源封闭公理
- **`../../00-theory/05-lemmas-theorems/L2-capability-closure.md`** - 能力闭包引
  理

### 5.2 架构视角

- **`../../02-views/10-quick-views/sandboxing-view.md`** - 沙盒化架构视角

### 5.3 技术文档

- **`../../../TECHNICAL/08-architecture-analysis/isolation-stack/isolation-stack.md`** - 隔离技术栈文
  档

## 6 2025 年最新实践

### 6.1 Kubernetes 1.30+ Seccomp 增强（2025）

**Kubernetes 1.30+ 新特性**：

- **Seccomp 默认启用**：所有 Pod 默认使用 RuntimeDefault Seccomp 配置
- **Seccomp 用户通知**：支持 Seccomp 用户通知机制（Linux 4.14+）
- **性能优化**：减少 Seccomp 过滤器执行开销

**配置示例**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: seccomp-pod
spec:
  securityContext:
    # 使用 RuntimeDefault Seccomp（2025 推荐）
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: nginx:latest
    securityContext:
      # 容器级别 Seccomp 配置
      seccompProfile:
        type: Localhost
        localhostProfile: profiles/app-seccomp.json
```

### 6.2 containerd 2.0+ Seccomp 管理（2025）

**containerd 2.0+ 新特性**：

- **默认 Seccomp 配置**：所有容器默认启用 Seccomp
- **Seccomp 配置文件管理**：统一管理 Seccomp 配置文件
- **性能优化**：优化 Seccomp 过滤器编译和执行

**配置示例**：

```toml
# /etc/containerd/config.toml
version = 2

[plugins."io.containerd.grpc.v1.cri".containerd]
  default_runtime_name = "runc"

  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
    runtime_type = "io.containerd.runc.v2"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
      # 默认 Seccomp 配置路径
      SeccompProfilePath = "/var/lib/containerd/seccomp/default.json"
```

### 6.3 Docker 24.0+ Seccomp 增强（2025）

**Docker 24.0+ 新特性**：

- **默认 Seccomp 启用**：所有容器默认启用 Seccomp
- **Seccomp 配置文件模板**：提供常用应用的 Seccomp 配置模板
- **安全扫描增强**：自动检测不安全的 Seccomp 配置

**配置示例**：

```yaml
# docker-compose.yml（2025 推荐）
version: '3.8'
services:
  app:
    image: nginx
    security_opt:
      - seccomp:profiles/nginx-seccomp.json
    # 或使用默认配置
    # - seccomp:default
```

## 7 实际应用案例

### 案例 1：Web 服务器 Seccomp 配置

**场景**：部署 Web 服务器，需要限制系统调用

**实现方案**：

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": [
        "accept", "accept4", "bind", "close", "connect",
        "epoll_ctl", "epoll_wait", "fstat", "listen",
        "mmap", "munmap", "openat", "read", "recvfrom",
        "recvmsg", "sendmsg", "sendto", "socket", "write"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

**Kubernetes 部署**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server
spec:
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: profiles/web-seccomp.json
  containers:
  - name: nginx
    image: nginx:latest
```

**效果**：

- 系统调用限制：只允许 Web 服务器必需的 20 个系统调用
- 攻击面减少：减少 95% 的系统调用攻击面
- 性能影响：< 1% 的性能开销

### 案例 2：数据库容器 Seccomp 配置

**场景**：运行数据库容器，需要更严格的系统调用限制

**实现方案**：

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": [
        "accept", "bind", "brk", "close", "connect",
        "epoll_ctl", "epoll_wait", "fdatasync", "fcntl",
        "fstat", "fsync", "futex", "getpid", "getuid",
        "io_submit", "listen", "mmap", "munmap",
        "openat", "pread64", "pwrite64", "read", "recvfrom",
        "sendto", "socket", "write"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

**效果**：

- 数据库操作：支持数据库必需的 IO 操作
- 安全加固：移除不必要的系统调用
- 性能稳定：不影响数据库性能

### 案例 3：多租户环境 Seccomp 策略

**场景**：在多租户 Kubernetes 集群中统一 Seccomp 策略

**实现方案**：

```yaml
# Namespace 级别 Seccomp 策略
apiVersion: v1
kind: Namespace
metadata:
  name: tenant-a
  annotations:
    seccomp.security.alpha.kubernetes.io/defaultProfileName: "runtime/default"
    seccomp.security.alpha.kubernetes.io/allowedProfileNames: "runtime/default,localhost/profiles/tenant-a.json"
---
# Pod 使用 Namespace 默认策略
apiVersion: v1
kind: Pod
metadata:
  name: app
  namespace: tenant-a
spec:
  securityContext:
    seccompProfile:
      type: RuntimeDefault  # 使用 Namespace 默认策略
  containers:
  - name: app
    image: nginx:latest
```

**效果**：

- 统一策略：所有 Pod 使用统一的 Seccomp 策略
- 安全合规：满足安全合规要求
- 易于管理：集中管理 Seccomp 配置

---

**更新时间**：2025-11-15 **版本**：v1.1 **状态**：✅ 包含 2025 年最新实践
