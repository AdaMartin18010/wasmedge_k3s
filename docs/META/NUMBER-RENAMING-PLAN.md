# 目录序号重命名计划

## 📊 问题分析

### 当前序号情况

**COGNITIVE 目录**（10 个目录）：

- 00, 01, 02, 03（连续）
- **缺失**：04-13
- 14（跳过）
- **缺失**：15-16
- 17, 18, 19, 20（连续）
- **缺失**：21-36
- 37（跳过）

**TECHNICAL 目录**（28 个目录）：

- 04-13（连续，10 个目录，从 04 开始）
- **缺失**：14
- 15, 16（连续，2 个目录）
- **缺失**：17-20
- 21-36（连续，16 个目录）
- **总计**：10 + 2 + 16 = 28 个目录

### 问题影响

1. **序号不连续** - 难以理解目录顺序和逻辑
2. **查找困难** - 编号跳转让人困惑
3. **维护不便** - 新增文档时不知道应该使用哪个序号

---

## 🎯 重新编号方案

### 方案：连续编号

**COGNITIVE 目录**：重新编号为 `00-09`（连续）

**TECHNICAL 目录**：重新编号为 `00-27`（连续，28 个目录）

### 映射表

#### COGNITIVE 目录重命名映射

| 旧名称                       | 新名称                       | 说明     |
| ---------------------------- | ---------------------------- | -------- |
| `00-knowledge-map`           | `00-knowledge-map`           | 保持不变 |
| `01-overview`                | `01-overview`                | 保持不变 |
| `02-principles`              | `02-principles`              | 保持不变 |
| `03-architecture`            | `03-architecture`            | 保持不变 |
| `14-benchmarks`              | `04-benchmarks`              | 14→04    |
| `17-architecture-design`     | `05-architecture-design`     | 17→05    |
| `18-problem-solution-matrix` | `06-problem-solution-matrix` | 18→06    |
| `19-formal-theory`           | `07-formal-theory`           | 19→07    |
| `20-category-theory`         | `08-category-theory`         | 20→08    |
| `37-matrix-perspective`      | `09-matrix-perspective`      | 37→09    |

#### TECHNICAL 目录重命名映射

| 旧名称                        | 新名称                        | 说明  |
| ----------------------------- | ----------------------------- | ----- |
| `04-docker`                   | `00-docker`                   | 04→00 |
| `05-kubernetes`               | `01-kubernetes`               | 05→01 |
| `06-k3s`                      | `02-k3s`                      | 06→02 |
| `07-wasm-edge`                | `03-wasm-edge`                | 07→03 |
| `08-orchestration-runtime`    | `04-orchestration-runtime`    | 08→04 |
| `09-oci-supply-chain`         | `05-oci-supply-chain`         | 09→05 |
| `10-policy-opa`               | `06-policy-opa`               | 10→06 |
| `11-edge-serverless`          | `07-edge-serverless`          | 11→07 |
| `12-ai-inference`             | `08-ai-inference`             | 12→08 |
| `13-security-compliance`      | `09-security-compliance`      | 13→09 |
| `15-installation`             | `10-installation`             | 15→10 |
| `16-troubleshooting`          | `11-troubleshooting`          | 16→11 |
| `21-network-stack`            | `12-network-stack`            | 21→12 |
| `22-acronyms-glossary`        | `13-acronyms-glossary`        | 22→13 |
| `23-theme-inventory`          | `14-theme-inventory`          | 23→14 |
| `24-storage-stack`            | `15-storage-stack`            | 24→15 |
| `25-observability`            | `16-observability`            | 25→16 |
| `26-gitops-cicd`              | `17-gitops-cicd`              | 26→17 |
| `27-operator-crd`             | `18-operator-crd`             | 27→18 |
| `28-service-mesh`             | `19-service-mesh`             | 28→19 |
| `29-multi-cluster`            | `20-multi-cluster`            | 29→20 |
| `30-image-registry`           | `21-image-registry`           | 30→21 |
| `31-upgrade-migration`        | `22-upgrade-migration`        | 31→22 |
| `32-dev-tools`                | `23-dev-tools`                | 32→23 |
| `33-cost-optimization`        | `24-cost-optimization`        | 33→24 |
| `34-community-best-practices` | `25-community-best-practices` | 34→25 |
| `35-analysis-improvement`     | `26-analysis-improvement`     | 35→26 |
| `36-2025-trends`              | `27-2025-trends`              | 36→27 |

---

## 📋 执行计划

### 阶段 1：COGNITIVE 目录重命名（6 个目录需要重命名）

需要重命名的目录：

1. `14-benchmarks` → `04-benchmarks`
2. `17-architecture-design` → `05-architecture-design`
3. `18-problem-solution-matrix` → `06-problem-solution-matrix`
4. `19-formal-theory` → `07-formal-theory`
5. `20-category-theory` → `08-category-theory`
6. `37-matrix-perspective` → `09-matrix-perspective`

### 阶段 2：TECHNICAL 目录重命名（28 个目录需要重命名）

需要重命名的目录：

1. `04-docker` → `00-docker`
2. `05-kubernetes` → `01-kubernetes`
3. `06-k3s` → `02-k3s`
4. `07-wasm-edge` → `03-wasm-edge`
5. `08-orchestration-runtime` → `04-orchestration-runtime`
6. `09-oci-supply-chain` → `05-oci-supply-chain`
7. `10-policy-opa` → `06-policy-opa`
8. `11-edge-serverless` → `07-edge-serverless`
9. `12-ai-inference` → `08-ai-inference`
10. `13-security-compliance` → `09-security-compliance`
11. `15-installation` → `10-installation`
12. `16-troubleshooting` → `11-troubleshooting`
13. `21-network-stack` → `12-network-stack`
14. `22-acronyms-glossary` → `13-acronyms-glossary`
15. `23-theme-inventory` → `14-theme-inventory`
16. `24-storage-stack` → `15-storage-stack`
17. `25-observability` → `16-observability`
18. `26-gitops-cicd` → `17-gitops-cicd`
19. `27-operator-crd` → `18-operator-crd`
20. `28-service-mesh` → `19-service-mesh`
21. `29-multi-cluster` → `20-multi-cluster`
22. `30-image-registry` → `21-image-registry`
23. `31-upgrade-migration` → `22-upgrade-migration`
24. `32-dev-tools` → `23-dev-tools`
25. `33-cost-optimization` → `24-cost-optimization`
26. `34-community-best-practices` → `25-community-best-practices`
27. `35-analysis-improvement` → `26-analysis-improvement`
28. `36-2025-trends` → `27-2025-trends`

### 阶段 3：链接更新（约 325 个链接）

需要更新所有文档中的链接引用：

- `docs/README.md` - 约 95 个链接
- `docs/INDEX.md` - 约 97 个链接
- `docs/COGNITIVE/` - 约 116 个内部链接
- `docs/TECHNICAL/` - 约 10 个内部链接
- `docs/META/` - 约 7 个内部链接

### 阶段 4：验证

- 验证目录结构
- 验证链接有效性
- 验证 Git 历史保留

---

## ⚠️ 注意事项

1. **使用 `git mv`** - 保持 Git 历史
2. **批量更新链接** - 使用 `replace_all` 参数
3. **验证测试** - 每个阶段后进行验证
4. **备份** - 确保有 Git 备份

---

**状态**：📋 计划阶段 **预计时间**：2-3 小时 **风险等级**：中（需要更新大量链接
）

---

**最后更新**：2025-11-01 **维护者**：项目团队
