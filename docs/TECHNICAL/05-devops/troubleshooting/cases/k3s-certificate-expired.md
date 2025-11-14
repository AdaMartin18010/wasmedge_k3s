# 案例 K-006：K3s 证书过期问题

> **案例编号**：K-006
> **故障类型**：证书过期故障
> **严重程度**：严重
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 K-006：K3s 证书过期问题](#案例-k-006k3s-证书过期问题)
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

- K3s API Server 无法访问
- 证书验证失败
- 日志显示：`x509: certificate has expired or is not yet valid`
- 集群功能完全不可用

**错误日志**：

```text
# K3s Server 日志
$ journalctl -u k3s -f

Nov 13 01:00:00 k3s-server-1 k3s[1234]: time="2025-11-13T01:00:00Z" level=error msg="Failed to start API server: x509: certificate has expired or is not yet valid"
Nov 13 01:00:00 k3s-server-1 k3s[1234]: time="2025-11-13T01:00:00Z" level=fatal msg="Failed to start K3s"
```

**时间线**：

- **01:00:00** - K3s 服务重启
- **01:00:05** - 证书验证失败
- **01:00:10** - API Server 启动失败
- **01:00:15** - 集群功能完全不可用

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **证书有效期**：1 年
- **证书过期时间**：2025-11-13
- **节点数量**：3 个

**证书信息**：

```bash
# 检查证书过期时间
$ openssl x509 -in /var/lib/rancher/k3s/server/tls/server-ca.crt -noout -dates

notBefore=Nov 13 00:00:00 2024 GMT
notAfter=Nov 13 00:00:00 2025 GMT
```

**K3s 配置**：

```bash
# K3s 服务配置
$ cat /etc/systemd/system/k3s.service

[Unit]
Description=Lightweight Kubernetes
After=network-online.target

[Service]
Type=notify
ExecStart=/usr/local/bin/k3s server
```

### 1.3 影响范围

- **受影响节点**：所有节点
- **受影响服务**：所有集群服务
- **业务影响**：集群完全不可用，影响生产环境
- **用户影响**：所有依赖集群的用户无法访问

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 K3s 服务状态**：

```bash
# 检查 K3s 服务状态
systemctl status k3s

# 输出
● k3s.service - Lightweight Kubernetes
   Loaded: loaded (/etc/systemd/system/k3s.service; enabled; vendor preset: enabled)
   Active: failed (Result: exit-code) since Mon 2025-11-13 01:00:00 UTC; 5min ago
```

**步骤 2：查看 K3s 日志**：

```bash
# 查看 K3s 日志
journalctl -u k3s -n 50

# 输出
Nov 13 01:00:00 k3s-server-1 k3s[1234]: time="2025-11-13T01:00:00Z" level=error msg="Failed to start API server: x509: certificate has expired or is not yet valid"
```

**步骤 3：检查证书过期时间**：

```bash
# 检查证书过期时间
openssl x509 -in /var/lib/rancher/k3s/server/tls/server-ca.crt -noout -dates

# 输出
notBefore=Nov 13 00:00:00 2024 GMT
notAfter=Nov 13 00:00:00 2025 GMT
```

**初步结论**：

- K3s 服务启动失败
- 证书已过期（2025-11-13）
- 需要更新证书

### 2.2 深入排查

**步骤 4：检查所有证书**：

```bash
# 检查所有证书过期时间
for cert in /var/lib/rancher/k3s/server/tls/*.crt; do
  echo "Certificate: $(basename $cert)"
  openssl x509 -in "$cert" -noout -dates
  echo "---"
done

# 输出
Certificate: server-ca.crt
notBefore=Nov 13 00:00:00 2024 GMT
notAfter=Nov 13 00:00:00 2025 GMT
---
Certificate: client-ca.crt
notBefore=Nov 13 00:00:00 2024 GMT
notAfter=Nov 13 00:00:00 2025 GMT
---
Certificate: request-header-ca.crt
notBefore=Nov 13 00:00:00 2024 GMT
notAfter=Nov 13 00:00:00 2025 GMT
```

**步骤 5：检查证书自动续期配置**：

```bash
# 检查 K3s 配置
cat /etc/rancher/k3s/config.yaml

# 输出
（无证书自动续期配置）
```

**步骤 6：检查 K3s 版本**：

```bash
# 检查 K3s 版本
k3s --version

# 输出
k3s version v1.30.4+k3s1 (go version go1.21.5)
```

**步骤 7：检查证书目录权限**：

```bash
# 检查证书目录权限
ls -la /var/lib/rancher/k3s/server/tls/

# 输出
total 48
drwx------ 3 root root  4096 Nov 13 00:00 .
drwx------ 5 root root  4096 Nov 13 00:00 ..
-rw------- 1 root root  1234 Nov 13 00:00 server-ca.crt
-rw------- 1 root root  1234 Nov 13 00:00 client-ca.crt
-rw------- 1 root root  1234 Nov 13 00:00 request-header-ca.crt
```

**步骤 8：检查集群状态**：

```bash
# 检查集群状态
kubectl get nodes

# 输出
The connection to the server was lost: x509: certificate has expired or is not yet valid
```

**深入排查结论**：

- 所有证书已过期
- 证书自动续期未配置
- 需要手动更新证书

### 2.3 根因分析

**根因 1：证书过期**：

- K3s 证书有效期 1 年
- 证书已过期（2025-11-13）
- 导致 API Server 无法启动

**根因 2：证书自动续期未配置**：

- K3s 证书自动续期未配置
- 证书过期后无法自动更新
- 需要手动更新证书

**根因 3：证书监控缺失**：

- 没有证书过期监控
- 证书过期前未收到告警
- 导致证书过期后才发现问题

**根本原因**：

**证书过期和自动续期未配置**：K3s 证书已过期，且证书自动续期未配置，导致证书过期后无法自动更新，从而集群功能完全不可用。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：手动更新证书**：

```bash
# 备份旧证书
sudo cp -r /var/lib/rancher/k3s/server/tls /var/lib/rancher/k3s/server/tls.backup

# 删除旧证书
sudo rm -rf /var/lib/rancher/k3s/server/tls/*.crt
sudo rm -rf /var/lib/rancher/k3s/server/tls/*.key

# 重启 K3s（会自动生成新证书）
sudo systemctl restart k3s
```

**方案 2：使用 k3s-killall 重置**：

```bash
# 使用 k3s-killall 重置
sudo /usr/local/bin/k3s-killall.sh
sudo systemctl restart k3s
```

**方案 3：重新安装 K3s**：

```bash
# 重新安装 K3s
sudo /usr/local/bin/k3s-uninstall.sh
curl -sfL https://get.k3s.io | sh -s - server
```

**临时方案效果**：

- ✅ 可以快速恢复服务
- ⚠️ 但未解决根本问题
- ⚠️ 可能丢失配置

### 3.2 永久解决方案

**方案 1：配置证书自动续期**：

```yaml
# 配置 K3s 证书自动续期
apiVersion: v1
kind: ConfigMap
metadata:
  name: k3s-config
  namespace: kube-system
data:
  config.yaml: |
    # 证书自动续期配置
    certificate-rotation:
      enabled: true
      interval: 24h
      threshold: 7d
```

**方案 2：使用 cert-manager 管理证书**：

```yaml
# 安装 cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# 配置证书自动续期
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: k3s-server-cert
  namespace: kube-system
spec:
  secretName: k3s-server-cert
  issuerRef:
    name: selfsigned-issuer
    kind: Issuer
  dnsNames:
    - k3s-server
  duration: 8760h  # 1 年
  renewBefore: 720h  # 30 天前续期
```

**方案 3：配置证书监控**：

```yaml
# 配置证书监控
apiVersion: v1
kind: ConfigMap
metadata:
  name: certificate-monitor
data:
  monitor.sh: |
    #!/bin/bash
    CERT_FILE="/var/lib/rancher/k3s/server/tls/server-ca.crt"
    EXPIRY_DATE=$(openssl x509 -in "$CERT_FILE" -noout -enddate | cut -d= -f2)
    EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
    CURRENT_EPOCH=$(date +%s)
    DAYS_UNTIL_EXPIRY=$(( ($EXPIRY_EPOCH - $CURRENT_EPOCH) / 86400 ))

    if [ $DAYS_UNTIL_EXPIRY -lt 30 ]; then
      echo "Certificate expires in $DAYS_UNTIL_EXPIRY days"
      # 发送告警
    fi
```

**方案 4：定期证书检查脚本**：

```bash
# 创建证书检查脚本
#!/bin/bash
# /usr/local/bin/k3s-cert-check.sh

CERT_DIR="/var/lib/rancher/k3s/server/tls"
ALERT_DAYS=30

for cert in "$CERT_DIR"/*.crt; do
  if [ -f "$cert" ]; then
    EXPIRY_DATE=$(openssl x509 -in "$cert" -noout -enddate | cut -d= -f2)
    EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
    CURRENT_EPOCH=$(date +%s)
    DAYS_UNTIL_EXPIRY=$(( ($EXPIRY_EPOCH - $CURRENT_EPOCH) / 86400 ))

    if [ $DAYS_UNTIL_EXPIRY -lt $ALERT_DAYS ]; then
      echo "WARNING: Certificate $(basename $cert) expires in $DAYS_UNTIL_EXPIRY days"
      # 发送告警
    fi
  fi
done
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：证书自动续期配置**：

```yaml
# 配置证书自动续期
apiVersion: v1
kind: ConfigMap
metadata:
  name: k3s-config
data:
  config.yaml: |
    certificate-rotation:
      enabled: true
      interval: 24h
      threshold: 7d
```

**措施 2：证书监控告警**：

```bash
# 配置证书监控告警
# 添加到 cron
0 0 * * * /usr/local/bin/k3s-cert-check.sh
```

**措施 3：证书备份**：

```bash
# 定期备份证书
#!/bin/bash
# /usr/local/bin/k3s-cert-backup.sh

BACKUP_DIR="/backup/k3s-certificates"
DATE=$(date +%Y%m%d)

mkdir -p "$BACKUP_DIR/$DATE"
cp -r /var/lib/rancher/k3s/server/tls "$BACKUP_DIR/$DATE/"
```

**措施 4：证书更新文档**：

```markdown
# 证书更新流程文档
1. 检查证书过期时间
2. 备份当前证书
3. 更新证书
4. 验证证书有效性
5. 重启 K3s 服务
```

---

## 4 验证与恢复

### 4.1 验证步骤

**步骤 1：验证证书有效期**：

```bash
# 检查证书过期时间
openssl x509 -in /var/lib/rancher/k3s/server/tls/server-ca.crt -noout -dates

# 预期输出
notBefore=Nov 13 00:00:00 2025 GMT
notAfter=Nov 13 00:00:00 2026 GMT
```

**步骤 2：验证 K3s 服务状态**：

```bash
# 检查 K3s 服务状态
systemctl status k3s

# 预期输出
● k3s.service - Lightweight Kubernetes
   Loaded: loaded (/etc/systemd/system/k3s.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2025-11-13 01:10:00 UTC; 5min ago
```

**步骤 3：验证集群状态**：

```bash
# 检查集群状态
kubectl get nodes

# 预期输出
NAME           STATUS   ROLES                  AGE   VERSION
k3s-server-1   Ready    control-plane,master   5d    v1.30.4+k3s1
k3s-worker-1   Ready    <none>                 5d    v1.30.4+k3s1
k3s-worker-2   Ready    <none>                 5d    v1.30.4+k3s1
```

**步骤 4：验证 API Server 访问**：

```bash
# 测试 API Server 访问
kubectl get pods -A

# 预期输出
NAMESPACE     NAME                                     READY   STATUS    RESTARTS   AGE
kube-system   coredns-xxx                             1/1     Running   0          5d
kube-system   traefik-xxx                             1/1     Running   0          5d
```

### 4.2 恢复确认

**恢复指标**：

- ✅ 证书有效期：已更新（2026-11-13）
- ✅ K3s 服务状态：运行正常
- ✅ 集群状态：正常
- ✅ API Server 访问：正常

**恢复时间**：

- **故障发现**：01:00:00
- **开始排查**：01:00:05
- **根因确认**：01:05:00
- **问题解决**：01:10:00
- **服务恢复**：01:10:05
- **总耗时**：10 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **证书过期会导致集群完全不可用**：
   - K3s 证书过期会导致 API Server 无法启动
   - 需要定期检查证书有效期

2. **证书自动续期重要**：
   - 证书自动续期可以防止证书过期
   - 需要配置证书自动续期

3. **证书监控必要**：
   - 证书监控可以提前发现证书过期问题
   - 需要配置证书监控告警

### 5.2 最佳实践

1. **配置证书自动续期**：
   - 启用证书自动续期功能
   - 设置合适的续期阈值

2. **证书监控告警**：
   - 配置证书过期监控
   - 提前 30 天发送告警

3. **证书备份**：
   - 定期备份证书
   - 防止证书丢失

4. **证书更新流程**：
   - 建立证书更新流程文档
   - 确保证书更新标准化

### 5.3 相关文档

- [`../../TECHNICAL/01-core-foundations/k3s/k3s.md`](../../TECHNICAL/01-core-foundations/k3s/k3s.md) - K3s 文档
- [`../../TECHNICAL/06-security/certificates/certificates.md`](../../TECHNICAL/06-security/certificates/certificates.md) - 证书文档
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
