# API Webhook 规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 Webhook API 架构](#11-webhook-api-架构)
  - [1.2 API Webhook 在 API 规范中的位置](#12-api-webhook-在-api-规范中的位置)
- [2. Webhook 注册](#2-webhook-注册)
  - [2.1 注册 API](#21-注册-api)
  - [2.2 订阅管理](#22-订阅管理)
- [3. 事件触发](#3-事件触发)
  - [3.1 事件类型](#31-事件类型)
  - [3.2 事件负载](#32-事件负载)
- [4. 签名和验证](#4-签名和验证)
  - [4.1 HMAC 签名](#41-hmac-签名)
  - [4.2 签名验证](#42-签名验证)
- [5. 重试机制](#5-重试机制)
  - [5.1 重试策略](#51-重试策略)
  - [5.2 退避算法](#52-退避算法)
- [6. 安全性](#6-安全性)
  - [6.1 TLS 加密](#61-tls-加密)
  - [6.2 IP 白名单](#62-ip-白名单)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API Webhook 规范定义了 API 在 Webhook 架构下的设计和实现，从 Webhook 注册到事件
触发，从签名验证到重试机制。本文档基于形式化方法，提供严格的数学定义和推理论证，
分析 API Webhook 的理论基础和实践方法。

**参考标准**：

- [Webhook Best Practices](https://webhooks.fyi/) - Webhook 最佳实践
- [GitHub Webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks) -
  GitHub Webhook 规范
- [Stripe Webhooks](https://stripe.com/docs/webhooks) - Stripe Webhook 规范
- [Webhook Security](https://www.ietf.org/archive/id/draft-ietf-httpapi-message-signatures-12.html) -
  Webhook 安全签名
- [Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html) -
  事件驱动架构

### 1.1 Webhook API 架构

```text
事件源（Event Source）
  ↓
Webhook 调度器（Webhook Dispatcher）
  ↓
签名和加密（Signing & Encryption）
  ↓
目标端点（Target Endpoint）
```

### 1.2 API Webhook 在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API Webhook 主要涉及 Governance 和 Security 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
                    ↑                            ↑
            Webhook (implementation)
```

API Webhook 在 API 规范中提供：

- **事件通知**：Webhook 事件触发和通知
- **签名验证**：HMAC 签名和验证机制
- **重试机制**：失败重试和退避算法
- **安全传输**：TLS 加密和 IP 白名单

---

## 2. Webhook 注册

### 2.1 注册 API

**Webhook 注册端点**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: webhook-registration-api
spec:
  paths:
    /api/v1/webhooks:
      post:
        summary: Register webhook
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  url:
                    type: string
                    format: uri
                  events:
                    type: array
                    items:
                      type: string
                  secret:
                    type: string
        responses:
          "201":
            description: Webhook registered
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    webhook_id:
                      type: string
                    status:
                      type: string
```

**Webhook CRD**：

```yaml
apiVersion: webhook.example.com/v1
kind: Webhook
metadata:
  name: payment-webhook
spec:
  url: https://example.com/webhooks/payment
  events:
    - payment.created
    - payment.updated
    - payment.completed
  secret: webhook-secret-key
  active: true
  retryPolicy:
    maxRetries: 3
    backoffStrategy: exponential
    initialDelay: "1s"
```

### 2.2 订阅管理

**订阅管理 API**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: webhook-subscription-api
spec:
  paths:
    /api/v1/webhooks/{webhook_id}:
      get:
        summary: Get webhook
      put:
        summary: Update webhook
      delete:
        summary: Delete webhook
    /api/v1/webhooks/{webhook_id}/events:
      get:
        summary: List webhook events
    /api/v1/webhooks/{webhook_id}/deliveries:
      get:
        summary: List webhook deliveries
```

---

## 3. 事件触发

### 3.1 事件类型

**事件类型定义**：

```yaml
apiVersion: webhook.example.com/v1
kind: WebhookEventType
metadata:
  name: payment-events
spec:
  types:
    - name: payment.created
      description: Payment created
      schema:
        type: object
        properties:
          payment_id:
            type: string
          order_id:
            type: string
          amount:
            type: integer
    - name: payment.updated
      description: Payment updated
      schema:
        type: object
        properties:
          payment_id:
            type: string
          status:
            type: string
    - name: payment.completed
      description: Payment completed
      schema:
        type: object
        properties:
          payment_id:
            type: string
          completed_at:
            type: string
            format: date-time
```

### 3.2 事件负载

**事件负载格式**：

```json
{
  "id": "evt_1234567890",
  "type": "payment.created",
  "created": "2025-11-07T10:00:00Z",
  "data": {
    "object": "payment",
    "id": "pay_123",
    "order_id": "order_456",
    "amount": 10000,
    "status": "completed"
  },
  "livemode": true,
  "pending_webhooks": 1,
  "request": {
    "id": "req_789",
    "idempotency_key": "idempotency_key_abc"
  }
}
```

---

## 4. 签名和验证

### 4.1 HMAC 签名

**HMAC 签名生成**：

```go
package main

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
    "fmt"
    "time"
)

func SignWebhook(secret string, payload []byte, timestamp int64) string {
    message := fmt.Sprintf("%d.%s", timestamp, string(payload))
    mac := hmac.New(sha256.New, []byte(secret))
    mac.Write([]byte(message))
    signature := hex.EncodeToString(mac.Sum(nil))
    return fmt.Sprintf("t=%d,v1=%s", timestamp, signature)
}
```

### 4.2 签名验证

**签名验证实现**：

```go
func VerifyWebhook(secret string, payload []byte, signature string) bool {
    // 解析签名
    parts := strings.Split(signature, ",")
    var timestamp int64
    var sig string

    for _, part := range parts {
        if strings.HasPrefix(part, "t=") {
            timestamp, _ = strconv.ParseInt(strings.TrimPrefix(part, "t="), 10, 64)
        }
        if strings.HasPrefix(part, "v1=") {
            sig = strings.TrimPrefix(part, "v1=")
        }
    }

    // 验证时间戳（防止重放攻击）
    if time.Now().Unix()-timestamp > 300 {
        return false
    }

    // 验证签名
    expectedSig := SignWebhook(secret, payload, timestamp)
    return hmac.Equal([]byte(sig), []byte(strings.Split(expectedSig, ",")[1][3:]))
}
```

---

## 5. 重试机制

### 5.1 重试策略

**重试策略配置**：

```yaml
apiVersion: webhook.example.com/v1
kind: WebhookRetryPolicy
metadata:
  name: payment-webhook-retry
spec:
  maxRetries: 5
  backoffStrategy: exponential
  initialDelay: "1s"
  maxDelay: "60s"
  retryableStatusCodes:
    - 408
    - 429
    - 500
    - 502
    - 503
    - 504
  nonRetryableStatusCodes:
    - 400
    - 401
    - 403
    - 404
```

### 5.2 退避算法

**指数退避实现**：

```go
func CalculateBackoff(retryCount int, initialDelay time.Duration, maxDelay time.Duration) time.Duration {
    delay := initialDelay * time.Duration(1<<uint(retryCount))
    if delay > maxDelay {
        delay = maxDelay
    }
    return delay
}
```

---

## 6. 安全性

### 6.1 TLS 加密

**TLS 配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: webhook-service
spec:
  hosts:
    - webhook.example.com
  tls:
    - match:
        - port: 443
          sniHosts:
            - webhook.example.com
      route:
        - destination:
            host: webhook-backend
            port:
              number: 8080
```

### 6.2 IP 白名单

**IP 白名单配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: webhook-ip-whitelist
spec:
  selector:
    matchLabels:
      app: webhook-receiver
  action: ALLOW
  rules:
    - from:
        - source:
            ipBlocks:
              - "192.168.1.0/24"
              - "10.0.0.0/8"
```

---

## 7. 相关文档

- **[API 事件驱动架构](../09-architecture/01-api-event-driven.md)** - Webhook
  事件
- **[API 安全规范](../05-security/01-api-security.md)** - Webhook 安全
- **[API 性能优化](../07-performance/01-api-performance.md)** - Webhook 性能优
  化
- **[最佳实践](../00-foundation/05-best-practices.md)** - Webhook 最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
