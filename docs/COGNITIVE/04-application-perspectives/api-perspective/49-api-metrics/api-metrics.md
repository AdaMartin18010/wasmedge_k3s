# API 指标规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 指标架构](#11-指标架构)
- [2. 指标类型](#2-指标类型)
  - [2.1 计数器（Counter）](#21-计数器counter)
  - [2.2 仪表盘（Gauge）](#22-仪表盘gauge)
  - [2.3 直方图（Histogram）](#23-直方图histogram)
  - [2.4 摘要（Summary）](#24-摘要summary)
- [3. RED 指标](#3-red-指标)
  - [3.1 速率（Rate）](#31-速率rate)
  - [3.2 错误（Errors）](#32-错误errors)
  - [3.3 持续时间（Duration）](#33-持续时间duration)
- [4. USE 指标](#4-use-指标)
  - [4.1 利用率（Utilization）](#41-利用率utilization)
  - [4.2 饱和度（Saturation）](#42-饱和度saturation)
  - [4.3 错误（Errors）](#43-错误errors)
- [5. 业务指标](#5-业务指标)
  - [5.1 业务指标定义](#51-业务指标定义)
  - [5.2 业务指标采集](#52-业务指标采集)
- [6. 指标导出](#6-指标导出)
  - [6.1 Prometheus 导出](#61-prometheus-导出)
  - [6.2 OTLP 导出](#62-otlp-导出)
- [7. 形式化定义与理论基础](#7-形式化定义与理论基础)
  - [7.1 API 指标形式化模型](#71-api-指标形式化模型)
  - [7.2 RED 指标形式化](#72-red-指标形式化)
  - [7.3 USE 指标形式化](#73-use-指标形式化)
- [8. 相关文档](#8-相关文档)

---

## 1. 概述

API 指标规范定义了 API 在指标监控场景下的设计和实现，从指标类型到 RED/USE 指标，
从业务指标到指标导出。本文档基于形式化方法，提供严格的数学定义和推理论证，分析
API 指标的理论基础和实践方法。

**参考标准**：

- [Prometheus Metrics](https://prometheus.io/docs/concepts/metric_types/) -
  Prometheus 指标类型
- [OpenMetrics](https://openmetrics.io/) - OpenMetrics 标准
- [RED Method](https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/) -
  RED 方法
- [USE Method](http://www.brendangregg.com/usemethod.html) - USE 方法
- [OTLP Metrics](https://opentelemetry.io/docs/specs/otel/metrics/) -
  OpenTelemetry 指标规范

### 1.1 指标架构

```text
API 请求（API Request）
  ↓
指标采集（Metrics Collection）
  ↓
指标存储（Metrics Storage）
  ↓
指标查询（Metrics Query）
```

---

## 2. 指标类型

### 2.1 计数器（Counter）

**计数器指标**：

```go
package main

import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    httpRequestsTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "path", "status"},
    )
)

func recordRequest(method, path string, status int) {
    httpRequestsTotal.WithLabelValues(method, path, strconv.Itoa(status)).Inc()
}
```

### 2.2 仪表盘（Gauge）

**仪表盘指标**：

```go
var (
    activeConnections = promauto.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "active_connections",
            Help: "Number of active connections",
        },
        []string{"service"},
    )

    memoryUsage = promauto.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "memory_usage_bytes",
            Help: "Memory usage in bytes",
        },
        []string{"service"},
    )
)

func updateActiveConnections(service string, count int) {
    activeConnections.WithLabelValues(service).Set(float64(count))
}
```

### 2.3 直方图（Histogram）

**直方图指标**：

```go
var (
    httpRequestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "path"},
    )
)

func recordRequestDuration(method, path string, duration time.Duration) {
    httpRequestDuration.WithLabelValues(method, path).Observe(duration.Seconds())
}
```

### 2.4 摘要（Summary）

**摘要指标**：

```go
var (
    paymentAmount = promauto.NewSummaryVec(
        prometheus.SummaryOpts{
            Name:       "payment_amount",
            Help:       "Payment amount summary",
            Objectives: map[float64]float64{0.5: 0.05, 0.9: 0.01, 0.99: 0.001},
        },
        []string{"currency"},
    )
)

func recordPaymentAmount(currency string, amount float64) {
    paymentAmount.WithLabelValues(currency).Observe(amount)
}
```

---

## 3. RED 指标

### 3.1 速率（Rate）

**请求速率指标**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: api-rate-metrics
spec:
  groups:
    - name: api_rate
      rules:
        - record: api:request_rate
          expr: |
            rate(http_requests_total[5m])
        - record: api:request_rate_by_method
          expr: |
            rate(http_requests_total[5m]) by (method)
```

### 3.2 错误（Errors）

**错误率指标**：

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
            rate(http_requests_total{status=~"5.."}[5m]) /
            rate(http_requests_total[5m])
        - record: api:error_count
          expr: |
            sum by (status) (rate(http_requests_total{status=~"5.."}[5m]))
```

### 3.3 持续时间（Duration）

**延迟指标**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: api-duration-metrics
spec:
  groups:
    - name: api_duration
      rules:
        - record: api:request_duration_p50
          expr: |
            histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))
        - record: api:request_duration_p95
          expr: |
            histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
        - record: api:request_duration_p99
          expr: |
            histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

---

## 4. USE 指标

### 4.1 利用率（Utilization）

**资源利用率指标**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: api-utilization-metrics
spec:
  groups:
    - name: api_utilization
      rules:
        - record: api:cpu_utilization
          expr: |
            rate(container_cpu_usage_seconds_total[5m]) /
            container_spec_cpu_quota * 100
        - record: api:memory_utilization
          expr: |
            container_memory_usage_bytes /
            container_spec_memory_limit_bytes * 100
```

### 4.2 饱和度（Saturation）

**资源饱和度指标**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: api-saturation-metrics
spec:
  groups:
    - name: api_saturation
      rules:
        - record: api:queue_length
          expr: |
            sum(queue_length) by (service)
        - record: api:thread_pool_active
          expr: |
            sum(thread_pool_active_threads) by (service)
```

### 4.3 错误（Errors）

**资源错误指标**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: api-resource-errors
spec:
  groups:
    - name: api_resource_errors
      rules:
        - record: api:disk_errors
          expr: |
            sum(rate(disk_io_errors_total[5m])) by (device)
        - record: api:network_errors
          expr: |
            sum(rate(network_errors_total[5m])) by (interface)
```

---

## 5. 业务指标

### 5.1 业务指标定义

**业务指标配置**：

```yaml
apiVersion: api.example.com/v1
kind: BusinessMetrics
metadata:
  name: payment-business-metrics
spec:
  metrics:
    - name: payment_created_total
      type: counter
      description: "Total number of payments created"
      labels:
        - currency
        - payment_method
    - name: payment_amount_total
      type: counter
      description: "Total payment amount"
      labels:
        - currency
    - name: payment_success_rate
      type: gauge
      description: "Payment success rate"
      labels:
        - payment_method
```

### 5.2 业务指标采集

**业务指标实现**：

```go
var (
    paymentCreatedTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "payment_created_total",
            Help: "Total number of payments created",
        },
        []string{"currency", "payment_method"},
    )

    paymentAmountTotal = promauto.NewCounterVec(
        prometheus.CounterOpts{
            Name: "payment_amount_total",
            Help: "Total payment amount",
        },
        []string{"currency"},
    )
)

func recordPaymentCreated(currency, paymentMethod string, amount float64) {
    paymentCreatedTotal.WithLabelValues(currency, paymentMethod).Inc()
    paymentAmountTotal.WithLabelValues(currency).Add(amount)
}
```

---

## 6. 指标导出

### 6.1 Prometheus 导出

**Prometheus 导出配置**：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: payment-service-metrics
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
spec:
  ports:
    - name: metrics
      port: 8080
      targetPort: 8080
```

**Prometheus ServiceMonitor**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: payment-service-monitor
spec:
  selector:
    matchLabels:
      app: payment-service
  endpoints:
    - port: metrics
      path: /metrics
      interval: 30s
```

### 6.2 OTLP 导出

**OTLP 指标导出**：

```go
package main

import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc"
    "go.opentelemetry.io/otel/sdk/metric"
)

func setupOTLPMetrics() (*metric.MeterProvider, error) {
    exporter, err := otlpmetricgrpc.New(
        context.Background(),
        otlpmetricgrpc.WithEndpoint("otel-collector:4317"),
    )
    if err != nil {
        return nil, err
    }

    mp := metric.NewMeterProvider(
        metric.WithReader(metric.NewPeriodicReader(exporter)),
    )

    otel.SetMeterProvider(mp)
    return mp, nil
}
```

---

## 7. 形式化定义与理论基础

### 7.1 API 指标形式化模型

**定义 7.1（API 指标）**：API 指标是一个四元组：

```text
API_Metrics = ⟨Metric_Types, RED_Metrics, USE_Metrics, Business_Metrics⟩
```

其中：

- **Metric_Types**：指标类型
  `Metric_Types: {Counter, Gauge, Histogram, Summary}`
- **RED_Metrics**：RED 指标 `RED_Metrics = ⟨Rate, Errors, Duration⟩`
- **USE_Metrics**：USE 指标 `USE_Metrics = ⟨Utilization, Saturation, Errors⟩`
- **Business_Metrics**：业务指标 `Business_Metrics: Business_Event → Metric`

**定义 7.2（指标采集）**：指标采集是一个函数：

```text
Collect_Metrics: API × Time → Metrics
```

**定理 7.1（指标完备性）**：如果 RED 和 USE 指标都采集，则监控完备：

```text
RED_Metrics(API) ∧ USE_Metrics(API) ⟹ Complete_Monitoring(API)
```

**证明**：RED 和 USE 指标覆盖了 API 的关键方面，因此监控完备。□

### 7.2 RED 指标形式化

**定义 7.3（RED 指标）**：RED 指标是一个三元组：

```text
RED_Metrics = ⟨Rate, Errors, Duration⟩
```

其中：

- **Rate**：速率 `Rate = |Requests| / Time`
- **Errors**：错误数 `Errors = |Error_Requests|`
- **Duration**：持续时间 `Duration = Response_Time`

**定理 7.2（RED 指标相关性）**：错误率与速率相关：

```text
Error_Rate = Errors / Rate
```

**证明**：错误率是错误数除以总请求数，而速率是请求数除以时间，因此错误率等于错误
数除以速率。□

### 7.3 USE 指标形式化

**定义 7.4（USE 指标）**：USE 指标是一个三元组：

```text
USE_Metrics = ⟨Utilization, Saturation, Errors⟩
```

其中：

- **Utilization**：利用率 `Utilization = Used_Resources / Total_Resources`
- **Saturation**：饱和度 `Saturation = Queue_Length`
- **Errors**：错误数 `Errors = |Errors|`

**定理 7.3（USE 指标预警）**：利用率和饱和度高时预警：

```text
Utilization > Threshold ∨ Saturation > Threshold ⟹ Alert(API)
```

**证明**：利用率和饱和度高时，系统接近容量上限，需要预警。□

---

## 8. 相关文档

- **[API 可观测性规范](../12-api-observability/api-observability.md)** - 指标可
  观测性
- **[API 监控告警](../20-api-monitoring/api-monitoring.md)** - 指标监控
- **[API 性能优化](../14-api-performance/api-performance.md)** - 性能指标
- **[最佳实践](../08-best-practices/best-practices.md)** - 指标最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
