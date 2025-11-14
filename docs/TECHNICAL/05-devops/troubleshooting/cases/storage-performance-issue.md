# 案例 S-002：存储性能问题

> **案例编号**：S-002
> **故障类型**：存储性能故障
> **严重程度**：中等
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 S-002：存储性能问题](#案例-s-002存储性能问题)
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

- 存储 I/O 性能下降
- 文件读写速度变慢（从 100MB/s 降低到 10MB/s）
- 应用响应时间变长
- 影响应用性能

**性能指标**：

```text
# 存储 I/O 测试
$ dd if=/dev/zero of=/data/test bs=1M count=1000

# 优化前
1000+0 records in
1000+0 records out
1048576000 bytes (1.0 GB, 1000 MiB) copied, 10.0 s, 105 MB/s

# 优化后
1000+0 records in
1000+0 records out
1048576000 bytes (1.0 GB, 1000 MiB) copied, 100.0 s, 10.5 MB/s
```

**时间线**：

- **00:00:00** - 发现性能下降
- **00:00:05** - 开始排查性能问题
- **00:00:10** - 确认存储 I/O 性能下降
- **00:05:00** - 定位到存储配置问题

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **存储类型**：NFS
- **存储类**：nfs-client
- **节点数量**：3 个

**存储配置**：

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
      storage: 100Gi
```

**NFS 配置**：

```bash
# NFS 服务器配置
/etc/exports:
/data  *(rw,sync,no_subtree_check)
```

### 1.3 影响范围

- **受影响存储**：所有 NFS 存储卷
- **受影响服务**：所有使用存储的服务
- **业务影响**：应用性能下降，影响用户体验
- **用户影响**：应用响应时间增加

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：测试存储 I/O 性能**：

```bash
# 测试存储 I/O 性能
kubectl exec -it app-pod-006 -n default -- dd if=/dev/zero of=/data/test bs=1M count=1000

# 输出
1000+0 records in
1000+0 records out
1048576000 bytes (1.0 GB, 1000 MiB) copied, 100.0 s, 10.5 MB/s
```

**步骤 2：检查存储使用情况**：

```bash
# 检查存储使用情况
kubectl exec -it app-pod-006 -n default -- df -h /data

# 输出
Filesystem      Size  Used Avail Use% Mounted on
nfs-server:/exports/pvc-xxx  100G   50G   50G  50% /data
```

**步骤 3：检查网络延迟**：

```bash
# 检查网络延迟
kubectl exec -it app-pod-006 -n default -- ping -c 5 nfs-server-ip

# 输出
PING nfs-server-ip (192.168.1.100) 56(84) bytes of data.
64 bytes from 192.168.1.100: icmp_seq=1 time=1.234 ms
64 bytes from 192.168.1.100: icmp_seq=2 time=1.256 ms
64 bytes from 192.168.1.100: icmp_seq=3 time=1.245 ms
64 bytes from 192.168.1.100: icmp_seq=4 time=1.267 ms
64 bytes from 192.168.1.100: icmp_seq=5 time=1.253 ms
```

**初步结论**：

- 存储 I/O 性能下降（10.5 MB/s）
- 存储使用正常（50%）
- 网络延迟正常（1.2ms）
- 需要检查 NFS 配置和存储设备

### 2.2 深入排查

**步骤 4：检查 NFS 挂载选项**：

```bash
# 检查 NFS 挂载选项
kubectl exec -it app-pod-006 -n default -- mount | grep nfs

# 输出
nfs-server:/exports/pvc-xxx on /data type nfs (rw,relatime,vers=3,rsize=32768,wsize=32768,namlen=255,hard,proto=tcp,timeo=600,retrans=2,sec=sys,mountaddr=192.168.1.100,mountvers=3,mountport=20048,mountproto=udp,local_lock=none,addr=192.168.1.100)
```

**步骤 5：检查 NFS 服务器性能**：

```bash
# 在 NFS 服务器上测试性能
dd if=/dev/zero of=/exports/test bs=1M count=1000

# 输出
1000+0 records in
1000+0 records out
1048576000 bytes (1.0 GB, 1000 MiB) copied, 10.0 s, 105 MB/s
```

**步骤 6：检查 NFS 服务器配置**：

```bash
# 检查 NFS 服务器配置
cat /etc/exports

# 输出
/data  *(rw,sync,no_subtree_check)
```

**步骤 7：检查存储设备 I/O**：

```bash
# 检查存储设备 I/O
iostat -x 1 5

# 输出
Device            r/s     w/s     rkB/s     wkB/s   await
sda              10.0    50.0     1000     50000   100.0
```

**步骤 8：检查 NFS 客户端配置**：

```bash
# 检查 NFS 客户端配置
cat /proc/mounts | grep nfs

# 输出
nfs-server:/exports/pvc-xxx /data nfs rw,relatime,vers=3,rsize=32768,wsize=32768 0 0
```

**深入排查结论**：

- NFS 服务器性能正常（105 MB/s）
- NFS 挂载选项可能不优化（rsize=32768, wsize=32768）
- 存储设备 I/O 正常
- 需要优化 NFS 挂载选项

### 2.3 根因分析

**根因 1：NFS 挂载选项不优化**：

- NFS 挂载选项 rsize 和 wsize 较小（32768）
- 导致 I/O 性能下降
- 需要增加 rsize 和 wsize

**根因 2：NFS 同步模式**：

- NFS 使用同步模式（sync）
- 导致写入性能下降
- 需要使用异步模式（async）

**根因 3：网络带宽限制**：

- 网络带宽可能不足
- 导致 I/O 性能下降
- 需要检查网络配置

**根本原因**：

**NFS 挂载选项不优化**：NFS 挂载选项 rsize 和 wsize 较小，且使用同步模式，导致 I/O 性能下降。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：增加 NFS 挂载选项**：

```bash
# 临时重新挂载 NFS
kubectl exec -it app-pod-006 -n default -- mount -o remount,rsize=1048576,wsize=1048576 /data
```

**方案 2：使用本地存储**：

```yaml
# 使用本地存储
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
      storage: 100Gi
```

**方案 3：增加网络带宽**：

```bash
# 检查网络带宽
ethtool eth0

# 增加网络带宽（如果可能）
```

**临时方案效果**：

- ✅ 可以快速恢复性能
- ⚠️ 但未解决根本问题
- ⚠️ 可能影响数据一致性

### 3.2 永久解决方案

**方案 1：优化 NFS 挂载选项**：

```yaml
# 优化 NFS StorageClass
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-client-optimized
provisioner: cluster.local/nfs-client
parameters:
  server: nfs-server-ip
  path: /exports
  mountOptions: "rsize=1048576,wsize=1048576,hard,intr,timeo=600"
```

**方案 2：优化 NFS 服务器配置**：

```bash
# 优化 NFS 服务器配置
/etc/exports:
/data  *(rw,async,no_subtree_check,no_root_squash)
```

**方案 3：使用 NFSv4**：

```yaml
# 使用 NFSv4
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-client-v4
provisioner: cluster.local/nfs-client
parameters:
  server: nfs-server-ip
  path: /exports
  mountOptions: "vers=4,rsize=1048576,wsize=1048576,hard,intr,timeo=600"
```

**方案 4：使用 SSD 存储**：

```yaml
# 使用 SSD 存储
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: ssd
  resources:
    requests:
      storage: 100Gi
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：存储性能监控**：

```bash
# 配置存储性能监控
iostat -x 1 5

# 定期检查存储 I/O 性能
watch -n 5 iostat -x 1 5
```

**措施 2：NFS 配置审查**：

```bash
# 定期审查 NFS 配置
cat /etc/exports
mount | grep nfs
```

**措施 3：存储性能测试**：

```bash
# 配置存储性能测试
dd if=/dev/zero of=/data/test bs=1M count=1000
```

**措施 4：网络带宽监控**：

```bash
# 配置网络带宽监控
iftop -i eth0

# 定期检查网络带宽
watch -n 5 iftop -i eth0
```

---

## 4 验证与恢复

### 4.1 验证步骤

**步骤 1：验证 NFS 挂载选项**：

```bash
# 检查 NFS 挂载选项
kubectl exec -it app-pod-006 -n default -- mount | grep nfs

# 预期输出
nfs-server:/exports/pvc-xxx on /data type nfs (rw,relatime,vers=4,rsize=1048576,wsize=1048576,...)
```

**步骤 2：验证存储 I/O 性能**：

```bash
# 测试存储 I/O 性能
kubectl exec -it app-pod-006 -n default -- dd if=/dev/zero of=/data/test bs=1M count=1000

# 预期输出
1000+0 records in
1000+0 records out
1048576000 bytes (1.0 GB, 1000 MiB) copied, 10.0 s, 105 MB/s
```

**步骤 3：验证应用性能**：

```bash
# 测试应用性能
kubectl exec -it app-pod-006 -n default -- time curl http://localhost:8080/api/data

# 预期输出
real    0.100s
user    0.050s
sys     0.050s
```

**步骤 4：验证存储使用**：

```bash
# 检查存储使用
kubectl exec -it app-pod-006 -n default -- df -h /data

# 预期输出
Filesystem      Size  Used Avail Use% Mounted on
nfs-server:/exports/pvc-xxx  100G   50G   50G  50% /data
```

### 4.2 恢复确认

**恢复指标**：

- ✅ NFS 挂载选项：已优化
- ✅ 存储 I/O 性能：105 MB/s（从10.5 MB/s提升）
- ✅ 应用性能：正常
- ✅ 存储使用：正常

**恢复时间**：

- **故障发现**：00:00:00
- **开始排查**：00:00:05
- **根因确认**：00:05:00
- **问题解决**：00:10:00
- **服务恢复**：00:10:05
- **总耗时**：10 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **NFS 挂载选项影响性能**：
   - NFS 挂载选项 rsize 和 wsize 影响 I/O 性能
   - 需要优化挂载选项

2. **NFS 同步模式影响性能**：
   - 同步模式会降低写入性能
   - 需要根据需求选择同步/异步模式

3. **网络带宽影响性能**：
   - 网络带宽不足会影响存储性能
   - 需要确保网络带宽充足

### 5.2 最佳实践

1. **优化 NFS 挂载选项**：
   - 增加 rsize 和 wsize
   - 使用合适的 NFS 版本

2. **NFS 配置优化**：
   - 根据需求选择同步/异步模式
   - 优化 NFS 服务器配置

3. **存储性能监控**：
   - 定期检查存储 I/O 性能
   - 及时发现性能问题

4. **网络带宽管理**：
   - 确保网络带宽充足
   - 监控网络使用情况

### 5.3 相关文档

- [`../../TECHNICAL/04-storage/nfs/nfs.md`](../../TECHNICAL/04-storage/nfs/nfs.md) - NFS 文档
- [`../../TECHNICAL/04-storage/pvc/pvc.md`](../../TECHNICAL/04-storage/pvc/pvc.md) - PVC 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

## 6 相关文档

- [`../README.md`](README.md) - 故障排查案例集目录
- [`../../TECHNICAL/04-storage/nfs/nfs.md`](../../TECHNICAL/04-storage/nfs/nfs.md) - NFS 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
