# Kubernetes 1.30 双运行时集成

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 核心特性](#11-核心特性)
- [2. 安装 containerd Wasm shim](#2-安装-containerd-wasm-shim)
  - [2.1 下载 Wasm shim](#21-下载-wasm-shim)
  - [2.2 安装 WasmEdge](#22-安装-wasmedge)
- [3. 配置 Kubernetes](#3-配置-kubernetes)
  - [3.1 配置 containerd](#31-配置-containerd)
  - [3.2 创建 RuntimeClass](#32-创建-runtimeclass)
- [4. 部署 Wasm Pod](#4-部署-wasm-pod)
  - [4.1 构建 Wasm 镜像](#41-构建-wasm-镜像)
  - [4.2 部署 Pod](#42-部署-pod)
  - [4.3 部署 Deployment](#43-部署-deployment)
- [5. 最佳实践](#5-最佳实践)
  - [5.1 资源限制](#51-资源限制)
  - [5.2 选择运行时](#52-选择运行时)
  - [5.3 监控和日志](#53-监控和日志)
- [6. 相关文档](#6-相关文档)
  - [6.1 其他实现细节文档](#61-其他实现细节文档)
  - [6.2 架构视角文档](#62-架构视角文档)
  - [6.3 Kubernetes 文档](#63-kubernetes-文档)

---

## 1. 概述

**Kubernetes 1.30** 支持双运行时（runc + WasmEdge），允许在同一集群中同时运行容
器和 Wasm 工作负载。

### 1.1 核心特性

- **双运行时支持**：runc（容器）+ WasmEdge（Wasm）
- **统一调度**：通过 Kubernetes RuntimeClass 选择运行时
- **资源优化**：Wasm 工作负载资源占用减少 60%
- **边缘计算**：在边缘节点部署 Wasm 工作负载

---

## 2. 安装 containerd Wasm shim

### 2.1 下载 Wasm shim

```bash
# 下载 containerd Wasm shim v2
wget https://github.com/containerd/containerd/releases/download/v2.0.0/containerd-wasm-shim-v2-2.0.0-linux-amd64.tar.gz

# 解压
tar -xzf containerd-wasm-shim-v2-2.0.0-linux-amd64.tar.gz

# 安装到系统路径
sudo mv containerd-wasm-shim-v2 /usr/local/bin/
sudo chmod +x /usr/local/bin/containerd-wasm-shim-v2
```

### 2.2 安装 WasmEdge

```bash
# 安装 WasmEdge 0.14
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- -v 0.14.0

# 设置环境变量
export PATH=$PATH:$HOME/.wasmedge/bin
```

---

## 3. 配置 Kubernetes

### 3.1 配置 containerd

**containerd 配置**（`/etc/containerd/config.toml`）：

```toml
version = 2

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
    runtime_type = "io.containerd.runc.v2"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
      SystemdCgroup = true

  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.wasm]
    runtime_type = "io.containerd.wasm.v2"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.wasm.options]
      BinaryName = "containerd-wasm-shim-v2"
```

**重启 containerd**：

```bash
sudo systemctl restart containerd
```

### 3.2 创建 RuntimeClass

**RuntimeClass 定义**：

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: wasm
handler: wasm
```

**应用配置**：

```bash
kubectl apply -f runtimeclass-wasm.yaml
```

---

## 4. 部署 Wasm Pod

### 4.1 构建 Wasm 镜像

**Dockerfile**：

```dockerfile
FROM scratch
COPY app.wasm /app.wasm
ENTRYPOINT ["/app.wasm"]
```

**构建镜像**：

```bash
docker build -t my-registry/wasm-app:latest .
docker push my-registry/wasm-app:latest
```

### 4.2 部署 Pod

**Pod 定义**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: wasm-pod
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: my-registry/wasm-app:latest
      resources:
        limits:
          memory: "128Mi"
          cpu: "500m"
        requests:
          memory: "64Mi"
          cpu: "250m"
```

**部署**：

```bash
kubectl apply -f wasm-pod.yaml
```

### 4.3 部署 Deployment

**Deployment 定义**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wasm-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wasm-app
  template:
    metadata:
      labels:
        app: wasm-app
    spec:
      runtimeClassName: wasm
      containers:
        - name: wasm-app
          image: my-registry/wasm-app:latest
          resources:
            limits:
              memory: "128Mi"
              cpu: "500m"
```

---

## 5. 最佳实践

### 5.1 资源限制

**Wasm 工作负载资源建议**：

```yaml
resources:
  limits:
    memory: "128Mi" # Wasm 内存占用较小
    cpu: "500m"
  requests:
    memory: "64Mi"
    cpu: "250m"
```

### 5.2 选择运行时

**何时使用 Wasm**：

- ✅ 边缘计算场景（资源受限）
- ✅ Serverless 函数（冷启动敏感）
- ✅ AI 推理（轻量部署）
- ✅ 策略执行（OPA-Wasm）

**何时使用容器**：

- ✅ 需要完整操作系统功能
- ✅ 需要大量系统调用
- ✅ 需要特权访问

### 5.3 监控和日志

**使用 OpenTelemetry**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: wasm-pod
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: my-registry/wasm-app:latest
      env:
        - name: OTEL_SERVICE_NAME
          value: "wasm-app"
        - name: OTEL_EXPORTER_OTLP_ENDPOINT
          value: "http://otel-collector:4317"
```

---

## 6. 相关文档

### 6.1 其他实现细节文档

- [`wasmedge-setup.md`](wasmedge-setup.md) - WasmEdge 安装和配置
- [`wasi-examples.md`](wasi-examples.md) - WASI 接口使用示例
- [`wasm-compilation.md`](wasm-compilation.md) - Wasm 编译示例

### 6.2 架构视角文档

- [`../../02-views/10-quick-views/webassembly-view.md`](../../02-views/10-quick-views/webassembly-view.md) -
  WebAssembly 架构视角

### 6.3 Kubernetes 文档

- [Kubernetes RuntimeClass](https://kubernetes.io/docs/concepts/containers/runtime-class/)
- [containerd Wasm shim](https://github.com/containerd/containerd/tree/main/runtime/v2)

---

**更新时间**：2025-11-05 **版本**：v1.0 **参考**：Kubernetes 1.30 官方文档
