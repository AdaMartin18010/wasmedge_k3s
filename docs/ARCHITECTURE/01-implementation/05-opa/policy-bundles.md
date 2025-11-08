# Policy Bundle 示例

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 理论基础](#11-理论基础)
- [2. Bundle 结构](#2-bundle-结构)
  - [2.1 Bundle 目录结构](#21-bundle-目录结构)
  - [2.2 manifest.json](#22-manifestjson)
- [3. Bundle 创建](#3-bundle-创建)
  - [3.1 创建策略文件](#31-创建策略文件)
  - [3.2 创建数据文件](#32-创建数据文件)
  - [3.3 创建 Bundle](#33-创建-bundle)
- [4. Bundle 分发](#4-bundle-分发)
  - [4.1 HTTP/HTTPS 分发](#41-httphttps-分发)
  - [4.2 OCI Registry 分发](#42-oci-registry-分发)
  - [4.3 Git 分发](#43-git-分发)
- [5. Bundle 部署](#5-bundle-部署)
  - [5.1 OPA Server 部署](#51-opa-server-部署)
  - [5.2 ConfigMap 配置](#52-configmap-配置)
  - [5.3 Sidecar 部署](#53-sidecar-部署)
- [6. 相关文档](#6-相关文档)
  - [6.1 理论论证](#61-理论论证)
  - [6.2 架构视角](#62-架构视角)
  - [6.3 技术文档](#63-技术文档)

---

## 1. 概述

本文档提供 **OPA Policy Bundle 的实际配置示例**，展示如何创建、分发和部署 OPA
Policy Bundle。

### 1.1 理论基础

Policy Bundle 配置基于以下理论论证：

- **公理 A5-A8（OPA 公理）**：
  - A5：能力闭包
  - A6：最小权限
  - A7：可证明性
  - A8：版本一致性
- **引理 L3（OPA 确定性）**：OPA 求值过程 ≡ 单调不动点迭代，决策在有限步内唯一且
  可重现

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2. Bundle 结构

### 2.1 Bundle 目录结构

```text
bundle/
├── policies/
│   ├── authz.rego
│   ├── rate-limit.rego
│   └── network-policy.rego
├── data/
│   └── config.json
└── .manifest
```

### 2.2 manifest.json

```json
{
  "revision": "abc123",
  "roots": ["policies", "data"],
  "metadata": {
    "author": "ops-team",
    "version": "1.0.0",
    "created": "2025-11-04T10:00:00Z"
  }
}
```

---

## 3. Bundle 创建

### 3.1 创建策略文件

```rego
# policies/authz.rego
package authz

default allow = false

allow {
    input.user.role == "admin"
    input.operation == "create"
}

allow {
    input.user.role == "user"
    input.operation == "read"
    input.resource == "public"
}
```

```rego
# policies/rate-limit.rego
package rate_limit

default allow = false

allow {
    input.requests_per_minute < 100
}
```

### 3.2 创建数据文件

```json
{
  "config": {
    "max_requests_per_minute": 100,
    "allowed_roles": ["admin", "user"],
    "blocked_ips": []
  }
}
```

### 3.3 创建 Bundle

```bash
# 使用 OPA CLI 创建 Bundle
opa bundle create \
  --revision abc123 \
  --manifest bundle.json \
  --bundle bundle/ \
  bundle.tar.gz

# 验证 Bundle
opa bundle verify bundle.tar.gz
```

---

## 4. Bundle 分发

### 4.1 HTTP/HTTPS 分发

```bash
# 配置 OPA 从 HTTP 服务器拉取 Bundle
cat > opa-config.yaml <<EOF
services:
  - name: bundle-service
    url: https://example.com/bundles

bundles:
  authz:
    service: bundle-service
    resource: /authz/bundle.tar.gz
    polling:
      min_delay_seconds: 60
      max_delay_seconds: 120
EOF

# 启动 OPA 使用配置
opa run --server --config-file opa-config.yaml
```

### 4.2 OCI Registry 分发

```bash
# 推送 Bundle 到 OCI Registry
opa bundle push \
  --registry example.com/opa/bundles \
  --tag v1.0.0 \
  bundle.tar.gz

# 从 OCI Registry 拉取 Bundle
cat > opa-config.yaml <<EOF
services:
  - name: registry-service
    url: https://example.com/opa

bundles:
  authz:
    service: registry-service
    resource: bundles/authz:v1.0.0
EOF
```

### 4.3 Git 分发

```bash
# 使用 Git 分发 Bundle
git clone https://github.com/example/opa-bundles.git
cd opa-bundles

# 创建 Bundle
opa bundle create bundle.tar.gz bundle/

# 推送更新
git add bundle.tar.gz
git commit -m "Update bundle"
git push
```

---

## 5. Bundle 部署

### 5.1 OPA Server 部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opa-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: opa-server
  template:
    metadata:
      labels:
        app: opa-server
    spec:
      containers:
        - name: opa
          image: openpolicyagent/opa:latest
          args:
            - "run"
            - "--server"
            - "--config-file=/etc/opa/config.yaml"
          volumeMounts:
            - name: opa-config
              mountPath: /etc/opa
      volumes:
        - name: opa-config
          configMap:
            name: opa-config
```

### 5.2 ConfigMap 配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: opa-config
data:
  config.yaml: |
    services:
      - name: bundle-service
        url: https://example.com/bundles
    bundles:
      authz:
        service: bundle-service
        resource: /authz/bundle.tar.gz
        polling:
          min_delay_seconds: 60
          max_delay_seconds: 120
```

### 5.3 Sidecar 部署

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: app
      image: myapp:v1.0
    - name: opa
      image: openpolicyagent/opa:latest
      args:
        - "run"
        - "--server"
        - "--config-file=/etc/opa/config.yaml"
      volumeMounts:
        - name: opa-config
          mountPath: /etc/opa
  volumes:
    - name: opa-config
      configMap:
        name: opa-config
```

---

## 6. 相关文档

### 6.1 理论论证

- **`../../00-theory/01-axioms/A5-A8-opa.md`** - OPA 公理（A5-A8）
- **`../../00-theory/05-lemmas-theorems/L3-opa-determinism.md`** - OPA 确定性引
  理

### 6.2 架构视角

- **`../../02-views/10-quick-views/opa-policy-governance-view.md`** - OPA 策略治
  理架构视角

### 6.3 技术文档

- **`../../../TECHNICAL/02-runtime-policy/policy-opa/policy-opa.md`** - OPA 技术文档

---

**更新时间**：2025-11-04 **版本**：v1.0 **状态**：✅ 基础示例已创建
