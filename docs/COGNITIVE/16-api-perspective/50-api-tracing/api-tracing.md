# API 追踪规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 追踪架构](#11-追踪架构)
- [2. 追踪上下文](#2-追踪上下文)
  - [2.1 Trace ID](#21-trace-id)
  - [2.2 Span ID](#22-span-id)
  - [2.3 Baggage](#23-baggage)
- [3. Span 操作](#3-span-操作)
  - [3.1 Span 创建](#31-span-创建)
  - [3.2 Span 属性](#32-span-属性)
  - [3.3 Span 事件](#33-span-事件)
- [4. 分布式追踪](#4-分布式追踪)
  - [4.1 上下文传播](#41-上下文传播)
  - [4.2 跨服务追踪](#42-跨服务追踪)
- [5. 追踪采样](#5-追踪采样)
  - [5.1 采样策略](#51-采样策略)
  - [5.2 采样配置](#52-采样配置)
- [6. 追踪导出](#6-追踪导出)
  - [6.1 OTLP 导出](#61-otlp-导出)
  - [6.2 Jaeger 导出](#62-jaeger-导出)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 追踪规范定义了 API 在分布式追踪场景下的设计和实现，从追踪上下文到 Span 操作
，从分布式追踪到追踪导出。

### 1.1 追踪架构

```text
API 请求（API Request）
  ↓
追踪上下文（Trace Context）
  ↓
Span 创建（Span Creation）
  ↓
追踪导出（Trace Export）
```

---

## 2. 追踪上下文

### 2.1 Trace ID

**Trace ID 生成**：

```go
package main

import (
    "crypto/rand"
    "encoding/hex"
)

func GenerateTraceID() string {
    bytes := make([]byte, 16)
    rand.Read(bytes)
    return hex.EncodeToString(bytes)
}
```

**Trace ID 传播**：

```go
package main

import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/trace"
    "go.opentelemetry.io/otel/propagation"
)

func ExtractTraceContext(r *http.Request) context.Context {
    propagator := otel.GetTextMapPropagator()
    return propagator.Extract(r.Context(), propagation.HeaderCarrier(r.Header))
}

func InjectTraceContext(ctx context.Context, w http.ResponseWriter) {
    propagator := otel.GetTextMapPropagator()
    propagator.Inject(ctx, propagation.HeaderCarrier(w.Header()))
}
```

### 2.2 Span ID

**Span ID 生成**：

```go
package main

import (
    "go.opentelemetry.io/otel/trace"
)

func CreateSpan(ctx context.Context, name string) (context.Context, trace.Span) {
    tracer := otel.Tracer("payment-service")
    return tracer.Start(ctx, name)
}
```

### 2.3 Baggage

**Baggage 使用**：

```go
package main

import (
    "go.opentelemetry.io/otel/baggage"
)

func SetBaggage(ctx context.Context, key, value string) (context.Context, error) {
    member, err := baggage.NewMember(key, value)
    if err != nil {
        return ctx, err
    }

    bag := baggage.FromContext(ctx)
    bag = bag.SetMember(member)
    return baggage.ContextWithBaggage(ctx, bag), nil
}

func GetBaggage(ctx context.Context, key string) string {
    bag := baggage.FromContext(ctx)
    member := bag.Member(key)
    return member.Value()
}
```

---

## 3. Span 操作

### 3.1 Span 创建

**Span 创建示例**：

```go
package main

import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/trace"
)

func HandlePayment(ctx context.Context, payment *Payment) error {
    tracer := otel.Tracer("payment-service")
    ctx, span := tracer.Start(ctx, "payment.process")
    defer span.End()

    // 处理支付
    if err := processPayment(ctx, payment); err != nil {
        span.RecordError(err)
        span.SetStatus(codes.Error, err.Error())
        return err
    }

    span.SetStatus(codes.Ok, "Payment processed successfully")
    return nil
}
```

### 3.2 Span 属性

**Span 属性设置**：

```go
func RecordSpanAttributes(span trace.Span, payment *Payment) {
    span.SetAttributes(
        attribute.String("payment.id", payment.ID),
        attribute.String("payment.order_id", payment.OrderID),
        attribute.Int64("payment.amount", payment.Amount),
        attribute.String("payment.currency", payment.Currency),
        attribute.String("payment.status", payment.Status),
    )
}
```

### 3.3 Span 事件

**Span 事件记录**：

```go
func RecordSpanEvents(span trace.Span, events []Event) {
    for _, event := range events {
        span.AddEvent(
            event.Name,
            trace.WithAttributes(
                attribute.String("event.type", event.Type),
                attribute.String("event.message", event.Message),
                attribute.String("event.timestamp", event.Timestamp.Format(time.RFC3339)),
            ),
        )
    }
}
```

---

## 4. 分布式追踪

### 4.1 上下文传播

**HTTP 上下文传播**：

```go
package main

import (
    "net/http"
    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

func SetupHTTPTracing() {
    handler := otelhttp.NewHandler(
        http.HandlerFunc(handleRequest),
        "payment-service",
        otelhttp.WithPropagators(otel.GetTextMapPropagator()),
    )

    http.Handle("/api/v1/payments", handler)
}
```

**gRPC 上下文传播**：

```go
package main

import (
    "go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc"
    "google.golang.org/grpc"
)

func SetupGRPCTracing() grpc.ServerOption {
    return grpc.UnaryInterceptor(
        otelgrpc.UnaryServerInterceptor(
            otelgrpc.WithPropagators(otel.GetTextMapPropagator()),
        ),
    )
}
```

### 4.2 跨服务追踪

**跨服务追踪示例**：

```go
func ProcessPaymentWithTracking(ctx context.Context, payment *Payment) error {
    tracer := otel.Tracer("payment-service")
    ctx, span := tracer.Start(ctx, "payment.process")
    defer span.End()

    // 调用订单服务
    ctx, orderSpan := tracer.Start(ctx, "order.validate")
    order, err := orderService.ValidateOrder(ctx, payment.OrderID)
    if err != nil {
        orderSpan.RecordError(err)
        orderSpan.End()
        return err
    }
    orderSpan.End()

    // 调用支付网关
    ctx, gatewaySpan := tracer.Start(ctx, "gateway.process")
    result, err := paymentGateway.Process(ctx, payment)
    if err != nil {
        gatewaySpan.RecordError(err)
        gatewaySpan.End()
        return err
    }
    gatewaySpan.End()

    return nil
}
```

---

## 5. 追踪采样

### 5.1 采样策略

**采样策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: TraceSamplingPolicy
metadata:
  name: trace-sampling-policy
spec:
  strategy: probabilistic
  rate: 0.1 # 10% 采样率
  rules:
    - condition: "service == 'payment-service'"
      rate: 1.0 # 100% 采样
    - condition: "error == true"
      rate: 1.0 # 错误 100% 采样
    - condition: "latency > 1s"
      rate: 0.5 # 慢请求 50% 采样
```

### 5.2 采样配置

**采样器实现**：

```go
package main

import (
    "go.opentelemetry.io/otel/sdk/trace"
    "go.opentelemetry.io/otel/trace"
)

func SetupSampler(rate float64) trace.Sampler {
    return trace.TraceIDRatioBased(rate)
}

func SetupCustomSampler() trace.Sampler {
    return trace.NewParentBased(
        trace.TraceIDRatioBased(0.1),
        trace.WithRemoteParentSampled(trace.AlwaysSample()),
        trace.WithLocalParentSampled(trace.AlwaysSample()),
    )
}
```

---

## 6. 追踪导出

### 6.1 OTLP 导出

**OTLP 追踪导出**：

```go
package main

import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/trace"
)

func setupOTLPTracing() (*trace.TracerProvider, error) {
    exporter, err := otlptracegrpc.New(
        context.Background(),
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
        trace.WithSampler(trace.TraceIDRatioBased(0.1)),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}
```

### 6.2 Jaeger 导出

**Jaeger 追踪导出**：

```go
package main

import (
    "go.opentelemetry.io/otel/exporters/jaeger"
    "go.opentelemetry.io/otel/sdk/trace"
)

func setupJaegerTracing() (*trace.TracerProvider, error) {
    exporter, err := jaeger.New(
        jaeger.WithCollectorEndpoint(jaeger.WithEndpoint("http://jaeger:14268/api/traces")),
    )
    if err != nil {
        return nil, err
    }

    tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
        trace.WithSampler(trace.TraceIDRatioBased(0.1)),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}
```

---

## 7. 相关文档

- **[API 可观测性规范](../12-api-observability/api-observability.md)** - 追踪可
  观测性
- **[API 监控告警](../20-api-monitoring/api-monitoring.md)** - 追踪监控
- **[API 微服务架构](../36-api-microservices/api-microservices.md)** - 分布式追
  踪
- **[最佳实践](../08-best-practices/best-practices.md)** - 追踪最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
