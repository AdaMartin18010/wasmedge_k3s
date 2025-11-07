# API 数据验证规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 数据验证架构](#11-数据验证架构)
  - [1.2 API 数据验证在 API 规范中的位置](#12-api-数据验证在-api-规范中的位置)
- [2. 输入验证](#2-输入验证)
  - [2.1 Schema 验证](#21-schema-验证)
  - [2.2 类型验证](#22-类型验证)
  - [2.3 格式验证](#23-格式验证)
- [3. 业务规则验证](#3-业务规则验证)
  - [3.1 自定义验证器](#31-自定义验证器)
  - [3.2 条件验证](#32-条件验证)
- [4. 验证错误处理](#4-验证错误处理)
  - [4.1 错误格式](#41-错误格式)
  - [4.2 错误码定义](#42-错误码定义)
- [5. 验证性能优化](#5-验证性能优化)
  - [5.1 异步验证](#51-异步验证)
  - [5.2 缓存验证结果](#52-缓存验证结果)
- [6. 验证工具](#6-验证工具)
  - [6.1 JSON Schema](#61-json-schema)
  - [6.2 OpenAPI 验证](#62-openapi-验证)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 数据验证规范定义了 API 在数据验证场景下的设计和实现，从输入验证到业务规则验
证，从验证错误处理到性能优化。本文档基于形式化方法，提供严格的数学定义和推理论证
，分析 API 数据验证的理论基础和实践方法。

**参考标准**：

- [JSON Schema](https://json-schema.org/) - JSON Schema 验证规范
- [OpenAPI Validation](https://swagger.io/specification/) - OpenAPI 验证
- [Data Validation Best Practices](https://www.owasp.org/index.php/Input_Validation_Cheat_Sheet) -
  数据验证最佳实践
- [Schema Validation](https://ajv.js.org/) - Ajv JSON Schema 验证器
- [Input Sanitization](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) -
  输入清理

### 1.1 数据验证架构

```text
API 请求（API Request）
  ↓
输入验证（Input Validation）
  ↓
业务规则验证（Business Rule Validation）
  ↓
验证结果（Validation Result）
```

### 1.2 API 数据验证在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../07-formalization/formalization.md#21-api-规范四元组)）
，API 数据验证主要涉及 IDL 和 Security 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
            ↑                            ↑
    Data Validation (implementation)
```

API 数据验证在 API 规范中提供：

- **输入验证**：Schema 验证、类型验证、格式验证
- **业务规则验证**：自定义验证器、条件验证
- **安全防护**：防止注入攻击、数据污染
- **错误处理**：验证错误格式化和错误码定义

---

## 2. 输入验证

### 2.1 Schema 验证

**JSON Schema 定义**：

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "order_id": {
      "type": "string",
      "pattern": "^order_[a-zA-Z0-9]+$",
      "minLength": 10,
      "maxLength": 50
    },
    "amount": {
      "type": "integer",
      "minimum": 1,
      "maximum": 1000000
    },
    "currency": {
      "type": "string",
      "enum": ["USD", "EUR", "CNY"],
      "default": "USD"
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "required": ["order_id", "amount"]
}
```

**Go Schema 验证**：

```go
package main

import (
    "github.com/xeipuuv/gojsonschema"
)

func ValidateJSON(schema, document string) (bool, []error) {
    schemaLoader := gojsonschema.NewStringLoader(schema)
    documentLoader := gojsonschema.NewStringLoader(document)

    result, err := gojsonschema.Validate(schemaLoader, documentLoader)
    if err != nil {
        return false, []error{err}
    }

    if result.Valid() {
        return true, nil
    }

    var errors []error
    for _, desc := range result.Errors() {
        errors = append(errors, fmt.Errorf("%s", desc))
    }

    return false, errors
}
```

### 2.2 类型验证

**类型验证实现**：

```go
package main

import (
    "reflect"
    "strconv"
)

func ValidateType(value interface{}, expectedType string) error {
    switch expectedType {
    case "string":
        if _, ok := value.(string); !ok {
            return fmt.Errorf("expected string, got %T", value)
        }
    case "integer":
        switch v := value.(type) {
        case int, int32, int64:
            return nil
        case string:
            if _, err := strconv.Atoi(v); err != nil {
                return fmt.Errorf("invalid integer: %v", v)
            }
        default:
            return fmt.Errorf("expected integer, got %T", value)
        }
    case "number":
        if !isNumeric(value) {
            return fmt.Errorf("expected number, got %T", value)
        }
    case "boolean":
        if _, ok := value.(bool); !ok {
            return fmt.Errorf("expected boolean, got %T", value)
        }
    }
    return nil
}

func isNumeric(value interface{}) bool {
    switch value.(type) {
    case int, int32, int64, float32, float64:
        return true
    }
    return false
}
```

### 2.3 格式验证

**格式验证实现**：

```go
package main

import (
    "regexp"
    "net/mail"
    "net/url"
)

func ValidateFormat(value string, format string) error {
    switch format {
    case "email":
        _, err := mail.ParseAddress(value)
        return err
    case "uri":
        _, err := url.Parse(value)
        return err
    case "date-time":
        _, err := time.Parse(time.RFC3339, value)
        return err
    case "uuid":
        matched, _ := regexp.MatchString(
            "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            value,
        )
        if !matched {
            return fmt.Errorf("invalid UUID format")
        }
    }
    return nil
}
```

---

## 3. 业务规则验证

### 3.1 自定义验证器

**自定义验证器实现**：

```go
package main

type Validator interface {
    Validate(value interface{}) error
}

type PaymentAmountValidator struct {
    minAmount int64
    maxAmount int64
}

func (v *PaymentAmountValidator) Validate(value interface{}) error {
    amount, ok := value.(int64)
    if !ok {
        return fmt.Errorf("invalid amount type")
    }

    if amount < v.minAmount {
        return fmt.Errorf("amount too small: %d < %d", amount, v.minAmount)
    }

    if amount > v.maxAmount {
        return fmt.Errorf("amount too large: %d > %d", amount, v.maxAmount)
    }

    return nil
}

type PaymentValidator struct {
    validators []Validator
}

func (pv *PaymentValidator) Validate(payment *Payment) error {
    for _, validator := range pv.validators {
        if err := validator.Validate(payment.Amount); err != nil {
            return err
        }
    }
    return nil
}
```

### 3.2 条件验证

**条件验证配置**：

```yaml
apiVersion: api.example.com/v1
kind: ValidationRule
metadata:
  name: payment-validation-rules
spec:
  rules:
    - name: amount-limit
      condition: "amount > 0 && amount <= 10000"
      message: "Amount must be between 1 and 10000"
    - name: currency-validation
      condition: "currency in ['USD', 'EUR', 'CNY']"
      message: "Invalid currency"
    - name: order-exists
      condition: "orderExists(order_id)"
      message: "Order does not exist"
```

---

## 4. 验证错误处理

### 4.1 错误格式

**验证错误响应格式**：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "amount",
        "code": "INVALID_VALUE",
        "message": "Amount must be between 1 and 10000",
        "value": 0
      },
      {
        "field": "currency",
        "code": "INVALID_ENUM",
        "message": "Currency must be one of: USD, EUR, CNY",
        "value": "JPY"
      }
    ]
  }
}
```

### 4.2 错误码定义

**错误码规范**：

```yaml
apiVersion: api.example.com/v1
kind: ValidationErrorCode
metadata:
  name: validation-error-codes
spec:
  codes:
    - code: VALIDATION_ERROR
      description: General validation error
      httpStatus: 400
    - code: INVALID_TYPE
      description: Invalid data type
      httpStatus: 400
    - code: INVALID_FORMAT
      description: Invalid format
      httpStatus: 400
    - code: MISSING_REQUIRED
      description: Missing required field
      httpStatus: 400
    - code: OUT_OF_RANGE
      description: Value out of range
      httpStatus: 400
```

---

## 5. 验证性能优化

### 5.1 异步验证

**异步验证实现**：

```go
package main

import (
    "context"
    "sync"
)

type AsyncValidator struct {
    validators []Validator
}

func (av *AsyncValidator) ValidateAsync(ctx context.Context, value interface{}) <-chan error {
    errChan := make(chan error, len(av.validators))
    var wg sync.WaitGroup

    for _, validator := range av.validators {
        wg.Add(1)
        go func(v Validator) {
            defer wg.Done()
            if err := v.Validate(value); err != nil {
                select {
                case errChan <- err:
                case <-ctx.Done():
                    return
                }
            }
        }(validator)
    }

    go func() {
        wg.Wait()
        close(errChan)
    }()

    return errChan
}
```

### 5.2 缓存验证结果

**验证结果缓存**：

```go
type CachedValidator struct {
    validator Validator
    cache     CacheService
}

func (cv *CachedValidator) Validate(value interface{}) error {
    cacheKey := generateCacheKey(value)

    // 检查缓存
    if cached, err := cv.cache.Get(cacheKey); err == nil {
        if cached.(bool) {
            return nil
        }
        return fmt.Errorf("validation failed (cached)")
    }

    // 执行验证
    err := cv.validator.Validate(value)
    isValid := err == nil

    // 缓存结果
    cv.cache.Set(cacheKey, isValid, time.Hour)

    return err
}
```

---

## 6. 验证工具

### 6.1 JSON Schema

**JSON Schema 验证工具**：

```yaml
apiVersion: api.example.com/v1
kind: ValidationTool
metadata:
  name: json-schema-validator
spec:
  type: json-schema
  version: "draft-07"
  features:
    - type-validation
    - format-validation
    - enum-validation
    - custom-keywords
```

### 6.2 OpenAPI 验证

**OpenAPI 验证配置**：

```yaml
apiVersion: api.example.com/v1
kind: OpenAPIValidation
metadata:
  name: payment-api-validation
spec:
  openapi: "3.1.0"
  validation:
    enabled: true
    strict: true
    validateRequests: true
    validateResponses: true
```

---

## 7. 相关文档

- **[API 标准化规范](../25-api-standardization/api-standardization.md)** - 数据
  格式标准
- **[API 错误处理](../25-api-standardization/api-standardization.md)** - 错误处
  理标准
- **[API 性能优化](../14-api-performance/api-performance.md)** - 验证性能优化
- **[最佳实践](../08-best-practices/best-practices.md)** - 数据验证最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
