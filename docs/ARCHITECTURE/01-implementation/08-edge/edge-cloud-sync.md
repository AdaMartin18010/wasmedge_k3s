# 边缘-云同步配置

## 📑 目录

- [1. 概述](#1-概述)
- [2. 配置同步](#2-配置同步)
- [3. 数据同步](#3-数据同步)
- [4. 状态同步](#4-状态同步)
- [5. 相关文档](#5-相关文档)

---

## 1. 概述

**边缘-云同步**是边缘计算的关键组件，实现边缘节点与云端节点的配置、数据和状态同
步。

### 1.1 核心功能

- **配置同步**：云端配置同步到边缘节点
- **数据同步**：边缘数据同步到云端
- **状态同步**：边缘状态同步到云端
- **版本管理**：边缘应用版本管理

---

## 2. 配置同步

### 2.1 ArgoCD 配置同步

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: edge-app-config
spec:
  source:
    repoURL: https://github.com/myorg/edge-configs
    path: configs/edge-app
    targetRevision: main
  destination:
    server: https://edge-k3s.example.com:6443
    namespace: edge-app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 2.2 K3s 配置管理

```yaml
# 云端配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: edge-app-config
data:
  config.yaml: |
    app:
      name: edge-app
      version: v1.0.0
      replicas: 3
```

---

## 3. 数据同步

### 3.1 数据上传（边缘 → 云端）

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: data-sync
spec:
  schedule: "*/5 * * * *" # 每 5 分钟同步一次
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: data-sync
              image: data-sync:latest
              command:
                - /bin/sh
                - -c
                - |
                  # 收集边缘数据
                  kubectl get pods -o json > /data/pods.json
                  # 上传到云端
                  aws s3 cp /data/pods.json s3://edge-data/$(hostname)/pods.json
```

### 3.2 数据下载（云端 → 边缘）

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-download
spec:
  template:
    spec:
      containers:
        - name: data-download
          image: data-sync:latest
          command:
            - /bin/sh
            - -c
            - |
              # 从云端下载数据
              aws s3 cp s3://edge-data/config.yaml /data/config.yaml
              # 应用配置
              kubectl apply -f /data/config.yaml
```

---

## 4. 状态同步

### 4.1 边缘状态上报

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: edge-status-reporter
spec:
  template:
    spec:
      containers:
        - name: status-reporter
          image: status-reporter:latest
          env:
            - name: CLOUD_API_URL
              value: "https://cloud-api.example.com"
            - name: EDGE_NODE_NAME
              valueFrom:
                fieldRef:
                  fieldPath: spec.nodeName
          command:
            - /bin/sh
            - -c
            - |
              while true; do
                # 收集状态
                STATUS=$(kubectl get nodes -o json | jq .)
                # 上报状态
                curl -X POST $CLOUD_API_URL/api/v1/edge-status \
                  -H "Content-Type: application/json" \
                  -d "$STATUS"
                sleep 60
              done
```

### 4.2 云端状态查询

```bash
# 查询边缘节点状态
curl https://cloud-api.example.com/api/v1/edge-status/edge-node-1

# 查询所有边缘节点状态
curl https://cloud-api.example.com/api/v1/edge-status
```

---

## 5. 相关文档

- [`README.md`](README.md) - 边缘计算实现细节总览
- [`k3s-setup.md`](k3s-setup.md) - K3s 安装和配置
- [`nsm-edge.md`](nsm-edge.md) - NSM 边缘网关配置

---

**更新时间**：2025-11-05 **版本**：v1.0
