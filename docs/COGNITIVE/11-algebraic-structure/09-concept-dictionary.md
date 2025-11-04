# 11.9 概念词典：80+ 技术概念完整映射

## 目录

- [目录](#目录)
- [11.9.1 词典概述](#1191-词典概述)
- [11.9.2 硬件/固件层（HW）](#1192-硬件固件层hw)
- [11.9.3 Hypervisor / 宿主机内核层（Kernel-space）](#1193-hypervisor--宿主机内核层kernel-space)
- [11.9.4 用户态运行时层（User-space Runtime）](#1194-用户态运行时层user-space-runtime)
- [11.9.5 镜像与打包语义（Image / Artifact）](#1195-镜像与打包语义image--artifact)
- [11.9.6 编排与调度（Orchestration）](#1196-编排与调度orchestration)
- [11.9.7 服务网格与流量治理（Mesh）](#1197-服务网格与流量治理mesh)
- [11.9.8 可观测与策略（Observability / Policy）](#1198-可观测与策略observability--policy)
- [11.9.9 边缘/机密/Serverless 算子](#1199-边缘机密serverless-算子)
- [11.9.10 符号汇总表](#11910-符号汇总表)
- [11.9.11 参考](#11911-参考)

---

## 11.9.1 词典概述

**概念词典**是代数结构视角的基础，将 80+ 技术概念按**层级-作用域-生命周期**三维
展开，避免漏项。

**词典结构**：

- **层级**：硬件/固件 → 内核 → 运行时 → 镜像 → 编排 → 网格 → 观测 → 边缘/机密/无
  服务器
- **作用域**：物理硬件、虚拟化、隔离、打包、调度、网络、监控、边缘
- **生命周期**：静态、动态、只读、可写

**映射关系**：

- **概念 → 符号**：每个技术概念映射到唯一符号
- **符号 → 算子**：符号可组合成算子
- **算子 → 技术栈**：算子组合形成完整技术栈

---

## 11.9.2 硬件/固件层（HW）

**层级特征**：物理硬件、固件、不可变

| 概念               | 一句话定义         | 符号 | 典型技术           | 备注             |
| ------------------ | ------------------ | ---- | ------------------ | ---------------- |
| **CPU 虚拟化扩展** | Intel VT-x / AMD-V | VT   | Intel VT-x, AMD-V  | 硬件级虚拟化支持 |
| **IOMMU**          | IO 设备直通隔离    | IO   | Intel VT-d, AMD-Vi | 设备直通         |
| **SGX/SEV**        | 机密计算 enclave   | E    | Intel SGX, AMD SEV | 可信执行区       |
| **TPM**            | 可信度量根         | T    | TPM 2.0            | 硬件安全模块     |
| **microcode**      | 固件级沙补丁       | μ    | Intel microcode    | 固件更新         |

**代数属性**：

- **封闭性**：硬件层概念不会互相转换
- **不可逆性**：硬件操作不可撤销
- **静态性**：硬件配置相对固定

---

## 11.9.3 Hypervisor / 宿主机内核层（Kernel-space）

**层级特征**：内核态、虚拟化、隔离

| 概念            | 一句话定义        | 符号 | 典型技术    | 备注               |
| --------------- | ----------------- | ---- | ----------- | ------------------ |
| **KVM**         | 内核态 hypervisor | K    | KVM         | Linux 内核态虚拟化 |
| **Xen**         | 裸机 hypervisor   | X    | Xen         | 裸机虚拟化         |
| **Hyper-V**     | 微软裸机          | Hv   | Hyper-V     | Windows 虚拟化     |
| **bhyve**       | FreeBSD 原生      | B    | bhyve       | FreeBSD 虚拟化     |
| **sev-es**      | 加密虚拟机状态    | E′   | AMD SEV-ES  | 加密 VM 状态       |
| **seccomp-bpf** | 系统调用过滤      | S    | seccomp-BPF | syscall 过滤       |
| **Landlock**    | 文件系统沙盒      | L    | Landlock    | FS 沙盒            |
| **eBPF**        | 内核可编程        | P    | eBPF        | 内核可编程         |
| **cgroup**      | 资源控制器        | Cg   | cgroup      | 资源限制           |
| **namespace**   | 隔离名字空间      | Ns   | namespace   | 命名空间隔离       |
| **OverlayFS**   | 联合挂载层        | O    | OverlayFS   | 联合文件系统       |
| **virtio**      | 半虚拟化设备      | Vio  | virtio      | 半虚拟设备         |
| **VFIO**        | 用户态驱动直通    | Vf   | VFIO        | 设备直通           |

**代数属性**：

- **可组合性**：内核层概念可以组合（如 `Cg + Ns = Container`）
- **幂等性**：部分概念满足幂等（如 `Ns² = Ns`）
- **交换性**：部分概念可交换（如 `Cg ∘ Ns = Ns ∘ Cg`）

---

## 11.9.4 用户态运行时层（User-space Runtime）

**层级特征**：容器/VM、动态、可执行

| 概念                         | 一句话定义         | 符号 | 典型技术                 | 备注        |
| ---------------------------- | ------------------ | ---- | ------------------------ | ----------- |
| **runc**                     | OCI 标准容器运行时 | R    | runc                     | OCI 标准    |
| **crun**                     | C 语言实现，更快   | R′   | crun                     | C 语言实现  |
| **youki**                    | Rust 实现          | R″   | youki                    | Rust 实现   |
| **kata-runtime**             | VM 级容器          | Kc   | Kata                     | VM 级容器   |
| **gVisor**                   | 用户态内核代理     | G    | gVisor                   | 用户态内核  |
| **firecracker**              | MicroVM            | F    | Firecracker              | 轻量 VM     |
| **qemu**                     | 全功能模拟器       | Q    | QEMU                     | 全功能模拟  |
| **virtiofs**                 | 共享文件系统       | Vfs  | virtiofs                 | 共享 FS     |
| **nvidia-container-runtime** | GPU 透传           | Rg   | nvidia-container-runtime | GPU 直通    |
| **wasmtime**                 | Wasm 运行时        | W    | wasmtime                 | Wasm 运行时 |
| **wasmEdge**                 | 云优化 Wasm        | W′   | WasmEdge                 | 云优化 Wasm |

**算子映射**：

- **C** ← `{runc, crun, youki}`
- **Kc** ← `{kata-runtime}`
- **G** ← `{gVisor}`
- **F** ← `{firecracker}`
- **W** ← `{wasmtime, wasmEdge}`

---

## 11.9.5 镜像与打包语义（Image / Artifact）

**层级特征**：打包、只读、静态

| 概念                 | 一句话定义           | 符号 | 典型技术    | 备注       |
| -------------------- | -------------------- | ---- | ----------- | ---------- |
| **OCI Image Spec**   | 分层 tar+config json | I    | OCI Image   | 层化镜像   |
| **Image Index**      | 多架构清单           | Ix   | Image Index | 多架构支持 |
| **Layer blob**       | 每层哈希块           | Lb   | Layer blob  | 单层哈希   |
| **Digest**           | content-hash         | D    | Digest      | 内容哈希   |
| **Manifest**         | 层顺序+config        | Mf   | Manifest    | 镜像清单   |
| **SBOM**             | 软件物料清单         | B    | SBOM        | 物料清单   |
| **cosign signature** | 镜像签名             | Sig  | cosign      | 镜像签名   |
| **attestation**      | 构建时证据           | Att  | attestation | 构建证据   |
| **Cache Image**      | 构建缓存             | Ca   | Cache Image | 构建缓存   |
| **Distroless**       | 仅运行时文件         | Id   | Distroless  | 最小镜像   |
| **Scratch**          | 空基底               | Is   | Scratch     | 空镜像     |

**算子映射**：

- **I** ← `{OCI Image, Image Index, Layer blob, Manifest}`

**代数属性**：

- **幂等性**：`I² = I`（多次打包同一镜像结果相同）
- **可交换性**：`I ∘ C = C ∘ I`（镜像打包和容器化可交换）

---

## 11.9.6 编排与调度（Orchestration）

**层级特征**：调度、复制、动态

| 概念                   | 一句话定义       | 符号 | 典型技术          | 备注         |
| ---------------------- | ---------------- | ---- | ----------------- | ------------ |
| **Pod**                | K8s 最小调度原子 | Po   | Pod               | K8s 最小单元 |
| **Deployment**         | 无状态控制器     | De   | Deployment        | 无状态控制器 |
| **StatefulSet**        | 有状态控制器     | Ss   | StatefulSet       | 有状态控制器 |
| **DaemonSet**          | 节点守护         | Da   | DaemonSet         | 守护进程     |
| **Job / CronJob**      | 批 / 定时        | J    | Job, CronJob      | 批处理       |
| **ReplicaSet**         | 副本集           | Rs   | ReplicaSet        | 副本管理     |
| **Namespace**          | 逻辑隔离         | N    | Namespace         | 逻辑隔离     |
| **Node**               | 工作节点         | No   | Node              | 工作节点     |
| **Taint / Toleration** | 排斥-容忍        | Tt   | Taint, Toleration | 调度策略     |
| **Affinity**           | 亲和性           | Af   | Affinity          | 亲和性       |
| **PriorityClass**      | 抢占优先级       | Pc   | PriorityClass     | 优先级       |
| **ResourceQuota**      | 资源配额         | Q    | ResourceQuota     | 资源配额     |
| **LimitRange**         | 默认规格         | Lr   | LimitRange        | 默认规格     |

**代数属性**：

- **可组合性**：编排概念可以组合（如 `De + Rs = Deployment`）
- **幂等性**：部分概念满足幂等（如 `De² = De`）

---

## 11.9.7 服务网格与流量治理（Mesh）

**层级特征**：网络、动态、可观测

| 概念                    | 一句话定义      | 符号 | 典型技术            | 备注       |
| ----------------------- | --------------- | ---- | ------------------- | ---------- |
| **Sidecar**             | 伴车代理        | Sc   | Sidecar             | 伴车代理   |
| **Envoy**               | L4/L7 代理      | E    | Envoy               | L4/L7 代理 |
| **Istiod**              | 控制平面        | Ist  | Istiod              | 控制平面   |
| **xDS**                 | 配置发现协议    | Xd   | xDS                 | 配置协议   |
| **VirtualService**      | 路由规则        | Vs   | VirtualService      | 路由规则   |
| **DestinationRule**     | 后端策略        | Dr   | DestinationRule     | 后端策略   |
| **Gateway**             | 入口网关        | Gw   | Gateway             | 入口网关   |
| **PeerAuthentication**  | mTLS 开关       | Pa   | PeerAuthentication  | mTLS 配置  |
| **AuthorizationPolicy** | 七层授权        | Ap   | AuthorizationPolicy | 授权策略   |
| **WasmPlugin**          | 过滤器插件      | Wp   | WasmPlugin          | Wasm 插件  |
| **Telemetry API**       | 统一遥测        | Tapi | Telemetry API       | 遥测 API   |
| **Ambient Mesh**        | 无 Sidecar 模式 | Am   | Istio Ambient       | 无 Sidecar |
| **Waypoint Proxy**      | 每服务 L7 代理  | Wp   | Waypoint Proxy      | L7 代理    |
| **ztunnel**             | 共享 L4 代理    | Zt   | ztunnel             | L4 代理    |

**算子映射**：

- **M** ← `{Sidecar, Envoy, xDS, VirtualService, DestinationRule}`
- **Am** ← `{Ambient Mesh, Waypoint Proxy, ztunnel}`
- **E** ← `{Envoy}`
- **Ist** ← `{Istiod, xDS}`

**代数属性**：

- **幂等性**：`M² = M`（多次注入服务网格结果相同）
- **可交换性**：`M ∘ C = C ∘ M`（服务网格和容器化可交换）

---

## 11.9.8 可观测与策略（Observability / Policy）

**层级特征**：监控、策略、动态

| 概念                   | 一句话定义   | 符号 | 典型技术          | 备注       |
| ---------------------- | ------------ | ---- | ----------------- | ---------- |
| **OpenTelemetry**      | 统一观测标准 | Otel | OpenTelemetry     | 统一观测   |
| **Prometheus**         | 指标存储     | Prom | Prometheus        | 指标存储   |
| **Jaeger / Tempo**     | 分布式追踪   | J    | Jaeger, Tempo     | 分布式追踪 |
| **FluentBit / Vector** | 日志收集     | Fb   | FluentBit, Vector | 日志收集   |
| **eBPF exporter**      | 内核指标     | Eb   | eBPF exporter     | 内核指标   |
| **Gatekeeper**         | OPA 准入     | Gk   | Gatekeeper        | OPA 准入   |
| **Falco**              | 运行时安全   | Fc   | Falco             | 运行时安全 |
| **Cilium Hubble**      | eBPF 观测    | Hb   | Cilium Hubble     | eBPF 观测  |
| **Inspektor Gadget**   | 调试工具箱   | Ig   | Inspektor Gadget  | 调试工具   |
| **Kyverno**            | 策略引擎     | Ky   | Kyverno           | 策略引擎   |

**算子映射**：

- **Otel** ← `{OpenTelemetry, Prometheus, Jaeger}`
- **Gk** ← `{Gatekeeper, Kyverno}`
- **P** ← `{eBPF exporter, Cilium Hubble}`

---

## 11.9.9 边缘/机密/Serverless 算子

**层级特征**：边缘、机密、无服务器

| 概念                       | 一句话定义      | 符号 | 典型技术               | 备注       |
| -------------------------- | --------------- | ---- | ---------------------- | ---------- |
| **K3s**                    | 轻量 K8s        | K3   | K3s                    | 轻量 K8s   |
| **KubeEdge**               | 边缘自治        | Ke   | KubeEdge               | 边缘自治   |
| **SuperEdge**              | 腾讯边缘        | Se   | SuperEdge              | 腾讯边缘   |
| **WasmEdge**               | 边缘 Wasm       | We   | WasmEdge               | 边缘 Wasm  |
| **Confidential Container** | 机密容器        | Cc   | Confidential Container | 机密容器   |
| **SGX Enclave**            | 可信执行区      | Sgx  | SGX Enclave            | 可信执行   |
| **AMD SEV-SNP**            | 加密虚机        | Sev  | AMD SEV-SNP            | 加密 VM    |
| **Firecracker**            | MicroVM         | F    | Firecracker            | MicroVM    |
| **gVisor**                 | 用户态内核      | G    | gVisor                 | 用户态内核 |
| **Kata**                   | VM 容器         | Kc   | Kata                   | VM 容器    |
| **Knative**                | Serverless 底座 | Kn   | Knative                | Serverless |
| **OpenFaaS**               | 函数框架        | Faas | OpenFaaS               | 函数框架   |
| **KEDA**                   | 事件驱动伸缩    | Keda | KEDA                   | 事件驱动   |
| **Dapr**                   | 应用运行时      | D    | Dapr                   | 应用运行时 |

**算子映射**：

- **We** ← `{WasmEdge, K3s}`
- **Cc** ← `{Confidential Container, SGX Enclave, AMD SEV-SNP}`
- **Kc** ← `{Kata, Firecracker}`

---

## 11.9.10 符号汇总表

**符号池汇总**（可直接代入代数式）：

| 类别                   | 符号池                                                    | 算子映射           |
| ---------------------- | --------------------------------------------------------- | ------------------ |
| **硬件**               | VT, IO, E, T, μ                                           | —                  |
| **内核**               | K, X, Hv, B, S, L, P, Cg, Ns, O, Vio, Vf                  | S, P, Ns, Cg, O    |
| **运行时**             | R, R′, R″, Kc, G, F, Q, Vfs, Rg, W, W′                    | C, Kc, G, F, W, We |
| **镜像**               | I, Ix, Lb, D, Mf, B, Sig, Att, Ca, Id, Is                 | I                  |
| **编排**               | Po, De, Ss, Da, J, Rs, N, No, Tt, Af, Pc, Q, Lr           | —                  |
| **网格**               | Sc, E, Ist, Xd, Vs, Dr, Gw, Pa, Ap, Wp, Tapi, Am, Wp, Zt  | M, Am, E, Ist      |
| **观测**               | Otel, Prom, J, Fb, Eb, Gk, Fc, Hb, Ig, Ky                 | Otel, Gk, P        |
| **边缘/机密/无服务器** | K3, Ke, Se, We, Cc, Sgx, Sev, F, G, Kc, Kn, Faas, Keda, D | We, Cc, Kc         |

**使用规则**：

1. **符号 → 算子**：多个符号可映射到同一算子（如 `{runc, crun, youki} → C`）
2. **算子 → 技术栈**：算子组合形成技术栈（如 `I∘C∘S∘M`）
3. **技术栈 → 指标**：通过同态映射得到性能指标

---

## 11.9.11 参考

**关联文档**：

- **[算子定义](01-operator-definition.md)** - 20 个一元算子的完整定义
- **[代数结构](02-algebraic-structure.md)** - 代数结构签名和对象集合
- **[复合运算表](04-composition-table.md)** - 20×20 复合运算表
- **[实践案例](08-practical-examples.md)** - 算子组合的实际应用

**外部参考**：

- [OCI Image Spec](https://opencontainers.org/)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
- [Istio Concepts](https://istio.io/latest/docs/concepts/)
- [OpenTelemetry Specification](https://opentelemetry.io/docs/specs/)

---

**最后更新**：2025-11-04 **维护者**：项目团队
