# NSM 边缘网关配置

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 核心特性](#11-核心特性)
- [2 NSM 安装](#2-nsm-安装)
  - [2.1 云端节点安装](#21-云端节点安装)
  - [2.2 边缘节点安装](#22-边缘节点安装)
- [3 边缘网关配置](#3-边缘网关配置)
  - [3.1 Edge Gateway 部署](#31-edge-gateway-部署)
  - [3.2 网络服务端点配置](#32-网络服务端点配置)
- [4 跨域网络聚合](#4-跨域网络聚合)
  - [4.1 vWire 配置](#41-vwire-配置)
  - [4.2 vL3 配置](#42-vl3-配置)
- [5 相关文档](#5-相关文档)

---

## 1 概述

**NSM（Network Service Mesh）** 是云原生网络服务网格，提供跨域网络聚合和边缘-云
连接能力。

### 1.1 核心特性

- **跨域网络**：支持跨域网络聚合
- **边缘网关**：NSM Edge Gateway 实现边缘-云连接
- **vWire**：虚拟 Wire 实现网络连接
- **vL3**：虚拟 L3 网络实现

---

## 2 NSM 安装

### 2.1 云端节点安装

```bash
# 安装 NSM
kubectl apply -f https://raw.githubusercontent.com/networkservicemesh/deployments-k8s/main/releases/v1.7.0/quick-start.yaml

# 验证安装
kubectl get pods -n nsm-system
```

### 2.2 边缘节点安装

```bash
# 在边缘节点安装 NSM
kubectl apply -f https://raw.githubusercontent.com/networkservicemesh/deployments-k8s/main/releases/v1.7.0/quick-start-edge.yaml
```

---

## 3 边缘网关配置

### 3.1 Edge Gateway 部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nsm-edge-gateway
  namespace: nsm-system
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: nsm-edge-gateway
          image: networkservicemesh/nsm-edge-gateway:v1.7.0
          env:
            - name: NSM_EDGE_GATEWAY_CLOUD_URL
              value: "https://cloud-nsm.example.com:443"
```

### 3.2 网络服务端点配置

```yaml
apiVersion: networkservicemesh.io/v1
kind: NetworkServiceEndpoint
metadata:
  name: edge-endpoint
spec:
  networkService: edge-network-service
  networkServiceLabels:
    app: edge-app
```

---

## 4 跨域网络聚合

### 4.1 vWire 配置

```yaml
apiVersion: networkservicemesh.io/v1
kind: NetworkService
metadata:
  name: cross-domain-network
spec:
  payload: IP
  matches:
    - sourceSelector:
        app: edge-app
      destinationSelector:
        app: cloud-app
```

### 4.2 vL3 配置

```yaml
apiVersion: networkservicemesh.io/v1
kind: NetworkService
metadata:
  name: vl3-network
spec:
  payload: IP
  mechanism:
    - type: VXLAN
      parameters:
        srcIP: "10.60.0.0/16"
```

---

## 5 相关文档

- [`README.md`](README.md) - 边缘计算实现细节总览
- [`edge-cloud-sync.md`](edge-cloud-sync.md) - 边缘-云同步配置
- [`../../02-views/10-quick-views/network-service-mesh-view.md`](../../02-views/10-quick-views/network-service-mesh-view.md) -
  NSM 架构视角

---

**更新时间**：2025-11-05 **版本**：v1.0
