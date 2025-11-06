# L-4 沙盒化层（syscall 过滤 / 二次内核）- 包括 WebAssembly

**最后更新**: 2025-11-07 **维护者**: 项目团队

## 📑 目录

- [📑 目录](#-目录)
- [L-4.1 层级定位](#l-41-层级定位)
- [L-4.2 核心概念](#l-42-核心概念)
- [L-4.3 技术实现](#l-43-技术实现)
  - [L-4.3.1 gVisor](#l-431-gvisor)
  - [L-4.3.2 Firecracker](#l-432-firecracker)
  - [L-4.3.3 Kata Containers](#l-433-kata-containers)
  - [L-4.3.4 Windows Sandbox](#l-434-windows-sandbox)
- [L-4.4 WebAssembly 详解](#l-44-webassembly-详解)
  - [L-4.4.1 WebAssembly 概述](#l-441-webassembly-概述)
  - [L-4.4.2 WASI（WebAssembly System Interface）](#l-442-wasiwebassembly-system-interface)
  - [L-4.4.3 WasmEdge](#l-443-wasmedge)
  - [L-4.4.4 Wasmtime](#l-444-wasmtime)
  - [L-4.4.5 WAMR（WebAssembly Micro Runtime）](#l-445-wamrwebassembly-micro-runtime)
  - [L-4.4.6 WebAssembly 与其他沙盒技术对比](#l-446-webassembly-与其他沙盒技术对比)
- [L-4.5 性能特点](#l-45-性能特点)
- [L-4.6 安全特点](#l-46-安全特点)
- [L-4.7 应用场景](#l-47-应用场景)
- [L-4.8 故障排查](#l-48-故障排查)
  - [L-4.8.1 诊断关键词](#l-481-诊断关键词)
  - [L-4.8.2 常见问题](#l-482-常见问题)
- [L-4.9 与其他层次对比](#l-49-与其他层次对比)
- [L-4.10 实际部署案例](#l-410-实际部署案例)
  - [L-4.10.1 案例一：K3s + WasmEdge 边缘计算部署](#l-4101-案例一k3s--wasmedge-边缘计算部署)
  - [L-4.10.2 案例二：gVisor 安全隔离部署](#l-4102-案例二gvisor-安全隔离部署)
  - [L-4.10.3 案例三：Firecracker Serverless 部署](#l-4103-案例三firecracker-serverless-部署)
- [L-4.11 最佳实践](#l-411-最佳实践)
  - [L-4.11.1 WebAssembly 最佳实践](#l-4111-webassembly-最佳实践)
  - [L-4.11.2 gVisor 最佳实践](#l-4112-gvisor-最佳实践)
  - [L-4.11.3 Firecracker 最佳实践](#l-4113-firecracker-最佳实践)
  - [L-4.11.4 通用最佳实践](#l-4114-通用最佳实践)
- [L-4.12 参考](#l-412-参考)
  - [L-4.12.2 外部资源](#l-4122-外部资源)
  - [L-4.12.3 技术标准](#l-4123-技术标准)

---

## L-4.1 层级定位

**层级定位**：在容器或 VM 基础上再增加一层隔离，通过用户态内核或字节码 VM 拦截系
统调用。

**核心作用**：

- 在容器或 VM 基础上增加额外隔离层
- 通过用户态内核或字节码 VM 拦截系统调用
- 实现快速启动（<10ms）
- 提供最强的安全隔离（syscall 过滤）

**位置**：位于沙盒层，可以依赖 L-0 硬件辅助层（可选），是未来主流的技术。

---

## L-4.2 核心概念

| 组件                | 子模块/黑话                    | 一句话解释                                                        |
| ------------------- | ------------------------------ | ----------------------------------------------------------------- |
| **gVisor**          | Sentry、Gofer、runsc、seccomp  | 用户态 Go 内核拦截 syscall，容器逃逸只能打到 Sentry               |
| **Firecracker**     | MicroVM、Jailer、vsock、MMDS   | AWS 开源的 Rust 轻量 VMM，启动 < 125 ms，给 Lambda 当「二次隔离」 |
| **Kata Containers** | qemu-lite、virtio-fs、shimv2   | 把容器放进最小 VM，用 virtio-fs 挂载镜像，兼顾 K8s API 与 VM 隔离 |
| **WASM runtime**    | Wasmtime、WasmEdge、WAMR       | 字节码 + 能力模型，浏览器/边缘/链上合约的"终极沙盒"               |
| **Windows Sandbox** | WSB、thin-ply VHDX             | 每次双击自动生成一次性的 Win10 轻量 VM，用完即焚                  |
| **Chrome Sandbox**  | seccomp-bpf、namespace、setuid | 浏览器标签页先降权再过滤 syscall，Renderer 被攻破也跑不出沙盒     |

---

## L-4.3 技术实现

### L-4.3.1 gVisor

**技术特点**：

- **Sentry**：gVisor 的用户态内核，用 Go 实现，拦截所有系统调用
- **Gofer**：gVisor 的文件系统代理，负责文件系统操作的转发
- **runsc**：gVisor 的 OCI 运行时实现，替代 runc

**架构图**：

```text
┌─────────────────────────────────────┐
│ Container Application               │
├─────────────────────────────────────┤
│ Sentry (用户态内核)                  │
│  - 拦截所有 syscall                  │
│  - Go 实现                           │
├─────────────────────────────────────┤
│ Gofer (文件系统代理)                 │
│  - 文件系统操作转发                  │
├─────────────────────────────────────┤
│ Linux Kernel                        │
│  - 受限的 syscall                   │
└─────────────────────────────────────┘
```

**部署示例**：

```bash
# 安装 gVisor
curl -fsSL https://gvisor.dev/runsc/install | sh

# 使用 gVisor 运行容器
docker run --runtime=runsc nginx

# 在 Kubernetes 中使用
# 创建 RuntimeClass
kubectl apply -f runtimeclass.yaml
```

### L-4.3.2 Firecracker

**技术特点**：

- **MicroVM**：Firecracker 的轻量级虚拟机，极简的 VMM，最小化攻击面
- **Jailer**：Firecracker 的安全隔离组件，在非特权模式下运行 MicroVM
- **vsock**：VM 和 Host 之间的通信机制
- **MMDS（Metadata Service）**：Firecracker 的元数据服务

**部署示例**：

```bash
# 启动 Firecracker MicroVM
firecracker --api-sock /tmp/firecracker.sock

# 通过 API 配置 MicroVM
curl --unix-socket /tmp/firecracker.sock \
  -X PUT 'http://localhost/boot-source' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "kernel_image_path": "/path/to/kernel",
    "boot_args": "console=ttyS0 reboot=k panic=1 pci=off"
  }'
```

### L-4.3.3 Kata Containers

**技术特点**：

- **qemu-lite**：Kata Containers 使用的轻量级 QEMU
- **virtio-fs**：高性能的文件系统共享机制
- **shimv2**：Kata Containers 的 shim 实现，符合 containerd shim v2 接口

**部署示例**：

```bash
# 安装 Kata Containers
sudo apt-get install kata-runtime

# 使用 Kata Containers 运行容器
docker run --runtime=kata nginx

# 在 Kubernetes 中使用
kubectl apply -f kata-runtimeclass.yaml
```

### L-4.3.4 Windows Sandbox

**技术特点**：

- **WSB（Windows Sandbox）**：Windows 10/11 的轻量级沙盒
- **thin-ply VHDX**：一次性使用的虚拟硬盘

**部署示例**：

```powershell
# 启用 Windows Sandbox
Enable-WindowsOptionalFeature -Online -FeatureName "Containers-DisposableClientVM"

# 运行 Windows Sandbox
# 通过开始菜单启动 Windows Sandbox
```

---

## L-4.4 WebAssembly 详解

### L-4.4.1 WebAssembly 概述

**WebAssembly（WASM）** 是一种低级的字节码格式，设计用于在 Web 浏览器和服务器环
境中高效执行。

**核心特点**：

- **字节码 VM**：基于字节码的虚拟机
- **能力模型**：基于能力的安全控制
- **快速启动**：<10ms 冷启动
- **低内存占用**：1-5MB 内存占用
- **跨平台**：可在任何支持 WASM 的环境中运行

### L-4.4.2 WASI（WebAssembly System Interface）

**WASI** 是 WebAssembly 的系统调用接口标准，提供安全的系统调用接口。

**核心特性**：

- **能力模型**：基于能力的安全控制
- **最小权限**：只授予必要的权限
- **系统调用抽象**：抽象的系统调用接口

**WASI 示例**：

```rust
// Rust + WASI 示例
use wasi::*;

fn main() {
    let fd = wasi::fd_open("file.txt", WASI_O_CREAT | WASI_O_WRONLY);
    wasi::fd_write(fd, b"Hello, WASI!");
    wasi::fd_close(fd);
}
```

### L-4.4.3 WasmEdge

**WasmEdge** 是一个高性能的 WebAssembly 运行时，专为边缘计算和云原生应用设计。

**技术特点**：

- **高性能**：优化的 WebAssembly 执行引擎
- **WASI 支持**：完整的 WASI 支持
- **Kubernetes 集成**：原生支持 Kubernetes RuntimeClass
- **多语言支持**：支持 Rust、C、C++、Go、Python 等

**架构图**：

```text
┌─────────────────────────────────────┐
│ Application (WASM)                  │
├─────────────────────────────────────┤
│ WasmEdge Runtime                    │
│  - WasmVM                           │
│  - WASI                             │
│  - Host Functions                   │
├─────────────────────────────────────┤
│ Kubernetes                          │
│  - RuntimeClass: wasm               │
│  - crun + WasmEdge                  │
└─────────────────────────────────────┘
```

**部署示例**：

```bash
# 安装 WasmEdge
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash

# 使用 WasmEdge 运行 WASM 应用
wasmedge app.wasm

# 在 Kubernetes 中使用
# 创建 RuntimeClass
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: wasm
handler: crun
```

```yaml
# Pod 配置
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-container
      image: wasm-app:latest
```

### L-4.4.4 Wasmtime

**Wasmtime** 是 Bytecode Alliance 开发的高性能 WebAssembly 运行时。

**技术特点**：

- **JIT 编译**：Just-In-Time 编译优化
- **WASI 支持**：完整的 WASI 支持
- **多语言嵌入**：支持 Rust、C、Python、Go 等

**部署示例**：

```bash
# 安装 Wasmtime
curl https://wasmtime.dev/install.sh -sSf | bash

# 使用 Wasmtime 运行 WASM 应用
wasmtime app.wasm
```

### L-4.4.5 WAMR（WebAssembly Micro Runtime）

**WAMR** 是 Intel 开发的轻量级 WebAssembly 运行时。

**技术特点**：

- **轻量级**：极小的运行时占用
- **快速启动**：优化的启动速度
- **IoT 优化**：专为 IoT 设备优化

### L-4.4.6 WebAssembly 与其他沙盒技术对比

| 特性         | WebAssembly | gVisor     | Firecracker | Kata Containers |
| ------------ | ----------- | ---------- | ----------- | --------------- |
| **启动时间** | <10ms       | 100-500ms  | <125ms      | 1-3s            |
| **内存占用** | 1-5MB       | 10-50MB    | 5-10MB      | 64-128MB        |
| **隔离强度** | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐      |
| **兼容性**   | ⭐⭐⭐      | ⭐⭐⭐⭐   | ⭐⭐⭐      | ⭐⭐⭐⭐        |
| **性能**     | ⭐⭐⭐⭐⭐  | ⭐⭐⭐     | ⭐⭐⭐⭐    | ⭐⭐⭐          |

---

## L-4.5 性能特点

| 性能指标       | 特点           | 说明                               |
| -------------- | -------------- | ---------------------------------- |
| **隔离强度**   | ⭐⭐⭐⭐⭐ (5) | 最强隔离，syscall 过滤             |
| **冷启动时间** | <10ms          | 极快启动（WASM）或快速启动（其他） |
| **内存开销**   | 1-5MB (WASM)   | 极低内存占用                       |
| **CPU 开销**   | <1%            | 极低 CPU 开销                      |
| **资源利用率** | ⭐⭐⭐⭐⭐ (5) | 极高密度部署                       |
| **网络性能**   | ⭐⭐⭐⭐⭐ (5) | 优秀的网络性能                     |
| **存储性能**   | ⭐⭐⭐⭐⭐ (5) | 优秀的存储性能                     |

**优势**：

- ✅ 最强隔离，syscall 过滤
- ✅ 快速启动（WASM <10ms）
- ✅ 低资源占用（WASM 1-5MB）
- ✅ 适合边缘计算和 Serverless

**劣势**：

- ⚠️ 兼容性相对较低（WASM）
- ⚠️ 需要应用适配（WASM）

---

## L-4.6 安全特点

| 安全特性       | 说明           | 安全等级               |
| -------------- | -------------- | ---------------------- |
| **隔离强度**   | ⭐⭐⭐⭐⭐ (5) | 最强隔离，syscall 过滤 |
| **攻击面**     | 最小           | 最小化攻击面           |
| **多租户隔离** | ✅ 完整隔离    | 每个沙盒完全独立       |
| **合规要求**   | ✅ 满足        | 最强隔离，满足合规要求 |

**安全优势**：

- ✅ 最强隔离，syscall 过滤
- ✅ 最小化攻击面
- ✅ 能力模型（WASM）
- ✅ 零信任架构支持

**安全加固**：

```bash
# gVisor 安全配置
docker run --runtime=runsc --security-opt seccomp=unconfined nginx

# Firecracker 安全配置
firecracker --jailer-config /path/to/jailer-config.json

# WasmEdge 安全配置
wasmedge --dir /allowed/dir app.wasm
```

---

## L-4.7 应用场景

**适用场景**：

- ✅ **边缘计算**：资源受限的边缘场景（WASM）
- ✅ **Serverless**：需要快速启动的 Serverless 场景（WASM）
- ✅ **AI 推理**：边缘 AI 推理（WASM）
- ✅ **安全隔离**：需要强隔离的安全场景
- ✅ **多租户 SaaS**：需要强隔离的多租户场景

**不适用场景**：

- ❌ **传统应用**：需要完全兼容的传统应用（WASM）
- ❌ **内核定制需求**：需要定制内核的场景

**典型技术栈**：

- **边缘计算**：K3s + WasmEdge
- **Serverless**：Knative + WasmEdge
- **安全隔离**：gVisor + Kubernetes
- **AWS Lambda**：Firecracker

---

## L-4.8 故障排查

### L-4.8.1 诊断关键词

| 关键词                                | 含义                          | 解决方法                    |
| ------------------------------------- | ----------------------------- | --------------------------- |
| `Gofer broken pipe`                   | gVisor 文件系统代理连接断开   | 检查 Gofer 进程，重启容器   |
| `Sentry syscall denied`               | gVisor 拦截了不允许的系统调用 | 检查 syscall 白名单配置     |
| `Firecracker MicroVM failed to start` | MicroVM 启动失败              | 检查 MicroVM 配置，查看日志 |
| `Kata shimv2 timeout`                 | Kata Containers shim 超时     | 检查 Kata 配置，重启 shim   |
| `WASI operation not permitted`        | WASM 运行时拒绝了系统调用     | 检查 WASI 权限配置          |
| `WasmEdge runtime error`              | WasmEdge 运行时错误           | 检查 WASM 模块，查看日志    |

### L-4.8.2 常见问题

**问题 1：gVisor 容器无法启动**:

```bash
# 检查 gVisor 日志
docker logs container-name

# 检查 Sentry 进程
ps aux | grep sentry

# 检查 Gofer 进程
ps aux | grep gofer
```

**问题 2：WASM 应用无法运行**:

```bash
# 检查 WasmEdge 安装
wasmedge --version

# 检查 WASM 模块
wasmedge app.wasm --help

# 检查 WASI 权限
wasmedge --dir /allowed/dir app.wasm
```

**问题 3：Kata Containers 启动失败**:

```bash
# 检查 Kata 配置
kata-runtime kata-env

# 检查 Kata shim 日志
journalctl -u kata-shim

# 检查 Kata VM 状态
kata-runtime list
```

---

## L-4.9 与其他层次对比

| 对比维度       | L-4 沙盒化    | L-1 全虚拟化 | L-2 半虚拟化 | L-3 容器化 |
| -------------- | ------------- | ------------ | ------------ | ---------- |
| **隔离强度**   | ⭐⭐⭐⭐⭐    | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐     | ⭐⭐⭐     |
| **冷启动时间** | <10ms (WASM)  | 5-30s        | 3-10s        | 1-5s       |
| **内存开销**   | 1-5MB (WASM)  | 128MB+       | 64-128MB     | 10-50MB    |
| **CPU 开销**   | <1%           | 5-10%        | 2-5%         | 1-3%       |
| **资源利用率** | ⭐⭐⭐⭐⭐    | ⭐⭐         | ⭐⭐⭐       | ⭐⭐⭐⭐⭐ |
| **兼容性**     | ⭐⭐⭐ (WASM) | ⭐⭐⭐⭐⭐   | ⭐⭐⭐⭐     | ⭐⭐⭐⭐⭐ |
| **部署密度**   | 极高          | 低           | 中           | 高         |

**关键区别**：

- **L-4** 提供最强隔离和最快启动（WASM）
- **L-4** 适合边缘计算和 Serverless 场景
- **L-4** 兼容性相对较低（WASM），需要应用适配

**相关文档**：

- 详细对比：[隔离层次总结合并对比](isolation-comparison.md)
- 依赖层次：[L-0 硬件辅助层](L-0-hardware-assist.md)（可选）
- 相关层次
  ：[L-1 全虚拟化层](L-1-full-virtualization.md)、[L-2 半虚拟化层](L-2-paravirtualization.md)、[L-3 容器化层](L-3-containerization.md)

---

## L-4.10 实际部署案例

### L-4.10.1 案例一：K3s + WasmEdge 边缘计算部署

**场景**：边缘节点需要快速启动和低资源占用，使用 K3s + WasmEdge 部署。

**配置步骤**：

```bash
# 1. 安装 K3s 并启用 WasmEdge
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--wasm" sh -

# 2. 创建 RuntimeClass
cat <<EOF | kubectl apply -f -
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: wasm
handler: crun
EOF

# 3. 部署 WASM 应用
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app
spec:
  runtimeClassName: wasm
  containers:
  - name: wasm-container
    image: wasm-app:latest
EOF
```

**预期结果**：

- 容器启动时间 <10ms
- 内存占用 <5MB
- 应用正常运行

### L-4.10.2 案例二：gVisor 安全隔离部署

**场景**：多租户场景需要强隔离，使用 gVisor 部署容器。

**配置步骤**：

```bash
# 1. 安装 gVisor
curl -fsSL https://gvisor.dev/runsc/install | sh

# 2. 配置 Docker 使用 gVisor
sudo mkdir -p /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "runtimes": {
    "runsc": {
      "path": "/usr/local/bin/runsc"
    }
  }
}
EOF

# 3. 重启 Docker
sudo systemctl restart docker

# 4. 使用 gVisor 运行容器
docker run --runtime=runsc nginx:latest
```

**预期结果**：

- 容器隔离强度提升
- syscall 被 gVisor 拦截
- 安全性提升

### L-4.10.3 案例三：Firecracker Serverless 部署

**场景**：Serverless 场景需要快速启动，使用 Firecracker 部署。

**配置步骤**：

```bash
# 1. 下载 Firecracker
wget https://github.com/firecracker-microvm/firecracker/releases/download/v1.4.0/firecracker-v1.4.0-x86_64.tgz
tar -xzf firecracker-v1.4.0-x86_64.tgz

# 2. 启动 Firecracker API 服务
./firecracker --api-sock /tmp/firecracker.sock &

# 3. 配置 MicroVM
curl --unix-socket /tmp/firecracker.sock \
  -X PUT 'http://localhost/boot-source' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "kernel_image_path": "/path/to/kernel",
    "boot_args": "console=ttyS0 reboot=k panic=1 pci=off"
  }'
```

**预期结果**：

- MicroVM 启动时间 <125ms
- 资源占用低
- 隔离强度高

---

## L-4.11 最佳实践

### L-4.11.1 WebAssembly 最佳实践

1. **应用设计**：

   - 设计无状态应用，利用 WASM 快速启动特性
   - 使用 WASI 标准接口，提高可移植性

2. **性能优化**：

   - 使用 AOT（Ahead-of-Time）编译优化性能
   - 合理使用 WASI 接口，避免频繁系统调用

3. **安全配置**：
   - 使用能力模型，只授予必要的权限
   - 配置 WASI 权限，限制文件系统和网络访问

### L-4.11.2 gVisor 最佳实践

1. **性能考虑**：

   - gVisor 的性能开销较大，不适合高性能场景
   - 适用于安全隔离要求高的场景

2. **兼容性**：
   - 部分系统调用可能不被支持，需要测试
   - 某些应用可能需要调整才能正常运行

### L-4.11.3 Firecracker 最佳实践

1. **资源配置**：

   - 合理配置 MicroVM 的资源（CPU、内存）
   - 使用 Jailer 增强安全性

2. **性能优化**：
   - 使用 vsock 进行 VM 通信，提升性能
   - 配置合适的网络和存储后端

### L-4.11.4 通用最佳实践

1. **技术选型**：

   - 根据场景选择合适的技术（WASM、gVisor、Firecracker）
   - 考虑性能、安全和兼容性的平衡

2. **监控和调试**：
   - 配置日志收集，便于问题排查
   - 监控资源使用情况和性能指标

---

## L-4.12 参考

- **[29. 隔离栈](../isolation-stack.md)** - 完整的四层隔离栈文档
  - **[29.3.5 L-4 沙盒化层](../isolation-stack.md#2935-l-4-沙盒化层syscall-过滤--二次内核)** -
    详细技术解析
- **[03. WasmEdge](../../03-wasm-edge/wasmedge.md)** - WasmEdge 详细文档
- **[07. 边缘和 Serverless](../../07-edge-serverless/edge-serverless.md)** - 边
  缘计算和 Serverless 文档
- **[08. AI 推理](../../08-ai-inference/ai-inference.md)** - AI 推理文档
- **[30. 概念关系矩阵](../../30-concept-relations-matrix/concept-relations-matrix.md)** -
  概念关系梳理
  - **[30.20 隔离层次全面对比分析](../../30-concept-relations-matrix/concept-relations-matrix.md#3020-隔离层次全面对比分析)** -
    隔离层次对比

### L-4.12.2 外部资源

- **gVisor 文档** - gVisor 官方文档
- **Firecracker 文档** - Firecracker 官方文档
- **Kata Containers 文档** - Kata Containers 官方文档
- **WebAssembly 标准** - WebAssembly 标准文档
- **WASI 标准** - WebAssembly System Interface 标准
- **WasmEdge 文档** - WasmEdge 官方文档
- **Wasmtime 文档** - Wasmtime 官方文档
- **WAMR 文档** - WAMR 官方文档

### L-4.12.3 技术标准

- **WebAssembly 标准** - WebAssembly 核心标准
- **WASI 标准** - WebAssembly System Interface 标准
- **OCI Runtime Spec** - OCI 运行时规范（gVisor、Kata）

---

**最后更新**: 2025-11-07 **维护者**: 项目团队
