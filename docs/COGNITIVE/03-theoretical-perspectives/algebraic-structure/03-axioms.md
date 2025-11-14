# 公理体系：A1-A7

## 📑 目录

- [📑 目录](#-目录)
- [1 公理体系概述](#1-公理体系概述)
- [2 A1：封闭性](#2-a1封闭性)
  - [公理 A1：封闭性](#公理-a1封闭性)
- [3 A2：幂等性](#3-a2幂等性)
  - [公理 A2：幂等性](#公理-a2幂等性)
- [4 A3：非交换性](#4-a3非交换性)
  - [公理 A3：非交换性](#公理-a3非交换性)
- [5 A4：短正合列](#5-a4短正合列)
  - [公理 A4：短正合列](#公理-a4短正合列)
- [6 A5：同态映射](#6-a5同态映射)
  - [公理 A5：同态映射](#公理-a5同态映射)
- [7 A6：吸收元](#7-a6吸收元)
  - [公理 A6：吸收元](#公理-a6吸收元)
- [8 A7：逆元](#8-a7逆元)
  - [公理 A7：逆元](#公理-a7逆元)
- [9 公理体系总结](#9-公理体系总结)
- [10 参考](#10-参考)

---

## 1 公理体系概述

**公理体系**：A1-A7

**核心作用**：约束算子间的交互，保证可归约与可比较。

**公理列表**：

| 公理   | 名称     | 说明                 | 例证                              |
| ------ | -------- | -------------------- | --------------------------------- |
| **A1** | 封闭性   | ∀x∈Ω, ℱ(x)∈Ω         | `C(I(Image)) = Container ∈ Ω`     |
| **A2** | 幂等性   | X² = X (X∈{C,S,M,W}) | `C² = C, S² = S, M² = M`          |
| **A3** | 非交换性 | V∘C ≠ C∘V            | VM-in-container ≠ container-in-VM |
| **A4** | 短正合列 | 0→Ker(S)→Ω→Im(S)→0   | seccomp 过滤                      |
| **A5** | 同态映射 | φ: (Ω,∘)→ℝ³          | φ(C) = (5▼, 3▲, 5▼)               |
| **A6** | 吸收元   | ∅ = No-op; ∀ω, ω∘∅=ω | 省略无操作                        |
| **A7** | 逆元     | 仅 V 有弱逆 V⁻¹      | V⁻¹：硬件解锁                     |

## 2 A1：封闭性

### 公理 A1：封闭性

**名称**：封闭性（Closure）

**定义**：∀x∈Ω, ℱ(x)∈Ω

**解释**：对任何 x∈Ω，算子作用后仍是"技术对象"。

**例证**：

- `C(I(Image)) = Container`（仍在 Ω）
- `S(C(Container)) = Sandbox Container`（仍在 Ω）
- `M(C(Container)) = Mesh Container`（仍在 Ω）

**作用**：保证所有算子结果都属于 Ω，表格中每行/列都合法。

**2025 年更新**：

- 支持 WasmEdge 运行时（W, We）
- 支持 Ambient Mesh（Am）
- 支持机密容器（Cc）

## 3 A2：幂等性

### 公理 A2：幂等性

**名称**：幂等性（Idempotence）

**定义**：X² = X (X∈{C,S,M,W})

**解释**：多次同一算子不产生额外层。

**例证**：

- `C∘C ≃ C`：容器里再容器 ≈ 单层容器
- `S∘S ≃ S`：seccomp 嵌套 ≈ 单层过滤
- `M∘M ≃ M`：服务网格里再服务网格 ≈ 单层服务网格
- `W∘W ≃ W`：WasmEdge 里再 WasmEdge ≈ 单层 WasmEdge

**例外**：

- `V² ≠ I`：嵌套虚拟化需硬件解锁，≠ 恒等

**作用**：让我们可以去掉重复的算子，简化序列。

**2025 年更新**：

- WasmEdge（W, We）满足幂等性
- Ambient Mesh（Am）满足幂等性

## 4 A3：非交换性

### 公理 A3：非交换性

**名称**：非交换性（Non-commutativity）

**定义**：V∘C ≠ C∘V

**解释**：VM 先于容器与容器先于 VM 产生不同的页表。

**例证**：

- `V∘C`：VM-in-container（VM 在容器内）
- `C∘V`：container-in-VM（容器在 VM 内）
- 页表深度不同，性能和安全特性不同

**交换算子**：

- `C∘S = S∘C`：容器后加沙盒 ≡ 沙盒后加容器
- `C∘M = M∘C`：容器后加网格 ≡ 网格后加容器
- `M∘W = W∘M`：网格后加 Wasm ≡ Wasm 后加网格

**作用**：给出唯一的 "V-先" 或 "V-后" 形式。

**2025 年更新**：

- Service Mesh（M）与容器（C）可交换
- Service Mesh（M）与 WasmEdge（W）可交换

## 5 A4：短正合列

### 公理 A4：短正合列

**名称**：短正合列（Short Exact Sequence）

**定义**：0 → Ker(S) → Ω → Im(S) → 0

**解释**：沙箱是一条短正合序列，过滤器是像"商"一样。

**数学表示**：

```text
0 → Ker(S) → Ω → Im(S) → 0
```

其中：

- **Ker(S)**：被过滤的 syscall（核）
- **Im(S)**：允许的 syscall（像）
- **Ω**：所有 syscall（全集）

**例证**：

- `seccomp` 过滤等价于商对象
- `Ker(S) = {被过滤的 syscall}`
- `Im(S) = {允许的 syscall}`
- `Ω = Ker(S) ∪ Im(S)`

**作用**：让 "S" 的安全性被视为 "商对象" 计数。

**2025 年更新**：

- 支持 Landlock（Linux 5.13+）
- 支持 eBPF LSM（Linux 5.7+）
- 支持 Capsicum（FreeBSD）

## 6 A5：同态映射

### 公理 A5：同态映射

**名称**：同态映射（Homomorphism）

**定义**：φ : (Ω,∘) → ℝ³ 使 φ(a∘b) = φ(a)⊕φ(b)

**解释**：在 Latency↑, Security↓, Observability→ 上保持运算分布。

**映射函数**：

```text
φ: (Ω,∘) → ℝ³
  ω ↦ (Latency↑, Security↓, Observability→)
```

**指标说明**：

- **Latency↑**：延迟（越低越好，数值越小越好）
- **Security↓**：安全（越高越好，数值越小越好）
- **Observability→**：可观测性（越高越好，数值越大越好）

**例证**：

- `φ(C) = (5▼, 3▲, 5▼)`
- `φ(S) = (5▼, 4▼, 5▼)`
- `φ(M) = (4▼, 4▼, 5▼)`
- `φ(V) = (2▲, 5▼, 3▲)`

**同态性**：

- `φ(a∘b) = φ(a) ⊕ φ(b)`
- 其中 `⊕` 对应延迟加法、安全取最小、观测取最大

**作用**：让"拉取"指标成为"算子值"+"子值"的"算术和"。

**2025 年更新**：

- Service Mesh（M）指标：Latency 4▼, Security 4▼, Observability 5▼
- Ambient Mesh（Am）指标：Latency 5▼, Security 4▼, Observability 5▼

## 7 A6：吸收元

### 公理 A6：吸收元

**名称**：吸收元（Absorbing Element）

**定义**：∅ = No-op; ∀ω, ω∘∅ = ω

**解释**：省略"无操作"不影响后续算子。

**例证**：

- `C∘∅ = C`（无操作不影响容器化）
- `S∘∅ = S`（无操作不影响沙盒化）
- `M∘∅ = M`（无操作不影响服务网格注入）

**作用**：简化不必要的 `∅`。

## 8 A7：逆元

### 公理 A7：逆元

**名称**：逆元（Inverse Element）

**定义**：仅 V 有弱逆 V⁻¹；其余无逆。

**解释**：仅虚拟化有弱逆（硬件解锁），其他算子无逆。

**例证**：

- `V⁻¹`：硬件解锁 VM（嵌套虚拟化）
- `C⁻¹`：不存在（容器化不可逆）
- `S⁻¹`：不存在（沙盒化不可逆）
- `M⁻¹`：不存在（服务网格注入不可逆）

**作用**：确定"V"只能出现在序列开头或结尾。

**2025 年更新**：

- 支持嵌套虚拟化（Intel VT-x/AMD-V）
- 支持机密计算（SGX/SEV）

## 9 公理体系总结

**公理体系完整性**：

| 公理   | 作用     | 保证                                      |
| ------ | -------- | ----------------------------------------- |
| **A1** | 封闭性   | 所有算子结果都属于 Ω                      |
| **A2** | 幂等性   | 可以去掉重复的算子                        |
| **A3** | 非交换性 | 给出唯一的 "V-先" 或 "V-后" 形式          |
| **A4** | 短正合列 | 让 "S" 的安全性被视为 "商对象" 计数       |
| **A5** | 同态映射 | 让"拉取"指标成为"算子值"+"子值"的"算术和" |
| **A6** | 吸收元   | 简化不必要的 `∅`                          |
| **A7** | 逆元     | 确定"V"只能出现在序列开头或结尾           |

**公理体系验证**：

- ✅ 所有算子满足封闭性（A1）
- ✅ C, S, M, W 满足幂等性（A2）
- ✅ V 与 C, S, M 非交换（A3）
- ✅ S 满足短正合列（A4）
- ✅ φ 映射满足同态性（A5）
- ✅ ∅ 满足吸收元性质（A6）
- ✅ V 有弱逆 V⁻¹（A7）

## 10 参考

**关联文档**：

- **[代数结构](02-algebraic-structure.md)** - 代数结构 Σ = ⟨Ω, ℱ, 𝒫, ℒ⟩
- **[复合运算表](04-composition-table.md)** - 20×20 运算表
- **[最简范式定理](05-normal-form-theorem.md)** - 主范式定理
- **[公理系统性质证明](../../ARCHITECTURE/00-theory/03-axiom-properties/axiom-properties-proofs.md)**
  ⭐ - 独立性、一致性、完备性证明
- **[形式化定义](../../ARCHITECTURE/00-theory/04-formal-definitions/formal-definitions.md)**
  ⭐ - 集合、函数与类型系统的严格定义

**外部参考**：

- [Axiom (Wikipedia)](https://en.wikipedia.org/wiki/Axiom)
- [Idempotence (Wikipedia)](https://en.wikipedia.org/wiki/Idempotence)
- [Homomorphism (Wikipedia)](https://en.wikipedia.org/wiki/Homomorphism)
- [Exact Sequence (Wikipedia)](https://en.wikipedia.org/wiki/Exact_sequence)
- [Model Theory (Wikipedia)](https://en.wikipedia.org/wiki/Model_theory)
- [Proof Theory (Wikipedia)](https://en.wikipedia.org/wiki/Proof_theory)

---

**最后更新**：2025-11-04 **维护者**：项目团队
