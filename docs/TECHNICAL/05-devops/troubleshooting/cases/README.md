# 故障排查案例集

> **创建日期**：2025-11-13  
> **更新频率**：随案例补充更新

---

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
- [2 案例分类](#2-案例分类)
- [3 案例列表](#3-案例列表)
  - [3.1 WasmEdge 故障案例](#31-wasmedge-故障案例)
  - [3.2 K3s 故障案例](#32-k3s-故障案例)
  - [3.3 OPA/Gatekeeper 故障案例](#33-opagatekeeper-故障案例)
  - [3.4 网络故障案例](#34-网络故障案例)
  - [3.5 存储故障案例](#35-存储故障案例)
- [4 使用指南](#4-使用指南)
- [5 相关文档](#5-相关文档)

---

## 1 概述

本文档集提供详细的故障排查案例，每个案例包含完整的故障描述、排查过程、根因分析、解决方案和验证结果。

**案例特点**：

- ✅ **真实性**：基于真实场景
- ✅ **完整性**：包含完整的排查过程
- ✅ **可重现性**：可在类似环境中重现
- ✅ **可验证性**：解决方案经过验证

---

## 2 案例分类

### 2.1 按组件分类

- **WasmEdge 故障案例**：Wasm 应用相关问题
- **K3s 故障案例**：K3s 集群相关问题
- **OPA/Gatekeeper 故障案例**：策略管理相关问题
- **网络故障案例**：网络连接和通信问题
- **存储故障案例**：存储卷和存储性能问题

### 2.2 按严重程度分类

- **严重故障**：影响生产环境，需要立即处理
- **中等故障**：影响部分功能，需要尽快处理
- **轻微故障**：影响性能或体验，可以计划处理

### 2.3 按故障类型分类

- **启动失败**：应用或服务无法启动
- **运行时错误**：运行过程中出现错误
- **性能问题**：性能不达预期
- **安全漏洞**：安全相关问题
- **配置错误**：配置不当导致的问题

---

## 3 案例列表

### 3.1 WasmEdge 故障案例

| 编号 | 案例标题 | 严重程度 | 状态 |
|-----|---------|---------|------|
| [W-001](wasmedge-cold-start-timeout.md) | Wasm 应用冷启动超时 | 严重 | ✅ 已完成 |
| [W-002](wasmedge-memory-overflow.md) | Wasm 内存溢出 | 严重 | ⏳ 待补充 |
| [W-003](wasmedge-network-connection-failed.md) | Wasm 网络连接失败 | 中等 | ⏳ 待补充 |
| [W-004](wasmedge-filesystem-access-error.md) | Wasm 文件系统访问错误 | 中等 | ⏳ 待补充 |
| [W-005](wasmedge-multithreading-issue.md) | Wasm 多线程问题 | 中等 | ⏳ 待补充 |
| [W-006](wasmedge-performance-degradation.md) | Wasm 性能下降 | 轻微 | ⏳ 待补充 |
| [W-007](wasmedge-image-pull-failed.md) | Wasm 镜像拉取失败 | 中等 | ⏳ 待补充 |
| [W-008](wasmedge-log-output-abnormal.md) | Wasm 日志输出异常 | 轻微 | ⏳ 待补充 |

### 3.2 K3s 故障案例

| 编号 | 案例标题 | 严重程度 | 状态 |
|-----|---------|---------|------|
| [K-001](k3s-node-join-failed.md) | K3s 节点无法加入集群 | 严重 | ⏳ 待补充 |
| [K-002](k3s-pod-scheduling-failed.md) | K3s Pod 调度失败 | 严重 | ⏳ 待补充 |
| [K-003](k3s-storage-volume-mount-failed.md) | K3s 存储卷挂载失败 | 中等 | ⏳ 待补充 |
| [K-004](k3s-network-policy-not-effective.md) | K3s 网络策略不生效 | 中等 | ⏳ 待补充 |
| [K-005](k3s-control-plane-high-load.md) | K3s 控制平面高负载 | 中等 | ⏳ 待补充 |
| [K-006](k3s-certificate-expired.md) | K3s 证书过期问题 | 严重 | ⏳ 待补充 |

### 3.3 OPA/Gatekeeper 故障案例

| 编号 | 案例标题 | 严重程度 | 状态 |
|-----|---------|---------|------|
| [O-001](gatekeeper-webhook-timeout.md) | Gatekeeper Webhook 超时 | 严重 | ⏳ 待补充 |
| [O-002](opa-policy-evaluation-failed.md) | OPA 策略评估失败 | 中等 | ⏳ 待补充 |
| [O-003](gatekeeper-policy-update-delayed.md) | Gatekeeper 策略更新延迟 | 中等 | ⏳ 待补充 |
| [O-004](opa-performance-issue.md) | OPA 性能问题 | 轻微 | ⏳ 待补充 |

### 3.4 网络故障案例

| 编号 | 案例标题 | 严重程度 | 状态 |
|-----|---------|---------|------|
| [N-001](pod-cross-node-communication-failed.md) | Pod 跨节点通信失败 | 严重 | ⏳ 待补充 |
| [N-002](service-unreachable.md) | Service 无法访问 | 严重 | ⏳ 待补充 |
| [N-003](ingress-routing-error.md) | Ingress 路由错误 | 中等 | ⏳ 待补充 |

### 3.5 存储故障案例

| 编号 | 案例标题 | 严重程度 | 状态 |
|-----|---------|---------|------|
| [S-001](pvc-mount-failed.md) | PVC 挂载失败 | 严重 | ⏳ 待补充 |
| [S-002](storage-performance-issue.md) | 存储性能问题 | 中等 | ⏳ 待补充 |

---

## 4 使用指南

### 4.1 如何查找案例

1. **按组件查找**：根据问题涉及的组件（WasmEdge、K3s、OPA 等）查找对应分类
2. **按严重程度查找**：根据故障的紧急程度查找对应分类
3. **按故障类型查找**：根据故障类型（启动失败、运行时错误等）查找对应分类

### 4.2 如何使用案例

1. **阅读故障描述**：了解故障现象和影响范围
2. **参考排查过程**：按照排查步骤进行诊断
3. **应用解决方案**：根据根因分析应用相应的解决方案
4. **验证修复效果**：按照验证方法确认问题已解决

### 4.3 案例贡献

如果您有新的故障排查案例，欢迎贡献：

1. 按照案例模板创建新案例文档
2. 确保案例包含完整的故障描述、排查过程、根因分析、解决方案和验证结果
3. 在本 README 中添加案例链接

---

## 5 相关文档

- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南
- [`../../PRACTICAL-CASE-SUPPLEMENT-PLAN.md`](../../PRACTICAL-CASE-SUPPLEMENT-PLAN.md) - 实践案例补充计划
- [`../../DOCUMENTATION-BENCHMARK-ANALYSIS.md`](../../DOCUMENTATION-BENCHMARK-ANALYSIS.md) - 文档对标分析报告

---

**最后更新**：2025-11-13  
**维护者**：项目团队  
**版本**：v1.0

