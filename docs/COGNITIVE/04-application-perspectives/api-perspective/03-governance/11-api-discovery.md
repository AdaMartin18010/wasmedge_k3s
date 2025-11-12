# API 发现规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 发现架构](#11-发现架构)
  - [1.2 API 发现在 API 规范中的位置](#12-api-发现在-api-规范中的位置)
- [2 发现机制](#2-发现机制)
  - [2.1 服务注册](#21-服务注册)
  - [2.2 服务发现](#22-服务发现)
  - [2.3 健康检查](#23-健康检查)
- [3 发现协议](#3-发现协议)
  - [3.1 DNS 发现](#31-dns-发现)
  - [3.2 注册中心发现](#32-注册中心发现)
  - [3.3 配置中心发现](#33-配置中心发现)
- [4 元数据管理](#4-元数据管理)
  - [4.1 API 元数据](#41-api-元数据)
  - [4.2 版本元数据](#42-版本元数据)
- [5 发现优化](#5-发现优化)
  - [5.1 缓存策略](#51-缓存策略)
  - [5.2 负载均衡](#52-负载均衡)
- [6 发现监控](#6-发现监控)
  - [6.1 发现指标](#61-发现指标)
  - [6.2 发现告警](#62-发现告警)
- [7 形式化定义与理论基础](#7-形式化定义与理论基础)
  - [7.1 API 发现形式化模型](#71-api-发现形式化模型)
  - [7.2 服务发现形式化](#72-服务发现形式化)
  - [7.3 发现可靠性形式化](#73-发现可靠性形式化)
- [8 相关文档](#8-相关文档)

---

## 1 概述

API 发现规范定义了 API 在发现场景下的设计和实现，从发现机制到发现协议，从元数据
管理到发现优化。本文档基于形式化方法，提供严格的数学定义和推理论证，分析 API 发
现的理论基础和实践方法。

**参考标准**：

- [Service Discovery](https://microservices.io/patterns/service-registry.html) -
  服务发现模式
- [Consul Service Discovery](https://www.consul.io/docs/discovery) - Consul 服务
  发现
- [Kubernetes Service Discovery](https://kubernetes.io/docs/concepts/services-networking/service/) -
  Kubernetes 服务发现
- [DNS-Based Discovery](https://en.wikipedia.org/wiki/Service_discovery) - 基于
  DNS 的发现
- [Service Discovery Best Practices](https://www.nginx.com/blog/service-discovery-in-a-microservices-architecture/) -
  服务发现最佳实践

### 1.1 发现架构

```text
API 服务（API Service）
  ↓
服务注册（Service Registration）
  ↓
注册中心（Registry）
  ↓
服务发现（Service Discovery）
  ↓
API 客户端（API Client）
```

### 1.2 API 发现在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API 发现主要涉及 Governance 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
                    ↑
        Discovery (implementation)
```

API 发现在 API 规范中提供：

- **发现机制**：服务注册、服务发现、健康检查
- **发现协议**：DNS 发现、注册中心发现、配置中心发现
- **元数据管理**：API 元数据、版本元数据
- **发现优化**：缓存策略、负载均衡

---

## 2 发现机制

### 2.1 服务注册

**服务注册配置**：

```yaml
apiVersion: api.example.com/v1
kind: ServiceRegistration
metadata:
  name: payment-service-registration
spec:
  service:
    name: "payment-service"
    version: "1.0.0"
    endpoint: "https://payment-service.example.com"
    protocol: "http"
  metadata:
    tags:
      - "payment"
      - "financial"
    description: "Payment processing service"
  healthCheck:
    endpoint: "/health"
    interval: 30
    timeout: 5
```

**服务注册实现**：

```go
package main

import (
    "context"
    "time"
)

type ServiceRegistry struct {
    client RegistryClient
}

type ServiceInfo struct {
    Name     string
    Version  string
    Endpoint string
    Metadata map[string]string
}

func (r *ServiceRegistry) Register(service ServiceInfo) error {
    registration := &Registration{
        Service:    service,
        Registered: time.Now(),
        TTL:        60 * time.Second,
    }

    return r.client.Register(context.Background(), registration)
}

func (r *ServiceRegistry) Deregister(serviceName string) error {
    return r.client.Deregister(context.Background(), serviceName)
}

func (r *ServiceRegistry) KeepAlive(serviceName string) error {
    ticker := time.NewTicker(30 * time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            if err := r.client.Renew(context.Background(), serviceName); err != nil {
                return err
            }
        }
    }
}
```

### 2.2 服务发现

**服务发现实现**：

```go
package main

type ServiceDiscovery struct {
    registry RegistryClient
    cache    *ServiceCache
}

func (d *ServiceDiscovery) Discover(serviceName string) ([]ServiceInfo, error) {
    // 检查缓存
    if cached := d.cache.Get(serviceName); cached != nil {
        return cached, nil
    }

    // 从注册中心发现
    services, err := d.registry.Discover(context.Background(), serviceName)
    if err != nil {
        return nil, err
    }

    // 过滤健康服务
    healthyServices := d.filterHealthy(services)

    // 更新缓存
    d.cache.Set(serviceName, healthyServices, 30*time.Second)

    return healthyServices, nil
}

func (d *ServiceDiscovery) filterHealthy(services []ServiceInfo) []ServiceInfo {
    var healthy []ServiceInfo
    for _, service := range services {
        if d.isHealthy(service) {
            healthy = append(healthy, service)
        }
    }
    return healthy
}
```

### 2.3 健康检查

**健康检查配置**：

```yaml
apiVersion: api.example.com/v1
kind: HealthCheck
metadata:
  name: payment-service-health-check
spec:
  endpoint: "/health"
  interval: 30
  timeout: 5
  failureThreshold: 3
  successThreshold: 2
  checks:
    - type: "http"
      path: "/health"
      expectedStatus: 200
    - type: "tcp"
      port: 8080
```

**健康检查实现**：

```go
package main

import (
    "net/http"
    "time"
)

type HealthChecker struct {
    endpoint string
    interval time.Duration
    timeout  time.Duration
}

func (h *HealthChecker) Check(service ServiceInfo) bool {
    client := &http.Client{
        Timeout: h.timeout,
    }

    resp, err := client.Get(service.Endpoint + h.endpoint)
    if err != nil {
        return false
    }
    defer resp.Body.Close()

    return resp.StatusCode == http.StatusOK
}

func (h *HealthChecker) StartMonitoring(service ServiceInfo, callback func(bool)) {
    ticker := time.NewTicker(h.interval)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            healthy := h.Check(service)
            callback(healthy)
        }
    }
}
```

---

## 3 发现协议

### 3.1 DNS 发现

**DNS 发现配置**：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: payment-service
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: payment-service
---
apiVersion: v1
kind: Endpoints
metadata:
  name: payment-service
subsets:
  - addresses:
      - ip: 10.0.1.10
    ports:
      - port: 8080
```

### 3.2 注册中心发现

**Consul 注册中心配置**：

```yaml
apiVersion: api.example.com/v1
kind: ConsulRegistry
metadata:
  name: payment-service-consul
spec:
  consul:
    address: "consul:8500"
    datacenter: "dc1"
  service:
    name: "payment-service"
    tags:
      - "payment"
      - "v1"
    check:
      http: "http://payment-service:8080/health"
      interval: "10s"
```

**Consul 发现实现**：

```go
package main

import (
    "github.com/hashicorp/consul/api"
)

type ConsulDiscovery struct {
    client *api.Client
}

func (d *ConsulDiscovery) Discover(serviceName string) ([]ServiceInfo, error) {
    services, _, err := d.client.Health().Service(serviceName, "", true, nil)
    if err != nil {
        return nil, err
    }

    var result []ServiceInfo
    for _, service := range services {
        result = append(result, ServiceInfo{
            Name:     service.Service.Service,
            Version:  service.Service.Meta["version"],
            Endpoint: service.Service.Address + ":" + string(service.Service.Port),
            Metadata: service.Service.Meta,
        })
    }

    return result, nil
}
```

### 3.3 配置中心发现

**配置中心发现配置**：

```yaml
apiVersion: api.example.com/v1
kind: ConfigCenterDiscovery
metadata:
  name: payment-service-config-discovery
spec:
  configCenter:
    type: "nacos"
    address: "nacos:8848"
  services:
    - name: "payment-service"
      group: "DEFAULT_GROUP"
      namespace: "public"
```

---

## 4 元数据管理

### 4.1 API 元数据

**API 元数据定义**：

```yaml
apiVersion: api.example.com/v1
kind: APIMetadata
metadata:
  name: payment-api-metadata
spec:
  api:
    name: "Payment API"
    version: "1.0.0"
    description: "Payment processing API"
    provider: "Payment Corp"
  endpoints:
    - path: "/api/v1/payments"
      method: "POST"
      description: "Create payment"
    - path: "/api/v1/payments/{id}"
      method: "GET"
      description: "Get payment"
  schemas:
    - name: "PaymentRequest"
      type: "object"
      properties:
        orderId:
          type: "string"
        amount:
          type: "integer"
```

### 4.2 版本元数据

**版本元数据管理**：

```yaml
apiVersion: api.example.com/v1
kind: APIVersionMetadata
metadata:
  name: payment-api-version-metadata
spec:
  api: "payment-api"
  versions:
    - version: "1.0.0"
      status: "stable"
      endpoints:
        - "/api/v1/payments"
      deprecated: false
    - version: "2.0.0"
      status: "beta"
      endpoints:
        - "/api/v2/payments"
      deprecated: false
```

---

## 5 发现优化

### 5.1 缓存策略

**缓存策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: DiscoveryCache
metadata:
  name: payment-service-discovery-cache
spec:
  strategy: "ttl"
  ttl: 30
  maxSize: 1000
  eviction: "lru"
```

**缓存策略实现**：

```go
package main

import (
    "sync"
    "time"
)

type ServiceCache struct {
    mu    sync.RWMutex
    cache map[string]*CacheEntry
    ttl   time.Duration
}

type CacheEntry struct {
    Services []ServiceInfo
    Expires  time.Time
}

func (c *ServiceCache) Get(serviceName string) []ServiceInfo {
    c.mu.RLock()
    defer c.mu.RUnlock()

    entry := c.cache[serviceName]
    if entry == nil {
        return nil
    }

    if time.Now().After(entry.Expires) {
        return nil
    }

    return entry.Services
}

func (c *ServiceCache) Set(serviceName string, services []ServiceInfo) {
    c.mu.Lock()
    defer c.mu.Unlock()

    c.cache[serviceName] = &CacheEntry{
        Services: services,
        Expires:  time.Now().Add(c.ttl),
    }
}
```

### 5.2 负载均衡

**负载均衡配置**：

```yaml
apiVersion: api.example.com/v1
kind: LoadBalancer
metadata:
  name: payment-service-lb
spec:
  strategy: "round_robin"
  healthCheck:
    enabled: true
    interval: 10
  services:
    - endpoint: "payment-service-1:8080"
      weight: 1
    - endpoint: "payment-service-2:8080"
      weight: 1
```

---

## 6 发现监控

### 6.1 发现指标

**发现指标配置**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: discovery-metrics
spec:
  groups:
    - name: discovery_metrics
      rules:
        - record: discovery:services_total
          expr: |
            count(service_registrations)
        - record: discovery:discoveries_total
          expr: |
            sum(rate(service_discoveries_total[5m])) by (service_name)
```

### 6.2 发现告警

**发现告警规则**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: discovery-alerts
spec:
  groups:
    - name: discovery_alerts
      rules:
        - alert: ServiceUnavailable
          expr: |
            count(service_registrations{status="healthy"}) == 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: "Service unavailable"
            description: "No healthy instances of {{ $labels.service_name }}"
```

---

## 7 形式化定义与理论基础

### 7.1 API 发现形式化模型

**定义 7.1（API 发现）**：API 发现是一个四元组：

```text
API_Discovery = ⟨Discovery_Mechanism, Discovery_Protocol, Metadata_Management, Discovery_Optimization⟩
```

其中：

- **Discovery_Mechanism**：发现机制
  `Discovery_Mechanism: {Service_Registration, Service_Discovery, Health_Check}`
- **Discovery_Protocol**：发现协议
  `Discovery_Protocol: {DNS, Registry, Config_Center}`
- **Metadata_Management**：元数据管理 `Metadata_Management: API → Metadata`
- **Discovery_Optimization**：发现优化
  `Discovery_Optimization: Discovery → Optimized_Discovery`

**定义 7.2（服务发现）**：服务发现是一个函数：

```text
Discover_Service: Query × Registry → Service[]
```

**定理 7.1（发现正确性）**：如果注册正确，则发现正确：

```text
Correct(Service_Registration) ⟹ Correct(Discover_Service(Query))
```

**证明**：如果服务注册正确，则注册中心包含正确信息，因此发现正确。□

### 7.2 服务发现形式化

**定义 7.3（服务注册）**：服务注册是一个函数：

```text
Register_Service: Service × Metadata → Registered_Service
```

**定义 7.4（健康检查）**：健康检查是一个函数：

```text
Health_Check: Service → {Healthy, Unhealthy}
```

**定理 7.2（健康检查与可用性）**：健康检查保证服务可用性：

```text
Health_Check(Service) = Healthy ⟹ Available(Service)
```

**证明**：如果服务健康，则服务可用，因此可用性得到保证。□

### 7.3 发现可靠性形式化

**定义 7.5（发现可靠性）**：发现可靠性是一个函数：

```text
Discovery_Reliability = f(Registration_Accuracy, Discovery_Speed, Service_Availability)
```

**定义 7.6（缓存策略）**：缓存策略是一个函数：

```text
Cache_Discovery: Discovery_Result → Cached_Result
```

**定理 7.3（缓存策略与性能）**：缓存策略提高发现性能：

```text
Cache_Discovery(Discovery) ⟹ Latency(Discovery) < Latency(No_Cache_Discovery)
```

**证明**：缓存策略减少注册中心查询，因此延迟更低。□

---

## 8 相关文档

- **[API 市场规范](../69-api-marketplace/api-marketplace.md)** - API 市场
- **[API 集成规范](../70-api-integration/api-integration.md)** - API 集成
- **[API 微服务规范](../36-api-microservices/api-microservices.md)** - 微服务发
  现
- **[最佳实践](../00-foundation/05-best-practices.md)** - 发现最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
