# Firecracker 配置示例

## 📑 目录

- [Firecracker 配置示例](#firecracker-配置示例)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 理论基础](#11-理论基础)
  - [2 Firecracker 安装](#2-firecracker-安装)
    - [2.1 下载 Firecracker](#21-下载-firecracker)
    - [2.2 验证安装](#22-验证安装)
  - [3 MicroVM 配置](#3-microvm-配置)
    - [3.1 创建根文件系统](#31-创建根文件系统)
    - [3.2 启动 MicroVM](#32-启动-microvm)
  - [4 Jailer 配置](#4-jailer-配置)
    - [4.1 使用 Jailer 启动 MicroVM](#41-使用-jailer-启动-microvm)
    - [4.2 Jailer 配置文件](#42-jailer-配置文件)
  - [5 Kubernetes 集成](#5-kubernetes-集成)
    - [5.1 安装 containerd-firecracker-runtime](#51-安装-containerd-firecracker-runtime)
    - [5.2 containerd 配置](#52-containerd-配置)
    - [5.3 Firecracker RuntimeClass](#53-firecracker-runtimeclass)
    - [5.4 Pod 使用 Firecracker](#54-pod-使用-firecracker)
  - [6 相关文档](#6-相关文档)
    - [6.1 理论论证](#61-理论论证)
    - [6.2 架构视角](#62-架构视角)
    - [6.3 技术文档](#63-技术文档)
  - [7 2025 年最新实践](#7-2025-年最新实践)
    - [7.1 Firecracker 1.7+ 新特性（2025）](#71-firecracker-17-新特性2025)
    - [7.2 containerd 2.0+ Firecracker 集成（2025）](#72-containerd-20-firecracker-集成2025)
    - [7.3 Serverless 场景优化（2025）](#73-serverless-场景优化2025)
  - [8 实际应用案例](#8-实际应用案例)
    - [案例 1：Serverless 函数执行](#案例-1serverless-函数执行)
    - [案例 2：多租户 VM 隔离](#案例-2多租户-vm-隔离)
    - [案例 3：边缘计算 VM 部署](#案例-3边缘计算-vm-部署)

---

## 1 概述

本文档提供 **Firecracker 的实际配置示例**，展示如何配置和使用 Firecracker 创建轻
量级 MicroVM。

### 1.1 理论基础

Firecracker 配置基于以下理论论证：

- **公理 A1（冯·诺依曼等价）**：任何图灵机可计算函数均可在虚拟化环境中实现
- **归纳映射 Ψ₁（虚拟化层）**：将物理硬件抽象为 VM 资源池
- **状态空间压缩**：通过虚拟化实现状态空间压缩

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2 Firecracker 安装

### 2.1 下载 Firecracker

```bash
# 下载最新版本的 Firecracker
wget https://github.com/firecracker-microvm/firecracker/releases/download/v1.7.0/firecracker-v1.7.0-x86_64.tgz
tar -xzf firecracker-v1.7.0-x86_64.tgz
sudo mv release-*/firecracker-*-x86_64 /usr/local/bin/firecracker
sudo mv release-*/jailer-*-x86_64 /usr/local/bin/jailer
sudo chmod +x /usr/local/bin/firecracker
sudo chmod +x /usr/local/bin/jailer
```

### 2.2 验证安装

```bash
# 验证 Firecracker 安装
firecracker --version

# 验证 Jailer 安装
jailer --version
```

---

## 3 MicroVM 配置

### 3.1 创建根文件系统

```bash
# 下载 Linux 内核镜像
wget https://s3.amazonaws.com/spec.ccfc.min/img/quickstart_guide/x86_64/kernels/vmlinux.bin

# 创建根文件系统镜像
dd if=/dev/zero of=rootfs.ext4 bs=1M count=100
mkfs.ext4 rootfs.ext4
```

### 3.2 启动 MicroVM

```bash
# 启动 Firecracker API 服务器
firecracker --api-sock /tmp/firecracker.sock &

# 配置 VM
curl --unix-socket /tmp/firecracker.sock -i \
  -X PUT 'http://localhost/boot-source' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "kernel_image_path": "./vmlinux.bin",
    "boot_args": "console=ttyS0 reboot=k panic=1 pci=off"
  }'

curl --unix-socket /tmp/firecracker.sock -i \
  -X PUT 'http://localhost/drives/rootfs' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "drive_id": "rootfs",
    "path_on_host": "./rootfs.ext4",
    "is_root_device": true,
    "is_read_only": false
  }'

curl --unix-socket /tmp/firecracker.sock -i \
  -X PUT 'http://localhost/machine-config' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "vcpu_count": 2,
    "mem_size_mib": 1024,
    "ht_enabled": false
  }'

# 启动 VM
curl --unix-socket /tmp/firecracker.sock -i \
  -X PUT 'http://localhost/actions' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "action_type": "InstanceStart"
  }'
```

---

## 4 Jailer 配置

### 4.1 使用 Jailer 启动 MicroVM

```bash
# 创建 Jailer 目录结构
sudo mkdir -p /srv/jailer/firecracker/1.7.0/root

# 使用 Jailer 启动 MicroVM
sudo jailer \
  --id=myvm \
  --exec-file=/usr/local/bin/firecracker \
  --uid=1000 \
  --gid=1000 \
  --daemonize \
  --chroot-base-dir=/srv/jailer \
  -- \
  --api-sock=/api.sock \
  --config-file=/config.json
```

### 4.2 Jailer 配置文件

```json
{
  "boot-source": {
    "kernel_image_path": "/vmlinux.bin",
    "boot_args": "console=ttyS0 reboot=k panic=1 pci=off"
  },
  "drives": [
    {
      "drive_id": "rootfs",
      "path_on_host": "/rootfs.ext4",
      "is_root_device": true,
      "is_read_only": false
    }
  ],
  "machine-config": {
    "vcpu_count": 2,
    "mem_size_mib": 1024,
    "ht_enabled": false
  }
}
```

---

## 5 Kubernetes 集成

### 5.1 安装 containerd-firecracker-runtime

```bash
# 安装 containerd-firecracker-runtime
git clone https://github.com/firecracker-microvm/fire containerd-firecracker-runtime
cd containerd-firecracker-runtime
make
sudo make install
```

### 5.2 containerd 配置

```toml
# /etc/containerd/config.toml
version = 2

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.firecracker]
  runtime_type = "io.containerd.firecracker.v1"
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.firecracker.options]
    ConfigPath = "/etc/containerd/firecracker-runtime.json"
```

### 5.3 Firecracker RuntimeClass

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: firecracker
handler: firecracker
```

### 5.4 Pod 使用 Firecracker

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  runtimeClassName: firecracker
  containers:
    - name: app
      image: myapp:v1.0
      resources:
        requests:
          memory: "512Mi"
          cpu: "1"
        limits:
          memory: "1Gi"
          cpu: "2"
```

---

## 6 相关文档

### 6.1 理论论证

- **`../../00-theory/02-induction-proof/psi1-virtualization.md`** - 虚拟化层归纳
  映射
- **`../../00-theory/01-axioms/A1-von-neumann.md`** - 冯·诺依曼等价公理

### 6.2 架构视角

- **`../../02-views/10-quick-views/virtualization-view.md`** - 虚拟化架构视角
- **`../../02-views/10-quick-views/sandboxing-view.md`** - 沙盒化架构视角

### 6.3 技术文档

- **`../../../TECHNICAL/08-architecture-analysis/isolation-stack/isolation-stack.md`** -
  隔离技术栈文档

## 7 2025 年最新实践

### 7.1 Firecracker 1.7+ 新特性（2025）

**最新版本**：Firecracker 1.7+（2025 年）

**新特性**：

- **性能优化**：减少 VM 启动时间（< 100ms）
- **内存优化**：减少内存占用
- **网络性能提升**：改进的网络性能

**安装最新版本**：

```bash
# 下载 Firecracker 1.7
wget https://github.com/firecracker-microvm/firecracker/releases/download/v1.7.0/firecracker-v1.7.0-x86_64.tgz
tar -xzf firecracker-v1.7.0-x86_64.tgz
sudo mv release-*/firecracker-* /usr/local/bin/
```

### 7.2 containerd 2.0+ Firecracker 集成（2025）

**containerd 2.0+ 新特性**：

- **统一运行时管理**：更好的 Firecracker 运行时管理
- **性能优化**：减少 VM 启动开销
- **资源管理**：改进的资源限制

**配置示例**：

```toml
# /etc/containerd/config.toml
version = 2

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.firecracker]
  runtime_type = "io.containerd.firecracker.v1"
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.firecracker.options]
    ConfigPath = "/etc/containerd/firecracker-runtime.json"
```

### 7.3 Serverless 场景优化（2025）

**2025 年趋势**：Firecracker 在 Serverless 场景的广泛应用

**优势**：

- **快速启动**：VM 启动时间 < 100ms
- **资源隔离**：VM 级别的隔离
- **资源效率**：低内存占用

**配置示例**：

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: firecracker
handler: firecracker
overhead:
  podFixed:
    cpu: "50m"
    memory: "80Mi"
```

## 8 实际应用案例

### 案例 1：Serverless 函数执行

**场景**：使用 Firecracker 运行 Serverless 函数

**实现方案**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: serverless-function
spec:
  runtimeClassName: firecracker
  containers:
  - name: function
    image: function:latest
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
      limits:
        cpu: "500m"
        memory: "256Mi"
```

**效果**：

- 快速启动：函数启动时间 < 100ms
- 资源隔离：VM 级别的隔离
- 资源效率：低资源占用

### 案例 2：多租户 VM 隔离

**场景**：在多租户环境中使用 Firecracker 提供 VM 级别隔离

**实现方案**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: tenant-vm
  namespace: tenant-a
spec:
  runtimeClassName: firecracker
  containers:
  - name: app
    image: app:latest
    resources:
      requests:
        cpu: "1"
        memory: "512Mi"
      limits:
        cpu: "2"
        memory: "1Gi"
```

**效果**：

- VM 隔离：每个租户有独立的 VM
- 安全隔离：VM 级别的安全隔离
- 性能稳定：稳定的性能表现

### 案例 3：边缘计算 VM 部署

**场景**：在边缘节点部署轻量级 VM

**实现方案**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: edge-vm
spec:
  runtimeClassName: firecracker
  nodeSelector:
    node-type: edge
  containers:
  - name: app
    image: edge-app:latest
    resources:
      requests:
        cpu: "500m"
        memory: "256Mi"
      limits:
        cpu: "1"
        memory: "512Mi"
```

**效果**：

- 快速启动：适合边缘计算场景
- 资源效率：低资源占用
- 安全隔离：VM 级别的隔离

---

**更新时间**：2025-11-15 **版本**：v1.1 **状态**：✅ 包含 2025 年最新实践
