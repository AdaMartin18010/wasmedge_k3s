# 沙盒化 API 规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 核心沙盒化 API](#11-核心沙盒化-api)
  - [1.2 沙盒化 API 层次](#12-沙盒化-api-层次)
  - [1.3 沙盒化在 API 规范中的位置](#13-沙盒化在-api-规范中的位置)
- [2 Seccomp/AppArmor Profile API](#2-seccompapparmor-profile-api)
  - [2.1 Seccomp Profile API](#21-seccomp-profile-api)
  - [2.2 AppArmor Profile API](#22-apparmor-profile-api)
  - [2.3 Landlock LSM API](#23-landlock-lsm-api)
- [3 gVisor Sentry API](#3-gvisor-sentry-api)
  - [3.1 Sentry 系统调用 API](#31-sentry-系统调用-api)
  - [3.2 gVisor 配置 API](#32-gvisor-配置-api)
  - [3.3 gVisor 性能 API](#33-gvisor-性能-api)
- [4 Firecracker API](#4-firecracker-api)
  - [4.1 Firecracker REST API](#41-firecracker-rest-api)
  - [4.2 Firecracker 性能 API](#42-firecracker-性能-api)
- [5 Kata Containers API](#5-kata-containers-api)
  - [5.1 Kata Runtime API](#51-kata-runtime-api)
  - [5.2 Kata 2.0 API（2024）](#52-kata-20-api2024)
- [6 沙盒化 API 安全模型](#6-沙盒化-api-安全模型)
  - [6.1 安全边界 API](#61-安全边界-api)
  - [6.2 能力模型 API](#62-能力模型-api)
  - [6.3 零信任 API 模型](#63-零信任-api-模型)
- [7 API 演进路径](#7-api-演进路径)
  - [7.1 从容器到沙盒的 API 演进](#71-从容器到沙盒的-api-演进)
  - [7.2 Kubernetes 沙盒化 API 演进](#72-kubernetes-沙盒化-api-演进)
- [8 形式化定义与理论基础](#8-形式化定义与理论基础)
  - [8.1 沙盒化 API 规范形式化](#81-沙盒化-api-规范形式化)
  - [8.2 安全隔离度模型](#82-安全隔离度模型)
  - [8.3 系统调用拦截形式化](#83-系统调用拦截形式化)
  - [8.4 安全边界形式化](#84-安全边界形式化)
- [9 相关文档](#9-相关文档)

---

## 1 概述

沙盒化 API 规范定义了安全沙盒的接口标准，从 Seccomp/AppArmor 到
gVisor、Firecracker，提供了不同级别的安全隔离 API。本文档基于形式化方法，提供严
格的数学定义和推理论证，确保沙盒化 API 的正确性和安全性。

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

**参考标准**：

- [Seccomp BPF](https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html) -
  Linux 系统调用过滤
- [AppArmor](https://apparmor.net/) - Linux 应用安全框架
- [Landlock](https://www.kernel.org/doc/html/latest/security/landlock.html) -
  Linux 5.13+ 文件系统安全
- [gVisor](https://gvisor.dev/) - 用户态内核沙盒
- [Firecracker](https://firecracker-microvm.github.io/) - 轻量级 MicroVM
- [Kata Containers](https://katacontainers.io/) - 安全容器运行时

### 1.3 沙盒化在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)），
沙盒化 API 属于 **Security** 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
                                        ↑
                            Sandboxing ∈ Security
```

沙盒化 API 在 API 规范中提供：

- **Security 层**：通过系统调用过滤、文件系统访问控制、网络隔离实现安全边界
- **隔离保证**：确保 API 调用在隔离环境中执行，防止恶意代码影响宿主系统
- **最小权限**：通过能力模型和策略引擎实现最小权限原则
- **零信任**：通过 SPIFFE/SPIRE 实现工作负载身份和认证

---

## 2 Seccomp/AppArmor Profile API

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

## 3 gVisor Sentry API

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

## 4 Firecracker API

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

## 5 Kata Containers API

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

## 6 沙盒化 API 安全模型

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

## 7 API 演进路径

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

## 8 形式化定义与理论基础

### 8.1 沙盒化 API 规范形式化

**定义 8.1（沙盒化 API 规范）**：沙盒化 API 规范是一个四元组：

```text
Sandbox_API = ⟨Syscall_Filter, FS_Control, Network_Isolation, Process_Isolation⟩
```

其中：

- **Syscall_Filter**：系统调用过滤 API `F: Syscall → Action`
- **FS_Control**：文件系统访问控制 API `C: Path × Operation → Bool`
- **Network_Isolation**：网络隔离 API `N: NetworkNamespace → NetworkConfig`
- **Process_Isolation**：进程隔离 API `P: ProcessNamespace → ProcessConfig`

**定义 8.2（沙盒环境）**：沙盒环境是一个三元组：

```text
Sandbox = ⟨API, Policy, Runtime⟩
```

其中：

- **API**：沙盒化 API 规范
- **Policy**：安全策略 `Policy: Request → Decision`
- **Runtime**：沙盒运行时 `Runtime: Code → Execution`

### 8.2 安全隔离度模型

**定义 8.3（安全隔离度）**：安全隔离度是一个函数：

```text
Isolation_Level(Sandbox_API) = f(Syscall_Filter, FS_Control, Network_Isolation, Process_Isolation)
```

**隔离度分级**：

- **L1（低）**：Seccomp 基础过滤 `Isolation_Level = 1`
- **L2（中）**：Seccomp + AppArmor `Isolation_Level = 2`
- **L3（高）**：gVisor Sentry（用户态内核）`Isolation_Level = 3`
- **L4（极高）**：Firecracker/Kata（硬件级隔离）`Isolation_Level = 4`

**定理 8.1（隔离度单调性）**：隔离度越高，安全性越高：

```text
Isolation_Level(S₁) < Isolation_Level(S₂) ⟹ Security(S₁) < Security(S₂)
```

**证明**：根据定义 8.3，隔离度越高，系统调用过滤、文件系统控制、网络隔离和进程隔
离越严格，因此安全性越高。□

### 8.3 系统调用拦截形式化

**定义 8.4（系统调用拦截）**：系统调用拦截是一个函数：

```text
Intercept: Syscall × Policy → Action
```

其中 `Action ∈ {Allow, Deny, Filter, Redirect}`。

**定义 8.5（gVisor 拦截）**：gVisor 拦截所有系统调用：

```text
∀ syscall: Intercept(syscall, Policy) ≠ Allow_Direct
```

即所有系统调用都经过 gVisor Sentry 处理，不直接访问内核。

**定理 8.2（拦截完备性）**：如果沙盒拦截所有系统调用，则沙盒是完备的：

```text
∀ syscall: Intercept(syscall, Policy) ≠ Allow_Direct ⟹ Complete(Sandbox)
```

**证明**：如果所有系统调用都经过拦截，则沙盒可以完全控制进程的行为，因此沙盒是完
备的。□

### 8.4 安全边界形式化

**定义 8.6（安全边界）**：安全边界是一个函数：

```text
Security_Boundary: Sandbox → Set(Resource)
```

其中 `Security_Boundary(Sandbox)` 表示沙盒可以访问的资源集合。

**定义 8.7（边界隔离性）**：两个沙盒相互隔离，当且仅当：

```text
Isolation(S₁, S₂) = Security_Boundary(S₁) ∩ Security_Boundary(S₂) = ∅
```

**定理 8.3（边界隔离性传递）**：如果沙盒 S₁ 与 S₂ 隔离，S₂ 与 S₃ 隔离，则 S₁ 与
S₃ 隔离：

```text
Isolation(S₁, S₂) ∧ Isolation(S₂, S₃) ⟹ Isolation(S₁, S₃)
```

**证明**：根据定义 8.7，如果 `Security_Boundary(S₁) ∩ Security_Boundary(S₂) = ∅`
且 `Security_Boundary(S₂) ∩ Security_Boundary(S₃) = ∅`，则
`Security_Boundary(S₁) ∩ Security_Boundary(S₃) = ∅`。□

**定理 8.4（最小权限原则）**：沙盒只访问必要的资源：

```text
Security_Boundary(Sandbox) = Minimal_Set(Required_Resources)
```

**证明**：根据最小权限原则，沙盒应该只授予执行任务所需的最小权限集合。□

---

## 9 相关文档

- **[沙盒化抽象](../../ARCHITECTURE/architecture-view/02-virtualization-containerization-sandboxing/03-sandboxing-abstraction.md)** -
  沙盒化 API 设计原理
- **[隔离栈技术实现](../../TECHNICAL/29-isolation-stack/isolation-stack.md)** -
  沙盒化在隔离栈中的位置
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新**：2025-11-07 **维护者**：项目团队
