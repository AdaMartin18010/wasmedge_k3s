# 3. 多租户与配额同构

> **文档版本**：v1.0 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [📑 目录](#-目录)
- [概述](#概述)
- [统一配额定义示例](#统一配额定义示例)
- [同构机制](#同构机制)
  - [1. 命名空间隔离](#1-命名空间隔离)
  - [2. RBAC 权限](#2-rbac-权限)
  - [3. 资源配额](#3-资源配额)
  - [4. 网络隔离](#4-网络隔离)
  - [5. 配额审计](#5-配额审计)
- [关键技术分析](#关键技术分析)
  - [1. 命名空间隔离机制](#1-命名空间隔离机制)
  - [2. RBAC 权限控制机制](#2-rbac-权限控制机制)
  - [3. 资源配额管理机制](#3-资源配额管理机制)
  - [4. 网络隔离机制](#4-网络隔离机制)
  - [5. 配额审计机制](#5-配额审计机制)
- [相关文档](#相关文档)

---

## 概述

本文档分析虚拟化容器化集群管理 API 中多租户与配额的同构性设计，对比容器和虚拟机
在多租户与配额管理上的统一性和差异性。

## 统一配额定义示例

```yaml
# 统一配额定义示例
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: tenant-a
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    # 同时限制容器和虚拟机
    count/virtualmachines.kubevirt.io: "5"
    count/pods: "20"
```

---

## 同构机制

### 1. 命名空间隔离

**机制**：VM 和 Pod 共享同一 Namespace 语义

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: tenant-a
  labels:
    tenant: tenant-a
```

**说明**：

- 容器和虚拟机都使用 Kubernetes Namespace 进行资源隔离
- 同一 Namespace 内的容器和虚拟机共享资源配额
- Namespace 提供逻辑隔离，不提供物理隔离

### 2. RBAC 权限

**机制**：`virt-api` 继承 K8s RBAC，角色绑定统一

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: tenant-a-operator
  namespace: tenant-a
rules:
  - apiGroups: ["kubevirt.io"]
    resources: ["virtualmachines"]
    verbs: ["get", "list", "create", "update"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "create", "update"]
```

**说明**：

- 容器和虚拟机都使用 Kubernetes RBAC 进行权限控制
- virt-api 继承 Kubernetes RBAC 机制
- 角色绑定统一管理容器和虚拟机的访问权限

### 3. 资源配额

**机制**：通过 CRD 计数器扩展 ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-a-quota
  namespace: tenant-a
spec:
  hard:
    # 计算资源配额
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    # 容器资源配额
    count/pods: "20"
    # 虚拟机资源配额（通过 CRD 计数器扩展）
    count/virtualmachines.kubevirt.io: "5"
    count/virtualmachineinstances.kubevirt.io: "10"
```

**说明**：

- 容器和虚拟机共享 ResourceQuota 配额管理
- 通过 CRD 计数器扩展 ResourceQuota，支持虚拟机资源配额
- 资源配额统一管理容器和虚拟机的资源使用

### 4. 网络隔离

**机制**：NetworkPolicy 对 VMI 和 Pod 同等生效

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tenant-a-isolation
  namespace: tenant-a
spec:
  podSelector: {} # 匹配所有 Pod 和 VMI
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

**说明**：

- NetworkPolicy 对容器和虚拟机同等生效
- 网络隔离通过 NetworkPolicy 统一管理
- 网络策略规则通过 CRD 统一描述

### 5. 配额审计

**机制**：CNStack 的 IAM Gateway 统一审计容器和虚拟机 API 调用

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: iam-gateway-config
data:
  config.yaml: |
    audit:
      enabled: true
      logPath: /var/log/audit.log
      resources:
        - apiGroups: [""]
          resources: ["pods"]
        - apiGroups: ["kubevirt.io"]
          resources: ["virtualmachines"]
```

**说明**：

- IAM Gateway 统一审计容器和虚拟机的 API 调用
- 审计日志统一记录容器和虚拟机的操作
- 配额审计通过 IAM Gateway 统一管理

---

## 关键技术分析

### 1. 命名空间隔离机制

**容器实现**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
  namespace: tenant-a
spec:
  containers:
    - name: test
      image: nginx:alpine
```

**虚拟机实现**：

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: test-vm
  namespace: tenant-a
spec:
  running: true
  template:
    spec:
      domain:
        resources:
          requests:
            memory: "1Gi"
            cpu: "1"
```

**同构性**：

- 容器和虚拟机都使用 Kubernetes Namespace 进行资源隔离
- 同一 Namespace 内的容器和虚拟机共享资源配额
- Namespace 提供逻辑隔离，不提供物理隔离

### 2. RBAC 权限控制机制

**容器实现**：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-operator
  namespace: tenant-a
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "create", "update", "delete"]
```

**虚拟机实现**：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: vm-operator
  namespace: tenant-a
rules:
  - apiGroups: ["kubevirt.io"]
    resources: ["virtualmachines"]
    verbs: ["get", "list", "create", "update", "delete"]
```

**同构性**：

- 容器和虚拟机都使用 Kubernetes RBAC 进行权限控制
- virt-api 继承 Kubernetes RBAC 机制
- 角色绑定统一管理容器和虚拟机的访问权限

### 3. 资源配额管理机制

**容器实现**：

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: pod-quota
  namespace: tenant-a
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    count/pods: "20"
```

**虚拟机实现**：

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: vm-quota
  namespace: tenant-a
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    # 通过 CRD 计数器扩展
    count/virtualmachines.kubevirt.io: "5"
    count/virtualmachineinstances.kubevirt.io: "10"
```

**同构性**：

- 容器和虚拟机共享 ResourceQuota 配额管理
- 通过 CRD 计数器扩展 ResourceQuota，支持虚拟机资源配额
- 资源配额统一管理容器和虚拟机的资源使用

### 4. 网络隔离机制

**容器实现**：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: pod-isolation
  namespace: tenant-a
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

**虚拟机实现**：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: vm-isolation
  namespace: tenant-a
spec:
  podSelector:
    matchLabels:
      kubevirt.io/domain: test-vm
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

**同构性**：

- NetworkPolicy 对容器和虚拟机同等生效
- 网络隔离通过 NetworkPolicy 统一管理
- 网络策略规则通过 CRD 统一描述

### 5. 配额审计机制

**容器实现**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: audit-config
data:
  config.yaml: |
    audit:
      enabled: true
      resources:
        - apiGroups: [""]
          resources: ["pods"]
```

**虚拟机实现**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: audit-config
data:
  config.yaml: |
    audit:
      enabled: true
      resources:
        - apiGroups: ["kubevirt.io"]
          resources: ["virtualmachines"]
```

**同构性**：

- IAM Gateway 统一审计容器和虚拟机的 API 调用
- 审计日志统一记录容器和虚拟机的操作
- 配额审计通过 IAM Gateway 统一管理

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [网络功能同构矩阵](../02-isomorphic-functions/01-network-isomorphism.md) - 网
  络功能同构分析
- [存储功能同构矩阵](../02-isomorphic-functions/02-storage-isomorphism.md) - 存
  储功能同构分析
- [运行时管理同构](../02-isomorphic-functions/04-runtime-management.md) - 运行时
  管理同构分析

---

**最后更新**：2025-11-10 **维护者**：项目团队
