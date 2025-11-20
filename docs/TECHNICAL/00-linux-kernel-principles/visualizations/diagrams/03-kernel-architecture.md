# 内核架构图

## 📑 目录

- [内核架构图](#内核架构图)
  - [📑 目录](#-目录)
  - [1 Linux 内核整体架构](#1-linux-内核整体架构)
  - [2 内核空间与用户空间](#2-内核空间与用户空间)
  - [3 内核子系统架构](#3-内核子系统架构)
  - [4 容器化架构](#4-容器化架构)

---

## 1 Linux 内核整体架构

```mermaid
graph TB
    subgraph "用户空间"
        A[应用程序]
        B[系统库]
        C[Shell]
    end

    subgraph "系统调用接口"
        D[syscall]
        E[系统调用表]
    end

    subgraph "内核空间"
        subgraph "进程管理"
            F[进程调度]
            G[进程创建]
            H[IPC]
        end

        subgraph "内存管理"
            I[虚拟内存]
            J[物理内存]
            K[内存映射]
        end

        subgraph "文件系统"
            L[VFS]
            M[文件系统]
            N[设备文件]
        end

        subgraph "网络子系统"
            O[Socket]
            P[TCP/IP]
            Q[网络设备]
        end

        subgraph "设备驱动"
            R[字符设备]
            S[块设备]
            T[网络设备]
        end

        subgraph "容器化机制"
            U[Namespace]
            V[Cgroup]
            W[Capabilities]
            X[Seccomp]
        end
    end

    subgraph "硬件层"
        Y[CPU]
        Z[内存]
        AA[存储]
        AB[网络]
    end

    A --> D
    B --> D
    C --> D

    D --> E
    E --> F
    E --> I
    E --> L
    E --> O
    E --> R

    F --> Y
    I --> Z
    L --> AA
    O --> AB
    R --> Y
    R --> Z
    R --> AA
    R --> AB

    U --> F
    V --> F
    V --> I
    W --> D
    X --> D

    style A fill:#ff9999
    style D fill:#99ccff
    style F fill:#99ff99
    style I fill:#ffcc99
    style L fill:#cc99ff
    style O fill:#ffff99
    style R fill:#ffccff
    style U fill:#ccccff
    style V fill:#ccffcc
    style W fill:#ffcccc
    style X fill:#ffffcc
```

---

## 2 内核空间与用户空间

```mermaid
graph TB
    subgraph "用户空间 (0x0000000000000000 - 0x00007FFFFFFFFFFF)"
        A[应用程序代码段]
        B[应用程序数据段]
        C[堆 Heap]
        D[栈 Stack]
        E[共享库]
        F[内存映射区]
    end

    subgraph "系统调用边界"
        G[syscall 指令]
        H[软中断]
    end

    subgraph "内核空间 (0xFFFF800000000000 - 0xFFFFFFFFFFFFFFFF)"
        I[内核代码段]
        J[内核数据段]
        K[直接映射区]
        L[vmalloc 区]
        M[持久映射区]
        N[固定映射区]
    end

    A --> G
    B --> G
    C --> G
    D --> G
    E --> G
    F --> G

    G --> H
    H --> I

    I --> J
    J --> K
    K --> L
    L --> M
    M --> N

    style A fill:#ff9999
    style B fill:#ff9999
    style C fill:#ff9999
    style D fill:#ff9999
    style E fill:#ff9999
    style F fill:#ff9999
    style G fill:#99ccff
    style H fill:#99ccff
    style I fill:#99ff99
    style J fill:#99ff99
    style K fill:#99ff99
    style L fill:#99ff99
    style M fill:#99ff99
    style N fill:#99ff99
```

---

## 3 内核子系统架构

```mermaid
graph LR
    subgraph "进程管理子系统"
        A[task_struct]
        B[进程调度器]
        C[进程创建]
        D[IPC 机制]
    end

    subgraph "内存管理子系统"
        E[虚拟地址空间]
        F[页表管理]
        G[物理内存管理]
        H[内存映射]
    end

    subgraph "文件系统子系统"
        I[VFS 抽象层]
        J[文件系统实现]
        K[设备文件]
        L[挂载管理]
    end

    subgraph "网络子系统"
        M[Socket 层]
        N[TCP/IP 协议栈]
        O[网络设备]
        P[路由表]
    end

    subgraph "设备驱动子系统"
        Q[设备模型]
        R[字符设备]
        S[块设备]
        T[网络设备]
    end

    A --> E
    A --> I
    A --> M

    E --> F
    F --> G
    G --> H

    I --> J
    J --> K
    K --> L

    M --> N
    N --> O
    O --> P

    Q --> R
    Q --> S
    Q --> T

    style A fill:#ff9999
    style E fill:#99ccff
    style I fill:#99ff99
    style M fill:#ffcc99
    style Q fill:#cc99ff
```

---

## 4 容器化架构

```mermaid
graph TB
    subgraph "容器应用层"
        A[容器应用]
        B[容器镜像]
    end

    subgraph "容器运行时层"
        C[Docker/containerd]
        D[runc]
    end

    subgraph "Linux 内核层"
        subgraph "隔离机制"
            E[PID Namespace]
            F[Network Namespace]
            G[Mount Namespace]
            H[User Namespace]
            I[UTS Namespace]
            J[IPC Namespace]
        end

        subgraph "资源限制"
            K[Cgroup v2]
            L[CPU Controller]
            M[Memory Controller]
            N[IO Controller]
        end

        subgraph "安全机制"
            O[Capabilities]
            P[Seccomp]
            Q[LSM]
        end

        subgraph "内核子系统"
            R[进程管理]
            S[内存管理]
            T[文件系统]
            U[网络子系统]
        end
    end

    A --> C
    B --> C
    C --> D

    D --> E
    D --> F
    D --> G
    D --> H
    D --> I
    D --> J

    D --> K
    K --> L
    K --> M
    K --> N

    D --> O
    D --> P
    D --> Q

    E --> R
    F --> U
    G --> T
    K --> R
    K --> S
    O --> R
    P --> R

    style A fill:#ff9999
    style C fill:#99ccff
    style D fill:#99ff99
    style E fill:#ffcc99
    style F fill:#ffcc99
    style G fill:#ffcc99
    style H fill:#ffcc99
    style I fill:#ffcc99
    style J fill:#ffcc99
    style K fill:#cc99ff
    style O fill:#ffff99
    style P fill:#ffff99
    style Q fill:#ffff99
```

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含架构图 | 🎯 生产就绪
**维护者**：项目团队
