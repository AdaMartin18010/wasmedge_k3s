# 14.2 虚拟机安全加固

> **文档版本**：v1.0 **最后更新：2025-11-15 **维护者**：项目团队

---

## 📑 目录

- [14.2 虚拟机安全加固](#142-虚拟机安全加固)
  - [📑 目录](#-目录)
  - [概述](#概述)
  - [安全配置矩阵](#安全配置矩阵)
  - [安全加固示例](#安全加固示例)
    - [虚拟机安全加固配置](#虚拟机安全加固配置)
  - [关键技术分析](#关键技术分析)
    - [1. Seccomp 配置](#1-seccomp-配置)
    - [2. AppArmor 配置](#2-apparmor-配置)
    - [3. SELinux 配置](#3-selinux-配置)
    - [4. Capabilities 限制](#4-capabilities-限制)
    - [5. 只读根文件系统](#5-只读根文件系统)
  - [相关文档](#相关文档)
  - [2025 年最新实践](#2025-年最新实践)
    - [虚拟机安全加固最佳实践（2025）](#虚拟机安全加固最佳实践2025)
  - [实际应用案例](#实际应用案例)
    - [案例 1：虚拟机安全加固配置（2025）](#案例-1虚拟机安全加固配置2025)

---

## 概述

本文档分析虚拟机安全加固的设计和实现，展示如何通过 Seccomp、AppArmor、SELinux 等
机制实现虚拟机安全加固。

## 安全配置矩阵

| **安全措施**       | **容器实现**                    | **虚拟机实现**                  | **API 配置**         |
| ------------------ | ------------------------------- | ------------------------------- | -------------------- |
| **Seccomp**        | SecurityContext.seccompProfile  | virt-launcher Pod Seccomp       | Pod SecurityContext  |
| **AppArmor**       | SecurityContext.appArmorProfile | virt-launcher AppArmor Profile  | Pod SecurityContext  |
| **SELinux**        | SecurityContext.seLinuxOptions  | virt-launcher SELinux Context   | Pod SecurityContext  |
| **Capabilities**   | SecurityContext.capabilities    | 限制 virt-launcher Capabilities | Pod SecurityContext  |
| **只读根文件系统** | readOnlyRootFilesystem          | 虚拟机磁盘只读挂载              | Volume ReadOnly 配置 |

---

## 安全加固示例

### 虚拟机安全加固配置

```yaml
# 虚拟机安全加固配置
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: secure-vm
spec:
  template:
    spec:
      # virt-launcher Pod安全上下文
      securityContext:
        # Seccomp配置
        seccompProfile:
          type: RuntimeDefault
        # AppArmor配置
        appArmorProfile: runtime/default
        # SELinux配置
        seLinuxOptions:
          level: "s0:c123,c456"
        # Capabilities限制
        capabilities:
          drop:
            - ALL
          add:
            - NET_ADMIN # 仅允许网络管理
        # 非root用户运行
        runAsNonRoot: true
        runAsUser: 1000
      domain:
        devices:
          disks:
            - name: bootdisk
              disk:
                bus: virtio
              # 只读根文件系统
              readOnly: true
          # 禁用不必要的设备
          rng: {} # 仅启用随机数生成器
          # 禁用USB、串口等
      # 网络安全策略
      network:
        # 禁用DHCP（手动配置IP）
        dhcpOptions: {}
```

---

## 关键技术分析

### 1. Seccomp 配置

**容器实现**：SecurityContext.seccompProfile

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: test
      image: nginx:alpine
```

**虚拟机实现**：virt-launcher Pod Seccomp

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: secure-vm
spec:
  template:
    spec:
      securityContext:
        seccompProfile:
          type: RuntimeDefault
      domain:
        resources:
          requests:
            memory: "1Gi"
            cpu: "1"
```

**说明**：

- Seccomp 限制系统调用
- 容器和虚拟机都使用 Seccomp 进行安全加固
- Seccomp 配置通过 Pod SecurityContext 实现

### 2. AppArmor 配置

**容器实现**：SecurityContext.appArmorProfile

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    appArmorProfile: runtime/default
  containers:
    - name: test
      image: nginx:alpine
```

**虚拟机实现**：virt-launcher AppArmor Profile

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: secure-vm
spec:
  template:
    spec:
      securityContext:
        appArmorProfile: runtime/default
      domain:
        resources:
          requests:
            memory: "1Gi"
            cpu: "1"
```

**说明**：

- AppArmor 限制进程权限
- 容器和虚拟机都使用 AppArmor 进行安全加固
- AppArmor 配置通过 Pod SecurityContext 实现

### 3. SELinux 配置

**容器实现**：SecurityContext.seLinuxOptions

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    seLinuxOptions:
      level: "s0:c123,c456"
  containers:
    - name: test
      image: nginx:alpine
```

**虚拟机实现**：virt-launcher SELinux Context

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: secure-vm
spec:
  template:
    spec:
      securityContext:
        seLinuxOptions:
          level: "s0:c123,c456"
      domain:
        resources:
          requests:
            memory: "1Gi"
            cpu: "1"
```

**说明**：

- SELinux 提供强制访问控制
- 容器和虚拟机都使用 SELinux 进行安全加固
- SELinux 配置通过 Pod SecurityContext 实现

### 4. Capabilities 限制

**容器实现**：SecurityContext.capabilities

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    capabilities:
      drop:
        - ALL
      add:
        - NET_ADMIN
  containers:
    - name: test
      image: nginx:alpine
```

**虚拟机实现**：限制 virt-launcher Capabilities

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: secure-vm
spec:
  template:
    spec:
      securityContext:
        capabilities:
          drop:
            - ALL
          add:
            - NET_ADMIN
      domain:
        resources:
          requests:
            memory: "1Gi"
            cpu: "1"
```

**说明**：

- Capabilities 限制进程权限
- 容器和虚拟机都使用 Capabilities 进行安全加固
- Capabilities 配置通过 Pod SecurityContext 实现

### 5. 只读根文件系统

**容器实现**：readOnlyRootFilesystem

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  containers:
    - name: test
      image: nginx:alpine
      securityContext:
        readOnlyRootFilesystem: true
```

**虚拟机实现**：虚拟机磁盘只读挂载

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: secure-vm
spec:
  template:
    spec:
      domain:
        devices:
          disks:
            - name: bootdisk
              disk:
                bus: virtio
              # 只读根文件系统
              readOnly: true
```

**说明**：

- 只读根文件系统防止文件系统被修改
- 容器和虚拟机都支持只读根文件系统
- 只读配置通过 SecurityContext 和 Volume 配置实现

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [多租户安全隔离](../10-security-design/01-multi-tenant-isolation.md) - 多租户
  安全隔离
- [数据加密与密钥管理](../10-security-design/03-data-encryption.md) - 数据加密

---

## 2025 年最新实践

### 虚拟机安全加固最佳实践（2025）

**2025 年趋势**：虚拟机安全加固的深度优化

**实践要点**：

- **多层安全**：使用 Seccomp、AppArmor、SELinux 等多层安全机制
- **最小权限**：使用 Capabilities 限制进程权限
- **只读文件系统**：使用只读根文件系统防止文件系统被修改

**代码示例**：

```python
# 2025 年虚拟机安全加固工具
class VMSecurityHardeningManager:
    def __init__(self):
        self.seccomp_manager = SeccompManager()
        self.apparmor_manager = AppArmorManager()
        self.selinux_manager = SELinuxManager()
        self.capabilities_manager = CapabilitiesManager()

    def harden_vm(self, vm_config, security_level):
        """加固虚拟机"""
        # Seccomp 配置
        self.seccomp_manager.configure(vm_config, security_level)

        # AppArmor 配置
        self.apparmor_manager.configure(vm_config, security_level)

        # SELinux 配置
        self.selinux_manager.configure(vm_config, security_level)

        # Capabilities 限制
        self.capabilities_manager.configure(vm_config, security_level)

        return vm_config
```

## 实际应用案例

### 案例 1：虚拟机安全加固配置（2025）

**场景**：使用多层安全机制加固虚拟机

**实现方案**：

```yaml
# 虚拟机安全加固配置
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: secure-vm
spec:
  template:
    spec:
      securityContext:
        seccompProfile:
          type: RuntimeDefault
        appArmorProfile: runtime/default
        seLinuxOptions:
          level: "s0:c123,c456"
        capabilities:
          drop:
            - ALL
          add:
            - NET_ADMIN
        runAsNonRoot: true
        runAsUser: 1000
      domain:
        devices:
          disks:
            - name: bootdisk
              disk:
                bus: virtio
              readOnly: true
```

**效果**：

- 多层安全：使用 Seccomp、AppArmor、SELinux 等多层安全机制
- 最小权限：使用 Capabilities 限制进程权限
- 只读文件系统：使用只读根文件系统防止文件系统被修改

---

**最后更新**：2025-11-15 **维护者**：项目团队
