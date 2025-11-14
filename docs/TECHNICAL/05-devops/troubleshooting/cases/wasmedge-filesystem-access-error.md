# 案例 W-004：Wasm 文件系统访问错误

> **案例编号**：W-004
> **故障类型**：文件系统访问故障
> **严重程度**：中等
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 W-004：Wasm 文件系统访问错误](#案例-w-004wasm-文件系统访问错误)
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

- Wasm 应用无法访问文件系统
- 应用启动后立即报错：`Permission denied: /data/config.json`
- 日志显示：`Error: failed to open file: /data/config.json`
- 应用状态为 `Running`，但无法读取配置文件

**错误日志**：

```text
2025-11-13T11:00:15.123Z ERROR [wasm-app] File system access failed
2025-11-13T11:00:15.124Z ERROR [wasm-app] Error: failed to open file: /data/config.json
2025-11-13T11:00:15.125Z ERROR [wasm-app] Permission denied
2025-11-13T11:00:15.126Z ERROR [wasm-app] Stack trace:
    at wasm_fs_open (wasm-app.wasm:0x1234)
    at main (wasm-app.wasm:0x5678)
```

**时间线**：

- **11:00:00** - Wasm 应用 Pod 启动
- **11:00:05** - 应用开始尝试读取配置文件
- **11:00:15** - 文件访问失败，应用报错
- **11:00:20** - 应用进入错误状态

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **WasmEdge 版本**：v0.14.0
- **存储类型**：本地存储
- **文件系统**：ext4

**应用配置**：

- **Runtime**：WasmEdge
- **存储卷**：ConfigMap
- **挂载路径**：/data
- **配置文件**：/data/config.json

**Pod 信息**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-002
  namespace: default
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      volumeMounts:
        - name: config
          mountPath: /data
      env:
        - name: CONFIG_PATH
          value: "/data/config.json"
  volumes:
    - name: config
      configMap:
        name: wasm-app-config
```

### 1.3 影响范围

- **受影响 Pod**：1 个（wasm-app-002）
- **受影响服务**：Wasm 应用服务
- **业务影响**：应用无法读取配置，服务功能受限
- **用户影响**：部分功能不可用

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 Pod 状态**：

```bash
# 检查 Pod 状态
kubectl get pod wasm-app-002 -n default

# 输出
NAME           READY   STATUS    RESTARTS   AGE
wasm-app-002   1/1     Running   0          5m
```

**步骤 2：查看 Pod 日志**：

```bash
# 查看 Pod 日志
kubectl logs wasm-app-002 -n default

# 输出
2025-11-13T11:00:15.123Z ERROR [wasm-app] File system access failed
2025-11-13T11:00:15.124Z ERROR [wasm-app] Error: failed to open file: /data/config.json
```

**步骤 3：检查文件是否存在**：

```bash
# 在 Pod 内检查文件
kubectl exec -it wasm-app-002 -n default -- ls -la /data

# 输出
total 8
drwxr-xr-x 2 root root 4096 Nov 13 11:00 .
drwxr-xr-x 1 root root 4096 Nov 13 11:00 ..
-rw-r--r-- 1 root root  123 Nov 13 11:00 config.json
```

**初步结论**：

- Pod 状态正常（Running）
- 文件存在且权限正常
- 但 Wasm 应用无法访问文件

### 2.2 深入排查

**步骤 4：检查文件权限**：

```bash
# 检查文件权限
kubectl exec -it wasm-app-002 -n default -- stat /data/config.json

# 输出
  File: /data/config.json
  Size: 123             Blocks: 8          IO Block: 4096   regular file
Device: 801h/2049d      Inode: 123456      Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
```

**步骤 5：检查 WasmEdge 文件系统权限**：

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

**步骤 6：检查 Pod 安全上下文**：

```bash
# 检查 Pod 安全上下文
kubectl get pod wasm-app-002 -n default -o yaml | grep -A 10 securityContext

# 输出
（无 securityContext 配置）
```

**步骤 7：检查 WasmEdge 文件系统权限配置**：

```bash
# 检查 WasmEdge 文件系统权限配置
kubectl describe pod wasm-app-002 -n default | grep -i filesystem

# 输出
（无文件系统相关配置）
```

**步骤 8：测试文件访问**：

```bash
# 测试文件访问
kubectl exec -it wasm-app-002 -n default -- cat /data/config.json

# 输出
{
  "app": "wasm-app",
  "version": "1.0.0"
}
```

**深入排查结论**：

- 文件存在且权限正常
- 容器可以访问文件
- WasmEdge 文件系统权限可能受限
- 需要检查 WasmEdge 的文件系统配置

### 2.3 根因分析

**根因 1：WasmEdge 文件系统权限受限**：

- WasmEdge 默认文件系统权限受限
- 需要显式配置文件系统权限才能访问挂载的卷

**根因 2：WASI 权限配置缺失**：

- WasmEdge 使用 WASI（WebAssembly System Interface）进行文件系统访问
- 需要显式配置 WASI 权限

**根因 3：挂载路径权限问题**：

- 挂载路径的权限可能不正确
- Wasm 应用运行的用户可能没有访问权限

**根本原因**：

**WasmEdge 文件系统权限配置缺失**：WasmEdge 默认不允许访问挂载的文件系统，需要在 Pod 配置中显式启用文件系统权限。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：重启 Pod**：

```bash
# 删除并重新创建 Pod
kubectl delete pod wasm-app-002 -n default
kubectl apply -f wasm-app.yaml
```

**方案 2：修改文件权限**：

```bash
# 修改文件权限
kubectl exec -it wasm-app-002 -n default -- chmod 644 /data/config.json
```

**临时方案效果**：

- ✅ 可以快速恢复服务
- ⚠️ 但未解决根本问题
- ⚠️ 可能再次出现相同问题

### 3.2 永久解决方案

**方案 1：配置 WasmEdge 文件系统权限**：

```yaml
# 修改 Pod 配置，启用文件系统权限
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-002
  namespace: default
  annotations:
    wasmedge.filesystem/allowed: "true"  # 启用文件系统权限
    wasmedge.filesystem/paths: "/data"   # 允许访问的路径
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      volumeMounts:
        - name: config
          mountPath: /data
          readOnly: true  # 只读挂载
      env:
        - name: CONFIG_PATH
          value: "/data/config.json"
      securityContext:
        runAsUser: 1000  # 指定运行用户
        runAsGroup: 1000
        fsGroup: 1000
  volumes:
    - name: config
      configMap:
        name: wasm-app-config
        defaultMode: 0644  # 设置文件权限
```

**方案 2：使用 WASI 权限配置**：

```yaml
# 配置 WASI 权限
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-002
  namespace: default
  annotations:
    wasmedge.wasi/preopened-dirs: "/data"  # 预打开目录
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      volumeMounts:
        - name: config
          mountPath: /data
      env:
        - name: CONFIG_PATH
          value: "/data/config.json"
        - name: WASMEDGE_FS_ALLOWED
          value: "true"
        - name: WASMEDGE_FS_PATHS
          value: "/data"
```

**方案 3：使用 ConfigMap 挂载**：

```yaml
# 使用 ConfigMap 挂载配置
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-002
  namespace: default
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      volumeMounts:
        - name: config
          mountPath: /data
          readOnly: true
      env:
        - name: CONFIG_PATH
          value: "/data/config.json"
  volumes:
    - name: config
      configMap:
        name: wasm-app-config
        items:
          - key: config.json
            path: config.json
            mode: 0644
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：标准化文件系统配置**：

```yaml
# 创建 Wasm 应用模板
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-template
  namespace: default
  annotations:
    wasmedge.filesystem/allowed: "true"
    wasmedge.filesystem/paths: "/data"
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasm-app:v1.0.0
      securityContext:
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
```

**措施 2：使用 ConfigMap 和 Secret**：

- 使用 ConfigMap 存储配置文件
- 使用 Secret 存储敏感信息
- 避免直接挂载文件系统

**措施 3：文件权限审查**：

- 定期审查文件权限配置
- 确保 Wasm 应用有必要的文件系统权限
- 使用最小权限原则

**措施 4：监控和告警**：

```yaml
# 配置文件访问监控
apiVersion: v1
kind: ConfigMap
metadata:
  name: wasm-fs-monitor
data:
  monitor.sh: |
    #!/bin/bash
    while true; do
      if [ ! -f "$CONFIG_PATH" ]; then
        echo "Config file not found"
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
kubectl get pod wasm-app-002 -n default -o yaml | grep -A 5 annotations

# 预期输出
annotations:
  wasmedge.filesystem/allowed: "true"
  wasmedge.filesystem/paths: "/data"
```

**步骤 2：验证文件访问**：

```bash
# 测试文件访问
kubectl exec -it wasm-app-002 -n default -- cat /data/config.json

# 预期输出
{
  "app": "wasm-app",
  "version": "1.0.0"
}
```

**步骤 3：验证应用功能**：

```bash
# 检查应用日志
kubectl logs wasm-app-002 -n default --tail=50

# 预期输出
2025-11-13T11:05:00.123Z INFO [wasm-app] Config file loaded successfully
2025-11-13T11:05:00.124Z INFO [wasm-app] Application started successfully
```

**步骤 4：验证服务可用性**：

```bash
# 测试服务端点
curl http://wasm-app-service.default.svc.cluster.local:8080/health

# 预期输出
{"status":"ok","config":"loaded"}
```

### 4.2 恢复确认

**恢复指标**：

- ✅ Pod 状态：Running
- ✅ 文件访问：成功
- ✅ 应用日志：无错误
- ✅ 服务可用性：正常

**恢复时间**：

- **故障发现**：11:00:00
- **开始排查**：11:00:05
- **根因确认**：11:05:00
- **问题解决**：11:10:00
- **服务恢复**：11:10:05
- **总耗时**：10 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **WasmEdge 文件系统权限默认受限**：
   - WasmEdge 默认不允许访问挂载的文件系统
   - 需要显式配置文件系统权限

2. **WASI 权限配置重要**：
   - WasmEdge 使用 WASI 进行文件系统访问
   - 需要正确配置 WASI 权限

3. **文件权限和用户上下文**：
   - 文件权限和运行用户上下文需要匹配
   - 需要正确配置 securityContext

### 5.2 最佳实践

1. **使用 ConfigMap 和 Secret**：
   - 使用 ConfigMap 存储配置文件
   - 使用 Secret 存储敏感信息
   - 避免直接挂载文件系统

2. **配置文件系统权限**：
   - 显式配置 WasmEdge 文件系统权限
   - 使用最小权限原则

3. **文件权限审查**：
   - 定期审查文件权限配置
   - 确保应用有必要的文件系统权限

4. **监控和告警**：
   - 配置文件访问监控
   - 及时发现文件系统问题

### 5.3 相关文档

- [`../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md`](../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md) - WasmEdge 文档
- [`../../TECHNICAL/04-storage/configmap/configmap.md`](../../TECHNICAL/04-storage/configmap/configmap.md) - ConfigMap 文档
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
