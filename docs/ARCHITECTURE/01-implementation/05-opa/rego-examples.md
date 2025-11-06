# Rego 语言示例

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 理论基础](#11-理论基础)
- [2. 基础 Rego 示例](#2-基础-rego-示例)
  - [2.1 简单允许/拒绝策略](#21-简单允许拒绝策略)
  - [2.2 资源访问控制策略](#22-资源访问控制策略)
  - [2.3 条件策略](#23-条件策略)
- [3. Kubernetes 准入控制示例](#3-kubernetes-准入控制示例)
  - [3.1 Pod 镜像验证策略](#31-pod-镜像验证策略)
  - [3.2 资源配额策略](#32-资源配额策略)
  - [3.3 标签验证策略](#33-标签验证策略)
- [4. 镜像验证策略示例](#4-镜像验证策略示例)
  - [4.1 镜像仓库验证](#41-镜像仓库验证)
  - [4.2 镜像签名验证](#42-镜像签名验证)
- [5. 相关文档](#5-相关文档)
  - [5.1 理论论证](#51-理论论证)
  - [5.2 架构视角](#52-架构视角)
  - [5.3 技术文档](#53-技术文档)

---

## 1. 概述

本文档提供 **Rego 语言的实际代码示例**，包含可直接使用的策略代码。

### 1.1 理论基础

OPA 实现基于以下理论论证：

- **公理 A5-A8（OPA 公理）**：
  - A5：能力闭包
  - A6：最小权限
  - A7：可证明性
  - A8：版本一致性
- **引理 L3（OPA 确定性）**：OPA 求值过程 ≡ 单调不动点迭代，决策在有限步内唯一且
  可重现

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2. 基础 Rego 示例

### 2.1 简单允许/拒绝策略

```rego
package example

import rego.v1

# 允许策略
allow {
    input.user == "admin"
}

# 拒绝策略
deny[msg] {
    input.user == "guest"
    msg := "Guest users are not allowed"
}
```

### 2.2 资源访问控制策略

```rego
package example

import rego.v1

# 允许访问资源
allow {
    # 用户是资源所有者
    input.user == input.resource.owner
}

allow {
    # 用户有管理员角色
    input.user.roles[_] == "admin"
}

# 拒绝访问资源
deny[msg] {
    not allow
    msg := "Access denied"
}
```

### 2.3 条件策略

```rego
package example

import rego.v1

# 条件允许
allow {
    input.method == "GET"
    input.path == "/public"
}

allow {
    input.method == "POST"
    input.user.roles[_] == "editor"
    input.path == "/articles"
}

# 默认拒绝
default allow := false
```

---

## 3. Kubernetes 准入控制示例

### 3.1 Pod 镜像验证策略

```rego
package kubernetes.admission

import rego.v1

# 拒绝使用未授权镜像的 Pod
deny[msg] {
    input.request.kind.kind == "Pod"
    image := input.request.object.spec.containers[_].image
    not startswith(image, "yourhub/")
    msg := sprintf("untrusted image: %v", [image])
}

# 拒绝使用 latest 标签的镜像
deny[msg] {
    input.request.kind.kind == "Pod"
    image := input.request.object.spec.containers[_].image
    endswith(image, ":latest")
    msg := sprintf("image with latest tag is not allowed: %v", [image])
}
```

### 3.2 资源配额策略

```rego
package kubernetes.admission

import rego.v1

# 拒绝超过资源限制的 Pod
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.resources.requests.memory > "512Mi"
    msg := sprintf("memory request exceeds limit: %v", [container.resources.requests.memory])
}

# 拒绝没有资源限制的 Pod
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources
    msg := sprintf("container %v must specify resource limits", [container.name])
}
```

### 3.3 标签验证策略

```rego
package kubernetes.admission

import rego.v1

# 拒绝缺少必需标签的 Pod
deny[msg] {
    input.request.kind.kind == "Pod"
    not input.request.object.metadata.labels["app"]
    msg := "pod must have 'app' label"
}

deny[msg] {
    input.request.kind.kind == "Pod"
    not input.request.object.metadata.labels["version"]
    msg := "pod must have 'version' label"
}
```

---

## 4. 镜像验证策略示例

### 4.1 镜像仓库验证

```rego
package image.validation

import rego.v1

# 允许的镜像仓库列表
allowed_registries := [
    "yourhub.com",
    "gcr.io",
    "docker.io/library"
]

# 验证镜像是否来自允许的仓库
deny[msg] {
    image := input.image
    registry := split(image, "/")[0]
    not registry in allowed_registries
    msg := sprintf("image registry not allowed: %v", [registry])
}
```

### 4.2 镜像签名验证

```rego
package image.validation

import rego.v1

# 验证镜像签名
deny[msg] {
    image := input.image
    not has_signature(image)
    msg := sprintf("image %v is not signed", [image])
}

# 检查镜像是否有签名（简化示例）
has_signature(image) {
    # 实际实现需要调用镜像签名验证 API
    startswith(image, "yourhub.com/signed/")
}
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
