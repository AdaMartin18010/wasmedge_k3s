# QEMU 配置示例

## 📑 目录

- [1. 概述](#1-概述)
- [2. QEMU 基本命令](#2-qemu-基本命令)
- [3. QEMU 设备配置](#3-qemu-设备配置)
- [4. QEMU 性能优化](#4-qemu-性能优化)
- [5. QEMU 与 KVM 集成](#5-qemu-与-kvm-集成)
- [6. 相关文档](#6-相关文档)

---

## 1. 概述

本文档提供 **QEMU（Quick Emulator）的实际配置示例**，展示如何配置和使用 QEMU 创
建和管理虚拟机。

### 1.1 理论基础

QEMU 配置基于以下理论论证：

- **公理 A1（冯·诺依曼等价）**：任何图灵机可计算函数均可在虚拟化环境中实现
- **归纳映射 Ψ₁（虚拟化层）**：将物理硬件抽象为 VM 资源池
- **状态空间压缩**：通过虚拟化实现状态空间压缩

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2. QEMU 基本命令

### 2.1 创建虚拟机

```bash
# 创建磁盘镜像
qemu-img create -f qcow2 myvm.qcow2 20G

# 启动虚拟机（使用 ISO 安装）
qemu-system-x86_64 \
  -enable-kvm \
  -cpu host \
  -m 2048 \
  -smp 2 \
  -drive file=myvm.qcow2,format=qcow2 \
  -cdrom ubuntu-22.04.iso \
  -boot d \
  -vnc :1
```

### 2.2 网络配置

```bash
# 使用用户模式网络（NAT）
qemu-system-x86_64 \
  -enable-kvm \
  -netdev user,id=net0 \
  -device virtio-net,netdev=net0 \
  ...

# 使用桥接网络
qemu-system-x86_64 \
  -enable-kvm \
  -netdev bridge,id=net0,br=br0 \
  -device virtio-net,netdev=net0 \
  ...

# 使用 tap 设备
qemu-system-x86_64 \
  -enable-kvm \
  -netdev tap,id=net0,ifname=tap0,script=no,downscript=no \
  -device virtio-net,netdev=net0 \
  ...
```

### 2.3 存储配置

```bash
# 使用 virtio-blk（性能最佳）
qemu-system-x86_64 \
  -enable-kvm \
  -drive file=myvm.qcow2,format=qcow2,if=virtio \
  ...

# 使用 SATA
qemu-system-x86_64 \
  -enable-kvm \
  -drive file=myvm.qcow2,format=qcow2,if=ide \
  ...

# 使用 SCSI
qemu-system-x86_64 \
  -enable-kvm \
  -drive file=myvm.qcow2,format=qcow2,if=scsi \
  ...
```

---

## 3. QEMU 设备配置

### 3.1 CPU 配置

```bash
# CPU 类型和数量
qemu-system-x86_64 \
  -enable-kvm \
  -cpu host \
  -smp sockets=1,cores=2,threads=1 \
  ...

# CPU 特性
qemu-system-x86_64 \
  -enable-kvm \
  -cpu host,+ssse3,+sse4.1,+sse4.2 \
  ...
```

### 3.2 内存配置

```bash
# 基础内存配置
qemu-system-x86_64 \
  -enable-kvm \
  -m 2048 \
  ...

# 大页内存
qemu-system-x86_64 \
  -enable-kvm \
  -m 2048,slots=2,maxmem=4G \
  -object memory-backend-file,id=mem0,size=2048M,mem-path=/dev/hugepages \
  -numa node,memdev=mem0 \
  ...
```

### 3.3 图形配置

```bash
# VNC 配置
qemu-system-x86_64 \
  -enable-kvm \
  -vnc :1 \
  ...

# SPICE 配置
qemu-system-x86_64 \
  -enable-kvm \
  -spice port=5900,addr=0.0.0.0,disable-ticketing \
  -device virtio-serial-pci \
  -device virtserialport,chardev=spicechannel0,name=com.redhat.spice.0 \
  -chardev spicevmc,id=spicechannel0,name=vdagent \
  ...

# 无图形模式
qemu-system-x86_64 \
  -enable-kvm \
  -nographic \
  -serial mon:stdio \
  ...
```

---

## 4. QEMU 性能优化

### 4.1 CPU 性能优化

```bash
# 使用 KVM 加速
qemu-system-x86_64 \
  -enable-kvm \
  -cpu host \
  -smp cores=4,threads=1 \
  ...

# CPU 亲和性
qemu-system-x86_64 \
  -enable-kvm \
  -numa node,nodeid=0,cpus=0-1 \
  -numa node,nodeid=1,cpus=2-3 \
  ...
```

### 4.2 网络性能优化

```bash
# 使用 virtio-net 和多队列
qemu-system-x86_64 \
  -enable-kvm \
  -netdev tap,id=net0,queues=4 \
  -device virtio-net-pci,netdev=net0,mq=on,vectors=8 \
  ...
```

### 4.3 存储性能优化

```bash
# 使用 virtio-blk 和缓存模式
qemu-system-x86_64 \
  -enable-kvm \
  -drive file=myvm.qcow2,format=qcow2,if=virtio,cache=none,aio=native \
  ...

# 使用 raw 格式（性能最佳）
qemu-img create -f raw myvm.raw 20G
qemu-system-x86_64 \
  -enable-kvm \
  -drive file=myvm.raw,format=raw,if=virtio,cache=none,aio=native \
  ...
```

---

## 5. QEMU 与 KVM 集成

### 5.1 使用 KVM 加速

```bash
# 检查 KVM 支持
lsmod | grep kvm
ls -l /dev/kvm

# 使用 KVM 加速
qemu-system-x86_64 \
  -enable-kvm \
  -machine accel=kvm \
  ...
```

### 5.2 libvirt 集成

```bash
# 使用 virsh 管理 QEMU/KVM 虚拟机
virsh list --all
virsh start myvm
virsh shutdown myvm
virsh destroy myvm
virsh console myvm
```

### 5.3 QEMU Monitor Protocol (QMP)

```bash
# 启动 QMP 服务器
qemu-system-x86_64 \
  -enable-kvm \
  -qmp unix:/tmp/qmp.sock,server,nowait \
  ...

# 使用 QMP 命令
echo '{"execute":"qmp_capabilities"}' | socat - UNIX-CONNECT:/tmp/qmp.sock
echo '{"execute":"query-status"}' | socat - UNIX-CONNECT:/tmp/qmp.sock
```

---

## 6. 相关文档

### 6.1 理论论证

- **`../../00-theory/02-induction-proof/psi1-virtualization.md`** - 虚拟化层归纳
  映射
- **`../../00-theory/01-axioms/A1-von-neumann.md`** - 冯·诺依曼等价公理

### 6.2 架构视角

- **`../../01-views/virtualization-view.md`** - 虚拟化架构视角

### 6.3 技术文档

- **`../../../TECHNICAL/29-isolation-stack/isolation-stack.md`** - 隔离技术栈文
  档

---

**更新时间**：2025-11-04 **版本**：v1.0 **状态**：✅ 基础示例已创建
