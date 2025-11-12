# API 国际化规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 国际化架构](#11-国际化架构)
- [2 语言支持](#2-语言支持)
  - [2.1 语言检测](#21-语言检测)
  - [2.2 语言切换](#22-语言切换)
- [3 本地化](#3-本地化)
  - [3.1 文本本地化](#31-文本本地化)
  - [3.2 日期时间本地化](#32-日期时间本地化)
  - [3.3 数字格式本地化](#33-数字格式本地化)
- [4 内容协商](#4-内容协商)
  - [4.1 Accept-Language](#41-accept-language)
  - [4.2 Content-Language](#42-content-language)
- [5 时区处理](#5-时区处理)
  - [5.1 时区检测](#51-时区检测)
  - [5.2 时区转换](#52-时区转换)
- [6 国际化最佳实践](#6-国际化最佳实践)
  - [6.1 字符编码](#61-字符编码)
  - [6.2 文本方向](#62-文本方向)
- [7 形式化定义与理论基础](#7-形式化定义与理论基础)
  - [7.1 API 国际化形式化模型](#71-api-国际化形式化模型)
  - [7.2 本地化形式化](#72-本地化形式化)
  - [7.3 内容协商形式化](#73-内容协商形式化)
- [8 相关文档](#8-相关文档)

---

## 1 概述

API 国际化规范定义了 API 在国际化场景下的设计和实现，从语言支持到本地化，从内容
协商到时区处理。本文档基于形式化方法，提供严格的数学定义和推理论证，分析 API 国
际化的理论基础和实践方法。

**参考标准**：

- [RFC 5646](https://tools.ietf.org/html/rfc5646) - 语言标签
- [Unicode](https://www.unicode.org/) - Unicode 字符编码
- [i18n Best Practices](https://www.w3.org/International/techniques/developing-specs) -
  国际化最佳实践
- [Locale Data](https://www.unicode.org/cldr/) - CLDR 本地化数据
- [Content Negotiation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation) -
  内容协商

### 1.1 国际化架构

```text
API 请求（API Request）
  ↓
语言检测（Language Detection）
  ↓
内容本地化（Content Localization）
  ↓
API 响应（API Response）
```

---

## 2 语言支持

### 2.1 语言检测

**语言检测实现**：

```go
package main

import (
    "net/http"
    "strings"
    "golang.org/x/text/language"
)

func DetectLanguage(r *http.Request) language.Tag {
    // 1. Check Accept-Language header
    acceptLang := r.Header.Get("Accept-Language")
    if acceptLang != "" {
        tags, _, err := language.ParseAcceptLanguage(acceptLang)
        if err == nil && len(tags) > 0 {
            return tags[0]
        }
    }

    // 2. Check query parameter
    if lang := r.URL.Query().Get("lang"); lang != "" {
        tag, err := language.Parse(lang)
        if err == nil {
            return tag
        }
    }

    // 3. Default to English
    return language.English
}

func LanguageMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        lang := DetectLanguage(r)
        ctx := context.WithValue(r.Context(), "language", lang)
        next(w, r.WithContext(ctx))
    }
}
```

### 2.2 语言切换

**语言切换 API**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: language-switching-api
spec:
  paths:
    /api/v1/locale:
      get:
        summary: Get current locale
        responses:
          "200":
            description: Current locale
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    language:
                      type: string
                      example: "en"
                    region:
                      type: string
                      example: "US"
      put:
        summary: Set locale
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  language:
                    type: string
                    example: "zh"
                  region:
                    type: string
                    example: "CN"
```

---

## 3 本地化

### 3.1 文本本地化

**文本本地化实现**：

```go
package main

import (
    "golang.org/x/text/message"
    "golang.org/x/text/language"
)

var translations = map[string]map[string]string{
    "en": {
        "payment.success": "Payment successful",
        "payment.failed": "Payment failed",
        "order.created": "Order created",
    },
    "zh": {
        "payment.success": "支付成功",
        "payment.failed": "支付失败",
        "order.created": "订单已创建",
    },
    "ja": {
        "payment.success": "支払い成功",
        "payment.failed": "支払い失敗",
        "order.created": "注文が作成されました",
    },
}

func Translate(lang language.Tag, key string) string {
    langStr := lang.String()
    if translations[langStr] != nil {
        if text := translations[langStr][key]; text != "" {
            return text
        }
    }
    // Fallback to English
    if translations["en"] != nil {
        return translations["en"][key]
    }
    return key
}
```

### 3.2 日期时间本地化

**日期时间本地化实现**：

```go
package main

import (
    "time"
    "golang.org/x/text/language"
    "golang.org/x/text/message"
)

func FormatDateTime(lang language.Tag, t time.Time) string {
    printer := message.NewPrinter(lang)

    switch lang {
    case language.Chinese:
        return printer.Sprintf("%d年%d月%d日 %d:%d:%d",
            t.Year(), t.Month(), t.Day(),
            t.Hour(), t.Minute(), t.Second())
    case language.Japanese:
        return printer.Sprintf("%d年%d月%d日 %d:%d:%d",
            t.Year(), t.Month(), t.Day(),
            t.Hour(), t.Minute(), t.Second())
    default:
        return t.Format("2006-01-02 15:04:05")
    }
}
```

### 3.3 数字格式本地化

**数字格式本地化实现**：

```go
package main

import (
    "golang.org/x/text/language"
    "golang.org/x/text/message"
    "golang.org/x/text/number"
)

func FormatNumber(lang language.Tag, value float64) string {
    printer := message.NewPrinter(lang)
    return printer.Sprintf("%v", number.Decimal(value))
}

func FormatCurrency(lang language.Tag, amount float64, currency string) string {
    printer := message.NewPrinter(lang)

    switch currency {
    case "USD":
        return printer.Sprintf("$%.2f", amount)
    case "CNY":
        return printer.Sprintf("¥%.2f", amount)
    case "JPY":
        return printer.Sprintf("¥%.0f", amount)
    default:
        return printer.Sprintf("%.2f %s", amount, currency)
    }
}
```

---

## 4 内容协商

### 4.1 Accept-Language

**Accept-Language 处理**：

```go
package main

import (
    "net/http"
    "golang.org/x/text/language"
)

func HandleAcceptLanguage(r *http.Request) language.Tag {
    acceptLang := r.Header.Get("Accept-Language")
    if acceptLang == "" {
        return language.English
    }

    tags, _, err := language.ParseAcceptLanguage(acceptLang)
    if err != nil || len(tags) == 0 {
        return language.English
    }

    // Return the highest priority language
    return tags[0]
}
```

### 4.2 Content-Language

**Content-Language 设置**：

```go
package main

import (
    "net/http"
    "golang.org/x/text/language"
)

func SetContentLanguage(w http.ResponseWriter, lang language.Tag) {
    w.Header().Set("Content-Language", lang.String())
}

func LocalizedHandler(w http.ResponseWriter, r *http.Request) {
    lang := DetectLanguage(r)
    SetContentLanguage(w, lang)

    response := map[string]interface{}{
        "message": Translate(lang, "payment.success"),
        "language": lang.String(),
    }

    json.NewEncoder(w).Encode(response)
}
```

---

## 5 时区处理

### 5.1 时区检测

**时区检测实现**：

```go
package main

import (
    "time"
    "net/http"
)

func DetectTimezone(r *http.Request) *time.Location {
    // 1. Check header
    if tz := r.Header.Get("X-Timezone"); tz != "" {
        loc, err := time.LoadLocation(tz)
        if err == nil {
            return loc
        }
    }

    // 2. Check query parameter
    if tz := r.URL.Query().Get("timezone"); tz != "" {
        loc, err := time.LoadLocation(tz)
        if err == nil {
            return loc
        }
    }

    // 3. Default to UTC
    return time.UTC
}
```

### 5.2 时区转换

**时区转换实现**：

```go
package main

import "time"

func ConvertToTimezone(t time.Time, tz *time.Location) time.Time {
    return t.In(tz)
}

func FormatWithTimezone(t time.Time, tz *time.Location) string {
    return t.In(tz).Format(time.RFC3339)
}
```

---

## 6 国际化最佳实践

### 6.1 字符编码

**字符编码配置**：

```yaml
apiVersion: api.example.com/v1
kind: APIEncoding
metadata:
  name: payment-api-encoding
spec:
  defaultEncoding: "UTF-8"
  supportedEncodings:
    - "UTF-8"
    - "UTF-16"
    - "ISO-8859-1"
  responseEncoding: "UTF-8"
```

### 6.2 文本方向

**文本方向处理**：

```go
package main

import (
    "golang.org/x/text/language"
)

func GetTextDirection(lang language.Tag) string {
    // RTL languages
    rtlLanguages := []string{"ar", "he", "fa", "ur"}

    langStr := lang.String()
    for _, rtl := range rtlLanguages {
        if langStr == rtl || strings.HasPrefix(langStr, rtl+"-") {
            return "rtl"
        }
    }

    return "ltr"
}
```

---

## 7 形式化定义与理论基础

### 7.1 API 国际化形式化模型

**定义 7.1（API 国际化）**：API 国际化是一个四元组：

```text
API_Internationalization = ⟨Language_Support, Localization, Content_Negotiation, Timezone_Handling⟩
```

其中：

- **Language_Support**：语言支持 `Language_Support: Request → Language`
- **Localization**：本地化 `Localization: Content × Locale → Localized_Content`
- **Content_Negotiation**：内容协商
  `Content_Negotiation: Request × Available_Languages → Language`
- **Timezone_Handling**：时区处理
  `Timezone_Handling: DateTime × Timezone → Localized_DateTime`

**定义 7.2（本地化）**：本地化是一个函数：

```text
Localize: Content × Locale → Localized_Content
```

**定理 7.1（国际化完备性）**：如果支持所有语言，则国际化完备：

```text
Support_All_Languages(API) ⟹ Complete_Internationalization(API)
```

**证明**：如果支持所有语言，则所有用户都可以使用 API，因此国际化完备。□

### 7.2 本地化形式化

**定义 7.3（文本本地化）**：文本本地化是一个函数：

```text
Localize_Text: Text × Locale → Localized_Text
```

**定义 7.4（日期时间本地化）**：日期时间本地化是一个函数：

```text
Localize_DateTime: DateTime × Locale → Localized_DateTime
```

**定理 7.2（本地化与用户体验）**：本地化提高用户体验：

```text
Localization(API) ⟹ User_Experience(API) ↑
```

**证明**：本地化使用用户熟悉的语言和格式，因此用户体验提高。□

### 7.3 内容协商形式化

**定义 7.5（内容协商）**：内容协商是一个函数：

```text
Negotiate_Content: Request × Available_Languages → Selected_Language
```

**定义 7.6（语言匹配）**：语言匹配是一个函数：

```text
Match_Language: Requested_Language × Available_Languages → Matched_Language
```

**定理 7.3（内容协商最优性）**：内容协商选择最佳匹配语言：

```text
Negotiate_Content(Request) = Best_Match(Requested_Language, Available_Languages)
```

**证明**：内容协商根据 Accept-Language 头选择最佳匹配语言，因此选择最优。□

---

## 8 相关文档

- **[API 标准化规范](../25-api-standardization/api-standardization.md)** - API
  标准化
- **[API 设计规范](../57-api-api-design/api-api-design.md)** - API 设计
- **[最佳实践](../08-best-practices/best-practices.md)** - 国际化最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
