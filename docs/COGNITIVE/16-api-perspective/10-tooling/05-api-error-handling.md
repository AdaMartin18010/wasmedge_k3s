# API 错误处理规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 错误处理架构](#11-错误处理架构)
  - [1.2 API 错误处理在 API 规范中的位置](#12-api-错误处理在-api-规范中的位置)
- [2. 错误分类](#2-错误分类)
  - [2.1 HTTP 状态码](#21-http-状态码)
  - [2.2 业务错误码](#22-业务错误码)
  - [2.3 错误严重性](#23-错误严重性)
- [3. 错误响应格式](#3-错误响应格式)
  - [3.1 标准错误格式](#31-标准错误格式)
  - [3.2 错误详情](#32-错误详情)
  - [3.3 错误追踪](#33-错误追踪)
- [4. 错误处理策略](#4-错误处理策略)
  - [4.1 错误重试](#41-错误重试)
  - [4.2 错误降级](#42-错误降级)
  - [4.3 错误恢复](#43-错误恢复)
- [5. 错误日志](#5-错误日志)
  - [5.1 日志格式](#51-日志格式)
  - [5.2 日志级别](#52-日志级别)
- [6. 错误监控](#6-错误监控)
  - [6.1 错误指标](#61-错误指标)
  - [6.2 错误告警](#62-错误告警)
- [7. 形式化定义与理论基础](#7-形式化定义与理论基础)
  - [7.1 API 错误处理形式化模型](#71-api-错误处理形式化模型)
  - [7.2 错误分类形式化](#72-错误分类形式化)
  - [7.3 错误处理策略形式化](#73-错误处理策略形式化)
- [8. 相关文档](#8-相关文档)

---

## 1. 概述

API 错误处理规范定义了 API 在错误处理场景下的设计和实现，从错误分类到错误响应格
式，从错误处理策略到错误监控。本文档基于形式化方法，提供严格的数学定义和推理论证
，分析 API 错误处理的理论基础和实践方法。

### 1.1 错误处理架构

```text
API 调用（API Call）
  ↓
错误检测（Error Detection）
  ↓
错误分类（Error Classification）
  ↓
错误响应（Error Response）
  ↓
错误处理（Error Handling）
```

### 1.2 API 错误处理在 API 规范中的位置

API 错误处理在 API 规范四元组 `⟨IDL, Governance, Observability, Security⟩` 中主
要涉及 **IDL** 和 **Observability** 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
            ↑                        ↑
    API 错误处理涉及 IDL 和 Observability
```

API 错误处理在 API 规范中提供：

- **错误分类**：HTTP 状态码、业务错误码、错误严重性
- **错误响应**：标准错误格式、错误详情、错误追踪
- **错误策略**：重试、降级、恢复
- **错误监控**：错误指标、错误告警

**参考标准**：

- [HTTP Status Codes](https://httpwg.org/specs/rfc7231.html#status.codes) - HTTP
  状态码规范
- [Problem Details for HTTP APIs](https://tools.ietf.org/html/rfc7807) - RFC
  7807 错误格式
- [Error Handling Best Practices](https://www.restapitutorial.com/httpstatuscodes.html) -
  错误处理最佳实践
- [Structured Error Responses](https://jsonapi.org/format/#errors) - JSON API 错
  误格式
- [Error Tracking](https://sentry.io/) - Sentry 错误追踪

---

## 2. 错误分类

### 2.1 HTTP 状态码

**HTTP 状态码规范**：

```yaml
apiVersion: api.example.com/v1
kind: ErrorCodePolicy
metadata:
  name: http-status-codes
spec:
  codes:
    - code: 400
      name: BAD_REQUEST
      description: Invalid request
      useCase: "Malformed request body"
    - code: 401
      name: UNAUTHORIZED
      description: Authentication required
      useCase: "Missing or invalid token"
    - code: 403
      name: FORBIDDEN
      description: Access denied
      useCase: "Insufficient permissions"
    - code: 404
      name: NOT_FOUND
      description: Resource not found
      useCase: "Resource does not exist"
    - code: 429
      name: TOO_MANY_REQUESTS
      description: Rate limit exceeded
      useCase: "Too many requests"
    - code: 500
      name: INTERNAL_SERVER_ERROR
      description: Server error
      useCase: "Unexpected server error"
    - code: 503
      name: SERVICE_UNAVAILABLE
      description: Service unavailable
      useCase: "Service temporarily unavailable"
```

### 2.2 业务错误码

**业务错误码定义**：

```yaml
apiVersion: api.example.com/v1
kind: BusinessErrorCode
metadata:
  name: payment-error-codes
spec:
  codes:
    - code: PAYMENT_INSUFFICIENT_FUNDS
      httpStatus: 400
      message: "Insufficient funds"
      description: "Account balance is insufficient"
    - code: PAYMENT_INVALID_CARD
      httpStatus: 400
      message: "Invalid card number"
      description: "Card number is invalid or expired"
    - code: PAYMENT_DUPLICATE_TRANSACTION
      httpStatus: 409
      message: "Duplicate transaction"
      description: "Transaction already exists"
    - code: PAYMENT_GATEWAY_ERROR
      httpStatus: 502
      message: "Payment gateway error"
      description: "External payment gateway error"
```

### 2.3 错误严重性

**错误严重性分类**：

```yaml
apiVersion: api.example.com/v1
kind: ErrorSeverity
metadata:
  name: error-severity-levels
spec:
  levels:
    - level: CRITICAL
      description: "System failure"
      action: "Immediate attention required"
      examples:
        - "Database connection failure"
        - "Service crash"
    - level: ERROR
      description: "Operation failure"
      action: "Investigation required"
      examples:
        - "Payment processing failure"
        - "Data validation error"
    - level: WARNING
      description: "Potential issue"
      action: "Monitor and review"
      examples:
        - "Rate limit approaching"
        - "Deprecated API usage"
    - level: INFO
      description: "Informational"
      action: "Log for reference"
      examples:
        - "Request processed successfully"
        - "Cache miss"
```

---

## 3. 错误响应格式

### 3.1 标准错误格式

**标准错误响应**：

```json
{
  "error": {
    "code": "PAYMENT_INSUFFICIENT_FUNDS",
    "message": "Insufficient funds",
    "type": "business_error",
    "status": 400,
    "request_id": "req_1234567890",
    "timestamp": "2025-11-07T10:00:00Z",
    "details": {
      "account_id": "acc_123",
      "required_amount": 10000,
      "available_balance": 5000
    },
    "links": {
      "documentation": "https://api.example.com/docs/errors/PAYMENT_INSUFFICIENT_FUNDS",
      "support": "https://support.example.com/contact"
    }
  }
}
```

### 3.2 错误详情

**详细错误响应**：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "status": 400,
    "errors": [
      {
        "field": "amount",
        "code": "INVALID_VALUE",
        "message": "Amount must be between 1 and 10000",
        "value": 0
      },
      {
        "field": "currency",
        "code": "INVALID_ENUM",
        "message": "Currency must be one of: USD, EUR, CNY",
        "value": "JPY"
      }
    ]
  }
}
```

### 3.3 错误追踪

**错误追踪信息**：

```json
{
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred",
    "status": 500,
    "request_id": "req_1234567890",
    "trace_id": "trace_abcdef123456",
    "span_id": "span_7890123456",
    "timestamp": "2025-11-07T10:00:00Z",
    "stack_trace": "..." // 仅在开发环境
  }
}
```

---

## 4. 错误处理策略

### 4.1 错误重试

**重试策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: RetryPolicy
metadata:
  name: payment-retry-policy
spec:
  maxRetries: 3
  backoffStrategy: exponential
  initialDelay: "1s"
  maxDelay: "10s"
  retryableErrors:
    - code: PAYMENT_GATEWAY_ERROR
      httpStatus: 502
    - code: SERVICE_UNAVAILABLE
      httpStatus: 503
  nonRetryableErrors:
    - code: PAYMENT_INSUFFICIENT_FUNDS
      httpStatus: 400
    - code: PAYMENT_INVALID_CARD
      httpStatus: 400
```

### 4.2 错误降级

**降级策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: FallbackPolicy
metadata:
  name: payment-fallback-policy
spec:
  strategies:
    - error: PAYMENT_GATEWAY_ERROR
      fallback: "Use cached payment method"
    - error: SERVICE_UNAVAILABLE
      fallback: "Return cached response"
    - error: TIMEOUT
      fallback: "Return default response"
```

### 4.3 错误恢复

**错误恢复实现**：

```go
package main

import (
    "context"
    "time"
)

type ErrorRecovery struct {
    maxRetries int
    backoff    time.Duration
}

func (er *ErrorRecovery) Recover(ctx context.Context, fn func() error) error {
    var lastErr error

    for i := 0; i < er.maxRetries; i++ {
        if err := fn(); err == nil {
            return nil
        } else {
            lastErr = err
            if !isRetryable(err) {
                return err
            }
        }

        if i < er.maxRetries-1 {
            select {
            case <-ctx.Done():
                return ctx.Err()
            case <-time.After(er.backoff * time.Duration(1<<uint(i))):
            }
        }
    }

    return lastErr
}

func isRetryable(err error) bool {
    // 判断错误是否可重试
    return true
}
```

---

## 5. 错误日志

### 5.1 日志格式

**结构化错误日志**：

```json
{
  "timestamp": "2025-11-07T10:00:00Z",
  "level": "ERROR",
  "service": "payment-service",
  "error": {
    "code": "PAYMENT_PROCESSING_FAILED",
    "message": "Payment processing failed",
    "type": "business_error",
    "status": 500
  },
  "request": {
    "id": "req_1234567890",
    "method": "POST",
    "path": "/api/v1/payments",
    "user_id": "user_123"
  },
  "context": {
    "payment_id": "pay_456",
    "order_id": "order_789",
    "amount": 10000
  },
  "stack_trace": "..."
}
```

### 5.2 日志级别

**日志级别配置**：

```yaml
apiVersion: api.example.com/v1
kind: LogLevelPolicy
metadata:
  name: error-log-levels
spec:
  levels:
    - level: ERROR
      useCase: "Operation failures"
      examples:
        - "Payment processing failed"
        - "Database query failed"
    - level: WARN
      useCase: "Potential issues"
      examples:
        - "Rate limit approaching"
        - "Deprecated API usage"
    - level: INFO
      useCase: "Informational events"
      examples:
        - "Request processed"
        - "Cache hit"
    - level: DEBUG
      useCase: "Debug information"
      examples:
        - "Request details"
        - "Response details"
```

---

## 6. 错误监控

### 6.1 错误指标

**错误指标定义**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: api-error-metrics
spec:
  groups:
    - name: api_errors
      rules:
        - record: api:error_rate
          expr: |
            rate(api_requests_total{status=~"5.."}[5m]) /
            rate(api_requests_total[5m])
        - record: api:error_count_by_code
          expr: |
            sum by (code) (rate(api_errors_total[5m]))
```

### 6.2 错误告警

**错误告警规则**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: api-error-alerts
spec:
  groups:
    - name: api_error_alerts
      rules:
        - alert: HighErrorRate
          expr: |
            rate(api_requests_total{status=~"5.."}[5m]) /
            rate(api_requests_total[5m]) > 0.05
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "High error rate detected"
            description: "Error rate is {{ $value | humanizePercentage }}"
```

---

## 7. 形式化定义与理论基础

### 7.1 API 错误处理形式化模型

**定义 7.1（API 错误处理）**：API 错误处理是一个四元组：

```text
API_Error_Handling = ⟨Error_Classification, Error_Response, Error_Strategy, Error_Monitoring⟩
```

其中：

- **Error_Classification**：错误分类
  `Error_Classification: Error → {Client_Error, Server_Error}`
- **Error_Response**：错误响应 `Error_Response: Error → HTTP_Response`
- **Error_Strategy**：错误策略
  `Error_Strategy: Error → {Retry, Degrade, Recover}`
- **Error_Monitoring**：错误监控 `Error_Monitoring: Error → Metrics`

**定义 7.2（错误率）**：错误率是一个函数：

```text
Error_Rate(API) = |Errors| / |Total_Requests|
```

**定理 7.1（错误处理有效性）**：如果错误处理正确，则错误率降低：

```text
Error_Handling(API) ⟹ Error_Rate(API) ↓
```

**证明**：如果错误处理正确，则错误可以被正确分类和处理，减少错误传播，因此错误率
降低。□

### 7.2 错误分类形式化

**定义 7.3（错误严重性）**：错误严重性是一个函数：

```text
Error_Severity: Error → {Critical, High, Medium, Low}
```

**定义 7.4（错误类型）**：错误类型是一个函数：

```text
Error_Type: Error → {Validation, Business, System, Network}
```

**定理 7.2（错误分类与处理）**：错误严重性越高，处理优先级越高：

```text
Severity(E₁) > Severity(E₂) ⟹ Priority(E₁) > Priority(E₂)
```

**证明**：错误严重性越高，对系统影响越大，因此处理优先级越高。□

### 7.3 错误处理策略形式化

**定义 7.5（错误重试）**：错误重试是一个函数：

```text
Retry_Error: Error × Retry_Policy → Result
```

**定义 7.6（错误降级）**：错误降级是一个函数：

```text
Degrade_Error: Error → Fallback_Response
```

**定理 7.3（错误处理策略有效性）**：错误处理策略提高系统可用性：

```text
Error_Strategy(API) ⟹ Availability(API) ↑
```

**证明**：错误处理策略（重试、降级）可以处理错误，保持系统可用，因此可用性提高
。□

---

## 8. 相关文档

- **[API 标准化规范](../25-api-standardization/api-standardization.md)** - 错误
  处理标准
- **[API 数据验证规范](../46-api-data-validation/api-data-validation.md)** - 验
  证错误处理
- **[API 监控告警](../20-api-monitoring/api-monitoring.md)** - 错误监控
- **[最佳实践](../00-foundation/05-best-practices.md)** - 错误处理最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
