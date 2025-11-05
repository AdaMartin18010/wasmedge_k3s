# 08. AI 推理（WasmEdge）：模型 Wasm 化与轻量插件

## 📑 目录

- [📑 目录](#-目录)
- [08.1 文档定位](#081-文档定位)
- [08.2 AI 推理场景](#082-ai-推理场景)
  - [08.2.1 边缘 AI 推理](#0821-边缘-ai-推理)
  - [08.2.2 模型 Wasm 化](#0822-模型-wasm-化)
  - [08.2.3 轻量插件方案](#0823-轻量插件方案)
- [08.3 技术对比](#083-技术对比)
  - [08.3.1 容器化 Python 推理 vs Wasm 推理](#0831-容器化-python-推理-vs-wasm-推理)
  - [08.3.2 性能对比分析](#0832-性能对比分析)
  - [08.3.3 成本对比分析](#0833-成本对比分析)
- [08.4 低延迟优化](#084-低延迟优化)
  - [08.4.1 启动延迟优化](#0841-启动延迟优化)
  - [08.4.2 推理延迟优化](#0842-推理延迟优化)
  - [08.4.3 延迟优化论证](#0843-延迟优化论证)
- [08.5 GPU 集成](#085-gpu-集成)
  - [08.5.1 WasmEdge GPU Plugin](#0851-wasmedge-gpu-plugin)
  - [08.5.2 GPU 推理架构](#0852-gpu-推理架构)
  - [08.5.3 GPU 集成论证](#0853-gpu-集成论证)
- [08.6 WasmEdge 0.14 + Llama2 实战方案（2025）](#086-wasmedge-014--llama2-实战方案2025)
  - [08.6.0 2025-11-06 最新方案概览](#0860-2025-11-06-最新方案概览)
- [08.7 技术场景分析](#087-技术场景分析)
  - [08.7.1 边缘 AI 推理场景](#0871-边缘-ai-推理场景)
  - [08.6.2 云端 AI 推理场景](#0862-云端-ai-推理场景)
  - [08.6.3 混合 AI 推理场景](#0863-混合-ai-推理场景)
- [08.8 决策依据与思路](#088-决策依据与思路)
  - [08.8.1 AI 推理场景决策树（2025-11-06 更新）](#0881-ai-推理场景决策树2025-11-06-更新)
  - [08.8.2 模型选择决策树（2025-11-06 更新）](#0882-模型选择决策树2025-11-06-更新)
  - [08.8.3 GPU 集成决策树（2025-11-06 更新）](#0883-gpu-集成决策树2025-11-06-更新)
- [08.9 形式化总结](#089-形式化总结)
  - [08.9.1 AI 推理延迟模型形式化](#0891-ai-推理延迟模型形式化)
  - [08.9.2 AI 推理成本模型形式化](#0892-ai-推理成本模型形式化)
- [08.10 实际部署案例](#0810-实际部署案例)
  - [08.10.1 案例 1：WasmEdge + Llama2 推理部署](#08101-案例-1wasmedge--llama2-推理部署)
  - [08.10.2 案例 2：边缘 AI 推理部署](#08102-案例-2边缘-ai-推理部署)
  - [08.10.3 案例 3：模型 Wasm 化流程](#08103-案例-3模型-wasm-化流程)
- [08.11 AI 推理故障排查](#0811-ai-推理故障排查)
  - [08.11.1 常见问题](#08111-常见问题)
- [08.12 AI 推理最佳实践](#0812-ai-推理最佳实践)
  - [08.12.1 模型 Wasm 化最佳实践](#08121-模型-wasm-化最佳实践)
  - [08.12.2 GPU 集成最佳实践](#08122-gpu-集成最佳实践)
  - [08.12.3 边缘 AI 推理最佳实践](#08123-边缘-ai-推理最佳实践)
  - [08.12.4 AI 推理检查清单](#08124-ai-推理检查清单)
- [08.13 参考](#0813-参考)
  - [08.13.1 隔离栈相关文档](#08131-隔离栈相关文档)
  - [08.13.2 AI 推理相关文档](#08132-ai-推理相关文档)
  - [08.13.3 其他相关文档](#08133-其他相关文档)

---

## 08.1 文档定位

本文档深入解析 WasmEdge 在 AI 推理场景中的应用，包括模型 Wasm 化、轻量插件方案和
低延迟优化的技术原理、实现方式和最佳实践。

**当前版本（2025-11-06）**：

- **WasmEdge 版本**：0.14.0（内置 Llama2/7B 插件，2025-11-06）
- **关键特性**：张量算子直接调用 GPU 驱动，推理延迟比 PyTorch 容器 ↓60%
- **模型市场**：".wasm 模型镜像"格式，镜像体积仅为 Python 容器 1/10
- **生产验证**：KubeCon 2025 中国议题，基于 WasmEdge + K8s 1.30，性能提升
  300%（2025-11-06）

**文档结构**：

- **AI 推理场景**：边缘 AI 推理、模型 Wasm 化、轻量插件方案
- **WasmEdge 0.14 + Llama2**：内置 Llama2 插件、模型 Wasm-化流程、GPU 加速推理
- **技术对比**：容器化 Python 推理 vs Wasm 推理的性能和成本对比
- **低延迟优化**：启动延迟和推理延迟的优化方案
- **GPU 集成**：WasmEdge GPU Plugin 的技术原理和应用
- **技术场景**：边缘、云端、混合 AI 推理场景的架构设计

## 08.2 AI 推理场景

### 08.2.1 边缘 AI 推理

> **💡 隔离层次关联**：边缘 AI 推理使用 L-4 沙盒化层的 WasmEdge 运行时，提供极速
> 冷启动（<10ms）和低资源占用，是边缘计算的理想选择。详细的技术解析请参考：
>
> - **[29. 隔离栈](../29-isolation-stack/isolation-stack.md)** - 完整的隔离栈技
>   术解析
> - **[L-4 沙盒化层](../29-isolation-stack/layers/L-4-sandboxing.md)** - WASM 运
>   行时详细文档，包含边缘 AI 推理应用场景
> - **[隔离层次对比文档](../29-isolation-stack/layers/isolation-comparison.md)** -
>   WASM 性能对比和应用场景匹配

**场景描述**：在边缘节点运行 AI 推理，降低延迟，减少数据传输。

**技术需求**：

- **低延迟**：需要 < 50ms 推理延迟
- **资源受限**：边缘节点资源有限
- **离线能力**：需要离线运行能力

**架构设计**：

```yaml
边缘 AI 推理架构:
  编排层: K3s（轻量 Kubernetes）
  运行时: WasmEdge（快速启动、低资源）
  模型: Wasm 模型（.wasm 文件）
  GPU: 可选 GPU（加速推理）
  特点: 低延迟、资源受限、离线能力
```

**边缘 AI 推理论证**：

- **低延迟需求**：WasmEdge 启动 < 10ms，推理延迟 < 50ms
- **资源受限**：Wasm 模型体积小，内存占用低，适合边缘节点
- **离线能力**：模型存储在本地，支持离线推理

### 08.2.2 模型 Wasm 化

**模型 Wasm 化**：将 AI 模型编译为 Wasm 格式，在 WasmEdge 中运行。

**Wasm 化流程**：

```mermaid
graph LR
    A[AI 模型<br/>ONNX/TensorFlow] --> B[模型转换工具]
    B --> C[Wasm 模型<br/>.wasm]
    C --> D[WasmEdge 推理]
    D --> E[推理结果]

    style A fill:#e1f5ff
    style E fill:#e6ffe6
```

**模型 Wasm 化论证**：

- **体积优化**：Wasm 模型体积小，便于传输和存储
- **跨平台**：Wasm 跨平台，可在不同架构运行
- **快速启动**：Wasm 启动快，满足边缘 AI 延迟要求

### 08.2.3 轻量插件方案

**轻量插件**：WasmEdge 提供轻量级 AI 推理插件，支持多种 AI 框架。

**插件类型**：

- **WASI-NN**：神经网络推理插件
- **TensorFlow Lite**：TensorFlow Lite 插件
- **ONNX Runtime**：ONNX Runtime 插件

**轻量插件论证**：

- **轻量级**：插件体积小，资源占用低
- **多框架**：支持多种 AI 框架（TensorFlow、ONNX 等）
- **高性能**：插件优化，推理性能好

## 08.3 技术对比

### 08.3.1 容器化 Python 推理 vs Wasm 推理

| 指标         | 容器化 Python 推理 | Wasm 推理 | 提升倍数          |
| ------------ | ------------------ | --------- | ----------------- |
| **启动时间** | 1-2s               | 6-10ms    | **100-200× 更快** |
| **镜像体积** | 500MB-2GB          | 1-10MB    | **50-200× 更小**  |
| **内存占用** | 100-500MB          | 10-50MB   | **10× 更小**      |
| **推理延迟** | 50-100ms           | 20-50ms   | **2× 更快**       |
| **CPU 占用** | 高                 | 低        | **更低**          |

**对比论证**：

- **启动时间**：Wasm 启动 < 10ms，比容器快 100-200 倍
- **镜像体积**：Wasm 镜像 < 10MB，比容器小 50-200 倍
- **内存占用**：Wasm 内存 10-50MB，比容器小 10 倍
- **推理延迟**：Wasm 推理延迟 20-50ms，比容器快 2 倍

### 08.3.2 性能对比分析

**性能优势**：

- **启动速度**：Wasm 启动 < 10ms，满足边缘 AI 延迟要求
- **资源占用**：Wasm 资源占用低，适合资源受限环境
- **推理性能**：Wasm 推理延迟低，满足实时推理要求

**性能论证**：

- **启动速度**：Wasm 启动 < 10ms，比容器快 100 倍，满足边缘 AI 延迟要求
- **资源占用**：Wasm 内存 10-50MB，比容器小 10 倍，适合资源受限环境
- **推理性能**：Wasm 推理延迟 20-50ms，比容器快 2 倍，满足实时推理要求

### 08.3.3 成本对比分析

**成本优势**：

- **存储成本**：Wasm 镜像体积小，存储成本低
- **计算成本**：Wasm 资源占用低，计算成本低
- **传输成本**：Wasm 镜像体积小，传输成本低

**成本论证**：

- **存储成本**：Wasm 镜像 < 10MB，比容器小 50-200 倍，存储成本低
- **计算成本**：Wasm 内存 10-50MB，比容器小 10 倍，计算成本低
- **传输成本**：Wasm 镜像体积小，传输成本低

## 08.4 低延迟优化

### 08.4.1 启动延迟优化

**优化策略**：

```yaml
启动延迟优化:
  运行时: WasmEdge（启动 < 10ms）
  镜像: scratch（零 rootfs，体积 < 1MB）
  预热: Pod 预热（保持最小 Pod 数）
  优势: 极速启动、低资源占用
```

**启动延迟优化论证**：

- **WasmEdge**：启动 < 10ms，比容器快 100 倍
- **零 rootfs**：使用 scratch 镜像，无需加载文件系统
- **Pod 预热**：保持最小 Pod 数，避免冷启动

### 08.4.2 推理延迟优化

**优化策略**：

```yaml
推理延迟优化:
  模型优化: 模型量化、剪枝
  GPU 加速: 使用 GPU 加速推理
  批量推理: 批量处理请求
  优势: 低推理延迟、高吞吐量
```

**推理延迟优化论证**：

- **模型优化**：模型量化、剪枝，减少计算量
- **GPU 加速**：使用 GPU 加速推理，降低延迟
- **批量推理**：批量处理请求，提高吞吐量

### 08.4.3 延迟优化论证

**为什么 Wasm 推理延迟更低？**

**技术论证**：

1. **启动速度快**：Wasm 启动 < 10ms，比容器快 100 倍
2. **资源占用低**：Wasm 资源占用低，减少资源竞争
3. **模型优化**：Wasm 模型可以优化，减少计算量

**延迟优化模型**：
$$L_{\text{total}} = L_{\text{startup}} + L_{\text{inference}}$$

其中：

- $L_{\text{startup}}$ = 启动延迟（Wasm < 10ms，容器 > 1s）
- $L_{\text{inference}}$ = 推理延迟（Wasm 20-50ms，容器 50-100ms）

**优化目标**：
$$\min_{W} L_{\text{total}} = \min_{W} (L_{\text{startup}} \downarrow + L_{\text{inference}} \downarrow)$$

## 08.5 GPU 集成

### 08.5.1 WasmEdge GPU Plugin

**GPU Plugin**：WasmEdge 提供 GPU 插件，支持 GPU 加速推理。

**GPU Plugin 特点**：

- **GPU 加速**：支持 GPU 加速推理
- **多框架**：支持 TensorFlow、ONNX 等框架
- **跨平台**：支持 CUDA、OpenCL 等 GPU 后端

**GPU Plugin 论证**：

- **GPU 加速**：使用 GPU 加速推理，降低延迟
- **多框架**：支持多种 AI 框架，灵活选择
- **跨平台**：支持多种 GPU 后端，兼容性好

### 08.5.2 GPU 推理架构

```mermaid
graph TB
    A[Wasm 模型] --> B[WasmEdge GPU Plugin]
    B --> C[GPU 后端<br/>CUDA/OpenCL]
    C --> D[GPU 推理]
    D --> E[推理结果]

    style A fill:#e1f5ff
    style E fill:#e6ffe6
```

**GPU 推理架构论证**：

- **Wasm 模型**：模型以 Wasm 格式存储
- **GPU Plugin**：WasmEdge GPU Plugin 处理 GPU 推理
- **GPU 后端**：支持 CUDA、OpenCL 等 GPU 后端

### 08.5.3 GPU 集成论证

**为什么需要 GPU 集成？**

**决策依据**：

- ✅ **性能需求**：GPU 加速推理，降低延迟
- ✅ **边缘 AI**：在边缘节点运行 AI 推理，需要 GPU 加速
- ✅ **实时推理**：满足实时推理延迟要求

**决策思路**：

```yaml
GPU 集成策略:
  Plugin: WasmEdge GPU Plugin
  后端: CUDA/OpenCL
  应用: 边缘 AI 推理、实时推理
  优势: GPU 加速、低延迟、高吞吐量
```

## 08.6 WasmEdge 0.14 + Llama2 实战方案（2025）

### 08.6.0 2025-11-06 最新方案概览

**WasmEdge 0.14 + Llama2 方案**（2025-11-06 已标准化）：

| 组件         | 版本/特性      | 状态     | 性能指标                    |
| ------------ | -------------- | -------- | --------------------------- |
| **WasmEdge** | 0.14.0         | 稳定     | 推理延迟 ↓60%（vs PyTorch） |
| **Llama2**   | 内置 7B 插件   | 生产就绪 | GPU 加速推理                |
| **K8s/K3s**  | 1.30+          | 原生支持 | RuntimeClass=wasm           |
| **模型格式** | .wasm 模型镜像 | 标准     | 镜像体积仅为 Python 1/10    |

**一键部署示例**：

```bash
# 1. 拉取 Llama2 Wasm 模型镜像
wasm-to-oci pull yourhub/llama2-7b.wasm:v1

# 2. 运行 WasmEdge + Llama2
wasmedge --dir .:/path/to/model \
  wasmedge_llama.wasm \
  --prompt "Hello, AI!"

# 3. 在 K3s 中部署（K3s 1.30+）
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: llama2-inference
spec:
  runtimeClassName: wasm
  containers:
  - name: llama2
    image: yourhub/llama2-7b.wasm:v1
    command: ["wasmedge", "--dir", ".", "/wasmedge_llama.wasm"]
EOF
```

**2025-11-06 生产案例**：

- **KubeCon 2025 中国议题**："生成式 AI 工作负载的 Linux 技术栈优化"
  - **技术栈**：全部基于 WasmEdge 0.14 + K8s 1.30
  - **性能提升**：300%（vs 传统容器化 PyTorch）
- **模型市场**：".wasm 模型镜像"格式已成为标准

## 08.7 技术场景分析

### 08.7.1 边缘 AI 推理场景

**场景描述**：在边缘节点运行 AI 推理，降低延迟，减少数据传输。

**架构挑战**：

1. **低延迟**：需要 < 50ms 推理延迟
2. **资源受限**：边缘节点资源有限
3. **离线能力**：需要离线运行能力

**架构决策**：

```yaml
边缘 AI 推理配置:
  编排: K3s（轻量 Kubernetes）
  运行时: WasmEdge（快速启动、低资源）
  模型: Wasm 模型（.wasm 文件）
  GPU: 可选 GPU（加速推理）
  优势: 低延迟、资源受限、离线能力
```

**决策依据**：

- ✅ **低延迟**：WasmEdge 启动 < 10ms，推理延迟 < 50ms
- ✅ **资源受限**：Wasm 模型体积小，内存占用低
- ✅ **离线能力**：模型存储在本地，支持离线推理

### 08.6.2 云端 AI 推理场景

**场景描述**：在云端运行 AI 推理，提供高吞吐量推理服务。

**架构挑战**：

1. **高吞吐量**：需要支持高并发推理请求
2. **资源充足**：云端资源充足
3. **GPU 加速**：需要使用 GPU 加速推理

**架构决策**：

```yaml
云端 AI 推理配置:
  编排: Kubernetes（大规模集群）
  运行时: WasmEdge（高密度部署）
  模型: Wasm 模型（.wasm 文件）
  GPU: GPU 加速（CUDA/OpenCL）
  优势: 高吞吐量、GPU 加速、高密度部署
```

**决策依据**：

- ✅ **高吞吐量**：单节点可部署 3000 Pod，支持高并发
- ✅ **GPU 加速**：使用 GPU 加速推理，提高吞吐量
- ✅ **高密度部署**：Wasm 资源占用低，支持高密度部署

### 08.6.3 混合 AI 推理场景

**场景描述**：边缘节点和云端协同，实现混合 AI 推理。

**架构挑战**：

1. **边缘推理**：边缘节点进行实时推理
2. **云端训练**：云端进行模型训练和更新
3. **模型同步**：边缘和云端模型同步

**架构决策**：

```yaml
混合 AI 推理配置:
  边缘: K3s + WasmEdge + Wasm 模型
  云端: Kubernetes + WasmEdge + Wasm 模型
  同步: OCI 镜像（模型版本管理）
  优势: 边缘推理、云端训练、模型同步
```

**决策依据**：

- ✅ **边缘推理**：边缘节点运行实时推理，降低延迟
- ✅ **云端训练**：云端进行模型训练，资源充足
- ✅ **模型同步**：通过 OCI 镜像同步模型，版本管理

## 08.8 决策依据与思路

### 08.8.1 AI 推理场景决策树（2025-11-06 更新）

```yaml
AI 推理场景决策（2025-11-06）:
  if 边缘 AI（低延迟）:
    选择: K3s 1.30 + WasmEdge 0.14 + Wasm 模型
    特性: --wasm flag 即开即用，冷启动 ≤6 ms
  elif 云端 AI（高吞吐量）:
    选择: Kubernetes 1.30 + WasmEdge 0.14 + Llama2 插件
    特性: RuntimeClass=wasm 原生支持，GPU 加速推理
  elif 混合 AI（边缘+云端）:
    选择: K3s + Kubernetes + WasmEdge 0.14
    特性: 统一模型格式（.wasm），镜像体积仅为 Python 1/10
  elif Llama2 推理（2025-11-06最新）:
    选择: WasmEdge 0.14 + Llama2/7B 插件 + GPU
    特性: 推理延迟 ↓60%，内置 GPU 支持
  else:
    选择: K3s 1.30 + WasmEdge 0.14（默认组合）
```

### 08.8.2 模型选择决策树（2025-11-06 更新）

```yaml
模型选择决策（2025-11-06）:
  if 资源受限:
    选择: Wasm 模型（体积小、资源占用低）
    格式: .wasm 模型镜像（仅为 Python 1/10）
  elif Llama2 推理（2025-11-06最新）:
    选择: WasmEdge 0.14 + Llama2/7B 插件
    特性: 内置 GPU 支持，推理延迟 ↓60%
  elif 边缘 AI:
    选择: Wasm 模型（体积小、资源占用低）
  elif 低延迟需求: Wasm 模型（启动快、推理快）
  elif 跨平台需求: Wasm 模型（跨平台、可移植）
  else: 传统模型（可选）
```

### 08.8.3 GPU 集成决策树（2025-11-06 更新）

```yaml
GPU 集成决策（2025-11-06）:
  if Llama2 推理（2025-11-06最新） and 有 GPU:
    选择: WasmEdge 0.14 + Llama2/7B 插件 + GPU
    特性: 推理延迟 ↓60%，内置 GPU 支持
  elif 低延迟需求 and 有 GPU:
    使用: GPU 加速（必须）
  elif 高吞吐量需求 and 有 GPU:
    使用: GPU 加速（推荐）
  else: CPU 推理（可选）
```

## 08.9 形式化总结

### 08.9.1 AI 推理延迟模型形式化

**推理延迟函数**：
$$L_{\text{total}} = L_{\text{startup}} + L_{\text{inference}} + L_{\text{transfer}}$$

其中：

- $L_{\text{startup}}$ = 启动延迟（Wasm < 10ms，容器 > 1s）
- $L_{\text{inference}}$ = 推理延迟（Wasm 20-50ms，容器 50-100ms）
- $L_{\text{transfer}}$ = 数据传输延迟（边缘 < 云端）

**优化目标**：
$$\min_{W} L_{\text{total}} = \min_{W} (L_{\text{startup}} \downarrow + L_{\text{inference}} \downarrow + L_{\text{transfer}} \downarrow)$$

### 08.9.2 AI 推理成本模型形式化

**推理成本函数**：
$$C_{\text{total}} = C_{\text{storage}} + C_{\text{compute}} + C_{\text{transfer}}$$

其中：

- $C_{\text{storage}}$ = 存储成本（Wasm < 容器）
- $C_{\text{compute}}$ = 计算成本（Wasm < 容器）
- $C_{\text{transfer}}$ = 传输成本（Wasm < 容器）

**优化目标**：
$$\min_{W} C_{\text{total}} = \min_{W} (C_{\text{storage}} \downarrow + C_{\text{compute}} \downarrow + C_{\text{transfer}} \downarrow)$$

## 08.10 实际部署案例

### 08.10.1 案例 1：WasmEdge + Llama2 推理部署

**场景**：在 Kubernetes 集群中部署 WasmEdge + Llama2 推理服务

**部署步骤**：

```bash
# 1. 安装 WasmEdge（如果未安装）
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash

# 2. 创建 RuntimeClass（K8s 1.30+ 原生支持）
kubectl apply -f - <<EOF
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: wasm
handler: crun
EOF

# 3. 部署 Llama2 推理 Pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: llama2-inference
spec:
  runtimeClassName: wasm
  containers:
    - name: llama2
      image: wasmedge/llama2:latest
      command: ["wasmedge", "--dir", ".", "/llama2.wasm"]
      resources:
        requests:
          memory: "4Gi"
          cpu: "2"
        limits:
          memory: "8Gi"
          cpu: "4"
EOF
```

**GPU 加速配置**（如果有 GPU）：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: llama2-gpu-inference
spec:
  runtimeClassName: wasm
  containers:
    - name: llama2
      image: wasmedge/llama2:latest
      command: ["wasmedge", "--dir", ".", "/llama2.wasm"]
      resources:
        requests:
          memory: "4Gi"
          cpu: "2"
          nvidia.com/gpu: 1
        limits:
          memory: "8Gi"
          cpu: "4"
          nvidia.com/gpu: 1
```

### 08.10.2 案例 2：边缘 AI 推理部署

**场景**：在 K3s 边缘节点部署 AI 推理服务

**部署步骤**：

```bash
# 1. 在 K3s 节点上安装 WasmEdge
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash

# 2. 配置 K3s 使用 WasmEdge（K3s 1.30+）
# 方法1：使用 --wasm flag（推荐）
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.30.4+k3s1 \
  sh -s - --wasm --write-kubeconfig-mode 644

# 方法2：如果已安装 K3s，创建 RuntimeClass（K8s 1.30+）
# 注意：K3s 1.30+ 使用 --wasm flag 会自动创建 RuntimeClass=wasm
# 如果需要手动创建，确保 handler 为 crun
kubectl apply -f - <<EOF
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: wasm
handler: crun
EOF

# 3. 部署 AI 推理应用
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-inference
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-inference
  template:
    metadata:
      labels:
        app: ai-inference
    spec:
      runtimeClassName: wasm
      containers:
        - name: inference
          image: myregistry.com/ai-model:latest
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "1Gi"
              cpu: "1"
---
apiVersion: v1
kind: Service
metadata:
  name: ai-inference
spec:
  selector:
    app: ai-inference
  ports:
    - port: 8080
      targetPort: 8080
EOF
```

### 08.10.3 案例 3：模型 Wasm 化流程

**场景**：将 ONNX 模型转换为 Wasm 格式

**转换步骤**：

```bash
# 1. 安装模型转换工具
pip install onnxruntime-wasm

# 2. 转换 ONNX 模型到 Wasm
onnx2wasm model.onnx -o model.wasm

# 3. 构建包含模型的 OCI 镜像
cat > Dockerfile <<EOF
FROM scratch
COPY model.wasm /model.wasm
EOF

docker build -t myregistry.com/ai-model:v1.0.0 .

# 4. 推送镜像
docker push myregistry.com/ai-model:v1.0.0
```

## 08.11 AI 推理故障排查

### 08.11.1 常见问题

**问题 1：Wasm 模型加载失败**:

```bash
# 检查 WasmEdge 版本
wasmedge --version

# 检查模型文件
file model.wasm

# 检查 Pod 日志
kubectl logs <pod-name>

# 检查模型格式
wasmedge --version
```

**问题 2：推理延迟过高**:

```bash
# 检查资源使用
kubectl top pod <pod-name>

# 检查节点资源
kubectl describe node <node-name>

# 检查 GPU 使用（如果有 GPU）
nvidia-smi

# 优化建议：
# - 使用 GPU 加速
# - 优化模型大小
# - 增加资源限制
```

**问题 3：GPU 无法使用**:

```bash
# 检查 GPU 节点标签
kubectl get nodes -l nvidia.com/gpu.present=true

# 检查 GPU 驱动
nvidia-smi

# 检查 Device Plugin
kubectl get pods -n kube-system | grep nvidia-device-plugin

# 检查 Pod GPU 请求
kubectl describe pod <pod-name> | grep -i gpu
```

## 08.12 AI 推理最佳实践

### 08.12.1 模型 Wasm 化最佳实践

**模型选择**：

- ✅ 优先选择轻量级模型（< 1GB）进行 Wasm 化
- ✅ 使用 ONNX 格式模型，兼容性更好
- ✅ 避免使用过大模型（> 5GB），Wasm 内存限制
- ✅ 考虑模型精度和大小平衡

**模型优化**：

- ✅ 使用模型量化技术减少模型大小
- ✅ 移除不必要的层和参数
- ✅ 使用 WasmEdge TensorFlow Lite 插件优化推理
- ✅ 测试不同优化级别，选择最佳平衡点

**镜像构建**：

- ✅ 使用多阶段构建减小镜像大小
- ✅ 将模型文件单独层，支持缓存
- ✅ 使用 `scratch` 基础镜像，最小化镜像体积
- ✅ 添加 OCI 注释标识 Wasm 镜像

### 08.12.2 GPU 集成最佳实践

**GPU 资源管理**：

- ✅ 使用 Node Feature Discovery 自动识别 GPU 节点
- ✅ 配置 RuntimeClass 的 nodeSelector 调度到 GPU 节点
- ✅ 合理设置 GPU 资源请求，避免资源浪费
- ✅ 监控 GPU 使用率，优化资源分配

**性能优化**：

- ✅ 使用 WasmEdge GPU 插件加速推理
- ✅ 配置 GPU 内存预分配，减少分配开销
- ✅ 使用批处理减少 GPU 调用次数
- ✅ 监控 GPU 温度和功耗，避免过热

**兼容性**：

- ✅ 检查 GPU 驱动版本兼容性
- ✅ 测试不同 GPU 型号的兼容性
- ✅ 提供 CPU fallback 方案
- ✅ 文档化 GPU 要求和限制

### 08.12.3 边缘 AI 推理最佳实践

**资源规划**：

- ✅ 根据边缘节点资源限制配置 Pod 资源
- ✅ 使用 `runtimeClassName: wasm` 减少资源占用
- ✅ 设置合理的副本数，避免资源耗尽
- ✅ 使用本地存储，减少网络依赖

**离线能力**：

- ✅ 配置本地镜像仓库，支持离线部署
- ✅ 模型文件存储在本地，避免网络拉取
- ✅ 配置健康检查和自动重启策略
- ✅ 测试离线场景下的推理能力

**延迟优化**：

- ✅ 使用 Wasm 运行时，冷启动 < 10ms
- ✅ 预热模型减少首次推理延迟
- ✅ 使用 GPU 加速（如果可用）
- ✅ 监控推理延迟，优化模型和配置

### 08.12.4 AI 推理检查清单

**部署前检查**：

- [ ] 模型文件已准备（ONNX/TFLite 格式）
- [ ] WasmEdge 运行时已正确安装和配置
- [ ] RuntimeClass `wasm` 已创建
- [ ] GPU 节点标签已配置（如需要 GPU）
- [ ] GPU Device Plugin 已安装（如需要 GPU）
- [ ] 资源请求和限制已合理配置
- [ ] 存储类配置完成（如需要持久化存储）

**运行时检查**：

- [ ] Pod 正常运行，无异常状态
- [ ] 模型加载成功，无错误日志
- [ ] 推理延迟符合预期（< 50ms）
- [ ] GPU 使用正常（如使用 GPU）
- [ ] 资源使用率在合理范围内
- [ ] 监控指标正常收集

**性能优化检查**：

- [ ] 冷启动时间 < 10ms
- [ ] 推理延迟 < 50ms（边缘场景）
- [ ] GPU 利用率 > 50%（如使用 GPU）
- [ ] 内存使用率 < 80%
- [ ] CPU 使用率在合理范围内

**故障排查准备**：

- [ ] 日志收集配置完成
- [ ] 监控告警规则配置完成
- [ ] 备份和恢复策略已制定
- [ ] 故障排查文档已准备

---

## 08.13 参考

### 08.13.1 隔离栈相关文档

- **[29. 隔离栈](../29-isolation-stack/isolation-stack.md)** - 完整的隔离栈技术
  解析，包括 AI 推理应用场景
- **[L-4 沙盒化层](../29-isolation-stack/layers/L-4-sandboxing.md)** - WASM 运行
  时详细文档，包含边缘 AI 推理最佳实践
- **[隔离层次对比文档](../29-isolation-stack/layers/isolation-comparison.md)** -
  WASM 性能对比和应用场景匹配

### 08.13.2 AI 推理相关文档

- **[03. WasmEdge](../03-wasm-edge/wasmedge.md)** - WasmEdge 技术规范
- **[07. 边缘与 Serverless](../07-edge-serverless/edge-serverless.md)** - 边缘计
  算和 Serverless 场景
- **[10. 安装部署](../10-installation/installation.md)** - 安装和部署指南

### 08.13.3 其他相关文档

- **[10. 快速参考指南](../../COGNITIVE/10-decision-models/QUICK-REFERENCE.md)** -
  设备访问（USB/PCI/GPU）和内核特性决策快速参考
- **[28. 架构框架](../28-architecture-framework/architecture-framework.md)** -
  多维度架构体系与技术规范

---

**最后更新**：2025-11-06 **维护者**：项目团队
