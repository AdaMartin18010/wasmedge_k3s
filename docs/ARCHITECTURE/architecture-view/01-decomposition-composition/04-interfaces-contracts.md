# 接口与契约：明确定义子结构的输入/输出

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 核心思想](#11-核心思想)
- [2. 接口与契约类型](#2-接口与契约类型)
  - [2.1 接口类型概览](#21-接口类型概览)
- [3. API 契约](#3-api-契约)
  - [3.1 OpenAPI 3.0](#31-openapi-30)
  - [3.2 gRPC Protobuf](#32-grpc-protobuf)
  - [3.3 GraphQL SDL](#33-graphql-sdl)
- [4. 事件契约](#4-事件契约)
  - [4.1 Avro Schema](#41-avro-schema)
  - [4.2 JSON Schema](#42-json-schema)
- [5. 数据契约](#5-数据契约)
  - [5.1 ER 图](#51-er-图)
  - [5.2 JSON Schema](#52-json-schema)
- [6. 配置契约](#6-配置契约)
  - [6.1 Terraform Modules](#61-terraform-modules)
  - [6.2 Helm Charts](#62-helm-charts)
- [7. 凭据契约](#7-凭据契约)
  - [7.1 OAuth2](#71-oauth2)
  - [7.2 SPIFFE](#72-spiffe)
- [8. 接口版本化](#8-接口版本化)
  - [8.1 语义化版本](#81-语义化版本)
  - [8.2 API 版本策略](#82-api-版本策略)
- [9. 接口测试](#9-接口测试)
  - [9.1 契约测试](#91-契约测试)
  - [9.2 接口测试示例](#92-接口测试示例)
- [10. 形式化定义](#10-形式化定义)
  - [10.1 接口定义](#101-接口定义)
  - [10.2 契约定义](#102-契约定义)
  - [10.3 版本定义](#103-版本定义)
- [11. 最佳实践](#11-最佳实践)
  - [11.1 契约优先](#111-契约优先)
  - [11.2 版本管理](#112-版本管理)
  - [11.3 测试验证](#113-测试验证)
- [12. 总结](#12-总结)

---

## 1. 概述

本文档详细阐述**接口与契约**的定义方法，这是确保拆分出的组件能够正确协作的关键。

### 1.1 核心思想

> **明确定义子结构的 **输入/输出**，确保组件间的接口契约清晰、可验证、可演进**

## 2. 接口与契约类型

### 2.1 接口类型概览

| 接口类型     | 定义方式                   | 典型工具                                 | 适用场景           |
| ------------ | -------------------------- | ---------------------------------------- | ------------------ |
| **API 契约** | OpenAPI 3.0、gRPC Protobuf | OpenAPI, GraphQL SDL, Avro/Protobuf      | REST API、gRPC API |
| **事件契约** | Avro、JSON Schema          | Kafka Schema Registry, Avro, JSON Schema | 事件驱动架构       |
| **数据契约** | ER 图、JSON Schema         | ERD, JSON Schema, Protocol Buffers       | 数据模型定义       |
| **配置契约** | Terraform modules、Helm    | Terraform, Helm, Kustomize               | 基础设施配置       |
| **凭据契约** | OAuth2、OpenID Connect     | OAuth2, OpenID Connect, SPIFFE           | 身份认证和授权     |

## 3. API 契约

### 3.1 OpenAPI 3.0

**定义方式**：使用 OpenAPI 3.0 规范定义 REST API

**示例**：

```yaml
openapi: 3.0.0
info:
  title: Order Service API
  version: 1.0.0
paths:
  /orders:
    post:
      summary: Create an order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Order"
      responses:
        "201":
          description: Order created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Order"
components:
  schemas:
    Order:
      type: object
      properties:
        id:
          type: string
        customerId:
          type: string
        items:
          type: array
          items:
            $ref: "#/components/schemas/OrderItem"
```

### 3.2 gRPC Protobuf

**定义方式**：使用 Protocol Buffers 定义 gRPC 服务

**示例**：

```protobuf
syntax = "proto3";

package order.v1;

service OrderService {
  rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);
  rpc GetOrder(GetOrderRequest) returns (GetOrderResponse);
}

message CreateOrderRequest {
  string customer_id = 1;
  repeated OrderItem items = 2;
}

message CreateOrderResponse {
  string order_id = 1;
  OrderStatus status = 2;
}

message OrderItem {
  string product_id = 1;
  int32 quantity = 2;
  double price = 3;
}

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_CONFIRMED = 2;
  ORDER_STATUS_SHIPPED = 3;
}
```

### 3.3 GraphQL SDL

**定义方式**：使用 GraphQL Schema Definition Language

**示例**：

```graphql
type Query {
  order(id: ID!): Order
  orders(customerId: ID!): [Order!]!
}

type Mutation {
  createOrder(input: CreateOrderInput!): Order!
}

type Order {
  id: ID!
  customerId: ID!
  items: [OrderItem!]!
  status: OrderStatus!
  createdAt: DateTime!
}

type OrderItem {
  productId: ID!
  quantity: Int!
  price: Float!
}

input CreateOrderInput {
  customerId: ID!
  items: [OrderItemInput!]!
}

input OrderItemInput {
  productId: ID!
  quantity: Int!
  price: Float!
}

enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
}
```

## 4. 事件契约

### 4.1 Avro Schema

**定义方式**：使用 Apache Avro 定义事件 Schema

**示例**：

```json
{
  "type": "record",
  "name": "OrderCreated",
  "namespace": "com.example.events",
  "fields": [
    {
      "name": "orderId",
      "type": "string"
    },
    {
      "name": "customerId",
      "type": "string"
    },
    {
      "name": "items",
      "type": {
        "type": "array",
        "items": {
          "type": "record",
          "name": "OrderItem",
          "fields": [
            {
              "name": "productId",
              "type": "string"
            },
            {
              "name": "quantity",
              "type": "int"
            },
            {
              "name": "price",
              "type": "double"
            }
          ]
        }
      }
    },
    {
      "name": "timestamp",
      "type": "long",
      "logicalType": "timestamp-millis"
    }
  ]
}
```

### 4.2 JSON Schema

**定义方式**：使用 JSON Schema 定义事件格式

**示例**：

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "OrderCreated",
  "properties": {
    "orderId": {
      "type": "string"
    },
    "customerId": {
      "type": "string"
    },
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "productId": {
            "type": "string"
          },
          "quantity": {
            "type": "integer"
          },
          "price": {
            "type": "number"
          }
        },
        "required": ["productId", "quantity", "price"]
      }
    },
    "timestamp": {
      "type": "integer",
      "format": "int64"
    }
  },
  "required": ["orderId", "customerId", "items", "timestamp"]
}
```

## 5. 数据契约

### 5.1 ER 图

**定义方式**：使用实体关系图定义数据模型

**示例**：

```text
Order
├── id (PK)
├── customerId (FK)
├── status
├── createdAt
└── items (1:N)
    └── OrderItem
        ├── id (PK)
        ├── orderId (FK)
        ├── productId
        ├── quantity
        └── price
```

### 5.2 JSON Schema

**定义方式**：使用 JSON Schema 定义数据模型

**示例**：

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "Order",
  "properties": {
    "id": {
      "type": "string"
    },
    "customerId": {
      "type": "string"
    },
    "status": {
      "type": "string",
      "enum": ["PENDING", "CONFIRMED", "SHIPPED"]
    },
    "items": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/OrderItem"
      }
    }
  },
  "definitions": {
    "OrderItem": {
      "type": "object",
      "properties": {
        "productId": {
          "type": "string"
        },
        "quantity": {
          "type": "integer"
        },
        "price": {
          "type": "number"
        }
      }
    }
  }
}
```

## 6. 配置契约

### 6.1 Terraform Modules

**定义方式**：使用 Terraform 模块定义基础设施配置

**示例**：

```hcl
module "kubernetes_cluster" {
  source = "./modules/kubernetes"

  cluster_name = "my-cluster"
  node_count   = 3
  node_size    = "standard-2"

  tags = {
    Environment = "production"
    Project     = "my-project"
  }
}

output "cluster_endpoint" {
  value = module.kubernetes_cluster.endpoint
}
```

### 6.2 Helm Charts

**定义方式**：使用 Helm Chart 定义 Kubernetes 应用配置

**示例**：

```yaml
# values.yaml
replicaCount: 3

image:
  repository: my-app
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  hosts:
    - host: my-app.example.com
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

## 7. 凭据契约

### 7.1 OAuth2

**定义方式**：使用 OAuth2 协议定义身份认证和授权

**示例**：

```yaml
oauth2:
  client_id: "my-client-id"
  client_secret: "my-client-secret"
  authorization_url: "https://auth.example.com/oauth/authorize"
  token_url: "https://auth.example.com/oauth/token"
  scopes:
    - "read:orders"
    - "write:orders"
  redirect_uri: "https://my-app.example.com/callback"
```

### 7.2 SPIFFE

**定义方式**：使用 SPIFFE 定义服务身份

**示例**：

```yaml
spiffe:
  trust_domain: "example.com"
  spiffe_id: "spiffe://example.com/ns/default/sa/order-service"
  workload_selector:
    app: order-service
    namespace: default
```

## 8. 接口版本化

### 8.1 语义化版本

**定义方式**：使用语义化版本控制接口版本

**规则**：

- **主版本号**：不兼容的 API 修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

**示例**：

- `v1.0.0`：初始版本
- `v1.1.0`：新增功能，向下兼容
- `v2.0.0`：不兼容的 API 修改

### 8.2 API 版本策略

**策略类型**：

- **URL 版本化**：`/api/v1/orders`、`/api/v2/orders`
- **Header 版本化**：`Accept: application/vnd.api+json;version=1`
- **Query 版本化**：`/api/orders?version=1`

## 9. 接口测试

### 9.1 契约测试

**工具**：

- **Pact**：消费者驱动契约测试
- **Spring Cloud Contract**：契约测试框架
- **OpenAPI Validator**：OpenAPI 规范验证

### 9.2 接口测试示例

**Pact 示例**：

```javascript
const { Pact } = require("@pact-foundation/pact");

const provider = new Pact({
  consumer: "OrderService",
  provider: "PaymentService",
  port: 1234,
  log: "./logs/pact.log",
  dir: "./pacts",
  logLevel: "INFO"
});

describe("Payment Service", () => {
  before(() => provider.setup());
  after(() => provider.finalize());

  it("should process payment", () => {
    return provider.addInteraction({
      state: "order exists",
      uponReceiving: "a request to process payment",
      withRequest: {
        method: "POST",
        path: "/payments",
        body: {
          orderId: "123",
          amount: 100.0
        }
      },
      willRespondWith: {
        status: 200,
        body: {
          paymentId: "456",
          status: "success"
        }
      }
    });
  });
});
```

## 10. 形式化定义

### 10.1 接口定义

```text
接口 I = ⟨name, type, input, output, contract⟩
其中：
- name: 接口名称
- type ∈ {API, Event, Data, Config, Credential}
- input: 输入参数集合
- output: 输出结果集合
- contract: 接口契约（Schema、验证规则）
```

### 10.2 契约定义

```text
契约 C = ⟨schema, validation, version⟩
其中：
- schema: 数据模式定义
- validation: 验证规则
- version: 版本信息
```

### 10.3 版本定义

```text
版本 V = ⟨major, minor, patch, compatibility⟩
其中：
- major: 主版本号
- minor: 次版本号
- patch: 修订号
- compatibility: 兼容性规则
```

## 11. 最佳实践

### 11.1 契约优先

1. **先定义接口契约**，再实现具体逻辑
2. **使用标准格式**（OpenAPI、Protobuf、Avro）
3. **文档完善**，包含示例和错误处理

### 11.2 版本管理

1. **语义化版本**：使用语义化版本控制
2. **向后兼容**：新版本保持向后兼容
3. **废弃策略**：制定明确的废弃策略

### 11.3 测试验证

1. **契约测试**：使用 Pact、Spring Cloud Contract
2. **接口测试**：验证接口功能和性能
3. **集成测试**：验证组件间协作

## 12. 总结

通过**接口与契约**，我们可以：

1. **明确定义**：清晰定义组件的输入输出
2. **可验证性**：通过 Schema 验证接口正确性
3. **可演进性**：通过版本化支持接口演进
4. **可测试性**：通过契约测试确保接口一致性
5. **可文档化**：通过标准格式自动生成文档

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第 28
行，接口与契约部分
