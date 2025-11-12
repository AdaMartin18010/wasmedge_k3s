# API 限流规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 限流架构](#11-限流架构)
  - [1.2 API 限流在 API 规范中的位置](#12-api-限流在-api-规范中的位置)
- [2 限流算法](#2-限流算法)
  - [2.1 令牌桶算法](#21-令牌桶算法)
  - [2.2 漏桶算法](#22-漏桶算法)
  - [2.3 滑动窗口算法](#23-滑动窗口算法)
- [3 限流策略](#3-限流策略)
  - [3.1 基于 IP 的限流](#31-基于-ip-的限流)
  - [3.2 基于用户的限流](#32-基于用户的限流)
  - [3.3 基于 API Key 的限流](#33-基于-api-key-的限流)
- [4 分布式限流](#4-分布式限流)
  - [4.1 Redis 限流](#41-redis-限流)
  - [4.2 一致性哈希](#42-一致性哈希)
- [5 限流响应](#5-限流响应)
  - [5.1 HTTP 状态码](#51-http-状态码)
  - [5.2 Rate Limit Headers](#52-rate-limit-headers)
- [6 动态限流](#6-动态限流)
  - [6.1 自适应限流](#61-自适应限流)
  - [6.2 熔断器集成](#62-熔断器集成)
- [7 相关文档](#7-相关文档)

---

## 1 概述

API 限流规范定义了 API 在限流场景下的设计和实现，从限流算法到限流策略，从分布式
限流到动态限流。本文档基于形式化方法，提供严格的数学定义和推理论证，分析 API 限
流的理论基础和实践方法。

**参考标准**：

- [Rate Limiting Best Practices](https://cloud.google.com/architecture/rate-limiting-strategies-techniques) -
  限流最佳实践
- [Token Bucket Algorithm](https://en.wikipedia.org/wiki/Token_bucket) - 令牌桶
  算法
- [Leaky Bucket Algorithm](https://en.wikipedia.org/wiki/Leaky_bucket) - 漏桶算
  法
- [RFC 6585](https://tools.ietf.org/html/rfc6585) - HTTP 429 状态码
- [Distributed Rate Limiting](https://redis.io/docs/manual/patterns/rate-limiting/) -
  分布式限流

### 1.1 限流架构

```text
API 请求（API Request）
  ↓
限流中间件（Rate Limiter Middleware）
  ↓
限流算法（Rate Limiting Algorithm）
  ↓
限流存储（Rate Limit Store）
```

### 1.2 API 限流在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../07-formalization/formalization.md#21-api-规范四元组)）
，API 限流主要涉及 Governance 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
                    ↑
            Rate Limiting (implementation)
```

API 限流在 API 规范中提供：

- **流量控制**：限制 API 请求速率
- **资源保护**：防止 API 过载
- **公平性**：确保资源公平分配
- **动态调整**：根据负载动态调整限流策略

---

## 2 限流算法

### 2.1 令牌桶算法

**令牌桶实现**：

```go
package main

import (
    "sync"
    "time"
)

type TokenBucket struct {
    capacity     int
    tokens       int
    refillRate   int
    refillPeriod time.Duration
    mutex        sync.Mutex
    lastRefill   time.Time
}

func NewTokenBucket(capacity, refillRate int, refillPeriod time.Duration) *TokenBucket {
    return &TokenBucket{
        capacity:     capacity,
        tokens:       capacity,
        refillRate:   refillRate,
        refillPeriod: refillPeriod,
        lastRefill:   time.Now(),
    }
}

func (tb *TokenBucket) Allow() bool {
    tb.mutex.Lock()
    defer tb.mutex.Unlock()

    now := time.Now()
    elapsed := now.Sub(tb.lastRefill)

    if elapsed >= tb.refillPeriod {
        tokensToAdd := int(elapsed / tb.refillPeriod) * tb.refillRate
        tb.tokens = min(tb.capacity, tb.tokens+tokensToAdd)
        tb.lastRefill = now
    }

    if tb.tokens > 0 {
        tb.tokens--
        return true
    }

    return false
}
```

### 2.2 漏桶算法

**漏桶实现**：

```go
type LeakyBucket struct {
    capacity     int
    current      int
    leakRate     int
    leakPeriod   time.Duration
    mutex        sync.Mutex
    lastLeak     time.Time
}

func (lb *LeakyBucket) Allow() bool {
    lb.mutex.Lock()
    defer lb.mutex.Unlock()

    now := time.Now()
    elapsed := now.Sub(lb.lastLeak)

    if elapsed >= lb.leakPeriod {
        leaks := int(elapsed / lb.leakPeriod) * lb.leakRate
        lb.current = max(0, lb.current-leaks)
        lb.lastLeak = now
    }

    if lb.current < lb.capacity {
        lb.current++
        return true
    }

    return false
}
```

### 2.3 滑动窗口算法

**滑动窗口实现**：

```go
type SlidingWindow struct {
    windowSize   time.Duration
    maxRequests  int
    requests     []time.Time
    mutex        sync.Mutex
}

func (sw *SlidingWindow) Allow() bool {
    sw.mutex.Lock()
    defer sw.mutex.Unlock()

    now := time.Now()
    cutoff := now.Add(-sw.windowSize)

    // 移除过期请求
    validRequests := []time.Time{}
    for _, req := range sw.requests {
        if req.After(cutoff) {
            validRequests = append(validRequests, req)
        }
    }
    sw.requests = validRequests

    if len(sw.requests) < sw.maxRequests {
        sw.requests = append(sw.requests, now)
        return true
    }

    return false
}
```

---

## 3 限流策略

### 3.1 基于 IP 的限流

**IP 限流配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: EnvoyFilter
metadata:
  name: ip-rate-limit
spec:
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.local_ratelimit
          typed_config:
            "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
            stat_prefix: http_local_rate_limiter
            token_bucket:
              max_tokens: 100
              tokens_per_fill: 100
              fill_interval: 60s
```

### 3.2 基于用户的限流

**用户限流配置**：

```yaml
apiVersion: api.example.com/v1
kind: RateLimitPolicy
metadata:
  name: user-rate-limit
spec:
  type: user
  limits:
    - user_id: "user_123"
      rate: 1000
      period: "1h"
    - user_id: "user_456"
      rate: 500
      period: "1h"
```

### 3.3 基于 API Key 的限流

**API Key 限流配置**：

```yaml
apiVersion: api.example.com/v1
kind: RateLimitPolicy
metadata:
  name: apikey-rate-limit
spec:
  type: apikey
  tiers:
    - name: free
      rate: 100
      period: "1h"
    - name: basic
      rate: 1000
      period: "1h"
    - name: premium
      rate: 10000
      period: "1h"
```

---

## 4 分布式限流

### 4.1 Redis 限流

**Redis 限流实现**：

```go
package main

import (
    "github.com/go-redis/redis/v8"
    "context"
    "time"
)

func RateLimitWithRedis(client *redis.Client, key string, limit int, window time.Duration) (bool, error) {
    ctx := context.Background()

    pipe := client.Pipeline()
    incr := pipe.Incr(ctx, key)
    pipe.Expire(ctx, key, window)
    _, err := pipe.Exec(ctx)

    if err != nil {
        return false, err
    }

    count := incr.Val()
    if count > int64(limit) {
        return false, nil
    }

    return true, nil
}
```

### 4.2 一致性哈希

**一致性哈希限流**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: EnvoyFilter
metadata:
  name: consistent-hash-rate-limit
spec:
  configPatches:
    - applyTo: HTTP_FILTER
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.ratelimit
          typed_config:
            "@type": type.googleapis.com/envoy.extensions.filters.http.ratelimit.v3.RateLimit
            domain: api_rate_limit
            rate_limit_service:
              grpc_service:
                envoy_grpc:
                  cluster_name: rate_limit_service
```

---

## 5 限流响应

### 5.1 HTTP 状态码

**限流响应**：

```yaml
apiVersion: api.example.com/v1
kind: RateLimitResponse
metadata:
  name: rate-limit-response
spec:
  statusCode: 429
  headers:
    Retry-After: "60"
    X-RateLimit-Limit: "1000"
    X-RateLimit-Remaining: "0"
    X-RateLimit-Reset: "1636272000"
  body:
    error: "Too Many Requests"
    message: "Rate limit exceeded"
```

### 5.2 Rate Limit Headers

**Rate Limit Headers 实现**：

```go
func AddRateLimitHeaders(w http.ResponseWriter, limit, remaining int, resetTime time.Time) {
    w.Header().Set("X-RateLimit-Limit", strconv.Itoa(limit))
    w.Header().Set("X-RateLimit-Remaining", strconv.Itoa(remaining))
    w.Header().Set("X-RateLimit-Reset", strconv.FormatInt(resetTime.Unix(), 10))

    if remaining == 0 {
        retryAfter := int(time.Until(resetTime).Seconds())
        w.Header().Set("Retry-After", strconv.Itoa(retryAfter))
        w.WriteHeader(http.StatusTooManyRequests)
    }
}
```

---

## 6 动态限流

### 6.1 自适应限流

**自适应限流配置**：

```yaml
apiVersion: api.example.com/v1
kind: AdaptiveRateLimit
metadata:
  name: adaptive-rate-limit
spec:
  algorithm: token-bucket
  initialRate: 1000
  minRate: 100
  maxRate: 10000
  adjustmentFactor: 0.1
  metrics:
    - cpu-usage
    - memory-usage
    - request-latency
  thresholds:
    cpu-usage: 80
    memory-usage: 80
    request-latency: "500ms"
```

### 6.2 熔断器集成

**熔断器限流**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: circuit-breaker-rate-limit
spec:
  host: payment-service
  trafficPolicy:
    outlierDetection:
      consecutiveErrors: 5
      interval: "30s"
      baseEjectionTime: "30s"
      maxEjectionPercent: 50
    connectionPool:
      http:
        http1MaxPendingRequests: 100
        http2MaxRequests: 100
```

---

## 7 相关文档

- **[API 安全规范](../11-api-security/api-security.md)** - 限流安全
- **[API 性能优化](../14-api-performance/api-performance.md)** - 限流性能优化
- **[API 网关](../17-api-gateway/api-gateway.md)** - 网关限流
- **[最佳实践](../08-best-practices/best-practices.md)** - 限流最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
