# WasmEdge 边缘部署

## 📑 目录

- [1. 概述](#1-概述)
- [2. WasmEdge 安装](#2-wasmedge-安装)
- [3. Kubernetes 集成](#3-kubernetes-集成)
- [4. 边缘 AI 推理](#4-边缘-ai-推理)
- [5. 相关文档](#5-相关文档)

---

## 1. 概述

**WasmEdge** 是云原生 WebAssembly 运行时，特别适合边缘计算场景，提供极速启动和极轻量的特性。

### 1.1 核心特性

- **极速启动**：冷启动 < 1ms
- **极轻量**：镜像 < 2 MB
- **边缘 AI**：支持边缘 AI 推理（WasmEdge AI）
- **Kubernetes 集成**：Kubernetes 1.30 双运行时支持

---

## 2. WasmEdge 安装

### 2.1 边缘节点安装

```bash
# 安装 WasmEdge
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash

# 验证安装
wasmedge --version

# 安装 crun（支持 Wasm）
sudo apt-get install -y crun
```

### 2.2 containerd Wasm shim 安装

```bash
# 安装 containerd-shim-wasmedge
wget https://github.com/containerd/containerd-shim-wasmedge/releases/download/v1.0.0/containerd-shim-wasmedge-v1.0.0-linux-amd64.tar.gz
tar -xzf containerd-shim-wasmedge-v1.0.0-linux-amd64.tar.gz
sudo mv containerd-shim-wasmedge-v1.0.0-linux-amd64 /usr/local/bin/containerd-shim-wasmedge-v1

# 配置 containerd
sudo mkdir -p /etc/containerd
cat <<EOF | sudo tee /etc/containerd/config.toml
version = 2
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.wasmedge]
  runtime_type = "io.containerd.wasmedge.v1"
EOF

# 重启 containerd
sudo systemctl restart containerd
```

---

## 3. Kubernetes 集成

### 3.1 RuntimeClass 配置

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: wasmedge
handler: wasmedge
---
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app
spec:
  runtimeClassName: wasmedge
  containers:
    - name: wasm-container
      image: docker.io/library/wasm-app:latest
      command: ["wasmedge", "/app/app.wasm"]
```

### 3.2 K3s WasmEdge 支持

```bash
# K3s 1.30 内置 WasmEdge 支持
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--wasm" sh -

# 验证 RuntimeClass
kubectl get runtimeclass
```

---

## 4. 边缘 AI 推理

### 4.1 WasmEdge AI 安装

```bash
# 安装 WasmEdge AI 插件
wget https://github.com/WasmEdge/WasmEdge/releases/download/0.14.0/WasmEdge-0.14.0-manylinux2014_x86_64.tar.gz
tar -xzf WasmEdge-0.14.0-manylinux2014_x86_64.tar.gz
sudo cp WasmEdge-0.14.0-Linux/bin/* /usr/local/bin/

# 安装 WasmEdge AI 插件
wget https://github.com/WasmEdge/WasmEdge/releases/download/0.14.0/WasmEdge-AI-0.14.0-manylinux2014_x86_64.tar.gz
tar -xzf WasmEdge-AI-0.14.0-manylinux2014_x86_64.tar.gz
sudo cp WasmEdge-AI-0.14.0-Linux/lib/* /usr/local/lib/
```

### 4.2 边缘 AI 推理 Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: edge-ai-inference
spec:
  runtimeClassName: wasmedge
  containers:
    - name: ai-inference
      image: docker.io/library/edge-ai-model:latest
      command: ["wasmedge", "--enable-gpu", "/app/model.wasm"]
      resources:
        limits:
          memory: "512Mi"
          cpu: "2"
```

---

## 5. 相关文档

- [`README.md`](README.md) - 边缘计算实现细节总览
- [`k3s-setup.md`](k3s-setup.md) - K3s 安装和配置
- [`../../06-wasm/wasmedge-setup.md`](../../06-wasm/wasmedge-setup.md) - WasmEdge 详细配置

---

**更新时间**：2025-11-05 **版本**：v1.0

