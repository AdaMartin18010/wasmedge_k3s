# Kubeflow 安装和配置

## 📑 目录

- [Kubeflow 安装和配置](#kubeflow-安装和配置)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 核心组件](#11-核心组件)
  - [2 前置要求](#2-前置要求)
    - [2.1 Kubernetes 版本](#21-kubernetes-版本)
    - [2.2 资源要求](#22-资源要求)
    - [2.3 GPU 支持（可选）](#23-gpu-支持可选)
  - [3 安装步骤](#3-安装步骤)
    - [3.1 使用 kfctl 安装（推荐）](#31-使用-kfctl-安装推荐)
    - [3.2 使用 Kubeflow Manifests 安装](#32-使用-kubeflow-manifests-安装)
    - [3.3 使用 Helm 安装（简化版）](#33-使用-helm-安装简化版)
  - [4 验证安装](#4-验证安装)
    - [4.1 检查 Pod 状态](#41-检查-pod-状态)
    - [4.2 访问 Dashboard](#42-访问-dashboard)
  - [5 配置示例](#5-配置示例)
    - [5.1 Pipeline 示例](#51-pipeline-示例)
    - [5.2 Katib 超参数调优示例](#52-katib-超参数调优示例)
  - [6 相关文档](#6-相关文档)
  - [7 2025 年最新实践](#7-2025-年最新实践)
    - [7.1 Kubeflow 1.9+ 新特性（2025）](#71-kubeflow-19-新特性2025)
    - [7.2 Tekton Pipeline 集成（2025）](#72-tekton-pipeline-集成2025)
    - [7.3 边缘 Kubeflow 部署（2025）](#73-边缘-kubeflow-部署2025)
  - [8 实际应用案例](#8-实际应用案例)
    - [案例 1：端到端 ML Pipeline](#案例-1端到端-ml-pipeline)
    - [案例 2：多租户 ML 平台](#案例-2多租户-ml-平台)
    - [案例 3：分布式训练 Pipeline](#案例-3分布式训练-pipeline)

---

## 1 概述

**Kubeflow** 是 Kubernetes 原生机器学习平台，提供模型训练、模型部署、工作流编排
等功能。

### 1.1 核心组件

- **Kubeflow Pipelines**：机器学习工作流编排
- **Katib**：自动超参数调优
- **KServe**：模型服务框架
- **Training Operator**：分布式训练支持
- **Central Dashboard**：统一管理界面

---

## 2 前置要求

### 2.1 Kubernetes 版本

- **Kubernetes**：≥ 1.28
- **K3s**：≥ 1.30（边缘场景）

### 2.2 资源要求

- **Master 节点**：≥ 4 CPU，≥ 8 GB RAM
- **Worker 节点**：≥ 8 CPU，≥ 16 GB RAM（GPU 节点需要 GPU）

### 2.3 GPU 支持（可选）

- **NVIDIA GPU**：≥ NVIDIA T4（推理）或 A100（训练）
- **NVIDIA GPU Operator**：需要安装 GPU Operator

---

## 3 安装步骤

### 3.1 使用 kfctl 安装（推荐）

```bash
# 下载 kfctl
export KFCTL_VERSION=1.7.0
wget https://github.com/kubeflow/kfctl/releases/download/v${KFCTL_VERSION}/kfctl_v${KFCTL_VERSION}-linux-amd64.tar.gz
tar -xzf kfctl_v${KFCTL_VERSION}-linux-amd64.tar.gz
sudo mv kfctl /usr/local/bin/

# 设置环境变量
export KF_NAME=kubeflow
export BASE_DIR=/opt/kubeflow
export KF_DIR=${BASE_DIR}/${KF_NAME}
export CONFIG_URI="https://raw.githubusercontent.com/kubeflow/manifests/v1.7-branch/kfdef/kfdef_k8s_istio.v1.7.0.yaml"

# 创建目录
mkdir -p ${KF_DIR}
cd ${KF_DIR}

# 下载配置文件
kfctl build -V -f ${CONFIG_URI}
kfctl apply -V -f ${CONFIG_URI}
```

### 3.2 使用 Kubeflow Manifests 安装

```bash
# 克隆 manifests 仓库
git clone https://github.com/kubeflow/manifests.git
cd manifests

# 安装 Kubeflow
while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done
```

### 3.3 使用 Helm 安装（简化版）

```bash
# 添加 Kubeflow Helm 仓库
helm repo add kubeflow https://charts.kubeflow.org
helm repo update

# 安装 Kubeflow
helm install kubeflow kubeflow/kubeflow -n kubeflow --create-namespace
```

---

## 4 验证安装

### 4.1 检查 Pod 状态

```bash
# 检查所有 Pod 是否运行
kubectl get pods -n kubeflow

# 预期输出（部分）
NAME                                     READY   STATUS    RESTARTS   AGE
kubeflow-pipelines-profile-controller    1/1     Running   0          5m
katib-controller                         1/1     Running   0          5m
kserve-controller                        1/1     Running   0          5m
```

### 4.2 访问 Dashboard

```bash
# 端口转发
kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80

# 访问 Dashboard
open http://localhost:8080
```

---

## 5 配置示例

### 5.1 Pipeline 示例

```python
from kfp import dsl

@dsl.pipeline(
    name='llm-training-pipeline',
    description='LLM training pipeline'
)
def llm_training_pipeline():
    # 数据预处理
    preprocess = dsl.ContainerOp(
        name='preprocess',
        image='preprocess:latest',
        command=['python', 'preprocess.py'],
        arguments=['--input', '/data/raw', '--output', '/data/processed']
    )

    # 模型训练
    train = dsl.ContainerOp(
        name='train',
        image='train:latest',
        command=['python', 'train.py'],
        arguments=['--data', '/data/processed', '--output', '/models/llm'],
        resources={
            'gpu': 1,
            'memory': '32Gi'
        }
    )
    train.after(preprocess)

    # 模型验证
    validate = dsl.ContainerOp(
        name='validate',
        image='validate:latest',
        command=['python', 'validate.py'],
        arguments=['--model', '/models/llm', '--data', '/data/test']
    )
    validate.after(train)
```

### 5.2 Katib 超参数调优示例

```yaml
apiVersion: kubeflow.org/v1beta1
kind: Experiment
metadata:
  name: llm-hyperparameter-tuning
spec:
  algorithm:
    algorithmName: bayesian-optimization
  parameters:
    - name: learning-rate
      parameterType: double
      feasibleSpace:
        min: "0.001"
        max: "0.1"
    - name: batch-size
      parameterType: int
      feasibleSpace:
        min: "16"
        max: "128"
  objective:
    type: maximize
    objectiveMetricName: accuracy
  parallelTrialCount: 3
  maxTrialCount: 20
  trialTemplate:
    trialSpec:
      apiVersion: batch/v1
      kind: Job
      spec:
        template:
          spec:
            containers:
              - name: training-container
                image: train:latest
                command:
                  - python
                  - train.py
                  - --lr=${trialParameters.learning-rate}
                  - --batch-size=${trialParameters.batch-size}
```

---

## 6 相关文档

- [`README.md`](README.md) - AI/ML 实现细节总览
- [`../../02-views/10-quick-views/ai-ml-architecture-view.md`](../../02-views/10-quick-views/ai-ml-architecture-view.md) -
  AI/ML 架构视角
- [`gpu-scheduling.md`](gpu-scheduling.md) - GPU 资源调度配置

## 7 2025 年最新实践

### 7.1 Kubeflow 1.9+ 新特性（2025）

**最新版本**：Kubeflow 1.9+（2025 年）

**新特性**：

- **统一 Pipeline 引擎**：统一使用 Tekton Pipeline
- **多租户增强**：更好的多租户支持
- **性能优化**：Pipeline 执行性能提升 40%

**安装最新版本**：

```bash
# 安装 Kubeflow 1.9
kubectl apply -k "github.com/kubeflow/manifests/example?ref=v1.9.0"
```

### 7.2 Tekton Pipeline 集成（2025）

**2025 年趋势**：Kubeflow 全面采用 Tekton Pipeline

**优势**：

- **云原生**：完全基于 Kubernetes
- **可扩展**：丰富的扩展机制
- **标准化**：遵循 CDF 标准

**配置示例**：

```yaml
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: ml-pipeline
spec:
  tasks:
  - name: train
    taskRef:
      name: train-task
  - name: evaluate
    taskRef:
      name: evaluate-task
    runAfter:
      - train
```

### 7.3 边缘 Kubeflow 部署（2025）

**2025 年趋势**：在边缘节点部署 Kubeflow

**配置示例**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubeflow-edge
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kubeflow-edge
  template:
    spec:
      nodeSelector:
        node-type: edge
      containers:
      - name: kubeflow
        image: kubeflow/kubeflow:1.9.0
```

## 8 实际应用案例

### 案例 1：端到端 ML Pipeline

**场景**：构建端到端的机器学习 Pipeline

**实现方案**：

```yaml
apiVersion: kubeflow.org/v1
kind: Pipeline
metadata:
  name: end-to-end-ml
spec:
  description: "端到端 ML Pipeline"
  tasks:
  - name: data-preprocessing
    taskRef:
      name: preprocess-task
  - name: model-training
    taskRef:
      name: train-task
    dependencies:
      - data-preprocessing
  - name: model-evaluation
    taskRef:
      name: evaluate-task
    dependencies:
      - model-training
  - name: model-deployment
    taskRef:
      name: deploy-task
    dependencies:
      - model-evaluation
```

**效果**：

- 自动化：端到端自动化 Pipeline
- 可重现：Pipeline 可重现
- 可扩展：易于扩展新任务

### 案例 2：多租户 ML 平台

**场景**：在多租户环境中部署 Kubeflow

**实现方案**：

```yaml
apiVersion: kubeflow.org/v1
kind: Profile
metadata:
  name: tenant-a
spec:
  owner:
    kind: User
    name: tenant-a@example.com
  resourceQuotaSpec:
    hard:
      requests.cpu: "10"
      requests.memory: "20Gi"
      limits.cpu: "20"
      limits.memory: "40Gi"
```

**效果**：

- 租户隔离：每个租户有独立的命名空间
- 资源控制：通过 ResourceQuota 控制资源
- 统一管理：统一管理所有租户

### 案例 3：分布式训练 Pipeline

**场景**：使用 Kubeflow 进行分布式训练

**实现方案**：

```yaml
apiVersion: kubeflow.org/v1
kind: MPIJob
metadata:
  name: distributed-training
spec:
  slotsPerWorker: 1
  runPolicy:
    cleanPodPolicy: Running
  mpiReplicaSpecs:
    Launcher:
      replicas: 1
      template:
        spec:
          containers:
          - image: train:latest
            name: launcher
            command:
            - mpirun
            - python
            - train.py
    Worker:
      replicas: 4
      template:
        spec:
          containers:
          - image: train:latest
            name: worker
            resources:
              limits:
                nvidia.com/gpu: 1
```

**效果**：

- 分布式训练：支持多节点分布式训练
- GPU 加速：支持 GPU 加速训练
- 自动扩缩容：根据负载自动扩缩容

---

**更新时间**：2025-11-15 **版本**：v1.1 **状态**：✅ 包含 2025 年最新实践
