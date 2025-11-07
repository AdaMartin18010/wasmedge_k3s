# API 弃用策略规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 弃用策略架构](#11-弃用策略架构)
- [2. 弃用决策](#2-弃用决策)
  - [2.1 弃用原因](#21-弃用原因)
  - [2.2 弃用评估](#22-弃用评估)
- [3. 弃用通知](#3-弃用通知)
  - [3.1 弃用声明](#31-弃用声明)
  - [3.2 弃用时间表](#32-弃用时间表)
- [4. 弃用迁移](#4-弃用迁移)
  - [4.1 迁移指南](#41-迁移指南)
  - [4.2 迁移工具](#42-迁移工具)
- [5. 弃用执行](#5-弃用执行)
  - [5.1 弃用阶段](#51-弃用阶段)
  - [5.2 弃用监控](#52-弃用监控)
- [6. 弃用回滚](#6-弃用回滚)
  - [6.1 回滚策略](#61-回滚策略)
  - [6.2 回滚流程](#62-回滚流程)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 弃用策略规范定义了 API 在弃用场景下的设计和实现，从弃用决策到弃用通知，从弃
用迁移到弃用执行。

### 1.1 弃用策略架构

```text
弃用决策（Deprecation Decision）
  ↓
弃用通知（Deprecation Notice）
  ↓
弃用迁移（Deprecation Migration）
  ↓
弃用执行（Deprecation Execution）
```

---

## 2. 弃用决策

### 2.1 弃用原因

**弃用原因分类**：

```yaml
apiVersion: api.example.com/v1
kind: DeprecationReason
metadata:
  name: deprecation-reasons
spec:
  reasons:
    - type: security
      description: "Security vulnerability"
      examples:
        - "Weak encryption"
        - "Authentication flaw"
    - type: performance
      description: "Performance issues"
      examples:
        - "High latency"
        - "Resource intensive"
    - type: compatibility
      description: "Compatibility issues"
      examples:
        - "Breaking changes"
        - "Version mismatch"
    - type: maintenance
      description: "Maintenance burden"
      examples:
        - "Legacy code"
        - "Outdated dependencies"
```

### 2.2 弃用评估

**弃用评估标准**：

```yaml
apiVersion: api.example.com/v1
kind: DeprecationAssessment
metadata:
  name: payment-api-deprecation-assessment
spec:
  api: payment-api-v1
  assessment:
    usage:
      activeUsers: 1000
      requestRate: "1000/min"
      criticalUsers: ["user_123", "user_456"]
    impact:
      severity: HIGH
      affectedServices: ["order-service", "invoice-service"]
    alternatives:
      - api: payment-api-v2
        migrationEffort: MEDIUM
        compatibility: HIGH
  recommendation: DEPRECATE
```

---

## 3. 弃用通知

### 3.1 弃用声明

**弃用声明格式**：

```yaml
apiVersion: api.example.com/v1
kind: DeprecationNotice
metadata:
  name: payment-api-v1-deprecation
spec:
  api: payment-api-v1
  deprecationDate: "2025-11-07"
  sunsetDate: "2026-11-07"
  reason: "Replaced by payment-api-v2 with improved performance"
  alternatives:
    - api: payment-api-v2
      documentation: "https://api.example.com/docs/v2"
  migrationGuide: "https://api.example.com/migration/v1-to-v2"
```

**HTTP 弃用头**：

```go
func AddDeprecationHeader(w http.ResponseWriter, deprecationDate, sunsetDate string) {
    w.Header().Set("Deprecation", "true")
    w.Header().Set("Deprecation-Date", deprecationDate)
    w.Header().Set("Sunset", sunsetDate)
    w.Header().Set("Link", "<https://api.example.com/docs/v2>; rel=\"successor-version\"")
}
```

### 3.2 弃用时间表

**弃用时间表**：

```yaml
apiVersion: api.example.com/v1
kind: DeprecationTimeline
metadata:
  name: payment-api-deprecation-timeline
spec:
  phases:
    - phase: announcement
      date: "2025-11-07"
      duration: "30d"
      actions:
        - "Send deprecation notice"
        - "Update documentation"
        - "Notify users"
    - phase: warning
      date: "2025-12-07"
      duration: "180d"
      actions:
        - "Add deprecation headers"
        - "Log deprecation warnings"
        - "Monitor usage"
    - phase: sunset
      date: "2026-06-07"
      duration: "30d"
      actions:
        - "Disable new requests"
        - "Return 410 Gone"
        - "Archive API"
```

---

## 4. 弃用迁移

### 4.1 迁移指南

**迁移指南配置**：

```yaml
apiVersion: api.example.com/v1
kind: MigrationGuide
metadata:
  name: payment-api-v1-to-v2-migration
spec:
  from: payment-api-v1
  to: payment-api-v2
  steps:
    - step: 1
      title: "Update API endpoint"
      description: "Change endpoint from /api/v1/payments to /api/v2/payments"
      code:
        before: "POST /api/v1/payments"
        after: "POST /api/v2/payments"
    - step: 2
      title: "Update request format"
      description: "Update request body format"
      code:
        before: |
          {
            "order_id": "order_123",
            "amount": 10000
          }
        after: |
          {
            "orderId": "order_123",
            "amount": 10000,
            "currency": "USD"
          }
    - step: 3
      title: "Update response handling"
      description: "Update response parsing"
      code:
        before: "response.payment_id"
        after: "response.paymentId"
```

### 4.2 迁移工具

**迁移工具配置**：

```yaml
apiVersion: api.example.com/v1
kind: MigrationTool
metadata:
  name: api-migration-tool
spec:
  type: automated
  features:
    - endpoint_mapping
    - request_transformation
    - response_transformation
    - validation
  config:
    mappings:
      - from: "/api/v1/payments"
        to: "/api/v2/payments"
      - from: "order_id"
        to: "orderId"
```

---

## 5. 弃用执行

### 5.1 弃用阶段

**弃用阶段配置**：

```yaml
apiVersion: api.example.com/v1
kind: DeprecationPhase
metadata:
  name: payment-api-deprecation-phases
spec:
  phases:
    - name: soft_deprecation
      date: "2025-11-07"
      actions:
        - "Add deprecation headers"
        - "Log deprecation warnings"
        - "Continue serving requests"
    - name: hard_deprecation
      date: "2026-05-07"
      actions:
        - "Return 410 Gone for new requests"
        - "Allow existing requests"
        - "Monitor usage"
    - name: sunset
      date: "2026-06-07"
      actions:
        - "Disable all requests"
        - "Return 410 Gone"
        - "Archive API"
```

### 5.2 弃用监控

**弃用监控配置**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: deprecation-monitoring
spec:
  groups:
    - name: deprecation_alerts
      rules:
        - alert: HighDeprecatedAPIUsage
          expr: |
            rate(http_requests_total{api_version="v1"}[5m]) > 100
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High usage of deprecated API"
            description: "{{ $value }} requests/min to deprecated API"
```

---

## 6. 弃用回滚

### 6.1 回滚策略

**回滚策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: DeprecationRollback
metadata:
  name: payment-api-rollback-strategy
spec:
  conditions:
    - type: critical_issue
      description: "Critical issue in new API"
      action: ROLLBACK
    - type: migration_failure
      description: "Migration failure"
      action: ROLLBACK
  rollbackPlan:
    - step: "Disable new API"
    - step: "Re-enable deprecated API"
    - step: "Notify users"
    - step: "Investigate issue"
```

### 6.2 回滚流程

**回滚流程实现**：

```go
package main

func RollbackDeprecation(ctx context.Context, api string) error {
    // 1. 禁用新 API
    if err := disableAPI(ctx, getNewAPI(api)); err != nil {
        return err
    }

    // 2. 重新启用弃用的 API
    if err := enableAPI(ctx, api); err != nil {
        return err
    }

    // 3. 通知用户
    if err := notifyUsers(ctx, api, "Rollback executed"); err != nil {
        return err
    }

    // 4. 记录回滚事件
    return logRollbackEvent(ctx, api)
}
```

---

## 7. 相关文档

- **[API 版本管理](../23-api-versioning/api-versioning.md)** - API 版本控制
- **[API 生命周期](../24-api-lifecycle/api-lifecycle.md)** - API 生命周期管理
- **[API 迁移指南](../19-api-migration/api-migration.md)** - API 迁移
- **[最佳实践](../08-best-practices/best-practices.md)** - 弃用最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
