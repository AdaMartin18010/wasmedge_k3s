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
  - [6 2025 年最新实践](#6-2025-年最新实践)
    - [6.1 MLflow 2.12+ 新特性（2025）](#61-mlflow-212-新特性2025)
    - [6.2 MLflow 与 Kubernetes 集成（2025）](#62-mlflow-与-kubernetes-集成2025)
    - [6.3 MLflow 模型服务化（2025）](#63-mlflow-模型服务化2025)
  - [7 实际应用案例](#7-实际应用案例)
    - [案例 1：模型版本管理](#案例-1模型版本管理)
    - [案例 2：模型 A/B 测试](#案例-2模型-ab-测试)
    - [案例 3：模型自动部署](#案例-3模型自动部署)

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

## 6 2025 年最新实践

### 6.1 MLflow 2.12+ 新特性（2025）

**最新版本**：MLflow 2.12+（2025 年）

**新特性**：

- **统一模型注册表**：统一的模型注册表
- **模型版本管理增强**：更好的模型版本管理
- **性能优化**：模型注册和查询性能提升 50%

**安装最新版本**：

```bash
# 安装 MLflow 2.12
pip install mlflow==2.12.0
```

### 6.2 MLflow 与 Kubernetes 集成（2025）

**2025 年趋势**：MLflow 与 Kubernetes 深度集成

**配置示例**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mlflow
  template:
    spec:
      containers:
      - name: mlflow
        image: mlflow/mlflow:2.12.0
        env:
        - name: MLFLOW_BACKEND_STORE_URI
          value: "postgresql://user:pass@postgres:5432/mlflow"
        - name: MLFLOW_DEFAULT_ARTIFACT_ROOT
          value: "s3://mlflow-artifacts"
```

### 6.3 MLflow 模型服务化（2025）

**2025 年趋势**：使用 MLflow 直接部署模型服务

**配置示例**：

```bash
# 使用 MLflow 部署模型服务
mlflow models serve -m models:/my-model/1 -p 5000

# Kubernetes 部署
kubectl create deployment mlflow-model \
  --image=mlflow/mlflow:2.12.0 \
  -- mlflow models serve -m models:/my-model/1
```

## 7 实际应用案例

### 案例 1：模型版本管理

**场景**：管理模型版本和生命周期

**实现方案**：

```python
# Python 模型版本管理
import mlflow

# 注册模型
mlflow.register_model(
    model_uri="runs:/run-id/model",
    name="my-model"
)

# 获取模型版本
client = mlflow.tracking.MlflowClient()
versions = client.search_model_versions("name='my-model'")

# 标记生产版本
client.transition_model_version_stage(
    name="my-model",
    version=1,
    stage="Production"
)
```

**效果**：

- 版本控制：完整的模型版本管理
- 生命周期：管理模型生命周期
- 可追溯：模型版本可追溯

### 案例 2：模型 A/B 测试

**场景**：使用 MLflow 进行模型 A/B 测试

**实现方案**：

```python
# Python A/B 测试
import mlflow

# 注册两个模型版本
mlflow.register_model("runs:/run-1/model", "my-model")
mlflow.register_model("runs:/run-2/model", "my-model")

# 部署 A/B 测试
client = mlflow.tracking.MlflowClient()
client.set_model_version_tag(
    name="my-model",
    version=1,
    key="test-group",
    value="A"
)
client.set_model_version_tag(
    name="my-model",
    version=2,
    key="test-group",
    value="B"
)
```

**效果**：

- A/B 测试：支持模型 A/B 测试
- 性能对比：对比不同模型版本性能
- 数据驱动：基于数据做出决策

### 案例 3：模型自动部署

**场景**：模型训练完成后自动部署

**实现方案**：

```python
# Python 自动部署
import mlflow
from kubernetes import client, config

def auto_deploy_model(model_name, version):
    # 获取模型 URI
    model_uri = f"models:/{model_name}/{version}"

    # 创建 Kubernetes Deployment
    config.load_incluster_config()
    v1 = client.AppsV1Api()

    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=f"{model_name}-{version}"),
        spec=client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={"app": model_name}
            ),
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="model",
                            image="mlflow/mlflow:2.12.0",
                            args=[
                                "mlflow", "models", "serve",
                                "-m", model_uri
                            ]
                        )
                    ]
                )
            )
        )
    )

    v1.create_namespaced_deployment(
        namespace="default",
        body=deployment
    )
```

**效果**：

- 自动化：模型训练完成后自动部署
- 快速迭代：快速迭代模型版本
- 减少人工：减少人工部署工作

---

**更新时间**：2025-11-15 **版本**：v1.1 **状态**：✅ 包含 2025 年最新实践
