# 内核机制关系图

## 📑 目录

- [内核机制关系图](#内核机制关系图)
  - [📑 目录](#-目录)
  - [1 内核机制依赖关系图](#1-内核机制依赖关系图)
  - [2 容器化机制关系图](#2-容器化机制关系图)
  - [3 安全机制关系图](#3-安全机制关系图)
  - [4 系统调用关系图](#4-系统调用关系图)
  - [5 内存管理关系图](#5-内存管理关系图)

---

## 1 内核机制依赖关系图

```mermaid
graph TD
    A[系统调用] --> B[进程管理]
    A --> C[内存管理]
    A --> D[文件系统]
    A --> E[网络子系统]
    A --> F[设备驱动]

    B --> C
    B --> D
    B --> E

    C --> D
    C --> E

    D --> F
    E --> F

    G[Namespace] --> B
    G --> D
    G --> E

    H[Cgroup] --> B
    H --> C
    H --> F

    I[Capabilities] --> A
    I --> B
    I --> D
    I --> F

    J[Seccomp] --> A

    K[LSM] --> A
    K --> B
    K --> D
    K --> E

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style D fill:#ffcc99
    style E fill:#cc99ff
    style F fill:#ffff99
    style G fill:#99ffcc
    style H fill:#ff99cc
    style I fill:#ccff99
    style J fill:#ffccff
    style K fill:#ccccff
```

**关系说明**：

- **红色**：系统调用（核心接口）
- **蓝色**：进程管理
- **绿色**：内存管理
- **橙色**：文件系统
- **紫色**：网络子系统
- **黄色**：设备驱动
- **青色**：容器化机制
- **粉色**：安全机制

---

## 2 容器化机制关系图

```mermaid
graph LR
    A[容器进程] --> B[PID Namespace]
    A --> C[Network Namespace]
    A --> D[Mount Namespace]
    A --> E[User Namespace]
    A --> F[UTS Namespace]
    A --> G[IPC Namespace]

    A --> H[Cgroup v2]
    H --> I[CPU Controller]
    H --> J[Memory Controller]
    H --> K[IO Controller]

    A --> L[Capabilities]
    A --> M[Seccomp]
    A --> N[LSM]

    N --> O[SELinux]
    N --> P[AppArmor]

    Q[Docker] --> A
    R[Kubernetes] --> A
    S[runc] --> A

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ccff
    style D fill:#99ccff
    style E fill:#99ccff
    style F fill:#99ccff
    style G fill:#99ccff
    style H fill:#99ff99
    style I fill:#99ff99
    style J fill:#99ff99
    style K fill:#99ff99
    style L fill:#ffcc99
    style M fill:#ffcc99
    style N fill:#ffcc99
    style O fill:#cc99ff
    style P fill:#cc99ff
    style Q fill:#ffff99
    style R fill:#ffff99
    style S fill:#ffff99
```

**关系说明**：

- **红色**：容器进程（核心）
- **蓝色**：Namespace（隔离机制）
- **绿色**：Cgroup（资源限制）
- **橙色**：安全机制（权限控制）
- **紫色**：LSM 模块
- **黄色**：容器运行时

---

## 3 安全机制关系图

```mermaid
graph TD
    A[进程] --> B[Capabilities]
    A --> C[Seccomp]
    A --> D[LSM]

    B --> E[Effective Set]
    B --> F[Permitted Set]
    B --> G[Inheritable Set]

    C --> H[Strict Mode]
    C --> I[Filter Mode]
    I --> J[BPF Filter]

    D --> K[SELinux]
    D --> L[AppArmor]
    D --> M[Smack]
    D --> N[Yama]

    K --> O[安全上下文]
    K --> P[策略规则]

    L --> Q[配置文件]
    L --> R[学习模式]

    S[容器] --> A
    S --> B
    S --> C
    S --> D

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style D fill:#ffcc99
    style E fill:#ccccff
    style F fill:#ccccff
    style G fill:#ccccff
    style H fill:#ccffcc
    style I fill:#ccffcc
    style J fill:#ccffcc
    style K fill:#ffccff
    style L fill:#ffccff
    style M fill:#ffccff
    style N fill:#ffccff
    style S fill:#ffff99
```

**关系说明**：

- **红色**：进程（核心）
- **蓝色**：Capabilities（权限控制）
- **绿色**：Seccomp（系统调用过滤）
- **橙色**：LSM（强制访问控制）
- **黄色**：容器（应用场景）

---

## 4 系统调用关系图

```mermaid
graph TD
    A[用户空间] -->|系统调用| B[系统调用入口]
    B --> C[sys_call_table]

    C --> D[进程管理]
    C --> E[内存管理]
    C --> F[文件系统]
    C --> G[网络子系统]
    C --> H[设备驱动]

    D --> I[fork]
    D --> J[clone]
    D --> K[execve]
    D --> L[exit]

    E --> M[mmap]
    E --> N[munmap]
    E --> O[brk]

    F --> P[open]
    F --> Q[read]
    F --> R[write]
    F --> S[close]

    G --> T[socket]
    G --> U[bind]
    G --> V[connect]
    G --> W[send/recv]

    H --> X[ioctl]

    Y[Seccomp] --> B
    Z[LSM] --> D
    Z --> E
    Z --> F
    Z --> G

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style D fill:#ffcc99
    style E fill:#cc99ff
    style F fill:#ffff99
    style G fill:#ffccff
    style H fill:#ccccff
    style Y fill:#ff6666
    style Z fill:#66ff66
```

**关系说明**：

- **红色**：用户空间
- **蓝色**：系统调用入口
- **绿色**：系统调用表
- **橙色/紫色/黄色**：各子系统
- **深红色**：Seccomp（过滤）
- **深绿色**：LSM（安全检查）

---

## 5 内存管理关系图

```mermaid
graph TD
    A[进程地址空间] --> B[虚拟地址]
    B --> C[页表]
    C --> D[物理地址]

    E[mmap] --> A
    F[malloc] --> A

    C --> G[四级页表]
    G --> H[PML4]
    G --> I[PDPT]
    G --> J[PD]
    G --> K[PT]

    D --> L[页帧]
    L --> M[Buddy System]
    L --> N[Slab Allocator]

    O[内存回收] --> L
    O --> P[LRU]
    O --> Q[Swap]
    O --> R[OOM Killer]

    S[Cgroup Memory] --> A
    S --> L

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style D fill:#ffcc99
    style E fill:#cc99ff
    style F fill:#ffff99
    style G fill:#ffccff
    style L fill:#ccccff
    style M fill:#ccffcc
    style N fill:#ffcccc
    style O fill:#ffffcc
    style S fill:#ccffff
```

**关系说明**：

- **红色**：进程地址空间
- **蓝色**：虚拟地址
- **绿色**：页表
- **橙色**：物理地址
- **紫色/黄色**：内存分配
- **青色**：内存回收
- **浅青色**：Cgroup 限制

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含关系图谱 | 🎯 生产就绪
**维护者**：项目团队
