# 安全形式化：把"安全"变成数据 + 规则

## 1. 概述

本文档详细阐述如何通过 **OPA** 将"安全"从不可量化的运维玄学变成**可单元测试、可
形式化验证、可与业务代码同版本回滚的 DSL**。

### 1.1 核心思想

> **OPA 把"安全"从不可量化的运维玄学**，**变成了一段可单元测试、可形式化验证、可
> 与业务代码同版本回滚的 DSL**；于是虚拟化-容器化-沙盒化所压缩出的中层世界 ℳ，终
> 于**在逻辑层面闭合**—— **计算可证明、资源可证明、通信可证明、安全亦可证明**。

## 2. 公理层——把"安全"形式化

### 2.1 公理定义

| 公理          | 形式化描述                         | OPA 对应实体                                    |
| ------------- | ---------------------------------- | ----------------------------------------------- |
| A5 能力闭包   | ∀u∈U, Capability(u) ⊆ ∩{syscallᵢ}  | `deny[msg] { capability[_] != required }`       |
| A6 最小权限   | ∀ edge e∈G, Role(e) ⊆ Need-to-know | `allow = true { input.user == resource.owner }` |
| A7 可证明性   | 策略决策 ≡ 布尔可满足性（SAT）     | Rego → JSON → AST → SAT 求解                    |
| A8 版本一致性 | Policy Δ ≃ Code Δ                  | Git SHA 相同即可重现决策                        |

### 2.2 公理说明

**A5 能力闭包**：

- 每个计算单元的能力集合是其所需系统调用的交集
- OPA 通过 `deny` 规则确保只有必要的系统调用被允许

**A6 最小权限**：

- 每条边的权限集合满足最小权限原则
- OPA 通过 `allow` 规则确保只有必要的权限被授予

**A7 可证明性**：

- 策略决策等价于布尔可满足性问题
- OPA 通过 Rego → JSON → AST → SAT 求解实现可证明性

**A8 版本一致性**：

- 策略变更与代码变更同步
- OPA 通过 Git SHA 确保策略与代码版本一致

## 3. 基础归纳步——没有 OPA 的时代（n=0）

### 3.1 系统 Σ₀

**系统特征**：

- 安全基线 = 2000 行 Bash + 52 个 Excel 检查项
- 证据 = 截图 + 人工签字
- 状态空间 |S_security| ≈ 2²⁰⁰⁰（每条脚本 branch 一个维度）

### 3.2 问题分析

**问题**：

1. 无法证明"全局能力闭包"→ 出现 **syscall 逃逸**
2. 无法组合"跨服务权限"→ **权限膨胀**
3. 无法版本化"谁改了哪条规则"→ **审计断层**

### 3.3 结论

Σ₀ 不满足 A5-A8，需引入 Ψ_policy : Σ₀ → Σ₁ = Σ₀ + OPA

## 4. 第一次归纳映射——把"安全"变成数据 + 规则

### 4.1 映射定义

**映射**：Ψ_policy

- **输入**：任意 JSON（K8s AdmissionReview / 容器镜像元数据 / Terraform plan）
- **输出**：**允许 / 拒绝 + 一组绑定变量**（可用于后续策略）
- **决策引擎**：**Rego 语言 = Datalog with negation** → 可证明终止

### 4.2 关键引理 L3（决策确定性）

> ∀ 输入 i, OPA 求值过程 ≡ 单调不动点迭代故决策 d = OPA(i) 在有限步内唯一且可重
> 现

### 4.3 实证

- **2023 年 CNCF Survey**：**OPA 平均评估延迟 1.2 ms，P99 6 ms**
- **同一 Bundle**（Git SHA=abc123）在**不同集群**决策一致性 = 100 %（n=5×10⁷）

## 5. Rego 语言基础

### 5.1 Rego 语法

**Rego** 是 OPA 的策略定义语言，基于 **Datalog with negation**。

**基本语法**：

```rego
package authz

# 默认拒绝
default allow = false

# 允许规则
allow {
  input.user.role == "admin"
  input.operation == "create"
}

# 拒绝规则
deny[msg] {
  input.user.role != "admin"
  msg := "only admin can create"
}
```

### 5.2 Rego 特性

- **声明式**：描述"什么"而不是"如何"
- **可组合**：规则可以组合和重用
- **可证明**：决策过程可形式化验证

## 6. OPA 决策流程

### 6.1 决策流程

```text
输入（JSON）
  ↓
OPA 评估（Rego）
  ↓
决策（allow/deny + 变量绑定）
  ↓
输出（JSON）
```

### 6.2 决策确定性

**决策确定性保证**：

- **单调不动点迭代**：决策过程保证收敛
- **有限步终止**：决策在有限步内完成
- **唯一性**：相同输入产生相同输出
- **可重现性**：决策结果可重现

## 7. 策略测试与验证

### 7.1 单元测试

**OPA 测试**：

```rego
package authz

test_admin_can_create {
  allow with input as {
    "user": {"role": "admin"},
    "operation": "create"
  }
}

test_non_admin_cannot_create {
  not allow with input as {
    "user": {"role": "user"},
    "operation": "create"
  }
}
```

### 7.2 形式化验证

**SAT 求解**：

- Rego → JSON → AST → SAT 求解
- 可自动验证策略的正确性

### 7.3 集成测试

**CI/CD 集成**：

```yaml
- name: OPA Test
  run: |
    opa test ./policies
    opa eval --data ./policies --input ./tests/test.json
```

## 8. 策略版本化

### 8.1 GitOps 集成

**策略版本化**：

- 策略存储在 Git 仓库中
- 每个策略变更都有 Git commit SHA
- 策略与代码同步版本化

### 8.2 Bundle 管理

**OPA Bundle**：

- 包含策略、数据、元数据
- 支持版本化（Git SHA）
- 支持热更新（无需重启服务）

**示例**：

```bash
# 创建 Bundle
opa bundle create -o authz.bundle authz.rego

# 推送 Bundle
opa bundle push authz.bundle

# 更新 Bundle
opa bundle push authz.bundle --revision abc123
```

## 9. 策略决策审计

### 9.1 Decision Log

**Decision Log** 记录每次策略决策：

- **Who**：谁发起的请求
- **What**：请求的内容
- **Why**：决策的原因（规则匹配）

### 9.2 审计集成

**审计工具集成**：

- **Loki**：日志聚合
- **Elasticsearch**：日志搜索
- **Prometheus**：指标收集

## 10. 形式化定义

### 10.1 OPA 映射定义

```text
OPA: Input → Decision
其中：
- Input: JSON 输入
- Decision: {allow: bool, deny: string[], variables: map}
```

### 10.2 决策确定性

```text
∀ i ∈ Input, ∃! d ∈ Decision
使得 d = OPA(i) 且 d 在有限步内唯一且可重现
```

### 10.3 版本一致性

```text
Policy Δ ≃ Code Δ
其中：
- Policy Δ: 策略变更（Git SHA）
- Code Δ: 代码变更（Git SHA）
- ≃: 版本一致
```

## 11. 总结

通过**安全形式化**，OPA 实现了：

1. **把"安全"变成数据 + 规则**：从不可量化的运维玄学变成可形式化的 DSL
2. **决策确定性**：决策在有限步内唯一且可重现
3. **可证明性**：策略决策等价于 SAT 问题，可自动验证
4. **版本一致性**：策略与代码同步版本化
5. **可审计性**：所有决策可审计和追溯

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
1992-2007 行，安全形式化部分
