# 架构视图文档索引

## 📚 文档导航

本文档集基于 `architecture_view.md` 的核心思想，从**软件架构的视角**系统梳理现代
云原生架构技术。

### 🎯 快速导航

- **入门路径**：从 [多视角架构视图](01-views/) 开始
- **深入路径**：进入 [分层架构模型](02-layers/) 和 [组合模式](03-composition/)
- **实践路径**：查看 [案例研究](07-case-studies/)，学习实际案例
- **理论路径**：研读 [形式化理论](06-formalization/)，理解数学基础
- **趋势路径**：了解 [2025 年技术趋势](05-trends-2025/)，把握最新动态

## 📋 文档结构

### 1. 多视角架构视图 (`01-views/`)

从不同视角理解架构：

- [架构拆解与组合](01-views/decomposition-composition.md) - 5 步拆分与组合流程
- [虚拟化视角](01-views/virtualization-view.md) - 虚拟化的"剪裁"作用
- [容器化视角](01-views/containerization-view.md) - 容器化的抽象层次
- [沙盒化视角](01-views/sandboxing-view.md) - 沙盒化的安全模型
- [Service Mesh 视角](01-views/service-mesh-view.md) - 网络服务的聚合与组合
- [Network Service Mesh 视角](01-views/network-service-mesh-view.md) - 跨域网络
  服务的聚合与组合
- [OPA 策略治理视角](01-views/opa-policy-governance-view.md) - 策略即代码的治理
  范式
- [动态运维视角](01-views/dynamic-operations-view.md) -
  GitOps、Observability、Autoscaling

### 2. 分层架构模型 (`02-layers/`)

从硬件到业务的分层抽象：

- [分层架构模型](02-layers/layer-model.md) - 整体分层模型
- [硬件/固件层](02-layers/hardware-firmware-layer.md) - CPU、内存、I/O、可信根
- [Hypervisor/Kernel 层](02-layers/hypervisor-kernel-layer.md) - VM 与容器的资源
  调度
- [容器运行时层](02-layers/runtime-container-layer.md) - 进程隔离、镜像运行
- [沙盒层](02-layers/sandbox-layer.md) - 系统调用过滤、文件系统隔离
- [Service Mesh 层](02-layers/service-mesh-layer.md) - 代理、流量治理、监控
- [应用层](02-layers/application-layer.md) - 业务逻辑、数据访问

### 3. 组合模式与实践 (`03-composition/`)

架构组合的核心模式：

- [组合模式与实践](03-composition/composition-patterns.md) - 组合模式分类
- [Adapter / Bridge 模式](03-composition/adapter-bridge-pattern.md) - 跨技术边界
- [Facade / API Gateway 模式](03-composition/facade-gateway-pattern.md) - 聚合多
  服务
- [Pipeline / Orchestration](03-composition/pipeline-orchestration.md) - 流程编
  排
- Service Mesh - 通讯治理
- Observability - 监控与追踪

### 4. 架构模式与设计 (`04-patterns/`)

常见的架构模式：

- [Composition Root](04-patterns/composition-root.md) - 全局依赖注入
- [Service Mesh Patterns](04-patterns/service-mesh-patterns.md) - 流量治理模式
- [NSM Patterns](04-patterns/nsm-patterns.md) - 网络服务聚合模式
- [OPA Patterns](04-patterns/opa-patterns.md) - 策略即代码模式
- [GitOps Patterns](04-patterns/gitops-patterns.md) - 持续交付模式

### 5. 2025 年技术趋势 (`05-trends-2025/`)

最新的技术动态：

- [2025 年 11 月架构技术更新](05-trends-2025/november-2025-architecture-updates.md) -
  最新架构技术更新
- [2025 年 11 月综合趋势报告](05-trends-2025/comprehensive-trends-november-2025.md) -
  综合技术趋势分析
- [2025 年 11 月技术趋势](05-trends-2025/november-2025-updates.md) - 最新技术更
  新
- 虚拟化趋势 - 轻量级虚拟机、机密计算
- 容器化趋势 - 轻量级运行时、eBPF 增强
- Service Mesh 趋势 - 轻量化、边缘计算
- OPA 趋势 - 策略即代码、安全合规

### 6. 形式化理论 (`06-formalization/`)

数学基础与理论：

- [多视角对比矩阵](06-formalization/comparison-matrix.md) - 技术对比矩阵
- [归纳证明](06-formalization/induction-proof.md) - 虚拟化-容器化-沙盒化的形式化
  论证
- [范畴论视角](06-formalization/category-theory.md) - 架构组合的形式化（对象、态
  射、函子）
- [状态空间压缩](06-formalization/state-space-compression.md) - 状态空间压缩比和
  形式化证明
- 函数式组合 - 组合函数、高阶函数

### 8. 概念属性关系 (`08-concepts-relations/`)

概念、属性、关系的系统梳理：

- [概念属性关系矩阵](08-concepts-relations/concept-properties-matrix.md) - 概念
  定义、属性矩阵、关系图谱
- [概念定义](08-concepts-relations/concept-definitions.md) - 核心概念定义
- [属性关系](08-concepts-relations/property-relations.md) - 属性矩阵和关系
- [关系图谱](08-concepts-relations/relationship-graph.md) - 技术关系图谱

### 9. 2025 年 11 月特别文档 (`09-november-2025-special/`)

基于 `architecture_view.md` 的专题文档集：

- [专题文档集](09-november-2025-special/README.md) - 专题文档总览
- [核心主题深化](09-november-2025-special/01-core-themes/) - 架构拆解与组合的完
  整流程
- [形式化论证](09-november-2025-special/02-formal-proofs/) - 虚拟化-容器化-沙盒
  化的完整归纳证明
- [概念属性关系](09-november-2025-special/03-concepts-relations/) - 概念属性关系
  完整矩阵
- [实证分析](09-november-2025-special/04-empirical-analysis/) - 生产环境数据实证
  分析
- [技术演进路径](09-november-2025-special/05-evolution-path/) - 从裸机到云原生的
  技术演进

### 10. 形式化证明 (`10-formal-proofs/`)

形式化证明文档：

- [README](10-formal-proofs/README.md) - 形式化证明说明
- **详细文档**：参见 `architecture-view/05-formal-proofs/` - 完整的形式化证明文
  档集

### 11. 拓展应用 (`11-extensions/`)

拓展应用场景文档：

- [README](11-extensions/README.md) - 拓展应用说明
- **详细文档**：参见
  `architecture-view/06-concepts-properties-relations/04-extensions.md` - 拓展场
  景详细文档

### 架构视图文档集 (`architecture-view/`)

完整的架构视图文档集（**推荐使用**）：

- [README](architecture-view/README.md) - 文档集说明
- [INDEX](architecture-view/INDEX.md) - 文档索引
- [SUMMARY](architecture-view/SUMMARY.md) - 文档总结

**包含 10 个主要目录，53 个详细文档，涵盖所有核心主题**。

## 🔗 相关文档

### 源文档

- **`architecture_view.md`** - 架构视角的核心论述

### 技术文档

- **`docs/TECHNICAL/`** - 技术实现细节
  - [Docker](TECHNICAL/00-docker/docker.md)
  - [Kubernetes](TECHNICAL/01-kubernetes/kubernetes.md)
  - [K3s](TECHNICAL/02-k3s/k3s.md)
  - [WasmEdge](TECHNICAL/03-wasm-edge/wasmedge.md)
  - [Service Mesh](TECHNICAL/19-service-mesh/service-mesh.md)
  - [OPA](TECHNICAL/06-policy-opa/policy-opa.md)

### 认知模型

- **`docs/COGNITIVE/`** - 认知框架和理论模型
  - [知识图谱](COGNITIVE/00-knowledge-map/knowledge-map.md)
  - [概览](COGNITIVE/01-overview/overview.md)
  - [原则](COGNITIVE/02-principles/principles.md)
  - [形式化理论](COGNITIVE/07-formal-theory/formal-theory.md)
  - [范畴论](COGNITIVE/08-category-theory/category-theory.md)

## 📖 阅读建议

### 初学者

1. 阅读 [架构拆解与组合](01-views/decomposition-composition.md)
2. 了解 [分层架构模型](02-layers/layer-model.md)
3. 查看 [支付网关案例](07-case-studies/payment-gateway.md)

### 进阶者

1. 深入 [组合模式与实践](03-composition/composition-patterns.md)
2. 研究 [形式化理论](06-formalization/comparison-matrix.md)
3. 跟踪 [2025 年技术趋势](05-trends-2025/november-2025-updates.md)

### 实践者

1. 参考 [案例研究](07-case-studies/)
2. 应用 [组合模式](03-composition/)
3. 优化 [分层架构](02-layers/)

## 🎯 核心主题

### 1. 架构拆解与组合

- **拆解**：把复杂系统拆成可维护、可替换的"模块"
- **组合**：用成熟的组合模式把子结构"拼接"成最终应用
- **验证**：通过 ADR、C4、CI/CD 证明组合后仍满足需求

### 2. 虚拟化 → 容器化 → 沙盒化

- **虚拟化**：把硬件抽象为 VM 资源池
- **容器化**：把 OS 抽象为轻量容器
- **沙盒化**：把容器内进程抽象为安全进程

### 3. Service Mesh / Network Service Mesh

- **节点聚合**：从物理地址到身份-驱动拓扑
- **服务组合**：从跨服务流到可编排的本地函数
- **架构范式重塑**：从"分层图"到"过滤器图"

### 4. OPA (Open Policy Agent)

- **策略即代码**：把安全策略写成 Rego
- **统一决策**：在每层统一施行安全策略
- **版本治理**：策略与代码同步版本管理

### 5. 动态运维

- **GitOps**：代码与基础设施同步
- **Observability**：统一监控、日志、追踪
- **Autoscaling**：自动扩缩容

## 📝 更新记录

- **2025-11-04**：初始版本，基于 `architecture_view.md` 创建文档结构

---

**维护者**：基于 `architecture_view.md` 内容扩展 **许可证**：与项目保持一致
