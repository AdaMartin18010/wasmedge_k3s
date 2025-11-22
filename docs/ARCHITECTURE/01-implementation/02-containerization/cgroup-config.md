# cgroup 配置示例

## 📑 目录

- [cgroup 配置示例](#cgroup-配置示例)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 理论基础](#11-理论基础)
  - [2 cgroup v2 配置示例](#2-cgroup-v2-配置示例)
    - [2.1 创建 cgroup](#21-创建-cgroup)
    - [2.2 cgroup 配置文件示例](#22-cgroup-配置文件示例)
  - [3 systemd cgroup 配置](#3-systemd-cgroup-配置)
    - [3.1 systemd 服务单元配置](#31-systemd-服务单元配置)
    - [3.2 systemd 切片配置](#32-systemd-切片配置)
  - [4 Docker cgroup 配置](#4-docker-cgroup-配置)
    - [4.1 Docker 容器资源限制](#41-docker-容器资源限制)
    - [4.2 docker-compose 资源限制](#42-docker-compose-资源限制)
    - [4.3 Kubernetes Pod 资源限制](#43-kubernetes-pod-资源限制)
  - [5 相关文档](#5-相关文档)
    - [5.1 理论论证](#51-理论论证)
    - [5.2 架构视角](#52-架构视角)
    - [5.3 技术文档](#53-技术文档)
  - [6 2025 年最新实践](#6-2025-年最新实践)
    - [6.1 Cgroup v2 全面采用（2025）](#61-cgroup-v2-全面采用2025)
    - [6.2 Kubernetes 1.30+ Cgroup 增强（2025）](#62-kubernetes-130-cgroup-增强2025)
    - [6.3 systemd 250+ Cgroup 管理（2025）](#63-systemd-250-cgroup-管理2025)
  - [7 实际应用案例](#7-实际应用案例)
    - [案例 1：多租户资源隔离](#案例-1多租户资源隔离)
    - [案例 2：高性能计算任务](#案例-2高性能计算任务)
    - [案例 3：数据库容器资源管理](#案例-3数据库容器资源管理)
  - [8 使用指南](#8-使用指南)
    - [8.1 快速开始](#81-快速开始)
    - [8.2 使用技巧](#82-使用技巧)
      - [资源限制设置](#资源限制设置)
      - [配置最佳实践](#配置最佳实践)
    - [8.3 常见问题](#83-常见问题)
    - [8.4 实践建议](#84-实践建议)

---

## 1 概述

本文档提供 **cgroup 的实际配置示例**，展示如何通过 cgroup 控制容器的资源使用。

### 1.1 理论基础

cgroup 配置基于以下理论论证：

- **公理 A2（OS 资源封闭）**：进程、内存、文件、网络四大命名空间可完全封闭
- **归纳映射 Ψ₂（容器化层）**：通过 cgroup 实现资源隔离和限制

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2 cgroup v2 配置示例

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

## 3 systemd cgroup 配置

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

## 4 Docker cgroup 配置

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

## 5 相关文档

### 5.1 理论论证

- **`../../00-theory/02-induction-proof/psi2-containerization.md`** - 容器化层归
  纳映射
- **`../../00-theory/01-axioms/A2-os-resource.md`** - OS 资源封闭公理

### 5.2 架构视角

- **`../../02-views/10-quick-views/containerization-view.md`** - 容器化架构视角

### 5.3 技术文档

- **`../../../TECHNICAL/01-core-foundations/docker/docker.md`** - Docker 技术文
  档

## 6 2025 年最新实践

### 6.1 Cgroup v2 全面采用（2025）

**2025 年趋势**：Cgroup v2 已成为主流

**采用情况**：

- **Kubernetes 1.25+**：默认使用 Cgroup v2
- **Docker 24.0+**：默认使用 Cgroup v2
- **systemd 250+**：默认使用 Cgroup v2

**检查 Cgroup 版本**：

```bash
# 检查 Cgroup 版本
stat -fc %T /sys/fs/cgroup/
# 输出 "cgroup2fs" 表示使用 Cgroup v2

# 检查可用控制器
cat /sys/fs/cgroup/cgroup.controllers
# 输出：cpuset cpu io memory hugetlb pids rdma misc
```

### 6.2 Kubernetes 1.30+ Cgroup 增强（2025）

**Kubernetes 1.30+ 新特性**：

- **Cgroup v2 完整支持**：所有功能基于 Cgroup v2
- **资源配额增强**：更精确的资源限制
- **性能优化**：减少 Cgroup 操作开销

**配置示例**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-limited-pod
spec:
  containers:
  - name: app
    image: nginx
    resources:
      requests:
        cpu: "500m"
        memory: "256Mi"
      limits:
        cpu: "1000m"
        memory: "512Mi"
    # Cgroup v2 配置
    securityContext:
      cgroupPolicy: "Restricted"  # 使用受限的 Cgroup 策略
```

### 6.3 systemd 250+ Cgroup 管理（2025）

**systemd 250+ 新特性**：

- **统一 Cgroup 管理**：systemd 统一管理所有 Cgroup
- **资源限制增强**：更灵活的资源配置
- **性能监控**：内置资源使用监控

**配置示例**：

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application

[Service]
Type=simple
ExecStart=/usr/bin/myapp
# Cgroup v2 资源限制
CPUQuota=50%
MemoryMax=512M
IOWeight=100
```

## 7 实际应用案例

### 案例 1：多租户资源隔离

**场景**：在 Kubernetes 集群中实现多租户资源隔离

**实现方案**：

```yaml
# 租户 A 的 Pod
apiVersion: v1
kind: Pod
metadata:
  name: tenant-a-pod
  namespace: tenant-a
spec:
  containers:
  - name: app
    image: nginx
    resources:
      requests:
        cpu: "1"
        memory: "1Gi"
      limits:
        cpu: "2"
        memory: "2Gi"

---
# 租户 B 的 Pod
apiVersion: v1
kind: Pod
metadata:
  name: tenant-b-pod
  namespace: tenant-b
spec:
  containers:
  - name: app
    image: nginx
    resources:
      requests:
        cpu: "1"
        memory: "1Gi"
      limits:
        cpu: "2"
        memory: "2Gi"
```

**效果**：

- 资源隔离：每个租户有独立的资源配额
- 公平调度：Kubernetes 根据 requests 进行调度
- 资源限制：limits 防止资源滥用

### 案例 2：高性能计算任务

**场景**：运行 CPU 密集型计算任务，需要精确的 CPU 控制

**实现方案**：

```bash
# 创建专用的 Cgroup
mkdir -p /sys/fs/cgroup/app

# 设置 CPU 限制（2 核）
echo "200000 100000" > /sys/fs/cgroup/app/cpu.max
# 格式：quota period (200000 = 2 核，100000 = 1 秒)

# 设置内存限制（4GB）
echo "4G" > /sys/fs/cgroup/app/memory.max

# 将进程加入 Cgroup
echo $$ > /sys/fs/cgroup/app/cgroup.procs

# 运行计算任务
./compute-intensive-task
```

**Kubernetes 配置**：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: compute-job
spec:
  template:
    spec:
      containers:
      - name: compute
        image: compute-tool:latest
        resources:
          requests:
            cpu: "2"
            memory: "4Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
      restartPolicy: Never
```

**效果**：

- CPU 控制：精确控制 CPU 使用率
- 内存限制：防止内存溢出
- 性能稳定：保证任务性能一致性

### 案例 3：数据库容器资源管理

**场景**：运行数据库容器，需要稳定的 IO 性能

**实现方案**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: database-pod
spec:
  containers:
  - name: postgres
    image: postgres:15
    resources:
      requests:
        cpu: "2"
        memory: "4Gi"
      limits:
        cpu: "4"
        memory: "8Gi"
    # IO 限制（Cgroup v2）
    securityContext:
      # 通过 annotations 设置 IO 限制
      annotations:
        io.kubernetes.cri-o/IOWeight: "500"  # IO 权重
```

**直接 Cgroup 配置**：

```bash
# 设置数据库容器的 IO 权重
echo 500 > /sys/fs/cgroup/kubepods/pod-xxx/container-xxx/io.weight

# 设置 IO 限制
echo "8:0 rbps=10485760 wbps=10485760" > /sys/fs/cgroup/kubepods/pod-xxx/container-xxx/io.max
```

**效果**：

- 资源保证：requests 保证最小资源
- 性能上限：limits 防止资源耗尽
- IO 控制：通过 IO 权重控制 IO 性能

---

## 8 使用指南

### 8.1 快速开始

**适用场景**：

- 需要限制容器资源使用
- 多租户环境资源隔离
- 性能优化和资源管理

**快速步骤**：

1. **检查 Cgroup 版本**：

   ```bash
   stat -fc %T /sys/fs/cgroup/
   # 输出 "cgroup2fs" 表示使用 Cgroup v2
   ```

2. **选择配置方式**：
   - **直接配置**：使用 `cgroup v2` 直接配置（适合系统级配置）
   - **systemd 配置**：使用 systemd 服务单元（适合服务管理）
   - **Docker 配置**：使用 Docker 资源限制（适合容器部署）
   - **Kubernetes 配置**：使用 Pod 资源限制（适合 Kubernetes 集群）

3. **应用配置**：根据实际场景选择对应的配置示例

### 8.2 使用技巧

#### 资源限制设置

**CPU 限制**：

- **requests**：保证最小 CPU 资源，用于调度决策
- **limits**：限制最大 CPU 使用，防止资源耗尽
- **建议**：requests 设置为预期平均使用量，limits 设置为峰值使用量

**内存限制**：

- **requests**：保证最小内存资源
- **limits**：限制最大内存使用，超过会被 OOM Killer 终止
- **建议**：limits 设置为 requests 的 1.5-2 倍

**IO 限制**：

- **IOWeight**：设置 IO 权重，影响 IO 优先级
- **io.max**：设置 IO 带宽限制
- **建议**：数据库等 IO 密集型应用设置较高 IOWeight

#### 配置最佳实践

1. **渐进式配置**：从宽松的限制开始，逐步收紧
2. **监控调整**：持续监控资源使用，根据实际情况调整
3. **预留缓冲**：limits 应略大于实际峰值，避免频繁限制
4. **统一管理**：使用 Kubernetes 或 systemd 统一管理资源

### 8.3 常见问题

**Q1：如何验证 Cgroup 配置是否生效？**

```bash
# 检查进程的 Cgroup
cat /proc/$$/cgroup

# 检查 Cgroup 资源使用
cat /sys/fs/cgroup/myapp/cpu.stat
cat /sys/fs/cgroup/myapp/memory.current
```

**Q2：容器内存超限如何处理？**

- 检查内存 limits 是否合理
- 优化应用内存使用
- 考虑增加 limits 或调整 requests

**Q3：如何实现动态资源调整？**

- Kubernetes：使用 Vertical Pod Autoscaler (VPA)
- systemd：修改服务单元配置后 reload
- 直接配置：修改 Cgroup 文件后重新加载

### 8.4 实践建议

**多租户环境**：

- 使用 Namespace 和 ResourceQuota 实现租户隔离
- 设置合理的 requests 和 limits
- 监控租户资源使用情况

**高性能计算**：

- 使用 CPU 亲和性（cpuset）绑定 CPU
- 设置精确的 CPU 和内存限制
- 考虑 NUMA 拓扑优化

**数据库应用**：

- 设置较高的 IOWeight
- 保证稳定的内存资源
- 使用 IO 带宽限制防止 IO 竞争

---

**更新时间**：2025-11-15 **版本**：v1.2 **状态**：✅ 包含使用指南和 2025 年最新实践
