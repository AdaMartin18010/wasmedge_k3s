# 虚拟机代码示例

## 📑 目录

- [虚拟机代码示例](#虚拟机代码示例)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 理论基础](#11-理论基础)
  - [2 libvirt Python 示例](#2-libvirt-python-示例)
    - [2.1 创建虚拟机](#21-创建虚拟机)
    - [2.2 管理虚拟机](#22-管理虚拟机)
  - [3 libvirt Go 示例](#3-libvirt-go-示例)
    - [3.1 创建虚拟机](#31-创建虚拟机)
    - [3.2 管理虚拟机](#32-管理虚拟机)
  - [4 QEMU API 示例](#4-qemu-api-示例)
    - [4.1 QMP 示例](#41-qmp-示例)
  - [5 虚拟机生命周期管理](#5-虚拟机生命周期管理)
    - [5.1 完整生命周期示例](#51-完整生命周期示例)
  - [6 相关文档](#6-相关文档)
    - [6.1 理论论证](#61-理论论证)
    - [6.2 架构视角](#62-架构视角)
    - [6.3 技术文档](#63-技术文档)
  - [7 2025 年最新实践](#7-2025-年最新实践)
    - [7.1 libvirt 9.0+ 新特性（2025）](#71-libvirt-90-新特性2025)
    - [7.2 KubeVirt 1.2+ VM 管理（2025）](#72-kubevirt-12-vm-管理2025)
    - [7.3 云原生 VM 部署（2025）](#73-云原生-vm-部署2025)
  - [8 实际应用案例](#8-实际应用案例)
    - [案例 1：开发环境 VM 自动化管理](#案例-1开发环境-vm-自动化管理)
    - [案例 2：测试环境 VM 快照管理](#案例-2测试环境-vm-快照管理)
    - [案例 3：生产环境 VM 高可用部署](#案例-3生产环境-vm-高可用部署)

---

## 1 概述

本文档提供 **虚拟机的实际代码示例**，展示如何使用 libvirt、QEMU API 等创建和管理
虚拟机。

### 1.1 理论基础

虚拟机代码示例基于以下理论论证：

- **公理 A1（冯·诺依曼等价）**：任何图灵机可计算函数均可在虚拟化环境中实现
- **归纳映射 Ψ₁（虚拟化层）**：将物理硬件抽象为 VM 资源池
- **状态空间压缩**：通过虚拟化实现状态空间压缩

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2 libvirt Python 示例

### 2.1 创建虚拟机

```python
import libvirt
from xml.etree import ElementTree as ET

# 连接到 libvirt
conn = libvirt.open('qemu:///system')

# 创建虚拟机 XML
vm_xml = """
<domain type='kvm'>
  <name>myvm</name>
  <memory unit='KiB'>2097152</memory>
  <vcpu placement='static'>2</vcpu>
  <os>
    <type arch='x86_64' machine='pc-i440fx-2.11'>hvm</type>
    <boot dev='hd'/>
  </os>
  <devices>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/var/lib/libvirt/images/myvm.qcow2'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='bridge'>
      <source bridge='virbr0'/>
      <model type='virtio'/>
    </interface>
  </devices>
</domain>
"""

# 定义并启动虚拟机
dom = conn.defineXML(vm_xml)
dom.create()
```

### 2.2 管理虚拟机

```python
import libvirt

conn = libvirt.open('qemu:///system')

# 获取所有虚拟机
domains = conn.listAllDomains()

for dom in domains:
    print(f"Name: {dom.name()}")
    print(f"State: {dom.state()}")
    print(f"UUID: {dom.UUIDString()}")

# 启动虚拟机
dom = conn.lookupByName('myvm')
dom.create()

# 关闭虚拟机
dom.shutdown()

# 强制关闭虚拟机
dom.destroy()

# 删除虚拟机
dom.undefine()
```

---

## 3 libvirt Go 示例

### 3.1 创建虚拟机

```go
package main

import (
    "fmt"
    "github.com/libvirt/libvirt-go"
    "github.com/libvirt/libvirt-go-xml"
)

func main() {
    // 连接到 libvirt
    conn, err := libvirt.NewConnect("qemu:///system")
    if err != nil {
        panic(err)
    }
    defer conn.Close()

    // 创建虚拟机配置
    domainConfig := &libvirtxml.Domain{
        Type: "kvm",
        Name: "myvm",
        Memory: &libvirtxml.DomainMemory{
            Value: 2048,
            Unit:  "KiB",
        },
        VCPU: &libvirtxml.DomainVCPU{
            Value: 2,
        },
        OS: &libvirtxml.DomainOS{
            Type: &libvirtxml.DomainOSType{
                Arch: "x86_64",
                Type: "hvm",
            },
            Boot: []libvirtxml.DomainBootDevice{
                {Dev: "hd"},
            },
        },
        Devices: &libvirtxml.DomainDeviceList{
            Disks: []libvirtxml.DomainDisk{
                {
                    Type:   "file",
                    Device:  "disk",
                    Driver: &libvirtxml.DomainDiskDriver{Name: "qemu", Type: "qcow2"},
                    Source: &libvirtxml.DomainDiskSource{
                        File: &libvirtxml.DomainDiskSourceFile{File: "/var/lib/libvirt/images/myvm.qcow2"},
                    },
                    Target: &libvirtxml.DomainDiskTarget{Dev: "vda", Bus: "virtio"},
                },
            },
            Interfaces: []libvirtxml.DomainInterface{
                {
                    Type: "bridge",
                    Source: &libvirtxml.DomainInterfaceSource{
                        Bridge: &libvirtxml.DomainInterfaceSourceBridge{Bridge: "virbr0"},
                    },
                    Model: &libvirtxml.DomainInterfaceModel{Type: "virtio"},
                },
            },
        },
    }

    // 转换为 XML
    xml, err := domainConfig.Marshal()
    if err != nil {
        panic(err)
    }

    // 定义并启动虚拟机
    dom, err := conn.DomainDefineXML(xml)
    if err != nil {
        panic(err)
    }

    err = dom.Create()
    if err != nil {
        panic(err)
    }

    fmt.Println("VM created successfully")
}
```

### 3.2 管理虚拟机

```go
package main

import (
    "fmt"
    "github.com/libvirt/libvirt-go"
)

func main() {
    conn, err := libvirt.NewConnect("qemu:///system")
    if err != nil {
        panic(err)
    }
    defer conn.Close()

    // 获取所有虚拟机
    domains, err := conn.ListAllDomains(libvirt.CONNECT_LIST_DOMAINS_ACTIVE | libvirt.CONNECT_LIST_DOMAINS_INACTIVE)
    if err != nil {
        panic(err)
    }

    for _, dom := range domains {
        name, _ := dom.GetName()
        state, _, _ := dom.GetState()
        uuid, _ := dom.GetUUIDString()

        fmt.Printf("Name: %s, State: %d, UUID: %s\n", name, state, uuid)
    }

    // 启动虚拟机
    dom, err := conn.LookupDomainByName("myvm")
    if err != nil {
        panic(err)
    }

    err = dom.Create()
    if err != nil {
        panic(err)
    }

    // 关闭虚拟机
    err = dom.Shutdown()
    if err != nil {
        panic(err)
    }

    // 删除虚拟机
    err = dom.Undefine()
    if err != nil {
        panic(err)
    }
}
```

---

## 4 QEMU API 示例

### 4.1 QMP 示例

```python
import socket
import json

# 连接到 QMP socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('/tmp/qmp.sock')

# 发送 QMP 命令
def send_qmp_command(cmd):
    request = json.dumps(cmd)
    sock.send(request.encode())
    response = sock.recv(4096)
    return json.loads(response.decode())

# 初始化 QMP
response = send_qmp_command({"execute": "qmp_capabilities"})
print(response)

# 查询 VM 状态
response = send_qmp_command({"execute": "query-status"})
print(response)

# 创建快照
response = send_qmp_command({
    "execute": "blockdev-snapshot-sync",
    "arguments": {
        "device": "drive-virtio-disk0",
        "snapshot-file": "/var/lib/libvirt/images/myvm-snapshot.qcow2"
    }
})
print(response)
```

---

## 5 虚拟机生命周期管理

### 5.1 完整生命周期示例

```python
import libvirt
import time

conn = libvirt.open('qemu:///system')

# 1. 创建虚拟机
vm_xml = """
<domain type='kvm'>
  <name>myvm</name>
  <memory unit='KiB'>2097152</memory>
  <vcpu placement='static'>2</vcpu>
  <os>
    <type arch='x86_64'>hvm</type>
    <boot dev='hd'/>
  </os>
  <devices>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/var/lib/libvirt/images/myvm.qcow2'/>
      <target dev='vda' bus='virtio'/>
    </disk>
  </devices>
</domain>
"""

dom = conn.defineXML(vm_xml)

# 2. 启动虚拟机
dom.create()

# 3. 等待虚拟机启动
time.sleep(5)

# 4. 检查虚拟机状态
state, reason = dom.state()
print(f"VM state: {state}")

# 5. 暂停虚拟机
dom.suspend()

# 6. 恢复虚拟机
dom.resume()

# 7. 重启虚拟机
dom.reboot()

# 8. 关闭虚拟机
dom.shutdown()

# 9. 等待虚拟机关闭
while dom.isActive():
    time.sleep(1)

# 10. 删除虚拟机
dom.undefine()
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

### 7.1 libvirt 9.0+ 新特性（2025）

**最新版本**：libvirt 9.0+（2025 年）

**新特性**：

- **性能优化**：改进的 VM 管理性能
- **QEMU 8.2+ 支持**：完整支持 QEMU 8.2+ 新特性
- **API 增强**：更丰富的 API 接口

**使用示例**：

```python
# libvirt 9.0+ 新 API
import libvirt

conn = libvirt.open('qemu:///system')

# 使用新的 API 创建 VM
dom = conn.createXML(vm_xml, flags=libvirt.VIR_DOMAIN_START_AUTODESTROY)
```

### 7.2 KubeVirt 1.2+ VM 管理（2025）

**KubeVirt 1.2+ 新特性**：

- **VM 生命周期管理**：更好的 VM 生命周期管理
- **性能优化**：减少 VM 启动时间
- **资源管理**：改进的资源限制

**配置示例**：

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: myvm
spec:
  running: true
  template:
    spec:
      domain:
        resources:
          requests:
            memory: 1Gi
            cpu: 1
        devices:
          disks:
          - name: disk0
            disk:
              bus: virtio
      volumes:
      - name: disk0
        containerDisk:
          image: myvm:latest
```

### 7.3 云原生 VM 部署（2025）

**2025 年趋势**：VM 和容器统一管理

**优势**：

- **统一编排**：VM 和容器使用 Kubernetes 统一编排
- **资源池化**：VM 资源池化管理
- **自动化运维**：自动化 VM 生命周期管理

**配置示例**：

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: myvmi
spec:
  domain:
    resources:
      requests:
        memory: 1Gi
        cpu: 1
    devices:
      disks:
      - name: disk0
        disk:
          bus: virtio
  volumes:
  - name: disk0
    containerDisk:
      image: myvm:latest
```

## 8 实际应用案例

### 案例 1：开发环境 VM 自动化管理

**场景**：自动化管理开发环境 VM

**实现方案**：

```python
# Python 脚本自动化管理 VM
import libvirt
import yaml

conn = libvirt.open('qemu:///system')

def create_dev_vm(name, memory_mb=2048, vcpu=2):
    """创建开发环境 VM"""
    vm_xml = f"""
    <domain type='kvm'>
      <name>{name}</name>
      <memory unit='KiB'>{memory_mb * 1024}</memory>
      <vcpu>{vcpu}</vcpu>
      <os>
        <type arch='x86_64'>hvm</type>
        <boot dev='hd'/>
      </os>
      <devices>
        <disk type='file' device='disk'>
          <driver name='qemu' type='qcow2'/>
          <source file='/var/lib/libvirt/images/{name}.qcow2'/>
          <target dev='vda' bus='virtio'/>
        </disk>
      </devices>
    </domain>
    """
    dom = conn.defineXML(vm_xml)
    dom.create()
    return dom

# 批量创建开发环境 VM
for i in range(5):
    create_dev_vm(f'dev-vm-{i}')
```

**效果**：

- 自动化创建：批量创建开发环境 VM
- 统一管理：统一管理所有开发环境 VM
- 快速部署：快速部署开发环境

### 案例 2：测试环境 VM 快照管理

**场景**：管理测试环境 VM 快照

**实现方案**：

```python
import libvirt

conn = libvirt.open('qemu:///system')
dom = conn.lookupByName('test-vm')

# 创建快照
snapshot_xml = """
<domainsnapshot>
  <name>snapshot-1</name>
  <description>Test environment snapshot</description>
</domainsnapshot>
"""
snap = dom.snapshotCreateXML(snapshot_xml, 0)

# 恢复到快照
dom.revertToSnapshot(snap)

# 删除快照
snap.delete(0)
```

**KubeVirt 配置**：

```yaml
apiVersion: snapshot.kubevirt.io/v1alpha1
kind: VirtualMachineSnapshot
metadata:
  name: test-snapshot
spec:
  source:
    apiGroup: kubevirt.io
    kind: VirtualMachine
    name: test-vm
```

**效果**：

- 快照管理：快速创建和恢复快照
- 测试隔离：每个测试使用独立的快照
- 快速重置：快速重置测试环境

### 案例 3：生产环境 VM 高可用部署

**场景**：部署高可用的生产环境 VM

**实现方案**：

```yaml
# KubeVirt VM 高可用配置
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: prod-vm
spec:
  running: true
  template:
    spec:
      evictionStrategy: LiveMigrate
      domain:
        resources:
          requests:
            memory: 4Gi
            cpu: 2
        devices:
          disks:
          - name: disk0
            disk:
              bus: virtio
      volumes:
      - name: disk0
        persistentVolumeClaim:
          claimName: prod-vm-disk
```

**libvirt 配置**：

```xml
<domain type='kvm'>
  <name>prod-vm</name>
  <memory unit='KiB'>4194304</memory>
  <vcpu placement='static'>2</vcpu>
  <features>
    <acpi/>
    <apic/>
  </features>
  <cpu mode='host-passthrough'/>
  <devices>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2' cache='none'/>
      <source file='/var/lib/libvirt/images/prod-vm.qcow2'/>
      <target dev='vda' bus='virtio'/>
    </disk>
  </devices>
</domain>
```

**效果**：

- 高可用：支持 VM 迁移和故障恢复
- 性能优化：优化的性能配置
- 资源保证：保证 VM 资源分配

---

**更新时间**：2025-11-15 **版本**：v1.1 **状态**：✅ 包含 2025 年最新实践
