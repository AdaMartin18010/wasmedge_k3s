# Argo vs Temporal：两条工作流演进路径

## 📑 目录

- [📑 目录](#-目录)
- [概述](#概述)
- [Argo Workflows：K8s 原生消解的极致](#argo-workflows：k8s-原生消解的极致)
- [Temporal：自包含消解的独立王国](#temporal：自包含消解的独立王国)
- [对比分析](#对比分析)
- [核心启示](#核心启示)
- [相关文档](#相关文档)

---


> **本文档是 Argo vs Temporal 对比分析的简化版本。详细分析请参考：**
> [`../04-domain-case-studies/02-argo-temporal-workflow-disintegration.md`](../04-domain-case-studies/02-argo-temporal-workflow-disintegration.md)

## 概述

本文档从**分层消解律视角**简要对比 Argo 和 Temporal 两条工作流演进路径。

### 核心思想

> **Argo 和 Temporal 代表了工作流基础设施消解的两种终极范式：前者将语义彻底消解
> 至 K8s 生态，后者将工作流通用能力内聚为独立运行时。两者共同验证了同一规律——越
> 靠近业务的不变性，越无法被通用框架消解。**

## Argo Workflows：K8s 原生消解的极致

- **消解路径**：K8s 原生消解（依赖 K8s 生态）
- **层 2 消解率**：90%（K8s 原语）
- **残留语义**：DAG 拓扑与 Artifact 依赖

## Temporal：自包含消解的独立王国

- **消解路径**：自包含消解（独立运行时）
- **层 2 消解率**：70%（自研引擎）
- **残留语义**：Workflow 代码的确定性约束

## 对比分析

| 维度            | Argo Workflows                | Temporal                    |
| --------------- | ----------------------------- | --------------------------- |
| **消解路径**    | K8s 原生消解（依赖 K8s 生态） | 自包含消解（独立运行时）     |
| **层 2 消解率** | 90%（K8s 原语）               | 70%（自研引擎）              |
| **适用场景**    | 数据管道、CI/CD                | 微服务编排、长运行流程       |

## 核心启示

1. **两种消解范式各有优势**
2. **领域语义无法被消解**
3. **技术选型取决于业务场景**

## 相关文档

- [详细分析文档](../04-domain-case-studies/02-argo-temporal-workflow-disintegration.md)
- [Temporal 独立分析](../04-domain-case-studies/05-temporal-workflow-semantic-model.md)
- [Argo Workflows 独立分析](../04-domain-case-studies/06-argo-workflows-semantic-model.md)
- [分布式工作流系统消解](../03-layered-disintegration-law/03-distributed-workflow-disintegration.md)

---

**最后更新**：2025-11-08 **维护者**：项目团队

