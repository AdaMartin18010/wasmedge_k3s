# WASM 化 API 规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 核心 WASM API 规范](#11-核心-wasm-api-规范)
  - [1.2 WASM API 层次](#12-wasm-api-层次)
  - [1.3 WASM 化在 API 规范中的位置](#13-wasm-化在-api-规范中的位置)
- [2. WASI Preview 2 接口](#2-wasi-preview-2-接口)
  - [2.1 WASI Preview 2 核心接口](#21-wasi-preview-2-核心接口)
  - [2.2 WASI 能力模型](#22-wasi-能力模型)
- [3. WIT 组件模型](#3-wit-组件模型)
  - [3.1 WIT 接口定义](#31-wit-接口定义)
  - [3.2 WIT 组件组合](#32-wit-组件组合)
- [4. WasmEdge API](#4-wasmedge-api)
- [5. wasmCloud Lattice API](#5-wasmcloud-lattice-api)
- [6. WASM 组件组合 API](#6-wasm-组件组合-api)
- [7. API 演进路径](#7-api-演进路径)
  - [7.1 WASM API 演进时间线](#71-wasm-api-演进时间线)
  - [7.2 Kubernetes WASM 支持演进](#72-kubernetes-wasm-支持演进)
- [8. 形式化定义与理论基础](#8-形式化定义与理论基础)
  - [8.1 WASM API 规范形式化](#81-wasm-api-规范形式化)
  - [8.2 组件模型形式化](#82-组件模型形式化)
  - [8.3 能力模型形式化](#83-能力模型形式化)
  - [8.4 WASM 安全性形式化](#84-wasm-安全性形式化)
- [9. 相关文档](#9-相关文档)

---

## 1. 概述

WASM 化 API 规范代表了 API 设计的最新范式，从 WASI 系统接口到 WIT 组件模型，实现
了跨语言、跨平台的 API 标准化。本文档基于形式化方法，提供严格的数学定义和推理论
证，确保 WASM 化 API 的正确性和可验证性。

### 1.1 核心 WASM API 规范

| API 规范              | 标准组织 | 版本   | 核心内容            |
| --------------------- | -------- | ------ | ------------------- |
| **WASI Preview 1**    | W3C      | 2020   | 基础系统接口        |
| **WASI Preview 2**    | W3C      | 2023   | 组件模型接口        |
| **WIT**               | W3C      | 2023   | 组件接口定义        |
| **WasmEdge API**      | CNCF     | 0.14.0 | WasmEdge 运行时 API |
| **wasmCloud Lattice** | CNCF     | 0.80+  | 分布式组件 API      |

### 1.2 WASM API 层次

```text
应用层 API
  ↓
WIT 组件接口 (Component Model)
  ↓
WASI 系统接口 (Preview 2)
  ↓
WASM 运行时 API (WasmEdge, Wasmtime)
  ↓
宿主环境 API (Kubernetes, Edge)
```

**参考标准**：

- [WebAssembly Core Specification](https://webassembly.github.io/spec/core/) -
  WebAssembly 核心规范
- [WASI Preview 2](https://github.com/WebAssembly/WASI) - WebAssembly 系统接口
- [WIT Specification](https://github.com/WebAssembly/component-model/blob/main/design/mvp/WIT.md) -
  WebAssembly Interface Types
- [WasmEdge](https://wasmedge.org/) - CNCF 云原生 WASM 运行时
- [wasmCloud](https://wasmcloud.com/) - CNCF 分布式 WASM 平台

### 1.3 WASM 化在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../07-formalization/formalization.md#21-api-规范四元组)）
，WASM 化 API 属于 **IDL** 和 **Security** 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
            ↑                                    ↑
    WASM API ∈ IDL ∩ Security
```

WASM 化 API 在 API 规范中提供：

- **IDL 层**：通过 WIT 定义跨语言的 API 接口，实现语言无关的 API 规范
- **Security 层**：通过 WASM 沙盒和能力模型实现强隔离和最小权限
- **可移植性**：WASM 模块可在不同平台和运行时之间移植
- **性能**：接近原生性能，适合边缘计算和云原生场景

---

## 2. WASI Preview 2 接口

### 2.1 WASI Preview 2 核心接口

**文件系统接口**：

```wit
// wasi:filesystem/types@0.2.0
interface types {
    record descriptor {
        // 文件描述符元数据
    }

    enum descriptor-type {
        block-device,
        character-device,
        directory,
        regular-file,
        socket,
        symbolic-link,
        unknown
    }
}

// wasi:filesystem/filesystem@0.2.0
interface filesystem {
    use types.{descriptor, descriptor-type};

    read-file: func(descriptor: descriptor) -> result<list<u8>, error-code>;
    write-file: func(descriptor: descriptor, contents: list<u8>) -> result<(), error-code>;
}
```

**网络接口**：

```wit
// wasi:sockets/tcp@0.2.0
interface tcp {
    use types.{ip-socket-address, network, tcp-socket};

    create-tcp-socket: func(address-family: ip-address-family) -> result<tcp-socket, error-code>;
    bind: func(this: tcp-socket, local-address: ip-socket-address) -> result<(), error-code>;
    connect: func(this: tcp-socket, remote-address: ip-socket-address) -> result<(), error-code>;
}
```

### 2.2 WASI 能力模型

**能力令牌（Capability Tokens）**：

```wit
// wasi:cli/environment@0.2.0
interface environment {
    get-environment: func() -> list<tuple<string, string>>;
    get-arguments: func() -> list<string>;
}

// 能力声明
world my-app {
    import wasi:cli/environment@0.2.0;
    import wasi:filesystem/filesystem@0.2.0;
    // 仅声明需要的接口，实现最小权限原则
}
```

---

## 3. WIT 组件模型

### 3.1 WIT 接口定义

**WIT 组件接口**：

```wit
// calculator.wit
package example:calculator;

interface calculator@1.0.0 {
    type error = variant {
        overflow,
        underflow,
        division-by-zero
    };

    add: func(a: u32, b: u32) -> result<u32, error>;
    subtract: func(a: u32, b: u32) -> result<u32, error>;
    multiply: func(a: u32, b: u32) -> result<u32, error>;
    divide: func(a: u32, b: u32) -> result<u32, error>;
}

world calculator-world {
    export calculator: self.calculator;
}
```

### 3.2 WIT 组件组合

**组件组合示例**：

```wit
// api-handler.wit
package example:api-handler;

interface http@0.1.0 {
    type request = record {
        method: string,
        path: string,
        headers: list<tuple<string, string>>,
        body: list<u8>
    };

    type response = record {
        status: u16,
        headers: list<tuple<string, string>>,
        body: list<u8>
    };
}

world api-handler {
    import calculator: example:calculator/calculator@1.0.0;
    import http: http@0.1.0;

    export handle: func(req: http.request) -> http.response;
}
```

### 3.3 WIT 版本化

**WIT 版本语义**：

```wit
// 主版本：不兼容变更
package example:calculator@2.0.0;

// 次版本：向后兼容的新功能
package example:calculator@1.1.0;

// 补丁版本：向后兼容的 bug 修复
package example:calculator@1.0.1;
```

---

## 4. WasmEdge API

### 4.1 WasmEdge Runtime API

**Rust API 示例**：

```rust
use wasmedge_sdk::{config::ConfigBuilder, VmBuilder, params};

// 创建 WasmEdge 虚拟机
let config = ConfigBuilder::default()
    .with_bulk_memory_operations(true)
    .with_reference_types(true)
    .with_tail_call(true)
    .build()?;

let vm = VmBuilder::default()
    .with_config(config)
    .build()?;

// 调用 WASM 函数
let result = vm.run_func(Some("main"), "add", params!(2, 3))?;
```

### 4.2 WasmEdge 0.14 新特性（2024）

**GPU 支持 API**：

```rust
use wasmedge_sdk::{config::ConfigBuilder, VmBuilder};

let config = ConfigBuilder::default()
    .with_gpu(true)  // 启用 GPU 支持
    .build()?;
```

**TensorFlow 推理 API**：

```rust
use wasmedge_tensorflow_interface;

let result = wasmedge_tensorflow_interface::run(
    &model_bytes,
    &input_tensors,
    &output_names
)?;
```

### 4.3 WasmEdge Kubernetes 集成

**RuntimeClass 配置**：

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: wasmedge
handler: wasmedge
overhead:
  podFixed:
    memory: "64Mi"
    cpu: "50m"
```

---

## 5. wasmCloud Lattice API

### 5.1 Lattice 组件通信 API

**wasmCloud Lattice** 提供了分布式组件通信 API：

```rust
use wasmcloud_interface_httpserver::{HttpRequest, HttpResponse, HttpServer};

// HTTP 服务器组件
#[async_trait]
impl HttpServer for MyComponent {
    async fn handle_request(&self, req: &HttpRequest) -> HttpResponse {
        // 处理 HTTP 请求
        HttpResponse {
            status_code: 200,
            body: b"Hello, wasmCloud!".to_vec(),
            ..Default::default()
        }
    }
}
```

### 5.2 Lattice 组件发现 API

**组件注册和发现**：

```bash
# 注册组件
wash ctl link put \
  wasmcloud.azurecr.io/httpserver:0.18.0 \
  wasmcloud.azurecr.io/kvredis:0.18.0 \
  --link-name default

# 查询组件
wash ctl get hosts
wash ctl get links
```

---

## 6. WASM 组件组合 API

### 6.1 组件导入/导出 API

**组件导入**：

```wit
world my-world {
    import wasi:http/incoming-handler@0.2.0;
    import wasi:keyvalue/readwrite@0.2.0;

    export my-handler: func(req: incoming-request) -> response;
}
```

**组件导出**：

```rust
use wasi::http::incoming_handler::{IncomingHandler, IncomingRequest, Response};

struct MyHandler;

impl IncomingHandler for MyHandler {
    fn handle(&mut self, request: IncomingRequest) -> Response {
        // 处理请求
        Response::new(200, vec![], b"OK".to_vec())
    }
}

export!(MyHandler);
```

### 6.2 组件组合模式

**适配器模式**：

```wit
// adapter.wit
world adapter {
    import old-api: old:api@1.0.0;
    export new-api: new:api@2.0.0;
}
```

**Facade 模式**：

```wit
// facade.wit
world facade {
    import service1: service1@1.0.0;
    import service2: service2@1.0.0;
    import service3: service3@1.0.0;

    export unified-api: unified:api@1.0.0;
}
```

---

## 7. API 演进路径

### 7.1 WASM API 演进时间线

```text
WebAssembly 1.0 (2017)
  ↓
WASI Preview 1 (2020)
  ↓
Component Model Proposal (2021)
  ↓
WIT 0.1 (2022)
  ↓
WASI Preview 2 (2023)
  ↓
WIT 0.2 (2024)
  ↓
WASI Preview 3 (2025 预计)
```

### 7.2 Kubernetes WASM 支持演进

| 版本   | WASM 支持                    | 时间 |
| ------ | ---------------------------- | ---- |
| v1.20  | RuntimeClass 实验性支持      | 2020 |
| v1.25  | RuntimeClass WASM 支持       | 2022 |
| v1.30  | RuntimeClass 增强，WASM 优化 | 2024 |
| v1.32+ | 原生 WASM 支持（预计）       | 2025 |

---

## 8. 形式化定义与理论基础

### 8.1 WASM API 规范形式化

**定义 8.1（WASM API 规范）**：WASM API 规范是一个三元组：

```text
WASM_API = ⟨WASI, WIT, Runtime_API⟩
```

其中：

- **WASI**：WebAssembly System Interface `WASI: SystemCall → Result`
- **WIT**：WebAssembly Interface Types `WIT: Interface → Type`
- **Runtime_API**：WASM 运行时 API `Runtime: Module → Execution`

**定义 8.2（WASM 模块）**：WASM 模块是一个三元组：

```text
Module = ⟨Code, Import, Export⟩
```

其中：

- **Code**：WASM 字节码
- **Import**：导入接口集合 `Import = {i₁, i₂, ..., iₙ}`
- **Export**：导出接口集合 `Export = {e₁, e₂, ..., eₘ}`

### 8.2 组件模型形式化

**定义 8.3（WIT 组件）**：WIT 组件是一个四元组：

```text
Component = ⟨World, Import, Export, Type⟩
```

其中：

- **World**：组件世界定义 `World: ComponentName → Interface`
- **Import**：导入接口集合 `Import = {I₁, I₂, ..., Iₙ}`
- **Export**：导出接口集合 `Export = {E₁, E₂, ..., Eₘ}`
- **Type**：类型定义集合 `Type = {T₁, T₂, ..., Tₖ}`

**定义 8.4（组件组合）**：组件组合是一个函数：

```text
Compose: Component₁ × Component₂ → Component_combined
```

其中 `Compose(C₁, C₂)` 将两个组件组合成一个新组件。

**定理 8.1（组件组合可结合性）**：组件组合是可结合的：

```text
Compose(Compose(C₁, C₂), C₃) = Compose(C₁, Compose(C₂, C₃))
```

**证明**：组件组合是函数组合，函数组合是可结合的。□

### 8.3 能力模型形式化

**定义 8.5（WASI 能力）**：WASI 能力是一个函数：

```text
Capability: Component → Set(CapabilityToken)
```

其中 `Capability(Component) = {c₁, c₂, ..., cₙ}`，每个 `cᵢ` 是一个能力令牌。

**定义 8.6（能力依赖）**：组件 C₁ 依赖组件 C₂，当且仅当：

```text
Depends(C₁, C₂) = Capability(C₁) ∩ Capability(C₂) ≠ ∅
```

**定理 8.2（最小权限原则）**：组件只声明必要的能力：

```text
∀ Component: Capability(Component) = Minimal_Set(Required_Operations)
```

**证明**：根据 WASI 能力模型的设计原则，组件只声明执行任务所需的最小能力集合。□

**定理 8.3（能力传递性）**：如果组件 C₁ 依赖 C₂，C₂ 依赖 C₃，则 C₁ 间接依赖 C₃：

```text
Depends(C₁, C₂) ∧ Depends(C₂, C₃) ⟹ Depends(C₁, C₃)
```

**证明**：根据定义 8.6，如果 `Capability(C₁) ∩ Capability(C₂) ≠ ∅` 且
`Capability(C₂) ∩ Capability(C₃) ≠ ∅`，则
`Capability(C₁) ∩ Capability(C₃) ≠ ∅`。□

### 8.4 WASM 安全性形式化

**定义 8.7（WASM 沙盒）**：WASM 沙盒是一个函数：

```text
Sandbox: Module × Policy → Execution
```

其中 `Policy` 是安全策略，`Execution` 是受限的执行环境。

**定义 8.8（内存安全）**：WASM 模块是内存安全的，当且仅当：

```text
Memory_Safe(Module) = ∀ access: Valid(access) ∧ Bounds_Check(access)
```

即所有内存访问都是有效的且在边界内。

**定理 8.4（WASM 内存安全）**：所有有效的 WASM 模块都是内存安全的：

```text
Valid(Module) ⟹ Memory_Safe(Module)
```

**证明**：根据 WebAssembly 规范，WASM 运行时在加载和执行模块时进行边界检查，确保
所有内存访问都在有效范围内。□

**定义 8.9（类型安全）**：WASM 模块是类型安全的，当且仅当：

```text
Type_Safe(Module) = ∀ operation: Type(operand) = Expected_Type(operation)
```

**定理 8.5（WASM 类型安全）**：所有有效的 WASM 模块都是类型安全的：

```text
Valid(Module) ⟹ Type_Safe(Module)
```

**证明**：根据 WebAssembly 规范，WASM 运行时在验证阶段检查所有操作的类型，确保类
型匹配。□

**定理 8.6（WASM 隔离性）**：WASM 模块相互隔离：

```text
∀ M₁, M₂: M₁ ≠ M₂ ⟹ Isolation(M₁, M₂)
```

**证明**：根据 WebAssembly 规范，每个 WASM 模块有独立的内存空间和执行上下文，因
此相互隔离。□

---

## 9. 相关文档

- **[WebAssembly 抽象层](../../ARCHITECTURE/architecture-view/02-virtualization-containerization-sandboxing/06-webassembly-abstraction.md)**
  ⭐ - WASM 组件模型与 WASI 接口详解
- **[WasmEdge 集成指南](../../TECHNICAL/03-wasm-edge/)** - WasmEdge API 实践指南
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新**：2025-11-07 **维护者**：项目团队
