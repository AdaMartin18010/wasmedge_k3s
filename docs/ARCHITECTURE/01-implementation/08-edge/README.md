# 边缘计算实现细节文档集

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 核心思想](#11-核心思想)
  - [1.2 实现目标](#12-实现目标)
- [2. 文档结构](#2-文档结构)
- [3. 核心概念](#3-核心概念)
  - [3.1 K3s](#31-k3s)
  - [3.2 WasmEdge](#32-wasmedge)
  - [3.3 NSM（Network Service Mesh）](#33-nsmnetwork-service-mesh)
  - [3.4 边缘-云同步](#34-边缘-云同步)
- [4. 相关文档](#4-相关文档)
  - [4.1 架构视角文档](#41-架构视角文档)
  - [4.2 理论文档](#42-理论文档)
  - [4.3 源文档](#43-源文档)

---

## 1. 概述

本目录包含 **边缘计算** 实现细节文档，包括 K3s 配置、WasmEdge 边缘部署、NSM 边缘
网关、边缘-云同步等。

### 1.1 核心思想

> **通过轻量级 Kubernetes（K3s）、WebAssembly 运行时（WasmEdge）和网络服务网格
> （NSM）实现边缘节点的统一管理、低延迟访问和离线运行能力**

### 1.2 实现目标

- **轻量级部署**：通过 K3s 实现边缘节点的轻量级 Kubernetes 部署
- **低延迟访问**：通过边缘节点实现低延迟访问
- **离线运行**：支持边缘节点的离线运行能力
- **统一管理**：通过云端控制平面实现边缘节点的统一管理

---

## 2. 文档结构

```text
08-edge/
├── README.md              # 本文档（总览）
├── k3s-setup.md          # K3s 安装和配置
├── wasmedge-edge.md      # WasmEdge 边缘部署
├── nsm-edge.md           # NSM 边缘网关配置
└── edge-cloud-sync.md    # 边缘-云同步配置
```

---

## 3. 核心概念

### 3.1 K3s

**K3s** 是轻量级 Kubernetes 发行版，专为边缘计算设计：

- **轻量级**：< 100 MB 二进制文件
- **ARM 支持**：支持 ARM64 架构
- **离线支持**：支持离线运行
- **内置组件**：内置 containerd、flannel、traefik

### 3.2 WasmEdge

**WasmEdge** 是云原生 WebAssembly 运行时：

- **极速启动**：冷启动 < 1ms
- **极轻量**：镜像 < 2 MB
- **边缘 AI**：支持边缘 AI 推理
- **Kubernetes 集成**：Kubernetes 1.30 双运行时支持

### 3.3 NSM（Network Service Mesh）

**NSM** 是云原生网络服务网格：

- **跨域网络**：支持跨域网络聚合
- **边缘网关**：NSM Edge Gateway 实现边缘-云连接
- **vWire**：虚拟 Wire 实现网络连接
- **vL3**：虚拟 L3 网络实现

### 3.4 边缘-云同步

**边缘-云同步**：

- **配置同步**：云端配置同步到边缘节点
- **数据同步**：边缘数据同步到云端
- **状态同步**：边缘状态同步到云端
- **版本管理**：边缘应用版本管理

---

## 4. 相关文档

### 4.1 架构视角文档

- [`../../02-views/10-quick-views/edge-computing-view.md`](../../02-views/10-quick-views/edge-computing-view.md) -
  边缘计算架构视角
- [`../../02-views/10-quick-views/webassembly-view.md`](../../02-views/10-quick-views/webassembly-view.md) -
  WebAssembly 架构视角（WasmEdge 边缘部署）
- [`../../02-views/10-quick-views/ai-ml-architecture-view.md`](../../02-views/10-quick-views/ai-ml-architecture-view.md)
  ⭐ 新增（2025-11-07） - AI/ML 架构视角（边缘 AI 推理）

### 4.2 理论文档

- [`../../00-theory/`](../../00-theory/) - 理论论证文档

### 4.3 源文档

- [`../../architecture_view.md`](../../architecture_view.md) - 架构视角的核心论
  述

---

**更新时间**：2025-11-05 **版本**：v1.0 **参考**：`architecture_view.md` 边缘计
算架构部分
