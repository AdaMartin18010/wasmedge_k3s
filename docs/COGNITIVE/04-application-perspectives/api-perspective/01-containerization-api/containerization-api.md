# 容器化 API 规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 核心 API 规范](#11-核心-api-规范)
  - [1.2 API 规范层次](#12-api-规范层次)
  - [1.3 容器化在 API 规范中的位置](#13-容器化在-api-规范中的位置)
- [2 OCI Runtime Spec API](#2-oci-runtime-spec-api)
  - [2.1 核心接口定义](#21-核心接口定义)
  - [2.2 API 调用流程](#22-api-调用流程)
  - [2.3 资源管理 API](#23-资源管理-api)
- [3 Kubernetes CRD API](#3-kubernetes-crd-api)
  - [3.1 CRD 定义示例](#31-crd-定义示例)
  - [3.2 CRD API 设计原则](#32-crd-api-设计原则)
  - [3.3 Operator 模式 API](#33-operator-模式-api)
- [4 服务发现 API](#4-服务发现-api)
  - [4.1 CoreDNS API](#41-coredns-api)
  - [4.2 etcd API](#42-etcd-api)
- [5 容器网络 API](#5-容器网络-api)
  - [5.1 CNI 接口规范](#51-cni-接口规范)
  - [5.2 CNI 插件 API](#52-cni-插件-api)
- [6 容器存储 API](#6-容器存储-api)
  - [6.1 CSI 接口规范](#61-csi-接口规范)
  - [6.2 PV/PVC API](#62-pvpvc-api)
- [7 API 演进路径](#7-api-演进路径)
  - [7.1 从 Docker API 到 OCI Runtime Spec](#71-从-docker-api-到-oci-runtime-spec)
  - [7.2 Kubernetes API 演进](#72-kubernetes-api-演进)
- [8 形式化定义与理论基础](#8-形式化定义与理论基础)
  - [8.1 容器 API 规范形式化](#81-容器-api-规范形式化)
  - [8.2 API 版本化模型](#82-api-版本化模型)
  - [8.3 容器生命周期形式化](#83-容器生命周期形式化)
  - [8.4 资源隔离形式化](#84-资源隔离形式化)
- [9 相关文档](#9-相关文档)

---

## 1 概述

容器化 API 规范是云原生技术栈的核心，从 OCI Runtime Spec 到 Kubernetes CRD，定义
了容器生命周期、资源管理、网络和存储的标准化接口。本文档基于形式化方法，提供严格
的数学定义和推理论证，确保容器化 API 的正确性和可验证性。

### 1.1 核心 API 规范

| API 规范             | 标准组织 | 版本   | 核心内容       |
| -------------------- | -------- | ------ | -------------- |
| **OCI Runtime Spec** | OCI      | v1.1.0 | 容器运行时接口 |
| **Kubernetes CRD**   | CNCF     | v1.30+ | 自定义资源定义 |
| **CNI**              | CNCF     | v1.0.0 | 容器网络接口   |
| **CSI**              | CNCF     | v1.9.0 | 容器存储接口   |
| **CRI**              | CNCF     | v1.0.0 | 容器运行时接口 |

### 1.2 API 规范层次

```text
应用层 API
  ↓
Kubernetes API (CRD, Custom Resources)
  ↓
CRI API (Container Runtime Interface)
  ↓
OCI Runtime Spec API
  ↓
CNI/CSI API (网络/存储)
  ↓
Linux 系统调用 API
```

**参考标准**：

- [OCI Runtime Specification](https://github.com/opencontainers/runtime-spec) -
  容器运行时标准
- [Kubernetes API Conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md) -
  Kubernetes API 约定
- [CNI Specification](https://github.com/containernetworking/cni/blob/main/SPEC.md) -
  容器网络接口规范
- [CSI Specification](https://github.com/container-storage-interface/spec) - 容
  器存储接口规范
- [CRI Specification](https://github.com/kubernetes/cri-api) - 容器运行时接口规
  范

### 1.3 容器化在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../07-formalization/formalization.md#21-api-规范四元组)），
容器化 API 属于 **IDL** 和 **Governance** 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
            ↑         ↑
    Containerization ∈ IDL ∩ Governance
```

容器化 API 在 API 规范中提供：

- **IDL 层**：通过 Kubernetes CRD 定义 API 规范（OpenAPI、Protobuf）
- **Governance 层**：通过 Kubernetes API Server 和 Admission Webhook 实现运行时
  治理
- **Observability 层**：通过 Kubernetes Metrics API 和 Events API 实现可观测性
- **Security 层**：通过 Pod Security Standards 和 Network Policies 实现安全控制

---

## 2 OCI Runtime Spec API

### 2.1 核心接口定义

**OCI Runtime Spec** 定义了容器运行时的标准接口：

```json
{
  "ociVersion": "1.1.0",
  "process": {
    "args": ["/bin/sh"],
    "env": ["PATH=/usr/local/sbin:/usr/local/bin"]
  },
  "root": {
    "path": "rootfs",
    "readonly": true
  },
  "mounts": [
    {
      "destination": "/proc",
      "type": "proc",
      "source": "proc"
    }
  ],
  "linux": {
    "resources": {
      "memory": {
        "limit": 536870912
      },
      "cpu": {
        "shares": 1024
      }
    },
    "namespaces": [
      {
        "type": "pid"
      },
      {
        "type": "network"
      }
    ]
  }
}
```

### 2.2 API 调用流程

```text
1. create() - 创建容器运行时环境
   ↓
2. start() - 启动容器进程
   ↓
3. state() - 查询容器状态
   ↓
4. kill() - 终止容器进程
   ↓
5. delete() - 删除容器资源
```

### 2.3 资源管理 API

**CPU 资源限制**：

```json
{
  "linux": {
    "resources": {
      "cpu": {
        "shares": 1024,
        "quota": 50000,
        "period": 100000,
        "cpus": "0-3",
        "mems": "0-1"
      }
    }
  }
}
```

**内存资源限制**：

```json
{
  "linux": {
    "resources": {
      "memory": {
        "limit": 536870912,
        "reservation": 268435456,
        "swap": 536870912,
        "kernel": 67108864
      }
    }
  }
}
```

---

## 3 Kubernetes CRD API

### 3.1 CRD 定义示例

**APIDefinition CRD**：

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: apidefinitions.api.example.com
spec:
  group: api.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                openapi:
                  type: string
                version:
                  type: string
                lifecycle:
                  type: string
                  enum: [active, deprecated, sunset]
  scope: Namespaced
  names:
    plural: apidefinitions
    singular: apidefinition
    kind: APIDefinition
```

### 3.2 CRD API 设计原则

1. **版本化**：使用 `apiVersion` 字段进行版本管理
2. **验证**：使用 OpenAPI v3 Schema 进行验证
3. **默认值**：使用 `default` 字段设置默认值
4. **必需字段**：使用 `required` 字段标记必需字段

### 3.3 Operator 模式 API

**Operator Controller API**：

```go
type APIDefinitionReconciler struct {
    client.Client
    Scheme *runtime.Scheme
}

func (r *APIDefinitionReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    apiDef := &apiv1.APIDefinition{}
    if err := r.Get(ctx, req.NamespacedName, apiDef); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // API 规范同步逻辑
    if err := r.syncAPISpec(ctx, apiDef); err != nil {
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil
}
```

---

## 4 服务发现 API

### 4.1 CoreDNS API

**CoreDNS 配置 API**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
```

### 4.2 etcd API

**etcd 服务注册 API**：

```go
// 服务注册
client.Put(ctx, "/services/payment-service/10.0.0.1:8080", "{\"version\":\"v1\"}")

// 服务发现
resp, err := client.Get(ctx, "/services/payment-service", client.WithPrefix())
```

---

## 5 容器网络 API

### 5.1 CNI 接口规范

**CNI 配置 API**：

```json
{
  "cniVersion": "1.0.0",
  "name": "bridge",
  "type": "bridge",
  "bridge": "cnio0",
  "isGateway": true,
  "ipMasq": true,
  "ipam": {
    "type": "host-local",
    "ranges": [
      [
        {
          "subnet": "10.22.0.0/16",
          "gateway": "10.22.0.1"
        }
      ]
    ],
    "routes": [
      {
        "dst": "0.0.0.0/0"
      }
    ]
  }
}
```

### 5.2 CNI 插件 API

**CNI 插件调用接口**：

```bash
# ADD 操作
echo '{"cniVersion":"1.0.0","name":"bridge","type":"bridge"}' | \
  CNI_COMMAND=ADD CNI_CONTAINERID=container123 CNI_NETNS=/proc/12345/ns/net \
  /opt/cni/bin/bridge

# DEL 操作
echo '{"cniVersion":"1.0.0","name":"bridge","type":"bridge"}' | \
  CNI_COMMAND=DEL CNI_CONTAINERID=container123 CNI_NETNS=/proc/12345/ns/net \
  /opt/cni/bin/bridge
```

---

## 6 容器存储 API

### 6.1 CSI 接口规范

**CSI Volume API**：

```go
// CreateVolume 请求
type CreateVolumeRequest struct {
    Name               string
    CapacityRange      *CapacityRange
    VolumeCapabilities []*VolumeCapability
    Parameters         map[string]string
}

// MountVolume 请求
type NodeStageVolumeRequest struct {
    VolumeId          string
    StagingTargetPath string
    VolumeCapability  *VolumeCapability
}
```

### 6.2 PV/PVC API

**PersistentVolume API**：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-example
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: fast-ssd
  csi:
    driver: com.example.csi.driver
    volumeHandle: volume-123
    volumeAttributes:
      type: ssd
```

---

## 7 API 演进路径

### 7.1 从 Docker API 到 OCI Runtime Spec

```text
Docker API (2013)
  ↓
containerd API (2016)
  ↓
CRI API (2017)
  ↓
OCI Runtime Spec (2017)
  ↓
OCI Runtime Spec v1.1.0 (2024)
```

### 7.2 Kubernetes API 演进

| 版本  | 主要 API 变更                  | 时间 |
| ----- | ------------------------------ | ---- |
| v1.0  | 基础 API                       | 2015 |
| v1.8  | CRD GA                         | 2017 |
| v1.16 | CustomResourceDefinition v1    | 2019 |
| v1.22 | ValidatingAdmissionPolicy      | 2021 |
| v1.28 | ValidatingAdmissionPolicy Beta | 2023 |
| v1.30 | RuntimeClass 增强              | 2024 |

---

## 8 形式化定义与理论基础

### 8.1 容器 API 规范形式化

**定义 8.1（容器 API 规范）**：容器 API 规范是一个五元组：

```text
Container_API = ⟨Runtime, Network, Storage, Discovery, Governance⟩
```

其中：

- **Runtime**：OCI Runtime Spec API `R: ContainerSpec → ContainerState`
- **Network**：CNI API `N: NetworkSpec → NetworkConfig`
- **Storage**：CSI API `S: VolumeSpec → VolumeState`
- **Discovery**：服务发现 API `D: ServiceSpec → ServiceEndpoint`
- **Governance**：Kubernetes CRD API `G: ResourceSpec → ResourceState`

**定义 8.2（容器生命周期）**：容器生命周期是一个状态机：

```text
Container_Lifecycle = ⟨States, Transitions⟩
```

其中：

- **States**：`{Created, Running, Stopped, Deleted}`
- **Transitions**：`{create, start, stop, delete}`

**状态转换规则**：

```text
Created --[start]--> Running
Running --[stop]--> Stopped
Stopped --[start]--> Running
Stopped --[delete]--> Deleted
```

### 8.2 API 版本化模型

**定义 8.3（API 版本）**：API 版本是一个三元组：

```text
API_Version = ⟨Major, Minor, Patch⟩
```

**版本兼容性规则**：

- **Major 版本**：不兼容变更 `M₂ = M₁ + 1 ⟹ ¬Compatible(v₁, v₂)`
- **Minor 版本**：向后兼容的新功能 `M₂ = M₁, m₂ = m₁ + 1 ⟹ Compatible(v₁, v₂)`
- **Patch 版本**：向后兼容的 bug 修复
  `M₂ = M₁, m₂ = m₁, p₂ = p₁ + 1 ⟹ Compatible(v₁, v₂)`

**定义 8.4（版本兼容性）**：版本 `v₁ = ⟨M₁, m₁, p₁⟩` 与 `v₂ = ⟨M₂, m₂, p₂⟩` 兼容
，当且仅当：

```text
Compatible(v₁, v₂) = (M₁ = M₂) ∧ ((m₁ = m₂) ∨ (m₁ < m₂))
```

### 8.3 容器生命周期形式化

**定理 8.1（容器生命周期确定性）**：容器生命周期是确定性的，即：

```text
∀ state₁, state₂: (state₁ = state₂) ⟹ (Next(state₁) = Next(state₂))
```

**证明**：根据定义 8.2，状态转换规则是确定的，因此容器生命周期是确定性的。□

**定理 8.2（容器生命周期可达性）**：从任意状态都可以到达 `Deleted` 状态：

```text
∀ state ∈ States: ∃ path: state --[path]--> Deleted
```

**证明**：根据状态转换规则，从任意状态都可以通过 `stop` 和 `delete` 操作到达
`Deleted` 状态。□

### 8.4 资源隔离形式化

**定义 8.5（资源隔离）**：资源隔离是一个函数：

```text
Isolation: Container × Resource → Bool
```

其中 `Isolation(c, r) = true` 表示容器 `c` 对资源 `r` 有隔离访问。

**定义 8.6（命名空间隔离）**：命名空间隔离是一个函数：

```text
NamespaceIsolation: Container × NamespaceType → NamespaceID
```

其中 `NamespaceType ∈ {PID, Network, Mount, IPC, UTS, User}`。

**定理 8.3（命名空间隔离性）**：如果两个容器在不同的命名空间中，则它们相互隔离：

```text
NamespaceIsolation(c₁, t) ≠ NamespaceIsolation(c₂, t) ⟹ Isolation(c₁, c₂)
```

**证明**：根据 Linux 命名空间的定义，不同命名空间中的进程相互隔离。□

**定义 8.7（资源限制）**：资源限制是一个函数：

```text
ResourceLimit: Container × ResourceType → Limit
```

其中 `ResourceType ∈ {CPU, Memory, Disk, Network}`。

**定理 8.4（资源限制有效性）**：资源限制确保容器不会超过分配的资源：

```text
∀ c, r: Usage(c, r) ≤ ResourceLimit(c, r)
```

**证明**：根据 OCI Runtime Spec，资源限制通过 cgroups 实现，cgroups 确保容器不会
超过分配的资源。□

---

## 9 相关文档

- **[容器化抽象](../../ARCHITECTURE/architecture-view/02-virtualization-containerization-sandboxing/02-containerization-abstraction.md)** -
  容器化 API 设计原理
- **[Operator/CRD 开发规范](../../TECHNICAL/18-operator-crd/)** - K8s CRD API 设
  计最佳实践
- **[Kubernetes 架构与实践](../../TECHNICAL/01-kubernetes/)** - Kubernetes API
  详解
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新**：2025-11-07 **维护者**：项目团队
