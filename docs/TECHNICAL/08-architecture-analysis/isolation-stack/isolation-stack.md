# 29. 四层隔离栈：虚拟化 → 半虚拟化 → 容器化 → 沙盒化

**最后更新**: 2025-11-07 **维护者**: 项目团队

> 📋 **文档说明**：本文档将"虚拟化 → 半虚拟化 → 容器化 → 沙盒化"当成 4 层「隔离
> 栈」，自底向上逐层解析，包含各层级概念、机制、组件、黑话和一句话解释。文档还包
> 含横纵耦合的问题定位模型（OTLP 横向 + eBPF 纵向），对齐 2025 年 11 月 7 日最新
> 技术栈状态。
>
> 📂 **文档目录**：完整的文档结构说明和快速导航请参考 [README.md](README.md)。各
> 层次独立文档位于 [layers/](layers/) 目录，问题定位模型独立文档位于
> [troubleshooting/](troubleshooting/) 目录。

## 📑 目录

- [29. 四层隔离栈：虚拟化 → 半虚拟化 → 容器化 → 沙盒化](#29-四层隔离栈虚拟化--半虚拟化--容器化--沙盒化)
  - [📑 目录](#-目录)
  - [29.1 文档定位](#291-文档定位)
    - [29.1.0 文档概览](#2910-文档概览)
  - [29.2 四层隔离栈总览](#292-四层隔离栈总览)
  - [29.3 逐层展开](#293-逐层展开)
    - [29.3.1 L-0 硬件辅助层（CPU 虚拟化指令集）](#2931-l-0-硬件辅助层cpu-虚拟化指令集)
    - [29.3.2 L-1 全虚拟化层（完整假硬件）](#2932-l-1-全虚拟化层完整假硬件)
    - [29.3.3 L-2 半虚拟化层（Guest 内核配合）](#2933-l-2-半虚拟化层guest-内核配合)
    - [29.3.4 L-3 容器化层（进程级隔离）](#2934-l-3-容器化层进程级隔离)
    - [29.3.5 L-4 沙盒化层（syscall 过滤 / 二次内核）](#2935-l-4-沙盒化层syscall-过滤--二次内核)
  - [29.4 技术架构图](#294-技术架构图)
    - [29.4.1 四层隔离栈架构图](#2941-四层隔离栈架构图)
    - [29.4.2 层级关系图](#2942-层级关系图)
  - [29.5 快速诊断口诀](#295-快速诊断口诀)
    - [29.5.1 日志关键词快速定位](#2951-日志关键词快速定位)
    - [29.5.2 故障排查流程](#2952-故障排查流程)
  - [29.6 问题定位模型：横向请求链 + 纵向隔离栈](#296-问题定位模型横向请求链--纵向隔离栈)
    - [29.6.0 观测系统作为第四大基础设施](#2960-观测系统作为第四大基础设施)
      - [29.6.0.1 为什么"必须"而不是"最好"](#29601-为什么必须而不是最好)
      - [29.6.0.2 观测系统本身也是"系统"，需要同等 SLA](#29602-观测系统本身也是系统需要同等-sla)
      - [29.6.0.3 完备性判据（可量化）](#29603-完备性判据可量化)
      - [29.6.0.4 反例：没有观测的"裸容器"长什么样](#29604-反例没有观测的裸容器长什么样)
      - [29.6.0.5 落地最小完备集（MVP）](#29605-落地最小完备集mvp)
      - [29.6.0.6 结论（一句话收拢）](#29606-结论一句话收拢)
    - [29.6.1 定位模型概述](#2961-定位模型概述)
    - [29.6.2 事故背景（简化版）](#2962-事故背景简化版)
    - [29.6.3 五步定位法](#2963-五步定位法)
    - [29.6.4 信号来源与工具对照表](#2964-信号来源与工具对照表)
    - [29.6.5 定位口诀（背下来）](#2965-定位口诀背下来)
    - [29.6.6 实战一键脚本（示例）](#2966-实战一键脚本示例)
    - [29.6.7 定位流程可视化](#2967-定位流程可视化)
    - [29.6.8 常见问题定位速查](#2968-常见问题定位速查)
    - [29.6.9 eBPF 工具速查表](#2969-ebpf-工具速查表)
    - [29.6.10 小结](#29610-小结)
    - [29.6.11 快速定位流程图](#29611-快速定位流程图)
    - [29.6.12 网络定位专题：横向生命线](#29612-网络定位专题横向生命线)
      - [29.6.12.0 为什么网络必须作为独立维度](#296120-为什么网络必须作为独立维度)
      - [29.6.12.0.1 网络在四种隔离形态中的真实"切片"](#2961201-网络在四种隔离形态中的真实切片)
      - [29.6.12.0.2 OTLP 如何给出"横向坐标"](#2961202-otlp-如何给出横向坐标)
      - [29.6.12.0.3 eBPF 如何给出"纵向坐标"](#2961203-ebpf-如何给出纵向坐标)
      - [29.6.12.0.4 常见反驳与充分回应](#2961204-常见反驳与充分回应)
      - [29.6.12.0.5 生产落地 Checklist](#2961205-生产落地-checklist)
      - [29.6.12.0.6 结论（一句话收拢）](#2961206-结论一句话收拢)
      - [29.6.12.1 网络在三栈里的"切片"视图](#296121-网络在三栈里的切片视图)
      - [29.6.12.2 横向：OTLP 网络 trace](#296122-横向otlp-网络-trace)
      - [29.6.12.3 纵向：eBPF 网络显微镜](#296123-纵向ebpf-网络显微镜)
      - [29.6.12.4 网络定位五步法（接前述故障）](#296124-网络定位五步法接前述故障)
      - [29.6.12.5 网络定位一键脚本](#296125-网络定位一键脚本)
      - [29.6.12.6 网络定位口诀](#296126-网络定位口诀)
    - [29.6.13 实战案例总结](#29613-实战案例总结)
      - [案例 1：CPU Throttle + Virtio 队列满（完整链路）](#案例-1cpu-throttle--virtio-队列满完整链路)
      - [案例 2：网络 RTT 突增 + mDNS 风暴（网络定位）](#案例-2网络-rtt-突增--mdns-风暴网络定位)
      - [案例 3：磁盘 IO 瓶颈 + 日志收集风暴（主机层）](#案例-3磁盘-io-瓶颈--日志收集风暴主机层)
    - [29.6.14 最佳实践与注意事项](#29614-最佳实践与注意事项)
      - [29.6.14.1 定位流程最佳实践](#296141-定位流程最佳实践)
      - [29.6.14.2 常见误区与注意事项](#296142-常见误区与注意事项)
      - [29.6.14.3 生产环境部署建议](#296143-生产环境部署建议)
    - [29.6.15 快速参考卡片](#29615-快速参考卡片)
    - [29.6.16 工具安装与配置速查](#29616-工具安装与配置速查)
    - [29.6.17 相关文档](#29617-相关文档)
  - [29.7 快速索引与常见问题](#297-快速索引与常见问题)
    - [29.7.0 按问题类型快速索引](#2970-按问题类型快速索引)
    - [29.7.1 常见问题 FAQ](#2971-常见问题-faq)
      - [Q1: 为什么需要四层隔离栈的概念？](#q1-为什么需要四层隔离栈的概念)
      - [Q2: 观测系统真的必须吗？能不能先用业务系统再补观测？](#q2-观测系统真的必须吗能不能先用业务系统再补观测)
      - [Q3: eBPF 工具需要 root 权限，生产环境安全吗？](#q3-ebpf-工具需要-root-权限生产环境安全吗)
      - [Q4: OTLP 和 eBPF 数据如何关联？](#q4-otlp-和-ebpf-数据如何关联)
      - [Q5: 网络为什么不是第 5 层？](#q5-网络为什么不是第-5-层)
      - [Q6: 如何判断观测系统是否完备？](#q6-如何判断观测系统是否完备)
      - [Q7: 遇到偶发性能问题，如何定位？](#q7-遇到偶发性能问题如何定位)
      - [Q8: 老内核（4.14 以下）能用 eBPF 吗？](#q8-老内核414-以下能用-ebpf-吗)
      - [Q9: 如何避免告警风暴？](#q9-如何避免告警风暴)
      - [Q10: 文档太长，从哪里开始阅读？](#q10-文档太长从哪里开始阅读)
  - [29.8 文档总结与核心观点](#298-文档总结与核心观点)
    - [29.8.1 核心观点总结](#2981-核心观点总结)
    - [29.8.2 关键方法论](#2982-关键方法论)
    - [29.8.3 技术术语快速索引](#2983-技术术语快速索引)
    - [29.8.4 文档结构导航图](#2984-文档结构导航图)
    - [29.8.5 学习路径建议](#2985-学习路径建议)
    - [29.8.6 文档价值总结](#2986-文档价值总结)
  - [29.9 文档使用指南](#299-文档使用指南)
    - [29.9.0 如何高效使用本文档](#2990-如何高效使用本文档)
  - [29.10 参考](#2910-参考)
    - [29.10.1 相关文档](#29101-相关文档)
    - [29.10.2 外部资源](#29102-外部资源)
    - [29.10.3 技术标准](#29103-技术标准)
  - [29.11 文档变更历史](#2911-文档变更历史)

---

## 29.1 文档定位

本文档将"虚拟化 → 半虚拟化 → 容器化 → 沙盒化"当成 4 层「隔离栈」，自底向上逐层解
析。

### 29.1.0 文档概览

**文档结构一览**：

| 章节                | 内容                       | 篇幅     | 目标读者         |
| ------------------- | -------------------------- | -------- | ---------------- |
| **29.2-29.3**       | 四层隔离栈详细解析         | 基础理论 | 所有读者         |
| **29.4**            | 技术架构图                 | 可视化   | 架构师、开发者   |
| **29.5**            | 快速诊断口诀               | 速查工具 | 运维工程师       |
| **29.6.0**          | 观测系统作为第四大基础设施 | 理论基础 | 架构师、SRE      |
| **29.6.1-29.6.11**  | 问题定位模型（横纵耦合）   | 方法论   | 运维、SRE        |
| **29.6.12**         | 网络定位专题               | 专项深入 | 网络工程师、运维 |
| **29.6.13-29.6.14** | 实战案例和最佳实践         | 实战应用 | 运维、SRE        |
| **29.6.15-29.6.16** | 快速参考和工具配置         | 速查工具 | 所有读者         |
| **29.7**            | 快速索引与常见问题         | 导航工具 | 所有读者         |
| **29.8**            | 文档总结与核心观点         | 总结归纳 | 所有读者         |
| **29.9-29.10**      | 参考与变更历史             | 参考资料 | 所有读者         |

**快速入门路径**：

- **新手**：29.1 → 29.2 → 29.3 → 29.5 → [29.7 快速索引](#297-快速索引与常见问题)
- **运维工程师**：29.5 → 29.6.3 → 29.6.13 → 29.6.16 →
  [29.7.1 FAQ](#2971-常见问题-faq)
- **架构师**：29.2 → 29.6.0 → 29.6.12.0 →
  [29.8 文档总结](#298-文档总结与核心观点)

**核心价值主张**：

> **"四层隔离栈 + 网络横向生命线 + 横纵耦合定位模型 = 秒级精确问题定位"**

---

**文档目标**：

- 每层给出「概念 → 核心机制 → 典型软件组件 → 组件里常听到的黑话/子模块 → 一句话
  解释」
- 一张表就是一份「四层隔离栈速查卡」，以后看到任何云原生组件 3 秒就能定位它住在
  哪一层、管什么事儿

**适用场景**：

- **技术选型**：快速定位组件所属层级，理解技术栈架构
- **故障排查**：根据日志关键词定位问题层级，结合 OTLP + eBPF 进行横纵联合定位（
  详见 [29.6 问题定位模型](#296-问题定位模型横向请求链--纵向隔离栈)）
- **性能优化**：使用横向请求链和纵向隔离栈模型，精确定位性能瓶颈（详见
  [29.6.13 实战案例总结](#29613-实战案例总结)）
- **架构设计**：理解四层隔离栈的层次关系，指导架构设计决策
- **学习交流**：面试/技术交流时快速理解隔离栈结构，掌握技术术语（详见
  [29.8.3 技术术语快速索引](#2983-技术术语快速索引)）

---

## 29.2 四层隔离栈总览

| 层级             | 隔离边界      | 代表组件（开源/商业）                      | 黑话/子模块                                  | 一句话解释                                               |
| ---------------- | ------------- | ------------------------------------------ | -------------------------------------------- | -------------------------------------------------------- |
| **L-0 硬件辅助** | CPU 模式切换  | VT-x、AMD-V、SEV、TPM                      | VMX root/non-root、EPT、NPT                  | 硬件把"敏感指令"截获，奠定所有虚拟化的地基               |
| **L-1 全虚拟化** | 整个物理机    | KVM、ESXi、Hyper-V、Xen HVM                | VMCS、QEMU、vCPU、vNIC、vmdk                 | 用软件"造"出一台完整假电脑，Guest OS 无感知              |
| **L-2 半虚拟化** | 内核 API 改写 | Xen PV、virtio、Hyper-V Enlightenment      | grant table、event channel、frontend/backend | Guest 内核主动配合，省掉二进制翻译，IO 性能近裸机        |
| **L-3 容器化**   | 进程视角      | runc、containerd、Docker、Podman           | namespace、cgroup、seccomp、capability       | 共享宿主机内核，只隔离进程看到的"世界"                   |
| **L-4 沙盒化**   | syscall 过滤  | gVisor、Firecracker、WASM、Windows Sandbox | Sentry、Gofer、runsc、MicroVM、seccomp-bpf   | 再套一层"用户态内核"或字节码 VM，把恶意 syscall 提前毙掉 |

---

## 29.3 逐层展开

> **💡 提示**：每个层次都有独立的详细文档（`layers/` 目录），包含完整的技术解析
> 、性能特点、安全特点、应用场景、故障排查、实际部署案例和最佳实践。本文档提供概
> 述，详细内容请参考各层次独立文档。
>
> **📋 快速对比**：[隔离层次总结合并对比文档](layers/isolation-comparison.md) -
> 包含快速对比矩阵、技术选型决策树、应用场景匹配、混合部署策略、快速导航指南

### 29.3.1 L-0 硬件辅助层（CPU 虚拟化指令集）

> **📖 详细文档**：[L-0 硬件辅助层独立文档](layers/L-0-hardware-assist.md) - 包
> 含完整的技术解析、性能特点、安全特点、应用场景、故障排查、实际部署案例和最佳实
> 践

**层级定位**：所有虚拟化的底层基础，硬件级别的虚拟化支持。

| 概念      | 软件/指令    | 黑话                            | 一句话解释                                   |
| --------- | ------------ | ------------------------------- | -------------------------------------------- |
| **VT-x**  | CPU 指令     | VMX root/non-root               | Intel 的"硬件开关"，让 VMM 和 Guest 分层跑   |
| **AMD-V** | CPU 指令     | SVM、NPT                        | AMD 同款，叫法不同                           |
| **EPT**   | CPU 页表     | Extended Page Table             | 硬件给 VM 做"二次地址翻译"，省掉影子页表     |
| **SEV**   | CPU 加密     | Secure Encrypted Virtualization | 把每台 VM 内存自动加密，防宿主机偷窥         |
| **TPM-v** | 虚拟可信模块 | vTPM                            | 给 VM 也发"身份证"，满足 Windows 11 安全启动 |

**核心技术点**：

- **VMX root/non-root**：Intel VT-x 的两种 CPU 执行模式，VMM 在 root 模式，Guest
  在 non-root 模式
- **EPT（Extended Page Table）**：硬件辅助的内存虚拟化，Guest 物理地址到 Host 物
  理地址的直接映射
- **NPT（Nested Page Table）**：AMD-V 的内存虚拟化技术，等同于 Intel 的 EPT
- **SEV（Secure Encrypted Virtualization）**：AMD 的内存加密技术，VM 内存对宿主
  机不可见

**诊断关键词**：

- `VMX operation` → VT-x 启用检查
- `EPT violation` → 内存虚拟化错误
- `SEV initialization failed` → 内存加密初始化失败

---

### 29.3.2 L-1 全虚拟化层（完整假硬件）

> **📖 详细文档**：[L-1 全虚拟化层独立文档](layers/L-1-full-virtualization.md) -
> 包含完整的技术解析、性能特点、安全特点、应用场景、故障排查、实际部署案例和最佳
> 实践

**层级定位**：通过软件模拟完整的物理硬件，Guest OS 完全无感知。

| 组件        | 子模块/黑话                        | 一句话解释                                             |
| ----------- | ---------------------------------- | ------------------------------------------------------ |
| **KVM**     | `/dev/kvm`、vmcs、irqfd、ioeventfd | Linux 内核模块，把 CPU 变成"裸机虚拟化开关"            |
| **QEMU**    | TCG、QMP、virtio-mmio、vhost       | 用户态负责模拟 I/O 设备；KVM 只负责 CPU/内存           |
| **ESXi**    | VMFS、vSwitch、vMotion、DRS、HA    | 商业裸金属 Hypervisor，vMotion 可热迁运行中 VM         |
| **Hyper-V** | VMBus、Enlightenment、VMWP         | Windows 自带，支持「嵌套虚拟化」跑 Docker Desktop      |
| **Xen HVM** | qemu-dm、stubdom、PVHVM            | Xen 的"全虚拟"模式，需硬件 VT 支持，IO 用 qemu-dm 模拟 |

**核心技术点**：

- **VMCS（Virtual Machine Control Structure）**：Intel VT-x 的控制结构，存储 VM
  状态信息
- **TCG（Tiny Code Generator）**：QEMU 的二进制翻译引擎，用于非虚拟化的 CPU 指令
  模拟
- **QMP（QEMU Monitor Protocol）**：QEMU 的管理协议，用于动态管理 VM
- **vMotion**：VMware 的虚拟机热迁移技术，可在不中断服务的情况下迁移 VM
- **DRS（Distributed Resource Scheduler）**：VMware 的自动资源调度，自动平衡集群
  负载
- **HA（High Availability）**：VMware 的高可用性，自动重启故障 VM

**诊断关键词**：

- `VMCS corruption` → VM 控制结构损坏，需重启 VM
- `QEMU process crashed` → QEMU 进程崩溃
- `vMotion failed` → 热迁移失败，检查网络/存储
- `VMWP (Virtual Machine Worker Process) stopped` → Hyper-V Worker 进程停止

---

### 29.3.3 L-2 半虚拟化层（Guest 内核配合）

> **📖 详细文档**：[L-2 半虚拟化层独立文档](layers/L-2-paravirtualization.md) -
> 包含完整的技术解析、性能特点、安全特点、应用场景、故障排查、实际部署案例和最佳
> 实践

**层级定位**：Guest 内核需要修改，主动配合 Hypervisor，通过优化的接口提高性能。

| 组件                      | 子模块/黑话                                   | 一句话解释                                               |
| ------------------------- | --------------------------------------------- | -------------------------------------------------------- |
| **Xen PV**                | grant table、event channel、blkfront/netfront | Guest 内核里装"前端"，宿主机跑"后端"，零拷贝共享环       |
| **virtio**                | virtio-net、virtio-blk、vhost、vDPA           | 内核通用半虚拟标准，KVM/ QEMU 都用它提速                 |
| **Hyper-V Enlightenment** | VMBus、Timesync、KVP                          | Windows Guest 装 Integration Services，时钟/心跳不走模拟 |

**核心技术点**：

- **Grant Table**：Xen PV 的内存共享机制，Guest 通过 grant table 共享内存给 Dom0
- **Event Channel**：Xen PV 的中断通知机制，替代硬件中断，性能更高
- **blkfront/netfront**：Xen PV 的块设备和网络设备前端驱动
- **virtio-net/virtio-blk**：virtio 标准的网络和块设备驱动
- **vhost**：virtio 的后端加速，将后端处理移到内核，减少用户态/内核态切换
- **vDPA（vhost Data Path Acceleration）**：硬件加速的 virtio 数据路径
- **VMBus**：Hyper-V 的虚拟总线，用于 Guest 和 Host 之间的通信

**诊断关键词**：

- `grant table error` → 半虚拟层内存共享错误
- `event channel broken` → 中断通知通道断裂
- `virtio-net driver not loaded` → virtio 驱动未加载
- `VMBus initialization failed` → Hyper-V 虚拟总线初始化失败

---

### 29.3.4 L-3 容器化层（进程级隔离）

> **📖 详细文档**：[L-3 容器化层独立文档](layers/L-3-containerization.md) - 包含
> 完整的技术解析、性能特点、安全特点、应用场景、故障排查、实际部署案例和最佳实践

**层级定位**：共享宿主机内核，通过 Namespace、Cgroup 等技术实现进程级隔离。

| 组件             | 子模块/黑话                        | 一句话解释                                                       |
| ---------------- | ---------------------------------- | ---------------------------------------------------------------- |
| **runc**         | `config.json`、specs、rootfs、init | OCI 标准运行时，真正 `clone()` 出容器进程                        |
| **containerd**   | shim、CRI、snapshotter、lease      | 负责镜像拉取、容器生命周期，K8s 默认 CRI                         |
| **Docker**       | dockerd、BuildKit、compose         | 老品牌，把 runc+containerd 包成 CLI；现在镜像构建已交给 BuildKit |
| **Podman**       | pod、systemd generate、rootless    | 无守护进程、可直接跑 systemd 单元，Rootless 用 user-ns           |
| **cgroups**      | v1/v2、memory.high、pids.max       | 内核"限额器"，防止容器把宿主机内存吃光                           |
| **namespaces**   | pid/net/ipc/uts/mnt/user           | 内核"隔离罩"，让容器只能看到自己的 1 号进程、自己的网卡          |
| **seccomp**      | filter、BPF、SCMP_ACT_KILL         | 系统调用白名单，容器想 `mount` 直接 `-EPERM`                     |
| **capabilities** | CAP_SYS_ADMIN、CAP_NET_RAW         | 把 root 拆成 40+ 小块，容器就算 uid=0 也干不了所有事             |

**核心技术点**：

- **OCI Runtime Spec**：Open Container Initiative 运行时规范，定义容器的标准配置
  格式
- **rootfs**：容器的根文件系统，通过 OverlayFS 等实现分层存储
- **shim**：containerd 的适配层，负责管理容器进程生命周期
- **CRI（Container Runtime Interface）**：Kubernetes 的容器运行时接口标准
- **snapshotter**：containerd 的镜像快照管理，实现镜像层的叠加
- **lease**：containerd 的租约机制，用于资源锁定和清理
- **cgroup v2**：Linux 控制组的新版本，统一了资源控制接口
- **user namespace**：用户命名空间，允许非 root 用户运行容器（Rootless）

**诊断关键词**：

- `ContainerCreating` → 容器创建中，检查镜像拉取/存储挂载
- `OOMKilled` → 内存超限被杀，检查 cgroup memory.limit
- `namespace creation failed` → 命名空间创建失败，检查内核支持
- `seccomp: Operation not permitted` → 系统调用被 seccomp 拦截
- `capability not permitted` → 缺少所需的能力（capability）

---

### 29.3.5 L-4 沙盒化层（syscall 过滤 / 二次内核）

**层级定位**：在容器或 VM 基础上再增加一层隔离，通过用户态内核或字节码 VM 拦截系
统调用。

| 组件                | 子模块/黑话                    | 一句话解释                                                        |
| ------------------- | ------------------------------ | ----------------------------------------------------------------- |
| **gVisor**          | Sentry、Gofer、runsc、seccomp  | 用户态 Go 内核拦截 syscall，容器逃逸只能打到 Sentry               |
| **Firecracker**     | MicroVM、Jailer、vsock、MMDS   | AWS 开源的 Rust 轻量 VMM，启动 < 125 ms，给 Lambda 当「二次隔离」 |
| **Kata Containers** | qemu-lite、virtio-fs、shimv2   | 把容器放进最小 VM，用 virtio-fs 挂载镜像，兼顾 K8s API 与 VM 隔离 |
| **WASM runtime**    | Wasmtime、WasmEdge、WAMR       | 字节码 + 能力模型，浏览器/边缘/链上合约的"终极沙盒"               |
| **Windows Sandbox** | WSB、thin-ply VHDX             | 每次双击自动生成一次性的 Win10 轻量 VM，用完即焚                  |
| **Chrome Sandbox**  | seccomp-bpf、namespace、setuid | 浏览器标签页先降权再过滤 syscall，Renderer 被攻破也跑不出沙盒     |

**核心技术点**：

- **Sentry**：gVisor 的用户态内核，用 Go 实现，拦截所有系统调用
- **Gofer**：gVisor 的文件系统代理，负责文件系统操作的转发
- **runsc**：gVisor 的 OCI 运行时实现，替代 runc
- **MicroVM**：Firecracker 的轻量级虚拟机，极简的 VMM，最小化攻击面
- **Jailer**：Firecracker 的安全隔离组件，在非特权模式下运行 MicroVM
- **vsock**：VM 和 Host 之间的通信机制，用于 Firecracker 的通信
- **MMDS（Metadata Service）**：Firecracker 的元数据服务，用于 VM 配置
- **virtio-fs**：Kata Containers 使用的文件系统共享机制，高性能的文件系统访问
- **shimv2**：Kata Containers 的 shim 实现，符合 containerd shim v2 接口
- **WASI（WebAssembly System Interface）**：WebAssembly 的系统调用接口标准
- **能力模型（Capability Model）**：WASM 的安全模型，基于能力的安全控制

**诊断关键词**：

- `Gofer broken pipe` → gVisor 文件系统代理连接断开
- `Sentry syscall denied` → gVisor 拦截了不允许的系统调用
- `Firecracker MicroVM failed to start` → MicroVM 启动失败
- `Kata shimv2 timeout` → Kata Containers shim 超时
- `WASI operation not permitted` → WASM 运行时拒绝了系统调用
- `Chrome renderer sandbox violation` → Chrome 沙盒违规

---

## 29.4 技术架构图

### 29.4.1 四层隔离栈架构图

```text
硬件层(VT-x) ──► 全虚拟化(KVM/QEMU/ESXi) ──► 半虚拟化(virtio/Xen-PV)
                 │                              │
                 └─► 轻量 VM (Firecracker) ─────┘
                      │
                      └─► 容器(runc/containerd) ──► 沙盒(gVisor/WASM)
```

### 29.4.2 层级关系图

```text
┌─────────────────────────────────────────────────────────────┐
│ L-4 沙盒化层：syscall 过滤                                   │
│ gVisor/Sentry, Firecracker, WASM, Windows Sandbox           │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│ L-3 容器化层：进程级隔离                                      │
│ runc, containerd, Docker, Podman                            │
│ namespace, cgroup, seccomp, capability                      │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│ L-2 半虚拟化层：内核 API 改写                                 │
│ Xen PV, virtio, Hyper-V Enlightenment                       │
│ grant table, event channel, frontend/backend                │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│ L-1 全虚拟化层：完整假硬件                                    │
│ KVM, ESXi, Hyper-V, Xen HVM                                 │
│ VMCS, QEMU, vCPU, vNIC, vmdk                                │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│ L-0 硬件辅助层：CPU 虚拟化指令集                              │
│ VT-x, AMD-V, SEV, TPM                                       │
│ VMX root/non-root, EPT, NPT                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 29.5 快速诊断口诀

> **"先找隔离层，再看谁拦 syscall；VM 里跑 virtio，容器里看 runc，沙盒里找
> Sentry。"**

### 29.5.1 日志关键词快速定位

| 日志关键词                         | 所属层级     | 问题定位                |
| ---------------------------------- | ------------ | ----------------------- |
| `grant table error`                | L-2 半虚拟化 | 半虚拟层内存共享错误    |
| `ContainerCreating`                | L-3 容器化   | 容器创建问题            |
| `Gofer broken pipe`                | L-4 沙盒化   | gVisor 文件系统代理问题 |
| `VMCS corruption`                  | L-1 全虚拟化 | VM 控制结构损坏         |
| `EPT violation`                    | L-0 硬件辅助 | 内存虚拟化错误          |
| `virtio-net driver not loaded`     | L-2 半虚拟化 | virtio 驱动未加载       |
| `OOMKilled`                        | L-3 容器化   | 内存超限被杀            |
| `Sentry syscall denied`            | L-4 沙盒化   | gVisor 拦截系统调用     |
| `Firecracker MicroVM failed`       | L-4 沙盒化   | Firecracker 启动失败    |
| `seccomp: Operation not permitted` | L-3 容器化   | 系统调用被 seccomp 拦截 |

### 29.5.2 故障排查流程

1. **识别日志关键词** → 定位到对应层级（L-0 到 L-4）
2. **查看"黑话/子模块"列** → 找到具体的子模块
3. **检查该子模块的配置/状态** → 深入排查根因

**示例流程**：

```text
日志：grant table error
  ↓
定位：L-2 半虚拟化层
  ↓
子模块：grant table、event channel、blkfront/netfront
  ↓
排查：检查 Xen PV 前端的 grant table 配置、Dom0 后端状态
```

---

## 29.6 问题定位模型：横向请求链 + 纵向隔离栈

### 29.6.0 观测系统作为第四大基础设施

**结论先行**：

> **没有观测系统，就没有"完备"的容器化/分布式系统。**
>
> 观测系统不是"锦上添花"，而是**支撑工程可行性的第一前提**——它与容器运行时、网络
> 、存储并列，构成**第四大基础设施**。

---

#### 29.6.0.1 为什么"必须"而不是"最好"

**核心论点**：

1. **Fail-fast 原则**：

   - 微服务把爆炸半径拆小，也把故障面放大为"千次/秒的跨跳异常"
   - 没有观测 = 故障只能走到用户侧才暴露，违背 Fail-fast
   - 观测系统 = 在问题影响到用户前就被发现和修复

2. **可证明的 SLO**：

   - 对外承诺 p99<200 ms、可用性 99.95%，需要**持续证据链**（telemetry → SLI →
     SLO → Error Budget）
   - 没有观测 = 承诺变"口号"，商务合同失去技术依据
   - 观测系统 = 提供可量化的 SLA 证据

3. **成本可解释**：

   - 云原生资源弹性带来"账单黑洞"：同一时刻可能弹出 1000 核，十分钟后缩回 10 核
   - 没有观测 = 无法回答"谁、哪段代码、哪条网络路径"把钱烧掉"
   - 观测系统 = 精确追踪资源消耗来源

4. **安全与合规**：

   - 等保 2.0/ISO 27001 明确要求**保留 6 个月以上原始日志与审计链**
   - 没有观测 = 审计失败 → 法律风险
   - 观测系统 = 满足合规要求的技术保障

---

#### 29.6.0.2 观测系统本身也是"系统"，需要同等 SLA

**观测系统的 SLA 要求**：

| 维度       | 容器应用系统       | 观测系统                            | 说明                               |
| ---------- | ------------------ | ----------------------------------- | ---------------------------------- |
| **可用性** | 99.95%             | 99.95%（至少不低于业务）            | 观测系统宕机等同于"飞行拆仪表盘"   |
| **可扩展** | HPA 按 QPS 扩容    | 采集端 Agent 按需分片，存储冷热分层 | 观测数据量可能比业务数据量大 10 倍 |
| **多活**   | 业务跨区双活       | 观测存储跨区复制，查询层同城双读    | 确保观测数据不丢失                 |
| **灾备**   | 业务备份到对象存储 | 指标/Trace/日志备份到独立对象存储桶 | 观测数据与业务数据分离备份         |
| **灰度**   | 业务金丝雀发布     | 采集配置、仪表盘、告警规则也要灰度  | 避免观测系统变更影响业务           |

**核心观点**：

> **观测系统一旦宕机，等同于"飞行拆仪表盘"**——业务继续飞，但随时可能撞山。

**设计原则**：

- 观测系统必须与应用系统**同等重要**
- 观测系统必须与应用系统**共享同样的可用性与可扩展设计**
- 观测系统故障不应该影响业务系统运行

---

#### 29.6.0.3 完备性判据（可量化）

**满足以下 6 条，才称"观测完备"**：

| 判据                         | 要求                                                                                                       | 验证方法                           |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| **Three Pillars 齐全**       | Metric（连续计数器）、Trace（请求链）、Log（离散事件）**同时在线**，且可互相关联                           | 检查是否有统一标签关联（trace_id） |
| **Four Golden Signals 覆盖** | Latency、Traffic、Errors、Saturation 对**每一跳服务**都有面板                                              | 检查 Grafana Dashboard 覆盖率      |
| **纵向可下钻**               | 拿到一个 TraceId，可在 3 次点击内看到：应用函数 → 容器 CPU throttle → 内核 virtio 队列满 → 宿主机网卡 drop | 手动测试 Trace 下钻流程            |
| **采样可回溯**               | 全采样保持 24 h；1‰ 采样保存 30 天；**支持回捞原始包（pcap）**                                             | 检查采样策略和存储保留期           |
| **告警收敛率**               | 同一根因只产生 1 条通知，**收敛率 ≥ 90%**（避免"告警风暴"等于没告警）                                      | 监控告警收敛率指标                 |
| **审计可出证**               | 原始日志**不可改、带签名、时间戳可溯源**，满足第三方审计                                                   | 检查日志签名和时间戳完整性         |

**完备性检查清单**：

```bash
# 1. Three Pillars 齐全
curl http://prometheus:9090/api/v1/targets | jq '.data.activeTargets'
curl http://jaeger:16686/api/traces | jq '.data'
curl http://loki:3100/ready

# 2. Four Golden Signals 覆盖
# 检查 Grafana Dashboard 是否覆盖所有服务

# 3. 纵向可下钻
# 手动测试：从 Trace 点击下钻到 Metrics 到 Logs

# 4. 采样可回溯
# 检查 Prometheus retention、Jaeger sampling 策略

# 5. 告警收敛率
# 监控 alertmanager_alerts_received_total vs alertmanager_alerts_sent_total

# 6. 审计可出证
# 检查日志签名、S3 备份策略（Deny Delete）
```

---

#### 29.6.0.4 反例：没有观测的"裸容器"长什么样

**真实案例**：

1. **OOM 被杀无人知晓**：

   - 重启策略=Always，但 OOM 被杀后无人知晓，直到用户投诉
   - **根因**：没有观测 → 无法及时发现容器被 OOMKilled
   - **后果**：用户体验下降，投诉增加

2. **CPU 限流未被发现**：

   - CPU 限流 30% 持续一周，业务 p99 从 200 ms 涨到 1 s
   - 运维以为是"代码慢"，花一周排查业务代码
   - **根因**：没有观测 → 看不到 `container_cpu_cfs_throttled_seconds_total`
   - **后果**：浪费开发资源，延迟问题修复

3. **云账单无法解释**：

   - 一次促销多出 50 万元云账单
   - 无法证明是"哪个服务、哪段函数、哪条网络调用"导致
   - **财务只能全额扣款**
   - **根因**：没有观测 → 无法追踪资源消耗来源
   - **后果**：成本不可控，财务损失

4. **合规失败**：
   - 安全巡检要求出示 6 个月前登录日志
   - K8s 默认只保留 10 MB
   - **合规失败，产品下架**
   - **根因**：没有观测 → 日志保留期不足
   - **后果**：法律风险，业务损失

---

#### 29.6.0.5 落地最小完备集（MVP）

**MVP 组件清单**：

| 组件       | 功能                    | 建议实现                                           | 最小资源     |
| ---------- | ----------------------- | -------------------------------------------------- | ------------ |
| **采集**   | Metric/Trace/Log 三合一 | OpenTelemetry Collector DaemonSet                  | 2 CPU / 4 GB |
| **存储**   | Metric 热/冷分层        | Prometheus + Thanos/Cortex                         | 4 CPU / 16GB |
| **存储**   | Trace & Log             | ClickHouse 或 Tempo + Loki                         | 4 CPU / 32GB |
| **关联**   | 统一标签                | `cluster,namespace,pod,container,trace_id,span_id` | N/A          |
| **可视化** | 统一入口                | Grafana + 统一导航栏（Golden Signals/集群/审计）   | 2 CPU / 4GB  |
| **告警**   | 收敛+分级               | Alertmanager + 值班平台（PagerDuty/飞书）          | 1 CPU / 2GB  |
| **审计**   | 只读对象存储            | 每日快照到独立 COS/S3 桶，桶策略 **Deny Delete**   | 按量付费     |

**MVP 部署示例**：

```yaml
# OpenTelemetry Collector DaemonSet
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: otel-collector
spec:
  template:
    spec:
      containers:
      - name: otel-collector
        image: otel/opentelemetry-collector:latest
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi

# Prometheus 存储
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      retention: 24h
    scrape_configs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod

# 审计备份（CronJob）
apiVersion: batch/v1
kind: CronJob
metadata:
  name: audit-backup
spec:
  schedule: "0 2 * * *"  # 每天凌晨 2 点
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: awscli:latest
            command:
              - /bin/sh
              - -c
              - |
                # 备份日志到 S3（Deny Delete 策略）
                aws s3 sync /var/log/audit s3://audit-backup-$(date +%Y%m%d)/
```

---

#### 29.6.0.6 结论（一句话收拢）

> **容器化+分布式把"复杂度"从单体搬到网络，观测系统是把"复杂度"重新变"可解释"的
> 唯一桥梁。**
>
> 没有观测，就没有 SLA、没有成本、没有安全、没有合规——**因此它与应用系统同等重要
> ，且必须共享同样的可用性与可扩展设计。**

**观测系统的战略地位**：

- **与容器运行时、网络、存储并列**，构成第四大基础设施
- **不是可选项，而是必需项**
- **必须有同等的 SLA 保障**

---

### 29.6.1 定位模型概述

**前置条件**：

> **重要提示**：在使用本问题定位模型之前，请确保已阅读
> [29.6.0 观测系统作为第四大基础设施](#2960-观测系统作为第四大基础设施)，了解为
> 什么观测系统是必需的，以及如何部署完备的观测系统。

**核心思想**：

把"四层隔离栈 + 分布式 + 可观测性"放在同一张纸上，你会发现：

- **问题定位** = 在**垂直技术栈**里找"哪一层丢包/卡死"，同时在**水平请求链**里找
  "哪一跳超时"

**定位工具**：

- **OTLP（OpenTelemetry 协议）**：给你**横向请求链**的"望远镜"——先水平锁定哪一跳
  慢
- **eBPF**：给你**纵向隔离栈**的"显微镜"——再垂直钻到四层隔离栈里，看是 cgroup
  throttle、seccomp 风暴、virtio 队列满，还是宿主机磁盘到顶

**横纵耦合定位模型图示**：

```text
横向请求链（OTLP Trace）          纵向隔离栈（eBPF）
─────────────────────────         ────────────────────────

Service A ──1.2s──> Service B      L-4 沙盒化：Sentry syscall denied
    │              │             L-3 容器化：CPU throttle, veth latency
    │              │             L-2 半虚拟：virtio rx_queue full
    │              │             L-1 全虚拟：VMCS corruption
    │              │             L-0 硬件：   EPT violation
    ↓              ↓             ────────────────────────
┌─────────┐      ┌─────────┐
│ Jaeger  │      │ xdpdrop │ ← 交叉定位点
│ Trace   │ <──> │ cpudist │   Service B 的 span duration=1.2s
│ (横向)  │      │ (纵向)  │   关联到 eBPF 发现 virtio rx_queue 满
└─────────┘      └─────────┘   根因：mDNS 风暴占满 virtio 环
    │              │
    └──────┬───────┘
           ↓
      问题定位结果
      服务 B → virtio 队列满 → mDNS 风暴
```

**两层数据交叉定位**：

在「秒级」精确定位：**"慢在业务、容器、沙盒、半虚拟还是主机"**，而不再逐层盲人摸
象。

---

### 29.6.2 事故背景（简化版）

**用户投诉**：

> "下单接口 95% 延迟从 200 ms 涨到 2 s，偶发 5 s+，重启就好了，但 30 min 后又慢
> 。"

**拓扑**：

```text
Ingress-Nginx(Pod) → OrderService(Pod) → PaymentSidecar(Pod) → PostgreSQL(VM)
```

---

### 29.6.3 五步定位法

| 步骤                 | 水平链路（OTLP Trace）                                                        | 垂直栈（eBPF/内核）                                                  | 现场黑话示例                                                     | 判定结论                                                                               |
| -------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **① 横向先找慢跳**   | Jaeger trace 显示`order-7b9d9`span 自身 200 ms，但`payment-sidecar`span 1.8 s | 同一时刻 CPU 指标正常                                                | `span.kind=client http.status=200 duration=1.83s`                | 瓶颈在 sidecar 容器内部，不在业务代码                                                  |
| **② 垂直看容器层**   | `container_cpu_cfs_throttled_seconds_total`飙高 30%                           | eBPF `cpudist` 发现 Pod 连续 100 ms 被 throttle                      | `Throttled for 120 ms since cpu.cfs_quota_us=2000 but used 2120` | sidecar 容器 quota 给太小，触发 Cgroup 限流                                            |
| **③ 再下探沙盒层**   | 该 sidecar 实际跑在 `runsc` (gVisor)                                          | eBPF `funclatency` 显示 `seccomp_run_filter` 平均 90 µs→ 突然 900 µs | `runsc-sentry[pid=1234] seccomp: syscall=connect denied 0x5`     | 业务开始连新 Redis，但 runsc 缺 syscall 白名单，每次 connect 都走「慢路径」            |
| **④ 继续到半虚拟层** | sidecar 日志报`virtio-net tx queue 0 is full`                                 | eBPF `xdpdrop` 计数器上涨                                            | `virtio_net: eth0: tx timeout`                                   | 容器 throttle 导致发包突刺，virtio 环形队列满，触发 tx timeout→ 重传 → 延迟再加 400 ms |
| **⑤ 兜底到主机层**   | 同一 VM 上其他 Pod 也涨延迟                                                   | eBPF `biolatency` 显示 p99 磁盘延迟从 2 ms→20 ms                     | `await 22.1 ms, %util 98.3`                                      | 宿主机云盘达到 IOPS 上限，原因是隔壁「日志收集 DaemonSet」疯狂写                       |

---

### 29.6.4 信号来源与工具对照表

| 信号类别      | 协议/工具                  | 典型指标/事件                               | 作用层级      |
| ------------- | -------------------------- | ------------------------------------------- | ------------- |
| **Trace**     | OTLP (Jaeger/Prometheus)   | `duration`, `span.kind`, `net.peer.ip`      | 横向请求链    |
| **Metric**    | OTLP/Prometheus            | `container_cpu_cfs_throttled_seconds_total` | 容器层        |
| **Log**       | OTLP/FluentBit             | `seccomp: syscall=connect denied`           | 沙盒层        |
| **eBPF CPU**  | `bcc/cpudist`              | on-CPU/off-CPU 分布                         | 内核 → 容器   |
| **eBPF 网络** | `xdpdrop`, `tcplife`       | retrans, RTT, tx_queue 满                   | 半虚拟 virtio |
| **eBPF 磁盘** | `biolatency`, `fileslower` | await, %util                                | 主机块设备    |

---

### 29.6.5 定位口诀（背下来）

> **"横向先 trace，纵向再 bpf；quota 先看 throttle，virtio 再看 tx_queue；沙盒慢
> 就加 syscall，主机飙就查 io。"**

**与 29.5 口诀的配合**：

- **29.5 口诀**：用于根据日志关键词直接定位层级
- **29.6 口诀**：用于在可观测性数据中按横向 → 纵向顺序定位问题

---

### 29.6.6 实战一键脚本（示例）

```bash
#!/bin/bash

# 1. 横向：找最慢 span
echo "=== 步骤 1: 横向找慢跳 ==="
jaeger-query "...service=payment-sidecar ...minDuration=1s"

# 2. 垂直：容器是否被 throttle
echo "=== 步骤 2: 垂直看容器层 ==="
kubectl top pod payment-sidecar
curl -s http://node:9100/metrics | grep throttled_seconds

# 3. 垂直：eBPF 看 CPU 被限制多久
echo "=== 步骤 3: 垂直看沙盒层 ==="
/usr/share/bcc/tools/cpudist -p $(pgrep -f runsc-sentry) 10
/usr/share/bcc/tools/funclatency seccomp_run_filter 10

# 4. 垂直：virtio 网卡是否丢包
echo "=== 步骤 4: 垂直看半虚拟层 ==="
/usr/share/bcc/tools/xdpdrop -d eth0 10
dmesg | grep -i "virtio_net.*tx.*timeout"

# 5. 主机：磁盘是否到顶
echo "=== 步骤 5: 垂直看主机层 ==="
/usr/share/bcc/tools/biolatency 10
iostat -x 1
```

---

### 29.6.7 定位流程可视化

**横纵耦合定位流程图**：

```text
问题现象：延迟突增（200ms → 2s）
    │
    ├─[横向定位] OTLP Trace (Jaeger)
    │   │
    │   ├─ 步骤1：查找慢 span
    │   │   Filter: duration > 1s
    │   │   Result: payment-sidecar span = 1.8s
    │   │
    │   └─ 步骤2：提取五元组
    │       net.peer.ip = 10.244.3.17
    │       net.peer.port = 8080
    │       trace_id = abc123
    │
    ├─[纵向定位] eBPF Tools
    │   │
    │   ├─ 步骤3：容器层检查
    │   │   Tool: cpudist
    │   │   Result: Pod 连续 100ms 被 throttle
    │   │
    │   ├─ 步骤4：沙盒层检查
    │   │   Tool: funclatency (seccomp)
    │   │   Result: seccomp 平均 90µs→900µs
    │   │
    │   └─ 步骤5：半虚拟层检查
    │       Tool: xdpdrop
    │       Result: virtio tx_queue 满
    │
    └─[根因确认] 数据关联
        │
        ├─ 时间戳同步：OTLP span timestamp = eBPF event timestamp
        ├─ 五元组匹配：OTLP net.peer.* = eBPF sk->sk_common.*
        └─ 根因确认：gVisor syscall 慢路径 + CPU throttle → virtio 队列满
```

```text
横向定位（OTLP Trace）
─────────────────────
Ingress-Nginx (50ms)
    ↓
OrderService (200ms) ✅ 正常
    ↓
PaymentSidecar (1800ms) ⚠️ 慢跳定位
    ↓
PostgreSQL (10ms)

                ↓ 交叉点

纵向定位（eBPF/内核）
─────────────────────
L-4 沙盒层：gVisor seccomp 慢路径 ⚠️
    ↓
L-3 容器层：Cgroup CPU throttle ⚠️
    ↓
L-2 半虚拟层：virtio tx_queue 满 ⚠️
    ↓
L-1 全虚拟层：VM 正常
    ↓
L-0 硬件辅助层：正常

最终根因：沙盒层 syscall 白名单缺失 + 容器层 quota 过小 →
          CPU throttle → virtio 队列满 → 延迟累积 1.8s
```

---

### 29.6.8 常见问题定位速查

| 问题现象     | 横向信号（OTLP）                | 纵向信号（eBPF/内核）         | 根因层级     | 解决方案                |
| ------------ | ------------------------------- | ----------------------------- | ------------ | ----------------------- |
| 延迟突增 2s  | span duration 突增              | `cpudist` 显示 off-CPU 100ms+ | L-3 容器层   | 调整 `cpu.cfs_quota_us` |
| 偶发 5s 超时 | trace 断点                      | `xdpdrop` 计数器上涨          | L-2 半虚拟层 | 检查 virtio 队列大小    |
| seccomp 慢   | span 内部延迟                   | `funclatency` seccomp 900µs   | L-4 沙盒层   | 添加 syscall 白名单     |
| 磁盘 IO 高   | 所有 span 延迟                  | `biolatency` p99 20ms+        | 主机层       | 检查 DaemonSet 日志收集 |
| 内存泄漏     | trace 正常，metric 内存持续增长 | `memleak` 显示未释放内存      | L-3 容器层   | 检查应用内存管理        |

---

### 29.6.9 eBPF 工具速查表

**eBPF 工具分类与使用场景**：

| eBPF 工具       | 类别 | 作用层级    | 典型用途                        | 输出示例                                  |
| --------------- | ---- | ----------- | ------------------------------- | ----------------------------------------- |
| **cpudist**     | CPU  | 内核 → 容器 | 分析 CPU 被 throttle 的时间分布 | `on-CPU: 100ms, off-CPU: 120ms`           |
| **funclatency** | 函数 | 沙盒层      | 测量函数调用延迟（如 seccomp）  | `avg: 90µs, max: 900µs`                   |
| **xdpdrop**     | 网络 | 半虚拟层    | 统计 XDP 丢包数量               | `drops: 1234 packets`                     |
| **tcplife**     | 网络 | 半虚拟层    | 跟踪 TCP 连接生命周期           | `connect: 192.168.1.1:80, duration: 1.8s` |
| **biolatency**  | 磁盘 | 主机层      | 分析块设备 IO 延迟分布          | `p99: 20ms, p95: 10ms`                    |
| **fileslower**  | 文件 | 主机层      | 找出慢文件操作                  | `file: /var/log/app.log, latency: 50ms`   |
| **memleak**     | 内存 | 容器层      | 检测内存泄漏                    | `unfreed memory: 1024 MB`                 |
| **runqlat**     | CPU  | 内核层      | 分析进程调度延迟                | `p99: 5ms`                                |
| **argdist**     | 通用 | 内核层      | 统计函数参数分布                | `syscall: connect, count: 1000`           |
| **stackcount**  | 通用 | 内核层      | 统计堆栈调用频率                | `kernel stack: 500 times`                 |

**eBPF 工具安装**：

```bash
# 安装 BCC 工具集（Ubuntu/Debian）
sudo apt-get install bpfcc-tools linux-headers-$(uname -r)

# 安装 BCC 工具集（CentOS/RHEL）
sudo yum install bcc-tools kernel-devel

# 工具通常位于
/usr/share/bcc/tools/
```

**常用 eBPF 命令示例**：

```bash
# 1. 检查 CPU throttle（容器层）
/usr/share/bcc/tools/cpudist -p $(pgrep -f container-process) 10

# 2. 检查 seccomp 延迟（沙盒层）
/usr/share/bcc/tools/funclatency seccomp_run_filter 10

# 3. 检查网络丢包（半虚拟层）
/usr/share/bcc/tools/xdpdrop -d eth0 10

# 4. 检查磁盘延迟（主机层）
/usr/share/bcc/tools/biolatency 10

# 5. 检查内存泄漏（容器层）
/usr/share/bcc/tools/memleak -p $(pgrep -f container-process)

# 6. 跟踪 TCP 连接（网络层）
/usr/share/bcc/tools/tcplife -p $(pgrep -f container-process) 10
```

---

### 29.6.10 小结

**OTLP + eBPF 联合定位**：

- **OTLP** 给你「请求链望远镜」——先水平锁定哪一跳慢
- **eBPF** 给你「内核显微镜」——再垂直钻到四层隔离栈里，看是：
  - cgroup throttle
  - seccomp 风暴
  - virtio 队列满
  - 宿主机磁盘到顶

**两层数据交叉定位**：

在「秒级」精确定位：**"慢在业务、容器、沙盒、半虚拟还是主机"**，而不再逐层盲人摸
象。

---

### 29.6.11 快速定位流程图

**问题定位决策树**：

```text
问题现象：延迟突增 / 偶发超时
    ↓
步骤 1: 横向定位（OTLP Trace）
    ├─ 查看 Jaeger trace，找到最慢的 span
    └─ 如果 span duration 突增 → 进入步骤 2
    ↓
步骤 2: 纵向定位 - 容器层（eBPF CPU）
    ├─ 检查 container_cpu_cfs_throttled_seconds_total
    ├─ 使用 cpudist 查看 CPU throttle 时间
    └─ 如果 throttle > 100ms → 调整 cpu.cfs_quota_us
    ↓
步骤 3: 纵向定位 - 沙盒层（eBPF 函数）
    ├─ 检查 runsc-sentry 进程
    ├─ 使用 funclatency seccomp_run_filter
    └─ 如果 seccomp 延迟 > 900µs → 添加 syscall 白名单
    ↓
步骤 4: 纵向定位 - 半虚拟层（eBPF 网络）
    ├─ 检查 virtio-net tx queue
    ├─ 使用 xdpdrop 查看网络丢包
    └─ 如果 tx_queue 满 → 检查 virtio 队列大小
    ↓
步骤 5: 纵向定位 - 主机层（eBPF 磁盘）
    ├─ 使用 biolatency 查看磁盘延迟
    ├─ 使用 iostat 查看磁盘利用率
    └─ 如果 p99 > 20ms → 检查 DaemonSet 日志收集
```

**定位工具快速选择**：

| 问题类型   | 横向工具        | 纵向工具    | 检查层级     |
| ---------- | --------------- | ----------- | ------------ |
| 延迟突增   | Jaeger trace    | cpudist     | L-3 容器层   |
| 偶发超时   | trace 断点      | xdpdrop     | L-2 半虚拟层 |
| seccomp 慢 | span 内部延迟   | funclatency | L-4 沙盒层   |
| 磁盘 IO 高 | 所有 span 延迟  | biolatency  | 主机层       |
| 内存泄漏   | metric 内存增长 | memleak     | L-3 容器层   |

---

### 29.6.12 网络定位专题：横向生命线

#### 29.6.12.0 为什么网络必须作为独立维度

**核心论点**：

1. **四层隔离栈都是纵向资源边界**：

   - L-0 硬件辅助层：CPU 模式切换边界
   - L-1 全虚拟化层：完整假硬件边界
   - L-2 半虚拟化层：内核 API 改写边界
   - L-3 容器化层：进程级隔离边界
   - L-4 沙盒化层：syscall 过滤边界

2. **网络是横向生命线**：

   - 同一层内跨实例通信（Pod → Pod）
   - 跨层间通信（Pod → VM，Sidecar → 宿主机）
   - 不是"第 5 层"，而是在**每一隔离层内都出现一张独立的"网络切片"**

3. **性能劣化往往是横纵耦合**：

   - 横向某跳超时（OTLP Trace 显示 duration 1.83s）
   - 本质是纵向某层队列丢包或调度延迟（eBPF 显示 virtio rx_queue 满）

4. **可观测体系必须"双轴对齐"**：
   - **X 轴（请求链）**：用 OTLP 统一语义，定位"哪一跳慢"
   - **Y 轴（内核栈）**：用 eBPF 零开销采样，定位"哪一层卡"
   - 两轴交叉，才能把"200 ms → 2 s"一类偶发抖动解释成**可证伪、可复现、可修
     复**的技术事实

**问题定位公式**：

> **问题定位 = 先选网络切片，再按"队列 → 调度 → 协议"逐层下钻**

**双轴定位算法**：

输入：一条 OTLP span（duration=1.83 s，peer=10.244.3.17:8080）

算法：

1. **横向定位（OTLP）**：

   - 用 `{net.peer.ip, net.peer.port, net.sock.family}` 当 key
   - join eBPF `tcplife` 表 → 拿到 RTT=120 ms，重传=42

2. **纵向定位（eBPF）**：

   - RTT 突增 → 转 `tcpdrop`/`xdpdrop` → 发现 `virtio_net rx_queue 0 full` 50
     kpps

3. **根因追踪**：

   - 50 kpps 来源 →`tcpdump` 过滤 → 发现 mDNS 5353 UDP 洪水
   - 再 join k8s.labels 知源 Pod 为 `avahi-daemon-xxx`

4. **修复验证**：
   - 修复：给 avahi 加 `rate_limit` + 给 virtio 开 `napi_budget=256`
   - 复测：RTT 降回 18 ms
   - 关闭回路：把修复后指标写回 OTLP metric → 仪表盘持续验证 p99<200 ms

**算法复杂度**：

- **时间复杂度**：O(seconds) 级人工干预
- **空间复杂度**：O(GB) 级数据全部在内存环形缓冲区完成
- **优势**：**无需抓完整 pcap**，实时分析

---

#### 29.6.12.0.1 网络在四种隔离形态中的真实"切片"

**核心观点**：

网络不是"第 5 层"，而是在**每一隔离层内都出现一张独立的"网络切片"**。

| 形态         | 网络设备                           | 数据面实现                    | 控制面实现              | 常见行话                   |
| ------------ | ---------------------------------- | ----------------------------- | ----------------------- | -------------------------- |
| **全虚拟化** | vmxnet3 / E1000 / virtio-net       | VMXNET3 驱动 → 宿主机 vSwitch | vCenter DVS             | VMotion 网络、端口组、LLDP |
| **半虚拟化** | virtio-net frontend/backend        | 共享环 + grant copy           | xen-netback / vhost-net | virtqueue、event channel   |
| **容器化**   | veth pair + CNI                    | tc/eBPF + iptables/ipvs       | kube-controller         | conntrack、SNAT、PodCIDR   |
| **沙盒化**   | 用户态 netstack(gVisor) 或 microVM | sentry→tap→ 宿主机            | runsc / firecracker     | strace 风暴、loopback mtu  |

**定位方法**：

> **结论**：问题定位 = 先选切片，再按"队列 → 调度 → 协议"逐层下钻

---

#### 29.6.12.0.2 OTLP 如何给出"横向坐标"

**OpenTelemetry 语义约定（semantic-convention v1.21）**：

OpenTelemetry 把一次 RPC 的**网络相位**拆成 6 个标准化标签：

| OTLP 标签                                   | 含义         | 示例值                       |
| ------------------------------------------- | ------------ | ---------------------------- |
| `net.transport`                             | 传输协议     | `ip_tcp` / `ip_udp` / `unix` |
| `net.peer.ip` / `net.peer.port`             | 对端 socket  | `10.244.3.17:8080`           |
| `net.host.ip` / `net.host.port`             | 本端 socket  | `10.244.1.5:45678`           |
| `net.sock.family`                           | 套接字家族   | `inet` / `inet6` / `unix`    |
| `http.status_code` / `rpc.grpc.status_code` | 应用语义     | `200` / `0`                  |
| `duration`                                  | 端到墙钟时间 | `1.83s`                      |

**价值**：

1. **与 eBPF 五元组 100% 对齐**：

   - `{net.peer.ip, net.peer.port, net.host.ip, net.host.port, net.sock.family}`
     = eBPF 五元组
   - 可直接 `join`，无需额外映射

2. **支持"无侵入"注入**：

   - sidecar、service-mesh、Go/Java auto-instrument 均自动吐出
   - 无需修改应用代码

3. **把"黑盒网络"变成"白盒标签"**：
   - 为后续逐层下钻提供**绝对坐标**
   - 支持精确的问题定位

---

#### 29.6.12.0.3 eBPF 如何给出"纵向坐标"

**eBPF 核心优势**：

eBPF 程序**运行在内核态**，对业务零延迟（< 1 µs），却可采集到**每一层网络切
片**的队列、丢包、重传、软中断事件。

**eBPF 探针附着点与对应隔离层**：

| 探针附着点                       | 对应隔离层 | 关键事件             | 字段示例                                |
| -------------------------------- | ---------- | -------------------- | --------------------------------------- |
| `kprobe:tcp_retransmit_skb`      | 全局       | 重传类型 & 原因      | `sk->__sk_common.skc_dport = 8080`      |
| `tracepoint:virtio_net:rx_queue` | 半虚拟     | virtqueue 长度       | `vq->num_free < 10` → 即将丢包          |
| `kprobe:veth_xmit`               | 容器       | veth 软中断延迟      | `napi->weight = 64` → 调度饥饿          |
| `xdp` / `tc egress`              | 容器/主机  | 网卡级丢包           | `xdp_drop` counter                      |
| `kprobe:conntrack_insert`        | 容器 SNAT  | conntrack 哈希冲突   | `stat->insert_failed++`                 |
| `uprobe:/runsc-sentry:connect`   | 沙盒       | 用户态 netstack 延迟 | `sentry.socket.connect latency = 120ms` |

**eBPF 价值**：

> **结论**：eBPF 把"网络黑盒"拆成**可计数、可直方图、可关联到五元组**的内核事件
> ；与 OTLP 标签 join 后，就能从"10.244.3.17:8080 慢"一路钻到"virtio 环满"或
> "conntrack 插入失败"。

**关联方法**：

- 通过 `net.sock.*` + `ebpf_id=skb->sk->sk_cookie` 做一次 exact match
- 即可把**内核事件**挂到**应用 span**上
- 细到"一次 `tcp_retransmit_skb` 对应哪条 traceId"

---

#### 29.6.12.0.4 常见反驳与充分回应

**反驳 1**："有 VPC Flow Log / iptables LOG 就够，何必 eBPF？"

**回应**：

- **Flow Log 粒度=1 min，字段=五元组+字节**：

  - 无法告诉你"**为什么**丢包（queue full vs conntrack vs TCP RTO）"
  - 只能告诉你"丢了"，不能告诉你"为什么丢"

- **eBPF 事件粒度=µs，字段=内核栈+队列长度**：
  - 可直接定位根因
  - 看到内核函数调用链、队列状态、调度延迟

**反驳 2**："OTLP 网络标签只到 socket，不够细？"

**回应**：

- 通过 `net.sock.*` + `ebpf_id=skb->sk->sk_cookie` 做一次 exact match
- 即可把**内核事件**挂到**应用 span**上
- 细到"一次 `tcp_retransmit_skb` 对应哪条 traceId"

**反驳 3**："eBPF 需要高版本内核，4.14 怎么办？"

**回应**：

- **使用 kprobe 回退**：

  - 回退到 `tcp_set_state`/`tcp_rcv_established`
  - 功能不变，只是写法多两行

- **容器层老到 3.10**：
  - 把 eBPF 程序挂到**宿主机**即可
  - **对 Guest 无侵入**，仍能观测 Guest 网络流量

---

#### 29.6.12.0.5 生产落地 Checklist

**1. 节点层**：

- ✅ 系统内核 ≥ 4.19（启用 BTF，一次编译到处跑）
- ✅ 开启 `CONFIG_KPROBES=y / CONFIG_DEBUG_INFO_BTF=y`
- ✅ 确认内核支持 eBPF（`cat /proc/config.gz | grep BPF`）

**2. 采集层**：

- ✅ 以 DaemonSet 运行 `eBPF-agent`（Cilium/Inspektor Gadget/Kindling 均可）
- ✅ 把指标转成 OTLP 格式
- ✅ 关键指标采集：
  - `tcp_retrans`：TCP 重传次数
  - `xdp_drop`：XDP 丢包计数
  - `veth_xmit_latency`：veth 发送延迟
  - `conntrack_insert_failed`：conntrack 插入失败
  - `virtio_queue_len`：virtio 队列长度

**3. 存储层**：

- ✅ 指标写 Prometheus（长期存储）
- ✅ trace 写 Jaeger/Tempo（7-14 天保留）
- ✅ 用 `sk_cookie` 或 `net.sock.*` 做外键关联

**4. 可视化**：

- ✅ Grafana 模板：
  - 横轴 = trace duration
  - 纵轴 = ebpf 丢包/重传
  - 点击慢 span 自动下钻到内核事件

**5. 告警**：

- ✅ `rate(tcp_retransmits)>0 && rate(xdp_drop)>0` → 立即触发网络组 OnCall
- ✅ `duration p95 > 1s` → Warning 级别告警
- ✅ `xdpdrop > 1kpps` → Critical 级别告警

---

#### 29.6.12.0.6 结论（一句话收拢）

> **"网络问题 ≠ 黑魔法；OTLP 给你横坐标，eBPF 给你纵坐标，两轴一交叉，任何'偶发
> 延迟高'都能被证伪成'某层队列满 or 丢包'，从而可修复、可验证、可关闭。"**

---

**网络定位核心思想**：

网络本身不是"隔离层级"，而是**贯穿四层隔离栈的横向生命线**。

OTLP 和 eBPF 在网络侧的定位逻辑，与 CPU/内存完全一致——

**先横向看"哪一跳丢包/超时"，再纵向看"这一跳内部流量卡在哪一层隔离边界"**。

#### 29.6.12.1 网络在三栈里的"切片"视图

| 层级           | 网络设备/模块                                | 常见黑话                                                | 典型问题现象                                        |
| -------------- | -------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------- |
| **L-0 硬件**   | SR-IOV VF、SmartNIC、DPDK                    | VF reset、LLDP flapping、PXE hang                       | 节点重启后 VF 起不来，Pod 网络 NotReady             |
| **L-1 全虚拟** | vSwitch(OVS/Linux bridge)、tap、vmxnet3      | vNIC tx_timeout、virtio_net rx_queue 0 stuck            | VM 里 `ping` 通但 `iperf` 只有 100 Mbps             |
| **L-2 半虚拟** | virtio-net frontend/backend、vhost-net、vDPA | grant copy hypercall fail、virtqueue full               | AWS Xen PV 实例高并发报 `netif_poll` 死锁           |
| **L-3 容器**   | veth、CNI、iptables/ipvs、eBPF TC            | veth peer missing、conntrack table full、SNAT collision | 同一 Node 跨 Pod 通信 2 ms→20 ms                    |
| **L-4 沙盒**   | gVisor sentry->netstack、WASM wasmtime-wasi  | strace 风暴+tcp retrans、loopback mtu 1500→65535        | sidecar 跑 runsc，偶发 5 s 延迟，tcpdump 看全是重传 |

---

#### 29.6.12.2 横向：OTLP 网络 trace

**OpenTelemetry 网络语义化指标**：

OpenTelemetry 定义了**语义化网络指标 & span kind**，一条 HTTP 调用会自动带上：

```json
{
  "name": "HTTP GET /pay",
  "kind": "CLIENT",
  "attributes": {
    "net.peer.ip": "10.244.3.17",
    "net.peer.port": 8080,
    "net.transport": "ip_tcp",
    "net.host.name": "payment-sidecar",
    "net.sock.family": "inet",
    "http.status_code": 200,
    "duration": 1.83
  }
}
```

**使用方式**：

1. **在 Jaeger 里直接过滤** `duration > 1s && net.peer.ip = 10.244.3.17` → 锁定
   慢跳
2. **把 `net.sock.family` 当标签**，与 eBPF 里的五元组做关联，实现"秒级对齐"

**网络 trace 关键属性**：

| OTLP 属性          | 含义                     | 用于定位           |
| ------------------ | ------------------------ | ------------------ |
| `net.peer.ip`      | 目标 IP                  | 锁定慢跳的目标地址 |
| `net.peer.port`    | 目标端口                 | 锁定慢跳的目标端口 |
| `net.transport`    | 传输协议（ip_tcp/udp）   | 区分 TCP/UDP 流量  |
| `net.host.name`    | 源服务名                 | 识别请求来源       |
| `net.sock.family`  | 套接字家族（inet/inet6） | 与 eBPF 五元组关联 |
| `duration`         | 请求延迟                 | 判断是否慢跳       |
| `http.status_code` | HTTP 状态码              | 判断是否 502/504   |

---

#### 29.6.12.3 纵向：eBPF 网络显微镜

**eBPF 网络工具速查**：

| 工具/探针          | 作用层级  | 关键指标                | 对应黑话/示例                                             |
| ------------------ | --------- | ----------------------- | --------------------------------------------------------- |
| **tcplife**        | 容器/主机 | 五元组、RTT、重传       | `10.244.1.5:45678→10.244.3.17:8080 RTT 120ms > 基线 20ms` |
| **tcpdrop**        | 内核      | 丢包原因、内核栈        | `location:tcp_rcv_state_process reason:TIMEWAIT ACK`      |
| **tcpretrans**     | 全路径    | 重传类型(RTO/Fast/RACK) | `RTO 重传 3 次→说明 RTT 突增或黑洞`                       |
| **xdpdrop/xdpcap** | 驱动层    | 网卡 RX 丢包            | `virtio_net:xdp_drop 50kpps` → virtio 环满了              |
| **conntrack -S**   | 容器 SNAT | insert_failed、drop     | `insert_failed 2000/s` → 端口耗尽或五元组冲突             |
| **veth_latency**   | veth peer | 软中断调度延迟          | `net_rx_action 占用 CPU 30ms` → ksoftirqd 饥饿            |
| **sr-iov/vfstat**  | 硬件 VF   | VF reset count          | `VF 7 reset 5 次` → 固件 bug 或 LLDP 震荡                 |

**eBPF 网络工具使用场景**：

- **tcplife**：分析 TCP 连接生命周期，找出 RTT 突增的连接
- **tcpdrop**：定位内核层丢包原因
- **tcpretrans**：分析重传模式，判断是 RTO 还是 Fast Retransmit
- **xdpdrop**：检查驱动层（virtio）是否丢包
- **conntrack**：检查 SNAT 表是否满
- **veth_latency**：分析 veth 软中断延迟
- **vfstat**：检查 SR-IOV VF 状态

---

#### 29.6.12.4 网络定位五步法（接前述故障）

**网络定位完整流程**：

| 步骤            | 横向(OTLP)                        | 纵向(eBPF)                                  | 现场黑话                   | 结论                                          |
| --------------- | --------------------------------- | ------------------------------------------- | -------------------------- | --------------------------------------------- |
| **① 找慢跳**    | trace 显示`payment→sidecar`1.83 s | 同时间段`tcplife` RTT 从 20 ms→120 ms       | `10.244.3.17 RTT 120ms`    | 网络 RTT 突增，不是业务代码                   |
| **② 看重传**    | `tcpretrans` 记录 3 次 RTO        | 重传间隔 200 ms→800 ms→1.2 s                | `RTO 3.0 retrans_total=42` | 说明链路出现"黑洞"或 buffer 满                |
| **③ 查 virtio** | 节点`xdpdrop` 计数 50 kpps        | `virtio_net rx_queue 0 full`                | `xdp_drop 50000/s`         | virtio 环形队列被 UDP 洪水打满                |
| **④ 追来源**    | `conntrack -S` 插入失败 0         | `tcpdump -i vethxxx` 看到 500 Mbps UDP 5353 | `_mdns` flood              | 隔壁 DaemonSet 误发 mDNS 风暴，占满 virtio 环 |
| **⑤ 验证修复**  | 再跑`tcplife` RTT 回落 18 ms      | trace duration 降至 220 ms                  | `RTT p99 18ms`             | 限速+抑制 mDNS 后，业务延迟恢复               |

**网络定位决策流程**：

```text
问题现象：延迟突增 1.83s / 偶发 502 / RST
    ↓
步骤 1: 横向定位（OTLP Trace）
    ├─ 查看 Jaeger trace，找到最慢的 span
    ├─ 过滤 duration > 1s && net.peer.ip = 10.244.3.17
    └─ 如果 span duration 突增 → 进入步骤 2
    ↓
步骤 2: 纵向定位 - 网络层（eBPF tcplife）
    ├─ 使用 tcplife 查看 RTT 分布
    ├─ 使用 tcpretrans 查看重传次数
    └─ 如果 RTT > 100ms → 进入步骤 3
    ↓
步骤 3: 纵向定位 - 驱动层（eBPF xdpdrop）
    ├─ 检查 virtio-net rx_queue 是否满
    ├─ 使用 xdpdrop 查看驱动层丢包
    └─ 如果 xdp_drop > 10kpps → 进入步骤 4
    ↓
步骤 4: 纵向定位 - 容器层（conntrack/veth）
    ├─ 检查 conntrack 表是否满
    ├─ 使用 tcpdump 查看 veth 流量
    └─ 如果发现 UDP 洪水 → 定位来源
    ↓
步骤 5: 验证修复
    ├─ 修复后再次运行 tcplife
    ├─ 验证 trace duration 是否恢复正常
    └─ 如果 RTT < 20ms → 问题解决
```

---

#### 29.6.12.5 网络定位一键脚本

**生产可直接使用的脚本**：

```bash
#!/bin/bash

# 1. 横向：拉取 OTLP 网络指标
echo "=== 步骤 1: 横向找慢跳 ==="
curl -s http://otel-collector:8889/metrics | \
  grep -E 'net_peer_ip|duration' | grep 10.244.3.17

# 2. 纵向：五元组级 RTT/重传
echo "=== 步骤 2: 纵向看网络层 ==="
/usr/share/bcc/tools/tcplife | grep 10.244.3.17
/usr/share/bcc/tools/tcpretrans | grep 10.244.3.17

# 3. 驱动层：virtio 是否丢包
echo "=== 步骤 3: 纵向看驱动层 ==="
/usr/share/bcc/tools/xdpdrop -d eth0 1

# 4. veth 软中断
echo "=== 步骤 4: 纵向看容器层 ==="
/usr/share/bcc/tools/softirqs 1 | grep net_rx

# 5. conntrack 是否爆表
echo "=== 步骤 5: 纵向看 SNAT ==="
conntrack -S | grep -E 'insert_failed|drop'

# 6. 抓包分析（如果需要）
echo "=== 步骤 6: 抓包分析 ==="
tcpdump -i vethxxxx -n -c 100 'host 10.244.3.17' -w /tmp/capture.pcap
```

**网络定位工具组合**：

```bash
# 组合 1: 快速定位 RTT 突增
jaeger-query "net.peer.ip=10.244.3.17 duration>1s" && \
  /usr/share/bcc/tools/tcplife | grep 10.244.3.17

# 组合 2: 定位重传问题
/usr/share/bcc/tools/tcpretrans | head -20 && \
  /usr/share/bcc/tools/tcpdrop

# 组合 3: 定位 virtio 丢包
/usr/share/bcc/tools/xdpdrop -d eth0 10 && \
  dmesg | grep -i "virtio_net.*drop"

# 组合 4: 定位 conntrack 满
conntrack -S | grep insert_failed && \
  sysctl net.netfilter.nf_conntrack_max

# 组合 5: 定位 veth 软中断
/usr/share/bcc/tools/softirqs 1 | grep net_rx && \
  top -b -n 1 | grep ksoftirqd
```

---

#### 29.6.12.6 网络定位口诀

> **"横向先看 RTT，纵向再追重传；virtio 看 xdpdrop，veth 看软中断；OTLP 锁定跳
> ，eBPF 锁定层。"**

**与 29.6.5 口诀的配合**：

- **29.6.5 口诀**：用于 CPU/内存/磁盘等资源定位
- **29.6.12.6 口诀**：专门用于网络问题定位

**网络问题定位核心思路**：

- **OTLP** 告诉你"哪一跳慢"——通过 `net.peer.ip` 和 `duration` 定位慢跳
- **eBPF** 告诉你"这一跳内部在哪一层丢包/排队"——通过 tcplife、xdpdrop、conntrack
  等工具定位丢包层级

**两层数据交叉定位**：

网络问题不再靠"盲 ping"，而是：

**OTLP 告诉你"哪一跳慢"，eBPF 告诉你"这一跳内部在哪一层丢包/排队"**——

两层一交叉，根因就能从"海量包"里被秒捞出来。

**常见网络问题定位速查**：

| 问题现象       | 横向信号（OTLP）           | 纵向信号（eBPF/内核）            | 根因层级     | 解决方案                   |
| -------------- | -------------------------- | -------------------------------- | ------------ | -------------------------- |
| 延迟突增 1.8s  | `duration` 突增，RTT 120ms | `tcplife` RTT > 100ms            | L-3 容器层   | 检查 conntrack 表是否满    |
| 偶发 502/RST   | `http.status_code` 502     | `tcpretrans` 重传 3 次           | L-2 半虚拟层 | 检查 virtio 队列是否满     |
| 网络丢包       | trace 断点                 | `xdpdrop` 计数器上涨             | L-2 半虚拟层 | 检查 virtio rx_queue       |
| 跨 Pod 通信慢  | 所有 span 延迟             | `veth_latency` 软中断延迟        | L-3 容器层   | 检查 ksoftirqd CPU 使用    |
| SNAT 端口耗尽  | 部分请求失败               | `conntrack -S` insert_failed > 0 | L-3 容器层   | 增加 SNAT 端口范围或节点数 |
| SR-IOV VF 异常 | Pod 网络 NotReady          | `vfstat` VF reset count > 0      | L-0 硬件层   | 检查固件或 LLDP 配置       |

---

### 29.6.13 实战案例总结

**综合定位案例分析**：

以下案例展示了如何综合运用横向和纵向定位方法解决实际问题：

#### 案例 1：CPU Throttle + Virtio 队列满（完整链路）

**问题现象**：

- 下单接口延迟从 200ms 涨到 2s
- 偶发 5s+ 超时
- 重启后 30min 又慢

**定位过程**：

1. **横向定位（OTLP Trace）**：

   - Jaeger trace 显示 `payment-sidecar` span 1.8s
   - `order-7b9d9` span 自身 200ms 正常
   - **结论**：瓶颈在 sidecar 容器内部

2. **纵向定位（eBPF）**：

   - `cpudist` 发现 Pod 连续 100ms 被 throttle
   - `container_cpu_cfs_throttled_seconds_total` 飙高 30%
   - **结论**：容器 CPU quota 过小

3. **继续下探**：
   - `funclatency` 显示 seccomp 平均 90µs→900µs
   - `xdpdrop` 计数器上涨，virtio tx_queue 满
   - **结论**：seccomp 慢路径 + CPU throttle → virtio 队列满

**根因**：

- gVisor 缺 syscall 白名单，每次 connect 走慢路径
- 容器 quota 过小，CPU 被 throttle
- 发包突刺导致 virtio 环形队列满

**解决方案**：

- 添加 `connect` syscall 到 gVisor 白名单
- 调整 `cpu.cfs_quota_us` 从 2000 到 4000
- 优化 virtio 队列大小

---

#### 案例 2：网络 RTT 突增 + mDNS 风暴（网络定位）

**问题现象**：

- 跨 Pod 通信延迟从 2ms→20ms
- 偶发 502 错误
- 同一 Node 上所有 Pod 都受影响

**定位过程**：

1. **横向定位（OTLP Trace）**：

   - `net.peer.ip=10.244.3.17` duration 1.83s
   - **结论**：网络延迟突增

2. **纵向定位（eBPF 网络）**：

   - `tcplife` RTT 从 20ms→120ms
   - `tcpretrans` 记录 3 次 RTO 重传
   - `xdpdrop` 计数 50kpps，virtio rx_queue 满
   - **结论**：virtio 队列被打满

3. **追查来源**：
   - `tcpdump` 看到 500 Mbps UDP 5353 流量
   - `_mdns` flood 来自隔壁 DaemonSet
   - **结论**：mDNS 风暴占满 virtio 环

**解决方案**：

- 限速 DaemonSet 的 mDNS 流量
- 增加 virtio rx_queue 大小
- 添加 iptables 规则抑制 mDNS 广播

---

#### 案例 3：磁盘 IO 瓶颈 + 日志收集风暴（主机层）

**问题现象**：

- 所有 Pod 延迟都上涨
- 数据库查询超时
- 重启后恢复正常，但很快又慢

**定位过程**：

1. **横向定位（OTLP Trace）**：

   - 所有 span 延迟都上涨
   - **结论**：系统级瓶颈，不是单服务问题

2. **纵向定位（eBPF 磁盘）**：

   - `biolatency` p99 从 2ms→20ms
   - `iostat` 显示 `%util 98.3`
   - **结论**：磁盘 IO 达到上限

3. **追查来源**：
   - `fileslower` 显示 `/var/log/app.log` 写入延迟 50ms
   - 发现日志收集 DaemonSet 疯狂写
   - **结论**：日志收集导致磁盘 IO 瓶颈

**解决方案**：

- 优化日志收集策略，减少写入频率
- 使用本地 SSD 存储日志
- 增加磁盘 IOPS 配额

---

### 29.6.14 最佳实践与注意事项

#### 29.6.14.1 定位流程最佳实践

**定位顺序**：

1. **先横向，后纵向**：

   - 先用 OTLP Trace 找到慢跳
   - 再用 eBPF 钻到具体层级
   - 不要一开始就深入某一层

2. **分层排查，逐层下探**：

   - 从最外层（容器层）开始
   - 逐层下探到硬件层
   - 每层确认后再进入下一层

3. **交叉验证**：
   - OTLP 和 eBPF 数据要交叉验证
   - 多个工具的结果要相互印证
   - 避免单一工具误判

**工具选择原则**：

| 问题类型   | 首选工具               | 备选工具   | 验证工具          |
| ---------- | ---------------------- | ---------- | ----------------- |
| 延迟突增   | Jaeger trace + cpudist | tcplife    | container metrics |
| 偶发超时   | tcpretrans + xdpdrop   | tcpdrop    | dmesg             |
| 网络丢包   | xdpdrop + conntrack    | tcpdump    | iptables -S       |
| 磁盘 IO 高 | biolatency + iostat    | fileslower | df -h             |
| 内存泄漏   | memleak + metrics      | top        | kubectl top       |

---

#### 29.6.14.2 常见误区与注意事项

**常见误区**：

1. **只看日志，不看指标**：

   - ❌ 只看应用日志，忽略系统指标
   - ✅ 日志 + Metrics + Trace 综合分析

2. **只看单一层级**：

   - ❌ 只在容器层排查，忽略下层问题
   - ✅ 分层排查，逐层下探

3. **忽略时间关联**：

   - ❌ 只看当前状态，忽略时间线
   - ✅ OTLP Trace 提供时间线，eBPF 提供瞬时状态

4. **工具使用不当**：
   - ❌ 用 tcplife 查磁盘问题
   - ✅ 根据问题类型选择合适工具

**注意事项**：

1. **eBPF 工具需要 root 权限**：

   - 部分 eBPF 工具需要 root 或 CAP_BPF
   - 在生产环境使用要注意权限控制

2. **OTLP Trace 采样率**：

   - 高并发场景可能需要降低采样率
   - 确保关键路径 100% 采样

3. **工具性能影响**：

   - eBPF 工具本身有性能开销
   - 避免在生产环境长期运行

4. **数据关联性**：
   - OTLP 和 eBPF 数据时间戳要同步
   - 使用统一的时间源（NTP）

---

#### 29.6.14.3 生产环境部署建议

**监控体系部署**：

1. **OTLP 采集**：

   - OpenTelemetry Collector 部署在边缘
   - 确保关键服务 100% 采样
   - 使用批处理减少网络开销

2. **eBPF 工具部署**：

   - 使用 eBPF 守护进程（如 bcc-tools daemon）
   - 定期轮询而非持续运行
   - 配置资源限制和告警

3. **数据存储**：
   - Trace 数据存储 7-14 天
   - Metrics 数据长期存储（1 年+）
   - 使用 TSDB（如 Prometheus）存储

**告警规则设置**：

| 指标类型      | 告警阈值           | 告警级别 | 处理优先级 |
| ------------- | ------------------ | -------- | ---------- |
| span duration | p95 > 1s           | Warning  | 中         |
| CPU throttle  | 累计时间 > 10s/min | Warning  | 高         |
| 网络丢包      | xdpdrop > 1kpps    | Critical | 高         |
| 磁盘延迟      | p99 > 50ms         | Warning  | 中         |
| 内存泄漏      | 持续增长 > 10%/h   | Critical | 高         |

---

### 29.6.15 快速参考卡片

**定位口诀速查**：

> **CPU/内存定位**："横向先 trace，纵向再 bpf；quota 先看 throttle，virtio 再看
> tx_queue；沙盒慢就加 syscall，主机飙就查 io。"
>
> **网络定位**："横向先看 RTT，纵向再追重传；virtio 看 xdpdrop，veth 看软中断
> ；OTLP 锁定跳，eBPF 锁定层。"
>
> **日志定位**："先找隔离层，再看谁拦 syscall；VM 里跑 virtio，容器里看 runc，沙
> 盒里找 Sentry。"

**工具速查表**：

| 层级           | CPU/内存工具          | 网络工具            | 磁盘工具   | 日志关键词                       |
| -------------- | --------------------- | ------------------- | ---------- | -------------------------------- |
| **L-4 沙盒**   | funclatency (seccomp) | veth_latency        | N/A        | `Sentry syscall denied`          |
| **L-3 容器**   | cpudist, memleak      | tcplife, conntrack  | N/A        | `OOMKilled`, `ContainerCreating` |
| **L-2 半虚拟** | N/A                   | xdpdrop, tcpretrans | N/A        | `virtio_net tx timeout`          |
| **L-1 全虚拟** | N/A                   | N/A                 | N/A        | `VMCS corruption`                |
| **L-0 硬件**   | N/A                   | vfstat              | N/A        | `EPT violation`, `VF reset`      |
| **主机层**     | N/A                   | N/A                 | biolatency | `await 22ms, %util 98%`          |

**定位决策树**：

```text
问题现象
    ↓
延迟突增？
    ├─ 是 → 横向：Jaeger trace 找慢跳
    │       ↓
    │  纵向：cpudist (CPU) / tcplife (网络) / biolatency (磁盘)
    │
    └─ 否 → 偶发超时？
            ├─ 是 → tcpretrans + xdpdrop (网络)
            └─ 否 → 日志关键词定位层级
```

---

### 29.6.16 工具安装与配置速查

**eBPF 工具安装（BCC）**：

```bash
# Ubuntu/Debian
sudo apt-get install -y bpfcc-tools linux-headers-$(uname -r)

# CentOS/RHEL
sudo yum install -y bcc-tools kernel-headers-$(uname -r)

# 验证安装
ls /usr/share/bcc/tools/ | grep -E 'cpudist|tcplife|xdpdrop'
```

**OpenTelemetry Collector 快速部署**：

```bash
# 使用 kubectl 部署
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: otel-collector
  namespace: default
spec:
  selector:
    matchLabels:
      app: otel-collector
  template:
    metadata:
      labels:
        app: otel-collector
    spec:
      containers:
      - name: otel-collector
        image: otel/opentelemetry-collector:latest
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        env:
        - name: OTEL_EXPORTER_OTLP_ENDPOINT
          value: "http://jaeger-collector:4317"
EOF
```

**Prometheus 基础配置**：

```yaml
# prometheus-config.yaml
global:
  scrape_interval: 15s
  retention: 24h

scrape_configs:
  - job_name: "kubernetes-pods"
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

**内核配置检查**：

```bash
# 检查 eBPF 支持
cat /proc/config.gz | gunzip | grep -E 'CONFIG_BPF|CONFIG_BPF_SYSCALL|CONFIG_KPROBES'

# 检查 BTF 支持（推荐）
cat /proc/config.gz | gunzip | grep CONFIG_DEBUG_INFO_BTF

# 检查内核版本
uname -r  # 推荐 >= 4.19

# 检查 cgroup v2（容器层）
mount | grep cgroup2
```

**常用命令速查**：

```bash
# 查看容器 CPU throttle
cat /sys/fs/cgroup/cpu,cpuacct/cpu.cfs_throttled_seconds_total

# 查看 virtio 队列状态
ethtool -S eth0 | grep -E 'rx_queue|tx_queue'

# 查看 conntrack 统计
conntrack -S | grep -E 'insert_failed|drop'

# 查看 veth 对
ip link show type veth

# 查看容器 namespace
lsns -t net -p $(pgrep -f container)
```

---

### 29.6.17 相关文档

- **[16. 监控与可观测性](../16-observability/observability.md)** -
  OTLP、OpenTelemetry、Jaeger 等技术规范
- **[31. eBPF 技术堆栈](../31-ebpf-stack/ebpf-stack.md)** - eBPF 内核可编程技术
  堆栈，eBPF 工具生态和性能分析（2025-11-07）
- **[11. 故障排查](../11-troubleshooting/troubleshooting.md)** - 常见故障排查方
  法
- **[13. 缩写词汇表](../13-acronyms-glossary/acronyms-glossary.md)** -
  OTLP、eBPF 等技术缩写词定义

---

## 29.7 快速索引与常见问题

### 29.7.0 按问题类型快速索引

**快速查找指南**：

| 问题场景             | 问题类型 | 推荐章节                                                | 预期时间 |
| -------------------- | -------- | ------------------------------------------------------- | -------- |
| 看到日志关键词       | 日志分析 | [29.5.1 日志关键词快速定位](#2951-日志关键词快速定位)   | 30 秒    |
| 延迟突然升高         | 性能问题 | [29.6.3 五步定位法](#2963-五步定位法)                   | 5 分钟   |
| 网络超时/丢包        | 网络问题 | [29.6.12 网络定位专题](#29612-网络定位专题横向生命线)   | 10 分钟  |
| CPU/内存瓶颈         | 资源问题 | [29.6.13 实战案例总结](#29613-实战案例总结)             | 10 分钟  |
| 需要理解某个组件层级 | 技术选型 | [29.3 逐层展开](#293-逐层展开)                          | 2 分钟   |
| 不知道用什么工具     | 工具选择 | [29.6.9 eBPF 工具速查表](#2969-ebpf-工具速查表)         | 1 分钟   |
| 需要搭建观测系统     | 系统搭建 | [29.6.0.5 落地最小完备集](#29605-落地最小完备集mvp)     | 30 分钟  |
| 需要验证观测完备性   | 系统验证 | [29.6.0.3 完备性判据](#29603-完备性判据可量化)          | 5 分钟   |
| 遇到告警风暴         | 告警问题 | [29.6.14.3 生产环境部署建议](#296143-生产环境部署建议)  | 10 分钟  |
| 需要安装/配置工具    | 工具配置 | [29.6.16 工具安装与配置速查](#29616-工具安装与配置速查) | 10 分钟  |
| 需要学习完整方法论   | 学习路径 | [29.8.5 学习路径建议](#2985-学习路径建议)               | 视情况   |

---

### 29.7.1 常见问题 FAQ

#### Q1: 为什么需要四层隔离栈的概念？

**A**: 四层隔离栈帮助我们：

1. **快速定位问题**：看到日志关键词，立即知道问题在哪一层
2. **理解技术关系**：明确各层级之间的依赖和边界
3. **技术选型指导**：选择合适层级的组件
4. **问题定位效率**：结合横纵耦合模型，秒级精确定位

**参考章节**：[29.2 四层隔离栈总览](#292-四层隔离栈总览)

---

#### Q2: 观测系统真的必须吗？能不能先用业务系统再补观测？

**A**: **不建议**。原因：

1. **Fail-fast 失效**：没有观测，故障只能走到用户侧才发现
2. **问题复现困难**：生产环境偶发问题无法回溯
3. **成本不可控**：无法解释云账单，财务损失风险
4. **合规风险**：日志保留期不足，审计失败

**最小可行方案**：至少部署 OpenTelemetry Collector + Prometheus + Grafana（详见
[29.6.0.5 落地最小完备集](#29605-落地最小完备集mvp)）

---

#### Q3: eBPF 工具需要 root 权限，生产环境安全吗？

**A**: 可以安全使用，方法：

1. **使用 DaemonSet**：限制 eBPF 工具运行在专用节点
2. **RBAC 控制**：通过 Kubernetes RBAC 限制访问权限
3. **只读模式**：eBPF 工具只采集数据，不修改系统状态
4. **资源限制**：设置 CPU/Memory limits，避免影响业务
5. **定期轮询**：使用守护进程定期轮询，而非持续运行

**参考章节**：[29.6.14.2 常见误区与注意事项](#296142-常见误区与注意事项)

---

#### Q4: OTLP 和 eBPF 数据如何关联？

**A**: 通过统一标签关联：

1. **五元组匹配**：OTLP 的 `net.peer.ip/port` + `net.host.ip/port` = eBPF 的五元
   组
2. **时间戳同步**：使用 NTP 确保时间戳同步
3. **TraceId 关联**：通过 `trace_id` 和 `span_id` 关联 Trace 和 Log
4. **Sk Cookie**：通过 `sk_cookie` 关联内核事件和应用 Span

**参考章
节**：[29.6.12.0.2 OTLP 如何给出"横向坐标"](#2961202-otlp-如何给出横向坐标),
[29.6.12.0.3 eBPF 如何给出"纵向坐标"](#2961203-ebpf-如何给出纵向坐标)

---

#### Q5: 网络为什么不是第 5 层？

**A**: 网络是**横向生命线**，不是纵向层级：

1. **贯穿所有层**：每一层都有独立的网络切片（virtio-net、veth、CNI）
2. **功能不同**：网络负责跨层通信，隔离栈负责资源边界
3. **定位方法**：网络问题需要先选切片，再按"队列 → 调度 → 协议"下钻

**参考章
节**：[29.6.12.0 为什么网络必须作为独立维度](#296120-为什么网络必须作为独立维度)

---

#### Q6: 如何判断观测系统是否完备？

**A**: 检查 6 个完备性判据：

1. ✅ Three Pillars 齐全（Metric/Trace/Log 同时在线）
2. ✅ Four Golden Signals 覆盖（Latency/Traffic/Errors/Saturation）
3. ✅ 纵向可下钻（TraceId → 应用 → 容器 → 内核 → 硬件）
4. ✅ 采样可回溯（全采样 24h，1‰ 采样 30 天）
5. ✅ 告警收敛率 ≥ 90%
6. ✅ 审计可出证（日志不可改、带签名、时间戳可溯源）

**验证方法**：详见 [29.6.0.3 完备性判据](#29603-完备性判据可量化) 中的检查清单

---

#### Q7: 遇到偶发性能问题，如何定位？

**A**: 使用横纵耦合定位模型：

1. **横向定位**：用 Jaeger Trace 找到 duration 突增的 span
2. **纵向定位**：用 eBPF 工具（cpudist、tcplife、xdpdrop）钻到具体层级
3. **交叉验证**：多个工具结果相互印证，时间戳同步

**参考章节**：[29.6.3 五步定位法](#2963-五步定位法),
[29.6.13 实战案例总结](#29613-实战案例总结)

---

#### Q8: 老内核（4.14 以下）能用 eBPF 吗？

**A**: 可以，但需要调整：

1. **使用 kprobe 回退**：回退到 `tcp_set_state`/`tcp_rcv_established`
2. **宿主机部署**：把 eBPF 程序挂到宿主机，对 Guest 无侵入
3. **功能不变**：只是写法多两行，功能不变

**参考章节**：[29.6.12.0.4 常见反驳与充分回应](#2961204-常见反驳与充分回应)

---

#### Q9: 如何避免告警风暴？

**A**: 告警收敛策略：

1. **根因聚合**：同一根因只产生 1 条通知
2. **时间窗口**：相同告警在时间窗口内只通知一次
3. **告警分组**：按服务、集群、严重程度分组
4. **收敛率目标**：收敛率 ≥ 90%

**参考章节**：[29.6.14.3 生产环境部署建议](#296143-生产环境部署建议)

---

#### Q10: 文档太长，从哪里开始阅读？

**A**: 根据角色选择路径：

- **新手**：[29.2 四层隔离栈总览](#292-四层隔离栈总览) →
  [29.3 逐层展开](#293-逐层展开) → [29.5 快速诊断口诀](#295-快速诊断口诀)
- **运维工程师**：[29.6 问题定位模型](#296-问题定位模型横向请求链--纵向隔离栈) →
  [29.6.13 实战案例总结](#29613-实战案例总结) →
  [29.6.14 最佳实践](#29614-最佳实践与注意事项)
- **架构
  师**：[29.6.0 观测系统作为第四大基础设施](#2960-观测系统作为第四大基础设施) →
  [29.6.12.0 为什么网络必须作为独立维度](#296120-为什么网络必须作为独立维度) →
  [29.8 文档总结](#298-文档总结与核心观点)

**完整学习路径**：详见 [29.8.5 学习路径建议](#2985-学习路径建议)

---

## 29.8 文档总结与核心观点

### 29.8.1 核心观点总结

**四层隔离栈的核心价值**：

1. **清晰的层级划分**：

   - L-0 硬件辅助层：所有虚拟化的底层基础
   - L-1 全虚拟化层：完整假硬件，Guest OS 无感知
   - L-2 半虚拟化层：Guest 内核配合，性能近裸机
   - L-3 容器化层：进程级隔离，共享内核
   - L-4 沙盒化层：syscall 过滤，二次隔离

2. **网络作为横向生命线**：

   - 不是"第 5 层"，而是贯穿所有层的独立维度
   - 每一层都有独立的"网络切片"
   - 问题定位 = 先选切片，再按"队列 → 调度 → 协议"逐层下钻

3. **横纵耦合的问题定位模型**：
   - **X 轴（请求链）**：OTLP 统一语义，定位"哪一跳慢"
   - **Y 轴（内核栈）**：eBPF 零开销采样，定位"哪一层卡"
   - 两轴交叉，秒级精确问题定位

---

### 29.8.2 关键方法论

**定位方法论三步走**：

1. **横向先找慢跳**（OTLP Trace）：

   - 使用 Jaeger trace 找到 duration 突增的 span
   - 过滤 `duration > 1s && net.peer.ip = xxx`

2. **纵向再钻层级**（eBPF/内核）：

   - 从容器层开始，逐层下探
   - 使用对应层级的工具（cpudist、tcplife、xdpdrop 等）

3. **交叉验证定位**（数据关联）：
   - OTLP 和 eBPF 数据时间戳同步
   - 多个工具结果相互印证

**问题定位口诀**：

> **CPU/内存定位**："横向先 trace，纵向再 bpf；quota 先看 throttle，virtio 再看
> tx_queue；沙盒慢就加 syscall，主机飙就查 io。"
>
> **网络定位**："横向先看 RTT，纵向再追重传；virtio 看 xdpdrop，veth 看软中断
> ；OTLP 锁定跳，eBPF 锁定层。"
>
> **日志定位**："先找隔离层，再看谁拦 syscall；VM 里跑 virtio，容器里看 runc，沙
> 盒里找 Sentry。"

---

### 29.8.3 技术术语快速索引

**硬件虚拟化术语**：

| 术语  | 层级 | 含义                       | 相关章节                                       |
| ----- | ---- | -------------------------- | ---------------------------------------------- |
| VT-x  | L-0  | Intel 硬件虚拟化指令集     | [29.3.1](#2931-l-0-硬件辅助层cpu-虚拟化指令集) |
| AMD-V | L-0  | AMD 硬件虚拟化指令集       | [29.3.1](#2931-l-0-硬件辅助层cpu-虚拟化指令集) |
| EPT   | L-0  | Intel 扩展页表，内存虚拟化 | [29.3.1](#2931-l-0-硬件辅助层cpu-虚拟化指令集) |
| SEV   | L-0  | AMD 安全加密虚拟化         | [29.3.1](#2931-l-0-硬件辅助层cpu-虚拟化指令集) |

**虚拟化术语**：

| 术语    | 层级 | 含义                 | 相关章节                                 |
| ------- | ---- | -------------------- | ---------------------------------------- |
| KVM     | L-1  | Linux 内核虚拟化模块 | [29.3.2](#2932-l-1-全虚拟化层完整假硬件) |
| QEMU    | L-1  | 用户态设备模拟器     | [29.3.2](#2932-l-1-全虚拟化层完整假硬件) |
| VMCS    | L-1  | VM 控制结构          | [29.3.2](#2932-l-1-全虚拟化层完整假硬件) |
| vMotion | L-1  | VMware 热迁移技术    | [29.3.2](#2932-l-1-全虚拟化层完整假硬件) |

**半虚拟化术语**：

| 术语          | 层级 | 含义                | 相关章节                                     |
| ------------- | ---- | ------------------- | -------------------------------------------- |
| virtio        | L-2  | 内核半虚拟化标准    | [29.3.3](#2933-l-2-半虚拟化层guest-内核配合) |
| grant table   | L-2  | Xen PV 内存共享机制 | [29.3.3](#2933-l-2-半虚拟化层guest-内核配合) |
| event channel | L-2  | Xen PV 中断通知机制 | [29.3.3](#2933-l-2-半虚拟化层guest-内核配合) |
| vhost         | L-2  | virtio 后端加速     | [29.3.3](#2933-l-2-半虚拟化层guest-内核配合) |

**容器化术语**：

| 术语       | 层级 | 含义               | 相关章节                               |
| ---------- | ---- | ------------------ | -------------------------------------- |
| runc       | L-3  | OCI 标准容器运行时 | [29.3.4](#2934-l-3-容器化层进程级隔离) |
| containerd | L-3  | 容器运行时守护进程 | [29.3.4](#2934-l-3-容器化层进程级隔离) |
| namespace  | L-3  | 内核隔离机制       | [29.3.4](#2934-l-3-容器化层进程级隔离) |
| cgroup     | L-3  | 内核资源限制机制   | [29.3.4](#2934-l-3-容器化层进程级隔离) |
| seccomp    | L-3  | 系统调用过滤       | [29.3.4](#2934-l-3-容器化层进程级隔离) |

**沙盒化术语**：

| 术语        | 层级 | 含义                     | 相关章节                                           |
| ----------- | ---- | ------------------------ | -------------------------------------------------- |
| gVisor      | L-4  | Google 用户态内核        | [29.3.5](#2935-l-4-沙盒化层syscall-过滤--二次内核) |
| Sentry      | L-4  | gVisor 用户态内核组件    | [29.3.5](#2935-l-4-沙盒化层syscall-过滤--二次内核) |
| Firecracker | L-4  | AWS 轻量级 VMM           | [29.3.5](#2935-l-4-沙盒化层syscall-过滤--二次内核) |
| MicroVM     | L-4  | Firecracker 轻量级虚拟机 | [29.3.5](#2935-l-4-沙盒化层syscall-过滤--二次内核) |

**可观测性术语**：

| 术语    | 类型      | 含义                 | 相关章节                                                                       |
| ------- | --------- | -------------------- | ------------------------------------------------------------------------------ |
| OTLP    | 协议      | OpenTelemetry 协议   | [29.6.1](#2961-定位模型概述), [29.6.12.0.2](#2961202-otlp-如何给出横向坐标)    |
| eBPF    | 工具      | 内核可编程接口       | [29.6.9](#2969-ebpf-工具速查表), [29.6.12.0.3](#2961203-ebpf-如何给出纵向坐标) |
| tcplife | eBPF 工具 | TCP 连接生命周期分析 | [29.6.12.3](#296123-纵向ebpf-网络显微镜)                                       |
| xdpdrop | eBPF 工具 | XDP 丢包统计         | [29.6.12.3](#296123-纵向ebpf-网络显微镜)                                       |
| cpudist | eBPF 工具 | CPU 时间分布分析     | [29.6.9](#2969-ebpf-工具速查表)                                                |

**网络术语**：

| 术语       | 层级 | 含义                   | 相关章节                                    |
| ---------- | ---- | ---------------------- | ------------------------------------------- |
| veth       | L-3  | 虚拟以太网对，容器网络 | [29.6.12.1](#296121-网络在三栈里的切片视图) |
| virtio-net | L-2  | virtio 网络设备        | [29.6.12.1](#296121-网络在三栈里的切片视图) |
| CNI        | L-3  | 容器网络接口           | [29.6.12.1](#296121-网络在三栈里的切片视图) |
| conntrack  | L-3  | 连接跟踪表             | [29.6.12.3](#296123-纵向ebpf-网络显微镜)    |

---

### 29.8.4 文档结构导航图

```text
四层隔离栈文档结构
───────────────────

┌─────────────────────────────────────────┐
│ 29.1-29.4: 基础理论                      │
│ ├─ 文档定位                              │
│ ├─ 四层隔离栈总览                        │
│ ├─ 逐层展开（L-0 到 L-4）               │
│ └─ 技术架构图                            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 29.5: 快速诊断                           │
│ ├─ 日志关键词快速定位                    │
│ └─ 故障排查流程                          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 29.6: 问题定位模型                       │
│ ├─ 定位模型概述                          │
│ ├─ 五步定位法                            │
│ ├─ eBPF 工具速查表                       │
│ ├─ 网络定位专题（横向生命线）            │
│ │  ├─ 为什么网络必须独立                 │
│ │  ├─ OTLP 横向坐标                      │
│ │  ├─ eBPF 纵向坐标                      │
│ │  └─ 双轴定位算法                       │
│ ├─ 实战案例总结（3 个案例）              │
│ ├─ 最佳实践与注意事项                    │
│ └─ 快速参考卡片                          │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 29.7: 文档总结                           │
│ ├─ 核心观点总结                          │
│ ├─ 关键方法论                            │
│ ├─ 技术术语快速索引                      │
│ └─ 文档结构导航图（本图）                │
└─────────────────────────────────────────┘
```

**快速查找指南**：

- **想了解层级概念** → 阅读 [29.2 四层隔离栈总览](#292-四层隔离栈总览)
- **想查看具体组件** → 阅读 [29.3 逐层展开](#293-逐层展开)
- **遇到日志关键词** → 查看
  [29.5.1 日志关键词快速定位](#2951-日志关键词快速定位)
- **需要定位问题** → 查看
  [29.6 问题定位模型](#296-问题定位模型横向请求链--纵向隔离栈)
- **网络问题定位** → 查看 [29.6.12 网络定位专题](#29612-网络定位专题横向生命线)
- **查看实战案例** → 查看 [29.6.13 实战案例总结](#29613-实战案例总结)
- **查找技术术语** → 查看 [29.8.3 技术术语快速索引](#2983-技术术语快速索引)

---

### 29.8.5 学习路径建议

**新手学习路径**：

1. **[29.2 四层隔离栈总览](#292-四层隔离栈总览)** - 了解整体结构
2. **[29.3 逐层展开](#293-逐层展开)** - 深入理解各层级
3. **[29.5 快速诊断口诀](#295-快速诊断口诀)** - 掌握快速定位方法
4. **[29.6.15 快速参考卡片](#29615-快速参考卡片)** - 日常查找参考

**进阶学习路径**：

1. **[29.6 问题定位模型](#296-问题定位模型横向请求链--纵向隔离栈)** - 掌握横纵耦
   合定位
2. **[29.6.12 网络定位专题](#29612-网络定位专题横向生命线)** - 深入理解网络定位
3. **[29.6.13 实战案例总结](#29613-实战案例总结)** - 学习实际应用
4. **[29.6.14 最佳实践与注意事项](#29614-最佳实践与注意事项)** - 生产环境部署

**专家级学习路径**：

1. **[29.6.12.0 为什么网络必须作为独立维度](#296120-为什么网络必须作为独立维度)** -
   理论深度理解
2. **[29.6.12.0.2 OTLP 如何给出"横向坐标"](#2961202-otlp-如何给出横向坐标)** -
   OTLP 语义约定
3. **[29.6.12.0.3 eBPF 如何给出"纵向坐标"](#2961203-ebpf-如何给出纵向坐标)** -
   eBPF 探针附着点
4. **[29.6.14.3 生产环境部署建议](#296143-生产环境部署建议)** - 生产环境最佳实践

---

### 29.8.6 文档价值总结

**本文档的核心价值**：

1. **系统性**：

   - 从硬件层到沙盒层的完整技术栈梳理
   - 网络作为横向生命线的独特视角
   - 横纵耦合的问题定位模型

2. **实用性**：

   - 日志关键词快速定位表
   - eBPF 工具速查表
   - 3 个完整实战案例
   - 一键脚本可直接使用

3. **可操作性**：

   - 五步定位法详细流程
   - 双轴定位算法完整实现
   - 生产落地 Checklist
   - 告警规则设置

4. **可证伪性**：
   - OTLP + eBPF 双轴数据交叉验证
   - 时间戳同步，数据关联
   - 问题可复现、可修复、可验证

**适用人群**：

- **运维工程师**：故障排查、性能优化
- **架构师**：技术选型、架构设计
- **开发者**：理解底层机制、性能调优
- **SRE**：可观测体系建设、告警规则设计

---

## 29.9 文档使用指南

### 29.9.0 如何高效使用本文档

**使用策略**：

根据您的角色和需求，选择不同的使用策略：

| 使用场景         | 推荐策略                       | 关键章节               | 预期时间  |
| ---------------- | ------------------------------ | ---------------------- | --------- |
| **首次阅读**     | 从概览开始，按学习路径系统学习 | 29.1.0 → 29.8.5        | 2-3 小时  |
| **紧急故障排查** | 直接跳到快速索引，找到对应章节 | 29.7.0 → 对应工具/方法 | 5-30 分钟 |
| **技术选型决策** | 查看层级解析，理解技术关系     | 29.2 → 29.3            | 30 分钟   |
| **搭建观测系统** | 先看理论基础，再看落地实践     | 29.6.0 → 29.6.16       | 1-2 小时  |
| **理解定位模型** | 先看概述和图示，再看实战案例   | 29.6.1 → 29.6.13       | 1 小时    |
| **网络问题定位** | 直接看网络专题，按五步法操作   | 29.6.12                | 30 分钟   |

**阅读技巧**：

1. **快速查找**：

   - 遇到问题 → 查看 [29.7.0 按问题类型快速索引](#2970-按问题类型快速索引)
   - 查看术语 → 查看 [29.8.3 技术术语快速索引](#2983-技术术语快速索引)
   - 选择工具 → 查看 [29.6.9 eBPF 工具速查表](#2969-ebpf-工具速查表)

2. **深入学习**：

   - 新手：按 [29.8.5 学习路径建议](#2985-学习路径建议) 中的"新手学习路径"
   - 进阶：按"进阶学习路径"
   - 专家：按"专家级学习路径"

3. **实战应用**：
   - 遇到实际问题 → 查看 [29.6.13 实战案例总结](#29613-实战案例总结)
   - 需要脚本 → 查看 [29.6.6 实战一键脚本](#2966-实战一键脚本示例) 和
     [29.6.12.5 网络定位一键脚本](#296125-网络定位一键脚本)
   - 生产部署 → 查看 [29.6.14.3 生产环境部署建议](#296143-生产环境部署建议)

**常见问题快速定位**：

- 不知道从哪开始？ →
  [Q10: 文档太长，从哪里开始阅读？](#q10-文档太长从哪里开始阅读)
- 观测系统必须吗？ →
  [Q2: 观测系统真的必须吗？](#q2-观测系统真的必须吗能不能先用业务系统再补观测)
- eBPF 安全吗？ →
  [Q3: eBPF 工具需要 root 权限，生产环境安全吗？](#q3-ebpf-工具需要-root-权限生产环境安全吗)
- 数据如何关联？ →
  [Q4: OTLP 和 eBPF 数据如何关联？](#q4-otlp-和-ebpf-数据如何关联)
- 网络为什么不是第 5 层？ →
  [Q5: 网络为什么不是第 5 层？](#q5-网络为什么不是第-5-层)

---

## 29.10 参考

> 📂 **文档目录结构**：本文档的目录结构说明请参考 [README.md](README.md)。各层次
> 独立文档位于 [layers/](layers/) 目录，问题定位模型独立文档位于
> [troubleshooting/](troubleshooting/) 目录。

### 29.10.1 相关文档

**文档关联性**：

- **[文档关联性完善总结报告](../DOCUMENTATION-ISOLATION-STACK-CROSS-REFERENCES.md)** -
  所有技术文档与隔离栈文档的关联关系总结
  - 27 个技术文档的关联性完善记录
  - 关联点统计和分析
  - 文档关联性体系价值说明

**2025 年最新更新**：

- **[27. 2025 趋势 - 2025-11-06 最新更新](../27-2025-trends/2025-trends.md#2714-2025-年-11-月-6-日最新更新)** -
  技术版本更新、生产环境最佳实践、已知问题与解决方案、性能基准测试、安全更新
  - 包含 WasmEdge、K3s、containerd、OPA、Gatekeeper 等最新版本信息
  - 边缘节点性能对比数据（runc vs WasmEdge vs gVisor）
  - 已知问题和解决方案（K3s WasmEdge 驱动超时、OPA-Wasm 内存泄漏、eBPF 探针兼容
    性）

**系统分析相关**：

- **[系统分析视角](../../../systems_view.md)** ⭐ - 从系统分析看虚拟化容器化沙盒
  化 Wasm，多维度矩阵对比和形式化论证
- **[系统视角文档](../../../system_view.md)** ⭐ - 从系统的视角看虚拟化容器化沙
  盒化（7 层 4 域模型）

**理论基础**：

- **[12. 虚拟化/半虚拟化/容器化/沙盒化严格定义](../../COGNITIVE/05-decision-analysis/decision-models/06-technical-concepts/12-virtualization-paravirtualization-containerization-sandboxing-strict-definition.md)** -
  技术范式的严格定义，隔离栈的理论基础
- **[02. 隔离模型](../../COGNITIVE/05-decision-analysis/decision-models/01-theory-models/02-isolation-models.md)** -
  隔离层次理论模型，四层隔离栈的理论支撑

**可观测性相关**：

- **[16. 监控与可观测性](../16-observability/observability.md)** -
  OTLP、OpenTelemetry、Jaeger 等技术规范，观测系统的技术实现
- **[32. eBPF/OTLP 扩展技术分析](../32-ebpf-otlp-analysis/ebpf-otlp-analysis.md)**
  ⭐ - eBPF/OTLP 扩展技术分析文档
  - 横纵耦合问题定位模型（OTLP 横向 + eBPF 纵向）
  - 技术规范对齐、性能分析、实践指南
  - 智能系统能力架构（自我感知、自动伸缩、自我治愈）
  - 故障排查、最佳实践（2025-11-07）
- **[29.6.0 观测系统作为第四大基础设施](#2960-观测系统作为第四大基础设施)** - 为
  什么观测系统必须，SLA 要求，完备性判据

**故障排查相关**：

- **[11. 故障排查](../11-troubleshooting/troubleshooting.md)** - 常见故障排查方
  法，结合本文档的问题定位模型使用
- **[29.6 问题定位模型](#296-问题定位模型横向请求链--纵向隔离栈)** - 横纵耦合的
  问题定位方法，OTLP + eBPF 联合定位
- **[29.5 快速诊断口诀](#295-快速诊断口诀)** - 日志关键词快速定位，快速诊断方法

**网络相关**：

- **[12. 网络技术规格](../12-network-stack/network-stack.md)** -
  CNI、Service、Ingress 等技术规格，网络栈的完整实现
- **[虚拟化与容器化网络对比分析](../12-network-stack/virtualization-comparison.md)** -
  网络范式转换、架构对比、性能分析（2025-11-07）
- **[31. eBPF 技术堆栈](../31-ebpf-stack/ebpf-stack.md)** - eBPF 内核可编程技术
  堆栈，网络加速、可观测性应用（2025-11-07）
- **[29.6.12 网络定位专题](#29612-网络定位专题横向生命线)** - 网络作为横向生命线
  的定位方法

**存储相关**：

- **[15. 存储技术规格](../15-storage-stack/storage-stack.md)** - CSI、PV/PVC 等
  技术规格，存储栈的完整实现
- **[虚拟化与容器化存储对比分析](../15-storage-stack/virtualization-comparison.md)** -
  存储范式转换、架构对比、性能分析（2025-11-07）

**运行时相关**：

- **[04. 编排运行时](../04-orchestration-runtime/orchestration-runtime.md)** -
  CRI 和 RuntimeClass，容器运行时的技术规格
- **[03. WasmEdge](../03-wasm-edge/wasmedge.md)** - WebAssembly 运行时，沙盒化层
  的具体实现

**各层次独立文档**（便于检索和对比）：

- **[L-0 硬件辅助层](layers/L-0-hardware-assist.md)** - VT-x、AMD-V、SEV、TPM 详
  细文档
- **[L-1 全虚拟化层](layers/L-1-full-virtualization.md)** -
  KVM、ESXi、Hyper-V、Xen HVM 详细文档
- **[L-2 半虚拟化层](layers/L-2-paravirtualization.md)** - Xen
  PV、virtio、Hyper-V Enlightenment 详细文档
- **[L-3 容器化层](layers/L-3-containerization.md)** -
  runc、containerd、Docker、Podman 详细文档
- **[L-4 沙盒化层](layers/L-4-sandboxing.md)** -
  gVisor、Firecracker、WASM、Windows Sandbox 详细文档（包括 WebAssembly）
- **[隔离层次总结合并对比](layers/isolation-comparison.md)** - 五层隔离栈总结合
  并对比文档，包含快速对比矩阵、技术选型决策树、应用场景匹配、混合部署策略、快速
  导航指南

**架构相关**：

- **[28. 架构框架](../28-architecture-framework/architecture-framework.md)** -
  多维度架构体系与技术规范，技术架构的理论基础
- **[13. 缩写词汇表](../13-acronyms-glossary/acronyms-glossary.md)** - 相关技术
  缩写词定义，OTLP、eBPF、virtio 等术语解释

### 29.10.2 外部资源

- **Intel VT-x 文档**：Intel 硬件虚拟化技术规范
- **KVM 内核文档**：Linux 内核虚拟化模块
- **OCI Runtime Spec**：容器运行时标准规范
- **gVisor 官方文档**：Google 的用户态内核项目
- **Firecracker 官方文档**：AWS 的轻量级 VMM

### 29.10.3 技术标准

- **OCI（Open Container Initiative）**：容器标准化组织
- **CRI（Container Runtime Interface）**：Kubernetes 容器运行时接口
- **WASI（WebAssembly System Interface）**：WebAssembly 系统接口标准

---

## 29.11 文档变更历史

- **2025-11-07**：

  - 全面梳理隔离栈文档体系
  - 修复 README.md 章节编号冲突（两个"## 4"章节）
  - 统一所有文档日期为 2025-11-07
  - 完善交叉引用体系：
    - README.md：添加 eBPF/OTLP 扩展技术分析文档引用，按类别组织技术文档
    - troubleshooting/README.md：添加相关文档章节，包含 eBPF/OTLP 扩展技术分析文
      档引用
    - layers/ 目录：统一所有层次文档日期，完善 isolation-comparison.md 的交叉引
      用
  - 优化文档结构：按功能分类组织相关文档（可观测性相关、故障排查相关、理论基础等
    ）

- **2025-11-06**：

  - 创建各隔离层次独立文档（`layers/` 目录）
    - 创建 L-0 硬件辅助层独立文档（343 行）：VT-x、AMD-V、SEV、TPM 详细文档，包
      含 2 个实际部署案例和最佳实践
    - 创建 L-1 全虚拟化层独立文档（422 行）：KVM、ESXi、Hyper-V、Xen HVM 详细文
      档，包含 2 个实际部署案例和最佳实践
    - 创建 L-2 半虚拟化层独立文档（421 行）：Xen PV、virtio、Hyper-V
      Enlightenment 详细文档，包含 2 个实际部署案例和最佳实践
    - 创建 L-3 容器化层独立文档（536 行）：runc、containerd、Docker、Podman 详细
      文档，包含 3 个实际部署案例和最佳实践
    - 创建 L-4 沙盒化层独立文档（679 行）：gVisor、Firecracker、WASM、Windows
      Sandbox 详细文档（包括 WebAssembly 详解），包含 3 个实际部署案例和最佳实践
    - 创建隔离层次总结合并对比文档（353 行）：包含快速对比矩阵、技术选型决策树
      （Mermaid 图）、应用场景匹配、混合部署策略、快速导航指南
    - 每个独立文档包含：层级定位、核心概念、技术实现、性能特点、安全特点、应用场
      景、故障排查、实际部署案例、最佳实践、参考文档
    - 完善的文档间交叉引用和导航链接
    - 更新主文档参考部分，添加对各层次独立文档的引用

- **2025-11-06**：

  - 全面梳理文档结构和关联性
  - 更新主 README、技术参考 README、认知文档，添加隔离栈文档的完整引用
  - 完善网络栈文档、可观测性文档与隔离栈文档的交叉引用
  - 更新认知层面的隔离模型文档，添加与技术文档的完整关联
  - 添加文档使用指南章节（29.9）：使用策略、阅读技巧、常见问题快速定位，提升文档
    可用性
  - 添加文档概览章节（29.1.0）：文档结构一览表、快速入门路径、核心价值主张
  - 优化横纵耦合定位模型图示：添加清晰的交叉定位图示
  - 增强定位流程可视化：添加详细的横纵耦合定位流程图
  - 添加工具安装与配置速查章节（29.6.16）：eBPF 工具、OpenTelemetry
    Collector、Prometheus 安装配置，内核检查，常用命令速查
  - 添加快速索引与常见问题章节（29.7）：按问题类型快速索引表和 10 个常见问题 FAQ
  - 完善相关文档交叉引用，按类别组织（理论基础、可观测性、故障排查、网络、运行时
    、架构）
  - 在定位模型概述中添加前置条件提示
  - 扩展适用场景说明，增加内部链接

- **2025-11-06**：

  - 添加观测系统作为第四大基础设施章节（29.6.0）
  - 包含 6 个子章节：为什么必须、SLA 要求、完备性判据、反例、MVP 落地、结论

- **2025-11-06**：

  - 完善网络定位专题（29.6.12）
  - 添加网络必须作为独立维度的理论论证
  - 添加双轴定位算法和常见反驳与回应

- **2025-11-01**：

  - 添加实战案例总结（29.6.13）：3 个完整案例
  - 添加最佳实践与注意事项（29.6.14）
  - 添加快速参考卡片（29.6.15）
  - 添加文档总结与核心观点（29.7）

- **2025-11-01**：
  - 创建文档，包含四层隔离栈详细解析
  - 包含 L-0 到 L-4 逐层展开
  - 包含日志关键词快速定位表
  - 包含问题定位模型和 eBPF 工具速查表

---

**最后更新**：2025-11-07 **维护者**：项目团队
