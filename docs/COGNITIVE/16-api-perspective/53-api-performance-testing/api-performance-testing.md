# API 性能测试规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 性能测试架构](#11-性能测试架构)
- [2. 性能测试类型](#2-性能测试类型)
  - [2.1 负载测试](#21-负载测试)
  - [2.2 压力测试](#22-压力测试)
  - [2.3 容量测试](#23-容量测试)
  - [2.4 稳定性测试](#24-稳定性测试)
- [3. 性能指标](#3-性能指标)
  - [3.1 延迟指标](#31-延迟指标)
  - [3.2 吞吐量指标](#32-吞吐量指标)
  - [3.3 资源指标](#33-资源指标)
- [4. 性能测试工具](#4-性能测试工具)
  - [4.1 k6](#41-k6)
  - [4.2 Apache Bench](#42-apache-bench)
  - [4.3 wrk](#43-wrk)
- [5. 性能测试场景](#5-性能测试场景)
  - [5.1 基准测试](#51-基准测试)
  - [5.2 峰值测试](#52-峰值测试)
  - [5.3 渐变测试](#53-渐变测试)
- [6. 性能优化](#6-性能优化)
  - [6.1 瓶颈分析](#61-瓶颈分析)
  - [6.2 优化策略](#62-优化策略)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 性能测试规范定义了 API 在性能测试场景下的设计和实现，从性能测试类型到性能指
标，从性能测试工具到性能优化。

### 1.1 性能测试架构

```text
性能测试工具（Performance Testing Tool）
  ↓
API 服务（API Service）
  ↓
性能指标采集（Metrics Collection）
  ↓
性能分析（Performance Analysis）
```

---

## 2. 性能测试类型

### 2.1 负载测试

**负载测试配置**：

```yaml
apiVersion: api.example.com/v1
kind: LoadTest
metadata:
  name: payment-api-load-test
spec:
  type: load
  target: "http://payment-service:8080/api/v1/payments"
  duration: "5m"
  virtualUsers: 100
  rampUp: "1m"
  scenarios:
    - name: create_payment
      weight: 80
      requests:
        - method: POST
          path: /api/v1/payments
          body:
            order_id: "order_123"
            amount: 10000
    - name: get_payment
      weight: 20
      requests:
        - method: GET
          path: /api/v1/payments/{payment_id}
```

### 2.2 压力测试

**压力测试配置**：

```yaml
apiVersion: api.example.com/v1
kind: StressTest
metadata:
  name: payment-api-stress-test
spec:
  type: stress
  target: "http://payment-service:8080/api/v1/payments"
  duration: "10m"
  virtualUsers:
    start: 10
    end: 1000
    step: 10
    stepDuration: "30s"
```

### 2.3 容量测试

**容量测试配置**：

```yaml
apiVersion: api.example.com/v1
kind: CapacityTest
metadata:
  name: payment-api-capacity-test
spec:
  type: capacity
  target: "http://payment-service:8080/api/v1/payments"
  duration: "1h"
  virtualUsers: 500
  metrics:
    - cpu_usage
    - memory_usage
    - network_bandwidth
    - database_connections
```

### 2.4 稳定性测试

**稳定性测试配置**：

```yaml
apiVersion: api.example.com/v1
kind: StabilityTest
metadata:
  name: payment-api-stability-test
spec:
  type: stability
  target: "http://payment-service:8080/api/v1/payments"
  duration: "24h"
  virtualUsers: 50
  checkInterval: "5m"
  failureThreshold: 0.01
```

---

## 3. 性能指标

### 3.1 延迟指标

**延迟指标定义**：

```yaml
apiVersion: api.example.com/v1
kind: PerformanceMetrics
metadata:
  name: payment-api-latency-metrics
spec:
  latency:
    p50: "50ms"
    p95: "200ms"
    p99: "500ms"
    p999: "1000ms"
    max: "2000ms"
```

**k6 延迟测试**：

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "1m", target: 100 },
    { duration: "3m", target: 100 },
    { duration: "1m", target: 0 }
  ],
  thresholds: {
    http_req_duration: ["p(50)<50", "p(95)<200", "p(99)<500"]
  }
};

export default function () {
  const res = http.post(
    "http://payment-service:8080/api/v1/payments",
    JSON.stringify({
      order_id: "order_123",
      amount: 10000
    }),
    {
      headers: { "Content-Type": "application/json" }
    }
  );

  check(res, {
    "status is 201": (r) => r.status === 201,
    "response time < 200ms": (r) => r.timings.duration < 200
  });

  sleep(1);
}
```

### 3.2 吞吐量指标

**吞吐量指标定义**：

```yaml
apiVersion: api.example.com/v1
kind: PerformanceMetrics
metadata:
  name: payment-api-throughput-metrics
spec:
  throughput:
    requestsPerSecond: 1000
    transactionsPerSecond: 500
    bytesPerSecond: "10MB"
```

### 3.3 资源指标

**资源指标定义**：

```yaml
apiVersion: api.example.com/v1
kind: PerformanceMetrics
metadata:
  name: payment-api-resource-metrics
spec:
  resources:
    cpu:
      average: "50%"
      peak: "80%"
    memory:
      average: "512Mi"
      peak: "1Gi"
    network:
      average: "100Mbps"
      peak: "500Mbps"
```

---

## 4. 性能测试工具

### 4.1 k6

**k6 测试脚本**：

```javascript
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

const errorRate = new Rate("errors");

export const options = {
  stages: [
    { duration: "2m", target: 100 },
    { duration: "5m", target: 100 },
    { duration: "2m", target: 200 },
    { duration: "5m", target: 200 },
    { duration: "2m", target: 0 }
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"],
    http_req_failed: ["rate<0.01"],
    errors: ["rate<0.1"]
  }
};

export default function () {
  const res = http.post(
    "http://payment-service:8080/api/v1/payments",
    JSON.stringify({
      order_id: `order_${__VU}_${__ITER}`,
      amount: 10000
    }),
    {
      headers: { "Content-Type": "application/json" }
    }
  );

  const checkRes = check(res, {
    "status is 201": (r) => r.status === 201,
    "response has payment_id": (r) =>
      JSON.parse(r.body).payment_id !== undefined
  });

  errorRate.add(!checkRes);
  sleep(1);
}
```

### 4.2 Apache Bench

**Apache Bench 测试**：

```bash
# 基本负载测试
ab -n 10000 -c 100 -p payment.json -T application/json \
  http://payment-service:8080/api/v1/payments

# 详细报告
ab -n 10000 -c 100 -p payment.json -T application/json \
  -v 2 -w http://payment-service:8080/api/v1/payments
```

### 4.3 wrk

**wrk 测试脚本**：

```lua
-- payment.lua
wrk.method = "POST"
wrk.body = '{"order_id":"order_123","amount":10000}'
wrk.headers["Content-Type"] = "application/json"

function response(status, headers, body)
  if status ~= 201 then
    print("Error: " .. status)
  end
end
```

**wrk 测试命令**：

```bash
wrk -t12 -c400 -d30s -s payment.lua \
  http://payment-service:8080/api/v1/payments
```

---

## 5. 性能测试场景

### 5.1 基准测试

**基准测试配置**：

```yaml
apiVersion: api.example.com/v1
kind: BenchmarkTest
metadata:
  name: payment-api-benchmark
spec:
  type: benchmark
  target: "http://payment-service:8080/api/v1/payments"
  duration: "5m"
  virtualUsers: 10
  warmUp: "1m"
  iterations: 1000
```

### 5.2 峰值测试

**峰值测试配置**：

```yaml
apiVersion: api.example.com/v1
kind: SpikeTest
metadata:
  name: payment-api-spike-test
spec:
  type: spike
  target: "http://payment-service:8080/api/v1/payments"
  duration: "10m"
  spike:
    startUsers: 10
    spikeUsers: 1000
    spikeDuration: "1m"
    recoveryDuration: "5m"
```

### 5.3 渐变测试

**渐变测试配置**：

```yaml
apiVersion: api.example.com/v1
kind: RampTest
metadata:
  name: payment-api-ramp-test
spec:
  type: ramp
  target: "http://payment-service:8080/api/v1/payments"
  duration: "30m"
  ramp:
    - duration: "5m"
      users: 10
    - duration: "5m"
      users: 50
    - duration: "5m"
      users: 100
    - duration: "5m"
      users: 200
    - duration: "5m"
      users: 500
    - duration: "5m"
      users: 0
```

---

## 6. 性能优化

### 6.1 瓶颈分析

**瓶颈分析工具**：

```yaml
apiVersion: api.example.com/v1
kind: PerformanceProfiling
metadata:
  name: payment-api-profiling
spec:
  tools:
    - name: pprof
      enabled: true
      port: 6060
    - name: flamegraph
      enabled: true
    - name: trace
      enabled: true
```

### 6.2 优化策略

**性能优化策略**：

```yaml
apiVersion: api.example.com/v1
kind: PerformanceOptimization
metadata:
  name: payment-api-optimization
spec:
  strategies:
    - type: caching
      enabled: true
      ttl: "5m"
    - type: connection_pooling
      enabled: true
      maxConnections: 100
    - type: compression
      enabled: true
      algorithm: gzip
    - type: batch_processing
      enabled: true
      batchSize: 100
```

---

## 7. 相关文档

- **[API 性能优化](../14-api-performance/api-performance.md)** - 性能优化策略
- **[API 基准测试](../27-api-benchmarks/api-benchmarks.md)** - 性能基准
- **[API 测试规范](../15-api-testing/api-testing.md)** - 性能测试
- **[最佳实践](../08-best-practices/best-practices.md)** - 性能测试最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
