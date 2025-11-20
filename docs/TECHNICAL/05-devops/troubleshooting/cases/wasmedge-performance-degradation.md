# 案例 W-006：Wasm 性能下降

> **案例编号**：W-006
> **故障类型**：性能问题
> **严重程度**：轻微
> **创建日期**：2025-11-15
> **最后更新**：2025-11-15

---

## 📑 目录

- [案例 W-006：Wasm 性能下降](#案例-w-006wasm-性能下降)
  - [📑 目录](#-目录)
  - [1. 问题描述](#1-问题描述)
    - [1.1 故障现象](#11-故障现象)
    - [1.2 环境信息](#12-环境信息)
    - [1.3 影响范围](#13-影响范围)
  - [2. 故障排查过程](#2-故障排查过程)
    - [2.1 初步诊断](#21-初步诊断)
    - [2.2 深入排查](#22-深入排查)
    - [2.3 根因分析](#23-根因分析)
  - [3. 解决方案](#3-解决方案)
    - [3.1 临时解决方案](#31-临时解决方案)
    - [3.2 永久解决方案](#32-永久解决方案)
    - [3.3 预防措施](#33-预防措施)
  - [4. 验证与恢复](#4-验证与恢复)
    - [4.1 验证步骤](#41-验证步骤)
    - [4.2 恢复确认](#42-恢复确认)
  - [5. 经验总结](#5-经验总结)
    - [5.1 关键发现](#51-关键发现)
    - [5.2 最佳实践](#52-最佳实践)
    - [5.3 相关文档](#53-相关文档)
  - [6. 相关文档](#6-相关文档)

---

## 1. 问题描述

### 1.1 故障现象

**主要症状**：

- Wasm 应用响应时间逐渐增加
- 应用吞吐量下降，从 1000 QPS 降至 600 QPS
- CPU 使用率异常升高，从 20% 升至 60%
- 内存使用量持续增长，存在内存泄漏迹象
- 应用延迟 P99 从 10ms 增加到 50ms

**性能指标变化**：

| 指标 | 正常值 | 异常值 | 变化幅度 |
|------|--------|--------|----------|
| **响应时间 P50** | 5ms | 15ms | +200% |
| **响应时间 P99** | 10ms | 50ms | +400% |
| **吞吐量 QPS** | 1000 | 600 | -40% |
| **CPU 使用率** | 20% | 60% | +200% |
| **内存使用** | 128MB | 256MB | +100% |

**错误日志**：

```text
2025-11-15T16:30:00.123Z WARN [wasm-app] Request processing time: 45ms (threshold: 20ms)
2025-11-15T16:30:05.456Z WARN [wasm-app] Memory usage: 200MB (threshold: 150MB)
2025-11-15T16:30:10.789Z ERROR [wasm-app] GC pause time: 15ms (threshold: 5ms)
2025-11-15T16:30:15.012Z WARN [wasm-app] CPU usage: 65% (threshold: 50%)
```

**时间线**：

- **16:00:00** - 应用正常启动，性能指标正常
- **16:15:00** - 开始出现性能下降迹象
- **16:30:00** - 性能明显下降，触发告警
- **16:45:00** - 性能持续恶化，需要紧急处理

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **WasmEdge 版本**：v0.14.0
- **CNI 插件**：flannel
- **监控系统**：Prometheus + Grafana

**应用配置**：

- **Runtime**：WasmEdge
- **工作负载**：高并发 API 服务
- **请求模式**：短连接，高频率
- **数据量**：每个请求处理 1-10KB 数据

**Pod 信息**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-performance-001
  namespace: default
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      resources:
        requests:
          cpu: "500m"
          memory: "256Mi"
        limits:
          cpu: "1000m"
          memory: "512Mi"
      env:
        - name: MAX_CONCURRENT_REQUESTS
          value: "100"
        - name: ENABLE_GC
          value: "true"
```

### 1.3 影响范围

- **受影响 Pod**：1 个（wasm-app-performance-001）
- **受影响服务**：API 服务
- **业务影响**：响应时间增加，用户体验下降
- **用户影响**：部分用户请求超时，服务可用性降低

---

## 2. 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 Pod 资源使用**：

```bash
# 检查 Pod 资源使用情况
kubectl top pod wasm-app-performance-001 -n default

# 输出
NAME                        CPU(cores)   MEMORY(bytes)
wasm-app-performance-001   650m         256Mi
```

**步骤 2：查看应用日志**：

```bash
# 查看应用日志
kubectl logs wasm-app-performance-001 -n default --tail=100

# 输出显示性能警告和 GC 暂停时间增加
```

**步骤 3：检查 Prometheus 指标**：

```bash
# 查询响应时间指标
curl -G 'http://prometheus:9090/api/v1/query' \
  --data-urlencode 'query=histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))'

# 输出显示 P99 延迟增加到 50ms
```

**初步结论**：

- CPU 使用率异常高（65%）
- 内存使用量持续增长
- 响应时间明显增加
- GC 暂停时间过长

### 2.2 深入排查

**步骤 4：分析 CPU 使用情况**：

```bash
# 使用 perf 工具分析 CPU 热点
kubectl exec -it wasm-app-performance-001 -n default -- perf record -g -p 1 sleep 10
kubectl exec -it wasm-app-performance-001 -n default -- perf report

# 发现大量时间花费在内存分配和 GC 上
```

**步骤 5：检查内存分配模式**：

```bash
# 检查内存分配统计
kubectl exec -it wasm-app-performance-001 -n default -- \
  wasmedge --enable-all-statistics wasm-app.wasm

# 发现频繁的内存分配和释放
```

**步骤 6：分析 Wasm 模块性能**：

```bash
# 使用 WasmEdge 性能分析工具
wasmedge --enable-all-statistics --enable-time-measuring wasm-app.wasm

# 发现函数调用开销过大
```

**步骤 7：检查网络 I/O**：

```bash
# 检查网络 I/O 统计
kubectl exec -it wasm-app-performance-001 -n default -- \
  cat /proc/net/sockstat

# 发现大量 TIME_WAIT 连接
```

**深入排查结论**：

- 内存分配频繁，导致 GC 压力大
- 函数调用开销过大
- 网络连接未正确关闭，导致资源泄漏
- Wasm 模块未启用优化编译

### 2.3 根因分析

**根因 1：内存分配频繁**：

- 应用代码中存在频繁的内存分配
- 未使用对象池或内存复用机制
- GC 压力大，导致暂停时间增加

**根因 2：Wasm 模块未优化**：

- Wasm 模块编译时未启用优化选项
- 未使用 AOT（Ahead-of-Time）编译
- 函数调用开销过大

**根因 3：资源泄漏**：

- 网络连接未正确关闭
- 事件监听器未清理
- 定时器未取消

**根因 4：并发控制不当**：

- 并发请求数过高，超出处理能力
- 缺少请求限流机制
- 资源竞争导致性能下降

**根本原因**：

**Wasm 模块性能优化不足和资源管理不当**：Wasm 模块未启用优化编译，且应用代码存在内存分配频繁、资源泄漏等问题，导致性能逐渐下降。

---

## 3. 解决方案

### 3.1 临时解决方案

**方案 1：增加资源限制**：

```yaml
# 临时增加 CPU 和内存限制
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-performance-001
  namespace: default
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      resources:
        requests:
          cpu: "1000m"  # 从 500m 增加到 1000m
          memory: "512Mi"  # 从 256Mi 增加到 512Mi
        limits:
          cpu: "2000m"  # 从 1000m 增加到 2000m
          memory: "1Gi"  # 从 512Mi 增加到 1Gi
```

**方案 2：降低并发数**：

```yaml
# 降低并发请求数
env:
  - name: MAX_CONCURRENT_REQUESTS
    value: "50"  # 从 100 降低到 50
```

**临时方案效果**：

- ✅ 可以快速缓解性能问题
- ⚠️ 但未解决根本问题
- ⚠️ 资源消耗增加

### 3.2 永久解决方案

**方案 1：优化 Wasm 模块编译**：

```bash
# 使用优化选项编译 Wasm 模块
wasm-pack build --target web --release -- --opt-level 3

# 或使用 wasm-opt 进行优化
wasm-opt wasm-app.wasm -o wasm-app-optimized.wasm \
  -O3 \
  --enable-bulk-memory \
  --enable-threads
```

**方案 2：启用 AOT 编译**：

```bash
# 使用 WasmEdge AOT 编译
wasmedgec wasm-app.wasm wasm-app.aot

# 使用 AOT 编译后的模块
wasmedge wasm-app.aot
```

**方案 3：优化内存管理**：

```rust
// 使用对象池减少内存分配
use std::collections::VecDeque;

struct ObjectPool<T> {
    pool: VecDeque<T>,
}

impl<T> ObjectPool<T> {
    fn get(&mut self) -> Option<T> {
        self.pool.pop_front()
    }

    fn put(&mut self, obj: T) {
        self.pool.push_back(obj);
    }
}

// 使用对象池
let mut pool = ObjectPool::new();
let obj = pool.get().unwrap_or_else(|| create_new_object());
// 使用对象
pool.put(obj);
```

**方案 4：修复资源泄漏**：

```rust
// 确保资源正确释放
use std::sync::Arc;

struct Connection {
    // 连接资源
}

impl Drop for Connection {
    fn drop(&mut self) {
        // 清理资源
        self.close();
    }
}

// 使用 RAII 模式管理资源
let conn = Arc::new(Connection::new());
// 使用连接
// 连接会在作用域结束时自动释放
```

**方案 5：添加请求限流**：

```rust
// 使用令牌桶算法限流
use std::sync::atomic::{AtomicU64, Ordering};
use std::time::{Duration, Instant};

struct RateLimiter {
    tokens: AtomicU64,
    last_refill: Instant,
    capacity: u64,
    refill_rate: u64, // tokens per second
}

impl RateLimiter {
    fn try_acquire(&self) -> bool {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_refill);
        let tokens_to_add = (elapsed.as_secs_f64() * self.refill_rate as f64) as u64;

        let current = self.tokens.fetch_update(
            Ordering::SeqCst,
            Ordering::SeqCst,
            |tokens| {
                let new_tokens = (tokens + tokens_to_add).min(self.capacity);
                if new_tokens > 0 {
                    Some(new_tokens - 1)
                } else {
                    None
                }
            }
        );

        current.is_ok()
    }
}
```

**方案 6：优化 GC 配置**：

```yaml
# 调整 GC 参数
env:
  - name: ENABLE_GC
    value: "true"
  - name: GC_THRESHOLD
    value: "80"  # GC 触发阈值（百分比）
  - name: GC_INTERVAL
    value: "1000"  # GC 间隔（毫秒）
```

### 3.3 预防措施

1. **性能监控**：
   - 配置性能指标监控和告警
   - 定期进行性能测试和基准测试

2. **代码审查**：
   - 审查代码中的内存分配模式
   - 检查资源管理是否正确

3. **编译优化**：
   - 始终使用优化选项编译 Wasm 模块
   - 考虑使用 AOT 编译提升性能

4. **压力测试**：
   - 定期进行压力测试
   - 验证性能在负载下的表现

---

## 4. 验证与恢复

### 4.1 验证步骤

**步骤 1：验证性能指标**：

```bash
# 查询性能指标
curl -G 'http://prometheus:9090/api/v1/query' \
  --data-urlencode 'query=histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))'

# 应该看到 P99 延迟恢复到 10ms 以下
```

**步骤 2：验证资源使用**：

```bash
# 检查资源使用情况
kubectl top pod wasm-app-performance-001 -n default

# 应该看到 CPU 和内存使用率恢复正常
```

**步骤 3：压力测试**：

```bash
# 运行压力测试
ab -n 10000 -c 100 http://wasm-app-service:8080/api/test

# 应该看到吞吐量和响应时间恢复正常
```

### 4.2 恢复确认

**恢复时间线**：

- **故障发现**：16:30:00
- **开始排查**：16:30:05
- **根因确认**：16:40:00
- **问题解决**：17:00:00
- **服务恢复**：17:00:05
- **总耗时**：30 分钟

**恢复验证**：

- ✅ 响应时间 P99 恢复到 10ms 以下
- ✅ 吞吐量恢复到 1000 QPS
- ✅ CPU 使用率降低到 20%
- ✅ 内存使用稳定，无泄漏
- ✅ 应用性能恢复正常

---

## 5. 经验总结

### 5.1 关键发现

1. **Wasm 模块优化至关重要**：
   - 使用优化选项编译可以显著提升性能
   - AOT 编译可以进一步减少启动时间和运行时开销

2. **内存管理是关键**：
   - 频繁的内存分配会导致 GC 压力
   - 使用对象池可以减少内存分配

3. **资源泄漏会导致性能下降**：
   - 未正确释放的资源会逐渐累积
   - 需要确保所有资源都有正确的生命周期管理

4. **并发控制很重要**：
   - 过高的并发会导致资源竞争
   - 需要合理的限流机制

### 5.2 最佳实践

1. **编译优化**：
   - 始终使用 `-O3` 优化选项
   - 考虑使用 AOT 编译

2. **内存管理**：
   - 使用对象池减少分配
   - 避免频繁的小对象分配

3. **资源管理**：
   - 使用 RAII 模式管理资源
   - 确保所有资源都有正确的清理逻辑

4. **性能监控**：
   - 配置性能指标监控
   - 设置合理的告警阈值

5. **压力测试**：
   - 定期进行压力测试
   - 验证性能在负载下的表现

### 5.3 相关文档

- [`../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md`](../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md) - WasmEdge 文档
- [`../../TECHNICAL/05-devops/performance-optimization/cases/wasm-cold-start-optimization.md`](../../TECHNICAL/05-devops/performance-optimization/cases/wasm-cold-start-optimization.md) - Wasm 冷启动优化案例
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

## 6. 相关文档

- [`../README.md`](README.md) - 故障排查案例集目录
- [`../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md`](../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md) - WasmEdge 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

**最后更新**：2025-11-15
**维护者**：项目团队
**版本**：v1.0
