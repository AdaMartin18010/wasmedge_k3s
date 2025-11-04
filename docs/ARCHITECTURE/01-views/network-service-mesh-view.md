# Network Service Mesh (NSM) 架构视角

## 目录

- [1. 目标与视角](#1-目标与视角)
- [2. 关键概念](#2-关键概念)
- [3. 架构层次（C4 视角）](#3-架构层次c4-视角)
- [4. 组合模式与技术实现](#4-组合模式与技术实现)
- [5. 设计论证](#5-设计论证)
- [6. 典型实现步骤](#6-典型实现步骤)
- [7. 最佳实践](#7-最佳实践)
- [8. 关键论证点](#8-关键论证点)
- [9. 架构设计范式的反向重塑](#9-架构设计范式的反向重塑)
- [10. 总结](#10-总结)
- [11. 参考资源](#11-参考资源)

---

## 1. 目标与视角

**从"架构"角度**把整个 **软件栈**拆分为 **可组合、可监控、可弹性** 的多层体系。

> **Network Service Mesh (NSM)** 的目标是把 **Service Mesh** 视为 **"网络服务
> "**，再通过 **NSM** 把 _多种网络节点_（Pod、VM、物理服务器、跨集群、边缘设备）
> 聚合到一个统一的**服务网格**，从而实现 **跨域、跨云、跨平台** 的网络治理。

### 核心思想

1. **Service Mesh 作为 Network Service**：把 Istio/Linkerd 的 **vL3** 与
   **Endpoint** 抽象为 **NSM Network Service**
2. **NSM 允许多 Service Mesh 叠加**：在同一 vL3 上注册多个 **Network Service**
3. **通过 vWire 细粒度流量治理**：vWire 负责 **TLS、熔断、限流**，可携带
   `labels` 进行流量路由

---

## 2. 关键概念

| 名称                           | 典型技术                       | 主要职责                                                                           |
| ------------------------------ | ------------------------------ | ---------------------------------------------------------------------------------- |
| **Service Mesh**               | Istio, Linkerd, Consul, Kuma   | 代理、流量治理、服务治理、熔断、监控、MTLS、侧车注入                               |
| **Network Service Mesh (NSM)** | Network-Service-Mesh.io        | 把任意工作负载（Pod、VM、物理机）连接到 **"网络服务"**；支持多网格、多云、跨域网络 |
| **网络服务 (Network Service)** | vL3、IPsec、WAF、IPS、DNS、VPN | 连接、加密、监控、策略、DNS 解析                                                   |
| **vWire (Virtual Wire)**       | 逻辑隧道                       | 负责在 **Client** 与 **Endpoint** 之间转发数据；可携带安全/可观测信息              |
| **Client / Endpoint**          | Pod、VM、物理机                | 参与 NSM 连接的终端，或提供网络服务的终端                                          |

---

## 3. 架构层次（C4 视角）

```text
+-----------------------------------------------------------+
│ 1. 应用层  (业务微服务)                                 │
│  └─ Service Mesh  (Istio/Linkerd sidecars)              │
+-----------------------------------------------------------+
          ▲
+-----------------------------------------------------------+
│ 2. 服务网格层 (Service Mesh)                            │
│  └─ Service‑Mesh Sidecar + Control Plane                │
+-----------------------------------------------------------+
          ▲
+-----------------------------------------------------------+
│ 3. 网络服务层 (NSM)                                      │
│  └─ vL3  +  vWire + Network Service Endpoints          │
+-----------------------------------------------------------+
          ▲
+-----------------------------------------------------------+
│ 4. 基础设施层 (K8s/VM/物理)                              │
│  └─ Pods / VMs / Physical Servers (Clients / Endpoints)│
+-----------------------------------------------------------+
```

### 层次划分

1. **应用层** – 业务功能
2. **Service Mesh** – 流量治理与安全
3. **NSM** – 跨域网络聚合
4. **基础设施** – Pod、VM、物理机

> 通过 **"侧车 + vWire"** 的组合，任何节点（Pod、VM、物理机）都可以无缝加入同一
> 服务网格，完成跨域治理。

---

## 4. 组合模式与技术实现

### 4.1 组合 Service Mesh 作为 Network Service

| 步骤                                          | 关键技术                                                                   | 结果                                             |
| --------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------ |
| **1. 把 Service Mesh 打包为 Network Service** | 把 Istio/Linkerd 的 **vL3** 与 **Endpoint** 抽象为 **NSM Network Service** | 业务层可像使用普通服务一样 "连接"到 Service Mesh |
| **2. NSM 允许多 Service Mesh 叠加**           | 在同一 vL3 上注册多个 **Network Service**（例如 Istio、Linkerd、Kuma）     | 一个 Pod 可同时访问多个网格，实现 _双向连接_     |
| **3. 通过 vWire 细粒度流量治理**              | vWire 负责 **TLS、熔断、限流**；可携带 `labels` 进行流量路由               | 统一流量策略，避免在业务层实现                   |

**技术栈示例**：

```bash
# 注册 Istio 为 NSM 网络服务
nsmctl ns create istio-namespace --namespace=istio-system

# 注册 VM 或物理服务器为 Endpoint
nsmctl endpoint create vm-endpoint --address=10.0.0.5

# 在 Pod 里请求 vWire
nsmctl client create orders-vwire --service=orders --endpoint=vm-endpoint
```

### 4.2 组合多云/跨集群网络

| 目标                   | 方案                                                                            | 关键技术                               |
| ---------------------- | ------------------------------------------------------------------------------- | -------------------------------------- |
| **跨 Kubernetes 集群** | 在每个集群部署 **NSM vL3**；使用 **NSM Federation**                             | `nsm create federated-network-service` |
| **跨物理机与云**       | 在物理机部署 **NSM Endpoint**（e.g., via `nsm-node` daemon）；使用 `vWire` 直连 | `nsmctl node create`                   |
| **跨多云**             | 在每个云环境部署 **NSM**，使用 **VPN** + `vWire` 连接                           | `nsm install --cloud`                  |

> 通过 **vWire**，流量可在 **Pod → VM → 物理机** 之间透明转发，且每个链路可独立
> 加密、监控。

---

## 5. 设计论证

### 5.1 为什么要把 Service Mesh 作为"网络服务"

| 传统 Service Mesh 关注点 | 限制                        | 作为 Network Service 的优势                             |
| ------------------------ | --------------------------- | ------------------------------------------------------- |
| 侧车代理、控制平面       | 仅在同一集群内运行          | 通过 **vWire** 连接跨集群、跨域                         |
| 网络策略、TLS            | 需要手工配置多域            | NSM 提供统一的 **身份验证**（Spiffe）、**授权**（OPA）  |
| 监控/日志                | 只覆盖 Mesh 内部            | NSM 能捕获 **跨边界** 的流量，可合并到 Prometheus/Tempo |
| 连接单点故障             | Mesh 与服务之间可能产生单点 | vWire 的多路径允许**负载均衡**、**故障转移**            |

> 通过将 Service Mesh 视为 **Network Service**，架构师只需关心 **"给业务提供哪些
> 网络功能"**，而不必去管理每个网格的细节。

### 5.2 组合网络服务的典型用例

| 场景                        | 组合方式                                                          | 关键技术                          | 业务价值                       |
| --------------------------- | ----------------------------------------------------------------- | --------------------------------- | ------------------------------ |
| **混合云（公有云 + 本地）** | 业务 Pod → Istio（公有云） → NSM vL3 → 本地 VMs → Physical Server | Istio, NSM, VPN, Spiffe           | 统一安全、统一可观测、无缝访问 |
| **多租户 SaaS**             | 业务 Pod → Istio (租户专属) → NSM (共享 vL3) → 共用 Endpoint      | Istio, NSM, Kubernetes Namespaces | 隔离 + 资源共享                |
| **边缘计算**                | 设备 → Edge NSM Node → Cloud NSM → Service Mesh                   | NSM, Edge Gateway, Istio          | 低延迟、统一治理               |
| **混合身份**                | Pod → Istio (MTLS) → NSM (Spiffe) → Identity Provider             | Istio, NSM, OIDC                  | 单一身份体系，跨域验证         |

---

## 6. 典型实现步骤

### 6.1 准备工作

1. 部署 **Kubernetes**（或裸机）
2. 安装 **NSM**：`nsmctl install`
3. 安装 **Service Mesh**（Istio/Linkerd）：`istioctl install`

### 6.2 注册网络服务

```bash
# 把 Istio 注册为 Network Service
nsmctl ns create istio-namespace --namespace=istio-system

# 注册 VM 或物理服务器为 Endpoint
nsmctl endpoint create vm-endpoint --address=10.0.0.5
```

### 6.3 为业务 Pod 创建 Client

```yaml
apiVersion: v1
kind: Service
metadata:
  name: orders
  namespace: prod
spec:
  selector:
    app: orders
  ports:
    - port: 80
```

```bash
# 通过 Istio sidecar 注入
istioctl kube-inject -f deployment.yaml | kubectl apply -f -
```

### 6.4 建立 vWire

```bash
# 在 Pod 里请求 vWire
nsmctl client create orders-vwire --service=orders --endpoint=vm-endpoint
```

### 6.5 验证 & 监控

- Prometheus + Grafana (Istio + NSM metrics)
- Tempo + Jaeger (跨域追踪)

### 6.6 安全与治理

- Spiffe ID 用于认证
- OPA/Gatekeeper 对 vWire 进行授权

---

## 7. 最佳实践

| 主题             | 关键建议                                                                             |
| ---------------- | ------------------------------------------------------------------------------------ |
| **隔离与多租户** | 在 NSM 里为每个租户创建单独的 vL3，使用 `labels` 控制访问                            |
| **可观测性**     | 在 NSM 的 `vWire` 上启用 **OpenTelemetry**；统一 Prometheus 报表                     |
| **弹性**         | vWire 支持 **多路径** 与 **自动重连**；在 Service Mesh 层配置熔断                    |
| **安全**         | 统一使用 **Spiffe** 证书；vWire 的 TLS 端点在 Endpoint 层完成                        |
| **多云**         | 对不同云使用不同的 NSM 节点，统一通过 **NSM Federation** 关联                        |
| **边缘**         | 在 Edge 节点部署 NSM Daemon，使用 `nsmctl node create` 让 Edge 直接访问 Service Mesh |

---

## 8. 关键论证点

### 8.1 可组合性

- Service Mesh 本身是 **网络服务**（Connectivity + Security + Observability）
- NSM 通过 **vWire** 把任何 "客户端" 与 "Endpoint" 连接，实现 **任意网络服务的组
  合**

### 8.2 抽象层次

- **业务层** → **Service Mesh**（侧车） → **NSM**（vL3） → **网络节点**（Pod/VM/
  物理）
- 每层只关心自己的职责，架构师可**聚焦业务**，不必管理细节

### 8.3 弹性与多租户

- vWire 的多路径、重连特性保证 **跨域可靠性**
- NSM 通过 `labels` 细粒度控制流量，支持 **多租户隔离**

### 8.4 安全统一

- Spiffe ID 统一身份验证；vWire 负责 **TLS/MTLS**
- OPA 与 NSM 的策略组合，实现 **细粒度授权**

### 8.5 观测统一

- Prometheus/Tempo/Jaeger 通过 Service Mesh 与 NSM 的**Exporters** 汇聚，形成
  **单一监控面板**

---

## 9. 架构设计范式的反向重塑

### 9.1 从"分层图"到"过滤器图"

**传统架构图**：

```text
Edge LB → API Gateway → Biz Service → Cache → DB
```

**NSM 时代等价图**：

```text
Request → [JWT|RBAC|RateLimit|Circuit|Retry|Transform] → upstream
```

> 整条链路由 **CRD 描述**，可 **版本化、差异比对、自动化测试**

### 9.2 非功能性从"后期治理"变为"设计期可组合元素"

- **安全**：mTLS 自动轮转，**架构图里把"锁"图标换成 Policy 对象**
- **可观测**：trace/metric 由 sidecar **自动注入 header**，架构师无需在时序图里
  画 Zipkin 箭头
- **弹性**：超时、重试、Hedging、**SlowStart** 都是 **Envoy 参数**，可被 **SLO
  驱动地自动调优**

---

## 10. 总结

> **将 Server‑Mesh 与 Network Service Mesh 组合**，可以把整个网络层从"技术细节"
> 剥离，形成一个 **可组合、可治理、可扩展** 的网络服务集成平台。架构师只需在业务
> 层定义接口和需求，**Service Mesh/NSM** 负责"如何将业务与网络连接起来"，从而让"
> 聚合网络节点"和"组合网络服务"成为自然的、可重复的设计模式。

### 核心价值

1. **跨域网络聚合**：Pod、VM、物理机无缝连接
2. **统一网络治理**：Service Mesh + NSM 形成统一控制平面
3. **细粒度安全**：Spiffe + OPA 实现细粒度访问控制
4. **统一可观测**：OpenTelemetry 统一监控、日志、追踪

---

## 11. 参考资源

- **Network Service Mesh**：<https://networkservicemesh.io>
- **Istio**：<https://istio.io>
- **OpenTelemetry**：<https://opentelemetry.io>
- **Spiffe**：<https://spiffe.io>

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
1.1-1.2 节，Network Service Mesh 视角部分
