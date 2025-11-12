# API 代理规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 代理架构](#11-代理架构)
  - [1.2 代理在 API 规范中的位置](#12-代理在-api-规范中的位置)
- [2 形式化定义与理论基础](#2-形式化定义与理论基础)
  - [2.1 API 代理形式化定义](#21-api-代理形式化定义)
  - [2.2 代理语义等价性](#22-代理语义等价性)
  - [2.3 代理透明性定理](#23-代理透明性定理)
- [3 代理类型](#3-代理类型)
  - [2.1 正向代理](#21-正向代理)
  - [3.2 反向代理](#32-反向代理)
  - [3.3 透明代理](#33-透明代理)
- [4 代理功能](#4-代理功能)
  - [4.1 请求转发](#41-请求转发)
  - [4.2 负载均衡](#42-负载均衡)
  - [4.3 缓存](#43-缓存)
- [5 代理配置](#5-代理配置)
  - [5.1 路由配置](#51-路由配置)
  - [5.2 策略配置](#52-策略配置)
- [6 代理监控](#6-代理监控)
  - [6.1 性能监控](#61-性能监控)
  - [6.2 健康监控](#62-健康监控)
- [7 代理安全](#7-代理安全)
  - [7.1 认证授权](#71-认证授权)
  - [7.2 流量加密](#72-流量加密)
- [8 容器化、沙盒化、WASM 化代理](#8-容器化沙盒化wasm-化代理)
  - [8.1 容器化代理](#81-容器化代理)
  - [8.2 沙盒化代理](#82-沙盒化代理)
  - [8.3 WASM 化代理](#83-wasm-化代理)
- [9 相关文档](#9-相关文档)

---

## 1 概述

API 代理规范定义了 API 在代理场景下的设计和实现，从代理类型到代理功能，从代理配
置到代理监控。本文档基于形式化方法，提供严格的数学定义和推理论证，确保代理行为的
正确性和可验证性。

### 1.1 代理架构

```text
API 客户端（API Client）
  ↓
API 代理（API Proxy）
  ↓
后端服务（Backend Service）
```

**参考标准**：

- [RFC 7230: HTTP/1.1 Message Syntax and Routing](https://tools.ietf.org/html/rfc7230) -
  HTTP 代理标准
- [RFC 7540: HTTP/2](https://tools.ietf.org/html/rfc7540) - HTTP/2 代理
- [Envoy Proxy Architecture](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/arch_overview) -
  云原生代理架构

### 1.2 代理在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API 代理属于 **Governance** 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
                ↑
            API Proxy ∈ Governance
```

API 代理作为运行时治理机制，在 API 调用链中提供：

- **请求路由**：根据策略将请求路由到后端服务
- **流量管理**：负载均衡、限流、熔断
- **安全增强**：认证、授权、加密
- **可观测性注入**：追踪、指标、日志

---

## 2 形式化定义与理论基础

### 2.1 API 代理形式化定义

**定义 2.1（API 代理）**：API 代理是一个三元组：

```text
Proxy = ⟨Client, Transform, Backend⟩
```

其中：

- **Client**：客户端接口 `C: Request → Response`
- **Transform**：转换函数 `T: Request → Request'`，`T': Response' → Response`
- **Backend**：后端接口 `B: Request' → Response'`

**代理语义**：对于任意请求 `req`，代理行为满足：

```text
Proxy(req) = Transform_response(Backend(Transform_request(req)))
```

**定义 2.2（代理透明性）**：代理是透明的，当且仅当：

```text
∀ req: Proxy(req) ≈ Direct(req)
```

其中 `≈` 表示语义等价，`Direct(req)` 表示直接调用后端服务。

### 2.2 代理语义等价性

**定理 2.1（代理语义等价性）**：如果代理满足以下条件，则代理是语义等价的：

1. **请求保真性**：`Transform_request` 保持请求语义
2. **响应保真性**：`Transform_response` 保持响应语义
3. **无副作用**：代理不引入额外的副作用

**证明**：

设 `req` 为任意请求，`resp = Backend(req)` 为直接调用的响应。

根据定义 2.1：

```text
Proxy(req) = Transform_response(Backend(Transform_request(req)))
```

根据条件 1（请求保真性）：

```text
Backend(Transform_request(req)) = Backend(req) = resp
```

根据条件 2（响应保真性）：

```text
Transform_response(resp) ≈ resp
```

因此：

```text
Proxy(req) = Transform_response(resp) ≈ resp = Direct(req)
```

根据条件 3（无副作用），代理不改变系统状态，因此 `Proxy(req) ≈ Direct(req)`。□

### 2.3 代理透明性定理

**定理 2.2（代理透明性）**：代理透明性是可组合的，即：

```text
Proxy₁ ∘ Proxy₂ 是透明的 ⟺ Proxy₁ 是透明的 ∧ Proxy₂ 是透明的
```

**证明**：

**必要性（⟹）**：如果 `Proxy₁ ∘ Proxy₂` 是透明的，则：

```text
∀ req: Proxy₁(Proxy₂(req)) ≈ Direct(req)
```

假设 `Proxy₂` 不透明，则存在 `req` 使得 `Proxy₂(req) ≉ Direct(req)`，因此
`Proxy₁(Proxy₂(req)) ≉ Proxy₁(Direct(req))`，与前提矛盾。同理可证 `Proxy₁` 必须
透明。

**充分性（⟸）**：如果 `Proxy₁` 和 `Proxy₂` 都透明，则：

```text
Proxy₁(Proxy₂(req)) ≈ Proxy₁(Direct(req)) ≈ Direct(req)
```

因此 `Proxy₁ ∘ Proxy₂` 是透明的。□

---

## 3 代理类型

### 2.1 正向代理

**正向代理配置**：

```yaml
apiVersion: api.example.com/v1
kind: ForwardProxy
metadata:
  name: payment-api-forward-proxy
spec:
  type: "forward"
  upstream:
    - endpoint: "https://payment-service.example.com"
      weight: 1
  rules:
    - match:
        path: "/api/v1/payments"
      action: "forward"
```

### 3.2 反向代理

**反向代理配置**：

```yaml
apiVersion: api.example.com/v1
kind: ReverseProxy
metadata:
  name: payment-api-reverse-proxy
spec:
  type: "reverse"
  frontend:
    listen: "0.0.0.0:8080"
  backend:
    - endpoint: "http://payment-service-1:8080"
      weight: 1
    - endpoint: "http://payment-service-2:8080"
      weight: 1
```

**反向代理实现**：

```go
package main

import (
    "net/http"
    "net/http/httputil"
    "net/url"
)

type ReverseProxy struct {
    targets []*url.URL
    proxy   *httputil.ReverseProxy
}

func NewReverseProxy(targets []string) (*ReverseProxy, error) {
    var urls []*url.URL
    for _, target := range targets {
        u, err := url.Parse(target)
        if err != nil {
            return nil, err
        }
        urls = append(urls, u)
    }

    return &ReverseProxy{
        targets: urls,
    }, nil
}

func (p *ReverseProxy) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    // 选择目标
    target := p.selectTarget(r)

    // 创建代理
    proxy := httputil.NewSingleHostReverseProxy(target)

    // 修改请求
    r.Host = target.Host

    // 转发请求
    proxy.ServeHTTP(w, r)
}

func (p *ReverseProxy) selectTarget(r *http.Request) *url.URL {
    // 简单的轮询负载均衡
    index := hashRequest(r) % len(p.targets)
    return p.targets[index]
}
```

### 3.3 透明代理

**透明代理配置**：

```yaml
apiVersion: api.example.com/v1
kind: TransparentProxy
metadata:
  name: payment-api-transparent-proxy
spec:
  type: "transparent"
  intercept:
    - port: 8080
      protocol: "http"
  forward:
    - endpoint: "http://payment-service:8080"
```

**定义 3.1（正向代理）**：正向代理是客户端可见的代理，满足：

```text
ForwardProxy = ⟨Client, Identity, Backend⟩
```

其中 `Identity` 表示恒等变换（可能包含认证、日志等副作用）。

**定义 3.2（反向代理）**：反向代理是客户端不可见的代理，满足：

```text
ReverseProxy = ⟨Client, Route ∘ LoadBalance, Backend⟩
```

其中 `Route` 是路由函数，`LoadBalance` 是负载均衡函数。

**定义 3.3（透明代理）**：透明代理是网络层拦截的代理，满足：

```text
TransparentProxy = ⟨Intercept, Transform, Forward⟩
```

其中 `Intercept` 是网络拦截函数。

---

## 4 代理功能

### 4.1 请求转发

**请求转发实现**：

```go
package main

import (
    "net/http"
    "io"
)

func ForwardRequest(w http.ResponseWriter, r *http.Request, targetURL string) error {
    // 创建新请求
    req, err := http.NewRequest(r.Method, targetURL+r.URL.Path, r.Body)
    if err != nil {
        return err
    }

    // 复制请求头
    for key, values := range r.Header {
        for _, value := range values {
            req.Header.Add(key, value)
        }
    }

    // 发送请求
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    // 复制响应头
    for key, values := range resp.Header {
        for _, value := range values {
            w.Header().Add(key, value)
        }
    }

    // 设置状态码
    w.WriteHeader(resp.StatusCode)

    // 复制响应体
    _, err = io.Copy(w, resp.Body)
    return err
}
```

### 4.2 负载均衡

**负载均衡实现**：

```go
package main

import (
    "sync"
)

type LoadBalancer struct {
    targets []*Target
    mu      sync.RWMutex
    strategy LoadBalanceStrategy
}

type Target struct {
    URL    string
    Weight int
    Health bool
}

type LoadBalanceStrategy interface {
    Select(targets []*Target, req *http.Request) *Target
}

type RoundRobinStrategy struct {
    index int
    mu    sync.Mutex
}

func (s *RoundRobinStrategy) Select(targets []*Target, req *http.Request) *Target {
    s.mu.Lock()
    defer s.mu.Unlock()

    healthy := filterHealthy(targets)
    if len(healthy) == 0 {
        return nil
    }

    target := healthy[s.index%len(healthy)]
    s.index++
    return target
}

type WeightedRoundRobinStrategy struct {
    weights map[string]int
    current map[string]int
    mu      sync.Mutex
}

func (s *WeightedRoundRobinStrategy) Select(targets []*Target, req *http.Request) *Target {
    s.mu.Lock()
    defer s.mu.Unlock()

    healthy := filterHealthy(targets)
    if len(healthy) == 0 {
        return nil
    }

    // 选择权重最高的目标
    var selected *Target
    maxWeight := 0

    for _, target := range healthy {
        weight := s.weights[target.URL] + target.Weight - s.current[target.URL]
        if weight > maxWeight {
            maxWeight = weight
            selected = target
        }
    }

    if selected != nil {
        s.current[selected.URL]++
    }

    return selected
}
```

### 4.3 缓存

**缓存实现**：

```go
package main

import (
    "time"
    "sync"
)

type ProxyCache struct {
    cache map[string]*CacheEntry
    mu    sync.RWMutex
    ttl   time.Duration
}

type CacheEntry struct {
    Response *http.Response
    Body      []byte
    Expires   time.Time
}

func (c *ProxyCache) Get(key string) (*http.Response, []byte, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()

    entry := c.cache[key]
    if entry == nil {
        return nil, nil, false
    }

    if time.Now().After(entry.Expires) {
        delete(c.cache, key)
        return nil, nil, false
    }

    return entry.Response, entry.Body, true
}

func (c *ProxyCache) Set(key string, resp *http.Response, body []byte) {
    c.mu.Lock()
    defer c.mu.Unlock()

    c.cache[key] = &CacheEntry{
        Response: resp,
        Body:     body,
        Expires:  time.Now().Add(c.ttl),
    }
}
```

**定义 4.1（请求转发）**：请求转发函数 `Forward: Request × Target → Response` 满
足：

```text
Forward(req, target) = Backend_target(Transform(req))
```

**性质 4.1（转发保序性）**：如果请求序列 `req₁, req₂, ..., reqₙ` 满足顺序关系，
则转发后的序列保持顺序关系。

**定义 4.2（负载均衡）**：负载均衡函数 `LB: Request × Targets → Target` 满足：

```text
∀ target ∈ Targets: P(LB(req, Targets) = target) = weight(target) / Σ weight(Targets)
```

**定理 4.1（负载均衡公平性）**：如果所有目标权重相等，则负载均衡是公平的：

```text
lim_{n→∞} |{i: LB(req_i) = target}| / n = 1 / |Targets|
```

**证明**：根据大数定律，当请求数量趋于无穷时，每个目标被选中的频率趋于其权重比例
。□

**定义 4.3（缓存一致性）**：缓存函数 `Cache: Request → Response` 满足：

```text
Cache(req) = if Valid(cache[req]) then cache[req] else Backend(req)
```

**定理 4.2（缓存有效性）**：缓存命中率 `h` 满足：

```text
h = |{req: Valid(cache[req])}| / |{req}|
```

缓存平均响应时间：

```text
T_avg = h × T_cache + (1-h) × T_backend
```

其中 `T_cache` 是缓存访问时间，`T_backend` 是后端访问时间。

---

## 5 代理配置

### 5.1 路由配置

**路由配置**：

```yaml
apiVersion: api.example.com/v1
kind: ProxyRoute
metadata:
  name: payment-api-proxy-routes
spec:
  routes:
    - match:
        path: "/api/v1/payments"
        method: "POST"
      backend:
        endpoint: "http://payment-service:8080"
        timeout: 30
    - match:
        path: "/api/v1/payments/{id}"
        method: "GET"
      backend:
        endpoint: "http://payment-service:8080"
        cache:
          enabled: true
          ttl: 300
```

### 5.2 策略配置

**策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: ProxyPolicy
metadata:
  name: payment-api-proxy-policy
spec:
  policies:
    - name: "rate_limit"
      type: "rate_limit"
      limit: 100
      window: "1m"
    - name: "authentication"
      type: "authentication"
      required: true
    - name: "caching"
      type: "caching"
      ttl: 300
      cacheControl: "public, max-age=300"
```

**定义 5.1（路由规则）**：路由规则是一个三元组：

```text
Route = ⟨Match, Action, Backend⟩
```

其中：

- **Match**：匹配条件 `M: Request → Bool`
- **Action**：动作函数 `A: Request → Request'`
- **Backend**：后端目标

**路由决策**：对于请求 `req`，路由决策为：

```text
Route(req) = if M(req) then A(req) → Backend else Next(Route, req)
```

---

## 6 代理监控

### 6.1 性能监控

**性能监控配置**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: proxy-performance-metrics
spec:
  groups:
    - name: proxy_performance
      rules:
        - record: proxy:requests_total
          expr: |
            sum(rate(proxy_requests_total[5m])) by (route, status)
        - record: proxy:latency_seconds
          expr: |
            histogram_quantile(0.95, sum(rate(proxy_latency_seconds_bucket[5m])) by (route, le))
```

### 6.2 健康监控

**健康监控实现**：

```go
package main

import (
    "net/http"
    "time"
)

type HealthChecker struct {
    targets []*Target
    interval time.Duration
}

func (h *HealthChecker) Check(target *Target) bool {
    client := &http.Client{
        Timeout: 5 * time.Second,
    }

    resp, err := client.Get(target.URL + "/health")
    if err != nil {
        return false
    }
    defer resp.Body.Close()

    return resp.StatusCode == http.StatusOK
}

func (h *HealthChecker) StartMonitoring() {
    ticker := time.NewTicker(h.interval)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            for _, target := range h.targets {
                target.Health = h.Check(target)
            }
        }
    }
}
```

**定义 6.1（代理性能指标）**：代理性能指标包括：

- **延迟**：`Latency = T_proxy + T_backend`
- **吞吐量**：`Throughput = Requests / Time`
- **错误率**：`ErrorRate = Errors / TotalRequests`

**定理 6.1（代理延迟下界）**：代理延迟满足：

```text
Latency ≥ T_backend
```

**证明**：代理必须等待后端响应，因此代理延迟至少等于后端延迟。□

---

## 7 代理安全

### 7.1 认证授权

**认证授权配置**：

```yaml
apiVersion: api.example.com/v1
kind: ProxyAuth
metadata:
  name: payment-api-proxy-auth
spec:
  authentication:
    type: "bearer"
    tokenSource: "header"
    tokenHeader: "Authorization"
  authorization:
    type: "rbac"
    policies:
      - resource: "/api/v1/payments"
        actions: ["create", "read"]
        roles: ["user", "admin"]
```

### 7.2 流量加密

**流量加密配置**：

```yaml
apiVersion: api.example.com/v1
kind: ProxyTLS
metadata:
  name: payment-api-proxy-tls
spec:
  enabled: true
  certificate: "/etc/ssl/certs/proxy.crt"
  privateKey: "/etc/ssl/private/proxy.key"
  protocols:
    - "TLSv1.2"
    - "TLSv1.3"
  cipherSuites:
    - "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
    - "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305"
```

**定义 7.1（代理认证）**：代理认证函数 `Auth: Request → Request'` 满足：

```text
Auth(req) = if Valid(token(req)) then req else Error(Unauthorized)
```

**定义 7.2（代理加密）**：代理加密函数 `Encrypt: Request → Request'` 满足：

```text
Encrypt(req) = TLS_Encrypt(req, Certificate)
```

**定理 7.1（代理安全性）**：如果代理满足：

1. 所有请求经过认证：`∀ req: Auth(req) ≠ Error`
2. 所有流量加密：`∀ req: Encrypt(req)`
3. 无信息泄露：代理不记录敏感信息

则代理是安全的。

**证明**：根据条件 1-3，代理确保请求的机密性、完整性和可用性。□

---

## 8 容器化、沙盒化、WASM 化代理

### 8.1 容器化代理

**容器化代理配置**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: envoy-proxy
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: envoy
          image: envoyproxy/envoy:v1.30.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "256Mi"
              cpu: "200m"
            limits:
              memory: "512Mi"
              cpu: "500m"
```

**容器化代理特性**：

- **资源隔离**：通过 Kubernetes 资源限制实现
- **网络隔离**：通过 CNI 插件实现
- **存储隔离**：通过 CSI 插件实现

### 8.2 沙盒化代理

**gVisor 沙盒化代理配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: envoy-gvisor
spec:
  runtimeClassName: gvisor
  containers:
    - name: envoy
      image: envoyproxy/envoy:v1.30.0
      securityContext:
        seccompProfile:
          type: RuntimeDefault
```

**沙盒化代理特性**：

- **系统调用过滤**：通过 Seccomp 实现
- **文件系统隔离**：通过 gVisor Sentry 实现
- **网络隔离**：通过 gVisor Netstack 实现

### 8.3 WASM 化代理

**Envoy WASM 代理配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: EnvoyFilter
metadata:
  name: wasm-proxy-filter
spec:
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.wasm
          typed_config:
            "@type": type.googleapis.com/envoy.extensions.filters.http.wasm.v3.Wasm
            config:
              vm_config:
                runtime: "envoy.wasm.runtime.v8"
                code:
                  local:
                    filename: "/etc/proxy-filter.wasm"
```

**WASM 化代理特性**：

- **轻量级**：WASM 模块体积小，启动快
- **安全性**：WASM 沙盒提供强隔离
- **可移植性**：WASM 模块可在不同平台运行

**形式化定义**：

**定义 8.1（WASM 代理）**：WASM 代理是一个四元组：

```text
WASMProxy = ⟨Envoy, WASMRuntime, WASMModule, Transform⟩
```

其中：

- **Envoy**：Envoy 代理核心
- **WASMRuntime**：WASM 运行时（如 wasmtime、V8）
- **WASMModule**：WASM 模块（实现代理逻辑）
- **Transform**：转换函数（在 WASM 模块中实现）

**定理 8.1（WASM 代理性能）**：WASM 代理的性能满足：

```text
T_WASM = T_Envoy + T_WASMRuntime + T_WASMModule
```

其中 `T_WASMRuntime` 和 `T_WASMModule` 通常远小于 `T_Envoy`，因此 WASM 代理的性
能开销可忽略。

---

## 9 相关文档

- **[API 网关规范](../17-api-gateway/api-gateway.md)** - API 网关
- **[API 集成规范](../70-api-integration/api-integration.md)** - API 集成
- **[API 安全规范](../11-api-security/api-security.md)** - API 安全
- **[最佳实践](../00-foundation/05-best-practices.md)** - 代理最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
