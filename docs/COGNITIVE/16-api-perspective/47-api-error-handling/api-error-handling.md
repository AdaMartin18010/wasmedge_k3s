# API 错误处理规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 错误处理架构](#11-错误处理架构)
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
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 错误处理规范定义了 API 在错误处理场景下的设计和实现，从错误分类到错误响应格
式，从错误处理策略到错误监控。

### 1.1 错误处理架构

```text
API 请求（API Request）
  ↓
错误检测（Error Detection）
  ↓
错误分类（Error Classification）
  ↓
错误响应（Error Response）
```

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

## 7. 相关文档

- **[API 标准化规范](../25-api-standardization/api-standardization.md)** - 错误
  处理标准
- **[API 数据验证规范](../46-api-data-validation/api-data-validation.md)** - 验
  证错误处理
- **[API 监控告警](../20-api-monitoring/api-monitoring.md)** - 错误监控
- **[最佳实践](../08-best-practices/best-practices.md)** - 错误处理最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
