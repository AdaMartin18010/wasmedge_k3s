# namespace 示例

## 📑 目录

- [namespace 示例](#namespace-示例)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 理论基础](#11-理论基础)
  - [2 Linux namespace 类型](#2-linux-namespace-类型)
  - [3 namespace 创建示例](#3-namespace-创建示例)
    - [3.1 使用 unshare 创建 namespace](#31-使用-unshare-创建-namespace)
    - [3.2 使用 clone 系统调用创建 namespace](#32-使用-clone-系统调用创建-namespace)
    - [3.3 查看 namespace](#33-查看-namespace)
  - [4 Docker namespace 示例](#4-docker-namespace-示例)
    - [4.1 Docker 容器 namespace 配置](#41-docker-容器-namespace-配置)
    - [4.2 Docker 容器 namespace 检查](#42-docker-容器-namespace-检查)
    - [4.3 Docker Compose namespace 配置](#43-docker-compose-namespace-配置)
  - [5 Kubernetes namespace 示例](#5-kubernetes-namespace-示例)
    - [5.1 Kubernetes Pod namespace 配置](#51-kubernetes-pod-namespace-配置)
    - [5.2 Kubernetes SecurityContext namespace 配置](#52-kubernetes-securitycontext-namespace-配置)
    - [5.3 Kubernetes NetworkPolicy namespace 配置](#53-kubernetes-networkpolicy-namespace-配置)
  - [6 相关文档](#6-相关文档)
    - [6.1 理论论证](#61-理论论证)
    - [6.2 架构视角](#62-架构视角)
    - [6.3 技术文档](#63-技术文档)
  - [7 2025 年最新实践](#7-2025-年最新实践)
    - [7.1 Linux 6.1+ Namespace 增强（2025）](#71-linux-61-namespace-增强2025)
    - [7.2 containerd 2.0+ Namespace 管理（2025）](#72-containerd-20-namespace-管理2025)
    - [7.3 Kubernetes 1.30+ Namespace 支持（2025）](#73-kubernetes-130-namespace-支持2025)
  - [8 实际应用案例](#8-实际应用案例)
    - [案例 1：多租户容器隔离](#案例-1多租户容器隔离)
    - [案例 2：高性能网络应用](#案例-2高性能网络应用)
    - [案例 3：容器化 CI/CD 系统](#案例-3容器化-cicd-系统)

---

## 1 概述

本文档提供 **Linux namespace 的实际代码示例**，展示如何通过 namespace 实现进程隔
离。

### 1.1 理论基础

namespace 配置基于以下理论论证：

- **公理 A2（OS 资源封闭）**：进程、内存、文件、网络四大命名空间可完全封闭
- **归纳映射 Ψ₂（容器化层）**：通过 namespace 实现进程隔离

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2 Linux namespace 类型

Linux 提供了以下 namespace 类型：

| namespace 类型 | 隔离资源       | 说明                   |
| -------------- | -------------- | ---------------------- |
| **PID**        | 进程 ID        | 进程只能看到自己的 PID |
| **Network**    | 网络设备、端口 | 独立的网络栈           |
| **Mount**      | 文件系统挂载点 | 独立的文件系统视图     |
| **IPC**        | 进程间通信     | 独立的 IPC 资源        |
| **UTS**        | 主机名和域名   | 独立的主机名           |
| **User**       | 用户和组 ID    | 独立的用户命名空间     |
| **Cgroup**     | cgroup 根目录  | 独立的 cgroup 层次结构 |

---

## 3 namespace 创建示例

### 3.1 使用 unshare 创建 namespace

```bash
# 创建新的 PID namespace
unshare --pid --fork bash

# 创建新的 Network namespace
unshare --net bash

# 创建新的 Mount namespace
unshare --mount bash

# 创建多个 namespace
unshare --pid --net --mount --fork bash
```

### 3.2 使用 clone 系统调用创建 namespace

```c
#define _GNU_SOURCE
#include <sched.h>
#include <sys/wait.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// 创建新的 PID namespace
int main() {
    pid_t pid = clone(child_func,
                     child_stack + STACK_SIZE,
                     CLONE_NEWPID | SIGCHLD,
                     NULL);

    waitpid(pid, NULL, 0);
    return 0;
}

int child_func(void *arg) {
    printf("Child PID: %d\n", getpid());
    return 0;
}
```

### 3.3 查看 namespace

```bash
# 查看进程的 namespace
ls -la /proc/$$/ns/

# 输出示例：
# lrwxrwxrwx 1 root root 0 Nov  4 10:00 pid -> pid:[4026531836]
# lrwxrwxrwx 1 root root 0 Nov  4 10:00 net -> net:[4026532008]
# lrwxrwxrwx 1 root root 0 Nov  4 10:00 mnt -> mnt:[4026531840]
```

---

## 4 Docker namespace 示例

### 4.1 Docker 容器 namespace 配置

```bash
# 运行容器时指定 namespace
docker run -d \
  --pid=host \
  --network=bridge \
  --uts=host \
  --name myapp \
  myapp:v1.0
```

### 4.2 Docker 容器 namespace 检查

```bash
# 查看容器的 namespace
docker inspect <container-id> | grep -i namespace

# 进入容器查看 namespace
docker exec <container-id> ls -la /proc/self/ns/
```

### 4.3 Docker Compose namespace 配置

```yaml
version: "3.8"

services:
  app:
    image: myapp:v1.0
    pid: "host" # 共享主机 PID namespace
    network_mode: "bridge" # 使用桥接网络
    uts: "host" # 共享主机 UTS namespace
```

---

## 5 Kubernetes namespace 示例

### 5.1 Kubernetes Pod namespace 配置

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  hostNetwork: false # 使用 Pod 网络 namespace
  hostPID: false # 使用 Pod PID namespace
  hostIPC: false # 使用 Pod IPC namespace
  containers:
    - name: app
      image: myapp:v1.0
```

### 5.2 Kubernetes SecurityContext namespace 配置

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
  containers:
    - name: app
      image: myapp:v1.0
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        capabilities:
          drop:
            - ALL
          add:
            - NET_BIND_SERVICE
```

### 5.3 Kubernetes NetworkPolicy namespace 配置

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: myapp-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: frontend
      ports:
        - protocol: TCP
          port: 8080
```

---

## 6 相关文档

### 6.1 理论论证

- **`../../00-theory/02-induction-proof/psi2-containerization.md`** - 容器化层归
  纳映射
- **`../../00-theory/01-axioms/A2-os-resource.md`** - OS 资源封闭公理

### 6.2 架构视角

- **`../../02-views/10-quick-views/containerization-view.md`** - 容器化架构视角

### 6.3 技术文档

- **`../../../TECHNICAL/08-architecture-analysis/isolation-stack/isolation-stack.md`** -
  隔离技术栈文档

## 7 2025 年最新实践

### 7.1 Linux 6.1+ Namespace 增强（2025）

**最新内核版本**：Linux 6.1+（2025 年）

**新特性**：

- **Time Namespace 增强**：支持更精确的时间隔离
- **User Namespace 改进**：更好的安全性和性能
- **PID Namespace 优化**：减少嵌套 Namespace 的开销

**使用示例**：

```bash
# 创建 Time Namespace（Linux 5.6+）
unshare --time --fork bash

# 设置时间偏移
echo "1000000000 0" > /proc/self/timens_offsets
```

### 7.2 containerd 2.0+ Namespace 管理（2025）

**containerd 2.0+ 新特性**：

- **统一 Namespace 管理**：更好的 Namespace 生命周期管理
- **性能优化**：减少 Namespace 创建和销毁的开销
- **安全增强**：默认启用 User Namespace

**配置示例**：

```toml
# /etc/containerd/config.toml
version = 2

[plugins."io.containerd.grpc.v1.cri"]
  # 启用 User Namespace（2025 推荐）
  enable_userns = true

  [plugins."io.containerd.grpc.v1.cri".containerd]
    default_runtime_name = "runc"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
      runtime_type = "io.containerd.runc.v2"
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
        SystemdCgroup = true
```

### 7.3 Kubernetes 1.30+ Namespace 支持（2025）

**Kubernetes 1.30+ 新特性**：

- **User Namespace 支持**：Pod 级别的 User Namespace
- **Network Namespace 共享**：支持 Pod 内容器共享 Network Namespace
- **PID Namespace 共享**：支持 Pod 内容器共享 PID Namespace

**配置示例**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: shared-ns-pod
spec:
  shareProcessNamespace: true  # 共享 PID Namespace
  shareNetworkNamespace: true  # 共享 Network Namespace
  containers:
  - name: app1
    image: nginx
  - name: app2
    image: nginx
```

## 8 实际应用案例

### 案例 1：多租户容器隔离

**场景**：在 Kubernetes 集群中实现多租户隔离

**实现方案**：

```yaml
# 使用 User Namespace 实现租户隔离
apiVersion: v1
kind: Pod
metadata:
  name: tenant-a-app
  namespace: tenant-a
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
  containers:
  - name: app
    image: nginx
    securityContext:
      # 移除不必要的 Capabilities
      capabilities:
        drop:
          - ALL
        add:
          - NET_BIND_SERVICE
```

**效果**：

- 租户隔离：每个租户有独立的 User Namespace
- 安全性：减少容器逃逸风险
- 资源隔离：通过 Namespace 实现资源隔离

### 案例 2：高性能网络应用

**场景**：部署高性能网络应用，需要独立的 Network Namespace

**实现方案**：

```bash
# 创建独立的 Network Namespace
ip netns add app-ns

# 配置网络接口
ip link add veth0 type veth peer name veth1
ip link set veth0 netns app-ns
ip netns exec app-ns ip addr add 10.0.0.1/24 dev veth0
ip netns exec app-ns ip link set veth0 up

# 在 Network Namespace 中运行应用
ip netns exec app-ns /usr/bin/myapp
```

**Kubernetes 配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: network-app
spec:
  hostNetwork: false  # 使用独立的 Network Namespace
  containers:
  - name: app
    image: nginx
```

**效果**：

- 网络隔离：应用有独立的网络栈
- 性能优化：减少网络干扰
- 安全性：网络流量隔离

### 案例 3：容器化 CI/CD 系统

**场景**：在容器中运行 CI/CD 任务，需要隔离的进程树

**实现方案**：

```yaml
# Kubernetes Job 配置
apiVersion: batch/v1
kind: Job
metadata:
  name: ci-job
spec:
  template:
    spec:
      # 使用独立的 PID Namespace
      shareProcessNamespace: false
      containers:
      - name: builder
        image: build-tool:latest
        securityContext:
          # 移除不必要的 Capabilities
          capabilities:
            drop:
              - ALL
```

**效果**：

- 进程隔离：每个 CI/CD 任务有独立的进程树
- 安全性：任务之间完全隔离
- 资源控制：通过 Cgroup 限制资源使用

---

**更新时间**：2025-11-15 **版本**：v1.1 **状态**：✅ 包含 2025 年最新实践
