# 随机过程：调度过程的随机性分析

> **文档版本**：v1.0 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
- [2 随机调度模型](#2-随机调度模型)
  - [2.1 Pod 到达过程](#21-pod-到达过程)
  - [2.2 服务时间分布](#22-服务时间分布)
  - [2.3 节点故障过程](#23-节点故障过程)
- [3 排队论模型](#3-排队论模型)
  - [3.1 M/M/1 模型](#31-mm1-模型)
  - [3.2 M/M/c 模型](#32-mmc-模型)
  - [3.3 M/G/1 模型](#33-mg1-模型)
- [4 概率分析](#4-概率分析)
  - [4.1 调度延迟分布](#41-调度延迟分布)
  - [4.2 系统负载分布](#42-系统负载分布)
  - [4.3 资源利用率分布](#43-资源利用率分布)
- [5 随机优化](#5-随机优化)
  - [5.1 随机调度策略](#51-随机调度策略)
  - [5.2 概率约束](#52-概率约束)
  - [5.3 随机算法](#53-随机算法)
- [6 实际应用](#6-实际应用)
  - [6.1 Kubernetes 调度器](#61-kubernetes-调度器)
  - [6.2 YARN 调度器](#62-yarn-调度器)
  - [6.3 实际案例分析](#63-实际案例分析)
    - [6.3.1 电商大促场景](#631-电商大促场景)
    - [6.3.2 微服务调用链场景](#632-微服务调用链场景)
    - [6.3.3 批处理任务调度场景](#633-批处理任务调度场景)
- [7 形式化证明](#7-形式化证明)
  - [7.1 Little's Law 证明](#71-littles-law-证明)
  - [7.2 M/M/1 队列长度分布证明](#72-mm1-队列长度分布证明)
- [8 相关文档](#8-相关文档)
- [9 参考](#9-参考)
  - [学术参考](#学术参考)
  - [实践参考](#实践参考)

---

## 1 概述

**随机过程**是分析调度过程随机性的方法。调度系统具有多种随机性：Pod 到达的随机性
、服务时间的随机性、节点故障的随机性等。随机过程理论提供了分析这些随机性的数学工
具。

**核心目标**：

1. **建立随机模型**：将调度过程建模为随机过程
2. **概率分析**：分析系统指标的概率分布
3. **性能预测**：预测系统在不同负载下的性能
4. **优化设计**：设计随机优化策略

**为什么需要随机过程分析？**

调度系统的随机性使得确定性分析无法完全描述系统行为：

1. **随机到达**：Pod 的到达是随机的，无法精确预测
2. **随机服务时间**：Pod 的服务时间是随机的，受多种因素影响
3. **随机故障**：节点故障是随机的，需要概率模型分析
4. **不确定性**：系统行为具有不确定性，需要概率保证

**随机过程的核心内容**：

1. **随机模型**：建立调度过程的随机模型（Poisson 过程、Markov 链等）
2. **概率分布**：分析系统指标的概率分布（延迟、负载、利用率等）
3. **排队论**：使用排队论分析调度系统（M/M/1、M/M/c、M/G/1 等）
4. **随机优化**：设计随机优化策略（概率约束、随机算法等）

---

## 2 随机调度模型

### 2.1 Pod 到达过程

**定义**：Pod 到达过程是 Pod 到达调度队列的随机过程。

**Poisson 过程模型**：

```text
Pod 到达过程 ~ Poisson(λ)
其中：
- λ: 到达率（单位时间内到达的 Pod 数量）
- 到达间隔时间 ~ Exponential(λ)
```

**到达过程特性**：

1. **无记忆性**：到达间隔时间具有无记忆性
2. **独立性**：不同 Pod 的到达相互独立
3. **平稳性**：到达率在时间上平稳

**到达率估计**：

```text
到达率估计：
  λ = N / T

  其中：
  - N: 时间 T 内到达的 Pod 数量
  - T: 观察时间
```

**实际应用**：

- **负载预测**：根据历史到达率预测未来负载
- **容量规划**：根据到达率规划系统容量
- **性能分析**：分析不同到达率下的系统性能

---

### 2.2 服务时间分布

**定义**：服务时间分布是 Pod 在节点上运行时间的分布。

**服务时间模型**：

```text
服务时间 ~ Exponential(μ) 或 General Distribution
其中：
- μ: 服务率（单位时间内完成的 Pod 数量）
- 平均服务时间 = 1/μ
```

**服务时间特性**：

1. **随机性**：服务时间是随机的
2. **分布特性**：可能服从指数分布、正态分布等
3. **负载相关**：服务时间可能与系统负载相关

**服务时间估计**：

```text
服务时间估计：
  μ = 1 / E[ServiceTime]

  其中 E[ServiceTime] 是平均服务时间。
```

**实际应用**：

- **资源规划**：根据服务时间规划资源
- **性能优化**：优化服务时间分布
- **SLA 保证**：根据服务时间保证 SLA

---

### 2.3 节点故障过程

**定义**：节点故障过程是节点发生故障的随机过程。

**故障过程模型**：

```text
节点故障过程 ~ Poisson(γ)
其中：
- γ: 故障率（单位时间内节点故障的概率）
- 故障间隔时间 ~ Exponential(γ)
```

**故障过程特性**：

1. **随机性**：节点故障是随机的
2. **独立性**：不同节点的故障相互独立
3. **可恢复性**：节点故障后可以恢复

**故障率估计**：

```text
故障率估计：
  γ = F / (N × T)

  其中：
  - F: 时间 T 内节点故障次数
  - N: 节点数量
  - T: 观察时间
```

**实际应用**：

- **可靠性分析**：分析系统可靠性
- **容错设计**：设计容错机制
- **恢复策略**：设计故障恢复策略

---

## 3 排队论模型

### 3.1 M/M/1 模型

**定义**：M/M/1 模型是单服务器排队模型。

**模型假设**：

1. **到达过程**：Poisson 过程（M）
2. **服务时间**：指数分布（M）
3. **服务器数量**：1 个（1）

**性能指标**：

$$
\begin{align}
\text{系统利用率} &: \rho = \frac{\lambda}{\mu} \\
\text{平均队列长度} &: L = \frac{\rho}{1-\rho} = \frac{\lambda}{\mu - \lambda} \\
\text{平均等待时间} &: W = \frac{L}{\lambda} = \frac{1}{\mu - \lambda} \\
\text{平均响应时间} &: R = W + \frac{1}{\mu} = \frac{1}{\mu - \lambda}
\end{align}
$$

**Little's Law（利特尔法则）**：

$$
L = \lambda \times W
$$

该公式在任意排队系统中都成立，是排队论的基本定律。

**队列长度分布**：

$$
P_n = (1-\rho)\rho^n, \quad n = 0, 1, 2, ...
$$

其中 $P_n$ 是系统中有 $n$ 个顾客的概率。

**稳定性条件**：

```text
稳定性条件：
  ρ = λ/μ < 1

  如果 ρ ≥ 1，系统不稳定，队列长度会无限增长。
```

**调度系统应用**：

```text
调度系统 M/M/1 模型：
  - 到达率 λ: Pod 到达率
  - 服务率 μ: 调度器处理率
  - 利用率 ρ: 调度器利用率
  - 等待时间 W: Pod 调度等待时间
```

---

### 3.2 M/M/c 模型

**定义**：M/M/c 模型是多服务器排队模型。

**模型假设**：

1. **到达过程**：Poisson 过程（M）
2. **服务时间**：指数分布（M）
3. **服务器数量**：c 个（c）

**性能指标**：

$$
\begin{align}
\text{系统利用率} &: \rho = \frac{\lambda}{c \times \mu} \\
\text{平均队列长度} &: L = L_q + c \times \rho \\
\text{平均等待时间} &: W = \frac{L_q}{\lambda} \\
\text{平均响应时间} &: R = W + \frac{1}{\mu}
\end{align}
$$

**队列长度概率**：

$$
P_0 = \left[ \sum_{n=0}^{c-1} \frac{(\lambda/\mu)^n}{n!} + \frac{(\lambda/\mu)^c}{c!} \cdot \frac{1}{1-\rho} \right]^{-1}
$$

$$
P_n = \begin{cases}
\frac{(\lambda/\mu)^n}{n!} P_0 & \text{if } n < c \\
\frac{(\lambda/\mu)^n}{c! c^{n-c}} P_0 & \text{if } n \ge c
\end{cases}
$$

**平均队列长度（等待队列）**：

$$
L_q = \frac{(\lambda/\mu)^c \rho}{c!(1-\rho)^2} P_0
$$

**稳定性条件**：

```text
稳定性条件：
  ρ = λ/(c×μ) < 1
```

**调度系统应用**：

```text
调度系统 M/M/c 模型：
  - 到达率 λ: Pod 到达率
  - 服务率 μ: 单个调度器的处理率
  - 服务器数 c: 调度器数量
  - 利用率 ρ: 调度器利用率
```

---

### 3.3 M/G/1 模型

**定义**：M/G/1 模型是单服务器、一般服务时间分布的排队模型。

**模型假设**：

1. **到达过程**：Poisson 过程（M）
2. **服务时间**：一般分布（G）
3. **服务器数量**：1 个（1）

**性能指标（Pollaczek-Khintchine 公式）**：

$$
\begin{align}
\text{系统利用率} &: \rho = \lambda \times E[S] \\
\text{平均队列长度} &: L = \rho + \frac{\rho^2 + \lambda^2 \times \text{Var}[S]}{2(1-\rho)} \\
\text{平均等待时间} &: W = \frac{L}{\lambda} = \frac{\rho^2 + \lambda^2 \times \text{Var}[S]}{2\lambda(1-\rho)} \\
\text{平均响应时间} &: R = W + E[S]
\end{align}
$$

其中：

- $E[S]$：平均服务时间
- $\text{Var}[S]$：服务时间方差
- $\rho = \lambda \times E[S]$：系统利用率

**Pollaczek-Khintchine 公式的意义**：

该公式表明，平均等待时间不仅依赖于利用率 $\rho$，还依赖于服务时间的方差
$\text{Var}[S]$。服务时间方差越大，平均等待时间越长。

**特殊情况**：

- **M/M/1**：$\text{Var}[S] = 1/\mu^2$，则 $W = \frac{\rho}{\mu(1-\rho)}$
- **M/D/1**（确定服务时间）：$\text{Var}[S] = 0$，则
  $W = \frac{\rho}{2\mu(1-\rho)}$

**调度系统应用**：

```text
调度系统 M/G/1 模型：
  - 到达率 λ: Pod 到达率
  - 服务时间 S: 调度时间（一般分布）
  - 利用率 ρ: 调度器利用率
```

---

## 4 概率分析

### 4.1 调度延迟分布

**定义**：调度延迟分布是 Pod 调度延迟的概率分布。

**延迟模型**：

```text
调度延迟 ~ General Distribution
可能服从：
  - 指数分布：如果服务时间是指数分布
  - 正态分布：如果服务时间是正态分布
  - 混合分布：如果服务时间是混合分布
```

**延迟分位数**：

对于 M/M/1 模型，延迟分布为指数分布：

$$
P(\text{Latency} \le t) = 1 - e^{-(\mu - \lambda)t}
$$

**分位数计算**：

$$
P_{p} = \frac{-\ln(1-p)}{\mu - \lambda}
$$

其中 $p$ 是分位数（如 0.95 表示 P95）。

**典型分位数**：

- **P50（中位数
  ）**：$P_{0.5} = \frac{-\ln(0.5)}{\mu - \lambda} = \frac{0.693}{\mu - \lambda}$
- **P95**：$P_{0.95} = \frac{-\ln(0.05)}{\mu - \lambda} = \frac{2.996}{\mu - \lambda} \approx 3 \times P_{0.5}$
- **P99**：$P_{0.99} = \frac{-\ln(0.01)}{\mu - \lambda} = \frac{4.605}{\mu - \lambda} \approx 4.6 \times P_{0.5}$

**延迟保证（SLA）**：

$$
P(\text{Latency} \le \text{threshold}) \ge \text{SLA}
$$

例如，要求 95% 的请求延迟小于 100ms：

$$
P(\text{Latency} \le 100\text{ms}) \ge 0.95
$$

对于 M/M/1 模型，这要求：

$$
1 - e^{-(\mu - \lambda) \times 0.1} \ge 0.95
$$

解得：

$$
\mu - \lambda \ge \frac{-\ln(0.05)}{0.1} \approx 30 \text{ requests/s}
$$

---

### 4.2 系统负载分布

**定义**：系统负载分布是系统负载的概率分布。

**负载模型**：

```text
系统负载 ~ General Distribution
可能服从：
  - 正态分布：如果负载变化平稳
  - 指数分布：如果负载变化剧烈
  - 混合分布：如果负载有多个模式
```

**负载预测**：

```text
负载预测：
  E[Load(t+1)] = f(Load(t), Load(t-1), ..., Load(t-k))

  其中 f 是预测函数（如 ARIMA、LSTM 等）。
```

**负载分布建模**：

如果负载服从正态分布 $N(\mu_L, \sigma_L^2)$：

$$
P(\text{Load} \le L) = \Phi\left(\frac{L - \mu_L}{\sigma_L}\right)
$$

其中 $\Phi$ 是标准正态分布的累积分布函数。

**负载峰值预测**：

对于 P99 负载峰值：

$$
L_{P99} = \mu_L + 2.33 \times \sigma_L
$$

**实际应用**：

- **容量规划**：根据负载分布规划系统容量
- **弹性伸缩**：根据负载预测进行弹性伸缩
- **资源预留**：根据负载峰值预留资源

---

### 4.3 资源利用率分布

**定义**：资源利用率分布是资源利用率的概率分布。

**利用率模型**：

```text
资源利用率 ~ Beta Distribution 或 General Distribution
范围：[0, 1]
```

**利用率分析**：

```text
利用率分析：
  - 平均利用率：E[Utilization]
  - 利用率方差：Var[Utilization]
  - 利用率分位数：P50, P95, P99
```

**Beta 分布建模**：

如果利用率服从 Beta 分布 $\text{Beta}(\alpha, \beta)$：

$$
f(u) = \frac{u^{\alpha-1}(1-u)^{\beta-1}}{B(\alpha, \beta)}, \quad 0 \le u \le 1
$$

其中 $B(\alpha, \beta)$ 是 Beta 函数。

**参数估计**：

$$
\alpha = \bar{u} \times \frac{\bar{u}(1-\bar{u})}{s^2} - 1
$$

$$
\beta = (1-\bar{u}) \times \frac{\bar{u}(1-\bar{u})}{s^2} - 1
$$

其中 $\bar{u}$ 是平均利用率，$s^2$ 是利用率方差。

**利用率阈值分析**：

$$
P(\text{Utilization} \le u_{th}) = \int_0^{u_{th}} f(u) du
$$

**实际应用**：

- **资源优化**：根据利用率分布优化资源分配
- **容量规划**：根据利用率阈值规划容量
- **性能调优**：识别利用率异常的服务

---

## 5 随机优化

### 5.1 随机调度策略

**定义**：随机调度策略是在调度决策中引入随机性的策略。

**随机策略类型**：

1. **随机选择**：随机选择候选节点
2. **概率加权**：根据概率权重选择节点
3. **随机扰动**：在确定性策略中加入随机扰动

**随机策略优势**：

1. **避免局部最优**：随机性有助于避免局部最优
2. **负载均衡**：随机性有助于负载均衡
3. **公平性**：随机性有助于保证公平性

---

### 5.2 概率约束

**定义**：概率约束是以概率形式表达的约束条件。

**概率约束类型**：

```text
概率约束：
  P(Constraint) ≥ probability

  例如：
  P(Latency ≤ 100ms) ≥ 0.95
  P(Utilization ≤ 80%) ≥ 0.99
```

**概率约束优化**：

```text
概率约束优化：
  minimize: Cost
  subject to: P(Constraint_i) ≥ p_i, ∀i
```

---

### 5.3 随机算法

**定义**：随机算法是在算法中引入随机性的算法。

**随机算法类型**：

1. **随机化算法**：在确定性算法中加入随机性
2. **蒙特卡洛方法**：使用随机采样求解问题
3. **模拟退火**：使用随机性避免局部最优

**调度系统应用**：

```text
调度系统随机算法：
  - 随机节点选择：随机选择候选节点
  - 蒙特卡洛调度：使用蒙特卡洛方法优化调度
  - 模拟退火调度：使用模拟退火优化调度决策
```

---

## 6 实际应用

### 6.1 Kubernetes 调度器

**随机过程特征**：

- **Pod 到达**：Pod 创建是随机的，通常服从 Poisson 过程
- **调度时间**：调度时间具有随机性，可能服从指数分布或一般分布
- **节点故障**：节点故障是随机的，通常服从 Poisson 过程
- **性能指标**：调度延迟、吞吐量等具有随机性

**M/M/c 模型应用**：

Kubernetes 调度器可以建模为 M/M/c 排队系统：

- **到达率** $\lambda$：Pod 创建速率（pods/s）
- **服务率** $\mu$：单个调度器处理速率（pods/s）
- **服务器数** $c$：调度器副本数（通常 $c=1$，但可以扩展）

**性能分析**：

$$
\text{调度延迟} = \frac{L_q}{\lambda} = \frac{(\lambda/\mu)^c \rho}{c!(1-\rho)^2 \lambda} P_0
$$

**容量规划**：

为保证 P95 调度延迟 < 100ms，需要：

$$
\frac{(\lambda/\mu)^c \rho}{c!(1-\rho)^2 \lambda} P_0 < 0.1
$$

### 6.2 YARN 调度器

**随机过程特征**：

- **Application 到达**：Application 提交是随机的，通常服从 Poisson 过程
- **资源分配**：资源分配时间具有随机性
- **节点故障**：节点故障是随机的
- **性能指标**：调度延迟、资源利用率等具有随机性

**M/G/1 模型应用**：

YARN ResourceManager 可以建模为 M/G/1 排队系统：

- **到达率** $\lambda$：Application 提交速率
- **服务时间** $S$：资源分配时间（一般分布）
- **利用率** $\rho = \lambda \times E[S]$

**性能分析**：

使用 Pollaczek-Khintchine 公式计算平均等待时间：

$$
W = \frac{\rho^2 + \lambda^2 \times \text{Var}[S]}{2\lambda(1-\rho)}
$$

### 6.3 实际案例分析

#### 6.3.1 电商大促场景

**场景描述**：

- Pod 创建速率：$\lambda = 100$ pods/s
- 调度器处理速率：$\mu = 200$ pods/s
- 调度器数量：$c = 1$

**M/M/1 模型分析**：

$$
\rho = \frac{100}{200} = 0.5
$$

$$
W = \frac{1}{200 - 100} = 0.01 \text{ s} = 10 \text{ ms}
$$

$$
P_{95} = \frac{-\ln(0.05)}{100} = \frac{2.996}{100} = 0.03 \text{ s} = 30 \text{ ms}
$$

**结论**：在正常负载下，P95 调度延迟为 30ms，满足 SLA 要求。

**高负载场景**：

当 $\lambda = 180$ pods/s 时：

$$
\rho = \frac{180}{200} = 0.9
$$

$$
W = \frac{1}{200 - 180} = 0.05 \text{ s} = 50 \text{ ms}
$$

$$
P_{95} = \frac{-\ln(0.05)}{20} = \frac{2.996}{20} = 0.15 \text{ s} = 150 \text{ ms}
$$

**结论**：在高负载下，P95 调度延迟增加到 150ms，可能需要扩容调度器或优化调度算法
。

#### 6.3.2 微服务调用链场景

**场景描述**：

- 服务调用到达率：$\lambda = 50$ requests/s
- 服务处理速率：$\mu = 100$ requests/s
- 调用链长度：$L = 5$ 个服务

**M/M/1 串联模型分析**：

每个服务可以建模为独立的 M/M/1 系统，总延迟为各服务延迟之和：

$$
W_{total} = \sum_{i=1}^{L} W_i = \sum_{i=1}^{L} \frac{1}{\mu_i - \lambda}
$$

假设所有服务具有相同的处理速率 $\mu = 100$ requests/s：

$$
W_{total} = 5 \times \frac{1}{100 - 50} = 5 \times 0.02 = 0.1 \text{ s} = 100 \text{ ms}
$$

**P95 延迟分析**：

对于串联系统，总延迟的 P95 分位数：

$$
P_{95,total} \approx \sum_{i=1}^{L} P_{95,i} = 5 \times \frac{-\ln(0.05)}{50} = 5 \times 0.06 = 0.3 \text{ s} = 300 \text{ ms}
$$

**结论**：在微服务调用链中，延迟会累积，需要优化每个服务的处理速率或减少调用链长
度。

#### 6.3.3 批处理任务调度场景

**场景描述**：

- 批处理任务到达率：$\lambda = 10$ jobs/hour
- 任务处理时间：服从一般分布，平均 $E[S] = 0.2$ hour，方差
  $\text{Var}[S] = 0.01$ hour²
- 服务器数量：$c = 1$

**M/G/1 模型分析**：

使用 Pollaczek-Khintchine 公式：

$$
\rho = \lambda \times E[S] = 10 \times 0.2 = 2
$$

由于 $\rho \ge 1$，系统不稳定，需要增加服务器数量。

**多服务器方案**：

假设使用 $c = 3$ 个服务器，则：

$$
\rho = \frac{\lambda}{c \times \mu} = \frac{10}{3 \times 5} = \frac{2}{3} < 1
$$

系统稳定。使用 M/M/c 模型估算平均等待时间：

$$
W \approx \frac{(\lambda/\mu)^c \rho}{c!(1-\rho)^2 \lambda} P_0
$$

**结论**：批处理任务的服务时间方差较大，需要更多的服务器资源来保证系统稳定性。

---

## 7 形式化证明

### 7.1 Little's Law 证明

**定理（Little's Law）**：在稳态排队系统中，平均队列长度等于到达率乘以平均等待时
间。

$$
L = \lambda \times W
$$

**证明**：

设 $N(t)$ 为时刻 $t$ 系统中的顾客数，$A(t)$ 为 $[0,t]$ 内到达的顾客数，$D(t)$ 为
$[0,t]$ 内离开的顾客数。

在稳态下：

$$
L = \lim_{t \to \infty} \frac{1}{t} \int_0^t N(s) ds
$$

$$
\lambda = \lim_{t \to \infty} \frac{A(t)}{t}
$$

$$
W = \lim_{t \to \infty} \frac{\sum_{i=1}^{A(t)} W_i}{A(t)}
$$

其中 $W_i$ 是第 $i$ 个顾客的等待时间。

由系统守恒性：

$$
\int_0^t N(s) ds = \sum_{i=1}^{A(t)} W_i
$$

因此：

$$
L = \lim_{t \to \infty} \frac{1}{t} \sum_{i=1}^{A(t)} W_i = \lim_{t \to \infty} \frac{A(t)}{t} \times \frac{\sum_{i=1}^{A(t)} W_i}{A(t)} = \lambda \times W
$$

### 7.2 M/M/1 队列长度分布证明

**定理**：M/M/1 系统中，队列长度服从几何分布。

$$
P_n = (1-\rho)\rho^n, \quad n = 0, 1, 2, ...
$$

**证明**：

使用生灭过程（Birth-Death Process）模型：

- **出生率**：$\lambda_n = \lambda$（常数）
- **死亡率**：$\mu_n = \mu$（常数）

稳态概率满足：

$$
\lambda P_{n-1} = \mu P_n, \quad n \ge 1
$$

因此：

$$
P_n = \left(\frac{\lambda}{\mu}\right)^n P_0 = \rho^n P_0
$$

由归一化条件 $\sum_{n=0}^{\infty} P_n = 1$：

$$
\sum_{n=0}^{\infty} \rho^n P_0 = \frac{P_0}{1-\rho} = 1
$$

因此 $P_0 = 1-\rho$，所以：

$$
P_n = (1-\rho)\rho^n
$$

---

## 8 相关文档

- [调度视角 README.md](README.md) - 调度视角主索引
- [静态分析](01-static-analysis.md) - 调度策略的静态分析
- [动态分析](02-dynamic-analysis.md) - 调度行为的动态分析
- [动态系统](05-dynamic-system.md) - 调度系统的动态系统模型
- [有界系统](07-bounded-system.md) - 调度系统的边界约束
- [跨层次调度协同](13-cross-layer-scheduling.md) - 端到端调度延迟分析

---

## 9 参考

### 学术参考

1. **排队论经典教材**：

   - Kleinrock, L. (1975). _Queueing Systems, Volume 1: Theory_. Wiley.
   - Gross, D., & Harris, C. M. (1998). _Fundamentals of Queueing Theory_.
     Wiley.

2. **随机过程理论**：

   - Ross, S. M. (2014). _Introduction to Probability Models_. Academic Press.
   - Karlin, S., & Taylor, H. M. (1975). _A First Course in Stochastic
     Processes_. Academic Press.

3. **调度理论中的随机过程**：

   - Pinedo, M. L. (2016). _Scheduling: Theory, Algorithms, and Systems_.
     Springer.
   - Leung, J. Y. T. (2004). _Handbook of Scheduling: Algorithms, Models, and
     Performance Analysis_. CRC Press.

### 实践参考

- [Kubernetes Scheduler Performance](https://kubernetes.io/docs/concepts/scheduling-eviction/scheduler-perf-tuning/)
- [YARN Capacity Scheduler](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html)

---

**最后更新**：2025-11-10 **维护者**：项目团队
