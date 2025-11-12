# 11. 代数结构视角快速参考

## 📑 目录

- [📑 目录](#-目录)
- [📋 算子速查表](#-算子速查表)
  - [20 个一元算子](#20-个一元算子)
- [🔢 公理速查](#-公理速查)
- [📊 主范式](#-主范式)
- [🎯 快速决策流程](#-快速决策流程)
- [📈 指标说明](#-指标说明)
- [📚 完整文档列表](#-完整文档列表)

---

## 📋 算子速查表

### 20 个一元算子

| 符号     | 名称                   | 作用                  | 生成对象               | 典型实现               |
| -------- | ---------------------- | --------------------- | ---------------------- | ---------------------- |
| **V**    | Virtualization         | Binary → VM           | VM                     | KVM, Xen               |
| **I**    | Image-packing          | Binary → Image        | Image                  | OCI Image              |
| **C**    | Containerization       | Image → Container     | Container              | runc, crun             |
| **S**    | Sandbox                | Container → Sandbox   | Sandbox                | seccomp-bpf            |
| **M**    | Mesh-inject            | Container → Mesh      | Mesh Container         | Istio, Linkerd         |
| **Kc**   | Kata-runtime           | Binary → Kata-VM      | Kata-VM-Container      | Kata                   |
| **G**    | gVisor                 | Binary → User-Kernel  | User-Kernel Container  | gVisor                 |
| **F**    | Firecracker            | Binary → microVM      | microVM                | Firecracker            |
| **W**    | WasmEdge               | Binary → Wasm         | Wasm Runtime           | WasmEdge               |
| **We**   | WasmEdge-Edge          | Binary → Wasm Edge    | Wasm Edge Runtime      | WasmEdge               |
| **Am**   | Ambient Mesh           | Container → Ambient   | Ambient Mesh           | Istio Ambient          |
| **P**    | eBPF                   | Kernel → eBPF         | eBPF Program           | eBPF                   |
| **Ns**   | Namespace              | Container → Namespace | Namespace              | namespace              |
| **Cg**   | Cgroup                 | Container → Cgroup    | Cgroup                 | cgroup                 |
| **O**    | OverlayFS              | FS → Overlay          | Overlay                | OverlayFS              |
| **E**    | Envoy                  | Network → Envoy       | Envoy Proxy            | Envoy                  |
| **Ist**  | Istio Control-Plane    | Config → Istio        | Istio                  | Istiod, xDS            |
| **Otel** | OpenTelemetry          | Runtime → Telemetry   | Telemetry              | Otel                   |
| **Gk**   | Gatekeeper             | Policy → Gatekeeper   | Gatekeeper             | Gatekeeper, OPA        |
| **Cc**   | Confidential Container | Container → Conf      | Confidential Container | Confidential Container |

## 🔢 公理速查

| 公理           | 说明                 | 示例                              |
| -------------- | -------------------- | --------------------------------- |
| **A1. 封闭性** | ∀x∈Ω, ℱ(x)∈Ω         | C(I(Image)) = Container ∈ Ω       |
| **A2. 幂等**   | X² = X (X∈{C,S,M,W}) | C² = C, S² = S, M² = M            |
| **A3. 非交换** | V∘C ≠ C∘V            | VM-in-container ≠ container-in-VM |
| **A4. 短正合** | 0→Ker(S)→Ω→Im(S)→0   | seccomp 过滤                      |
| **A5. 同态**   | φ: (Ω,∘)→ℝ³          | φ(C) = (5▼, 3▲, 5▼)               |
| **A6. 吸收元** | ∅ = No-op; ∀ω, ω∘∅=ω | 省略无操作                        |
| **A7. 逆元**   | 仅 V 有弱逆 V⁻¹      | V⁻¹：硬件解锁                     |

## 📊 主范式

- **I∘C∘S∘M**：无虚拟化路径（镜像 → 容器 → 沙盒 → 网格）
- **V∘S∘C∘M**：含虚拟化路径（VM→ 沙盒 → 容器 → 网格）

## 🎯 快速决策流程

1. **写出需求串**：`V → C → M → C`
2. **化简**：C² → C ⇒ `V → C → M`
3. **查表**：查找 `(V∘C∘M)` → `(4▼-5▼-4▼)`
4. **技术落地**：`Kata VM (V)` → `containerd (C)` → `Istio Ambient (M)`

## 📈 指标说明

- **Latency↑**：延迟（越低越好，数值越小越好）
- **Security↓**：安全（越高越好，数值越小越好）
- **Observability→**：可观测性（越高越好，数值越大越好）

## 📚 完整文档列表

| 文档             | 路径                                                 | 核心内容                     |
| ---------------- | ---------------------------------------------------- | ---------------------------- |
| **概念词典**     | [09-concept-dictionary.md](09-concept-dictionary.md) | 80+ 技术概念的完整映射表     |
| **矩阵思维导图** | [10-matrix-mindmap.md](10-matrix-mindmap.md)         | 矩阵模板与思维导图一体化方案 |
| **工具与代码**   | [11-tools-code.md](11-tools-code.md)                 | Python 实现与脚本工具        |

---

**最后更新**：2025-11-04 **维护者**：项目团队
