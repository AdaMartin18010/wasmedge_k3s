# IoT：业务硬核如何穿透基础设施消解

## 📑 目录

- [IoT：业务硬核如何穿透基础设施消解](#iot业务硬核如何穿透基础设施消解)
  - [📑 目录](#-目录)
  - [概述](#概述)
    - [核心思想](#核心思想)
  - [IoT 核心领域模型](#iot-核心领域模型)
  - [顽固残留的领域语义](#顽固残留的领域语义)
  - [消解率分析](#消解率分析)
  - [核心启示](#核心启示)
  - [IoT 架构实施指南](#iot-架构实施指南)
    - [设备影子实现](#设备影子实现)
    - [规则链设计](#规则链设计)
    - [时空分区策略](#时空分区策略)
  - [相关文档](#相关文档)

---

> **本文档是 IoT 领域案例分析的简化版本。详细分析请参考：**
> [`../04-domain-case-studies/04-iot-domain-model-penetration.md`](../04-domain-case-studies/04-iot-domain-model-penetration.md)

## 概述

本文档从**领域模型视角**简要分析 IoT 架构中的业务硬核如何穿透基础设施消解。

### 核心思想

> **基础设施的通用能力（容器/K8s）向上渗透，但 IoT 领域的核心语义（设备影子、规
> 则链、时空属性）因其强烈的业务契约性，反而成为架构中不可压缩的硬核层。**

## IoT 核心领域模型

1. **设备影子（Device Shadow）** - 设备数字孪生，强一致性状态机
2. **规则链（Rule Chain）** - 事件驱动的业务决策流
3. **时空分区（Time-Location Sharding）** - 设备数据按地理/时间分片策略
4. **设备认证生命周期（Device Certificate Lifecycle）** - 设备身份的可信链管理

## 顽固残留的领域语义

- **设备影子同步**：reported/desired 状态差异必须显式同步
- **规则链执行**：规则触发顺序影响业务结果（时序敏感）
- **时空分区策略**：时序数据必须按时间区间聚合（降采样）

## 消解率分析

- **基础设施层**：消解率 ≈ 80%（K8s 原生支持）
- **领域语义层**：消解率 ≈ 0%（业务规则无法消解）

## 核心启示

1. **设备影子、规则链、时空分区是 IoT 领域的核心知识**
2. **这些领域语义无法被通用框架消解**
3. **云原生 IoT 架构需要领域层"寄生"于通用层**

## IoT 架构实施指南

### 设备影子实现

**核心功能**：

- **状态同步**：reported/desired 状态同步
- **状态机管理**：设备状态机管理
- **版本控制**：状态版本控制
- **冲突解决**：状态冲突解决机制

**技术实现**：

- **Kubernetes CRD**：使用 CRD 定义设备影子
- **状态存储**：使用 etcd 或数据库存储状态
- **事件驱动**：使用事件驱动架构同步状态

**代码示例**：

```yaml
# 设备影子 CRD 定义
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: deviceshadows.iot.example.com
spec:
  group: iot.example.com
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              deviceId:
                type: string
              reported:
                type: object
              desired:
                type: object
          status:
            type: object
            properties:
              state:
                type: string
              version:
                type: integer
              lastSyncTime:
                type: string
                format: date-time
---
# 设备影子实例
apiVersion: iot.example.com/v1
kind: DeviceShadow
metadata:
  name: sensor-001
spec:
  deviceId: "sensor-001"
  reported:
    temperature: 25.5
    humidity: 60.0
    timestamp: "2025-11-06T10:00:00Z"
  desired:
    targetTemperature: 24.0
    mode: "auto"
status:
  state: "syncing"
  version: 42
  lastSyncTime: "2025-11-06T10:00:00Z"
```

**状态同步逻辑**：

```go
// 设备影子状态同步（Go 示例）
func (s *DeviceShadow) SyncState() error {
    // 比较 reported 和 desired 状态
    if !reflect.DeepEqual(s.Spec.Reported, s.Spec.Desired) {
        // 生成状态差异
        delta := computeDelta(s.Spec.Reported, s.Spec.Desired)

        // 发送状态更新到设备
        if err := s.sendToDevice(delta); err != nil {
            return err
        }

        // 更新状态版本
        s.Status.Version++
        s.Status.LastSyncTime = time.Now()
    }

    return nil
}
```

### 规则链设计

**设计原则**：

- **时序保证**：保证规则执行顺序
- **幂等性**：规则执行幂等性
- **可扩展性**：支持规则动态添加
- **可观测性**：规则执行可观测

**实现方式**：

- **规则引擎**：使用规则引擎（如 Drools）
- **工作流引擎**：使用工作流引擎（如 Temporal）
- **事件流处理**：使用事件流处理（如 Kafka Streams）

**代码示例**：

```yaml
# 规则链定义
apiVersion: iot.example.com/v1
kind: RuleChain
metadata:
  name: temperature-alert-chain
spec:
  rules:
  - name: check-temperature
    condition: "device.temperature > 30"
    action: "send-alert"
    priority: 1
  - name: check-humidity
    condition: "device.humidity > 80"
    action: "send-alert"
    priority: 2
  - name: auto-adjust
    condition: "device.temperature > 25 && device.mode == 'auto'"
    action: "adjust-cooling"
    priority: 3
```

**规则执行引擎**：

```python
# 规则链执行（Python 示例）
class RuleChain:
    def __init__(self, rules):
        self.rules = sorted(rules, key=lambda r: r.priority)

    def execute(self, device_state):
        results = []
        for rule in self.rules:
            if self.evaluate_condition(rule.condition, device_state):
                result = self.execute_action(rule.action, device_state)
                results.append(result)
        return results

    def evaluate_condition(self, condition, state):
        # 使用表达式引擎评估条件
        return eval(condition, {"device": state})

    def execute_action(self, action, state):
        # 执行动作
        if action == "send-alert":
            return self.send_alert(state)
        elif action == "adjust-cooling":
            return self.adjust_cooling(state)
        return None
```

### 时空分区策略

**分区维度**：

- **时间分区**：按时间区间分区（小时、天、月）
- **地理分区**：按地理位置分区（区域、城市）
- **设备类型**：按设备类型分区

**数据管理**：

- **降采样**：时序数据降采样
- **数据归档**：历史数据归档
- **查询优化**：分区查询优化

**代码示例**：

```sql
-- 时序数据分区表（PostgreSQL 示例）
CREATE TABLE device_metrics (
    device_id VARCHAR(50),
    metric_type VARCHAR(50),
    value DOUBLE PRECISION,
    timestamp TIMESTAMP,
    location VARCHAR(50)
) PARTITION BY RANGE (timestamp);

-- 按月分区
CREATE TABLE device_metrics_2025_11 PARTITION OF device_metrics
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');

CREATE TABLE device_metrics_2025_12 PARTITION OF device_metrics
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');

-- 按地理位置分区
CREATE TABLE device_metrics_beijing PARTITION OF device_metrics_2025_11
    FOR VALUES WITH (location = 'beijing');

CREATE TABLE device_metrics_shanghai PARTITION OF device_metrics_2025_11
    FOR VALUES WITH (location = 'shanghai');
```

**降采样示例**：

```python
# 时序数据降采样（Python 示例）
import pandas as pd

def downsample_metrics(df, interval='1H'):
    """
    将高频数据降采样到指定间隔
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')

    # 按时间间隔聚合
    downsampled = df.resample(interval).agg({
        'temperature': 'mean',
        'humidity': 'mean',
        'pressure': 'mean'
    })

    return downsampled.reset_index()

# 使用示例
hourly_data = downsample_metrics(device_data, interval='1H')
daily_data = downsample_metrics(device_data, interval='1D')
```

**2025 年最新实践**：

- **时序数据库**：使用 InfluxDB 3.0 或 TimescaleDB 2.0 进行时序数据存储
- **边缘计算**：使用 K3s + WasmEdge 在边缘节点进行数据预处理
- **实时流处理**：使用 Kafka Streams 或 Flink 进行实时数据处理

## 相关文档

- [详细分析文档](../04-domain-case-studies/04-iot-domain-model-penetration.md)
- [领域语义无法通用化](../02-semantic-model-perspective/02-irreducibility-of-domain-semantics.md)
- [分层消解律概述](../03-layered-disintegration-law/01-introduction.md)

---

**最后更新**：2025-11-08 **维护者**：项目团队
