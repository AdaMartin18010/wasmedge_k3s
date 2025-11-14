# 案例 K-002：K3s Pod 调度失败

> **案例编号**：K-002
> **故障类型**：调度故障
> **严重程度**：高
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 K-002：K3s Pod 调度失败](#案例-k-002k3s-pod-调度失败)
  - [📑 目录](#-目录)
  - [1 问题描述](#1-问题描述)
    - [1.1 故障现象](#11-故障现象)
    - [1.2 环境信息](#12-环境信息)
    - [1.3 影响范围](#13-影响范围)
  - [2 故障排查过程](#2-故障排查过程)
    - [2.1 初步诊断](#21-初步诊断)
    - [2.2 深入排查](#22-深入排查)
    - [2.3 根因分析](#23-根因分析)
  - [3 解决方案](#3-解决方案)
    - [3.1 临时解决方案](#31-临时解决方案)
    - [3.2 永久解决方案](#32-永久解决方案)
    - [3.3 预防措施](#33-预防措施)
  - [4 验证与恢复](#4-验证与恢复)
    - [4.1 验证步骤](#41-验证步骤)
    - [4.2 恢复确认](#42-恢复确认)
  - [5 经验总结](#5-经验总结)
    - [5.1 关键发现](#51-关键发现)
    - [5.2 最佳实践](#52-最佳实践)
    - [5.3 相关文档](#53-相关文档)
  - [6 相关文档](#6-相关文档)

---

## 1 问题描述

### 1.1 故障现象

**主要症状**：

- Pod 一直处于 `Pending` 状态
- 调度器无法将 Pod 分配到节点
- 事件显示：`0/1 nodes are available: 1 Insufficient memory`
- 应用无法启动，服务不可用

**错误日志**：

```text
Events:
  Type     Reason            Age                From               Message
  ----     ------            ----               ----               -------
  Warning  FailedScheduling  5m (x12 over 5m)   default-scheduler  0/1 nodes are available: 1 Insufficient memory.
  Warning  FailedScheduling  5m (x12 over 5m)   default-scheduler  0/1 nodes are available: 1 node(s) had taint {node-role.kubernetes.io/master: }.
```

**时间线**：

- **14:00:00** - 创建 Pod
- **14:00:05** - Pod 进入 Pending 状态
- **14:00:10** - 调度器开始尝试调度
- **14:05:00** - 调度失败，Pod 仍为 Pending

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **节点数量**：1 个（单节点集群）
- **节点类型**：边缘节点
- **资源限制**：内存 2GB，CPU 4 核

**Pod 配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-001
  namespace: default
spec:
  containers:
    - name: app
      image: app:v1.0.0
      resources:
        requests:
          memory: "1Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "1000m"
```

**节点信息**：

```bash
# 节点资源
$ kubectl describe node k3s-server-1

Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests    Limits
  --------           --------     ------
  cpu                2000m (50%)  4000m (100%)
  memory             1500Mi (75%) 2000Mi (100%)
```

### 1.3 影响范围

- **受影响 Pod**：1 个（app-pod-001）
- **受影响服务**：应用服务
- **业务影响**：应用无法启动，服务完全不可用
- **用户影响**：所有依赖该服务的用户无法访问

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 Pod 状态**：

```bash
# 检查 Pod 状态
kubectl get pod app-pod-001 -n default

# 输出
NAME          READY   STATUS    RESTARTS   AGE
app-pod-001   0/1     Pending   0          5m
```

**步骤 2：查看 Pod 事件**：

```bash
# 查看 Pod 事件
kubectl describe pod app-pod-001 -n default

# 输出
Events:
  Type     Reason            Age                From               Message
  ----     ------            ----               ----               -------
  Warning  FailedScheduling  5m (x12 over 5m)   default-scheduler  0/1 nodes are available: 1 Insufficient memory.
```

**步骤 3：检查节点资源**：

```bash
# 检查节点资源
kubectl top node k3s-server-1

# 输出
NAME           CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
k3s-server-1   2000m       50%    1500Mi          75%
```

**初步结论**：

- Pod 状态为 Pending
- 调度器报告内存不足
- 节点资源使用率较高

### 2.2 深入排查

**步骤 4：检查节点可分配资源**：

```bash
# 检查节点详细信息
kubectl describe node k3s-server-1 | grep -A 10 "Allocated resources"

# 输出
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource           Requests    Limits
  --------           --------     ------
  cpu                2000m (50%)  4000m (100%)
  memory             1500Mi (75%) 2000Mi (100%)
```

**步骤 5：检查节点容量**：

```bash
# 检查节点容量
kubectl describe node k3s-server-1 | grep -A 5 "Capacity\|Allocatable"

# 输出
Capacity:
  cpu:                4
  memory:             2Gi
  pods:               110
Allocatable:
  cpu:                4
  memory:             2Gi
  pods:               110
```

**步骤 6：检查节点污点**：

```bash
# 检查节点污点
kubectl describe node k3s-server-1 | grep Taints

# 输出
Taints:             node-role.kubernetes.io/master:NoSchedule
```

**步骤 7：检查 Pod 容忍度**：

```bash
# 检查 Pod 容忍度
kubectl get pod app-pod-001 -n default -o yaml | grep -A 5 tolerations

# 输出
（无 tolerations 配置）
```

**步骤 8：检查其他 Pod 资源使用**：

```bash
# 检查其他 Pod 资源使用
kubectl top pods -A

# 输出
NAME                    CPU(cores)   MEMORY(bytes)
kube-system-coredns     10m          50Mi
kube-system-traefik    100m         200Mi
app-pod-002             500m         500Mi
```

**深入排查结论**：

- 节点内存已分配 1500Mi，剩余 500Mi
- Pod 请求 1Gi 内存，但节点只有 500Mi 可用
- 节点有 master 污点，Pod 没有容忍度
- 需要检查资源请求和节点容量

### 2.3 根因分析

**根因 1：资源不足**：

- 节点内存已分配 1500Mi（75%）
- Pod 请求 1Gi（1024Mi）内存
- 节点剩余内存 500Mi，不足以满足 Pod 请求

**根因 2：节点污点**：

- 节点有 `node-role.kubernetes.io/master:NoSchedule` 污点
- Pod 没有相应的容忍度
- 调度器无法将 Pod 调度到该节点

**根因 3：资源请求过大**：

- Pod 资源请求可能过大
- 没有考虑节点实际可用资源

**根本原因**：

**资源不足和节点污点双重问题**：节点内存不足且存在污点，导致调度器无法将 Pod 调度到节点。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：减少 Pod 资源请求**：

```yaml
# 修改 Pod 配置，减少资源请求
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-001
  namespace: default
spec:
  containers:
    - name: app
      image: app:v1.0.0
      resources:
        requests:
          memory: "400Mi"  # 减少内存请求
          cpu: "200m"      # 减少 CPU 请求
        limits:
          memory: "1Gi"
          cpu: "500m"
```

**方案 2：添加节点容忍度**：

```yaml
# 添加节点容忍度
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-001
  namespace: default
spec:
  tolerations:
    - key: node-role.kubernetes.io/master
      operator: Exists
      effect: NoSchedule
  containers:
    - name: app
      image: app:v1.0.0
      resources:
        requests:
          memory: "400Mi"
          cpu: "200m"
```

**方案 3：移除节点污点**：

```bash
# 移除节点污点（仅用于单节点集群）
kubectl taint nodes k3s-server-1 node-role.kubernetes.io/master:NoSchedule-
```

**临时方案效果**：

- ✅ 可以快速恢复服务
- ⚠️ 但未解决根本问题
- ⚠️ 可能影响系统稳定性

### 3.2 永久解决方案

**方案 1：优化资源请求**：

```yaml
# 优化 Pod 资源请求
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-001
  namespace: default
spec:
  containers:
    - name: app
      image: app:v1.0.0
      resources:
        requests:
          memory: "256Mi"  # 根据实际需求调整
          cpu: "100m"
        limits:
          memory: "512Mi"
          cpu: "500m"
```

**方案 2：配置节点容忍度**：

```yaml
# 配置节点容忍度（适用于单节点集群）
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-001
  namespace: default
spec:
  tolerations:
    - key: node-role.kubernetes.io/master
      operator: Exists
      effect: NoSchedule
  containers:
    - name: app
      image: app:v1.0.0
      resources:
        requests:
          memory: "256Mi"
          cpu: "100m"
```

**方案 3：添加节点标签和选择器**：

```yaml
# 使用节点选择器
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-001
  namespace: default
spec:
  nodeSelector:
    node-type: worker  # 选择工作节点
  tolerations:
    - key: node-role.kubernetes.io/master
      operator: Exists
      effect: NoSchedule
  containers:
    - name: app
      image: app:v1.0.0
      resources:
        requests:
          memory: "256Mi"
          cpu: "100m"
```

**方案 4：使用 Deployment 和资源配额**：

```yaml
# 使用 Deployment 管理 Pod
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      tolerations:
        - key: node-role.kubernetes.io/master
          operator: Exists
          effect: NoSchedule
      containers:
        - name: app
          image: app:v1.0.0
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：资源请求标准化**：

```yaml
# 创建资源请求模板
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-template
  namespace: default
spec:
  containers:
    - name: app
      image: app:v1.0.0
      resources:
        requests:
          memory: "256Mi"  # 标准内存请求
          cpu: "100m"      # 标准 CPU 请求
        limits:
          memory: "512Mi"  # 标准内存限制
          cpu: "500m"      # 标准 CPU 限制
```

**措施 2：节点资源监控**：

```bash
# 配置节点资源监控
kubectl top nodes

# 定期检查节点资源使用
watch -n 5 kubectl top nodes
```

**措施 3：资源配额管理**：

```yaml
# 创建资源配额
apiVersion: v1
kind: ResourceQuota
metadata:
  name: default-quota
  namespace: default
spec:
  hard:
    requests.memory: "2Gi"
    requests.cpu: "2"
    limits.memory: "4Gi"
    limits.cpu: "4"
```

**措施 4：节点污点管理**：

```bash
# 对于单节点集群，移除 master 污点
kubectl taint nodes k3s-server-1 node-role.kubernetes.io/master:NoSchedule-

# 或添加容忍度到默认 Pod 模板
```

---

## 4 验证与恢复

### 4.1 验证步骤

**步骤 1：验证 Pod 配置**：

```bash
# 检查 Pod 配置
kubectl get pod app-pod-001 -n default -o yaml | grep -A 10 resources

# 预期输出
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

**步骤 2：验证 Pod 调度**：

```bash
# 检查 Pod 状态
kubectl get pod app-pod-001 -n default

# 预期输出
NAME          READY   STATUS    RESTARTS   AGE
app-pod-001   1/1     Running   0          1m
```

**步骤 3：验证节点资源**：

```bash
# 检查节点资源使用
kubectl top node k3s-server-1

# 预期输出
NAME           CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
k3s-server-1   2100m       52%    1756Mi          88%
```

**步骤 4：验证服务可用性**：

```bash
# 测试服务端点
curl http://app-service.default.svc.cluster.local:8080/health

# 预期输出
{"status":"ok"}
```

### 4.2 恢复确认

**恢复指标**：

- ✅ Pod 状态：Running
- ✅ 调度成功：Pod 已分配到节点
- ✅ 资源使用：正常
- ✅ 服务可用性：正常

**恢复时间**：

- **故障发现**：14:00:00
- **开始排查**：14:00:05
- **根因确认**：14:10:00
- **问题解决**：14:15:00
- **服务恢复**：14:15:05
- **总耗时**：15 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **资源请求过大导致调度失败**：
   - Pod 资源请求超过节点可用资源
   - 需要根据实际需求调整资源请求

2. **节点污点影响调度**：
   - 节点污点会阻止 Pod 调度
   - 需要配置相应的容忍度

3. **单节点集群特殊配置**：
   - 单节点集群需要移除 master 污点或添加容忍度
   - 需要合理配置资源请求

### 5.2 最佳实践

1. **合理配置资源请求**：
   - 根据实际需求配置资源请求
   - 避免资源请求过大

2. **节点污点管理**：
   - 对于单节点集群，移除 master 污点
   - 或为 Pod 添加相应的容忍度

3. **资源监控**：
   - 定期监控节点资源使用
   - 及时发现资源不足问题

4. **使用 Deployment**：
   - 使用 Deployment 管理 Pod
   - 便于资源管理和调度

### 5.3 相关文档

- [`../../TECHNICAL/01-core-foundations/k3s/k3s.md`](../../TECHNICAL/01-core-foundations/k3s/k3s.md) - K3s 文档
- [`../../TECHNICAL/02-runtime-policy/scheduling/scheduling.md`](../../TECHNICAL/02-runtime-policy/scheduling/scheduling.md) - 调度文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

## 6 相关文档

- [`../README.md`](README.md) - 故障排查案例集目录
- [`../../TECHNICAL/01-core-foundations/k3s/k3s.md`](../../TECHNICAL/01-core-foundations/k3s/k3s.md) - K3s 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
