# 软件架构视角文档索引

## 📑 目录

- [📑 目录](#-目录)
- [1. 文档索引](#1-文档索引)
  - [1.1 架构拆解与组合 (`01-decomposition-composition/`)](#11-架构拆解与组合-01-decomposition-composition)
  - [1.2 虚拟化容器化沙盒化 (`02-virtualization-containerization-sandboxing/`)](#12-虚拟化容器化沙盒化-02-virtualization-containerization-sandboxing)
  - [1.3 服务网格与网络服务网格 (`03-service-mesh-nsm/`)](#13-服务网格与网络服务网格-03-service-mesh-nsm)
  - [1.4 OPA 策略治理 (`04-opa-policy-governance/`)](#14-opa-策略治理-04-opa-policy-governance)
  - [1.5 形式化论证 (`05-formal-proofs/`)](#15-形式化论证-05-formal-proofs)
  - [1.6 概念属性关系 (`06-concepts-properties-relations/`)](#16-概念属性关系-06-concepts-properties-relations)
  - [1.7 动态运维 (`07-dynamic-operations/`)](#17-动态运维-07-dynamic-operations)
  - [1.8 组合模式 (`08-composition-patterns/`)](#18-组合模式-08-composition-patterns)
  - [1.9 多视角分析 (`09-multi-perspectives/`)](#19-多视角分析-09-multi-perspectives)
  - [1.10 2025 年 11 月更新 ⚠️ 已删除（内容合并到 `05-trends-2025/`）](#110-2025-年-11-月更新-️-已删除内容合并到-05-trends-2025)
- [2. 相关文档](#2-相关文档)
  - [2.1 参考资源](#21-参考资源)
  - [2.2 组合模式文档](#22-组合模式文档)

---

## 1. 文档索引

### 1.1 架构拆解与组合 (`01-decomposition-composition/`)

- [01. 5 步拆分与组合流程](01-decomposition-composition/01-5-step-process.md)

  - 需求关切抽取
  - 结构化拆分
  - 接口与契约
  - 组合模式
  - 自动化与验证

- [02. 分层拆解](01-decomposition-composition/02-layered-decomposition.md)

  - 9 层架构模型
  - 层次依赖关系
  - 接口边界定义

- [03. 组合模式](01-decomposition-composition/03-composition-patterns.md)

  - Composition Root
  - Adapter / Bridge
  - Facade / Gateway
  - Composite
  - Pipeline / Orchestrator

- [04. 接口与契约](01-decomposition-composition/04-interfaces-contracts.md)

  - API 文档
  - gRPC/Protobuf
  - 事件 Schema
  - 数据模型

- [05. 思维模型](01-decomposition-composition/05-thinking-models.md)

  - 层次化
  - 领域边界
  - 接口契约
  - 组合模式
  - 技术栈
  - 可持续

---

### 1.2 虚拟化容器化沙盒化 (`02-virtualization-containerization-sandboxing/`)

- [01. 虚拟化抽象](02-virtualization-containerization-sandboxing/01-virtualization-abstraction.md)

  - 硬件抽象
  - VM 资源池
  - Hypervisor 层

- [02. 容器化抽象](02-virtualization-containerization-sandboxing/02-containerization-abstraction.md)

  - OS 抽象
  - 轻量容器
  - 共享内核

- [03. 沙盒化抽象](02-virtualization-containerization-sandboxing/03-sandboxing-abstraction.md)

  - 进程抽象
  - 安全进程
  - 隔离边界

- [04. 递进抽象](02-virtualization-containerization-sandboxing/04-progressive-abstraction.md)

  - 抽象层次
  - 状态压缩
  - 形式化映射

- [05. 对比矩阵](02-virtualization-containerization-sandboxing/05-comparison-matrix.md)

  - 技术对比
  - 性能对比
  - 安全对比

---

### 1.3 服务网格与网络服务网格 (`03-service-mesh-nsm/`)

- [01. Service Mesh 架构](03-service-mesh-nsm/01-service-mesh-architecture.md)

  - Sidecar 模式
  - 控制平面
  - 数据平面

- [02. Network Service Mesh 架构](03-service-mesh-nsm/02-nsm-architecture.md)

  - vWire 连接
  - 跨域网络
  - 统一网络抽象

- [03. 流量治理](03-service-mesh-nsm/03-traffic-governance.md)

  - 流量路由
  - 负载均衡
  - 熔断降级

- [04. NSM 架构](03-service-mesh-nsm/04-nsm-architecture.md)

  - vWire 连接
  - 跨域聚合
  - 网络服务组合

---

### 1.4 OPA 策略治理 (`04-opa-policy-governance/`)

- [01. OPA 架构](04-opa-policy-governance/01-opa-architecture.md)

  - 策略即代码
  - 统一决策
  - 版本治理

- [02. 策略语言](04-opa-policy-governance/02-policy-language.md)

  - Rego 语言
  - 策略规则
  - 策略测试

- [03. 策略执行](04-opa-policy-governance/03-policy-execution.md)

  - 决策点
  - 执行点
  - 策略分发

---

### 1.5 形式化论证 (`05-formal-proofs/`)

> **注意**：本目录已删除，内容已合并到 `../../00-theory/` 目录。详细内容请参考：
>
> - [`../../00-theory/`](../../00-theory/) - 完整的理论论证文档集
> - [`../../00-theory/README.md`](../../00-theory/README.md) - 理论论证文档集总
>   览

---

### 1.6 概念属性关系 (`06-concepts-properties-relations/`)

- [01. 概念定义](06-concepts-properties-relations/01-concept-definitions.md)

  - 核心概念
  - 概念分类
  - 概念关系

- [02. 属性关系](06-concepts-properties-relations/02-property-relations.md)

  - 属性定义
  - 属性分类
  - 属性关系

- [03. 关系图谱](06-concepts-properties-relations/03-relationship-graph.md)

  - 关系定义
  - 关系分类
  - 关系图谱

- [04. 拓展场景](06-concepts-properties-relations/04-extensions.md)

  - 拓展概念
  - 拓展属性
  - 拓展关系

---

### 1.7 动态运维 (`07-dynamic-operations/`)

- [01. GitOps](07-dynamic-operations/01-gitops.md)

  - Git 驱动
  - 自动化部署
  - 版本控制

- [02. Observability](07-dynamic-operations/02-observability.md)

  - 监控
  - 日志
  - 追踪

- [03. Autoscaling](07-dynamic-operations/03-autoscaling.md)

  - HPA
  - VPA
  - 集群扩缩容

---

### 1.8 组合模式 (`08-composition-patterns/`)

- [01. Adapter / Bridge 模式](08-composition-patterns/01-adapter-bridge.md)

  - 跨技术边界
  - 协议转换
  - 运行时适配

- [02. Facade / Gateway 模式](08-composition-patterns/02-facade.md)

  - 统一接口
  - 服务聚合
  - API Gateway

- [03. Pipeline / Orchestration 模式](08-composition-patterns/03-pipeline.md)

  - 流程编排
  - 数据流
  - 步骤组合

- [04. Service Mesh 模式](08-composition-patterns/04-service-mesh-pattern.md)

  - Sidecar 模式
  - 流量治理
  - mTLS

- [05. NSM 模式](08-composition-patterns/05-nsm-pattern.md)
  - vWire 连接
  - 跨域网络聚合
  - 多 Mesh 叠加

**相关文档**：

- [Service Aggregation 模式](../08-composition-patterns/05-nsm-pattern.md#service-aggregation) -
  Service Aggregation 模式（在 NSM 模式文档中）
- [组合模式文档集](../08-composition-patterns/README.md) - 组合模式文档集总览

---

### 1.9 多视角分析 (`09-multi-perspectives/`)

- [01. 功能视角](09-multi-perspectives/01-functional-perspective.md)

  - 功能需求
  - 服务契约
  - 业务能力

- [02. 结构视角](09-multi-perspectives/02-structural-perspective.md)

  - 组件结构
  - 依赖关系
  - 接口定义

- [03. 行为视角](09-multi-perspectives/03-behavioral-perspective.md)

  - 动态行为
  - 交互流程
  - 状态转换

- [04. 数据视角](09-multi-perspectives/04-data-perspective.md)

  - 数据模型
  - 数据流
  - 数据一致性

- [05. 安全视角](09-multi-perspectives/05-security-perspective.md)

  - 访问控制
  - 身份鉴权
  - 策略治理

- [06. 可观测视角](09-multi-perspectives/06-observability-perspective.md)
  - 指标
  - 日志
  - 追踪

---

### 1.10 2025 年 11 月更新 ⚠️ 已删除（内容合并到 `05-trends-2025/`）

> **注意**：`10-november-2025-updates/` 目录已删除，内容已合并到
> `../../05-trends-2025/`。详细内容请参考：
>
> - [`../../05-trends-2025/trends-november-2025.md`](../../05-trends-2025/trends-november-2025.md) -
>   2025 年 11 月趋势（合并自
>   `10-november-2025-updates/01-trends-november-2025.md`）
> - [`../../05-trends-2025/technology-updates.md`](../../05-trends-2025/technology-updates.md) -
>   技术更新（合并自 `10-november-2025-updates/02-technology-updates.md`）
> - [`../../05-trends-2025/best-practices.md`](../../05-trends-2025/best-practices.md) -
>   最佳实践（合并自 `10-november-2025-updates/03-best-practices.md`）
> - [`../../05-trends-2025/README.md`](../../05-trends-2025/README.md) - 趋势文
>   档总览

---

## 2. 相关文档

### 2.1 参考资源

- **`REFERENCES.md`** - 参考标准、框架、工具和资源
- **`ACADEMIC-REFERENCES.md`** - Wikipedia、大学课程、学术论文等学术资源

### 2.2 组合模式文档

- **[组合模式文档集](../08-composition-patterns/README.md)** - 组合模式文档集总
  览
- **[Adapter / Bridge 模式](../08-composition-patterns/01-adapter-bridge.md)** -
  Adapter/Bridge 模式
- **[Facade / Gateway 模式](../08-composition-patterns/02-facade.md)** -
  Facade/Gateway 模式
- **[Pipeline / Orchestration 模式](../08-composition-patterns/03-pipeline.md)** -
  Pipeline/Orchestration 模式
- **[Service Mesh 模式](../08-composition-patterns/04-service-mesh-pattern.md)** -
  Service Mesh 模式
- **[NSM 模式](../08-composition-patterns/05-nsm-pattern.md)** - NSM 模式
- **[Service Aggregation 模式](../08-composition-patterns/05-nsm-pattern.md#service-aggregation)** -
  Service Aggregation 模式（在 NSM 模式文档中）

---

**更新时间**：2025-11-05 **版本**：v1.1（更新引用）
