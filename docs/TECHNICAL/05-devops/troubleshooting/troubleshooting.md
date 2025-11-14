# 11. 故障排查：常见问题与解决方案

## 📑 目录

- [11. 故障排查：常见问题与解决方案](#11-故障排查常见问题与解决方案)
  - [📑 目录](#-目录)
  - [11.1 文档定位](#111-文档定位)
  - [11.2 WasmEdge 相关问题](#112-wasmedge-相关问题)
    - [11.2.1 kubectl logs 为空](#1121-kubectl-logs-为空)
    - [11.2.2 镜像拉取失败](#1122-镜像拉取失败)
    - [11.2.3 无法解析 DNS](#1123-无法解析-dns)
    - [11.2.4 WasmEdge "out of bounds" 错误](#1124-wasmedge-out-of-bounds-错误)
  - [11.3 K3s 相关问题](#113-k3s-相关问题)
    - [11.3.1 节点无法加入](#1131-节点无法加入)
    - [11.3.2 Pod 无法启动](#1132-pod-无法启动)
    - [11.3.3 存储问题](#1133-存储问题)
    - [11.3.4 网络问题](#1134-网络问题)
  - [11.4 OPA Gatekeeper 相关问题](#114-opa-gatekeeper-相关问题)
    - [11.4.1 Webhook 超时](#1141-webhook-超时)
    - [11.4.2 策略更新未生效](#1142-策略更新未生效)
    - [11.4.3 策略验证失败](#1143-策略验证失败)
  - [11.5 HPA 相关问题](#115-hpa-相关问题)
    - [11.5.1 HPA 基于 CPU 不触发](#1151-hpa-基于-cpu-不触发)
    - [11.5.2 HPA 指标收集失败](#1152-hpa-指标收集失败)
  - [11.6 性能相关问题](#116-性能相关问题)
    - [11.6.1 启动时间过长](#1161-启动时间过长)
    - [11.6.2 内存占用过高](#1162-内存占用过高)
  - [11.7 网络相关问题](#117-网络相关问题)
    - [11.7.1 Pod 无法访问服务](#1171-pod-无法访问服务)
    - [11.7.2 跨节点 Pod 通信失败](#1172-跨节点-pod-通信失败)
    - [11.7.3 外部访问失败](#1173-外部访问失败)
  - [11.8 存储相关问题](#118-存储相关问题)
    - [11.8.1 PVC 挂载失败](#1181-pvc-挂载失败)
    - [11.8.2 存储性能问题](#1182-存储性能问题)
  - [11.9 故障排查方法](#119-故障排查方法)
    - [11.9.1 基础故障排查步骤](#1191-基础故障排查步骤)
    - [11.9.2 一键诊断脚本](#1192-一键诊断脚本)
    - [11.9.3 性能问题诊断](#1193-性能问题诊断)
    - [11.9.4 高级故障排查方法](#1194-高级故障排查方法)
    - [11.9.5 常用命令速查](#1195-常用命令速查)
  - [11.10 故障排查检查清单](#1110-故障排查检查清单)
    - [11.10.1 WasmEdge 故障排查清单](#11101-wasmedge-故障排查清单)
    - [11.10.2 K3s 故障排查清单](#11102-k3s-故障排查清单)
    - [11.10.3 OPA Gatekeeper 故障排查清单](#11103-opa-gatekeeper-故障排查清单)
    - [11.10.4 综合故障排查清单](#11104-综合故障排查清单)
  - [11.11 故障排查与概念关系矩阵](#1111-故障排查与概念关系矩阵)
    - [11.11.1 使用概念关系矩阵定位问题](#11111-使用概念关系矩阵定位问题)
    - [11.11.2 依赖关系故障排查](#11112-依赖关系故障排查)
    - [11.11.3 属性传递故障排查](#11113-属性传递故障排查)
  - [11.12 参考](#1112-参考)
    - [11.12.1 虚拟化与容器化对比分析](#11121-虚拟化与容器化对比分析)
    - [11.12.2 eBPF 技术堆栈相关文档](#11122-ebpf-技术堆栈相关文档)

---

## 11.1 文档定位

本文档提供 K3s + WasmEdge + OPA 常见问题的排查和解决方案，包括
WasmEdge、K3s、OPA Gatekeeper、HPA 和性能相关问题的诊断和修复。

**文档结构**：

- **WasmEdge 问题**：kubectl logs 为空、镜像拉取失败、DNS 解析失败等
- **K3s 问题**：节点无法加入、Pod 无法启动、存储网络问题等
- **OPA Gatekeeper 问题**：Webhook 超时、策略更新未生效等
- **HPA 问题**：HPA 不触发、指标收集失败等
- **性能问题**：启动时间、内存占用等性能问题

**详细案例**：

- 📚 **[故障排查案例集](cases/README.md)** - 详细的故障排查案例，包含完整的故障描述、排查过程、根因分析、解决方案和验证结果

## 11.2 WasmEdge 相关问题

### 11.2.1 kubectl logs 为空

**现象**：

```bash
$ kubectl logs hello-wasm
# 无输出
```

**根因**： crun 未把 wasm stdout 重定向到 cgroup 的 pipe，导致日志无法输出。

**解决方案**：

```bash
# 升级 crun ≥ 1.8.5
sudo apt-get update
sudo apt-get install -y crun

# 或从源码编译
git clone https://github.com/containers/crun.git
cd crun
./autogen.sh
./configure
make
sudo make install

# 验证 crun 版本
crun --version
# 应该显示 1.8.5 或更高版本
```

**验证**：

```bash
# 重启 kubelet（如果需要）
sudo systemctl restart k3s

# 重新部署 Pod
kubectl delete pod hello-wasm
kubectl apply -f hello-wasm.yaml

# 检查日志
kubectl logs hello-wasm
# 应该有输出
```

### 11.2.2 镜像拉取失败

**现象**：

```bash
$ kubectl describe pod hello-wasm
Events:
  Warning  Failed      Error: failed to pull image "yourhub/hello-wasm:v1"
```

**根因**： Docker Hub 将 `.wasm` 文件视为 blob，需要特殊处理或 token。

**解决方案**：

```bash
# 方法 1：使用 wasm-to-oci 推送
wasm-to-oci push hello-wasm.wasm yourhub/hello-wasm:v1

# 方法 2：使用支持 Wasm 的镜像仓库（如 ghcr.io、阿里云 ACR）
docker tag hello-wasm:v1 ghcr.io/youruser/hello-wasm:v1
docker push ghcr.io/youruser/hello-wasm:v1

# 方法 3：手动构建和推送（使用 Dockerfile FROM scratch）
cat > Dockerfile <<EOF
FROM scratch
COPY hello-wasm.wasm /hello-wasm.wasm
EOF
docker build -t yourhub/hello-wasm:v1 .
docker push yourhub/hello-wasm:v1
```

**验证**：

```bash
# 检查镜像是否可用
docker pull yourhub/hello-wasm:v1

# 重新部署 Pod
kubectl apply -f hello-wasm.yaml

# 检查 Pod 状态
kubectl get pod hello-wasm
```

### 11.2.3 无法解析 DNS

**现象**：

```bash
$ kubectl logs hello-wasm
Error: failed to resolve DNS: example.com
```

**根因**： WASI 预览版网络未完全支持，需要启用 WasmEdge 的
`wasmedge_wasi_socket` 插件。

**解决方案**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-wasm
  annotations:
    module.wasm.image/variant: compat-smart
spec:
  runtimeClassName: wasm
  containers:
    - name: app
      image: yourhub/hello-wasm:v1
      command: ["hello-wasm.wasm"]
      env:
        - name: WASMEDGE_WASI_SOCKET
          value: "true"
```

**或安装 WasmEdge WASI socket 插件**：

```bash
# 安装 WASI socket 插件
wasmedge --plugin wasi_socket

# 验证插件
wasmedge --list-plugins
```

### 11.2.4 WasmEdge "out of bounds" 错误

**现象**：

```bash
$ kubectl logs hello-wasm
Error: out of bounds memory access
```

**根因**：输入 JSON 过大，超出了 Wasm 内存限制。

**解决方案**：

```bash
# 方法 1：增加 Wasm 内存限制
wasmedge --max-memory-page 1024 hello-wasm.wasm

# 方法 2：分段处理输入（在应用代码中）
# 将大 JSON 分段处理，避免一次性加载

# 方法 3：调整 Pod 资源限制
apiVersion: v1
kind: Pod
metadata:
  name: hello-wasm
spec:
  runtimeClassName: wasm
  containers:
    - name: app
      image: yourhub/hello-wasm:v1
      resources:
        limits:
          memory: "100Mi"
        requests:
          memory: "50Mi"
```

## 11.3 K3s 相关问题

### 11.3.1 节点无法加入

**现象**：

```bash
$ kubectl get nodes
# Agent 节点未显示
```

**根因**： Token 错误或网络不通。

**解决方案**：

```bash
# 检查 Token（在 Server 节点）
sudo cat /var/lib/rancher/k3s/server/node-token

# 检查防火墙
sudo ufw status
sudo ufw allow 6443/tcp

# 检查网络连通性（从 Agent 节点）
ping server-ip
curl -k https://server-ip:6443

# 重新加入节点（使用正确的 Token）
curl -sfL https://get.k3s.io | K3S_TOKEN=correct-token \
  K3S_URL=https://server-ip:6443 sh -s - agent
```

**验证**：

```bash
# 在 Server 节点检查
kubectl get nodes

# 应该显示所有节点
```

### 11.3.2 Pod 无法启动

**现象**：

```bash
$ kubectl get pod hello-wasm
NAME          READY   STATUS    RESTARTS   AGE
hello-wasm    0/1     Pending  0          5m
```

**根因**：资源不足（内存或 CPU）。

**解决方案**：

```bash
# 检查节点资源
kubectl describe node

# 检查 Pod 资源请求
kubectl describe pod hello-wasm

# 调整 Pod 资源限制
apiVersion: v1
kind: Pod
metadata:
  name: hello-wasm
spec:
  runtimeClassName: wasm
  containers:
    - name: app
      image: yourhub/hello-wasm:v1
      resources:
        requests:
          memory: "10Mi"  # 减少内存请求
          cpu: "50m"      # 减少 CPU 请求
        limits:
          memory: "50Mi"
          cpu: "200m"
```

**验证**：

```bash
# 重新部署 Pod
kubectl delete pod hello-wasm
kubectl apply -f hello-wasm.yaml

# 检查 Pod 状态
kubectl get pod hello-wasm
```

### 11.3.3 存储问题

**现象**：

```bash
$ kubectl get pods
# Pods 状态异常，提示存储问题
```

**根因**： sqlite 文件损坏或存储空间不足。

**解决方案**：

```bash
# 检查 sqlite 文件
sudo ls -lh /var/lib/rancher/k3s/server/db/state.db

# 备份 sqlite 文件
sudo cp /var/lib/rancher/k3s/server/db/state.db \
  /var/lib/rancher/k3s/server/db/state.db.backup

# 检查存储空间
df -h

# 清理存储空间（如果需要）
sudo k3s crictl rmi --prune

# 恢复 sqlite 文件（如果损坏）
sudo systemctl stop k3s
sudo cp /var/lib/rancher/k3s/server/db/state.db.backup \
  /var/lib/rancher/k3s/server/db/state.db
sudo systemctl start k3s
```

### 11.3.4 网络问题

**现象**：

```bash
$ kubectl get pods
# Pods 无法通信
```

**根因**： flannel 配置错误或网络插件未正确安装。

**解决方案**：

```bash
# 检查 flannel Pod
kubectl get pods -n kube-system | grep flannel

# 检查 flannel 配置
kubectl get configmap -n kube-system kube-flannel-cfg -o yaml

# 重启 flannel（如果需要）
kubectl delete pod -n kube-system -l app=flannel

# 检查 CNI 配置
ls -la /var/lib/rancher/k3s/server/manifests/
```

## 11.4 OPA Gatekeeper 相关问题

### 11.4.1 Webhook 超时

**现象**：

```bash
$ kubectl apply -f test-pod.yaml
Error: admission webhook timeout
```

**根因**：回退到 runc 或 RuntimeClass 不匹配，导致 Webhook 无法及时响应。

**解决方案**：

```bash
# 检查 RuntimeClass
kubectl get runtimeclass

# 确认 RuntimeClass 存在
kubectl get runtimeclass crun-wasm -o yaml

# 检查 Gatekeeper shim 版本
kubectl get pods -n gatekeeper-system
kubectl logs -n gatekeeper-system gatekeeper-controller-manager

# 确认 shim 版本 ≥ 1.8（支持 Wasm）
# 升级 Gatekeeper（如果需要）
helm upgrade gatekeeper gatekeeper/gatekeeper \
  --namespace gatekeeper-system \
  --set enableExternalData=true \
  --set policyEngine=wasm
```

### 11.4.2 策略更新未生效

**现象**：

```bash
# 更新策略后，策略未生效
```

**根因**： Wasm 文件被缓存，导致策略更新未生效。

**解决方案**：

```bash
# 方法 1：使用 ConfigMap 热挂载
apiVersion: v1
kind: ConfigMap
metadata:
  name: policy-wasm
  namespace: gatekeeper-system
data:
  policy.wasm: |
    # Wasm 二进制内容（base64 编码）

# 方法 2：监听 inotify（自动更新）
# 在 Gatekeeper 配置中启用 inotify 监听

# 方法 3：强制重新加载策略
kubectl delete pod -n gatekeeper-system -l app=gatekeeper
```

### 11.4.3 策略验证失败

**现象**：

```bash
$ kubectl apply -f test-pod.yaml
Error: admission webhook denied
```

**根因**：策略配置错误或策略逻辑有问题。

**解决方案**：

```bash
# 检查策略配置
kubectl get config -n gatekeeper-system -o yaml

# 测试策略（使用 opa test）
opa test policy.rego policy_test.rego

# 检查策略日志
kubectl logs -n gatekeeper-system gatekeeper-controller-manager

# 修复策略后重新编译和部署
opa build -t wasm -e 'kubernetes/admission' policy.rego
docker build -t yourhub/policy-wasm:v2 .
docker push yourhub/policy-wasm:v2

# 更新策略镜像版本
kubectl set image -n gatekeeper-system deployment/gatekeeper-controller-manager \
  policy=yourhub/policy-wasm:v2
```

## 11.5 HPA 相关问题

### 11.5.1 HPA 基于 CPU 不触发

**现象**：

```bash
$ kubectl get hpa
NAME      REFERENCE        TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
my-hpa    Deployment/app   0%/70%    1         10        1          5m
# TARGETS 始终为 0%
```

**根因**： Wasm 运行时间片极小，CPU 采样失真，导致 HPA 无法正确收集 CPU 指标。

**解决方案**：

```yaml
# 方法 1：改用 QPS 指标（推荐）
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "100"
```

**或使用 KEDA**：

```bash
# 安装 KEDA
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda --namespace keda-system --create-namespace

# 使用 KEDA ScaledObject
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: wasm-scaledobject
spec:
  scaleTargetRef:
    name: app
  triggers:
    - type: prometheus
      metadata:
        serverAddress: http://prometheus:9090
        metricName: http_requests_per_second
        threshold: '100'
```

### 11.5.2 HPA 指标收集失败

**现象**：

```bash
$ kubectl get hpa
NAME      REFERENCE        TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
my-hpa    Deployment/app   <unknown>/70%   1         10        1          5m
# TARGETS 为 <unknown>
```

**根因**： metrics-server 未正确安装或无法收集指标。

**解决方案**：

```bash
# 检查 metrics-server
kubectl get pods -n kube-system | grep metrics-server

# 检查 metrics-server 日志
kubectl logs -n kube-system -l k8s-app=metrics-server

# 重启 metrics-server（如果需要）
kubectl delete pod -n kube-system -l k8s-app=metrics-server

# 验证指标收集
kubectl top nodes
kubectl top pods
```

## 11.6 性能相关问题

### 11.6.1 启动时间过长

**现象**：

```bash
# Pod 启动时间 > 10ms（对于 Wasm）
```

**根因**：镜像体积过大、网络延迟、资源不足。

**解决方案**：

```bash
# 检查镜像体积
docker images | grep hello-wasm

# 使用 scratch 基础镜像（零 rootfs）
cat > Dockerfile <<EOF
FROM scratch
COPY hello-wasm.wasm /hello-wasm.wasm
EOF

# 检查网络延迟
ping image-registry

# 优化 Pod 资源请求
apiVersion: v1
kind: Pod
metadata:
  name: hello-wasm
spec:
  runtimeClassName: wasm
  containers:
    - name: app
      image: yourhub/hello-wasm:v1
      resources:
        requests:
          memory: "10Mi"
          cpu: "50m"
```

### 11.6.2 内存占用过高

**现象**：

```bash
# Pod 内存占用 > 10MB（对于 Wasm）
```

**根因**： Wasm 内存配置过大、应用内存泄漏。

**解决方案**：

```bash
# 检查 Pod 内存使用
kubectl top pod hello-wasm

# 优化 Wasm 内存限制
wasmedge --max-memory-page 256 hello-wasm.wasm

# 检查应用内存泄漏（在代码中）
# 确保及时释放内存

# 调整 Pod 资源限制
apiVersion: v1
kind: Pod
metadata:
  name: hello-wasm
spec:
  runtimeClassName: wasm
  containers:
    - name: app
      image: yourhub/hello-wasm:v1
      resources:
        requests:
          memory: "10Mi"
        limits:
          memory: "50Mi"
```

## 11.7 网络相关问题

### 11.7.1 Pod 无法访问服务

**现象**：

```bash
# 在 Pod 内无法访问 Service
$ kubectl exec -it pod-name -- curl http://service-name:port
# 连接超时或拒绝连接
```

**诊断步骤**：

```bash
# 1. 检查 Service 是否存在
kubectl get svc service-name

# 2. 检查 Service 的 Endpoints
kubectl get endpoints service-name

# 3. 检查 Pod 标签是否匹配
kubectl get pods -l app=your-app-label

# 4. 检查 DNS 解析
kubectl exec -it pod-name -- nslookup service-name

# 5. 检查 CNI 插件状态
kubectl get pods -n kube-system | grep cni

# 6. 检查网络策略
kubectl get networkpolicies
```

**常见原因与解决方案**：

| 原因                   | 解决方案                               |
| ---------------------- | -------------------------------------- |
| Service 没有 Endpoints | 检查 Pod 标签是否匹配 Service selector |
| DNS 解析失败           | 检查 CoreDNS 是否正常运行              |
| NetworkPolicy 阻止     | 检查 NetworkPolicy 规则                |
| CNI 插件异常           | 重启 CNI 插件 Pod                      |

### 11.7.2 跨节点 Pod 通信失败

**现象**：

```bash
# 不同节点上的 Pod 无法互相访问
```

**诊断步骤**：

```bash
# 1. 检查节点间网络连通性
ping <node-ip>

# 2. 检查路由表
ip route show

# 3. 检查 iptables 规则
sudo iptables -L -n -v

# 4. 检查 CNI 配置
cat /etc/cni/net.d/*.conf

# 5. 检查 Flannel/Calico 状态（如果使用）
kubectl get pods -n kube-system | grep flannel
kubectl get pods -n kube-system | grep calico
```

**解决方案**：

```bash
# 如果是 Flannel，检查 VXLAN 接口
ip link show flannel.1

# 如果是 Calico，检查 BGP 状态
calicoctl node status

# 重启 CNI 插件
kubectl delete pod -n kube-system -l app=flannel
```

### 11.7.3 外部访问失败

**现象**：

```bash
# 外部无法访问 Ingress 或 LoadBalancer Service
```

**诊断步骤**：

```bash
# 1. 检查 Ingress Controller
kubectl get pods -n ingress-nginx

# 2. 检查 Ingress 资源
kubectl get ingress
kubectl describe ingress <ingress-name>

# 3. 检查 Service 类型
kubectl get svc

# 4. 检查端口映射
kubectl get svc <service-name> -o yaml

# 5. 检查防火墙规则
sudo iptables -L -n | grep <port>
```

## 11.8 存储相关问题

### 11.8.1 PVC 挂载失败

**现象**：

```bash
# Pod 无法挂载 PVC
Events:
  Warning  FailedMount  Unable to mount volumes for pod
```

**诊断步骤**：

```bash
# 1. 检查 PVC 状态
kubectl get pvc
kubectl describe pvc <pvc-name>

# 2. 检查 PV 状态
kubectl get pv
kubectl describe pv <pv-name>

# 3. 检查 StorageClass
kubectl get storageclass
kubectl describe storageclass <storageclass-name>

# 4. 检查 CSI 驱动状态
kubectl get pods -n kube-system | grep csi

# 5. 检查节点上的挂载点
kubectl debug node/<node-name> -it --image=busybox -- mount | grep volume
```

**常见原因与解决方案**：

| 原因                | 解决方案                      |
| ------------------- | ----------------------------- |
| StorageClass 不存在 | 创建或指定正确的 StorageClass |
| CSI 驱动未安装      | 安装对应的 CSI 驱动           |
| 节点资源不足        | 检查节点磁盘空间              |
| 权限问题            | 检查 ServiceAccount 权限      |

### 11.8.2 存储性能问题

**现象**：

```bash
# 读写速度慢，IO 延迟高
```

**诊断步骤**：

```bash
# 1. 检查磁盘 IO
kubectl top pod <pod-name>

# 2. 使用 iostat 检查（在节点上）
iostat -x 1

# 3. 检查存储后端性能
# 如果是本地存储，检查磁盘健康状态
smartctl -a /dev/sda

# 4. 检查文件系统类型
df -T

# 5. 检查是否有磁盘配额限制
quota -u
```

**优化建议**：

- 使用 SSD 存储
- 调整文件系统挂载选项（如 `noatime`）
- 使用本地存储类（local-path-provisioner）
- 考虑使用分布式存储（如 Ceph）

## 11.9 故障排查方法

### 11.9.1 基础故障排查步骤

**标准排查流程**：

1. **检查 Pod 状态**：`kubectl get pods`
2. **查看 Pod 事件**：`kubectl describe pod <pod-name>`
3. **查看 Pod 日志**：`kubectl logs <pod-name>`
4. **检查节点资源**：`kubectl describe node`
5. **检查系统组件**：`kubectl get pods -A`

### 11.9.2 一键诊断脚本

**创建诊断脚本**：

```bash
#!/bin/bash
# cluster-diagnosis.sh

echo "=== Cluster Status ==="
kubectl get nodes
kubectl get pods -A | grep -v Running

echo "=== Resource Usage ==="
kubectl top nodes 2>/dev/null || echo "Metrics server not available"
kubectl top pods -A 2>/dev/null | head -20

echo "=== Recent Events ==="
kubectl get events --sort-by='.lastTimestamp' | tail -20

echo "=== System Components ==="
kubectl get pods -n kube-system

echo "=== Network Check ==="
kubectl get svc -A | grep -v ClusterIP

echo "=== Storage Check ==="
kubectl get pvc -A
kubectl get pv

echo "=== DNS Check ==="
kubectl get pods -n kube-system | grep coredns
```

**使用方法**：

```bash
chmod +x cluster-diagnosis.sh
./cluster-diagnosis.sh > diagnosis.txt
```

### 11.9.3 性能问题诊断

**性能诊断流程**：

```bash
# 1. 检查资源使用情况
kubectl top nodes
kubectl top pods -A

# 2. 检查 CPU 和内存限制
kubectl describe pod <pod-name> | grep -A 5 "Limits"

# 3. 检查节点资源压力
kubectl describe node <node-name> | grep -A 10 "Allocated resources"

# 4. 使用 cAdvisor 查看详细指标（如果已安装）
# 访问 http://<node-ip>:4194

# 5. 检查慢查询或长时间运行的进程
kubectl exec -it <pod-name> -- ps aux | sort -k3 -rn | head -10
```

### 11.9.4 高级故障排查方法

对于复杂的性能问题和延迟问题，请参考：

- **[29.6 问题定位模型：横向请求链 + 纵向隔离栈](../29-isolation-stack/isolation-stack.md#296-问题定位模型横向请求链--纵向隔离栈)** -
  使用 OTLP + eBPF 进行横向和纵向联合定位
- **[29.5 快速诊断口诀](../29-isolation-stack/isolation-stack.md#295-快速诊断口诀)** -
  根据日志关键词快速定位问题层级
- **[29.6.9 eBPF 工具速查表](../29-isolation-stack/isolation-stack.md#2969-ebpf-工具速查表)** -
  eBPF 工具分类和使用方法

### 11.9.5 常用命令速查

**集群状态检查**：

```bash
# 检查集群状态
kubectl get nodes
kubectl get pods -A
kubectl cluster-info

# 检查资源使用
kubectl top nodes
kubectl top pods

# 检查事件
kubectl get events --sort-by='.lastTimestamp'
kubectl get events --field-selector type=Warning

# 检查组件日志
kubectl logs -n <namespace> <pod-name>
kubectl logs -n kube-system -l app=k3s
kubectl logs -n gatekeeper-system -l app=gatekeeper
```

**网络诊断**：

```bash
# DNS 诊断
kubectl exec -it <pod-name> -- nslookup <service-name>
kubectl exec -it <pod-name> -- dig <service-name>

# 网络连通性
kubectl exec -it <pod-name> -- ping <target-ip>
kubectl exec -it <pod-name> -- curl <url>

# 端口检查
kubectl get svc
kubectl port-forward svc/<service-name> 8080:80
```

**存储诊断**：

```bash
# PVC/PV 状态
kubectl get pvc -A
kubectl get pv
kubectl describe pvc <pvc-name>

# StorageClass
kubectl get storageclass
kubectl describe storageclass <storageclass-name>

# CSI 驱动
kubectl get pods -n kube-system | grep csi
```

**调试工具**：

```bash
# 进入 Pod 调试
kubectl exec -it <pod-name> -- /bin/sh

# 调试 Pod（临时容器）
kubectl debug <pod-name> -it --image=busybox

# 端口转发
kubectl port-forward <pod-name> 8080:80

# 查看 Pod 详细信息
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o yaml
```

## 11.10 故障排查检查清单

### 11.10.1 WasmEdge 故障排查清单

**WasmEdge 问题快速检查**：

| 检查项            | 命令/方法                                           | 预期结果     | 问题处理          |
| ----------------- | --------------------------------------------------- | ------------ | ----------------- |
| **crun 版本**     | `crun --version`                                    | ≥ 1.8.5      | 升级 crun         |
| **WasmEdge 镜像** | `kubectl describe pod <pod>`                        | 镜像拉取成功 | 检查镜像仓库      |
| **RuntimeClass**  | `kubectl get runtimeclass wasm`                     | wasm 存在    | 创建 RuntimeClass |
| **Pod 日志**      | `kubectl logs <pod>`                                | 有日志输出   | 检查 crun 版本    |
| **DNS 解析**      | `kubectl exec <pod> -- nslookup kubernetes.default` | 解析成功     | 检查 CoreDNS      |
| **资源限制**      | `kubectl describe pod <pod>`                        | 资源充足     | 调整资源限制      |

### 11.10.2 K3s 故障排查清单

**K3s 问题快速检查**：

| 检查项         | 命令/方法                                            | 预期结果        | 问题处理        |
| -------------- | ---------------------------------------------------- | --------------- | --------------- |
| **节点状态**   | `kubectl get nodes`                                  | Ready           | 检查节点连接    |
| **Pod 状态**   | `kubectl get pods -A`                                | Running/Pending | 查看 Pod 事件   |
| **系统组件**   | `kubectl get pods -n kube-system`                    | 所有 Running    | 重启异常组件    |
| **网络插件**   | `kubectl get pods -n kube-system \| grep flannel`    | Running         | 检查 CNI 配置   |
| **存储插件**   | `kubectl get pods -n kube-system \| grep local-path` | Running         | 检查存储配置    |
| **API Server** | `kubectl cluster-info`                               | 正常响应        | 检查 API Server |

### 11.10.3 OPA Gatekeeper 故障排查清单

**OPA Gatekeeper 问题快速检查**：

| 检查项              | 命令/方法                                                               | 预期结果      | 问题处理        |
| ------------------- | ----------------------------------------------------------------------- | ------------- | --------------- |
| **Gatekeeper 状态** | `kubectl get pods -n gatekeeper-system`                                 | Running       | 检查 Gatekeeper |
| **Webhook 状态**    | `kubectl get validatingwebhookconfigurations`                           | Active        | 检查 Webhook    |
| **策略状态**        | `kubectl get constraints`                                               | 所有 Enforced | 检查策略配置    |
| **策略模板**        | `kubectl get constrainttemplates`                                       | 所有 Ready    | 检查模板定义    |
| **Webhook 超时**    | `kubectl describe pod <pod>`                                            | 无超时错误    | 增加超时时间    |
| **策略日志**        | `kubectl logs -n gatekeeper-system -l control-plane=controller-manager` | 无错误        | 检查策略语法    |

### 11.10.4 综合故障排查清单

**通用故障排查流程**：

1. **环境检查**：

   - [ ] K3s 版本 ≥ 1.28
   - [ ] crun 版本 ≥ 1.8.5
   - [ ] containerd 正常运行
   - [ ] 节点资源充足

2. **网络检查**：

   - [ ] CoreDNS 正常运行
   - [ ] CNI 插件正常
   - [ ] 节点间网络连通
   - [ ] Service DNS 解析正常

3. **存储检查**：

   - [ ] StorageClass 存在
   - [ ] CSI 驱动正常
   - [ ] PVC 绑定成功
   - [ ] 存储空间充足

4. **策略检查**：

   - [ ] Gatekeeper 运行正常
   - [ ] Webhook 配置正确
   - [ ] 策略语法正确
   - [ ] 策略已生效

5. **性能检查**：
   - [ ] Pod 启动时间正常
   - [ ] 内存占用合理
   - [ ] CPU 使用正常
   - [ ] 网络延迟正常

---

## 11.11 故障排查与概念关系矩阵

### 11.11.1 使用概念关系矩阵定位问题

**概念关系矩阵在故障排查中的应用**：

参考
[30. 概念关系矩阵](../30-concept-relations-matrix/concept-relations-matrix.md)
进行故障定位：

**步骤 1：确定问题域**:

根据问题现象确定涉及的概念（参考 30.19.1 概念索引）。

**步骤 2：查询依赖链**:

使用 30.7.3 依赖关系图谱定位依赖链问题。

**步骤 3：检查属性传递**:

使用 30.15 关系属性传递分析检查属性传递是否异常。

**步骤 4：验证演进兼容**:

使用 30.16 动态演进分析检查技术演进是否兼容。

**示例**：性能问题定位

```text
1. 问题：冷启动慢
2. 概念：运行时 → WasmEdge (参考 30.19.1)
3. 依赖链：应用 → K3s → containerd → crun → WasmEdge (参考 30.7.3)
4. 属性传递：性能属性传递 → 检查组合关系 (参考 30.15.2)
5. 演进：检查是否使用最新版本（2025技术栈，参考 30.16）
```

### 11.11.2 依赖关系故障排查

**依赖关系故障排查**：

根据
[30.11.3 依赖关系传递](../30-concept-relations-matrix/concept-relations-matrix.md#30113-依赖关系传递)，
如果 A → B → C，则 A → C。

**排查步骤**：

1. **检查直接依赖**：

   ```bash
   # 检查 K3s → containerd
   systemctl status containerd
   ```

2. **检查间接依赖**：

   ```bash
   # 检查 containerd → crun
   which crun
   crun --version
   ```

3. **检查完整依赖链**：

   ```bash
   # 应用 → K3s → containerd → crun → WasmEdge
   kubectl get nodes
   kubectl get pods -n kube-system | grep containerd
   crun --version
   kubectl get runtimeclass wasm
   ```

### 11.11.3 属性传递故障排查

**属性传递故障排查**：

根据
[30.15 关系属性传递分析](../30-concept-relations-matrix/concept-relations-matrix.md#3015-关系属性传递分析)：

**性能属性传递**：

```text
K3s(性能=4) ∘ WasmEdge(性能=5) = 边缘Wasm编排(性能=5)
```

如果性能未达到预期，检查：

1. **组件性能**：

   ```bash
   # 检查 K3s 性能
   kubectl top nodes

   # 检查 WasmEdge 性能
   kubectl exec <wasm-pod> -- time wasmtime run <wasm-file>
   ```

2. **组合关系**：

   ```bash
   # 检查 RuntimeClass 配置
   kubectl get runtimeclass wasm -o yaml
   ```

**安全属性传递**：

```text
应用层 → K3s → containerd → crun → WasmEdge
```

如果安全属性未达到预期，检查：

1. **各层安全配置**：

   ```bash
   # 检查 K3s RBAC
   kubectl get clusterrolebindings

   # 检查 NetworkPolicy
   kubectl get networkpolicies -A

   # 检查 Pod Security
   kubectl get pod -o json | jq '.spec.securityContext'
   ```

---

## 11.12 参考

**关联文档**：

**概念关系矩阵**：

- **[30. 概念关系矩阵](../30-concept-relations-matrix/concept-relations-matrix.md)** -
  技术堆栈概念关系梳理
  - **[文档目录](../30-concept-relations-matrix/README.md)** - 完整的文档结构说
    明和快速导航
  - **[独立文档目录](../30-concept-relations-matrix/README.md#2-文档列表)** - 27
    个独立文档目录（关系矩阵、关系图谱、属性矩阵、应用案例、决策树、分析部分、快
    速参考）
  - **[关系矩阵](../30-concept-relations-matrix/matrices/)** - 3 个独立文档（二
    维、三维、多维关系矩阵）
  - **[关系图谱](../30-concept-relations-matrix/graphs/)** - 4 个独立文档（包含
    、组合、依赖、实现关系图谱）
  - **[属性矩阵](../30-concept-relations-matrix/properties/)** - 4 个独立文档（
    性能、安全、可扩展性、可观测性属性矩阵）
  - **[应用案例](../30-concept-relations-matrix/applications/)** - 4 个独立文档
    （边缘计算、AI 推理、Serverless、微服务场景）
  - **[决策树](../30-concept-relations-matrix/decision-trees/)** - 3 个独立文档
    （运行时、编排平台、策略引擎选型决策）
  - **[分析部分](../30-concept-relations-matrix/analysis/)** - 6 个独立文档（结
    构关系、属性传递、动态演进、范畴论、传递规则、形式化定义）
  - **[快速参考](../30-concept-relations-matrix/reference/)** - 3 个独立文档（快
    速参考指南、概念索引、隔离层次对比）
  - [30.19.1 核心概念索引](../30-concept-relations-matrix/concept-relations-matrix.md#30191-核心概念索引) -
    快速查找概念
  - [30.20.3 问题定位使用](../30-concept-relations-matrix/concept-relations-matrix.md#30203-问题定位使用) -
    使用概念关系矩阵定位问题
  - [30.7.3 依赖关系图谱](../30-concept-relations-matrix/concept-relations-matrix.md#3073-依赖关系图谱) -
    依赖关系可视化
  - [30.15 关系属性传递分析](../30-concept-relations-matrix/concept-relations-matrix.md#3015-关系属性传递分析) -
    属性传递检查

**高级故障排查方法**：

- **[29. 隔离栈 - 问题定位模型](../29-isolation-stack/isolation-stack.md#296-问题定位模型横向请求链--纵向隔离栈)** -
  横纵耦合的问题定位方法，OTLP + eBPF 联合定位
  - [定位模型概述](../29-isolation-stack/isolation-stack.md#2961-定位模型概述) -
    横纵耦合定位的核心思想
  - [五步定位法](../29-isolation-stack/isolation-stack.md#2963-五步定位法) - 详
    细的问题定位流程
  - [eBPF 工具速查表](../29-isolation-stack/isolation-stack.md#2969-ebpf-工具速查表) -
    工具分类和使用方法
  - [网络定位专题](../29-isolation-stack/isolation-stack.md#29612-网络定位专题横向生命线) -
    网络问题定位方法
  - [实战案例总结](../29-isolation-stack/isolation-stack.md#29613-实战案例总结) -
    3 个完整实战案例
- **[29. 隔离栈 - 快速诊断口诀](../29-isolation-stack/isolation-stack.md#295-快速诊断口诀)** -
  根据日志关键词快速定位问题层级
- **[29. 隔离栈 - 观测系统作为第四大基础设施](../29-isolation-stack/isolation-stack.md#2960-观测系统作为第四大基础设施)** -
  为什么观测系统必须，完备性判据，MVP 落地
- **[隔离层次对比文档 - 故障排查快速参考](../29-isolation-stack/layers/isolation-comparison.md#10-故障排查快速参考)** -
  诊断命令速查、日志关键词定位、性能问题排查

**隔离栈相关文档**：

- **[29. 隔离栈](../29-isolation-stack/isolation-stack.md)** - 完整的隔离栈技术
  解析
  - **[文档目录](../29-isolation-stack/README.md)** - 完整的文档结构说明和快速导
    航
  - **[问题定位模型文档目录](../29-isolation-stack/troubleshooting/README.md)** -
    问题定位模型独立文档目录
- **[L-3 容器化层](../29-isolation-stack/layers/L-3-containerization.md)** - 容
  器故障排查相关内容
- **[L-4 沙盒化层](../29-isolation-stack/layers/L-4-sandboxing.md)** - WASM 故障
  排查相关内容
- **[隔离层次对比文档](../29-isolation-stack/layers/isolation-comparison.md)** -
  故障排查快速参考和常见问题 FAQ

**技术规范**：

> 完整参考列表见 [REFERENCES.md](../REFERENCES.md)

---

> **重要提示**：对于复杂的性能问题和延迟问题，强烈建议使用
> [29. 隔离栈的问题定位模型](../29-isolation-stack/isolation-stack.md#296-问题定位模型横向请求链--纵向隔离栈)
> 进行横纵耦合定位。

---

### 11.12.1 虚拟化与容器化对比分析

- **[虚拟化与容器化网络对比分析](../12-network-stack/virtualization-comparison.md)** -
  网络技术对比、性能分析、故障排查参考
- **[虚拟化与容器化存储对比分析](../15-storage-stack/virtualization-comparison.md)** -
  存储技术对比、性能分析、故障排查参考

### 11.12.2 eBPF 技术堆栈相关文档

- **[31. eBPF 技术堆栈](../31-ebpf-stack/ebpf-stack.md)** - eBPF 内核可编程技术
  堆栈
  - eBPF 工具生态和故障排查应用
  - 网络、可观测性、安全等场景的 eBPF 应用（2025-11-07）

**最后更新**：2025-11-07 **维护者**：项目团队
