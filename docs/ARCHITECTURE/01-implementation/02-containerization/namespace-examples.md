# namespace 示例

## 📑 目录

- [1. 概述](#1-概述)
- [2. Linux namespace 类型](#2-linux-namespace-类型)
- [3. namespace 创建示例](#3-namespace-创建示例)
- [4. Docker namespace 示例](#4-docker-namespace-示例)
- [5. Kubernetes namespace 示例](#5-kubernetes-namespace-示例)
- [6. 相关文档](#6-相关文档)

---

## 1. 概述

本文档提供 **Linux namespace 的实际代码示例**，展示如何通过 namespace 实现进程隔
离。

### 1.1 理论基础

namespace 配置基于以下理论论证：

- **公理 A2（OS 资源封闭）**：进程、内存、文件、网络四大命名空间可完全封闭
- **归纳映射 Ψ₂（容器化层）**：通过 namespace 实现进程隔离

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2. Linux namespace 类型

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

## 3. namespace 创建示例

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

## 4. Docker namespace 示例

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

## 5. Kubernetes namespace 示例

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

## 6. 相关文档

### 6.1 理论论证

- **`../../00-theory/02-induction-proof/psi2-containerization.md`** - 容器化层归
  纳映射
- **`../../00-theory/01-axioms/A2-os-resource.md`** - OS 资源封闭公理

### 6.2 架构视角

- **`../../01-views/containerization-view.md`** - 容器化架构视角

### 6.3 技术文档

- **`../../../TECHNICAL/29-isolation-stack/isolation-stack.md`** - 隔离技术栈文
  档

---

**更新时间**：2025-11-04 **版本**：v1.0 **状态**：✅ 基础示例已创建
