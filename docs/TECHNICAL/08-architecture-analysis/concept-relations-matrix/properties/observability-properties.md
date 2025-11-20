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

---

**最后更新**：2025-11-15
**维护者**：项目团队
**版本**：v1.1
