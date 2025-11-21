# KServe 模型部署

## 📑 目录

- [KServe 模型部署](#kserve-模型部署)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 核心特性](#11-核心特性)
  - [2 KServe 安装](#2-kserve-安装)
    - [2.1 前置要求](#21-前置要求)
    - [2.2 安装步骤](#22-安装步骤)
    - [2.3 验证安装](#23-验证安装)
  - [3 模型部署](#3-模型部署)
    - [3.1 简单部署（TensorFlow）](#31-简单部署tensorflow)
    - [3.2 GPU 部署（PyTorch）](#32-gpu-部署pytorch)
    - [3.3 自定义推理服务](#33-自定义推理服务)
  - [4 金丝雀发布](#4-金丝雀发布)
    - [4.1 多版本部署](#41-多版本部署)
    - [4.2 Istio 流量管理](#42-istio-流量管理)
  - [5 相关文档](#5-相关文档)
  - [6 2025 年最新实践](#6-2025-年最新实践)
    - [6.1 KServe 0.12+ 新特性（2025）](#61-kserve-012-新特性2025)
    - [6.2 边缘 KServe 部署（2025）](#62-边缘-kserve-部署2025)
    - [6.3 Wasm 模型推理（2025）](#63-wasm-模型推理2025)
  - [7 实际应用案例](#7-实际应用案例)
    - [案例 1：多模型服务部署](#案例-1多模型服务部署)
    - [案例 2：模型金丝雀发布](#案例-2模型金丝雀发布)
    - [案例 3：边缘 AI 推理](#案例-3边缘-ai-推理)

---

## 1 概述

**KServe** 是 Kubernetes 原生模型服务框架，提供模型部署、自动扩缩容、金丝雀发布
等功能。

### 1.1 核心特性

- **多框架支持**：TensorFlow、PyTorch、Scikit-learn、ONNX、XGBoost
- **自动扩缩容**：基于请求量自动扩缩容
- **金丝雀发布**：支持模型版本的金丝雀发布
- **推理图**：支持复杂的推理图（预处理、推理、后处理）

---

## 2 KServe 安装

### 2.1 前置要求

- **Kubernetes**：≥ 1.28
- **Istio**：≥ 1.21（可选，用于流量管理）

### 2.2 安装步骤

```bash
# 安装 KServe
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.11.0/kserve.yaml

# 安装 KServe 运行时（以 PyTorch 为例）
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.11.0/pytorch.yaml
```

### 2.3 验证安装

```bash
# 检查 KServe 控制器
kubectl get pods -n kserve-system

# 检查 KServe CRD
kubectl get crd | grep kserve
```

---

## 3 模型部署

### 3.1 简单部署（TensorFlow）

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: tensorflow-model
spec:
  predictor:
    tensorflow:
      storageUri: s3://models/tensorflow-model/
      resources:
        limits:
          memory: "4Gi"
          cpu: "2"
        requests:
          memory: "2Gi"
          cpu: "1"
```

### 3.2 GPU 部署（PyTorch）

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: pytorch-model
spec:
  predictor:
    pytorch:
      storageUri: s3://models/pytorch-model/
      resources:
        limits:
          nvidia.com/gpu: 1
          memory: "32Gi"
          cpu: "8"
        requests:
          nvidia.com/gpu: 1
          memory: "32Gi"
          cpu: "8"
```

### 3.3 自定义推理服务

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: custom-model
spec:
  predictor:
    containers:
      - name: custom-inference
        image: my-registry/custom-inference:v1.0.0
        resources:
          limits:
            memory: "4Gi"
            cpu: "2"
```

---

## 4 金丝雀发布

### 4.1 多版本部署

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: llm-model
spec:
  predictor:
    canaryTrafficPercent: 10 # 10% 流量到新版本
    pytorch:
      storageUri: s3://models/llm-model-v2/
      resources:
        limits:
          nvidia.com/gpu: 1
---
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: llm-model-canary
spec:
  predictor:
    pytorch:
      storageUri: s3://models/llm-model-v2/
      resources:
        limits:
          nvidia.com/gpu: 1
```

### 4.2 Istio 流量管理

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: llm-model
spec:
  hosts:
    - llm-model
  http:
    - match:
        - headers:
            version:
              exact: "v2"
      route:
        - destination:
            host: llm-model-canary
            weight: 100
    - route:
        - destination:
            host: llm-model
            weight: 90
        - destination:
            host: llm-model-canary
            weight: 10
```

---

## 5 相关文档

- [`README.md`](README.md) - AI/ML 实现细节总览
- [`kubeflow-setup.md`](kubeflow-setup.md) - Kubeflow 安装和配置
- [`mlflow-integration.md`](mlflow-integration.md) - MLflow 集成和配置

## 6 2025 年最新实践

### 6.1 KServe 0.12+ 新特性（2025）

**最新版本**：KServe 0.12+（2025 年）

**新特性**：

- **多模型服务**：支持多模型服务
- **自动扩缩容增强**：改进的自动扩缩容
- **性能优化**：推理性能提升 30%

**安装最新版本**：

```bash
# 安装 KServe 0.12
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.12.0/kserve.yaml
```

### 6.2 边缘 KServe 部署（2025）

**2025 年趋势**：在边缘节点部署 KServe

**配置示例**：

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: edge-model
spec:
  predictor:
    nodeSelector:
      node-type: edge
    containers:
    - name: kserve-container
      image: model:latest
      resources:
        requests:
          cpu: "500m"
          memory: "1Gi"
        limits:
          cpu: "1"
          memory: "2Gi"
```

### 6.3 Wasm 模型推理（2025）

**2025 年趋势**：使用 Wasm 运行模型推理

**配置示例**：

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: wasm-model
spec:
  predictor:
    runtimeClassName: wasm
    containers:
    - name: wasm-container
      image: wasm-model:latest
      resources:
        requests:
          cpu: "100m"
          memory: "128Mi"
```

## 7 实际应用案例

### 案例 1：多模型服务部署

**场景**：部署多个模型服务

**实现方案**：

```yaml
# 模型 A
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: model-a
spec:
  predictor:
    pytorch:
      storageUri: s3://models/model-a
---
# 模型 B
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: model-b
spec:
  predictor:
    tensorflow:
      storageUri: s3://models/model-b
```

**效果**：

- 多模型：支持部署多个模型
- 独立扩缩容：每个模型独立扩缩容
- 统一管理：统一管理所有模型

### 案例 2：模型金丝雀发布

**场景**：使用 KServe 进行模型金丝雀发布

**实现方案**：

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: model-canary
spec:
  predictor:
    canaryTrafficPercent: 10
    pytorch:
      storageUri: s3://models/model-v2
    traffic: 90
    pytorch:
      storageUri: s3://models/model-v1
```

**效果**：

- 金丝雀发布：逐步发布新模型
- 风险控制：降低新模型发布风险
- 快速回滚：快速回滚到旧模型

### 案例 3：边缘 AI 推理

**场景**：在边缘节点部署 AI 推理服务

**实现方案**：

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: edge-ai
spec:
  predictor:
    nodeSelector:
      node-type: edge
    pytorch:
      storageUri: s3://models/edge-model
      resources:
        requests:
          cpu: "500m"
          memory: "1Gi"
        limits:
          cpu: "1"
          memory: "2Gi"
```

**效果**：

- 边缘部署：在边缘节点部署推理服务
- 低延迟：减少推理延迟
- 离线支持：支持离线推理

---

**更新时间**：2025-11-15 **版本**：v1.1 **状态**：✅ 包含 2025 年最新实践
