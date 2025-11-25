# 性能测试方法和测试环境说明

> **创建日期**：2025-11-15
> **最后更新**：2025-11-15
> **维护者**：项目团队

---

## 📑 目录

- [性能测试方法和测试环境说明](#性能测试方法和测试环境说明)
  - [📑 目录](#-目录)
  - [1. 文档概述](#1-文档概述)
  - [2. 测试环境配置](#2-测试环境配置)
    - [2.1 硬件环境](#21-硬件环境)
    - [2.2 软件环境](#22-软件环境)
  - [3. 性能测试方法](#3-性能测试方法)
    - [3.1 冷启动时间测试](#31-冷启动时间测试)
    - [3.2 延迟测试](#32-延迟测试)
    - [3.3 吞吐量测试](#33-吞吐量测试)
    - [3.4 资源占用测试](#34-资源占用测试)
  - [4. 性能指标定义](#4-性能指标定义)
    - [4.1 启动时间指标](#41-启动时间指标)
    - [4.2 延迟指标](#42-延迟指标)
    - [4.3 吞吐量指标](#43-吞吐量指标)
    - [4.4 资源占用指标](#44-资源占用指标)
  - [5. 测试工具和脚本](#5-测试工具和脚本)
    - [5.1 测试脚本示例](#51-测试脚本示例)
    - [5.2 测试工具安装](#52-测试工具安装)
  - [6. 测试结果分析](#6-测试结果分析)
    - [6.1 结果记录格式](#61-结果记录格式)
    - [6.2 结果分析方法](#62-结果分析方法)
  - [7. 参考资源](#7-参考资源)
    - [7.1 测试工具文档](#71-测试工具文档)
    - [7.2 性能测试最佳实践](#72-性能测试最佳实践)

---

## 1. 文档概述

本文档提供**性能测试方法和测试环境说明**，用于验证项目中案例和文档中提到的性能指标。

**文档目标**：

- ✅ 提供标准化的性能测试方法
- ✅ 说明测试环境配置要求
- ✅ 定义性能指标的计算方法
- ✅ 提供测试工具和脚本
- ✅ 说明测试结果分析方法

**适用范围**：

- 所有案例中的性能指标验证
- 技术文档中的性能对比分析
- 技术选型决策的性能评估

---

## 2. 测试环境配置

### 2.1 硬件环境

**标准测试环境**：

| 组件 | 配置 | 说明 |
|------|------|------|
| **CPU** | Intel Xeon E5-2680 v4 (14核) 或同等性能 | 支持硬件虚拟化（VT-x） |
| **内存** | 64GB DDR4 | 足够运行多个 VM/容器 |
| **存储** | 500GB SSD (NVMe) | 低延迟存储 |
| **网络** | 10Gbps 网卡 | 网络性能测试 |

**边缘测试环境**：

| 组件 | 配置 | 说明 |
|------|------|------|
| **CPU** | ARM Cortex-A72 (4核) 或同等性能 | ARM64 架构 |
| **内存** | 8GB LPDDR4 | 资源受限环境 |
| **存储** | 64GB eMMC | 嵌入式存储 |
| **网络** | 1Gbps 网卡 | 边缘网络环境 |

### 2.2 软件环境

**操作系统**：

- **Host OS**：Ubuntu 22.04 LTS 或 CentOS 8
- **Kernel**：Linux 5.15+（支持 eBPF）
- **容器运行时**：containerd 2.0+
- **编排平台**：Kubernetes 1.31+ 或 K3s 1.30.4+

**测试工具**：

- **压力测试**：wrk、ab、hey
- **性能监控**：Prometheus、Grafana
- **追踪工具**：Jaeger、OpenTelemetry
- **资源监控**：cAdvisor、node-exporter

---

## 3. 性能测试方法

### 3.1 冷启动时间测试

**测试方法**：

1. **准备测试环境**：

   ```bash
   # 清理所有容器/VM
   kubectl delete pods --all

   # 等待资源释放
   sleep 30
   ```

2. **执行冷启动测试**：

   ```bash
   # 记录启动开始时间
   START_TIME=$(date +%s%N)

   # 创建 Pod
   kubectl apply -f test-pod.yaml

   # 等待 Pod Ready
   kubectl wait --for=condition=Ready pod/test-pod --timeout=60s

   # 记录启动结束时间
   END_TIME=$(date +%s%N)

   # 计算启动时间（毫秒）
   STARTUP_TIME=$((($END_TIME - $START_TIME) / 1000000))
   echo "Cold start time: ${STARTUP_TIME}ms"
   ```

3. **重复测试**：
   - 执行 10 次测试
   - 计算平均值、P50、P99

**测试指标**：

- **冷启动时间**：从创建 Pod 到 Pod Ready 的时间
- **首次响应时间**：从 Pod Ready 到首次响应的时间

### 3.2 延迟测试

**测试方法**：

1. **准备测试环境**：

   ```bash
   # 部署测试应用
   kubectl apply -f test-app.yaml

   # 等待应用就绪
   kubectl wait --for=condition=Ready pod/test-app --timeout=60s
   ```

2. **执行延迟测试**：

   ```bash
   # 使用 wrk 进行延迟测试
   wrk -t4 -c100 -d30s --latency http://test-app:8080/api/test
   ```

3. **分析结果**：
   - P50 延迟（中位数）
   - P95 延迟
   - P99 延迟
   - 平均延迟

**测试指标**：

- **P50 延迟**：50% 请求的延迟
- **P95 延迟**：95% 请求的延迟
- **P99 延迟**：99% 请求的延迟
- **平均延迟**：所有请求的平均延迟

### 3.3 吞吐量测试

**测试方法**：

1. **准备测试环境**：

   ```bash
   # 部署测试应用
   kubectl apply -f test-app.yaml
   ```

2. **执行吞吐量测试**：

   ```bash
   # 使用 hey 进行吞吐量测试
   hey -n 100000 -c 100 http://test-app:8080/api/test
   ```

3. **分析结果**：
   - QPS（每秒请求数）
   - 吞吐量（MB/s）
   - 错误率

**测试指标**：

- **QPS**：每秒处理的请求数
- **吞吐量**：每秒处理的数据量（MB/s）
- **错误率**：失败请求的百分比

### 3.4 资源占用测试

**测试方法**：

1. **准备测试环境**：

   ```bash
   # 部署测试应用
   kubectl apply -f test-app.yaml
   ```

2. **监控资源占用**：

   ```bash
   # 使用 cAdvisor 监控资源
   kubectl top pod test-app

   # 或使用 Prometheus 查询
   curl -G 'http://prometheus:9090/api/v1/query' \
     --data-urlencode 'query=container_memory_usage_bytes{pod="test-app"}'
   ```

3. **分析结果**：
   - CPU 使用率（%）
   - 内存占用（MB）
   - 网络带宽（Mbps）
   - 存储 I/O（IOPS）

**测试指标**：

- **CPU 使用率**：CPU 使用百分比
- **内存占用**：内存使用量（MB）
- **网络带宽**：网络吞吐量（Mbps）
- **存储 I/O**：存储 IOPS

---

## 4. 性能指标定义

### 4.1 启动时间指标

| 指标 | 定义 | 计算方法 |
|------|------|---------|
| **冷启动时间** | 从创建 Pod 到 Pod Ready 的时间 | `(Ready时间 - Create时间) / 1000000` (ms) |
| **首次响应时间** | 从 Pod Ready 到首次响应的时间 | `(FirstResponse时间 - Ready时间) / 1000000` (ms) |
| **总启动时间** | 从创建 Pod 到首次响应的时间 | `冷启动时间 + 首次响应时间` |

### 4.2 延迟指标

| 指标 | 定义 | 计算方法 |
|------|------|---------|
| **P50 延迟** | 50% 请求的延迟 | 排序后的第 50 百分位数 |
| **P95 延迟** | 95% 请求的延迟 | 排序后的第 95 百分位数 |
| **P99 延迟** | 99% 请求的延迟 | 排序后的第 99 百分位数 |
| **平均延迟** | 所有请求的平均延迟 | `总延迟 / 请求数` |

### 4.3 吞吐量指标

| 指标 | 定义 | 计算方法 |
|------|------|---------|
| **QPS** | 每秒处理的请求数 | `总请求数 / 测试时间` |
| **吞吐量** | 每秒处理的数据量 | `总数据量 / 测试时间` (MB/s) |
| **并发数** | 同时处理的请求数 | 测试工具配置的并发数 |

### 4.4 资源占用指标

| 指标 | 定义 | 计算方法 |
|------|------|---------|
| **CPU 使用率** | CPU 使用百分比 | `(CPU使用时间 / CPU总时间) * 100` |
| **内存占用** | 内存使用量 | `RSS + Cache` (MB) |
| **网络带宽** | 网络吞吐量 | `(发送字节数 + 接收字节数) / 测试时间` (Mbps) |
| **存储 I/O** | 存储 IOPS | `(读IOPS + 写IOPS)` |

---

## 5. 测试工具和脚本

### 5.1 测试脚本示例

**冷启动测试脚本**：

```bash
#!/bin/bash
# cold-start-test.sh

POD_NAME="test-pod"
ITERATIONS=10
RESULTS=()

for i in $(seq 1 $ITERATIONS); do
    # 清理
    kubectl delete pod $POD_NAME --ignore-not-found=true
    sleep 5

    # 记录开始时间
    START_TIME=$(date +%s%N)

    # 创建 Pod
    kubectl apply -f test-pod.yaml

    # 等待 Ready
    kubectl wait --for=condition=Ready pod/$POD_NAME --timeout=60s

    # 记录结束时间
    END_TIME=$(date +%s%N)

    # 计算启动时间（毫秒）
    STARTUP_TIME=$((($END_TIME - $START_TIME) / 1000000))
    RESULTS+=($STARTUP_TIME)

    echo "Iteration $i: ${STARTUP_TIME}ms"
done

# 计算统计值
AVG=$(echo "${RESULTS[@]}" | awk '{sum=0; for(i=1;i<=NF;i++) sum+=$i; print sum/NF}')
echo "Average: ${AVG}ms"
```

**延迟测试脚本**：

```bash
#!/bin/bash
# latency-test.sh

URL="http://test-app:8080/api/test"
DURATION=30
CONCURRENCY=100

# 使用 wrk 进行延迟测试
wrk -t4 -c$CONCURRENCY -d${DURATION}s --latency $URL
```

### 5.2 测试工具安装

**安装 wrk**：

```bash
# Ubuntu/Debian
sudo apt-get install wrk

# CentOS/RHEL
sudo yum install wrk

# 或从源码编译
git clone https://github.com/wg/wrk.git
cd wrk
make
sudo cp wrk /usr/local/bin/
```

**安装 hey**：

```bash
# 下载 hey
wget https://github.com/rakyll/hey/releases/download/v0.1.4/hey_linux_amd64
chmod +x hey_linux_amd64
sudo mv hey_linux_amd64 /usr/local/bin/hey
```

---

## 6. 测试结果分析

### 6.1 结果记录格式

**测试结果记录**：

```markdown
## 性能测试结果

**测试日期**：2025-11-15

**测试环境**：
- CPU: Intel Xeon E5-2680 v4 (14核)
- 内存: 64GB DDR4
- 存储: 500GB SSD (NVMe)
- 网络: 10Gbps

**测试配置**：
- 并发数: 100
- 测试时长: 30s
- 测试次数: 10

**测试结果**：

| 指标 | 数值 | 单位 |
|------|------|------|
| 冷启动时间 | 8.5 | ms |
| P50 延迟 | 12.3 | ms |
| P95 延迟 | 25.6 | ms |
| P99 延迟 | 45.2 | ms |
| QPS | 10,000 | req/s |
| CPU 使用率 | 45.2 | % |
| 内存占用 | 128 | MB |
```

### 6.2 结果分析方法

**统计分析**：

- **平均值**：所有测试结果的平均值
- **中位数**：排序后的中间值
- **标准差**：数据的离散程度
- **百分位数**：P50、P95、P99

**对比分析**：

- **与基准对比**：与标准基准对比
- **与理论值对比**：与理论分析值对比
- **趋势分析**：多次测试的趋势分析

---

## 7. 参考资源

### 7.1 测试工具文档

- **wrk**: <https://github.com/wg/wrk>
- **hey**: <https://github.com/rakyll/hey>
- **ab**: <https://httpd.apache.org/docs/2.4/programs/ab.html>

### 7.2 性能测试最佳实践

- **Kubernetes 性能测试**: <https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/>
- **容器性能测试**: <https://docs.docker.com/config/containers/resource_constraints/>
- **eBPF 性能分析**: <https://ebpf.io/what-is-ebpf/>

---

**最后更新**：2025-11-15
**维护者**：项目团队
