# API 标准化规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 标准化框架](#11-标准化框架)
- [2. API 设计标准](#2-api-设计标准)
  - [2.1 RESTful API 标准](#21-restful-api-标准)
  - [2.2 GraphQL API 标准](#22-graphql-api-标准)
  - [2.3 gRPC API 标准](#23-grpc-api-标准)
- [3. 命名规范](#3-命名规范)
  - [3.1 资源命名规范](#31-资源命名规范)
  - [3.2 操作命名规范](#32-操作命名规范)
  - [3.3 字段命名规范](#33-字段命名规范)
- [4. 数据格式标准](#4-数据格式标准)
  - [4.1 JSON Schema 标准](#41-json-schema-标准)
  - [4.2 Protobuf 标准](#42-protobuf-标准)
  - [4.3 WIT 标准](#43-wit-标准)
- [5. 错误处理标准](#5-错误处理标准)
  - [5.1 HTTP 状态码标准](#51-http-状态码标准)
  - [5.2 错误响应格式标准](#52-错误响应格式标准)
- [6. 认证授权标准](#6-认证授权标准)
  - [6.1 OAuth 2.0 标准](#61-oauth-20-标准)
  - [6.2 JWT 标准](#62-jwt-标准)
  - [6.3 mTLS 标准](#63-mtls-标准)
- [7. 标准化工具](#7-标准化工具)
  - [7.1 API Linter](#71-api-linter)
  - [7.2 API 验证工具](#72-api-验证工具)
- [8. 相关文档](#8-相关文档)

---

## 1. 概述

API 标准化规范定义了 API 在不同运行时环境下的标准化要求，从设计标准到命名规范，
从数据格式到错误处理，确保 API 的一致性和互操作性。

### 1.1 标准化框架

```text
设计标准（RESTful、GraphQL、gRPC）
  ↓
命名规范（资源命名、操作命名）
  ↓
数据格式标准（JSON Schema、Protobuf、WIT）
  ↓
错误处理标准（HTTP 状态码、错误响应格式）
  ↓
认证授权标准（OAuth 2.0、JWT、mTLS）
```

---

## 2. API 设计标准

### 2.1 RESTful API 标准

**RESTful 原则**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-restful
spec:
  style: restful
  standards:
    restful:
      resourceBased: true
      httpMethods:
        - GET
        - POST
        - PUT
        - DELETE
      statusCodes:
        - 200
        - 201
        - 204
        - 400
        - 404
        - 500
```

**RESTful 资源设计**：

```yaml
paths:
  /api/v1/payments:
    get:
      summary: List payments
      operationId: listPayments
    post:
      summary: Create payment
      operationId: createPayment
  /api/v1/payments/{id}:
    get:
      summary: Get payment
      operationId: getPayment
    put:
      summary: Update payment
      operationId: updatePayment
    delete:
      summary: Delete payment
      operationId: deletePayment
```

### 2.2 GraphQL API 标准

**GraphQL Schema**：

```graphql
type Payment {
  id: ID!
  orderId: String!
  amount: Int!
  status: PaymentStatus!
  createdAt: DateTime!
}

type Query {
  payment(id: ID!): Payment
  payments(filter: PaymentFilter): [Payment!]!
}

type Mutation {
  createPayment(input: CreatePaymentInput!): Payment!
  updatePayment(id: ID!, input: UpdatePaymentInput!): Payment!
}
```

### 2.3 gRPC API 标准

**Protobuf 定义**：

```protobuf
syntax = "proto3";

package payment.v1;

service PaymentService {
  rpc CreatePayment(CreatePaymentRequest) returns (CreatePaymentResponse);
  rpc GetPayment(GetPaymentRequest) returns (GetPaymentResponse);
  rpc ListPayments(ListPaymentsRequest) returns (ListPaymentsResponse);
}

message CreatePaymentRequest {
  string order_id = 1;
  int64 amount = 2;
}

message CreatePaymentResponse {
  string payment_id = 1;
  string status = 2;
}
```

---

## 3. 命名规范

### 3.1 资源命名规范

**RESTful 资源命名**：

```yaml
# ✅ 正确：使用复数名词
/api/v1/payments
/api/v1/orders
/api/v1/users

# ❌ 错误：使用单数名词
/api/v1/payment
/api/v1/order
/api/v1/user

# ✅ 正确：使用小写和连字符
/api/v1/payment-methods
/api/v1/user-profiles

# ❌ 错误：使用驼峰命名
/api/v1/paymentMethods
/api/v1/userProfiles
```

### 3.2 操作命名规范

**gRPC 操作命名**：

```protobuf
// ✅ 正确：使用动词+名词
rpc CreatePayment(CreatePaymentRequest) returns (CreatePaymentResponse);
rpc GetPayment(GetPaymentRequest) returns (GetPaymentResponse);
rpc UpdatePayment(UpdatePaymentRequest) returns (UpdatePaymentResponse);
rpc DeletePayment(DeletePaymentRequest) returns (DeletePaymentResponse);

// ❌ 错误：使用名词
rpc Payment(CreatePaymentRequest) returns (CreatePaymentResponse);
```

### 3.3 字段命名规范

**JSON 字段命名**：

```json
{
  "payment_id": "pay_123",
  "order_id": "order_456",
  "created_at": "2025-11-07T10:00:00Z",
  "total_amount": 10000
}
```

---

## 4. 数据格式标准

### 4.1 JSON Schema 标准

**JSON Schema 定义**：

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["order_id", "amount"],
  "properties": {
    "order_id": {
      "type": "string",
      "pattern": "^order_[a-zA-Z0-9]+$"
    },
    "amount": {
      "type": "integer",
      "minimum": 0,
      "maximum": 1000000
    }
  }
}
```

### 4.2 Protobuf 标准

**Protobuf 字段标准**：

```protobuf
message Payment {
  string payment_id = 1;        // 必填字段
  string order_id = 2;          // 必填字段
  int64 amount = 3;             // 必填字段
  optional string description = 4;  // 可选字段
  repeated string tags = 5;     // 重复字段
}
```

### 4.3 WIT 标准

**WIT 类型标准**：

```wit
package example:payment@1.0.0;

type payment-request = record {
    order-id: string,
    amount: u64,
    currency: option<string>,
};

type payment-response = record {
    payment-id: string,
    status: string,
    created-at: string,
};
```

---

## 5. 错误处理标准

### 5.1 HTTP 状态码标准

**状态码使用规范**：

```yaml
responses:
  "200":
    description: Success
  "201":
    description: Created
  "204":
    description: No Content
  "400":
    description: Bad Request
  "401":
    description: Unauthorized
  "403":
    description: Forbidden
  "404":
    description: Not Found
  "409":
    description: Conflict
  "500":
    description: Internal Server Error
  "503":
    description: Service Unavailable
```

### 5.2 错误响应格式标准

**标准错误响应**：

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid payment amount",
    "details": [
      {
        "field": "amount",
        "reason": "Amount must be greater than 0"
      }
    ],
    "request_id": "req_123456",
    "timestamp": "2025-11-07T10:00:00Z"
  }
}
```

**gRPC 错误标准**：

```protobuf
message Error {
  string code = 1;
  string message = 2;
  repeated ErrorDetail details = 3;
  string request_id = 4;
  google.protobuf.Timestamp timestamp = 5;
}
```

---

## 6. 认证授权标准

### 6.1 OAuth 2.0 标准

**OAuth 2.0 配置**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-oauth
spec:
  security:
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: "https://auth.example.com/oauth/authorize"
          tokenUrl: "https://auth.example.com/oauth/token"
          scopes:
            payments:read: "Read payments"
            payments:write: "Write payments"
```

### 6.2 JWT 标准

**JWT Token 标准**：

```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_123",
    "iss": "https://auth.example.com",
    "aud": "payment-api",
    "exp": 1733587200,
    "iat": 1733500800,
    "scope": "payments:read payments:write"
  }
}
```

### 6.3 mTLS 标准

**mTLS 配置**：

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: payment-api-mtls
spec:
  selector:
    matchLabels:
      app: payment-api
  mtls:
    mode: STRICT
```

---

## 7. 标准化工具

### 7.1 API Linter

**Spectral 配置**：

```yaml
extends: ["spectral:oas"]
rules:
  operation-operationId: error
  operation-tags: error
  operation-summary: error
  path-params: error
  no-$ref-siblings: error
  no-enum-type-mismatch: error
```

### 7.2 API 验证工具

**OpenAPI 验证**：

```bash
# 使用 swagger-codegen 验证
swagger-codegen validate -i api/openapi.yaml

# 使用 spectral 验证
spectral lint api/openapi.yaml
```

**gRPC 验证**：

```bash
# 使用 protoc 验证
protoc --validate_out=. payment.proto
```

---

## 8. 相关文档

- **[最佳实践](../08-best-practices/best-practices.md)** - API 标准化最佳实践
- **[API 设计规范](../01-containerization-api/containerization-api.md)** - API
  设计标准
- **[API 安全规范](../11-api-security/api-security.md)** - 认证授权标准
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新**：2025-11-07 **维护者**：项目团队
