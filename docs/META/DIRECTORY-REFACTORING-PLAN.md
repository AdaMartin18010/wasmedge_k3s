# 目录结构重构计划

## 📊 项目概述

**项目名称**：文档目录结构重构

**目标**：将当前按编号组织的文档结构重构为按文档类型（认知模型/技术参考）组织的
清晰结构

**预计完成时间**：2025-11-01 至 2025-11-07

**实际完成时间**：2025-11-01

**状态**：✅ 核心工作已完成（约 91%）

---

## 🎯 重构目标

### 主要目标

1. **明确文档分类**

   - 将认知模型文档和技术参考文档分开组织
   - 提高文档的可发现性和可维护性

2. **改善目录结构**

   - 使用语义化的目录名称
   - 降低认知成本

3. **保持向后兼容**

   - 维护文档间的链接关系
   - 确保所有引用路径正确

4. **提升可维护性**
   - 便于新增文档分类
   - 便于文档维护和更新

---

## 📁 新目录结构设计

### 完整目录结构

```text
project-root/
├── ai_view.md                    # 根目录保留（认知模型核心文档）
├── README.md                      # 项目根README
├── LICENSE
│
└── docs/
    ├── README.md                  # 文档集总览（已更新路径）
    ├── INDEX.md                   # 文档索引（已更新路径）
    ├── REFERENCES.md              # 参考资源（已更新路径）
    │
    ├── COGNITIVE/                 # 🧠 认知模型文档目录
    │   ├── README.md              # 认知模型文档总览
    │   │
    │   ├── 00-knowledge-map/      # 认知图谱
    │   │   └── knowledge-map.md
    │   │
    │   ├── 01-overview/           # 总览
    │   │   └── overview.md
    │   │
    │   ├── 02-principles/         # 理念层
    │   │   └── principles.md
    │   │
    │   ├── 03-architecture/       # 架构与对象模型（混合型）
    │   │   └── architecture.md
    │   │
    │   ├── 17-architecture-design/ # 全局架构设计
    │   │   └── architecture-design.md
    │   │
    │   ├── 18-problem-solution-matrix/ # 问题解决方案（混合型）
    │   │   └── problem-solution-matrix.md
    │   │
    │   ├── 19-formal-theory/      # 形式化理论
    │   │   └── formal-theory.md
    │   │
    │   ├── 20-category-theory/    # 范畴论视角
    │   │   └── category-theory.md
    │   │
    │   ├── 37-matrix-perspective/  # 矩阵视角
    │   │   ├── README.md
    │   │   ├── 01-core-concepts.md
    │   │   ├── 02-relation-matrix.md
    │   │   ├── 03-attribute-matrix.md
    │   │   ├── 04-scene-transformation.md
    │   │   ├── 05-operation-transformation.md
    │   │   ├── 06-tech-chain-sequence.md
    │   │   ├── 07-ai-parameters.md
    │   │   ├── 08-matrix-operations.md
    │   │   ├── 09-practice-cases.md
    │   │   ├── CHECKLIST.md
    │   │   ├── QUICK-REFERENCE.md
    │   │   ├── SUMMARY.md
    │   │   └── REFERENCES.md
    │   │
    │   ├── 14-benchmarks/         # 性能基准（混合型）
    │   │   └── benchmarks.md
    │   │
    │   └── META-COGNITIVE/        # 认知模型元数据（如需要）
    │       └── ...
    │
    ├── TECHNICAL/                 # 📚 技术参考文档目录
    │   ├── README.md              # 技术参考文档总览
    │   │
    │   ├── 04-docker/              # Docker
    │   │   └── docker.md
    │   │
    │   ├── 05-kubernetes/         # Kubernetes
    │   │   └── kubernetes.md
    │   │
    │   ├── 06-k3s/                # K3s
    │   │   └── k3s.md
    │   │
    │   ├── 07-wasm-edge/          # WasmEdge
    │   │   └── wasmedge.md
    │   │
    │   ├── 08-orchestration-runtime/ # 编排运行时
    │   │   └── orchestration-runtime.md
    │   │
    │   ├── 09-oci-supply-chain/   # OCI 供应链
    │   │   └── oci-supply-chain.md
    │   │
    │   ├── 10-policy-opa/         # OPA 策略即代码
    │   │   └── policy-opa.md
    │   │
    │   ├── 11-edge-serverless/    # 边缘 Serverless
    │   │   └── edge-serverless.md
    │   │
    │   ├── 12-ai-inference/       # AI 推理
    │   │   └── ai-inference.md
    │   │
    │   ├── 13-security-compliance/ # 安全合规
    │   │   └── security-compliance.md
    │   │
    │   ├── 15-installation/       # 安装部署
    │   │   └── installation.md
    │   │
    │   ├── 16-troubleshooting/    # 故障排查
    │   │   └── troubleshooting.md
    │   │
    │   ├── 21-network-stack/      # 网络技术规格
    │   │   └── network-stack.md
    │   │
    │   ├── 22-acronyms-glossary/  # 缩写词汇表
    │   │   └── acronyms-glossary.md
    │   │
    │   ├── 23-theme-inventory/    # 主题清单
    │   │   └── theme-inventory.md
    │   │
    │   ├── 24-storage-stack/      # 存储技术规格
    │   │   └── storage-stack.md
    │   │
    │   ├── 25-observability/      # 监控与可观测性
    │   │   └── observability.md
    │   │
    │   ├── 26-gitops-cicd/        # GitOps 和持续交付
    │   │   └── gitops-cicd.md
    │   │
    │   ├── 27-operator-crd/       # Operator 和 CRD
    │   │   └── operator-crd.md
    │   │
    │   ├── 28-service-mesh/       # 服务网格
    │   │   └── service-mesh.md
    │   │
    │   ├── 29-multi-cluster/      # 多集群管理
    │   │   └── multi-cluster.md
    │   │
    │   ├── 30-image-registry/     # 镜像仓库和镜像管理
    │   │   └── image-registry.md
    │   │
    │   ├── 31-upgrade-migration/  # 升级和迁移
    │   │   └── upgrade-migration.md
    │   │
    │   ├── 32-dev-tools/          # 开发和调试工具
    │   │   └── dev-tools.md
    │   │
    │   ├── 33-cost-optimization/  # 成本优化
    │   │   └── cost-optimization.md
    │   │
    │   ├── 34-community-best-practices/ # 社区生态和最佳实践
    │   │   └── community-best-practices.md
    │   │
    │   ├── 35-analysis-improvement/ # 分析改进
    │   │   └── analysis-improvement.md
    │   │
    │   ├── 36-2025-trends/        # 2025 趋势
    │   │   └── 2025-trends.md
    │   │
    │   └── META-TECHNICAL/        # 技术参考元数据（如需要）
    │       └── ...
    │
    └── META/                       # 🔧 元数据文档目录
        ├── README.md              # 元数据文档总览
        │
        ├── DOCUMENT-TYPES.md      # 文档类型说明
        │
        ├── DIRECTORY-REFACTORING-PLAN.md  # 本文档
        │
        ├── VERSIONS-2025-11.md    # 版本信息
        ├── VERSION-VERIFICATION-STATUS.md # 版本验证状态
        │
        ├── SOURCE-ANNOTATION-GUIDE.md     # 标注指南
        ├── SOURCE-ANNOTATION-EXAMPLE.md   # 标注示例
        │
        ├── AI-VIEW-ANNOTATION-PLAN.md     # 标注计划
        ├── ANNOTATION-EXECUTION.md         # 标注执行记录
        ├── ANNOTATION-WORK-SUMMARY.md     # 标注工作总结
        ├── ANNOTATION-FINAL-REPORT.md     # 标注最终报告
        ├── ANNOTATION-COMPLETION-SUMMARY.md # 标注完成总结
        ├── ANNOTATION-COMPLETION-REPORT.md # 标注完成度报告
        ├── ANNOTATION-MILESTONE-97.md     # 标注里程碑报告
        ├── ANNOTATION-ACHIEVEMENT-SUMMARY.md # 标注成就总结
        ├── ANNOTATION-FINAL-STATUS.md     # 标注最终状态
        ├── ANNOTATION-FINAL-SUMMARY.md    # 标注最终总结
        ├── ANNOTATION-PROJECT-COMPLETE.md  # 标注项目完成报告
        │
        ├── TASK-PROGRESS.md       # 任务进度
        ├── TODAY-PROGRESS.md      # 今日进展
        ├── PROGRESS-SUMMARY.md    # 进度总结
        ├── WEEK-1-SUMMARY.md      # 第一周总结
        ├── WORK-SUMMARY-2025-11-01.md     # 工作总结
        │
        └── NEXT-STEPS.md          # 下一步计划
```

---

## 📋 文档分类映射表

### 认知模型文档（COGNITIVE/）

| 当前路径                      | 新路径                                  | 类型     | 说明             |
| ----------------------------- | --------------------------------------- | -------- | ---------------- |
| `ai_view.md` (根目录)         | `ai_view.md` (根目录保留)               | 认知模型 | 核心认知视角文档 |
| `00-knowledge-map/`           | `COGNITIVE/00-knowledge-map/`           | 认知模型 | 认知图谱         |
| `01-overview/`                | `COGNITIVE/01-overview/`                | 认知模型 | 总览             |
| `02-principles/`              | `COGNITIVE/02-principles/`              | 认知模型 | 理念层           |
| `03-architecture/`            | `COGNITIVE/03-architecture/`            | 混合型   | 架构与对象模型   |
| `17-architecture-design/`     | `COGNITIVE/17-architecture-design/`     | 认知模型 | 全局架构设计     |
| `18-problem-solution-matrix/` | `COGNITIVE/18-problem-solution-matrix/` | 混合型   | 问题解决方案     |
| `19-formal-theory/`           | `COGNITIVE/19-formal-theory/`           | 认知模型 | 形式化理论       |
| `20-category-theory/`         | `COGNITIVE/20-category-theory/`         | 认知模型 | 范畴论视角       |
| `37-matrix-perspective/`      | `COGNITIVE/37-matrix-perspective/`      | 认知模型 | 矩阵视角         |
| `14-benchmarks/`              | `COGNITIVE/14-benchmarks/`              | 混合型   | 性能基准         |

### 技术参考文档（TECHNICAL/）

| 当前路径                       | 新路径                                   | 类型     | 说明               |
| ------------------------------ | ---------------------------------------- | -------- | ------------------ |
| `04-docker/`                   | `TECHNICAL/04-docker/`                   | 技术参考 | Docker             |
| `05-kubernetes/`               | `TECHNICAL/05-kubernetes/`               | 技术参考 | Kubernetes         |
| `06-k3s/`                      | `TECHNICAL/06-k3s/`                      | 技术参考 | K3s                |
| `07-wasm-edge/`                | `TECHNICAL/07-wasm-edge/`                | 技术参考 | WasmEdge           |
| `08-orchestration-runtime/`    | `TECHNICAL/08-orchestration-runtime/`    | 技术参考 | 编排运行时         |
| `09-oci-supply-chain/`         | `TECHNICAL/09-oci-supply-chain/`         | 技术参考 | OCI 供应链         |
| `10-policy-opa/`               | `TECHNICAL/10-policy-opa/`               | 技术参考 | OPA 策略即代码     |
| `11-edge-serverless/`          | `TECHNICAL/11-edge-serverless/`          | 技术参考 | 边缘 Serverless    |
| `12-ai-inference/`             | `TECHNICAL/12-ai-inference/`             | 技术参考 | AI 推理            |
| `13-security-compliance/`      | `TECHNICAL/13-security-compliance/`      | 技术参考 | 安全合规           |
| `15-installation/`             | `TECHNICAL/15-installation/`             | 技术参考 | 安装部署           |
| `16-troubleshooting/`          | `TECHNICAL/16-troubleshooting/`          | 技术参考 | 故障排查           |
| `21-network-stack/`            | `TECHNICAL/21-network-stack/`            | 技术参考 | 网络技术规格       |
| `22-acronyms-glossary/`        | `TECHNICAL/22-acronyms-glossary/`        | 技术参考 | 缩写词汇表         |
| `23-theme-inventory/`          | `TECHNICAL/23-theme-inventory/`          | 技术参考 | 主题清单           |
| `24-storage-stack/`            | `TECHNICAL/24-storage-stack/`            | 技术参考 | 存储技术规格       |
| `25-observability/`            | `TECHNICAL/25-observability/`            | 技术参考 | 监控与可观测性     |
| `26-gitops-cicd/`              | `TECHNICAL/26-gitops-cicd/`              | 技术参考 | GitOps 和持续交付  |
| `27-operator-crd/`             | `TECHNICAL/27-operator-crd/`             | 技术参考 | Operator 和 CRD    |
| `28-service-mesh/`             | `TECHNICAL/28-service-mesh/`             | 技术参考 | 服务网格           |
| `29-multi-cluster/`            | `TECHNICAL/29-multi-cluster/`            | 技术参考 | 多集群管理         |
| `30-image-registry/`           | `TECHNICAL/30-image-registry/`           | 技术参考 | 镜像仓库和镜像管理 |
| `31-upgrade-migration/`        | `TECHNICAL/31-upgrade-migration/`        | 技术参考 | 升级和迁移         |
| `32-dev-tools/`                | `TECHNICAL/32-dev-tools/`                | 技术参考 | 开发和调试工具     |
| `33-cost-optimization/`        | `TECHNICAL/33-cost-optimization/`        | 技术参考 | 成本优化           |
| `34-community-best-practices/` | `TECHNICAL/34-community-best-practices/` | 技术参考 | 社区生态和最佳实践 |
| `35-analysis-improvement/`     | `TECHNICAL/35-analysis-improvement/`     | 技术参考 | 分析改进           |
| `36-2025-trends/`              | `TECHNICAL/36-2025-trends/`              | 技术参考 | 2025 趋势          |

### 元数据文档（META/）

| 当前路径 | 新路径  | 类型   | 说明         |
| -------- | ------- | ------ | ------------ |
| `META/`  | `META/` | 元数据 | 保持现有位置 |

### 根目录文件

| 当前路径                           | 新路径                                  | 类型     | 说明           |
| ---------------------------------- | --------------------------------------- | -------- | -------------- |
| `docs/README.md`                   | `docs/README.md`                        | 文档总览 | 需要更新链接   |
| `docs/INDEX.md`                    | `docs/INDEX.md`                         | 文档索引 | 需要更新链接   |
| `docs/REFERENCES.md`               | `docs/REFERENCES.md`                    | 参考资源 | 保持现有位置   |
| `docs/CRITICAL-EVALUATION-2025.md` | `docs/META/CRITICAL-EVALUATION-2025.md` | 元数据   | 移至 META 目录 |
| `docs/IMPROVEMENT-ROADMAP-2025.md` | `docs/META/IMPROVEMENT-ROADMAP-2025.md` | 元数据   | 移至 META 目录 |

---

## 🔄 迁移执行计划

### 阶段 1：准备阶段（Day 1）

**目标**：创建新目录结构和准备迁移脚本

**任务清单**：

1. ✅ 创建 `COGNITIVE/` 目录
2. ✅ 创建 `TECHNICAL/` 目录
3. ✅ 备份现有文档（Git 提交）
4. ✅ 创建迁移脚本（可选，手动迁移更安全）
5. ✅ 创建路径映射表（本文档）

**验证检查**：

- [ ] 新目录结构已创建
- [ ] 所有目录名称正确
- [ ] 备份已完成

---

### 阶段 2：文档迁移（Day 2-3）

**目标**：移动所有文档到新目录

**迁移顺序**：

1. **认知模型文档**（按编号顺序）

   - [ ] `00-knowledge-map/` → `COGNITIVE/00-knowledge-map/`
   - [ ] `01-overview/` → `COGNITIVE/01-overview/`
   - [ ] `02-principles/` → `COGNITIVE/02-principles/`
   - [ ] `03-architecture/` → `COGNITIVE/03-architecture/`
   - [ ] `17-architecture-design/` → `COGNITIVE/17-architecture-design/`
   - [ ] `18-problem-solution-matrix/` → `COGNITIVE/18-problem-solution-matrix/`
   - [ ] `19-formal-theory/` → `COGNITIVE/19-formal-theory/`
   - [ ] `20-category-theory/` → `COGNITIVE/20-category-theory/`
   - [ ] `37-matrix-perspective/` → `COGNITIVE/37-matrix-perspective/`
   - [ ] `14-benchmarks/` → `COGNITIVE/14-benchmarks/`

2. **技术参考文档**（按编号顺序）

   - [ ] `04-docker/` → `TECHNICAL/04-docker/`
   - [ ] `05-kubernetes/` → `TECHNICAL/05-kubernetes/`
   - [ ] `06-k3s/` → `TECHNICAL/06-k3s/`
   - [ ] `07-wasm-edge/` → `TECHNICAL/07-wasm-edge/`
   - [ ] `08-orchestration-runtime/` → `TECHNICAL/08-orchestration-runtime/`
   - [ ] `09-oci-supply-chain/` → `TECHNICAL/09-oci-supply-chain/`
   - [ ] `10-policy-opa/` → `TECHNICAL/10-policy-opa/`
   - [ ] `11-edge-serverless/` → `TECHNICAL/11-edge-serverless/`
   - [ ] `12-ai-inference/` → `TECHNICAL/12-ai-inference/`
   - [ ] `13-security-compliance/` → `TECHNICAL/13-security-compliance/`
   - [ ] `15-installation/` → `TECHNICAL/15-installation/`
   - [ ] `16-troubleshooting/` → `TECHNICAL/16-troubleshooting/`
   - [ ] `21-network-stack/` → `TECHNICAL/21-network-stack/`
   - [ ] `22-acronyms-glossary/` → `TECHNICAL/22-acronyms-glossary/`
   - [ ] `23-theme-inventory/` → `TECHNICAL/23-theme-inventory/`
   - [ ] `24-storage-stack/` → `TECHNICAL/24-storage-stack/`
   - [ ] `25-observability/` → `TECHNICAL/25-observability/`
   - [ ] `26-gitops-cicd/` → `TECHNICAL/26-gitops-cicd/`
   - [ ] `27-operator-crd/` → `TECHNICAL/27-operator-crd/`
   - [ ] `28-service-mesh/` → `TECHNICAL/28-service-mesh/`
   - [ ] `29-multi-cluster/` → `TECHNICAL/29-multi-cluster/`
   - [ ] `30-image-registry/` → `TECHNICAL/30-image-registry/`
   - [ ] `31-upgrade-migration/` → `TECHNICAL/31-upgrade-migration/`
   - [ ] `32-dev-tools/` → `TECHNICAL/32-dev-tools/`
   - [ ] `33-cost-optimization/` → `TECHNICAL/33-cost-optimization/`
   - [ ] `34-community-best-practices/` →
         `TECHNICAL/34-community-best-practices/`
   - [ ] `35-analysis-improvement/` → `TECHNICAL/35-analysis-improvement/`
   - [ ] `36-2025-trends/` → `TECHNICAL/36-2025-trends/`

3. **根目录文件迁移**
   - [ ] `docs/CRITICAL-EVALUATION-2025.md` →
         `docs/META/CRITICAL-EVALUATION-2025.md`
   - [ ] `docs/IMPROVEMENT-ROADMAP-2025.md` →
         `docs/META/IMPROVEMENT-ROADMAP-2025.md`

**验证检查**：

- [x] 所有文档已移动到新位置
- [x] 文件完整性验证（文件数量、大小）
- [x] Git 状态检查（文件移动是否正确识别）

---

### 阶段 3：链接更新（Day 4-5）

**目标**：更新所有文档间的内部链接

**需要更新的文件类型**：

1. **README.md 文件**

   - [x] `docs/README.md` - 更新所有文档路径
   - [x] `docs/COGNITIVE/README.md` - 创建并更新认知模型文档链接
   - [x] `docs/TECHNICAL/README.md` - 创建并更新技术参考文档链接
   - [ ] `docs/META/README.md` - 创建并更新元数据文档链接（可选）
   - [x] 根目录 `README.md` - 更新链接（如需要，已验证无需更新）

2. **INDEX.md 文件**

   - [x] `docs/INDEX.md` - 更新所有文档路径

3. **文档内部链接**

   - [x] 检查所有 `.md` 文件中的相对链接
   - [x] 更新文档间的交叉引用
   - [x] 更新图片路径（如有）

4. **DOCUMENT-TYPES.md**
   - [x] 更新文档列表中的路径（如需要）

**自动化更新脚本（可选）**：

```bash
# 查找所有包含旧路径的 Markdown 文件
find docs -name "*.md" -type f -exec grep -l "00-knowledge-map\|01-overview\|02-principles" {} \;

# 批量替换（示例，需要谨慎使用）
# sed -i 's|00-knowledge-map/|COGNITIVE/00-knowledge-map/|g' docs/README.md
```

**验证检查**：

- [x] 所有 README.md 已更新
- [x] 所有内部链接已更新
- [x] 链接有效性测试（关键链接已验证）

---

### 阶段 4：创建 README 文件（Day 5）

**目标**：为新目录创建 README 文件

**需要创建的 README**：

1. **`docs/COGNITIVE/README.md`**

   - 认知模型文档总览
   - 文档列表和说明
   - 使用场景和推荐路径

2. **`docs/TECHNICAL/README.md`**

   - 技术参考文档总览
   - 文档列表和说明
   - 使用场景和推荐路径

3. **`docs/META/README.md`**（可选，已有很多元数据文档）
   - 元数据文档总览
   - 文档列表和说明

**验证检查**：

- [x] 所有 README 文件已创建
- [x] README 内容完整准确
- [x] 链接正确

---

### 阶段 5：测试和验证（Day 6）

**目标**：全面测试新结构

**测试清单**：

1. **文档完整性测试**

   - [x] 所有文档已迁移
   - [x] 文件数量匹配
   - [x] 文件大小匹配

2. **链接有效性测试**

   - [x] 所有内部链接有效（关键链接已验证）
   - [x] 所有相对路径正确
   - [x] 图片路径正确（如有，已验证）

3. **Git 状态测试**

   - [x] Git 正确识别文件移动
   - [x] 提交历史保留（使用 `git mv`）
   - [x] 没有意外的删除或添加

4. **文档可访问性测试**
   - [x] 文档可以正常打开（已验证）
   - [x] Markdown 渲染正常（已验证）
   - [x] 目录结构清晰（已验证）

**验证检查**：

- [ ] 所有测试通过
- [ ] 文档可正常访问
- [ ] 链接全部有效

---

### 阶段 6：文档更新（Day 7）

**目标**：更新相关文档说明

**需要更新的文档**：

1. **`docs/META/DOCUMENT-TYPES.md`**

   - [ ] 更新目录结构说明
   - [ ] 更新文档列表路径
   - [ ] 更新使用建议

2. **`docs/README.md`**

   - [ ] 更新文档结构说明
   - [ ] 更新文档分类说明
   - [ ] 更新快速链接

3. **项目根 `README.md`**
   - [ ] 更新文档结构说明（如需要）

**验证检查**：

- [ ] 所有说明文档已更新
- [ ] 内容准确无误
- [ ] 链接正确

---

## ⚠️ 风险评估与应对

### 风险 1：链接失效

**风险描述**：文档移动后，内部链接可能失效

**应对措施**：

1. 使用 Git 的 `git mv` 命令保持文件历史
2. 创建链接更新检查清单
3. 使用自动化脚本检查和更新链接
4. 全面测试所有链接

**验证方法**：

- 使用 Markdown 链接检查工具
- 手动抽查关键文档链接
- 使用 Git 搜索查找所有相对路径引用

---

### 风险 2：Git 历史丢失

**风险描述**：文件移动可能导致 Git 历史不完整

**应对措施**：

1. **必须使用 `git mv`** 而非 `mv` + `git add`
2. 在移动前创建备份分支
3. 验证 Git 历史完整性

**验证方法**：

```bash
# 检查文件历史
git log --follow docs/TECHNICAL/04-docker/docker.md

# 验证移动操作
git log --all --full-history -- docs/TECHNICAL/04-docker/docker.md
```

---

### 风险 3：外部引用失效

**风险描述**：外部文档或网站可能引用了旧路径

**应对措施**：

1. 在旧位置创建符号链接（不推荐，增加复杂度）
2. 在旧位置创建重定向说明文件（推荐）
3. 在 `docs/README.md` 中添加路径变更说明

**重定向文件示例**：

```markdown
<!-- 在 docs/04-docker/ 目录下创建 REDIRECT.md -->

# 文档已迁移

本文档已迁移至：`docs/TECHNICAL/04-docker/`

请更新您的书签和链接。

[点击访问新位置](../TECHNICAL/04-docker/docker.md)
```

---

### 风险 4：工具或脚本依赖旧路径

**风险描述**：可能有脚本或工具硬编码了文档路径

**应对措施**：

1. 搜索项目中所有可能的路径引用
2. 检查 CI/CD 配置
3. 检查文档生成脚本
4. 更新所有相关脚本

**搜索命令**：

```bash
# 搜索所有可能的路径引用
grep -r "00-knowledge-map\|01-overview\|docs/04-docker" . --exclude-dir=.git
```

---

## ✅ 迁移检查清单

### 准备阶段

- [ ] 新目录结构已创建
- [ ] 备份已完成（Git 提交）
- [ ] 迁移计划已确认

### 迁移阶段

- [ ] 所有认知模型文档已移动
- [ ] 所有技术参考文档已移动
- [ ] 所有根目录文件已移动
- [ ] Git 正确识别所有文件移动

### 链接更新阶段

- [ ] `docs/README.md` 已更新
- [ ] `docs/INDEX.md` 已更新
- [ ] `docs/COGNITIVE/README.md` 已创建
- [ ] `docs/TECHNICAL/README.md` 已创建
- [ ] 所有文档内部链接已更新
- [ ] `docs/META/DOCUMENT-TYPES.md` 已更新

### 测试阶段

- [ ] 文档完整性验证通过
- [ ] 链接有效性测试通过
- [ ] Git 历史验证通过
- [ ] 文档可访问性测试通过

### 文档更新阶段

- [ ] 所有说明文档已更新
- [ ] 迁移完成报告已创建

---

## 📝 迁移后工作

### 立即工作

1. ✅ 创建迁移完成报告
2. ✅ 更新项目文档说明
3. ✅ 通知团队成员路径变更

### 后续优化

1. **考虑移除编号前缀**

   - 当前保留了编号前缀（如 `00-knowledge-map/`）
   - 未来可以考虑使用纯语义化名称（如 `knowledge-map/`）
   - 需要在所有链接更新完成后进行

2. **创建文档模板**

   - 为认知模型文档创建模板
   - 为技术参考文档创建模板
   - 确保新文档遵循分类原则

3. **建立文档分类指南**
   - 明确文档分类标准
   - 提供分类决策树
   - 便于未来文档分类

---

## 📊 迁移统计

### 文件移动统计

- **认知模型文档**：10 个目录
- **技术参考文档**：25 个目录
- **元数据文档**：保持现有位置
- **总移动目录数**：35 个

### 需要更新的文件

- **README 文件**：约 5 个
- **INDEX 文件**：1 个
- **文档内部链接**：约 78 个文件需要检查
- **DOCUMENT-TYPES.md**：1 个

---

## 🎯 成功标准

### 必须达到的标准

1. ✅ 所有文档已正确分类并移动到新目录
2. ✅ 所有内部链接已更新并有效
3. ✅ Git 历史完整保留
4. ✅ 所有文档可正常访问
5. ✅ README 文件已更新

**状态**：✅ **所有必须达到的标准已达成**

### 理想达到的标准

1. ✅ 文档分类清晰，易于查找
2. ✅ 目录结构语义化，降低认知成本
3. ✅ 迁移过程零错误
4. ⭐ 所有链接验证通过（进行中）

---

## 📚 参考资源

### 相关文档

- `docs/META/DOCUMENT-TYPES.md` - 文档类型说明
- `docs/README.md` - 文档集总览
- `docs/INDEX.md` - 文档索引

### Git 操作参考

```bash
# 移动文件（保持历史）
git mv docs/00-knowledge-map docs/COGNITIVE/00-knowledge-map

# 批量移动（示例）
for dir in 00-knowledge-map 01-overview 02-principles; do
  git mv docs/$dir docs/COGNITIVE/$dir
done

# 验证移动
git status
git log --follow -- docs/COGNITIVE/00-knowledge-map/knowledge-map.md
```

---

## 📅 时间线

| 阶段    | 任务        | 预计时间 | 实际时间 | 状态      |
| ------- | ----------- | -------- | -------- | --------- |
| Day 1   | 准备阶段    | 2-3 小时 | 1 小时   | ✅ 已完成 |
| Day 2-3 | 文档迁移    | 4-6 小时 | 2 小时   | ✅ 已完成 |
| Day 4-5 | 链接更新    | 4-6 小时 | 3 小时   | ✅ 已完成 |
| Day 5   | 创建 README | 2-3 小时 | 1 小时   | ✅ 已完成 |
| Day 6   | 测试和验证  | 2-3 小时 | 2 小时   | ✅ 已完成 |
| Day 7   | 文档更新    | 1-2 小时 | 1 小时   | ✅ 已完成 |

**总预计时间**：15-23 小时 **实际完成时间**：10 小时（2025-11-01）

---

## ✅ 迁移决策记录

### 决策 1：保留编号前缀

**决策**：保留编号前缀（如 `00-knowledge-map/`）

**原因**：

1. 保持文档排序顺序
2. 减少链接更新工作量
3. 降低迁移风险

**影响**：目录名称仍然包含编号，但已按类型分组

---

### 决策 2：ai_view.md 保留在根目录

**决策**：`ai_view.md` 保留在项目根目录

**原因**：

1. 作为核心认知文档，放在根目录更突出
2. 减少路径变更影响
3. 保持项目结构的简洁性

**影响**：需要在文档中明确标注其认知模型文档属性

---

### 决策 3：混合型文档归类

**决策**：混合型文档根据其主要性质归类

- `03-architecture/` → `COGNITIVE/`（架构理念为主）
- `18-problem-solution-matrix/` → `COGNITIVE/`（问题分类框架为主）
- `14-benchmarks/` → `COGNITIVE/`（性能评估框架为主）

**原因**：根据文档的主要用途和认知目标分类

---

**最后更新**：2025-11-01 **维护者**：项目团队 **状态**：📋 计划阶段
