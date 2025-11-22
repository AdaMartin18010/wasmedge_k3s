# 四、NUMA 拓扑函子

> **文档版本**：v1.0 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [四、NUMA 拓扑函子](#四numa-拓扑函子)
  - [📑 目录](#-目录)
  - [概述](#概述)
  - [一、NUMA 拓扑函子定义](#一numa-拓扑函子定义)
    - [1.1 NUMA 拓扑函子类型](#11-numa-拓扑函子类型)
    - [1.2 NUMA 拓扑提取](#12-numa-拓扑提取)
    - [1.3 NUMA 拓扑验证](#13-numa-拓扑验证)
  - [二、NUMA 感知调度](#二numa-感知调度)
    - [2.1 vCPU 到 NUMA 映射](#21-vcpu-到-numa-映射)
    - [2.2 内存到 NUMA 映射](#22-内存到-numa-映射)
    - [2.3 最优放置条件](#23-最优放置条件)
  - [三、资源拓扑的纤维丛构造](#三资源拓扑的纤维丛构造)
    - [3.1 纤维丛定义](#31-纤维丛定义)
    - [3.2 NUMA 纤维](#32-numa-纤维)
    - [3.3 水平提升](#33-水平提升)
  - [四、形式化验证](#四形式化验证)
    - [4.1 NUMA 拓扑一致性验证](#41-numa-拓扑一致性验证)
    - [4.2 最优放置验证](#42-最优放置验证)
  - [相关文档](#相关文档)

---

## 概述

本文档从**范畴论**和**纤维丛理论**的视角形式化分析 NUMA 拓扑函子，将 NUMA 拓扑
、vCPU 映射、内存映射等概念抽象为函子、纤维丛等数学结构，建立 NUMA 感知调度的严
格数学模型。

**为什么使用范畴论和纤维丛理论分析 NUMA 拓扑函子？**

范畴论和纤维丛理论提供了统一的数学框架来描述 NUMA 拓扑函子的结构和行为：

1. **统一抽象**：通过范畴论，我们可以将 NUMA 拓扑、vCPU 映射、内存映射等抽象为函
   子，实现统一的数学描述
2. **结构保持**：通过纤维丛理论，我们可以保持 NUMA 拓扑的结构，确保 NUMA 感知调
   度的正确性
3. **最优放置**：通过纤维丛理论，我们可以实现最优的 NUMA 感知调度請持續 推進 簡體中文輸出
請詳細的解釋和論證

**范畴论和纤维丛理论在 NUMA 拓扑函子分析中的应用**：

- **NUMA 拓扑函子（NUMA Topology Functor）**：NUMA 拓扑函子，描述 NUMA 拓扑的映
  射
- **纤维丛（Fiber Bundle）**：资源拓扑的纤维丛构造，描述 NUMA 拓扑的纤维结构
- **水平提升（Horizontal Lift）**：水平提升，描述 NUMA 感知调度的最优路径

**核心内容**：

1. **NUMA 拓扑函子定义**：NUMA 拓扑函子类型、提取、验证
2. **NUMA 感知调度**：vCPU 到 NUMA 映射、内存到 NUMA 映射、最优放置条件
3. **资源拓扑的纤维丛构造**：纤维丛定义、NUMA 纤维、水平提升
4. **形式化验证**：NUMA 拓扑一致性、最优放置验证

---

## 一、NUMA 拓扑函子定义

### 1.1 NUMA 拓扑函子类型

**NUMA 拓扑函子** `Numa: Node → TopologyGraph`：

```haskell
-- NUMA 拓扑函子类型
data NumaTopologyFunctor = NumaTopology {
    extract :: Node -> NumaGraph,
    validate :: NumaGraph -> VMSpec -> Bool,
    match :: NumaGraph -> VMSpec -> Bool
}

-- NUMA 拓扑函子实例
instance Functor NumaTopology where
    fmap f (NumaTopology extract validate match) =
        NumaTopology (f . extract) validate match
```

**形式化定义**：

```text
Numa: Node → TopologyGraph
Numa(node) = {NUMA_0, NUMA_1, ..., NUMA_n}
```

其中：

- **Node**：物理节点对象
- **TopologyGraph**：NUMA 拓扑图
- **NUMA_i**：第 i 个 NUMA 节点

### 1.2 NUMA 拓扑提取

**NUMA 拓扑提取**：

```haskell
-- NUMA 拓扑提取
numaTopology :: Node -> NumaGraph
numaTopology node =
    NumaGraph {
        nodes = numaNodes node,
        distances = numaDistances node,
        topology = numaTopology node
    }
```

**形式化定义**：

```text
Numa(node) = {NUMA_0, NUMA_1, ..., NUMA_n}
其中 NUMA_i = {CPU_i, Memory_i, Distance_i}
```

**NUMA 拓扑结构**：

| **NUMA 节点** | **CPU 核心** | **内存容量** | **距离** |
| ------------- | ------------ | ------------ | -------- |
| **NUMA_0**    | CPU_0-7      | 32GB         | 0        |
| **NUMA_1**    | CPU_8-15     | 32GB         | 1        |
| **NUMA_2**    | CPU_16-23    | 32GB         | 2        |
| **NUMA_3**    | CPU_24-31    | 32GB         | 3        |

### 1.3 NUMA 拓扑验证

**NUMA 拓扑验证**：

```haskell
-- NUMA 拓扑验证
validateNumaTopology :: NumaGraph -> VMSpec -> Bool
validateNumaTopology numaGraph vmSpec =
    let vcpuNodes = map vcpuToNuma (vmSpec.vcpus)
        memNodes = map memoryToNuma (vmSpec.memory)
        allSameNUMA = all (== head vcpuNodes) vcpuNodes
        vcpuMemSameNUMA = head vcpuNodes == head memNodes
    in allSameNUMA && vcpuMemSameNUMA
```

**形式化定义**：

```text
validateNumaTopology(numaGraph, vmSpec) =
  allSameNUMA(vcpuNodes) ∧ vcpuMemSameNUMA(vcpuNodes, memNodes)
```

---

## 二、NUMA 感知调度

### 2.1 vCPU 到 NUMA 映射

**vCPU 到 NUMA 映射** `vcpuToNuma: VCPU → NumaNode`：

```haskell
-- vCPU 到 NUMA 映射
vcpuToNuma :: VCPU -> NumaNode
vcpuToNuma vcpu =
    let cpuCore = vcpu.core
        numaNode = findNumaNode cpuCore
    in numaNode
```

**形式化定义**：

```text
vcpuToNuma: VCPU → NumaNode
vcpuToNuma(vcpu) = NUMA_i 其中 vcpu.core ∈ CPU_i
```

**vCPU 到 NUMA 映射表**：

| **vCPU**   | **CPU 核心** | **NUMA 节点** |
| ---------- | ------------ | ------------- |
| **vCPU_0** | CPU_0        | NUMA_0        |
| **vCPU_1** | CPU_1        | NUMA_0        |
| **vCPU_2** | CPU_8        | NUMA_1        |
| **vCPU_3** | CPU_9        | NUMA_1        |

### 2.2 内存到 NUMA 映射

**内存到 NUMA 映射** `memoryToNuma: Memory → NumaNode`：

```haskell
-- 内存到 NUMA 映射
memoryToNuma :: Memory -> NumaNode
memoryToNuma memory =
    let memoryAddress = memory.address
        numaNode = findNumaNode memoryAddress
    in numaNode
```

**形式化定义**：

```text
memoryToNuma: Memory → NumaNode
memoryToNuma(memory) = NUMA_i 其中 memory.address ∈ Memory_i
```

**内存到 NUMA 映射表**：

| **内存**     | **地址范围**          | **NUMA 节点** |
| ------------ | --------------------- | ------------- |
| **Memory_0** | 0x0-0x7FFFFFFF        | NUMA_0        |
| **Memory_1** | 0x80000000-0xFFFFFFFF | NUMA_1        |

### 2.3 最优放置条件

**最优放置条件**：

```haskell
-- 最优放置条件
optimalPlacement :: VMSpec -> Node -> Bool
optimalPlacement vmSpec node =
    let vcpuNodes = map vcpuToNuma (vmSpec.vcpus)
        memNodes = map memoryToNuma (vmSpec.memory)
        allSameNUMA = all (== head vcpuNodes) vcpuNodes  -- 所有vCPU在同一NUMA
        vcpuMemSameNUMA = head vcpuNodes == head memNodes -- vCPU与内存同NUMA
    in allSameNUMA && vcpuMemSameNUMA
```

**形式化定义**：

```text
optimalPlacement(vmSpec, node) =
  allSameNUMA(vcpuNodes) ∧ vcpuMemSameNUMA(vcpuNodes, memNodes)
```

其中：

- **allSameNUMA**：所有 vCPU 在同一 NUMA 节点
- **vcpuMemSameNUMA**：vCPU 与内存在同一 NUMA 节点

**最优放置条件验证**：

```text
∀vmSpec ∈ VMSpec, node ∈ Node:
optimalPlacement(vmSpec, node) ⇔
  ∀vcpu₁, vcpu₂ ∈ vmSpec.vcpus, vcpuToNuma(vcpu₁) = vcpuToNuma(vcpu₂) ∧
  ∀mem ∈ vmSpec.memory, vcpuToNuma(vcpu₁) = memoryToNuma(mem)
```

---

## 三、资源拓扑的纤维丛构造

### 3.1 纤维丛定义

**资源拓扑的纤维丛（Fiber Bundle）**：将集群资源建模为**纤维丛** `E → B`：

```haskell
-- 纤维丛类型
data FiberBundle = Bundle {
    baseSpace :: Set Node,  -- 基空间 B
    fiber :: Node -> Set Resource,  -- 纤维 F_p
    section :: Node -> Resource  -- 截面 σ: B → E
}

-- 纤维丛实例
resourceFiberBundle = Bundle {
    baseSpace = allNodes,
    fiber = \node -> {CPU(node), Memory(node)},
    section = \node -> PodPlacement(node)
}
```

**形式化定义**：

```text
E → B 其中：
- B：物理节点集合（基空间）
- F_p：节点 p 上的资源（CPU/Memory）（纤维）
- σ: B → E：Pod/VMI 的放置（截面）
```

### 3.2 NUMA 纤维

**VM 的 NUMA 纤维**：

```text
F_numa(p) = ⨆_{i=1}^n (CPU_i, Memory_i)
```

**形式化定义**：

```haskell
-- NUMA 纤维类型
data NumaFiber = Fiber {
    numaNode :: NumaNode,
    cpu :: Set CPU,
    memory :: Set Memory
}

-- NUMA 纤维实例
numaFiber node numaNode =
    Fiber {
        numaNode = numaNode,
        cpu = filter (\c -> vcpuToNuma c == numaNode) (node.cpus),
        memory = filter (\m -> memoryToNuma m == numaNode) (node.memory)
    }
```

**NUMA 纤维结构**：

| **NUMA 节点** | **CPU 核心** | **内存容量** |
| ------------- | ------------ | ------------ |
| **NUMA_0**    | CPU_0-7      | 32GB         |
| **NUMA_1**    | CPU_8-15     | 32GB         |

### 3.3 水平提升

**容器调度忽略纤维结构，VM 调度需**水平提升**（Horizontal Lift）**：

```text
lift(p, vcpu) = argmin_{f∈F(p)} distance(vcpu, f)
```

**形式化定义**：

```haskell
-- 水平提升
horizontalLift :: Node -> VCPU -> NumaFiber
horizontalLift node vcpu =
    let numaNode = vcpuToNuma vcpu
        fibers = map (numaFiber node) (numaNodes node)
        matchingFiber = find (\f -> f.numaNode == numaNode) fibers
    in fromJust matchingFiber
```

**水平提升条件**：

```text
∀node ∈ Node, vcpu ∈ VCPU:
lift(node, vcpu) = f 其中 f ∈ F(node) 且 vcpuToNuma(vcpu) = f.numaNode
```

---

## 四、形式化验证

### 4.1 NUMA 拓扑一致性验证

**NUMA 拓扑一致性定理**：

```text
□(∀vmSpec ∈ VMSpec, node ∈ Node,
  optimalPlacement(vmSpec, node) →
  ∀vcpu₁, vcpu₂ ∈ vmSpec.vcpus, vcpuToNuma(vcpu₁) = vcpuToNuma(vcpu₂))
```

**形式化验证**：

```haskell
-- NUMA 拓扑一致性验证
verifyNumaTopologyConsistency :: VMSpec -> Node -> Bool
verifyNumaTopologyConsistency vmSpec node =
    let vcpuNodes = map vcpuToNuma (vmSpec.vcpus)
        allSameNUMA = all (== head vcpuNodes) vcpuNodes
    in optimalPlacement vmSpec node → allSameNUMA
```

**一致性性质**：

1. **vCPU NUMA 一致性**：`∀vcpu₁, vcpu₂, vcpuToNuma(vcpu₁) = vcpuToNuma(vcpu₂)`
2. **内存 NUMA 一致性**：`∀mem₁, mem₂, memoryToNuma(mem₁) = memoryToNuma(mem₂)`
3. **vCPU 内存 NUMA 一致性**：`∀vcpu, mem, vcpuToNuma(vcpu) = memoryToNuma(mem)`

### 4.2 最优放置验证

**最优放置验证**：

```text
□(∀vmSpec ∈ VMSpec, node ∈ Node,
  optimalPlacement(vmSpec, node) →
  cost(vmSpec, node) = min_{n∈NodeList} cost(vmSpec, n))
```

**形式化验证**：

```haskell
-- 最优放置验证
verifyOptimalPlacement :: VMSpec -> NodeList -> Bool
verifyOptimalPlacement vmSpec nodeList =
    let optimalNodes = filter (\n -> optimalPlacement vmSpec n) nodeList
        costs = map (\n -> (n, cost vmSpec n)) optimalNodes
        minCost = minimum (map snd costs)
        bestNodes = filter ((== minCost) . snd) costs
    in length bestNodes == 1
```

**最优放置性质**：

1. **NUMA 最优
   性**：`∀vmSpec, node, optimalPlacement(vmSpec, node) → NUMA_optimal(node)`
2. **成本最优
   性**：`∀vmSpec, node, optimalPlacement(vmSpec, node) → cost_optimal(node)`
3. **放置唯一性**：`∀vmSpec, nodeList, ∃!node, optimalPlacement(vmSpec, node)`

---

## 相关文档

- [调度器的拉回构造](./01-scheduler-category-theory.md) - 调度器范畴论模型
- [调度决策作为拉回](./02-scheduler-pullback.md) - 调度决策拉回构造
- [虚拟机调度的扩展拉回](./03-vm-scheduling-extension.md) - VM 调度扩展拉回
- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵

---

**最后更新**：2025-11-10 **维护者**：项目团队
