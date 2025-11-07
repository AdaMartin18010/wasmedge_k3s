# API 授权规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 授权架构](#11-授权架构)
- [2. 授权模型](#2-授权模型)
  - [2.1 RBAC](#21-rbac)
  - [2.2 ABAC](#22-abac)
  - [2.3 基于策略的授权](#23-基于策略的授权)
- [3. 权限定义](#3-权限定义)
  - [3.1 权限模型](#31-权限模型)
  - [3.2 权限继承](#32-权限继承)
- [4. 授权检查](#4-授权检查)
  - [4.1 授权中间件](#41-授权中间件)
  - [4.2 授权决策](#42-授权决策)
- [5. 权限管理](#5-权限管理)
  - [5.1 角色管理](#51-角色管理)
  - [5.2 权限分配](#52-权限分配)
- [6. 授权审计](#6-授权审计)
  - [6.1 授权日志](#61-授权日志)
  - [6.2 授权分析](#62-授权分析)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 授权规范定义了 API 在授权场景下的设计和实现，从授权模型到权限定义，从授权检
查到授权审计。

### 1.1 授权架构

```text
API 请求（API Request）
  ↓
授权检查（Authorization Check）
  ↓
权限验证（Permission Verification）
  ↓
授权决策（Authorization Decision）
```

---

## 2. 授权模型

### 2.1 RBAC

**RBAC 配置**：

```yaml
apiVersion: api.example.com/v1
kind: RBACPolicy
metadata:
  name: payment-api-rbac
spec:
  roles:
    - name: admin
      permissions:
        - resource: payments
          actions: [create, read, update, delete]
    - name: user
      permissions:
        - resource: payments
          actions: [create, read]
    - name: viewer
      permissions:
        - resource: payments
          actions: [read]
  roleBindings:
    - user: user_123
      role: admin
    - user: user_456
      role: user
```

**RBAC 实现**：

```go
package main

type Role string

const (
    RoleAdmin Role = "admin"
    RoleUser  Role = "user"
    RoleViewer Role = "viewer"
)

type Permission struct {
    Resource string
    Action   string
}

var rolePermissions = map[Role][]Permission{
    RoleAdmin: {
        {Resource: "payments", Action: "create"},
        {Resource: "payments", Action: "read"},
        {Resource: "payments", Action: "update"},
        {Resource: "payments", Action: "delete"},
    },
    RoleUser: {
        {Resource: "payments", Action: "create"},
        {Resource: "payments", Action: "read"},
    },
    RoleViewer: {
        {Resource: "payments", Action: "read"},
    },
}

func CheckPermission(userRole Role, resource, action string) bool {
    permissions := rolePermissions[userRole]
    for _, perm := range permissions {
        if perm.Resource == resource && perm.Action == action {
            return true
        }
    }
    return false
}
```

### 2.2 ABAC

**ABAC 配置**：

```yaml
apiVersion: api.example.com/v1
kind: ABACPolicy
metadata:
  name: payment-api-abac
spec:
  rules:
    - name: owner_access
      condition: "user.id == resource.owner_id"
      effect: allow
    - name: department_access
      condition: "user.department == resource.department"
      effect: allow
    - name: amount_limit
      condition: "resource.amount <= user.max_amount"
      effect: allow
```

### 2.3 基于策略的授权

**OPA 策略**：

```rego
package api.authorization

import rego.v1

default allow := false

allow if {
    input.method == "GET"
    input.path == ["api", "v1", "payments"]
    input.user.role == "viewer"
}

allow if {
    input.method == "POST"
    input.path == ["api", "v1", "payments"]
    input.user.role == "user"
    input.body.amount <= input.user.max_amount
}

allow if {
    input.method == "DELETE"
    input.path == ["api", "v1", "payments"]
    input.user.role == "admin"
}
```

---

## 3. 权限定义

### 3.1 权限模型

**权限模型定义**：

```yaml
apiVersion: api.example.com/v1
kind: PermissionModel
metadata:
  name: payment-api-permissions
spec:
  resources:
    - name: payments
      actions:
        - create
        - read
        - update
        - delete
        - refund
  permissions:
    - name: payments:create
      resource: payments
      action: create
    - name: payments:read
      resource: payments
      action: read
    - name: payments:update
      resource: payments
      action: update
    - name: payments:delete
      resource: payments
      action: delete
    - name: payments:refund
      resource: payments
      action: refund
```

### 3.2 权限继承

**权限继承配置**：

```yaml
apiVersion: api.example.com/v1
kind: PermissionInheritance
metadata:
  name: payment-api-permission-inheritance
spec:
  hierarchy:
    - role: admin
      inherits: []
      permissions:
        - payments:*
    - role: user
      inherits: [viewer]
      permissions:
        - payments:create
        - payments:update
    - role: viewer
      inherits: []
      permissions:
        - payments:read
```

---

## 4. 授权检查

### 4.1 授权中间件

**授权中间件实现**：

```go
package main

import (
    "net/http"
    "strings"
)

func AuthorizationMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        user := getUserFromContext(r.Context())
        resource := extractResource(r.URL.Path)
        action := mapHTTPMethodToAction(r.Method)

        if !checkPermission(user, resource, action) {
            http.Error(w, "Forbidden", http.StatusForbidden)
            return
        }

        next(w, r)
    }
}

func checkPermission(user *User, resource, action string) bool {
    // 实现权限检查逻辑
    return true
}
```

### 4.2 授权决策

**授权决策实现**：

```go
type AuthorizationDecision struct {
    Allowed bool
    Reason  string
}

func MakeAuthorizationDecision(user *User, resource, action string, context map[string]interface{}) *AuthorizationDecision {
    // RBAC 检查
    if checkRBAC(user, resource, action) {
        return &AuthorizationDecision{Allowed: true, Reason: "RBAC"}
    }

    // ABAC 检查
    if checkABAC(user, resource, action, context) {
        return &AuthorizationDecision{Allowed: true, Reason: "ABAC"}
    }

    // 策略检查
    if checkPolicy(user, resource, action, context) {
        return &AuthorizationDecision{Allowed: true, Reason: "Policy"}
    }

    return &AuthorizationDecision{Allowed: false, Reason: "No permission"}
}
```

---

## 5. 权限管理

### 5.1 角色管理

**角色管理 API**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: role-management-api
spec:
  paths:
    /api/v1/roles:
      get:
        summary: List roles
      post:
        summary: Create role
    /api/v1/roles/{role_id}:
      get:
        summary: Get role
      put:
        summary: Update role
      delete:
        summary: Delete role
```

### 5.2 权限分配

**权限分配配置**：

```yaml
apiVersion: api.example.com/v1
kind: PermissionAssignment
metadata:
  name: payment-api-permission-assignment
spec:
  assignments:
    - user: user_123
      role: admin
      expiresAt: null
    - user: user_456
      role: user
      expiresAt: "2026-11-07T00:00:00Z"
    - user: user_789
      permissions:
        - payments:read
        - payments:create
      expiresAt: null
```

---

## 6. 授权审计

### 6.1 授权日志

**授权日志格式**：

```json
{
  "timestamp": "2025-11-07T10:00:00.123Z",
  "event": "authorization_decision",
  "user_id": "user_123",
  "resource": "payments",
  "action": "delete",
  "decision": "allowed",
  "reason": "RBAC",
  "request_id": "req_1234567890"
}
```

### 6.2 授权分析

**授权分析配置**：

```yaml
apiVersion: api.example.com/v1
kind: AuthorizationAnalysis
metadata:
  name: payment-api-authorization-analysis
spec:
  metrics:
    - name: authorization_success_rate
      type: rate
    - name: authorization_failure_rate
      type: rate
    - name: most_common_permissions
      type: top_n
      n: 10
  timeRange: "30d"
```

---

## 7. 相关文档

- **[API 安全规范](../11-api-security/api-security.md)** - API 安全
- **[API 认证规范](../61-api-authentication/api-authentication.md)** - API 认证
- **[API 安全测试](../54-api-security-testing/api-security-testing.md)** - 授权
  测试
- **[最佳实践](../08-best-practices/best-practices.md)** - 授权最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
