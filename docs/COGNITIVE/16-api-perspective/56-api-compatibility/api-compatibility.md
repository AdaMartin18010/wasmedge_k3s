# API 兼容性规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 兼容性架构](#11-兼容性架构)
- [2. 兼容性类型](#2-兼容性类型)
  - [2.1 向后兼容](#21-向后兼容)
  - [2.2 向前兼容](#22-向前兼容)
  - [2.3 双向兼容](#23-双向兼容)
- [3. 兼容性检查](#3-兼容性检查)
  - [3.1 Schema 兼容性](#31-schema-兼容性)
  - [3.2 行为兼容性](#32-行为兼容性)
- [4. 破坏性变更](#4-破坏性变更)
  - [4.1 变更分类](#41-变更分类)
  - [4.2 变更影响](#42-变更影响)
- [5. 兼容性测试](#5-兼容性测试)
  - [5.1 兼容性测试用例](#51-兼容性测试用例)
  - [5.2 兼容性验证](#52-兼容性验证)
- [6. 兼容性策略](#6-兼容性策略)
  - [6.1 版本策略](#61-版本策略)
  - [6.2 迁移策略](#62-迁移策略)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 兼容性规范定义了 API 在兼容性场景下的设计和实现，从兼容性类型到兼容性检查，
从破坏性变更到兼容性策略。

### 1.1 兼容性架构

```text
API 变更（API Change）
  ↓
兼容性检查（Compatibility Check）
  ↓
兼容性验证（Compatibility Verification）
  ↓
兼容性策略（Compatibility Strategy）
```

---

## 2. 兼容性类型

### 2.1 向后兼容

**向后兼容定义**：

```yaml
apiVersion: api.example.com/v1
kind: BackwardCompatibility
metadata:
  name: payment-api-backward-compatibility
spec:
  definition: "New API version can handle requests from old clients"
  examples:
    - type: add_field
      compatible: true
      description: "Adding optional fields"
    - type: add_endpoint
      compatible: true
      description: "Adding new endpoints"
    - type: remove_field
      compatible: false
      description: "Removing required fields"
```

**向后兼容示例**：

```yaml
# v1 API
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-v1
spec:
  paths:
    /api/v1/payments:
      post:
        requestBody:
          schema:
            type: object
            required: [order_id, amount]
            properties:
              order_id:
                type: string
              amount:
                type: integer

# v2 API (向后兼容)
apiVersion: api.example.com/v2
kind: APIDefinition
metadata:
  name: payment-api-v2
spec:
  paths:
    /api/v2/payments:
      post:
        requestBody:
          schema:
            type: object
            required: [order_id, amount]
            properties:
              order_id:
                type: string
              amount:
                type: integer
              currency:  # 新增可选字段
                type: string
                default: "USD"
```

### 2.2 向前兼容

**向前兼容定义**：

```yaml
apiVersion: api.example.com/v1
kind: ForwardCompatibility
metadata:
  name: payment-api-forward-compatibility
spec:
  definition: "Old API version can handle requests from new clients"
  examples:
    - type: ignore_unknown_fields
      compatible: true
      description: "Ignoring unknown fields"
    - type: default_values
      compatible: true
      description: "Using default values"
```

### 2.3 双向兼容

**双向兼容定义**：

```yaml
apiVersion: api.example.com/v1
kind: BidirectionalCompatibility
metadata:
  name: payment-api-bidirectional-compatibility
spec:
  definition: "Both API versions can handle requests from each other"
  requirements:
    - backward_compatible: true
    - forward_compatible: true
```

---

## 3. 兼容性检查

### 3.1 Schema 兼容性

**Schema 兼容性检查**：

```go
package main

import (
    "github.com/xeipuuv/gojsonschema"
)

func CheckSchemaCompatibility(oldSchema, newSchema string) (bool, []error) {
    oldLoader := gojsonschema.NewStringLoader(oldSchema)
    newLoader := gojsonschema.NewStringLoader(newSchema)

    // 检查向后兼容性
    backwardCompatible := checkBackwardCompatibility(oldLoader, newLoader)

    // 检查向前兼容性
    forwardCompatible := checkForwardCompatibility(oldLoader, newLoader)

    return backwardCompatible && forwardCompatible, nil
}

func checkBackwardCompatibility(old, new gojsonschema.JSONLoader) bool {
    // 新 schema 必须接受所有旧 schema 接受的请求
    // 实现兼容性检查逻辑
    return true
}
```

### 3.2 行为兼容性

**行为兼容性检查**：

```yaml
apiVersion: api.example.com/v1
kind: BehaviorCompatibility
metadata:
  name: payment-api-behavior-compatibility
spec:
  checks:
    - name: response_format
      description: "Response format must remain the same"
      test:
        request:
          method: POST
          path: /api/v1/payments
          body:
            order_id: "order_123"
            amount: 10000
        expectedResponse:
          status: 201
          body:
            payment_id: string
            status: string
    - name: error_handling
      description: "Error handling must remain consistent"
      test:
        request:
          method: POST
          path: /api/v1/payments
          body:
            order_id: ""
            amount: -1
        expectedResponse:
          status: 400
          error:
            code: VALIDATION_ERROR
```

---

## 4. 破坏性变更

### 4.1 变更分类

**破坏性变更分类**：

```yaml
apiVersion: api.example.com/v1
kind: BreakingChange
metadata:
  name: breaking-change-classification
spec:
  categories:
    - name: schema_change
      severity: HIGH
      examples:
        - "Remove required field"
        - "Change field type"
        - "Remove endpoint"
    - name: behavior_change
      severity: MEDIUM
      examples:
        - "Change error code"
        - "Change response format"
        - "Change authentication method"
    - name: contract_change
      severity: HIGH
      examples:
        - "Change request/response contract"
        - "Change error contract"
```

### 4.2 变更影响

**变更影响分析**：

```yaml
apiVersion: api.example.com/v1
kind: ChangeImpact
metadata:
  name: payment-api-change-impact
spec:
  change: "Remove field 'currency' from PaymentRequest"
  impact:
    affectedClients: 50
    affectedServices: ["order-service", "invoice-service"]
    migrationEffort: MEDIUM
    riskLevel: HIGH
  mitigation:
    - "Add deprecation notice"
    - "Provide migration guide"
    - "Support both formats temporarily"
```

---

## 5. 兼容性测试

### 5.1 兼容性测试用例

**兼容性测试用例**：

```yaml
apiVersion: api.example.com/v1
kind: CompatibilityTestCase
metadata:
  name: payment-api-compatibility-tests
spec:
  testCases:
    - name: backward_compatibility_test
      type: backward
      test:
        - request:
            apiVersion: v1
            method: POST
            path: /api/v1/payments
            body:
              order_id: "order_123"
              amount: 10000
          expectedStatus: 201
        - request:
            apiVersion: v2
            method: POST
            path: /api/v2/payments
            body:
              order_id: "order_123"
              amount: 10000
          expectedStatus: 201
    - name: forward_compatibility_test
      type: forward
      test:
        - request:
            apiVersion: v2
            method: POST
            path: /api/v2/payments
            body:
              order_id: "order_123"
              amount: 10000
              currency: "USD"
          expectedStatus: 201
```

### 5.2 兼容性验证

**兼容性验证工具**：

```yaml
apiVersion: api.example.com/v1
kind: CompatibilityValidator
metadata:
  name: api-compatibility-validator
spec:
  tools:
    - name: openapi-diff
      enabled: true
      config:
        format: markdown
        failOnBreaking: true
    - name: spectral
      enabled: true
      rules:
        - oas3-api-servers
        - oas3-operation-tags
```

---

## 6. 兼容性策略

### 6.1 版本策略

**版本策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: CompatibilityVersionStrategy
metadata:
  name: payment-api-version-strategy
spec:
  strategy: semantic_versioning
  rules:
    - version: "1.x.x"
      compatible: true
      description: "Patch and minor versions are backward compatible"
    - version: "2.x.x"
      compatible: false
      description: "Major versions may have breaking changes"
  migration:
    - from: "1.x.x"
      to: "2.x.x"
      guide: "https://api.example.com/migration/v1-to-v2"
```

### 6.2 迁移策略

**迁移策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: CompatibilityMigrationStrategy
metadata:
  name: payment-api-migration-strategy
spec:
  strategy: gradual
  phases:
    - phase: parallel_support
      duration: "6m"
      actions:
        - "Support both v1 and v2"
        - "Monitor v1 usage"
        - "Encourage v2 migration"
    - phase: deprecation
      duration: "6m"
      actions:
        - "Deprecate v1"
        - "Provide migration tools"
        - "Monitor migration progress"
    - phase: sunset
      duration: "1m"
      actions:
        - "Disable v1"
        - "Archive v1"
```

---

## 7. 相关文档

- **[API 版本管理](../23-api-versioning/api-versioning.md)** - API 版本控制
- **[API 弃用策略](../55-api-deprecation/api-deprecation.md)** - API 弃用
- **[API 契约测试](../51-api-contract-testing/api-contract-testing.md)** - 契约
  兼容性
- **[最佳实践](../08-best-practices/best-practices.md)** - 兼容性最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
