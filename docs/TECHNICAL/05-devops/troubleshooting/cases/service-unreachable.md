# 案例 N-002：Service 无法访问

> **案例编号**：N-002
> **故障类型**：服务访问故障
> **严重程度**：严重
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 N-002：Service 无法访问](#案例-n-002service-无法访问)
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

- Service 无法访问
- 连接超时或连接被拒绝
- DNS 解析失败
- 应用无法通过 Service 访问后端 Pod

**错误日志**：

```text
# 尝试访问 Service
$ curl http://app-service.default.svc.cluster.local:8080

curl: (7) Failed to connect to app-service.default.svc.cluster.local port 8080: Connection refused
```

**时间线**：

- **20:00:00** - 发现 Service 无法访问
- **20:00:05** - 开始排查网络问题
- **20:00:10** - 确认 Service 无法访问
- **20:05:00** - 定位到 Endpoints 问题

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **CNI 插件**：flannel
- **DNS 插件**：CoreDNS
- **节点数量**：3 个

**Service 配置**：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: default
spec:
  selector:
    app: app
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
  type: ClusterIP
```

**Pod 配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-005
  namespace: default
  labels:
    app: app
spec:
  containers:
    - name: app
      image: app:v1.0.0
      ports:
        - containerPort: 8080
```

### 1.3 影响范围

- **受影响 Service**：1 个（app-service）
- **受影响服务**：应用服务
- **业务影响**：服务无法访问，影响生产环境
- **用户影响**：所有依赖该服务的用户无法访问

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 Service 状态**：

```bash
# 检查 Service 状态
kubectl get svc app-service -n default

# 输出
NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
app-service   ClusterIP   10.43.0.10      <none>        8080/TCP   5m
```

**步骤 2：测试 Service 访问**：

```bash
# 测试 Service 访问
curl http://app-service.default.svc.cluster.local:8080

# 输出
curl: (7) Failed to connect to app-service.default.svc.cluster.local port 8080: Connection refused
```

**步骤 3：检查 Pod 状态**：

```bash
# 检查 Pod 状态
kubectl get pod app-pod-005 -n default

# 输出
NAME          READY   STATUS    RESTARTS   AGE
app-pod-005   1/1     Running   0          5m
```

**初步结论**：

- Service 状态正常
- Pod 状态正常
- 但 Service 无法访问
- 需要检查 Endpoints 和 DNS

### 2.2 深入排查

**步骤 4：检查 Endpoints**：

```bash
# 检查 Endpoints
kubectl get endpoints app-service -n default

# 输出
NAME          ENDPOINTS   AGE
app-service   <none>      5m
```

**步骤 5：检查 Service Selector**：

```bash
# 检查 Service Selector
kubectl get svc app-service -n default -o yaml | grep -A 5 selector

# 输出
selector:
  app: app
```

**步骤 6：检查 Pod Labels**：

```bash
# 检查 Pod Labels
kubectl get pod app-pod-005 -n default --show-labels

# 输出
NAME          READY   STATUS    RESTARTS   AGE   LABELS
app-pod-005   1/1     Running   0          5m    app=app,version=v1.0.0
```

**步骤 7：检查 DNS 解析**：

```bash
# 测试 DNS 解析
kubectl run test-dns --image=busybox --rm -it --restart=Never -- nslookup app-service.default.svc.cluster.local

# 输出
Server:    10.43.0.10
Address 1: 10.43.0.10

Name:      app-service.default.svc.cluster.local
Address 1: 10.43.0.10
```

**步骤 8：检查 CoreDNS**：

```bash
# 检查 CoreDNS Pod
kubectl get pod -n kube-system | grep coredns

# 输出
coredns-xxx   1/1     Running   0          5d
```

**深入排查结论**：

- Endpoints 为空（`<none>`）
- Service Selector 和 Pod Labels 匹配
- DNS 解析正常
- 需要检查为什么 Endpoints 为空

### 2.3 根因分析

**根因 1：Service Selector 不匹配**：

- Service Selector 可能不匹配 Pod Labels
- 导致 Endpoints 为空
- Service 无法路由到 Pod

**根因 2：Pod 端口不匹配**：

- Pod 端口可能不匹配 Service targetPort
- 导致 Endpoints 无法创建
- Service 无法访问 Pod

**根因 3：Pod 未就绪**：

- Pod 可能未就绪（Readiness Probe 失败）
- 导致 Endpoints 为空
- Service 无法访问 Pod

**根本原因**：

**Service Selector 不匹配 Pod Labels**：Service Selector 配置为 `app: app`，但 Pod Labels 可能不匹配，导致 Endpoints 为空，从而 Service 无法访问 Pod。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：直接访问 Pod IP**：

```bash
# 直接访问 Pod IP
kubectl get pod app-pod-005 -n default -o wide

# 输出
NAME          READY   STATUS    RESTARTS   AGE   IP           NODE
app-pod-005   1/1     Running   0          5m    10.42.1.10   k3s-server-1

# 访问 Pod IP
curl http://10.42.1.10:8080
```

**方案 2：修改 Service Selector**：

```yaml
# 修改 Service Selector
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: default
spec:
  selector:
    app: app
    version: v1.0.0  # 添加版本标签
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
  type: ClusterIP
```

**方案 3：使用 NodePort**：

```yaml
# 使用 NodePort 访问
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: default
spec:
  selector:
    app: app
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
  type: NodePort  # 使用 NodePort
```

**临时方案效果**：

- ✅ 可以快速恢复服务
- ⚠️ 但未解决根本问题
- ⚠️ 可能影响服务发现

### 3.2 永久解决方案

**方案 1：修复 Service Selector**：

```yaml
# 修复 Service Selector
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: default
spec:
  selector:
    app: app  # 确保与 Pod Labels 匹配
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
  type: ClusterIP
```

**方案 2：修复 Pod Labels**：

```yaml
# 修复 Pod Labels
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-005
  namespace: default
  labels:
    app: app  # 确保与 Service Selector 匹配
spec:
  containers:
    - name: app
      image: app:v1.0.0
      ports:
        - containerPort: 8080
```

**方案 3：使用 Deployment 管理 Pod**：

```yaml
# 使用 Deployment 管理 Pod
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app  # 确保与 Service Selector 匹配
    spec:
      containers:
        - name: app
          image: app:v1.0.0
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
```

**方案 4：配置 Endpoints 手动管理**：

```yaml
# 手动配置 Endpoints
apiVersion: v1
kind: Endpoints
metadata:
  name: app-service
  namespace: default
subsets:
  - addresses:
      - ip: 10.42.1.10
    ports:
      - port: 8080
        protocol: TCP
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：Service Selector 标准化**：

```yaml
# 创建 Service 模板
apiVersion: v1
kind: Service
metadata:
  name: app-service-template
  namespace: default
spec:
  selector:
    app: app  # 标准 Selector
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
  type: ClusterIP
```

**措施 2：Pod Labels 标准化**：

```yaml
# 创建 Pod 模板
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-template
  namespace: default
  labels:
    app: app  # 标准 Labels
spec:
  containers:
    - name: app
      image: app:v1.0.0
      ports:
        - containerPort: 8080
```

**措施 3：Endpoints 监控**：

```bash
# 配置 Endpoints 监控
kubectl get endpoints -A

# 定期检查 Endpoints 状态
watch -n 5 kubectl get endpoints -A
```

**措施 4：Service 健康检查**：

```yaml
# 配置 Service 健康检查
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: default
  annotations:
    service.beta.kubernetes.io/health-check: "true"
spec:
  selector:
    app: app
  ports:
    - port: 8080
      targetPort: 8080
      protocol: TCP
  type: ClusterIP
```

---

## 4 验证与恢复

### 4.1 验证步骤

**步骤 1：验证 Service Selector**：

```bash
# 检查 Service Selector
kubectl get svc app-service -n default -o yaml | grep -A 5 selector

# 预期输出
selector:
  app: app
```

**步骤 2：验证 Pod Labels**：

```bash
# 检查 Pod Labels
kubectl get pod -n default --show-labels | grep app

# 预期输出
app-pod-005   1/1     Running   0          1m    app=app
```

**步骤 3：验证 Endpoints**：

```bash
# 检查 Endpoints
kubectl get endpoints app-service -n default

# 预期输出
NAME          ENDPOINTS              AGE
app-service   10.42.1.10:8080       1m
```

**步骤 4：验证 Service 访问**：

```bash
# 测试 Service 访问
curl http://app-service.default.svc.cluster.local:8080

# 预期输出
{"status":"ok"}
```

### 4.2 恢复确认

**恢复指标**：

- ✅ Service Selector：匹配 Pod Labels
- ✅ Endpoints：已创建
- ✅ DNS 解析：正常
- ✅ Service 访问：成功

**恢复时间**：

- **故障发现**：20:00:00
- **开始排查**：20:00:05
- **根因确认**：20:05:00
- **问题解决**：20:10:00
- **服务恢复**：20:10:05
- **总耗时**：10 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **Service Selector 必须匹配 Pod Labels**：
   - Service Selector 不匹配会导致 Endpoints 为空
   - 需要确保 Selector 和 Labels 匹配

2. **Endpoints 状态重要**：
   - Endpoints 为空会导致 Service 无法访问
   - 需要定期检查 Endpoints 状态

3. **使用 Deployment 管理 Pod**：
   - 使用 Deployment 可以确保 Pod Labels 一致性
   - 便于 Service 管理

### 5.2 最佳实践

1. **Service Selector 标准化**：
   - 使用标准 Selector 格式
   - 确保与 Pod Labels 匹配

2. **Pod Labels 标准化**：
   - 使用标准 Labels 格式
   - 确保与 Service Selector 匹配

3. **Endpoints 监控**：
   - 定期检查 Endpoints 状态
   - 及时发现 Endpoints 问题

4. **使用 Deployment**：
   - 使用 Deployment 管理 Pod
   - 确保 Pod Labels 一致性

### 5.3 相关文档

- [`../../TECHNICAL/03-networking/service/service.md`](../../TECHNICAL/03-networking/service/service.md) - Service 文档
- [`../../TECHNICAL/03-networking/endpoints/endpoints.md`](../../TECHNICAL/03-networking/endpoints/endpoints.md) - Endpoints 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

## 6 相关文档

- [`../README.md`](README.md) - 故障排查案例集目录
- [`../../TECHNICAL/03-networking/service/service.md`](../../TECHNICAL/03-networking/service/service.md) - Service 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
