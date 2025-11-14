# 案例 W-003：Wasm 网络连接失败

> **案例编号**：W-003
> **故障类型**：网络连接故障
> **严重程度**：高
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 W-003：Wasm 网络连接失败](#案例-w-003wasm-网络连接失败)
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

- Wasm 应用无法建立网络连接
- 应用启动后立即报错：`Network connection failed: Connection refused`
- 日志显示：`Error: failed to connect to 10.0.0.1:8080`
- 应用状态为 `Running`，但无法处理请求

**错误日志**：

```text
2025-11-13T10:30:15.123Z ERROR [wasm-app] Network connection failed
2025-11-13T10:30:15.124Z ERROR [wasm-app] Error: failed to connect to 10.0.0.1:8080
2025-11-13T10:30:15.125Z ERROR [wasm-app] Connection refused
2025-11-13T10:30:15.126Z ERROR [wasm-app] Stack trace:
    at wasm_network_connect (wasm-app.wasm:0x1234)
    at main (wasm-app.wasm:0x5678)
```

**时间线**：

- **10:30:00** - Wasm 应用 Pod 启动
- **10:30:05** - 应用开始尝试连接外部服务
- **10:30:15** - 连接失败，应用报错
- **10:30:20** - 应用进入错误状态

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **WasmEdge 版本**：v0.14.0
- **CNI 插件**：flannel
- **网络模式**：VXLAN

**应用配置**：

- **Runtime**：WasmEdge
- **网络策略**：无
- **Service**：ClusterIP
- **目标服务**：10.0.0.1:8080

**Pod 信息**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-001
  namespace: default
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      env:
        - name: TARGET_HOST
          value: "10.0.0.1"
        - name: TARGET_PORT
          value: "8080"
```

### 1.3 影响范围

- **受影响 Pod**：1 个（wasm-app-001）
- **受影响服务**：Wasm 应用服务
- **业务影响**：应用无法处理请求，服务完全不可用
- **用户影响**：所有依赖该服务的用户无法访问

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 Pod 状态**：

```bash
# 检查 Pod 状态
kubectl get pod wasm-app-001 -n default

# 输出
NAME           READY   STATUS    RESTARTS   AGE
wasm-app-001   1/1     Running   0          5m
```

**步骤 2：查看 Pod 日志**：

```bash
# 查看 Pod 日志
kubectl logs wasm-app-001 -n default

# 输出
2025-11-13T10:30:15.123Z ERROR [wasm-app] Network connection failed
2025-11-13T10:30:15.124Z ERROR [wasm-app] Error: failed to connect to 10.0.0.1:8080
```

**步骤 3：检查网络连接**：

```bash
# 在 Pod 内测试网络连接
kubectl exec -it wasm-app-001 -n default -- ping -c 3 10.0.0.1

# 输出
PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.
64 bytes from 10.0.0.1: icmp_seq=1 time=0.123 ms
64 bytes from 10.0.0.1: icmp_seq=2 time=0.145 ms
64 bytes from 10.0.0.1: icmp_seq=3 time=0.134 ms
```

**初步结论**：

- Pod 状态正常（Running）
- 网络可达（ping 成功）
- 但应用无法建立 TCP 连接

### 2.2 深入排查

**步骤 4：检查端口连通性**：

```bash
# 测试端口连通性
kubectl exec -it wasm-app-001 -n default -- nc -zv 10.0.0.1 8080

# 输出
nc: connect to 10.0.0.1 port 8080 (tcp) failed: Connection refused
```

**步骤 5：检查目标服务**：

```bash
# 检查目标服务状态
kubectl get svc -A | grep 10.0.0.1

# 输出
（无结果）

# 检查目标 Pod
kubectl get pod -A -o wide | grep 10.0.0.1

# 输出
（无结果）
```

**步骤 6：检查 WasmEdge 网络配置**：

```bash
# 检查 WasmEdge Runtime 配置
kubectl get runtimeclass wasm -o yaml

# 输出
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: wasm
handler: wasmedge
overhead:
  podFixed:
    memory: "64Mi"
    cpu: "100m"
```

**步骤 7：检查网络策略**：

```bash
# 检查网络策略
kubectl get networkpolicy -A

# 输出
（无结果）
```

**步骤 8：检查 WasmEdge 网络权限**：

```bash
# 检查 WasmEdge 网络权限配置
kubectl describe pod wasm-app-001 -n default | grep -i network

# 输出
（无网络相关配置）
```

**深入排查结论**：

- 目标服务不存在或未启动
- WasmEdge 网络权限可能受限
- 需要检查 WasmEdge 的网络配置

### 2.3 根因分析

**根因 1：目标服务不存在**：

- 目标 IP `10.0.0.1:8080` 对应的服务不存在或未启动
- 应用配置中的目标地址错误

**根因 2：WasmEdge 网络权限受限**：

- WasmEdge 默认网络权限受限
- 需要显式配置网络权限才能访问外部服务

**根因 3：网络策略限制**：

- 可能存在隐式的网络策略限制
- Wasm 应用无法访问集群外部服务

**根本原因**：

**WasmEdge 网络权限配置缺失**：WasmEdge 默认不允许访问外部网络，需要在 Pod 配置中显式启用网络权限。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：重启 Pod**：

```bash
# 删除并重新创建 Pod
kubectl delete pod wasm-app-001 -n default
kubectl apply -f wasm-app.yaml
```

**方案 2：使用 Service 名称替代 IP**：

```yaml
# 修改应用配置，使用 Service 名称
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-001
  namespace: default
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      env:
        - name: TARGET_HOST
          value: "target-service.default.svc.cluster.local"  # 使用 Service 名称
        - name: TARGET_PORT
          value: "8080"
```

**临时方案效果**：

- ✅ 可以快速恢复服务
- ⚠️ 但未解决根本问题
- ⚠️ 可能再次出现相同问题

### 3.2 永久解决方案

**方案 1：配置 WasmEdge 网络权限**：

```yaml
# 修改 Pod 配置，启用网络权限
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-001
  namespace: default
  annotations:
    wasmedge.network/allowed: "true"  # 启用网络权限
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      env:
        - name: TARGET_HOST
          value: "target-service.default.svc.cluster.local"
        - name: TARGET_PORT
          value: "8080"
      securityContext:
        capabilities:
          add:
            - NET_ADMIN  # 添加网络管理权限
```

**方案 2：使用 Service 和 Endpoints**：

```yaml
# 创建目标服务
apiVersion: v1
kind: Service
metadata:
  name: target-service
  namespace: default
spec:
  selector:
    app: target-app
  ports:
    - port: 8080
      targetPort: 8080
---
# 修改应用配置，使用 Service 名称
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-001
  namespace: default
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      env:
        - name: TARGET_HOST
          value: "target-service.default.svc.cluster.local"
        - name: TARGET_PORT
          value: "8080"
```

**方案 3：配置网络策略**：

```yaml
# 创建网络策略，允许 Wasm 应用访问目标服务
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: wasm-app-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: wasm-app
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: target-app
      ports:
        - protocol: TCP
          port: 8080
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：标准化网络配置**：

```yaml
# 创建 Wasm 应用模板
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-template
  namespace: default
  annotations:
    wasmedge.network/allowed: "true"
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      securityContext:
        capabilities:
          add:
            - NET_ADMIN
```

**措施 2：使用 Service 发现**：

- 使用 Kubernetes Service 进行服务发现
- 避免硬编码 IP 地址
- 使用 DNS 名称解析

**措施 3：网络策略审查**：

- 定期审查网络策略配置
- 确保 Wasm 应用有必要的网络权限
- 使用最小权限原则

**措施 4：监控和告警**：

```yaml
# 配置网络连接监控
apiVersion: v1
kind: ConfigMap
metadata:
  name: wasm-network-monitor
data:
  monitor.sh: |
    #!/bin/bash
    while true; do
      if ! nc -zv $TARGET_HOST $TARGET_PORT; then
        echo "Network connection failed"
        # 发送告警
      fi
      sleep 30
    done
```

---

## 4 验证与恢复

### 4.1 验证步骤

**步骤 1：验证 Pod 配置**：

```bash
# 检查 Pod 配置
kubectl get pod wasm-app-001 -n default -o yaml | grep -A 10 annotations

# 预期输出
annotations:
  wasmedge.network/allowed: "true"
```

**步骤 2：验证网络连接**：

```bash
# 测试网络连接
kubectl exec -it wasm-app-001 -n default -- nc -zv target-service.default.svc.cluster.local 8080

# 预期输出
Connection to target-service.default.svc.cluster.local 8080 port [tcp/http-alt] succeeded!
```

**步骤 3：验证应用功能**：

```bash
# 检查应用日志
kubectl logs wasm-app-001 -n default --tail=50

# 预期输出
2025-11-13T10:35:00.123Z INFO [wasm-app] Connected to target service
2025-11-13T10:35:00.124Z INFO [wasm-app] Application started successfully
```

**步骤 4：验证服务可用性**：

```bash
# 测试服务端点
curl http://wasm-app-service.default.svc.cluster.local:8080/health

# 预期输出
{"status":"ok"}
```

### 4.2 恢复确认

**恢复指标**：

- ✅ Pod 状态：Running
- ✅ 网络连接：成功
- ✅ 应用日志：无错误
- ✅ 服务可用性：正常

**恢复时间**：

- **故障发现**：10:30:00
- **开始排查**：10:30:05
- **根因确认**：10:35:00
- **问题解决**：10:40:00
- **服务恢复**：10:40:05
- **总耗时**：10 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **WasmEdge 网络权限默认受限**：
   - WasmEdge 默认不允许访问外部网络
   - 需要显式配置网络权限

2. **IP 地址硬编码问题**：
   - 硬编码 IP 地址容易导致连接失败
   - 应使用 Service 名称进行服务发现

3. **网络策略影响**：
   - 网络策略可能限制 Wasm 应用的网络访问
   - 需要正确配置网络策略

### 5.2 最佳实践

1. **使用 Service 发现**：
   - 使用 Kubernetes Service 进行服务发现
   - 避免硬编码 IP 地址

2. **配置网络权限**：
   - 显式配置 WasmEdge 网络权限
   - 使用最小权限原则

3. **网络策略审查**：
   - 定期审查网络策略配置
   - 确保应用有必要的网络权限

4. **监控和告警**：
   - 配置网络连接监控
   - 及时发现网络问题

### 5.3 相关文档

- [`../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md`](../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md) - WasmEdge 文档
- [`../../TECHNICAL/03-networking/service/service.md`](../../TECHNICAL/03-networking/service/service.md) - Service 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

## 6 相关文档

- [`../README.md`](README.md) - 故障排查案例集目录
- [`../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md`](../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md) - WasmEdge 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
