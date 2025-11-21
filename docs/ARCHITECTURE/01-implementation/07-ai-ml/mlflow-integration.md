# MLflow 集成和配置

## 📑 目录

- [MLflow 集成和配置](#mlflow-集成和配置)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 核心组件](#11-核心组件)
  - [2 MLflow Server 部署](#2-mlflow-server-部署)
    - [2.1 Kubernetes 部署](#21-kubernetes-部署)
    - [2.2 访问 MLflow UI](#22-访问-mlflow-ui)
  - [3 模型注册](#3-模型注册)
    - [3.1 Python 代码示例](#31-python-代码示例)
    - [3.2 模型版本管理](#32-模型版本管理)
  - [4 GitOps 集成](#4-gitops-集成)
    - [4.1 ArgoCD 配置](#41-argocd-配置)
    - [4.2 Webhook 触发](#42-webhook-触发)
  - [5 相关文档](#5-相关文档)

---

## 1 概述

**MLflow** 是机器学习生命周期管理平台，提供实验跟踪、模型注册、模型部署等功能。

### 1.1 核心组件

- **MLflow Tracking**：实验跟踪
- **MLflow Projects**：可重现的代码打包
- **MLflow Models**：模型打包和部署
- **MLflow Registry**：模型注册表

---

## 2 MLflow Server 部署

### 2.1 Kubernetes 部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow-server
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: mlflow
          image: ghcr.io/mlflow/mlflow:v2.8.1
          command:
            - mlflow
            - server
            - --host
            - 0.0.0.0
            - --port
            - "5000"
            - --backend-store-uri
            - sqlite:///mlflow.db
            - --default-artifact-root
            - s3://mlflow-artifacts/
          ports:
            - containerPort: 5000
          env:
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: mlflow-s3-secret
                  key: access-key-id
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: mlflow-s3-secret
                  key: secret-access-key
---
apiVersion: v1
kind: Service
metadata:
  name: mlflow-server
spec:
  ports:
    - port: 5000
      targetPort: 5000
  selector:
    app: mlflow-server
```

### 2.2 访问 MLflow UI

```bash
# 端口转发
kubectl port-forward svc/mlflow-server 5000:5000

# 访问 UI
open http://localhost:5000
```

---

## 3 模型注册

### 3.1 Python 代码示例

```python
import mlflow
import mlflow.sklearn

# 设置 MLflow 跟踪 URI
mlflow.set_tracking_uri("http://mlflow-server:5000")

# 开始实验
with mlflow.start_run():
    # 训练模型
    model = train_model()

    # 记录参数
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("batch_size", 32)

    # 记录指标
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05)

    # 保存模型
    mlflow.sklearn.log_model(model, "model")

    # 注册模型
    mlflow.register_model(
        model_uri=f"runs:/{mlflow.active_run().info.run_id}/model",
        name="llm-model"
    )
```

### 3.2 模型版本管理

```python
# 获取模型版本
client = mlflow.tracking.MlflowClient()
model_versions = client.get_latest_versions("llm-model", stages=["Production"])

# 加载生产模型
model = mlflow.sklearn.load_model(f"models:/llm-model/Production")
```

---

## 4 GitOps 集成

### 4.1 ArgoCD 配置

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: mlflow-model-deployment
spec:
  source:
    repoURL: https://github.com/myorg/ml-models
    path: deployments/llm-inference
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: ml-production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### 4.2 Webhook 触发

```python
# MLflow Webhook（模型注册后触发 GitOps）
import requests

def trigger_gitops(model_name, version):
    webhook_url = "https://argocd-server/api/v1/webhooks/mlflow"
    payload = {
        "model_name": model_name,
        "version": version,
        "action": "register"
    }
    requests.post(webhook_url, json=payload)
```

---

## 5 相关文档

- [`README.md`](README.md) - AI/ML 实现细节总览
- [`kubeflow-setup.md`](kubeflow-setup.md) - Kubeflow 安装和配置
- [`kserve-deployment.md`](kserve-deployment.md) - KServe 模型部署

---

**更新时间**：2025-11-05 **版本**：v1.0
