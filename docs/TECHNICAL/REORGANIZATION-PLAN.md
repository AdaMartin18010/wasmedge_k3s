# TECHNICAL 目录重组方案

**创建日期**：2025-11-08 **版本**：v1.0

## 📊 当前状况

- **目录总数**：33 个
- **组织方式**：按数字编号（00-32）
- **问题**：目录过多，难以快速定位；数字编号不直观

## 🎯 重组目标

1. **按主题分类**：将相关文档归类到同一主题下
2. **减少顶层目录**：从 33 个减少到约 10 个主题目录
3. **保持向后兼容**：通过 README.md 提供旧路径映射
4. **提升可导航性**：清晰的分类便于快速定位

## 📁 新目录结构

```text
TECHNICAL/
├── 01-core-foundations/          # 核心基础
│   ├── docker/
│   ├── kubernetes/
│   └── k3s/
│
├── 02-runtime-policy/            # 运行时与策略
│   ├── wasm-edge/
│   ├── orchestration-runtime/
│   ├── oci-supply-chain/
│   └── policy-opa/
│
├── 03-application-scenarios/     # 应用场景
│   ├── edge-serverless/
│   └── ai-inference/
│
├── 04-infrastructure-stack/      # 基础设施栈
│   ├── network-stack/
│   ├── storage-stack/
│   ├── observability/
│   └── ebpf-stack/
│
├── 05-devops/                     # 开发与运维
│   ├── installation/
│   ├── troubleshooting/
│   ├── gitops-cicd/
│   ├── operator-crd/
│   ├── dev-tools/
│   └── upgrade-migration/
│
├── 06-advanced-features/         # 高级功能
│   ├── service-mesh/
│   ├── multi-cluster/
│   └── image-registry/
│
├── 07-security-compliance/       # 安全与合规
│   └── security-compliance/
│
├── 08-architecture-analysis/     # 架构与分析
│   ├── architecture-framework/
│   ├── isolation-stack/
│   ├── concept-relations-matrix/
│   └── ebpf-otlp-analysis/
│
├── 09-optimization-practices/    # 优化与实践
│   ├── cost-optimization/
│   ├── community-best-practices/
│   └── analysis-improvement/
│
└── 10-reference-trends/          # 参考与趋势
    ├── acronyms-glossary/
    ├── theme-inventory/
    └── 2025-trends/
```

## 🔄 迁移映射表

| 旧路径                         | 新路径                                                |
| ------------------------------ | ----------------------------------------------------- |
| `00-docker/`                   | `01-core-foundations/docker/`                         |
| `01-kubernetes/`               | `01-core-foundations/kubernetes/`                     |
| `02-k3s/`                      | `01-core-foundations/k3s/`                            |
| `03-wasm-edge/`                | `02-runtime-policy/wasm-edge/`                        |
| `04-orchestration-runtime/`    | `02-runtime-policy/orchestration-runtime/`            |
| `05-oci-supply-chain/`         | `02-runtime-policy/oci-supply-chain/`                 |
| `06-policy-opa/`               | `02-runtime-policy/policy-opa/`                       |
| `07-edge-serverless/`          | `03-application-scenarios/edge-serverless/`           |
| `08-ai-inference/`             | `03-application-scenarios/ai-inference/`              |
| `09-security-compliance/`      | `07-security-compliance/security-compliance/`         |
| `10-installation/`             | `05-devops/installation/`                             |
| `11-troubleshooting/`          | `05-devops/troubleshooting/`                          |
| `12-network-stack/`            | `04-infrastructure-stack/network-stack/`              |
| `13-acronyms-glossary/`        | `10-reference-trends/acronyms-glossary/`              |
| `14-theme-inventory/`          | `10-reference-trends/theme-inventory/`                |
| `15-storage-stack/`            | `04-infrastructure-stack/storage-stack/`              |
| `16-observability/`            | `04-infrastructure-stack/observability/`              |
| `17-gitops-cicd/`              | `05-devops/gitops-cicd/`                              |
| `18-operator-crd/`             | `05-devops/operator-crd/`                             |
| `19-service-mesh/`             | `06-advanced-features/service-mesh/`                  |
| `20-multi-cluster/`            | `06-advanced-features/multi-cluster/`                 |
| `21-image-registry/`           | `06-advanced-features/image-registry/`                |
| `22-upgrade-migration/`        | `05-devops/upgrade-migration/`                        |
| `23-dev-tools/`                | `05-devops/dev-tools/`                                |
| `24-cost-optimization/`        | `09-optimization-practices/cost-optimization/`        |
| `25-community-best-practices/` | `09-optimization-practices/community-best-practices/` |
| `26-analysis-improvement/`     | `09-optimization-practices/analysis-improvement/`     |
| `27-2025-trends/`              | `10-reference-trends/2025-trends/`                    |
| `28-architecture-framework/`   | `08-architecture-analysis/architecture-framework/`    |
| `29-isolation-stack/`          | `08-architecture-analysis/isolation-stack/`           |
| `30-concept-relations-matrix/` | `08-architecture-analysis/concept-relations-matrix/`  |
| `31-ebpf-stack/`               | `04-infrastructure-stack/ebpf-stack/`                 |
| `32-ebpf-otlp-analysis/`       | `08-architecture-analysis/ebpf-otlp-analysis/`        |

## ✅ 实施步骤

1. ✅ 创建新的目录结构
2. ✅ 移动文件到新位置
3. ✅ 更新所有文档中的路径引用（34 个文件）
4. ✅ 更新 README.md
5. ✅ 创建路径映射文档（向后兼容）
6. ✅ 验证所有链接

---

**状态**：✅ 已完成（2025-11-08）

## 📊 完成统计

- **目录重组**：从 33 个数字编号目录 → 10 个主题分类目录
- **文件组织**：84 个 Markdown 文件已组织到新位置
- **路径更新**：34 个文件已更新路径引用
  - 核心导航文档：11 个
  - 实现细节文档：22 个
  - 索引文档：1 个
- **支持文档**：
  - `PATH-MAPPING.md` - 路径映射表（向后兼容）
  - `README.md` - 技术参考文档说明（已更新）
- **验证结果**：
  - ✅ 所有实际链接引用已更新（0 个遗漏）
  - ✅ 无 linter 错误
  - ✅ 文档完整性验证通过
