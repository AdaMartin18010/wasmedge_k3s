# 可观测性属性矩阵

## 📑 目录

- [可观测性属性矩阵](#可观测性属性矩阵)
  - [📑 目录](#-目录)
  - [可观测性属性对比](#可观测性属性对比)
  - [可观测性关系](#可观测性关系)
  - [可观测性优势分析](#可观测性优势分析)
    - [三大支柱](#三大支柱)
    - [横纵耦合定位](#横纵耦合定位)
    - [关联能力](#关联能力)
  - [可观测性实施建议](#可观测性实施建议)
    - [Metrics 实施](#metrics-实施)
    - [Logs 实施](#logs-实施)
    - [Traces 实施](#traces-实施)
    - [横纵耦合定位](#横纵耦合定位-1)
  - [可观测性测试方法](#可观测性测试方法)
    - [Metrics 测试](#metrics-测试)
    - [Logs 测试](#logs-测试)
    - [Traces 测试](#traces-测试)
  - [可观测性对比总结](#可观测性对比总结)
  - [可观测性代码示例](#可观测性代码示例)
    - [OTLP 实施示例](#otlp-实施示例)
    - [eBPF 实施示例](#ebpf-实施示例)
    - [横纵耦合定位示例](#横纵耦合定位示例)
  - [2025 年最新实践](#2025-年最新实践)
    - [OTLP 优化](#otlp-优化)
    - [eBPF 优化](#ebpf-优化)
    - [横纵耦合定位优化](#横纵耦合定位优化)
  - [实际应用案例](#实际应用案例)
    - [案例 1：大规模微服务集群](#案例-1大规模微服务集群)
    - [案例 2：边缘计算可观测性](#案例-2边缘计算可观测性)

---

**最后更新**: 2025-11-06 **维护者**: 项目团队

> 📋 **主文档链
> 接**：[30.8.4 可观测性属性矩阵](../concept-relations-matrix.md#3084-可观测性属性矩阵)

## 可观测性属性对比

| 技术           | Metrics | Logs | Traces | 采样 | 关联 | 下钻 |
| -------------- | ------- | ---- | ------ | ---- | ---- | ---- |
| **Prometheus** | ✅      | ❌   | ❌     | ✅   | ⚠️   | ⚠️   |
| **Loki**       | ❌      | ✅   | ❌     | ✅   | ⚠️   | ⚠️   |
| **Jaeger**     | ❌      | ❌   | ✅     | ✅   | ✅   | ✅   |
| **OTLP**       | ✅      | ✅   | ✅     | ✅   | ✅   | ✅   |
| **eBPF**       | ✅      | ✅   | ✅     | ✅   | ✅   | ✅   |

## 可观测性关系

```text
完整可观测性 = OTLP(横向) + eBPF(纵向)
OTLP提供横向坐标(请求链)
eBPF提供纵向坐标(内核栈)
```

## 可观测性优势分析

### 三大支柱

- **Metrics**：Prometheus（时间序列指标）
- **Logs**：Loki（日志聚合）
- **Traces**：Jaeger（分布式追踪）

### 横纵耦合定位

- **横向坐标（OTLP）**：请求链追踪，服务间调用关系
- **纵向坐标（eBPF）**：内核栈追踪，系统调用层级

### 关联能力

- **OTLP**：✅ 完整关联（Trace、Metrics、Logs 统一标签）
- **eBPF**：✅ 完整关联（内核层到应用层全链路）
- **传统工具**：⚠️ 部分关联（需要手动配置）

**优势**：OTLP + eBPF 组合提供最完整的可观测性能力

## 可观测性实施建议

### Metrics 实施

**Prometheus 实施**：

- 配置指标收集
- 设置告警规则
- 使用 Grafana 可视化

**OTLP Metrics 实施**：

- 使用 OpenTelemetry SDK
- 配置指标导出
- 使用 OTLP 接收器

### Logs 实施

**Loki 实施**：

- 配置日志收集
- 使用 Promtail 收集
- 使用 Grafana 查询

**OTLP Logs 实施**：

- 使用 OpenTelemetry SDK
- 配置日志导出
- 使用 OTLP 接收器

### Traces 实施

**Jaeger 实施**：

- 配置分布式追踪
- 使用 OpenTracing/OpenTelemetry
- 使用 Jaeger UI 查看

**OTLP Traces 实施**：

- 使用 OpenTelemetry SDK
- 配置追踪导出
- 使用 OTLP 接收器

### 横纵耦合定位

**横向坐标（OTLP）**：

- 实现请求链追踪
- 关联服务间调用
- 使用 Trace ID 关联

**纵向坐标（eBPF）**：

- 实现内核栈追踪
- 关联系统调用
- 使用 eBPF 探针

**耦合定位**：

- 结合横向和纵向坐标
- 实现全链路定位
- 快速定位问题根因

## 可观测性测试方法

### Metrics 测试

```bash
# 查询 Prometheus 指标
curl http://prometheus:9090/api/v1/query?query=up

# 查询 OTLP Metrics
curl http://otel-collector:4318/v1/metrics
```

### Logs 测试

```bash
# 查询 Loki 日志
curl -G -s "http://loki:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={job="app"}' \
  --data-urlencode 'start=1234567890' \
  --data-urlencode 'end=1234567900'
```

### Traces 测试

```bash
# 查询 Jaeger 追踪
curl http://jaeger:16686/api/traces?service=app

# 查询 OTLP Traces
curl http://otel-collector:4318/v1/traces
```

## 可观测性对比总结

| 可观测性指标 | Prometheus | Loki | Jaeger | OTLP | eBPF | 最佳组合 |
|-------------|-----------|------|--------|------|------|---------|
| **Metrics** | ✅ | ❌ | ❌ | ✅ | ✅ | OTLP/eBPF |
| **Logs** | ❌ | ✅ | ❌ | ✅ | ✅ | OTLP/eBPF |
| **Traces** | ❌ | ❌ | ✅ | ✅ | ✅ | OTLP/eBPF |
| **关联能力** | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | OTLP/eBPF |
| **下钻能力** | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | OTLP/eBPF |

**综合评估**：OTLP + eBPF 组合提供最完整的可观测性能力，支持横纵耦合定位。

## 可观测性代码示例

### OTLP 实施示例

**OpenTelemetry Go SDK**：

```go
// OpenTelemetry 指标和追踪
package main

import (
    "context"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc"
    "go.opentelemetry.io/otel/sdk/metric"
    "go.opentelemetry.io/otel/sdk/trace"
)

func setupOTLP(ctx context.Context) error {
    // 配置 Trace 导出器
    traceExporter, err := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint("otel-collector:4317"),
        otlptracegrpc.WithInsecure(),
    )
    if err != nil {
        return err
    }

    // 配置 Metric 导出器
    metricExporter, err := otlpmetricgrpc.New(ctx,
        otlpmetricgrpc.WithEndpoint("otel-collector:4317"),
        otlpmetricgrpc.WithInsecure(),
    )
    if err != nil {
        return err
    }

    // 创建 Trace Provider
    tp := trace.NewTracerProvider(
        trace.WithBatcher(traceExporter),
    )
    otel.SetTracerProvider(tp)

    // 创建 Metric Provider
    mp := metric.NewMeterProvider(
        metric.WithReader(metric.NewPeriodicReader(metricExporter)),
    )
    otel.SetMeterProvider(mp)

    return nil
}
```

**OpenTelemetry Collector 配置**：

```yaml
# OpenTelemetry Collector 配置
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
      - key: service.name
        value: my-service
        action: upsert

exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
  loki:
    endpoint: http://loki:3100/loki/api/v1/push
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

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
    logs:
      receivers: [otlp]
      processors: [batch, resource]
      exporters: [loki]
```

### eBPF 实施示例

**eBPF 内核追踪**：

```c
// eBPF 系统调用追踪
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 10240);
    __type(key, u32);
    __type(value, u64);
} syscall_count SEC(".maps");

SEC("tracepoint/syscalls/sys_enter_openat")
int trace_sys_enter_openat(void *ctx) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    u64 *count = bpf_map_lookup_elem(&syscall_count, &pid);
    if (count) {
        (*count)++;
    } else {
        u64 init = 1;
        bpf_map_update_elem(&syscall_count, &pid, &init, BPF_ANY);
    }
    return 0;
}

char LICENSE[] SEC("license") = "GPL";
```

**eBPF 程序部署**：

```yaml
# eBPF 程序部署
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: ebpf-tracer
spec:
  selector:
    matchLabels:
      app: ebpf-tracer
  template:
    metadata:
      labels:
        app: ebpf-tracer
    spec:
      hostNetwork: true
      hostPID: true
      containers:
      - name: ebpf-tracer
        image: ebpf-tracer:latest
        securityContext:
          privileged: true
        volumeMounts:
        - name: sys
          mountPath: /sys
        - name: debugfs
          mountPath: /sys/kernel/debug
      volumes:
      - name: sys
        hostPath:
          path: /sys
      - name: debugfs
        hostPath:
          path: /sys/kernel/debug
```

### 横纵耦合定位示例

**OTLP + eBPF 关联**：

```go
// OTLP 和 eBPF 数据关联
package main

import (
    "context"
    "go.opentelemetry.io/otel/trace"
)

func correlateOTLPAndEBPF(ctx context.Context, traceID trace.TraceID) {
    // 从 OTLP Trace 获取 Trace ID
    span := trace.SpanFromContext(ctx)
    traceID := span.SpanContext().TraceID()

    // 从 eBPF 获取系统调用信息
    syscallInfo := getEBPFSyscallInfo(traceID)

    // 关联 OTLP Trace 和 eBPF 系统调用
    correlateTraceAndSyscall(traceID, syscallInfo)
}
```

## 2025 年最新实践

### OTLP 优化

**技术栈**：

- OpenTelemetry 1.30（2025 最新）
- OTLP 1.0
- Kubernetes 1.30

**优化策略**：

- **列式编码**：使用 Arrow Flight 列式编码
- **采样优化**：智能采样减少数据量
- **批处理**：批处理提升性能

### eBPF 优化

**技术栈**：

- eBPF（Linux 6.1+）
- BCC/BPFTrace
- Kubernetes 1.30

**优化策略**：

- **内核态聚合**：内核态预聚合减少开销
- **零拷贝**：使用零拷贝技术
- **智能采样**：智能采样减少数据量

### 横纵耦合定位优化

**技术栈**：

- OTLP 1.0（横向坐标）
- eBPF（纵向坐标）
- Kubernetes 1.30

**优化策略**：

- **统一标签**：使用统一标签关联数据
- **智能关联**：使用 AI 算法智能关联
- **快速定位**：快速定位问题根因

## 实际应用案例

### 案例 1：大规模微服务集群

**场景**：1000+ 微服务的可观测性系统

**技术栈**：

- OpenTelemetry 1.30（OTLP）
- eBPF（内核追踪）
- Prometheus + Loki + Jaeger

**效果**：

- 数据关联：100% 关联
- 定位时间：< 1 分钟（从分钟级到秒级）
- 数据量：减少 60%（智能采样）

### 案例 2：边缘计算可观测性

**场景**：10000+ 边缘节点的可观测性系统

**技术栈**：

- OpenTelemetry 1.30（OTLP）
- eBPF（边缘节点追踪）
- K3s 1.30

**效果**：

- 数据收集：实时收集
- 定位时间：< 30 秒
- 带宽节省：80%（边缘预处理）

---

**最后更新**：2025-11-15
**维护者**：项目团队
**版本**：v1.2
