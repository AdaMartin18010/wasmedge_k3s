# API 缓存规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 缓存架构](#11-缓存架构)
  - [1.2 API 缓存在 API 规范中的位置](#12-api-缓存在-api-规范中的位置)
- [2. 缓存策略](#2-缓存策略)
  - [2.1 HTTP 缓存](#21-http-缓存)
  - [2.2 应用层缓存](#22-应用层缓存)
  - [2.3 分布式缓存](#23-分布式缓存)
- [3. 缓存键设计](#3-缓存键设计)
  - [3.1 键命名规范](#31-键命名规范)
  - [3.2 键版本管理](#32-键版本管理)
- [4. 缓存失效](#4-缓存失效)
  - [4.1 TTL 策略](#41-ttl-策略)
  - [4.2 主动失效](#42-主动失效)
  - [4.3 失效模式](#43-失效模式)
- [5. 缓存预热](#5-缓存预热)
  - [5.1 预热策略](#51-预热策略)
  - [5.2 预热时机](#52-预热时机)
- [6. 缓存一致性](#6-缓存一致性)
  - [6.1 一致性模型](#61-一致性模型)
  - [6.2 缓存更新策略](#62-缓存更新策略)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 缓存规范定义了 API 在缓存场景下的设计和实现，从缓存策略到缓存键设计，从缓存
失效到缓存一致性。本文档基于形式化方法，提供严格的数学定义和推理论证，分析 API
缓存的理论基础和实践方法。

**参考标准**：

- [HTTP Caching](https://httpwg.org/specs/rfc7234.html) - HTTP 缓存规范
- [Cache-Control Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control) -
  Cache-Control 头
- [Redis Caching](https://redis.io/docs/manual/patterns/cache/) - Redis 缓存模式
- [Cache Invalidation](https://martinfowler.com/bliki/CacheInvalidation.html) -
  缓存失效策略
- [CDN Caching](https://www.cloudflare.com/learning/cdn/what-is-caching/) - CDN
  缓存

### 1.1 缓存架构

```text
API 请求（API Request）
  ↓
缓存层（Cache Layer）
  ↓
缓存存储（Cache Store）
  ↓
数据源（Data Source）
```

### 1.2 API 缓存在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API 缓存主要涉及 Observability 和 Performance 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
                                ↑
                    Caching (implementation)
```

API 缓存在 API 规范中提供：

- **性能优化**：减少 API 响应时间
- **资源节约**：减少后端负载
- **可用性提升**：缓存失效时的降级方案
- **一致性保证**：缓存一致性策略

---

## 2. 缓存策略

### 2.1 HTTP 缓存

**HTTP 缓存头配置**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-cache
spec:
  paths:
    /api/v1/payments/{id}:
      get:
        responses:
          "200":
            headers:
              Cache-Control: "public, max-age=3600"
              ETag: "{{payment.etag}}"
              Last-Modified: "{{payment.updated_at}}"
```

**Go HTTP 缓存实现**：

```go
package main

import (
    "net/http"
    "time"
    "crypto/md5"
    "encoding/hex"
)

func CacheMiddleware(handler http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // 检查 ETag
        if match := r.Header.Get("If-None-Match"); match != "" {
            etag := generateETag(r.URL.Path)
            if match == etag {
                w.WriteHeader(http.StatusNotModified)
                return
            }
        }

        // 设置缓存头
        w.Header().Set("Cache-Control", "public, max-age=3600")
        w.Header().Set("ETag", generateETag(r.URL.Path))
        w.Header().Set("Last-Modified", time.Now().UTC().Format(http.TimeFormat))

        handler(w, r)
    }
}

func generateETag(path string) string {
    hash := md5.Sum([]byte(path))
    return hex.EncodeToString(hash[:])
}
```

### 2.2 应用层缓存

**Redis 缓存实现**：

```go
package main

import (
    "github.com/go-redis/redis/v8"
    "context"
    "encoding/json"
    "time"
)

type CacheService struct {
    client *redis.Client
}

func (cs *CacheService) Get(ctx context.Context, key string, dest interface{}) error {
    val, err := cs.client.Get(ctx, key).Result()
    if err == redis.Nil {
        return ErrCacheMiss
    }
    if err != nil {
        return err
    }

    return json.Unmarshal([]byte(val), dest)
}

func (cs *CacheService) Set(ctx context.Context, key string, value interface{}, ttl time.Duration) error {
    data, err := json.Marshal(value)
    if err != nil {
        return err
    }

    return cs.client.Set(ctx, key, data, ttl).Err()
}
```

### 2.3 分布式缓存

**分布式缓存配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cache-config
data:
  cache.yaml: |
    type: redis-cluster
    endpoints:
      - redis-cluster-0:6379
      - redis-cluster-1:6379
      - redis-cluster-2:6379
    ttl: 3600s
    maxMemory: 2GB
```

---

## 3. 缓存键设计

### 3.1 键命名规范

**缓存键命名规范**：

```yaml
apiVersion: api.example.com/v1
kind: CacheKeyPolicy
metadata:
  name: payment-cache-keys
spec:
  pattern: "{service}:{resource}:{id}:{version}"
  examples:
    - key: "payment:payment:pay_123:v1"
      description: Payment resource cache key
    - key: "payment:order:order_456:v1"
      description: Order resource cache key
    - key: "payment:user:user_789:v1"
      description: User resource cache key
```

**缓存键生成**：

```go
func GenerateCacheKey(service, resource, id, version string) string {
    return fmt.Sprintf("%s:%s:%s:%s", service, resource, id, version)
}

func GenerateCacheKeyWithParams(service, resource string, params map[string]string) string {
    parts := []string{service, resource}
    for k, v := range params {
        parts = append(parts, fmt.Sprintf("%s:%s", k, v))
    }
    return strings.Join(parts, ":")
}
```

### 3.2 键版本管理

**缓存键版本管理**：

```yaml
apiVersion: api.example.com/v1
kind: CacheVersion
metadata:
  name: payment-cache-version
spec:
  currentVersion: "v2"
  versions:
    - version: "v1"
      deprecated: true
      sunsetDate: "2025-12-31"
    - version: "v2"
      active: true
      migrationStrategy: "gradual"
```

---

## 4. 缓存失效

### 4.1 TTL 策略

**TTL 配置**：

```yaml
apiVersion: api.example.com/v1
kind: CacheTTLPolicy
metadata:
  name: payment-cache-ttl
spec:
  defaultTTL: "1h"
  resources:
    - resource: payment
      ttl: "30m"
    - resource: order
      ttl: "1h"
    - resource: user
      ttl: "24h"
```

### 4.2 主动失效

**主动失效 API**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: cache-invalidation-api
spec:
  paths:
    /api/v1/cache/invalidate:
      post:
        summary: Invalidate cache
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  pattern:
                    type: string
                  keys:
                    type: array
                    items:
                      type: string
```

**缓存失效实现**：

```go
func (cs *CacheService) Invalidate(ctx context.Context, pattern string) error {
    keys, err := cs.client.Keys(ctx, pattern).Result()
    if err != nil {
        return err
    }

    if len(keys) > 0 {
        return cs.client.Del(ctx, keys...).Err()
    }

    return nil
}
```

### 4.3 失效模式

**失效模式配置**：

```yaml
apiVersion: api.example.com/v1
kind: CacheInvalidationPolicy
metadata:
  name: payment-cache-invalidation
spec:
  strategies:
    - type: write-through
      description: "Write to cache and database simultaneously"
    - type: write-behind
      description: "Write to cache first, then database"
    - type: cache-aside
      description: "Application manages cache"
```

---

## 5. 缓存预热

### 5.1 预热策略

**缓存预热配置**：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: cache-warmup
spec:
  template:
    spec:
      containers:
        - name: cache-warmup
          image: cache-warmup:latest
          command:
            - /bin/sh
            - -c
            - |
              # 预热热门数据
              curl -X POST http://api/v1/cache/warmup \
                -H "Content-Type: application/json" \
                -d '{"resources": ["payment", "order"], "limit": 1000}'
```

### 5.2 预热时机

**预热时机配置**：

```yaml
apiVersion: api.example.com/v1
kind: CacheWarmupPolicy
metadata:
  name: payment-cache-warmup
spec:
  triggers:
    - type: startup
      enabled: true
    - type: schedule
      schedule: "0 2 * * *" # 每天凌晨2点
    - type: event
      events:
        - deployment.created
        - cache.flush
```

---

## 6. 缓存一致性

### 6.1 一致性模型

**一致性模型配置**：

```yaml
apiVersion: api.example.com/v1
kind: CacheConsistencyPolicy
metadata:
  name: payment-cache-consistency
spec:
  model: eventual-consistency
  syncStrategy: pub-sub
  syncChannels:
    - payment.created
    - payment.updated
    - payment.deleted
```

### 6.2 缓存更新策略

**缓存更新策略**：

```go
type CacheUpdateStrategy interface {
    Update(ctx context.Context, key string, value interface{}) error
}

type WriteThroughStrategy struct {
    cache    CacheService
    database DatabaseService
}

func (wts *WriteThroughStrategy) Update(ctx context.Context, key string, value interface{}) error {
    // 同时更新缓存和数据库
    if err := wts.database.Update(ctx, key, value); err != nil {
        return err
    }

    return wts.cache.Set(ctx, key, value, time.Hour)
}

type WriteBehindStrategy struct {
    cache    CacheService
    database DatabaseService
    queue    MessageQueue
}

func (wbs *WriteBehindStrategy) Update(ctx context.Context, key string, value interface{}) error {
    // 先更新缓存
    if err := wbs.cache.Set(ctx, key, value, time.Hour); err != nil {
        return err
    }

    // 异步更新数据库
    return wbs.queue.Publish(ctx, "cache.update", map[string]interface{}{
        "key":   key,
        "value": value,
    })
}
```

---

## 7. 相关文档

- **[API 性能优化](../14-api-performance/api-performance.md)** - 缓存性能优化
- **[API 网关](../17-api-gateway/api-gateway.md)** - 网关缓存
- **[API 边缘计算](../34-api-edge-computing/api-edge-computing.md)** - 边缘缓存
- **[最佳实践](../00-foundation/05-best-practices.md)** - 缓存最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
