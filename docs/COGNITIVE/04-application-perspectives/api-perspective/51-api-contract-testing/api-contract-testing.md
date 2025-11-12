# API 契约测试规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 契约测试架构](#11-契约测试架构)
  - [1.2 API 契约测试在 API 规范中的位置](#12-api-契约测试在-api-规范中的位置)
- [2 契约定义](#2-契约定义)
  - [2.1 OpenAPI 契约](#21-openapi-契约)
  - [2.2 gRPC 契约](#22-grpc-契约)
  - [2.3 GraphQL 契约](#23-graphql-契约)
- [3 消费者驱动契约](#3-消费者驱动契约)
  - [3.1 Pact 契约](#31-pact-契约)
  - [3.2 Spring Cloud Contract](#32-spring-cloud-contract)
- [4 契约验证](#4-契约验证)
  - [4.1 提供者验证](#41-提供者验证)
  - [4.2 消费者验证](#42-消费者验证)
- [5 契约版本管理](#5-契约版本管理)
  - [5.1 版本兼容性](#51-版本兼容性)
  - [5.2 版本演进](#52-版本演进)
- [6 契约测试工具](#6-契约测试工具)
  - [6.1 Pact](#61-pact)
  - [6.2 Dredd](#62-dredd)
- [7 形式化定义与理论基础](#7-形式化定义与理论基础)
  - [7.1 API 契约测试形式化模型](#71-api-契约测试形式化模型)
  - [7.2 契约验证形式化](#72-契约验证形式化)
  - [7.3 契约兼容性形式化](#73-契约兼容性形式化)
- [8 相关文档](#8-相关文档)

---

## 1 概述

API 契约测试规范定义了 API 在契约测试场景下的设计和实现，从契约定义到契约验证，
从消费者驱动契约到契约版本管理。本文档基于形式化方法，提供严格的数学定义和推理论
证，分析 API 契约测试的理论基础和实践方法。

**参考标准**：

- [Pact](https://docs.pact.io/) - Pact 契约测试框架
- [Consumer-Driven Contracts](https://martinfowler.com/articles/consumerDrivenContracts.html) -
  消费者驱动契约
- [Spring Cloud Contract](https://spring.io/projects/spring-cloud-contract) -
  Spring Cloud Contract
- [Contract Testing Best Practices](https://docs.pact.io/best_practices/) - 契约
  测试最佳实践
- [API Contract Testing](https://www.postman.com/api-platform/api-testing/) -
  API 契约测试

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

### 1.2 API 契约测试在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../07-formalization/formalization.md#21-api-规范四元组)）
，API 契约测试主要涉及 IDL 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
            ↑
    Contract Testing (implementation)
```

API 契约测试在 API 规范中提供：

- **契约定义**：OpenAPI、gRPC、GraphQL 契约
- **契约验证**：提供者验证、消费者验证
- **版本管理**：契约版本兼容性、版本演进
- **测试工具**：Pact、Dredd 等契约测试工具

---

## 2 契约定义

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

## 3 消费者驱动契约

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

## 4 契约验证

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

## 5 契约版本管理

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

## 6 契约测试工具

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

## 7 形式化定义与理论基础

### 7.1 API 契约测试形式化模型

**定义 7.1（API 契约测试）**：API 契约测试是一个四元组：

```text
API_Contract_Testing = ⟨Contract_Definition, Provider_Verification, Consumer_Verification, Version_Management⟩
```

其中：

- **Contract_Definition**：契约定义 `Contract_Definition: API → Contract`
- **Provider_Verification**：提供者验证
  `Provider_Verification: Contract × Provider → Bool`
- **Consumer_Verification**：消费者验证
  `Consumer_Verification: Contract × Consumer → Bool`
- **Version_Management**：版本管理 `Version_Management: Contract → Version`

**定义 7.2（契约一致性）**：契约一致性是一个函数：

```text
Contract_Consistency: Contract × Implementation → Bool
```

**定理 7.1（契约测试有效性）**：如果契约测试通过，则实现符合契约：

```text
Pass(Contract_Test(Contract, Implementation)) ⟹ Consistent(Contract, Implementation)
```

**证明**：如果契约测试通过，则实现满足契约的所有要求，因此实现符合契约。□

### 7.2 契约验证形式化

**定义 7.3（提供者验证）**：提供者验证是一个函数：

```text
Verify_Provider: Contract × Provider_API → {Pass, Fail}
```

**定义 7.4（消费者验证）**：消费者验证是一个函数：

```text
Verify_Consumer: Contract × Consumer_Usage → {Pass, Fail}
```

**定理 7.2（契约验证完备性）**：提供者和消费者验证都通过，则契约完备：

```text
Verify_Provider(Contract, Provider) = Pass ∧ Verify_Consumer(Contract, Consumer) = Pass ⟹ Complete(Contract)
```

**证明**：如果提供者和消费者验证都通过，则契约满足双方需求，因此契约完备。□

### 7.3 契约兼容性形式化

**定义 7.5（契约兼容性）**：契约兼容性是一个函数：

```text
Contract_Compatibility: Contract₁ × Contract₂ → {Compatible, Incompatible}
```

**定义 7.6（向后兼容）**：向后兼容是一个函数：

```text
Backward_Compatible: Contract_Old × Contract_New → Bool
```

**定理 7.3（向后兼容性传递）**：如果 Contract₂ 向后兼容 Contract₁，Contract₃ 向
后兼容 Contract₂，则 Contract₃ 向后兼容 Contract₁：

```text
Backward_Compatible(C₁, C₂) ∧ Backward_Compatible(C₂, C₃) ⟹ Backward_Compatible(C₁, C₃)
```

**证明**：向后兼容性具有传递性，因此如果 C₂ 兼容 C₁，C₃ 兼容 C₂，则 C₃ 兼容
C₁。□

---

## 8 相关文档

- **[API 测试规范](../15-api-testing/api-testing.md)** - 契约测试
- **[API 版本管理](../23-api-versioning/api-versioning.md)** - 契约版本管理
- **[API 标准化规范](../25-api-standardization/api-standardization.md)** - 契约
  标准
- **[最佳实践](../08-best-practices/best-practices.md)** - 契约测试最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
