# 技术栈分层架构图：思维导图视角

**版本**：v1.1 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 核心问题](#11-核心问题)
  - [1.2 架构设计原则](#12-架构设计原则)
    - [1.2.1 关注点分离（Separation of Concerns）](#121-关注点分离separation-of-concerns)
    - [1.2.2 单向数据流（Unidirectional Data Flow）](#122-单向数据流unidirectional-data-flow)
    - [1.2.3 水平扩展优先（Horizontal Scaling First）](#123-水平扩展优先horizontal-scaling-first)
  - [1.3 分层架构理论](#13-分层架构理论)
- [2 垂直穿透架构：从内核到后端的单向数据流](#2-垂直穿透架构从内核到后端的单向数据流)
  - [2.1 第 1 层：内核态执行沙盒](#21-第-1-层内核态执行沙盒)
  - [2.2 第 2 层：容器化命名空间](#22-第-2-层容器化命名空间)
  - [2.3 第 3 层：用户态 Agent（DaemonSet）](#23-第-3-层用户态-agentdaemonset)
  - [2.4 第 4 层：OTLP 协议传输](#24-第-4-层otlp-协议传输)
  - [2.5 第 5 层：Collector 处理管道](#25-第-5-层collector-处理管道)
  - [2.6 第 6 层：后端存储生态](#26-第-6-层后端存储生态)
  - [2.7 第 7 层：智能控制面](#27-第-7-层智能控制面)
  - [2.8 架构思维导图解读](#28-架构思维导图解读)
- [3 水平扩展架构：多租户与多集群联邦](#3-水平扩展架构多租户与多集群联邦)
  - [3.1 边缘集群架构](#31-边缘集群架构)
  - [3.2 中心集群架构](#32-中心集群架构)
  - [3.3 虚拟化环境](#33-虚拟化环境)
  - [3.4 多云环境](#34-多云环境)
  - [3.5 扩展性洞察](#35-扩展性洞察)
- [4 控制闭环架构：从感知到自愈的反馈回路](#4-控制闭环架构从感知到自愈的反馈回路)
  - [4.1 执行层（Actuator）](#41-执行层actuator)
  - [4.2 分析层（Analyzer）](#42-分析层analyzer)
  - [4.3 感知层（Sensor）](#43-感知层sensor)
  - [4.4 数据层（Data）](#44-数据层data)
  - [4.5 决策层（Controller）](#45-决策层controller)
  - [4.6 控制闭环特性](#46-控制闭环特性)
- [5 架构模式分析](#5-架构模式分析)
  - [5.1 分层模式（Layered Pattern）](#51-分层模式layered-pattern)
  - [5.2 管道-过滤器模式（Pipe-Filter Pattern）](#52-管道-过滤器模式pipe-filter-pattern)
  - [5.3 事件驱动模式（Event-Driven Pattern）](#53-事件驱动模式event-driven-pattern)
- [6 结论与展望](#6-结论与展望)
  - [6.1 核心结论](#61-核心结论)
  - [6.2 理论意义](#62-理论意义)
  - [6.3 未来展望](#63-未来展望)
- [🔗 相关文档](#-相关文档)

---

## 1 概述

### 1.1 核心问题

传统可观测性架构采用"烟囱式"设计，各层职责不清，导致：

- **层次混乱**：业务逻辑、采集逻辑、处理逻辑混合
- **依赖复杂**：组件间依赖关系复杂，难以理解
- **扩展困难**：水平扩展和垂直扩展都面临挑战

### 1.2 架构设计原则

#### 1.2.1 关注点分离（Separation of Concerns）

**原则**：每一层只关注一个关注点，职责单一。

**应用**：

- **内核层**：只负责数据采集
- **用户态层**：只负责数据处理
- **协议层**：只负责数据传输
- **存储层**：只负责数据存储

#### 1.2.2 单向数据流（Unidirectional Data Flow）

**原则**：数据从底层流向高层，避免反向依赖。

**应用**：

- 数据流：内核 → 用户态 → 协议 → 处理 → 存储
- 控制流：控制面 → 执行层（反向）

#### 1.2.3 水平扩展优先（Horizontal Scaling First）

**原则**：优先通过增加实例实现扩展，而非垂直扩展。

**应用**：

- DaemonSet 模式：每个节点一个 Agent
- Collector 集群：多实例负载均衡

### 1.3 分层架构理论

根据软件架构中的分层架构理论：

**经典分层架构**：

```text
表示层（Presentation Layer）
业务逻辑层（Business Logic Layer）
数据访问层（Data Access Layer）
```

**eBPF+OTLP 分层架构**：

```text
内核执行层（Kernel Execution Layer）
容器化层（Containerization Layer）
用户态处理层（User Space Processing Layer）
协议传输层（Protocol Transport Layer）
数据处理层（Data Processing Layer）
存储层（Storage Layer）
控制层（Control Layer）
```

**分层优势**：

- **可维护性**：每层独立维护
- **可测试性**：每层独立测试
- **可扩展性**：每层独立扩展

---

## 2 垂直穿透架构：从内核到后端的单向数据流

### 2.1 第 1 层：内核态执行沙盒

**核心组件**：

- **内核函数**：tcp_connect()
- **eBPF Program**：kprobe/tcp_connect
- **当前进程上下文**：PID=12345
- **网络包元数据**：sk_buff
- **时间戳**：bpf_ktime_get_ns()
- **延迟计算**：delta = t2 - t1
- **BPF_MAP_TYPE_HASH**：Key: <PodIP,Port>, Value: latency_hist

**沙盒安全**：

- **Verifier**：静态分析
  - **验证时间**：10-5000ms
  - **验证通过率**：>95%
  - **失败处理**：拒绝加载，verifier_error.log → OTLP Log Exporter
- **JIT Compiler**：x86-64 机器码
  - **编译时间**：<10ms
  - **执行效率**：接近原生代码（>95%）

**性能指标**：

- **延迟**：<1μs（内核态执行）
- **吞吐量**：>1M events/s
- **CPU 开销**：<1%

### 2.2 第 2 层：容器化命名空间

**核心组件**：

- **Container Runtime**：runc/containerd
- **cgroup**：/k8s/pod-abc
- **进程 PID**：12345
- **Network Namespace**：netns=4026532245
- **Pod 定义**：Labels: team=payments
- **K8s API Server**：查询元数据
- **元数据注入**：k8s.pod.name=payment-abc

**命名空间隔离**：

- **PID Namespace**：进程隔离
- **Network Namespace**：网络隔离
- **Mount Namespace**：文件系统隔离
- **UTS Namespace**：主机名隔离

**元数据关联**：

```text
PID → cgroup_id → Pod UID → K8s Labels → OTLP Resource
```

### 2.3 第 3 层：用户态 Agent（DaemonSet）

**核心组件**：

- **eBPF Agent**：DaemonSet 单例
- **轮询 Map**：读取 BPF_MAP_TYPE_HASH
- **BTF 解析**：符号解析 func_name=tcp_connect
- **上下文关联**：PID→Pod→Service
- **原始事件流**：10000 events/s
- **批处理**：Batch Processor (timeout=5s, size=1000)
- **OTLP 格式转换**：Resource, Spans, Metrics
- **压缩**：ZSTD 压缩（压缩率 5:1）

**处理流程**：

```text
读取 Map → BTF 解析 → 上下文关联 → 批处理 → OTLP 转换 → 压缩
```

**性能指标**：

- **处理延迟**：<10ms（批处理）
- **内存占用**：200MB/节点
- **CPU 占用**：<5%

### 2.4 第 4 层：OTLP 协议传输

**核心组件**：

- **OTLP gRPC Exporter**：发送
- **HTTP/2 + gRPC**：承载
- **Protocol Buffer 序列化**：优化
- **Apache Arrow 列式编码**：批大小=10000 行
- **mTLS 双向认证**：Cert-ID: eb1f2a
- **网络边界**：延迟<100ms

**协议特性**：

- **序列化效率**：Protobuf 比 JSON 快 **3-5 倍**
- **压缩率**：Arrow + ZSTD 压缩率 **5:1**
- **带宽节省**：相比传统格式节省 **80%**

### 2.5 第 5 层：Collector 处理管道

**核心组件**：

- **OTLP Receiver**：接收
- **准入控制**：限流/背压
- **Resource Detection Processor**：注入 k8s 属性
- **Metrics Transform**：Histogram→ExponentialHistogram
- **Tail-based Sampling**：异常事件全采样
- **Routing Processor**：按租户/服务分流

**处理管道**：

```text
接收 → 限流 → 资源检测 → 转换 → 采样 → 路由 → 导出
```

**性能指标**：

- **吞吐量**：>100K spans/s
- **延迟**：<50ms（端到端）
- **采样率**：1-100%（可配置）

### 2.6 第 6 层：后端存储生态

**存储后端**：

- **Prometheus Remote Write**：时序数据
- **Elasticsearch**：日志数据
- **Jaeger gRPC**：追踪数据
- **Tempo HTTP**：追踪数据
- **ClickHouse**：分析数据

**存储特性**：

- **数据保留**：7-90 天（可配置）
- **查询延迟**：<100ms（P95）
- **存储成本**：$0.01/GB/月（S3）

### 2.7 第 7 层：智能控制面

**核心组件**：

- **Prometheus Alertmanager**：触发告警
- **自定义 HPA Controller**：驱动伸缩
- **K8s Policy Engine**：OPA/Rego，安全事件

**控制流程**：

```text
监控数据 → 告警规则 → 告警触发 → 策略执行 → 动作反馈
```

### 2.8 架构思维导图解读

**七层垂直穿透**：

- 内核态 → 容器化 → 用户态 → 协议 → 处理 → 存储 → 控制
- 每层职责单一，单层省却率达 **70-100%**

**关键节点**：

- **`Verifier`**（红色）：安全边界，静态验证
- **`BPF_MAP`**（绿色）：数据枢纽，零拷贝传输
- **`Arrow 编码`**（蓝色）：效率引擎，带宽节省 80%

**数据流动**：

- 单向流动，无反向依赖
- 符合事件驱动架构原则

---

## 3 水平扩展架构：多租户与多集群联邦

### 3.1 边缘集群架构

**边缘集群 1（Edge）**：

- **eBPF Agent**：节点=50
- **Edge Collector**：缓存+预处理
- **压缩批处理**：ZSTD+限流
- **跨地域传输**：带宽=10Mbps

**边缘特性**：

- **低延迟**：本地处理，延迟<10ms
- **带宽优化**：压缩+限流，带宽节省 **80%**
- **离线能力**：本地缓存，网络中断时可用

### 3.2 中心集群架构

**中心集群（Central）**：

- **Global Collector**：多租户隔离
- **Router**：
  - Tenant A Stream（QoS=高）
  - Tenant B Stream（QoS=中）
  - Tenant C Stream（QoS=低）
- **存储**：
  - VictoriaMetrics（保留 30 天）
  - Elasticsearch（保留 7 天）
  - 低成本 S3（保留 90 天）

**多租户隔离**：

- **QoS 分级**：高/中/低优先级
- **资源隔离**：CPU/内存/带宽配额
- **数据隔离**：租户级数据分区

### 3.3 虚拟化环境

**KVM Host1**：VM 数=20 **KVM Host2**：VM 数=20 **VM 层 Collector**：聚合

**虚拟化特性**：

- **跨 VM 追踪**：virtio 设备追踪
- **资源聚合**：VM 级资源统计
- **热迁移支持**：迁移时保持追踪连续性

### 3.4 多云环境

**AWS EKS**：Region=us-west-2 **GCP GKE**：Region=us-central1 **Cross-Cloud
VPN**：连接到中心集群

**多云特性**：

- **跨云联邦**：统一视图
- **数据同步**：跨云数据复制
- **故障转移**：云级故障转移

### 3.5 扩展性洞察

**三层架构**：

- Edge（聚合）→ Central（路由）→ Cloud（存储）
- 每层省却 **50%** 带宽和存储

**租户隔离**：

- 通过 OTTL（OpenTelemetry Transformation Language）实现 QoS 分级
- 高价值租户（A）全采样，低价值（C）采样率 1%

**跨域传输**：

- Arrow + ZSTD 将跨云传输成本降低 **80%**

---

## 4 控制闭环架构：从感知到自愈的反馈回路

### 4.1 执行层（Actuator）

**执行动作**：

- **bpf_send_signal()**：发送 SIGTERM
- **bpf_sockmap_update()**：流量切换
- **kubectl delete pod**：K8s API 调用
- **virsh migrate vm**：热迁移

**执行特性**：

- **延迟**：<10ms
- **可靠性**：>99.9%
- **安全性**：LSM Hook 保护

### 4.2 分析层（Analyzer）

**分析能力**：

- **PromQL 查询**：goroutine_count > 10000
- **机器学习模型**：预测 OOM 概率>0.9
- **关联分析**：网络延迟 ↑ + TCP 重传 ↑
- **基线偏离**：CPU 使用>3σ

**分析延迟**：

- **实时分析**：<1s
- **批量分析**：<5s
- **预测分析**：<10s

### 4.3 感知层（Sensor）

**感知能力**：

- **eBPF perf_event**：采样 CPU 周期
- **eBPF Map**：Goroutine 计数器
- **eBPF Tracepoint**：捕获 TCP 重传
- **eBPF LSM**：文件访问审计

**感知延迟**：

- **事件捕获**：<1ms
- **数据聚合**：<10ms
- **告警触发**：<100ms

### 4.4 数据层（Data）

**数据存储**：

- **VictoriaMetrics**：时序存储
- **Elasticsearch**：日志索引
- **Jaeger**：追踪存储
- **Profile Store**：火焰图存储

**数据特性**：

- **查询延迟**：<100ms（P95）
- **数据保留**：7-90 天
- **存储成本**：$0.01/GB/月

### 4.5 决策层（Controller）

**决策组件**：

- **HPA Controller**：水平扩容
- **VPA Controller**：垂直扩容
- **Policy Engine**：OPA 策略
- **Service Mesh**：Istio bpf-sdk

**决策延迟**：

- **规则匹配**：<100ms
- **策略执行**：<1s
- **反馈循环**：<10s

### 4.6 控制闭环特性

**延迟层次**：

- 感知层 **1ms** → 分析层 **5s** → 决策层 **1s** → 执行层 **10ms**
- 总闭环 **<10s**

**可靠性**：

- eBPF 内核态执行具备 **99.99%** 可用性
- 远高于用户态 Agent（**99.9%**）

**安全性**：

- LSM Hook 防止恶意自愈动作（如误杀关键进程）

---

## 5 架构模式分析

### 5.1 分层模式（Layered Pattern）

**模式定义**：将系统组织成一系列层次，每层提供服务给上层，使用下层服务。

**eBPF+OTLP 应用**：

```text
L7: 控制层（智能决策）
L6: 存储层（数据持久化）
L5: 处理层（数据转换）
L4: 协议层（数据传输）
L3: 用户态层（数据处理）
L2: 容器层（资源隔离）
L1: 内核层（数据采集）
```

**优势**：

- **职责清晰**：每层职责单一
- **易于维护**：修改一层不影响其他层
- **可测试性**：每层独立测试

### 5.2 管道-过滤器模式（Pipe-Filter Pattern）

**模式定义**：数据流通过一系列过滤器处理，每个过滤器独立处理数据。

**eBPF+OTLP 应用**：

```text
数据源 → 采集过滤器 → 转换过滤器 → 采样过滤器 → 路由过滤器 → 存储过滤器
```

**优势**：

- **可组合性**：过滤器可自由组合
- **可扩展性**：新增过滤器不影响现有流程
- **并行处理**：过滤器可并行执行

### 5.3 事件驱动模式（Event-Driven Pattern）

**模式定义**：系统响应事件，事件生产者发布事件，事件消费者订阅事件。

**eBPF+OTLP 应用**：

```text
内核事件 → eBPF Program → BPF Map → Agent → OTLP Event → Collector → Backend
```

**优势**：

- **解耦**：生产者和消费者解耦
- **可扩展性**：新增消费者不影响生产者
- **实时性**：事件实时处理

---

## 6 结论与展望

### 6.1 核心结论

eBPF+OTLP 技术栈的分层架构实现了：

1. **垂直穿透**：7 层架构，每层职责单一，省却率 **70-100%**
2. **水平扩展**：三层架构（Edge/Central/Cloud），带宽节省 **80%**
3. **控制闭环**：感知 → 分析 → 决策 → 执行，总延迟 **<10s**

### 6.2 理论意义

1. **分层架构理论的实践**：经典分层架构在可观测性领域的应用
2. **管道-过滤器模式的验证**：数据流处理的高效性
3. **事件驱动架构的体现**：实时响应和可扩展性

### 6.3 未来展望

**短期（2024-2025）**：

- 分层架构标准化
- 更多架构模式应用

**中期（2025-2026）**：

- AI 驱动的智能控制面
- 完全自治的闭环系统

**长期（2026+）**：

- 零配置的分层架构
- 自我优化的架构系统

---

## 🔗 相关文档

- [知识图谱](../04-knowledge-graph/knowledge-graph.md) - 核心概念体系图
- [矩阵分析](../06-matrix-analysis/matrix-analysis.md) - 多维矩阵对比
- [演进路径](../07-evolution-path/evolution-path.md) - 架构演进路径图

---

**最后更新**：2025-11-07 **维护者**：项目团队
