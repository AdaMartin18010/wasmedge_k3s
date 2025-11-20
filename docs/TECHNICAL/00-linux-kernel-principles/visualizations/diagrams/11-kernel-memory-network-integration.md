# 内核内存与网络集成关系图

## 📑 目录

- [内核内存与网络集成关系图](#内核内存与网络集成关系图)
  - [📑 目录](#-目录)
  - [1 内存与网络集成全景](#1-内存与网络集成全景)
  - [2 零拷贝技术关系图](#2-零拷贝技术关系图)
  - [3 网络缓冲区管理关系图](#3-网络缓冲区管理关系图)

---

## 1 内存与网络集成全景

```mermaid
graph TB
    subgraph "内存管理"
        A[页面分配]
        B[内存映射]
        C[零拷贝]
    end

    subgraph "网络子系统"
        D[Socket 缓冲区]
        E[网络数据包]
        F[网络设备]
    end

    subgraph "数据传输"
        G[sendfile]
        H[splice]
        I[MSG_ZEROCOPY]
    end

    A --> D
    B --> E
    C --> F

    D --> G
    E --> H
    F --> I

    G --> C
    H --> C
    I --> C

    style A fill:#ff9999
    style D fill:#99ccff
    style G fill:#99ff99
    style C fill:#ffcc99
```

---

## 2 零拷贝技术关系图

```mermaid
graph LR
    subgraph "文件系统"
        A[文件读取]
        B[文件写入]
    end

    subgraph "网络传输"
        C[Socket 发送]
        D[Socket 接收]
    end

    subgraph "零拷贝技术"
        E[sendfile]
        F[splice]
        G[MSG_ZEROCOPY]
    end

    A --> E
    B --> F
    C --> G
    D --> G

    E --> C
    F --> C
    G --> C

    style A fill:#ff9999
    style C fill:#99ccff
    style E fill:#99ff99
```

---

## 3 网络缓冲区管理关系图

```mermaid
graph TB
    subgraph "内存管理"
        A[页面分配]
        B[内存池]
        C[缓冲区]
    end

    subgraph "网络缓冲区"
        D[sk_buff]
        E[数据包]
        F[缓冲区管理]
    end

    subgraph "网络设备"
        G[网卡驱动]
        H[DMA]
        I[网络设备]
    end

    A --> D
    B --> E
    C --> F

    D --> G
    E --> H
    F --> I

    style A fill:#ff9999
    style D fill:#99ccff
    style G fill:#99ff99
```

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核内存与网络集成关系图 | 🎯 生产就绪
**维护者**：项目团队
