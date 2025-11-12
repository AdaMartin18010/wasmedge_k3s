# Wasm 编译示例

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 编译目标](#11-编译目标)
- [2 Rust 编译](#2-rust-编译)
  - [2.1 基本配置](#21-基本配置)
  - [2.2 编译命令](#22-编译命令)
  - [2.3 示例代码](#23-示例代码)
- [3 Go 编译](#3-go-编译)
  - [3.1 基本配置](#31-基本配置)
  - [3.2 编译命令](#32-编译命令)
  - [3.3 示例代码](#33-示例代码)
- [4 C/C++ 编译](#4-cc-编译)
  - [4.1 安装 wasi-sdk](#41-安装-wasi-sdk)
  - [4.2 编译命令](#42-编译命令)
  - [4.3 示例代码](#43-示例代码)
- [5 AssemblyScript 编译](#5-assemblyscript-编译)
  - [5.1 安装 AssemblyScript](#51-安装-assemblyscript)
  - [5.2 编译命令](#52-编译命令)
  - [5.3 示例代码](#53-示例代码)
- [6 相关文档](#6-相关文档)
  - [6.1 其他实现细节文档](#61-其他实现细节文档)
  - [6.2 架构视角文档](#62-架构视角文档)
  - [6.3 编译工具文档](#63-编译工具文档)

---

## 1 概述

本文档提供多种语言的 WebAssembly 编译示例，包括 Rust、Go、C/C++、AssemblyScript
等。

### 1.1 编译目标

- **目标平台**：`wasm32-wasi`
- **WASI 版本**：WASI Preview 2
- **优化选项**：减小二进制体积，提升性能

---

## 2 Rust 编译

### 2.1 基本配置

**项目结构**：

```bash
my-wasm-app/
├── Cargo.toml
└── src/
    └── main.rs
```

**Cargo.toml**：

```toml
[package]
name = "my-wasm-app"
version = "0.1.0"
edition = "2021"

[dependencies]
wasi = "0.2"

[target.'cfg(target_arch = "wasm32")'.dependencies]
wasi = { version = "0.2", features = ["filesystem", "sockets"] }
```

### 2.2 编译命令

**基本编译**：

```bash
# 添加 wasm32-wasi 目标
rustup target add wasm32-wasi

# 编译
cargo build --target wasm32-wasi --release
```

**优化编译**：

```bash
# 启用 LTO（链接时优化）
RUSTFLAGS="-C lto=fat" cargo build --target wasm32-wasi --release

# 减小二进制体积
RUSTFLAGS="-C opt-level=z -C lto=fat" cargo build --target wasm32-wasi --release

# 使用 wasm-opt 进一步优化
wasm-opt -Os target/wasm32-wasi/release/my-wasm-app.wasm -o app.wasm
```

### 2.3 示例代码

**main.rs**：

```rust
use wasi::filesystem::preopens::get_directories;

fn main() {
    println!("Hello, WebAssembly!");

    let dirs = get_directories();
    println!("Pre-opened directories: {:?}", dirs);
}
```

---

## 3 Go 编译

### 3.1 基本配置

**Go 版本要求**：Go 1.21+

**环境变量**：

```bash
export GOOS=wasip1
export GOARCH=wasm
```

### 3.2 编译命令

**基本编译**：

```bash
# 编译为 Wasm
GOOS=wasip1 GOARCH=wasm go build -o app.wasm main.go
```

**优化编译**：

```bash
# 减小二进制体积
GOOS=wasip1 GOARCH=wasm go build -ldflags="-s -w" -o app.wasm main.go

# 使用 wasm-opt 优化
wasm-opt -Os app.wasm -o app.wasm
```

### 3.3 示例代码

**main.go**：

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    fmt.Println("Hello, WebAssembly!")

    // 获取环境变量
    for _, env := range os.Environ() {
        fmt.Println(env)
    }
}
```

---

## 4 C/C++ 编译

### 4.1 安装 wasi-sdk

**下载 wasi-sdk**：

```bash
# 下载 wasi-sdk 20.0
wget https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-20/wasi-sdk-20.0-linux.tar.gz
tar -xzf wasi-sdk-20.0-linux.tar.gz
export WASI_SDK_PATH=$(pwd)/wasi-sdk-20.0
```

### 4.2 编译命令

**C 编译**：

```bash
# 基本编译
$WASI_SDK_PATH/bin/clang \
    --target=wasm32-wasi \
    --sysroot=$WASI_SDK_PATH/share/wasi-sysroot \
    -o app.wasm \
    app.c

# 优化编译
$WASI_SDK_PATH/bin/clang \
    --target=wasm32-wasi \
    --sysroot=$WASI_SDK_PATH/share/wasi-sysroot \
    -Oz \
    -flto \
    -o app.wasm \
    app.c
```

**C++ 编译**：

```bash
# 基本编译
$WASI_SDK_PATH/bin/clang++ \
    --target=wasm32-wasi \
    --sysroot=$WASI_SDK_PATH/share/wasi-sysroot \
    -o app.wasm \
    app.cpp

# 优化编译
$WASI_SDK_PATH/bin/clang++ \
    --target=wasm32-wasi \
    --sysroot=$WASI_SDK_PATH/share/wasi-sysroot \
    -Oz \
    -flto \
    -o app.wasm \
    app.cpp
```

### 4.3 示例代码

**app.c**：

```c
#include <stdio.h>

int main() {
    printf("Hello, WebAssembly!\n");
    return 0;
}
```

**app.cpp**：

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, WebAssembly!" << std::endl;
    return 0;
}
```

---

## 5 AssemblyScript 编译

### 5.1 安装 AssemblyScript

```bash
# 初始化项目
npm init -y
npm install --save-dev assemblyscript

# 初始化 AssemblyScript 项目
npx asinit .
```

### 5.2 编译命令

**基本编译**：

```bash
# 编译
npm run asbuild

# 优化编译
npm run asbuild:optimized
```

### 5.3 示例代码

**assembly/index.ts**：

```typescript
export function add(a: i32, b: i32): i32 {
  return a + b;
}

export function fibonacci(n: i32): i32 {
  if (n <= 1) {
    return n;
  }
  return fibonacci(n - 1) + fibonacci(n - 2);
}
```

**package.json**：

```json
{
  "scripts": {
    "asbuild:untouched": "asc assembly/index.ts --target debug",
    "asbuild:optimized": "asc assembly/index.ts --target release",
    "asbuild": "npm run asbuild:untouched && npm run asbuild:optimized"
  }
}
```

---

## 6 相关文档

### 6.1 其他实现细节文档

- [`wasmedge-setup.md`](wasmedge-setup.md) - WasmEdge 安装和配置
- [`wasi-examples.md`](wasi-examples.md) - WASI 接口使用示例
- [`kubernetes-integration.md`](kubernetes-integration.md) - Kubernetes 集成

### 6.2 架构视角文档

- [`../../02-views/10-quick-views/webassembly-view.md`](../../02-views/10-quick-views/webassembly-view.md) -
  WebAssembly 架构视角

### 6.3 编译工具文档

- [Rust wasm32-wasi 文档](https://doc.rust-lang.org/stable/nightly-rustc/rustc_target/spec/wasm32_wasi/index.html)
- [Go WebAssembly 文档](https://pkg.go.dev/cmd/go/internal/buildid)
- [wasi-sdk 文档](https://github.com/WebAssembly/wasi-sdk)
- [AssemblyScript 文档](https://www.assemblyscript.org/)

---

**更新时间**：2025-11-05 **版本**：v1.0 **参考**：各语言 WebAssembly 官方文档
