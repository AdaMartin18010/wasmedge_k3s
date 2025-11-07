# API 计费规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 计费架构](#11-计费架构)
- [2. 计费模型](#2-计费模型)
  - [2.1 按请求计费](#21-按请求计费)
  - [2.2 按使用量计费](#22-按使用量计费)
  - [2.3 订阅计费](#23-订阅计费)
- [3. 计费指标](#3-计费指标)
  - [3.1 API 调用次数](#31-api-调用次数)
  - [3.2 数据传输量](#32-数据传输量)
  - [3.3 计算资源](#33-计算资源)
- [4. 计费策略](#4-计费策略)
  - [4.1 免费额度](#41-免费额度)
  - [4.2 分层定价](#42-分层定价)
  - [4.3 动态定价](#43-动态定价)
- [5. 计费记录](#5-计费记录)
  - [5.1 使用记录](#51-使用记录)
  - [5.2 账单生成](#52-账单生成)
- [6. 计费监控](#6-计费监控)
  - [6.1 使用量监控](#61-使用量监控)
  - [6.2 成本分析](#62-成本分析)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 计费规范定义了 API 在计费场景下的设计和实现，从计费模型到计费指标，从计费策
略到计费记录。

### 1.1 计费架构

```text
API 调用（API Call）
  ↓
使用量记录（Usage Recording）
  ↓
计费计算（Billing Calculation）
  ↓
账单生成（Invoice Generation）
```

---

## 2. 计费模型

### 2.1 按请求计费

**按请求计费配置**：

```yaml
apiVersion: api.example.com/v1
kind: BillingModel
metadata:
  name: payment-api-billing
spec:
  model: "per_request"
  pricing:
    - tier: "free"
      price: 0
      limit: 1000
    - tier: "basic"
      price: 0.001
      unit: "USD"
      per: "request"
    - tier: "premium"
      price: 0.0005
      unit: "USD"
      per: "request"
      volumeDiscount: true
```

**按请求计费实现**：

```go
package main

import (
    "time"
)

type BillingRecord struct {
    UserID      string
    APIEndpoint string
    RequestID   string
    Timestamp   time.Time
    Cost        float64
}

func RecordAPIRequest(userID, endpoint, requestID string) error {
    cost := calculateRequestCost(endpoint)

    record := BillingRecord{
        UserID:      userID,
        APIEndpoint: endpoint,
        RequestID:   requestID,
        Timestamp:   time.Now(),
        Cost:        cost,
    }

    return saveBillingRecord(record)
}

func calculateRequestCost(endpoint string) float64 {
    // 根据端点和用户套餐计算费用
    return 0.001
}
```

### 2.2 按使用量计费

**按使用量计费配置**：

```yaml
apiVersion: api.example.com/v1
kind: BillingModel
metadata:
  name: storage-api-billing
spec:
  model: "usage_based"
  pricing:
    - resource: "storage"
      price: 0.023
      unit: "USD"
      per: "GB"
      period: "month"
    - resource: "bandwidth"
      price: 0.09
      unit: "USD"
      per: "GB"
      period: "month"
```

### 2.3 订阅计费

**订阅计费配置**：

```yaml
apiVersion: api.example.com/v1
kind: SubscriptionBilling
metadata:
  name: payment-api-subscription
spec:
  plans:
    - name: "basic"
      price: 29
      unit: "USD"
      period: "month"
      features:
        - api_calls: 10000
        - support: "email"
    - name: "premium"
      price: 99
      unit: "USD"
      period: "month"
      features:
        - api_calls: 100000
        - support: "24/7"
        - sla: "99.9%"
```

---

## 3. 计费指标

### 3.1 API 调用次数

**API 调用次数记录**：

```go
package main

import (
    "sync/atomic"
    "time"
)

type APICallCounter struct {
    count int64
    resetTime time.Time
}

func (c *APICallCounter) Increment() {
    atomic.AddInt64(&c.count, 1)
}

func (c *APICallCounter) GetCount() int64 {
    return atomic.LoadInt64(&c.count)
}

func (c *APICallCounter) Reset() {
    atomic.StoreInt64(&c.count, 0)
    c.resetTime = time.Now()
}
```

### 3.2 数据传输量

**数据传输量记录**：

```go
package main

import (
    "sync/atomic"
)

type DataTransferTracker struct {
    bytesIn  int64
    bytesOut int64
}

func (t *DataTransferTracker) RecordInbound(bytes int64) {
    atomic.AddInt64(&t.bytesIn, bytes)
}

func (t *DataTransferTracker) RecordOutbound(bytes int64) {
    atomic.AddInt64(&t.bytesOut, bytes)
}

func (t *DataTransferTracker) GetTotalBytes() int64 {
    return atomic.LoadInt64(&t.bytesIn) + atomic.LoadInt64(&t.bytesOut)
}
```

### 3.3 计算资源

**计算资源记录**：

```yaml
apiVersion: api.example.com/v1
kind: ComputeResourceBilling
metadata:
  name: payment-api-compute-billing
spec:
  resources:
    - resource: "cpu"
      price: 0.01
      unit: "USD"
      per: "cpu_hour"
    - resource: "memory"
      price: 0.005
      unit: "USD"
      per: "GB_hour"
    - resource: "storage"
      price: 0.0001
      unit: "USD"
      per: "GB_hour"
```

---

## 4. 计费策略

### 4.1 免费额度

**免费额度配置**：

```yaml
apiVersion: api.example.com/v1
kind: FreeTier
metadata:
  name: payment-api-free-tier
spec:
  limits:
    - resource: "api_calls"
      amount: 1000
      period: "month"
    - resource: "storage"
      amount: 5
      unit: "GB"
      period: "month"
    - resource: "bandwidth"
      amount: 10
      unit: "GB"
      period: "month"
```

### 4.2 分层定价

**分层定价配置**：

```yaml
apiVersion: api.example.com/v1
kind: TieredPricing
metadata:
  name: payment-api-tiered-pricing
spec:
  tiers:
    - tier: 1
      range: "0-1000"
      price: 0.001
      unit: "USD"
      per: "request"
    - tier: 2
      range: "1001-10000"
      price: 0.0008
      unit: "USD"
      per: "request"
    - tier: 3
      range: "10001+"
      price: 0.0005
      unit: "USD"
      per: "request"
```

### 4.3 动态定价

**动态定价实现**：

```go
package main

import (
    "time"
)

func CalculateDynamicPrice(basePrice float64, demand float64, timeOfDay time.Time) float64 {
    // 基于需求和时间调整价格
    multiplier := 1.0

    // 需求调整
    if demand > 0.8 {
        multiplier *= 1.2
    } else if demand < 0.3 {
        multiplier *= 0.8
    }

    // 时间调整
    hour := timeOfDay.Hour()
    if hour >= 9 && hour <= 17 {
        multiplier *= 1.1 // 工作时间溢价
    }

    return basePrice * multiplier
}
```

---

## 5. 计费记录

### 5.1 使用记录

**使用记录格式**：

```json
{
  "user_id": "user_123",
  "api_endpoint": "/api/v1/payments",
  "request_id": "req_456",
  "timestamp": "2025-11-07T10:00:00Z",
  "metrics": {
    "request_count": 1,
    "data_in": 1024,
    "data_out": 2048,
    "cpu_time": 0.05,
    "memory_usage": 128
  },
  "cost": {
    "request_cost": 0.001,
    "data_cost": 0.0001,
    "compute_cost": 0.0005,
    "total": 0.0016
  }
}
```

### 5.2 账单生成

**账单生成配置**：

```yaml
apiVersion: api.example.com/v1
kind: InvoiceGeneration
metadata:
  name: payment-api-invoice
spec:
  period: "monthly"
  billingDate: "1"
  currency: "USD"
  items:
    - name: "API Calls"
      unit: "request"
      quantity: "usage.api_calls"
      price: "tiered_pricing"
    - name: "Data Transfer"
      unit: "GB"
      quantity: "usage.data_transfer"
      price: 0.09
  discounts:
    - type: "volume"
      threshold: 10000
      discount: 0.1
```

---

## 6. 计费监控

### 6.1 使用量监控

**使用量监控指标**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: billing-usage-metrics
spec:
  groups:
    - name: billing_usage
      rules:
        - record: billing:api_calls_total
          expr: |
            sum(rate(http_requests_total[5m])) by (user_id)
        - record: billing:data_transfer_total
          expr: |
            sum(rate(http_request_bytes_total[5m])) by (user_id)
        - record: billing:cost_total
          expr: |
            sum(billing_cost_total) by (user_id)
```

### 6.2 成本分析

**成本分析报告**：

```yaml
apiVersion: api.example.com/v1
kind: CostAnalysis
metadata:
  name: payment-api-cost-analysis
spec:
  period: "2025-10-01T00:00:00Z/2025-10-31T23:59:59Z"
  dimensions:
    - dimension: "api_endpoint"
    - dimension: "user_tier"
    - dimension: "region"
  metrics:
    - metric: "total_cost"
    - metric: "cost_per_request"
    - metric: "cost_per_user"
  output:
    format: "csv"
    destination: "s3://billing-reports/cost-analysis-2025-10.csv"
```

---

## 7. 相关文档

- **[API SLA 规范](../66-api-sla/api-sla.md)** - SLA 与计费关联
- **[API 多租户规范](../64-api-multi-tenancy/api-multi-tenancy.md)** - 多租户计
  费
- **[API 成本优化](../21-api-cost-optimization/api-cost-optimization.md)** - 成
  本优化
- **[最佳实践](../08-best-practices/best-practices.md)** - 计费最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
