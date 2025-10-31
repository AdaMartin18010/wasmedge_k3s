# 16. 故障排查：常见问题与解决方案

## 目录

- [目录](#目录)
- [16.1 文档定位](#161-文档定位)
- [16.2 WasmEdge 相关问题](#162-wasmedge-相关问题)
  - [16.2.1 kubectl logs 为空](#1621-kubectl-logs-为空)
  - [16.2.2 镜像拉取失败](#1622-镜像拉取失败)
  - [16.2.3 无法解析 DNS](#1623-无法解析-dns)
  - [16.2.4 WasmEdge "out of bounds" 错误](#1624-wasmedge-out-of-bounds-错误)
- [16.3 K3s 相关问题](#163-k3s-相关问题)
  - [16.3.1 节点无法加入](#1631-节点无法加入)
  - [16.3.2 Pod 无法启动](#1632-pod-无法启动)
  - [16.3.3 存储问题](#1633-存储问题)
  - [16.3.4 网络问题](#1634-网络问题)
- [16.4 OPA Gatekeeper 相关问题](#164-opa-gatekeeper-相关问题)
  - [16.4.1 Webhook 超时](#1641-webhook-超时)
  - [16.4.2 策略更新未生效](#1642-策略更新未生效)
  - [16.4.3 策略验证失败](#1643-策略验证失败)
- [16.5 HPA 相关问题](#165-hpa-相关问题)
  - [16.5.1 HPA 基于 CPU 不触发](#1651-hpa-基于-cpu-不触发)
  - [16.5.2 HPA 指标收集失败](#1652-hpa-指标收集失败)
- [16.6 性能相关问题](#166-性能相关问题)
  - [16.6.1 启动时间过长](#1661-启动时间过长)
  - [16.6.2 内存占用过高](#1662-内存占用过高)
- [16.7 故障排查方法](#167-故障排查方法)
- [16.8 参考](#168-参考)

---

## 16.1 文档定位

本文档提供 K3s + WasmEdge + OPA 常见问题的排查和解决方案，包括
WasmEdge、K3s、OPA Gatekeeper、HPA 和性能相关问题的诊断和修复。

**文档结构**：

- **WasmEdge 问题**：kubectl logs 为空、镜像拉取失败、DNS 解析失败等
- **K3s 问题**：节点无法加入、Pod 无法启动、存储网络问题等
- **OPA Gatekeeper 问题**：Webhook 超时、策略更新未生效等
- **HPA 问题**：HPA 不触发、指标收集失败等
- **性能问题**：启动时间、内存占用等性能问题

## 16.2 WasmEdge 相关问题

### 16.2.1 kubectl logs 为空

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

### 16.2.2 镜像拉取失败

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

### 16.2.3 无法解析 DNS

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
  runtimeClassName: crun-wasm
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

### 16.2.4 WasmEdge "out of bounds" 错误

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
  runtimeClassName: crun-wasm
  containers:
    - name: app
      image: yourhub/hello-wasm:v1
      resources:
        limits:
          memory: "100Mi"
        requests:
          memory: "50Mi"
```

## 16.3 K3s 相关问题

### 16.3.1 节点无法加入

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

### 16.3.2 Pod 无法启动

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
  runtimeClassName: crun-wasm
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

### 16.3.3 存储问题

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

### 16.3.4 网络问题

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

## 16.4 OPA Gatekeeper 相关问题

### 16.4.1 Webhook 超时

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

### 16.4.2 策略更新未生效

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

### 16.4.3 策略验证失败

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

## 16.5 HPA 相关问题

### 16.5.1 HPA 基于 CPU 不触发

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

### 16.5.2 HPA 指标收集失败

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

## 16.6 性能相关问题

### 16.6.1 启动时间过长

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
  runtimeClassName: crun-wasm
  containers:
    - name: app
      image: yourhub/hello-wasm:v1
      resources:
        requests:
          memory: "10Mi"
          cpu: "50m"
```

### 16.6.2 内存占用过高

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
  runtimeClassName: crun-wasm
  containers:
    - name: app
      image: yourhub/hello-wasm:v1
      resources:
        requests:
          memory: "10Mi"
        limits:
          memory: "50Mi"
```

## 16.7 故障排查方法

**故障排查步骤**：

1. **检查 Pod 状态**：`kubectl get pods`
2. **查看 Pod 事件**：`kubectl describe pod <pod-name>`
3. **查看 Pod 日志**：`kubectl logs <pod-name>`
4. **检查节点资源**：`kubectl describe node`
5. **检查系统组件**：`kubectl get pods -A`
6. **查看组件日志**：`kubectl logs -n <namespace> <pod-name>`

**常用命令**：

```bash
# 检查集群状态
kubectl get nodes
kubectl get pods -A

# 检查资源使用
kubectl top nodes
kubectl top pods

# 检查事件
kubectl get events --sort-by='.lastTimestamp'

# 检查组件日志
kubectl logs -n kube-system -l app=k3s
kubectl logs -n gatekeeper-system -l app=gatekeeper
```

## 16.8 参考

> 完整参考列表见 [REFERENCES.md](../REFERENCES.md)

---

> **重要提示**：如果问题仍未解决，请查看相关技术文档或提交 Issue。
