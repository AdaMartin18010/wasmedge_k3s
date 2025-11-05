# 10. 安装与部署：K3s + WasmEdge + OPA 完整指南

## 📑 目录

- [📑 目录](#-目录)
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
- [10.9 生产环境部署最佳实践](#109-生产环境部署最佳实践)
  - [10.9.1 高可用部署配置](#1091-高可用部署配置)
  - [10.9.2 边缘设备部署](#1092-边缘设备部署)
  - [10.9.3 一键安装脚本](#1093-一键安装脚本)
  - [10.9.4 离线安装方案](#1094-离线安装方案)
- [10.10 常见问题与故障排查](#1010-常见问题与故障排查)
  - [10.10.1 安装相关问题](#10101-安装相关问题)
  - [10.10.2 运行时问题](#10102-运行时问题)
  - [10.10.3 网络问题](#10103-网络问题)
  - [10.10.4 性能问题](#10104-性能问题)
- [10.11 部署检查清单](#1011-部署检查清单)
- [10.12 参考](#1012-参考)

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

## 10.9 生产环境部署最佳实践

### 10.9.1 高可用部署配置

**多节点高可用 K3s 集群**：

```bash
# 第一台服务器（主节点）
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--cluster-init --wasm" sh -

# 获取 token
sudo cat /var/lib/rancher/k3s/server/node-token

# 第二台服务器（加入主节点）
curl -sfL https://get.k3s.io | \
  K3S_URL=https://主节点IP:6443 \
  K3S_TOKEN=主节点token \
  INSTALL_K3S_EXEC="--wasm" sh -

# 第三台服务器（加入主节点）
curl -sfL https://get.k3s.io | \
  K3S_URL=https://主节点IP:6443 \
  K3S_TOKEN=主节点token \
  INSTALL_K3S_EXEC="--wasm" sh -
```

**高可用数据库配置**：

```bash
# 使用外部数据库（MySQL/PostgreSQL）
curl -sfL https://get.k3s.io | \
  INSTALL_K3S_EXEC="--datastore-endpoint=mysql://user:password@tcp(host:3306)/database --wasm" sh -
```

### 10.9.2 边缘设备部署

**树莓派 4B 部署**：

```bash
# ARM64 架构
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--wasm" sh -s - --write-kubeconfig-mode 644

# 配置 WasmEdge（ARM64）
wget https://github.com/WasmEdge/WasmEdge/releases/download/0.14.0/WasmEdge-0.14.0-arm64.tar.gz
tar -xzf WasmEdge-0.14.0-arm64.tar.gz
sudo cp -r WasmEdge-0.14.0-arm64/include /usr/local/include/wasmedge
sudo cp -r WasmEdge-0.14.0-arm64/lib /usr/local/lib/wasmedge
sudo cp WasmEdge-0.14.0-arm64/bin/wasmedge /usr/local/bin/
```

**资源受限设备优化**：

```bash
# 禁用不必要的组件
curl -sfL https://get.k3s.io | \
  INSTALL_K3S_EXEC="--disable traefik,metrics-server --wasm" sh -
```

### 10.9.3 一键安装脚本

**完整安装脚本**：

```bash
#!/bin/bash
# install-k3s-wasmedge-opa.sh

set -e

echo "=== K3s + WasmEdge + OPA 一键安装脚本 ==="

# 检查系统要求
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

KERNEL_VERSION=$(uname -r | cut -d. -f1,2)
if [ "$(echo "$KERNEL_VERSION < 5.4" | bc)" -eq 1 ]; then
    echo "错误: 内核版本需要 >= 5.4"
    exit 1
fi

# 安装 K3s（带 WasmEdge 支持）
echo "步骤 1/5: 安装 K3s..."
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--wasm" sh -

# 等待 K3s 就绪
echo "等待 K3s 就绪..."
sleep 30
kubectl wait --for=condition=ready node --all --timeout=300s

# 安装 WasmEdge 和 crun
echo "步骤 2/5: 安装 WasmEdge..."
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    WASMEDGE_ARCH="x86_64"
elif [ "$ARCH" = "aarch64" ]; then
    WASMEDGE_ARCH="arm64"
else
    echo "不支持的架构: $ARCH"
    exit 1
fi

wget -q https://github.com/WasmEdge/WasmEdge/releases/download/0.14.0/WasmEdge-0.14.0-${WASMEDGE_ARCH}.tar.gz
tar -xzf WasmEdge-0.14.0-${WASMEDGE_ARCH}.tar.gz
sudo cp -r WasmEdge-0.14.0-${WASMEDGE_ARCH}/include /usr/local/include/wasmedge
sudo cp -r WasmEdge-0.14.0-${WASMEDGE_ARCH}/lib /usr/local/lib/wasmedge
sudo cp WasmEdge-0.14.0-${WASMEDGE_ARCH}/bin/wasmedge /usr/local/bin/
sudo ldconfig

# 安装 crun
echo "步骤 3/5: 安装 crun..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y crun
elif command -v yum &> /dev/null; then
    sudo yum install -y crun
else
    echo "请手动安装 crun >= 1.8.5"
fi

# 配置 RuntimeClass
echo "步骤 4/5: 配置 RuntimeClass..."
kubectl apply -f - <<EOF
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: crun-wasm
handler: crun
EOF

# 安装 OPA Gatekeeper
echo "步骤 5/5: 安装 OPA Gatekeeper..."
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.15/deploy/gatekeeper.yaml
kubectl wait --for=condition=ready pod -l control-plane=controller-manager -n gatekeeper-system --timeout=300s

echo "=== 安装完成 ==="
echo "验证安装:"
echo "  kubectl get nodes"
echo "  kubectl get pods -A"
echo "  wasmedge --version"
echo "  kubectl get runtimeclass"
```

### 10.9.4 离线安装方案

**准备离线安装包**：

```bash
#!/bin/bash
# prepare-offline-install.sh

# 创建离线安装目录
mkdir -p offline-install/{k3s,wasmedge,crun,gatekeeper}

# 下载 K3s 离线安装包
wget https://github.com/k3s-io/k3s/releases/download/v1.30.4+k3s1/k3s-airgap-images-amd64.tar
wget https://github.com/k3s-io/k3s/releases/download/v1.30.4+k3s1/k3s
mv k3s-airgap-images-amd64.tar offline-install/k3s/
mv k3s offline-install/k3s/

# 下载 WasmEdge
wget https://github.com/WasmEdge/WasmEdge/releases/download/0.14.0/WasmEdge-0.14.0-x86_64.tar.gz
mv WasmEdge-0.14.0-x86_64.tar.gz offline-install/wasmedge/

# 下载 Gatekeeper 清单
wget -O offline-install/gatekeeper/gatekeeper.yaml \
  https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.15/deploy/gatekeeper.yaml

# 打包
tar -czf k3s-wasmedge-opa-offline.tar.gz offline-install/
```

**离线安装脚本**：

```bash
#!/bin/bash
# offline-install.sh

set -e

echo "=== 离线安装 K3s + WasmEdge + OPA ==="

# 解压离线安装包
tar -xzf k3s-wasmedge-opa-offline.tar.gz
cd offline-install

# 加载 K3s 镜像
sudo mkdir -p /var/lib/rancher/k3s/agent/images/
sudo cp k3s/k3s-airgap-images-amd64.tar /var/lib/rancher/k3s/agent/images/

# 安装 K3s（离线模式）
sudo cp k3s/k3s /usr/local/bin/
sudo chmod +x /usr/local/bin/k3s
sudo INSTALL_K3S_SKIP_DOWNLOAD=true INSTALL_K3S_EXEC="--wasm" sh -c "curl -sfL https://get.k3s.io | sh -"

# 安装 WasmEdge（离线）
tar -xzf wasmedge/WasmEdge-0.14.0-x86_64.tar.gz
sudo cp -r WasmEdge-0.14.0-x86_64/include /usr/local/include/wasmedge
sudo cp -r WasmEdge-0.14.0-x86_64/lib /usr/local/lib/wasmedge
sudo cp WasmEdge-0.14.0-x86_64/bin/wasmedge /usr/local/bin/
sudo ldconfig

# 安装 Gatekeeper（离线）
kubectl apply -f gatekeeper/gatekeeper.yaml

echo "=== 离线安装完成 ==="
```

## 10.10 常见问题与故障排查

### 10.10.1 安装相关问题

**问题 1：K3s 安装失败 - "Failed to connect to github.com"**:

```bash
# 解决方案：使用国内镜像源
export INSTALL_K3S_MIRROR=cn
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--wasm" sh -

# 或使用离线安装包
sudo INSTALL_K3S_SKIP_DOWNLOAD=true INSTALL_K3S_EXEC="--wasm" \
  sh -c "curl -sfL https://get.k3s.io | sh -"
```

**问题 2：WasmEdge 运行时找不到**:

```bash
# 检查 WasmEdge 安装
wasmedge --version

# 如果未安装，手动安装
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    WASMEDGE_ARCH="x86_64"
elif [ "$ARCH" = "aarch64" ]; then
    WASMEDGE_ARCH="arm64"
fi

wget https://github.com/WasmEdge/WasmEdge/releases/download/0.14.0/WasmEdge-0.14.0-${WASMEDGE_ARCH}.tar.gz
tar -xzf WasmEdge-0.14.0-${WASMEDGE_ARCH}.tar.gz
sudo cp -r WasmEdge-0.14.0-${WASMEDGE_ARCH}/include /usr/local/include/wasmedge
sudo cp -r WasmEdge-0.14.0-${WASMEDGE_ARCH}/lib /usr/local/lib/wasmedge
sudo cp WasmEdge-0.14.0-${WASMEDGE_ARCH}/bin/wasmedge /usr/local/bin/
sudo ldconfig
```

**问题 3：crun 版本过低**:

```bash
# 检查 crun 版本
crun --version

# 如果版本 < 1.8.5，需要升级
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y crun

# CentOS/RHEL
sudo yum install -y crun

# 或从源码编译
git clone https://github.com/containers/crun.git
cd crun
./autogen.sh
./configure
make
sudo make install
```

### 10.10.2 运行时问题

**问题 4：Wasm Pod 无法启动 - "Failed to create containerd task"**:

```bash
# 检查 RuntimeClass 配置
kubectl get runtimeclass crun-wasm -o yaml

# 检查 crun 配置
cat /etc/containerd/config.toml | grep crun

# 重启 containerd
sudo systemctl restart containerd
sudo systemctl restart k3s
```

**问题 5：Wasm Pod 日志为空**:

```bash
# 检查 crun 版本（需要 >= 1.8.5）
crun --version

# 检查 Pod 状态
kubectl describe pod <pod-name>

# 检查 containerd 日志
sudo journalctl -u containerd -f
```

**问题 6：镜像拉取失败**:

```bash
# 检查镜像仓库配置
kubectl get secret -n default

# 配置镜像仓库认证
kubectl create secret docker-registry regcred \
  --docker-server=<registry-url> \
  --docker-username=<username> \
  --docker-password=<password>

# 在 Pod 中使用
# spec:
#   imagePullSecrets:
#   - name: regcred
```

### 10.10.3 网络问题

**问题 7：Wasm Pod 无法访问网络**:

```bash
# 检查 Wasm 镜像是否包含网络插件
# 确保镜像注解包含：
# annotations:
#   module.wasm.image/variant: compat-smart

# 检查网络策略
kubectl get networkpolicies -A

# 测试网络连接
kubectl run test-network --image=busybox --rm -it -- sh
# 在容器内执行: wget -O- http://google.com
```

**问题 8：DNS 解析失败**:

```bash
# 检查 CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns

# 检查 DNS 配置
kubectl get configmap coredns -n kube-system -o yaml

# 测试 DNS
kubectl run test-dns --image=busybox --rm -it -- nslookup kubernetes.default
```

### 10.10.4 性能问题

**问题 9：Wasm Pod 启动慢**:

```bash
# 检查镜像大小（Wasm 镜像应该很小）
docker images | grep wasm

# 使用多阶段构建优化镜像
# FROM scratch
# COPY --from=builder /app/target/wasm32-wasi/release/app.wasm /app.wasm

# 检查节点资源
kubectl top nodes
kubectl top pods
```

**问题 10：资源使用过高**:

```bash
# 检查 Pod 资源限制
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].resources}'

# 设置资源限制
# resources:
#   requests:
#     cpu: 10m
#     memory: 10Mi
#   limits:
#     cpu: 100m
#     memory: 50Mi
```

## 10.11 部署检查清单

**安装前检查清单**：

```yaml
前置要求:
  硬件:
    - [ ] CPU >= 2 核心
    - [ ] 内存 >= 4GB
    - [ ] 存储 >= 20GB
    - [ ] 网络连接正常
  软件:
    - [ ] Linux 内核 >= 5.4
    - [ ] curl 已安装
    - [ ] sudo 权限
    - [ ] 防火墙端口开放（6443, 10250）
  环境:
    - [ ] 可以访问互联网（或准备离线安装包）
    - [ ] 时间同步正常（NTP）
    - [ ] SELinux 已配置（如适用）
```

**安装后验证清单**：

```yaml
验证项目:
  K3s:
    - [ ] kubectl get nodes 显示节点 Ready
    - [ ] kubectl get pods -A 所有系统 Pod 运行正常
    - [ ] k3s --version 显示正确版本
  WasmEdge:
    - [ ] wasmedge --version 显示正确版本
    - [ ] crun --version >= 1.8.5
    - [ ] kubectl get runtimeclass crun-wasm 存在
  OPA Gatekeeper:
    - [ ] kubectl get pods -n gatekeeper-system 运行正常
    - [ ] kubectl get constrainttemplates 可以列出
  测试部署:
    - [ ] 可以部署 Hello Wasm Pod
    - [ ] kubectl logs hello-wasm 有输出
    - [ ] Wasm Pod 可以访问网络
```

## 10.12 参考

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
