# 领域驱动设计（Domain-Driven Design）

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 Wikipedia 定义](#11-wikipedia-定义)
  - [1.2 文档定位](#12-文档定位)
- [2 Wikipedia 定义与解释](#2-wikipedia-定义与解释)
  - [2.1 核心定义](#21-核心定义)
  - [2.2 技术原理](#22-技术原理)
  - [2.3 应用场景](#23-应用场景)
- [3 核心概念](#3-核心概念)
  - [3.1 领域模型](#31-领域模型)
  - [3.2 有界上下文](#32-有界上下文)
  - [3.3 聚合根](#33-聚合根)
  - [3.4 领域事件](#34-领域事件)
- [4 设计模式](#4-设计模式)
  - [4.1 实体（Entity）](#41-实体entity)
  - [4.2 值对象（Value Object）](#42-值对象value-object)
  - [4.3 领域服务（Domain Service）](#43-领域服务domain-service)
  - [4.4 仓储（Repository）](#44-仓储repository)
- [5 与分层消解律的关系](#5-与分层消解律的关系)
  - [5.1 领域语义的不可约简性](#51-领域语义的不可约简性)
  - [5.2 通用框架的消解边界](#52-通用框架的消解边界)
  - [5.3 双向赋能](#53-双向赋能)
- [6 2025 年 11 月趋势](#6-2025-年-11-月趋势)
  - [6.1 技术趋势](#61-技术趋势)
  - [6.2 架构演进](#62-架构演进)
- [7 总结](#7-总结)
- [8 参考资源](#8-参考资源)
  - [8.1 Wikipedia 资源](#81-wikipedia-资源)
  - [8.2 技术文档](#82-技术文档)
  - [8.3 相关文档](#83-相关文档)

---

## 1 概述

本文档基于**Wikipedia 定义**系统阐述领域驱动设计（Domain-Driven Design）的概念、
技术原理和应用场景，并分析其在分层消解律中的位置。

### 1.1 Wikipedia 定义

**领域驱动设计（Domain-Driven Design）**：领域驱动设计是一种软件开发方法，专注于
复杂软件的设计，通过将实现与不断发展的核心概念模型联系起来。

**来
源**：[Wikipedia - Domain-driven design](https://en.wikipedia.org/wiki/Domain-driven_design)

### 1.2 文档定位

- **目标读者**：软件架构师、领域驱动设计研究者、业务分析师
- **前置知识**：面向对象设计、软件架构、业务建模
- **关联文档**：
  - [`../02-semantic-model-perspective/02-irreducibility-of-domain-semantics.md`](../02-semantic-model-perspective/02-irreducibility-of-domain-semantics.md) -
    领域语义无法通用化的本质原因
  - [`../02-semantic-model-perspective/03-mutual-empowerment-of-frameworks-domains.md`](../02-semantic-model-perspective/03-mutual-empowerment-of-frameworks-domains.md) -
    通用框架与领域模型的双向赋能
  - [`06-layer-abstraction.md`](06-layer-abstraction.md) - 分层抽象（Layered
    Abstraction）

---

## 2 Wikipedia 定义与解释

### 2.1 核心定义

**领域驱动设计（Domain-Driven Design）**：

> **领域驱动设计是一种软件开发方法，专注于复杂软件的设计，通过将实现与不断发展的
> 核心概念模型联系起来。**

**核心特征**：

- **领域模型**：以领域模型为核心，将实现与领域模型联系起来
- **有界上下文**：通过有界上下文划分领域边界
- **通用语言**：使用通用语言（Ubiquitous Language）沟通
- **持续演进**：领域模型持续演进，反映业务变化

### 2.2 技术原理

**领域驱动设计技术原理**：

- **领域模型**：以领域模型为核心，将实现与领域模型联系起来
- **有界上下文**：通过有界上下文划分领域边界
- **通用语言**：使用通用语言（Ubiquitous Language）沟通
- **持续演进**：领域模型持续演进，反映业务变化

**典型实现**：

- **实体（Entity）**：具有唯一标识的对象
- **值对象（Value Object）**：没有唯一标识的对象
- **领域服务（Domain Service）**：不属于任何实体的领域逻辑
- **仓储（Repository）**：封装数据访问逻辑

### 2.3 应用场景

**领域驱动设计应用场景**：

- **复杂业务系统**：电商、金融、医疗等复杂业务系统
- **微服务架构**：通过领域驱动设计划分微服务边界
- **遗留系统重构**：通过领域驱动设计重构遗留系统
- **新系统设计**：在新系统设计中应用领域驱动设计

---

## 3 核心概念

### 3.1 领域模型

**领域模型（Domain Model）**：

- **定义**：领域模型是对业务领域的抽象表示
- **特征**：领域模型反映业务规则和业务逻辑
- **作用**：领域模型是软件设计的核心，指导实现

### 3.2 有界上下文

**有界上下文（Bounded Context）**：

- **定义**：有界上下文是领域模型的边界，定义了领域模型的适用范围
- **特征**：每个有界上下文有自己的领域模型和通用语言
- **作用**：通过有界上下文划分领域边界，避免领域模型混乱

### 3.3 聚合根

**聚合根（Aggregate Root）**：

- **定义**：聚合根是聚合的入口，负责维护聚合的一致性
- **特征**：聚合根是唯一可以从外部访问的对象
- **作用**：通过聚合根维护聚合的一致性边界

### 3.4 领域事件

**领域事件（Domain Event）**：

- **定义**：领域事件是领域中发生的重要业务事件
- **特征**：领域事件是不可变的，反映业务状态变化
- **作用**：通过领域事件实现领域间的解耦和通信

---

## 4 设计模式

### 4.1 实体（Entity）

**实体（Entity）**：

- **定义**：实体是具有唯一标识的对象
- **特征**：实体通过唯一标识区分，即使属性相同也是不同的对象
- **示例**：订单、用户、商品等

### 4.2 值对象（Value Object）

**值对象（Value Object）**：

- **定义**：值对象是没有唯一标识的对象
- **特征**：值对象通过属性值区分，属性值相同就是同一个对象
- **示例**：金额、地址、颜色等

### 4.3 领域服务（Domain Service）

**领域服务（Domain Service）**：

- **定义**：领域服务是不属于任何实体的领域逻辑
- **特征**：领域服务是无状态的，包含领域逻辑
- **示例**：转账服务、风险评估服务等

### 4.4 仓储（Repository）

**仓储（Repository）**：

- **定义**：仓储封装数据访问逻辑，提供领域对象的持久化接口
- **特征**：仓储隐藏数据访问细节，提供领域友好的接口
- **示例**：订单仓储、用户仓储等

---

## 5 与分层消解律的关系

### 5.1 领域语义的不可约简性

**领域语义的不可约简性**：

- **核心观点**：业务领域模型需要针对性设计，本质是 CAP 定理的语义版本
- **不可约简性**：通用性、领域表达力、执行效率三者不可兼得
- **结论**：领域语义无法被通用框架消解，必须显性设计

### 5.2 通用框架的消解边界

**通用框架的消解边界**：

- **消解能力**：通用框架可以消解分布式系统的通用功能（服务发现、负载均衡、容错等
  ）
- **消解边界**：通用框架无法消解领域特定语义（业务规则、领域模型、有界上下文等）
- **结论**：通用框架的消解边界是领域语义的起点

### 5.3 双向赋能

**通用框架与领域模型的双向赋能**：

- **通用框架 → 领域模型**：通用框架为领域模型提供可扩展、高可用、可观测的运行底
  座
- **领域模型 → 通用框架**：领域模型通过 CRD/Operator 反向定义框架行为
- **结论**：通用框架与领域模型双向赋能，协同增效

---

## 6 2025 年 11 月趋势

### 6.1 技术趋势

**2025 年 11 月技术趋势**：

1. **领域特定基础设施**：Dapr、Temporal 等将领域模式固化为基础设施
2. **领域专用运行时**：金融风控运行时、物联网运行时、电商运行时
3. **零开销抽象**：通过 WebAssembly 和 eBPF 实现零开销抽象

### 6.2 架构演进

**架构演进方向**：

- **领域特定基础设施**：高频出现的领域模式下沉为领域特定基础设施
- **领域专用运行时**：形成领域专用运行时，实现领域语义与通用框架的零开销融合
- **零开销抽象**：通过 WebAssembly 和 eBPF 实现零开销抽象

---

## 7 总结

**领域驱动设计（Domain-Driven Design）核心结论**：

1. **Wikipedia 定义**：领域驱动设计是一种软件开发方法，专注于复杂软件的设计，通
   过将实现与不断发展的核心概念模型联系起来
2. **技术原理**：通过领域模型、有界上下文、通用语言、持续演进实现领域驱动设计
3. **应用场景**：复杂业务系统、微服务架构、遗留系统重构、新系统设计
4. **核心概念**：领域模型、有界上下文、聚合根、领域事件
5. **与分层消解律的关系**：领域语义的不可约简性、通用框架的消解边界、双向赋能

**核心结论**：领域驱动设计强调领域语义的不可约简性，这与分层消解律的核心观点一致
。领域语义无法被通用框架消解，必须显性设计。这并非技术债务，而是**语义分工的必然
结果**。

---

## 8 参考资源

### 8.1 Wikipedia 资源

- [Domain-driven design](https://en.wikipedia.org/wiki/Domain-driven_design)
- [Domain model](https://en.wikipedia.org/wiki/Domain_model)
- [Bounded context](https://en.wikipedia.org/wiki/Bounded_context)

### 8.2 技术文档

- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Domain-Driven Design: Tackling Complexity in the Heart of Software](https://www.domainlanguage.com/ddd/)
- [Domain-Driven Design Reference](https://www.domainlanguage.com/ddd/reference/)

### 8.3 相关文档

- [`../02-semantic-model-perspective/02-irreducibility-of-domain-semantics.md`](../02-semantic-model-perspective/02-irreducibility-of-domain-semantics.md) -
  领域语义无法通用化的本质原因
- [`../02-semantic-model-perspective/03-mutual-empowerment-of-frameworks-domains.md`](../02-semantic-model-perspective/03-mutual-empowerment-of-frameworks-domains.md) -
  通用框架与领域模型的双向赋能
- [`06-layer-abstraction.md`](06-layer-abstraction.md) - 分层抽象（Layered
  Abstraction）

---
