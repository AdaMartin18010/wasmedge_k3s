# 多视角架构视图

## 📑 目录

- [📑 目录](#-目录)
- [📖 文档简介](#-文档简介)
- [📋 视角文档列表](#-视角文档列表)
- [🔗 相关文档](#-相关文档)
  - [架构视角文档](#架构视角文档)
  - [技术文档](#技术文档)
  - [认知模型文档](#认知模型文档)
  - [多视角文档](#多视角文档)

---

## 📖 文档简介

本文档集从**多个视角**阐述软件架构，每个视角关注不同的架构维度：

- **功能视角**：关注系统的功能和行为
- **结构视角**：关注系统的组件和关系
- **行为视角**：关注系统的动态行为
- **数据视角**：关注数据的流动和处理
- **安全视角**：关注系统的安全性
- **可观测性视角**：关注系统的监控、追踪、日志
- **eBPF/OTLP 视角**：关注横纵耦合的可观测性驱动架构 ⭐

---

## 📋 视角文档列表

| 文档                                                 | 视角      | 核心内容                   | 状态    |
| ---------------------------------------------------- | --------- | -------------------------- | ------- |
| [01. 功能视角](01-functional-perspective.md)         | 功能      | 系统的功能和行为           | ✅      |
| [02. 结构视角](02-structural-perspective.md)         | 结构      | 系统的组件和关系           | ✅      |
| [03. 行为视角](03-behavioral-perspective.md)         | 行为      | 系统的动态行为             | ✅      |
| [04. 数据视角](04-data-perspective.md)               | 数据      | 数据的流动和处理           | ✅      |
| [05. 安全视角](05-security-perspective.md)           | 安全      | 系统的安全性               | ✅      |
| [06. 可观测性视角](06-observability-perspective.md)  | 可观测性  | 监控、追踪、日志           | ✅      |
| [07. eBPF/OTLP 视角](07-ebpf-otlp-perspective.md) ⭐ | eBPF/OTLP | 横纵耦合的可观测性驱动架构 | ✅ 新增 |

---

## 🔗 相关文档

### 架构视角文档

- **[架构视图总览](../README.md)** - 完整的架构视图文档集
- **[架构视角主文档](../../../../architecture_view.md)** - 架构视角的核心论述

### 技术文档

- **[32. eBPF/OTLP 扩展技术分析](../../../../TECHNICAL/32-ebpf-otlp-analysis/ebpf-otlp-analysis.md)**
  ⭐ - eBPF/OTLP 扩展技术分析文档
- **[31. eBPF 技术堆栈](../../../../TECHNICAL/31-ebpf-stack/ebpf-stack.md)** -
  eBPF 技术堆栈完整技术参考文档
- **[29. 隔离栈](../../../../TECHNICAL/29-isolation-stack/isolation-stack.md)** -
  问题定位模型、横纵耦合定位方法
- **[16. 监控与可观测性](../../../../TECHNICAL/16-observability/observability.md)** -
  OTLP、OpenTelemetry、eBPF 等技术规范

### 认知模型文档

- **[13. eBPF/OTLP 认知视角](../../../../COGNITIVE/04-application-perspectives/ebpf-otlp-perspective/ebpf-otlp-perspective.md)**
  ⭐ - eBPF/OTLP 认知视角分析文档

### 多视角文档

- **[eBPF/OTLP 视角完整文档](../../../../ebpf_otlp_view.md)** - eBPF/OTLP 视角完
  整文档（1438 行）

---

**最后更新**：2025-11-07 **版本**：v1.0 **维护者**：项目团队
