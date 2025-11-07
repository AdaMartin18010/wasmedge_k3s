# API 契约测试规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 契约测试架构](#11-契约测试架构)
- [2. 契约定义](#2-契约定义)
  - [2.1 OpenAPI 契约](#21-openapi-契约)
  - [2.2 gRPC 契约](#22-grpc-契约)
  - [2.3 GraphQL 契约](#23-graphql-契约)
- [3. 消费者驱动契约](#3-消费者驱动契约)
  - [3.1 Pact 契约](#31-pact-契约)
  - [3.2 Spring Cloud Contract](#32-spring-cloud-contract)
- [4. 契约验证](#4-契约验证)
  - [4.1 提供者验证](#41-提供者验证)
  - [4.2 消费者验证](#42-消费者验证)
- [5. 契约版本管理](#5-契约版本管理)
  - [5.1 版本兼容性](#51-版本兼容性)
  - [5.2 版本演进](#52-版本演进)
- [6. 契约测试工具](#6-契约测试工具)
  - [6.1 Pact](#61-pact)
  - [6.2 Dredd](#62-dredd)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 契约测试规范定义了 API 在契约测试场景下的设计和实现，从契约定义到契约验证，
从消费者驱动契约到契约版本管理。

### 1.1 契约测试架构

```text
API 契约（API Contract）
  ↓
契约定义（Contract Definition）
  ↓
契约验证（Contract Verification）
  ↓
契约测试（Contract Testing）
```

---

## 2. 契约定义

### 2.1 OpenAPI 契约

**OpenAPI 契约定义**：

```yaml
openapi: 3.1.0
info:
  title: Payment Service API
  version: 1.0.0
paths:
  /api/v1/payments:
    post:
      summary: Create payment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - order_id
                - amount
              properties:
                order_id:
                  type: string
                  pattern: "^order_[a-zA-Z0-9]+$"
                amount:
                  type: integer
                  minimum: 1
                  maximum: 1000000
      responses:
        "201":
          description: Payment created
          content:
            application/json:
              schema:
                type: object
                properties:
                  payment_id:
                    type: string
                  status:
                    type: string
                    enum: [pending, processing, completed, failed]
```

### 2.2 gRPC 契约

**gRPC 契约定义**：

```protobuf
syntax = "proto3";

package payment.v1;

service PaymentService {
  rpc CreatePayment(CreatePaymentRequest) returns (CreatePaymentResponse);
}

message CreatePaymentRequest {
  string order_id = 1;
  int64 amount = 2;
  string currency = 3;
}

message CreatePaymentResponse {
  string payment_id = 1;
  PaymentStatus status = 2;
}

enum PaymentStatus {
  PAYMENT_STATUS_UNSPECIFIED = 0;
  PAYMENT_STATUS_PENDING = 1;
  PAYMENT_STATUS_PROCESSING = 2;
  PAYMENT_STATUS_COMPLETED = 3;
  PAYMENT_STATUS_FAILED = 4;
}
```

### 2.3 GraphQL 契约

**GraphQL 契约定义**：

```graphql
type Payment {
  id: ID!
  orderId: String!
  amount: Int!
  status: PaymentStatus!
  createdAt: DateTime!
}

enum PaymentStatus {
  PENDING
  PROCESSING
  COMPLETED
  FAILED
}

type Mutation {
  createPayment(input: CreatePaymentInput!): Payment!
}

input CreatePaymentInput {
  orderId: String!
  amount: Int!
  currency: String!
}
```

---

## 3. 消费者驱动契约

### 3.1 Pact 契约

**Pact 契约定义**：

```json
{
  "consumer": {
    "name": "order-service"
  },
  "provider": {
    "name": "payment-service"
  },
  "interactions": [
    {
      "description": "a request to create a payment",
      "request": {
        "method": "POST",
        "path": "/api/v1/payments",
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "order_id": "order_123",
          "amount": 10000
        }
      },
      "response": {
        "status": 201,
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "payment_id": "pay_456",
          "status": "pending"
        }
      }
    }
  ],
  "metadata": {
    "pactSpecification": {
      "version": "3.0.0"
    }
  }
}
```

**Pact 测试实现**：

```go
package main

import (
    "github.com/pact-foundation/pact-go/v2/consumer"
    "github.com/pact-foundation/pact-go/v2/matchers"
)

func TestPaymentServiceContract(t *testing.T) {
    pact, err := consumer.NewV3Pact(consumer.MockHTTPProvider{
        Consumer: "order-service",
        Provider: "payment-service",
    })
    if err != nil {
        t.Fatal(err)
    }

    pact.
        AddInteraction().
        Given("order exists").
        UponReceiving("a request to create a payment").
        WithRequest("POST", "/api/v1/payments", func(b *consumer.Request) {
            b.Header("Content-Type", "application/json")
            b.JSONBody(map[string]interface{}{
                "order_id": matchers.String("order_123"),
                "amount":   matchers.Integer(10000),
            })
        }).
        WillRespondWith(201, func(b *consumer.Response) {
            b.Header("Content-Type", "application/json")
            b.JSONBody(map[string]interface{}{
                "payment_id": matchers.String("pay_456"),
                "status":     matchers.String("pending"),
            })
        })

    err = pact.ExecuteTest(func(config consumer.MockServerConfig) error {
        // 执行实际测试
        return testPaymentService(config.URL)
    })
    if err != nil {
        t.Fatal(err)
    }
}
```

### 3.2 Spring Cloud Contract

**Spring Cloud Contract 定义**：

```groovy
package contracts

import org.springframework.cloud.contract.spec.Contract

Contract.make {
    description "should create a payment"
    request {
        method POST()
        url "/api/v1/payments"
        headers {
            contentType(applicationJson())
        }
        body([
            order_id: "order_123",
            amount: 10000
        ])
    }
    response {
        status CREATED()
        headers {
            contentType(applicationJson())
        }
        body([
            payment_id: "pay_456",
            status: "pending"
        ])
    }
}
```

---

## 4. 契约验证

### 4.1 提供者验证

**提供者验证配置**：

```yaml
apiVersion: api.example.com/v1
kind: ContractVerification
metadata:
  name: payment-service-verification
spec:
  provider: payment-service
  contracts:
    - consumer: order-service
      contract: order-service-payment-service.json
  verification:
    type: pact
    providerVersion: "1.0.0"
```

**提供者验证实现**：

```go
package main

import (
    "github.com/pact-foundation/pact-go/v2/provider"
)

func VerifyProvider() error {
    verifier := provider.NewVerifier()

    return verifier.VerifyProvider(provider.VerifyRequest{
        ProviderBaseURL: "http://localhost:8080",
        PactFiles: []string{
            "./pacts/order-service-payment-service.json",
        },
        ProviderVersion: "1.0.0",
        PublishVerificationResults: true,
        BrokerURL: "http://pact-broker:9292",
    })
}
```

### 4.2 消费者验证

**消费者验证实现**：

```go
package main

import (
    "github.com/pact-foundation/pact-go/v2/consumer"
)

func VerifyConsumer() error {
    pact, err := consumer.NewV3Pact(consumer.MockHTTPProvider{
        Consumer: "order-service",
        Provider: "payment-service",
    })
    if err != nil {
        return err
    }

    // 定义契约
    pact.AddInteraction().
        Given("order exists").
        UponReceiving("a request to create a payment").
        WithRequest("POST", "/api/v1/payments", func(b *consumer.Request) {
            b.Header("Content-Type", "application/json")
            b.JSONBody(map[string]interface{}{
                "order_id": "order_123",
                "amount":   10000,
            })
        }).
        WillRespondWith(201, func(b *consumer.Response) {
            b.Header("Content-Type", "application/json")
            b.JSONBody(map[string]interface{}{
                "payment_id": "pay_456",
                "status":     "pending",
            })
        })

    // 验证契约
    return pact.ExecuteTest(func(config consumer.MockServerConfig) error {
        return testPaymentService(config.URL)
    })
}
```

---

## 5. 契约版本管理

### 5.1 版本兼容性

**版本兼容性检查**：

```yaml
apiVersion: api.example.com/v1
kind: ContractCompatibility
metadata:
  name: payment-contract-compatibility
spec:
  currentVersion: "1.0.0"
  compatibility:
    - version: "1.0.0"
      compatible: true
      breakingChanges: []
    - version: "1.1.0"
      compatible: true
      breakingChanges: []
    - version: "2.0.0"
      compatible: false
      breakingChanges:
        - "Removed field: old_field"
        - "Changed type: amount (int -> string)"
```

### 5.2 版本演进

**版本演进策略**：

```yaml
apiVersion: api.example.com/v1
kind: ContractEvolution
metadata:
  name: payment-contract-evolution
spec:
  strategy: additive
  rules:
    - type: add_field
      allowed: true
      requireDefault: false
    - type: remove_field
      allowed: false
      requireDeprecation: true
    - type: change_type
      allowed: false
      requireVersionBump: true
```

---

## 6. 契约测试工具

### 6.1 Pact

**Pact Broker 配置**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pact-broker
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: pact-broker
          image: pactfoundation/pact-broker:latest
          env:
            - name: PACT_BROKER_DATABASE_URL
              value: "postgres://pact:pact@postgres:5432/pact"
            - name: PACT_BROKER_BASIC_AUTH_USERNAME
              value: "admin"
            - name: PACT_BROKER_BASIC_AUTH_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: pact-broker-secret
                  key: password
```

### 6.2 Dredd

**Dredd 配置**：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: dredd-contract-test
spec:
  template:
    spec:
      containers:
        - name: dredd
          image: apiaryio/dredd:latest
          command:
            - dredd
            - api/openapi.yaml
            - http://payment-service:8080
            - --hookfiles=./hooks.js
            - --reporter=json
```

---

## 7. 相关文档

- **[API 测试规范](../15-api-testing/api-testing.md)** - 契约测试
- **[API 版本管理](../23-api-versioning/api-versioning.md)** - 契约版本管理
- **[API 标准化规范](../25-api-standardization/api-standardization.md)** - 契约
  标准
- **[最佳实践](../08-best-practices/best-practices.md)** - 契约测试最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
