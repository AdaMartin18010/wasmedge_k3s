# 案例 O-001：Gatekeeper Webhook 超时

> **案例编号**：O-001
> **故障类型**：Webhook 超时故障
> **严重程度**：严重
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 O-001：Gatekeeper Webhook 超时](#案例-o-001gatekeeper-webhook-超时)
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

- Pod 创建/更新操作超时
- 事件显示：`admission webhook "validation.gatekeeper.sh" is unavailable`
- 日志显示：`context deadline exceeded`
- 应用无法部署，服务不可用

**错误日志**：

```text
Events:
  Type     Reason              Age                From               Message
  ----     ------              ----               ----               -------
  Warning  FailedCreate        5m (x12 over 5m)   replicaset-controller  Error creating: Internal error occurred: failed calling webhook "validation.gatekeeper.sh": Post "https://gatekeeper-webhook-service.gatekeeper-system.svc:443/v1/admit?timeout=3s": context deadline exceeded
```

**时间线**：

- **16:00:00** - 尝试创建 Pod
- **16:00:03** - Webhook 调用开始
- **16:00:06** - Webhook 超时（3秒）
- **16:00:10** - Pod 创建失败

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **Gatekeeper 版本**：v3.15
- **OPA 版本**：v0.58.0
- **节点数量**：3 个

**Gatekeeper 配置**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gatekeeper-controller-manager
  namespace: gatekeeper-system
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: manager
          image: openpolicyagent/gatekeeper:v3.15.0
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
```

**Webhook 配置**：

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: gatekeeper-validating-webhook-configuration
webhooks:
  - name: validation.gatekeeper.sh
    clientConfig:
      service:
        name: gatekeeper-webhook-service
        namespace: gatekeeper-system
        path: "/v1/admit"
    timeoutSeconds: 3
    failurePolicy: Fail
```

### 1.3 影响范围

- **受影响操作**：所有 Pod 创建/更新操作
- **受影响服务**：所有需要部署的服务
- **业务影响**：无法部署新服务，影响生产环境
- **用户影响**：所有依赖新部署服务的用户

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 Pod 创建状态**：

```bash
# 检查 Pod 创建状态
kubectl get pod app-pod-003 -n default

# 输出
NAME          READY   STATUS    RESTARTS   AGE
app-pod-003   0/1     Pending   0          5m
```

**步骤 2：查看 Pod 事件**：

```bash
# 查看 Pod 事件
kubectl describe pod app-pod-003 -n default

# 输出
Events:
  Type     Reason              Age                From               Message
  ----     ------              ----               ----               -------
  Warning  FailedCreate        5m (x12 over 5m)   replicaset-controller  Error creating: Internal error occurred: failed calling webhook "validation.gatekeeper.sh": Post "https://gatekeeper-webhook-service.gatekeeper-system.svc:443/v1/admit?timeout=3s": context deadline exceeded
```

**步骤 3：检查 Gatekeeper Pod 状态**：

```bash
# 检查 Gatekeeper Pod 状态
kubectl get pod -n gatekeeper-system

# 输出
NAME                                             READY   STATUS    RESTARTS   AGE
gatekeeper-controller-manager-xxx                1/1     Running   0          5d
gatekeeper-audit-xxx                             1/1     Running   0          5d
```

**初步结论**：

- Pod 创建失败，Webhook 超时
- Gatekeeper Pod 状态正常
- 需要检查 Webhook 服务状态

### 2.2 深入排查

**步骤 4：检查 Webhook Service**：

```bash
# 检查 Webhook Service
kubectl get svc -n gatekeeper-system

# 输出
NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
gatekeeper-webhook-service     ClusterIP   10.43.0.10      <none>        443/TCP   5d
```

**步骤 5：测试 Webhook 服务连通性**：

```bash
# 测试 Webhook 服务连通性
kubectl run test-pod --image=curlimages/curl --rm -it --restart=Never -- curl -k https://gatekeeper-webhook-service.gatekeeper-system.svc:443/v1/admit

# 输出
curl: (28) Operation timed out after 30000 milliseconds
```

**步骤 6：检查 Gatekeeper 日志**：

```bash
# 检查 Gatekeeper 日志
kubectl logs -n gatekeeper-system gatekeeper-controller-manager-xxx --tail=50

# 输出
time="2025-11-13T16:00:03Z" level=error msg="Failed to evaluate policy: timeout"
time="2025-11-13T16:00:03Z" level=error msg="Policy evaluation took too long: 5s"
```

**步骤 7：检查策略数量**：

```bash
# 检查策略数量
kubectl get constrainttemplates -A | wc -l
kubectl get constraints -A | wc -l

# 输出
10
150
```

**步骤 8：检查 Gatekeeper 资源使用**：

```bash
# 检查 Gatekeeper 资源使用
kubectl top pod -n gatekeeper-system

# 输出
NAME                                             CPU(cores)   MEMORY(bytes)
gatekeeper-controller-manager-xxx                500m         450Mi
gatekeeper-audit-xxx                             100m         200Mi
```

**深入排查结论**：

- Webhook 服务存在但响应超时
- Gatekeeper 策略评估超时
- 策略数量较多（150个约束）
- Gatekeeper 资源使用较高

### 2.3 根因分析

**根因 1：策略评估超时**：

- 策略数量过多（150个约束）
- 策略评估时间过长（超过3秒超时时间）
- OPA 评估性能不足

**根因 2：Webhook 超时时间过短**：

- Webhook 超时时间设置为3秒
- 策略评估需要更长时间
- 超时时间不足以完成评估

**根因 3：Gatekeeper 资源不足**：

- Gatekeeper 资源使用较高（450Mi 内存）
- CPU 使用率较高（500m）
- 资源不足导致评估性能下降

**根本原因**：

**策略评估超时和 Webhook 超时时间过短**：策略数量过多导致评估时间超过 Webhook 超时时间，同时 Gatekeeper 资源不足进一步降低了评估性能。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：增加 Webhook 超时时间**：

```yaml
# 修改 Webhook 配置，增加超时时间
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: gatekeeper-validating-webhook-configuration
webhooks:
  - name: validation.gatekeeper.sh
    clientConfig:
      service:
        name: gatekeeper-webhook-service
        namespace: gatekeeper-system
        path: "/v1/admit"
    timeoutSeconds: 10  # 增加超时时间到10秒
    failurePolicy: Fail
```

**方案 2：临时禁用部分策略**：

```bash
# 临时禁用部分策略
kubectl delete constraint <constraint-name> -n <namespace>
```

**方案 3：增加 Gatekeeper 资源**：

```yaml
# 增加 Gatekeeper 资源
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gatekeeper-controller-manager
  namespace: gatekeeper-system
spec:
  template:
    spec:
      containers:
        - name: manager
          resources:
            requests:
              memory: "512Mi"  # 增加内存
              cpu: "500m"     # 增加 CPU
            limits:
              memory: "1Gi"
              cpu: "1000m"
```

**临时方案效果**：

- ✅ 可以快速恢复服务
- ⚠️ 但未解决根本问题
- ⚠️ 可能影响安全性（禁用策略）

### 3.2 永久解决方案

**方案 1：优化策略性能**：

```yaml
# 优化策略结构，减少评估时间
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg}] {
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }
```

**方案 2：使用策略缓存**：

```yaml
# 配置策略缓存
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
  namespace: gatekeeper-system
spec:
  match:
    - excludedNamespaces: ["kube-system", "kube-public"]
  validation:
    traces:
      - user: "system:serviceaccount:gatekeeper-system:gatekeeper-admin"
  sync:
    syncOnly:
      - group: ""
        version: "v1"
        kind: "Pod"
```

**方案 3：增加 Webhook 超时时间**：

```yaml
# 增加 Webhook 超时时间
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: gatekeeper-validating-webhook-configuration
webhooks:
  - name: validation.gatekeeper.sh
    clientConfig:
      service:
        name: gatekeeper-webhook-service
        namespace: gatekeeper-system
        path: "/v1/admit"
    timeoutSeconds: 10  # 增加到10秒
    failurePolicy: Fail
    admissionReviewVersions: ["v1", "v1beta1"]
```

**方案 4：优化 Gatekeeper 配置**：

```yaml
# 优化 Gatekeeper 配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gatekeeper-controller-manager
  namespace: gatekeeper-system
spec:
  replicas: 2  # 增加副本数
  template:
    spec:
      containers:
        - name: manager
          image: openpolicyagent/gatekeeper:v3.15.0
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "1Gi"
              cpu: "1000m"
          env:
            - name: GOMAXPROCS
              value: "2"
            - name: GATEKEEPER_CONCURRENT_SYNC_LIMIT
              value: "10"
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：策略性能监控**：

```bash
# 配置策略性能监控
kubectl logs -n gatekeeper-system gatekeeper-controller-manager-xxx | grep "evaluation time"

# 定期检查策略评估时间
watch -n 5 kubectl logs -n gatekeeper-system gatekeeper-controller-manager-xxx --tail=10
```

**措施 2：策略数量管理**：

```bash
# 定期审查策略数量
kubectl get constraints -A | wc -l

# 删除不必要的策略
kubectl delete constraint <constraint-name> -n <namespace>
```

**措施 3：Webhook 超时时间审查**：

```yaml
# 定期审查 Webhook 超时时间
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: gatekeeper-validating-webhook-configuration
webhooks:
  - name: validation.gatekeeper.sh
    timeoutSeconds: 10  # 根据实际需求调整
```

**措施 4：Gatekeeper 资源监控**：

```bash
# 配置 Gatekeeper 资源监控
kubectl top pod -n gatekeeper-system

# 定期检查资源使用
watch -n 5 kubectl top pod -n gatekeeper-system
```

---

## 4 验证与恢复

### 4.1 验证步骤

**步骤 1：验证 Webhook 配置**：

```bash
# 检查 Webhook 配置
kubectl get validatingwebhookconfiguration gatekeeper-validating-webhook-configuration -o yaml | grep timeoutSeconds

# 预期输出
timeoutSeconds: 10
```

**步骤 2：验证 Pod 创建**：

```bash
# 测试 Pod 创建
kubectl run test-pod --image=nginx --restart=Never

# 预期输出
pod/test-pod created
```

**步骤 3：验证 Gatekeeper 日志**：

```bash
# 检查 Gatekeeper 日志
kubectl logs -n gatekeeper-system gatekeeper-controller-manager-xxx --tail=50

# 预期输出
time="2025-11-13T16:10:00Z" level=info msg="Policy evaluation completed: 2s"
```

**步骤 4：验证服务可用性**：

```bash
# 测试服务部署
kubectl apply -f app-deployment.yaml

# 预期输出
deployment.apps/app-deployment created
```

### 4.2 恢复确认

**恢复指标**：

- ✅ Webhook 超时时间：10秒
- ✅ Pod 创建：成功
- ✅ Gatekeeper 日志：无错误
- ✅ 服务可用性：正常

**恢复时间**：

- **故障发现**：16:00:00
- **开始排查**：16:00:05
- **根因确认**：16:10:00
- **问题解决**：16:15:00
- **服务恢复**：16:15:05
- **总耗时**：15 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **策略数量影响评估性能**：
   - 策略数量过多会导致评估时间过长
   - 需要优化策略结构或减少策略数量

2. **Webhook 超时时间重要**：
   - Webhook 超时时间过短会导致评估失败
   - 需要根据实际需求调整超时时间

3. **Gatekeeper 资源影响性能**：
   - Gatekeeper 资源不足会降低评估性能
   - 需要合理配置 Gatekeeper 资源

### 5.2 最佳实践

1. **优化策略性能**：
   - 优化策略结构，减少评估时间
   - 使用策略缓存提高性能

2. **合理配置 Webhook 超时时间**：
   - 根据实际需求配置超时时间
   - 定期审查超时时间配置

3. **Gatekeeper 资源管理**：
   - 合理配置 Gatekeeper 资源
   - 定期监控资源使用

4. **策略数量管理**：
   - 定期审查策略数量
   - 删除不必要的策略

### 5.3 相关文档

- [`../../TECHNICAL/02-runtime-policy/opa/opa.md`](../../TECHNICAL/02-runtime-policy/opa/opa.md) - OPA 文档
- [`../../TECHNICAL/02-runtime-policy/gatekeeper/gatekeeper.md`](../../TECHNICAL/02-runtime-policy/gatekeeper/gatekeeper.md) - Gatekeeper 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

## 6 相关文档

- [`../README.md`](README.md) - 故障排查案例集目录
- [`../../TECHNICAL/02-runtime-policy/gatekeeper/gatekeeper.md`](../../TECHNICAL/02-runtime-policy/gatekeeper/gatekeeper.md) - Gatekeeper 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
