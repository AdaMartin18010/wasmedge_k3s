# 11. 代数结构视角参考资源

## 📑 目录

- [11.1 核心文档](#111-核心文档)
  - [项目内部文档](#项目内部文档)
  - [相关文档](#相关文档)
- [11.2 技术文档](#112-技术文档)
  - [虚拟化](#虚拟化)
  - [容器化](#容器化)
  - [服务网格](#服务网格)
  - [WasmEdge](#wasmedge)
- [11.3 学术资源](#113-学术资源)
  - [代数结构](#代数结构)
  - [范畴论](#范畴论)
- [11.4 开源项目](#114-开源项目)
  - [核心项目](#核心项目)
- [11.5 社区资源](#115-社区资源)
  - [CNCF](#cncf)
- [11.6 2025 年最新资源](#116-2025-年最新资源)
  - [服务网格（2025 年更新）](#服务网格2025-年更新)
  - [WasmEdge（2025 年更新）](#wasmedge2025-年更新)
  - [性能基准（2025 年）](#性能基准2025-年)

---

## 11.1 核心文档

### 项目内部文档

- **[算子定义](01-operator-definition.md)** - 20 个一元算子详解
- **[代数结构](02-algebraic-structure.md)** - 代数结构 Σ = ⟨Ω, ℱ, 𝒫, ℒ⟩
- **[公理体系](03-axioms.md)** - 公理 A1-A7
- **[复合运算表](04-composition-table.md)** - 20×20 运算表
- **[最简范式定理](05-normal-form-theorem.md)** - 主范式定理
- **[同态映射](06-homomorphism.md)** - 指标映射
- **[范畴论视角](07-category-view.md)** - 函子、自然变换
- **[实践案例](08-practical-examples.md)** - 算子组合 → 技术栈

### 相关文档

- **[09. 矩阵视角](../09-matrix-perspective/README.md)** - 矩阵力学模型（互补视
  角）
- **[08. 范畴论视角](../08-category-theory/category-theory.md)** - 对象、态射与
  函子（理论基础）
- **[07. 形式化理论](../07-formal-theory/formal-theory.md)** - 结构同构和关系等
  价（数学基础）
- **[10. 决策模型](../10-decision-models/decision-models.md)** - 技术决策模型（
  应用场景）

## 11.2 技术文档

### 虚拟化

- [KVM (Kernel-based Virtual Machine)](https://www.linux-kvm.org/)
- [Xen Project](https://xenproject.org/)
- [Hyper-V](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/)
- [Virtualization (Wikipedia)](https://en.wikipedia.org/wiki/Virtualization)

### 容器化

- [Docker](https://www.docker.com/)
- [containerd](https://containerd.io/)
- [runc](https://github.com/opencontainers/runc)
- [Containerization (Wikipedia)](https://en.wikipedia.org/wiki/Containerization)

### 服务网格

- [Istio](https://istio.io/)
- [Linkerd](https://linkerd.io/)
- [Cilium Service Mesh](https://docs.cilium.io/en/stable/network/service-mesh/)
- [Service Mesh (CNCF)](https://www.cncf.io/blog/2017/04/25/service-mesh/)

### WasmEdge

- [WasmEdge](https://wasmedge.org/)
- [WebAssembly](https://webassembly.org/)
- [WASI](https://wasi.dev/)

## 11.3 学术资源

### 代数结构

- [Universal Algebra (Wikipedia)](https://en.wikipedia.org/wiki/Universal_algebra)
- [Category Theory (Wikipedia)](https://en.wikipedia.org/wiki/Category_theory)
- [Homomorphism (Wikipedia)](https://en.wikipedia.org/wiki/Homomorphism)

### 范畴论

- [Category Theory Foundations](https://ncatlab.org/nlab/show/category+theory)
- [Homotopy Type Theory](https://homotopytypetheory.org/)

## 11.4 开源项目

### 核心项目

- [Kubernetes](https://kubernetes.io/)
- [Istio](https://istio.io/)
- [Linkerd](https://linkerd.io/)
- [WasmEdge](https://wasmedge.org/)

## 11.5 社区资源

### CNCF

- [CNCF](https://www.cncf.io/)
- [Service Mesh Interface (SMI)](https://smi-spec.io/)

## 11.6 2025 年最新资源

### 服务网格（2025 年更新）

- [Istio Ambient Mesh](https://istio.io/latest/docs/ambient/)
- [Service Mesh Performance](https://istio.io/latest/docs/ops/deployment/performance-and-scalability/)
- [Wasm Plugin in Envoy](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/wasm_filter)

### WasmEdge（2025 年更新）

- [WasmEdge 0.14](https://wasmedge.org/docs/start/install)
- [WasmEdge with Service Mesh](https://wasmedge.org/docs/develop/mesh/istio/)

### 性能基准（2025 年）

- [Service Mesh Performance Benchmark](https://github.com/istio/tools/tree/master/perf/benchmark)
- [WasmEdge Performance](https://wasmedge.org/docs/start/performance/)

---

**最后更新**：2025-11-04 **维护者**：项目团队
