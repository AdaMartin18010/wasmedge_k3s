# 容器化技术栈关系图

## 📑 目录

- [容器化技术栈关系图](#容器化技术栈关系图)
  - [📑 目录](#-目录)
  - [1 容器化技术栈全景](#1-容器化技术栈全景)
  - [2 Docker 技术栈关系图](#2-docker-技术栈关系图)
  - [3 Kubernetes 技术栈关系图](#3-kubernetes-技术栈关系图)
  - [4 容器运行时关系图](#4-容器运行时关系图)

---

## 1 容器化技术栈全景

```mermaid
graph TB
    A[应用程序] --> B[容器镜像]
    B --> C[容器运行时]

    C --> D[Namespace]
    C --> E[Cgroup]
    C --> F[Capabilities]
    C --> G[Seccomp]
    C --> H[LSM]

    D --> I[PID Namespace]
    D --> J[Network Namespace]
    D --> K[Mount Namespace]
    D --> L[User Namespace]

    E --> M[CPU Controller]
    E --> N[Memory Controller]
    E --> O[IO Controller]

    F --> P[Effective Set]
    F --> Q[Permitted Set]

    G --> R[BPF Filter]

    H --> S[SELinux]
    H --> T[AppArmor]

    U[Docker] --> C
    V[Kubernetes] --> C
    W[containerd] --> C
    X[runc] --> C

    Y[Linux 内核] --> D
    Y --> E
    Y --> F
    Y --> G
    Y --> H

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style D fill:#ffcc99
    style E fill:#cc99ff
    style F fill:#ffff99
    style G fill:#ffccff
    style H fill:#ccccff
    style Y fill:#66ff66
```

---

## 2 Docker 技术栈关系图

```mermaid
graph LR
    A[Docker CLI] --> B[Docker Daemon]
    B --> C[containerd]
    C --> D[containerd-shim]
    D --> E[runc]

    E --> F[Namespace]
    E --> G[Cgroup]
    E --> H[Capabilities]
    E --> I[Seccomp]

    F --> J[PID]
    F --> K[Network]
    F --> L[Mount]
    F --> M[User]

    G --> N[CPU]
    G --> O[Memory]
    G --> P[IO]

    Q[镜像存储] --> B
    R[网络管理] --> B
    S[存储驱动] --> B

    T[OverlayFS] --> S

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style D fill:#ffcc99
    style E fill:#cc99ff
    style F fill:#ffff99
    style G fill:#ffccff
    style H fill:#ccccff
    style I fill:#ccffcc
```

---

## 3 Kubernetes 技术栈关系图

```mermaid
graph TD
    A[kubectl] --> B[API Server]
    B --> C[etcd]

    B --> D[kube-scheduler]
    B --> E[kube-controller-manager]

    D --> F[Node]
    E --> F

    F --> G[kubelet]
    G --> H[CRI]
    H --> I[containerd]
    H --> J[CRI-O]

    I --> K[runc]
    J --> K

    K --> L[Namespace]
    K --> M[Cgroup]
    K --> N[Capabilities]
    K --> O[Seccomp]
    K --> P[LSM]

    Q[CNI] --> F
    R[CSI] --> F
    S[Device Plugin] --> F

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style D fill:#ffcc99
    style E fill:#cc99ff
    style F fill:#ffff99
    style G fill:#ffccff
    style H fill:#ccccff
    style I fill:#ccffcc
    style J fill:#ffcccc
    style K fill:#ffffcc
```

---

## 4 容器运行时关系图

```mermaid
graph TD
    A[容器运行时] --> B[OCI Runtime]
    A --> C[CRI Runtime]

    B --> D[runc]
    B --> E[crun]
    B --> F[runwasi]

    C --> G[containerd]
    C --> H[CRI-O]
    C --> I[Docker Engine]

    D --> J[Namespace]
    D --> K[Cgroup]
    D --> L[Capabilities]
    D --> M[Seccomp]

    E --> J
    E --> K
    E --> L
    E --> M

    F --> N[Wasm Runtime]
    N --> O[WasmEdge]
    N --> P[wasmtime]

    Q[Kata Containers] --> R[KVM]
    Q --> S[QEMU]
    Q --> T[轻量级 VM]

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style D fill:#ffcc99
    style E fill:#cc99ff
    style F fill:#ffff99
    style G fill:#ffccff
    style H fill:#ccccff
    style I fill:#ccffcc
    style Q fill:#ffcccc
```

---

## 5 安全机制关系图

```mermaid
graph TD
    A[容器安全] --> B[隔离机制]
    A --> C[权限控制]
    A --> D[访问控制]

    B --> E[Namespace]
    B --> F[Cgroup]

    C --> G[Capabilities]
    C --> H[Seccomp]
    C --> I[User Namespace]

    D --> J[LSM]
    J --> K[SELinux]
    J --> L[AppArmor]

    M[Docker] --> A
    N[Kubernetes] --> A

    O[安全策略] --> G
    O --> H
    O --> J

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style D fill:#ffcc99
    style E fill:#cc99ff
    style F fill:#ffff99
    style G fill:#ffccff
    style H fill:#ccccff
    style I fill:#ccffcc
    style J fill:#ffcccc
    style K fill:#ffffcc
    style L fill:#ccffff
```

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含技术栈关系图 | 🎯 生产就绪
**维护者**：项目团队
