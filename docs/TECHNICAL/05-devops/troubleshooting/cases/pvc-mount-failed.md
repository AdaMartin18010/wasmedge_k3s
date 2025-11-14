# 案例 S-001：PVC 挂载失败

> **案例编号**：S-001
> **故障类型**：存储挂载故障
> **严重程度**：严重
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 S-001：PVC 挂载失败](#案例-s-001pvc-挂载失败)
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
- PVC 无法挂载到 Pod
- 事件显示：`MountVolume.SetUp failed for volume "pvc-xxx" : mount failed: exit status 32`
- 应用无法启动，服务不可用

**错误日志**：

```text
Events:
  Type     Reason       Age                From               Message
  ----     ------       ----               ----               -------
  Warning  FailedMount  5m (x12 over 5m)   kubelet            MountVolume.SetUp failed for volume "pvc-xxx" : mount failed: exit status 32
  Warning  FailedMount  5m (x12 over 5m)   kubelet            Unable to attach or mount volumes: unmounted volumes=[data-volume], unattached volumes=[data-volume]: timed out waiting for the condition
```

**时间线**：

- **19:00:00** - 创建 Pod
- **19:00:05** - Pod 进入 ContainerCreating 状态
- **19:00:10** - PVC 挂载开始
- **19:05:00** - 挂载失败，Pod 仍为 ContainerCreating

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **存储类型**：NFS
- **存储类**：nfs-client
- **节点数量**：3 个

**Pod 配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-004
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
    - ReadWriteMany
  storageClassName: nfs-client
  resources:
    requests:
      storage: 10Gi
```

### 1.3 影响范围

- **受影响 Pod**：1 个（app-pod-004）
- **受影响服务**：应用服务
- **业务影响**：应用无法启动，服务完全不可用
- **用户影响**：所有依赖该服务的用户无法访问

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 Pod 状态**：

```bash
# 检查 Pod 状态
kubectl get pod app-pod-004 -n default

# 输出
NAME          READY   STATUS              RESTARTS   AGE
app-pod-004   0/1     ContainerCreating   0          5m
```

**步骤 2：查看 Pod 事件**：

```bash
# 查看 Pod 事件
kubectl describe pod app-pod-004 -n default

# 输出
Events:
  Type     Reason       Age                From               Message
  ----     ------       ----               ----               -------
  Warning  FailedMount  5m (x12 over 5m)   kubelet            MountVolume.SetUp failed for volume "pvc-xxx" : mount failed: exit status 32
```

**步骤 3：检查 PVC 状态**：

```bash
# 检查 PVC 状态
kubectl get pvc data-pvc -n default

# 输出
NAME       STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
data-pvc   Pending                                      nfs-client     5m
```

**初步结论**：

- Pod 状态为 ContainerCreating
- PVC 状态为 Pending
- 存储卷挂载失败

### 2.2 深入排查

**步骤 4：检查 PV 状态**：

```bash
# 检查 PV 状态
kubectl get pv

# 输出
（无 PV 创建）
```

**步骤 5：检查 StorageClass**：

```bash
# 检查 StorageClass
kubectl get storageclass nfs-client

# 输出
NAME         PROVISIONER      RECLAIMPOLICY   VOLUMEBINDINGMODE   AGE
nfs-client   cluster.local/nfs-client   Delete          Immediate           5d
```

**步骤 6：检查 NFS Provisioner**：

```bash
# 检查 NFS Provisioner Pod
kubectl get pod -n kube-system | grep nfs-client

# 输出
nfs-client-provisioner-xxx   0/1     CrashLoopBackOff   0          10m
```

**步骤 7：查看 NFS Provisioner 日志**：

```bash
# 查看 NFS Provisioner 日志
kubectl logs -n kube-system nfs-client-provisioner-xxx

# 输出
time="2025-11-13T19:00:10Z" level=error msg="Failed to connect to NFS server: connection refused"
time="2025-11-13T19:00:10Z" level=error msg="NFS server is not reachable"
```

**步骤 8：检查 NFS 服务器**：

```bash
# 检查 NFS 服务器连接
ping nfs-server-ip

# 输出
PING nfs-server-ip (192.168.1.100) 56(84) bytes of data.
^C
--- nfs-server-ip ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 4000ms
```

**深入排查结论**：

- NFS Provisioner Pod 处于 CrashLoopBackOff 状态
- NFS 服务器无法连接
- 需要检查 NFS 服务器状态和网络连接

### 2.3 根因分析

**根因 1：NFS 服务器不可达**：

- NFS 服务器无法连接
- 网络连接问题或 NFS 服务器故障
- 导致 NFS Provisioner 无法创建存储卷

**根因 2：NFS Provisioner 配置错误**：

- NFS Provisioner 配置可能错误
- NFS 服务器地址或路径配置不正确
- 导致无法连接到 NFS 服务器

**根因 3：网络策略阻止连接**：

- 网络策略可能阻止了 NFS 连接
- 防火墙规则可能阻止了 NFS 端口
- 导致无法连接到 NFS 服务器

**根本原因**：

**NFS 服务器不可达**：NFS 服务器无法连接，导致 NFS Provisioner 无法创建存储卷，从而 PVC 无法绑定到 PV，最终导致 Pod 无法挂载存储卷。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：使用临时存储**：

```yaml
# 使用 emptyDir 作为临时存储
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-004
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

**方案 2：使用 hostPath**：

```yaml
# 使用 hostPath 存储
apiVersion: v1
kind: Pod
metadata:
  name: app-pod-004
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

**方案 3：修复 NFS 服务器连接**：

```bash
# 检查 NFS 服务器状态
systemctl status nfs-server

# 重启 NFS 服务器
sudo systemctl restart nfs-server
```

**临时方案效果**：

- ✅ 可以快速恢复服务
- ⚠️ 但未解决根本问题
- ⚠️ 数据可能丢失（使用 emptyDir）

### 3.2 永久解决方案

**方案 1：修复 NFS 服务器**：

```bash
# 检查 NFS 服务器状态
systemctl status nfs-server

# 检查 NFS 服务器配置
cat /etc/exports

# 重启 NFS 服务器
sudo systemctl restart nfs-server
sudo systemctl enable nfs-server
```

**方案 2：修复 NFS Provisioner 配置**：

```yaml
# 修复 NFS Provisioner 配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nfs-client-provisioner
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nfs-client-provisioner
  template:
    metadata:
      labels:
        app: nfs-client-provisioner
    spec:
      serviceAccountName: nfs-client-provisioner
      containers:
        - name: nfs-client-provisioner
          image: quay.io/external_storage/nfs-client-provisioner:latest
          volumeMounts:
            - name: nfs-client-root
              mountPath: /persistentvolumes
          env:
            - name: PROVISIONER_NAME
              value: cluster.local/nfs-client
            - name: NFS_SERVER
              value: nfs-server-ip  # 修复 NFS 服务器地址
            - name: NFS_PATH
              value: /exports  # 修复 NFS 路径
      volumes:
        - name: nfs-client-root
          nfs:
            server: nfs-server-ip
            path: /exports
```

**方案 3：配置网络策略**：

```yaml
# 配置网络策略允许 NFS 连接
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-nfs
  namespace: kube-system
spec:
  podSelector:
    matchLabels:
      app: nfs-client-provisioner
  policyTypes:
    - Egress
  egress:
    - to:
        - ipBlock:
            cidr: 192.168.1.0/24  # NFS 服务器网段
      ports:
        - protocol: TCP
          port: 2049  # NFS 端口
        - protocol: TCP
          port: 111   # RPC 端口
```

**方案 4：使用其他存储方案**：

```yaml
# 使用 local-path-provisioner
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
      storage: 10Gi
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：NFS 服务器监控**：

```bash
# 配置 NFS 服务器监控
systemctl status nfs-server

# 定期检查 NFS 服务器状态
watch -n 5 systemctl status nfs-server
```

**措施 2：NFS Provisioner 监控**：

```bash
# 配置 NFS Provisioner 监控
kubectl get pod -n kube-system | grep nfs-client

# 定期检查 NFS Provisioner 状态
watch -n 5 kubectl get pod -n kube-system | grep nfs-client
```

**措施 3：网络连通性测试**：

```bash
# 配置网络连通性测试
ping nfs-server-ip
telnet nfs-server-ip 2049
```

**措施 4：存储卷备份**：

```bash
# 定期备份存储卷数据
kubectl exec -it app-pod-004 -n default -- tar -czf /backup/data.tar.gz /data
```

---

## 4 验证与恢复

### 4.1 验证步骤

**步骤 1：验证 NFS 服务器**：

```bash
# 检查 NFS 服务器状态
systemctl status nfs-server

# 预期输出
Active: active (running)
```

**步骤 2：验证 NFS Provisioner**：

```bash
# 检查 NFS Provisioner Pod 状态
kubectl get pod -n kube-system | grep nfs-client

# 预期输出
nfs-client-provisioner-xxx   1/1     Running   0          1m
```

**步骤 3：验证 PVC 状态**：

```bash
# 检查 PVC 状态
kubectl get pvc data-pvc -n default

# 预期输出
NAME       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
data-pvc   Bound    pvc-12345678-1234-1234-1234-123456789012   10Gi       RWX            nfs-client     1m
```

**步骤 4：验证 Pod 状态**：

```bash
# 检查 Pod 状态
kubectl get pod app-pod-004 -n default

# 预期输出
NAME          READY   STATUS    RESTARTS   AGE
app-pod-004   1/1     Running   0          1m
```

**步骤 5：验证存储卷挂载**：

```bash
# 检查存储卷挂载
kubectl exec -it app-pod-004 -n default -- df -h /data

# 预期输出
Filesystem      Size  Used Avail Use% Mounted on
nfs-server-ip:/exports/pvc-xxx  10G  100M  9.9G   1% /data
```

### 4.2 恢复确认

**恢复指标**：

- ✅ NFS 服务器：运行正常
- ✅ NFS Provisioner：Running
- ✅ PVC 状态：Bound
- ✅ Pod 状态：Running
- ✅ 存储卷挂载：成功

**恢复时间**：

- **故障发现**：19:00:00
- **开始排查**：19:00:05
- **根因确认**：19:10:00
- **问题解决**：19:15:00
- **服务恢复**：19:15:05
- **总耗时**：15 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **NFS 服务器不可达导致 PVC 挂载失败**：
   - NFS 服务器故障会导致存储卷无法创建
   - 需要确保 NFS 服务器正常运行

2. **NFS Provisioner 配置重要**：
   - NFS Provisioner 配置错误会导致存储卷创建失败
   - 需要正确配置 NFS 服务器地址和路径

3. **网络连通性影响存储**：
   - 网络连通性问题会影响存储卷挂载
   - 需要确保网络连接正常

### 5.2 最佳实践

1. **NFS 服务器监控**：
   - 定期检查 NFS 服务器状态
   - 及时处理 NFS 服务器故障

2. **NFS Provisioner 配置**：
   - 正确配置 NFS 服务器地址和路径
   - 定期审查 NFS Provisioner 配置

3. **网络连通性测试**：
   - 定期测试 NFS 服务器连接
   - 及时发现网络问题

4. **存储卷备份**：
   - 定期备份存储卷数据
   - 防止数据丢失

### 5.3 相关文档

- [`../../TECHNICAL/04-storage/pvc/pvc.md`](../../TECHNICAL/04-storage/pvc/pvc.md) - PVC 文档
- [`../../TECHNICAL/04-storage/nfs/nfs.md`](../../TECHNICAL/04-storage/nfs/nfs.md) - NFS 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

## 6 相关文档

- [`../README.md`](README.md) - 故障排查案例集目录
- [`../../TECHNICAL/04-storage/pvc/pvc.md`](../../TECHNICAL/04-storage/pvc/pvc.md) - PVC 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
