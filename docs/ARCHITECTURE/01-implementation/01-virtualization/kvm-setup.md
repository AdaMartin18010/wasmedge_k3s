# KVM 配置示例

## 📑 目录

- [KVM 配置示例](#kvm-配置示例)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 理论基础](#11-理论基础)
  - [2 KVM 安装与检查](#2-kvm-安装与检查)
    - [2.1 KVM 安装](#21-kvm-安装)
    - [2.2 检查 CPU 虚拟化支持](#22-检查-cpu-虚拟化支持)
    - [2.3 用户权限配置](#23-用户权限配置)
  - [3 libvirt 配置](#3-libvirt-配置)
    - [3.1 libvirt 默认网络配置](#31-libvirt-默认网络配置)
    - [3.2 桥接网络配置](#32-桥接网络配置)
    - [3.3 存储池配置](#33-存储池配置)
  - [4 KVM 虚拟机创建](#4-kvm-虚拟机创建)
    - [4.1 使用 virt-install 创建虚拟机](#41-使用-virt-install-创建虚拟机)
    - [4.2 使用 virt-manager 创建虚拟机](#42-使用-virt-manager-创建虚拟机)
    - [4.3 虚拟机 XML 配置示例](#43-虚拟机-xml-配置示例)
  - [5 KVM 性能优化](#5-kvm-性能优化)
    - [5.1 CPU 性能优化](#51-cpu-性能优化)
    - [5.2 内存性能优化](#52-内存性能优化)
    - [5.3 网络性能优化](#53-网络性能优化)
    - [5.4 存储性能优化](#54-存储性能优化)
  - [6 相关文档](#6-相关文档)
    - [6.1 理论论证](#61-理论论证)
    - [6.2 架构视角](#62-架构视角)
    - [6.3 技术文档](#63-技术文档)
  - [7 2025 年最新实践](#7-2025-年最新实践)
    - [7.1 KVM 性能优化（2025）](#71-kvm-性能优化2025)
    - [7.2 容器与 VM 混合部署（2025）](#72-容器与-vm-混合部署2025)
    - [7.3 边缘计算 KVM 部署（2025）](#73-边缘计算-kvm-部署2025)
  - [8 实际应用案例](#8-实际应用案例)
    - [案例 1：云原生 VM 部署](#案例-1云原生-vm-部署)
    - [案例 2：安全隔离 VM 部署](#案例-2安全隔离-vm-部署)
    - [案例 3：高性能计算 VM 部署](#案例-3高性能计算-vm-部署)

---

## 1 概述

本文档提供 **KVM（Kernel-based Virtual Machine）的实际配置示例**，展示如何配置和
使用 KVM 虚拟化。

### 1.1 理论基础

KVM 配置基于以下理论论证：

- **公理 A1（冯·诺依曼等价）**：任何图灵机可计算函数均可在虚拟化环境中实现
- **归纳映射 Ψ₁（虚拟化层）**：将物理硬件抽象为 VM 资源池
- **状态空间压缩**：通过虚拟化实现状态空间压缩

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2 KVM 安装与检查

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

## 3 libvirt 配置

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

## 4 KVM 虚拟机创建

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

## 5 KVM 性能优化

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

## 6 相关文档

### 6.1 理论论证

- **`../../00-theory/02-induction-proof/psi1-virtualization.md`** - 虚拟化层归纳
  映射
- **`../../00-theory/01-axioms/A1-von-neumann.md`** - 冯·诺依曼等价公理

### 6.2 架构视角

- **`../../02-views/10-quick-views/virtualization-view.md`** - 虚拟化架构视角

### 6.3 技术文档

- **`../../../TECHNICAL/08-architecture-analysis/isolation-stack/isolation-stack.md`** -
  隔离技术栈文档

## 7 2025 年最新实践

### 7.1 KVM 性能优化（2025）

**最新内核版本**：Linux 6.1+（2025 年）

**新特性**：

- **嵌套虚拟化增强**：更好的嵌套虚拟化支持
- **IO 虚拟化优化**：virtio 性能提升
- **内存虚拟化优化**：EPT/NPT 性能提升

**性能提升配置**：

```bash
# 启用 KVM 性能优化
echo 1 > /sys/module/kvm/parameters/allow_unsafe_assigned_interrupts
echo 1 > /sys/module/kvm_intel/parameters/nested

# 配置 CPU 特性
virsh cpu-baseline /usr/share/libvirt/cpu_map.xml
```

### 7.2 容器与 VM 混合部署（2025）

**2025 年趋势**：容器和 VM 混合部署

**Kata Containers 2.0+**：

- **轻量级 VM**：每个容器运行在轻量级 VM 中
- **KVM 支持**：基于 KVM 构建
- **性能优化**：接近容器的性能

**配置示例**：

```yaml
# Kubernetes RuntimeClass 配置
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: kata
handler: kata
overhead:
  podFixed:
    cpu: "100m"
    memory: "160Mi"
```

### 7.3 边缘计算 KVM 部署（2025）

**边缘 KVM 部署**：

- **轻量级 Hypervisor**：适合边缘设备的 KVM 配置
- **资源优化**：最小化资源占用
- **快速启动**：优化 VM 启动时间

**配置示例**：

```bash
# 边缘 KVM 配置
qemu-system-x86_64 \
  -enable-kvm \
  -cpu host \
  -m 512M \
  -smp 2 \
  -drive file=vm.img,format=qcow2 \
  -netdev user,id=net0 \
  -device virtio-net-pci,netdev=net0 \
  -nographic
```

## 8 实际应用案例

### 案例 1：云原生 VM 部署

**场景**：在 Kubernetes 中部署 VM 工作负载

**实现方案**：

```yaml
# 使用 KubeVirt 部署 VM
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: myvm
spec:
  running: true
  template:
    spec:
      domain:
        devices:
          disks:
          - name: disk0
            disk:
              bus: virtio
        resources:
          requests:
            memory: 1Gi
            cpu: 1
      volumes:
      - name: disk0
        containerDisk:
          image: myvm:latest
```

**效果**：

- 统一管理：VM 和容器统一管理
- 资源隔离：VM 提供更强的隔离
- 灵活部署：支持混合部署

### 案例 2：安全隔离 VM 部署

**场景**：需要强安全隔离的工作负载

**实现方案**：

```bash
# 使用 Kata Containers 部署
# 每个容器运行在独立的轻量级 VM 中
kubectl run secure-app --image=nginx:latest \
  --runtimeclass=kata \
  --restart=Never
```

**Kata Containers 配置**：

```toml
# /etc/kata-containers/configuration.toml
[hypervisor.qemu]
path = "/usr/bin/qemu-system-x86_64"
kernel = "/usr/share/kata-containers/vmlinux.container"
machine_type = "pc"
enable_annotations = ["enable_iommu", "virtio_fs_extra_args"]
```

**效果**：

- 安全隔离：VM 级别的隔离
- 性能优化：接近容器的性能
- 兼容性：完全兼容容器接口

### 案例 3：高性能计算 VM 部署

**场景**：运行高性能计算任务

**实现方案**：

```bash
# 配置高性能 VM
qemu-system-x86_64 \
  -enable-kvm \
  -cpu host,+x2apic \
  -smp 8,sockets=2,cores=4,threads=1 \
  -m 16G \
  -numa node,nodeid=0,cpus=0-3,mem=8G \
  -numa node,nodeid=1,cpus=4-7,mem=8G \
  -drive file=vm.img,format=raw,cache=none \
  -netdev tap,id=net0,ifname=tap0 \
  -device virtio-net-pci,netdev=net0 \
  -device vfio-pci,host=01:00.0
```

**效果**：

- 性能优化：接近原生性能
- NUMA 优化：NUMA 感知配置
- GPU 直通：支持 GPU 直通

---

## 9 使用指南

### 9.1 快速开始

**适用场景**：

- 需要完整的操作系统隔离
- 运行不同操作系统
- 安全隔离要求高的场景

**快速步骤**：

1. **检查虚拟化支持**：

   ```bash
   # 检查 CPU 虚拟化支持
   grep -E '(vmx|svm)' /proc/cpuinfo
   # 输出包含 vmx (Intel) 或 svm (AMD) 表示支持
   ```

2. **安装 KVM**：

   ```bash
   # Ubuntu/Debian
   sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils

   # CentOS/RHEL
   sudo yum install qemu-kvm libvirt libvirt-python libguestfs-tools
   ```

3. **创建虚拟机**：使用 `virt-install` 或 `virt-manager` 创建虚拟机

### 9.2 使用技巧

#### 性能优化

**CPU 优化**：

- 使用 `host-passthrough` CPU 模式获得最佳性能
- 设置 CPU 亲和性绑定到特定 CPU 核心
- 考虑 NUMA 拓扑优化

**内存优化**：

- 使用大页内存（HugePages）提升性能
- 启用内存气球（balloon）动态调整内存
- 设置合理的内存限制

**网络优化**：

- 使用 virtio-net 驱动获得最佳网络性能
- 考虑 SR-IOV 直通获得接近原生性能
- 使用桥接网络实现网络隔离

**存储优化**：

- 使用 virtio-blk 驱动
- 考虑使用 raw 格式获得最佳性能
- 使用缓存策略优化 IO 性能

#### 配置最佳实践

1. **安全配置**：启用 SELinux/AppArmor，限制 VM 访问
2. **资源管理**：使用 libvirt 统一管理 VM 资源
3. **监控告警**：设置资源使用监控和告警
4. **备份策略**：定期备份 VM 镜像和配置

### 9.3 常见问题

**Q1：如何检查 KVM 是否正常工作？**

```bash
# 检查 KVM 模块
lsmod | grep kvm

# 检查 libvirt 服务
systemctl status libvirtd

# 测试创建简单 VM
virt-install --name test --ram 1024 --disk size=5 --cdrom /path/to/iso
```

**Q2：VM 性能不佳如何优化？**

- 检查 CPU 模式是否为 `host-passthrough`
- 确认启用了 CPU 虚拟化扩展（vmx/svm）
- 检查是否使用了 virtio 驱动
- 考虑使用 SR-IOV 或 GPU 直通

**Q3：如何实现 VM 高可用？**

- 使用 libvirt 的迁移功能
- 配置共享存储（NFS/Ceph）
- 使用集群管理工具（如 oVirt）

### 9.4 实践建议

**云原生部署**：

- 使用 Kubernetes + KubeVirt 管理 VM
- 配置 VM 资源限制和调度策略
- 实现 VM 生命周期管理

**安全隔离**：

- 使用独立的网络和存储
- 启用安全增强功能（SELinux/AppArmor）
- 定期更新 VM 镜像和宿主机系统

**高性能计算**：

- 使用 CPU 和内存直通
- 配置 NUMA 拓扑优化
- 使用 GPU 直通支持 GPU 计算

---

**更新时间**：2025-11-15 **版本**：v1.2 **状态**：✅ 包含使用指南和 2025 年最新实践
