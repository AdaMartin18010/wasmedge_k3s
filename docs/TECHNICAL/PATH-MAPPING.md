# TECHNICAL 目录路径映射表

## 📑 目录

- [TECHNICAL 目录路径映射表](#technical-目录路径映射表)
  - [📑 目录](#-目录)
  - [📋 路径映射表](#-路径映射表)
    - [核心基础（Core Foundations）](#核心基础core-foundations)
    - [运行时与策略（Runtime \& Policy）](#运行时与策略runtime--policy)
    - [应用场景（Application Scenarios）](#应用场景application-scenarios)
    - [基础设施栈（Infrastructure Stack）](#基础设施栈infrastructure-stack)
    - [开发与运维（DevOps）](#开发与运维devops)
    - [高级功能（Advanced Features）](#高级功能advanced-features)
    - [安全与合规（Security \& Compliance）](#安全与合规security--compliance)
    - [架构与分析（Architecture \& Analysis）](#架构与分析architecture--analysis)
    - [优化与实践（Optimization \& Practices）](#优化与实践optimization--practices)
    - [参考与趋势（Reference \& Trends）](#参考与趋势reference--trends)
  - [🔍 快速查找](#-快速查找)
    - [按主题查找](#按主题查找)
  - [📝 使用说明](#-使用说明)

---

**创建日期**：2025-11-08 **版本**：v1.0

> ⚠️ **向后兼容性说明**：本文档提供旧路径到新路径的映射，帮助查找已迁移的文档。

## 📋 路径映射表

### 核心基础（Core Foundations）

| 旧路径           | 新路径                            |
| ---------------- | --------------------------------- |
| `00-docker/`     | `01-core-foundations/docker/`     |
| `01-kubernetes/` | `01-core-foundations/kubernetes/` |
| `02-k3s/`        | `01-core-foundations/k3s/`        |

### 运行时与策略（Runtime & Policy）

| 旧路径                      | 新路径                                     |
| --------------------------- | ------------------------------------------ |
| `03-wasm-edge/`             | `02-runtime-policy/wasm-edge/`             |
| `04-orchestration-runtime/` | `02-runtime-policy/orchestration-runtime/` |
| `05-oci-supply-chain/`      | `02-runtime-policy/oci-supply-chain/`      |
| `06-policy-opa/`            | `02-runtime-policy/policy-opa/`            |

### 应用场景（Application Scenarios）

| 旧路径                | 新路径                                      |
| --------------------- | ------------------------------------------- |
| `07-edge-serverless/` | `03-application-scenarios/edge-serverless/` |
| `08-ai-inference/`    | `03-application-scenarios/ai-inference/`    |

### 基础设施栈（Infrastructure Stack）

| 旧路径              | 新路径                                   |
| ------------------- | ---------------------------------------- |
| `12-network-stack/` | `04-infrastructure-stack/network-stack/` |
| `15-storage-stack/` | `04-infrastructure-stack/storage-stack/` |
| `16-observability/` | `04-infrastructure-stack/observability/` |
| `31-ebpf-stack/`    | `04-infrastructure-stack/ebpf-stack/`    |

### 开发与运维（DevOps）

| 旧路径                  | 新路径                         |
| ----------------------- | ------------------------------ |
| `10-installation/`      | `05-devops/installation/`      |
| `11-troubleshooting/`   | `05-devops/troubleshooting/`   |
| `17-gitops-cicd/`       | `05-devops/gitops-cicd/`       |
| `18-operator-crd/`      | `05-devops/operator-crd/`      |
| `22-upgrade-migration/` | `05-devops/upgrade-migration/` |
| `23-dev-tools/`         | `05-devops/dev-tools/`         |

### 高级功能（Advanced Features）

| 旧路径               | 新路径                                 |
| -------------------- | -------------------------------------- |
| `19-service-mesh/`   | `06-advanced-features/service-mesh/`   |
| `20-multi-cluster/`  | `06-advanced-features/multi-cluster/`  |
| `21-image-registry/` | `06-advanced-features/image-registry/` |

### 安全与合规（Security & Compliance）

| 旧路径                    | 新路径                                        |
| ------------------------- | --------------------------------------------- |
| `09-security-compliance/` | `07-security-compliance/security-compliance/` |

### 架构与分析（Architecture & Analysis）

| 旧路径                         | 新路径                                               |
| ------------------------------ | ---------------------------------------------------- |
| `28-architecture-framework/`   | `08-architecture-analysis/architecture-framework/`   |
| `29-isolation-stack/`          | `08-architecture-analysis/isolation-stack/`          |
| `30-concept-relations-matrix/` | `08-architecture-analysis/concept-relations-matrix/` |
| `32-ebpf-otlp-analysis/`       | `08-architecture-analysis/ebpf-otlp-analysis/`       |

### 优化与实践（Optimization & Practices）

| 旧路径                         | 新路径                                                |
| ------------------------------ | ----------------------------------------------------- |
| `24-cost-optimization/`        | `09-optimization-practices/cost-optimization/`        |
| `25-community-best-practices/` | `09-optimization-practices/community-best-practices/` |
| `26-analysis-improvement/`     | `09-optimization-practices/analysis-improvement/`     |

### 参考与趋势（Reference & Trends）

| 旧路径                  | 新路径                                   |
| ----------------------- | ---------------------------------------- |
| `13-acronyms-glossary/` | `10-reference-trends/acronyms-glossary/` |
| `14-theme-inventory/`   | `10-reference-trends/theme-inventory/`   |
| `27-2025-trends/`       | `10-reference-trends/2025-trends/`       |

## 🔍 快速查找

### 按主题查找

- **核心基础**：`01-core-foundations/`
- **运行时与策略**：`02-runtime-policy/`
- **应用场景**：`03-application-scenarios/`
- **基础设施栈**：`04-infrastructure-stack/`
- **开发与运维**：`05-devops/`
- **高级功能**：`06-advanced-features/`
- **安全与合规**：`07-security-compliance/`
- **架构与分析**：`08-architecture-analysis/`
- **优化与实践**：`09-optimization-practices/`
- **参考与趋势**：`10-reference-trends/`

## 📝 使用说明

1. 如果遇到旧路径引用，请使用本映射表查找新路径
2. 建议更新所有文档中的路径引用为新路径
3. 新文档请使用新路径结构

---

**最后更新**：2025-11-08 **维护者**：项目团队
