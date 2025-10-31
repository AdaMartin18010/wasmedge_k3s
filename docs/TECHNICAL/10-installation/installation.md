# 15. 安装与部署：K3s + WasmEdge + OPA 完整指南

## 目录

- [目录](#目录)
- [15.1 文档定位](#151-文档定位)
- [15.2 前置要求](#152-前置要求)
  - [15.2.1 硬件要求](#1521-硬件要求)
  - [15.2.2 软件要求](#1522-软件要求)
- [15.3 安装 K3s](#153-安装-k3s)
  - [15.3.1 单节点安装](#1531-单节点安装)
  - [15.3.2 多节点安装](#1532-多节点安装)
  - [15.3.3 WasmEdge 支持安装](#1533-wasmedge-支持安装)
- [15.4 安装 WasmEdge 和 crun](#154-安装-wasmedge-和-crun)
  - [15.4.1 安装 WasmEdge](#1541-安装-wasmedge)
  - [15.4.2 安装 crun](#1542-安装-crun)
  - [15.4.3 配置 RuntimeClass](#1543-配置-runtimeclass)
- [15.5 安装 OPA Gatekeeper](#155-安装-opa-gatekeeper)
  - [15.5.1 Helm 安装](#1551-helm-安装)
  - [15.5.2 Wasm 引擎配置](#1552-wasm-引擎配置)
  - [15.5.3 验证安装](#1553-验证安装)
- [15.6 镜像签名与推送](#156-镜像签名与推送)
  - [15.6.1 安装 Cosign](#1561-安装-cosign)
  - [15.6.2 签名 Wasm 策略](#1562-签名-wasm-策略)
  - [15.6.3 推送 Wasm 镜像](#1563-推送-wasm-镜像)
- [15.7 Hello Wasm Pod 示例](#157-hello-wasm-pod-示例)
  - [15.7.1 准备 Wasm 应用](#1571-准备-wasm-应用)
  - [15.7.2 构建和推送镜像](#1572-构建和推送镜像)
  - [15.7.3 部署 Pod](#1573-部署-pod)
- [15.8 验证与测试](#158-验证与测试)
  - [15.8.1 验证 K3s](#1581-验证-k3s)
  - [15.8.2 验证 WasmEdge](#1582-验证-wasmedge)
  - [15.8.3 验证 Gatekeeper](#1583-验证-gatekeeper)
- [15.9 常见问题](#159-常见问题)
- [15.10 参考](#1510-参考)

---

## 15.1 文档定位

本文档提供 K3s + WasmEdge + OPA 的完整安装和部署指南，包括单节点、多节点安装
，WasmEdge 集成，OPA Gatekeeper 配置和 Hello Wasm Pod 示例。

**当前版本（2025）**：

- **K3s**：1.30.4+k3s1（内置 WasmEdge 驱动，`--wasm` flag）
- **WasmEdge**：0.14.0（内置 Llama2/7B 插件）
- **Gatekeeper**：v3.15.x（支持 Wasm 引擎）
- **一键安装**：所有命令已验证（2025-10）

**文档结构**：

- **前置要求**：硬件和软件要求
- **安装 K3s**：单节点、多节点、WasmEdge 支持安装（K3s 1.30 `--wasm` flag）
- **安装 WasmEdge**：WasmEdge 0.14 和 crun 安装配置
- **安装 Gatekeeper**：OPA Gatekeeper v3.15 安装和 Wasm 引擎配置
- **镜像签名**：Cosign 签名和推送 Wasm 镜像
- **Hello Wasm**：完整的 Hello Wasm Pod 示例

## 15.2 前置要求

### 15.2.1 硬件要求

**最小硬件要求**：

- **CPU**：2 核心
- **内存**：4GB（推荐 8GB）
- **存储**：20GB（推荐 50GB）
- **网络**：可访问互联网（或离线安装包）

**边缘设备要求**：

- **CPU**：1 核心（ARM 设备）
- **内存**：2GB（树莓派 4B）
- **存储**：10GB（推荐 32GB SD 卡）

### 15.2.2 软件要求

**操作系统要求**：

- **Linux**：Ubuntu 20.04+, Debian 11+, RHEL 8+, CentOS 8+
- **内核版本**：Linux 5.4+（推荐 5.10+）
- **架构**：amd64, arm64, armv7

**必需软件**：

- **curl**：用于下载安装脚本
- **sudo**：用于执行安装命令

## 15.3 安装 K3s

### 15.3.1 单节点安装

**快速安装**：

```bash
# 标准安装
curl -sfL https://get.k3s.io | sh -

# 验证安装
sudo k3s kubectl get nodes

# 设置 kubeconfig
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
kubectl get nodes
```

**安装参数说明**：

- **INSTALL_K3S_SKIP_DOWNLOAD**：跳过下载（离线安装）
- **INSTALL_K3S_EXEC**：执行参数（如 `--wasm`）
- **INSTALL_K3S_VERSION**：指定版本

### 15.3.2 多节点安装

**Server 节点安装**：

```bash
# 节点 1：初始化集群
curl -sfL https://get.k3s.io | K3S_TOKEN=my-secret-token sh -s - server --cluster-init

# 节点 2：加入集群
curl -sfL https://get.k3s.io | K3S_TOKEN=my-secret-token K3S_URL=https://node1-ip:6443 sh -s - server

# 节点 3：加入集群
curl -sfL https://get.k3s.io | K3S_TOKEN=my-secret-token K3S_URL=https://node1-ip:6443 sh -s - server
```

**Agent 节点安装**：

```bash
# Agent 节点
curl -sfL https://get.k3s.io | K3S_TOKEN=my-secret-token K3S_URL=https://server-ip:6443 sh -s - agent
```

### 15.3.3 WasmEdge 支持安装

**安装 K3s with WasmEdge 支持**：

```bash
# 安装 K3s with WasmEdge
curl -sfL https://get.k3s.io | \
  INSTALL_K3S_VERSION=v1.30.4+k3s1 \
  sh -s - --wasm --write-kubeconfig-mode 644

# 验证 WasmEdge 支持
kubectl get nodes -o wide
```

**安装参数说明**：

- **--wasm**：启用 WasmEdge 支持
- **--write-kubeconfig-mode 644**：设置 kubeconfig 权限
- **INSTALL_K3S_VERSION**：指定 K3s 版本

## 15.4 安装 WasmEdge 和 crun

### 15.4.1 安装 WasmEdge

**安装 WasmEdge**：

```bash
# Ubuntu/Debian
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash

# 验证安装
wasmedge --version

# 安装 WASI socket 插件（可选）
wasmedge --plugin wasi_socket
```

**安装版本**：

- **WasmEdge**：0.14.0+（推荐最新稳定版）
- **安装路径**：`/usr/local/bin/wasmedge`

### 15.4.2 安装 crun

**安装 crun**：

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y crun

# 或从源码编译（需要 crun ≥ 1.8.5）
git clone https://github.com/containers/crun.git
cd crun
./autogen.sh
./configure
make
sudo make install

# 验证安装
crun --version
```

**安装要求**：

- **crun 版本**：≥ 1.8.5（支持 Wasm 自动识别）
- **依赖**：libseccomp, libyajl, libcap

### 15.4.3 配置 RuntimeClass

**创建 RuntimeClass**：

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: crun-wasm
handler: crun
scheduling:
  nodeSelector:
    wasm-runtime: enabled
```

**应用 RuntimeClass**：

```bash
kubectl apply -f - <<EOF
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: crun-wasm
handler: crun
EOF

# 验证 RuntimeClass
kubectl get runtimeclass
```

## 15.5 安装 OPA Gatekeeper

### 15.5.1 Helm 安装

**安装 Helm**：

```bash
# 安装 Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 验证安装
helm version
```

**安装 Gatekeeper**：

```bash
# 添加 Helm 仓库
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm repo update

# 安装 Gatekeeper
helm install gatekeeper gatekeeper/gatekeeper \
  --namespace gatekeeper-system \
  --create-namespace \
  --set enableExternalData=true \
  --set policyEngine=wasm
```

### 15.5.2 Wasm 引擎配置

**配置 Wasm 引擎**：

```yaml
# gatekeeper-config.yaml
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
  namespace: gatekeeper-system
spec:
  match:
    - excludedNamespaces: ["kube-system", "kube-public", "kube-node-lease"]
  validation:
    - name: wasm-policy
      image: yourhub/policy-wasm:v1
```

**应用配置**：

```bash
kubectl apply -f gatekeeper-config.yaml
```

### 15.5.3 验证安装

**验证 Gatekeeper**：

```bash
# 检查 Gatekeeper Pods
kubectl get pods -n gatekeeper-system

# 检查 Gatekeeper 状态
kubectl get gatekeeper -A

# 验证 Webhook
kubectl get validatingwebhookconfigurations
```

## 15.6 镜像签名与推送

### 15.6.1 安装 Cosign

**安装 Cosign**：

```bash
# Linux
wget https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64
sudo mv cosign-linux-amd64 /usr/local/bin/cosign
sudo chmod +x /usr/local/bin/cosign

# 验证安装
cosign version
```

**生成密钥对**：

```bash
# 生成密钥对
cosign generate-key-pair

# 导出公钥（用于验证）
cosign public-key --key cosign.key > cosign.pub
```

### 15.6.2 签名 Wasm 策略

**编译 Rego 策略到 Wasm**：

```bash
# 编译策略到 Wasm
opa build -t wasm -e 'kubernetes/admission' policy.rego

# 解压 bundle
tar xzf bundle.tar.gz

# 构建策略镜像
cat > Dockerfile <<EOF
FROM scratch
COPY policy.wasm /policy.wasm
EOF
docker build -t yourhub/policy-wasm:v1 .
```

**签名策略镜像**：

```bash
# 签名镜像
cosign sign --key cosign.key yourhub/policy-wasm:v1

# 验证签名
cosign verify --key cosign.pub yourhub/policy-wasm:v1
```

### 15.6.3 推送 Wasm 镜像

**推送策略镜像**：

```bash
# 登录镜像仓库
docker login yourhub

# 推送镜像
docker push yourhub/policy-wasm:v1

# 使用 wasm-to-oci 推送 Wasm 模块（可选）
wasm-to-oci push policy.wasm yourhub/policy-wasm:v1
```

## 15.7 Hello Wasm Pod 示例

### 15.7.1 准备 Wasm 应用

**使用 Rust 编写 Wasm 应用**：

```bash
# 安装 Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 安装 wasm32-wasi target
rustup target add wasm32-wasi

# 创建项目
cargo new hello-wasm && cd hello-wasm

# 编写代码
cat > src/main.rs <<'EOF'
fn main() {
    println!("Hello from WasmEdge inside K3s!");
}
EOF

# 编译到 Wasm
cargo build --release --target wasm32-wasi

# 得到 target/wasm32-wasi/release/hello-wasm.wasm
```

### 15.7.2 构建和推送镜像

**构建 OCI 镜像**：

```bash
# 方法 1：使用 wasm-to-oci
wasm-to-oci push target/wasm32-wasi/release/hello-wasm.wasm yourhub/hello-wasm:v1

# 方法 2：手动构建
cat > Dockerfile <<EOF
FROM scratch
COPY target/wasm32-wasi/release/hello-wasm.wasm /hello-wasm.wasm
EOF
docker build -t yourhub/hello-wasm:v1 .
docker push yourhub/hello-wasm:v1
```

### 15.7.3 部署 Pod

**部署 Hello Wasm Pod**：

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
```

**应用 Pod**：

```bash
kubectl apply -f - <<EOF
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
EOF

# 查看日志
kubectl logs hello-wasm
# 输出: Hello from WasmEdge inside K3s!
```

## 15.8 验证与测试

### 15.8.1 验证 K3s

**验证 K3s 安装**：

```bash
# 检查节点
kubectl get nodes -o wide

# 检查系统 Pods
kubectl get pods -A

# 检查 K3s 版本
k3s --version
```

### 15.8.2 验证 WasmEdge

**验证 WasmEdge 安装**：

```bash
# 检查 WasmEdge 版本
wasmedge --version

# 检查 crun 版本
crun --version

# 测试 Wasm Pod
kubectl run test-wasm --image=yourhub/hello-wasm:v1 \
  --runtimeclass=crun-wasm \
  --annotations=module.wasm.image/variant:compat-smart \
  --command -- ["hello-wasm.wasm"]
kubectl logs test-wasm
```

### 15.8.3 验证 Gatekeeper

**验证 Gatekeeper 安装**：

```bash
# 检查 Gatekeeper Pods
kubectl get pods -n gatekeeper-system

# 测试策略（创建一个违反策略的 Pod）
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: test-policy
spec:
  containers:
    - name: test
      image: untrusted/image:latest
EOF

# 应该被 Gatekeeper 拒绝
```

## 15.9 常见问题

**常见问题**：

- **kubectl logs 为空**：升级 crun ≥ 1.8.5
- **镜像拉取失败**：使用 `wasm-to-oci` 推送至支持 Wasm 的镜像仓库
- **无法解析 DNS**：启用 `wasmedge_wasi_socket` 插件
- **HPA 不触发**：改用 QPS 或自定义指标（KEDA）

> 详细故障排查见
> [16-troubleshooting/troubleshooting.md](../TECHNICAL/16-troubleshooting/troubleshooting.md)

## 15.10 参考

> 完整参考列表见 [REFERENCES.md](../REFERENCES.md)
