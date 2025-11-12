# WASI Preview 2 接口使用示例

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 核心接口](#11-核心接口)
- [2 文件系统接口](#2-文件系统接口)
  - [2.1 Rust 示例](#21-rust-示例)
  - [2.2 Go 示例](#22-go-示例)
- [3 网络接口](#3-网络接口)
  - [3.1 Rust 示例](#31-rust-示例)
  - [3.2 Go 示例](#32-go-示例)
- [4 进程接口](#4-进程接口)
  - [4.1 Rust 示例](#41-rust-示例)
  - [4.2 Go 示例](#42-go-示例)
- [5 随机数和时钟接口](#5-随机数和时钟接口)
  - [5.1 Rust 示例](#51-rust-示例)
  - [5.2 Go 示例](#52-go-示例)
- [6 相关文档](#6-相关文档)
  - [6.1 其他实现细节文档](#61-其他实现细节文档)
  - [6.2 架构视角文档](#62-架构视角文档)
  - [6.3 WASI 官方文档](#63-wasi-官方文档)

---

## 1 概述

**WASI Preview 2** 是 WebAssembly System Interface 的最新版本（2024 年发布，2025
年广泛采用），提供了标准化的系统调用接口。

### 1.1 核心接口

- **文件系统**：`wasi:filesystem` - 文件读写接口
- **网络**：`wasi:sockets` - TCP/UDP 网络接口
- **进程**：`wasi:process` - 进程管理接口
- **随机数**：`wasi:random` - 随机数生成接口
- **时钟**：`wasi:clocks` - 时间接口

---

## 2 文件系统接口

### 2.1 Rust 示例

**依赖配置**（`Cargo.toml`）：

```toml
[package]
name = "wasi-example"
version = "0.1.0"
edition = "2021"

[dependencies]
wasi = "0.2"

[target.'cfg(target_arch = "wasm32")'.dependencies]
wasi = { version = "0.2", features = ["filesystem"] }
```

**文件读写示例**：

```rust
use wasi::filesystem::preopens::get_directories;
use wasi::filesystem::types::{Descriptor, OpenFlags, Rights};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 获取预打开的目录
    let dirs = get_directories();

    // 打开文件
    let file = dirs.open_at(
        "/tmp",
        "test.txt",
        OpenFlags::CREATE | OpenFlags::WRITE,
        Rights::READ | Rights::WRITE,
    )?;

    // 写入数据
    let data = b"Hello, WASI!";
    file.write(data)?;

    // 读取数据
    let mut buffer = vec![0; 1024];
    let bytes_read = file.read(&mut buffer)?;
    println!("Read {} bytes", bytes_read);

    Ok(())
}
```

### 2.2 Go 示例

**文件读写示例**：

```go
package main

import (
    "os"
    "io"
)

func main() {
    // 打开文件
    file, err := os.OpenFile("/tmp/test.txt", os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        panic(err)
    }
    defer file.Close()

    // 写入数据
    _, err = file.WriteString("Hello, WASI!")
    if err != nil {
        panic(err)
    }

    // 读取数据
    data, err := os.ReadFile("/tmp/test.txt")
    if err != nil {
        panic(err)
    }
    println(string(data))
}
```

---

## 3 网络接口

### 3.1 Rust 示例

**HTTP 服务器示例**：

```rust
use wasi::sockets::tcp::{TcpSocket, TcpListener};
use wasi::sockets::ip::{IpAddress, Ipv4Address};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 创建 TCP 监听器
    let listener = TcpListener::bind(Ipv4Address::new(127, 0, 0, 1), 8080)?;

    println!("Listening on 127.0.0.1:8080");

    loop {
        // 接受连接
        let stream = listener.accept()?;

        // 处理请求
        let mut buffer = vec![0; 1024];
        let bytes_read = stream.read(&mut buffer)?;

        // 发送响应
        let response = b"HTTP/1.1 200 OK\r\n\r\nHello, WASI!";
        stream.write(response)?;
    }
}
```

### 3.2 Go 示例

**HTTP 服务器示例**：

```go
package main

import (
    "net"
    "io"
)

func main() {
    // 监听端口
    listener, err := net.Listen("tcp", ":8080")
    if err != nil {
        panic(err)
    }
    defer listener.Close()

    println("Listening on :8080")

    for {
        // 接受连接
        conn, err := listener.Accept()
        if err != nil {
            continue
        }

        // 处理请求
        go handleConnection(conn)
    }
}

func handleConnection(conn net.Conn) {
    defer conn.Close()

    // 读取请求
    buffer := make([]byte, 1024)
    _, err := conn.Read(buffer)
    if err != nil {
        return
    }

    // 发送响应
    response := "HTTP/1.1 200 OK\r\n\r\nHello, WASI!"
    conn.Write([]byte(response))
}
```

---

## 4 进程接口

### 4.1 Rust 示例

**环境变量和参数**：

```rust
use wasi::process::environ;

fn main() {
    // 获取环境变量
    let env_vars = environ::get_env();
    for (key, value) in env_vars {
        println!("{}={}", key, value);
    }

    // 获取命令行参数
    let args = environ::get_args();
    for arg in args {
        println!("Arg: {}", arg);
    }
}
```

### 4.2 Go 示例

**环境变量和参数**：

```go
package main

import (
    "os"
)

func main() {
    // 获取环境变量
    for _, env := range os.Environ() {
        println(env)
    }

    // 获取命令行参数
    for _, arg := range os.Args {
        println("Arg:", arg)
    }
}
```

---

## 5 随机数和时钟接口

### 5.1 Rust 示例

**随机数生成**：

```rust
use wasi::random::random;

fn main() {
    // 生成随机字节
    let mut buffer = vec![0u8; 16];
    random::get_random_bytes(&mut buffer);

    println!("Random bytes: {:?}", buffer);
}
```

**时钟接口**：

```rust
use wasi::clocks::monotonic_clock;
use std::time::Duration;

fn main() {
    // 获取单调时钟
    let now = monotonic_clock::now();
    println!("Monotonic time: {:?}", now);

    // 休眠
    monotonic_clock::sleep(Duration::from_secs(1));
}
```

### 5.2 Go 示例

**随机数生成**：

```go
package main

import (
    "crypto/rand"
    "fmt"
)

func main() {
    // 生成随机字节
    buffer := make([]byte, 16)
    rand.Read(buffer)
    fmt.Println("Random bytes:", buffer)
}
```

**时钟接口**：

```go
package main

import (
    "time"
)

func main() {
    // 获取当前时间
    now := time.Now()
    println("Current time:", now.String())

    // 休眠
    time.Sleep(time.Second)
}
```

---

## 6 相关文档

### 6.1 其他实现细节文档

- [`wasmedge-setup.md`](wasmedge-setup.md) - WasmEdge 安装和配置
- [`wasm-compilation.md`](wasm-compilation.md) - Wasm 编译示例
- [`kubernetes-integration.md`](kubernetes-integration.md) - Kubernetes 集成

### 6.2 架构视角文档

- [`../../02-views/10-quick-views/webassembly-view.md`](../../02-views/10-quick-views/webassembly-view.md) -
  WebAssembly 架构视角

### 6.3 WASI 官方文档

- [WASI Preview 2 规范](https://github.com/WebAssembly/WASI)
- [WASI API 文档](https://docs.rs/wasi/)

---

**更新时间**：2025-11-05 **版本**：v1.0 **参考**：WASI Preview 2 规范
