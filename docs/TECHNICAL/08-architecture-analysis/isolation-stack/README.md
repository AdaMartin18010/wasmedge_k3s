# 29. 隔离栈文档目录

## 1. 文档概述

本目录包含四层隔离栈的技术文档，详细解析虚拟化 → 半虚拟化 → 容器化 → 沙盒化的技
术栈结构。

## 2. 文档列表

| 文档                                     | 描述                                                                 |
| ---------------------------------------- | -------------------------------------------------------------------- |
| [isolation-stack.md](isolation-stack.md) | 四层隔离栈完整技术文档，包含各层级概念、机制、组件、黑话和一句话解释 |
| [layers/](layers/)                       | 各隔离层次独立文档目录，便于检索和对比                               |
| [troubleshooting/](troubleshooting/)     | 问题定位模型独立文档目录                                             |

### 2.1 各层次独立文档

| 文档                                                   | 描述                                                                    |
| ------------------------------------------------------ | ----------------------------------------------------------------------- |
| [L-0 硬件辅助层](layers/L-0-hardware-assist.md)        | VT-x、AMD-V、SEV、TPM 详细文档                                          |
| [L-1 全虚拟化层](layers/L-1-full-virtualization.md)    | KVM、ESXi、Hyper-V、Xen HVM 详细文档                                    |
| [L-2 半虚拟化层](layers/L-2-paravirtualization.md)     | Xen PV、virtio、Hyper-V Enlightenment 详细文档                          |
| [L-3 容器化层](layers/L-3-containerization.md)         | runc、containerd、Docker、Podman 详细文档                               |
| [L-4 沙盒化层](layers/L-4-sandboxing.md)               | gVisor、Firecracker、WASM、Windows Sandbox 详细文档（包括 WebAssembly） |
| [隔离层次总结合并对比](layers/isolation-comparison.md) | 五层隔离栈总结合并对比文档                                              |

## 3. 文档结构

### 3.1 主文档结构

主文档 `isolation-stack.md` 包含以下主要章节：

- **29.1 文档定位** - 文档概述和定位
- **29.2 四层隔离栈总览** - 总体架构概览
- **29.3 逐层展开** - 各层级详细解析（L-0 到 L-4）
- **29.4 技术架构图** - 架构图可视化
- **29.5 快速诊断口诀** - 日志关键词快速定位和故障排查流程
- **29.6 问题定位模型** - 横向请求链 + 纵向隔离栈定位方法（重要章节，包含大量内
  容）
  - 29.6.0 观测系统作为第四大基础设施
  - 29.6.1-29.6.10 定位模型详细内容
  - 29.6.12 网络定位专题
  - 29.6.13 实战案例总结
- **29.7 快速索引与常见问题** - 按问题类型快速索引和 FAQ
- **29.8 文档总结与核心观点** - 核心观点总结和方法论
- **29.9 文档使用指南** - 如何使用本文档
- **29.10 参考** - 相关文档和外部资源

### 3.2 分层文档（layers/ 目录）

各隔离层次的独立文档：

- **[L-0 硬件辅助层](layers/L-0-hardware-assist.md)** - VT-x、AMD-V、SEV、TPM
- **[L-1 全虚拟化层](layers/L-1-full-virtualization.md)** -
  KVM、ESXi、Hyper-V、Xen HVM
- **[L-2 半虚拟化层](layers/L-2-paravirtualization.md)** - Xen
  PV、virtio、Hyper-V Enlightenment
- **[L-3 容器化层](layers/L-3-containerization.md)** -
  runc、containerd、Docker、Podman
- **[L-4 沙盒化层](layers/L-4-sandboxing.md)** -
  gVisor、Firecracker、WASM、Windows Sandbox（包括 WebAssembly）
- **[隔离层次总结合并对比](layers/isolation-comparison.md)** - 五层隔离栈总结合
  并对比文档

### 3.3 问题定位文档（troubleshooting/ 目录）

问题定位模型相关文档：

- **[问题定位模型概述](troubleshooting/README.md)** - 横向请求链 + 纵向隔离栈定
  位方法
  - 观测系统作为第四大基础设施
  - 网络定位专题
  - 实战案例总结
  - 最佳实践与注意事项

## 4. 快速导航

### 4.1 按层次导航

- **[L-0 硬件辅助层](layers/L-0-hardware-assist.md)** - VT-x、AMD-V、SEV、TPM
- **[L-1 全虚拟化层](layers/L-1-full-virtualization.md)** -
  KVM、ESXi、Hyper-V、Xen HVM
- **[L-2 半虚拟化层](layers/L-2-paravirtualization.md)** - Xen
  PV、virtio、Hyper-V Enlightenment
- **[L-3 容器化层](layers/L-3-containerization.md)** -
  runc、containerd、Docker、Podman
- **[L-4 沙盒化层](layers/L-4-sandboxing.md)** -
  gVisor、Firecracker、WASM、Windows Sandbox（包括 WebAssembly）

### 4.2 总结合并对比

- **[隔离层次总结合并对比](layers/isolation-comparison.md)** - 五层隔离栈总结合
  并对比文档
  - 快速对比矩阵
  - 技术选型决策树
  - 应用场景匹配
  - 混合部署策略

### 4.3 完整文档导航

- **[L-0 硬件辅助层](isolation-stack.md#2931-l-0-硬件辅助层cpu-虚拟化指令集)** -
  VT-x、AMD-V、SEV、TPM
- **[L-1 全虚拟化层](isolation-stack.md#2932-l-1-全虚拟化层完整假硬件)** -
  KVM、ESXi、Hyper-V、Xen HVM
- **[L-2 半虚拟化层](isolation-stack.md#2933-l-2-半虚拟化层guest-内核配合)** -
  Xen PV、virtio、Hyper-V Enlightenment
- **[L-3 容器化层](isolation-stack.md#2934-l-3-容器化层进程级隔离)** -
  runc、containerd、Docker、Podman
- **[L-4 沙盒化层](isolation-stack.md#2935-l-4-沙盒化层syscall-过滤--二次内核)** -
  gVisor、Firecracker、WASM、Windows Sandbox
- **[问题定位模型](isolation-stack.md#296-问题定位模型横向请求链--纵向隔离栈)** -
  横向请求链 + 纵向隔离栈定位方法，OTLP + eBPF 联合定位
  - **[观测系统作为第四大基础设施](isolation-stack.md#2960-观测系统作为第四大基础设施)** -
    为什么观测系统必须而不是最好，SLA 要求，完备性判据，MVP 落地
- **[网络定位专题](isolation-stack.md#29612-网络定位专题横向生命线)** - 网络作为
  横向生命线的定位方法，OTLP + eBPF 网络工具组合
  - **[为什么网络必须作为独立维度](isolation-stack.md#296120-为什么网络必须作为独立维度)** -
    横纵耦合定位模型、双轴定位算法、常见反驳与回应
- **[实战案例总结](isolation-stack.md#29613-实战案例总结)** - 3 个完整实战案例
  ：CPU Throttle、网络 RTT 突增、磁盘 IO 瓶颈
- **[最佳实践与注意事项](isolation-stack.md#29614-最佳实践与注意事项)** - 定位流
  程最佳实践、常见误区、生产环境部署建议
- **[快速参考卡片](isolation-stack.md#29615-快速参考卡片)** - 定位口诀、工具速查
  表、定位决策树
- **[工具安装与配置速查](isolation-stack.md#29616-工具安装与配置速查)** - eBPF
  工具、OpenTelemetry、Prometheus 安装配置
- **[快速索引与常见问题](isolation-stack.md#297-快速索引与常见问题)** - 按问题类
  型快速索引表、10 个常见问题 FAQ
- **[文档总结与核心观点](isolation-stack.md#298-文档总结与核心观点)** - 核心观点
  总结、关键方法论、技术术语索引、学习路径建议
- **[文档使用指南](isolation-stack.md#299-文档使用指南)** - 使用策略、阅读技巧、
  常见问题快速定位

## 5. 使用场景

- **技术选型**：快速定位组件所属层级
- **故障排查**：根据日志关键词定位问题层级，结合 OTLP + eBPF 进行横向和纵向定位
- **面试/技术交流**：快速理解隔离栈结构
- **问题定位**：使用"横向请求链 + 纵向隔离栈"模型进行系统性问题定位

## 6. 相关文档

### 6.1 文档关联性

- **[文档关联性完善总结报告](../DOCUMENTATION-ISOLATION-STACK-CROSS-REFERENCES.md)** -
  所有技术文档与隔离栈文档的关联关系总结
  - 27 个技术文档的关联性完善记录
  - 关联点统计和分析
  - 文档关联性体系价值说明

### 6.2 技术文档

**可观测性相关**：

- **[16. 监控与可观测性](../16-observability/observability.md)** -
  OTLP、OpenTelemetry、Jaeger 等技术规范
- **[31. eBPF 技术堆栈](../31-ebpf-stack/ebpf-stack.md)** - eBPF 内核可编程技术
  堆栈，网络加速、可观测性应用（2025-11-07）
- **[32. eBPF/OTLP 扩展技术分析](../32-ebpf-otlp-analysis/ebpf-otlp-analysis.md)**
  ⭐ - eBPF/OTLP 扩展技术分析文档
  - 横纵耦合问题定位模型（OTLP 横向 + eBPF 纵向）
  - 技术规范对齐、性能分析、实践指南
  - 智能系统能力架构（自我感知、自动伸缩、自我治愈）
  - 故障排查、最佳实践（2025-11-07）

**故障排查相关**：

- **[11. 故障排查](../11-troubleshooting/troubleshooting.md)** - 常见故障排查方
  法

**理论基础**：

- **[12. 虚拟化/半虚拟化/容器化/沙盒化严格定义](../../COGNITIVE/05-decision-analysis/decision-models/06-technical-concepts/12-virtualization-paravirtualization-containerization-sandboxing-strict-definition.md)** -
  技术范式的严格定义
- **[02. 隔离模型](../../COGNITIVE/05-decision-analysis/decision-models/01-theory-models/02-isolation-models.md)** -
  隔离层次理论模型

**其他技术文档**：

- **[13. 缩写词汇表](../13-acronyms-glossary/acronyms-glossary.md)** - 技术缩写
  词定义

---

**最后更新**：2025-11-07 **维护者**：项目团队
