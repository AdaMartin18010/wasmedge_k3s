# NSM 架构：Network Service Mesh 网络抽象

## 1. 概述

本文档详细阐述**Network Service Mesh (NSM)** 的架构设计，这是将 Service Mesh 作
为 Network Service 的网络抽象层。

### 1.1 核心思想

> **NSM 通过 vL3、vWire、Endpoints 实现跨域网络聚合，将 Service Mesh 作为
> Network Service 统一管理**

## 2. NSM 核心概念

### 2.1 关键概念

| 名称                           | 典型技术                       | 主要职责                                                                           |
| ------------------------------ | ------------------------------ | ---------------------------------------------------------------------------------- |
| **Service Mesh**               | Istio, Linkerd, Consul, Kuma   | 代理、流量治理、服务治理、熔断、监控、MTLS、侧车注入                               |
| **Network Service Mesh (NSM)** | Network‑Service‑Mesh.io        | 把任意工作负载（Pod、VM、物理机）连接到 **"网络服务"**；支持多网格、多云、跨域网络 |
| **网络服务 (Network Service)** | vL3、IPsec、WAF、IPS、DNS、VPN | 连接、加密、监控、策略、DNS 解析                                                   |
| **vWire (Virtual Wire)**       | 逻辑隧道                       | 负责在 **Client** 与 **Endpoint** 之间转发数据；可携带安全/可观测信息              |
| **Client / Endpoint**          | Pod、VM、物理机                | 参与 NSM 连接的终端，或提供网络服务的终端                                          |

### 2.2 NSM 架构层次

```text
+-----------------------------------------------------------+
| 1. 应用层  (业务微服务)                                 |
|   └─ Service Mesh  (Istio/Linkerd sidecars)              |
+-----------------------------------------------------------+
| 2. 服务网格层 (Service Mesh)                            |
|   └─ Service‑Mesh Sidecar + Control Plane                |
+-----------------------------------------------------------+
| 3. 网络服务层 (NSM)                                      |
|   └─ vL3  +  vWire + Network Service Endpoints          |
+-----------------------------------------------------------+
| 4. 基础设施层 (K8s/VM/物理)                              |
|   └─ Pods / VMs / Physical Servers (Clients / Endpoints)|
+-----------------------------------------------------------+
```

## 3. NSM 核心组件

### 3.1 vL3（虚拟 L3 网络）

**vL3** 是 NSM 的虚拟 L3 网络层，提供：

- **网络抽象**：将物理网络抽象为虚拟网络
- **服务发现**：发现和注册网络服务
- **路由管理**：管理虚拟网络路由

### 3.2 vWire（虚拟隧道）

**vWire** 是 NSM 的虚拟隧道，提供：

- **逻辑隧道**：在 Client 与 Endpoint 之间建立逻辑隧道
- **数据转发**：负责数据转发，可携带安全/可观测信息
- **跨域连接**：支持跨集群、跨云、跨硬件连接

### 3.3 Endpoints（端点）

**Endpoints** 是 NSM 的端点，包括：

- **Client**：请求网络服务的客户端（Pod、VM、物理机）
- **Endpoint**：提供网络服务的端点（Pod、VM、物理机）

## 4. NSM 架构设计

### 4.1 把 Service Mesh 打包为 Network Service

**步骤**：

1. **注册 Service Mesh**：把 Istio/Linkerd 的 **vL3** 与 **Endpoint** 抽象为
   **NSM Network Service**
2. **NSM 允许多 Service Mesh 叠加**：在同一 vL3 上注册多个 **Network Service**（
   例如 Istio、Linkerd、Kuma）
3. **通过 vWire 细粒度流量治理**：vWire 负责 **TLS、熔断、限流**；可携带
   `labels` 进行流量路由

**示例**：

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

**通过 vWire**，流量可在 **Pod → VM → 物理机** 之间透明转发，且每个链路可独立加
密、监控。

## 5. NSM 与 Service Mesh 的组合

### 5.1 组合方式

**组合策略**：

1. **把 Service Mesh 作为 Network Service** 注册到 NSM
2. 在 **Pod** 内通过 `Istio` 侧车注入，`nsmctl client create` 生成 `vWire` 与
   **Endpoint** 连接
3. 通过 **NSM Federation** 把多集群、跨云的 Service Mesh 互联

### 5.2 典型场景

**混合云（公有云 + 本地）**：

```text
业务 Pod → Istio（公有云） → NSM vL3 → 本地 VMs → Physical Server
```

**多租户 SaaS**：

```text
业务 Pod → Istio (租户专属) → NSM (共享 vL3) → 共用 Endpoint
```

**边缘计算**：

```text
设备 → Edge NSM Node → Cloud NSM → Service Mesh
```

## 6. NSM 架构优势

### 6.1 跨域网络聚合

- **跨集群**：支持跨 Kubernetes 集群连接
- **跨云**：支持跨公有云和私有云连接
- **跨硬件**：支持 Pod、VM、物理机统一管理

### 6.2 统一网络治理

- **统一策略**：通过 NSM 统一管理网络策略
- **统一监控**：通过 NSM 统一监控网络流量
- **统一安全**：通过 NSM 统一实施安全策略

### 6.3 可组合性

- **多 Service Mesh 叠加**：支持多个 Service Mesh 同时运行
- **灵活组合**：支持不同的网络服务组合

## 7. 形式化定义

### 7.1 NSM 架构定义

```text
NSM = ⟨vL3, vWire, endpoints, clients⟩
其中：
- vL3: 虚拟 L3 网络
- vWire: 虚拟隧道集合
- endpoints: 端点集合
- clients: 客户端集合
```

### 7.2 vWire 定义

```text
vWire = ⟨client, endpoint, tunnel, policies⟩
其中：
- client: 客户端
- endpoint: 端点
- tunnel: 隧道配置
- policies: 策略配置（安全、监控、路由）
```

### 7.3 Network Service 定义

```text
NetworkService = ⟨name, vL3, endpoints, policies⟩
其中：
- name: 服务名称
- vL3: 虚拟 L3 网络
- endpoints: 端点集合
- policies: 策略配置
```

## 8. 总结

通过**NSM 架构**，我们可以：

1. **跨域网络聚合**：支持跨集群、跨云、跨硬件统一管理
2. **统一网络治理**：通过 NSM 统一管理网络策略、监控、安全
3. **可组合性**：支持多个 Service Mesh 叠加和灵活组合
4. **透明转发**：通过 vWire 实现 Pod → VM → 物理机透明转发

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
391-610 行，NSM 部分
