# API 可观测性规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 可观测性三大支柱](#11-可观测性三大支柱)
  - [1.2 API 可观测性在 API 规范中的位置](#12-api-可观测性在-api-规范中的位置)
- [2. 容器化 API 可观测性](#2-容器化-api-可观测性)
  - [2.1 Kubernetes Metrics API](#21-kubernetes-metrics-api)
  - [2.2 Kubernetes Events API](#22-kubernetes-events-api)
- [3. 沙盒化 API 可观测性](#3-沙盒化-api-可观测性)
  - [3.1 gVisor Tracing](#31-gvisor-tracing)
  - [3.2 eBPF 系统调用追踪](#32-ebpf-系统调用追踪)
- [4. WASM 化 API 可观测性](#4-wasm-化-api-可观测性)
  - [4.1 WASI Tracing 接口](#41-wasi-tracing-接口)
  - [4.2 WasmEdge 可观测性](#42-wasmedge-可观测性)
- [5. OTLP 统一可观测性](#5-otlp-统一可观测性)
  - [5.1 OTLP 协议概述](#51-otlp-协议概述)
  - [5.2 OTLP 集成示例](#52-otlp-集成示例)
  - [5.3 OpenTelemetry Collector 配置](#53-opentelemetry-collector-配置)
- [6. eBPF 增强可观测性](#6-ebpf-增强可观测性)
  - [6.1 eBPF 零侵入追踪](#61-ebpf-零侵入追踪)
  - [6.2 eBPF + OTLP 集成](#62-ebpf--otlp-集成)
- [7. 可观测性最佳实践](#7-可观测性最佳实践)
  - [7.1 采样策略](#71-采样策略)
  - [7.2 追踪上下文传播](#72-追踪上下文传播)
  - [7.3 指标聚合](#73-指标聚合)
- [8. 形式化定义与理论基础](#8-形式化定义与理论基础)
  - [8.1 API 可观测性形式化模型](#81-api-可观测性形式化模型)
  - [8.2 追踪形式化](#82-追踪形式化)
  - [8.3 指标形式化](#83-指标形式化)
- [9. 相关文档](#9-相关文档)

---

## 1. 概述

API 可观测性是 API 规范的重要组成部分，通过 OTLP、eBPF、Prometheus 等技术实现
API 调用的全链路追踪、指标采集和日志聚合。本文档基于形式化方法，提供严格的数学定
义和推理论证，分析 API 可观测性的理论基础和实践方法。

**参考标准**：

- [OpenTelemetry Specification](https://opentelemetry.io/docs/specs/) -
  OpenTelemetry 规范
- [OTLP Protocol](https://opentelemetry.io/docs/specs/otlp/) - OTLP 协议
- [Prometheus Metrics](https://prometheus.io/docs/concepts/metric_types/) -
  Prometheus 指标
- [eBPF Documentation](https://ebpf.io/) - eBPF 文档
- [Distributed Tracing](https://opentracing.io/) - 分布式追踪

### 1.1 可观测性三大支柱

```text
Tracing（追踪）
  ↓
Metrics（指标）
  ↓
Logging（日志）
  ↓
统一 OTLP 协议
```

### 1.2 API 可观测性在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API 可观测性是 Observability 维度的核心：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
                            ↑
                    API Observability
```

API 可观测性在 API 规范中提供：

- **追踪（Tracing）**：OTLP、OpenTelemetry 等全链路追踪
- **指标（Metrics）**：Prometheus、OTLP Metrics 等指标采集
- **日志（Logging）**：结构化日志、OTLP Logs 等日志聚合
- **eBPF 增强**：零侵入的运行时追踪和监控

---

## 2. 容器化 API 可观测性

### 2.1 Kubernetes Metrics API

**Pod Metrics API**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: payment-service
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
spec:
  containers:
    - name: app
      image: payment-service:latest
      ports:
        - containerPort: 8080
```

**ServiceMonitor（Prometheus Operator）**：

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
    - port: http
      path: /metrics
      interval: 30s
```

### 2.2 Kubernetes Events API

**事件查询**：

```bash
# 查询 Pod 事件
kubectl get events --field-selector involvedObject.name=payment-service

# 查询 API 相关事件
kubectl get events --field-selector reason=APIDefinitionUpdated
```

---

## 3. 沙盒化 API 可观测性

### 3.1 gVisor Tracing

**gVisor 追踪配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gvisor-pod
spec:
  runtimeClassName: gvisor
  containers:
    - name: app
      image: app:latest
      env:
        - name: GVISOR_TRACE
          value: "true"
        - name: GVISOR_TRACE_FILE
          value: "/tmp/gvisor-trace.log"
```

**gVisor 追踪数据格式**：

```json
{
  "timestamp": "2025-11-07T10:00:00Z",
  "event": "syscall",
  "syscall": "openat",
  "pid": 12345,
  "args": {
    "fd": -100,
    "path": "/etc/passwd",
    "flags": 0
  },
  "result": -1
}
```

### 3.2 eBPF 系统调用追踪

**eBPF 追踪程序**：

```c
// trace_syscalls.c
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

SEC("tracepoint/syscalls/sys_enter_openat")
int trace_openat(struct trace_event_raw_sys_enter *ctx) {
    u64 pid_tgid = bpf_get_current_pid_tgid();
    u32 pid = pid_tgid >> 32;

    // 过滤容器进程
    struct task_struct *task = (struct task_struct *)bpf_get_current_task();
    if (!is_container_process(task)) {
        return 0;
    }

    // 记录系统调用事件
    struct syscall_event event = {
        .pid = pid,
        .syscall = __NR_openat,
        .timestamp = bpf_ktime_get_ns()
    };

    bpf_perf_event_output(ctx, &events, BPF_F_CURRENT_CPU, &event, sizeof(event));
    return 0;
}
```

---

## 4. WASM 化 API 可观测性

### 4.1 WASI Tracing 接口

**WIT Tracing 定义**：

```wit
// wasi:tracing@0.1.0
interface tracing {
    type span-context = record {
        trace-id: list<u8>,
        span-id: list<u8>
    };

    type span-id = u64;

    type key-value = record {
        key: string,
        value: string
    };

    get-parent-span: func() -> span-context;
    record-span: func(
        name: string,
        start-time: u64,
        attributes: list<key-value>
    ) -> span-id;
    finish-span: func(span-id: span-id, end-time: u64);
}
```

**Rust 实现示例**：

```rust
use wasi::tracing::{Tracing, SpanContext, SpanId};

struct TracingImpl;

impl Tracing for TracingImpl {
    fn get_parent_span(&mut self) -> SpanContext {
        // 从 HTTP 头中提取 TraceParent
        // traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
        SpanContext {
            trace_id: extract_trace_id(),
            span_id: extract_span_id(),
        }
    }

    fn record_span(&mut self, name: String, start_time: u64, attributes: Vec<KeyValue>) -> SpanId {
        // 记录 Span 到 OTLP
        let span_id = generate_span_id();
        export_to_otlp(span_id, name, start_time, attributes);
        span_id
    }
}
```

### 4.2 WasmEdge 可观测性

**WasmEdge 配置**：

```toml
[wasmtime]
# 启用追踪
enable_tracing = true

# OTLP 导出配置
[observability]
otlp_endpoint = "http://otel-collector:4317"
service_name = "wasm-service"
```

---

## 5. OTLP 统一可观测性

### 5.1 OTLP 协议概述

**OTLP（OpenTelemetry Protocol）**是 CNCF 标准，统一了 Trace、Metric、Log 三种可
观测性数据。

**OTLP 数据模型**：

```protobuf
// Trace
message Span {
    string trace_id = 1;
    string span_id = 2;
    string parent_span_id = 3;
    string name = 4;
    SpanKind kind = 5;
    uint64 start_time_unix_nano = 6;
    uint64 end_time_unix_nano = 7;
    repeated KeyValue attributes = 8;
}

// Metric
message Metric {
    string name = 1;
    MetricType type = 2;
    repeated NumberDataPoint data_points = 3;
}

// Log
message LogRecord {
    uint64 time_unix_nano = 1;
    SeverityNumber severity_number = 2;
    string body = 3;
    repeated KeyValue attributes = 4;
}
```

### 5.2 OTLP 集成示例

**Go SDK 配置**：

```go
package main

import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/sdk/resource"
    "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
)

func initTracer() (*trace.TracerProvider, error) {
    exporter, err := otlptracegrpc.New(context.Background(),
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return nil, err
    }

    tp := trace.NewTracerProvider(
        trace.WithBatcher(exporter),
        trace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceNameKey.String("payment-service"),
            semconv.ServiceVersionKey.String("1.0.0"),
        )),
    )

    otel.SetTracerProvider(tp)
    return tp, nil
}
```

**HTTP 客户端追踪**：

```go
func callAPI(ctx context.Context, url string) error {
    tracer := otel.Tracer("payment-service")
    ctx, span := tracer.Start(ctx, "call-payment-api")
    defer span.End()

    req, _ := http.NewRequestWithContext(ctx, "POST", url, nil)

    // 注入 Trace 上下文
    otel.GetTextMapPropagator().Inject(ctx, propagation.HeaderCarrier(req.Header))

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        span.RecordError(err)
        return err
    }

    span.SetAttributes(
        attribute.Int("http.status_code", resp.StatusCode),
        attribute.String("http.method", "POST"),
    )

    return nil
}
```

### 5.3 OpenTelemetry Collector 配置

**Collector 配置**：

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024
  resource:
    attributes:
      - key: environment
        value: production
        action: upsert

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true
  prometheus:
    endpoint: 0.0.0.0:8889

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, resource]
      exporters: [jaeger]
    metrics:
      receivers: [otlp]
      processors: [batch, resource]
      exporters: [prometheus]
```

---

## 6. eBPF 增强可观测性

### 6.1 eBPF 零侵入追踪

**eBPF 追踪 gRPC 调用**：

```c
// trace_grpc.c
SEC("uprobe/grpc_call")
int trace_grpc_call(struct pt_regs *ctx) {
    struct grpc_span_t span = {
        .trace_id = bpf_get_current_task(),
        .span_id = bpf_ktime_get_ns(),
        .name = "grpc_call",
        .kind = SPAN_KIND_CLIENT,
        .start_time = bpf_ktime_get_ns(),
    };

    // 提取 gRPC 方法名
    char method[64];
    bpf_probe_read_user_str(method, sizeof(method), (void *)PT_REGS_PARM1(ctx));
    bpf_probe_read_user_str(span.method, sizeof(span.method), method);

    bpf_perf_event_output(ctx, &events, BPF_F_CURRENT_CPU, &span, sizeof(span));
    return 0;
}
```

### 6.2 eBPF + OTLP 集成

**eBPF 事件转换为 OTLP**：

```go
func convertEBPFToOTLP(event *EBPFSpanEvent) *otlptrace.Span {
    span := &otlptrace.Span{
        TraceId:           event.TraceID,
        SpanId:            event.SpanID,
        ParentSpanId:      event.ParentSpanID,
        Name:              event.Name,
        Kind:              otlptrace.Span_SpanKind(event.Kind),
        StartTimeUnixNano: event.StartTime,
        EndTimeUnixNano:   event.EndTime,
        Attributes: []*otlpcommon.KeyValue{
            {
                Key:   "ebpf.source",
                Value: &otlpcommon.AnyValue{Value: &otlpcommon.AnyValue_StringValue{StringValue: "ebpf"}},
            },
        },
    }
    return span
}
```

---

## 7. 可观测性最佳实践

### 7.1 采样策略

**概率采样**：

```yaml
# OpenTelemetry Collector 采样配置
processors:
  probabilistic_sampler:
    sampling_percentage: 1.0 # 1% 采样率
```

**基于延迟的采样**：

```yaml
processors:
  tail_sampling:
    policies:
      - name: always-sample
        type: always_sample
      - name: latency
        type: latency
        latency:
          threshold_ms: 100 # P99 以上全采样
```

### 7.2 追踪上下文传播

**HTTP 传播**：

```go
// 服务端提取 Trace 上下文
func extractTraceContext(r *http.Request) context.Context {
    ctx := r.Context()

    // 从 HTTP 头提取 TraceParent
    traceParent := r.Header.Get("traceparent")
    if traceParent != "" {
        ctx = otel.GetTextMapPropagator().Extract(ctx, propagation.HeaderCarrier(r.Header))
    }

    return ctx
}
```

**gRPC 传播**：

```go
// gRPC 拦截器
func UnaryTraceInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
    ctx = otel.GetTextMapPropagator().Extract(ctx, metadata.NewIncoming(ctx))

    tracer := otel.Tracer("payment-service")
    ctx, span := tracer.Start(ctx, info.FullMethod)
    defer span.End()

    return handler(ctx, req)
}
```

### 7.3 指标聚合

**Prometheus 指标定义**：

```go
var (
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "status", "endpoint"},
    )

    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint"},
    )
)
```

---

## 8. 形式化定义与理论基础

### 8.1 API 可观测性形式化模型

**定义 8.1（API 可观测性）**：API 可观测性是一个三元组：

```text
API_Observability = ⟨Tracing, Metrics, Logging⟩
```

其中：

- **Tracing**：追踪数据 `Tracing: Span[]`
- **Metrics**：指标数据 `Metrics: Metric[]`
- **Logging**：日志数据 `Logging: Log[]`

**定义 8.2（可观测性覆盖度）**：可观测性覆盖度是一个函数：

```text
Coverage(API) = f(Trace_Coverage, Metric_Coverage, Log_Coverage)
```

其中每个覆盖度 `[0, 1]`。

**定理 8.1（可观测性完备性）**：如果可观测性覆盖度为 1，则 API 完全可观测：

```text
Coverage(API) = 1 ⟹ Fully_Observable(API)
```

**证明**：如果追踪、指标和日志覆盖度都为 1，则所有 API 调用都被追踪、监控和记录
，因此 API 完全可观测。□

### 8.2 追踪形式化

**定义 8.3（Span）**：Span 是一个五元组：

```text
Span = ⟨TraceID, SpanID, Operation, StartTime, EndTime⟩
```

**定义 8.4（追踪上下文）**：追踪上下文是一个函数：

```text
Trace_Context: Request → Span[]
```

**定理 8.2（追踪完整性）**：如果所有 Span 都关联到同一个 TraceID，则追踪完整：

```text
∀ span₁, span₂ ∈ Trace_Context(req): span₁.TraceID = span₂.TraceID ⟹ Complete_Trace(req)
```

**证明**：如果所有 Span 共享同一个 TraceID，则它们属于同一个追踪链路，因此追踪完
整。□

### 8.3 指标形式化

**定义 8.5（指标）**：指标是一个三元组：

```text
Metric = ⟨Name, Value, Timestamp⟩
```

**定义 8.6（指标聚合）**：指标聚合是一个函数：

```text
Aggregate: Metric[] × TimeWindow → Aggregated_Metric
```

**定理 8.3（指标一致性）**：相同时间窗口的指标聚合结果一致：

```text
Aggregate(Metrics, Window) = Aggregate(Metrics', Window) ⟺ Metrics = Metrics'
```

**证明**：如果指标集合相同，则聚合结果相同。□

**定义 8.7（RED 指标）**：RED 指标是一个三元组：

```text
RED_Metrics = ⟨Rate, Errors, Duration⟩
```

其中：

- **Rate**：请求速率 `Rate: Requests/Time`
- **Errors**：错误率 `Errors: Error_Rate`
- **Duration**：响应时间 `Duration: Time`

**定理 8.4（RED 指标完备性）**：RED 指标足以评估 API 性能：

```text
RED_Metrics(API) ⟹ Performance_Assessable(API)
```

**证明**：RED 指标覆盖了请求速率、错误率和响应时间，这些是评估 API 性能的关键指
标。□

---

## 9. 相关文档

- **[最佳实践](../00-foundation/05-best-practices.md)** - API 可观测性最佳实践
- **[eBPF/OTLP 扩展技术分析](../../TECHNICAL/32-ebpf-otlp-analysis/ebpf-otlp-analysis.md)**
  ⭐ - eBPF 和 OTLP 技术详解
- **[eBPF/OTLP 认知视角](../../COGNITIVE/13-ebpf-otlp-perspective/ebpf-otlp-perspective.md)** -
  eBPF/OTLP 认知视角
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
