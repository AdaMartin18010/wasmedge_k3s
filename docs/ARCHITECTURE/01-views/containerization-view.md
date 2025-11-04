# 容器化视角

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 核心思想](#11-核心思想)
- [2. 容器化的"剪裁"作用](#2-容器化的剪裁作用)
  - [核心作用](#核心作用)
- [2. 层级模型中的位置](#2-层级模型中的位置)
- [3. 容器化的形式化描述](#3-容器化的形式化描述)
  - [3.1 容器定义](#31-容器定义)
  - [3.2 状态压缩](#32-状态压缩)
- [4. 容器隔离机制](#4-容器隔离机制)
  - [4.1 Linux Namespaces](#41-linux-namespaces)
  - [4.2 Cgroups (Control Groups)](#42-cgroups-control-groups)
- [5. 容器镜像结构](#5-容器镜像结构)
  - [5.1 OCI Image Format](#51-oci-image-format)
  - [5.2 层式存储](#52-层式存储)
- [6. 容器化 vs 虚拟化](#6-容器化-vs-虚拟化)
- [7. 容器编排](#7-容器编排)
  - [7.1 Kubernetes](#71-kubernetes)
  - [7.2 Docker Compose](#72-docker-compose)
  - [7.3 K3s](#73-k3s)
- [8. 容器安全](#8-容器安全)
  - [8.1 镜像安全](#81-镜像安全)
  - [8.2 运行时安全](#82-运行时安全)
  - [8.3 合规性](#83-合规性)
- [9. 2025 年容器化趋势](#9-2025-年容器化趋势)
  - [9.1 轻量级运行时](#91-轻量级运行时)
  - [9.2 eBPF 增强](#92-ebpf-增强)
  - [9.3 无服务器容器](#93-无服务器容器)
- [10. 典型案例](#10-典型案例)
  - [10.1 微服务架构](#101-微服务架构)
  - [10.2 CI/CD 流水线](#102-cicd-流水线)
- [12. 最佳实践](#12-最佳实践)
  - [12.1 容器设计原则](#121-容器设计原则)
  - [12.2 编排策略](#122-编排策略)
  - [12.3 安全实践](#123-安全实践)
- [13. 参考资源](#13-参考资源)

---

## 1. 概述

本文档从**容器化**视角阐述架构设计，说明容器化如何通过 OS 抽象和状态空间压缩，将
VM 状态压缩为轻量容器，让架构师聚焦应用逻辑。

### 1.1 核心思想

> **容器化通过共享宿主机内核和层式存储，将 VM 状态压缩为轻量容器，实现计算单元从
> "机"降维为"进程+命名空间"，让架构师聚焦应用逻辑**

---

## 2. 容器化的"剪裁"作用

**容器化**进一步抽象操作系统，把**完整操作系统**抽象成**轻量容器**，让架构师聚
焦**应用逻辑**而非系统管理。

### 核心作用

1. **OS 抽象**：共享宿主机内核，镜像仅包 rootfs + meta → 镜像 10~100 MB
2. **快速启动**：启动时间 ≈ 进程 fork + pivot_root ≈ 50~300 ms
3. **资源精细控制**：资源边界细化到**毫秒级 CPU 份额、字节级内存页**
4. **可移植性**：镜像可跨平台运行

## 2. 层级模型中的位置

| 层级           | 主要职责           | 典型技术                                  | 关注点（被裁剪）       | 让架构师聚焦         |
| -------------- | ------------------ | ----------------------------------------- | ---------------------- | -------------------- |
| **容器运行时** | 进程隔离、镜像管理 | runc, Kata, gVisor, Firecracker, WasmEdge | 容器生命周期、镜像压缩 | 轻量化部署、快速迭代 |

## 3. 容器化的形式化描述

### 3.1 容器定义

| 结构     | 定义                | 形式化                                   | 关键属性                     |
| -------- | ------------------- | ---------------------------------------- | ---------------------------- |
| **容器** | 进程+共享内核的集合 | **C = ⟨processes, namespaces, cgroups⟩** | **轻量、共享资源、快速启动** |

其中：

- processes：容器内的进程集合
- namespaces：隔离机制（PID, NET, MNT, IPC, UTS, USER）
- cgroups：资源限制（CPU, Memory, IO）

### 3.2 状态压缩

**状态压缩比**：

```text
|Σ₂| = |Host Kernel| + Σ|Containerᵢ| ≈ 10^(6) ≪ 10^(9) = |Σ₁|
```

容器化将 VM 状态空间进一步压缩：

- 计算单元从"机"**降维成"进程+命名空间"**
- 架构图首次**可画出带版本号的方框**（image@sha256:…）

## 4. 容器隔离机制

### 4.1 Linux Namespaces

| Namespace | 隔离内容       | 作用                   |
| --------- | -------------- | ---------------------- |
| **PID**   | 进程 ID        | 每个容器有独立的进程树 |
| **NET**   | 网络栈         | 独立的网络接口、路由表 |
| **MNT**   | 文件系统挂载点 | 独立的文件系统视图     |
| **IPC**   | 进程间通信     | 独立的 IPC 对象        |
| **UTS**   | 主机名和域名   | 独立的主机名           |
| **USER**  | 用户和组 ID    | 独立的用户映射         |

### 4.2 Cgroups (Control Groups)

| Controller | 限制内容   | 示例                           |
| ---------- | ---------- | ------------------------------ |
| **cpu**    | CPU 使用率 | cpu.shares = 1024              |
| **memory** | 内存使用量 | memory.limit_in_bytes = 512M   |
| **blkio**  | 块设备 I/O | blkio.throttle.read_bps_device |
| **pids**   | 进程数     | pids.max = 100                 |

## 5. 容器镜像结构

### 5.1 OCI Image Format

```text
Image
├── Manifest
│   ├── Config
│   └── Layers[]
│       ├── Layer 1 (base OS)
│       ├── Layer 2 (runtime)
│       └── Layer 3 (application)
└── Index (multi-arch)
```

### 5.2 层式存储

- **联合文件系统（UnionFS）**：OverlayFS, AUFS
- **写时复制（CoW）**：共享只读层，独立写入层
- **层缓存**：相同层可复用，加速部署

## 6. 容器化 vs 虚拟化

| 维度         | 虚拟化               | 容器化                    |
| ------------ | -------------------- | ------------------------- |
| **隔离级别** | 硬件级隔离           | OS 进程级隔离             |
| **资源开销** | 高（每 VM 2-3× RAM） | 低（共享内核）            |
| **启动时间** | 10-30 秒             | < 1 秒                    |
| **镜像大小** | 1-10 GB              | 10-100 MB                 |
| **适用场景** | 完整 OS 环境、多租户 | 微服务、CI/CD、无状态服务 |

## 7. 容器编排

### 7.1 Kubernetes

- **Pod**：最小调度单元，包含一个或多个容器
- **Deployment**：声明式部署管理
- **Service**：服务发现与负载均衡
- **ConfigMap / Secret**：配置管理

### 7.2 Docker Compose

- 单机多容器编排
- 适合开发环境

### 7.3 K3s

- 轻量级 Kubernetes
- 适合边缘和 IoT

## 8. 容器安全

### 8.1 镜像安全

- **镜像扫描**：Trivy, Clair, Snyk
- **镜像签名**：Notary, Cosign
- **最小化镜像**：Distroless, Alpine

### 8.2 运行时安全

- **Seccomp**：系统调用过滤
- **AppArmor / SELinux**：强制访问控制
- **Cilium**：网络策略

### 8.3 合规性

- **CIS Benchmarks**：容器安全基准
- **OPA Gatekeeper**：策略即代码

## 9. 2025 年容器化趋势

### 9.1 轻量级运行时

- **containerd**：CNCF 标准运行时
- **CRI-O**：Kubernetes 原生运行时
- **Podman**：无守护进程容器工具

### 9.2 eBPF 增强

- **Cilium**：eBPF 驱动的网络和安全
- **Falco**：eBPF 驱动的运行时安全

### 9.3 无服务器容器

- **Knative**：Kubernetes 上的 Serverless
- **OpenFaaS**：函数即服务
- **Cloud Run**：托管容器服务

## 10. 典型案例

### 10.1 微服务架构

```text
┌─────────────┐
│   Frontend  │
└──────┬──────┘
       │
┌──────▼──────┐
│ API Gateway │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──┐
│Order│ │Payment│
└─────┘ └─────┘
```

### 10.2 CI/CD 流水线

```text
Code → Build → Test → Package → Deploy
         ↓
    Docker Image
         ↓
    Container Registry
         ↓
    Kubernetes Cluster
```

## 12. 最佳实践

### 12.1 容器设计原则

1. **单一职责**：每个容器只运行一个进程
2. **最小化镜像**：使用 Distroless 或 Alpine 基础镜像
3. **层缓存优化**：将变化频率低的层放在底层
4. **健康检查**：配置合理的健康检查机制

### 12.2 编排策略

1. **声明式部署**：使用 Kubernetes Deployment
2. **资源限制**：为每个容器设置 requests 和 limits
3. **自动扩缩容**：使用 HPA 和 VPA 实现自动扩缩容
4. **滚动更新**：使用 RollingUpdate 策略实现零停机更新

### 12.3 安全实践

1. **镜像扫描**：CI/CD 中自动扫描镜像漏洞
2. **最小权限**：使用非 root 用户运行容器
3. **网络策略**：使用 NetworkPolicy 限制容器网络访问
4. **策略即代码**：使用 OPA 管理容器安全策略

---

## 13. 参考资源

- **OCI Image Spec**：<https://github.com/opencontainers/image-spec>
- **Docker**：<https://www.docker.com/>
- **Podman**：<https://podman.io/>
- **BuildKit**：<https://github.com/moby/buildkit>
- **Kubernetes 文档**：<https://kubernetes.io/docs/>
- **containerd 文档**：<https://containerd.io/>
- **相关文档**：
  - `02-virtualization-containerization-sandboxing/02-containerization-abstraction.md` -
    容器化抽象详细说明
  - `02-layers/runtime-container-layer.md` - 容器运行时层详细说明
  - `07-case-studies/e-commerce-platform.md` - 电商平台案例（包含容器化实践）

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
2.1-2.8 节，容器化视角部分
