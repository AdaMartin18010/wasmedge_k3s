# 02. 进程与线程

## 📑 目录

- [02. 进程与线程](#02-进程与线程)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 进程概念](#11-进程概念)
    - [1.2 线程概念](#12-线程概念)
  - [2 进程描述符](#2-进程描述符)
    - [2.1 task\_struct 结构](#21-task_struct-结构)
    - [2.2 关键字段](#22-关键字段)
  - [3 进程创建与销毁](#3-进程创建与销毁)
    - [3.1 fork() 系统调用](#31-fork-系统调用)
    - [3.2 exec() 系统调用](#32-exec-系统调用)
    - [3.3 exit() 系统调用](#33-exit-系统调用)
  - [4 线程实现](#4-线程实现)
    - [4.1 clone() 系统调用](#41-clone-系统调用)
    - [4.2 pthread 实现](#42-pthread-实现)
  - [5 进程调度](#5-进程调度)
    - [5.1 CFS 调度器](#51-cfs-调度器)
    - [5.2 实时调度](#52-实时调度)
    - [5.3 调度策略](#53-调度策略)
  - [6 进程间通信](#6-进程间通信)
    - [6.1 管道（Pipe）](#61-管道pipe)
    - [6.2 信号（Signal）](#62-信号signal)
    - [6.3 共享内存](#63-共享内存)
    - [6.4 消息队列](#64-消息队列)
  - [7 与容器化的关系](#7-与容器化的关系)
    - [7.1 进程隔离](#71-进程隔离)
    - [7.2 进程创建](#72-进程创建)
    - [7.3 进程调度](#73-进程调度)
  - [8 相关文档](#8-相关文档)
    - [8.1 详细机制文档](#81-详细机制文档)
    - [8.2 架构分析](#82-架构分析)
  - [2025 年最新实践](#2025-年最新实践)
    - [进程与线程管理应用最佳实践（2025）](#进程与线程管理应用最佳实践2025)
  - [实际应用案例](#实际应用案例)
    - [案例 1：容器进程安全配置（2025）](#案例-1容器进程安全配置2025)

---

## 1 概述

**进程**是 Linux 系统中资源分配和调度的基本单位，**线程**是进程内的执行单元。

### 1.1 进程概念

- **进程**：程序的执行实例
- **进程 ID（PID）**：唯一标识进程
- **进程状态**：运行、就绪、阻塞等
- **进程地址空间**：独立的虚拟地址空间

### 1.2 线程概念

- **线程**：进程内的执行流
- **线程 ID（TID）**：线程标识
- **共享资源**：同一进程的线程共享地址空间、文件描述符等
- **独立资源**：每个线程有独立的栈、寄存器

---

## 2 进程描述符

### 2.1 task_struct 结构

内核使用 `task_struct` 结构描述进程：

```c
// include/linux/sched.h
struct task_struct {
    // 进程状态
    volatile long state;

    // 进程标识
    pid_t pid;
    pid_t tgid;  // 线程组 ID

    // 进程关系
    struct task_struct *parent;
    struct list_head children;
    struct list_head sibling;

    // 内存管理
    struct mm_struct *mm;
    struct mm_struct *active_mm;

    // 文件系统
    struct fs_struct *fs;
    struct files_struct *files;

    // 命名空间
    struct nsproxy *nsproxy;

    // 调度相关
    int prio;
    int static_prio;
    int normal_prio;
    unsigned int rt_priority;
    struct sched_entity se;

    // 信号处理
    struct signal_struct *signal;
    struct sighand_struct *sighand;

    // 线程信息
    struct thread_info *thread_info;

    // ...
};
```

### 2.2 关键字段

**进程标识**：

- `pid`：进程 ID
- `tgid`：线程组 ID（主线程的 PID）

**进程状态**：

```c
#define TASK_RUNNING        0
#define TASK_INTERRUPTIBLE  1
#define TASK_UNINTERRUPTIBLE 2
#define TASK_STOPPED        4
#define TASK_TRACED         8
#define EXIT_ZOMBIE         16
#define EXIT_DEAD           32
```

**内存管理**：

- `mm`：进程的内存描述符
- `active_mm`：活动内存描述符（内核线程使用）

---

## 3 进程创建与销毁

### 3.1 fork() 系统调用

`fork()` 创建子进程，复制父进程的地址空间：

```c
#include <unistd.h>

pid_t fork(void);
```

**内核实现**：

```c
// kernel/fork.c
long sys_fork(struct pt_regs *regs) {
    return do_fork(SIGCHLD, regs->sp, regs, 0, NULL, NULL);
}

long do_fork(unsigned long clone_flags, unsigned long stack_start,
             struct pt_regs *regs, unsigned long stack_size,
             int __user *parent_tidptr, int __user *child_tidptr) {
    struct task_struct *p;
    // 复制进程描述符
    p = copy_process(clone_flags, stack_start, regs, stack_size,
                     child_tidptr, NULL, trace);
    // 唤醒新进程
    wake_up_new_task(p);
    return p->pid;
}
```

**写时复制（CoW）**：

- 父进程和子进程共享物理页面
- 只有在写入时才复制页面
- 节省内存，提高性能

### 3.2 exec() 系统调用

`exec()` 系列函数加载新程序，替换当前进程的地址空间：

```c
#include <unistd.h>

int execve(const char *pathname, char *const argv[], char *const envp[]);
```

**内核实现**：

```c
// fs/exec.c
long sys_execve(const char __user *filename,
                const char __user *const __user *argv,
                const char __user *const __user *envp) {
    return do_execve(getname(filename), argv, envp);
}
```

### 3.3 exit() 系统调用

`exit()` 终止进程：

```c
#include <stdlib.h>

void exit(int status);
```

**进程终止流程**：

1. 设置进程状态为 `EXIT_ZOMBIE`
2. 释放大部分资源
3. 通知父进程（通过 SIGCHLD）
4. 父进程调用 `wait()` 回收子进程

---

## 4 线程实现

### 4.1 clone() 系统调用

Linux 使用 `clone()` 系统调用创建线程：

```c
#include <sched.h>

pid_t clone(int (*fn)(void *), void *stack, int flags, void *arg, ...);
```

**关键 flags**：

- `CLONE_VM`：共享地址空间（线程）
- `CLONE_FILES`：共享文件描述符
- `CLONE_FS`：共享文件系统信息
- `CLONE_SIGHAND`：共享信号处理

**线程创建示例**：

```c
#define STACK_SIZE (1024 * 1024)
static char child_stack[STACK_SIZE];

int thread_function(void *arg) {
    printf("Thread running\n");
    return 0;
}

int main() {
    pid_t tid = clone(thread_function,
                      child_stack + STACK_SIZE,
                      CLONE_VM | CLONE_FILES | CLONE_SIGHAND | SIGCHLD,
                      NULL);
    waitpid(tid, NULL, 0);
    return 0;
}
```

### 4.2 pthread 实现

**pthread** 是 POSIX 线程库，基于 `clone()` 实现：

```c
#include <pthread.h>

int pthread_create(pthread_t *thread, const pthread_attr_t *attr,
                   void *(*start_routine)(void *), void *arg);
```

**pthread 与 clone 的关系**：

- `pthread_create()` 内部调用 `clone()`
- 使用 `CLONE_VM | CLONE_FILES | CLONE_SIGHAND` 标志
- 每个线程有独立的栈

---

## 5 进程调度

### 5.1 CFS 调度器

**CFS（Completely Fair Scheduler）** 是 Linux 的默认调度器（2.6.23+）：

**核心思想**：

- 公平分配 CPU 时间
- 使用虚拟运行时间（vruntime）排序
- 红黑树维护就绪队列

**关键数据结构**：

```c
// kernel/sched/fair.c
struct sched_entity {
    struct load_weight load;
    struct rb_node run_node;
    unsigned int on_rq;
    u64 exec_start;
    u64 sum_exec_runtime;
    u64 vruntime;  // 虚拟运行时间
    // ...
};

struct cfs_rq {
    struct load_weight load;
    unsigned int nr_running;
    struct rb_root_cached tasks_timeline;  // 红黑树根
    struct sched_entity *curr;
    // ...
};
```

**调度算法**：

```c
// 选择下一个要运行的进程
static struct task_struct *pick_next_task_fair(struct rq *rq) {
    struct cfs_rq *cfs_rq = &rq->cfs;
    struct sched_entity *se;
    // 从红黑树中选择 vruntime 最小的进程
    se = __pick_first_entity(cfs_rq);
    return task_of(se);
}
```

### 5.2 实时调度

**实时调度策略**：

- **SCHED_FIFO**：先进先出，高优先级抢占低优先级
- **SCHED_RR**：轮询调度，相同优先级时间片轮转

**实时调度器**：

```c
// kernel/sched/rt.c
struct rt_rq {
    struct rt_prio_array active;  // 优先级数组
    // ...
};
```

### 5.3 调度策略

| 调度策略 | 说明 | 优先级范围 |
|---------|------|-----------|
| **SCHED_NORMAL** | 普通进程（CFS） | 100-139 |
| **SCHED_FIFO** | 实时 FIFO | 1-99 |
| **SCHED_RR** | 实时轮询 | 1-99 |
| **SCHED_IDLE** | 空闲调度 | - |

---

## 6 进程间通信

### 6.1 管道（Pipe）

**匿名管道**：

```c
#include <unistd.h>

int pipe(int pipefd[2]);
```

**内核实现**：

```c
// fs/pipe.c
long sys_pipe(int __user *fildes) {
    struct file *files[2];
    int fd[2];
    // 创建管道
    error = __do_pipe_flags(fd, files, flags);
    // 返回文件描述符
    if (copy_to_user(fildes, fd, sizeof(fd)))
        error = -EFAULT;
    return error;
}
```

### 6.2 信号（Signal）

**发送信号**：

```c
#include <signal.h>

int kill(pid_t pid, int sig);
```

**信号处理**：

```c
// 注册信号处理函数
void signal_handler(int sig) {
    // 处理信号
}

signal(SIGINT, signal_handler);
```

### 6.3 共享内存

**System V 共享内存**：

```c
#include <sys/shm.h>

int shmget(key_t key, size_t size, int shmflg);
void *shmat(int shmid, const void *shmaddr, int shmflg);
```

**POSIX 共享内存**：

```c
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>

int shm_fd = shm_open("/my_shm", O_CREAT | O_RDWR, 0666);
void *ptr = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
```

### 6.4 消息队列

**System V 消息队列**：

```c
#include <sys/msg.h>

int msgget(key_t key, int msgflg);
int msgsnd(int msqid, const void *msgp, size_t msgsz, int msgflg);
ssize_t msgrcv(int msqid, void *msgp, size_t msgsz, long msgtyp, int msgflg);
```

---

## 7 与容器化的关系

### 7.1 进程隔离

容器通过 PID Namespace 实现进程隔离：

- **独立的进程树**：每个容器有独立的 PID 空间
- **init 进程**：每个容器有自己的 init 进程（PID 1）
- **进程可见性**：容器内只能看到容器内的进程

### 7.2 进程创建

容器运行时通过 `clone()` 创建容器进程：

```c
// 创建容器进程
pid_t pid = clone(child_main, stack,
                  CLONE_NEWPID | CLONE_NEWNS | CLONE_NEWNET |
                  CLONE_NEWUTS | CLONE_NEWIPC | SIGCHLD,
                  NULL);
```

### 7.3 进程调度

容器进程与宿主机进程共享同一个调度器：

- **CFS 调度**：容器进程使用 CFS 调度器
- **CPU 限制**：通过 Cgroup 限制 CPU 使用
- **优先级**：容器进程的优先级受 Cgroup 影响

---

## 8 相关文档

### 8.1 详细机制文档

- **[Namespace 机制详解](08-namespace.md)** - PID Namespace 详解
- **[Cgroup 机制详解](09-cgroup.md)** - 进程资源限制
- **[系统调用机制](07-syscall.md)** - fork、exec、clone 等系统调用

### 8.2 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 隔离机制层次分析
- **[容器化架构视角](../../ARCHITECTURE/02-views/02-virtualization-containerization-sandboxing/)** - 容器化抽象层

---

---

## 2025 年最新实践

### 进程与线程管理应用最佳实践（2025）

**2025 年趋势**：进程管理在容器进程、云原生进程、边缘进程中的深度应用

**实践要点**：

- **容器进程**：使用 PID 命名空间进行进程隔离
- **进程性能优化**：使用进程调度优化进程性能
- **进程监控**：使用 eBPF 进行进程监控

**代码示例**：

```yaml
# 2025 年 Kubernetes 进程配置
apiVersion: v1
kind: Pod
metadata:
  name: process-pod
spec:
  containers:
  - name: app
    image: nginx:latest
    securityContext:
      runAsNonRoot: true
      runAsUser: 1000
```

## 实际应用案例

### 案例 1：容器进程安全配置（2025）

**场景**：使用 PID 命名空间和安全上下文进行进程隔离

**实现方案**：

```yaml
# 容器进程安全配置
apiVersion: v1
kind: Pod
metadata:
  name: secure-process-pod
spec:
  containers:
  - name: app
    image: nginx:latest
    securityContext:
      runAsNonRoot: true
      runAsUser: 1000
      allowPrivilegeEscalation: false
      capabilities:
        drop:
        - ALL
```

**效果**：

- 进程隔离：使用 PID 命名空间进行进程隔离
- 安全加固：使用安全上下文进行安全加固
- 进程监控：实时监控进程状态

---

**最后更新**：2025-11-15
**文档状态**：✅ 完整 | 📊 包含内核实现分析、2025 年最新实践、实际应用案例 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
