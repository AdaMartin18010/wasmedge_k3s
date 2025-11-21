# Policy Bundle 示例

## 📑 目录

- [Policy Bundle 示例](#policy-bundle-示例)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 理论基础](#11-理论基础)
  - [2 Bundle 结构](#2-bundle-结构)
    - [2.1 Bundle 目录结构](#21-bundle-目录结构)
    - [2.2 manifest.json](#22-manifestjson)
  - [3 Bundle 创建](#3-bundle-创建)
    - [3.1 创建策略文件](#31-创建策略文件)
    - [3.2 创建数据文件](#32-创建数据文件)
    - [3.3 创建 Bundle](#33-创建-bundle)
  - [4 Bundle 分发](#4-bundle-分发)
    - [4.1 HTTP/HTTPS 分发](#41-httphttps-分发)
    - [4.2 OCI Registry 分发](#42-oci-registry-分发)
    - [4.3 Git 分发](#43-git-分发)
  - [5 Bundle 部署](#5-bundle-部署)
    - [5.1 OPA Server 部署](#51-opa-server-部署)
    - [5.2 ConfigMap 配置](#52-configmap-配置)
    - [5.3 Sidecar 部署](#53-sidecar-部署)
  - [6 相关文档](#6-相关文档)
    - [6.1 理论论证](#61-理论论证)
    - [6.2 架构视角](#62-架构视角)
    - [6.3 技术文档](#63-技术文档)
  - [7 2025 年最新实践](#7-2025-年最新实践)
    - [7.1 OPA 0.60+ Bundle 增强（2025）](#71-opa-060-bundle-增强2025)
    - [7.2 OCI Registry Bundle 分发（2025）](#72-oci-registry-bundle-分发2025)
    - [7.3 Wasm Bundle 编译（2025）](#73-wasm-bundle-编译2025)
  - [8 实际应用案例](#8-实际应用案例)
    - [案例 1：多环境策略管理](#案例-1多环境策略管理)
    - [案例 2：策略版本管理](#案例-2策略版本管理)
    - [案例 3：分布式策略分发](#案例-3分布式策略分发)

---

## 1 概述

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

## 2 Bundle 结构

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

## 3 Bundle 创建

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

## 4 Bundle 分发

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

## 5 Bundle 部署

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

## 6 相关文档

### 6.1 理论论证

- **`../../00-theory/01-axioms/A5-A8-opa.md`** - OPA 公理（A5-A8）
- **`../../00-theory/05-lemmas-theorems/L3-opa-determinism.md`** - OPA 确定性引
  理

### 6.2 架构视角

- **`../../02-views/10-quick-views/opa-policy-governance-view.md`** - OPA 策略治
  理架构视角

### 6.3 技术文档

- **`../../../TECHNICAL/02-runtime-policy/policy-opa/policy-opa.md`** - OPA 技术文档

## 7 2025 年最新实践

### 7.1 OPA 0.60+ Bundle 增强（2025）

**最新版本**：OPA 0.60+（2025 年）

**新特性**：

- **Bundle 签名验证**：支持 Bundle 签名验证
- **增量 Bundle 更新**：支持增量 Bundle 更新
- **Bundle 压缩优化**：改进的 Bundle 压缩

**配置示例**：

```yaml
# OPA 0.60+ Bundle 配置
services:
  - name: bundle-service
    url: https://example.com/bundles
    credentials:
      bearer:
        token: ${BUNDLE_TOKEN}
bundles:
  authz:
    service: bundle-service
    resource: /authz/bundle.tar.gz
    # 启用签名验证
    signing:
      keyid: mykey
      public_key: |
        -----BEGIN PUBLIC KEY-----
        ...
        -----END PUBLIC KEY-----
    polling:
      min_delay_seconds: 60
      max_delay_seconds: 120
```

### 7.2 OCI Registry Bundle 分发（2025）

**2025 年趋势**：使用 OCI Registry 分发 Bundle

**优势**：

- **统一管理**：使用 OCI Registry 统一管理
- **版本控制**：支持 Bundle 版本控制
- **安全扫描**：支持 Bundle 安全扫描

**配置示例**：

```yaml
# OCI Registry Bundle 配置
services:
  - name: oci-registry
    url: https://registry.example.com
    type: oci
bundles:
  authz:
    service: oci-registry
    resource: bundles/authz:latest
    polling:
      min_delay_seconds: 60
      max_delay_seconds: 120
```

### 7.3 Wasm Bundle 编译（2025）

**2025 年趋势**：使用 Wasm 编译 Bundle 提升性能

**配置示例**：

```bash
# 编译 Bundle 为 Wasm
opa build -t wasm -e authz/allow bundle/

# 使用 Wasm Bundle
opa run --server --set bundles.authz.resource=bundle.wasm
```

## 8 实际应用案例

### 案例 1：多环境策略管理

**场景**：在不同环境使用不同的策略 Bundle

**实现方案**：

```yaml
# 生产环境 Bundle 配置
services:
  - name: prod-bundle-service
    url: https://bundles.example.com/prod
bundles:
  authz:
    service: prod-bundle-service
    resource: /prod/authz/bundle.tar.gz
    polling:
      min_delay_seconds: 300
      max_delay_seconds: 600
---
# 开发环境 Bundle 配置
services:
  - name: dev-bundle-service
    url: https://bundles.example.com/dev
bundles:
  authz:
    service: dev-bundle-service
    resource: /dev/authz/bundle.tar.gz
    polling:
      min_delay_seconds: 60
      max_delay_seconds: 120
```

**效果**：

- 环境隔离：每个环境有独立的策略
- 灵活配置：不同环境使用不同策略
- 统一管理：通过 Bundle 统一管理

### 案例 2：策略版本管理

**场景**：管理策略版本和回滚

**实现方案**：

```bash
# 创建策略版本
opa build -b bundle/ -o bundle-v1.0.0.tar.gz

# 上传到 Registry
docker push registry.example.com/bundles/authz:v1.0.0

# 回滚到旧版本
kubectl set image deployment/opa opa=openpolicyagent/opa:latest \
  --env="BUNDLE_VERSION=v1.0.0"
```

**效果**：

- 版本控制：支持策略版本管理
- 快速回滚：快速回滚到旧版本
- 灰度发布：支持策略灰度发布

### 案例 3：分布式策略分发

**场景**：在多个集群中分发策略 Bundle

**实现方案**：

```yaml
# 多集群 Bundle 配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: opa-config
data:
  config.yaml: |
    services:
      - name: bundle-service
        url: https://bundles.example.com
    bundles:
      authz:
        service: bundle-service
        resource: /authz/bundle.tar.gz
        # 启用签名验证
        signing:
          keyid: mykey
          public_key: |
            -----BEGIN PUBLIC KEY-----
            ...
            -----END PUBLIC KEY-----
        polling:
          min_delay_seconds: 60
          max_delay_seconds: 120
```

**效果**：

- 统一分发：多个集群使用相同的策略
- 安全验证：通过签名验证 Bundle 完整性
- 自动更新：策略自动更新到所有集群

---

**更新时间**：2025-11-15 **版本**：v1.1 **状态**：✅ 包含 2025 年最新实践
