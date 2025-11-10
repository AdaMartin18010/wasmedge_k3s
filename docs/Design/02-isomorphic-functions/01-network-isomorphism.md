# 1. 网络功能同构矩阵

> **文档版本**：v1.1 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [📑 目录](#-目录)
- [概述](#概述)
- [网络功能同构矩阵](#网络功能同构矩阵)
- [架构特点](#架构特点)
  - [关键设计要点](#关键设计要点)
- [关键技术分析](#关键技术分析)
  - [1. 基础网络](#1-基础网络)
  - [2. 多平面网络](#2-多平面网络)
  - [3. 服务发现](#3-服务发现)
  - [4. 负载均衡](#4-负载均衡)
  - [5. 网络策略](#5-网络策略)
  - [6. 固定 IP](#6-固定-ip)
  - [7. 性能加速](#7-性能加速)
- [相关文档](#相关文档)

---

## 概述

本文档分析虚拟化容器化集群管理 API 中网络功能的同构性设计，对比容器和虚拟机在网
络功能实现上的统一性和差异性。

## 网络功能同构矩阵

| **能力**       | **容器实现**         | **虚拟机实现**     | **API 统一性**                   | **关键技术**   |
| -------------- | -------------------- | ------------------ | -------------------------------- | -------------- |
| **基础网络**   | Pod 网络命名空间     | VMI 网络接口       | CRD 字段复用                     | CNI 插件       |
| **多平面网络** | Multus 多网卡        | 虚拟网卡(vNIC)     | 共享 NetworkAttachmentDefinition | Multus CNI     |
| **服务发现**   | Service/Endpoints    | Headless Service   | 完全一致                         | kube-proxy     |
| **负载均衡**   | Service/Ingress      | 复用 Service       | 完全同构                         | 统一负载均衡器 |
| **网络策略**   | NetworkPolicy        | 复用 NetworkPolicy | 规则一致                         | OVN-Kubernetes |
| **固定 IP**    | StatefulSet          | 固定 IP 配置       | 扩展字段                         | Kubevirt 特性  |
| **性能加速**   | SR-IOV Device Plugin | PCI 直通           | 统一资源分配                     | SR-IOV CNI     |

---

## 架构特点

虚拟机通过`Multus`与容器共享 CNI 生态，网络配置通过`NetworkAttachmentDefinition`
CRD 统一描述，实现 Layer2/Layer3 网络策略的同构管理。

### 关键设计要点

1. **CNI 生态复用**：虚拟机通过 Multus 复用 Kubernetes CNI 生态
2. **统一网络配置**：通过 NetworkAttachmentDefinition CRD 统一描述网络配置
3. **网络策略同构**：NetworkPolicy 对 VMI 和 Pod 同等生效
4. **性能优化支持**：通过 SR-IOV 实现网络性能加速

---

## 关键技术分析

### 1. 基础网络

**容器实现**：Pod 网络命名空间

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test
      image: nginx:alpine
```

**虚拟机实现**：VMI 网络接口

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    devices:
      interfaces:
        - name: default
          masquerade: {}
    networks:
      - name: default
        pod: {}
```

**API 统一性**：CRD 字段复用

- 容器和虚拟机都通过 CNI 插件管理网络
- VMI 网络接口通过 virt-launcher Pod 的网络命名空间实现
- 网络配置通过 CRD 字段统一描述

### 2. 多平面网络

**容器实现**：Multus 多网卡

```yaml
apiVersion: k8s.cni.cncf.io/v1
kind: NetworkAttachmentDefinition
metadata:
  name: macvlan-conf
spec:
  config: |
    {
      "cniVersion": "0.3.1",
      "type": "macvlan",
      "master": "eth0",
      "mode": "bridge",
      "ipam": {
        "type": "host-local",
        "subnet": "10.56.0.0/16"
      }
    }
```

**虚拟机实现**：虚拟网卡(vNIC)

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    devices:
      interfaces:
        - name: default
          masquerade: {}
        - name: macvlan-net
          bridge: {}
    networks:
      - name: default
        pod: {}
      - name: macvlan-net
        multus:
          networkName: macvlan-conf
```

**API 统一性**：共享 NetworkAttachmentDefinition

- 容器和虚拟机共享 NetworkAttachmentDefinition CRD
- Multus CNI 插件统一管理多平面网络
- 网络配置通过 CRD 统一描述

### 3. 服务发现

**容器实现**：Service/Endpoints

```yaml
apiVersion: v1
kind: Service
metadata:
  name: test-service
spec:
  selector:
    app: test
  ports:
    - port: 80
      targetPort: 8080
```

**虚拟机实现**：Headless Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: test-vmi-service
spec:
  clusterIP: None
  selector:
    kubevirt.io/domain: test-vmi
  ports:
    - port: 80
      targetPort: 8080
```

**API 统一性**：完全一致

- 容器和虚拟机都使用 Kubernetes Service 进行服务发现
- Service 和 Endpoints 机制对 VMI 和 Pod 同等生效
- kube-proxy 统一处理服务发现和负载均衡

### 4. 负载均衡

**容器实现**：Service/Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: test-ingress
spec:
  rules:
    - host: test.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: test-service
                port:
                  number: 80
```

**虚拟机实现**：复用 Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: test-vmi-service
spec:
  selector:
    kubevirt.io/domain: test-vmi
  ports:
    - port: 80
      targetPort: 8080
  type: LoadBalancer
```

**API 统一性**：完全同构

- 容器和虚拟机都使用 Kubernetes Service 进行负载均衡
- Ingress 控制器对 VMI 和 Pod 同等生效
- 统一负载均衡器处理流量分发

### 5. 网络策略

**容器实现**：NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
spec:
  podSelector:
    matchLabels:
      app: test
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: tenant-a
  egress:
    - to: []
```

**虚拟机实现**：复用 NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-vmi-network-policy
spec:
  podSelector:
    matchLabels:
      kubevirt.io/domain: test-vmi
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: tenant-a
  egress:
    - to: []
```

**API 统一性**：规则一致

- NetworkPolicy 对 VMI 和 Pod 同等生效
- OVN-Kubernetes 等网络插件统一处理网络策略
- 网络策略规则通过 CRD 统一描述

### 6. 固定 IP

**容器实现**：StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: test-statefulset
spec:
  serviceName: test-service
  replicas: 3
  template:
    metadata:
      labels:
        app: test
    spec:
      containers:
        - name: test
          image: nginx:alpine
```

**虚拟机实现**：固定 IP 配置

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    devices:
      interfaces:
        - name: default
          masquerade: {}
    networks:
      - name: default
        pod: {}
        # 固定 IP 配置（KubeVirt 特性）
        # 通过 NetworkAttachmentDefinition 配置
```

**API 统一性**：扩展字段

- StatefulSet 为容器提供固定 IP 支持
- KubeVirt 通过扩展字段支持虚拟机固定 IP 配置
- 固定 IP 配置通过 NetworkAttachmentDefinition CRD 统一描述

### 7. 性能加速

**容器实现**：SR-IOV Device Plugin

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test
      image: nginx:alpine
      resources:
        requests:
          intel.com/sriov: "1"
        limits:
          intel.com/sriov: "1"
```

**虚拟机实现**：PCI 直通

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    devices:
      interfaces:
        - name: sriov-net
          sriov: {}
          resources:
            requests:
              intel.com/sriov: "1"
    networks:
      - name: sriov-net
        multus:
          networkName: sriov-network
```

**API 统一性**：统一资源分配

- 容器和虚拟机都通过 Device Plugin 机制分配 SR-IOV 资源
- SR-IOV CNI 插件统一管理 SR-IOV 网络
- 资源分配通过 Kubernetes 资源管理机制统一处理

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [存储功能同构矩阵](../02-isomorphic-functions/02-storage-isomorphism.md) - 存
  储功能同构分析
- [多租户与配额同构](../02-isomorphic-functions/03-multi-tenant-quota.md) - 多租
  户配额同构分析
- [运行时管理同构](../02-isomorphic-functions/04-runtime-management.md) - 运行时
  管理同构分析

---

**最后更新**：2025-11-10 **维护者**：项目团队
