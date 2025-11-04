# 容器运行时层架构视图

## 目录

- [1. 概述](#1-概述)
- [2. 容器运行时定义](#2-容器运行时定义)
- [3. 容器运行时架构](#3-容器运行时架构)
- [4. Namespace 隔离](#4-namespace-隔离)
- [5. Cgroup 资源控制](#5-cgroup-资源控制)
- [6. OverlayFS 文件系统](#6-overlayfs-文件系统)
- [7. 网络管理](#7-网络管理)
- [8. 容器运行时实现](#8-容器运行时实现)
- [9. 性能优化](#9-性能优化)
- [10. 安全加固](#10-安全加固)
- [11. 可观测性](#11-可观测性)
- [12. 总结](#12-总结)

---

## 1. 概述

本文档基于 `architecture_view.md` 的核心思想，详细阐述容器运行时层的架构设计和技
术实现。

## 2. 容器运行时定义

### 2.1 形式化定义

**容器运行时**：C : Image → Container

**定义**：

```text
Container = ⟨
  Image: ImageID,
  Namespace: {pid, mnt, net, ipc, uts, user},
  Cgroup: {cpu, memory, io, pids},
  Rootfs: OverlayFS,
  State: {Created, Running, Stopped, Paused}
⟩
```

**属性**：

- **隔离级别**：OS-level (namespace, cgroup)
- **资源开销**：Medium（共享内核）
- **启动时间**：< 1 s
- **可移植性**：High（镜像可跨平台）
- **安全模型**：隔离 + Overlay

### 2.2 核心组件

**容器运行时组件**：

1. **镜像管理**：Image 的拉取、存储、删除
2. **容器生命周期**：创建、启动、停止、删除
3. **资源隔离**：Namespace 和 Cgroup 管理
4. **文件系统**：OverlayFS 管理
5. **网络管理**：CNI 插件集成

## 3. 容器运行时架构

### 3.1 分层架构

```text
┌─────────────────────────────────────┐
│  Application Layer (业务应用)        │
└─────────────────────────────────────┘
           ▲
┌─────────────────────────────────────┐
│  Container Runtime Layer             │
│  ├─ containerd / cri-o               │
│  ├─ runc / crun                      │
│  ├─ CNI Plugins                      │
│  └─ Storage Drivers                   │
└─────────────────────────────────────┘
           ▲
┌─────────────────────────────────────┐
│  Host Kernel Layer                   │
│  ├─ Namespaces (pid, mnt, net, ...) │
│  ├─ Cgroups (cpu, memory, io, ...)  │
│  ├─ OverlayFS                        │
│  └─ Seccomp / AppArmor               │
└─────────────────────────────────────┘
           ▲
┌─────────────────────────────────────┐
│  Hypervisor / Hardware Layer         │
└─────────────────────────────────────┘
```

### 3.2 容器运行时接口

**CRI (Container Runtime Interface)**：

```yaml
# Pod 定义
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image:latest
      resources:
        requests:
          cpu: "100m"
          memory: "128Mi"
        limits:
          cpu: "200m"
          memory: "256Mi"
```

**OCI (Open Container Initiative)**：

```json
{
  "ociVersion": "1.0.0",
  "process": {
    "user": { "uid": 0, "gid": 0 },
    "args": ["/bin/sh"],
    "env": ["PATH=/usr/bin"]
  },
  "root": {
    "path": "rootfs",
    "readonly": true
  },
  "mounts": [
    {
      "destination": "/proc",
      "type": "proc",
      "source": "proc"
    }
  ],
  "linux": {
    "namespaces": [
      { "type": "pid" },
      { "type": "network" },
      { "type": "mount" }
    ],
    "cgroupsPath": "/my-container",
    "resources": {
      "cpu": { "shares": 1024 },
      "memory": { "limit": 268435456 }
    }
  }
}
```

## 4. Namespace 隔离

### 4.1 Namespace 类型

**PID Namespace**：

- **功能**：进程隔离
- **实现**：每个容器有独立的 PID 空间
- **效果**：容器内进程看不到宿主机进程

**Mount Namespace**：

- **功能**：文件系统隔离
- **实现**：每个容器有独立的挂载点
- **效果**：容器内文件系统独立

**Network Namespace**：

- **功能**：网络隔离
- **实现**：每个容器有独立的网络栈
- **效果**：容器内网络接口独立

**IPC Namespace**：

- **功能**：进程间通信隔离
- **实现**：每个容器有独立的 IPC 空间
- **效果**：容器间无法通过 IPC 通信

**UTS Namespace**：

- **功能**：主机名隔离
- **实现**：每个容器有独立的主机名
- **效果**：容器内主机名独立

**User Namespace**：

- **功能**：用户隔离
- **实现**：每个容器有独立的用户空间
- **效果**：容器内用户 ID 映射到宿主机

### 4.2 Namespace 实现

**创建 Namespace**：

```c
// 创建 PID Namespace
int pid_fd = open("/proc/self/ns/pid", O_RDONLY);
unshare(CLONE_NEWPID);
```

**进入 Namespace**：

```c
// 进入 PID Namespace
setns(pid_fd, CLONE_NEWPID);
```

## 5. Cgroup 资源控制

### 5.1 Cgroup v2 架构

**Cgroup v2 层次结构**：

```text
/sys/fs/cgroup/
├── cgroup.controllers
├── cgroup.events
├── cgroup.procs
├── cpu.weight
├── memory.max
├── io.weight
└── pids.max
```

**控制器**：

- **CPU**：cpu.weight, cpu.max
- **Memory**：memory.max, memory.swap.max
- **IO**：io.weight, io.max
- **PIDs**：pids.max

### 5.2 资源限制示例

**CPU 限制**：

```bash
# 设置 CPU 权重
echo 1024 > /sys/fs/cgroup/my-container/cpu.weight

# 设置 CPU 最大使用率
echo "50000 100000" > /sys/fs/cgroup/my-container/cpu.max
```

**Memory 限制**：

```bash
# 设置内存限制
echo 268435456 > /sys/fs/cgroup/my-container/memory.max
```

**IO 限制**：

```bash
# 设置 IO 权重
echo 500 > /sys/fs/cgroup/my-container/io.weight
```

## 6. OverlayFS 文件系统

### 6.1 OverlayFS 架构

**OverlayFS 层次结构**：

```text
upperdir (可写层)
    ↑
lowerdir (只读层)
    ↓
merged (合并视图)
```

**实现**：

```bash
# 挂载 OverlayFS
mount -t overlay overlay \
  -o lowerdir=lower,upperdir=upper,workdir=work \
  merged
```

### 6.2 镜像层化

**镜像层结构**：

```json
{
  "layers": ["sha256:base-layer", "sha256:app-layer", "sha256:config-layer"],
  "config": {
    "Cmd": ["/bin/sh"],
    "Env": ["PATH=/usr/bin"],
    "WorkingDir": "/app"
  }
}
```

**层合并**：

```bash
# 合并层
lowerdir=layer1:layer2:layer3
upperdir=writable
merged=final
```

## 7. 网络管理

### 7.1 CNI (Container Network Interface)

**CNI 插件**：

- **bridge**：桥接网络
- **host-local**：本地 IP 分配
- **portmap**：端口映射
- **firewall**：防火墙规则

**CNI 配置**：

```json
{
  "cniVersion": "0.4.0",
  "name": "mynet",
  "type": "bridge",
  "bridge": "cni0",
  "ipam": {
    "type": "host-local",
    "subnet": "10.22.0.0/16"
  }
}
```

### 7.2 网络模式

**Bridge 模式**：

- 容器连接到虚拟网桥
- 通过 NAT 访问外部网络
- 默认网络模式

**Host 模式**：

- 容器共享宿主机网络
- 直接使用宿主机网络接口
- 性能最高

**None 模式**：

- 容器没有网络接口
- 需要手动配置网络
- 用于特殊场景

## 8. 容器运行时实现

### 8.1 containerd

**架构**：

```text
containerd
├─ CRI Plugin (Kubernetes 接口)
├─ Runtime Plugin (runc, Kata, gVisor)
├─ Image Service (镜像管理)
├─ Content Service (内容存储)
└─ Metadata Service (元数据管理)
```

**特点**：

- 轻量级运行时
- 支持多种运行时后端
- 完整的镜像管理

### 8.2 cri-o

**架构**：

```text
cri-o
├─ CRI Interface (Kubernetes 接口)
├─ Runtime (runc, crun)
├─ Image Service (镜像管理)
└─ Storage Service (存储管理)
```

**特点**：

- 专为 Kubernetes 设计
- 轻量级实现
- 快速启动

### 8.3 runc

**架构**：

```text
runc
├─ OCI Runtime Spec (OCI 标准)
├─ Namespace Management (命名空间管理)
├─ Cgroup Management (资源控制)
└─ Process Management (进程管理)
```

**特点**：

- OCI 标准实现
- 轻量级运行时
- 广泛采用

## 9. 性能优化

### 9.1 启动时间优化

**优化策略**：

1. **镜像层缓存**：复用基础镜像层
2. **延迟挂载**：按需挂载文件系统
3. **进程预启动**：预热容器进程
4. **镜像压缩**：减小镜像大小

**优化效果**：

- 镜像拉取时间：从 10 s → 2 s
- 容器启动时间：从 1 s → 200 ms

### 9.2 资源利用率优化

**优化策略**：

1. **Cgroup v2**：统一资源控制
2. **资源配额**：精确的资源限制
3. **资源回收**：及时释放资源
4. **资源预测**：基于历史数据预测

**优化效果**：

- 资源利用率：从 50% → 70%
- 资源浪费：从 30% → 10%

## 10. 安全加固

### 10.1 安全策略

**Seccomp**：

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "syscalls": [
    {
      "names": ["read", "write"],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

**AppArmor**：

```bash
# 加载 AppArmor 配置文件
apparmor_parser -r /etc/apparmor.d/my-container
```

**SELinux**：

```bash
# 设置 SELinux 上下文
chcon -t container_file_t /var/lib/containers/my-container
```

### 10.2 镜像安全

**镜像扫描**：

- Trivy：镜像漏洞扫描
- Clair：镜像安全分析
- Falco：运行时安全监控

**镜像签名**：

- Notary：镜像签名和验证
- Cosign：镜像签名工具

## 11. 可观测性

### 11.1 指标监控

**cAdvisor**：

- 容器资源使用指标
- CPU、内存、网络、IO 统计

**Prometheus**：

- 指标收集和存储
- 查询和告警

### 11.2 日志聚合

**容器日志**：

- stdout/stderr 日志
- 日志驱动（json-file, syslog, journald）

**日志聚合**：

- Fluentd：日志收集
- Loki：日志聚合
- ELK：日志分析

## 12. 总结

容器运行时层是云原生架构的核心组件，提供了：

1. **资源隔离**：Namespace 和 Cgroup 隔离
2. **快速启动**：< 1 s 启动时间
3. **镜像管理**：层化镜像和 OverlayFS
4. **网络管理**：CNI 插件和网络模式
5. **安全加固**：Seccomp、AppArmor、SELinux
6. **可观测性**：cAdvisor、Prometheus、日志聚合

通过这些特性，容器运行时层实现了从 VM 到 Container 的抽象，为上层应用提供了轻量
级、快速、安全的运行环境。

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第 3 节
