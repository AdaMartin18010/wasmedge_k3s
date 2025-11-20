# 09. Cgroup 机制详解

## 📑 目录

- [09. Cgroup 机制详解](#09-cgroup-机制详解)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 核心概念](#11-核心概念)
    - [1.2 与容器化的关系](#12-与容器化的关系)
  - [2 Cgroup 基础](#2-cgroup-基础)
    - [2.1 Cgroup v1 vs v2](#21-cgroup-v1-vs-v2)
    - [2.2 Cgroup 层次结构](#22-cgroup-层次结构)
    - [2.3 Cgroup 控制器](#23-cgroup-控制器)
  - [3 Cgroup v2 详解](#3-cgroup-v2-详解)
    - [3.1 统一层次结构](#31-统一层次结构)
    - [3.2 控制器启用](#32-控制器启用)
    - [3.3 文件系统接口](#33-文件系统接口)
  - [4 主要控制器详解](#4-主要控制器详解)
    - [4.1 CPU 控制器](#41-cpu-控制器)
    - [4.2 Memory 控制器](#42-memory-控制器)
    - [4.3 IO 控制器](#43-io-控制器)
    - [4.4 PIDs 控制器](#44-pids-控制器)
  - [5 内核实现机制](#5-内核实现机制)
    - [5.1 Cgroup 数据结构](#51-cgroup-数据结构)
    - [5.2 控制器实现](#52-控制器实现)
    - [5.3 资源限制流程](#53-资源限制流程)
  - [6 容器中的应用](#6-容器中的应用)
    - [6.1 Docker 中的 Cgroup 使用](#61-docker-中的-cgroup-使用)
    - [6.2 Kubernetes 中的 Cgroup 使用](#62-kubernetes-中的-cgroup-使用)
  - [7 性能与限制](#7-性能与限制)
    - [7.1 性能特点](#71-性能特点)
    - [7.2 限制与注意事项](#72-限制与注意事项)
  - [8 相关文档](#8-相关文档)
    - [8.1 实现细节](#81-实现细节)
    - [8.2 架构分析](#82-架构分析)
    - [8.3 理论分析](#83-理论分析)

---

## 1 概述

**Cgroup**（Control Group）是 Linux 内核提供的资源限制和优先级控制机制，用于限制、记录和隔离进程组的资源使用（CPU、内存、IO 等）。

### 1.1 核心概念

- **资源限制**：限制进程组可以使用的 CPU、内存、IO 等资源
- **优先级控制**：控制进程组的资源分配优先级
- **资源统计**：记录进程组的资源使用情况
- **层次结构**：支持树形层次结构，子 Cgroup 继承父 Cgroup 的限制

### 1.2 与容器化的关系

Cgroup 是容器化的核心机制之一：

- **资源隔离**：每个容器有独立的 Cgroup，限制其资源使用
- **资源配额**：通过 Cgroup 设置容器的 CPU、内存配额
- **资源监控**：通过 Cgroup 统计容器的资源使用情况
- **多租户隔离**：通过 Cgroup 实现多租户环境下的资源隔离

---

## 2 Cgroup 基础

### 2.1 Cgroup v1 vs v2

| 特性 | Cgroup v1 | Cgroup v2 |
|------|-----------|-----------|
| **层次结构** | 每个控制器独立层次 | 统一层次结构 |
| **控制器** | 可挂载多个控制器 | 统一挂载点 |
| **接口** | `/sys/fs/cgroup/<controller>/` | `/sys/fs/cgroup/` |
| **兼容性** | 传统实现 | Linux 4.15+ |
| **推荐使用** | 旧系统 | 新系统（推荐） |

**Cgroup v1 问题**：

- 每个控制器有独立的层次结构，导致管理复杂
- 控制器可以挂载到不同位置，造成混乱
- 某些功能（如内存和 IO 控制）存在冲突

**Cgroup v2 优势**：

- 统一层次结构，简化管理
- 所有控制器在同一挂载点
- 更好的资源控制和统计

### 2.2 Cgroup 层次结构

Cgroup 采用树形层次结构：

```text
/sys/fs/cgroup/
├── cgroup.controllers      # 可用的控制器列表
├── cgroup.subtree_control  # 启用的控制器
├── cgroup.procs            # 进程列表
├── cpu.max                 # CPU 限制
├── memory.max              # 内存限制
├── io.max                  # IO 限制
├── system.slice/           # systemd 服务
├── user.slice/             # 用户会话
└── kubepods/               # Kubernetes Pods
    ├── pod-xxx/
    │   ├── container-1/
    │   └── container-2/
    └── pod-yyy/
```

### 2.3 Cgroup 控制器

Cgroup 控制器（Controller）负责特定资源的限制和统计：

| 控制器 | 功能 | Cgroup v1 | Cgroup v2 |
|--------|------|-----------|-----------|
| **cpu** | CPU 使用限制 | ✅ | ✅ |
| **memory** | 内存使用限制 | ✅ | ✅ |
| **io** | IO 使用限制 | ✅ | ✅ |
| **pids** | 进程数限制 | ✅ | ✅ |
| **cpuset** | CPU 和内存节点绑定 | ✅ | ✅ |
| **devices** | 设备访问控制 | ✅ | ❌（已移除） |
| **freezer** | 进程冻结 | ✅ | ✅ |
| **net_cls** | 网络流量分类 | ✅ | ❌（已移除） |
| **net_prio** | 网络优先级 | ✅ | ❌（已移除） |

---

## 3 Cgroup v2 详解

### 3.1 统一层次结构

Cgroup v2 使用统一的层次结构，所有控制器在同一挂载点：

```bash
# 挂载 Cgroup v2
mount -t cgroup2 none /sys/fs/cgroup

# 查看可用的控制器
cat /sys/fs/cgroup/cgroup.controllers
# 输出：cpuset cpu io memory pids

# 查看启用的控制器
cat /sys/fs/cgroup/cgroup.subtree_control
```

### 3.2 控制器启用

在 Cgroup v2 中，需要在父 Cgroup 中启用控制器，子 Cgroup 才能使用：

```bash
# 在根 Cgroup 启用 CPU 和 Memory 控制器
echo "+cpu +memory" > /sys/fs/cgroup/cgroup.subtree_control

# 创建子 Cgroup
mkdir /sys/fs/cgroup/mycontainer

# 子 Cgroup 自动继承启用的控制器
cat /sys/fs/cgroup/mycontainer/cgroup.controllers
# 输出：cpu memory
```

### 3.3 文件系统接口

Cgroup v2 通过文件系统接口进行管理：

**核心文件**：

- `cgroup.controllers`：可用的控制器列表
- `cgroup.subtree_control`：启用的控制器
- `cgroup.procs`：进程列表（写入 PID 将进程加入 Cgroup）
- `cgroup.threads`：线程列表
- `cgroup.events`：Cgroup 事件（如进程 OOM）

**控制器文件**：

- `cpu.max`：CPU 使用限制
- `memory.max`：内存使用限制
- `io.max`：IO 使用限制
- `pids.max`：进程数限制

---

## 4 主要控制器详解

### 4.1 CPU 控制器

**功能**：限制和控制 CPU 资源使用。

**Cgroup v2 接口**：

```bash
# 设置 CPU 使用限制（格式：quota period）
# quota: 每 period 时间内的 CPU 时间（微秒）
# period: 时间周期（微秒）
echo "50000 100000" > /sys/fs/cgroup/mycontainer/cpu.max
# 表示：每 100ms 内可以使用 50ms CPU 时间（50% CPU）

# 设置 CPU 权重（1-10000，默认 100）
echo 500 > /sys/fs/cgroup/mycontainer/cpu.weight
# 权重越高，分配的 CPU 时间越多

# 查看 CPU 使用统计
cat /sys/fs/cgroup/mycontainer/cpu.stat
```

**内核实现**：

```c
// kernel/sched/core.c
struct cgroup_subsys_state *css;

// CPU 控制器结构
struct cgroup_subsys cpu_cgrp_subsys = {
    .css_alloc = cpu_cgroup_css_alloc,
    .css_online = cpu_cgroup_css_online,
    .css_offline = cpu_cgroup_css_offline,
    .css_free = cpu_cgroup_css_free,
    .attach = cpu_cgroup_attach,
    .can_attach = cpu_cgroup_can_attach,
    .cancel_attach = cpu_cgroup_cancel_attach,
    .legacy_cftypes = cpu_files,
    .early_init = true,
};
```

### 4.2 Memory 控制器

**功能**：限制和控制内存资源使用。

**Cgroup v2 接口**：

```bash
# 设置内存限制（字节）
echo "268435456" > /sys/fs/cgroup/mycontainer/memory.max
# 限制为 256MB

# 设置内存软限制（可超限，但会被回收）
echo "134217728" > /sys/fs/cgroup/mycontainer/memory.high
# 软限制为 128MB

# 设置交换空间限制
echo "134217728" > /sys/fs/cgroup/mycontainer/memory.swap.max
# 交换空间限制为 128MB

# 查看内存使用统计
cat /sys/fs/cgroup/mycontainer/memory.current
cat /sys/fs/cgroup/mycontainer/memory.stat
```

**内存回收机制**：

当内存使用超过 `memory.high` 时，内核会尝试回收内存：

- 页面回收（Page Reclaim）
- 交换到交换空间（Swap）
- OOM Killer（如果超过 `memory.max`）

**内核实现**：

```c
// mm/memcontrol.c
struct mem_cgroup {
    struct cgroup_subsys_state css;
    struct page_counter memory;
    struct page_counter swap;
    struct page_counter memsw;
    // ...
};

// 内存限制检查
bool mem_cgroup_charge(struct page *page, struct mm_struct *mm, gfp_t gfp_mask) {
    struct mem_cgroup *memcg;
    // 检查内存限制
    if (page_counter_try_charge(&memcg->memory, 1, &counter)) {
        return true;
    }
    // 超过限制，触发回收或 OOM
    return false;
}
```

### 4.3 IO 控制器

**功能**：限制和控制 IO 资源使用。

**Cgroup v2 接口**：

```bash
# 设置 IO 权重（1-10000，默认 100）
echo 500 > /sys/fs/cgroup/mycontainer/io.weight
# 权重越高，IO 优先级越高

# 设置 IO 限制（格式：major:minor max）
# 限制设备 8:0（通常是 /dev/sda）的读取速度
echo "8:0 rbps=10485760" > /sys/fs/cgroup/mycontainer/io.max
# 限制读取速度为 10MB/s

# 限制写入速度
echo "8:0 wbps=10485760" > /sys/fs/cgroup/mycontainer/io.max

# 限制 IOPS
echo "8:0 riops=1000 wiops=1000" > /sys/fs/cgroup/mycontainer/io.max

# 查看 IO 统计
cat /sys/fs/cgroup/mycontainer/io.stat
```

**内核实现**：

```c
// block/blk-cgroup.c
struct blkcg {
    struct cgroup_subsys_state css;
    // ...
};

// IO 限制检查
void blk_mq_make_request(struct request_queue *q, struct bio *bio) {
    struct blkcg_gq *blkg;
    // 检查 IO 限制
    if (blkcg_bio_issue_check(blkg, bio)) {
        // 超过限制，限流
        blk_throtl_bio(blkg, bio);
    }
}
```

### 4.4 PIDs 控制器

**功能**：限制进程数。

**Cgroup v2 接口**：

```bash
# 设置最大进程数
echo 100 > /sys/fs/cgroup/mycontainer/pids.max

# 查看当前进程数
cat /sys/fs/cgroup/mycontainer/pids.current

# 查看进程数统计
cat /sys/fs/cgroup/mycontainer/pids.events
```

**内核实现**：

```c
// kernel/cgroup/pids.c
struct pids_cgroup {
    struct cgroup_subsys_state css;
    atomic64_t counter;
    atomic64_t limit;
    // ...
};

// 进程数限制检查
static int pids_can_attach(struct cgroup_taskset *tset) {
    struct pids_cgroup *pids = css_pids(tset->dst_css);
    // 检查进程数限制
    if (atomic64_read(&pids->counter) >= atomic64_read(&pids->limit)) {
        return -EAGAIN;
    }
    return 0;
}
```

---

## 5 内核实现机制

### 5.1 Cgroup 数据结构

内核中的 Cgroup 数据结构：

```c
// include/linux/cgroup-defs.h
struct cgroup {
    struct cgroup_subsys_state *self;
    struct cgroup_subsys_state __rcu *subsys[CGROUP_SUBSYS_COUNT];
    struct cgroup *parent;
    struct cgroup_subsys_state *root;
    struct list_head children;
    struct list_head sibling;
    // ...
};

// Cgroup 子系统状态
struct cgroup_subsys_state {
    struct cgroup *cgroup;
    struct cgroup_subsys *ss;
    struct percpu_ref refcnt;
    // ...
};
```

### 5.2 控制器实现

每个控制器实现 `cgroup_subsys` 接口：

```c
// include/linux/cgroup-defs.h
struct cgroup_subsys {
    const char *name;
    int (*css_alloc)(struct cgroup_subsys_state *css);
    void (*css_online)(struct cgroup_subsys_state *css);
    void (*css_offline)(struct cgroup_subsys_state *css);
    void (*css_free)(struct cgroup_subsys_state *css);
    int (*can_attach)(struct cgroup_taskset *tset);
    void (*attach)(struct cgroup_taskset *tset);
    void (*cancel_attach)(struct cgroup_taskset *tset);
    // ...
};
```

### 5.3 资源限制流程

资源限制的执行流程：

1. **进程加入 Cgroup**：写入 PID 到 `cgroup.procs`
2. **控制器检查**：控制器检查资源限制
3. **资源分配**：如果未超限，分配资源
4. **超限处理**：如果超限，触发限制机制（限流、回收、OOM）

**示例：内存限制流程**：

```c
// 进程尝试分配内存
page = alloc_pages(gfp_mask, order);

// 检查 Cgroup 内存限制
memcg = get_mem_cgroup_from_mm(mm);
if (page_counter_try_charge(&memcg->memory, 1, &counter)) {
    // 未超限，分配成功
    return page;
} else {
    // 超限，触发回收
    mem_cgroup_oom(memcg, gfp_mask, order);
    // 或返回 NULL
    return NULL;
}
```

---

## 6 容器中的应用

### 6.1 Docker 中的 Cgroup 使用

Docker 为每个容器创建独立的 Cgroup：

```bash
# Docker 容器 Cgroup 路径（Cgroup v2）
/sys/fs/cgroup/docker/<container-id>/

# 查看容器的 CPU 限制
cat /sys/fs/cgroup/docker/<container-id>/cpu.max

# 查看容器的内存限制
cat /sys/fs/cgroup/docker/<container-id>/memory.max

# 查看容器的资源使用
docker stats <container-id>
```

**Docker 配置示例**：

```yaml
# docker-compose.yml
services:
  app:
    image: nginx
    deploy:
      resources:
        limits:
          cpus: '0.5'      # CPU 限制：50%
          memory: 256M      # 内存限制：256MB
        reservations:
          cpus: '0.25'     # CPU 预留：25%
          memory: 128M     # 内存预留：128MB
```

### 6.2 Kubernetes 中的 Cgroup 使用

Kubernetes 通过 Cgroup 实现 Pod 和容器的资源限制：

```yaml
# Pod 资源限制
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: app
    image: nginx
    resources:
      requests:
        cpu: "250m"        # CPU 请求：0.25 核
        memory: "128Mi"    # 内存请求：128MB
      limits:
        cpu: "500m"        # CPU 限制：0.5 核
        memory: "256Mi"    # 内存限制：256MB
```

**Kubernetes Cgroup 路径**：

```bash
# Pod Cgroup 路径（Cgroup v2）
/sys/fs/cgroup/kubepods/
  ├── pod-<pod-uid>/
  │   ├── cpu.max
  │   ├── memory.max
  │   └── <container-id>/
  │       ├── cpu.max
  │       └── memory.max
```

**Kubernetes 资源限制实现**：

1. **QoS 类别**：
   - **Guaranteed**：requests == limits
   - **Burstable**：requests < limits
   - **BestEffort**：无 requests 和 limits

2. **Cgroup 配置**：
   - Pod 级别：设置 Pod 的总体资源限制
   - 容器级别：设置单个容器的资源限制

---

## 7 性能与限制

### 7.1 性能特点

- **低开销**：Cgroup 检查开销极小（纳秒级）
- **实时限制**：资源限制实时生效
- **精确统计**：提供精确的资源使用统计

### 7.2 限制与注意事项

**限制**：

- **内核共享**：所有容器共享同一个内核的 Cgroup 机制
- **控制器依赖**：某些控制器可能有依赖关系
- **层次限制**：子 Cgroup 的资源不能超过父 Cgroup

**注意事项**：

- **内存 OOM**：超过 `memory.max` 会触发 OOM Killer
- **CPU 限流**：超过 CPU 限制会导致进程被限流
- **IO 限流**：超过 IO 限制会导致 IO 操作被限流
- **进程数限制**：超过 `pids.max` 会导致无法创建新进程

---

## 8 相关文档

### 8.1 实现细节

- **[Cgroup 配置示例](../../ARCHITECTURE/01-implementation/02-containerization/cgroup-config.md)** - 实际配置示例
- **[容器化实现](../../ARCHITECTURE/01-implementation/02-containerization/)** - 容器化技术实现

### 8.2 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 隔离机制层次分析
- **[容器化架构视角](../../ARCHITECTURE/02-views/02-virtualization-containerization-sandboxing/)** - 容器化抽象层

### 8.3 理论分析

- **[资源模型](../../COGNITIVE/05-decision-analysis/decision-models/01-theory-models/01-resource-models.md)** - 资源管理的理论分析
- **[隔离模型](../../COGNITIVE/05-decision-analysis/decision-models/01-theory-models/02-isolation-models.md)** - 隔离机制的理论分析

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核实现分析 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
