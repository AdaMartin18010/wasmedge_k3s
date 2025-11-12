# 服务组合：从"跨服务流"到"可编排的本地函数"

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 核心思想](#11-核心思想)
- [2 传统模型 vs Service Mesh 模型](#2-传统模型-vs-service-mesh-模型)
  - [2.1 传统跨服务流](#21-传统跨服务流)
  - [2.2 Service Mesh 服务组合](#22-service-mesh-服务组合)
- [3 Filter Chain（过滤器链）](#3-filter-chain过滤器链)
  - [3.1 Filter Chain 定义](#31-filter-chain-定义)
  - [3.2 Filter Chain 示例](#32-filter-chain-示例)
- [4 服务组合粒度](#4-服务组合粒度)
  - [4.1 组合粒度从"进程"降到"请求路径"](#41-组合粒度从进程降到请求路径)
  - [4.2 Filter Chain = 可编程的 lambda 管道](#42-filter-chain--可编程的-lambda-管道)
- [5 服务组合语义](#5-服务组合语义)
  - [5.1 组合语义上升到"架构描述层"](#51-组合语义上升到架构描述层)
  - [5.2 VirtualService 示例](#52-virtualservice-示例)
- [6 架构设计范式转换](#6-架构设计范式转换)
  - [6.1 "先定接口，再定部署" → "先定流量，再定接口"](#61-先定接口再定部署--先定流量再定接口)
  - [6.2 "分层图" → "过滤器图"](#62-分层图--过滤器图)
  - [6.3 非功能性从"后期治理"变为"设计期可组合元素"](#63-非功能性从后期治理变为设计期可组合元素)
- [7 服务组合模式](#7-服务组合模式)
  - [7.1 组合模式类型](#71-组合模式类型)
  - [7.2 组合示例](#72-组合示例)
- [8 形式化定义](#8-形式化定义)
  - [8.1 服务组合定义](#81-服务组合定义)
  - [8.2 Filter Chain 定义](#82-filter-chain-定义)
  - [8.3 服务组合函数](#83-服务组合函数)
- [9 架构收益](#9-架构收益)
  - [9.1 可组合性](#91-可组合性)
  - [9.2 可版本化](#92-可版本化)
  - [9.3 可测试性](#93-可测试性)
  - [9.4 可观测性](#94-可观测性)
- [10 总结](#10-总结)

---

## 1 概述

本文档阐述 Service Mesh 如何通过**服务组合**实现从"跨服务流"到"可编排的本地函数"
的范式转换。

### 1.1 核心思想

> **Service Mesh 把"跨服务流"变成"可编排的本地函数"，通过 Filter Chain 实现细粒
> 度的流量控制**

## 2 传统模型 vs Service Mesh 模型

### 2.1 传统跨服务流

**传统方式**：

```text
Client → Service A → Service B → Service C → Database
```

**问题**：

- 跨服务调用耦合在代码中
- 流量控制逻辑分散在各个服务
- 难以统一管理和监控

### 2.2 Service Mesh 服务组合

**Service Mesh 方式**：

```text
Request → [JWT|RBAC|RateLimit|Circuit|Retry|Transform] → upstream
```

**优势**：

- 流量控制逻辑集中在 Filter Chain
- 可编排、可版本化、可测试
- 统一监控和治理

## 3 Filter Chain（过滤器链）

### 3.1 Filter Chain 定义

**Filter Chain** 是可编程的 lambda 管道，包含多个过滤器：

```text
Filter Chain = [Filter₁, Filter₂, ..., Filterₙ]
```

**典型过滤器**：

- **认证**（JWT、mTLS）
- **授权**（RBAC、OPA）
- **限流**（Rate Limit）
- **熔断**（Circuit Breaker）
- **重试**（Retry）
- **转换**（Transform）
- **缓存**（Cache）
- **转发**（Forward）

### 3.2 Filter Chain 示例

**Envoy Filter Chain**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: EnvoyFilter
metadata:
  name: custom-filter
spec:
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
        listener:
          filterChain:
            filter:
              name: envoy.filters.network.http_connection_manager
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.rate_limit
          typed_config:
            "@type": type.googleapis.com/envoy.extensions.filters.http.rate_limit.v3.RateLimit
            domain: custom-domain
            rate_limit_service:
              grpc_service:
                envoy_grpc:
                  cluster_name: rate_limit_cluster
```

## 4 服务组合粒度

### 4.1 组合粒度从"进程"降到"请求路径"

**传统方式**：

- 组合粒度：进程级别
- 流量控制：服务级别

**Service Mesh 方式**：

- 组合粒度：请求路径级别
- 流量控制：请求级别

### 4.2 Filter Chain = 可编程的 lambda 管道

**Filter Chain 特点**：

- **认证** → **限流** → **熔断** → **重试** → **转换** → **缓存** → **转发**
- 每条 filter 都可 **热插拔、A/B 对比、灰度发布**
- 架构图里用 **"VirtualService + EnvoyFilter"** 就能描述 **"服务组合工作流"**

## 5 服务组合语义

### 5.1 组合语义上升到"架构描述层"

**传统方式**：

- 需要画 7 层网关、Nginx conf、Spring Cloud Gateway 的爆炸图
- 流量控制逻辑分散在代码和配置中

**Service Mesh 方式**：

- 用 **"VirtualService + EnvoyFilter"** 描述 **"服务组合工作流"**
- 不再需要画复杂的架构图

### 5.2 VirtualService 示例

**流量组合 + 版本组合**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: checkout
spec:
  http:
    - match:
        - headers:
            x-canary:
              exact: "1"
      route:
        - destination:
            host: checkout
            subset: v2
          weight: 100
    - route:
        - destination:
            host: checkout
            subset: v1
          weight: 90
        - destination:
            host: checkout
            subset: v2
          weight: 10
```

**这段 YAML 同时完成**：

- **"流量组合"**：根据 header 路由到不同版本
- **"版本组合"**：金丝雀发布（10% 流量到 v2）

**验证、测试、回溯**：

- **被验证**（flagger 自动金丝雀）
- **被测试**（k6+prometheus）
- **被回溯**（git-ops）

## 6 架构设计范式转换

### 6.1 "先定接口，再定部署" → "先定流量，再定接口"

**传统方式**：

1. 先定义 Java interface/proto file
2. 再部署服务
3. 最后配置网络

**Service Mesh 方式**：

1. **流量特征**（延迟、重试、超时、安全）先于 **Java interface/proto file** 被固
   定下来
2. 接口演进 = **VirtualService 版本化**，不再需要 **v1/v2 两套代码仓库**

### 6.2 "分层图" → "过滤器图"

**传统架构图**：

```text
Edge LB → API Gateway → Biz Service → Cache → DB
```

**Service Mesh 架构图**：

```text
Request → [JWT|RBAC|RateLimit|Circuit|Retry|Transform] → upstream
```

**整条链路由 **CRD 描述**，可**版本化、差异比对、自动化测试\*\*

### 6.3 非功能性从"后期治理"变为"设计期可组合元素"

**传统方式**：

- 安全、可观测、弹性在**后期治理**阶段添加
- 需要修改代码或配置

**Service Mesh 方式**：

- **安全**：mTLS 自动轮转，**架构图里把"锁"图标换成 Policy 对象**
- **可观测**：trace/metric 由 sidecar **自动注入 header**，架构师无需在时序图里
  画 Zipkin 箭头
- **弹性**：超时、重试、 Hedging、**SlowStart** 都是 **Envoy 参数**，可被 **SLO
  驱动地自动调优**

## 7 服务组合模式

### 7.1 组合模式类型

| 组合模式            | 说明               | 典型实现               |
| ------------------- | ------------------ | ---------------------- |
| **Pipeline**        | 顺序执行多个过滤器 | Envoy Filter Chain     |
| **Fan-out**         | 并行调用多个服务   | Envoy Weighted Cluster |
| **Fan-in**          | 聚合多个服务响应   | Envoy Aggregator       |
| **Circuit Breaker** | 熔断保护           | Envoy Circuit Breaker  |
| **Retry**           | 重试机制           | Envoy Retry Policy     |
| **Rate Limit**      | 限流保护           | Envoy Rate Limit       |

### 7.2 组合示例

**Pipeline 组合**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: order-service
spec:
  http:
    - route:
        - destination:
            host: order-service
        fault:
          delay:
            percentage:
              value: 0.1
            fixedDelay: 5s
        retries:
          attempts: 3
          perTryTimeout: 2s
          retryOn: 5xx,reset,connect-failure,refused-stream
```

**Fan-out 组合**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: aggregate-service
spec:
  http:
    - route:
        - destination:
            host: service-a
          weight: 50
        - destination:
            host: service-b
          weight: 50
```

## 8 形式化定义

### 8.1 服务组合定义

```text
服务组合 C = ⟨filters, orchestration, policies⟩
其中：
- filters: 过滤器集合
- orchestration: 编排逻辑
- policies: 策略配置
```

### 8.2 Filter Chain 定义

```text
FilterChain = [Filter₁, Filter₂, ..., Filterₙ]
其中：
- Filterᵢ = ⟨type, config, order⟩
- type ∈ {auth, rate-limit, circuit-breaker, retry, transform, cache, forward}
- order: 执行顺序
```

### 8.3 服务组合函数

```text
服务组合函数 Compose: Filters → Service
其中 Compose(filters) 将过滤器组合成服务
```

## 9 架构收益

### 9.1 可组合性

- **Filter Chain 可编排**：支持 Pipeline、Fan-out、Fan-in 等组合模式
- **策略可组合**：支持多种策略组合使用

### 9.2 可版本化

- **CRD 可版本化**：VirtualService 和 EnvoyFilter 可版本化
- **GitOps**：所有配置在 Git 中，可回溯

### 9.3 可测试性

- **自动化测试**：k6+prometheus 自动测试
- **A/B 测试**：支持灰度发布和 A/B 测试

### 9.4 可观测性

- **统一监控**：所有流量都经过 sidecar，统一监控
- **自动追踪**：trace 自动注入，无需修改代码

## 10 总结

通过**服务组合**，Service Mesh 实现了：

1. **从"跨服务流"到"可编排的本地函数"**：通过 Filter Chain 实现细粒度控制
2. **组合粒度从"进程"降到"请求路径"**：支持请求级别的流量控制
3. **组合语义上升到"架构描述层"**：用 CRD 描述服务组合工作流
4. **架构设计范式转换**：从"先定接口，再定部署"到"先定流量，再定接口"
5. **非功能性从"后期治理"变为"设计期可组合元素"**：安全、可观测、弹性成为设计期
   元素

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
914-983 行，服务组合部分
