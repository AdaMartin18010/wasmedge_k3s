# 案例 W-002：Wasm 内存溢出

> **案例编号**：W-002
> **故障类型**：运行时错误
> **严重程度**：严重
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 W-002：Wasm 内存溢出](#案例-w-002wasm-内存溢出)
  - [📑 目录](#-目录)
  - [1 故障描述](#1-故障描述)
    - [1.1 现象](#11-现象)
    - [1.2 影响范围](#12-影响范围)
    - [1.3 发生时间](#13-发生时间)
  - [2 环境信息](#2-环境信息)
    - [2.1 软件版本](#21-软件版本)
    - [2.2 硬件配置](#22-硬件配置)
    - [2.3 部署配置](#23-部署配置)
  - [3 排查过程](#3-排查过程)
    - [3.1 初步诊断](#31-初步诊断)
    - [3.2 深入分析](#32-深入分析)
    - [3.3 根因定位](#33-根因定位)
  - [4 根因分析](#4-根因分析)
    - [4.1 技术根因](#41-技术根因)
    - [4.2 配置根因](#42-配置根因)
  - [5 解决方案](#5-解决方案)
    - [5.1 临时方案](#51-临时方案)
    - [5.2 根本方案](#52-根本方案)
    - [5.3 预防措施](#53-预防措施)
  - [6 验证结果](#6-验证结果)
    - [6.1 验证方法](#61-验证方法)
    - [6.2 验证结果](#62-验证结果)
    - [6.3 验证时间](#63-验证时间)
  - [7 经验总结](#7-经验总结)
    - [7.1 关键教训](#71-关键教训)
    - [7.2 最佳实践](#72-最佳实践)
    - [7.3 相关文档](#73-相关文档)
  - [8 相关文档](#8-相关文档)

---

## 1 故障描述

### 1.1 现象

**故障现象**：

```bash
$ kubectl logs payment-wasm
Error: out of bounds memory access
Error: memory limit exceeded
Error: wasm trap: unreachable

$ kubectl describe pod payment-wasm
Events:
  Warning  OOMKilled  2m (x3 over 10m)  kubelet
           Container payment-wasm was killed due to memory limit exceeded
```

**实际表现**：

- Pod 频繁重启，状态在 `CrashLoopBackOff` 和 `Running` 之间切换
- 日志显示 "out of bounds memory access" 和 "memory limit exceeded" 错误
- 应用在处理大 JSON 数据时崩溃
- 内存使用率持续上升，最终触发 OOMKilled

### 1.2 影响范围

- **受影响服务**：支付网关服务（payment-wasm）
- **受影响用户**：所有使用支付功能的用户
- **业务影响**：支付功能完全不可用，影响交易处理

### 1.3 发生时间

- **首次发现**：2025-11-11 09:15
- **持续时间**：约 3 小时
- **解决时间**：2025-11-11 12:30

---

## 2 环境信息

### 2.1 软件版本

- **K3s 版本**：v1.30.4+k3s1
- **WasmEdge 版本**：v0.14.0
- **crun 版本**：v1.8.5
- **Kubernetes 版本**：v1.30.4
- **操作系统**：Ubuntu 22.04 LTS
- **内核版本**：5.15.0-91-generic

### 2.2 硬件配置

- **节点类型**：边缘节点
- **CPU**：4 核 ARM64
- **内存**：2GB RAM
- **存储**：32GB eMMC

### 2.3 部署配置

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: payment-wasm
  annotations:
    module.wasm.image/variant: compat-smart
spec:
  runtimeClassName: wasm
  containers:
    - name: app
      image: yourhub/payment-wasm:v1
      resources:
        requests:
          memory: "10Mi"
          cpu: "50m"
        limits:
          memory: "20Mi"  # 问题：内存限制过小
          cpu: "200m"
      env:
        - name: MAX_JSON_SIZE
          value: "10485760"  # 10MB，但 Wasm 内存限制仅 20Mi
```

---

## 3 排查过程

### 3.1 初步诊断

**步骤 1：检查 Pod 状态**:

```bash
$ kubectl get pods
NAME           READY   STATUS             RESTARTS   AGE
payment-wasm   0/1     CrashLoopBackOff   5          10m
```

**步骤 2：查看 Pod 事件**:

```bash
$ kubectl describe pod payment-wasm
Events:
  Warning  OOMKilled  2m (x3 over 10m)  kubelet
           Container payment-wasm was killed due to memory limit exceeded
  Warning  Failed     2m (x3 over 10m)  kubelet
           Error: out of bounds memory access
```

**步骤 3：查看应用日志**:

```bash
$ kubectl logs payment-wasm --previous
Error: out of bounds memory access
Error: memory limit exceeded
Error: wasm trap: unreachable
```

**初步结论**：Pod 因内存溢出被 OOMKilled，应用在处理大 JSON 数据时超出内存限制。

### 3.2 深入分析

**步骤 1：检查内存使用情况**:

```bash
$ kubectl top pod payment-wasm
NAME           CPU(cores)   MEMORY(bytes)
payment-wasm   10m          22Mi  # 超过 20Mi 限制
```

**步骤 2：分析应用代码**:

```rust
// 问题代码：一次性加载整个 JSON
pub fn process_payment(json_data: &str) -> Result<PaymentResult> {
    let data: PaymentData = serde_json::from_str(json_data)?;  // 需要大量内存
    // 处理逻辑...
}
```

**步骤 3：测试不同 JSON 大小**:

```bash
# 测试小 JSON（1KB）
curl -X POST http://payment-wasm/api/payment -d @small.json
# 成功

# 测试大 JSON（5MB）
curl -X POST http://payment-wasm/api/payment -d @large.json
# 失败：out of bounds memory access
```

**深入分析结论**：

1. 应用在处理大 JSON（>5MB）时，需要一次性加载到内存
2. Wasm 内存限制仅 20Mi，无法容纳大 JSON 数据和处理过程中的临时对象
3. 应用代码未实现流式处理，导致内存溢出

### 3.3 根因定位

**根因 1：内存限制配置过小**:

- Pod 配置中 `resources.limits.memory: "20Mi"` 过小
- 无法处理大 JSON 数据（5-10MB）
- 未考虑处理过程中的临时对象内存占用

**根因 2：应用代码未优化**:

- 使用 `serde_json::from_str` 一次性加载整个 JSON
- 未实现流式处理或分块处理
- 未限制输入数据大小

**根因 3：缺乏内存监控**:

- 未监控 Wasm 应用的内存使用情况
- 未设置内存使用告警
- 未及时发现内存问题

---

## 4 根因分析

### 4.1 技术根因

**Wasm 内存限制特点**：

1. **线性内存限制**：Wasm 使用线性内存，有明确的大小限制
2. **内存分配**：每次内存分配都需要检查是否超出限制
3. **OOM 处理**：超出限制会触发 trap，导致应用崩溃

**应用代码问题**：

- 使用 `serde_json::from_str` 一次性反序列化整个 JSON
- 对于大 JSON（5-10MB），需要至少 2 倍内存（原始数据 + 反序列化对象）
- 20Mi 内存限制无法满足需求

### 4.2 配置根因

**资源配置不当**：

```yaml
resources:
  limits:
    memory: "20Mi"  # ❌ 过小，无法处理大 JSON
```

**正确的配置**：

```yaml
resources:
  limits:
    memory: "100Mi"  # ✅ 根据实际需求设置
```

**应用代码问题**：

```rust
// ❌ 问题代码：一次性加载
let data: PaymentData = serde_json::from_str(json_data)?;

// ✅ 优化代码：流式处理
let mut deserializer = serde_json::Deserializer::from_str(json_data);
let data: PaymentData = PaymentData::deserialize(&mut deserializer)?;
```

---

## 5 解决方案

### 5.1 临时方案

**方案 1：增加内存限制**:

```bash
# 编辑 Pod 配置
kubectl edit pod payment-wasm

# 修改内存限制
resources:
  limits:
    memory: "100Mi"  # 从 20Mi 增加到 100Mi
```

**方案 2：限制输入数据大小**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: payment-wasm
spec:
  containers:
    - name: app
      env:
        - name: MAX_JSON_SIZE
          value: "5242880"  # 限制为 5MB
```

### 5.2 根本方案

**方案 1：优化应用代码（流式处理）**:

```rust
// 使用流式 JSON 解析
use serde_json::Deserializer;

pub fn process_payment_streaming<R: Read>(reader: R) -> Result<PaymentResult> {
    let mut deserializer = Deserializer::from_reader(reader);
    let mut payment_data = PaymentData::default();

    // 流式处理，避免一次性加载
    while let Some(field) = deserializer.next_field()? {
        match field {
            "amount" => payment_data.amount = deserializer.next_value()?,
            "currency" => payment_data.currency = deserializer.next_value()?,
            // 其他字段...
            _ => deserializer.skip_value()?,
        }
    }

    // 处理逻辑...
    Ok(process(payment_data)?)
}
```

**方案 2：优化 Pod 资源配置**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: payment-wasm
  annotations:
    module.wasm.image/variant: compat-smart
spec:
  runtimeClassName: wasm
  containers:
    - name: app
      image: yourhub/payment-wasm:v1
      resources:
        requests:
          memory: "50Mi"    # ✅ 根据实际需求设置
          cpu: "50m"
        limits:
          memory: "100Mi"   # ✅ 为处理大 JSON 留出空间
          cpu: "200m"
      env:
        - name: MAX_JSON_SIZE
          value: "10485760"  # 10MB
        - name: WASM_MEMORY_LIMIT
          value: "104857600"  # 100MB
```

**方案 3：使用 WasmEdge 内存配置**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: payment-wasm
spec:
  runtimeClassName: wasm
  containers:
    - name: app
      image: yourhub/payment-wasm:v1
      command:
        - "wasmedge"
        - "--max-memory-page"
        - "16384"  # 16MB * 64KB/page = 1GB（如果需要）
        - "payment.wasm"
```

### 5.3 预防措施

1. **建立内存基准测试**：
   - 测试不同 JSON 大小的内存使用
   - 根据测试结果设置合理的内存限制

2. **实现流式处理**：
   - 对于大 JSON，使用流式解析
   - 避免一次性加载整个数据

3. **监控和告警**：
   - 监控 Wasm 应用的内存使用率
   - 当内存使用率超过阈值时发送告警

4. **输入验证**：
   - 限制输入数据大小
   - 在应用层进行输入验证

---

## 6 验证结果

### 6.1 验证方法

**步骤 1：应用解决方案**:

```bash
# 更新 Pod 配置
kubectl apply -f payment-wasm-optimized.yaml
```

**步骤 2：测试不同 JSON 大小**:

```bash
# 测试小 JSON（1KB）
curl -X POST http://payment-wasm/api/payment -d @small.json
# 成功

# 测试中等 JSON（1MB）
curl -X POST http://payment-wasm/api/payment -d @medium.json
# 成功

# 测试大 JSON（5MB）
curl -X POST http://payment-wasm/api/payment -d @large.json
# 成功
```

**步骤 3：监控内存使用**:

```bash
$ kubectl top pod payment-wasm
NAME           CPU(cores)   MEMORY(bytes)
payment-wasm   15m          45Mi  # 在限制范围内
```

**步骤 4：压力测试**:

```bash
# 并发测试
for i in {1..100}; do
  curl -X POST http://payment-wasm/api/payment -d @large.json &
done
wait
# 所有请求成功，无 OOMKilled
```

### 6.2 验证结果

- ✅ **Pod 状态**：`Running`，无重启
- ✅ **内存使用**：45Mi（在 100Mi 限制范围内）
- ✅ **功能测试**：所有 JSON 大小测试通过
- ✅ **压力测试**：100 并发请求全部成功，无 OOMKilled

### 6.3 验证时间

- **验证时间**：2025-11-11 12:30
- **验证人员**：运维团队
- **验证环境**：生产环境

---

## 7 经验总结

### 7.1 关键教训

1. **Wasm 内存限制需要合理配置**：
   - 应根据实际数据处理需求设置内存限制
   - 考虑原始数据和处理过程中的临时对象内存占用

2. **大 JSON 处理需要优化**：
   - 避免一次性加载整个 JSON
   - 使用流式处理或分块处理

3. **内存监控很重要**：
   - 定期监控 Wasm 应用的内存使用
   - 及时发现内存问题

### 7.2 最佳实践

1. **内存限制配置**：
   - 根据实际数据处理需求设置内存限制
   - 为处理过程中的临时对象留出空间（通常为数据大小的 2-3 倍）

2. **应用代码优化**：
   - 对于大 JSON，使用流式处理
   - 限制输入数据大小
   - 及时释放不需要的内存

3. **监控和告警**：
   - 监控内存使用率
   - 设置内存使用告警（建议阈值：80%）

4. **测试和验证**：
   - 测试不同数据大小的内存使用
   - 进行压力测试，验证内存限制的合理性

### 7.3 相关文档

- [`../troubleshooting.md`](../troubleshooting.md#1124-wasmedge-out-of-bounds-错误) - 故障排查指南
- [`../../../../COGNITIVE/05-decision-analysis/benchmarks/benchmarks.md`](../../../../COGNITIVE/05-decision-analysis/benchmarks/benchmarks.md) - 性能基准文档
- [`../../PRACTICAL-CASE-SUPPLEMENT-PLAN.md`](../../PRACTICAL-CASE-SUPPLEMENT-PLAN.md) - 实践案例补充计划

---

## 8 相关文档

- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南
- [`../cases/README.md`](README.md) - 案例集目录
- [`../../../../COGNITIVE/05-decision-analysis/benchmarks/benchmarks.md`](../../../../COGNITIVE/05-decision-analysis/benchmarks/benchmarks.md) - 性能基准文档

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
