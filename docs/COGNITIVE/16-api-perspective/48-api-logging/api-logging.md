# API 日志规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 日志架构](#11-日志架构)
- [2. 日志格式](#2-日志格式)
  - [2.1 结构化日志](#21-结构化日志)
  - [2.2 日志字段](#22-日志字段)
- [3. 日志级别](#3-日志级别)
  - [3.1 级别定义](#31-级别定义)
  - [3.2 级别使用](#32-级别使用)
- [4. 日志采集](#4-日志采集)
  - [4.1 容器日志](#41-容器日志)
  - [4.2 应用日志](#42-应用日志)
- [5. 日志存储](#5-日志存储)
  - [5.1 日志保留](#51-日志保留)
  - [5.2 日志归档](#52-日志归档)
- [6. 日志查询](#6-日志查询)
  - [6.1 查询语法](#61-查询语法)
  - [6.2 日志分析](#62-日志分析)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 日志规范定义了 API 在日志场景下的设计和实现，从日志格式到日志级别，从日志采
集到日志查询。

### 1.1 日志架构

```text
API 请求（API Request）
  ↓
日志生成（Log Generation）
  ↓
日志采集（Log Collection）
  ↓
日志存储（Log Storage）
  ↓
日志查询（Log Query）
```

---

## 2. 日志格式

### 2.1 结构化日志

**JSON 结构化日志**：

```json
{
  "timestamp": "2025-11-07T10:00:00.123Z",
  "level": "INFO",
  "service": "payment-service",
  "version": "1.0.0",
  "environment": "production",
  "request": {
    "id": "req_1234567890",
    "method": "POST",
    "path": "/api/v1/payments",
    "user_id": "user_123",
    "ip": "192.168.1.1"
  },
  "response": {
    "status": 201,
    "latency_ms": 45
  },
  "message": "Payment created successfully",
  "context": {
    "payment_id": "pay_456",
    "order_id": "order_789",
    "amount": 10000
  }
}
```

**Go 结构化日志实现**：

```go
package main

import (
    "github.com/sirupsen/logrus"
    "encoding/json"
)

type StructuredLogger struct {
    logger *logrus.Logger
}

func NewStructuredLogger() *StructuredLogger {
    logger := logrus.New()
    logger.SetFormatter(&logrus.JSONFormatter{
        TimestampFormat: time.RFC3339Nano,
    })
    return &StructuredLogger{logger: logger}
}

func (sl *StructuredLogger) LogRequest(req *http.Request, resp *http.Response, latency time.Duration) {
    sl.logger.WithFields(logrus.Fields{
        "request_id": req.Header.Get("X-Request-ID"),
        "method":     req.Method,
        "path":       req.URL.Path,
        "status":     resp.StatusCode,
        "latency_ms": latency.Milliseconds(),
    }).Info("Request processed")
}
```

### 2.2 日志字段

**标准日志字段**：

```yaml
apiVersion: api.example.com/v1
kind: LogFieldPolicy
metadata:
  name: standard-log-fields
spec:
  requiredFields:
    - timestamp
    - level
    - service
    - message
  optionalFields:
    - request_id
    - user_id
    - trace_id
    - span_id
    - environment
    - version
  customFields:
    - payment_id
    - order_id
    - amount
```

---

## 3. 日志级别

### 3.1 级别定义

**日志级别规范**：

```yaml
apiVersion: api.example.com/v1
kind: LogLevelPolicy
metadata:
  name: log-level-definitions
spec:
  levels:
    - level: TRACE
      priority: 0
      useCase: "Very detailed debugging"
      examples:
        - "Function entry/exit"
        - "Variable values"
    - level: DEBUG
      priority: 1
      useCase: "Debugging information"
      examples:
        - "Request details"
        - "Response details"
    - level: INFO
      priority: 2
      useCase: "Informational messages"
      examples:
        - "Request processed"
        - "Cache hit"
    - level: WARN
      priority: 3
      useCase: "Warning messages"
      examples:
        - "Rate limit approaching"
        - "Deprecated API usage"
    - level: ERROR
      priority: 4
      useCase: "Error messages"
      examples:
        - "Payment processing failed"
        - "Database query failed"
    - level: FATAL
      priority: 5
      useCase: "Fatal errors"
      examples:
        - "Service crash"
        - "Critical system failure"
```

### 3.2 级别使用

**日志级别配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: log-level-config
data:
  log-level.yaml: |
    default: INFO
    services:
      payment-service: DEBUG
      order-service: INFO
      user-service: WARN
    environments:
      development: DEBUG
      staging: INFO
      production: WARN
```

---

## 4. 日志采集

### 4.1 容器日志

**Kubernetes 日志采集**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: payment-service
spec:
  containers:
    - name: payment-service
      image: payment-service:latest
      env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: LOG_FORMAT
          value: "json"
      volumeMounts:
        - name: log-volume
          mountPath: /var/log
  volumes:
    - name: log-volume
      emptyDir: {}
```

**Fluentd 日志采集**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      read_from_head true
      <parse>
        @type json
        time_key time
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>

    <match kubernetes.**>
      @type forward
      <server>
        host elasticsearch.logging.svc.cluster.local
        port 9200
      </server>
    </match>
```

### 4.2 应用日志

**应用日志配置**：

```go
package main

import (
    "github.com/sirupsen/logrus"
    "go.opentelemetry.io/otel/trace"
)

func SetupLogger() *logrus.Logger {
    logger := logrus.New()
    logger.SetFormatter(&logrus.JSONFormatter{})
    logger.SetLevel(logrus.InfoLevel)

    // 添加追踪上下文
    logger.AddHook(&TraceHook{})

    return logger
}

type TraceHook struct{}

func (h *TraceHook) Levels() []logrus.Level {
    return logrus.AllLevels
}

func (h *TraceHook) Fire(entry *logrus.Entry) error {
    ctx := entry.Context
    if ctx != nil {
        span := trace.SpanFromContext(ctx)
        if span.SpanContext().IsValid() {
            entry.Data["trace_id"] = span.SpanContext().TraceID().String()
            entry.Data["span_id"] = span.SpanContext().SpanID().String()
        }
    }
    return nil
}
```

---

## 5. 日志存储

### 5.1 日志保留

**日志保留策略**：

```yaml
apiVersion: api.example.com/v1
kind: LogRetentionPolicy
metadata:
  name: log-retention-policy
spec:
  retention:
    - level: INFO
      days: 30
    - level: WARN
      days: 90
    - level: ERROR
      days: 365
    - level: FATAL
      days: 365
  storage:
    type: s3
    bucket: logs-production
    prefix: "api-logs/"
```

### 5.2 日志归档

**日志归档配置**：

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: log-archive
spec:
  schedule: "0 2 * * *" # 每天凌晨2点
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: log-archiver
              image: log-archiver:latest
              command:
                - /bin/sh
                - -c
                - |
                  # 归档30天前的日志
                  find /var/log -name "*.log" -mtime +30 -exec gzip {} \;
                  # 上传到S3
                  aws s3 sync /var/log/archived s3://logs-production/archived/
```

---

## 6. 日志查询

### 6.1 查询语法

**Elasticsearch 查询示例**：

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "service": "payment-service"
          }
        },
        {
          "range": {
            "timestamp": {
              "gte": "2025-11-07T00:00:00Z",
              "lte": "2025-11-07T23:59:59Z"
            }
          }
        },
        {
          "match": {
            "level": "ERROR"
          }
        }
      ]
    }
  },
  "sort": [
    {
      "timestamp": {
        "order": "desc"
      }
    }
  ]
}
```

### 6.2 日志分析

**日志分析查询**：

```yaml
apiVersion: api.example.com/v1
kind: LogAnalysisQuery
metadata:
  name: error-analysis
spec:
  queries:
    - name: error-rate-by-service
      query: |
        SELECT service, count(*) as error_count
        FROM logs
        WHERE level = 'ERROR'
        GROUP BY service
        ORDER BY error_count DESC
    - name: error-trend
      query: |
        SELECT date_trunc('hour', timestamp) as hour, count(*) as error_count
        FROM logs
        WHERE level = 'ERROR'
        GROUP BY hour
        ORDER BY hour DESC
        LIMIT 24
```

---

## 7. 相关文档

- **[API 可观测性规范](../12-api-observability/api-observability.md)** - 日志可
  观测性
- **[API 监控告警](../20-api-monitoring/api-monitoring.md)** - 日志监控
- **[API 错误处理](../47-api-error-handling/api-error-handling.md)** - 错误日志
- **[最佳实践](../08-best-practices/best-practices.md)** - 日志最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
