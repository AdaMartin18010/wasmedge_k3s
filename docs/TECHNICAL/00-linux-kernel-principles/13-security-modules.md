# 13. Linux 安全模块

## 📑 目录

- [13. Linux 安全模块](#13-linux-安全模块)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 LSM 的作用](#11-lsm-的作用)
    - [1.2 LSM 架构](#12-lsm-架构)
  - [2 LSM 框架](#2-lsm-框架)
    - [2.1 LSM 钩子](#21-lsm-钩子)
    - [2.2 LSM 注册](#22-lsm-注册)
    - [2.3 LSM 调用](#23-lsm-调用)
  - [3 SELinux](#3-selinux)
    - [3.1 SELinux 概念](#31-selinux-概念)
    - [3.2 安全上下文](#32-安全上下文)
    - [3.3 策略配置](#33-策略配置)
  - [4 AppArmor](#4-apparmor)
    - [4.1 AppArmor 概念](#41-apparmor-概念)
    - [4.2 配置文件](#42-配置文件)
    - [4.3 策略管理](#43-策略管理)
  - [5 其他 LSM 模块](#5-其他-lsm-模块)
    - [5.1 Smack](#51-smack)
    - [5.2 TOMOYO Linux](#52-tomoyo-linux)
    - [5.3 Yama](#53-yama)
  - [6 内核实现机制](#6-内核实现机制)
    - [6.1 LSM 数据结构](#61-lsm-数据结构)
    - [6.2 钩子调用](#62-钩子调用)
    - [6.3 权限检查](#63-权限检查)
  - [7 与容器化的关系](#7-与容器化的关系)
    - [7.1 容器安全上下文](#71-容器安全上下文)
    - [7.2 SELinux 在容器中的应用](#72-selinux-在容器中的应用)
    - [7.3 AppArmor 在容器中的应用](#73-apparmor-在容器中的应用)
  - [8 相关文档](#8-相关文档)
    - [8.1 详细机制文档](#81-详细机制文档)
    - [8.2 容器化基础机制](#82-容器化基础机制)
    - [8.3 架构分析](#83-架构分析)

---

## 1 概述

**LSM（Linux Security Module）** 是 Linux 内核提供的安全框架，允许安全模块在内核的关键位置插入安全检查，实现强制访问控制（MAC）。

### 1.1 LSM 的作用

- **强制访问控制**：实现基于策略的访问控制
- **安全增强**：提供细粒度的安全控制
- **模块化设计**：支持多种安全模块（SELinux、AppArmor 等）
- **灵活配置**：可以根据需求选择合适的安全模块

### 1.2 LSM 架构

**LSM 架构**：

```
用户空间
    │
    ├── 安全策略配置
    │
内核空间
    │
    ├── LSM 框架
    │   ├── LSM 钩子
    │   └── LSM 调用
    │
    ├── LSM 模块
    │   ├── SELinux
    │   ├── AppArmor
    │   └── 其他模块
    │
内核子系统
    ├── 文件系统
    ├── 网络
    └── 进程管理
```

---

## 2 LSM 框架

### 2.1 LSM 钩子

**LSM 钩子类型**：

- **文件系统钩子**：文件操作、inode 操作
- **网络钩子**：Socket 操作、网络数据包
- **进程钩子**：进程创建、信号发送
- **系统调用钩子**：系统调用拦截

**LSM 钩子示例**：

```c
// include/linux/security.h
// 文件打开钩子
int security_file_open(struct file *file);

// 文件读取钩子
int security_file_read(struct file *file, char __user *buf, size_t count, loff_t *pos);

// 进程创建钩子
int security_task_create(unsigned long clone_flags);

// Socket 创建钩子
int security_socket_create(int family, int type, int protocol, int kern);
```

### 2.2 LSM 注册

**LSM 模块注册**：

```c
// security/security.c
// 注册 LSM 模块
int __init security_init(void) {
    // 初始化 LSM 框架
    security_add_hooks(NULL, 0, "base");

    // 加载 LSM 模块
    if (IS_ENABLED(CONFIG_SECURITY_SELINUX))
        security_add_hooks(selinux_hooks, ARRAY_SIZE(selinux_hooks), "selinux");

    if (IS_ENABLED(CONFIG_SECURITY_APPARMOR))
        security_add_hooks(apparmor_hooks, ARRAY_SIZE(apparmor_hooks), "apparmor");

    return 0;
}
```

### 2.3 LSM 调用

**LSM 钩子调用**：

```c
// security/security.c
// 调用 LSM 钩子
int security_file_open(struct file *file) {
    int ret;

    // 调用所有注册的 LSM 模块
    ret = call_int_hook(file_open, 0, file);

    return ret;
}
```

---

## 3 SELinux

### 3.1 SELinux 概念

**SELinux（Security-Enhanced Linux）**：

- **强制访问控制**：基于安全上下文的访问控制
- **类型强制**：基于类型的访问控制（TE）
- **多级安全**：支持 MLS（Multi-Level Security）
- **策略驱动**：通过策略文件定义访问规则

**SELinux 模式**：

- **Enforcing**：强制模式，拒绝未授权的访问
- **Permissive**：宽松模式，记录但不拒绝
- **Disabled**：禁用模式

### 3.2 安全上下文

**安全上下文格式**：

```
user:role:type:level
```

**示例**：

```bash
# 查看文件安全上下文
ls -Z /etc/passwd
-rw-r--r--. root root system_u:object_r:passwd_file_t:s0 /etc/passwd

# 查看进程安全上下文
ps -Z
system_u:system_r:init_t:s0       1 ?        00:00:01 systemd
```

**安全上下文组件**：

- **User**：用户标识
- **Role**：角色标识
- **Type**：类型标识（最重要的组件）
- **Level**：安全级别（MLS）

### 3.3 策略配置

**SELinux 策略规则**：

```text
# 允许 httpd_t 类型读取 httpd_exec_t 类型的文件
allow httpd_t httpd_exec_t:file read;

# 允许 httpd_t 类型绑定 80 端口
allow httpd_t httpd_port_t:tcp_socket name_bind;
```

**SELinux 策略文件**：

```bash
# 查看当前策略
sestatus

# 查看策略模块
semodule -l

# 加载策略模块
semodule -i mypolicy.pp
```

---

## 4 AppArmor

### 4.1 AppArmor 概念

**AppArmor（Application Armor）**：

- **基于路径的访问控制**：基于文件路径而非 inode
- **配置文件驱动**：通过配置文件定义访问规则
- **学习模式**：可以学习应用行为生成策略
- **简单易用**：比 SELinux 更容易配置

**AppArmor 模式**：

- **Enforce**：强制模式
- **Complain**：学习模式
- **Unconfined**：未限制模式

### 4.2 配置文件

**AppArmor 配置文件示例**：

```text
# /etc/apparmor.d/usr.bin.nginx
/usr/sbin/nginx {
    # 包含抽象配置
    include <abstractions/base>
    include <abstractions/nameservice>

    # 允许读取配置文件
    /etc/nginx/** r,

    # 允许读取日志
    /var/log/nginx/** rw,

    # 允许绑定端口
    network,

    # 允许执行
    /usr/sbin/nginx ix,
}
```

### 4.3 策略管理

**AppArmor 管理命令**：

```bash
# 查看当前配置
aa-status

# 加载配置
apparmor_parser -r /etc/apparmor.d/usr.bin.nginx

# 卸载配置
apparmor_parser -R /etc/apparmor.d/usr.bin.nginx

# 进入学习模式
aa-complain /usr/sbin/nginx

# 退出学习模式
aa-enforce /usr/sbin/nginx
```

---

## 5 其他 LSM 模块

### 5.1 Smack

**Smack（Simplified Mandatory Access Control Kernel）**：

- **简单易用**：设计简单，易于理解
- **标签系统**：基于标签的访问控制
- **应用场景**：嵌入式系统、IoT 设备

### 5.2 TOMOYO Linux

**TOMOYO Linux**：

- **基于路径**：基于文件路径的访问控制
- **学习模式**：自动学习应用行为
- **简单配置**：配置文件简单易懂

### 5.3 Yama

**Yama（Yet Another Module for Access control）**：

- **进程限制**：限制进程调试和跟踪
- **Ptrace 控制**：控制 ptrace 的使用
- **轻量级**：轻量级安全模块

---

## 6 内核实现机制

### 6.1 LSM 数据结构

**LSM 钩子结构**：

```c
// include/linux/lsm_hooks.h
struct security_hook_list {
    struct hlist_node list;
    struct hlist_head *head;
    union security_list_options hook;
    const char *lsm;
};

struct security_hook_heads {
    struct hlist_head binder_set_context_mgr;
    struct hlist_head binder_transaction;
    struct hlist_head binder_transfer_binder;
    // ... 更多钩子
};
```

### 6.2 钩子调用

**钩子调用机制**：

```c
// security/security.c
// 调用 LSM 钩子
#define call_int_hook(FUNC, IRC, ...) ({ \
    int RC = IRC; \
    do { \
        struct security_hook_list *P; \
        \
        hlist_for_each_entry(P, &security_hook_heads.FUNC, list) { \
            RC = P->hook.FUNC(__VA_ARGS__); \
            if (RC != 0) \
                break; \
        } \
    } while (0); \
    RC; \
})
```

### 6.3 权限检查

**权限检查流程**：

```c
// 文件打开权限检查
int security_file_open(struct file *file) {
    int ret;

    // 调用 LSM 钩子
    ret = call_int_hook(file_open, 0, file);

    if (ret)
        return ret;

    // 继续文件打开流程
    return 0;
}
```

---

## 7 与容器化的关系

### 7.1 容器安全上下文

**容器安全上下文**：

- **SELinux**：为容器分配独立的安全上下文
- **AppArmor**：为容器应用配置访问规则
- **隔离增强**：与 Namespace、Capabilities 配合使用

### 7.2 SELinux 在容器中的应用

**Docker SELinux 配置**：

```bash
# 启用 SELinux
docker run --security-opt label=type:svirt_lxc_net_t ubuntu:20.04

# 查看容器 SELinux 上下文
docker inspect --format='{{.ProcessLabel}}' container_id
```

**Kubernetes SELinux 配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: selinux-pod
spec:
  containers:
  - name: test-container
    image: nginx:1.21
    securityContext:
      seLinuxOptions:
        level: "s0:c123,c456"
```

### 7.3 AppArmor 在容器中的应用

**Docker AppArmor 配置**：

```bash
# 使用 AppArmor 配置
docker run --security-opt apparmor=docker-default ubuntu:20.04

# 使用自定义 AppArmor 配置
docker run --security-opt apparmor=my-profile ubuntu:20.04
```

**Kubernetes AppArmor 配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: apparmor-pod
  annotations:
    container.apparmor.security.beta.kubernetes.io/test-container: localhost/my-profile
spec:
  containers:
  - name: test-container
    image: nginx:1.21
```

---

## 8 相关文档

### 8.1 详细机制文档

- **[Capabilities 机制](10-capabilities.md)** - 权限控制机制
- **[Seccomp 安全机制](11-seccomp.md)** - 系统调用过滤
- **[Namespace 机制详解](08-namespace.md)** - 进程隔离机制

### 8.2 容器化基础机制

- **[Capabilities 机制](10-capabilities.md)** - 权限控制
- **[Seccomp 安全机制](11-seccomp.md)** - 系统调用过滤
- **[Namespace 机制详解](08-namespace.md)** - 进程隔离

### 8.3 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 隔离机制层次分析
- **[容器化架构视角](../../ARCHITECTURE/02-views/02-virtualization-containerization-sandboxing/)** - 容器化抽象层

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核实现分析 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
