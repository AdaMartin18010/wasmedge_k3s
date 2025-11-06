# KVM 配置示例

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 理论基础](#11-理论基础)
- [2. KVM 安装与检查](#2-kvm-安装与检查)
  - [2.1 KVM 安装](#21-kvm-安装)
  - [2.2 检查 CPU 虚拟化支持](#22-检查-cpu-虚拟化支持)
  - [2.3 用户权限配置](#23-用户权限配置)
- [3. libvirt 配置](#3-libvirt-配置)
  - [3.1 libvirt 默认网络配置](#31-libvirt-默认网络配置)
  - [3.2 桥接网络配置](#32-桥接网络配置)
  - [3.3 存储池配置](#33-存储池配置)
- [4. KVM 虚拟机创建](#4-kvm-虚拟机创建)
  - [4.1 使用 virt-install 创建虚拟机](#41-使用-virt-install-创建虚拟机)
  - [4.2 使用 virt-manager 创建虚拟机](#42-使用-virt-manager-创建虚拟机)
  - [4.3 虚拟机 XML 配置示例](#43-虚拟机-xml-配置示例)
- [5. KVM 性能优化](#5-kvm-性能优化)
  - [5.1 CPU 性能优化](#51-cpu-性能优化)
  - [5.2 内存性能优化](#52-内存性能优化)
  - [5.3 网络性能优化](#53-网络性能优化)
  - [5.4 存储性能优化](#54-存储性能优化)
- [6. 相关文档](#6-相关文档)
  - [6.1 理论论证](#61-理论论证)
  - [6.2 架构视角](#62-架构视角)
  - [6.3 技术文档](#63-技术文档)

---

## 1. 概述

本文档提供 **KVM（Kernel-based Virtual Machine）的实际配置示例**，展示如何配置和
使用 KVM 虚拟化。

### 1.1 理论基础

KVM 配置基于以下理论论证：

- **公理 A1（冯·诺依曼等价）**：任何图灵机可计算函数均可在虚拟化环境中实现
- **归纳映射 Ψ₁（虚拟化层）**：将物理硬件抽象为 VM 资源池
- **状态空间压缩**：通过虚拟化实现状态空间压缩

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2. KVM 安装与检查

### 2.1 KVM 安装

```bash
# Ubuntu/Debian 安装 KVM
sudo apt update
sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager

# CentOS/RHEL 安装 KVM
sudo yum install -y qemu-kvm libvirt libvirt-daemon-system libvirt-clients bridge-utils virt-manager

# 启动 libvirt 服务
sudo systemctl enable libvirtd
sudo systemctl start libvirtd
```

### 2.2 检查 CPU 虚拟化支持

```bash
# 检查 Intel VT-x 支持
grep -E 'vmx|svm' /proc/cpuinfo

# 检查 KVM 模块
lsmod | grep kvm

# 检查 /dev/kvm 设备
ls -l /dev/kvm

# 检查虚拟化功能
virt-host-validate
```

### 2.3 用户权限配置

```bash
# 将用户添加到 libvirt 组
sudo usermod -aG libvirt $USER
sudo usermod -aG kvm $USER

# 重新登录使权限生效
```

---

## 3. libvirt 配置

### 3.1 libvirt 默认网络配置

```xml
<!-- /etc/libvirt/qemu/networks/default.xml -->
<network>
  <name>default</name>
  <uuid>12345678-1234-1234-1234-123456789abc</uuid>
  <forward mode='nat'>
    <nat>
      <port start='1024' end='65535'/>
    </nat>
  </forward>
  <bridge name='virbr0' stp='on' delay='0'/>
  <ip address='192.168.122.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.122.2' end='192.168.122.254'/>
    </dhcp>
  </ip>
</network>
```

### 3.2 桥接网络配置

```bash
# 创建桥接网络
cat > /tmp/bridge.xml <<EOF
<network>
  <name>bridge-net</name>
  <forward mode='bridge'/>
  <bridge name='br0'/>
</network>
EOF

# 定义并启动桥接网络
virsh net-define /tmp/bridge.xml
virsh net-start bridge-net
virsh net-autostart bridge-net
```

### 3.3 存储池配置

```bash
# 创建目录存储池
virsh pool-define-as --name default --type dir --target /var/lib/libvirt/images
virsh pool-build default
virsh pool-start default
virsh pool-autostart default
```

---

## 4. KVM 虚拟机创建

### 4.1 使用 virt-install 创建虚拟机

```bash
# 创建 Ubuntu 虚拟机
virt-install \
  --name ubuntu-vm \
  --ram 2048 \
  --vcpus 2 \
  --disk path=/var/lib/libvirt/images/ubuntu-vm.qcow2,size=20 \
  --cdrom /path/to/ubuntu-22.04.iso \
  --network bridge=virbr0 \
  --graphics vnc,listen=0.0.0.0 \
  --os-type linux \
  --os-variant ubuntu22.04 \
  --virt-type kvm
```

### 4.2 使用 virt-manager 创建虚拟机

```bash
# 启动 virt-manager GUI
virt-manager

# 或使用命令行创建虚拟机定义
virsh define /path/to/vm.xml
```

### 4.3 虚拟机 XML 配置示例

```xml
<!-- /etc/libvirt/qemu/myvm.xml -->
<domain type='kvm'>
  <name>myvm</name>
  <uuid>12345678-1234-1234-1234-123456789abc</uuid>
  <memory unit='KiB'>2097152</memory>
  <currentMemory unit='KiB'>2097152</currentMemory>
  <vcpu placement='static'>2</vcpu>
  <os>
    <type arch='x86_64' machine='pc-i440fx-2.11'>hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <cpu mode='host-passthrough'/>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/var/lib/libvirt/images/myvm.qcow2'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='bridge'>
      <mac address='52:54:00:12:34:56'/>
      <source bridge='virbr0'/>
      <model type='virtio'/>
    </interface>
    <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0'/>
  </devices>
</domain>
```

---

## 5. KVM 性能优化

### 5.1 CPU 性能优化

```xml
<!-- CPU 配置优化 -->
<cpu mode='host-passthrough'>
  <topology sockets='1' cores='2' threads='1'/>
  <cache mode='passthrough'/>
</cpu>

<!-- CPU 亲和性配置 -->
<cputune>
  <vcpupin vcpu='0' cpuset='0'/>
  <vcpupin vcpu='1' cpuset='1'/>
</cputune>
```

### 5.2 内存性能优化

```xml
<!-- 大页内存配置 -->
<memory unit='KiB'>2097152</memory>
<memoryBacking>
  <hugepages>
    <page size='2048' unit='KiB'/>
  </hugepages>
</memoryBacking>
```

### 5.3 网络性能优化

```xml
<!-- virtio-net 配置 -->
<interface type='bridge'>
  <source bridge='br0'/>
  <model type='virtio'/>
  <driver name='vhost'/>
</interface>
```

### 5.4 存储性能优化

```xml
<!-- virtio-blk 配置 -->
<disk type='file' device='disk'>
  <driver name='qemu' type='qcow2' cache='none' io='native'/>
  <source file='/var/lib/libvirt/images/myvm.qcow2'/>
  <target dev='vda' bus='virtio'/>
</disk>
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
