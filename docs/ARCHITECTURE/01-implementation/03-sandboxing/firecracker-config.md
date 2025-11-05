# Firecracker 配置示例

## 📑 目录

- [1. 概述](#1-概述)
- [2. Firecracker 安装](#2-firecracker-安装)
- [3. MicroVM 配置](#3-microvm-配置)
- [4. Jailer 配置](#4-jailer-配置)
- [5. Kubernetes 集成](#5-kubernetes-集成)
- [6. 相关文档](#6-相关文档)

---

## 1. 概述

本文档提供 **Firecracker 的实际配置示例**，展示如何配置和使用 Firecracker 创建轻
量级 MicroVM。

### 1.1 理论基础

Firecracker 配置基于以下理论论证：

- **公理 A1（冯·诺依曼等价）**：任何图灵机可计算函数均可在虚拟化环境中实现
- **归纳映射 Ψ₁（虚拟化层）**：将物理硬件抽象为 VM 资源池
- **状态空间压缩**：通过虚拟化实现状态空间压缩

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2. Firecracker 安装

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

## 3. MicroVM 配置

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

## 4. Jailer 配置

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

## 5. Kubernetes 集成

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

## 6. 相关文档

### 6.1 理论论证

- **`../../00-theory/02-induction-proof/psi1-virtualization.md`** - 虚拟化层归纳
  映射
- **`../../00-theory/01-axioms/A1-von-neumann.md`** - 冯·诺依曼等价公理

### 6.2 架构视角

- **`../../01-views/virtualization-view.md`** - 虚拟化架构视角
- **`../../01-views/sandboxing-view.md`** - 沙盒化架构视角

### 6.3 技术文档

- **`../../../TECHNICAL/29-isolation-stack/isolation-stack.md`** - 隔离技术栈文
  档

---

**更新时间**：2025-11-04 **版本**：v1.0 **状态**：✅ 基础示例已创建
