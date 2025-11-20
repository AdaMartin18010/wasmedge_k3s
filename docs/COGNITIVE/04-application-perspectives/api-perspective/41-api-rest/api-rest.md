# API RESTful 规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [API RESTful 规范](#api-restful-规范)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 RESTful API 架构](#11-restful-api-架构)
    - [1.2 API RESTful 在 API 规范中的位置](#12-api-restful-在-api-规范中的位置)
  - [2 资源设计](#2-资源设计)
    - [2.1 资源命名](#21-资源命名)
    - [2.2 HTTP 方法](#22-http-方法)
  - [3 状态码和响应](#3-状态码和响应)
    - [3.1 HTTP 状态码](#31-http-状态码)
    - [3.2 响应格式](#32-响应格式)
  - [4 版本控制](#4-版本控制)
    - [4.1 URL 版本控制](#41-url-版本控制)
    - [4.2 Header 版本控制](#42-header-版本控制)
  - [5 分页和过滤](#5-分页和过滤)
    - [5.1 分页策略](#51-分页策略)
    - [5.2 过滤和排序](#52-过滤和排序)
  - [6 HATEOAS](#6-hateoas)
    - [6.1 超媒体链接](#61-超媒体链接)
    - [6.2 资源关系](#62-资源关系)
  - [7 形式化定义与理论基础](#7-形式化定义与理论基础)
    - [7.1 API RESTful 形式化模型](#71-api-restful-形式化模型)
    - [7.2 资源操作形式化](#72-资源操作形式化)
    - [7.3 HATEOAS 形式化](#73-hateoas-形式化)
  - [8 相关文档](#8-相关文档)

---

## 1 概述

API RESTful 规范定义了 API 在 RESTful 架构下的设计和实现，从资源设计到状态码响应
，从版本控制到 HATEOAS。本文档基于形式化方法，提供严格的数学定义和推理论证，分析
API RESTful 的理论基础和实践方法。

**参考标准**：

- [REST API Design](https://restfulapi.net/) - RESTful API 设计指南
- [HTTP/1.1 Specification](https://httpwg.org/specs/rfc7231.html) - HTTP/1.1 规
  范
- [OpenAPI Specification](https://swagger.io/specification/) - OpenAPI 规范
- [REST Best Practices](https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api) -
  REST 最佳实践
- [HATEOAS](https://restfulapi.net/hateoas/) - HATEOAS 超媒体约束

### 1.1 RESTful API 架构

```text
资源（Resources）
  ↓
HTTP 方法（HTTP Methods）
  ↓
状态码（Status Codes）
  ↓
超媒体（Hypermedia）
```

### 1.2 API RESTful 在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../07-formalization/formalization.md#21-api-规范四元组)）
，API RESTful 主要涉及 IDL 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
            ↑
    RESTful (implementation)
```

API RESTful 在 API 规范中提供：

- **资源设计**：RESTful 资源命名和设计
- **HTTP 方法**：GET、POST、PUT、DELETE 等
- **状态码**：HTTP 状态码规范
- **HATEOAS**：超媒体链接和资源关系

---

## 2 资源设计

### 2.1 资源命名

**RESTful 资源命名**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-restful
spec:
  style: restful
  resources:
    - name: payments
      path: /api/v1/payments
      methods:
        - GET
        - POST
    - name: payment
      path: /api/v1/payments/{id}
      methods:
        - GET
        - PUT
        - PATCH
        - DELETE
```

### 2.2 HTTP 方法

**HTTP 方法映射**：

| HTTP 方法  | 操作             | 幂等性 | 安全性 |
| ---------- | ---------------- | ------ | ------ |
| **GET**    | 查询资源         | 是     | 是     |
| **POST**   | 创建资源         | 否     | 否     |
| **PUT**    | 更新资源（完整） | 是     | 否     |
| **PATCH**  | 更新资源（部分） | 否     | 否     |
| **DELETE** | 删除资源         | 是     | 否     |

---

## 3 状态码和响应

### 3.1 HTTP 状态码

**状态码使用规范**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-status-codes
spec:
  responses:
    "200":
      description: Success
      useCase: "GET /payments/{id}"
    "201":
      description: Created
      useCase: "POST /payments"
    "204":
      description: No Content
      useCase: "DELETE /payments/{id}"
    "400":
      description: Bad Request
      useCase: "Invalid request body"
    "404":
      description: Not Found
      useCase: "Resource not found"
    "500":
      description: Internal Server Error
      useCase: "Server error"
```

### 3.2 响应格式

**标准响应格式**：

```json
{
  "data": {
    "id": "pay_123",
    "order_id": "order_456",
    "amount": 10000,
    "status": "completed",
    "created_at": "2025-11-07T10:00:00Z"
  },
  "links": {
    "self": "/api/v1/payments/pay_123",
    "order": "/api/v1/orders/order_456"
  },
  "meta": {
    "request_id": "req_789",
    "timestamp": "2025-11-07T10:00:00Z"
  }
}
```

---

## 4 版本控制

### 4.1 URL 版本控制

**URL 版本控制**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-v1
spec:
  versioning:
    strategy: url
    version: "v1"
  paths:
    /api/v1/payments:
      get:
        summary: List payments
    /api/v2/payments:
      get:
        summary: List payments (v2)
```

### 4.2 Header 版本控制

**Header 版本控制**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-header-version
spec:
  versioning:
    strategy: header
    header: "API-Version"
    default: "v1"
  paths:
    /api/payments:
      get:
        summary: List payments
        parameters:
          - name: API-Version
            in: header
            schema:
              type: string
              default: "v1"
```

---

## 5 分页和过滤

### 5.1 分页策略

**基于偏移的分页**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-pagination
spec:
  paths:
    /api/v1/payments:
      get:
        parameters:
          - name: page
            in: query
            schema:
              type: integer
              default: 1
          - name: limit
            in: query
            schema:
              type: integer
              default: 20
              maximum: 100
```

**基于游标的分页**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-cursor-pagination
spec:
  paths:
    /api/v1/payments:
      get:
        parameters:
          - name: cursor
            in: query
            schema:
              type: string
          - name: limit
            in: query
            schema:
              type: integer
              default: 20
```

### 5.2 过滤和排序

**过滤和排序参数**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-filtering
spec:
  paths:
    /api/v1/payments:
      get:
        parameters:
          - name: status
            in: query
            schema:
              type: string
              enum: [pending, processing, completed, failed]
          - name: min_amount
            in: query
            schema:
              type: integer
          - name: max_amount
            in: query
            schema:
              type: integer
          - name: sort
            in: query
            schema:
              type: string
              enum: [created_at, amount]
          - name: order
            in: query
            schema:
              type: string
              enum: [asc, desc]
              default: desc
```

---

## 6 HATEOAS

### 6.1 超媒体链接

**HATEOAS 响应**：

```json
{
  "data": [
    {
      "id": "pay_123",
      "order_id": "order_456",
      "amount": 10000,
      "status": "completed",
      "_links": {
        "self": {
          "href": "/api/v1/payments/pay_123"
        },
        "order": {
          "href": "/api/v1/orders/order_456"
        },
        "refund": {
          "href": "/api/v1/payments/pay_123/refund",
          "method": "POST"
        }
      }
    }
  ],
  "_links": {
    "self": {
      "href": "/api/v1/payments?page=1"
    },
    "next": {
      "href": "/api/v1/payments?page=2"
    },
    "prev": {
      "href": "/api/v1/payments?page=0"
    }
  }
}
```

### 6.2 资源关系

**资源关系定义**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-hateoas
spec:
  resources:
    - name: payments
      relationships:
        - name: order
          type: belongs-to
          resource: orders
        - name: refunds
          type: has-many
          resource: refunds
```

---

## 7 形式化定义与理论基础

### 7.1 API RESTful 形式化模型

**定义 7.1（API RESTful）**：API RESTful 是一个四元组：

```text
API_RESTful = ⟨Resources, HTTP_Methods, Status_Codes, Hypermedia⟩
```

其中：

- **Resources**：资源集合 `Resources: Resource[]`
- **HTTP_Methods**：HTTP 方法 `HTTP_Methods: {GET, POST, PUT, DELETE, PATCH}`
- **Status_Codes**：状态码 `Status_Codes: {200, 201, 400, 404, 500, ...}`
- **Hypermedia**：超媒体链接 `Hypermedia: Resource → Link[]`

**定义 7.2（资源操作）**：资源操作是一个函数：

```text
Resource_Operation: Resource × HTTP_Method × Request → Response
```

**定理 7.1（RESTful 幂等性）**：GET、PUT、DELETE 方法是幂等的：

```text
Method ∈ {GET, PUT, DELETE} ⟹ Idempotent(Resource_Operation(Resource, Method, Request))
```

**证明**：GET、PUT、DELETE 方法多次执行结果相同，因此是幂等的。□

### 7.2 资源操作形式化

**定义 7.3（资源状态）**：资源状态是一个函数：

```text
Resource_State: Resource → State
```

**定义 7.4（状态转换）**：状态转换是一个函数：

```text
State_Transition: Resource × HTTP_Method → Resource'
```

**定理 7.2（RESTful 状态转换）**：PUT 和 PATCH 可以更新资源状态：

```text
Method ∈ {PUT, PATCH} ⟹ Resource_State(Resource') ≠ Resource_State(Resource)
```

**证明**：PUT 和 PATCH 方法用于更新资源，因此会改变资源状态。□

### 7.3 HATEOAS 形式化

**定义 7.5（超媒体链接）**：超媒体链接是一个函数：

```text
Hypermedia_Link: Resource → Link[]
```

**定义 7.6（链接关系）**：链接关系是一个函数：

```text
Link_Relation: Link → Relation
```

**定理 7.3（HATEOAS 可发现性）**：HATEOAS 提高 API 可发现性：

```text
HATEOAS(API) ⟹ Discoverable(API)
```

**证明**：HATEOAS 通过超媒体链接提供资源关系，客户端可以发现可用操作，因此 API
可发现。□

---

## 8 相关文档

- **[API 标准化规范](../25-api-standardization/api-standardization.md)** -
  RESTful 标准
- **[API 版本管理](../23-api-versioning/api-versioning.md)** - RESTful 版本控制
- **[API 性能优化](../14-api-performance/api-performance.md)** - RESTful 性能优
  化
- **[最佳实践](../08-best-practices/best-practices.md)** - RESTful 最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
