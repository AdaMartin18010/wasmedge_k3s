# WasmEdge 0.14 安装和配置

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 核心特性](#11-核心特性)
- [2 安装](#2-安装)
  - [2.1 Linux 安装](#21-linux-安装)
  - [2.2 macOS 安装](#22-macos-安装)
  - [2.3 Docker 安装](#23-docker-安装)
  - [2.4 验证安装](#24-验证安装)
- [3 基本配置](#3-基本配置)
  - [3.1 配置文件](#31-配置文件)
  - [3.2 运行时配置](#32-运行时配置)
  - [3.3 环境变量](#33-环境变量)
- [4 Kubernetes 集成](#4-kubernetes-集成)
  - [4.1 安装 containerd Wasm shim](#41-安装-containerd-wasm-shim)
  - [4.2 配置 containerd](#42-配置-containerd)
  - [4.3 创建 RuntimeClass](#43-创建-runtimeclass)
  - [4.4 部署 Wasm Pod](#44-部署-wasm-pod)
- [5 性能优化](#5-性能优化)
  - [5.1 编译优化](#51-编译优化)
  - [5.2 运行时优化](#52-运行时优化)
  - [5.3 GPU 加速](#53-gpu-加速)
- [6 相关文档](#6-相关文档)
  - [6.1 其他实现细节文档](#61-其他实现细节文档)
  - [6.2 架构视角文档](#62-架构视角文档)
  - [6.3 理论文档](#63-理论文档)

---

## 1 概述

**WasmEdge 0.14** 是云原生 WebAssembly 运行时，支持 WASI Preview 2，提供极速启动
（< 1ms）和极轻量（镜像 < 2 MB）的计算单元。

### 1.1 核心特性

- **WASI Preview 2**：标准化系统调用接口
- **极速启动**：冷启动 < 1ms（vs 容器 < 1s，快 1000×）
- **GPU 加速**：支持 GPU 加速推理
- **Kubernetes 集成**：Kubernetes 1.30 双运行时支持

---

## 2 安装

### 2.1 Linux 安装

**使用安装脚本**：

```bash
# 安装 WasmEdge 0.14
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- -v 0.14.0

# 设置环境变量
export PATH=$PATH:$HOME/.wasmedge/bin
```

**使用包管理器**：

```bash
# Ubuntu/Debian
curl -s https://packagecloud.io/install/repositories/wasmedge/wasmedge/script.deb.sh | sudo bash
sudo apt-get install wasmedge

# CentOS/RHEL
curl -s https://packagecloud.io/install/repositories/wasmedge/wasmedge/script.rpm.sh | sudo bash
sudo yum install wasmedge
```

### 2.2 macOS 安装

```bash
# 使用 Homebrew
brew install wasmedge

# 或使用安装脚本
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- -v 0.14.0
```

### 2.3 Docker 安装

```bash
# 拉取 WasmEdge 镜像
docker pull wasmedge/wasmedge:0.14.0

# 运行 Wasm 模块
docker run --rm wasmedge/wasmedge:0.14.0 wasmedge app.wasm
```

### 2.4 验证安装

```bash
# 检查版本
wasmedge --version
# 输出：wasmedge 0.14.0

# 运行测试模块
wasmedge --version
```

---

## 3 基本配置

### 3.1 配置文件

**WasmEdge 配置文件**（`~/.wasmedge/config.toml`）：

```toml
[wasm]
  # 内存限制（MB）
  memory_limit = 256

  # 最大内存页数（64KB per page）
  max_memory_pages = 4096

  # 启用 WASI
  wasi_enabled = true

  # WASI 预览版本
  wasi_preview2 = true

[permissions]
  # 文件系统权限
  read = ["/tmp", "/home"]
  write = ["/tmp"]

  # 网络权限
  network = ["tcp://0.0.0.0:8080"]
```

### 3.2 运行时配置

**命令行选项**：

```bash
# 基本运行
wasmedge app.wasm

# 指定内存限制
wasmedge --memory-limit 512 app.wasm

# 启用 WASI Preview 2
wasmedge --wasm wasi-preview2 app.wasm

# 指定目录权限
wasmedge --dir /tmp:/tmp --dir /home:/home app.wasm

# 指定网络权限
wasmedge --network tcp://0.0.0.0:8080 app.wasm
```

### 3.3 环境变量

```bash
# 设置默认内存限制
export WASMEDGE_MEMORY_LIMIT=512

# 设置日志级别
export WASMEDGE_LOG_LEVEL=info

# 设置插件路径
export WASMEDGE_PLUGIN_PATH=/usr/local/lib/wasmedge
```

---

## 4 Kubernetes 集成

### 4.1 安装 containerd Wasm shim

**Kubernetes 1.30** 支持双运行时（runc + WasmEdge）：

```bash
# 安装 containerd Wasm shim
wget https://github.com/containerd/containerd/releases/download/v2.0.0/containerd-wasm-shim-v2-2.0.0-linux-amd64.tar.gz
tar -xzf containerd-wasm-shim-v2-2.0.0-linux-amd64.tar.gz
sudo mv containerd-wasm-shim-v2 /usr/local/bin/
```

### 4.2 配置 containerd

**containerd 配置**（`/etc/containerd/config.toml`）：

```toml
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
    runtime_type = "io.containerd.runc.v2"
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.wasm]
    runtime_type = "io.containerd.wasm.v2"
```

### 4.3 创建 RuntimeClass

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: wasm
handler: wasm
```

### 4.4 部署 Wasm Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: wasm-pod
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: docker.io/library/wasm-app:latest
      resources:
        limits:
          memory: "128Mi"
```

---

## 5 性能优化

### 5.1 编译优化

**Rust 编译优化**：

```bash
# 启用优化
cargo build --target wasm32-wasi --release

# 启用 LTO（链接时优化）
RUSTFLAGS="-C lto=fat" cargo build --target wasm32-wasi --release

# 减小二进制体积
cargo build --target wasm32-wasi --release -- -C opt-level=z
```

### 5.2 运行时优化

**启用 AOT 编译**：

```bash
# 预编译 Wasm 模块
wasmedge compile app.wasm app.so

# 运行预编译模块（更快）
wasmedge app.so
```

### 5.3 GPU 加速

**启用 GPU 加速**（AI 推理）：

```bash
# 安装 GPU 插件
wasmedge install tensorflow

# 运行 GPU 加速推理
wasmedge --enable-gpu tensorflow.wasm
```

---

## 6 相关文档

### 6.1 其他实现细节文档

- [`wasi-examples.md`](wasi-examples.md) - WASI 接口使用示例
- [`wasm-compilation.md`](wasm-compilation.md) - Wasm 编译示例
- [`kubernetes-integration.md`](kubernetes-integration.md) - Kubernetes 集成

### 6.2 架构视角文档

- [`../../02-views/10-quick-views/webassembly-view.md`](../../02-views/10-quick-views/webassembly-view.md) -
  WebAssembly 架构视角

### 6.3 理论文档

- [`../../00-theory/02-induction-proof/psi5-wasm.md`](../../00-theory/02-induction-proof/psi5-wasm.md) -
  Ψ₅：第五次归纳映射

---

**更新时间**：2025-11-05 **版本**：v1.0 **参考**：WasmEdge 0.14 官方文档
