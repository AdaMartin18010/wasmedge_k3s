# 虚拟机代码示例

## 📑 目录

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

---

**更新时间**：2025-11-04 **版本**：v1.0 **状态**：✅ 基础示例已创建
