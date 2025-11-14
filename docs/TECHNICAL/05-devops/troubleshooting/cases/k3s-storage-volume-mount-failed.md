# 案例 K-003：K3s 存储卷挂载失败

> **案例编号**：K-003
> **故障类型**：存储故障
> **严重程度**：中等
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 K-003：K3s 存储卷挂载失败](#案例-k-003k3s-存储卷挂载失败)
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

- Pod 一直处于 `ContainerCreating` 状态
- 存储卷无法挂载到 Pod
- 事件显示：`MountVolume.SetUp failed for volume "data-volume" : mount failed: exit status 32`
- 应用无法启动，服务不可用

**错误日志**：

```text
Events:
  Type     Reason       Age                From               Message
  ----     ------       ----               ----               -------
  Warning  FailedMount  5m (x12 over 5m)   kubelet            MountVolume.SetUp failed for volume "data-volume" : mount failed: exit status 32
  Warning  FailedMount  5m (x12 over 5m)   kubelet            Unable to attach or mount volumes: unmounted volumes=[data-volume], unattached volumes=[data-volume]: timed out waiting for the condition
```

**时间线**：

- **15:00:00** - 创建 Pod
- **15:00:05** - Pod 进入 ContainerCreating 状态
- **15:00:10** - 存储卷挂载开始
- **15:05:00** - 挂载失败，Pod 仍为 ContainerCreating

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **存储类型**：local-path-provisioner
- **存储类**：local-path
- **节点数量**：1 个

**Pod 配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-002
  namespace: default
spec:
  containers:
    - name: app
      image: app:v1.0.0
      volumeMounts:
        - name: data-volume
          mountPath: /data
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: data-pvc
```

**PVC 配置**：

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: local-path
  resources:
    requests:
      storage: 1Gi
```

### 1.3 影响范围

- **受影响 Pod**：1 个（app-pod-002）
- **受影响服务**：应用服务
- **业务影响**：应用无法启动，服务完全不可用
- **用户影响**：所有依赖该服务的用户无法访问

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 Pod 状态**：

```bash
# 检查 Pod 状态
kubectl get pod app-pod-002 -n default

# 输出
NAME          READY   STATUS              RESTARTS   AGE
app-pod-002   0/1     ContainerCreating   0          5m
```

**步骤 2：查看 Pod 事件**：

```bash
# 查看 Pod 事件
kubectl describe pod app-pod-002 -n default

# 输出
Events:
  Type     Reason       Age                From               Message
  ----     ------       ----               ----               -------
  Warning  FailedMount  5m (x12 over 5m)   kubelet            MountVolume.SetUp failed for volume "data-volume" : mount failed: exit status 32
```

**步骤 3：检查 PVC 状态**：

```bash
# 检查 PVC 状态
kubectl get pvc data-pvc -n default

# 输出
NAME       STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
data-pvc   Pending                                      local-path     5m
```

**初步结论**：

- Pod 状态为 ContainerCreating
- PVC 状态为 Pending
- 存储卷挂载失败

### 2.2 深入排查

**步骤 4：检查 StorageClass**：

```bash
# 检查 StorageClass
kubectl get storageclass local-path

# 输出
NAME          PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE   AGE
local-path   rancher.io/local-path   Delete          Immediate           5d
```

**步骤 5：检查 PV 状态**：

```bash
# 检查 PV 状态
kubectl get pv

# 输出
（无 PV 创建）
```

**步骤 6：检查 local-path-provisioner**：

```bash
# 检查 local-path-provisioner Pod
kubectl get pod -n kube-system | grep local-path

# 输出
local-path-provisioner-xxx   0/1     CrashLoopBackOff   0          10m
```

**步骤 7：查看 local-path-provisioner 日志**：

```bash
# 查看 local-path-provisioner 日志
kubectl logs -n kube-system local-path-provisioner-xxx

# 输出
time="2025-11-13T15:00:10Z" level=error msg="Failed to create volume: mkdir /opt/local-path-provisioner: permission denied"
```

**步骤 8：检查节点存储路径**：

```bash
# 检查节点存储路径
kubectl exec -it local-path-provisioner-xxx -n kube-system -- ls -la /opt/local-path-provisioner

# 输出
ls: cannot access /opt/local-path-provisioner: Permission denied
```

**深入排查结论**：

- local-path-provisioner Pod 处于 CrashLoopBackOff 状态
- 存储路径权限不足
- 需要检查存储路径配置和权限

### 2.3 根因分析

**根因 1：local-path-provisioner 故障**：

- local-path-provisioner Pod 处于 CrashLoopBackOff 状态
- 无法创建和管理存储卷

**根因 2：存储路径权限不足**：

- 存储路径 `/opt/local-path-provisioner` 权限不足
- local-path-provisioner 无法创建目录

**根因 3：存储路径配置错误**：

- 存储路径可能不存在或配置错误
- 需要检查 local-path-provisioner 配置

**根本原因**：

**local-path-provisioner 故障和存储路径权限不足**：local-path-provisioner Pod 故障导致无法创建存储卷，同时存储路径权限不足进一步阻止了存储卷的创建。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：重启 local-path-provisioner**：

```bash
# 删除并重新创建 local-path-provisioner Pod
kubectl delete pod -n kube-system local-path-provisioner-xxx
kubectl apply -f local-path-provisioner.yaml
```

**方案 2：修复存储路径权限**：

```bash
# 在节点上修复存储路径权限
sudo mkdir -p /opt/local-path-provisioner
sudo chmod 777 /opt/local-path-provisioner
```

**方案 3：使用临时存储**：

```yaml
# 使用 emptyDir 作为临时存储
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-002
  namespace: default
spec:
  containers:
    - name: app
      image: app:v1.0.0
      volumeMounts:
        - name: data-volume
          mountPath: /data
  volumes:
    - name: data-volume
      emptyDir: {}  # 使用临时存储
```

**临时方案效果**：

- ✅ 可以快速恢复服务
- ⚠️ 但未解决根本问题
- ⚠️ 数据可能丢失（使用 emptyDir）

### 3.2 永久解决方案

**方案 1：修复 local-path-provisioner 配置**：

```yaml
# 修复 local-path-provisioner 配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: local-path-provisioner
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: local-path-provisioner
  template:
    metadata:
      labels:
        app: local-path-provisioner
    spec:
      serviceAccountName: local-path-provisioner-service-account
      containers:
        - name: local-path-provisioner
          image: rancher/local-path-provisioner:v0.0.24
          imagePullPolicy: IfNotPresent
          command:
            - local-path-provisioner
            - --debug
            - start
            - --config
            - /etc/config/config.json
          volumeMounts:
            - name: config-volume
              mountPath: /etc/config/
          env:
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
      volumes:
        - name: config-volume
          configMap:
            name: local-path-config
```

**方案 2：配置存储路径和权限**：

```yaml
# 创建 ConfigMap 配置存储路径
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-path-config
  namespace: kube-system
data:
  config.json: |
    {
      "nodePathMap": [
        {
          "node": "DEFAULT_PATH_FOR_NON_LISTED_NODES",
          "paths": ["/opt/local-path-provisioner"]
        }
      ]
    }
  setup: |
    #!/bin/sh
    mkdir -p /opt/local-path-provisioner
    chmod 777 /opt/local-path-provisioner
```

**方案 3：使用 hostPath 存储**：

```yaml
# 使用 hostPath 存储
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-002
  namespace: default
spec:
  containers:
    - name: app
      image: app:v1.0.0
      volumeMounts:
        - name: data-volume
          mountPath: /data
  volumes:
    - name: data-volume
      hostPath:
        path: /opt/app-data
        type: DirectoryOrCreate
```

**方案 4：使用 NFS 或其他存储**：

```yaml
# 使用 NFS 存储
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: nfs
  resources:
    requests:
      storage: 1Gi
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：存储路径标准化**：

```bash
# 创建标准存储路径
sudo mkdir -p /opt/local-path-provisioner
sudo chmod 777 /opt/local-path-provisioner
sudo chown k3s:k3s /opt/local-path-provisioner
```

**措施 2：local-path-provisioner 监控**：

```bash
# 配置 local-path-provisioner 监控
kubectl get pod -n kube-system | grep local-path

# 定期检查 local-path-provisioner 状态
watch -n 5 kubectl get pod -n kube-system | grep local-path
```

**措施 3：存储类配置审查**：

```yaml
# 定期审查 StorageClass 配置
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-path
provisioner: rancher.io/local-path
volumeBindingMode: Immediate
reclaimPolicy: Delete
```

**措施 4：存储卷备份**：

```bash
# 定期备份存储卷数据
kubectl exec -it app-pod-002 -n default -- tar -czf /backup/data.tar.gz /data
```

---

## 4 验证与恢复

### 4.1 验证步骤

**步骤 1：验证 local-path-provisioner**：

```bash
# 检查 local-path-provisioner Pod 状态
kubectl get pod -n kube-system | grep local-path

# 预期输出
local-path-provisioner-xxx   1/1     Running   0          1m
```

**步骤 2：验证 PVC 状态**：

```bash
# 检查 PVC 状态
kubectl get pvc data-pvc -n default

# 预期输出
NAME       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
data-pvc   Bound    pvc-12345678-1234-1234-1234-123456789012   1Gi        RWO            local-path     1m
```

**步骤 3：验证 Pod 状态**：

```bash
# 检查 Pod 状态
kubectl get pod app-pod-002 -n default

# 预期输出
NAME          READY   STATUS    RESTARTS   AGE
app-pod-002   1/1     Running   0          1m
```

**步骤 4：验证存储卷挂载**：

```bash
# 检查存储卷挂载
kubectl exec -it app-pod-002 -n default -- df -h /data

# 预期输出
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       1.0G  100M  900M  10% /data
```

### 4.2 恢复确认

**恢复指标**：

- ✅ local-path-provisioner：Running
- ✅ PVC 状态：Bound
- ✅ Pod 状态：Running
- ✅ 存储卷挂载：成功

**恢复时间**：

- **故障发现**：15:00:00
- **开始排查**：15:00:05
- **根因确认**：15:10:00
- **问题解决**：15:15:00
- **服务恢复**：15:15:05
- **总耗时**：15 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **local-path-provisioner 故障导致存储卷无法创建**：
   - local-path-provisioner Pod 故障会阻止存储卷创建
   - 需要确保 local-path-provisioner 正常运行

2. **存储路径权限重要**：
   - 存储路径权限不足会导致存储卷创建失败
   - 需要正确配置存储路径权限

3. **存储类配置影响存储卷创建**：
   - StorageClass 配置错误会影响存储卷创建
   - 需要正确配置 StorageClass

### 5.2 最佳实践

1. **确保 local-path-provisioner 正常运行**：
   - 定期检查 local-path-provisioner Pod 状态
   - 及时处理 local-path-provisioner 故障

2. **配置存储路径权限**：
   - 创建标准存储路径
   - 正确配置存储路径权限

3. **存储类配置审查**：
   - 定期审查 StorageClass 配置
   - 确保存储类配置正确

4. **存储卷备份**：
   - 定期备份存储卷数据
   - 防止数据丢失

### 5.3 相关文档

- [`../../TECHNICAL/01-core-foundations/k3s/k3s.md`](../../TECHNICAL/01-core-foundations/k3s/k3s.md) - K3s 文档
- [`../../TECHNICAL/04-storage/pvc/pvc.md`](../../TECHNICAL/04-storage/pvc/pvc.md) - PVC 文档
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
