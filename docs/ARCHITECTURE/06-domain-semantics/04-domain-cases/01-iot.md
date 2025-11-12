# IoT：业务硬核如何穿透基础设施消解

## 📑 目录

- [📑 目录](#-目录)
- [概述](#概述)
- [IoT 核心领域模型](#iot-核心领域模型)
- [顽固残留的领域语义](#顽固残留的领域语义)
- [消解率分析](#消解率分析)
- [核心启示](#核心启示)
- [相关文档](#相关文档)

---


> **本文档是 IoT 领域案例分析的简化版本。详细分析请参考：**
> [`../04-domain-case-studies/04-iot-domain-model-penetration.md`](../04-domain-case-studies/04-iot-domain-model-penetration.md)

## 概述

本文档从**领域模型视角**简要分析 IoT 架构中的业务硬核如何穿透基础设施消解。

### 核心思想

> **基础设施的通用能力（容器/K8s）向上渗透，但 IoT 领域的核心语义（设备影子、规
> 则链、时空属性）因其强烈的业务契约性，反而成为架构中不可压缩的硬核层。**

## IoT 核心领域模型

1. **设备影子（Device Shadow）** - 设备数字孪生，强一致性状态机
2. **规则链（Rule Chain）** - 事件驱动的业务决策流
3. **时空分区（Time-Location Sharding）** - 设备数据按地理/时间分片策略
4. **设备认证生命周期（Device Certificate Lifecycle）** - 设备身份的可信链管理

## 顽固残留的领域语义

- **设备影子同步**：reported/desired 状态差异必须显式同步
- **规则链执行**：规则触发顺序影响业务结果（时序敏感）
- **时空分区策略**：时序数据必须按时间区间聚合（降采样）

## 消解率分析

- **基础设施层**：消解率 ≈ 80%（K8s 原生支持）
- **领域语义层**：消解率 ≈ 0%（业务规则无法消解）

## 核心启示

1. **设备影子、规则链、时空分区是 IoT 领域的核心知识**
2. **这些领域语义无法被通用框架消解**
3. **云原生 IoT 架构需要领域层"寄生"于通用层**

## 相关文档

- [详细分析文档](../04-domain-case-studies/04-iot-domain-model-penetration.md)
- [领域语义无法通用化](../02-semantic-model-perspective/02-irreducibility-of-domain-semantics.md)
- [分层消解律概述](../03-layered-disintegration-law/01-introduction.md)

---

**最后更新**：2025-11-08 **维护者**：项目团队

