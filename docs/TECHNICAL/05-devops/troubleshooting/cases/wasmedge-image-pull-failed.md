# 案例 W-007：Wasm 镜像拉取失败

> **案例编号**：W-007
> **故障类型**：镜像拉取故障
> **严重程度**：中等
> **创建日期**：2025-11-15
> **最后更新**：2025-11-15

---

## 📑 目录

- [案例 W-007：Wasm 镜像拉取失败](#案例-w-007wasm-镜像拉取失败)
  - [📑 目录](#-目录)
  - [1. 问题描述](#1-问题描述)
    - [1.1 故障现象](#11-故障现象)
    - [1.2 环境信息](#12-环境信息)
    - [1.3 影响范围](#13-影响范围)
  - [2. 故障排查过程](#2-故障排查过程)
    - [2.1 初步诊断](#21-初步诊断)
    - [2.2 深入排查](#22-深入排查)
    - [2.3 根因分析](#23-根因分析)
  - [3. 解决方案](#3-解决方案)
    - [3.1 临时解决方案](#31-临时解决方案)
    - [3.2 永久解决方案](#32-永久解决方案)
    - [3.3 预防措施](#33-预防措施)
  - [4. 验证与恢复](#4-验证与恢复)
    - [4.1 验证步骤](#41-验证步骤)
    - [4.2 恢复确认](#42-恢复确认)
  - [5. 经验总结](#5-经验总结)
    - [5.1 关键发现](#51-关键发现)
    - [5.2 最佳实践](#52-最佳实践)
    - [5.3 相关文档](#53-相关文档)
  - [6. 相关文档](#6-相关文档)

---

## 1. 问题描述

### 1.1 故障现象

**主要症状**：

- Wasm Pod 无法拉取镜像
- Pod 状态一直处于 `ImagePullBackOff` 或 `ErrImagePull`
- 日志显示：`Failed to pull image "myregistry.com/wasm-app:v1.0.0"`
- 错误信息：`Error response from daemon: pull access denied`

**错误日志**：

```text
2025-11-15T18:00:00.123Z ERROR [kubelet] Failed to pull image "myregistry.com/wasm-app:v1.0.0"
2025-11-15T18:00:00.124Z ERROR [kubelet] Error response from daemon: pull access denied, repository does not exist or may require 'docker login'
2025-11-15T18:00:05.456Z ERROR [kubelet] Back-off pulling image "myregistry.com/wasm-app:v1.0.0"
```

**时间线**：

- **18:00:00** - Pod 创建，开始拉取镜像
- **18:00:05** - 镜像拉取失败，Pod 进入 `ImagePullBackOff` 状态
- **18:00:10** - 重试拉取，仍然失败
- **18:00:15** - Pod 状态持续为 `ImagePullBackOff`

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **containerd 版本**：v1.7.1
- **镜像仓库**：私有镜像仓库

**应用配置**：

- **Runtime**：WasmEdge
- **镜像地址**：myregistry.com/wasm-app:v1.0.0
- **镜像类型**：Wasm 镜像（OCI Artifact）

**Pod 信息**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-image-001
  namespace: default
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: myregistry.com/wasm-app:v1.0.0
      imagePullPolicy: Always
```

### 1.3 影响范围

- **受影响 Pod**：1 个（wasm-app-image-001）
- **受影响服务**：Wasm 应用服务
- **业务影响**：应用无法启动，服务完全不可用
- **用户影响**：所有依赖该服务的用户无法访问

---

## 2. 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 Pod 状态**：

```bash
# 检查 Pod 状态
kubectl get pod wasm-app-image-001 -n default

# 输出
NAME                  READY   STATUS             RESTARTS   AGE
wasm-app-image-001    0/1     ImagePullBackOff   0          5m
```

**步骤 2：查看 Pod 事件**：

```bash
# 查看 Pod 事件
kubectl describe pod wasm-app-image-001 -n default

# 输出显示镜像拉取失败
Events:
  Warning  Failed     5m ago   kubelet  Failed to pull image "myregistry.com/wasm-app:v1.0.0"
  Warning  Failed     5m ago   kubelet  Error response from daemon: pull access denied
```

**步骤 3：检查镜像是否存在**：

```bash
# 尝试手动拉取镜像
crictl pull myregistry.com/wasm-app:v1.0.0

# 输出
FATA[0000] pulling image failed: rpc error: code = Unknown desc = failed to pull and unpack image
```

**初步结论**：

- Pod 状态为 `ImagePullBackOff`
- 镜像拉取失败，可能是认证问题或镜像不存在

### 2.2 深入排查

**步骤 4：检查镜像仓库认证**：

```bash
# 检查 containerd 配置
cat /etc/containerd/config.toml | grep -A 10 "registry"

# 检查镜像仓库认证配置
cat /var/lib/rancher/k3s/agent/etc/containerd/config.toml | grep -A 10 "myregistry.com"
```

**步骤 5：检查镜像仓库连接**：

```bash
# 测试镜像仓库连接
curl -I https://myregistry.com/v2/

# 输出
HTTP/1.1 401 Unauthorized
```

**步骤 6：检查镜像标签**：

```bash
# 检查镜像是否存在
curl -u username:password https://myregistry.com/v2/wasm-app/manifests/v1.0.0

# 输出
404 Not Found
```

**步骤 7：检查 Wasm 镜像格式**：

```bash
# 检查镜像是否为 Wasm 格式
crictl image inspect myregistry.com/wasm-app:v1.0.0

# 输出显示镜像格式不支持
```

**深入排查结论**：

- 镜像仓库需要认证，但未配置认证信息
- 镜像标签不存在或已被删除
- Wasm 镜像格式可能不被支持

### 2.3 根因分析

**根因 1：镜像仓库认证缺失**：

- 私有镜像仓库需要认证，但 K3s 节点未配置认证信息
- containerd 无法通过认证拉取镜像

**根因 2：镜像不存在**：

- 镜像标签 `v1.0.0` 不存在或已被删除
- 镜像仓库中只有其他版本的镜像

**根因 3：Wasm 镜像格式不支持**：

- containerd 可能不支持 Wasm OCI Artifact 格式
- 需要配置 containerd 支持 Wasm 镜像

**根因 4：网络连接问题**：

- 节点无法访问镜像仓库
- 防火墙或网络策略阻止了连接

**根本原因**：

**镜像仓库认证配置缺失和镜像不存在**：私有镜像仓库需要认证，但 K3s 节点未配置认证信息，且镜像标签可能不存在。

---

## 3. 解决方案

### 3.1 临时解决方案

**方案 1：使用公共镜像**：

```yaml
# 临时使用公共镜像
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-image-001
  namespace: default
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: wasmedge/example-app:latest  # 使用公共镜像
```

**方案 2：手动拉取镜像**：

```bash
# 在节点上手动拉取镜像
docker login myregistry.com
docker pull myregistry.com/wasm-app:v1.0.0
```

**临时方案效果**：

- ✅ 可以快速恢复服务
- ⚠️ 但未解决根本问题
- ⚠️ 可能再次出现相同问题

### 3.2 永久解决方案

**方案 1：配置镜像仓库认证**：

```bash
# 创建镜像仓库认证 Secret
kubectl create secret docker-registry regcred \
  --docker-server=myregistry.com \
  --docker-username=username \
  --docker-password=password \
  --docker-email=user@example.com \
  -n default

# 在 Pod 中使用 Secret
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-image-001
  namespace: default
spec:
  runtimeClassName: wasm
  imagePullSecrets:
    - name: regcred
  containers:
    - name: wasm-app
      image: myregistry.com/wasm-app:v1.0.0
```

**方案 2：配置 containerd 镜像仓库认证**：

```bash
# 创建 containerd 认证配置
mkdir -p /var/lib/rancher/k3s/agent/etc/containerd/registry.d/myregistry.com
cat > /var/lib/rancher/k3s/agent/etc/containerd/registry.d/myregistry.com/config.toml <<EOF
[host."https://myregistry.com"]
  capabilities = ["pull", "resolve"]
  skip_verify = false
  [host."https://myregistry.com".tls]
    insecure_skip_verify = false
EOF

# 创建认证文件
cat > /var/lib/rancher/k3s/agent/etc/containerd/registry.d/myregistry.com/auth.toml <<EOF
[host."https://myregistry.com"]
  username = "username"
  password = "password"
EOF

# 重启 containerd
systemctl restart containerd
```

**方案 3：检查并修复镜像标签**：

```bash
# 检查镜像仓库中的可用标签
curl -u username:password https://myregistry.com/v2/wasm-app/tags/list

# 输出
{"name":"wasm-app","tags":["v1.0.1","v1.0.2","latest"]}

# 使用存在的标签
apiVersion: v1
kind: Pod
metadata:
  name: wasm-app-image-001
  namespace: default
spec:
  runtimeClassName: wasm
  containers:
    - name: wasm-app
      image: myregistry.com/wasm-app:v1.0.1  # 使用存在的标签
```

**方案 4：配置 Wasm 镜像支持**：

```bash
# 配置 containerd 支持 Wasm OCI Artifact
cat >> /var/lib/rancher/k3s/agent/etc/containerd/config.toml <<EOF
[plugins."io.containerd.grpc.v1.cri".registry]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."myregistry.com"]
      endpoint = ["https://myregistry.com"]
  [plugins."io.containerd.grpc.v1.cri".registry.configs."myregistry.com".tls]
    insecure_skip_verify = false
EOF

# 重启 containerd
systemctl restart containerd
```

### 3.3 预防措施

1. **镜像管理**：
   - 使用镜像标签管理版本
   - 定期清理旧版本镜像
   - 使用镜像签名确保完整性

2. **认证管理**：
   - 使用 Secret 管理镜像仓库认证
   - 定期更新认证信息
   - 使用 ServiceAccount 统一管理

3. **镜像验证**：
   - 在部署前验证镜像是否存在
   - 使用镜像扫描工具检查镜像
   - 配置镜像拉取策略

4. **监控告警**：
   - 监控镜像拉取失败事件
   - 配置告警及时发现问题
   - 定期检查镜像仓库状态

---

## 4. 验证与恢复

### 4.1 验证步骤

**步骤 1：验证镜像拉取**：

```bash
# 检查 Pod 状态
kubectl get pod wasm-app-image-001 -n default

# 应该看到 Pod 状态为 Running
```

**步骤 2：验证镜像存在**：

```bash
# 检查节点上的镜像
crictl images | grep wasm-app

# 应该看到镜像已拉取
```

**步骤 3：验证认证配置**：

```bash
# 检查认证配置
kubectl get secret regcred -n default

# 应该看到 Secret 存在
```

### 4.2 恢复确认

**恢复时间线**：

- **故障发现**：18:00:00
- **开始排查**：18:00:05
- **根因确认**：18:10:00
- **问题解决**：18:15:00
- **服务恢复**：18:15:05
- **总耗时**：15 分钟

**恢复验证**：

- ✅ 镜像成功拉取
- ✅ Pod 状态为 Running
- ✅ 应用正常启动
- ✅ 服务可用性恢复

---

## 5. 经验总结

### 5.1 关键发现

1. **镜像仓库认证至关重要**：
   - 私有镜像仓库必须配置认证
   - 可以使用 Secret 或 containerd 配置

2. **镜像标签管理**：
   - 确保使用的镜像标签存在
   - 使用语义化版本管理镜像

3. **Wasm 镜像格式**：
   - Wasm 镜像使用 OCI Artifact 格式
   - 需要确保 containerd 支持该格式

4. **网络连接**：
   - 确保节点可以访问镜像仓库
   - 检查防火墙和网络策略

### 5.2 最佳实践

1. **镜像管理**：
   - 使用镜像仓库管理镜像
   - 使用标签管理版本
   - 定期清理旧版本

2. **认证管理**：
   - 使用 Secret 管理认证信息
   - 使用 ServiceAccount 统一管理
   - 定期更新认证信息

3. **镜像验证**：
   - 在部署前验证镜像
   - 使用镜像扫描工具
   - 配置镜像拉取策略

4. **监控告警**：
   - 监控镜像拉取事件
   - 配置告警规则
   - 定期检查镜像仓库

### 5.3 相关文档

- [`../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md`](../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md) - WasmEdge 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南
- [Kubernetes 镜像拉取文档](https://kubernetes.io/docs/concepts/containers/images/) - K8s 镜像管理

---

## 6. 相关文档

- [`../README.md`](README.md) - 故障排查案例集目录
- [`../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md`](../../TECHNICAL/01-core-foundations/wasmedge/wasmedge.md) - WasmEdge 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

**最后更新**：2025-11-15
**维护者**：项目团队
**版本**：v1.0
