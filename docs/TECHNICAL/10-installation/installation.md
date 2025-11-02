# 10. 安装与部署：K3s + WasmEdge + OPA 完整指南

## 目录

- [目录](#目录)
- [10.1 文档定位](#101-文档定位)
- [10.2 前置要求](#102-前置要求)
  - [10.2.1 硬件要求](#1021-硬件要求)
  - [10.2.2 软件要求](#1022-软件要求)
- [10.3 安装 K3s](#103-安装-k3s)
  - [10.3.1 单节点安装](#1031-单节点安装)
  - [10.3.2 多节点安装](#1032-多节点安装)
  - [10.3.3 WasmEdge 支持安装](#1033-wasmedge-支持安装)
- [10.4 安装 WasmEdge 和 crun](#104-安装-wasmedge-和-crun)
  - [10.4.1 安装 WasmEdge](#1041-安装-wasmedge)
  - [10.4.2 安装 crun](#1042-安装-crun)
  - [10.4.3 配置 RuntimeClass](#1043-配置-runtimeclass)
- [10.5 安装 OPA Gatekeeper](#105-安装-opa-gatekeeper)
  - [10.5.1 Helm 安装](#1051-helm-安装)
  - [10.5.2 Wasm 引擎配置](#1052-wasm-引擎配置)
  - [10.5.3 验证安装](#1053-验证安装)
- [10.6 镜像签名与推送](#106-镜像签名与推送)
  - [10.6.1 安装 Cosign](#1061-安装-cosign)
  - [10.6.2 签名 Wasm 策略](#1062-签名-wasm-策略)
  - [10.6.3 推送 Wasm 镜像](#1063-推送-wasm-镜像)
- [10.7 Hello Wasm Pod 示例](#107-hello-wasm-pod-示例)
  - [10.7.1 准备 Wasm 应用](#1071-准备-wasm-应用)
  - [10.7.2 构建和推送镜像](#1072-构建和推送镜像)
  - [10.7.3 部署 Pod](#1073-部署-pod)
- [10.8 验证与测试](#108-验证与测试)
  - [10.8.1 验证 K3s](#1081-验证-k3s)
  - [10.8.2 验证 WasmEdge](#1082-验证-wasmedge)
  - [10.8.3 验证 Gatekeeper](#1083-验证-gatekeeper)
- [10.9 常见问题](#109-常见问题)
- [10.10 参考](#1010-参考)

---

## 10.1 文档定位

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

## 10.2 前置要求

### 10.2.1 硬件要求

**最小硬件要求**：

- **CPU**：2 核心
- **内存**：4GB（推荐 8GB）
- **存储**：20GB（推荐 50GB）
- **网络**：可访问互联网（或离线安装包）

**边缘设备要求**：

- **CPU**：1 核心（ARM 设备）
- **内存**：2GB（树莓派 4B）
- **存储**：10GB（推荐 32GB SD 卡）

### 10.2.2 软件要求

**操作系统要求**：

- **Linux**：Ubuntu 20.04+, Debian 11+, RHEL 8+, CentOS 8+
- **内核版本**：Linux 5.4+（推荐 5.10+）
- **架构**：amd64, arm64, armv7

**必需软件**：

- **curl**：用于下载安装脚本
- **sudo**：用于执行安装命令

## 10.3 安装 K3s

### 10.3.1 单节点安装

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

### 10.3.2 多节点安装

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

### 10.3.3 WasmEdge 支持安装

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

## 10.4 安装 WasmEdge 和 crun

### 10.4.1 安装 WasmEdge

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

### 10.4.2 安装 crun

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

### 10.4.3 配置 RuntimeClass

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

## 10.5 安装 OPA Gatekeeper

### 10.5.1 Helm 安装

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

### 10.5.2 Wasm 引擎配置

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

### 10.5.3 验证安装

**验证 Gatekeeper**：

```bash
# 检查 Gatekeeper Pods
kubectl get pods -n gatekeeper-system

# 检查 Gatekeeper 状态
kubectl get gatekeeper -A

# 验证 Webhook
kubectl get validatingwebhookconfigurations
```

## 10.6 镜像签名与推送

### 10.6.1 安装 Cosign

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

### 10.6.2 签名 Wasm 策略

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

### 10.6.3 推送 Wasm 镜像

**推送策略镜像**：

```bash
# 登录镜像仓库
docker login yourhub

# 推送镜像
docker push yourhub/policy-wasm:v1

# 使用 wasm-to-oci 推送 Wasm 模块（可选）
wasm-to-oci push policy.wasm yourhub/policy-wasm:v1
```

## 10.7 Hello Wasm Pod 示例

### 10.7.1 准备 Wasm 应用

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

### 10.7.2 构建和推送镜像

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

### 10.7.3 部署 Pod

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

## 10.8 验证与测试

### 10.8.1 验证 K3s

**验证 K3s 安装**：

```bash
# 检查节点
kubectl get nodes -o wide

# 检查系统 Pods
kubectl get pods -A

# 检查 K3s 版本
k3s --version
```

### 10.8.2 验证 WasmEdge

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

### 10.8.3 验证 Gatekeeper

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

## 10.9 常见问题

**常见问题**：

- **kubectl logs 为空**：升级 crun ≥ 1.8.5
- **镜像拉取失败**：使用 `wasm-to-oci` 推送至支持 Wasm 的镜像仓库
- **无法解析 DNS**：启用 `wasmedge_wasi_socket` 插件
- **HPA 不触发**：改用 QPS 或自定义指标（KEDA）

> 详细故障排查见
> [16-troubleshooting/troubleshooting.md](../TECHNICAL/16-troubleshooting/troubleshooting.md)

## 10.10 参考

**关联文档**：

- **[10. 技术决策模型](../../COGNITIVE/10-decision-models/decision-models.md)** -
  技术选型决策框架
- **[10. 快速参考指南](../../COGNITIVE/10-decision-models/QUICK-REFERENCE.md)** -
  设备访问（USB/PCI/GPU）和内核特性决策快速参考
- **[10. 一致性检查报告](../../COGNITIVE/10-decision-models/CONSISTENCY-REPORT.md)** -
  文档一致性检查与 Wikipedia 标准对齐
- **[02. K3s](../02-k3s/k3s.md)** - K3s 轻量级架构
- **[03. WasmEdge](../03-wasm-edge/wasmedge.md)** - WasmEdge 集成指南
- **[06. OPA 策略即代码](../06-policy-opa/policy-opa.md)** - Open Policy Agent

> 完整参考列表见 [REFERENCES.md](../REFERENCES.md)

---

**最后更新**：2025-11-03 **维护者**：项目团队
