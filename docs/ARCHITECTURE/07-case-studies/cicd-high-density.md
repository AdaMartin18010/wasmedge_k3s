# CI/CD 高密度场景架构设计

## 📑 目录

- [1. 场景概述](#1-场景概述)
- [2. 架构设计](#2-架构设计)
- [3. 技术选型](#3-技术选型)
- [4. 实现细节](#4-实现细节)
- [5. 性能优化](#5-性能优化)
- [6. 成本分析](#6-成本分析)

---

## 1. 场景概述

### 1.1 业务需求

基于 `system_view.md` 案例 B：互联网 CI/CD（10 万 job/天，成本敏感）

**核心需求**：

- **启动延迟**：毫秒级冷启动
- **内存占用**：单实例 <10 MB
- **多租户安全**：外部开发者代码不可逃逸
- **成本优化**：降低 18%+ 运营成本

### 1.2 挑战分析

| 挑战     | 描述                           | 影响               |
| -------- | ------------------------------ | ------------------ |
| 高并发   | 10 万 job/天，峰值 1000+ 并发  | 需要快速启动和调度 |
| 成本敏感 | 内存和 CPU 成本占运营成本 60%+ | 需要极致优化       |
| 安全隔离 | 外部 PR 代码不可信             | 需要强隔离机制     |
| 镜像缓存 | 镜像拉取是主要瓶颈             | 需要 P2P 预热      |

---

## 2. 架构设计

### 2.1 整体架构

```text
┌─────────────────────────────────────────────────────────┐
│                    CI/CD 调度层                         │
│  (Kubernetes Scheduler + 自定义调度器)                   │
└─────────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
│  runC 容器   │ │   gVisor    │ │ Firecracker│
│  (内部业务)  │ │  (外部 PR)  │ │ (外部 PR)  │
│              │ │             │ │            │
│ 启动: 100ms  │ │ 启动: 400ms │ │ 启动: 125ms│
│ 内存: 10MB   │ │ 内存: 30MB  │ │ 内存: 5MB  │
└──────────────┘ └─────────────┘ └────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
┌───────────────────────▼───────────────────────┐
│           镜像缓存层 (Dragonfly P2P)            │
└───────────────────────────────────────────────┘
```

### 2.2 路由决策逻辑

**基于信任级别的自动路由**：

```yaml
# 路由策略
routing_policy:
  trusted_code:
    runtime: runc
    conditions:
      - source: internal_repo
      - user_group: internal_team
  untrusted_code:
    runtime: firecracker # 首选：性能最优
    fallback: gvisor # 备选：兼容性更好
    conditions:
      - source: external_pr
      - user_group: external_contributor
```

### 2.3 渐进式迁移策略

**阶段 1（2021-2023 Q1）**：gVisor 方案

- 外部 PR → gVisor + runsc
- 内存开销：30 MB/job
- 启动延迟：400 ms

**阶段 2（2023 Q2-2024 Q1）**：Firecracker 灰度

- 50% 外部 PR → Firecracker
- 内存开销：5 MB/job
- 启动延迟：125 ms
- 成本节省：10%

**阶段 3（2024 Q2+）**：Firecracker 全量

- 100% 外部 PR → Firecracker
- 预计成本节省：18%

---

## 3. 技术选型

### 3.1 理论支撑

#### 3.1.1 安全隔离

**引用理论**：L2（能力闭包引理）- 参见
[`00-theory/05-lemmas-theorems/L2-capability-closure.md`](00-theory/05-lemmas-theorems/L2-capability-closure.md)

**分析**：

- gVisor：113 个 syscall 白名单，最小权限原则
- Firecracker：microVM 硬件级隔离，攻击面最小

#### 3.1.2 成本优化

**引用理论**：状态空间压缩 - 参见
[`00-theory/04-state-compression/`](00-theory/04-state-compression/)

**分析**：

- Firecracker 内存 5 MB vs gVisor 30 MB，压缩比 6:1
- 启动延迟 125 ms vs gVisor 400 ms，提升 3.2x

### 3.2 技术对比

| 维度         | runC 容器      | gVisor             | Firecracker  |
| ------------ | -------------- | ------------------ | ------------ |
| **启动延迟** | 100 ms         | 400 ms             | 125 ms       |
| **内存占用** | 10 MB          | 30 MB              | 5 MB         |
| **CPU 性能** | 99-100%        | 85-90%             | 95%          |
| **安全隔离** | 弱（共享内核） | 强（syscall 拦截） | 强（硬件级） |
| **兼容性**   | 100%           | 90%                | 95%          |
| **成本**     | 基准           | +200%              | -18%         |

---

## 4. 实现细节

### 4.1 Kubernetes 集成

**RuntimeClass 配置**：

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: firecracker
handler: firecracker
---
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
```

**Pod 调度策略**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ci-job-external-pr
spec:
  runtimeClassName: firecracker # 自动选择
  containers:
    - name: job-runner
      image: ci-runner:latest
```

### 4.2 镜像缓存优化

**Dragonfly P2P 预热**：

```yaml
# Dragonfly 配置
dfdaemon:
  registry_mirror:
    remote: https://registry.example.com
    p2p:
      enabled: true
      prefetch: true
      prefetch_limit: 100
```

### 4.3 资源配额管理

**ResourceQuota 配置**：

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: cicd-quota
spec:
  hard:
    requests.memory: 1000Gi
    limits.memory: 2000Gi
    requests.cpu: "500"
    limits.cpu: "1000"
    pods: "10000"
  scopes:
    - NotTerminating
```

---

## 5. 性能优化

### 5.1 启动优化

**Firecracker 快照优化**：

```bash
# 创建基础快照
firecracker-ctr snapshot create \
  --vm-state-path /snapshots/base-vm-state \
  --mem-file-path /snapshots/base-mem \
  --kernel-image-path /vmlinux \
  --rootfs-path /base-rootfs.ext4

# 从快照启动（< 125ms）
firecracker-ctr snapshot restore \
  --vm-state-path /snapshots/base-vm-state \
  --mem-file-path /snapshots/base-mem \
  --kernel-image-path /vmlinux \
  --rootfs-path /base-rootfs.ext4
```

### 5.2 内存优化

**Memory Balloon 配置**：

```json
{
  "balloon": {
    "size_mib": 128,
    "deflate_on_oom": true,
    "stats_polling_interval_s": 10
  }
}
```

### 5.3 网络优化

**Virtio-net 配置**：

```json
{
  "net": {
    "iface_id": "net0",
    "guest_mac": "AA:FC:00:00:00:01",
    "host_dev_name": "veth0",
    "rx_rate_limiter": {
      "bandwidth": {
        "size": 100000000,
        "refill_time": 1000000000
      }
    }
  }
}
```

---

## 6. 成本分析

### 6.1 成本对比（1000 并发场景）

| 方案             | 内存成本/月 | CPU 成本/月 | 总成本/月 | 节省    |
| ---------------- | ----------- | ----------- | --------- | ------- |
| 全 runC          | $5000       | $3000       | $8000     | 基准    |
| 全 gVisor        | $15000      | $3000       | $18000    | +125%   |
| 混部（当前）     | $8000       | $3000       | $11000    | +37.5%  |
| Firecracker 全量 | $4100       | $3000       | $7100     | -11.25% |

### 6.2 ROI 分析

**Firecracker 迁移 ROI**：

- **迁移成本**：开发 + 测试 = $50k
- **年节省成本**：($11000 - $7100) × 12 = $46800
- **回收期**：$50k / $46800 = 1.07 年
- **3 年 ROI**：($46800 × 3 - $50k) / $50k = 180%

---

## 7. 监控与可观测性

### 7.1 指标监控

**Prometheus 指标**：

```yaml
# Firecracker 指标
firecracker_vm_uptime_seconds
firecracker_vm_memory_used_bytes
firecracker_vm_cpu_usage_percent
firecracker_snapshot_restore_duration_seconds

# 调度指标
scheduler_job_startup_duration_seconds{runtime="firecracker"}
scheduler_job_memory_usage_bytes{runtime="firecracker"}
scheduler_job_cost_dollars{runtime="firecracker"}
```

### 7.2 日志聚合

**Fluentd 配置**：

```yaml
<source> @type tail path /var/log/firecracker/*.log tag firecracker.log format
json </source>

<match firecracker.log> @type elasticsearch host
elasticsearch.logging.svc.cluster.local index_name firecracker-logs </match>
```

---

## 8. 安全考虑

### 8.1 隔离验证

**渗透测试结果**：

- ✅ 外部 PR 代码无法逃逸到宿主机
- ✅ 无法访问其他 job 的资源
- ✅ 无法访问内部网络资源
- ✅ syscall 白名单有效阻止恶意调用

### 8.2 合规性

**符合标准**：

- ISO 27001：信息安全管理
- SOC 2：服务组织控制
- PCI-DSS：支付卡行业数据安全标准

---

## 9. 故障处理

### 9.1 常见问题

**问题 1：Firecracker 启动失败**:

**原因**：快照文件损坏或版本不匹配

**解决**：

```bash
# 重新创建快照
firecracker-ctr snapshot create --force
```

**问题 2：内存不足**:

**原因**：Balloon 配置不当

**解决**：

```json
{
  "balloon": {
    "size_mib": 256,
    "deflate_on_oom": true
  }
}
```

### 9.2 回滚策略

**gVisor 作为备选**：

```yaml
routing_policy:
  untrusted_code:
    runtime: firecracker
    fallback: gvisor # 自动回滚
    fallback_conditions:
      - firecracker_failure_rate > 0.01
      - firecracker_available < 0.5
```

---

## 10. 未来规划

### 10.1 WASM 集成（2025）

**计划**：部分轻量级 job 迁移到 WASM

**优势**：

- 启动延迟：< 10 ms
- 内存占用：< 1 MB
- 安全性：内存安全保证

**参考**：参见 [`01-views/webassembly-view.md`](01-views/webassembly-view.md)

### 10.2 边缘计算扩展

**计划**：将 CI/CD 扩展到边缘节点

**优势**：

- 降低延迟（就近执行）
- 降低带宽成本（边缘缓存）

**参考**：参见
[`01-views/edge-computing-view.md`](01-views/edge-computing-view.md)

---

## 11. 结论

### 11.1 关键成果

✅ **成本优化**：通过 Firecracker 迁移，预计节省 18% 成本 ✅ **性能提升**：启动
延迟从 400ms 降至 125ms ✅ **安全增强**：硬件级隔离，零逃逸记录 ✅ **可扩展
性**：支持 10 万+ job/天

### 11.2 经验总结

1. **渐进式迁移**：灰度发布，逐步替换
2. **性能监控**：实时监控，快速响应
3. **成本优化**：持续优化，量化收益
4. **安全优先**：外部代码强制隔离

---

**相关文档**：

- [`system-view-cases-analysis.md`](system-view-cases-analysis.md) - system_view
  案例扩展分析
- [`../01-implementation/03-sandboxing/firecracker-config.md`](../01-implementation/03-sandboxing/firecracker-config.md) -
  Firecracker 配置
- [`../01-implementation/03-sandboxing/gvisor-setup.md`](../01-implementation/03-sandboxing/gvisor-setup.md) -
  gVisor 设置

---

**更新时间**：2025-11-05 **版本**：v1.0 **维护者**：基于 system_view.md 案例 B
扩展
