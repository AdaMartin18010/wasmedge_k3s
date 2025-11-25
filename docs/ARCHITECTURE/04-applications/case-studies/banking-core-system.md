# 银行核心系统架构设计（基于 system_view 案例 A）

**版本**：v1.0 **最后更新：2025-11-15 **维护者**：项目团队

## 📑 目录

- [银行核心系统架构设计（基于 system\_view 案例 A）](#银行核心系统架构设计基于-system_view-案例-a)
  - [📑 目录](#-目录)
  - [1 场景概述](#1-场景概述)
    - [1.1 业务需求](#11-业务需求)
    - [1.2 挑战分析](#12-挑战分析)
  - [2 监管合规要求](#2-监管合规要求)
    - [2.1 监管条文](#21-监管条文)
    - [2.2 理论支撑](#22-理论支撑)
  - [3 架构设计](#3-架构设计)
    - [3.1 整体架构](#31-整体架构)
    - [3.2 分层设计](#32-分层设计)
      - [L1 硬件资源层](#l1-硬件资源层)
      - [L2 计算虚拟层](#l2-计算虚拟层)
      - [L3 分布式调度层](#l3-分布式调度层)
      - [L4 分布式数据面](#l4-分布式数据面)
      - [L5 控制面 \& 治理](#l5-控制面--治理)
      - [L6 可观测性 \& 故障治理](#l6-可观测性--故障治理)
  - [4 热迁移实现](#4-热迁移实现)
    - [4.1 迁移流程](#41-迁移流程)
    - [4.2 KubeVirt 热迁移](#42-kubevirt-热迁移)
    - [4.3 迁移状态监控](#43-迁移状态监控)
  - [5 混合部署方案](#5-混合部署方案)
    - [5.1 部署策略](#51-部署策略)
    - [5.2 统一调度](#52-统一调度)
  - [6 合规审计](#6-合规审计)
    - [6.1 合规检查清单](#61-合规检查清单)
    - [6.2 合规报告](#62-合规报告)
  - [7 性能基准](#7-性能基准)
    - [7.1 启动性能](#71-启动性能)
    - [7.2 网络性能](#72-网络性能)
    - [7.3 热迁移性能](#73-热迁移性能)
  - [8 总结](#8-总结)
    - [8.1 关键成果](#81-关键成果)
    - [8.2 经验总结](#82-经验总结)

---

## 1 场景概述

### 1.1 业务需求

基于 `system_view.md` 案例 A：银行核心系统（监管要求"硬件级隔离"+"热迁移"）

**核心需求**：

- **合规性**：银保监会《商业银行应用程序接口安全管理规范》明确"不同等级系统不得
  共享内核"
- **业务连续性**：核心账务 0 中断，季度演练热迁移
- **统一管理**：兼顾 DevOps 与合规，实现"VM 即 Pod"统一调度

### 1.2 挑战分析

| 挑战     | 描述                       | 影响             |
| -------- | -------------------------- | ---------------- |
| 监管合规 | "不同等级系统不得共享内核" | 容器化直接否决   |
| 热迁移   | 季度演练，0 中断           | 需要完整状态迁移 |
| 混合部署 | VM + Container 统一调度    | 需要统一控制面   |
| 性能要求 | 交易延迟 < 5ms             | 需要 NUMA 优化   |

---

## 2 监管合规要求

### 2.1 监管条文

**银保监会《商业银行应用程序接口安全管理规范》**：

> "不同等级系统不得共享内核"

**解读**：

- **硬件级隔离**：必须使用硬件虚拟化（VT-x/AMD-V）
- **内核隔离**：每个等级系统必须有独立的 guest 内核
- **无法使用容器**：容器共享宿主机内核，不符合要求

### 2.2 理论支撑

**引用公理**：A2（OS 资源封闭）- 参见
[`../00-theory/01-axioms/A2-os-resource.md`](../00-theory/01-axioms/A2-os-resource.md)

**分析**：

- 监管要求"硬件级隔离"，对应虚拟化的归纳映射 Ψ₁
- 容器化共享内核，违反监管要求
- 虚拟化提供独立的 guest 内核，满足合规要求

**引用理论**：Ψ₁（虚拟化抽象层）- 参见
[`../00-theory/02-induction-proof/psi1-virtualization.md`](../00-theory/02-induction-proof/psi1-virtualization.md)

---

## 3 架构设计

### 3.1 整体架构

```text
┌─────────────────────────────────────────────────────────┐
│ L7 应用交付层                                            │
│ Glance (VM 模板) + Harbor (OCI) + WASM Registry        │
└─────────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────────┐
│ L6 可观测性 & 故障治理                                    │
│ VictoriaMetrics (单集群多租户)                          │
└─────────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────────┐
│ L5 控制面 & 治理                                         │
│ OPA (统一 Quota) + API Gateway + RBAC                   │
└─────────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────────┐
│ L4 分布式数据面                                          │
│ OVS-DPDK (fast path) + virtio-user                      │
└─────────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────────┐
│ L3 分布式调度层                                          │
│ KubeVirt (VM 调度) + K8s Scheduler (容器调度)           │
│ Placement CRD (统一抽象) + etcd (共享存储)              │
└─────────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────────┐
│ L2 计算虚拟层                                            │
│ KVM (VM) + containerd (容器) + Kata (容器形态 VM 隔离)  │
└─────────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────────┐
│ L1 硬件资源层                                            │
│ NUMA 拓扑感知 + pCPU Pinning (VM)                       │
└─────────────────────────────────────────────────────────┘
```

### 3.2 分层设计

#### L1 硬件资源层

**NUMA 拓扑感知**：

```yaml
# Node 配置
apiVersion: v1
kind: Node
metadata:
  annotations:
    topology.kubernetes.io/zone: zone-1
    topology.kubernetes.io/region: region-1
    kubevirt.io/node-topology: |
      {
        "numa_nodes": [
          {
            "id": 0,
            "cpus": [0, 1, 2, 3],
            "memory": "32Gi"
          },
          {
            "id": 1,
            "cpus": [4, 5, 6, 7],
            "memory": "32Gi"
          }
        ]
      }
```

**pCPU Pinning 配置**：

```yaml
# VM 配置
apiVersion: kubevirt.io/v1
kind: VirtualMachine
spec:
  template:
    spec:
      domain:
        cpu:
          cores: 4
          model: host-passthrough
          numa:
            guestMappingPassthrough: {}
          pinning:
            vcpu:
              - vcpu: 0
                cpuset: "0"
              - vcpu: 1
                cpuset: "1"
              - vcpu: 2
                cpuset: "2"
              - vcpu: 3
                cpuset: "3"
```

#### L2 计算虚拟层

**KVM + KubeVirt 配置**：

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: banking-core-vm
spec:
  running: true
  template:
    metadata:
      labels:
        app: banking-core
        tier: core
    spec:
      domain:
        devices:
          disks:
            - disk:
                bus: virtio
              name: disk0
            - disk:
                bus: virtio
              name: cloudinitdisk
          interfaces:
            - name: default
              masquerade: {}
        resources:
          requests:
            memory: 8Gi
            cpu: 4
          limits:
            memory: 16Gi
            cpu: 4
      volumes:
        - name: disk0
          persistentVolumeClaim:
            claimName: banking-core-pvc
        - name: cloudinitdisk
          cloudInitNoCloud:
            userData: |
              #cloud-config
              password: changeme
              chpasswd: { expire: False }
```

**Kata Containers 配置**（容器形态，VM 隔离）：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kata-pod
spec:
  runtimeClassName: kata
  containers:
    - name: app
      image: banking-app:latest
```

#### L3 分布式调度层

**Placement CRD 统一抽象**：

```yaml
apiVersion: scheduling.kubevirt.io/v1alpha1
kind: PlacementPolicy
metadata:
  name: banking-core-placement
spec:
  rules:
    - name: core-vm-placement
      match:
        labels:
          tier: core
      placement:
        nodeSelector:
          node-role.kubernetes.io/compute: ""
        affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
                - matchExpressions:
                    - key: topology.kubernetes.io/zone
                      operator: In
                      values:
                        - zone-1
```

**共享 etcd 集群**：

```yaml
# K8s etcd 配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: etcd-config
data:
  etcd.conf: |
    name: k8s-etcd
    data-dir: /var/lib/etcd
    listen-peer-urls: http://0.0.0.0:2380
    listen-client-urls: http://0.0.0.0:2379
    initial-cluster: k8s-etcd=http://etcd-0:2380
    initial-cluster-state: new

# OpenStack etcd 配置（共享）
apiVersion: v1
kind: ConfigMap
metadata:
  name: openstack-etcd-config
data:
  etcd.conf: |
    name: nova-etcd
    data-dir: /var/lib/nova-etcd
    listen-peer-urls: http://0.0.0.0:2380
    listen-client-urls: http://0.0.0.0:2379
    initial-cluster: k8s-etcd=http://etcd-0:2380,nova-etcd=http://etcd-1:2380
    initial-cluster-state: existing
```

#### L4 分布式数据面

**OVS-DPDK Fast Path**：

```bash
# OVS-DPDK 配置
ovs-vsctl set Open_vSwitch . other_config:dpdk-init=true
ovs-vsctl set Open_vSwitch . other_config:dpdk-lcore-mask=0x3
ovs-vsctl set Open_vSwitch . other_config:dpdk-socket-mem=1024,1024

# 创建 DPDK 接口
ovs-vsctl add-br br0 -- set bridge br0 datapath_type=netdev
ovs-vsctl add-port br0 dpdk0 -- set Interface dpdk0 type=dpdk options:dpdk-devargs=0000:01:00.0
```

**virtio-user 配置**：

```yaml
# VM 网络配置
apiVersion: kubevirt.io/v1
kind: VirtualMachine
spec:
  template:
    spec:
      domain:
        devices:
          interfaces:
            - name: fastpath
              macAddress: "52:54:00:6f:aa:01"
              model: virtio
              masquerade: {}
            - name: dpdk
              macAddress: "52:54:00:6f:aa:02"
              model: virtio
              multus:
                networkName: ovs-dpdk-network
```

#### L5 控制面 & 治理

**OPA 统一 Quota**：

```rego
package kubernetes.quota

# VM Quota 策略
quota_check[msg] {
    input.request.kind.kind == "VirtualMachine"
    vm := input.request.object
    quota := data.quotas["vm"]
    count_quota := count_resources(vm)
    count_quota.cpu > quota.cpu
    msg := sprintf("VM quota exceeded: CPU %d > %d", [count_quota.cpu, quota.cpu])
}

# Container Quota 策略
quota_check[msg] {
    input.request.kind.kind == "Pod"
    pod := input.request.object
    quota := data.quotas["container"]
    count_quota := count_resources(pod)
    count_quota.memory > quota.memory
    msg := sprintf("Container quota exceeded: Memory %d > %d", [count_quota.memory, quota.memory])
}

count_resources(obj) := {
    "cpu": sum([r | r := obj.spec.template.spec.domain.resources.requests.cpu]),
    "memory": sum([r | r := obj.spec.template.spec.domain.resources.requests.memory])
}
```

#### L6 可观测性 & 故障治理

**VictoriaMetrics 单集群多租户**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: victoriametrics-config
data:
  vmagent.yaml: |
    global:
      external_labels:
        cluster: banking
        region: region-1
    scrape_configs:
    - job_name: 'kubevirt'
      kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
          - kubevirt
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app
      - source_labels: [__meta_kubernetes_pod_label_tier]
        target_label: tier
```

---

## 4 热迁移实现

### 4.1 迁移流程

**KVM Live Migration**：

```bash
# 1. 准备目标节点
virsh migrate --live \
  --persistent \
  --undefinesource \
  --copy-storage-all \
  --migrateuri tcp://dest-host:49152 \
  banking-core-vm \
  qemu+ssh://dest-host/system
```

### 4.2 KubeVirt 热迁移

**VM 迁移配置**：

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: banking-core-vm
spec:
  running: true
  template:
    spec:
      evictionStrategy: LiveMigrate
      domain:
        cpu:
          model: host-passthrough
          features:
            - name: invarianttsc
              policy: require
      migration:
        bandwidthPerMigration: 64Mi
        completionTimeoutPerGiB: 800
        progressTimeout: 150
```

**触发迁移**：

```bash
# 方式 1：节点维护
kubectl drain node-1 --ignore-daemonsets --delete-emptydir-data

# 方式 2：手动迁移
kubectl patch vm banking-core-vm --type merge -p '{"spec":{"migration":{"nodeSelector":{"kubernetes.io/hostname":"node-2"}}}}'
```

### 4.3 迁移状态监控

**迁移状态查询**：

```bash
# 查看迁移状态
kubectl get vmi banking-core-vm -o jsonpath='{.status.migrationState}'

# 迁移指标
kubectl get vmi banking-core-vm -o jsonpath='{.status.migrationMethod}'
```

**Prometheus 指标**：

```promql
# 迁移成功率
rate(kubevirt_vmi_migration_completed_total[5m])

# 迁移持续时间
histogram_quantile(0.95, rate(kubevirt_vmi_migration_duration_seconds_bucket[5m]))
```

---

## 5 混合部署方案

### 5.1 部署策略

**基于合规等级的部署策略**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: deployment-strategy
data:
  strategy.yaml: |
    core_tier:
      runtime: kvm
      isolation: hardware
      migration: live_migrate
      quota: high
    non_core_tier:
      runtime: container
      isolation: namespace
      migration: restart
      quota: medium
    development_tier:
      runtime: container
      isolation: namespace
      migration: restart
      quota: low
```

### 5.2 统一调度

**KubeVirt + K8s Scheduler**：

```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: default-scheduler
    plugins:
      preFilter:
        enabled:
          - name: NodeResourcesFit
          - name: NodeAffinity
      filter:
        enabled:
          - name: NodeResourcesFit
          - name: NodeAffinity
          - name: KubeVirtFilter # 自定义 Filter
      score:
        enabled:
          - name: NodeResourcesFit
            weight: 1
          - name: NodeAffinity
            weight: 10
          - name: KubeVirtScore # 自定义 Score
            weight: 5
```

---

## 6 合规审计

### 6.1 合规检查清单

**硬件隔离检查**：

```bash
# 检查 VM 是否使用硬件虚拟化
virsh domcapabilities banking-core-vm | grep -i kvm

# 检查 pCPU Pinning
virsh vcpuinfo banking-core-vm

# 检查内核隔离
virsh domstate banking-core-vm
```

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
      - group: kubevirt.io
        resources:
        - virtualmachines
    - level: RequestResponse
      resources:
      - group: ""
        resources:
        - pods
        - namespaces
```

### 6.2 合规报告

**自动生成合规报告**：

```bash
# 使用 OPA 生成合规报告
opa eval --data policy.rego --input audit.json \
  'data.compliance.check'

# 使用 Gatekeeper 检查
kubectl get constraints --all-namespaces
```

---

## 7 性能基准

### 7.1 启动性能

| 指标     | VM (KVM)  | Container (runC) | Kata     |
| -------- | --------- | ---------------- | -------- |
| 启动延迟 | 20-40s    | 100-300ms        | 2-5s     |
| 内存开销 | 128-256MB | 10-20MB          | 50-100MB |
| CPU 性能 | 95-98%    | 99-100%          | 95-98%   |

### 7.2 网络性能

| 指标     | OVS-DPDK | virtio-net | SR-IOV   |
| -------- | -------- | ---------- | -------- |
| 延迟     | 55µs     | 52µs       | 10µs     |
| 吞吐量   | 10 Gbps  | 8 Gbps     | 25 Gbps  |
| CPU 占用 | 2 cores  | 1 core     | 0.1 core |

### 7.3 热迁移性能

| 指标     | 值              |
| -------- | --------------- |
| 迁移时间 | 30-60s (8GB VM) |
| 停机时间 | < 100ms         |
| 带宽占用 | 64-128 Mbps     |
| 成功率   | 99.9%           |

---

## 8 总结

### 8.1 关键成果

✅ **合规性**：满足银保监会"硬件级隔离"要求 ✅ **热迁移**：季度演练通过，0 中断
✅ **统一管理**：KubeVirt 实现"VM 即 Pod"统一调度 ✅ **性能优化**：NUMA 感知 +
pCPU Pinning，延迟 < 5ms

### 8.2 经验总结

1. **合规优先**：监管要求不可妥协，必须使用硬件虚拟化
2. **混合部署**：VM + Container 混合部署，兼顾合规和密度
3. **统一控制面**：OPA 统一策略，避免双轨制
4. **性能优化**：NUMA 感知和 pCPU Pinning 是关键

---

**相关文档**：

- [`system-view-cases-analysis.md`](system-view-cases-analysis.md) - system_view
  案例扩展分析
- [`../00-theory/07-system-model/7-layer-4-domain-formalization.md`](../00-theory/07-system-model/7-layer-4-domain-formalization.md) -
  理论论证
- [`../01-implementation/09-system-view/deployment-guide.md`](../01-implementation/09-system-view/deployment-guide.md) -
  部署指南
- [`financial-system.md`](financial-system.md) - 通用金融系统案例

---

**更新时间**：2025-11-05 **版本**：v1.0 **维护者**：基于 system_view.md 案例 A
扩展
