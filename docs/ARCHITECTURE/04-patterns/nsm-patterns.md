# Network Service Mesh 模式

## 📑 目录

- [1. 概述](#1-概述)
- [🎯 核心模式](#-核心模式)
  - [1. Service Mesh 作为 Network Service](#1-service-mesh-作为-network-service)
  - [2. 多 Service Mesh 叠加模式](#2-多-service-mesh-叠加模式)
  - [3. 跨域网络聚合模式](#3-跨域网络聚合模式)
- [🔧 技术实现](#-技术实现)
  - [1. 注册 Service Mesh 为 Network Service](#1-注册-service-mesh-为-network-service)
  - [2. 创建 vWire 连接](#2-创建-vwire-连接)
  - [3. 多集群 Federation](#3-多集群-federation)
- [📊 模式对比矩阵](#-模式对比矩阵)
- [🔗 组合模式](#-组合模式)
  - [1. Service Mesh + NSM 组合](#1-service-mesh--nsm-组合)
  - [2. 多租户 SaaS 模式](#2-多租户-saas-模式)
  - [3. 边缘计算模式](#3-边缘计算模式)
- [🔐 安全模式](#-安全模式)
  - [1. 统一身份认证](#1-统一身份认证)
  - [2. 策略统一治理](#2-策略统一治理)
- [📈 演进路径](#-演进路径)
  - [第一阶段：单集群 Service Mesh（2017-2020）](#第一阶段单集群-service-mesh2017-2020)
  - [第二阶段：Multi-cluster Service Mesh（2020-2023）](#第二阶段multi-cluster-service-mesh2020-2023)
  - [第三阶段：Network Service Mesh（2023-2025）](#第三阶段network-service-mesh2023-2025)
  - [第四阶段：边缘计算集成（2025-）](#第四阶段边缘计算集成2025-)
- [🎯 最佳实践](#-最佳实践)
  - [1. 渐进式采用](#1-渐进式采用)
  - [2. 统一配置管理](#2-统一配置管理)
  - [3. 可观测性优先](#3-可观测性优先)
  - [4. 安全策略](#4-安全策略)
- [9. 参考资源](#9-参考资源)
  - [相关文档](#相关文档)
  - [学术资源](#学术资源)

---

## 1. 概述

Network Service Mesh (NSM) 模式提供了一种将 Service Mesh 作为网络服务进行组合的
架构模式。它通过 vWire（虚拟连线）和 vL3（虚拟 L3 网络）实现跨域网络服务的聚合，
支持 Pod、VM、物理机之间的统一网络治理。

## 🎯 核心模式

### 1. Service Mesh 作为 Network Service

**模式描述**：

- 将 Service Mesh（Istio/Linkerd）注册为 NSM Network Service
- 业务层可以像使用普通服务一样"连接"到 Service Mesh
- 实现跨域、跨云的网络服务统一治理

**架构图**：

```text
┌─────────────────────────────────────┐
│      Application Layer              │
│  (业务微服务)                        │
└─────────────────────────────────────┘
                 ▲
┌─────────────────────────────────────┐
│      Service Mesh Layer             │
│  (Istio/Linkerd sidecar)            │
└─────────────────────────────────────┘
                 ▲
┌─────────────────────────────────────┐
│      Network Service Mesh           │
│  ├─ vL3 (虚拟 L3 网络)               │
│  ├─ vWire (虚拟连线)                 │
│  └─ Network Service Endpoints       │
│      ├─ Pod Endpoints               │
│      ├─ VM Endpoints                │
│      └─ Physical Server Endpoints   │
└─────────────────────────────────────┘
```

### 2. 多 Service Mesh 叠加模式

**模式描述**：

- 在同一 vL3 上注册多个 Network Service（例如 Istio、Linkerd、Kuma）
- 一个 Pod 可同时访问多个网格
- 实现双向连接和灵活组合

**实现示例**：

```bash
# 注册 Istio 为 Network Service
nsmctl ns create istio-namespace --namespace=istio-system

# 注册 Linkerd 为 Network Service
nsmctl ns create linkerd-namespace --namespace=linkerd-system

# Pod 可以同时连接两个网格
nsmctl client create multi-mesh-vwire \
  --service=istio-namespace \
  --service=linkerd-namespace
```

### 3. 跨域网络聚合模式

**模式描述**：

- 通过 NSM Federation 连接多个集群
- 支持跨 Kubernetes 集群、跨云、跨物理机
- 统一网络治理和安全策略

**架构图**：

```text
Cluster A (K8s) ──NSM Federation── Cluster B (K8s)
     │                                  │
     └─────── vWire ────────┐           │
                           │            │
                    Physical Server ────┘
```

## 🔧 技术实现

### 1. 注册 Service Mesh 为 Network Service

```bash
# 创建 NSM Network Service
nsmctl ns create istio-mesh \
  --namespace=istio-system \
  --address=10.0.0.0/24 \
  --labels=app=istio,version=v1.15
```

### 2. 创建 vWire 连接

```bash
# 客户端请求 vWire
nsmctl client create orders-vwire \
  --service=orders \
  --endpoint=vm-endpoint \
  --labels=env=prod,version=v2
```

### 3. 多集群 Federation

```bash
# 创建 Federation
nsmctl federation create multi-cluster-federation \
  --clusters=cluster-a,cluster-b \
  --namespace=istio-system
```

## 📊 模式对比矩阵

| 模式         | 传统 Service Mesh | NSM 模式               |
| ------------ | ----------------- | ---------------------- |
| **网络边界** | 单集群内          | 跨集群、跨云、跨物理机 |
| **节点类型** | Pod 为主          | Pod、VM、物理机统一    |
| **连接方式** | Sidecar 注入      | vWire 动态连接         |
| **治理范围** | 集群内            | 跨域统一治理           |
| **适用场景** | 单集群微服务      | 多云、混合云、边缘计算 |

## 🔗 组合模式

### 1. Service Mesh + NSM 组合

**模式**：Adapter/Bridge 模式

**描述**：

- Service Mesh 作为网络服务的适配器
- NSM 作为跨域网络的桥接器
- 组合后实现跨域统一治理

**示例**：

```text
Pod (Cluster A) ──Istio Sidecar──> NSM vWire ──> Pod (Cluster B)
                                          │
                                          └──> VM (Data Center)
                                          └──> Physical Server (Edge)
```

### 2. 多租户 SaaS 模式

**模式**：Facade 模式

**描述**：

- 每个租户拥有独立的 Service Mesh
- 共享 NSM vL3 基础设施
- 通过标签隔离不同租户

**实现**：

```yaml
# 租户 A 的 Service Mesh
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: tenant-a-service
  labels:
    tenant: tenant-a
spec:
  # ...

# 租户 B 的 Service Mesh
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: tenant-b-service
  labels:
    tenant: tenant-b
spec:
  # ...

# NSM 通过标签路由
nsmctl client create tenant-a-vwire \
  --service=tenant-a-service \
  --labels=tenant=tenant-a
```

### 3. 边缘计算模式

**模式**：Gateway 模式

**描述**：

- 边缘设备通过 NSM 连接到云端 Service Mesh
- 实现低延迟、统一治理
- 支持离线能力和边缘自治

**架构图**：

```text
Edge Device ──Edge NSM Node──> Cloud NSM ──> Service Mesh
                                    │
                                    └──> Cloud Services
```

## 🔐 安全模式

### 1. 统一身份认证

**模式**：SPIFFE/SPIRE 集成

**描述**：

- NSM 使用 SPIFFE ID 作为统一身份标识
- Service Mesh 使用 SPIFFE 证书进行 mTLS
- 跨域身份验证无缝衔接

**实现**：

```yaml
# NSM 配置 SPIFFE
apiVersion: nsm.networkservicemesh.io/v1
kind: NetworkServiceEndpoint
metadata:
  name: istio-endpoint
spec:
  networkService: istio-mesh
  spiffeId: spiffe://cluster-a/ns/default/sa/istio
```

### 2. 策略统一治理

**模式**：OPA + NSM 组合

**描述**：

- OPA 定义跨域访问策略
- NSM 执行策略决策
- Service Mesh 执行流量策略

**实现**：

```rego
# OPA 策略
package nsm.authz

default allow = false

allow {
  input.source.spiffeId = "spiffe://cluster-a/ns/default/sa/frontend"
  input.destination.spiffeId = "spiffe://cluster-b/ns/default/sa/backend"
  input.action = "connect"
}
```

## 📈 演进路径

### 第一阶段：单集群 Service Mesh（2017-2020）

- **特点**：Istio、Linkerd 在单集群内提供服务网格
- **限制**：跨集群需要手动配置 VPN

### 第二阶段：Multi-cluster Service Mesh（2020-2023）

- **特点**：Istio Multi-cluster、Linkerd Multi-cluster
- **限制**：主要支持 K8s 集群，不支持 VM、物理机

### 第三阶段：Network Service Mesh（2023-2025）

- **特点**：NSM 统一管理 Pod、VM、物理机
- **优势**：跨域统一治理、灵活组合

### 第四阶段：边缘计算集成（2025-）

- **特点**：边缘设备、IoT 设备接入
- **趋势**：边缘自治、离线能力

## 🎯 最佳实践

### 1. 渐进式采用

- 从单集群开始
- 逐步扩展到多集群
- 最后集成 VM 和物理机

### 2. 统一配置管理

- 使用 GitOps 管理配置
- 版本化配置变更
- 自动化测试

### 3. 可观测性优先

- 部署前建立可观测性
- 分布式追踪、指标、日志全覆盖
- 建立告警机制

### 4. 安全策略

- 启用统一身份认证（SPIFFE）
- 实施零信任网络
- 定期审计策略

## 9. 参考资源

- **Network Service Mesh**：<https://networkservicemesh.io/>
- **Istio**：<https://istio.io>
- **NSM 文档**：<https://networkservicemesh.io/docs>

### 相关文档

- `architecture-view/08-composition-patterns/05-nsm-pattern.md` - NSM 模式详细说
  明
- `01-views/network-service-mesh-view.md` - Network Service Mesh 视角文档
- `architecture-view/08-composition-patterns/05-nsm-pattern.md#service-aggregation` -
  Service Aggregation 模式详细说明

### 学术资源

- **[ACADEMIC-REFERENCES.md](../ACADEMIC-REFERENCES.md)** - Wikipedia、大学课程
  、学术论文等学术资源
- **[REFERENCES.md](../REFERENCES.md)** - 参考标准、框架、工具和资源

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` NSM 模
式部分
