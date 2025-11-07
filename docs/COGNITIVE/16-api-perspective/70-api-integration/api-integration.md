# API 集成规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 集成架构](#11-集成架构)
- [2. 集成模式](#2-集成模式)
  - [2.1 点对点集成](#21-点对点集成)
  - [2.2 中心化集成](#22-中心化集成)
  - [2.3 事件驱动集成](#23-事件驱动集成)
- [3. 集成协议](#3-集成协议)
  - [3.1 REST API](#31-rest-api)
  - [3.2 gRPC](#32-grpc)
  - [3.3 GraphQL](#33-graphql)
- [4. 数据转换](#4-数据转换)
  - [4.1 数据映射](#41-数据映射)
  - [4.2 数据验证](#42-数据验证)
  - [4.3 数据转换](#43-数据转换)
- [5. 错误处理](#5-错误处理)
  - [5.1 重试策略](#51-重试策略)
  - [5.2 降级策略](#52-降级策略)
- [6. 集成测试](#6-集成测试)
  - [6.1 集成测试策略](#61-集成测试策略)
  - [6.2 集成测试工具](#62-集成测试工具)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 集成规范定义了 API 在集成场景下的设计和实现，从集成模式到集成协议，从数据转
换到错误处理。

### 1.1 集成架构

```text
API A（API A）
  ↓
集成层（Integration Layer）
  ↓
API B（API B）
```

---

## 2. 集成模式

### 2.1 点对点集成

**点对点集成配置**：

```yaml
apiVersion: api.example.com/v1
kind: PointToPointIntegration
metadata:
  name: payment-order-integration
spec:
  source:
    api: "order-service"
    endpoint: "/api/v1/orders"
  target:
    api: "payment-service"
    endpoint: "/api/v1/payments"
  mapping:
    - source: "order.id"
      target: "order_id"
    - source: "order.amount"
      target: "amount"
```

**点对点集成实现**：

```go
package main

import (
    "net/http"
)

func IntegrateOrderToPayment(order Order) error {
    payment := Payment{
        OrderID: order.ID,
        Amount:  order.Amount,
        Status:  "pending",
    }

    resp, err := http.Post("https://payment-service/api/v1/payments", "application/json", payment)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusCreated {
        return fmt.Errorf("payment creation failed: %d", resp.StatusCode)
    }

    return nil
}
```

### 2.2 中心化集成

**中心化集成配置**：

```yaml
apiVersion: api.example.com/v1
kind: CentralizedIntegration
metadata:
  name: api-hub-integration
spec:
  hub:
    endpoint: "https://api-hub.example.com"
    protocol: "rest"
  apis:
    - name: "order-service"
      endpoint: "https://order-service/api/v1"
    - name: "payment-service"
      endpoint: "https://payment-service/api/v1"
    - name: "inventory-service"
      endpoint: "https://inventory-service/api/v1"
```

### 2.3 事件驱动集成

**事件驱动集成配置**：

```yaml
apiVersion: api.example.com/v1
kind: EventDrivenIntegration
metadata:
  name: payment-event-integration
spec:
  eventBus: "kafka"
  topics:
    - topic: "order.created"
      consumers:
        - service: "payment-service"
          handler: "handleOrderCreated"
    - topic: "payment.completed"
      consumers:
        - service: "order-service"
          handler: "handlePaymentCompleted"
```

**事件驱动集成实现**：

```go
package main

import (
    "github.com/segmentio/kafka-go"
)

func HandleOrderCreated(event OrderCreatedEvent) error {
    payment := Payment{
        OrderID: event.OrderID,
        Amount:  event.Amount,
    }

    if err := createPayment(payment); err != nil {
        return err
    }

    // 发布支付创建事件
    publishEvent("payment.created", PaymentCreatedEvent{
        PaymentID: payment.ID,
        OrderID:   event.OrderID,
    })

    return nil
}
```

---

## 3. 集成协议

### 3.1 REST API

**REST API 集成配置**：

```yaml
apiVersion: api.example.com/v1
kind: RESTAPIIntegration
metadata:
  name: payment-rest-integration
spec:
  baseURL: "https://api.payment.com/v1"
  authentication:
    type: "bearer"
    token: "${PAYMENT_API_TOKEN}"
  endpoints:
    - path: "/payments"
      method: "POST"
    - path: "/payments/{id}"
      method: "GET"
```

### 3.2 gRPC

**gRPC 集成配置**：

```yaml
apiVersion: api.example.com/v1
kind: GRPCIntegration
metadata:
  name: payment-grpc-integration
spec:
  endpoint: "payment-service:50051"
  protoFile: "payment.proto"
  services:
    - name: "PaymentService"
      methods:
        - name: "CreatePayment"
        - name: "GetPayment"
```

**gRPC 集成实现**：

```go
package main

import (
    "google.golang.org/grpc"
    pb "example.com/payment/proto"
)

func CreateGRPCClient() (pb.PaymentServiceClient, error) {
    conn, err := grpc.Dial("payment-service:50051", grpc.WithInsecure())
    if err != nil {
        return nil, err
    }

    return pb.NewPaymentServiceClient(conn), nil
}

func CreatePaymentViaGRPC(client pb.PaymentServiceClient, req *pb.CreatePaymentRequest) (*pb.PaymentResponse, error) {
    return client.CreatePayment(context.Background(), req)
}
```

### 3.3 GraphQL

**GraphQL 集成配置**：

```yaml
apiVersion: api.example.com/v1
kind: GraphQLIntegration
metadata:
  name: payment-graphql-integration
spec:
  endpoint: "https://api.payment.com/graphql"
  schema: "payment.graphql"
  queries:
    - name: "getPayment"
      query: |
        query GetPayment($id: ID!) {
          payment(id: $id) {
            id
            amount
            status
          }
        }
```

---

## 4. 数据转换

### 4.1 数据映射

**数据映射配置**：

```yaml
apiVersion: api.example.com/v1
kind: DataMapping
metadata:
  name: order-payment-mapping
spec:
  source:
    format: "json"
    schema: "order-schema.json"
  target:
    format: "json"
    schema: "payment-schema.json"
  mappings:
    - source: "order.id"
      target: "order_id"
      transform: "string"
    - source: "order.total"
      target: "amount"
      transform: "multiply(100)" # Convert to cents
```

### 4.2 数据验证

**数据验证实现**：

```go
package main

import (
    "github.com/go-playground/validator/v10"
)

type PaymentRequest struct {
    OrderID string `validate:"required,uuid"`
    Amount  int64  `validate:"required,min=1"`
    Currency string `validate:"required,len=3"`
}

func ValidatePaymentRequest(req PaymentRequest) error {
    validate := validator.New()
    return validate.Struct(req)
}
```

### 4.3 数据转换

**数据转换实现**：

```go
package main

func TransformOrderToPayment(order Order) Payment {
    return Payment{
        OrderID:  order.ID,
        Amount:   order.Total * 100, // Convert to cents
        Currency: order.Currency,
        Status:   "pending",
    }
}

func TransformPaymentToOrder(payment Payment) Order {
    return Order{
        ID:       payment.OrderID,
        Total:    payment.Amount / 100, // Convert from cents
        Currency: payment.Currency,
        Status:   mapPaymentStatusToOrderStatus(payment.Status),
    }
}
```

---

## 5. 错误处理

### 5.1 重试策略

**重试策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: RetryPolicy
metadata:
  name: payment-api-retry
spec:
  maxRetries: 3
  backoff:
    strategy: "exponential"
    initialDelay: "1s"
    maxDelay: "10s"
    multiplier: 2
  retryableErrors:
    - "500"
    - "502"
    - "503"
    - "504"
  nonRetryableErrors:
    - "400"
    - "401"
    - "403"
    - "404"
```

**重试策略实现**：

```go
package main

import (
    "time"
    "math"
)

func RetryWithBackoff(fn func() error, maxRetries int) error {
    var err error
    delay := time.Second

    for i := 0; i < maxRetries; i++ {
        err = fn()
        if err == nil {
            return nil
        }

        if i < maxRetries-1 {
            time.Sleep(delay)
            delay = time.Duration(float64(delay) * 2)
            if delay > 10*time.Second {
                delay = 10 * time.Second
            }
        }
    }

    return err
}
```

### 5.2 降级策略

**降级策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: FallbackPolicy
metadata:
  name: payment-api-fallback
spec:
  fallback:
    - condition: "error_rate > 0.5"
      action: "use_cache"
    - condition: "latency > 1000ms"
      action: "use_cache"
    - condition: "service_unavailable"
      action: "use_queue"
```

**降级策略实现**：

```go
package main

func CreatePaymentWithFallback(order Order) error {
    // 尝试直接调用
    err := createPayment(order)
    if err == nil {
        return nil
    }

    // 降级到缓存
    if shouldUseCache(err) {
        return createPaymentViaCache(order)
    }

    // 降级到队列
    if shouldUseQueue(err) {
        return enqueuePayment(order)
    }

    return err
}
```

---

## 6. 集成测试

### 6.1 集成测试策略

**集成测试配置**：

```yaml
apiVersion: api.example.com/v1
kind: IntegrationTest
metadata:
  name: payment-order-integration-test
spec:
  testCases:
    - name: "create_payment_from_order"
      steps:
        - step: "create_order"
          endpoint: "/api/v1/orders"
          method: "POST"
        - step: "verify_payment_created"
          endpoint: "/api/v1/payments"
          method: "GET"
          assertion: "payment.order_id == order.id"
```

### 6.2 集成测试工具

**集成测试实现**：

```go
package main

import (
    "testing"
    "net/http"
)

func TestOrderPaymentIntegration(t *testing.T) {
    // 创建订单
    order := createTestOrder(t)

    // 等待集成处理
    time.Sleep(1 * time.Second)

    // 验证支付创建
    payment := getPaymentByOrderID(order.ID)
    if payment == nil {
        t.Fatal("Payment not created")
    }

    if payment.OrderID != order.ID {
        t.Errorf("Expected order ID %s, got %s", order.ID, payment.OrderID)
    }
}
```

---

## 7. 相关文档

- **[API 生态系统规范](../26-api-ecosystem/api-ecosystem.md)** - API 生态系统
- **[API 微服务规范](../36-api-microservices/api-microservices.md)** - 微服务集
  成
- **[API 事件驱动规范](../35-api-event-driven/api-event-driven.md)** - 事件驱动
  集成
- **[最佳实践](../08-best-practices/best-practices.md)** - 集成最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
