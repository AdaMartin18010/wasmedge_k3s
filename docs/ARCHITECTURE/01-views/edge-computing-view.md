# 边缘计算架构视角

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 核心思想](#11-核心思想)
- [2. 边缘计算在架构中的定位](#2-边缘计算在架构中的定位)
  - [2.1 在统一中层模型中的位置](#21-在统一中层模型中的位置)
  - [2.2 与四层抽象的关系](#22-与四层抽象的关系)
- [3. 边缘计算场景](#3-边缘计算场景)
  - [3.1 低延迟需求](#31-低延迟需求)
  - [3.2 离线运行需求](#32-离线运行需求)
  - [3.3 统一治理需求](#33-统一治理需求)
- [4. 5G MEC 架构](#4-5g-mec-架构)
  - [4.1 MEC 架构概述](#41-mec-架构概述)
  - [4.2 MEC 与 K3s 集成](#42-mec-与-k3s-集成)
  - [4.3 边缘-云协同](#43-边缘-云协同)
- [5. 边缘 Kubernetes 平台](#5-边缘-kubernetes-平台)
  - [5.1 K3s](#51-k3s)
  - [5.2 KubeEdge](#52-kubeedge)
  - [5.3 EdgeMesh](#53-edgemesh)
- [6. 边缘网络服务](#6-边缘网络服务)
  - [6.1 NSM Edge Gateway](#61-nsm-edge-gateway)
  - [6.2 边缘 Service Mesh](#62-边缘-service-mesh)
  - [6.3 跨域网络聚合](#63-跨域网络聚合)
- [7. 边缘计算技术栈](#7-边缘计算技术栈)
  - [7.1 容器运行时](#71-容器运行时)
  - [7.2 Wasm 运行时](#72-wasm-运行时)
  - [7.3 边缘存储](#73-边缘存储)
- [8. 边缘 AI 推理](#8-边缘-ai-推理)
  - [8.1 边缘 AI 架构](#81-边缘-ai-架构)
  - [8.2 模型部署](#82-模型部署)
  - [8.3 推理优化](#83-推理优化)
- [9. 最佳实践](#9-最佳实践)
  - [9.1 资源管理](#91-资源管理)
  - [9.2 网络优化](#92-网络优化)
  - [9.3 安全策略](#93-安全策略)
- [10. 相关文档](#10-相关文档)
  - [相关文档](#相关文档)
  - [理论文档](#理论文档)
  - [实现细节](#实现细节)
  - [学术资源](#学术资源)

---

## 1. 概述

本文档从**边缘计算**视角阐述架构设计，说明边缘计算如何通过云原生架构实现低延迟、
离线运行和统一治理。

### 1.1 核心思想

> **边缘计算通过轻量级 Kubernetes（K3s）、WebAssembly 运行时（WasmEdge）和网络服
> 务网格（NSM）实现边缘节点的统一管理、低延迟访问和离线运行能力**

---

## 2. 边缘计算在架构中的定位

### 2.1 在统一中层模型中的位置

**统一中层模型 ℳ**：ℳ ≜ ⟨U, G, P, Δ⟩

**边缘计算映射**：

- **U（计算单元）**：
  - **边缘节点**：K3s + WasmEdge / Container
  - **云端节点**：Kubernetes + Container
- **G（组合图谱）**：
  - **边缘服务**：边缘应用、边缘 AI 推理
  - **云端服务**：云端应用、数据服务
  - **边缘-云连接**：NSM vWire、Service Mesh
- **P（策略层）**：
  - **部署策略**：边缘部署、云端部署、混合部署
  - **流量策略**：边缘优先、云端回退
  - **安全策略**：边缘认证、数据加密

### 2.2 与四层抽象的关系

**边缘计算在不同抽象层的应用**：

| 抽象层          | 边缘计算应用场景      | 典型技术              |
| --------------- | --------------------- | --------------------- |
| **虚拟化**      | 边缘 GPU 资源池化     | GPU 虚拟化、MIG       |
| **容器化**      | 边缘容器部署          | K3s、containerd       |
| **沙盒化**      | 边缘轻量沙盒          | Firecracker、gVisor   |
| **WebAssembly** | 边缘轻量应用、AI 推理 | WasmEdge、WasmEdge AI |

---

## 3. 边缘计算场景

### 3.1 低延迟需求

**场景描述**：

- **IoT 设备**：需要低延迟响应
- **实时交互**：AR/VR 应用需要低延迟
- **自动驾驶**：需要毫秒级响应

**架构设计**：

```text
IoT 设备
  ↓ (< 10ms)
边缘节点（K3s + WasmEdge）
  ↓
边缘服务（低延迟处理）
  ↓
结果返回
```

**延迟对比**：

- **云端处理**：50-200ms（网络延迟 + 处理延迟）
- **边缘处理**：< 10ms（本地处理）

### 3.2 离线运行需求

**场景描述**：

- **网络不稳定**：边缘节点网络可能不稳定
- **离线能力**：需要支持离线运行
- **数据同步**：网络恢复后同步数据

**架构设计**：

```text
边缘节点（离线模式）
├── 本地服务（继续运行）
├── 本地存储（数据暂存）
└── 同步服务（网络恢复后同步）

云端节点（在线模式）
├── 数据服务（接收同步数据）
├── 配置服务（下发配置）
└── 监控服务（监控边缘节点）
```

### 3.3 统一治理需求

**场景描述**：

- **统一管理**：边缘和云端统一管理
- **统一监控**：边缘和云端统一监控
- **统一策略**：边缘和云端统一策略

**架构设计**：

```text
云端控制平面
├── Kubernetes API Server
├── Service Mesh Control Plane
└── OPA Control Plane
    ↓
边缘节点
├── K3s Agent
├── Service Mesh Data Plane
└── OPA Agent
```

---

## 4. 5G MEC 架构

### 4.1 MEC 架构概述

**MEC（Multi-access Edge Computing）**：

- **位置**：5G 基站附近
- **延迟**：< 10ms（vs 云端 50-200ms）
- **带宽**：高带宽、低延迟

**MEC 架构**：

```text
5G 基站
  ↓
MEC 节点（K3s + WasmEdge）
  ├── 边缘应用
  ├── 边缘 AI 推理
  └── 边缘存储
  ↓
核心网
  ↓
云端节点（Kubernetes）
```

### 4.2 MEC 与 K3s 集成

**K3s 在 MEC 中的优势**：

- **轻量级**：K3s < 100 MB，适合边缘节点
- **ARM 支持**：支持 ARM 架构，适合边缘设备
- **离线支持**：支持离线运行

**MEC 部署**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mec-app
spec:
  runtimeClassName: wasm
  containers:
    - name: edge-app
      image: my-registry/edge-app:latest
      resources:
        limits:
          memory: "128Mi"
          cpu: "500m"
```

### 4.3 边缘-云协同

**协同模式**：

1. **边缘优先**：请求优先在边缘处理
2. **云端回退**：边缘不可用时回退到云端
3. **混合处理**：部分处理在边缘，部分在云端

**流量路由**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: edge-service
spec:
  hosts:
    - edge-service
  http:
    - match:
        - headers:
            location:
              regex: "edge-.*"
      route:
        - destination:
            host: edge-service
            subset: edge
          weight: 100
    - route:
        - destination:
            host: edge-service
            subset: cloud
          weight: 100
```

---

## 5. 边缘 Kubernetes 平台

### 5.1 K3s

**K3s 特性**：

- **轻量级**：K3s < 100 MB（vs Kubernetes 数百 MB）
- **ARM 支持**：支持 ARM、ARM64、x86_64
- **离线支持**：支持离线运行
- **简化部署**：一键安装，无需复杂配置

**K3s 部署**：

```bash
# 安装 K3s
curl -sfL https://get.k3s.io | sh -

# 配置 K3s
sudo k3s server --cluster-init

# 加入节点
sudo k3s agent --server https://master:6443 --token <token>
```

**K3s 资源占用**：

- **内存**：< 512 MB（vs Kubernetes 2-4 GB）
- **CPU**：< 1 core（vs Kubernetes 2-4 cores）
- **磁盘**：< 1 GB（vs Kubernetes 10-20 GB）

### 5.2 KubeEdge

**KubeEdge 特性**：

- **边缘计算**：专为边缘计算设计
- **设备管理**：IoT 设备管理
- **离线支持**：支持边缘节点离线运行
- **云端-边缘协同**：云端控制平面 + 边缘数据平面

**KubeEdge 架构**：

```text
云端（Cloud）
├── KubeEdge CloudCore
│   ├── API Server
│   ├── Controller Manager
│   └── Cloud Hub
    ↓
边缘（Edge）
├── KubeEdge EdgeCore
│   ├── EdgeHub
│   ├── EdgeMesh
│   └── DeviceTwin
```

### 5.3 EdgeMesh

**EdgeMesh 特性**：

- **Service Mesh**：边缘 Service Mesh
- **跨节点通信**：边缘节点间直接通信
- **流量管理**：流量路由、负载均衡

**EdgeMesh 部署**：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: edge-service
spec:
  selector:
    app: edge-app
  ports:
    - port: 8080
```

---

## 6. 边缘网络服务

### 6.1 NSM Edge Gateway

**NSM Edge Gateway**：

- **跨域连接**：边缘节点与云端节点连接
- **统一网络**：边缘和云端统一网络平面
- **低延迟**：直接连接，降低延迟

**NSM Edge Gateway 架构**：

```text
边缘节点（Edge Node）
├── NSM Edge Gateway
│   ├── vWire（虚拟线路）
│   └── vL3（虚拟 L3 网络）
    ↓
云端节点（Cloud Node）
├── NSM Cloud Gateway
│   ├── vWire
│   └── vL3
```

### 6.2 边缘 Service Mesh

**边缘 Service Mesh**：

- **Istio Ambient**：Istio 的轻量级模式
- **Linkerd Edge**：Linkerd 的边缘版本
- **Cilium Service Mesh**：基于 eBPF 的 Service Mesh

**Istio Ambient 部署**：

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: edge-namespace
  labels:
    istio.io/dataplane-mode: ambient
---
apiVersion: v1
kind: Pod
metadata:
  name: edge-app
  namespace: edge-namespace
spec:
  containers:
    - name: app
      image: my-registry/edge-app:latest
```

### 6.3 跨域网络聚合

**跨域网络聚合**：

- **NSM Federation**：NSM 联邦，跨域网络聚合
- **统一网络平面**：边缘和云端统一网络平面
- **动态路由**：根据网络状态动态路由

**NSM Federation 配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nsm-federation-config
data:
  config.yaml: |
    federation:
      domains:
        - name: edge-domain
          gateway: edge-gateway.nsm.svc
        - name: cloud-domain
          gateway: cloud-gateway.nsm.svc
```

---

## 7. 边缘计算技术栈

### 7.1 容器运行时

**边缘容器运行时**：

- **containerd**：轻量级容器运行时
- **CRI-O**：Kubernetes CRI 实现
- **双运行时**：runc + WasmEdge（Kubernetes 1.30）

**containerd 配置**：

```toml
version = 2

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
    runtime_type = "io.containerd.runc.v2"
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.wasm]
    runtime_type = "io.containerd.wasm.v2"
```

### 7.2 Wasm 运行时

**边缘 Wasm 运行时**：

- **WasmEdge 0.14**：云原生 WebAssembly 运行时
- **特性**：冷启动 < 1ms，镜像 < 2 MB，支持 GPU 加速

**WasmEdge 部署**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: my-registry/wasm-app:latest
      resources:
        limits:
          memory: "64Mi"
          cpu: "250m"
```

### 7.3 边缘存储

**边缘存储方案**：

- **本地存储**：HostPath、Local PV
- **分布式存储**：Longhorn、Rook
- **对象存储**：MinIO Edge

**Local PV 配置**：

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: /mnt/edge-storage
```

---

## 8. 边缘 AI 推理

### 8.1 边缘 AI 架构

**架构设计**：

```text
云端训练
  ↓
模型优化（量化、剪枝）
  ↓
模型编译（ONNX → Wasm）
  ↓
边缘部署（K3s + WasmEdge AI）
  ↓
边缘推理（< 10ms）
  ↓
结果上报（云端）
```

**边缘 AI 优势**：

- **低延迟**：< 10ms 推理延迟
- **隐私保护**：数据不出边缘
- **离线支持**：支持离线推理

### 8.2 模型部署

**WasmEdge AI 部署**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: edge-ai-inference
spec:
  runtimeClassName: wasm
  containers:
    - name: ai-inference
      image: my-registry/ai-model:latest
      resources:
        limits:
          memory: "256Mi"
          cpu: "1000m"
      env:
        - name: MODEL_PATH
          value: "/models/model.wasm"
```

### 8.3 推理优化

**优化技术**：

- **模型量化**：INT8 量化，减少模型大小
- **模型剪枝**：移除冗余参数
- **编译优化**：WasmEdge AI 优化

**优化效果**：

- **模型大小**：减少 70-90%
- **推理速度**：提升 2-5×
- **内存占用**：减少 50-80%

---

## 9. 最佳实践

### 9.1 资源管理

**边缘资源管理**：

- **资源限制**：设置合理的资源限制
- **资源优先级**：关键服务优先分配资源
- **自动扩缩容**：根据工作负载自动扩缩容

**HPA 配置**：

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: edge-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: edge-app
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### 9.2 网络优化

**网络优化策略**：

- **边缘优先**：请求优先在边缘处理
- **本地缓存**：缓存常用数据到边缘
- **压缩传输**：压缩数据传输

**缓存策略**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: edge-cache-config
data:
  cache.yaml: |
    cache:
      ttl: 3600
      maxSize: 1GB
      strategy: LRU
```

### 9.3 安全策略

**边缘安全策略**：

- **认证授权**：使用 SPIFFE/SPIRE 进行身份认证
- **数据加密**：传输加密和存储加密
- **安全策略**：使用 OPA 进行安全策略管理

**OPA 策略**：

```rego
package edge.security

default allow = false

allow {
    input.user == "edge-user"
    input.resource == "edge-service"
    input.action == "read"
}
```

---

## 10. 相关文档

### 相关文档

- **[WebAssembly 视角](webassembly-view.md)** - WebAssembly 架构视角（边缘计算）
- **[AI/ML 视角](ai-ml-architecture-view.md)** - AI/ML 架构视角（边缘 AI 推理）
- **[Service Mesh 视角](service-mesh-view.md)** - Service Mesh 架构视角（边缘
  Service Mesh）
- **[Network Service Mesh 视角](network-service-mesh-view.md)** - NSM 架构视角（
  边缘网络）

### 理论文档

- **[Ψ₅：第五次归纳映射](../00-theory/02-induction-proof/psi5-wasm.md)** -
  WebAssembly 抽象层（边缘计算）
- **[L4：Wasm 内存安全引理](../00-theory/05-lemmas-theorems/L4-wasm-memory-safety.md)** -
  内存安全（边缘安全）

### 实现细节

- **[WasmEdge 实现细节](../01-implementation/06-wasm/)** - WasmEdge 实现细节
- **[K3s 实现细节](../TECHNICAL/02-k3s/)** - K3s 实现细节

### 学术资源

- **[ACADEMIC-REFERENCES.md](../ACADEMIC-REFERENCES.md)** - 学术资源文档
  - **Wikipedia**：Edge Computing、5G、MEC

---

**更新时间**：2025-11-05 **版本**：v1.0 **参考**：`architecture_view.md` 边缘计
算部分
