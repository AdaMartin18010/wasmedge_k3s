# 7 层 4 域模型部署指南

## 📑 目录

- [1. 部署概述](#1-部署概述)
- [2. 部署架构](#2-部署架构)
- [3. 部署步骤](#3-部署步骤)
- [4. 验证测试](#4-验证测试)

---

## 1. 部署概述

本文档提供 7 层 4 域模型的完整部署指南，包括每层的部署配置和层间交互。

### 1.1 部署目标

- **L1-L2**：计算资源抽象和虚拟化
- **L3**：分布式调度
- **L4**：网络和存储数据面
- **L5**：控制面和策略治理
- **L6**：可观测性和故障治理
- **L7**：应用交付

### 1.2 部署前提

- Kubernetes 集群（v1.24+）
- OpenStack 集群（可选，用于 VM 管理）
- 网络和存储基础设施
- 监控和日志系统

---

## 2. 部署架构

### 2.1 整体部署拓扑

```text
┌─────────────────────────────────────────┐
│            L7 应用交付层                 │
│  (GitLab CI, Argo CD, Helm)             │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│       L6 可观测性 & 故障治理              │
│  (Prometheus, Grafana, Jaeger, ChaosMesh)│
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         L5 控制面 & 治理                 │
│  (kube-apiserver, OPA, Gatekeeper)       │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│        L4 分布式数据面                   │
│  (CNI, CSI, Kafka)                       │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│        L3 分布式调度层                   │
│  (K8s Scheduler, Nova Scheduler)         │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│        L2 计算虚拟层                     │
│  (containerd, runC, gVisor, Firecracker) │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│        L1 硬件资源层                     │
│  (CPU, Memory, I/O, NUMA)                │
└─────────────────────────────────────────┘
```

---

## 3. 部署步骤

### 3.1 L1 硬件资源层部署

**步骤 1：配置 NUMA 拓扑**:

```bash
# 查看 NUMA 拓扑
numactl --hardware

# 配置 NUMA 策略
echo 0 > /proc/sys/vm/zone_reclaim_mode
```

**步骤 2：启用 IOMMU**:

```bash
# 编辑 grub
GRUB_CMDLINE_LINUX="intel_iommu=on iommu=pt"

# 重启后验证
dmesg | grep -i iommu
```

**步骤 3：配置大页内存**:

```bash
# 分配大页内存
echo 1024 > /proc/sys/vm/nr_hugepages

# 创建 hugepage 目录
mkdir -p /mnt/huge
mount -t hugetlbfs nodev /mnt/huge
```

---

### 3.2 L2 计算虚拟层部署

**步骤 1：安装 containerd**:

```bash
# 安装 containerd
wget https://github.com/containerd/containerd/releases/download/v1.7.0/containerd-1.7.0-linux-amd64.tar.gz
tar xvf containerd-1.7.0-linux-amd64.tar.gz
sudo cp bin/* /usr/local/bin/

# 配置 containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
```

**步骤 2：配置 gVisor**:

```bash
# 下载 runsc
wget https://storage.googleapis.com/gvisor/releases/release/latest/x86_64/runsc
sudo mv runsc /usr/local/bin
sudo chmod +x /usr/local/bin/runsc

# 配置 containerd
sudo mkdir -p /etc/containerd
cat >> /etc/containerd/config.toml <<EOF
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runsc]
  runtime_type = "io.containerd.runsc.v1"
EOF
```

**步骤 3：配置 Firecracker**:

```bash
# 下载 Firecracker
wget https://github.com/firecracker-microvm/firecracker/releases/download/v1.4.0/firecracker-v1.4.0-x86_64.tgz
tar xvf firecracker-v1.4.0-x86_64.tgz
sudo mv release-*/firecracker-*/firecracker-* /usr/local/bin/firecracker
```

---

### 3.3 L3 分布式调度层部署

**步骤 1：部署 Kubernetes**:

```bash
# 使用 kubeadm 初始化集群
kubeadm init --pod-network-cidr=10.244.0.0/16

# 配置 kubectl
mkdir -p $HOME/.kube
sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

**步骤 2：部署 CNI**:

```bash
# 部署 Calico
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

**步骤 3：配置调度器**:

```yaml
# 创建调度器配置
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: default-scheduler
    plugins:
      score:
        enabled:
          - name: NodeResourcesFit
            weight: 1
          - name: NodeAffinity
            weight: 10
```

---

### 3.4 L4 分布式数据面部署

**步骤 1：部署 Service Mesh**:

```bash
# 安装 Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH
istioctl install --set profile=default
```

**步骤 2：配置存储**:

```bash
# 部署 Ceph CSI
kubectl apply -f https://raw.githubusercontent.com/ceph/ceph-csi/main/deploy/rbd/kubernetes/csi-provisioner-rbac.yaml
kubectl apply -f https://raw.githubusercontent.com/ceph/ceph-csi/main/deploy/rbd/kubernetes/csi-nodeplugin-rbac.yaml
kubectl apply -f https://raw.githubusercontent.com/ceph/ceph-csi/main/deploy/rbd/kubernetes/csi-rbdplugin-provisioner.yaml
```

---

### 3.5 L5 控制面 & 治理部署

**步骤 1：部署 OPA Gatekeeper**:

```bash
# 安装 Gatekeeper
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.14/deploy/gatekeeper.yaml

# 验证安装
kubectl wait --for=condition=Ready pod -l control-plane=controller-manager -n gatekeeper-system
```

**步骤 2：配置策略**:

```yaml
# 创建 ConstraintTemplate
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg}] {
          not input.review.object.metadata.labels.app
          msg := "Pod must have 'app' label"
        }
```

---

### 3.6 L6 可观测性 & 故障治理部署

**步骤 1：部署 Prometheus**:

```bash
# 使用 Helm 安装
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
```

**步骤 2：部署 Jaeger**:

```bash
# 使用 Operator 安装
kubectl create namespace observability
kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.49.0/jaeger-operator.yaml -n observability
```

**步骤 3：部署 ChaosMesh**:

```bash
# 安装 ChaosMesh
curl -sSL https://mirrors.chaos-mesh.org/latest/install.sh | bash
```

---

### 3.7 L7 应用交付层部署

**步骤 1：部署 Argo CD**:

```bash
# 安装 Argo CD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 获取初始密码
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**步骤 2：配置 GitLab CI**:

```yaml
# .gitlab-ci.yml
stages:
  - build
  - deploy

build:
  stage: build
  script:
    - docker build -t app:latest .
    - docker push registry.example.com/app:latest

deploy:
  stage: deploy
  script:
    - kubectl apply -f k8s/
```

---

## 4. 验证测试

### 4.1 L1-L2 验证

**测试 CPU 分区**：

```bash
# 创建测试 Pod
kubectl run test-pod --image=busybox --limits=cpu=500m,memory=512Mi

# 验证资源分配
kubectl describe pod test-pod | grep -A 5 "Limits\|Requests"
```

**测试内存分区**：

```bash
# 监控内存使用
kubectl top pod test-pod
```

### 4.2 L3 验证

**测试调度**：

```bash
# 创建 Deployment
kubectl create deployment test --image=nginx --replicas=3

# 验证调度
kubectl get pods -o wide
```

### 4.3 L4 验证

**测试网络**：

```bash
# 创建 Service
kubectl expose deployment test --port=80

# 测试连通性
kubectl run test-client --image=busybox --rm -it -- wget -O- test:80
```

**测试存储**：

```bash
# 创建 PVC
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
EOF

# 验证 PVC
kubectl get pvc test-pvc
```

### 4.4 L5 验证

**测试策略**：

```bash
# 创建违反策略的 Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: test
    image: busybox
EOF

# 验证策略阻止
kubectl get pod test-pod
```

### 4.5 L6 验证

**测试监控**：

```bash
# 访问 Prometheus
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090

# 查询指标
curl http://localhost:9090/api/v1/query?query=up
```

### 4.6 L7 验证

**测试 GitOps**：

```bash
# 创建 Argo CD Application
kubectl apply -f - <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: test-app
spec:
  source:
    repoURL: https://github.com/example/repo
    path: k8s/
  destination:
    server: https://kubernetes.default.svc
    namespace: default
EOF

# 验证同步状态
argocd app get test-app
```

---

## 5. 故障排查

### 5.1 常见问题

**问题 1：Pod 无法启动**:

**排查步骤**：

```bash
# 查看 Pod 状态
kubectl describe pod <pod-name>

# 查看日志
kubectl logs <pod-name>

# 查看事件
kubectl get events --sort-by='.lastTimestamp'
```

**问题 2：网络不通**:

**排查步骤**：

```bash
# 检查 CNI
kubectl get pods -n kube-system | grep cni

# 检查网络策略
kubectl get networkpolicies

# 测试连通性
kubectl run test --image=busybox --rm -it -- ping <target>
```

**问题 3：存储无法挂载**:

**排查步骤**：

```bash
# 检查 CSI 驱动
kubectl get pods -n kube-system | grep csi

# 检查 PV/PVC
kubectl get pv,pvc

# 查看存储类
kubectl get storageclass
```

---

## 6. 性能调优

### 6.1 启动优化

**镜像预热**：

```bash
# 预拉取镜像
kubectl create job --from=cronjob/prepull --image=app:latest
```

**快照优化**：

```bash
# 创建 Firecracker 快照
firecracker-ctr snapshot create \
  --vm-state-path /snapshots/base-vm-state \
  --mem-file-path /snapshots/base-mem
```

### 6.2 内存优化

**内存池配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: memory-config
data:
  pool-size: "4Gi"
  chunk-size: "64Mi"
```

### 6.3 网络优化

**eBPF 加速**：

```bash
# 启用 Cilium eBPF
helm install cilium cilium/cilium \
  --set eBPF.enabled=true \
  --set eBPF.hostRouting=true
```

---

## 7. 安全加固

### 7.1 网络策略

**默认拒绝**：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### 7.2 Pod 安全策略

**PSP 配置**：

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  runAsUser:
    rule: MustRunAsNonRoot
  seLinux:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
```

---

## 8. 结论

### 8.1 部署检查清单

- [ ] L1：硬件资源层配置完成
- [ ] L2：计算虚拟层部署完成
- [ ] L3：分布式调度层配置完成
- [ ] L4：分布式数据面部署完成
- [ ] L5：控制面 & 治理部署完成
- [ ] L6：可观测性 & 故障治理部署完成
- [ ] L7：应用交付层部署完成
- [ ] 所有层验证测试通过
- [ ] 性能调优完成
- [ ] 安全加固完成

---

**相关文档**：

- [`7-layer-4-domain-implementation.md`](7-layer-4-domain-implementation.md) -
  实现细节
- [`../00-theory/07-system-model/7-layer-4-domain-formalization.md`](../00-theory/07-system-model/7-layer-4-domain-formalization.md) -
  理论论证

---

**更新时间**：2025-11-05 **版本**：v1.0
