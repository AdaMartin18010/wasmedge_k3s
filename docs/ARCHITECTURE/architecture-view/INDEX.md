# 软件架构视角文档索引

## 目录

- [目录](#目录)
- [📋 文档索引](#-文档索引)
  - [1. 架构拆解与组合 (`01-decomposition-composition/`)](#1-架构拆解与组合-01-decomposition-composition)
  - [2. 虚拟化容器化沙盒化 (`02-virtualization-containerization-sandboxing/`)](#2-虚拟化容器化沙盒化-02-virtualization-containerization-sandboxing)
  - [3. 服务网格与网络服务网格 (`03-service-mesh-nsm/`)](#3-服务网格与网络服务网格-03-service-mesh-nsm)
  - [4. OPA 策略治理 (`04-opa-policy-governance/`)](#4-opa-策略治理-04-opa-policy-governance)
  - [5. 形式化论证 (`05-formal-proofs/`)](#5-形式化论证-05-formal-proofs)
  - [6. 概念属性关系 (`06-concepts-properties-relations/`)](#6-概念属性关系-06-concepts-properties-relations)
  - [7. 动态运维 (`07-dynamic-operations/`)](#7-动态运维-07-dynamic-operations)
  - [8. 组合模式 (`08-composition-patterns/`)](#8-组合模式-08-composition-patterns)
  - [9. 多视角分析 (`09-multi-perspectives/`)](#9-多视角分析-09-multi-perspectives)
  - [10. 2025 年 11 月更新 (`10-november-2025-updates/`)](#10-2025-年-11-月更新-10-november-2025-updates)

---

## 📋 文档索引

### 1. 架构拆解与组合 (`01-decomposition-composition/`)

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

### 2. 虚拟化容器化沙盒化 (`02-virtualization-containerization-sandboxing/`)

- [01. 虚拟化抽象](02-virtualization-containerization-sandboxing/01-virtualization-abstraction.md)

  - VM 资源池抽象
  - Hypervisor 层
  - 资源隔离与调度

- [02. 容器化抽象](02-virtualization-containerization-sandboxing/02-containerization-abstraction.md)

  - 轻量容器抽象
  - 运行时环境
  - 镜像管理

- [03. 沙盒化抽象](02-virtualization-containerization-sandboxing/03-sandboxing-abstraction.md)

  - 系统调用过滤
  - 文件系统隔离
  - 最小权限模型

- [04. 递进抽象论证](02-virtualization-containerization-sandboxing/04-progressive-abstraction.md)

  - 三层抽象的形式化
  - 状态空间压缩证明
  - 动态性论证

- [05. 矩阵对比](02-virtualization-containerization-sandboxing/05-comparison-matrix.md)
  - 隔离级别对比
  - 资源开销对比
  - 启动时间对比
  - 安全模型对比

### 3. 服务网格与网络服务网格 (`03-service-mesh-nsm/`)

- [01. 节点聚合](03-service-mesh-nsm/01-node-aggregation.md)

  - 从"物理地址"到"身份-驱动拓扑"
  - 拓扑动态生成
  - 负载均衡算法

- [02. 服务组合](03-service-mesh-nsm/02-service-composition.md)

  - 从"跨服务流"到"可编排的本地函数"
  - Filter Chain
  - 灰度发布

- [03. 范式重塑](03-service-mesh-nsm/03-paradigm-reshaping.md)

  - "先定接口，再定部署" → "先定流量，再定接口"
  - "分层图" → "过滤器图"
  - 非功能性从"后期治理"变为"设计期可组合元素"

- [04. NSM 架构](03-service-mesh-nsm/04-nsm-architecture.md)

  - vL3 / vWire
  - Client / Endpoint
  - 多集群 Federation

- [05. 典型用例](03-service-mesh-nsm/05-use-cases.md)
  - 混合云
  - 多租户 SaaS
  - 边缘计算
  - 混合身份

### 4. OPA 策略治理 (`04-opa-policy-governance/`)

- [01. OPA 在中层模型中的定位](04-opa-policy-governance/01-opa-in-middle-layer.md)

  - ℳ = ⟨U, G, P⟩
  - OPA 负责 security 策略
  - 从"人读基线"到"机读可验证约束"

- [02. 安全形式化](04-opa-policy-governance/02-formalization.md)

  - 能力闭包（A5）
  - 最小权限（A6）
  - 可证明性（A7）
  - 版本一致性（A8）

- [03. 能力闭包](04-opa-policy-governance/03-capability-closure.md)

  - gVisor + OPA
  - 双层闸门
  - 编译期 + 运行期

- [04. 服务间权限](04-opa-policy-governance/04-service-permissions.md)

  - Service Mesh + OPA
  - SPIFFE ID
  - Rego 策略

- [05. OPA 体系结构](04-opa-policy-governance/05-opa-architecture.md)
  - PDP / PEP / OCP
  - Bundle
  - Decision Log

### 5. 形式化论证 (`05-formal-proofs/`)

- [01. 公理层](05-formal-proofs/01-axioms.md)

  - A1: 冯·诺依曼等价
  - A2: OS 资源封闭
  - A3: 网络异步交付
  - A4: 分层可抽象

- [02. 归纳证明](05-formal-proofs/02-induction-proof.md)

  - 基础归纳步（n=0）
  - 第一次归纳映射（Ψ₁）
  - 第二次归纳映射（Ψ₂）
  - 第三次归纳映射（Ψ₃）
  - 网络抽象归纳（Ψ₄）

- [03. 范畴论视角](05-formal-proofs/03-category-theory.md)

  - 对象/算子集合
  - 函子与态射
  - 组合运算
  - 同态映射

- [04. 状态空间压缩](05-formal-proofs/04-state-space-compression.md)

  - 状态压缩比
  - 状态向量定义
  - 差分进化

- [05. 封闭证明](05-formal-proofs/05-closure-proof.md)
  - 待证命题 P(n)
  - 基础步
  - 归纳步
  - 结论

### 6. 概念属性关系 (`06-concepts-properties-relations/`)

- [01. 概念定义](06-concepts-properties-relations/01-concept-definitions.md)

  - VM / Container / Sandbox
  - Service Mesh / NSM
  - OPA / Policy

- [02. 属性矩阵](06-concepts-properties-relations/02-property-matrix.md)

  - 隔离级别
  - 资源开销
  - 启动时间
  - 安全模型

- [03. 关系图](06-concepts-properties-relations/03-relationship-graph.md)

  - 虚拟化 ⊃ 容器化
  - 容器化 ⊃ 沙盒化
  - 沙盒化 ↔ 服务网格
  - 服务网格 ↔ NSM

- [04. 拓展](06-concepts-properties-relations/04-extensions.md)

  - 边缘计算
  - 无服务器
  - AI 推理
  - 多租户

- [05. 形式化映射](06-concepts-properties-relations/05-formal-mapping.md)
  - 对象 → 范畴
  - 算子 → 函子
  - 组合 → 态射
  - 同态 → 性能/安全/观测

### 7. 动态运维 (`07-dynamic-operations/`)

- [01. GitOps](07-dynamic-operations/01-gitops.md)

  - ArgoCD
  - Flux
  - Git 仓库即真相源

- [02. 可观测性](07-dynamic-operations/02-observability.md)

  - OpenTelemetry
  - Prometheus
  - Tempo / Jaeger
  - Grafana

- [03. 弹性伸缩](07-dynamic-operations/03-autoscaling.md)

  - HPA
  - VPA
  - Knative
  - Argo Rollouts

- [04. CI/CD](07-dynamic-operations/04-ci-cd.md)

  - GitHub Actions
  - Jenkins
  - Tekton
  - 自动化构建测试部署

- [05. 混沌工程](07-dynamic-operations/05-chaos-engineering.md)
  - Chaos Monkey
  - Litmus
  - 故障注入
  - 可靠性测试

### 8. 组合模式 (`08-composition-patterns/`)

- [01. 适配器/桥接](08-composition-patterns/01-adapter-bridge.md)

  - gRPC ↔ REST
  - Docker ↔ K8s
  - 跨技术边界

- [02. Facade 模式](08-composition-patterns/02-facade.md)

  - 统一接口
  - 隐藏复杂性
  - 简化客户端使用

- [03. Pipeline 模式](08-composition-patterns/03-pipeline.md)

  - 顺序执行
  - 数据流
  - 独立处理

- [04. Service Mesh 模式](08-composition-patterns/04-service-mesh-pattern.md)

  - Sidecar
  - Control Plane
  - Data Plane

- [05. NSM 模式](08-composition-patterns/05-nsm-pattern.md)
  - Sidecar
  - Control Plane
  - Data Plane

### 9. 多视角分析 (`09-multi-perspectives/`)

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

### 10. 2025 年 11 月更新 (`10-november-2025-updates/`)

- [01. 2025 年 11 月趋势](10-november-2025-updates/01-trends-november-2025.md)

  - 虚拟化趋势
  - 容器化趋势
  - 服务网格趋势
  - 策略治理趋势

- [02. 技术更新](10-november-2025-updates/02-technology-updates.md)

  - 技术动态
  - 技术趋势
  - 技术选择建议

- [03. 最佳实践](10-november-2025-updates/03-best-practices.md)
  - 虚拟化最佳实践
  - 容器化最佳实践
  - 沙盒化最佳实践
  - Service Mesh 最佳实践
  - OPA 最佳实践
  - 动态运维最佳实践

---

**更新时间**：2025-11-04 **版本**：v1.0
