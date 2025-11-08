# API 认证规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 认证架构](#11-认证架构)
  - [1.2 API 认证在 API 规范中的位置](#12-api-认证在-api-规范中的位置)
- [2. 认证方式](#2-认证方式)
  - [2.1 API Key](#21-api-key)
  - [2.2 OAuth 2.0](#22-oauth-20)
  - [2.3 JWT](#23-jwt)
  - [2.4 mTLS](#24-mtls)
- [3. 认证流程](#3-认证流程)
  - [3.1 客户端凭证流程](#31-客户端凭证流程)
  - [3.2 授权码流程](#32-授权码流程)
  - [3.3 刷新令牌流程](#33-刷新令牌流程)
- [4. 令牌管理](#4-令牌管理)
  - [4.1 令牌生成](#41-令牌生成)
  - [4.2 令牌验证](#42-令牌验证)
  - [4.3 令牌撤销](#43-令牌撤销)
- [5. 安全最佳实践](#5-安全最佳实践)
  - [5.1 密钥管理](#51-密钥管理)
  - [5.2 令牌存储](#52-令牌存储)
- [6. 认证监控](#6-认证监控)
  - [6.1 认证指标](#61-认证指标)
  - [6.2 认证告警](#62-认证告警)
- [7. 形式化定义与理论基础](#7-形式化定义与理论基础)
  - [7.1 API 认证形式化模型](#71-api-认证形式化模型)
  - [7.2 认证流程形式化](#72-认证流程形式化)
  - [7.3 令牌安全形式化](#73-令牌安全形式化)
- [8. 相关文档](#8-相关文档)

---

## 1. 概述

API 认证规范定义了 API 在认证场景下的设计和实现，从认证方式到认证流程，从令牌管
理到安全最佳实践。本文档基于形式化方法，提供严格的数学定义和推理论证，分析 API
认证的理论基础和实践方法。

### 1.1 认证架构

```text
客户端（Client）
  ↓
认证请求（Authentication Request）
  ↓
认证服务（Authentication Service）
  ↓
令牌生成（Token Generation）
  ↓
API 调用（API Call with Token）
```

### 1.2 API 认证在 API 规范中的位置

API 认证在 API 规范四元组 `⟨IDL, Governance, Observability, Security⟩` 中主要涉
及 **Security** 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
                                    ↑
            API 认证属于 Security 维度
```

API 认证在 API 规范中提供：

- **认证方式**：API Key、OAuth 2.0、JWT、mTLS
- **认证流程**：客户端凭证、授权码、刷新令牌
- **令牌管理**：令牌生成、验证、撤销
- **安全实践**：密钥管理、令牌存储、安全监控

**参考标准**：

- [OAuth 2.0](https://oauth.net/2/) - OAuth 2.0 授权框架
- [JWT](https://jwt.io/) - JSON Web Token
- [mTLS](https://datatracker.ietf.org/doc/html/rfc8705) - 相互 TLS
- [API Key Best Practices](https://cloud.google.com/endpoints/docs/openapi/api-key-as-header) -
  API Key 最佳实践
- [Authentication Best Practices](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/) -
  认证最佳实践

---

## 2. 认证方式

### 2.1 API Key

**API Key 配置**：

```yaml
apiVersion: api.example.com/v1
kind: APIKey
metadata:
  name: payment-api-key
spec:
  key: "pk_live_1234567890abcdef"
  secret: "sk_live_1234567890abcdef"
  permissions:
    - payments:read
    - payments:write
  rateLimit: 1000
  expiresAt: "2026-11-07T00:00:00Z"
```

**API Key 验证**：

```go
package main

import (
    "net/http"
    "strings"
)

func APIKeyMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        apiKey := r.Header.Get("X-API-Key")
        if apiKey == "" {
            http.Error(w, "Missing API key", http.StatusUnauthorized)
            return
        }

        if !validateAPIKey(apiKey) {
            http.Error(w, "Invalid API key", http.StatusUnauthorized)
            return
        }

        next(w, r)
    }
}
```

### 2.2 OAuth 2.0

**OAuth 2.0 配置**：

```yaml
apiVersion: api.example.com/v1
kind: OAuth2Config
metadata:
  name: payment-api-oauth2
spec:
  clientId: "client_123"
  clientSecret: "secret_456"
  authorizationEndpoint: "https://auth.example.com/oauth/authorize"
  tokenEndpoint: "https://auth.example.com/oauth/token"
  scopes:
    - payments:read
    - payments:write
  grantTypes:
    - authorization_code
    - client_credentials
```

**OAuth 2.0 实现**：

```go
package main

import (
    "golang.org/x/oauth2"
)

var oauth2Config = &oauth2.Config{
    ClientID:     "client_123",
    ClientSecret: "secret_456",
    Scopes:       []string{"payments:read", "payments:write"},
    Endpoint: oauth2.Endpoint{
        AuthURL:  "https://auth.example.com/oauth/authorize",
        TokenURL: "https://auth.example.com/oauth/token",
    },
}

func GetAccessToken(code string) (*oauth2.Token, error) {
    return oauth2Config.Exchange(context.Background(), code)
}
```

### 2.3 JWT

**JWT 配置**：

```yaml
apiVersion: api.example.com/v1
kind: JWTConfig
metadata:
  name: payment-api-jwt
spec:
  issuer: "https://auth.example.com"
  audience: "payment-api"
  algorithm: RS256
  publicKey: |
    -----BEGIN PUBLIC KEY-----
    ...
    -----END PUBLIC KEY-----
  expiresIn: "1h"
```

**JWT 验证**：

```go
package main

import (
    "github.com/golang-jwt/jwt/v5"
)

func ValidateJWT(tokenString string) (*jwt.Token, error) {
    token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
        if _, ok := token.Method.(*jwt.SigningMethodRSA); !ok {
            return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
        }
        return publicKey, nil
    })

    if err != nil {
        return nil, err
    }

    if !token.Valid {
        return nil, fmt.Errorf("invalid token")
    }

    return token, nil
}
```

### 2.4 mTLS

**mTLS 配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: payment-api-mtls
spec:
  selector:
    matchLabels:
      app: payment-service
  mtls:
    mode: STRICT
```

---

## 3. 认证流程

### 3.1 客户端凭证流程

**客户端凭证流程**：

```yaml
apiVersion: api.example.com/v1
kind: ClientCredentialsFlow
metadata:
  name: payment-api-client-credentials
spec:
  grantType: client_credentials
  steps:
    - step: 1
      action: "Client sends credentials to token endpoint"
    - step: 2
      action: "Server validates credentials"
    - step: 3
      action: "Server issues access token"
    - step: 4
      action: "Client uses access token for API calls"
```

### 3.2 授权码流程

**授权码流程**：

```yaml
apiVersion: api.example.com/v1
kind: AuthorizationCodeFlow
metadata:
  name: payment-api-authorization-code
spec:
  grantType: authorization_code
  steps:
    - step: 1
      action: "Client redirects user to authorization endpoint"
    - step: 2
      action: "User authorizes client"
    - step: 3
      action: "Server redirects to client with authorization code"
    - step: 4
      action: "Client exchanges code for access token"
```

### 3.3 刷新令牌流程

**刷新令牌流程**：

```yaml
apiVersion: api.example.com/v1
kind: RefreshTokenFlow
metadata:
  name: payment-api-refresh-token
spec:
  grantType: refresh_token
  steps:
    - step: 1
      action: "Client sends refresh token to token endpoint"
    - step: 2
      action: "Server validates refresh token"
    - step: 3
      action: "Server issues new access token"
```

---

## 4. 令牌管理

### 4.1 令牌生成

**令牌生成实现**：

```go
package main

import (
    "github.com/golang-jwt/jwt/v5"
    "time"
)

func GenerateAccessToken(userID string, scopes []string) (string, error) {
    claims := jwt.MapClaims{
        "sub":    userID,
        "scopes": scopes,
        "exp":    time.Now().Add(time.Hour).Unix(),
        "iat":    time.Now().Unix(),
    }

    token := jwt.NewWithClaims(jwt.SigningMethodRS256, claims)
    return token.SignedString(privateKey)
}

func GenerateRefreshToken(userID string) (string, error) {
    claims := jwt.MapClaims{
        "sub": userID,
        "exp": time.Now().Add(24 * time.Hour * 7).Unix(), // 7 days
        "iat": time.Now().Unix(),
    }

    token := jwt.NewWithClaims(jwt.SigningMethodRS256, claims)
    return token.SignedString(privateKey)
}
```

### 4.2 令牌验证

**令牌验证实现**：

```go
func ValidateAccessToken(tokenString string) (*jwt.Token, error) {
    token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
        if _, ok := token.Method.(*jwt.SigningMethodRSA); !ok {
            return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
        }
        return publicKey, nil
    })

    if err != nil {
        return nil, err
    }

    if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
        // 检查过期时间
        if exp, ok := claims["exp"].(float64); ok {
            if time.Now().Unix() > int64(exp) {
                return nil, fmt.Errorf("token expired")
            }
        }

        return token, nil
    }

    return nil, fmt.Errorf("invalid token")
}
```

### 4.3 令牌撤销

**令牌撤销实现**：

```yaml
apiVersion: api.example.com/v1
kind: TokenRevocation
metadata:
  name: payment-api-token-revocation
spec:
  endpoint: "/api/v1/auth/revoke"
  methods:
    - POST
  requestBody:
    token: string
    token_type_hint: "access_token"
```

---

## 5. 安全最佳实践

### 5.1 密钥管理

**密钥管理配置**：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-keys
type: Opaque
data:
  api-key-1: <base64-encoded-key>
  api-key-2: <base64-encoded-key>
```

**密钥轮换**：

```yaml
apiVersion: api.example.com/v1
kind: KeyRotation
metadata:
  name: payment-api-key-rotation
spec:
  strategy: automatic
  interval: "90d"
  gracePeriod: "30d"
```

### 5.2 令牌存储

**令牌存储策略**：

```yaml
apiVersion: api.example.com/v1
kind: TokenStorage
metadata:
  name: payment-api-token-storage
spec:
  storage:
    accessToken:
      location: memory
      ttl: "1h"
    refreshToken:
      location: database
      ttl: "7d"
  encryption:
    algorithm: AES-256-GCM
    keyRotation: "90d"
```

---

## 6. 认证监控

### 6.1 认证指标

**认证指标定义**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: authentication-metrics
spec:
  groups:
    - name: authentication
      rules:
        - record: auth:success_rate
          expr: |
            rate(auth_requests_total{status="success"}[5m]) /
            rate(auth_requests_total[5m])
        - record: auth:failure_rate
          expr: |
            rate(auth_requests_total{status="failure"}[5m]) /
            rate(auth_requests_total[5m])
```

### 6.2 认证告警

**认证告警规则**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: authentication-alerts
spec:
  groups:
    - name: authentication_alerts
      rules:
        - alert: HighAuthFailureRate
          expr: |
            rate(auth_requests_total{status="failure"}[5m]) /
            rate(auth_requests_total[5m]) > 0.1
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High authentication failure rate"
            description:
              "Authentication failure rate is {{ $value | humanizePercentage }}"
```

---

## 7. 形式化定义与理论基础

### 7.1 API 认证形式化模型

**定义 7.1（API 认证）**：API 认证是一个四元组：

```text
API_Authentication = ⟨Auth_Method, Auth_Flow, Token_Management, Security_Practices⟩
```

其中：

- **Auth_Method**：认证方式 `Auth_Method: {API_Key, OAuth2, JWT, mTLS}`
- **Auth_Flow**：认证流程 `Auth_Flow: Client × Server → Token`
- **Token_Management**：令牌管理
  `Token_Management: Token → {Generate, Verify, Revoke}`
- **Security_Practices**：安全实践
  `Security_Practices: {Key_Management, Token_Storage}`

**定义 7.2（认证）**：认证是一个函数：

```text
Authenticate: Request × Credentials → {Success, Failure}
```

**定理 7.1（认证有效性）**：如果认证通过，则请求来自合法用户：

```text
Authenticate(Request, Credentials) = Success ⟹ Valid_User(Request)
```

**证明**：如果认证通过，则凭证有效，因此请求来自合法用户。□

### 7.2 认证流程形式化

**定义 7.3（OAuth 2.0 流程）**：OAuth 2.0 流程是一个函数：

```text
OAuth2_Flow: Client × Authorization_Server → Access_Token
```

**定义 7.4（令牌验证）**：令牌验证是一个函数：

```text
Verify_Token: Token × Secret → {Valid, Invalid}
```

**定理 7.2（令牌验证正确性）**：如果令牌有效，则验证通过：

```text
Valid(Token) ∧ Correct(Secret) ⟹ Verify_Token(Token, Secret) = Valid
```

**证明**：如果令牌有效且密钥正确，则令牌签名验证通过，因此验证通过。□

### 7.3 令牌安全形式化

**定义 7.5（令牌过期）**：令牌过期是一个函数：

```text
Token_Expired: Token × Current_Time → Bool
```

**定义 7.6（令牌安全）**：令牌安全是一个函数：

```text
Token_Security = f(Expiration, Encryption, Revocation)
```

**定理 7.3（令牌安全与认证安全）**：令牌安全提高认证安全：

```text
Token_Security(Token₁) > Token_Security(Token₂) ⟹ Auth_Security(API₁) > Auth_Security(API₂)
```

**证明**：令牌安全越高，令牌越难被滥用，因此认证安全越高。□

---

## 8. 相关文档

- **[API 安全规范](../11-api-security/api-security.md)** - API 安全
- **[API 安全测试](../54-api-security-testing/api-security-testing.md)** - 认证
  测试
- **[最佳实践](../00-foundation/05-best-practices.md)** - 认证最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
