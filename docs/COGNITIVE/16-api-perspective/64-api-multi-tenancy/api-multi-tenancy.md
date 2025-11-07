# API 多租户规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 多租户架构](#11-多租户架构)
- [2. 租户隔离](#2-租户隔离)
  - [2.1 数据隔离](#21-数据隔离)
  - [2.2 计算隔离](#22-计算隔离)
  - [2.3 网络隔离](#23-网络隔离)
- [3. 租户识别](#3-租户识别)
  - [3.1 租户标识](#31-租户标识)
  - [3.2 租户上下文](#32-租户上下文)
- [4. 租户管理](#4-租户管理)
  - [4.1 租户创建](#41-租户创建)
  - [4.2 租户配置](#42-租户配置)
  - [4.3 租户删除](#43-租户删除)
- [5. 资源配额](#5-资源配额)
  - [5.1 配额定义](#51-配额定义)
  - [5.2 配额执行](#52-配额执行)
- [6. 多租户监控](#6-多租户监控)
  - [6.1 租户指标](#61-租户指标)
  - [6.2 租户告警](#62-租户告警)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 多租户规范定义了 API 在多租户场景下的设计和实现，从租户隔离到租户识别，从租
户管理到资源配额。

### 1.1 多租户架构

```text
API 请求（API Request）
  ↓
租户识别（Tenant Identification）
  ↓
租户隔离（Tenant Isolation）
  ↓
资源配额（Resource Quota）
  ↓
API 处理（API Processing）
```

---

## 2. 租户隔离

### 2.1 数据隔离

**数据隔离策略**：

```yaml
apiVersion: api.example.com/v1
kind: TenantDataIsolation
metadata:
  name: payment-api-data-isolation
spec:
  strategy: "database_per_tenant"
  isolation:
    - level: "database"
      description: "Each tenant has separate database"
    - level: "schema"
      description: "Each tenant has separate schema"
    - level: "row"
      description: "Tenant ID in each row"
  dataRetention:
    perTenant: true
    retentionPolicy: "tenant_specific"
```

**数据隔离实现**：

```go
package main

import (
    "gorm.io/gorm"
)

type TenantAwareModel struct {
    TenantID string `gorm:"index"`
}

func (m *TenantAwareModel) BeforeCreate(tx *gorm.DB) error {
    tenantID := getTenantIDFromContext(tx.Statement.Context)
    m.TenantID = tenantID
    return nil
}

func (m *TenantAwareModel) ScopeTenant(tenantID string) func(*gorm.DB) *gorm.DB {
    return func(db *gorm.DB) *gorm.DB {
        return db.Where("tenant_id = ?", tenantID)
    }
}
```

### 2.2 计算隔离

**计算隔离配置**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  template:
    spec:
      containers:
        - name: payment-service
          image: payment-service:latest
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
      nodeSelector:
        tenant: "tenant-1"
```

### 2.3 网络隔离

**网络隔离配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service-tenant-isolation
spec:
  hosts:
    - payment-service
  http:
    - match:
        - headers:
            x-tenant-id:
              exact: "tenant-1"
      route:
        - destination:
            host: payment-service
            subset: tenant-1
    - match:
        - headers:
            x-tenant-id:
              exact: "tenant-2"
      route:
        - destination:
            host: payment-service
            subset: tenant-2
```

---

## 3. 租户识别

### 3.1 租户标识

**租户标识提取**：

```go
package main

import (
    "net/http"
    "context"
)

func ExtractTenantID(r *http.Request) (string, error) {
    // 1. Check header
    if tenantID := r.Header.Get("X-Tenant-ID"); tenantID != "" {
        return tenantID, nil
    }

    // 2. Check subdomain
    host := r.Host
    if tenantID := extractTenantFromSubdomain(host); tenantID != "" {
        return tenantID, nil
    }

    // 3. Check JWT claim
    if token := extractTokenFromRequest(r); token != nil {
        if tenantID := getTenantIDFromToken(token); tenantID != "" {
            return tenantID, nil
        }
    }

    return "", fmt.Errorf("tenant ID not found")
}

func TenantMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        tenantID, err := ExtractTenantID(r)
        if err != nil {
            http.Error(w, "Tenant ID required", http.StatusBadRequest)
            return
        }

        ctx := context.WithValue(r.Context(), "tenant_id", tenantID)
        next(w, r.WithContext(ctx))
    }
}
```

### 3.2 租户上下文

**租户上下文实现**：

```go
package main

import "context"

type TenantContext struct {
    TenantID   string
    TenantName string
    Plan       string
    Features   []string
}

func GetTenantContext(ctx context.Context) (*TenantContext, error) {
    tenantID, ok := ctx.Value("tenant_id").(string)
    if !ok {
        return nil, fmt.Errorf("tenant ID not found in context")
    }

    tenant, err := getTenantByID(tenantID)
    if err != nil {
        return nil, err
    }

    return &TenantContext{
        TenantID:   tenant.ID,
        TenantName: tenant.Name,
        Plan:       tenant.Plan,
        Features:   tenant.Features,
    }, nil
}
```

---

## 4. 租户管理

### 4.1 租户创建

**租户创建 API**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: tenant-management-api
spec:
  paths:
    /api/v1/tenants:
      post:
        summary: Create tenant
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  name:
                    type: string
                  plan:
                    type: string
                    enum: [free, basic, premium]
                  config:
                    type: object
        responses:
          "201":
            description: Tenant created
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    tenant_id:
                      type: string
                    status:
                      type: string
```

### 4.2 租户配置

**租户配置管理**：

```yaml
apiVersion: api.example.com/v1
kind: TenantConfig
metadata:
  name: tenant-1-config
spec:
  tenantId: "tenant-1"
  plan: "premium"
  features:
    - feature: "advanced_analytics"
      enabled: true
    - feature: "custom_branding"
      enabled: true
  limits:
    api_calls_per_minute: 10000
    storage_gb: 1000
    users: 10000
  settings:
    default_language: "en"
    timezone: "UTC"
```

### 4.3 租户删除

**租户删除流程**：

```yaml
apiVersion: api.example.com/v1
kind: TenantDeletion
metadata:
  name: tenant-1-deletion
spec:
  tenantId: "tenant-1"
  steps:
    - step: 1
      action: "Disable tenant access"
    - step: 2
      action: "Export tenant data"
    - step: 3
      action: "Delete tenant data"
    - step: 4
      action: "Release tenant resources"
  retention:
    dataRetention: "30d"
    backupRetention: "90d"
```

---

## 5. 资源配额

### 5.1 配额定义

**配额定义配置**：

```yaml
apiVersion: api.example.com/v1
kind: TenantQuota
metadata:
  name: tenant-1-quota
spec:
  tenantId: "tenant-1"
  quotas:
    - resource: "api_calls"
      limit: 10000
      period: "1m"
      action: "rate_limit"
    - resource: "storage"
      limit: 1000
      unit: "GB"
      action: "block"
    - resource: "users"
      limit: 10000
      action: "reject"
```

### 5.2 配额执行

**配额执行实现**：

```go
package main

import (
    "context"
    "fmt"
)

type QuotaChecker struct {
    quotaService QuotaService
}

func (qc *QuotaChecker) CheckQuota(ctx context.Context, tenantID string, resource string, amount int64) error {
    quota, err := qc.quotaService.GetQuota(ctx, tenantID, resource)
    if err != nil {
        return err
    }

    usage, err := qc.quotaService.GetUsage(ctx, tenantID, resource)
    if err != nil {
        return err
    }

    if usage+amount > quota.Limit {
        return fmt.Errorf("quota exceeded for resource %s", resource)
    }

    return nil
}

func (qc *QuotaChecker) IncrementUsage(ctx context.Context, tenantID string, resource string, amount int64) error {
    return qc.quotaService.IncrementUsage(ctx, tenantID, resource, amount)
}
```

---

## 6. 多租户监控

### 6.1 租户指标

**租户指标定义**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: tenant-metrics
spec:
  groups:
    - name: tenant_metrics
      rules:
        - record: tenant:api_calls_total
          expr: |
            sum(rate(http_requests_total[5m])) by (tenant_id)
        - record: tenant:api_errors_total
          expr: |
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (tenant_id)
        - record: tenant:api_latency_p95
          expr: |
            histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (tenant_id, le))
```

### 6.2 租户告警

**租户告警规则**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: tenant-alerts
spec:
  groups:
    - name: tenant_alerts
      rules:
        - alert: TenantQuotaExceeded
          expr: |
            tenant:quota_usage{resource="api_calls"} > 0.9
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Tenant quota exceeded"
            description:
              "Tenant {{ $labels.tenant_id }} has exceeded 90% of quota for {{
              $labels.resource }}"
```

---

## 7. 相关文档

- **[API 管理规范](../58-api-api-management/api-api-management.md)** - API 管理
- **[API 限流规范](../44-api-rate-limiting/api-rate-limiting.md)** - 租户限流
- **[API 监控规范](../20-api-monitoring/api-monitoring.md)** - 租户监控
- **[最佳实践](../08-best-practices/best-practices.md)** - 多租户最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
