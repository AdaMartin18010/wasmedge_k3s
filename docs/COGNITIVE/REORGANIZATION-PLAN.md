# COGNITIVE 目录重组方案

**创建日期**：2025-11-08 **版本**：v1.0

## 📊 当前状况

- **目录总数**：17 个
- **组织方式**：按数字编号（00-16）
- **问题**：目录过多，难以快速定位；数字编号不直观；相关主题分散

## 🎯 重组目标

1. **按主题分类**：将相关文档归类到同一主题下
2. **减少顶层目录**：从 17 个减少到约 5 个主题目录
3. **保持向后兼容**：通过 README.md 提供旧路径映射
4. **提升可导航性**：清晰的分类便于快速定位

## 📁 新目录结构

```text
COGNITIVE/
├── 01-core-foundations/          # 核心基础
│   ├── knowledge-map/            # 知识地图和学习路径
│   ├── overview/                 # 技术栈总览和决策框架
│   └── principles/               # 云原生核心理念
│
├── 02-architecture-design/      # 架构与设计
│   ├── architecture/             # 架构理念和设计思想
│   ├── architecture-design/      # 技术组合和架构决策
│   └── problem-solution-matrix/  # 问题分类框架
│
├── 03-theoretical-perspectives/  # 理论视角
│   ├── formal-theory/            # 形式化理论
│   ├── category-theory/          # 范畴论视角
│   ├── matrix-perspective/        # 矩阵视角
│   ├── algebraic-structure/       # 代数结构视角
│   └── structural-perspective/   # 结构视角
│
├── 04-application-perspectives/   # 应用视角
│   ├── ebpf-otlp-perspective/    # eBPF/OTLP 视角
│   ├── programming-perspective/  # 程序设计视角
│   ├── application-perspective/  # 应用业务架构视角
│   └── api-perspective/          # API 规范视角
│
└── 05-decision-analysis/         # 决策与分析
    ├── decision-models/           # 技术决策模型
    └── benchmarks/               # 性能评估框架
```

## 🔄 迁移映射表

| 旧路径                        | 新路径                                                 |
| ----------------------------- | ------------------------------------------------------ |
| `00-knowledge-map/`           | `01-core-foundations/knowledge-map/`                   |
| `01-overview/`                | `01-core-foundations/overview/`                        |
| `02-principles/`              | `01-core-foundations/principles/`                      |
| `03-architecture/`            | `02-architecture-design/architecture/`                 |
| `05-architecture-design/`     | `02-architecture-design/architecture-design/`          |
| `06-problem-solution-matrix/` | `02-architecture-design/problem-solution-matrix/`      |
| `07-formal-theory/`           | `03-theoretical-perspectives/formal-theory/`           |
| `08-category-theory/`         | `03-theoretical-perspectives/category-theory/`         |
| `09-matrix-perspective/`      | `03-theoretical-perspectives/matrix-perspective/`      |
| `11-algebraic-structure/`     | `03-theoretical-perspectives/algebraic-structure/`     |
| `12-structural-perspective/`  | `03-theoretical-perspectives/structural-perspective/`  |
| `13-ebpf-otlp-perspective/`   | `04-application-perspectives/ebpf-otlp-perspective/`   |
| `14-programming-perspective/` | `04-application-perspectives/programming-perspective/` |
| `15-application-perspective/` | `04-application-perspectives/application-perspective/` |
| `16-api-perspective/`         | `04-application-perspectives/api-perspective/`         |
| `10-decision-models/`         | `05-decision-analysis/decision-models/`                |
| `04-benchmarks/`              | `05-decision-analysis/benchmarks/`                     |

## ✅ 实施步骤

1. ✅ 创建新的目录结构
2. ✅ 移动文件到新位置
3. ✅ 更新所有文档中的路径引用（核心导航文档）
4. ✅ 更新所有文档中的路径引用（内部文档）
5. ✅ 更新 README.md
6. ✅ 创建路径映射文档（向后兼容）
7. ✅ 验证所有链接

---

**状态**：✅ 全部完成（2025-11-08）

## 📊 完成统计

- **目录重组**：从 17 个数字编号目录 → 5 个主题分类目录
- **文件组织**：所有文件已组织到新位置
- **路径更新**：所有文档路径引用已更新
  - `docs/INDEX.md` - 路径更新完成
  - `docs/README.md` - 路径更新完成
  - `docs/COGNITIVE/README.md` - 路径更新完成
  - `docs/ARCHITECTURE/INDEX.md` - 路径更新完成
  - `docs/ARCHITECTURE/README.md` - 路径更新完成
  - `docs/TECHNICAL/README.md` - 路径更新完成
  - `PROJECT-OVERVIEW.md` - 路径更新完成
  - `README.md` - 路径更新完成
  - 所有一致性文档 - 路径更新完成
  - 所有内部文档 - 路径更新完成
- **支持文档**：
  - `PATH-MAPPING.md` - 路径映射表（向后兼容）
  - `README.md` - 认知模型文档说明（已更新）
- **验证结果**：
  - ✅ 所有路径引用已更新
  - ✅ 文档结构已重组
  - ✅ 向后兼容性已保证（PATH-MAPPING.md）
  - ⚠️  有 12 个 linter 警告（链接片段验证，不影响功能）
