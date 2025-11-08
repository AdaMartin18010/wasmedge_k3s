# NSM 模式：跨域网络聚合

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 核心思想](#11-核心思想)
- [2. NSM 模式定义](#2-nsm-模式定义)
  - [2.1 NSM 模式概念](#21-nsm-模式概念)
  - [2.2 NSM 模式结构](#22-nsm-模式结构)
  - [2.3 NSM 模式特点](#23-nsm-模式特点)
- [3. NSM 核心概念](#3-nsm-核心概念)
  - [3.1 vL3（虚拟 L3 网络）](#31-vl3虚拟-l3-网络)
  - [3.2 vWire（虚拟隧道）](#32-vwire虚拟隧道)
  - [3.3 Endpoints（端点）](#33-endpoints端点)
  - [3.4 Clients（客户端）](#34-clients客户端)
- [4. NSM 与 Service Mesh 的组合](#4-nsm-与-service-mesh-的组合)
  - [4.1 组合架构](#41-组合架构)
  - [4.2 组合步骤](#42-组合步骤)
  - [4.3 组合示例](#43-组合示例)
- [5. NSM 模式实现](#5-nsm-模式实现)
  - [5.1 NSM 安装](#51-nsm-安装)
  - [5.2 NSM 客户端配置](#52-nsm-客户端配置)
  - [5.3 NSM 跨域连接](#53-nsm-跨域连接)
- [6. NSM 模式优势](#6-nsm-模式优势)
  - [6.1 跨域聚合](#61-跨域聚合)
  - [6.2 细粒度治理](#62-细粒度治理)
  - [6.3 多 Service Mesh 叠加](#63-多-service-mesh-叠加)
- [7. NSM 模式与其他模式](#7-nsm-模式与其他模式)
  - [7.1 NSM vs Service Mesh](#71-nsm-vs-service-mesh)
  - [7.2 NSM vs VPN](#72-nsm-vs-vpn)
- [8. 形式化定义](#8-形式化定义)
  - [8.1 NSM 模式定义](#81-nsm-模式定义)
  - [8.2 vWire 定义](#82-vwire-定义)
  - [8.3 Endpoint 定义](#83-endpoint-定义)
- [9. 相关文档](#9-相关文档)
  - [9.1 组合模式文档](#91-组合模式文档)
  - [9.2 参考资源](#92-参考资源)
- [10. 总结](#10-总结)

---

## 1. 概述

本文档详细阐述**NSM（Network Service Mesh）模式**在架构设计中的应用，通过跨域网
络聚合实现统一网络治理。

### 1.1 核心思想

> **通过 NSM 模式实现跨域网络聚合，将 Service Mesh 作为 Network Service 统一管理
> ，实现 Pod、VM、物理机的统一网络连接**

## 2. NSM 模式定义

### 2.1 NSM 模式概念

**NSM 模式**是一种网络架构模式，通过跨域网络聚合实现统一网络治理。

### 2.2 NSM 模式结构

```text
NSM Network
├── vL3 (虚拟 L3 网络)
├── vWire (虚拟隧道)
├── Endpoints (端点)
└── Clients (客户端)
    ├── Pod (Kubernetes)
    ├── VM (虚拟机)
    └── Physical Machine (物理机)
```

### 2.3 NSM 模式特点

**NSM 模式特点**：

- **跨域聚合**：聚合 Pod、VM、物理机
- **统一网络**：统一的网络抽象
- **细粒度治理**：vWire 支持细粒度流量治理
- **透明连接**：透明的跨域连接

## 3. NSM 核心概念

### 3.1 vL3（虚拟 L3 网络）

**vL3 定义**：

- **虚拟 L3 网络**：虚拟的 L3 网络层
- **服务发现**：通过 vL3 实现服务发现
- **路由**：通过 vL3 实现路由

### 3.2 vWire（虚拟隧道）

**vWire 定义**：

- **虚拟隧道**：虚拟的网络隧道
- **流量治理**：通过 vWire 实现流量治理
- **安全**：通过 vWire 实现加密和认证

### 3.3 Endpoints（端点）

**Endpoints 定义**：

- **服务端点**：服务的网络端点
- **服务注册**：通过 Endpoints 注册服务
- **服务发现**：通过 Endpoints 发现服务

### 3.4 Clients（客户端）

**Clients 定义**：

- **客户端**：使用 NSM 的客户端
- **跨域支持**：支持 Pod、VM、物理机
- **透明连接**：透明的跨域连接

## 4. NSM 与 Service Mesh 的组合

### 4.1 组合架构

**NSM + Service Mesh 组合**：

```text
Service Mesh (Istio/Linkerd)
    ├── vL3 (虚拟 L3 网络)
    └── Endpoints (端点)
        ↓
NSM Network
    ├── vL3 (虚拟 L3 网络)
    ├── vWire (虚拟隧道)
    └── Endpoints (端点)
        ↓
跨域网络
    ├── Pod (Kubernetes)
    ├── VM (虚拟机)
    └── Physical Machine (物理机)
```

### 4.2 组合步骤

**组合步骤**：

1. **注册 Service Mesh**：把 Istio/Linkerd 的 **vL3** 与 **Endpoint** 抽象为
   **NSM Network Service**
2. **NSM 允许多 Service Mesh 叠加**：在同一 vL3 上注册多个 **Network Service**（
   例如 Istio、Linkerd、Kuma）
3. **通过 vWire 细粒度流量治理**：vWire 负责 **TLS、熔断、限流**；可携带
   `labels` 进行流量路由

### 4.3 组合示例

**组合示例**：

```yaml
# NSM Network Service
apiVersion: networkservicemesh.io/v1
kind: NetworkService
metadata:
  name: istio-service
spec:
  vL3: istio-vl3
  endpoints:
    - name: order-service
      address: 10.0.0.1
      port: 8080
  vWire:
    - name: order-service-vwire
      source: pod-order-service
      destination: vm-order-service
      policy:
        tls: true
        rateLimit: 1000
        circuitBreaker: true
```

## 5. NSM 模式实现

### 5.1 NSM 安装

**NSM 安装**：

```bash
# 安装 NSM
kubectl apply -f https://raw.githubusercontent.com/networkservicemesh/deployments-k8s/main/examples/use-cases/nsm-1.yaml

# 安装 NSM Control Plane
kubectl apply -f https://raw.githubusercontent.com/networkservicemesh/deployments-k8s/main/examples/use-cases/nsm-control-plane.yaml
```

### 5.2 NSM 客户端配置

**NSM 客户端配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: order-service
  annotations:
    networkservicemesh.io/request: |
      {
        "mechanism": "vWire",
        "networkService": "order-service",
        "labels": {
          "app": "order-service",
          "version": "v1"
        }
      }
spec:
  containers:
    - name: order-service
      image: order-service:latest
```

### 5.3 NSM 跨域连接

**跨域连接配置**：

```yaml
# Pod 到 VM
apiVersion: networkservicemesh.io/v1
kind: NetworkServiceEndpoint
metadata:
  name: pod-to-vm
spec:
  networkService: order-service
  vWire:
    source:
      type: Pod
      name: order-service-pod
    destination:
      type: VM
      name: order-service-vm
    policy:
      tls: true
      rateLimit: 1000
      circuitBreaker: true

# VM 到物理机
apiVersion: networkservicemesh.io/v1
kind: NetworkServiceEndpoint
metadata:
  name: vm-to-physical
spec:
  networkService: order-service
  vWire:
    source:
      type: VM
      name: order-service-vm
    destination:
      type: PhysicalMachine
      name: order-service-physical
    policy:
      tls: true
      rateLimit: 1000
      circuitBreaker: true
```

## 6. NSM 模式优势

### 6.1 跨域聚合

**NSM 模式优势**：

- **统一网络**：统一的网络抽象
- **跨域支持**：支持 Pod、VM、物理机
- **透明连接**：透明的跨域连接

### 6.2 细粒度治理

**NSM 模式优势**：

- **vWire 治理**：通过 vWire 实现细粒度流量治理
- **策略支持**：支持 TLS、限流、熔断等策略
- **标签路由**：通过 labels 进行流量路由

### 6.3 多 Service Mesh 叠加

**NSM 模式优势**：

- **多 Mesh 支持**：支持多个 Service Mesh 叠加
- **统一管理**：通过 NSM 统一管理
- **灵活组合**：可以灵活组合不同的 Service Mesh

## 7. NSM 模式与其他模式

### 7.1 NSM vs Service Mesh

**NSM vs Service Mesh**：

| 模式             | 特点           | 使用场景       |
| ---------------- | -------------- | -------------- |
| **NSM**          | 跨域网络聚合   | 跨域网络连接   |
| **Service Mesh** | 微服务流量治理 | 微服务内部通信 |

### 7.2 NSM vs VPN

**NSM vs VPN**：

| 模式    | 特点           | 使用场景     |
| ------- | -------------- | ------------ |
| **NSM** | 细粒度流量治理 | 跨域网络连接 |
| **VPN** | 网络层加密     | 网络层加密   |

## 8. 形式化定义

### 8.1 NSM 模式定义

```text
NSM N = ⟨vL3, vWire, endpoints, clients⟩
其中：
- vL3: 虚拟 L3 网络
- vWire: 虚拟隧道集合
- endpoints: 端点集合
- clients: 客户端集合
```

### 8.2 vWire 定义

```text
vWire W = ⟨source, destination, policy, labels⟩
其中：
- source: 源端点
- destination: 目标端点
- policy: 策略配置
- labels: 标签集合
```

### 8.3 Endpoint 定义

```text
Endpoint E = ⟨name, address, port, service⟩
其中：
- name: 端点名称
- address: 端点地址
- port: 端点端口
- service: 所属服务
```

## 9. 相关文档

### 9.1 组合模式文档

- **[组合模式文档集](README.md)** - 组合模式文档集说明
- **[NSM 模式](./05-nsm-pattern.md)** - NSM 模式（本文件）
- **[Service Aggregation 模式](./05-nsm-pattern.md#service-aggregation)** -
  Service Aggregation 模式（在本文件中）
- **[Service Mesh 与 NSM](../03-service-mesh-nsm/)** - Service Mesh 和 NSM 的组
  合模式
- **[Network Service Mesh 视角](../10-quick-views/network-service-mesh-view.md)** -
  Network Service Mesh 视角文档

### 9.2 参考资源

- **[REFERENCES.md](../../REFERENCES.md)** - 参考标准、框架、工具和资源
- **[ACADEMIC-REFERENCES.md](../../ACADEMIC-REFERENCES.md)** - Wikipedia、大学课
  程、学术论文等学术资源

## 10. 总结

通过**NSM 模式**，我们实现了：

1. **跨域聚合**：聚合 Pod、VM、物理机，实现统一网络连接
2. **统一网络**：统一的网络抽象，简化网络管理
3. **细粒度治理**：通过 vWire 实现细粒度流量治理
4. **多 Mesh 叠加**：支持多个 Service Mesh 叠加，灵活组合
5. **透明连接**：透明的跨域连接，简化网络配置

**相关模式**：NSM 模式与 Service Aggregation 模式可以结合使用，NSM 负责跨域网络
聚合，Service Aggregation 负责服务聚合。详细内容请参考
[Service Aggregation 模式](./05-nsm-pattern.md#service-aggregation)。

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
391-610 行，NSM 模式部分
