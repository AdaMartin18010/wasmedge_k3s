# 三、风险调整后的期望效用

> **文档版本**：v1.0 **最后更新：2025-11-15 **维护者**：项目团队

---

## 📑 目录

- [三、风险调整后的期望效用](#三风险调整后的期望效用)
  - [📑 目录](#-目录)
  - [概述](#概述)
  - [一、期望效用定义](#一期望效用定义)
    - [1.1 期望效用计算](#11-期望效用计算)
    - [1.2 效用函数](#12-效用函数)
    - [1.3 概率分布](#13-概率分布)
  - [二、风险调整](#二风险调整)
    - [2.1 风险调整定义](#21-风险调整定义)
    - [2.2 风险厌恶系数](#22-风险厌恶系数)
    - [2.3 风险偏好系数](#23-风险偏好系数)
  - [三、风险调整后的期望效用](#三风险调整后的期望效用-1)
    - [3.1 风险调整后的期望效用计算](#31-风险调整后的期望效用计算)
    - [3.2 风险调整对比](#32-风险调整对比)
    - [3.3 风险调整优化](#33-风险调整优化)
  - [四、形式化验证](#四形式化验证)
    - [4.1 期望效用范围验证](#41-期望效用范围验证)
    - [4.2 风险调整单调性验证](#42-风险调整单调性验证)
  - [相关文档](#相关文档)

---

## 概述

本文档从**决策理论**和**风险理论**的视角形式化分析风险调整后的期望效用，将期望效
用、风险调整、风险厌恶系数等概念抽象为数学结构，建立风险调整后的期望效用的严格数
学模型。

**为什么使用决策理论和风险理论分析风险调整后的期望效用？**

决策理论和风险理论提供了统一的数学框架来描述风险调整后的期望效用的结构和行为：

1. **统一抽象**：通过决策理论和风险理论，我们可以将期望效用、风险调整、风险厌恶
   系数等抽象为数学结构，实现统一的数学描述
2. **风险量化**：通过风险调整，我们可以量化决策中的风险
3. **决策支持**：通过风险调整后的期望效用，我们可以为决策提供支持

**决策理论和风险理论在风险调整后的期望效用分析中的应用**：

- **期望效用（Expected Utility）**：期望效用，描述决策的期望收益
- **风险调整（Risk Adjustment）**：风险调整，描述对风险的调整
- **风险厌恶系数（Risk Aversion Coefficient）**：风险厌恶系数，描述决策者对风险
  的厌恶程度

**核心内容**：

1. **期望效用**：`E[U] = Σ_{i} P(outcome_i) × U(outcome_i)`
2. **风险调整**：`U_risk_adjusted = E[U] - λ·Var[U]`
3. **风险厌恶系数**：`λ > 0`（风险厌恶）
4. **风险偏好系数**：`λ < 0`（风险偏好）
5. **形式化验证**：期望效用范围、风险调整单调性验证

---

## 一、期望效用定义

### 1.1 期望效用计算

**风险调整后的期望效用**：

```haskell
-- 期望效用类型
data ExpectedUtility = Utility {
    outcomes :: [Outcome],
    probabilities :: [Double],
    utilities :: [Double],
    expected :: Double
}

-- 期望效用计算
expectedUtility :: [Outcome] -> [Double] -> [Double] -> Double
expectedUtility outcomes probabilities utilities =
    sum [p * u | (p, u) <- zip probabilities utilities]
```

**形式化定义**：

```text
E[U] = Σ_{i} p_i·u(outcome_i) - λ·Risk(architecture)
```

其中：

- **p_i**：结果 i 的概率
- **u(outcome_i)**：结果 i 的效用
- **λ**：风险厌恶系数
- **Risk(architecture)**：架构的风险

### 1.2 效用函数

**效用函数**：

```haskell
-- 效用函数类型
data UtilityFunction = Utility {
    function :: Outcome -> Double,
    domain :: [Outcome],
    range :: [Double]
}

-- 效用函数实例
utilityFunction = Utility {
    function = \outcome ->
        case outcome of
            KubeVirt -> 0.8
            BareMetalK8s -> 0.9
            SmartXSKS -> 0.85,
    domain = [KubeVirt, BareMetalK8s, SmartXSKS],
    range = [0.8, 0.9, 0.85]
}
```

**形式化定义**：

```text
效用函数：
U: Outcome → [0, 1]
U(KubeVirt) = 0.8
U(BareMetalK8s) = 0.9
U(SmartXSKS) = 0.85
```

### 1.3 概率分布

**概率分布**：

```haskell
-- 概率分布类型
data ProbabilityDistribution = Distribution {
    outcomes :: [Outcome],
    probabilities :: [Double]
}

-- 概率分布实例
probabilityDistribution = Distribution {
    outcomes = [KubeVirt, BareMetalK8s, SmartXSKS],
    probabilities = [0.3, 0.4, 0.3]
}
```

**形式化定义**：

```text
概率分布：
P: Outcome → [0, 1]
P(KubeVirt) = 0.3
P(BareMetalK8s) = 0.4
P(SmartXSKS) = 0.3
```

**概率分布性质**：

1. **非负性**：`∀outcome, P(outcome) ≥ 0`
2. **归一性**：`Σ_{outcome} P(outcome) = 1`
3. **可加
   性**：`∀outcome₁, outcome₂, P(outcome₁ ∪ outcome₂) = P(outcome₁) + P(outcome₂)`

---

## 二、风险调整

### 2.1 风险调整定义

**风险调整**：

```haskell
-- 风险调整类型
data RiskAdjustment = Adjustment {
    expectedUtility :: Double,
    variance :: Double,
    riskAversion :: Double,
    adjustedUtility :: Double
}

-- 风险调整计算
riskAdjustment :: Double -> Double -> Double -> Double
riskAdjustment expectedUtility variance riskAversion =
    expectedUtility - riskAversion * variance
```

**形式化定义**：

```text
风险调整后的期望效用：
U_risk_adjusted = E[U] - λ·Var[U]
```

其中：

- **E[U]**：期望效用
- **Var[U]**：效用方差
- **λ**：风险厌恶系数

### 2.2 风险厌恶系数

**风险厌恶系数** `λ`：

```haskell
-- 风险厌恶系数类型
data RiskAversionCoefficient = Coefficient {
    lambda :: Double,
    type :: RiskType
}

-- 风险厌恶系数实例
riskAversionCoefficient = Coefficient {
    lambda = 0.5,
    type = RiskAverse  -- λ > 0：风险厌恶
}
```

**形式化定义**：

```text
风险厌恶系数：
λ > 0：风险厌恶
λ = 0：风险中性
λ < 0：风险偏好
```

**风险厌恶系数对比**：

| **架构**         | **风险厌恶系数 λ** | **风险类型** | **说明** |
| ---------------- | ------------------ | ------------ | -------- |
| **KubeVirt**     | 0.5                | 风险厌恶     | 中等风险 |
| **BareMetalK8s** | 0.3                | 风险厌恶     | 低风险   |
| **SmartXSKS**    | 0.2                | 风险厌恶     | 低风险   |

其中 `Risk(KubeVirt) > Risk(SKS)`。

### 2.3 风险偏好系数

**风险偏好系数**：

```haskell
-- 风险偏好系数实例
riskPreferenceCoefficient = Coefficient {
    lambda = -0.3,
    type = RiskSeeking  -- λ < 0：风险偏好
}
```

**形式化定义**：

```text
风险偏好系数：
λ < 0：风险偏好
```

**风险偏好系数对比**：

| **架构**         | **风险偏好系数 λ** | **风险类型** | **说明**     |
| ---------------- | ------------------ | ------------ | ------------ |
| **KubeVirt**     | -0.2               | 风险偏好     | 高风险高收益 |
| **BareMetalK8s** | -0.1               | 风险偏好     | 中等风险     |
| **SmartXSKS**    | -0.05              | 风险偏好     | 低风险       |

---

## 三、风险调整后的期望效用

### 3.1 风险调整后的期望效用计算

**风险调整后的期望效用**：

```haskell
-- 风险调整后的期望效用计算
computeRiskAdjustedUtility :: ExpectedUtility -> RiskAdjustment -> Double
computeRiskAdjustedUtility utility adjustment =
    let expected = expected utility
        variance = computeVariance utility
        lambda = riskAversion adjustment
    in expected - lambda * variance
```

**形式化定义**：

```text
风险调整后的期望效用：
U_risk_adjusted = E[U] - λ·Var[U]
```

**风险调整后的期望效用对比**：

| **架构**         | **期望效用 E[U]** | **方差 Var[U]** | **风险厌恶系数 λ** | **风险调整后的期望效用** |
| ---------------- | ----------------- | --------------- | ------------------ | ------------------------ |
| **KubeVirt**     | 0.8               | 0.1             | 0.5                | 0.75                     |
| **BareMetalK8s** | 0.9               | 0.05            | 0.3                | 0.885                    |
| **SmartXSKS**    | 0.85              | 0.03            | 0.2                | 0.844                    |

### 3.2 风险调整对比

**风险调整对比**：

| **架构**         | **无风险调整** | **风险调整后** | **差异** |
| ---------------- | -------------- | -------------- | -------- |
| **KubeVirt**     | 0.8            | 0.75           | -6.25%   |
| **BareMetalK8s** | 0.9            | 0.885          | -1.67%   |
| **SmartXSKS**    | 0.85           | 0.844          | -0.71%   |

**形式化定义**：

```text
风险调整影响：
ΔU = U_risk_adjusted - E[U] = -λ·Var[U]
```

### 3.3 风险调整优化

**风险调整优化**：

```haskell
-- 风险调整优化
optimizeRiskAdjustment :: ExpectedUtility -> RiskAdjustment -> RiskAdjustment
optimizeRiskAdjustment utility adjustment =
    let optimalLambda = optimizeLambda utility
        optimized = adjustment {riskAversion = optimalLambda}
    in optimized
```

**形式化定义**：

```text
风险调整优化：
optimize: RiskAdjustment → RiskAdjustment
optimize(A) = A' 其中 U_risk_adjusted(A') ≥ U_risk_adjusted(A)
```

---

## 四、形式化验证

### 4.1 期望效用范围验证

**期望效用范围定理**：

```text
□(∀utility ∈ ExpectedUtility, E[U] ∈ [0, 1])
```

**形式化验证**：

```haskell
-- 期望效用范围验证
verifyExpectedUtilityRange :: ExpectedUtility -> Bool
verifyExpectedUtilityRange utility =
    let expected = expected utility
    in expected >= 0.0 && expected <= 1.0
```

**期望效用范围性质**：

1. **下界**：`∀utility, E[U] ≥ 0`
2. **上界**：`∀utility, E[U] ≤ 1`
3. **归一性**：`∀utility, E[U] ∈ [0, 1]`

### 4.2 风险调整单调性验证

**风险调整单调性定理**：

```text
□(∀utility₁, utility₂ ∈ ExpectedUtility,
  Var[U₁] > Var[U₂] ∧ λ > 0 →
  U_risk_adjusted(utility₁) < U_risk_adjusted(utility₂))
```

**形式化验证**：

```haskell
-- 风险调整单调性验证
verifyRiskAdjustmentMonotonicity :: ExpectedUtility -> ExpectedUtility -> Double -> Bool
verifyRiskAdjustmentMonotonicity utility1 utility2 lambda =
    let variance1 = computeVariance utility1
        variance2 = computeVariance utility2
        adjusted1 = computeRiskAdjustedUtility utility1 (RiskAdjustment 0 variance1 lambda)
        adjusted2 = computeRiskAdjustedUtility utility2 (RiskAdjustment 0 variance2 lambda)
    in variance1 > variance2 && lambda > 0 → adjusted1 < adjusted2
```

**风险调整单调性性质**：

1. **单调递
   减**：`∀utility₁, utility₂, Var[U₁] > Var[U₂] ∧ λ > 0 → U_risk_adjusted(utility₁) < U_risk_adjusted(utility₂)`
2. **单调递
   增**：`∀utility₁, utility₂, Var[U₁] < Var[U₂] ∧ λ < 0 → U_risk_adjusted(utility₁) > U_risk_adjusted(utility₂)`
3. **单调不
   变**：`∀utility₁, utility₂, Var[U₁] = Var[U₂] → U_risk_adjusted(utility₁) = U_risk_adjusted(utility₂)`

---

## 相关文档

- [系统架构的极限构造](./01-system-architecture-limit.md) - 系统架构的极限构造
- [生产环境选型决策树](./02-production-decision-tree.md) - 生产环境选型决策树
- [扩展性极限](./04-extension-limits.md) - 扩展性极限
- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵

---

**最后更新：2025-11-15 **维护者**：项目团队
