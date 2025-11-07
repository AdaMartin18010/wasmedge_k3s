# 沙盒化 API 规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [1. 概述](#1-概述)
- [2. Seccomp/AppArmor Profile API](#2-seccompapparmor-profile-api)
- [3. gVisor Sentry API](#3-gvisor-sentry-api)
- [4. Firecracker API](#4-firecracker-api)
- [5. Kata Containers API](#5-kata-containers-api)
- [6. 沙盒化 API 安全模型](#6-沙盒化-api-安全模型)
- [7. API 演进路径](#7-api-演进路径)
- [8. 形式化定义](#8-形式化定义)
- [9. 相关文档](#9-相关文档)

---

## 1. 概述

沙盒化 API 规范定义了安全沙盒的接口标准，从 Seccomp/AppArmor 到
gVisor、Firecracker，提供了不同级别的安全隔离 API。

### 1.1 核心沙盒化 API

| API 规范            | 技术           | 隔离级别         | 性能开销 |
| ------------------- | -------------- | ---------------- | -------- |
| **Seccomp**         | Linux Kernel   | 系统调用过滤     | <1%      |
| **AppArmor**        | Linux Kernel   | 文件系统访问控制 | 2-5%     |
| **gVisor Sentry**   | 用户态内核     | 完整系统调用拦截 | 10-20%   |
| **Firecracker**     | MicroVM        | 硬件级隔离       | 5-10%    |
| **Kata Containers** | VM + Container | 硬件级隔离       | 10-15%   |

### 1.2 沙盒化 API 层次

```text
应用层 API
  ↓
沙盒运行时 API (gVisor Sentry, Firecracker)
  ↓
安全策略 API (Seccomp, AppArmor, Landlock)
  ↓
Linux 系统调用 API
  ↓
硬件虚拟化 API (VT-x, AMD-V)
```

---

## 2. Seccomp/AppArmor Profile API

### 2.1 Seccomp Profile API

**Seccomp Profile 定义**：

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64", "SCMP_ARCH_X86", "SCMP_ARCH_X32"],
  "syscalls": [
    {
      "names": ["accept", "accept4", "access", "arch_prctl"],
      "action": "SCMP_ACT_ALLOW",
      "args": []
    },
    {
      "names": ["clone"],
      "action": "SCMP_ACT_ALLOW",
      "args": [
        {
          "index": 0,
          "value": 2114060288,
          "valueTwo": 0,
          "op": "SCMP_CMP_MASKED_EQ"
        }
      ]
    }
  ]
}
```

### 2.2 AppArmor Profile API

**AppArmor Profile 定义**：

```text
profile docker-default flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  network,
  capability,
  file,
  umount,

  deny @{PROC}/* w,
  deny /sys/[^f]** wklx,
  deny /sys/f[^s]** wklx,
  deny /sys/fs/[^c]** wklx,
  deny /sys/fs/c[^g]** wklx,
  deny /sys/fs/cg[^r]** wklx,
  deny /sys/firmware/** rwklx,
  deny /sys/kernel/security/** rwklx,
}
```

### 2.3 Landlock LSM API

**Landlock 规则定义**（Linux 5.13+）：

```c
struct landlock_ruleset_attr ruleset_attr = {
    .handled_access_fs = LANDLOCK_ACCESS_FS_READ_FILE |
                         LANDLOCK_ACCESS_FS_WRITE_FILE |
                         LANDLOCK_ACCESS_FS_READ_DIR |
                         LANDLOCK_ACCESS_FS_REMOVE_DIR,
};

int ruleset_fd = landlock_create_ruleset(&ruleset_attr, sizeof(ruleset_attr), 0);
```

---

## 3. gVisor Sentry API

### 3.1 Sentry 系统调用 API

**gVisor Sentry** 实现了用户态内核，拦截所有系统调用：

```go
// Sentry 系统调用处理
func (s *Syscall) HandleSyscall(ctx context.Context, args arch.SyscallArguments) (uintptr, error) {
    switch args[0].Uint64() {
    case syscall.SYS_READ:
        return s.handleRead(ctx, args)
    case syscall.SYS_WRITE:
        return s.handleWrite(ctx, args)
    // ... 其他系统调用
    }
}
```

### 3.2 gVisor 配置 API

**gVisor 运行时配置**：

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
overhead:
  podFixed:
    memory: "2Gi"
    cpu: "100m"
scheduling:
  nodeSelector:
    runtime: gvisor
```

### 3.3 gVisor 性能 API

**gVisor 性能指标**：

| 指标         | 值       | 说明                 |
| ------------ | -------- | -------------------- |
| **启动时间** | 50-100ms | 相比容器增加 10-20ms |
| **内存开销** | +20-50MB | 用户态内核开销       |
| **CPU 开销** | +10-20%  | 系统调用拦截开销     |
| **网络延迟** | +0.5-1ms | 网络栈虚拟化开销     |

---

## 4. Firecracker API

### 4.1 Firecracker REST API

**Firecracker API 端点**：

```bash
# 创建 MicroVM
PUT /vms/{vm_id}
{
  "vcpu_count": 2,
  "mem_size_mib": 512,
  "ht_enabled": false
}

# 启动 MicroVM
PUT /vms/{vm_id}/actions
{
  "action_type": "InstanceStart"
}

# 配置网络接口
PUT /vms/{vm_id}/networks/{iface_id}
{
  "iface_id": "eth0",
  "guest_mac": "AA:FC:00:00:00:01",
  "host_dev_name": "tap0"
}
```

### 4.2 Firecracker 性能 API

**Firecracker 性能指标**：

| 指标         | 值            | 说明           |
| ------------ | ------------- | -------------- |
| **启动时间** | <125ms        | 极速冷启动     |
| **内存开销** | <5MB          | 最小化内存占用 |
| **CPU 开销** | 5-10%         | 硬件虚拟化开销 |
| **并发密度** | 150+ VMs/core | 高密度部署     |

---

## 5. Kata Containers API

### 5.1 Kata Runtime API

**Kata Containers 配置**：

```toml
[hypervisor.qemu]
path = "/usr/bin/qemu-system-x86_64"
kernel = "/usr/share/kata-containers/vmlinux.container"
image = "/usr/share/kata-containers/kata-containers.img"
machine_type = "pc"
memory_slots = 10
enable_annotations = ["enable_iommu", "virtio_fs_extra_args"]
disable_block_device_use = false
disable_network = false
enable_iommu = false
```

### 5.2 Kata 2.0 API（2024）

**Kata 2.0 新特性**：

- **Rust 运行时**：性能提升 30%
- **VMM 选择**：支持 QEMU、Cloud Hypervisor、Firecracker
- **GPU 支持**：NVIDIA GPU 直通
- **热迁移**：支持 VM 热迁移

---

## 6. 沙盒化 API 安全模型

### 6.1 安全边界 API

**安全边界定义**：

```text
安全边界 = {
    系统调用过滤 (Seccomp),
    文件系统访问控制 (AppArmor/Landlock),
    网络隔离 (Network Namespace),
    进程隔离 (PID Namespace),
    用户隔离 (User Namespace)
}
```

### 6.2 能力模型 API

**Linux Capabilities API**：

```yaml
securityContext:
  capabilities:
    add:
      - NET_ADMIN
      - SYS_TIME
    drop:
      - ALL
```

### 6.3 零信任 API 模型

**SPIFFE/SPIRE API**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    spiffe.io/spiffe-id: spiffe://example.com/ns/default/sa/payment-service
spec:
  containers:
    - name: app
      image: payment-service:latest
```

---

## 7. API 演进路径

### 7.1 从容器到沙盒的 API 演进

```text
Docker API (2013)
  ↓
OCI Runtime Spec + Seccomp (2017)
  ↓
gVisor Sentry API (2018)
  ↓
Firecracker API (2018)
  ↓
Kata Containers API (2020)
  ↓
Landlock LSM API (2021)
  ↓
统一沙盒化 API (2025)
```

### 7.2 Kubernetes 沙盒化 API 演进

| 版本  | API 特性                  | 时间 |
| ----- | ------------------------- | ---- |
| v1.0  | PodSecurityPolicy         | 2015 |
| v1.8  | RuntimeClass              | 2017 |
| v1.12 | RuntimeClass Beta         | 2018 |
| v1.20 | RuntimeClass GA           | 2020 |
| v1.25 | PodSecurityPolicy 废弃    | 2022 |
| v1.28 | ValidatingAdmissionPolicy | 2023 |
| v1.30 | RuntimeClass 增强         | 2024 |

---

## 8. 形式化定义

### 8.1 沙盒化 API 规范形式化

**定义 8.1（沙盒化 API 规范）**：沙盒化 API 规范是一个四元组：

```text
Sandbox_API = ⟨Syscall_Filter, FS_Control, Network_Isolation, Process_Isolation⟩
```

其中：

- **Syscall_Filter**：系统调用过滤 API（Seccomp）
- **FS_Control**：文件系统访问控制 API（AppArmor、Landlock）
- **Network_Isolation**：网络隔离 API（Network Namespace）
- **Process_Isolation**：进程隔离 API（PID Namespace、User Namespace）

### 8.2 安全隔离度模型

**定义 8.2（安全隔离度）**：安全隔离度是一个函数：

```text
Isolation_Level(Sandbox_API) = f(Syscall_Filter, FS_Control, Network_Isolation, Process_Isolation)
```

**隔离度分级**：

- **L1（低）**：Seccomp 基础过滤
- **L2（中）**：Seccomp + AppArmor
- **L3（高）**：gVisor Sentry（用户态内核）
- **L4（极高）**：Firecracker/Kata（硬件级隔离）

---

## 9. 相关文档

- **[沙盒化抽象](../../ARCHITECTURE/architecture-view/02-virtualization-containerization-sandboxing/03-sandboxing-abstraction.md)** -
  沙盒化 API 设计原理
- **[隔离栈技术实现](../../TECHNICAL/29-isolation-stack/isolation-stack.md)** -
  沙盒化在隔离栈中的位置
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新**：2025-11-07 **维护者**：项目团队
