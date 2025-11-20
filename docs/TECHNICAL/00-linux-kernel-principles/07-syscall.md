# 07. 系统调用机制

## 📑 目录

- [07. 系统调用机制](#07-系统调用机制)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 系统调用的作用](#11-系统调用的作用)
    - [1.2 系统调用流程](#12-系统调用流程)
  - [2 系统调用接口](#2-系统调用接口)
    - [2.1 系统调用编号](#21-系统调用编号)
    - [2.2 系统调用表](#22-系统调用表)
    - [2.3 系统调用参数](#23-系统调用参数)
  - [3 系统调用实现](#3-系统调用实现)
    - [3.1 x86\_64 实现](#31-x86_64-实现)
    - [3.2 ARM64 实现](#32-arm64-实现)
    - [3.3 系统调用入口](#33-系统调用入口)
  - [4 常用系统调用分析](#4-常用系统调用分析)
    - [4.1 进程管理](#41-进程管理)
    - [4.2 文件操作](#42-文件操作)
    - [4.3 网络操作](#43-网络操作)
    - [4.4 内存管理](#44-内存管理)
  - [5 系统调用性能](#5-系统调用性能)
    - [5.1 系统调用开销](#51-系统调用开销)
    - [5.2 优化技术](#52-优化技术)
  - [6 与容器化的关系](#6-与容器化的关系)
    - [6.1 容器系统调用](#61-容器系统调用)
    - [6.2 系统调用过滤](#62-系统调用过滤)
  - [7 相关文档](#7-相关文档)
    - [7.1 详细机制文档](#71-详细机制文档)
    - [7.2 架构分析](#72-架构分析)

---

## 1 概述

**系统调用**是用户空间程序访问内核功能的唯一接口，提供了进程管理、文件操作、网络通信等核心功能。

### 1.1 系统调用的作用

- **内核访问**：用户空间访问内核功能的唯一方式
- **权限控制**：内核可以检查权限和限制
- **抽象接口**：提供统一的系统功能接口
- **安全隔离**：用户空间和内核空间的边界

### 1.2 系统调用流程

1. **用户空间调用**：调用 C 库函数（如 `open()`）
2. **进入内核**：通过软中断或 `syscall` 指令进入内核
3. **参数检查**：内核检查参数有效性
4. **权限检查**：检查进程权限
5. **执行操作**：执行相应的内核操作
6. **返回结果**：返回执行结果或错误码

---

## 2 系统调用接口

### 2.1 系统调用编号

每个系统调用有唯一的编号：

```c
// include/uapi/asm-generic/unistd.h
#define __NR_read           0
#define __NR_write          1
#define __NR_open           2
#define __NR_close          3
#define __NR_fork           57
#define __NR_execve         59
#define __NR_clone          56
#define __NR_mmap           9
#define __NR_munmap         11
// ... 更多系统调用
```

### 2.2 系统调用表

内核维护系统调用表，将系统调用编号映射到处理函数：

```c
// arch/x86/entry/syscall_64.c
asmlinkage const sys_call_ptr_t sys_call_table[] = {
    [0] = sys_read,
    [1] = sys_write,
    [2] = sys_open,
    [3] = sys_close,
    // ...
    [56] = sys_clone,
    [57] = sys_fork,
    [59] = sys_execve,
    // ...
};
```

### 2.3 系统调用参数

系统调用通过寄存器传递参数（x86_64）：

- **rax**：系统调用编号
- **rdi**：第一个参数
- **rsi**：第二个参数
- **rdx**：第三个参数
- **r10**：第四个参数
- **r8**：第五个参数
- **r9**：第六个参数

**示例**：

```c
// 用户空间调用
long syscall(long number, ...);

// open() 系统调用
int fd = open("/path/to/file", O_RDONLY);

// 汇编等价代码
mov rax, 2        // __NR_open
mov rdi, path     // 文件路径
mov rsi, O_RDONLY // 标志
syscall           // 进入内核
```

---

## 3 系统调用实现

### 3.1 x86_64 实现

**系统调用入口**：

```c
// arch/x86/entry/entry_64.S
ENTRY(entry_SYSCALL_64)
    // 保存用户空间寄存器
    pushq %rdi
    pushq %rsi
    // ...

    // 调用系统调用处理函数
    call do_syscall_64

    // 恢复寄存器
    popq %rsi
    popq %rdi
    // ...

    sysretq  // 返回用户空间
END(entry_SYSCALL_64)
```

**系统调用处理**：

```c
// arch/x86/entry/common.c
__visible noinstr void do_syscall_64(struct pt_regs *regs, int nr) {
    // 检查系统调用编号
    if (likely(nr < NR_syscalls)) {
        // 从系统调用表获取处理函数
        regs->ax = sys_call_table[nr](regs);
    } else {
        regs->ax = -ENOSYS;
    }
}
```

### 3.2 ARM64 实现

**系统调用入口**：

```assembly
// arch/arm64/kernel/entry.S
el0_svc:
    // 保存用户空间寄存器
    stp x0, x1, [sp, #-16]!
    // ...

    // 调用系统调用处理函数
    bl el0_svc_handler

    // 恢复寄存器
    ldp x0, x1, [sp], #16
    // ...

    eret  // 返回用户空间
```

### 3.3 系统调用入口

**用户空间到内核空间的切换**：

1. **保存上下文**：保存用户空间寄存器
2. **切换栈**：切换到内核栈
3. **切换页表**：切换到内核页表
4. **执行系统调用**：调用相应的处理函数
5. **恢复上下文**：恢复用户空间寄存器
6. **返回用户空间**：使用 `sysret` 或 `eret`

---

## 4 常用系统调用分析

### 4.1 进程管理

**fork()**：

```c
// kernel/fork.c
long sys_fork(struct pt_regs *regs) {
    return do_fork(SIGCHLD, regs->sp, regs, 0, NULL, NULL);
}
```

**execve()**：

```c
// fs/exec.c
long sys_execve(const char __user *filename,
                const char __user *const __user *argv,
                const char __user *const __user *envp) {
    return do_execve(getname(filename), argv, envp);
}
```

**clone()**：

```c
// kernel/fork.c
long sys_clone(struct pt_regs *regs) {
    unsigned long clone_flags;
    unsigned long newsp;
    // 从寄存器获取参数
    clone_flags = regs->di;
    newsp = regs->si;
    return do_fork(clone_flags, newsp, regs, 0, NULL, NULL);
}
```

### 4.2 文件操作

**open()**：

```c
// fs/open.c
long sys_open(const char __user *filename, int flags, umode_t mode) {
    return do_sys_open(AT_FDCWD, filename, flags, mode);
}
```

**read()**：

```c
// fs/read_write.c
ssize_t sys_read(unsigned int fd, char __user *buf, size_t count) {
    struct fd f = fdget_pos(fd);
    ssize_t ret = vfs_read(f.file, buf, count, &pos);
    fdput_pos(f);
    return ret;
}
```

**write()**：

```c
// fs/read_write.c
ssize_t sys_write(unsigned int fd, const char __user *buf, size_t count) {
    struct fd f = fdget_pos(fd);
    ssize_t ret = vfs_write(f.file, buf, count, &pos);
    fdput_pos(f);
    return ret;
}
```

### 4.3 网络操作

**socket()**：

```c
// net/socket.c
long sys_socket(int family, int type, int protocol) {
    return __sys_socket(family, type, protocol);
}
```

**bind()**：

```c
// net/socket.c
long sys_bind(int fd, struct sockaddr __user *umyaddr, int addrlen) {
    return __sys_bind(fd, umyaddr, addrlen);
}
```

**connect()**：

```c
// net/socket.c
long sys_connect(int fd, struct sockaddr __user *uservaddr, int addrlen) {
    return __sys_connect(fd, uservaddr, addrlen);
}
```

### 4.4 内存管理

**mmap()**：

```c
// mm/mmap.c
long sys_mmap(unsigned long addr, unsigned long len,
              unsigned long prot, unsigned long flags,
              unsigned long fd, unsigned long off) {
    return ksys_mmap_pgoff(addr, len, prot, flags, fd, off >> PAGE_SHIFT);
}
```

**munmap()**：

```c
// mm/mmap.c
long sys_munmap(unsigned long addr, size_t len) {
    return __vm_munmap(addr, len, true);
}
```

---

## 5 系统调用性能

### 5.1 系统调用开销

**系统调用开销组成**：

- **上下文切换**：用户态 ↔ 内核态切换（~100-200 纳秒）
- **参数检查**：参数有效性检查
- **权限检查**：Capabilities 检查
- **实际操作**：执行具体操作的时间

**典型系统调用开销**：

- `getpid()`：~50 纳秒（简单系统调用）
- `read()`：~1-10 微秒（取决于数据量）
- `fork()`：~10-100 微秒（取决于地址空间大小）

### 5.2 优化技术

**快速系统调用**：

- **vsyscall**：已废弃
- **vDSO（Virtual Dynamic Shared Object）**：将部分系统调用映射到用户空间
- **io_uring**：异步 IO 接口，减少系统调用次数

**vDSO 示例**：

```c
// 某些系统调用通过 vDSO 在用户空间执行
// 如 gettimeofday()、clock_gettime() 等
```

---

## 6 与容器化的关系

### 6.1 容器系统调用

容器进程的系统调用流程与普通进程相同：

1. **用户空间调用**：容器内进程调用系统调用
2. **进入内核**：通过 `syscall` 进入内核
3. **Namespace 检查**：内核检查进程的 Namespace
4. **权限检查**：检查 Capabilities
5. **执行操作**：在相应的 Namespace 中执行
6. **返回结果**：返回执行结果

### 6.2 系统调用过滤

**Seccomp** 可以过滤系统调用：

```c
// 只允许 read、write、exit 系统调用
struct sock_fprog prog = {
    .len = 3,
    .filter = {
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_read, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
        // ... 更多规则
    }
};
seccomp(SECCOMP_SET_MODE_FILTER, 0, &prog);
```

---

## 7 相关文档

### 7.1 详细机制文档

- **[进程与线程](02-process-thread.md)** - fork、clone 等系统调用详解
- **[Namespace 机制详解](08-namespace.md)** - clone、unshare、setns 系统调用
- **[Seccomp 安全机制](11-seccomp.md)** - 系统调用过滤

### 7.2 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 隔离机制层次分析
- **[容器化架构视角](../../ARCHITECTURE/02-views/02-virtualization-containerization-sandboxing/)** - 容器化抽象层

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核实现分析 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
