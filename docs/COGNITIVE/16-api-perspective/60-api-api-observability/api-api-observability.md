# API 可观测性规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 可观测性架构](#11-可观测性架构)
- [2. 三大支柱](#2-三大支柱)
  - [2.1 日志（Logs）](#21-日志logs)
  - [2.2 指标（Metrics）](#22-指标metrics)
  - [2.3 追踪（Traces）](#23-追踪traces)
- [3. 统一可观测性](#3-统一可观测性)
  - [3.1 OTLP 协议](#31-otlp-协议)
  - [3.2 OpenTelemetry](#32-opentelemetry)
- [4. 可观测性工具](#4-可观测性工具)
  - [4.1 Prometheus](#41-prometheus)
  - [4.2 Grafana](#42-grafana)
  - [4.3 Jaeger](#43-jaeger)
- [5. 可观测性实践](#5-可观测性实践)
  - [5.1 分布式追踪](#51-分布式追踪)
  - [5.2 服务依赖图](#52-服务依赖图)
- [6. 可观测性优化](#6-可观测性优化)
  - [6.1 采样策略](#61-采样策略)
  - [6.2 数据保留](#62-数据保留)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 可观测性规范定义了 API 在可观测性场景下的设计和实现，从三大支柱到统一可观测
性，从可观测性工具到可观测性实践。

### 1.1 可观测性架构

```text
API 服务（API Service）
  ↓
可观测性数据采集（Observability Collection）
  ↓
可观测性数据存储（Observability Storage）
  ↓
可观测性数据查询（Observability Query）
```

---

## 2. 三大支柱

### 2.1 日志（Logs）

**结构化日志**：

```json
{
  "timestamp": "2025-11-07T10:00:00.123Z",
  "level": "INFO",
  "service": "payment-service",
  "request_id": "req_1234567890",
  "trace_id": "trace_abcdef123456",
  "span_id": "span_7890123456",
  "message": "Payment created",
  "context": {
    "payment_id": "pay_456",
    "order_id": "order_789",
    "amount": 10000
  }
}
```

### 2.2 指标（Metrics）

**Prometheus 指标**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: payment-service-metrics
spec:
  selector:
    matchLabels:
      app: payment-service
  endpoints:
    - port: metrics
      path: /metrics
      interval: 30s
```

### 2.3 追踪（Traces）

**OpenTelemetry 追踪**：

```go
package main

import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/trace"
)

func HandlePayment(ctx context.Context, payment *Payment) error {
    tracer := otel.Tracer("payment-service")
    ctx, span := tracer.Start(ctx, "payment.process")
    defer span.End()

    span.SetAttributes(
        attribute.String("payment.id", payment.ID),
        attribute.Int64("payment.amount", payment.Amount),
    )

    return processPayment(ctx, payment)
}
```

---

## 3. 统一可观测性

### 3.1 OTLP 协议

**OTLP 配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: otlp-config
data:
  otlp.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318

    exporters:
      otlp:
        endpoint: otel-collector:4317

    service:
      pipelines:
        traces:
          receivers: [otlp]
          exporters: [otlp]
        metrics:
          receivers: [otlp]
          exporters: [otlp]
        logs:
          receivers: [otlp]
          exporters: [otlp]
```

### 3.2 OpenTelemetry

**OpenTelemetry SDK 配置**：

```go
package main

import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/trace"
)

func setupOpenTelemetry() (*trace.TracerProvider, error) {
    exporter, err := otlptracegrpc.New(
        context.Background(),
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
    )
    if err != nil {
        return nil, err
    }

    tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
        trace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("payment-service"),
        )),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}
```

---

## 4. 可观测性工具

### 4.1 Prometheus

**Prometheus 配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s

    scrape_configs:
      - job_name: 'payment-service'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_label_app]
            action: keep
            regex: payment-service
```

### 4.2 Grafana

**Grafana 仪表板**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "Payment API Dashboard",
        "panels": [
          {
            "title": "Request Rate",
            "targets": [
              {
                "expr": "rate(http_requests_total[5m])"
              }
            ]
          }
        ]
      }
    }
```

### 4.3 Jaeger

**Jaeger 配置**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
spec:
  template:
    spec:
      containers:
        - name: jaeger
          image: jaegertracing/all-in-one:latest
          env:
            - name: COLLECTOR_ZIPKIN_HTTP_PORT
              value: "9411"
```

---

## 5. 可观测性实践

### 5.1 分布式追踪

**分布式追踪实现**：

```go
package main

import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/propagation"
)

func PropagateTraceContext(ctx context.Context, req *http.Request) {
    propagator := otel.GetTextMapPropagator()
    propagator.Inject(ctx, propagation.HeaderCarrier(req.Header))
}

func ExtractTraceContext(ctx context.Context, req *http.Request) context.Context {
    propagator := otel.GetTextMapPropagator()
    return propagator.Extract(ctx, propagation.HeaderCarrier(req.Header))
}
```

### 5.2 服务依赖图

**服务依赖图生成**：

```yaml
apiVersion: api.example.com/v1
kind: ServiceDependencyGraph
metadata:
  name: payment-service-dependencies
spec:
  service: payment-service
  dependencies:
    - service: order-service
      type: http
      calls:
        - endpoint: "/api/v1/orders/{id}"
          method: GET
    - service: payment-gateway
      type: http
      calls:
        - endpoint: "/api/v1/process"
          method: POST
```

---

## 6. 可观测性优化

### 6.1 采样策略

**采样策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: ObservabilitySampling
metadata:
  name: payment-api-sampling
spec:
  traces:
    strategy: probabilistic
    rate: 0.1
    rules:
      - condition: "error == true"
        rate: 1.0
      - condition: "latency > 1s"
        rate: 0.5
  logs:
    strategy: rate_limit
    rate: 1000
```

### 6.2 数据保留

**数据保留策略**：

```yaml
apiVersion: api.example.com/v1
kind: ObservabilityRetention
metadata:
  name: payment-api-retention
spec:
  logs:
    retention: "30d"
    compression: true
  metrics:
    retention: "90d"
    downsampling: true
  traces:
    retention: "7d"
    sampling: true
```

---

## 7. 相关文档

- **[API 可观测性规范](../12-api-observability/api-observability.md)** - API 可
  观测性
- **[API 日志规范](../48-api-logging/api-logging.md)** - 日志管理
- **[API 指标规范](../49-api-metrics/api-metrics.md)** - 指标管理
- **[API 追踪规范](../50-api-tracing/api-tracing.md)** - 追踪管理
- **[最佳实践](../08-best-practices/best-practices.md)** - 可观测性最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
