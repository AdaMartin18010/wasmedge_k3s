# API 版本管理规范

**版本**：v1.0 **最后更新：2025-11-15 **维护者**：项目团队

## 📑 目录

- [API 版本管理规范](#api-版本管理规范)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 版本管理流程](#11-版本管理流程)
    - [1.2 API 版本管理在 API 规范中的位置](#12-api-版本管理在-api-规范中的位置)
  - [2 版本策略](#2-版本策略)
    - [2.1 语义化版本](#21-语义化版本)
    - [2.2 API 版本策略](#22-api-版本策略)
  - [3 版本兼容性](#3-版本兼容性)
    - [3.1 向后兼容性](#31-向后兼容性)
    - [3.2 破坏性变更](#32-破坏性变更)
  - [4 版本迁移](#4-版本迁移)
    - [4.1 渐进式迁移](#41-渐进式迁移)
    - [4.2 版本共存](#42-版本共存)
  - [5 版本弃用](#5-版本弃用)
    - [5.1 弃用策略](#51-弃用策略)
    - [5.2 生命周期管理](#52-生命周期管理)
  - [6 版本管理工具](#6-版本管理工具)
    - [6.1 Git 版本管理](#61-git-版本管理)
    - [6.2 CRD 版本管理](#62-crd-版本管理)
  - [7 形式化定义与理论基础](#7-形式化定义与理论基础)
    - [7.1 API 版本形式化模型](#71-api-版本形式化模型)
    - [7.2 版本兼容性形式化](#72-版本兼容性形式化)
    - [7.3 版本迁移形式化](#73-版本迁移形式化)
  - [8 相关文档](#8-相关文档)

---

## 1 概述

API 版本管理规范定义了 API 在不同运行时环境下的版本管理策略，从版本号规范到兼容
性保证，从版本迁移到版本弃用。本文档基于形式化方法，提供严格的数学定义和推理论证
，分析 API 版本管理的理论基础和实践方法。

**参考标准**：

- [Semantic Versioning](https://semver.org/) - 语义化版本规范
- [Kubernetes API Versioning](https://kubernetes.io/docs/reference/using-api/api-concepts/#api-versioning) -
  Kubernetes API 版本管理
- [OpenAPI Versioning](https://swagger.io/specification/) - OpenAPI 版本管理
- [API Versioning Best Practices](https://restfulapi.net/versioning/) - API 版本
  管理最佳实践
- [Versioning Strategies](https://www.baeldung.com/rest-versioning) - 版本管理策
  略

### 1.1 版本管理流程

```text
版本设计（语义化版本）
  ↓
版本发布（Git Tag、CRD 版本）
  ↓
版本兼容性（向后兼容、破坏性变更）
  ↓
版本迁移（渐进式迁移、并行运行）
  ↓
版本弃用（弃用通知、生命周期管理）
```

### 1.2 API 版本管理在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API 版本管理是 Governance 维度的核心组成部分：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
                    ↑
            API Versioning (core)
```

API 版本管理在 API 规范中提供：

- **版本定义**：语义化版本号、API 版本标识
- **兼容性保证**：向后兼容性、破坏性变更管理
- **版本迁移**：渐进式迁移、版本共存策略
- **生命周期管理**：版本弃用、版本下线流程

---

## 2 版本策略

### 2.1 语义化版本

**版本号格式**：

```text
MAJOR.MINOR.PATCH

MAJOR: 破坏性变更
MINOR: 向后兼容的新功能
PATCH: 向后兼容的 bug 修复
```

**版本示例**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api
spec:
  version: "1.2.3"
  versioning:
    strategy: semantic
    major: 1
    minor: 2
    patch: 3
```

### 2.2 API 版本策略

**URL 版本控制**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-v1
spec:
  version: "1.0.0"
  paths:
    /api/v1/payments:
      get:
        summary: List payments
```

**Header 版本控制**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-header-version
spec:
  version: "2.0.0"
  versioning:
    strategy: header
    header: "API-Version"
    default: "2.0.0"
```

---

## 3 版本兼容性

### 3.1 向后兼容性

**兼容性保证**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-v1
spec:
  version: "1.0.0"
  compatibility:
    backwardCompatible: true
    breakingChanges: []
    deprecatedFields:
      - name: old_field
        replacement: new_field
        removalDate: "2025-12-31"
```

**兼容性测试**：

```yaml
apiVersion: api.example.com/v1
kind: APITest
metadata:
  name: compatibility-test
spec:
  testType: compatibility
  sourceVersion: "1.0.0"
  targetVersion: "1.1.0"
  tests:
    - name: backward-compatibility
      assertions:
        - type: schema
          check: backwardCompatible
```

### 3.2 破坏性变更

**破坏性变更声明**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-v2
spec:
  version: "2.0.0"
  compatibility:
    backwardCompatible: false
    breakingChanges:
      - description: "Removed field 'old_field'"
        migrationGuide: "https://docs.example.com/migration/v1-to-v2"
      - description: "Changed response format"
        migrationGuide: "https://docs.example.com/migration/v1-to-v2"
```

---

## 4 版本迁移

### 4.1 渐进式迁移

**迁移策略**：

```yaml
apiVersion: api.example.com/v1
kind: APIMigration
metadata:
  name: payment-api-migration
spec:
  sourceVersion: "1.0.0"
  targetVersion: "2.0.0"
  strategy: gradual
  trafficSplit:
    - version: "1.0.0"
      weight: 90
    - version: "2.0.0"
      weight: 10
  rollbackThreshold: 0.05
```

**VirtualService 流量分割**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-api-vs
spec:
  hosts:
    - payment-api
  http:
    - match:
        - headers:
            api-version:
              exact: "2.0.0"
      route:
        - destination:
            host: payment-api-v2
    - route:
        - destination:
            host: payment-api-v1
          weight: 90
        - destination:
            host: payment-api-v2
          weight: 10
```

### 4.2 版本共存

**多版本部署**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-api-v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-api
      version: "1.0.0"
  template:
    metadata:
      labels:
        app: payment-api
        version: "1.0.0"
    spec:
      containers:
        - name: app
          image: payment-api:v1.0.0
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-api-v2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: payment-api
      version: "2.0.0"
  template:
    metadata:
      labels:
        app: payment-api
        version: "2.0.0"
    spec:
      containers:
        - name: app
          image: payment-api:v2.0.0
```

---

## 5 版本弃用

### 5.1 弃用策略

**弃用声明**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-v1-deprecated
spec:
  version: "1.0.0"
  lifecycle: deprecated
  deprecationPolicy:
    announcementDate: "2025-01-01"
    sunsetDate: "2025-12-31"
    migrationGuide: "https://docs.example.com/migration/v1-to-v2"
    supportContact: "api-support@example.com"
```

**弃用通知**：

```yaml
apiVersion: api.example.com/v1
kind: APIDeprecation
metadata:
  name: payment-api-v1-deprecation
spec:
  apiVersion: "1.0.0"
  deprecationDate: "2025-01-01"
  sunsetDate: "2025-12-31"
  notifications:
    - type: header
      header: "Deprecation"
      value: 'version="1.0.0", sunset="2025-12-31"'
    - type: response
      field: "deprecation_warning"
```

### 5.2 生命周期管理

**生命周期状态**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-lifecycle
spec:
  version: "1.0.0"
  lifecycle: active
  lifecyclePolicy:
    states:
      - state: alpha
        duration: "3M"
      - state: beta
        duration: "6M"
      - state: stable
        duration: "12M"
      - state: deprecated
        duration: "6M"
      - state: sunset
        duration: "0"
```

---

## 6 版本管理工具

### 6.1 Git 版本管理

**Git Tag 管理**：

```bash
# 创建版本标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签
git push origin v1.0.0

# 查看版本标签
git tag -l "v1.*"
```

**版本发布流程**：

```yaml
# .github/workflows/release.yml
name: API Release
on:
  push:
    tags:
      - "v*"
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Create API Definition
        run: |
          kubectl apply -f api-definition.yaml
          kubectl annotate apidefinition payment-api \
            version=${{ github.ref_name }}
```

### 6.2 CRD 版本管理

**CRD 版本升级**：

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: apidefinitions.api.example.com
spec:
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                version:
                  type: string
    - name: v2
      served: true
      storage: false
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                version:
                  type: string
                newField:
                  type: string
```

---

## 7 形式化定义与理论基础

### 7.1 API 版本形式化模型

**定义 7.1（API 版本）**：API 版本是一个三元组：

```text
API_Version = ⟨Major, Minor, Patch⟩
```

其中：

- **Major**：主版本号 `Major: ℕ`（破坏性变更）
- **Minor**：次版本号 `Minor: ℕ`（向后兼容的新功能）
- **Patch**：补丁版本号 `Patch: ℕ`（向后兼容的 bug 修复）

**定义 7.2（版本比较）**：版本比较是一个函数：

```text
Compare_Version: API_Version × API_Version → {Less, Equal, Greater}
```

**定理 7.1（版本序关系）**：版本号具有全序关系：

```text
∀v₁, v₂: Compare_Version(v₁, v₂) ∈ {Less, Equal, Greater}
```

**证明**：根据语义化版本规范，版本号可以按字典序比较，因此具有全序关系。□

### 7.2 版本兼容性形式化

**定义 7.3（向后兼容性）**：向后兼容性是一个函数：

```text
Backward_Compatible: API_Version × API_Version → Bool
```

**定义 7.4（破坏性变更）**：破坏性变更是一个函数：

```text
Breaking_Change: API_Version × API_Version → Bool
```

**定理 7.2（版本兼容性规则）**：相同主版本号的不同次版本号向后兼容：

```text
v₁.Major = v₂.Major ∧ v₁.Minor ≤ v₂.Minor ⟹ Backward_Compatible(v₁, v₂)
```

**证明**：根据语义化版本规范，相同主版本号的不同次版本号只添加向后兼容的新功能，
因此向后兼容。□

**定理 7.3（破坏性变更规则）**：不同主版本号之间存在破坏性变更：

```text
v₁.Major ≠ v₂.Major ⟹ Breaking_Change(v₁, v₂)
```

**证明**：根据语义化版本规范，主版本号变更表示破坏性变更，因此不同主版本号之间存
在破坏性变更。□

### 7.3 版本迁移形式化

**定义 7.5（版本迁移）**：版本迁移是一个函数：

```text
Migrate_Version: API_Version × API_Version → Migration_Plan
```

其中 `Migration_Plan = ⟨Steps, Compatibility_Check, Rollback_Plan⟩`。

**定义 7.6（版本共存）**：版本共存是一个函数：

```text
Coexist_Versions: API_Version[] → Bool
```

**定理 7.4（版本共存条件）**：如果版本向后兼容，则可以共存：

```text
∀v₁, v₂ ∈ Versions: Backward_Compatible(v₁, v₂) ⟹ Coexist_Versions([v₁, v₂])
```

**证明**：如果版本向后兼容，则旧版本客户端可以继续使用，新版本客户端可以使用新功
能，因此可以共存。□

---

## 8 相关文档

- **[API 演进路径](../00-foundation/04-api-evolution.md)** - API 演进理论
- **[API 迁移指南](../08-operations/01-api-migration.md)** - 版本迁移实践
- **[最佳实践](../00-foundation/05-best-practices.md)** - 版本管理最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新：2025-11-15 **维护者**：项目团队
