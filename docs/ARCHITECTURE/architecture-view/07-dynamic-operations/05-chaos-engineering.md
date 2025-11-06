# 混沌工程：可靠性测试与故障注入

## 📑 目录

- [1. 概述](#1-概述)
- [2. 混沌工程定义](#2-混沌工程定义)
- [3. Litmus](#3-litmus)
- [4. Chaos Mesh](#4-chaos-mesh)
- [5. 混沌工程实践](#5-混沌工程实践)
- [6. 形式化定义](#6-形式化定义)
- [7. 总结](#7-总结)

---

## 1. 概述

本文档详细阐述**混沌工程**的实现方法，通过 **Chaos Monkey、Litmus** 等技术实现可
靠性测试和故障注入。

### 1.1 核心思想

> **通过混沌工程主动注入故障，验证系统的容错能力和恢复能力，提高系统的可靠性**

## 2. 混沌工程定义

### 2.1 混沌工程概念

**混沌工程**是通过主动注入故障来验证系统容错能力的工程实践。

### 2.2 混沌工程原则

**混沌工程原则**：

1. **建立稳定状态假设**：定义系统的正常状态
2. **引入混沌变量**：注入故障和异常
3. **验证假设**：验证系统是否仍能保持稳定
4. **持续改进**：根据结果改进系统

### 2.3 混沌工程工具

| 工具             | 特点                | 适用场景        |
| ---------------- | ------------------- | --------------- |
| **Chaos Monkey** | Netflix 开源工具    | AWS 环境        |
| **Litmus**       | Kubernetes 原生工具 | Kubernetes 环境 |
| **Chaos Mesh**   | PingCAP 开源工具    | Kubernetes 环境 |
| **Gremlin**      | 商业工具            | 多云环境        |

## 3. Litmus

### 3.1 Litmus 定义

**Litmus** 是 Kubernetes 原生的混沌工程工具，提供：

- **Kubernetes 原生**：完全基于 Kubernetes CRD
- **丰富的故障类型**：支持多种故障类型
- **可观测性**：集成 Prometheus 和 Grafana

### 3.2 Litmus 故障类型

**Litmus 故障类型**：

| 故障类型          | 说明     | 典型场景          |
| ----------------- | -------- | ----------------- |
| **Pod Kill**      | 杀死 Pod | 验证 Pod 重启能力 |
| **Pod Delete**    | 删除 Pod | 验证 Pod 恢复能力 |
| **Network Chaos** | 网络故障 | 验证网络容错能力  |
| **CPU Stress**    | CPU 压力 | 验证资源限制能力  |
| **Memory Stress** | 内存压力 | 验证内存限制能力  |

### 3.3 Litmus 配置示例

**Pod Kill 配置**：

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-kill-chaos
spec:
  appinfo:
    appns: default
    applabel: app=order-service
    appkind: deployment
  chaosServiceAccount: litmus-admin
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TARGET_CONTAINER
              value: order-service
            - name: TOTAL_CHAOS_DURATION
              value: "60"
            - name: CHAOS_INTERVAL
              value: "10"
            - name: FORCE
              value: "false"
```

## 4. Chaos Mesh

### 4.1 Chaos Mesh 定义

**Chaos Mesh** 是 PingCAP 开源的混沌工程工具，提供：

- **Kubernetes 原生**：完全基于 Kubernetes CRD
- **丰富的故障类型**：支持多种故障类型
- **可视化界面**：提供 Web UI

### 4.2 Chaos Mesh 故障类型

**Chaos Mesh 故障类型**：

| 故障类型         | 说明     | 典型场景          |
| ---------------- | -------- | ----------------- |
| **PodChaos**     | Pod 故障 | 验证 Pod 容错能力 |
| **NetworkChaos** | 网络故障 | 验证网络容错能力  |
| **StressChaos**  | 压力测试 | 验证资源限制能力  |
| **TimeChaos**    | 时间故障 | 验证时间依赖能力  |
| **IOChaos**      | I/O 故障 | 验证存储容错能力  |

### 4.3 Chaos Mesh 配置示例

**NetworkChaos 配置**：

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay
spec:
  action: delay
  mode: one
  selector:
    namespaces:
      - default
    labelSelectors:
      app: order-service
  delay:
    latency: "10ms"
    correlation: "100"
    jitter: "0ms"
  duration: "5m"
```

## 5. 混沌工程实践

### 5.1 混沌实验流程

**混沌实验流程**：

```text
1. 建立稳定状态假设
    ↓
2. 设计混沌实验
    ↓
3. 注入故障
    ↓
4. 观察系统行为
    ↓
5. 验证假设
    ↓
6. 改进系统
```

### 5.2 混沌实验类型

**混沌实验类型**：

| 实验类型     | 说明             | 典型场景             |
| ------------ | ---------------- | -------------------- |
| **基础实验** | 单次故障注入     | 验证基本容错能力     |
| **持续实验** | 持续故障注入     | 验证持续容错能力     |
| **组合实验** | 多个故障组合注入 | 验证复杂场景容错能力 |
| **生产实验** | 生产环境故障注入 | 验证生产环境容错能力 |

### 5.3 混沌实验最佳实践

**混沌实验最佳实践**：

- **从小规模开始**：先在小规模环境测试
- **逐步扩大范围**：逐步扩大实验范围
- **监控关键指标**：监控错误率、延迟等关键指标
- **自动回滚**：配置自动回滚策略

## 6. 形式化定义

### 6.1 混沌工程定义

```text
混沌工程 C = ⟨hypothesis, experiment, observation, validation⟩
其中：
- hypothesis: 稳定状态假设
- experiment: 混沌实验
- observation: 观察结果
- validation: 验证结果
```

### 6.2 混沌实验定义

```text
混沌实验 E = ⟨fault, duration, scope, metrics⟩
其中：
- fault: 故障类型
- duration: 实验持续时间
- scope: 实验范围
- metrics: 监控指标集合
```

## 7. 总结

通过**混沌工程**，我们实现了：

1. **主动故障注入**：主动注入故障验证系统容错能力
2. **可靠性测试**：通过混沌实验测试系统可靠性
3. **故障恢复验证**：验证系统的故障恢复能力
4. **持续改进**：根据实验结果持续改进系统
5. **自动化**：通过工具自动化混沌实验

### 7.1 相关文档

**扩展阅读**：

- **[eBPF/OTLP 架构视角](../09-multi-perspectives/07-ebpf-otlp-perspective.md)**
  ⭐ - 横纵耦合的可观测性驱动架构
  - **自我治愈：从发现到恢复的闭环**（5.3 章节）
  - 故障模式的内核态检测（内存泄漏、死锁、DNS 解析超时、容器逃逸）
  - OTLP 驱动的自愈编排（事件驱动的自愈工作流）
  - 自愈能力分级模型（L1-L4：局部隔离、服务重启、流量调度、架构降级）
- **[可观测性文档](../07-dynamic-operations/02-observability.md)** - 统一遥测与
  监控
- **[32. eBPF/OTLP 扩展技术分析](../../../TECHNICAL/32-ebpf-otlp-analysis/ebpf-otlp-analysis.md)**
  ⭐ - eBPF/OTLP 扩展技术分析文档

---

**更新时间**：2025-11-07 **版本**：v1.1 **参考**：`architecture_view.md` 第 30
行，混沌工程部分
