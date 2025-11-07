# API 模拟/Mock 规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 Mock 架构](#11-mock-架构)
- [2. Mock 服务](#2-mock-服务)
  - [2.1 WireMock](#21-wiremock)
  - [2.2 MockServer](#22-mockserver)
  - [2.3 Prism](#23-prism)
- [3. Mock 数据生成](#3-mock-数据生成)
  - [3.1 数据生成器](#31-数据生成器)
  - [3.2 模板引擎](#32-模板引擎)
- [4. Mock 场景](#4-mock-场景)
  - [4.1 成功场景](#41-成功场景)
  - [4.2 错误场景](#42-错误场景)
  - [4.3 延迟场景](#43-延迟场景)
- [5. Mock 验证](#5-mock-验证)
  - [5.1 请求验证](#51-请求验证)
  - [5.2 调用验证](#52-调用验证)
- [6. Mock 管理](#6-mock-管理)
  - [6.1 Mock 存储](#61-mock-存储)
  - [6.2 Mock 版本管理](#62-mock-版本管理)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 模拟/Mock 规范定义了 API 在 Mock 场景下的设计和实现，从 Mock 服务到 Mock 数
据生成，从 Mock 场景到 Mock 验证。

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

---

## 2. Mock 服务

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

## 3. Mock 数据生成

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

## 4. Mock 场景

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

## 5. Mock 验证

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

## 6. Mock 管理

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

## 7. 相关文档

- **[API 测试规范](../15-api-testing/api-testing.md)** - Mock 测试
- **[API 契约测试](../51-api-contract-testing/api-contract-testing.md)** - 契约
  Mock
- **[最佳实践](../08-best-practices/best-practices.md)** - Mock 最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
