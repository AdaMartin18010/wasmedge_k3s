# KServe 模型部署

## 📑 目录

- [1. 概述](#1-概述)
- [2. KServe 安装](#2-kserve-安装)
- [3. 模型部署](#3-模型部署)
- [4. 金丝雀发布](#4-金丝雀发布)
- [5. 相关文档](#5-相关文档)

---

## 1. 概述

**KServe** 是 Kubernetes 原生模型服务框架，提供模型部署、自动扩缩容、金丝雀发布等功能。

### 1.1 核心特性

- **多框架支持**：TensorFlow、PyTorch、Scikit-learn、ONNX、XGBoost
- **自动扩缩容**：基于请求量自动扩缩容
- **金丝雀发布**：支持模型版本的金丝雀发布
- **推理图**：支持复杂的推理图（预处理、推理、后处理）

---

## 2. KServe 安装

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

## 3. 模型部署

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

## 4. 金丝雀发布

### 4.1 多版本部署

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: llm-model
spec:
  predictor:
    canaryTrafficPercent: 10  # 10% 流量到新版本
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

## 5. 相关文档

- [`README.md`](README.md) - AI/ML 实现细节总览
- [`kubeflow-setup.md`](kubeflow-setup.md) - Kubeflow 安装和配置
- [`mlflow-integration.md`](mlflow-integration.md) - MLflow 集成和配置

---

**更新时间**：2025-11-05 **版本**：v1.0

