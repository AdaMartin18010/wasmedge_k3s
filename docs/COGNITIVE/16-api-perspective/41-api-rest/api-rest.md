# API RESTful 规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 RESTful API 架构](#11-restful-api-架构)
- [2. 资源设计](#2-资源设计)
  - [2.1 资源命名](#21-资源命名)
  - [2.2 HTTP 方法](#22-http-方法)
- [3. 状态码和响应](#3-状态码和响应)
  - [3.1 HTTP 状态码](#31-http-状态码)
  - [3.2 响应格式](#32-响应格式)
- [4. 版本控制](#4-版本控制)
  - [4.1 URL 版本控制](#41-url-版本控制)
  - [4.2 Header 版本控制](#42-header-版本控制)
- [5. 分页和过滤](#5-分页和过滤)
  - [5.1 分页策略](#51-分页策略)
  - [5.2 过滤和排序](#52-过滤和排序)
- [6. HATEOAS](#6-hateoas)
  - [6.1 超媒体链接](#61-超媒体链接)
  - [6.2 资源关系](#62-资源关系)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API RESTful 规范定义了 API 在 RESTful 架构下的设计和实现，从资源设计到状态码响应
，从版本控制到 HATEOAS。

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

---

## 2. 资源设计

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

## 3. 状态码和响应

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

## 4. 版本控制

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

## 5. 分页和过滤

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

## 6. HATEOAS

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

## 7. 相关文档

- **[API 标准化规范](../25-api-standardization/api-standardization.md)** -
  RESTful 标准
- **[API 版本管理](../23-api-versioning/api-versioning.md)** - RESTful 版本控制
- **[API 性能优化](../14-api-performance/api-performance.md)** - RESTful 性能优
  化
- **[最佳实践](../08-best-practices/best-practices.md)** - RESTful 最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
