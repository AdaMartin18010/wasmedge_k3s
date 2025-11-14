# 案例 K-001：K3s 节点无法加入集群

> **案例编号**：K-001
> **故障类型**：启动失败
> **严重程度**：严重
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 K-001：K3s 节点无法加入集群](#案例-k-001k3s-节点无法加入集群)
  - [📑 目录](#-目录)
  - [1 故障描述](#1-故障描述)
    - [1.1 现象](#11-现象)
    - [1.2 影响范围](#12-影响范围)
    - [1.3 发生时间](#13-发生时间)
  - [2 环境信息](#2-环境信息)
    - [2.1 软件版本](#21-软件版本)
    - [2.2 硬件配置](#22-硬件配置)
    - [2.3 部署配置](#23-部署配置)
  - [3 排查过程](#3-排查过程)
    - [3.1 初步诊断](#31-初步诊断)
    - [3.2 深入分析](#32-深入分析)
    - [3.3 根因定位](#33-根因定位)
  - [4 根因分析](#4-根因分析)
    - [4.1 技术根因](#41-技术根因)
    - [4.2 配置根因](#42-配置根因)
  - [5 解决方案](#5-解决方案)
    - [5.1 临时方案](#51-临时方案)
    - [5.2 根本方案](#52-根本方案)
    - [5.3 预防措施](#53-预防措施)
  - [6 验证结果](#6-验证结果)
    - [6.1 验证方法](#61-验证方法)
    - [6.2 验证结果](#62-验证结果)
    - [6.3 验证时间](#63-验证时间)
  - [7 经验总结](#7-经验总结)
    - [7.1 关键教训](#71-关键教训)
    - [7.2 最佳实践](#72-最佳实践)
    - [7.3 相关文档](#73-相关文档)
  - [8 相关文档](#8-相关文档)

---

## 1 故障描述

### 1.1 现象

**故障现象**：

```bash
$ kubectl get nodes
NAME           STATUS     ROLES                  AGE   VERSION
k3s-server-1   Ready      control-plane,master   5d    v1.30.4+k3s1
# Agent 节点未显示

$ kubectl get nodes -o wide
NAME           STATUS     ROLES                  AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE
k3s-server-1   Ready      control-plane,master   5d    v1.30.4+k3s1   10.0.1.10      <none>        Ubuntu 22.04
# 只有 Server 节点，Agent 节点未加入
```

**在 Agent 节点上的错误日志**：

```bash
$ journalctl -u k3s-agent -f
Nov 11 10:30:15 edge-node-1 k3s-agent[1234]: time="2025-11-11T10:30:15Z" level=error msg="Failed to join cluster: failed to get node-token: Get \"https://10.0.1.10:6443/v1-k3s/node-token\": dial tcp 10.0.1.10:6443: connect: connection refused"
Nov 11 10:30:15 edge-node-1 k3s-agent[1234]: time="2025-11-11T10:30:15Z" level=fatal msg="failed to join cluster"
```

**实际表现**：

- Agent 节点无法加入 K3s 集群
- 日志显示连接被拒绝（connection refused）
- 节点状态一直为 `NotReady`
- 无法在 Agent 节点上部署 Pod

### 1.2 影响范围

- **受影响节点**：所有 Agent 节点
- **受影响服务**：所有需要在 Agent 节点上运行的服务
- **业务影响**：无法扩展集群，影响服务部署和负载均衡

### 1.3 发生时间

- **首次发现**：2025-11-11 10:15
- **持续时间**：约 1.5 小时
- **解决时间**：2025-11-11 11:45

---

## 2 环境信息

### 2.1 软件版本

- **K3s Server 版本**：v1.30.4+k3s1
- **K3s Agent 版本**：v1.30.4+k3s1
- **Kubernetes 版本**：v1.30.4
- **操作系统**：Ubuntu 22.04 LTS
- **内核版本**：5.15.0-91-generic

### 2.2 硬件配置

**Server 节点**：

- **节点类型**：控制平面节点
- **CPU**：4 核 x86_64
- **内存**：8GB RAM
- **存储**：100GB SSD
- **网络**：1Gbps

**Agent 节点**：

- **节点类型**：边缘节点
- **CPU**：4 核 ARM64
- **内存**：2GB RAM
- **存储**：32GB eMMC
- **网络**：1Gbps

### 2.3 部署配置

**Server 节点配置**：

```bash
# Server 节点安装命令
curl -sfL https://get.k3s.io | sh -s - server \
  --cluster-init \
  --tls-san 10.0.1.10 \
  --bind-address 10.0.1.10
```

**Agent 节点配置**：

```bash
# Agent 节点安装命令
curl -sfL https://get.k3s.io | K3S_URL=https://10.0.1.10:6443 \
  K3S_TOKEN=xxx sh -s - agent
```

---

## 3 排查过程

### 3.1 初步诊断

**步骤 1：检查节点状态**:

```bash
# 在 Server 节点检查
$ kubectl get nodes
NAME           STATUS     ROLES                  AGE   VERSION
k3s-server-1   Ready      control-plane,master   5d    v1.30.4+k3s1
# Agent 节点未显示
```

**步骤 2：检查 Agent 节点服务状态**:

```bash
# 在 Agent 节点检查
$ systemctl status k3s-agent
● k3s-agent.service - Lightweight Kubernetes
   Loaded: loaded (/etc/systemd/system/k3s-agent.service; enabled; vendor preset: enabled)
   Active: failed (Result: exit-code) since Mon 2025-11-11 10:30:15 UTC; 5min ago
   Main PID: 1234 (code=exited, status=1/FAILURE)
```

**步骤 3：查看 Agent 节点日志**:

```bash
$ journalctl -u k3s-agent -n 50
Nov 11 10:30:15 edge-node-1 k3s-agent[1234]: time="2025-11-11T10:30:15Z" level=error msg="Failed to join cluster: failed to get node-token: Get \"https://10.0.1.10:6443/v1-k3s/node-token\": dial tcp 10.0.1.10:6443: connect: connection refused"
```

**初步结论**：Agent 节点无法连接到 Server 节点的 6443 端口，连接被拒绝。

### 3.2 深入分析

**步骤 1：检查网络连通性**:

```bash
# 在 Agent 节点测试网络连通性
$ ping 10.0.1.10
PING 10.0.1.10 (10.0.1.10) 56(84) bytes of data.
64 bytes from 10.0.1.10: icmp_seq=1 ttl=64 time=0.5ms
# 网络连通正常

$ telnet 10.0.1.10 6443
Trying 10.0.1.10...
telnet: Unable to connect to remote host: Connection refused
# 端口 6443 连接被拒绝
```

**步骤 2：检查 Server 节点防火墙**:

```bash
# 在 Server 节点检查防火墙
$ sudo ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
6443/tcp                   DENY        Anywhere  # 问题：6443 端口被拒绝
```

**步骤 3：检查 Server 节点 K3s 服务**:

```bash
# 在 Server 节点检查 K3s 服务
$ sudo systemctl status k3s
● k3s.service - Lightweight Kubernetes
   Loaded: loaded (/etc/systemd/system/k3s.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2025-11-11 08:00:00 UTC; 2h 30min ago
   Main PID: 5678 (k3s-server)
   # 服务运行正常

$ sudo netstat -tlnp | grep 6443
tcp6       0      0 127.0.0.1:6443          :::*                    LISTEN      5678/k3s-server
# 问题：只监听 127.0.0.1，未监听 10.0.1.10
```

**深入分析结论**：

1. Server 节点防火墙阻止了 6443 端口的访问
2. K3s Server 只监听 127.0.0.1，未监听 10.0.1.10
3. Agent 节点无法连接到 Server 节点的 API Server

### 3.3 根因定位

**根因 1：防火墙配置错误**:

- Server 节点防火墙（ufw）阻止了 6443 端口的访问
- 防火墙规则配置为 `DENY`，导致 Agent 节点无法连接

**根因 2：K3s Server 绑定地址配置错误**:

- K3s Server 使用 `--bind-address 10.0.1.10`，但实际只监听 127.0.0.1
- 可能是网络接口配置问题或 K3s 配置问题

**根因 3：Token 验证问题**:

- Agent 节点使用的 Token 可能已过期或无效
- Token 文件权限可能不正确

---

## 4 根因分析

### 4.1 技术根因

**防火墙问题**：

1. **ufw 默认策略**：ufw 默认拒绝所有入站连接
2. **6443 端口规则**：6443 端口被明确拒绝，而非允许
3. **网络接口绑定**：K3s Server 可能未正确绑定到网络接口

**K3s 配置问题**：

1. **绑定地址**：`--bind-address` 参数可能未生效
2. **网络接口**：网络接口可能未正确配置
3. **TLS SAN**：TLS SAN 配置可能不完整

### 4.2 配置根因

**防火墙配置错误**：

```bash
# ❌ 错误配置：拒绝 6443 端口
$ sudo ufw deny 6443/tcp

# ✅ 正确配置：允许 6443 端口
$ sudo ufw allow 6443/tcp
```

**K3s Server 配置问题**：

```bash
# ❌ 问题配置：绑定地址可能未生效
curl -sfL https://get.k3s.io | sh -s - server \
  --bind-address 10.0.1.10

# ✅ 正确配置：明确指定所有必要的网络参数
curl -sfL https://get.k3s.io | sh -s - server \
  --cluster-init \
  --tls-san 10.0.1.10 \
  --bind-address 0.0.0.0 \
  --advertise-address 10.0.1.10
```

---

## 5 解决方案

### 5.1 临时方案

**方案 1：开放防火墙端口**:

```bash
# 在 Server 节点开放 6443 端口
sudo ufw allow 6443/tcp
sudo ufw reload

# 验证防火墙规则
sudo ufw status | grep 6443
# 应该显示：6443/tcp                     ALLOW       Anywhere
```

**方案 2：临时禁用防火墙（不推荐）**:

```bash
# 仅在紧急情况下使用
sudo ufw disable
```

### 5.2 根本方案

**方案 1：正确配置防火墙**:

```bash
# 在 Server 节点配置防火墙规则
sudo ufw allow 6443/tcp comment 'K3s API Server'
sudo ufw allow 10250/tcp comment 'K3s Kubelet'
sudo ufw allow 8472/udp comment 'K3s Flannel VXLAN'
sudo ufw allow 51820/udp comment 'K3s Flannel Wireguard'
sudo ufw reload

# 验证防火墙规则
sudo ufw status numbered
```

**方案 2：重新配置 K3s Server**:

```bash
# 停止 K3s Server
sudo systemctl stop k3s

# 备份现有配置
sudo cp /etc/rancher/k3s/k3s.yaml /etc/rancher/k3s/k3s.yaml.bak

# 重新安装 K3s Server（使用正确配置）
curl -sfL https://get.k3s.io | sh -s - server \
  --cluster-init \
  --tls-san 10.0.1.10 \
  --bind-address 0.0.0.0 \
  --advertise-address 10.0.1.10 \
  --node-ip 10.0.1.10

# 验证 K3s Server 监听地址
sudo netstat -tlnp | grep 6443
# 应该显示：tcp6       0      0 :::6443          :::*                    LISTEN
```

**方案 3：更新 Agent 节点配置**:

```bash
# 获取新的 Token（在 Server 节点）
sudo cat /var/lib/rancher/k3s/server/node-token

# 在 Agent 节点重新加入集群
sudo systemctl stop k3s-agent
sudo rm -rf /var/lib/rancher/k3s/agent

curl -sfL https://get.k3s.io | K3S_URL=https://10.0.1.10:6443 \
  K3S_TOKEN=<new-token> sh -s - agent \
  --node-ip <agent-node-ip>
```

### 5.3 预防措施

1. **建立防火墙配置模板**：
   - 记录 K3s 所需的所有端口
   - 提供防火墙配置脚本

2. **验证网络配置**：
   - 在安装前验证网络连通性
   - 验证端口是否可访问

3. **监控和告警**：
   - 监控节点加入状态
   - 当节点无法加入时发送告警

4. **文档化最佳实践**：
   - 记录 K3s 安装和配置的最佳实践
   - 提供故障排查指南

---

## 6 验证结果

### 6.1 验证方法

**步骤 1：应用解决方案**:

```bash
# 在 Server 节点开放防火墙
sudo ufw allow 6443/tcp
sudo ufw reload

# 重新配置 K3s Server（如果需要）
sudo systemctl restart k3s
```

**步骤 2：验证 Server 节点监听**:

```bash
# 在 Server 节点检查
$ sudo netstat -tlnp | grep 6443
tcp6       0      0 :::6443          :::*                    LISTEN      5678/k3s-server
# ✅ 现在监听所有接口
```

**步骤 3：在 Agent 节点重新加入**:

```bash
# 在 Agent 节点
curl -sfL https://get.k3s.io | K3S_URL=https://10.0.1.10:6443 \
  K3S_TOKEN=<correct-token> sh -s - agent
```

**步骤 4：验证节点状态**:

```bash
# 在 Server 节点检查
$ kubectl get nodes
NAME           STATUS   ROLES                  AGE   VERSION
k3s-server-1   Ready    control-plane,master   5d    v1.30.4+k3s1
edge-node-1    Ready    <none>                 30s   v1.30.4+k3s1
# ✅ Agent 节点成功加入
```

### 6.2 验证结果

- ✅ **节点状态**：Agent 节点状态为 `Ready`
- ✅ **网络连通性**：Agent 节点可以连接到 Server 节点
- ✅ **API 访问**：Agent 节点可以访问 K3s API Server
- ✅ **Pod 调度**：可以在 Agent 节点上调度 Pod

### 6.3 验证时间

- **验证时间**：2025-11-11 11:45
- **验证人员**：运维团队
- **验证环境**：生产环境

---

## 7 经验总结

### 7.1 关键教训

1. **防火墙配置很重要**：
   - K3s 需要多个端口开放（6443、10250、8472、51820 等）
   - 防火墙配置错误会导致节点无法加入集群

2. **网络绑定地址需要正确配置**：
   - K3s Server 需要监听正确的网络接口
   - 使用 `0.0.0.0` 监听所有接口，或明确指定 IP 地址

3. **Token 管理很重要**：
   - Token 需要正确配置和保存
   - Token 文件权限需要正确设置

### 7.2 最佳实践

1. **防火墙配置**：
   - 开放 K3s 所需的所有端口
   - 使用注释说明每个端口的用途
   - 定期审查防火墙规则

2. **K3s Server 配置**：
   - 使用 `--bind-address 0.0.0.0` 监听所有接口
   - 使用 `--advertise-address` 指定对外 IP
   - 使用 `--tls-san` 添加 TLS SAN

3. **网络验证**：
   - 在安装前验证网络连通性
   - 验证端口是否可访问
   - 使用 `telnet` 或 `nc` 测试端口

4. **文档化**：
   - 记录 K3s 安装和配置步骤
   - 提供防火墙配置模板
   - 提供故障排查指南

### 7.3 相关文档

- [`../troubleshooting.md`](../troubleshooting.md#1131-节点无法加入) - 故障排查指南
- [`../../../../TECHNICAL/01-core-foundations/k3s/k3s.md`](../../../../TECHNICAL/01-core-foundations/k3s/k3s.md) - K3s 文档
- [`../../PRACTICAL-CASE-SUPPLEMENT-PLAN.md`](../../PRACTICAL-CASE-SUPPLEMENT-PLAN.md) - 实践案例补充计划

---

## 8 相关文档

- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南
- [`../cases/README.md`](README.md) - 案例集目录
- [`../../../../TECHNICAL/01-core-foundations/k3s/k3s.md`](../../../../TECHNICAL/01-core-foundations/k3s/k3s.md) - K3s 文档

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
