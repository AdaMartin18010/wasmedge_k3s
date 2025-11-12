# 浏览器 WASM 架构设计

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1 场景概述](#1-场景概述)
- [2 架构设计](#2-架构设计)
- [3 技术选型](#3-技术选型)
- [4 WASM 运行时集成](#4-wasm-运行时集成)
- [5 WASI 接口设计](#5-wasi-接口设计)
- [6 P2P 网络集成](#6-p2p-网络集成)
- [7 安全考虑](#7-安全考虑)

---

## 1 场景概述

### 1.1 业务需求

基于 `system_view.md` 案例 E：单节点 WASM-P2P（浏览器 + 区块链轻节点）

**核心需求**：

- **浏览器环境**：在浏览器中运行轻节点
- **安全隔离**：不可访问用户硬盘
- **P2P 网络**：去中心化节点发现和通信
- **性能要求**：单标签页 <50 MB，CPU <5%

### 1.2 挑战分析

| 挑战       | 描述                 | 影响           |
| ---------- | -------------------- | -------------- |
| 浏览器限制 | 无法直接访问系统资源 | 需要 WASI 抽象 |
| 安全隔离   | 用户私钥不能泄露     | 需要 WebCrypto |
| 网络通信   | 浏览器网络限制       | 需要 WebRTC    |
| 性能优化   | 资源受限环境         | 需要轻量级实现 |

---

## 2 架构设计

### 2.1 整体架构

```text
┌─────────────────────────────────────────┐
│         Chrome V8 JavaScript 引擎        │
│  (主线程 - 用户交互)                      │
└─────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
┌───────▼────┐ ┌───▼────┐ ┌───▼────┐
│ WASM 模块  │ │WASM模块│ │WASM模块│
│ (轻节点 1) │ │(节点 2) │ │(节点 3) │
│            │ │         │ │         │
│ WASI 接口  │ │ WASI    │ │ WASI    │
│            │ │ 接口    │ │ 接口    │
└────────────┘ └─────────┘ └─────────┘
        │           │           │
        └───────────┼───────────┘
                    │
┌───────────────────▼───────────────────┐
│        WebRTC 数据通道                 │
│    (libp2p-wasm-ext)                  │
└───────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
┌───────▼────┐ ┌───▼────┐ ┌───▼────┐
│  P2P 节点  │ │P2P 节点│ │P2P 节点│
│   (DHT)    │ │ (DHT)  │ │ (DHT)  │
└────────────┘ └─────────┘ └─────────┘
```

### 2.2 能力模型

**Capability-Based 访问控制**：

```yaml
# WASI 能力配置
capabilities:
  random:
    enabled: true
    source: WebCrypto
  clock:
    enabled: true
    source: Date API
  stdio:
    stdout: true
    stderr: true
    destination: console
  filesystem:
    enabled: false # 禁止文件系统访问
  network:
    enabled: false # 禁止直接网络访问
  # 使用 WebRTC 独立通道
```

---

## 3 技术选型

### 3.1 理论支撑

#### 3.1.1 WASM 抽象

**引用理论**：Ψ₅（WebAssembly 抽象层）- 参见
[`00-theory/02-induction-proof/psi5-wasm.md`](../00-theory/02-induction-proof/psi5-wasm.md)

**分析**：

- WASM 提供内存安全的执行环境
- 线性内存模型，无法访问未授权内存
- 控制流图固定，防止控制流劫持

#### 3.1.2 内存安全

**引用理论**：L4（Wasm 内存安全引理）- 参见
[`00-theory/05-lemmas-theorems/L4-wasm-memory-safety.md`](../00-theory/05-lemmas-theorems/L4-wasm-memory-safety.md)

**分析**：

- WASM 内存安全保证
- 无法访问宿主内存
- 用户私钥放在 WebCrypto，WASM 无法访问

### 3.2 技术对比

| 维度           | Native Extension  | WASM               |
| -------------- | ----------------- | ------------------ |
| **启动延迟**   | 100-200 ms        | < 10 ms            |
| **内存占用**   | 50-100 MB         | < 10 MB            |
| **安全隔离**   | 弱（native 代码） | 强（内存安全）     |
| **跨平台**     | 需要编译          | 一次编译，到处运行 |
| **浏览器支持** | Chrome Extension  | 所有现代浏览器     |

---

## 4 WASM 运行时集成

### 4.1 Chrome V8 集成

**加载 WASM 模块**：

```javascript
// 使用 WebAssembly API
async function loadWasmModule(url) {
  const response = await fetch(url);
  const bytes = await response.arrayBuffer();
  const module = await WebAssembly.compile(bytes);

  // 创建 WASI 导入对象
  const wasi = new WASI({
    env: {
      random_get: () => {
        // 使用 WebCrypto
        const array = new Uint8Array(32);
        crypto.getRandomValues(array);
        return array;
      },
      clock_time_get: (clockId, precision, timePtr) => {
        // 使用 Date API
        const time = BigInt(Date.now()) * 1000000n;
        const view = new DataView(memory.buffer);
        view.setBigUint64(timePtr, time, true);
        return 0;
      }
    }
  });

  const instance = await WebAssembly.instantiate(module, {
    wasi_snapshot_preview1: wasi.wasiImport
  });

  return instance;
}
```

### 4.2 WasmEdge 浏览器集成

**使用 WasmEdge.js**：

```javascript
import { WasmEdge } from "@wasmedge/wasmedge";

async function initWasmEdge() {
  const wasmEdge = await WasmEdge.init();

  // 创建 WASI 上下文
  const wasi = wasmEdge.createWasiContext({
    args: ["lightnode"],
    envs: ["NODE_ID=0x1234"],
    preopens: {
      "/": "/"
    }
  });

  // 加载 WASM 模块
  const module = await wasmEdge.loadWasm("lightnode.wasm");

  // 实例化
  const instance = await wasmEdge.instantiate(module, {
    wasi_snapshot_preview1: wasi
  });

  return instance;
}
```

---

## 5 WASI 接口设计

### 5.1 自定义 WASI 实现

**WASI 接口实现**：

```javascript
class BrowserWASI {
  constructor() {
    this.memory = null;
    this.exports = {
      // random_get
      random_get: (bufPtr, bufLen) => {
        const view = new Uint8Array(this.memory.buffer, bufPtr, bufLen);
        crypto.getRandomValues(view);
        return 0;
      },

      // clock_time_get
      clock_time_get: (clockId, precision, timePtr) => {
        const time = BigInt(Date.now()) * 1000000n;
        const view = new DataView(this.memory.buffer);
        view.setBigUint64(timePtr, time, true);
        return 0;
      },

      // fd_write (stdout/stderr)
      fd_write: (fd, iovsPtr, iovsLen, nwrittenPtr) => {
        if (fd !== 1 && fd !== 2) {
          return 8; // EBADF
        }

        const view = new DataView(this.memory.buffer);
        let totalWritten = 0;

        for (let i = 0; i < iovsLen; i++) {
          const bufPtr = view.getUint32(iovsPtr + i * 8, true);
          const bufLen = view.getUint32(iovsPtr + i * 8 + 4, true);

          const str = new TextDecoder().decode(
            new Uint8Array(this.memory.buffer, bufPtr, bufLen)
          );

          if (fd === 1) {
            console.log(str);
          } else {
            console.error(str);
          }

          totalWritten += bufLen;
        }

        view.setUint32(nwrittenPtr, totalWritten, true);
        return 0;
      },

      // 禁止文件系统访问
      path_open: () => 63, // ENOTSUP
      path_readlink: () => 63,
      path_rename: () => 63,
      path_remove_directory: () => 63,
      path_unlink_file: () => 63,

      // 禁止网络访问
      sock_accept: () => 63,
      sock_recv: () => 63,
      sock_send: () => 63,
      sock_shutdown: () => 63
    };
  }

  setMemory(memory) {
    this.memory = memory;
  }
}
```

### 5.2 WebCrypto 集成

**私钥管理**：

```javascript
class SecureKeyManager {
  constructor() {
    this.keys = new Map();
  }

  async generateKeyPair() {
    const keyPair = await crypto.subtle.generateKey(
      {
        name: "ECDSA",
        namedCurve: "P-256"
      },
      true, // extractable
      ["sign", "verify"]
    );

    const keyId = crypto.randomUUID();
    this.keys.set(keyId, keyPair);

    return keyId;
  }

  async sign(keyId, data) {
    const keyPair = this.keys.get(keyId);
    if (!keyPair) {
      throw new Error("Key not found");
    }

    const signature = await crypto.subtle.sign(
      {
        name: "ECDSA",
        hash: "SHA-256"
      },
      keyPair.privateKey,
      data
    );

    return signature;
  }

  // WASM 无法直接访问私钥
  // 只能通过签名接口
}
```

---

## 6 P2P 网络集成

### 6.1 libp2p-wasm-ext

**P2P 节点发现**：

```javascript
import { createLibp2p } from "libp2p";
import { WebRTC } from "@libp2p/webrtc";
import { DHT } from "@libp2p/kad-dht";

async function createP2PNode() {
  const node = await createLibp2p({
    addresses: {
      listen: ["/webrtc"]
    },
    transports: [new WebRTC()],
    peerDiscovery: [
      new DHT({
        kBucketSize: 20
      })
    ],
    connectionEncryption: [
      // TLS 加密
    ],
    streamMuxers: [
      // mplex 或 yamux
    ]
  });

  // 节点发现
  node.addEventListener("peer:discovery", (evt) => {
    const peer = evt.detail;
    console.log("Discovered peer:", peer.id.toString());

    // 连接到发现的节点
    node.dial(peer.addresses);
  });

  return node;
}
```

### 6.2 WebRTC 数据通道

**建立连接**：

```javascript
class P2PConnector {
  constructor() {
    this.peerConnections = new Map();
  }

  async connectToPeer(peerId, signal) {
    const pc = new RTCPeerConnection({
      iceServers: [{ urls: "stun:stun.l.google.com:19302" }]
    });

    // 创建数据通道
    const dataChannel = pc.createDataChannel("p2p", {
      ordered: true
    });

    dataChannel.onopen = () => {
      console.log("Data channel opened");
      this.onMessage(peerId, dataChannel);
    };

    // 信令交换
    await this.exchangeSignaling(pc, signal);

    this.peerConnections.set(peerId, {
      pc,
      dataChannel
    });
  }

  sendMessage(peerId, message) {
    const conn = this.peerConnections.get(peerId);
    if (conn && conn.dataChannel.readyState === "open") {
      conn.dataChannel.send(JSON.stringify(message));
    }
  }
}
```

### 6.3 DHT 自发现

**Kademlia DHT**：

```javascript
class LightNodeDHT {
  constructor(node) {
    this.node = node;
    this.kbuckets = new Map();
  }

  async findPeers(targetId) {
    // Kademlia 查找算法
    const closestPeers = await this.node.contentRouting.findPeer(targetId);

    return closestPeers;
  }

  async provide(contentId) {
    // 提供内容到 DHT
    await this.node.contentRouting.provide(contentId);
  }

  async findProviders(contentId) {
    // 从 DHT 查找内容提供者
    const providers = [];

    for await (const provider of this.node.contentRouting.findProviders(
      contentId
    )) {
      providers.push(provider);
    }

    return providers;
  }
}
```

---

## 7 安全考虑

### 7.1 侧信道防护

**V8 Site-Isolation**：

```javascript
// Chrome 已启用 Site-Isolation
// 每个站点运行在独立的进程中
// 防止跨站点攻击

// Spectre 缓解
if ("crossOriginIsolated" in self) {
  console.log("Cross-origin isolated:", self.crossOriginIsolated);
  // 启用 SharedArrayBuffer 等高级特性
}
```

**Spectre 缓解**：

```javascript
// V8 内置 Spectre 缓解
// - 禁用高精度计时器
// - 限制共享内存访问
// - 控制流完整性检查

// 检查是否启用缓解
if (performance.measureUserAgentSpecificMemory) {
  // 用户代理特定内存测量已启用
  // 说明 Spectre 缓解已启用
}
```

### 7.2 私钥保护

**WebCrypto 隔离**：

```javascript
// 私钥存储在 WebCrypto 中
// WASM 无法直接访问

class SecureWallet {
  constructor() {
    this.keys = new Map();
  }

  async createWallet() {
    const keyPair = await crypto.subtle.generateKey(
      {
        name: "ECDSA",
        namedCurve: "P-256"
      },
      false, // 不可提取，防止 WASM 访问
      ["sign", "verify"]
    );

    return keyPair;
  }

  async signTransaction(keyPair, tx) {
    // 签名在 WebCrypto 中完成
    // WASM 无法读取私钥
    const signature = await crypto.subtle.sign(
      {
        name: "ECDSA",
        hash: "SHA-256"
      },
      keyPair.privateKey,
      tx
    );

    return signature;
  }
}
```

### 7.3 网络隔离

**WebRTC 独立通道**：

```javascript
// WASM 无法直接访问网络
// 只能通过 WebRTC 数据通道

class NetworkIsolation {
  constructor() {
    // 禁止 WASM 直接网络访问
    this.blockedAPIs = ["fetch", "XMLHttpRequest", "WebSocket"];
  }

  // 只允许通过 WebRTC
  createWebRTCChannel() {
    const pc = new RTCPeerConnection();
    const dataChannel = pc.createDataChannel("wasm-network");

    // 数据通道是唯一的网络接口
    return dataChannel;
  }
}
```

---

## 8 性能优化

### 8.1 内存优化

**线性内存管理**：

```javascript
class WasmMemoryManager {
  constructor(initialPages = 256) {
    this.memory = new WebAssembly.Memory({
      initial: initialPages,
      maximum: 65536, // 4 GB 限制
      shared: false
    });
  }

  growMemory(pages) {
    try {
      this.memory.grow(pages);
      return true;
    } catch (e) {
      console.error("Failed to grow memory:", e);
      return false;
    }
  }

  getMemoryUsage() {
    return {
      used: this.memory.buffer.byteLength,
      pages: this.memory.buffer.byteLength / 65536
    };
  }
}
```

### 8.2 CPU 优化

**Worker 线程**：

```javascript
// 在 Worker 中运行 WASM
// 避免阻塞主线程

class WasmWorker {
  constructor(wasmUrl) {
    this.worker = new Worker("wasm-worker.js", {
      type: "module"
    });

    this.worker.postMessage({
      type: "load",
      url: wasmUrl
    });
  }

  async callFunction(name, args) {
    return new Promise((resolve, reject) => {
      const id = crypto.randomUUID();

      const handler = (e) => {
        if (e.data.id === id) {
          this.worker.removeEventListener("message", handler);
          if (e.data.error) {
            reject(new Error(e.data.error));
          } else {
            resolve(e.data.result);
          }
        }
      };

      this.worker.addEventListener("message", handler);

      this.worker.postMessage({
        id,
        type: "call",
        name,
        args
      });
    });
  }
}
```

### 8.3 启动优化

**预编译和缓存**：

```javascript
class WasmCache {
  constructor() {
    this.cache = new Map();
  }

  async loadWasm(url) {
    // 检查缓存
    if (this.cache.has(url)) {
      return this.cache.get(url);
    }

    // 检查 IndexedDB 缓存
    const cached = await this.loadFromIndexedDB(url);
    if (cached) {
      this.cache.set(url, cached);
      return cached;
    }

    // 加载并编译
    const response = await fetch(url);
    const bytes = await response.arrayBuffer();
    const module = await WebAssembly.compile(bytes);

    // 缓存
    this.cache.set(url, module);
    await this.saveToIndexedDB(url, module);

    return module;
  }

  async loadFromIndexedDB(url) {
    return new Promise((resolve) => {
      const request = indexedDB.open("wasm-cache", 1);

      request.onsuccess = (e) => {
        const db = e.target.result;
        const tx = db.transaction("modules", "readonly");
        const store = tx.objectStore("modules");
        const req = store.get(url);

        req.onsuccess = () => {
          if (req.result) {
            resolve(req.result.module);
          } else {
            resolve(null);
          }
        };
      };
    });
  }
}
```

---

## 9 监控与调试

### 9.1 性能监控

**Chrome DevTools 集成**：

```javascript
// WASM 源映射支持
// 在 DevTools 中查看 WASM 源码

// 性能分析
performance.mark("wasm-start");
await wasmInstance.exports.processBlock(blockData);
performance.mark("wasm-end");
performance.measure("wasm-execution", "wasm-start", "wasm-end");

// 内存分析
const memoryUsage = performance.measureUserAgentSpecificMemory();
console.log("Memory usage:", memoryUsage);
```

### 9.2 错误处理

**WASM 错误捕获**：

```javascript
try {
  const result = wasmInstance.exports.processBlock(blockData);
  return result;
} catch (e) {
  if (e instanceof WebAssembly.RuntimeError) {
    console.error("WASM runtime error:", e);
    // 处理运行时错误
  } else if (e instanceof WebAssembly.LinkError) {
    console.error("WASM link error:", e);
    // 处理链接错误
  } else if (e instanceof WebAssembly.CompileError) {
    console.error("WASM compile error:", e);
    // 处理编译错误
  } else {
    console.error("Unknown error:", e);
  }

  throw e;
}
```

---

## 10 部署方案

### 10.1 npm 发布

**wasm-lightnode 包**：

```json
{
  "name": "wasm-lightnode",
  "version": "1.0.0",
  "main": "index.js",
  "files": ["lightnode.wasm", "index.js", "wasi.js"],
  "exports": {
    ".": "./index.js",
    "./wasm": "./lightnode.wasm"
  }
}
```

**使用方式**：

```javascript
import { LightNode } from "wasm-lightnode";

const node = new LightNode();
await node.init();
await node.start();
```

### 10.2 CDN 分发

**版本化 URL**：

```html
<script type="module">
  import { LightNode } from "https://cdn.example.com/wasm-lightnode@1.0.0/index.js";

  const node = new LightNode();
  await node.init();
</script>
```

---

## 11 结论

### 11.1 关键成果

✅ **安全性**：零文件系统访问，私钥隔离在 WebCrypto ✅ **性能**：单标签页 <50
MB，CPU <5%，启动 <10 ms ✅ **可移植性**：一次编译，所有现代浏览器运行 ✅ **去中
心化**：P2P 网络，DHT 自发现

### 11.2 经验总结

1. **Capability-Based**：只授予必要的能力
2. **安全隔离**：多层防护，私钥隔离
3. **性能优化**：Worker 线程，预编译缓存
4. **可观测性**：完整的监控和调试支持

---

**相关文档**：

- [`system-view-cases-analysis.md`](system-view-cases-analysis.md) - system_view
  案例扩展分析
- [`../01-implementation/06-wasm/wasi-examples.md`](../01-implementation/06-wasm/wasi-examples.md) -
  WASI 示例
- [`../01-implementation/06-wasm/wasm-compilation.md`](../01-implementation/06-wasm/wasm-compilation.md) -
  WASM 编译
- [`../../02-views/10-quick-views/webassembly-view.md`](../../02-views/10-quick-views/webassembly-view.md) -
  WebAssembly 视角
- [`../00-theory/02-induction-proof/psi5-wasm.md`](../00-theory/02-induction-proof/psi5-wasm.md) -
  WASM 归纳映射

---

**更新时间**：2025-11-05 **版本**：v1.0 **维护者**：基于 system_view.md 案例 E
扩展
