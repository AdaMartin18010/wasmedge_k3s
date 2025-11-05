# cgroup 配置示例

## 📑 目录

- [1. 概述](#1-概述)
- [2. cgroup v2 配置示例](#2-cgroup-v2-配置示例)
- [3. systemd cgroup 配置](#3-systemd-cgroup-配置)
- [4. Docker cgroup 配置](#4-docker-cgroup-配置)
- [5. 相关文档](#5-相关文档)

---

## 1. 概述

本文档提供 **cgroup 的实际配置示例**，展示如何通过 cgroup 控制容器的资源使用。

### 1.1 理论基础

cgroup 配置基于以下理论论证：

- **公理 A2（OS 资源封闭）**：进程、内存、文件、网络四大命名空间可完全封闭
- **归纳映射 Ψ₂（容器化层）**：通过 cgroup 实现资源隔离和限制

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2. cgroup v2 配置示例

### 2.1 创建 cgroup

```bash
# 创建 cgroup
sudo mkdir -p /sys/fs/cgroup/myapp

# 设置 CPU 限制（50% CPU）
echo "50000 100000" | sudo tee /sys/fs/cgroup/myapp/cpu.max

# 设置内存限制（512MB）
echo "536870912" | sudo tee /sys/fs/cgroup/myapp/memory.max

# 添加进程到 cgroup
echo $$ | sudo tee /sys/fs/cgroup/myapp/cgroup.procs
```

### 2.2 cgroup 配置文件示例

```bash
# /etc/cgroup.conf
# CPU 限制
cpu.max=50000 100000

# 内存限制
memory.max=536870912

# IO 限制
io.max=8:16 rbps=1048576 wbps=1048576
```

---

## 3. systemd cgroup 配置

### 3.1 systemd 服务单元配置

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/myapp
Restart=always

# CPU 限制
CPUQuota=50%

# 内存限制
MemoryLimit=512M

# IO 限制
IOWeight=100
```

### 3.2 systemd 切片配置

```ini
# /etc/systemd/system/myapp.slice
[Unit]
Description=My Application Slice

[Slice]
CPUQuota=50%
MemoryLimit=512M
```

---

## 4. Docker cgroup 配置

### 4.1 Docker 容器资源限制

```bash
# 运行容器时设置资源限制
docker run -d \
  --cpus="0.5" \
  --memory="512m" \
  --memory-swap="512m" \
  --cpuset-cpus="0-1" \
  --name myapp \
  myapp:v1.0
```

### 4.2 docker-compose 资源限制

```yaml
version: "3.8"

services:
  app:
    image: myapp:v1.0
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 256M
```

### 4.3 Kubernetes Pod 资源限制

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: app
      image: myapp:v1.0
      resources:
        requests:
          memory: "256Mi"
          cpu: "250m"
        limits:
          memory: "512Mi"
          cpu: "500m"
```

---

## 5. 相关文档

### 5.1 理论论证

- **`../../00-theory/02-induction-proof/psi2-containerization.md`** - 容器化层归
  纳映射
- **`../../00-theory/01-axioms/A2-os-resource.md`** - OS 资源封闭公理

### 5.2 架构视角

- **`../../01-views/containerization-view.md`** - 容器化架构视角

### 5.3 技术文档

- **`../../../TECHNICAL/00-docker/docker.md`** - Docker 技术文档

---

**更新时间**：2025-11-04 **版本**：v1.0 **状态**：✅ 基础示例已创建
