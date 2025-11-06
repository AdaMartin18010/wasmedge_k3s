# gVisor 配置示例

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 理论基础](#11-理论基础)
- [2. gVisor 安装](#2-gvisor-安装)
  - [2.1 下载 runsc](#21-下载-runsc)
  - [2.2 安装 containerd shim](#22-安装-containerd-shim)
  - [2.3 验证安装](#23-验证安装)
- [3. runsc 配置](#3-runsc-配置)
  - [3.1 runsc 配置文件](#31-runsc-配置文件)
  - [3.2 性能优化配置](#32-性能优化配置)
- [4. Docker 集成](#4-docker-集成)
  - [4.1 配置 Docker 使用 runsc](#41-配置-docker-使用-runsc)
  - [4.2 使用 gVisor 运行容器](#42-使用-gvisor-运行容器)
  - [4.3 Docker Compose 配置](#43-docker-compose-配置)
- [5. Kubernetes 集成](#5-kubernetes-集成)
  - [5.1 创建 RuntimeClass](#51-创建-runtimeclass)
  - [5.2 Pod 使用 gVisor RuntimeClass](#52-pod-使用-gvisor-runtimeclass)
  - [5.3 containerd 配置](#53-containerd-配置)
  - [5.4 runsc.toml 配置](#54-runsctoml-配置)
- [6. 相关文档](#6-相关文档)
  - [6.1 理论论证](#61-理论论证)
  - [6.2 架构视角](#62-架构视角)
  - [6.3 技术文档](#63-技术文档)

---

## 1. 概述

本文档提供 **gVisor 的实际配置示例**，展示如何配置和使用 gVisor 实现沙盒隔离。

### 1.1 理论基础

gVisor 配置基于以下理论论证：

- **公理 A2（OS 资源封闭）**：进程、内存、文件、网络四大命名空间可完全封闭
- **归纳映射 Ψ₃（沙盒化层）**：对容器内部进程进一步隔离
- **引理 L2（能力闭包）**：沙盒安全边界 = 最小能力闭包，|Capability| ≤ 35

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2. gVisor 安装

### 2.1 下载 runsc

```bash
# 下载最新版本的 runsc
wget https://storage.googleapis.com/gvisor/releases/release/latest/x86_64/runsc
chmod +x runsc
sudo mv runsc /usr/local/bin
```

### 2.2 安装 containerd shim

```bash
# 安装 containerd gVisor shim
sudo apt-get install -y golang-go
go install github.com/google/gvisor-containerd-shim/cmd/containerd-shim-runsc-v1@latest
```

### 2.3 验证安装

```bash
# 验证 runsc 安装
runsc --version

# 验证 gVisor 是否可用
runsc do echo "gVisor is working"
```

---

## 3. runsc 配置

### 3.1 runsc 配置文件

```json
{
  "root": "/var/run/gvisor",
  "log_dir": "/var/log/gvisor",
  "debug": false,
  "log_format": "text",
  "platform": "ptrace",
  "file_access": "proxy",
  "network": "sandbox"
}
```

### 3.2 性能优化配置

```json
{
  "root": "/var/run/gvisor",
  "platform": "kvm",
  "file_access": "direct",
  "network": "host"
}
```

---

## 4. Docker 集成

### 4.1 配置 Docker 使用 runsc

```bash
# 注册 runsc 运行时
sudo runsc install

# 配置 Docker daemon.json
sudo tee /etc/docker/daemon.json <<EOF
{
  "runtimes": {
    "runsc": {
      "path": "/usr/local/bin/runsc",
      "runtimeArgs": [
        "--platform=ptrace"
      ]
    }
  }
}
EOF

# 重启 Docker
sudo systemctl restart docker
```

### 4.2 使用 gVisor 运行容器

```bash
# 使用 runsc 运行时运行容器
docker run --runtime=runsc -d \
  --name myapp \
  myapp:v1.0

# 使用特定平台
docker run --runtime=runsc \
  --runtime-opt=--platform=kvm \
  -d --name myapp \
  myapp:v1.0
```

### 4.3 Docker Compose 配置

```yaml
version: "3.8"

services:
  app:
    image: myapp:v1.0
    runtime: runsc
    runtime_options:
      - --platform=ptrace
```

---

## 5. Kubernetes 集成

### 5.1 创建 RuntimeClass

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
```

### 5.2 Pod 使用 gVisor RuntimeClass

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  runtimeClassName: gvisor
  containers:
    - name: app
      image: myapp:v1.0
```

### 5.3 containerd 配置

```toml
# /etc/containerd/config.toml
version = 2

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc]
  runtime_type = "io.containerd.runsc.v1"
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc.options]
    TypeUrl = "io.containerd.runsc.v1.options"
    ConfigPath = "/etc/containerd/runsc.toml"
```

### 5.4 runsc.toml 配置

```toml
# /etc/containerd/runsc.toml
root = "/var/run/gvisor"
log_dir = "/var/log/gvisor"
debug = false
log_format = "text"
platform = "ptrace"
file_access = "proxy"
network = "sandbox"
```

---

## 6. 相关文档

### 6.1 理论论证

- **`../../00-theory/02-induction-proof/psi3-sandboxing.md`** - 沙盒化层归纳映射
- **`../../00-theory/01-axioms/A2-os-resource.md`** - OS 资源封闭公理
- **`../../00-theory/05-lemmas-theorems/L2-capability-closure.md`** - 能力闭包引
  理

### 6.2 架构视角

- **`../../01-views/sandboxing-view.md`** - 沙盒化架构视角

### 6.3 技术文档

- **`../../../TECHNICAL/29-isolation-stack/isolation-stack.md`** - 隔离技术栈文
  档

---

**更新时间**：2025-11-04 **版本**：v1.0 **状态**：✅ 基础示例已创建
