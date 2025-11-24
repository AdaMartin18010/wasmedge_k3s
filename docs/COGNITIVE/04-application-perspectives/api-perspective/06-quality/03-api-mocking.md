# API 模拟/Mock 规范

**版本**：v1.0 **最后更新：2025-11-15 **维护者**：项目团队

## 📑 目录

- [API 模拟/Mock 规范](#api-模拟mock-规范)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 Mock 架构](#11-mock-架构)
    - [1.2 API Mock 在 API 规范中的位置](#12-api-mock-在-api-规范中的位置)
  - [2 Mock 服务](#2-mock-服务)
    - [2.1 WireMock](#21-wiremock)
    - [2.2 MockServer](#22-mockserver)
    - [2.3 Prism](#23-prism)
  - [3 Mock 数据生成](#3-mock-数据生成)
    - [3.1 数据生成器](#31-数据生成器)
    - [3.2 模板引擎](#32-模板引擎)
  - [4 Mock 场景](#4-mock-场景)
    - [4.1 成功场景](#41-成功场景)
    - [4.2 错误场景](#42-错误场景)
    - [4.3 延迟场景](#43-延迟场景)
  - [5 Mock 验证](#5-mock-验证)
    - [5.1 请求验证](#51-请求验证)
    - [5.2 调用验证](#52-调用验证)
  - [6 Mock 管理](#6-mock-管理)
    - [6.1 Mock 存储](#61-mock-存储)
    - [6.2 Mock 版本管理](#62-mock-版本管理)
  - [7 形式化定义与理论基础](#7-形式化定义与理论基础)
    - [7.1 API Mock 形式化模型](#71-api-mock-形式化模型)
    - [7.2 Mock 数据生成形式化](#72-mock-数据生成形式化)
    - [7.3 Mock 验证形式化](#73-mock-验证形式化)
  - [8 相关文档](#8-相关文档)

---

## 1 概述

API 模拟/Mock 规范定义了 API 在 Mock 场景下的设计和实现，从 Mock 服务到 Mock 数
据生成，从 Mock 场景到 Mock 验证。本文档基于形式化方法，提供严格的数学定义和推理
论证，分析 API Mock 的理论基础和实践方法。

**参考标准**：

- [WireMock](https://wiremock.org/) - WireMock Mock 服务
- [MockServer](https://www.mock-server.com/) - MockServer Mock 服务
- [Prism](https://stoplight.io/open-source/prism) - Prism OpenAPI Mock
- [Mocking Best Practices](https://martinfowler.com/articles/mocksArentStubs.html) -
  Mock 最佳实践
- [Test Doubles](https://martinfowler.com/bliki/TestDouble.html) - 测试替身

### 1.1 Mock 架构

```text
API 请求（API Request）
  ↓
Mock 服务（Mock Service）
  ↓
Mock 响应（Mock Response）
  ↓
Mock 验证（Mock Verification）
```

### 1.2 API Mock 在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API Mock 主要涉及 IDL 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
            ↑
    Mocking (implementation)
```

API Mock 在 API 规范中提供：

- **Mock 服务**：WireMock、MockServer、Prism
- **Mock 数据**：数据生成器、模板引擎
- **Mock 场景**：成功场景、错误场景、延迟场景
- **Mock 验证**：请求验证、调用验证

---

## 2 Mock 服务

### 2.1 WireMock

**WireMock 配置**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wiremock
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: wiremock
          image: wiremock/wiremock:latest
          ports:
            - containerPort: 8080
          volumeMounts:
            - name: wiremock-mappings
              mountPath: /home/wiremock/mappings
      volumes:
        - name: wiremock-mappings
          configMap:
            name: wiremock-mappings
```

**WireMock 映射定义**：

```json
{
  "request": {
    "method": "POST",
    "url": "/api/v1/payments",
    "headers": {
      "Content-Type": {
        "equalTo": "application/json"
      }
    },
    "bodyPatterns": [
      {
        "matchesJsonPath": "$.order_id"
      },
      {
        "matchesJsonPath": "$.amount"
      }
    ]
  },
  "response": {
    "status": 201,
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "payment_id": "{{randomValue length=10 type='ALPHANUMERIC'}}",
      "status": "pending"
    }
  }
}
```

### 2.2 MockServer

**MockServer 配置**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mockserver
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: mockserver
          image: mockserver/mockserver:latest
          ports:
            - containerPort: 1080
          env:
            - name: MOCKSERVER_INITIALIZATION_JSON_PATH
              value: "/config/expectations.json"
```

**MockServer 期望定义**：

```json
{
  "httpRequest": {
    "method": "POST",
    "path": "/api/v1/payments",
    "headers": {
      "Content-Type": ["application/json"]
    },
    "body": {
      "type": "JSON",
      "json": "{\"order_id\": \".*\", \"amount\": [0-9]+}"
    }
  },
  "httpResponse": {
    "statusCode": 201,
    "headers": {
      "Content-Type": ["application/json"]
    },
    "body": {
      "type": "JSON",
      "json": "{\"payment_id\": \"pay_123\", \"status\": \"pending\"}"
    }
  }
}
```

### 2.3 Prism

**Prism 配置**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prism
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: prism
          image: stoplight/prism:latest
          command:
            - prism
            - mock
            - /api/openapi.yaml
            - -h
            - 0.0.0.0
            - -p
            - "4010"
```

---

## 3 Mock 数据生成

### 3.1 数据生成器

**Faker 数据生成**：

```go
package main

import (
    "github.com/brianvoe/gofakeit/v6"
)

func GenerateMockPayment() map[string]interface{} {
    return map[string]interface{}{
        "payment_id": gofakeit.UUID(),
        "order_id":  "order_" + gofakeit.LetterN(10),
        "amount":     gofakeit.IntRange(1000, 100000),
        "status":    gofakeit.RandomString([]string{"pending", "processing", "completed"}),
        "created_at": gofakeit.Date().Format(time.RFC3339),
    }
}
```

### 3.2 模板引擎

**模板引擎 Mock 响应**：

```json
{
  "response": {
    "status": 201,
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "payment_id": "{{faker.uuid}}",
      "order_id": "{{request.body.order_id}}",
      "amount": "{{request.body.amount}}",
      "status": "pending",
      "created_at": "{{faker.date.iso8601}}"
    }
  }
}
```

---

## 4 Mock 场景

### 4.1 成功场景

**成功场景 Mock**：

```json
{
  "scenario": "payment_created",
  "request": {
    "method": "POST",
    "url": "/api/v1/payments"
  },
  "response": {
    "status": 201,
    "body": {
      "payment_id": "pay_123",
      "status": "pending"
    }
  }
}
```

### 4.2 错误场景

**错误场景 Mock**：

```json
{
  "scenario": "payment_insufficient_funds",
  "request": {
    "method": "POST",
    "url": "/api/v1/payments",
    "bodyPatterns": [
      {
        "matchesJsonPath": "$[?(@.amount > 10000)]"
      }
    ]
  },
  "response": {
    "status": 400,
    "body": {
      "error": {
        "code": "INSUFFICIENT_FUNDS",
        "message": "Insufficient funds"
      }
    }
  }
}
```

### 4.3 延迟场景

**延迟场景 Mock**：

```json
{
  "scenario": "payment_slow_response",
  "request": {
    "method": "POST",
    "url": "/api/v1/payments"
  },
  "response": {
    "status": 201,
    "fixedDelayMilliseconds": 2000,
    "body": {
      "payment_id": "pay_123",
      "status": "pending"
    }
  }
}
```

---

## 5 Mock 验证

### 5.1 请求验证

**请求验证实现**：

```go
package main

import (
    "github.com/wiremock/go-wiremock"
)

func VerifyRequest(client *wiremock.Client, expectedRequest wiremock.RequestPatternBuilder) error {
    requests, err := client.FindRequests(expectedRequest.Build())
    if err != nil {
        return err
    }

    if len(requests) == 0 {
        return fmt.Errorf("request not found")
    }

    return nil
}
```

### 5.2 调用验证

**调用验证实现**：

```go
func VerifyCallCount(client *wiremock.Client, expectedRequest wiremock.RequestPatternBuilder, expectedCount int) error {
    requests, err := client.FindRequests(expectedRequest.Build())
    if err != nil {
        return err
    }

    if len(requests) != expectedCount {
        return fmt.Errorf("expected %d calls, got %d", expectedCount, len(requests))
    }

    return nil
}
```

---

## 6 Mock 管理

### 6.1 Mock 存储

**Mock 存储配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: wiremock-mappings
data:
  payment-created.json: |
    {
      "request": {
        "method": "POST",
        "url": "/api/v1/payments"
      },
      "response": {
        "status": 201,
        "body": {
          "payment_id": "pay_123",
          "status": "pending"
        }
      }
    }
```

### 6.2 Mock 版本管理

**Mock 版本管理**：

```yaml
apiVersion: api.example.com/v1
kind: MockVersion
metadata:
  name: payment-mock-version
spec:
  currentVersion: "1.0.0"
  versions:
    - version: "1.0.0"
      active: true
      mappings:
        - payment-created.json
        - payment-error.json
    - version: "1.1.0"
      active: false
      mappings:
        - payment-created-v2.json
```

---

## 7 形式化定义与理论基础

### 7.1 API Mock 形式化模型

**定义 7.1（API Mock）**：API Mock 是一个四元组：

```text
API_Mock = ⟨Mock_Service, Data_Generator, Scenario_Manager, Verification⟩
```

其中：

- **Mock_Service**：Mock 服务 `Mock_Service: Request → Mock_Response`
- **Data_Generator**：数据生成器 `Data_Generator: Schema → Mock_Data`
- **Scenario_Manager**：场景管理器 `Scenario_Manager: Scenario → Mock_Behavior`
- **Verification**：验证 `Verification: Request × Mock_Service → Bool`

**定义 7.2（Mock 响应）**：Mock 响应是一个函数：

```text
Mock_Response: Request × Scenario → Response
```

**定理 7.1（Mock 正确性）**：如果 Mock 符合契约，则 Mock 正确：

```text
Compliant(Mock, Contract) ⟹ Correct(Mock)
```

**证明**：如果 Mock 符合契约，则 Mock 响应满足契约要求，因此 Mock 正确。□

### 7.2 Mock 数据生成形式化

**定义 7.3（数据生成）**：数据生成是一个函数：

```text
Generate_Data: Schema × Constraints → Data
```

**定义 7.4（数据真实性）**：数据真实性是一个函数：

```text
Data_Realism: Mock_Data → [0, 1]
```

**定理 7.2（数据生成有效性）**：如果数据生成器正确，则生成的数据有效：

```text
Correct(Data_Generator) ⟹ Valid(Generate_Data(Schema))
```

**证明**：如果数据生成器正确，则生成的数据符合 Schema，因此数据有效。□

### 7.3 Mock 验证形式化

**定义 7.5（请求验证）**：请求验证是一个函数：

```text
Verify_Request: Request × Expected_Request → Bool
```

**定义 7.6（调用验证）**：调用验证是一个函数：

```text
Verify_Calls: Mock_Service × Expected_Calls → Bool
```

**定理 7.3（Mock 验证完备性）**：如果请求和调用验证都通过，则 Mock 使用正确：

```text
Verify_Request(Request) = Pass ∧ Verify_Calls(Mock) = Pass ⟹ Correct_Usage(Mock)
```

**证明**：如果请求和调用验证都通过，则 Mock 被正确使用，因此使用正确。□

---

## 8 相关文档

- **[API 测试规范](../15-api-testing/api-testing.md)** - Mock 测试
- **[API 契约测试](../51-api-contract-testing/api-contract-testing.md)** - 契约
  Mock
- **[最佳实践](../00-foundation/05-best-practices.md)** - Mock 最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新：2025-11-15 **维护者**：项目团队
