# 矩阵模板与思维导图：一体化方案

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
- [2 矩阵模板（20×20 可折叠）](#2-矩阵模板2020-可折叠)
- [3 思维导图节点规范](#3-思维导图节点规范)
- [4 折叠/展开规则](#4-折叠展开规则)
- [5 动态索引](#5-动态索引)
- [6 使用流程](#6-使用流程)
- [7 参考](#7-参考)

---

## 1 概述

**矩阵模板与思维导图**是一体化方案，将**20×20 复合运算表**与**思维导图**结合，让
"查表"像"看地铁线路图"一样直观。

**核心思想**：

- **矩阵** = 可折叠的对比表（20×20）
- **导图** = 层级与颜色编码的节点树
- **联动** = 矩阵与导图同步更新

**适用工具**：

- **Excel**：矩阵表格，支持条件格式化
- **Notion**：数据库视图，支持公式计算
- **Miro**：思维导图，支持拖拽连线

---

## 2 矩阵模板（20×20 可折叠）

**矩阵结构**：

| 维度 →    | 延迟 | 安全 | 观测 | 资源 | 易用 | 冷启 | 合规 | 成本 | 备注                   | 导图色 |
| --------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---------------------- | ------ |
| **I**∘    | 5▼   | 3▲   | 5▼   | 5▼   | 5▼   | 5▼   | 3▲   | 5▼   | 镜像幂等               | 🟦     |
| **C**∘    | 5▼   | 3▲   | 5▼   | 4▼   | 5▼   | 5▼   | 4▼   | 5▼   | 容器理想               | 🟦     |
| **S**∘    | 5▼   | 5▼   | 4▼   | 5▼   | 4▼   | 5▼   | 5▼   | 5▼   | syscall 商             | 🟩     |
| **M**∘    | 4▼   | 4▼   | 5▼   | 3▲   | 3▲   | 4▼   | 4▼   | 3▲   | 网格吸收               | 🟨     |
| **V**∘    | 2▲   | 5▼   | 3▲   | 2▲   | 2▲   | 2▲   | 5▼   | 2▲   | VM 环扩张              | 🟥     |
| **Kc**∘   | 3▲   | 5▼   | 4▼   | 3▲   | 3▲   | 3▲   | 5▼   | 3▲   | Kata MicroVM           | 🟥     |
| **G**∘    | 4▼   | 4▼   | 4▼   | 4▼   | 3▲   | 4▼   | 4▼   | 4▼   | gVisor 用户态内核      | 🟩     |
| **F**∘    | 4▼   | 4▼   | 3▲   | 5▼   | 3▲   | 5▼   | 4▼   | 4▼   | Firecracker microVM    | 🟥     |
| **W**∘    | 5▼   | 3▲   | 4▼   | 5▼   | 4▼   | 5▼   | 3▲   | 5▼   | Wasm 幂等              | 🟪     |
| **We**∘   | 5▼   | 3▲   | 4▼   | 5▼   | 4▼   | 5▼   | 3▲   | 5▼   | WasmEdge               | 🟪     |
| **Am**∘   | 5▼   | 4▼   | 5▼   | 5▼   | 4▼   | 5▼   | 4▼   | 4▼   | Istio Ambient          | 🟨     |
| **P**∘    | 5▼   | 4▼   | 5▼   | 5▼   | 3▲   | 5▼   | 4▼   | 5▼   | eBPF 程序              | 🟩     |
| **Ns**∘   | 5▼   | 3▲   | 4▼   | 5▼   | 5▼   | 5▼   | 3▲   | 5▼   | namespace 理想         | 🟦     |
| **Cg**∘   | 5▼   | 3▲   | 4▼   | 5▼   | 5▼   | 5▼   | 3▲   | 5▼   | cgroup 理想            | 🟦     |
| **O**∘    | 5▼   | 3▲   | 4▼   | 5▼   | 5▼   | 5▼   | 3▲   | 5▼   | OverlayFS              | 🟦     |
| **E**∘    | 4▼   | 5▼   | 4▼   | 3▲   | 3▲   | 3▲   | 5▼   | 3▲   | Envoy 代理             | 🟨     |
| **Ist**∘  | 4▼   | 4▼   | 5▼   | 3▲   | 3▲   | 4▼   | 4▼   | 3▲   | Istio 控制面           | 🟨     |
| **Otel**∘ | 5▼   | 4▼   | 5▼   | 5▼   | 4▼   | 5▼   | 4▼   | 5▼   | OpenTelemetry          | 🟩     |
| **Gk**∘   | 4▼   | 5▼   | 4▼   | 5▼   | 3▲   | 5▼   | 5▼   | 5▼   | Gatekeeper OPA         | 🟩     |
| **Cc**∘   | 3▲   | 5▼   | 4▼   | 3▲   | 3▲   | 3▲   | 5▼   | 2▲   | Confidential Container | 🟥     |

**色块 = 思维导图一级分支**：

- 🟦 **打包/隔离**：I, C, Ns, Cg, O
- 🟩 **安全/观测**：S, G, P, Otel, Gk
- 🟨 **流量/治理**：M, Am, E, Ist
- 🟥 **虚拟化/机密**：V, Kc, F, Cc
- 🟪 **Wasm/边缘**：W, We

**评分说明**：

- **1▲** = 最低（最差）
- **5▼** = 最高（最好）
- **延迟**：越低越好（5▼ 表示延迟最低）
- **安全**：越高越好（5▼ 表示安全最高）
- **观测**：越高越好（5▼ 表示可观测性最高）

---

## 3 思维导图节点规范

**Xmind/Miro 快速导入格式**：

```text
根: Cloud-Native Operators
├─ 🟦 Pack&Isolate (I,C,Ns,Cg,O)
│  ├─ I: 镜像幂等, layer hash
│  ├─ C: 容器理想, namespace+cgroup
│  └─ O: OverlayFS, 联合挂载
├─ 🟩 Sec&Observe (S,P,Gk,Otel,Fc)
│  ├─ S: syscall 商, seccomp
│  ├─ P: eBPF 程序, 5▼延迟
│  └─ Gk: Gatekeeper, 云原生策略
├─ 🟨 Traffic&Mesh (M,E,Ist,Am,Dr)
│  ├─ M: 网格吸收, mTLS
│  ├─ Am: Ambient, 无 Sidecar
│  └─ E: Envoy, L4/L7
├─ 🟥 Virt&Confidential (V,Kc,F,G,Cc)
│  ├─ V: VM 环扩张, 2▲延迟
│  ├─ Kc: Kata, microVM
│  └─ Cc: SGX/SEV, 机密容器
└─ 🟪 Wasm&Edge (W,We,Kn,Keda)
   ├─ W: 幂等, <50 MB
   └─ We: WasmEdge, 冷启 10 ms
```

**连线规则**：

- **实线** = 可交换（`C∘S = S∘C`）
- **虚线** = 非交换（`V∘C ≠ C∘V`）
- **颜色渐变** = 复合后得分区间（绿 → 红）

**节点属性**：

- **颜色**：对应色块（🟦、🟩、🟨、🟥、🟪）
- **大小**：表示使用频率
- **形状**：表示算子类型（圆形=幂等，方形=非幂等）

---

## 4 折叠/展开规则

**矩阵 = 导图联动**：

| 手势         | 矩阵动作         | 导图动作                    |
| ------------ | ---------------- | --------------------------- |
| **点击色块** | 隐藏其他色列     | 折叠非同色节点              |
| **双击算子** | 仅留该算子行     | 高亮该分支+子节点           |
| **拖拽复合** | 自动生成 `I∘C∘S` | 在导图生成新节点"ICS"并连线 |

**实现方式**：

1. **Excel**：使用 `FILTER` 和 `CONDITIONAL FORMATTING`
2. **Notion**：使用 `filter` 和 `formula` 属性
3. **Miro**：使用 `API` 和 `Webhook` 同步

---

## 5 动态索引

**Excel 公式**（可直接用）：

```excel
=INDEX($B$2:$K$21, MATCH("C", $A$2:$A$21, 0), MATCH("安全", $B$1:$K$1, 0))
→ 返回 3▲
```

**Notion 模板**：

```notion
filter(prop("算子"), prop("导图色") == "🟦")
→ 列出所有打包隔离算子
```

**Python 脚本**：

```python
import pandas as pd

# 读取矩阵
df = pd.read_excel('operator_matrix.xlsx')

# 查询算子指标
def get_metric(operator, dimension):
    return df.loc[df['算子'] == operator, dimension].values[0]

# 示例
latency = get_metric('C', '延迟')  # 返回 5▼
security = get_metric('C', '安全')  # 返回 3▲
```

---

## 6 使用流程

**三步决策流程**：

1. **需求 → 算子串**

   - 例："高密+高安+冷启<30 ms" → 优先色 🟩+🟪+🟦

2. **矩阵查行**

   - 同时看 S、We、C 三行，取交集最高分 → **S∘We∘C**

3. **导图验证**
   - 在 🟩→🟪→🟦 路径上拖线，自动生成节点"SWC"并标绿

**示例**：

```text
需求: 高密+高安+冷启<30 ms
  ↓
算子串: S∘We∘C
  ↓
查表: (Latency=5▼, Security=4▼, Observability=4▼)
  ↓
技术栈: seccomp + WasmEdge + crun
  ↓
验证: 在导图上拖线，确认路径 🟩→🟪→🟦
```

---

## 7 参考

**关联文档**：

- **[复合运算表](04-composition-table.md)** - 20×20 完整运算表
- **[实践案例](08-practical-examples.md)** - 矩阵查询的实际应用
- **[快速参考](QUICK-REFERENCE.md)** - 算子表和运算表速查

**工具参考**：

- [Excel Conditional Formatting](https://support.microsoft.com/en-us/office/use-conditional-formatting-to-highlight-information-fed60dfa-1d3f-4e13-9ecb-f1951ff89d7f)
- [Notion Formula Reference](https://www.notion.so/help/formulas)
- [Miro API Documentation](https://developers.miro.com/docs/api-reference)

---

**最后更新**：2025-11-04 **维护者**：项目团队
