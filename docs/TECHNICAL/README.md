# 技术参考文档

## 📖 文档简介

本目录包含**技术参考文档**，提供详细的技术规格、接口定义和实践指南，作为认知模型
的技术支撑。

## 🎯 文档定位

**核心特征**：

- 📝 **技术细节**：包含完整的技术规范、API 定义、配置选项
- 🔧 **实践指导**：提供 YAML 示例、命令、故障排查步骤
- ✅ **最佳实践**：总结生产环境的最佳实践和注意事项
- 🚀 **可操作性**：读者可以直接按照文档实施

## 📚 文档列表

### 容器与编排

| 文档       | 路径             | 核心内容              |
| ---------- | ---------------- | --------------------- |
| Docker     | `00-docker/`     | Docker 技术规范       |
| Kubernetes | `01-kubernetes/` | Kubernetes 架构与实践 |
| K3s        | `02-k3s/`        | K3s 轻量级架构        |

### 运行时与策略

| 文档           | 路径                        | 核心内容             |
| -------------- | --------------------------- | -------------------- |
| WasmEdge       | `03-wasm-edge/`             | WasmEdge 集成指南    |
| 编排运行时     | `04-orchestration-runtime/` | CRI 和 RuntimeClass  |
| OCI 供应链     | `05-oci-supply-chain/`      | OCI 标准和供应链安全 |
| OPA 策略即代码 | `06-policy-opa/`            | Open Policy Agent    |

### 应用场景

| 文档            | 路径                  | 核心内容              |
| --------------- | --------------------- | --------------------- |
| 边缘 Serverless | `07-edge-serverless/` | 边缘计算和 Serverless |
| AI 推理         | `08-ai-inference/`    | AI 推理应用           |

### 实践指南

| 文档     | 路径                      | 核心内容           |
| -------- | ------------------------- | ------------------ |
| 安全合规 | `09-security-compliance/` | 安全与合规最佳实践 |
| 安装部署 | `10-installation/`        | 安装和最小示例     |
| 故障排查 | `11-troubleshooting/`     | 常见问题解决方案   |

### 技术规格堆栈

| 文档               | 路径                           | 核心内容                   |
| ------------------ | ------------------------------ | -------------------------- |
| 网络技术规格       | `12-network-stack/`            | CNI、Service、Ingress      |
| 缩写词汇表         | `13-acronyms-glossary/`        | 所有缩写词定义与关系       |
| 主题清单           | `14-theme-inventory/`          | 全面梳理所有主题与子主题   |
| 存储技术规格       | `15-storage-stack/`            | CSI、PV/PVC                |
| 监控与可观测性     | `16-observability/`            | Metrics、Logging、Tracing  |
| GitOps 和持续交付  | `17-gitops-cicd/`              | GitOps/CI/CD 技术规范      |
| Operator 和 CRD    | `18-operator-crd/`             | Operator/CRD 开发规范      |
| 服务网格           | `19-service-mesh/`             | 服务网格技术规范（可选）   |
| 多集群管理         | `20-multi-cluster/`            | 多集群管理技术规范（可选） |
| 镜像仓库和镜像管理 | `21-image-registry/`           | 镜像仓库与管理技术规范     |
| 升级和迁移         | `22-upgrade-migration/`        | 升级和迁移技术规范         |
| 开发和调试工具     | `23-dev-tools/`                | 开发和调试工具规范         |
| 成本优化           | `24-cost-optimization/`        | 成本优化技术规范（可选）   |
| 社区生态和最佳实践 | `25-community-best-practices/` | 社区生态和最佳实践（可选） |
| 分析改进           | `26-analysis-improvement/`     | 分析改进文档               |
| 2025 趋势          | `27-2025-trends/`              | 2025 技术趋势              |

## 🚀 快速开始

### 新手入门路径

1. **[Docker](00-docker/docker.md)** - 掌握容器技术基础
2. **[Kubernetes](01-kubernetes/kubernetes.md)** - 深入学习容器编排
3. **[安装部署](10-installation/installation.md)** - 快速上手各技术

### 进阶学习路径

1. **[K3s](02-k3s/k3s.md)** - 了解轻量级 Kubernetes
2. **[WasmEdge](03-wasm-edge/wasmedge.md)** - 探索字节码运行时
3. **[OPA 策略即代码](06-policy-opa/policy-opa.md)** - 掌握策略管理

### 实践应用路径

1. **[故障排查](11-troubleshooting/troubleshooting.md)** - 解决常见问题
2. **[安全合规](09-security-compliance/security-compliance.md)** - 安全最佳实践
3. **[GitOps 和持续交付](17-gitops-cicd/gitops-cicd.md)** - 实现自动化部署

### 技术规格深入

1. **[网络技术规格](12-network-stack/network-stack.md)** - CNI、Service、Ingress
2. **[存储技术规格](15-storage-stack/storage-stack.md)** - CSI、PV/PVC
3. **[监控与可观测性](16-observability/observability.md)** -
   Metrics、Logging、Tracing

## 📖 使用场景

### ✅ 适用场景

- ✅ 深入学习特定技术
- ✅ 实施技术方案
- ✅ 故障排查和性能优化
- ✅ 需要"怎么做"的具体指导

### 🔗 与其他文档的关系

- **技术参考文档**提供 **"怎么做"**（How）和 **"具体细节"**（Details）
- **认知模型文档**（`../COGNITIVE/`）提供 **"为什么"**（Why）和 **"是什么
  "**（What）

## 🎯 按角色选择文档

### 开发者

- [00. Docker](00-docker/docker.md)
- [01. Kubernetes](01-kubernetes/kubernetes.md)
- [02. K3s](02-k3s/k3s.md)
- [03. WasmEdge](03-wasm-edge/wasmedge.md)
- [18. Operator 和 CRD](18-operator-crd/operator-crd.md)

### 运维工程师

- [10. 安装部署](10-installation/installation.md)
- [11. 故障排查](11-troubleshooting/troubleshooting.md)
- [16. 监控与可观测性](16-observability/observability.md)
- [17. GitOps 和持续交付](17-gitops-cicd/gitops-cicd.md)
- [22. 升级和迁移](22-upgrade-migration/upgrade-migration.md)

### DevOps 工程师

- [17. GitOps 和持续交付](17-gitops-cicd/gitops-cicd.md)
- [21. 镜像仓库和镜像管理](21-image-registry/image-registry.md)
- [05. OCI 供应链](05-oci-supply-chain/oci-supply-chain.md)
- [06. OPA 策略即代码](06-policy-opa/policy-opa.md)

## 📊 文档统计

- **总文档数**：25 个核心技术参考文档
- **覆盖范围**：容器编排、运行时、策略、实践指南、技术规格
- **文档类型**：技术参考文档

---

**最后更新**：2025-11-01 **维护者**：项目团队 **参
考**：[文档类型说明](../META/DOCUMENT-TYPES.md)
