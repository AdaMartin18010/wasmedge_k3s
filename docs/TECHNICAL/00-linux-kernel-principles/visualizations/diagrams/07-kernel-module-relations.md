# 内核模块关系图

## 📑 目录

- [内核模块关系图](#内核模块关系图)
  - [📑 目录](#-目录)
  - [1 模块加载关系图](#1-模块加载关系图)
  - [2 模块依赖关系图](#2-模块依赖关系图)
  - [3 模块接口关系图](#3-模块接口关系图)
  - [4 模块开发关系图](#4-模块开发关系图)

---

## 1 模块加载关系图

```mermaid
graph TB
    subgraph "用户空间"
        A[insmod]
        B[modprobe]
        C[kmod]
    end

    subgraph "系统调用层"
        D[init_module]
        E[delete_module]
    end

    subgraph "内核模块层"
        F[模块验证]
        G[符号解析]
        H[模块初始化]
        I[module_init]
        J[模块清理]
        K[module_exit]
    end

    subgraph "模块接口"
        L[导出符号]
        M[模块参数]
        N[模块信息]
    end

    A --> D
    B --> D
    C --> D

    D --> F
    F --> G
    G --> H
    H --> I

    E --> J
    J --> K

    I --> L
    I --> M
    I --> N

    style A fill:#ff9999
    style B fill:#ff9999
    style C fill:#ff9999
    style D fill:#99ccff
    style E fill:#99ccff
    style I fill:#99ff99
    style K fill:#99ff99
```

---

## 2 模块依赖关系图

```mermaid
graph LR
    subgraph "模块 A"
        A1[模块 A]
        A2[导出符号]
    end

    subgraph "模块 B"
        B1[模块 B]
        B2[依赖符号]
    end

    subgraph "模块 C"
        C1[模块 C]
        C2[依赖符号]
    end

    A2 --> B2
    A2 --> C2
    B1 --> A1
    C1 --> A1

    style A1 fill:#ff9999
    style B1 fill:#99ccff
    style C1 fill:#99ff99
```

---

## 3 模块接口关系图

```mermaid
graph TB
    subgraph "内核模块"
        A[模块代码]
        B[导出符号]
        C[模块参数]
        D[模块信息]
    end

    subgraph "内核核心"
        E[内核符号表]
        F[模块子系统]
    end

    subgraph "用户空间"
        G[/sys/module/]
        H[模块参数文件]
    end

    A --> B
    A --> C
    A --> D

    B --> E
    A --> F

    C --> G
    G --> H

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style E fill:#ffcc99
    style F fill:#cc99ff
```

---

## 4 模块开发关系图

```mermaid
graph TB
    subgraph "模块开发"
        A[模块头文件]
        B[模块初始化]
        C[模块清理]
        D[设备注册]
        E[中断注册]
    end

    subgraph "内核接口"
        F[module_init]
        G[module_exit]
        H[register_chrdev]
        I[request_irq]
    end

    subgraph "资源管理"
        J[内存分配]
        K[内存释放]
        L[错误处理]
    end

    A --> B
    A --> C
    B --> D
    B --> E

    B --> F
    C --> G
    D --> H
    E --> I

    B --> J
    C --> K
    B --> L
    C --> L

    style A fill:#ff9999
    style B fill:#99ccff
    style C fill:#99ff99
    style F fill:#ffcc99
    style G fill:#cc99ff
```

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核模块关系图 | 🎯 生产就绪
**维护者**：项目团队
