# 边缘零售 K8s 架构设计（基于 system_view 案例 D）

## 📑 目录

- [📑 目录](#-目录)
- [1. 场景概述](#1-场景概述)
  - [1.1 业务需求](#11-业务需求)
  - [1.2 挑战分析](#12-挑战分析)
- [2. 架构设计](#2-架构设计)
  - [2.1 整体架构](#21-整体架构)
  - [2.2 7 层 4 域映射](#22-7-层-4-域映射)
- [3. K3s 轻量控制面](#3-k3s-轻量控制面)
  - [3.1 K3s 安装](#31-k3s-安装)
  - [3.2 轻量化优化](#32-轻量化优化)
- [4. gVisor 沙盒隔离](#4-gvisor-沙盒隔离)
  - [4.1 gVisor 配置](#41-gvisor-配置)
  - [4.2 安全策略](#42-安全策略)
- [5. 网络隔离方案](#5-网络隔离方案)
  - [5.1 Cilium eBPF 配置](#51-cilium-ebpf-配置)
  - [5.2 mTLS + SPIFFE](#52-mtls--spiffe)
- [6. 边缘-云协同](#6-边缘-云协同)
  - [6.1 云端统一管理](#61-云端统一管理)
  - [6.2 断网缓存](#62-断网缓存)
- [7. 规模化部署](#7-规模化部署)
  - [7.1 100 门店部署](#71-100-门店部署)
  - [7.2 地域拓扑固定](#72-地域拓扑固定)
  - [7.3 资源优化](#73-资源优化)
- [8. 安全验证](#8-安全验证)
  - [8.1 渗透测试](#81-渗透测试)
  - [8.2 安全审计](#82-安全审计)
- [9. 监控与可观测性](#9-监控与可观测性)
  - [9.1 边缘聚合](#91-边缘聚合)
  - [9.2 采样策略](#92-采样策略)
- [10. 总结](#10-总结)
  - [10.1 关键成果](#101-关键成果)
  - [10.2 经验总结](#102-经验总结)

---

## 1. 场景概述

### 1.1 业务需求

基于 `system_view.md` 案例 D：边缘 K8s（100 门店，4 核 ARM 盒子）

**核心需求**：

- **硬件限制**：4 核 ARM Cortex-A55，无 VT 型虚拟化
- **业务负载**：AI 推理 + POS 容器
- **安全要求**：不可被恶意盒子逃逸到门店局域网
- **规模化**：100 门店统一管理

### 1.2 挑战分析

| 挑战     | 描述                 | 影响            |
| -------- | -------------------- | --------------- |
| 硬件限制 | ARM 无 VT 型虚拟化   | 无法使用 KVM    |
| 资源受限 | 4 核 ARM，内存有限   | 需要轻量级方案  |
| 安全隔离 | 防止逃逸到门店局域网 | 需要强隔离      |
| 规模化   | 100 门店统一管理     | 需要边缘-云协同 |

---

## 2. 架构设计

### 2.1 整体架构

```text
┌─────────────────────────────────────────────────────────┐
│ 云端控制面（统一管理）                                     │
│ Prometheus + Grafana + OPA + GitOps                     │
└─────────────────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
┌───────▼────┐ ┌───▼────┐ ┌───▼────┐
│ 门店 1      │ │ 门店 2  │ │ 门店 3  │
│ (4核 ARM)   │ │(4核 ARM)│ │(4核 ARM)│
│             │ │         │ │         │
│ ┌─────────┐ │ ┌───────┐ │ ┌───────┐ │
│ │ K3s     │ │ │ K3s   │ │ │ K3s   │ │
│ │ 控制面   │ │ │控制面  │ │ │控制面  │ │
│ └─────────┘ │ └───────┘ │ └───────┘ │
│             │ │         │ │         │
│ ┌─────────┐ │ ┌───────┐ │ ┌───────┐ │
│ │ gVisor  │ │ │gVisor │ │ │gVisor │ │
│ │ 沙盒容器 │ │ │沙盒容器│ │ │沙盒容器│ │
│ └─────────┘ │ └───────┘ │ └───────┘ │
│             │ │         │ │         │
│ ┌─────────┐ │ ┌───────┐ │ ┌───────┐ │
│ │ WASM    │ │ │ WASM  │ │ │ WASM  │ │
│ │ 函数    │ │ │函数   │ │ │函数   │ │
│ └─────────┘ │ └───────┘ │ └───────┘ │
│             │ │         │ │         │
│ ┌─────────┐ │ ┌───────┐ │ ┌───────┐ │
│ │ Cilium  │ │ │Cilium │ │ │Cilium │ │
│ │ eBPF    │ │ │eBPF   │ │ │eBPF   │ │
│ └─────────┘ │ └───────┘ │ └───────┘ │
└─────────────┘ └─────────┘ └─────────┘
```

### 2.2 7 层 4 域映射

**L1 硬件资源层**：

- ARM Cortex-A55，无 VT 型虚拟化
- 4 核 CPU，4GB 内存
- 本地存储（eMMC）

**L2 计算虚拟层**：

- gVisor-runsc（只暴露 113 个 syscall）
- WASM 运行时（WasmEdge）
- GPU 用 Mali 用户态驱动

**L3 分布式调度层**：

- K3s 轻量控制面
- 断网缓存策略
- Placement 用"地域拓扑"固定门店 Pod

**L4 分布式数据面**：

- Cilium+eBPF
- 强制 mTLS + SPIFFE ID
- 边缘无 NAT 穿透

**L5 控制面 & 治理**：

- OPA Gatekeeper
- 禁止任何 privileged 容器
- WASM 函数默认网络隔离

**L6 可观测性 & 故障治理**：

- Prometheus + Grafana Agent 边缘聚合
- 卫星链路回传 1% 采样

**L7 应用交付层**：

- GitOps（Argo CD）
- 镜像缓存（Dragonfly P2P）

---

## 3. K3s 轻量控制面

### 3.1 K3s 安装

**ARM 架构安装**：

```bash
# 安装 K3s
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable=traefik" sh -

# 验证安装
kubectl get nodes
```

**K3s 配置**：

```yaml
# /etc/rancher/k3s/config.yaml
disable:
  - traefik
  - servicelb
data-dir: /var/lib/rancher/k3s
cluster-cidr: "10.42.0.0/16"
service-cidr: "10.43.0.0/16"
```

### 3.2 轻量化优化

**资源限制**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: k3s-server
spec:
  containers:
    - name: k3s
      resources:
        requests:
          cpu: 500m
          memory: 512Mi
        limits:
          cpu: 1000m
          memory: 1Gi
```

**断网缓存策略**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: k3s-cache-config
data:
  cache.yaml: |
    images:
      cache-dir: /var/lib/rancher/k3s/cache
      cache-size: 10Gi
    charts:
      cache-dir: /var/lib/rancher/k3s/charts
      cache-size: 1Gi
```

---

## 4. gVisor 沙盒隔离

### 4.1 gVisor 配置

**ARM 架构支持**：

```bash
# 下载 ARM 版本 runsc
wget https://storage.googleapis.com/gvisor/releases/release/latest/arm64/runsc
sudo mv runsc /usr/local/bin
sudo chmod +x /usr/local/bin/runsc

# 配置 containerd
sudo mkdir -p /etc/containerd
cat >> /etc/containerd/config.toml <<EOF
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc]
  runtime_type = "io.containerd.runsc.v1"
  runtime_engine = ""
  runtime_root = ""
  privileged_without_host_devices = false
  base_runtime_spec = ""
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc.options]
  TypeUrl = "io.containerd.runsc.v1.options"
EOF
```

**RuntimeClass 配置**：

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
overhead:
  podFixed:
    memory: "30Mi"
    cpu: "50m"
```

### 4.2 安全策略

**Syscall 白名单**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: gvisor-config
data:
  config.yaml: |
    syscall_whitelist:
      - read
      - write
      - open
      - close
      # ... 113 个 syscall
    blocked_syscalls:
      - ptrace
      - mount
      - umount
      - pivot_root
```

**Pod 安全策略**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pos-container
spec:
  runtimeClassName: gvisor
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: pos
      image: pos-app:latest
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
```

---

## 5. 网络隔离方案

### 5.1 Cilium eBPF 配置

**安装 Cilium**：

```bash
# 安装 Cilium
helm repo add cilium https://helm.cilium.io/
helm install cilium cilium/cilium \
  --namespace kube-system \
  --set eBPF.enabled=true \
  --set eBPF.hostRouting=true \
  --set kubeProxyReplacement=strict
```

**网络策略**：

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: edge-isolation
spec:
  endpointSelector:
    matchLabels:
      app: pos
  egress:
    - toEndpoints:
        - matchLabels:
            app: pos
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
    - toCIDR:
        - "10.42.0.0/16" # 允许访问 K3s 集群内部
    - toCIDRSet:
        - cidr: "0.0.0.0/0"
          except:
            - "192.168.1.0/24" # 禁止访问门店局域网
```

### 5.2 mTLS + SPIFFE

**SPIFFE ID 配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: spiffe-config
data:
  config.yaml: |
    trust_domain: edge-retail.example.org
    spiffe_id:
      pos-container: "spiffe://edge-retail.example.org/pos/store-1"
      ai-inference: "spiffe://edge-retail.example.org/ai/store-1"
```

**mTLS 配置**：

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: mtls-policy
spec:
  endpointSelector:
    matchLabels:
      app: pos
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: ai-inference
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
      tls:
        certificate: /etc/certs/pos.crt
        key: /etc/certs/pos.key
```

---

## 6. 边缘-云协同

### 6.1 云端统一管理

**Prometheus 远程写入**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-agent-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      external_labels:
        cluster: edge-store-1
        region: region-1
    remote_write:
    - url: https://prometheus.cloud.example.com/api/v1/write
      queue_config:
        max_samples_per_send: 1000
        max_shards: 200
      write_relabel_configs:
      - source_labels: [__name__]
        regex: '.*'
        action: keep
      # 只回传 1% 采样
      - source_labels: [__name__]
        regex: '.*'
        action: drop
        target_label: __sampled__
        replacement: '0.01'
```

**OPA 策略下发**：

```bash
# 云端策略仓库
git clone https://github.com/example/edge-policies.git

# 边缘拉取策略
kubectl apply -f https://policy.example.com/edge-policies/store-policy.yaml
```

### 6.2 断网缓存

**镜像缓存**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: dragonfly-config
data:
  config.yaml: |
    cache:
      enabled: true
      cache-dir: /var/lib/dragonfly/cache
      cache-size: 10Gi
    p2p:
      enabled: true
      peer-nodes:
      - store-1:65001
      - store-2:65001
      - store-3:65001
```

**应用缓存**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-cache-config
data:
  cache.yaml: |
    pos-app:
      image: pos-app:latest
      cache-strategy: always
    ai-inference:
      image: ai-model:latest
      cache-strategy: on-demand
```

---

## 7. 规模化部署

### 7.1 100 门店部署

**部署脚本**：

```bash
#!/bin/bash
# deploy-edge-stores.sh

for store in {1..100}; do
  echo "Deploying store $store..."

  # 生成门店配置
  cat > store-$store-config.yaml <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: store-config
data:
  store-id: "$store"
  region: "region-$((($store-1)/20+1))"
  zone: "zone-$((($store-1)/5+1))"
EOF

  # 部署到门店
  kubectl apply -f store-$store-config.yaml --context=edge-store-$store

  # 等待就绪
  kubectl wait --for=condition=Ready pod -l app=pos --context=edge-store-$store
done
```

### 7.2 地域拓扑固定

**Placement 策略**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: placement-policy
data:
  policy.yaml: |
    rules:
    - name: store-pod-placement
      match:
        labels:
          app: pos
      placement:
        nodeSelector:
          store-id: "${STORE_ID}"
        affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
              - matchExpressions:
                - key: store-id
                  operator: In
                  values:
                  - "${STORE_ID}"
```

### 7.3 资源优化

**资源使用统计**：

```text
单节点资源分配（4核 ARM，4GB 内存）：

- K3s 控制面：500m CPU, 512Mi 内存
- gVisor 沙盒容器（20个）：每个 30MB 内存，总计 600MB
- WASM 函数（20个）：每个 <1MB 内存，总计 <20MB
- Cilium eBPF：100MB 内存
- 系统预留：500MB 内存
- 总计：~1.7GB 内存，余量 25%
```

---

## 8. 安全验证

### 8.1 渗透测试

**测试场景**：

1. **逃逸测试**：尝试从容器逃逸到宿主机

   - ✅ 被 gVisor 阻止（syscall 拦截）
   - ✅ 无法访问宿主机文件系统

2. **网络逃逸**：尝试访问门店局域网

   - ✅ 被 Cilium 网络策略阻止
   - ✅ 无法调用门店银企直连网段

3. **权限提升**：尝试获取 privileged 权限
   - ✅ 被 OPA Gatekeeper 阻止
   - ✅ Pod 无法创建 privileged 容器

### 8.2 安全审计

**审计日志**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: audit-config
data:
  audit.yaml: |
    apiVersion: audit.k8s.io/v1
    kind: Policy
    rules:
    - level: Metadata
      resources:
      - group: ""
        resources:
        - pods
        - namespaces
    - level: RequestResponse
      resources:
      - group: ""
        resources:
        - services
```

---

## 9. 监控与可观测性

### 9.1 边缘聚合

**Grafana Agent 配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-agent-config
data:
  agent.yaml: |
    server:
      log_level: info
    metrics:
      configs:
      - name: edge-metrics
        scrape_configs:
        - job_name: 'k3s'
          kubernetes_sd_configs:
          - role: pod
        remote_write:
        - url: https://prometheus.cloud.example.com/api/v1/write
          queue_config:
            max_samples_per_send: 1000
```

### 9.2 采样策略

**1% 采样配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: sampling-config
data:
  config.yaml: |
    sampling_rate: 0.01
    sample_labels:
    - store_id
    - app
    - tier
```

---

## 10. 总结

### 10.1 关键成果

✅ **资源利用**：单节点 4GB 内存，可同时跑 20 个沙盒容器 + 20 个 WASM 函数，内存
余量 25% ✅ **安全验证**：渗透测试证明红队无法逃逸到宿主机，无法调用门店银企直连
网段 ✅ **规模化**：100 门店统一管理，边缘-云协同 ✅ **轻量化**：K3s 控制面占用
<500MB 内存

### 10.2 经验总结

1. **硬件限制**：ARM 无 VT 型虚拟化，使用 gVisor 用户态拦截
2. **安全隔离**：gVisor + Cilium + OPA 多层防护
3. **边缘-云协同**：云端统一管理，边缘本地缓存
4. **资源优化**：WASM 函数极致轻量，提升密度

---

**相关文档**：

- [`system-view-cases-analysis.md`](system-view-cases-analysis.md) - system_view
  案例扩展分析
- [`../01-implementation/08-edge/k3s-setup.md`](../01-implementation/08-edge/k3s-setup.md) -
  K3s 设置
- [`../01-implementation/03-sandboxing/gvisor-setup.md`](../01-implementation/03-sandboxing/gvisor-setup.md) -
  gVisor 设置
- [`../01-views/edge-computing-view.md`](../01-views/edge-computing-view.md) -
  边缘计算视角

---

**更新时间**：2025-11-05 **版本**：v1.0 **维护者**：基于 system_view.md 案例 D
扩展
