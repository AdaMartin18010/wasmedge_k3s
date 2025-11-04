# 5 步拆分与组合流程

## 1. 概述

本文档详细阐述**架构拆解与组合的 5 步流程**，这是从软件架构视角理解虚拟化、容器
化、沙盒化的核心方法论。

### 1.1 核心思想

> **把"软件架构"拆成"子结构"（decomposition）后再组合回"整体"（composition）**

整个流程包含 5 个步骤，每步都提供**可复用的工具/模板/模式**，以便在任何项目中快
速上手。

### 1.2 5 步流程概览

| 步骤                 | 目标                             | 关键活动                                                                                                                                                                                                       | 工具 / 模板                                                               |
| -------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **1. 需求‑关切抽取** | 找到所有业务 & 非业务关切        | 访谈、用户故事、服务契约、技术约束、性能指标、合规需求                                                                                                                                                         | 问题卡、业务地图、技术债务清单                                            |
| **2. 结构化拆分**    | 把系统拆成可维护、可替换的"模块" | 按 **关注点分离**（Presentation, Application, Domain, Integration, Data, Infra, Security, Observability, Deployment）拆分；按 **Bounded Context** 或 **微服务** 进一步拆分                                     | C4/ArchiMate 模型、DDD 边界图、服务矩阵                                   |
| **3. 接口与契约**    | 明确定义子结构的 **输入/输出**   | API 文档、gRPC/Protobuf、事件 schema、数据模型、配置/凭据契约                                                                                                                                                  | OpenAPI, GraphQL SDL, Avro/Protobuf, Terraform modules                    |
| **4. 组合模式**      | 让拆分出的组件互联、互操作       | ① **依赖注入 / Composition Root** <br>② **适配器 / 桥接**（跨技术边界）<br>③ **Facade / Gateway**（聚合多服务）<br>④ **Pipeline / Orchestrator**（业务流程）<br>⑤ **Service Mesh / API Gateway**（通信、流控） | Spring DI / Guice, OSGi / CDI, Netflix Eureka, Envoy, Istio, Apache Camel |
| **5. 自动化 & 验证** | 确保组合后可运行、可监控、可测试 | CI/CD（Jenkins, GitHub Actions）, K8s + Helm, Prometheus/Tempo, OpenTelemetry, Chaos Monkey, ADR 生成                                                                                                          | GitHub repo + GitHub Actions, ArgoCD, Kustomize, Argo Rollouts            |

## 2. 步骤 1：需求关切抽取

### 2.1 目标

找到所有业务与非业务关切，为后续拆分提供依据。

### 2.2 关键活动

#### 2.2.1 业务关切

- **用户故事**：从用户视角描述功能需求
- **业务流程**：识别核心业务流程和关键路径
- **服务契约**：定义服务接口和交互协议

#### 2.2.2 非业务关切

- **技术约束**：性能、延迟、吞吐量要求
- **合规需求**：安全、审计、合规性要求
- **运维需求**：可观测性、可扩展性、灾难恢复

### 2.3 工具与模板

- **问题卡**：记录关键问题和约束
- **业务地图**：可视化业务流程和依赖关系
- **技术债务清单**：记录现有技术债务和限制

### 2.4 形式化定义

```text
需求集 R = {r₁, r₂, ..., rₙ}
其中 rᵢ = ⟨type, priority, constraint⟩
type ∈ {business, technical, compliance, operations}
```

## 3. 步骤 2：结构化拆分

### 3.1 目标

把系统拆成可维护、可替换的"模块"。

### 3.2 拆分原则

#### 3.2.1 关注点分离（Separation of Concerns）

按以下 9 个关注点拆分：

1. **表现层（Presentation）**：交互、展示、前端
2. **应用层（Application）**：业务流程、协调
3. **领域层（Domain）**：业务核心
4. **集成层（Integration）**：与外部系统交互
5. **数据层（Data）**：数据存储、事务
6. **基础设施层（Infrastructure）**：主机、网络、存储
7. **安全层（Security）**：访问控制、身份鉴权
8. **可观测层（Observability）**：监控、日志、追踪
9. **运营层（Operations）**：部署、滚动升级、灾备

#### 3.2.2 领域驱动设计（DDD）

按 **Bounded Context** 进一步拆分：

- **Order Service**（订单服务）
- **Payment Service**（支付服务）
- **Inventory Service**（库存服务）
- **Catalog Service**（目录服务）
- **User Service**（用户服务）

### 3.3 工具与模板

- **C4/ArchiMate 模型**：层次化架构可视化
- **DDD 边界图**：领域边界和上下文映射
- **服务矩阵**：服务依赖关系矩阵

### 3.4 形式化定义

```text
系统 S = {C₁, C₂, ..., Cₙ}
其中 Cᵢ = ⟨name, layer, responsibilities, interfaces⟩
layer ∈ {presentation, application, domain, integration, data, infra, security, observability, operations}
```

## 4. 步骤 3：接口与契约

### 4.1 目标

明确定义子结构的 **输入/输出**。

### 4.2 契约类型

#### 4.2.1 API 契约

- **REST API**：OpenAPI 3.0 规范
- **gRPC**：Protobuf 定义
- **GraphQL**：SDL Schema

#### 4.2.2 事件契约

- **事件 Schema**：Avro、JSON Schema
- **消息格式**：Kafka、RabbitMQ

#### 4.2.3 数据契约

- **数据模型**：ER 图、JSON Schema
- **配置契约**：Terraform modules、Helm charts

### 4.3 工具与模板

- **OpenAPI**：REST API 规范
- **GraphQL SDL**：GraphQL Schema
- **Avro/Protobuf**：事件和数据序列化
- **Terraform modules**：基础设施配置

### 4.4 形式化定义

```text
接口 I = ⟨name, type, input, output, contract⟩
其中 type ∈ {API, Event, Data, Config}
contract 定义了接口的语义和行为约束
```

## 5. 步骤 4：组合模式

### 5.1 目标

让拆分出的组件互联、互操作。

### 5.2 组合模式类型

#### 5.2.1 依赖注入 / Composition Root

- **Spring DI**：依赖注入框架
- **Guice**：Google 依赖注入
- **CDI**：Java EE 上下文和依赖注入

#### 5.2.2 适配器 / 桥接

- **gRPC ↔ REST**：跨协议转换
- **Docker ↔ K8s**：容器运行时适配

#### 5.2.3 Facade / Gateway

- **API Gateway**：Kong、Istio Gateway
- **Service Gateway**：Netflix Zuul、Spring Cloud Gateway

#### 5.2.4 Pipeline / Orchestrator

- **Temporal**：工作流引擎
- **Argo Workflows**：Kubernetes 工作流
- **Camunda**：业务流程管理

#### 5.2.5 Service Mesh / API Gateway

- **Istio**：服务网格
- **Linkerd**：轻量级服务网格
- **Envoy**：云原生代理

### 5.3 工具与模板

- **Spring DI / Guice**：依赖注入
- **OSGi / CDI**：模块化框架
- **Netflix Eureka**：服务发现
- **Envoy**：云原生代理
- **Istio**：服务网格
- **Apache Camel**：企业集成模式

### 5.4 形式化定义

```text
组合模式 P = ⟨type, components, relations⟩
其中 type ∈ {DI, Adapter, Facade, Pipeline, Mesh}
relations 定义了组件间的连接关系
```

## 6. 步骤 5：自动化与验证

### 6.1 目标

确保组合后可运行、可监控、可测试。

### 6.2 自动化活动

#### 6.2.1 CI/CD

- **GitHub Actions**：自动化构建、测试、部署
- **Jenkins**：持续集成服务器
- **ArgoCD**：GitOps 持续交付

#### 6.2.2 部署自动化

- **Kubernetes + Helm**：容器编排和包管理
- **Kustomize**：配置管理
- **Argo Rollouts**：渐进式交付

#### 6.2.3 可观测性

- **Prometheus**：指标收集
- **Tempo / Jaeger**：分布式追踪
- **OpenTelemetry**：统一遥测

#### 6.2.4 测试与验证

- **Chaos Monkey**：混沌工程
- **ADR 生成**：架构决策记录

### 6.3 工具与模板

- **GitHub Actions**：CI/CD 自动化
- **ArgoCD**：GitOps
- **Kustomize**：配置管理
- **Argo Rollouts**：渐进式交付

### 6.4 形式化定义

```text
自动化流程 A = ⟨trigger, stages, validation⟩
其中 stages = {build, test, deploy, monitor}
validation 确保每个阶段的质量标准
```

## 7. 实践建议

### 7.1 每完成一次拆分/组合

都在 **ADR** 里写一条记录：`<Component> 采用 <Pattern> 以满足 <Constraint>`。

### 7.2 采用 C4 模型

- **上下文图**：系统与外部环境的关系
- **容器图**：应用容器和部署单元
- **组件图**：组件内部结构
- **代码图**：类和函数级别

### 7.3 用 ArchiMate 或 UML

记录 **业务能力**、**技术能力**、**安全/合规** 等非功能需求。

## 8. 典型案例

### 8.1 电商平台

| 步骤          | 结果                                                                                                                               | 说明         |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| 1. 需求抽取   | 订单、支付、库存、营销、用户                                                                                                       | 业务功能列表 |
| 2. 结构化拆分 | **Order Service** (微服务)<br>**Payment Service**<br>**Inventory Service**<br>**Catalog Service**<br>**User Service**              | DDD 边界     |
| 3. 接口契约   | OpenAPI / gRPC                                                                                                                     | 统一文档     |
| 4. 组合       | <br>• API Gateway (Kong) 聚合 REST <br>• Service Mesh (Istio) 进行熔断、流量镜像 <br>• Kafka 作为事件总线 (OrderCreated → Payment) |              |
| 5. 自动化     | CI/CD (GitHub Actions) <br>Helm chart 部署 <br>Prometheus/Tempo 监控 <br>Chaos Monkey 可靠性                                       |              |

### 8.2 金融系统

| 步骤          | 结果                                                                               | 说明   |
| ------------- | ---------------------------------------------------------------------------------- | ------ |
| 1. 需求抽取   | 交易、清算、风险、合规                                                             | 业务线 |
| 2. 结构化拆分 | 交易微服务 + 风险校验微服务 + 合规审计微服务                                       |        |
| 3. 接口契约   | gRPC + Protobuf（强类型）                                                          |        |
| 4. 组合       | ① Service Mesh + Sidecar <br>② 事件总线 + 事务 Saga <br>③ 统一认证（OAuth2 + JWT） |        |
| 5. 自动化     | Terraform + Pulumi <br>ArgoCD <br>OPA + Gatekeeper <br>Grafana Loki                |        |

## 9. 总结

通过 **5 步拆分与组合流程**，我们可以：

1. **拆分**：按关切、领域、层次把系统拆成清晰的"组件"
2. **合成**：用 **组合模式**把组件拼接
3. **验证**：通过 **ADR、C4 模型、CI/CD、监控** 证明组合后仍满足功能与非功能需求
4. **迭代**：随业务变更、技术演进，持续拆分并重新组合，保持架构的弹性与可维护性

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第 2 节
