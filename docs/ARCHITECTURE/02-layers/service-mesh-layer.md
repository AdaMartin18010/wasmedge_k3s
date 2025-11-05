# Service Mesh 层架构

## 目录

---

## 📋 概述

Service Mesh 层是在应用层之下，提供网络服务治理的中间层。它通过 Sidecar 代理模式
，将网络功能从业务代码中剥离，实现流量治理、安全、可观测性的统一管理。

## 🎯 核心职责

### 1. 流量治理

- **路由规则**：基于标签、版本的路由
- **负载均衡**：多种负载均衡算法
- **熔断降级**：故障隔离和快速失败
- **限流控制**：请求速率限制

### 2. 安全通信

- **mTLS**：双向 TLS 加密
- **身份认证**：SPIFFE/SPIRE
- **授权策略**：基于角色的访问控制（RBAC）
- **零信任网络**：默认拒绝、最小权限

### 3. 可观测性

- **分布式追踪**：OpenTelemetry、Jaeger
- **指标监控**：Prometheus、Grafana
- **日志聚合**：Fluentd、Loki
- **服务拓扑**：动态服务依赖图

### 4. 策略治理

- **OPA 集成**：策略即代码
- **配置管理**：统一配置中心
- **版本管理**：灰度发布、金丝雀部署

## 🏗️ 架构层次

```text
┌─────────────────────────────────────┐
│      Application Layer              │
│  (业务微服务、业务逻辑)              │
└─────────────────────────────────────┘
                 ▲
┌─────────────────────────────────────┐
│      Service Mesh Layer              │
│  ├─ Data Plane (Envoy sidecar)      │
│  │   ├─ 流量路由                      │
│  │   ├─ 负载均衡                      │
│  │   ├─ 熔断降级                      │
│  │   └─ mTLS 加密                     │
│  ├─ Control Plane (Istio/Linkerd)   │
│  │   ├─ 配置管理                      │
│  │   ├─ 服务发现                      │
│  │   └─ 策略下发                      │
│  └─ Observability (OTel)            │
│      ├─ 分布式追踪                    │
│      ├─ 指标监控                      │
│      └─ 日志聚合                      │
└─────────────────────────────────────┘
                 ▲
┌─────────────────────────────────────┐
│      Network Service Mesh (NSM)      │
│  (跨域网络聚合)                       │
└─────────────────────────────────────┘
```

## 🔧 技术实现

### 1. Istio

**架构组件**：

- **Envoy**：数据平面代理
- **Istiod**：控制平面
- **Pilot**：服务发现和配置管理
- **Citadel**：证书管理
- **Galley**：配置验证

**核心 CRD**：

- `VirtualService`：路由规则
- `DestinationRule`：负载均衡策略
- `AuthorizationPolicy`：授权策略
- `PeerAuthentication`：mTLS 配置

### 2. Linkerd

**架构组件**：

- **Linkerd-proxy**：Rust 实现的轻量级代理
- **Linkerd-control-plane**：控制平面
- **Linkerd-viz**：可视化组件

**特点**：

- 轻量级（< 10 MB 内存）
- 低延迟（< 1 ms P99）
- 简单易用

### 3. Consul Connect

**架构组件**：

- **Consul Agent**：服务注册与发现
- **Consul Connect**：服务网格
- **Envoy**：数据平面

**特点**：

- 多数据中心支持
- 服务发现集成
- 丰富的生态

## 📊 Service Mesh 对比矩阵

| 属性         | Istio            | Linkerd        | Consul Connect | Kuma         |
| ------------ | ---------------- | -------------- | -------------- | ------------ |
| **代理**     | Envoy            | Linkerd-proxy  | Envoy          | Envoy        |
| **语言**     | Go/Java          | Rust           | Go             | Go           |
| **资源占用** | 高（~100 MB）    | 低（~10 MB）   | 中（~50 MB）   | 中（~50 MB） |
| **延迟**     | < 1 ms           | < 1 ms         | < 1 ms         | < 1 ms       |
| **学习曲线** | 陡峭             | 平缓           | 中等           | 中等         |
| **生态**     | 丰富             | 中等           | 丰富           | 中等         |
| **适用场景** | 企业级、复杂场景 | 简单场景、边缘 | 多数据中心     | 多云         |

## 🔐 安全模型

### 1. 身份驱动拓扑

**传统模型**：

```text
节点 = IP:Port
拓扑 = 静态路由表
```

**Service Mesh 模型**：

```text
节点 = SPIFFE ID (身份)
拓扑 = 动态 xDS 配置
路由 = 基于标签/版本
```

### 2. mTLS 自动轮转

**流程**：

1. **SPIRE** 生成 SPIFFE 证书
2. **Istio Citadel** 管理证书生命周期
3. **Envoy** 自动使用证书进行 mTLS
4. **证书自动轮转**：定期更新

### 3. 零信任网络

**原则**：

- 默认拒绝所有流量
- 显式授权才允许
- 最小权限原则
- 持续验证

## 🔗 与 Network Service Mesh 的关系

### Service Mesh 作为 Network Service

**组合方式**：

1. 将 Service Mesh 注册为 NSM Network Service
2. 通过 vWire 连接跨域节点
3. 统一网络治理

**示例**：

```bash
# 注册 Istio 为 NSM 网络服务
nsmctl ns create istio-namespace --namespace=istio-system

# 创建 vWire 连接
nsmctl client create orders-vwire --service=orders --endpoint=vm-endpoint
```

## 📈 节点聚合：从物理地址到身份驱动拓扑

### 传统模型 vs Service Mesh 模型

| 维度         | 传统 TCP/HTTP        | Service Mesh        |
| ------------ | -------------------- | ------------------- |
| **节点标识** | IP:Port              | SPIFFE ID (身份)    |
| **拓扑生成** | kube-proxy/IPVS 静态 | 控制面 xDS 动态下发 |
| **负载均衡** | 语言 SDK 耦合        | Envoy 可插拔 filter |
| **服务发现** | DNS/A 记录           | Envoy CDS + EDS     |
| **版本管理** | 手动 DNS 切换        | 标签选择器 + 权重   |

### 聚合逻辑成为声明式配置

**传统方式**：

```yaml
# 硬编码在代码中
apiVersion: v1
kind: Service
metadata:
  name: orders
spec:
  selector:
    app: orders
    version: v1 # 硬编码版本
```

**Service Mesh 方式**：

```yaml
# 声明式配置
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: orders
spec:
  http:
    - match:
        - headers:
            x-canary:
              exact: "1"
      route:
        - destination:
            host: orders
            subset: v2
          weight: 100
    - route:
        - destination:
            host: orders
            subset: v1
          weight: 90
        - destination:
            host: orders
            subset: v2
          weight: 10
```

## 📊 服务组合：从跨服务流到可编排的本地函数

### Envoy Filter Chain

**Pipeline 模式**：

```text
Request → [Auth] → [RateLimit] → [CircuitBreaker] → [Retry] → [Transform] → [Cache] → Upstream
```

**可编程 Lambda**：

- 每条 filter 可热插拔
- A/B 对比
- 灰度发布

### 组合语义上升到架构描述层

**架构图从"分层图"到"过滤器图"**：

传统架构图：

```text
Edge LB → API Gateway → Biz Service → Cache → DB
```

Service Mesh 时代：

```text
Request → [JWT|RBAC|RateLimit|Circuit|Retry|Transform] → Upstream
```

## 🔄 架构设计范式重塑

### 1. "先定接口，再定部署" → "先定流量，再定接口"

- **流量特征**（延迟、重试、超时、安全）先于 **Java interface/proto file** 被固
  定
- **接口演进** = VirtualService 版本化
- 不再需要 v1/v2 两套代码仓库

### 2. 非功能性从"后期治理"变为"设计期可组合元素"

- **安全**：mTLS 自动轮转，架构图里把"锁"图标换成 Policy 对象
- **可观测**：trace/metric 由 sidecar 自动注入 header，架构师无需在时序图里画
  Zipkin 箭头
- **弹性**：超时、重试、Hedging、SlowStart 都是 Envoy 参数，可被 SLO 驱动地自动
  调优

## 🎯 最佳实践

### 1. 渐进式采用

- 从关键服务开始
- 逐步扩展到全量服务
- 监控性能和稳定性

### 2. 统一配置管理

- 使用 GitOps 管理配置
- 版本化配置变更
- 自动化测试

### 3. 可观测性优先

- 部署前先建立可观测性
- 分布式追踪、指标、日志全覆盖
- 建立告警机制

### 4. 安全策略

- 启用 mTLS
- 实施零信任网络
- 定期审计策略

## 📚 参考资源

- **Istio**：<https://istio.io/>
- **Linkerd**：<https://linkerd.io/>
- **Consul**：<https://www.consul.io/>
- **Envoy**：<https://www.envoyproxy.io/>
- **SPIFFE**：<https://spiffe.io/>

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` Service
Mesh 层部分
