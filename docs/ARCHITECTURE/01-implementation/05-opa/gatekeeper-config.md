# Gatekeeper 配置示例

## 📑 目录

- [1. 概述](#1-概述)
- [2. Gatekeeper 安装配置](#2-gatekeeper-安装配置)
- [3. ConstraintTemplate 示例](#3-constrainttemplate-示例)
- [4. Constraint 示例](#4-constraint-示例)
- [5. 相关文档](#5-相关文档)

---

## 1. 概述

本文档提供 **Gatekeeper 的实际配置示例**，展示如何通过 Gatekeeper 在 Kubernetes
中实施 OPA 策略。

### 1.1 理论基础

Gatekeeper 配置基于以下理论论证：

- **公理 A5-A8（OPA 公理）**：
  - A5：能力闭包
  - A6：最小权限
  - A7：可证明性
  - A8：版本一致性
- **引理 L3（OPA 确定性）**：OPA 求值过程 ≡ 单调不动点迭代，决策在有限步内唯一且
  可重现

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2. Gatekeeper 安装配置

### 2.1 Helm 安装 Gatekeeper

```bash
# 添加 Gatekeeper Helm 仓库
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts

# 安装 Gatekeeper
helm install gatekeeper gatekeeper/gatekeeper \
  --namespace gatekeeper-system \
  --create-namespace
```

### 2.2 Gatekeeper 验证安装

```bash
# 检查 Gatekeeper 组件
kubectl get pods -n gatekeeper-system

# 检查 Gatekeeper CRD
kubectl get crd | grep gatekeeper
```

### 2.3 Gatekeeper 配置

```yaml
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
  namespace: gatekeeper-system
spec:
  match:
    - excludedNamespaces: ["kube-system", "kube-public", "kube-node-lease"]
    - processes: ["*"]
```

---

## 3. ConstraintTemplate 示例

### 3.1 镜像验证 ConstraintTemplate

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredimages
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredImages
      validation:
        openAPIV3Schema:
          type: object
          properties:
            allowedRepos:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredimages

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not starts_with(container.image, allowed_repo)
          allowed_repo := input.parameters.allowedRepos[_]
          msg := sprintf("Image '%v' is not from allowed repositories", [container.image])
        }
```

### 3.2 资源限制 ConstraintTemplate

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredresources
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredResources
      validation:
        openAPIV3Schema:
          type: object
          properties:
            limits:
              type: object
              properties:
                cpu:
                  type: string
                memory:
                  type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredresources

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.resources.limits
          msg := sprintf("Container '%v' must specify resource limits", [container.name])
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          cpu_limit := container.resources.limits.cpu
          cpu_limit > input.parameters.limits.cpu
          msg := sprintf("Container '%v' CPU limit '%v' exceeds maximum '%v'", [container.name, cpu_limit, input.parameters.limits.cpu])
        }
```

### 3.3 标签验证 ConstraintTemplate

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg}] {
          required_label := input.parameters.labels[_]
          not input.review.object.metadata.labels[required_label]
          msg := sprintf("Missing required label: %v", [required_label])
        }
```

---

## 4. Constraint 示例

### 4.1 镜像验证 Constraint

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredImages
metadata:
  name: must-have-allowed-repo
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    allowedRepos:
      - "yourhub.com/"
      - "gcr.io/"
```

### 4.2 资源限制 Constraint

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredResources
metadata:
  name: must-have-resource-limits
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    limits:
      cpu: "2"
      memory: "2Gi"
```

### 4.3 标签验证 Constraint

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: must-have-labels
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    labels:
      - "app"
      - "version"
      - "environment"
```

---

## 5. 相关文档

### 5.1 理论论证

- **`../../00-theory/01-axioms/A5-A8-opa.md`** - OPA 公理（A5-A8）
- **`../../00-theory/05-lemmas-theorems/L3-opa-determinism.md`** - OPA 确定性引
  理

### 5.2 架构视角

- **`../../01-views/opa-policy-governance-view.md`** - OPA 策略治理架构视角

### 5.3 技术文档

- **`../../../TECHNICAL/06-policy-opa/policy-opa.md`** - OPA 技术文档

---

**更新时间**：2025-11-04 **版本**：v1.0 **状态**：✅ 基础示例已创建
