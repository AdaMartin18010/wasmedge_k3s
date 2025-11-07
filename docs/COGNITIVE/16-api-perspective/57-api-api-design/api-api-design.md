# API 设计规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 API 设计原则](#11-api-设计原则)
- [2. 资源设计](#2-资源设计)
  - [2.1 资源命名](#21-资源命名)
  - [2.2 资源关系](#22-资源关系)
- [3. 操作设计](#3-操作设计)
  - [3.1 HTTP 方法映射](#31-http-方法映射)
  - [3.2 自定义操作](#32-自定义操作)
- [4. 数据模型设计](#4-数据模型设计)
  - [4.1 数据类型](#41-数据类型)
  - [4.2 数据验证](#42-数据验证)
- [5. 错误设计](#5-错误设计)
  - [5.1 错误码设计](#51-错误码设计)
  - [5.2 错误消息设计](#52-错误消息设计)
- [6. 版本设计](#6-版本设计)
  - [6.1 版本策略](#61-版本策略)
  - [6.2 版本演进](#62-版本演进)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 设计规范定义了 API 在设计阶段的原则和最佳实践，从资源设计到操作设计，从数据
模型到错误处理。

### 1.1 API 设计原则

```text
一致性（Consistency）
  ↓
简洁性（Simplicity）
  ↓
可扩展性（Extensibility）
  ↓
可维护性（Maintainability）
```

---

## 2. 资源设计

### 2.1 资源命名

**资源命名规范**：

```yaml
apiVersion: api.example.com/v1
kind: ResourceNamingPolicy
metadata:
  name: resource-naming-policy
spec:
  rules:
    - name: use_nouns
      description: "Use nouns, not verbs"
      examples:
        good: "/api/v1/payments"
        bad: "/api/v1/createPayment"
    - name: use_plural
      description: "Use plural nouns"
      examples:
        good: "/api/v1/payments"
        bad: "/api/v1/payment"
    - name: use_hyphens
      description: "Use hyphens for multi-word resources"
      examples:
        good: "/api/v1/payment-methods"
        bad: "/api/v1/paymentMethods"
```

### 2.2 资源关系

**资源关系设计**：

```yaml
apiVersion: api.example.com/v1
kind: ResourceRelationship
metadata:
  name: payment-resource-relationships
spec:
  resources:
    - name: payments
      relationships:
        - type: belongs_to
          resource: orders
          path: /api/v1/orders/{order_id}/payments
        - type: has_many
          resource: refunds
          path: /api/v1/payments/{payment_id}/refunds
```

---

## 3. 操作设计

### 3.1 HTTP 方法映射

**HTTP 方法映射规范**：

```yaml
apiVersion: api.example.com/v1
kind: HTTPMethodMapping
metadata:
  name: http-method-mapping
spec:
  mappings:
    - method: GET
      operation: read
      idempotent: true
      safe: true
      examples:
        - "/api/v1/payments"
        - "/api/v1/payments/{id}"
    - method: POST
      operation: create
      idempotent: false
      safe: false
      examples:
        - "/api/v1/payments"
    - method: PUT
      operation: update_full
      idempotent: true
      safe: false
      examples:
        - "/api/v1/payments/{id}"
    - method: PATCH
      operation: update_partial
      idempotent: false
      safe: false
      examples:
        - "/api/v1/payments/{id}"
    - method: DELETE
      operation: delete
      idempotent: true
      safe: false
      examples:
        - "/api/v1/payments/{id}"
```

### 3.2 自定义操作

**自定义操作设计**：

```yaml
apiVersion: api.example.com/v1
kind: CustomOperation
metadata:
  name: payment-custom-operations
spec:
  operations:
    - name: refund
      method: POST
      path: /api/v1/payments/{id}/refund
      description: "Refund a payment"
    - name: cancel
      method: POST
      path: /api/v1/payments/{id}/cancel
      description: "Cancel a payment"
    - name: retry
      method: POST
      path: /api/v1/payments/{id}/retry
      description: "Retry a failed payment"
```

---

## 4. 数据模型设计

### 4.1 数据类型

**数据类型规范**：

```yaml
apiVersion: api.example.com/v1
kind: DataTypePolicy
metadata:
  name: data-type-policy
spec:
  types:
    - name: string
      useCase: "Text data"
      examples:
        - "order_id"
        - "description"
    - name: integer
      useCase: "Whole numbers"
      examples:
        - "amount"
        - "quantity"
    - name: number
      useCase: "Decimal numbers"
      examples:
        - "price"
        - "discount"
    - name: boolean
      useCase: "True/false values"
      examples:
        - "is_active"
        - "is_verified"
    - name: datetime
      useCase: "Date and time"
      format: ISO8601
      examples:
        - "created_at"
        - "updated_at"
```

### 4.2 数据验证

**数据验证规则**：

```yaml
apiVersion: api.example.com/v1
kind: DataValidationPolicy
metadata:
  name: data-validation-policy
spec:
  rules:
    - field: order_id
      type: string
      required: true
      pattern: "^order_[a-zA-Z0-9]+$"
      minLength: 10
      maxLength: 50
    - field: amount
      type: integer
      required: true
      minimum: 1
      maximum: 1000000
    - field: currency
      type: string
      required: false
      enum: ["USD", "EUR", "CNY"]
      default: "USD"
```

---

## 5. 错误设计

### 5.1 错误码设计

**错误码规范**：

```yaml
apiVersion: api.example.com/v1
kind: ErrorCodePolicy
metadata:
  name: error-code-policy
spec:
  format: "SERVICE_ERROR_TYPE"
  codes:
    - code: PAYMENT_INSUFFICIENT_FUNDS
      httpStatus: 400
      description: "Insufficient funds"
    - code: PAYMENT_INVALID_CARD
      httpStatus: 400
      description: "Invalid card number"
    - code: PAYMENT_NOT_FOUND
      httpStatus: 404
      description: "Payment not found"
    - code: PAYMENT_GATEWAY_ERROR
      httpStatus: 502
      description: "Payment gateway error"
```

### 5.2 错误消息设计

**错误消息规范**：

```yaml
apiVersion: api.example.com/v1
kind: ErrorMessagePolicy
metadata:
  name: error-message-policy
spec:
  format:
    - code
    - message
    - details
    - request_id
  examples:
    - code: PAYMENT_INSUFFICIENT_FUNDS
      message: "Insufficient funds"
      details:
        account_id: "acc_123"
        required_amount: 10000
        available_balance: 5000
```

---

## 6. 版本设计

### 6.1 版本策略

**版本策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: VersionStrategy
metadata:
  name: api-version-strategy
spec:
  strategy: url_versioning
  format: "v{major}.{minor}"
  examples:
    - "/api/v1/payments"
    - "/api/v2/payments"
  rules:
    - major: "Breaking changes"
    - minor: "Backward compatible changes"
```

### 6.2 版本演进

**版本演进策略**：

```yaml
apiVersion: api.example.com/v1
kind: VersionEvolution
metadata:
  name: api-version-evolution
spec:
  evolution:
    - version: "v1"
      status: stable
      deprecationDate: null
    - version: "v2"
      status: beta
      deprecationDate: null
      migrationGuide: "https://api.example.com/migration/v1-to-v2"
```

---

## 7. 相关文档

- **[API 标准化规范](../25-api-standardization/api-standardization.md)** - API
  标准
- **[API 版本管理](../23-api-versioning/api-versioning.md)** - API 版本控制
- **[API 兼容性规范](../56-api-compatibility/api-compatibility.md)** - API 兼容
  性
- **[最佳实践](../08-best-practices/best-practices.md)** - API 设计最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
