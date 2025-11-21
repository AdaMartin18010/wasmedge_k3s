# Envoy 配置示例

## 📑 目录

- [Envoy 配置示例](#envoy-配置示例)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 理论基础](#11-理论基础)
  - [2 Envoy 配置文件格式](#2-envoy-配置文件格式)
    - [2.1 基础配置结构](#21-基础配置结构)
    - [2.2 Admin 接口配置](#22-admin-接口配置)
  - [3 Listener 配置](#3-listener-配置)
    - [3.1 HTTP Listener](#31-http-listener)
    - [3.2 TCP Listener](#32-tcp-listener)
  - [4 Cluster 配置](#4-cluster-配置)
    - [4.1 静态 Cluster](#41-静态-cluster)
    - [4.2 DNS Cluster](#42-dns-cluster)
    - [4.3 EDS Cluster](#43-eds-cluster)
  - [5 Route 配置](#5-route-配置)
    - [5.1 路径匹配](#51-路径匹配)
    - [5.2 Header 匹配](#52-header-匹配)
    - [5.3 权重路由](#53-权重路由)
  - [6 Filter 配置](#6-filter-配置)
    - [6.1 CORS Filter](#61-cors-filter)
    - [6.2 Rate Limit Filter](#62-rate-limit-filter)
    - [6.3 JWT Filter](#63-jwt-filter)
  - [7 相关文档](#7-相关文档)
    - [7.1 理论论证](#71-理论论证)
    - [7.2 架构视角](#72-架构视角)
    - [7.3 技术文档](#73-技术文档)
  - [8 2025 年最新实践](#8-2025-年最新实践)
    - [8.1 Envoy 1.30+ 新特性（2025）](#81-envoy-130-新特性2025)
    - [8.2 HTTP/3 和 QUIC 支持（2025）](#82-http3-和-quic-支持2025)
    - [8.3 Envoy Wasm 扩展（2025）](#83-envoy-wasm-扩展2025)
  - [9 实际应用案例](#9-实际应用案例)
    - [案例 1：API 网关配置](#案例-1api-网关配置)
    - [案例 2：限流和熔断](#案例-2限流和熔断)
    - [案例 3：边缘代理配置](#案例-3边缘代理配置)

---

## 1 概述

本文档提供 **Envoy 代理的实际配置示例**，展示如何配置 Envoy 实现流量管理和策略执
行。

### 1.1 理论基础

Envoy 配置基于以下理论论证：

- **公理 A3（网络异步交付）**：消息传递语义 ≥ 共享内存语义
- **归纳映射 Ψ₄（网络抽象层）**：将 IP:Port 抽象为 ServiceName
- **定理 T1（身份-路由等价）**：身份-路由等价，路由函数 R(e) = v 是双射

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2 Envoy 配置文件格式

### 2.1 基础配置结构

```yaml
# envoy.yaml
static_resources:
  listeners:
    - name: listener_0
      address:
        socket_address:
          address: 0.0.0.0
          port_value: 8080
      filter_chains:
        - filters:
            - name: envoy.filters.network.http_connection_manager
              typed_config:
                "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                stat_prefix: ingress_http
                route_config:
                  name: local_route
                  virtual_hosts:
                    - name: local_service
                      domains: ["*"]
                      routes:
                        - match:
                            prefix: "/"
                          route:
                            cluster: service_cluster
                http_filters:
                  - name: envoy.filters.http.router
                    typed_config:
                      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
  clusters:
    - name: service_cluster
      connect_timeout: 0.25s
      type: LOGICAL_DNS
      lb_policy: ROUND_ROBIN
      load_assignment:
        cluster_name: service_cluster
        endpoints:
          - lb_endpoints:
              - endpoint:
                  address:
                    socket_address:
                      address: 127.0.0.1
                      port_value: 8080
```

### 2.2 Admin 接口配置

```yaml
admin:
  address:
    socket_address:
      address: 127.0.0.1
      port_value: 9901
```

---

## 3 Listener 配置

### 3.1 HTTP Listener

```yaml
listeners:
  - name: http_listener
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 8080
    filter_chains:
      - filters:
          - name: envoy.filters.network.http_connection_manager
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
              stat_prefix: ingress_http
              codec_type: AUTO
              route_config:
                name: local_route
                virtual_hosts:
                  - name: local_service
                    domains: ["*"]
                    routes:
                      - match:
                          prefix: "/"
                        route:
                          cluster: backend_service
              http_filters:
                - name: envoy.filters.http.router
                  typed_config:
                    "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```

### 3.2 TCP Listener

```yaml
listeners:
  - name: tcp_listener
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 3306
    filter_chains:
      - filters:
          - name: envoy.filters.network.tcp_proxy
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.network.tcp_proxy.v3.TcpProxy
              stat_prefix: tcp_stats
              cluster: mysql_cluster
```

---

## 4 Cluster 配置

### 4.1 静态 Cluster

```yaml
clusters:
  - name: backend_service
    connect_timeout: 0.25s
    type: STATIC
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: backend_service
      endpoints:
        - lb_endpoints:
            - endpoint:
                address:
                  socket_address:
                    address: 10.0.0.1
                    port_value: 8080
            - endpoint:
                address:
                  socket_address:
                    address: 10.0.0.2
                    port_value: 8080
```

### 4.2 DNS Cluster

```yaml
clusters:
  - name: dns_service
    connect_timeout: 0.25s
    type: LOGICAL_DNS
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: dns_service
      endpoints:
        - lb_endpoints:
            - endpoint:
                address:
                  socket_address:
                    address: service.example.com
                    port_value: 8080
```

### 4.3 EDS Cluster

```yaml
clusters:
  - name: eds_service
    connect_timeout: 0.25s
    type: EDS
    lb_policy: ROUND_ROBIN
    eds_cluster_config:
      eds_config:
        api_config_source:
          api_type: GRPC
          grpc_services:
            - envoy_grpc:
                cluster_name: xds_cluster
```

---

## 5 Route 配置

### 5.1 路径匹配

```yaml
routes:
  - match:
      prefix: "/api"
    route:
      cluster: api_service
  - match:
      prefix: "/static"
    route:
      cluster: static_service
```

### 5.2 Header 匹配

```yaml
routes:
  - match:
      prefix: "/"
      headers:
        - name: x-version
          exact_match: "v2"
    route:
      cluster: v2_service
  - match:
      prefix: "/"
    route:
      cluster: v1_service
```

### 5.3 权重路由

```yaml
routes:
  - match:
      prefix: "/"
    route:
      weighted_clusters:
        clusters:
          - name: v1_service
            weight: 90
          - name: v2_service
            weight: 10
```

---

## 6 Filter 配置

### 6.1 CORS Filter

```yaml
http_filters:
  - name: envoy.filters.http.cors
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.cors.v3.Cors
  - name: envoy.filters.http.router
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```

### 6.2 Rate Limit Filter

```yaml
http_filters:
  - name: envoy.filters.http.ratelimit
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.ratelimit.v3.RateLimit
      domain: rate_limit_domain
      rate_limit_service:
        grpc_service:
          envoy_grpc:
            cluster_name: rate_limit_service
  - name: envoy.filters.http.router
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```

### 6.3 JWT Filter

```yaml
http_filters:
  - name: envoy.filters.http.jwt_authn
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.jwt_authn.v3.JwtAuthentication
      providers:
        provider1:
          issuer: https://example.com
          audiences:
            - api.example.com
          remote_jwks:
            http_uri:
              uri: https://example.com/.well-known/jwks.json
              cluster: jwks_cluster
            cache_duration: 300s
      rules:
        - match:
            prefix: "/"
          requires:
            provider_name: provider1
  - name: envoy.filters.http.router
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```

---

## 7 相关文档

### 7.1 理论论证

- **`../../00-theory/02-induction-proof/psi4-network.md`** - 网络抽象层归纳映射
- **`../../00-theory/01-axioms/A3-network-async.md`** - 网络异步交付公理
- **`../../00-theory/05-lemmas-theorems/T1-identity-routing.md`** - 身份-路由等
  价定理

### 7.2 架构视角

- **`../../02-views/10-quick-views/service-mesh-view.md`** - Service Mesh 架构视
  角

### 7.3 技术文档

- **`../../../TECHNICAL/06-advanced-features/service-mesh/service-mesh.md`** - Service Mesh 技术文
  档

## 8 2025 年最新实践

### 8.1 Envoy 1.30+ 新特性（2025）

**最新版本**：Envoy 1.30+（2025 年 11 月）

**新特性**：

- **HTTP/3 支持**：完整的 HTTP/3 和 QUIC 支持
- **性能优化**：减少内存占用和 CPU 使用
- **Wasm 扩展增强**：更好的 Wasm 插件支持
- **可观测性增强**：改进的遥测和追踪

**安装最新版本**：

```bash
# 使用 Docker 运行 Envoy 1.30
docker run --rm -it \
  -v $(pwd)/envoy.yaml:/etc/envoy/envoy.yaml \
  -p 8080:8080 \
  envoyproxy/envoy:v1.30.0
```

### 8.2 HTTP/3 和 QUIC 支持（2025）

**HTTP/3 优势**：

- **低延迟**：基于 UDP 的 QUIC 协议，减少延迟
- **多路复用**：更好的多路复用支持
- **连接迁移**：支持连接迁移

**配置示例**：

```yaml
listeners:
- name: listener_0
  address:
    socket_address:
      address: 0.0.0.0
      port_value: 8080
  filter_chains:
  - filters:
    - name: envoy.filters.network.http_connection_manager
      typed_config:
        "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
        codec_type: HTTP3
        stat_prefix: ingress_http3
        http3_protocol_options: {}
        route_config:
          name: local_route
          virtual_hosts:
          - name: local_service
            domains: ["*"]
            routes:
            - match:
                prefix: "/"
              route:
                cluster: service_cluster
```

### 8.3 Envoy Wasm 扩展（2025）

**Wasm 扩展优势**：

- **动态加载**：无需重启即可加载扩展
- **安全隔离**：Wasm 提供安全隔离
- **高性能**：接近原生性能

**配置示例**：

```yaml
http_filters:
- name: envoy.filters.http.wasm
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.wasm.v3.Wasm
    config:
      name: my_wasm_filter
      root_id: my_root_id
      vm_config:
        vm_id: my_vm_id
        runtime: envoy.wasm.runtime.v8
        code:
          remote:
            http_uri:
              uri: http://myregistry.com/filters/my-filter.wasm
              cluster: wasm_cluster
              timeout: 5s
            sha256: abc123...
```

## 9 实际应用案例

### 案例 1：API 网关配置

**场景**：使用 Envoy 作为 API 网关

**实现方案**：

```yaml
static_resources:
  listeners:
  - name: api_gateway
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 8080
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: api_gateway
          route_config:
            name: api_routes
            virtual_hosts:
            - name: api
              domains: ["api.example.com"]
              routes:
              - match:
                  prefix: "/v1/users"
                route:
                  cluster: user_service
              - match:
                  prefix: "/v1/orders"
                route:
                  cluster: order_service
          http_filters:
          - name: envoy.filters.http.cors
          - name: envoy.filters.http.router
  clusters:
  - name: user_service
    connect_timeout: 0.25s
    type: LOGICAL_DNS
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: user_service
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: user-service.default.svc.cluster.local
                port_value: 8080
  - name: order_service
    connect_timeout: 0.25s
    type: LOGICAL_DNS
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: order_service
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: order-service.default.svc.cluster.local
                port_value: 8080
```

**效果**：

- 统一入口：所有 API 请求通过 Envoy 网关
- 路由管理：根据路径路由到不同服务
- CORS 支持：自动处理跨域请求

### 案例 2：限流和熔断

**场景**：实现 API 限流和熔断保护

**实现方案**：

```yaml
http_filters:
- name: envoy.filters.http.local_ratelimit
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
    stat_prefix: local_rate_limiter
    token_bucket:
      max_tokens: 100
      tokens_per_fill: 100
      fill_interval: 1s
- name: envoy.filters.http.circuit_breaker
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.circuit_breaker.v3.CircuitBreaker
    max_connections: 100
    max_pending_requests: 50
    max_requests: 200
    max_retries: 3
```

**效果**：

- 限流保护：防止 API 过载
- 熔断保护：自动隔离故障服务
- 服务稳定：提高服务可用性

### 案例 3：边缘代理配置

**场景**：在边缘节点部署 Envoy 作为边缘代理

**实现方案**：

```yaml
static_resources:
  listeners:
  - name: edge_listener
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 80
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: edge
          route_config:
            name: edge_routes
            virtual_hosts:
            - name: edge_service
              domains: ["*"]
              routes:
              - match:
                  prefix: "/"
                route:
                  cluster: backend_service
                  timeout: 5s
                  retry_policy:
                    retry_on: 5xx,reset
                    num_retries: 3
                    per_try_timeout: 2s
          http_filters:
          - name: envoy.filters.http.router
```

**效果**：

- 边缘缓存：在边缘节点缓存响应
- 故障恢复：自动重试和超时处理
- 低延迟：减少到后端的延迟

---

**更新时间**：2025-11-15 **版本**：v1.1 **状态**：✅ 包含 2025 年最新实践
