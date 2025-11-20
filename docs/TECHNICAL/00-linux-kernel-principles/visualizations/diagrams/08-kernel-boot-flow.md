# 内核启动流程关系图

## 📑 目录

- [内核启动流程关系图](#内核启动流程关系图)
  - [📑 目录](#-目录)
  - [1 完整启动流程关系图](#1-完整启动流程关系图)
  - [2 内核初始化关系图](#2-内核初始化关系图)
  - [3 系统初始化关系图](#3-系统初始化关系图)

---

## 1 完整启动流程关系图

```mermaid
graph TB
    subgraph "硬件层"
        A[BIOS/UEFI]
        B[硬件初始化]
    end

    subgraph "引导层"
        C[Bootloader]
        D[GRUB]
        E[内核加载]
    end

    subgraph "内核层"
        F[head.S]
        G[内核解压]
        H[start_kernel]
        I[CPU 初始化]
        J[内存初始化]
        K[中断初始化]
        L[设备初始化]
    end

    subgraph "系统层"
        M[init 进程]
        N[用户空间]
        O[系统服务]
    end

    A --> B
    B --> C
    C --> D
    D --> E

    E --> F
    F --> G
    G --> H

    H --> I
    H --> J
    H --> K
    H --> L

    I --> M
    J --> M
    K --> M
    L --> M

    M --> N
    N --> O

    style A fill:#ff9999
    style C fill:#99ccff
    style H fill:#99ff99
    style M fill:#ffcc99
```

---

## 2 内核初始化关系图

```mermaid
graph LR
    subgraph "start_kernel"
        A[start_kernel]
        B[setup_arch]
        C[mm_init]
        D[sched_init]
        E[time_init]
        F[init_IRQ]
        G[rest_init]
    end

    subgraph "子系统初始化"
        H[进程管理]
        I[内存管理]
        J[调度器]
        K[时间管理]
        L[中断管理]
    end

    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G

    B --> H
    C --> I
    D --> J
    E --> K
    F --> L

    style A fill:#ff9999
    style G fill:#99ccff
```

---

## 3 系统初始化关系图

```mermaid
graph TB
    subgraph "内核空间"
        A[rest_init]
        B[kernel_init]
        C[kthreadd]
    end

    subgraph "用户空间"
        D[init 进程]
        E[systemd/sysvinit]
        F[系统服务]
    end

    A --> B
    A --> C

    B --> D
    D --> E
    E --> F

    style A fill:#ff9999
    style D fill:#99ccff
    style E fill:#99ff99
```

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核启动流程关系图 | 🎯 生产就绪
**维护者**：项目团队
