# API 目录规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 目录架构](#11-目录架构)
- [2. 目录结构](#2-目录结构)
  - [2.1 分类体系](#21-分类体系)
  - [2.2 标签体系](#22-标签体系)
- [3. API 注册](#3-api-注册)
  - [3.1 注册流程](#31-注册流程)
  - [3.2 元数据管理](#32-元数据管理)
- [4. API 搜索](#4-api-搜索)
  - [4.1 搜索功能](#41-搜索功能)
  - [4.2 过滤功能](#42-过滤功能)
- [5. 目录管理](#5-目录管理)
  - [5.1 版本管理](#51-版本管理)
  - [5.2 权限管理](#52-权限管理)
- [6. 目录同步](#6-目录同步)
  - [6.1 同步策略](#61-同步策略)
  - [6.2 同步监控](#62-同步监控)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 目录规范定义了 API 在目录场景下的设计和实现，从目录结构到 API 注册，从 API
搜索到目录管理。

### 1.1 目录架构

```text
API 提供者（API Provider）
  ↓
API 注册（API Registration）
  ↓
API 目录（API Catalog）
  ↓
API 消费者（API Consumer）
```

---

## 2. 目录结构

### 2.1 分类体系

**分类体系定义**：

```yaml
apiVersion: api.example.com/v1
kind: APICategory
metadata:
  name: api-category-system
spec:
  categories:
    - name: "payment"
      description: "Payment related APIs"
      subcategories:
        - name: "payment-processing"
        - name: "payment-gateway"
        - name: "payment-verification"
    - name: "order"
      description: "Order related APIs"
      subcategories:
        - name: "order-management"
        - name: "order-tracking"
    - name: "inventory"
      description: "Inventory related APIs"
      subcategories:
        - name: "inventory-management"
        - name: "stock-tracking"
```

**分类管理实现**：

```go
package main

type APICategory struct {
    ID          string
    Name        string
    Description string
    ParentID    string
    Subcategories []*APICategory
}

type CategoryManager struct {
    categories map[string]*APICategory
}

func (m *CategoryManager) AddCategory(category *APICategory) error {
    if category.ParentID != "" {
        parent := m.categories[category.ParentID]
        if parent == nil {
            return fmt.Errorf("parent category not found: %s", category.ParentID)
        }
        parent.Subcategories = append(parent.Subcategories, category)
    }

    m.categories[category.ID] = category
    return nil
}

func (m *CategoryManager) GetCategoryTree() []*APICategory {
    var roots []*APICategory
    for _, category := range m.categories {
        if category.ParentID == "" {
            roots = append(roots, category)
        }
    }
    return roots
}
```

### 2.2 标签体系

**标签体系定义**：

```yaml
apiVersion: api.example.com/v1
kind: APITag
metadata:
  name: api-tag-system
spec:
  tags:
    - name: "payment"
      description: "Payment related"
      color: "#FF5733"
    - name: "secure"
      description: "Secure API"
      color: "#33FF57"
    - name: "public"
      description: "Public API"
      color: "#3357FF"
    - name: "deprecated"
      description: "Deprecated API"
      color: "#FF33F5"
```

---

## 3. API 注册

### 3.1 注册流程

**注册流程配置**：

```yaml
apiVersion: api.example.com/v1
kind: APIRegistrationFlow
metadata:
  name: payment-api-registration
spec:
  steps:
    - step: 1
      action: "Provide API information"
      required:
        - name
        - version
        - endpoint
    - step: 2
      action: "Upload API specification"
      formats:
        - openapi
        - graphql
        - grpc
    - step: 3
      action: "Set metadata"
      fields:
        - categories
        - tags
        - description
    - step: 4
      action: "Review and publish"
```

**注册实现**：

```go
package main

type APIRegistration struct {
    ID          string
    Name        string
    Version     string
    Endpoint    string
    Specification string
    Metadata    APIMetadata
    Status      string
}

type CatalogManager struct {
    apis map[string]*APIRegistration
}

func (m *CatalogManager) Register(registration APIRegistration) error {
    // 验证 API 信息
    if err := m.validateRegistration(registration); err != nil {
        return err
    }

    // 解析 API 规范
    spec, err := m.parseSpecification(registration.Specification)
    if err != nil {
        return err
    }

    // 提取元数据
    metadata := m.extractMetadata(spec)
    registration.Metadata = metadata

    // 保存到目录
    registration.ID = generateID()
    registration.Status = "pending"
    m.apis[registration.ID] = &registration

    return nil
}

func (m *CatalogManager) validateRegistration(registration APIRegistration) error {
    if registration.Name == "" {
        return fmt.Errorf("API name is required")
    }
    if registration.Version == "" {
        return fmt.Errorf("API version is required")
    }
    if registration.Endpoint == "" {
        return fmt.Errorf("API endpoint is required")
    }
    return nil
}
```

### 3.2 元数据管理

**元数据管理实现**：

```go
package main

type APIMetadata struct {
    Name        string
    Version     string
    Description string
    Provider    string
    Categories  []string
    Tags        []string
    Endpoints   []EndpointMetadata
    Schemas     []SchemaMetadata
}

type EndpointMetadata struct {
    Path        string
    Method      string
    Description string
    Parameters  []ParameterMetadata
    Responses   []ResponseMetadata
}

func (m *CatalogManager) extractMetadata(spec interface{}) APIMetadata {
    metadata := APIMetadata{}

    // 从 OpenAPI 规范提取元数据
    if openapiSpec, ok := spec.(*OpenAPISpec); ok {
        metadata.Name = openapiSpec.Info.Title
        metadata.Version = openapiSpec.Info.Version
        metadata.Description = openapiSpec.Info.Description

        for path, pathItem := range openapiSpec.Paths {
            for method, operation := range pathItem.Operations {
                endpoint := EndpointMetadata{
                    Path:        path,
                    Method:      method,
                    Description: operation.Summary,
                }
                metadata.Endpoints = append(metadata.Endpoints, endpoint)
            }
        }
    }

    return metadata
}
```

---

## 4. API 搜索

### 4.1 搜索功能

**搜索实现**：

```go
package main

import (
    "strings"
)

type SearchQuery struct {
    Query      string
    Categories []string
    Tags       []string
    Provider   string
    Version    string
}

type SearchEngine struct {
    catalog *CatalogManager
    index   *SearchIndex
}

func (e *SearchEngine) Search(query SearchQuery) ([]*APIRegistration, error) {
    // 构建搜索条件
    conditions := e.buildConditions(query)

    // 从索引搜索
    results := e.index.Search(conditions)

    // 排序和过滤
    sorted := e.sortResults(results, query.Query)

    return sorted, nil
}

func (e *SearchEngine) buildConditions(query SearchQuery) SearchConditions {
    conditions := SearchConditions{}

    if query.Query != "" {
        conditions.TextQuery = query.Query
    }

    if len(query.Categories) > 0 {
        conditions.Categories = query.Categories
    }

    if len(query.Tags) > 0 {
        conditions.Tags = query.Tags
    }

    if query.Provider != "" {
        conditions.Provider = query.Provider
    }

    return conditions
}
```

### 4.2 过滤功能

**过滤实现**：

```go
package main

type FilterOptions struct {
    Categories  []string
    Tags        []string
    Providers   []string
    Versions    []string
    Status      []string
    MinRating   float64
}

func (e *SearchEngine) Filter(apis []*APIRegistration, options FilterOptions) []*APIRegistration {
    var filtered []*APIRegistration

    for _, api := range apis {
        if e.matchesFilter(api, options) {
            filtered = append(filtered, api)
        }
    }

    return filtered
}

func (e *SearchEngine) matchesFilter(api *APIRegistration, options FilterOptions) bool {
    // 分类过滤
    if len(options.Categories) > 0 {
        if !containsAny(api.Metadata.Categories, options.Categories) {
            return false
        }
    }

    // 标签过滤
    if len(options.Tags) > 0 {
        if !containsAny(api.Metadata.Tags, options.Tags) {
            return false
        }
    }

    // 提供商过滤
    if len(options.Providers) > 0 {
        if !contains(options.Providers, api.Metadata.Provider) {
            return false
        }
    }

    // 版本过滤
    if len(options.Versions) > 0 {
        if !contains(options.Versions, api.Version) {
            return false
        }
    }

    // 状态过滤
    if len(options.Status) > 0 {
        if !contains(options.Status, api.Status) {
            return false
        }
    }

    return true
}
```

---

## 5. 目录管理

### 5.1 版本管理

**版本管理实现**：

```go
package main

type APIVersionManager struct {
    catalog *CatalogManager
}

func (m *APIVersionManager) GetVersions(apiName string) ([]string, error) {
    var versions []string

    for _, api := range m.catalog.apis {
        if api.Name == apiName {
            versions = append(versions, api.Version)
        }
    }

    return versions, nil
}

func (m *APIVersionManager) GetLatestVersion(apiName string) (string, error) {
    versions, err := m.GetVersions(apiName)
    if err != nil {
        return "", err
    }

    if len(versions) == 0 {
        return "", fmt.Errorf("no versions found for API: %s", apiName)
    }

    // 排序版本号
    sorted := sortVersions(versions)
    return sorted[len(sorted)-1], nil
}
```

### 5.2 权限管理

**权限管理配置**：

```yaml
apiVersion: api.example.com/v1
kind: CatalogPermission
metadata:
  name: payment-api-catalog-permission
spec:
  permissions:
    - user: "admin"
      actions:
        - "read"
        - "write"
        - "delete"
    - user: "developer"
      actions:
        - "read"
        - "write"
    - user: "viewer"
      actions:
        - "read"
```

---

## 6. 目录同步

### 6.1 同步策略

**同步策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: CatalogSync
metadata:
  name: payment-api-catalog-sync
spec:
  strategy: "incremental"
  sources:
    - type: "git"
      repository: "https://github.com/example/api-specs"
      branch: "main"
      path: "apis/"
    - type: "registry"
      endpoint: "https://registry.example.com"
  schedule: "0 */6 * * *" # 每6小时
```

### 6.2 同步监控

**同步监控配置**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: catalog-sync-metrics
spec:
  groups:
    - name: catalog_sync
      rules:
        - record: catalog:sync_total
          expr: |
            sum(rate(catalog_syncs_total[5m])) by (source, status)
        - record: catalog:sync_duration_seconds
          expr: |
            histogram_quantile(0.95, sum(rate(catalog_sync_duration_seconds_bucket[5m])) by (source, le))
```

---

## 7. 相关文档

- **[API 发现规范](../75-api-discovery/api-discovery.md)** - API 发现
- **[API 市场规范](../69-api-marketplace/api-marketplace.md)** - API 市场
- **[API 管理规范](../58-api-api-management/api-api-management.md)** - API 管理
- **[最佳实践](../08-best-practices/best-practices.md)** - 目录最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
