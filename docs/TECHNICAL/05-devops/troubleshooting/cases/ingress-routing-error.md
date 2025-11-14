# 案例 N-003：Ingress 路由错误

> **案例编号**：N-003
> **故障类型**：路由故障
> **严重程度**：中等
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 N-003：Ingress 路由错误](#案例-n-003ingress-路由错误)
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

- Ingress 路由无法正确转发请求
- 请求返回 404 或 502 错误
- 路由规则不生效
- 应用无法通过 Ingress 访问

**错误日志**：

```text
# 访问 Ingress
$ curl http://app.example.com/api/v1/health

HTTP/1.1 404 Not Found
Content-Type: text/html
Content-Length: 123

404 Not Found
```

**时间线**：

- **21:00:00** - 创建 Ingress
- **21:00:05** - Ingress 配置完成
- **21:00:10** - 测试访问，返回 404
- **21:05:00** - 定位到路由规则问题

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **Ingress 控制器**：Traefik
- **Traefik 版本**：v2.10
- **节点数量**：3 个

**Ingress 配置**：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: default
spec:
  ingressClassName: traefik
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: app-service
                port:
                  number: 8080
```

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

### 1.3 影响范围

- **受影响 Ingress**：1 个（app-ingress）
- **受影响服务**：应用服务
- **业务影响**：应用无法通过 Ingress 访问，影响生产环境
- **用户影响**：所有依赖 Ingress 访问的用户无法访问

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 Ingress 状态**：

```bash
# 检查 Ingress 状态
kubectl get ingress app-ingress -n default

# 输出
NAME          CLASS    HOSTS              ADDRESS        PORTS   AGE
app-ingress   traefik  app.example.com    10.0.1.10      80      5m
```

**步骤 2：测试 Ingress 访问**：

```bash
# 测试 Ingress 访问
curl -H "Host: app.example.com" http://10.0.1.10/api/v1/health

# 输出
HTTP/1.1 404 Not Found
```

**步骤 3：检查 Traefik Pod**：

```bash
# 检查 Traefik Pod
kubectl get pod -n kube-system | grep traefik

# 输出
traefik-xxx   1/1     Running   0          5d
```

**初步结论**：

- Ingress 状态正常
- Traefik Pod 运行正常
- 但路由无法正确转发
- 需要检查路由规则和 Service

### 2.2 深入排查

**步骤 4：检查 Ingress 规则**：

```bash
# 检查 Ingress 规则
kubectl get ingress app-ingress -n default -o yaml | grep -A 10 rules

# 输出
rules:
  - host: app.example.com
    http:
      paths:
        - path: /api
          pathType: Prefix
          backend:
            service:
              name: app-service
              port:
                number: 8080
```

**步骤 5：检查 Service 状态**：

```bash
# 检查 Service 状态
kubectl get svc app-service -n default

# 输出
NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
app-service   ClusterIP   10.43.0.10      <none>        8080/TCP   5m
```

**步骤 6：检查 Endpoints**：

```bash
# 检查 Endpoints
kubectl get endpoints app-service -n default

# 输出
NAME          ENDPOINTS              AGE
app-service   10.42.1.10:8080       5m
```

**步骤 7：检查 Traefik 日志**：

```bash
# 检查 Traefik 日志
kubectl logs -n kube-system traefik-xxx --tail=50

# 输出
time="2025-11-13T21:00:10Z" level=error msg="Route not found: /api/v1/health"
time="2025-11-13T21:00:10Z" level=error msg="No service found for path: /api"
```

**步骤 8：检查应用路径**：

```bash
# 检查应用实际路径
kubectl exec -it app-pod-005 -n default -- curl http://localhost:8080/health

# 输出
{"status":"ok"}
```

**深入排查结论**：

- Ingress 规则配置为 `/api`，但应用实际路径为 `/health`
- 路径不匹配导致路由失败
- 需要修复 Ingress 路径配置

### 2.3 根因分析

**根因 1：路径配置不匹配**：

- Ingress 路径配置为 `/api`，但应用实际路径为 `/health`
- 路径不匹配导致路由失败
- 需要修复路径配置

**根因 2：pathType 配置错误**：

- pathType 可能配置错误
- Prefix 和 Exact 使用不当
- 导致路由规则不生效

**根因 3：Service 端口不匹配**：

- Service 端口可能不匹配
- targetPort 配置错误
- 导致路由无法转发到 Pod

**根本原因**：

**路径配置不匹配**：Ingress 路径配置为 `/api`，但应用实际路径为 `/health`，导致路由规则不匹配，从而 Ingress 无法正确转发请求。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：直接访问 Service**：

```bash
# 直接访问 Service
kubectl port-forward svc/app-service 8080:8080 -n default

# 访问
curl http://localhost:8080/health
```

**方案 2：修改 Ingress 路径**：

```yaml
# 修改 Ingress 路径
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: default
spec:
  ingressClassName: traefik
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-service
                port:
                  number: 8080
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
- ⚠️ 可能影响路由规则

### 3.2 永久解决方案

**方案 1：修复 Ingress 路径**：

```yaml
# 修复 Ingress 路径
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: default
spec:
  ingressClassName: traefik
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-service
                port:
                  number: 8080
```

**方案 2：使用路径重写**：

```yaml
# 使用 Traefik 路径重写
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: default
  annotations:
    traefik.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: traefik
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: app-service
                port:
                  number: 8080
```

**方案 3：配置多个路径规则**：

```yaml
# 配置多个路径规则
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: default
spec:
  ingressClassName: traefik
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: app-service
                port:
                  number: 8080
          - path: /health
            pathType: Exact
            backend:
              service:
                name: app-service
                port:
                  number: 8080
```

**方案 4：使用 IngressRoute（Traefik CRD）**：

```yaml
# 使用 IngressRoute
apiVersion: traefik.containo.us/v1alpha1
kind: IngressRoute
metadata:
  name: app-ingressroute
  namespace: default
spec:
  entryPoints:
    - web
  routes:
    - match: Host(`app.example.com`) && PathPrefix(`/`)
      kind: Rule
      services:
        - name: app-service
          port: 8080
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：Ingress 路径标准化**：

```yaml
# 创建 Ingress 模板
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress-template
  namespace: default
spec:
  ingressClassName: traefik
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-service
                port:
                  number: 8080
```

**措施 2：路径配置审查**：

```bash
# 定期审查 Ingress 路径配置
kubectl get ingress -A -o yaml | grep -A 5 paths
```

**措施 3：路由测试自动化**：

```bash
# 配置路由测试脚本
#!/bin/bash
curl -H "Host: app.example.com" http://10.0.1.10/health
if [ $? -eq 0 ]; then
  echo "Route test passed"
else
  echo "Route test failed"
fi
```

**措施 4：Traefik 监控**：

```bash
# 配置 Traefik 监控
kubectl logs -n kube-system traefik-xxx --tail=50

# 定期检查 Traefik 日志
watch -n 5 kubectl logs -n kube-system traefik-xxx --tail=10
```

---

## 4 验证与恢复

### 4.1 验证步骤

**步骤 1：验证 Ingress 配置**：

```bash
# 检查 Ingress 配置
kubectl get ingress app-ingress -n default -o yaml | grep -A 10 paths

# 预期输出
paths:
  - path: /
    pathType: Prefix
    backend:
      service:
        name: app-service
        port:
          number: 8080
```

**步骤 2：验证路由访问**：

```bash
# 测试路由访问
curl -H "Host: app.example.com" http://10.0.1.10/health

# 预期输出
{"status":"ok"}
```

**步骤 3：验证 Traefik 日志**：

```bash
# 检查 Traefik 日志
kubectl logs -n kube-system traefik-xxx --tail=10

# 预期输出
time="2025-11-13T21:10:00Z" level=info msg="Route matched: /health"
time="2025-11-13T21:10:00Z" level=info msg="Request forwarded to service: app-service"
```

**步骤 4：验证服务可用性**：

```bash
# 测试服务端点
curl -H "Host: app.example.com" http://10.0.1.10/api/v1/data

# 预期输出
{"data":"..."}
```

### 4.2 恢复确认

**恢复指标**：

- ✅ Ingress 配置：正确
- ✅ 路由访问：成功
- ✅ Traefik 日志：无错误
- ✅ 服务可用性：正常

**恢复时间**：

- **故障发现**：21:00:00
- **开始排查**：21:00:05
- **根因确认**：21:05:00
- **问题解决**：21:10:00
- **服务恢复**：21:10:05
- **总耗时**：10 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **路径配置必须匹配应用路径**：
   - Ingress 路径配置必须与应用实际路径匹配
   - 路径不匹配会导致路由失败

2. **pathType 配置重要**：
   - Prefix 和 Exact 使用不当会导致路由规则不生效
   - 需要根据实际需求选择 pathType

3. **路径重写功能有用**：
   - 使用路径重写可以解决路径不匹配问题
   - Traefik 支持路径重写功能

### 5.2 最佳实践

1. **Ingress 路径标准化**：
   - 使用标准路径格式
   - 确保路径与应用路径匹配

2. **路径配置审查**：
   - 定期审查 Ingress 路径配置
   - 确保路径配置正确

3. **路由测试自动化**：
   - 配置路由测试脚本
   - 自动发现路由问题

4. **Traefik 监控**：
   - 定期检查 Traefik 日志
   - 及时发现路由问题

### 5.3 相关文档

- [`../../TECHNICAL/03-networking/ingress/ingress.md`](../../TECHNICAL/03-networking/ingress/ingress.md) - Ingress 文档
- [`../../TECHNICAL/03-networking/traefik/traefik.md`](../../TECHNICAL/03-networking/traefik/traefik.md) - Traefik 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

## 6 相关文档

- [`../README.md`](README.md) - 故障排查案例集目录
- [`../../TECHNICAL/03-networking/ingress/ingress.md`](../../TECHNICAL/03-networking/ingress/ingress.md) - Ingress 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
