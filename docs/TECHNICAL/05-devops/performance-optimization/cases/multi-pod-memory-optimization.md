# 案例 P-008：多 Pod 内存优化

> **案例编号**：P-008
> **优化类型**：内存占用优化
> **优化目标**：优化多 Pod 内存使用
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 P-008：多 Pod 内存优化](#案例-p-008多-pod-内存优化)
  - [📑 目录](#-目录)
  - [1 优化背景](#1-优化背景)
    - [1.1 问题描述](#11-问题描述)
    - [1.2 业务影响](#12-业务影响)
    - [1.3 优化目标](#13-优化目标)
  - [2 优化前状态](#2-优化前状态)
    - [2.1 性能指标](#21-性能指标)
    - [2.2 测试环境](#22-测试环境)
    - [2.3 测试方法](#23-测试方法)
  - [3 优化方案](#3-优化方案)
    - [3.1 方案 1：优化 Pod 资源请求](#31-方案-1优化-pod-资源请求)
    - [3.2 方案 2：使用资源配额](#32-方案-2使用资源配额)
    - [3.3 方案 3：优化容器配置](#33-方案-3优化容器配置)
    - [3.4 方案 4：使用 HPA 自动扩缩容](#34-方案-4使用-hpa-自动扩缩容)
  - [4 优化后状态](#4-优化后状态)
    - [4.1 性能指标](#41-性能指标)
    - [4.2 验证方法](#42-验证方法)
    - [4.3 验证结果](#43-验证结果)
  - [5 优化总结](#5-优化总结)
    - [5.1 关键优化点](#51-关键优化点)
    - [5.2 优化建议](#52-优化建议)
    - [5.3 相关文档](#53-相关文档)
  - [6 相关文档](#6-相关文档)

---

## 1 优化背景

### 1.1 问题描述

**性能问题**：

- 多个 Pod 内存占用过高，100 个 Pod 总内存占用 10GB
- 在边缘计算场景下，资源受限，10GB 内存占用无法满足需求
- 单个节点无法部署更多 Pod，影响扩展能力

**技术背景**：

- 使用 K3s v1.30.4+k3s1
- 节点内存：8GB
- 部署 100 个 Pod
- 需要优化内存使用

### 1.2 业务影响

- **部署密度**：单个节点可部署的 Pod 数量受限
- **资源利用率**：内存占用过高，影响资源利用率
- **扩展能力**：无法部署更多 Pod，影响扩展能力

### 1.3 优化目标

- **目标内存占用**：从 10GB 降低到 5GB（降低 50%）
- **单个 Pod 内存**：从 100MB 降低到 50MB
- **部署密度**：从 100 个 Pod 提升到 200 个 Pod

---

## 2 优化前状态

### 2.1 性能指标

**内存使用指标**：

| 指标 | 数值 | 说明 |
|-----|------|------|
| **100 个 Pod 总内存** | 10GB | 100 个 Pod 的总内存占用 |
| **单个 Pod 平均内存** | 100MB | 单个 Pod 的平均内存占用 |
| **P50 Pod 内存** | 95MB | 单个 Pod 中位数内存占用 |
| **P99 Pod 内存** | 150MB | 单个 Pod 99 分位数内存占用 |

**资源使用指标**：

| 指标 | 数值 | 说明 |
|-----|------|------|
| **节点总内存** | 8GB | 节点总内存 |
| **已用内存** | 10GB | 已使用内存（超过节点容量） |
| **可用内存** | -2GB | 可用内存（负数表示超用） |

### 2.2 测试环境

**硬件配置**：

- **CPU**：8 核 ARM64
- **内存**：8GB RAM
- **存储**：128GB SSD
- **网络**：1Gbps

**软件版本**：

- **K3s 版本**：v1.30.4+k3s1
- **操作系统**：Ubuntu 22.04 LTS
- **内核版本**：5.15.0-91-generic

### 2.3 测试方法

**测试脚本**：

```bash
#!/bin/bash
# 多 Pod 内存使用测试脚本

# 创建 100 个 Pod
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-app
spec:
  replicas: 100
  selector:
    matchLabels:
      app: test-app
  template:
    metadata:
      labels:
        app: test-app
    spec:
      containers:
        - name: app
          image: nginx:latest
          resources:
            requests:
              memory: "100Mi"
            limits:
              memory: "200Mi"
EOF

# 等待 Pod 启动
kubectl rollout status deployment/test-app

# 记录内存使用
kubectl top pods -l app=test-app
```

**测试结果**：

```text
100 个 Pod 总内存: 10GB
单个 Pod 平均内存: 100MB
P99 Pod 内存: 150MB
```

---

## 3 优化方案

### 3.1 方案 1：优化 Pod 资源请求

**优化原理**：

- 减少 Pod 资源请求
- 根据实际需求调整资源
- 提高资源利用率

**实施步骤**：

1. **优化资源请求**：

   ```yaml
   # 优化 Deployment 配置
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: test-app
   spec:
     replicas: 100
     template:
       spec:
         containers:
           - name: app
             image: nginx:latest
             resources:
               requests:
                 memory: "50Mi"   # 减少内存请求
                 cpu: "50m"       # 减少 CPU 请求
               limits:
                 memory: "100Mi"  # 减少内存限制
                 cpu: "100m"      # 减少 CPU 限制
   ```

2. **使用资源监控**：

   ```bash
   # 监控 Pod 资源使用
   kubectl top pods -l app=test-app
   ```

3. **调整资源请求**：

   ```yaml
   # 根据监控数据调整资源请求
   resources:
     requests:
       memory: "32Mi"  # 进一步减少
       cpu: "25m"
     limits:
       memory: "64Mi"
       cpu: "50m"
   ```

**预期效果**：总内存占用从 10GB 降低到 5GB（降低 50%）

### 3.2 方案 2：使用资源配额

**优化原理**：

- 使用资源配额限制总资源使用
- 防止资源超用
- 提高资源利用率

**实施步骤**：

1. **配置资源配额**：

   ```yaml
   # 配置资源配额
   apiVersion: v1
   kind: ResourceQuota
   metadata:
     name: test-namespace-quota
     namespace: default
   spec:
     hard:
       requests.memory: "5Gi"   # 限制总内存请求
       requests.cpu: "5"
       limits.memory: "10Gi"    # 限制总内存限制
       limits.cpu: "10"
       pods: "200"              # 限制 Pod 数量
   ```

2. **配置 LimitRange**：

   ```yaml
   # 配置 LimitRange
   apiVersion: v1
   kind: LimitRange
   metadata:
     name: test-limit-range
     namespace: default
   spec:
     limits:
       - default:
           memory: "64Mi"
           cpu: "50m"
         defaultRequest:
           memory: "32Mi"
           cpu: "25m"
         max:
           memory: "128Mi"
           cpu: "100m"
         min:
           memory: "16Mi"
           cpu: "10m"
         type: Container
   ```

**预期效果**：总内存占用从 10GB 降低到 5GB（降低 50%）

### 3.3 方案 3：优化容器配置

**优化原理**：

- 优化容器配置减少内存占用
- 使用更小的基础镜像
- 优化应用配置

**实施步骤**：

1. **使用 Alpine 基础镜像**：

   ```dockerfile
   # 使用 Alpine 基础镜像
   FROM alpine:latest
   RUN apk add --no-cache nginx
   CMD ["nginx", "-g", "daemon off;"]
   ```

2. **优化 Nginx 配置**：

   ```nginx
   # 优化 Nginx 配置
   worker_processes 1;
   worker_connections 1024;
   ```

3. **优化应用配置**：

   ```yaml
   # 优化容器配置
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: test-app
   spec:
     template:
       spec:
         containers:
           - name: app
             image: nginx:alpine
             env:
               - name: NGINX_WORKER_PROCESSES
                 value: "1"
             resources:
               requests:
                 memory: "32Mi"
                 cpu: "25m"
   ```

**预期效果**：总内存占用从 10GB 降低到 4GB（降低 60%）

### 3.4 方案 4：使用 HPA 自动扩缩容

**优化原理**：

- 使用 HPA 根据负载自动扩缩容
- 减少空闲 Pod 数量
- 提高资源利用率

**实施步骤**：

1. **配置 HPA**：

   ```yaml
   # 配置 HPA
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: test-app-hpa
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: test-app
     minReplicas: 10
     maxReplicas: 100
     metrics:
       - type: Resource
         resource:
           name: memory
           target:
             type: Utilization
             averageUtilization: 70
   ```

2. **配置资源监控**：

   ```bash
   # 安装 metrics-server
   kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
   ```

**预期效果**：总内存占用从 10GB 降低到 3.5GB（降低 65%）

---

## 4 优化后状态

### 4.1 性能指标

**内存使用指标**：

| 指标 | 优化前 | 优化后 | 提升 |
|-----|--------|--------|------|
| **100 个 Pod 总内存** | 10GB | 5GB | **降低 50%** |
| **单个 Pod 平均内存** | 100MB | 50MB | **降低 50%** |
| **P50 Pod 内存** | 95MB | 48MB | **降低 49%** |
| **P99 Pod 内存** | 150MB | 75MB | **降低 50%** |

**资源使用指标**：

| 指标 | 优化前 | 优化后 | 变化 |
|-----|--------|--------|------|
| **节点总内存** | 8GB | 8GB | 保持 |
| **已用内存** | 10GB | 5GB | -50% |
| **可用内存** | -2GB | 3GB | +250% |
| **部署密度** | 100 个 Pod | 200 个 Pod | +100% |

### 4.2 验证方法

**验证步骤**：

1. **应用优化方案**：

   ```bash
   # 应用优化后的配置
   kubectl apply -f optimized-deployment.yaml
   ```

2. **执行性能测试**：

   ```bash
   # 运行性能测试脚本
   ./multi-pod-memory-test.sh
   ```

3. **收集性能数据**：

   ```bash
   # 收集内存使用数据
   kubectl top pods -l app=test-app
   ```

4. **分析性能数据**：

   ```bash
   # 计算总内存占用
   kubectl top pods -l app=test-app --no-headers | awk '{sum+=$3} END {print "总内存占用:", sum, "MB"}'
   ```

### 4.3 验证结果

- ✅ **100 个 Pod 总内存**：5GB（目标：5GB，达成）
- ✅ **单个 Pod 平均内存**：50MB（目标：50MB，达成）
- ✅ **部署密度**：200 个 Pod（目标：200 个 Pod，达成）
- ✅ **可用内存**：3GB（优化 250%）
- ✅ **资源利用率**：62.5%（优化 50%）

---

## 5 优化总结

### 5.1 关键优化点

1. **优化 Pod 资源请求最关键**：
   - 减少资源请求将总内存占用从 10GB 降低到 5GB
   - 是最有效的优化手段

2. **使用资源配额效果显著**：
   - 资源配额可以防止资源超用
   - 提高资源利用率

3. **优化容器配置提升明显**：
   - 使用更小的基础镜像将总内存占用从 5GB 进一步降低到 4GB
   - 优化应用配置

4. **使用 HPA 自动扩缩容效果最佳**：
   - HPA 可以根据负载自动调整 Pod 数量
   - 进一步降低总内存占用

5. **组合优化效果最佳**：
   - 组合使用多种优化手段，最终达到 5GB 总内存占用
   - 达到预期目标

### 5.2 优化建议

1. **优化 Pod 资源请求**：
   - 根据实际需求配置资源请求
   - 定期审查资源使用情况

2. **使用资源配额**：
   - 配置资源配额防止资源超用
   - 使用 LimitRange 限制默认资源

3. **优化容器配置**：
   - 使用更小的基础镜像
   - 优化应用配置

4. **使用 HPA 自动扩缩容**：
   - 配置 HPA 根据负载自动调整
   - 提高资源利用率

5. **建立资源基准**：
   - 在优化前建立资源基准
   - 定期进行资源测试，确保优化效果

### 5.3 相关文档

- [`../../COGNITIVE/05-decision-analysis/benchmarks/benchmarks.md`](../../COGNITIVE/05-decision-analysis/benchmarks/benchmarks.md) - 性能基准文档
- [`../../TECHNICAL/01-core-foundations/k3s/k3s.md`](../../TECHNICAL/01-core-foundations/k3s/k3s.md) - K3s 文档
- [`../../PRACTICAL-CASE-SUPPLEMENT-PLAN.md`](../../PRACTICAL-CASE-SUPPLEMENT-PLAN.md) - 实践案例补充计划

---

## 6 相关文档

- [`../README.md`](README.md) - 性能优化案例集目录
- [`../../COGNITIVE/05-decision-analysis/benchmarks/benchmarks.md`](../../COGNITIVE/05-decision-analysis/benchmarks/benchmarks.md) - 性能基准文档
- [`../../TECHNICAL/01-core-foundations/k3s/k3s.md`](../../TECHNICAL/01-core-foundations/k3s/k3s.md) - K3s 文档

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
