# GPU 资源调度配置

## 📑 目录

- [GPU 资源调度配置](#gpu-资源调度配置)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 核心概念](#11-核心概念)
  - [2 NVIDIA GPU Operator 安装](#2-nvidia-gpu-operator-安装)
    - [2.1 前置要求](#21-前置要求)
    - [2.2 安装步骤](#22-安装步骤)
    - [2.3 验证安装](#23-验证安装)
  - [3 GPU 资源分配](#3-gpu-资源分配)
    - [3.1 Pod 级别的 GPU 请求](#31-pod-级别的-gpu-请求)
    - [3.2 GPU 共享配置](#32-gpu-共享配置)
    - [3.3 Deployment 级别的 GPU 配置](#33-deployment-级别的-gpu-配置)
  - [4 MIG 配置](#4-mig-配置)
    - [4.1 MIG 概述](#41-mig-概述)
    - [4.2 MIG 配置步骤](#42-mig-配置步骤)
    - [4.3 MIG Pod 配置](#43-mig-pod-配置)
  - [5 GPU 监控](#5-gpu-监控)
    - [5.1 DCGM（NVIDIA Data Center GPU Manager）](#51-dcgmnvidia-data-center-gpu-manager)
    - [5.2 Prometheus 集成](#52-prometheus-集成)
  - [6 相关文档](#6-相关文档)
  - [7 2025 年最新实践](#7-2025-年最新实践)
    - [7.1 GPU Operator 2.0+ 新特性（2025）](#71-gpu-operator-20-新特性2025)
    - [7.2 MIG（Multi-Instance GPU）支持（2025）](#72-migmulti-instance-gpu支持2025)
    - [7.3 边缘 GPU 调度（2025）](#73-边缘-gpu-调度2025)
  - [8 实际应用案例](#8-实际应用案例)
    - [案例 1：多租户 GPU 共享](#案例-1多租户-gpu-共享)
    - [案例 2：GPU 自动扩缩容](#案例-2gpu-自动扩缩容)
    - [案例 3：GPU 时间切片](#案例-3gpu-时间切片)

---

## 1 概述

**GPU 资源调度**是 AI/ML 工作负载的关键组件，通过 Kubernetes GPU 插件实现 GPU 资
源的动态调度和管理。

### 1.1 核心概念

- **GPU 资源分配**：Pod 级别的 GPU 资源请求和限制
- **GPU 共享**：多个 Pod 共享 GPU 资源
- **MIG（Multi-Instance GPU）**：GPU 资源分割
- **GPU 监控**：GPU 使用情况监控

---

## 2 NVIDIA GPU Operator 安装

### 2.1 前置要求

- **Kubernetes**：≥ 1.28
- **NVIDIA GPU**：≥ NVIDIA T4
- **NVIDIA 驱动**：≥ 535.54

### 2.2 安装步骤

```bash
# 添加 NVIDIA Helm 仓库
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update

# 安装 NVIDIA GPU Operator
helm install --wait gpu-operator nvidia/gpu-operator \
  -n gpu-operator --create-namespace \
  --set driver.enabled=true \
  --set toolkit.enabled=true \
  --set devicePlugin.enabled=true \
  --set operator.defaultRuntime=containerd
```

### 2.3 验证安装

```bash
# 检查 GPU Operator Pod
kubectl get pods -n gpu-operator

# 检查 GPU 节点
kubectl get nodes -l nvidia.com/gpu.present=true

# 检查 GPU 资源
kubectl describe node <gpu-node-name> | grep nvidia.com/gpu
```

---

## 3 GPU 资源分配

### 3.1 Pod 级别的 GPU 请求

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-training-pod
spec:
  containers:
    - name: training-container
      image: pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime
      resources:
        limits:
          nvidia.com/gpu: 1 # 请求 1 个 GPU
          memory: "32Gi"
          cpu: "8"
        requests:
          nvidia.com/gpu: 1
          memory: "32Gi"
          cpu: "8"
```

### 3.2 GPU 共享配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: device-plugin-config
  namespace: gpu-operator
data:
  config.yaml: |
    version: v1
    sharing:
      timeSlicing:
        resources:
          - name: nvidia.com/gpu
            replicas: 4  # 每个 GPU 支持 4 个 Pod 共享
```

### 3.3 Deployment 级别的 GPU 配置

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-inference
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: llm-service
          image: my-registry/llm-service:v1.0.0
          resources:
            limits:
              nvidia.com/gpu: 1
            requests:
              nvidia.com/gpu: 1
```

---

## 4 MIG 配置

### 4.1 MIG 概述

**MIG（Multi-Instance GPU）**是 NVIDIA A100/H100 GPU 的特性，可以将一个 GPU 分割
成多个独立的 GPU 实例。

### 4.2 MIG 配置步骤

```bash
# 启用 MIG
nvidia-smi -mig 1

# 创建 MIG 实例（示例：A100 分割为 7 个实例）
nvidia-smi mig -cgi 19,19,19,19,19,19,19 -C

# 配置 GPU Operator 使用 MIG
kubectl patch node <gpu-node-name> \
  -p '{"spec":{"gpu":{"migStrategy":"mixed"}}}'
```

### 4.3 MIG Pod 配置

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mig-pod
spec:
  containers:
    - name: mig-container
      image: pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime
      resources:
        limits:
          nvidia.com/mig-1g.10gb: 1 # 使用 MIG 实例
```

---

## 5 GPU 监控

### 5.1 DCGM（NVIDIA Data Center GPU Manager）

```bash
# 安装 DCGM Exporter
helm install dcgm-exporter nvidia/dcgm-exporter \
  -n gpu-operator

# 查看 GPU 指标
kubectl port-forward -n gpu-operator svc/dcgm-exporter 9400:9400
curl http://localhost:9400/metrics
```

### 5.2 Prometheus 集成

```yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: dcgm-exporter
  namespace: gpu-operator
spec:
  selector:
    matchLabels:
      app: dcgm-exporter
  endpoints:
    - port: metrics
      interval: 30s
```

---

## 6 相关文档

- [`README.md`](README.md) - AI/ML 实现细节总览
- [`kubeflow-setup.md`](kubeflow-setup.md) - Kubeflow 安装和配置
- [`kserve-deployment.md`](kserve-deployment.md) - KServe 模型部署

## 7 2025 年最新实践

### 7.1 GPU Operator 2.0+ 新特性（2025）

**最新版本**：GPU Operator 2.0+（2025 年）

**新特性**：

- **多 GPU 厂商支持**：支持 NVIDIA、AMD、Intel GPU
- **动态 GPU 分配**：支持动态 GPU 分配
- **性能优化**：GPU 利用率提升 30%

**安装最新版本**：

```bash
# 安装 GPU Operator 2.0
helm install gpu-operator nvidia/gpu-operator \
  --version 2.0.0 \
  --namespace gpu-operator-system \
  --create-namespace
```

### 7.2 MIG（Multi-Instance GPU）支持（2025）

**2025 年趋势**：使用 MIG 实现 GPU 细粒度共享

**配置示例**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: device-plugin-config
  namespace: gpu-operator-system
data:
  config.yaml: |
    version: v1
    sharing:
      timeSlicing:
        resources:
        - name: nvidia.com/gpu
          replicas: 4
```

### 7.3 边缘 GPU 调度（2025）

**2025 年趋势**：在边缘节点调度 GPU 工作负载

**配置示例**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: edge-gpu-app
spec:
  nodeSelector:
    node-type: edge
    accelerator: nvidia-tesla-t4
  containers:
  - name: app
    image: gpu-app:latest
    resources:
      limits:
        nvidia.com/gpu: 1
```

## 8 实际应用案例

### 案例 1：多租户 GPU 共享

**场景**：在多租户环境中共享 GPU 资源

**实现方案**：

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-quota
  namespace: tenant-a
spec:
  hard:
    requests.nvidia.com/gpu: "2"
    limits.nvidia.com/gpu: "4"
---
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
  namespace: tenant-a
spec:
  containers:
  - name: app
    image: gpu-app:latest
    resources:
      requests:
        nvidia.com/gpu: 1
      limits:
        nvidia.com/gpu: 1
```

**效果**：

- 资源隔离：每个租户有独立的 GPU 配额
- 公平调度：通过 ResourceQuota 公平调度
- 资源利用：提高 GPU 利用率

### 案例 2：GPU 自动扩缩容

**场景**：根据负载自动扩缩容 GPU 工作负载

**实现方案**：

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gpu-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: gpu-app
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: nvidia.com/gpu
      target:
        type: Utilization
        averageUtilization: 80
```

**效果**：

- 自动扩缩容：根据 GPU 利用率自动扩缩容
- 资源优化：优化 GPU 资源使用
- 成本控制：降低 GPU 运行成本

### 案例 3：GPU 时间切片

**场景**：使用 GPU 时间切片实现 GPU 共享

**实现方案**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: device-plugin-config
  namespace: gpu-operator-system
data:
  config.yaml: |
    version: v1
    sharing:
      timeSlicing:
        resources:
        - name: nvidia.com/gpu
          replicas: 4
---
apiVersion: v1
kind: Pod
metadata:
  name: gpu-shared-pod
spec:
  containers:
  - name: app
    image: gpu-app:latest
    resources:
      limits:
        nvidia.com/gpu: 1  # 共享 GPU 的 1/4
```

**效果**：

- GPU 共享：多个 Pod 共享同一个 GPU
- 资源效率：提高 GPU 利用率
- 成本优化：降低 GPU 使用成本

---

**更新时间**：2025-11-15 **版本**：v1.1 **状态**：✅ 包含 2025 年最新实践
