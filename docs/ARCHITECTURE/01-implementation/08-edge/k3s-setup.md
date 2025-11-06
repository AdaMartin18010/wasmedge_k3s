# K3s 安装和配置

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 核心特性](#11-核心特性)
- [2. 前置要求](#2-前置要求)
  - [2.1 系统要求](#21-系统要求)
  - [2.2 网络要求](#22-网络要求)
- [3. 安装步骤](#3-安装步骤)
  - [3.1 单节点安装](#31-单节点安装)
  - [3.2 Agent 节点安装](#32-agent-节点安装)
  - [3.3 启用 WasmEdge 支持](#33-启用-wasmedge-支持)
- [4. 配置示例](#4-配置示例)
  - [4.1 基本配置](#41-基本配置)
  - [4.2 禁用组件](#42-禁用组件)
  - [4.3 使用外部数据库](#43-使用外部数据库)
- [5. 高可用配置](#5-高可用配置)
  - [5.1 嵌入式 etcd（推荐）](#51-嵌入式-etcd推荐)
  - [5.2 外部数据库](#52-外部数据库)
- [6. 相关文档](#6-相关文档)

---

## 1. 概述

**K3s** 是轻量级 Kubernetes 发行版，专为边缘计算设计，提供完整的 Kubernetes API
支持。

### 1.1 核心特性

- **轻量级**：< 100 MB 二进制文件
- **ARM 支持**：支持 ARM64 架构
- **离线支持**：支持离线运行
- **内置组件**：内置 containerd、flannel、traefik、metrics-server

---

## 2. 前置要求

### 2.1 系统要求

- **操作系统**：Linux（Ubuntu 20.04+, RHEL 8+, CentOS 8+）
- **内核版本**：≥ 5.4
- **CPU**：≥ 1 CPU
- **内存**：≥ 512 MB RAM（推荐 ≥ 1 GB）

### 2.2 网络要求

- **端口**：6443（API Server）、10250（kubelet）、8472（flannel VXLAN）
- **DNS**：需要可用的 DNS 服务器

---

## 3. 安装步骤

### 3.1 单节点安装

```bash
# 安装 K3s Server
curl -sfL https://get.k3s.io | sh -

# 验证安装
kubectl get nodes

# 获取 kubeconfig
sudo cat /etc/rancher/k3s/k3s.yaml
```

### 3.2 Agent 节点安装

```bash
# 在 Server 节点获取 token
sudo cat /var/lib/rancher/k3s/server/node-token

# 在 Agent 节点安装
curl -sfL https://get.k3s.io | K3S_URL=https://<server-ip>:6443 K3S_TOKEN=<token> sh -
```

### 3.3 启用 WasmEdge 支持

```bash
# 安装 K3s 时启用 WasmEdge
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--wasm" sh -

# 验证 WasmEdge 支持
kubectl get runtimeclass
```

---

## 4. 配置示例

### 4.1 基本配置

```yaml
# /etc/rancher/k3s/config.yaml
write-kubeconfig-mode: "0644"
tls-san:
  - "k3s.example.com"
cluster-cidr: "10.42.0.0/16"
service-cidr: "10.43.0.0/16"
```

### 4.2 禁用组件

```bash
# 禁用 traefik
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik" sh -

# 禁用 flannel（使用自定义 CNI）
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--flannel-backend=none" sh -
```

### 4.3 使用外部数据库

```bash
# 使用 MySQL
curl -sfL https://get.k3s.io | \
  INSTALL_K3S_EXEC="--datastore-endpoint mysql://user:password@tcp(host:3306)/database" sh -

# 使用 PostgreSQL
curl -sfL https://get.k3s.io | \
  INSTALL_K3S_EXEC="--datastore-endpoint postgres://user:password@host:5432/database" sh -
```

---

## 5. 高可用配置

### 5.1 嵌入式 etcd（推荐）

```bash
# 第一个 Server 节点
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--cluster-init" sh -

# 其他 Server 节点
curl -sfL https://get.k3s.io | \
  K3S_URL=https://<first-server-ip>:6443 \
  K3S_TOKEN=<token> \
  INSTALL_K3S_EXEC="server" sh -
```

### 5.2 外部数据库

```bash
# 所有 Server 节点使用相同的外部数据库
curl -sfL https://get.k3s.io | \
  INSTALL_K3S_EXEC="--datastore-endpoint mysql://user:password@tcp(host:3306)/database" sh -
```

---

## 6. 相关文档

- [`README.md`](README.md) - 边缘计算实现细节总览
- [`wasmedge-edge.md`](wasmedge-edge.md) - WasmEdge 边缘部署
- [`nsm-edge.md`](nsm-edge.md) - NSM 边缘网关配置

---

**更新时间**：2025-11-05 **版本**：v1.0
