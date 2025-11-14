# 案例 N-001：Pod 跨节点通信失败

> **案例编号**：N-001
> **故障类型**：网络通信故障
> **严重程度**：严重
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 N-001：Pod 跨节点通信失败](#案例-n-001pod-跨节点通信失败)
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

- Pod 无法与其他节点上的 Pod 通信
- 同节点 Pod 之间通信正常
- 跨节点 Pod 之间通信失败
- 网络连接超时或连接被拒绝

**错误日志**：

```text
# Pod A (节点1) 尝试连接 Pod B (节点2)
$ kubectl exec -it pod-a -- ping pod-b-ip

PING pod-b-ip (10.42.2.10) 56(84) bytes of data.
^C
--- pod-b-ip ping statistics ---
5 packets transmitted, 0 received, 100% packet loss, time 4000ms
```

**时间线**：

- **17:00:00** - 发现跨节点通信问题
- **17:00:05** - 开始排查网络问题
- **17:00:10** - 确认跨节点通信失败
- **17:05:00** - 定位到 CNI 插件问题

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **CNI 插件**：flannel
- **网络模式**：VXLAN
- **节点数量**：3 个

**节点信息**：

```bash
# 节点列表
$ kubectl get nodes -o wide

NAME           STATUS   ROLES                  AGE   VERSION   INTERNAL-IP     EXTERNAL-IP
k3s-server-1   Ready    control-plane,master   5d    v1.30.4   10.0.1.10       <none>
k3s-worker-1   Ready    <none>                 5d    v1.30.4   10.0.1.11       <none>
k3s-worker-2   Ready    <none>                 5d    v1.30.4   10.0.1.12       <none>
```

**Pod 信息**：

```bash
# Pod 分布
$ kubectl get pods -o wide

NAME       READY   STATUS    RESTARTS   AGE   IP           NODE
pod-a      1/1     Running   0          1h    10.42.1.10   k3s-server-1
pod-b      1/1     Running   0          1h    10.42.2.10   k3s-worker-1
pod-c      1/1     Running   0          1h    10.42.3.10   k3s-worker-2
```

### 1.3 影响范围

- **受影响 Pod**：所有跨节点 Pod
- **受影响服务**：所有需要跨节点通信的服务
- **业务影响**：服务间通信失败，影响生产环境
- **用户影响**：所有依赖跨节点通信的用户

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：测试同节点 Pod 通信**：

```bash
# 在同一节点创建测试 Pod
kubectl run test-pod-1 --image=busybox --overrides='{"spec":{"nodeName":"k3s-server-1"}}' -- sleep 3600
kubectl run test-pod-2 --image=busybox --overrides='{"spec":{"nodeName":"k3s-server-1"}}' -- sleep 3600

# 测试通信
kubectl exec -it test-pod-1 -- ping -c 3 test-pod-2-ip

# 输出
PING test-pod-2-ip (10.42.1.11) 56(84) bytes of data.
64 bytes from 10.42.1.11: icmp_seq=1 time=0.123 ms
64 bytes from 10.42.1.11: icmp_seq=2 time=0.145 ms
64 bytes from 10.42.1.11: icmp_seq=3 time=0.134 ms
```

**步骤 2：测试跨节点 Pod 通信**：

```bash
# 测试跨节点通信
kubectl exec -it pod-a -- ping -c 3 10.42.2.10

# 输出
PING 10.42.2.10 (10.42.2.10) 56(84) bytes of data.
^C
--- 10.42.2.10 ping statistics ---
3 packets transmitted, 0 received, 100% packet loss, time 2000ms
```

**步骤 3：检查节点网络**：

```bash
# 检查节点网络接口
kubectl exec -it pod-a -- ip addr show

# 输出
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    inet 127.0.0.1/8 scope host lo
3: eth0@if4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP
    inet 10.42.1.10/24 scope global eth0
```

**初步结论**：

- 同节点 Pod 通信正常
- 跨节点 Pod 通信失败
- 需要检查 CNI 插件和网络路由

### 2.2 深入排查

**步骤 4：检查 flannel 状态**：

```bash
# 检查 flannel Pod
kubectl get pod -n kube-system | grep flannel

# 输出
kube-flannel-ds-xxx   1/1     Running   0          5d
```

**步骤 5：检查 flannel 配置**：

```bash
# 检查 flannel ConfigMap
kubectl get configmap -n kube-system kube-flannel-cfg -o yaml

# 输出
apiVersion: v1
kind: ConfigMap
data:
  cni-conf.json: |
    {
      "name": "cbr0",
      "type": "flannel",
      "delegate": {
        "isDefaultGateway": true
      }
    }
  net-conf.json: |
    {
      "Network": "10.42.0.0/16",
      "Backend": {
        "Type": "vxlan"
      }
    }
```

**步骤 6：检查节点路由**：

```bash
# 在节点上检查路由
ip route show

# 输出
default via 10.0.1.1 dev eth0
10.42.1.0/24 dev cni0 proto kernel scope link src 10.42.1.1
10.42.0.0/16 via 10.42.1.1 dev flannel.1 onlink
```

**步骤 7：检查 VXLAN 接口**：

```bash
# 检查 VXLAN 接口
ip link show flannel.1

# 输出
4: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN
    link/ether 02:42:0a:2a:01:01 brd ff:ff:ff:ff:ff:ff
```

**步骤 8：检查防火墙规则**：

```bash
# 检查防火墙规则
sudo iptables -L -n | grep -i flannel

# 输出
（无 flannel 相关规则）
```

**深入排查结论**：

- flannel Pod 运行正常
- flannel 配置正常
- 节点路由配置正常
- 需要检查 VXLAN 通信和防火墙规则

### 2.3 根因分析

**根因 1：VXLAN 端口被防火墙阻止**：

- VXLAN 使用 UDP 端口 8472
- 防火墙可能阻止了该端口
- 导致跨节点通信失败

**根因 2：flannel 网络接口故障**：

- flannel.1 接口可能配置错误
- VXLAN 隧道无法建立
- 导致跨节点通信失败

**根因 3：节点间网络不通**：

- 节点间网络可能不通
- 防火墙或网络策略阻止了通信
- 导致跨节点通信失败

**根本原因**：

**VXLAN 端口被防火墙阻止**：防火墙阻止了 VXLAN 使用的 UDP 端口 8472，导致 flannel 无法建立 VXLAN 隧道，从而阻止了跨节点 Pod 通信。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：开放 VXLAN 端口**：

```bash
# 在所有节点上开放 VXLAN 端口
sudo ufw allow 8472/udp
sudo iptables -A INPUT -p udp --dport 8472 -j ACCEPT
```

**方案 2：重启 flannel**：

```bash
# 重启 flannel Pod
kubectl delete pod -n kube-system -l app=flannel
```

**方案 3：使用 hostNetwork**：

```yaml
# 临时使用 hostNetwork
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  hostNetwork: true  # 使用主机网络
  containers:
    - name: app
      image: app:v1.0.0
```

**临时方案效果**：

- ✅ 可以快速恢复服务
- ⚠️ 但未解决根本问题
- ⚠️ 可能影响安全性（开放端口）

### 3.2 永久解决方案

**方案 1：配置防火墙规则**：

```bash
# 在所有节点上配置防火墙规则
sudo ufw allow 8472/udp comment 'flannel VXLAN'
sudo ufw allow 51820/udp comment 'flannel WireGuard'
sudo ufw allow 51821/udp comment 'flannel WireGuard'
```

**方案 2：修复 flannel 配置**：

```yaml
# 修复 flannel ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: kube-flannel-cfg
  namespace: kube-system
data:
  cni-conf.json: |
    {
      "name": "cbr0",
      "type": "flannel",
      "delegate": {
        "isDefaultGateway": true
      }
    }
  net-conf.json: |
    {
      "Network": "10.42.0.0/16",
      "Backend": {
        "Type": "vxlan",
        "Port": 8472
      }
    }
```

**方案 3：使用 Calico 替代 flannel**：

```yaml
# 安装 Calico CNI
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```

**方案 4：配置网络策略**：

```yaml
# 配置网络策略允许跨节点通信
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-cross-node
  namespace: default
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector: {}
  egress:
    - to:
        - namespaceSelector: {}
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：防火墙规则标准化**：

```bash
# 创建防火墙规则脚本
#!/bin/bash
# 配置 flannel 防火墙规则
sudo ufw allow 8472/udp comment 'flannel VXLAN'
sudo ufw allow 51820/udp comment 'flannel WireGuard'
sudo ufw allow 51821/udp comment 'flannel WireGuard'
```

**措施 2：网络连通性监控**：

```bash
# 配置网络连通性监控
kubectl run network-test --image=busybox --rm -it -- ping -c 3 <target-pod-ip>
```

**措施 3：CNI 插件监控**：

```bash
# 配置 CNI 插件监控
kubectl get pod -n kube-system | grep flannel

# 定期检查 CNI 插件状态
watch -n 5 kubectl get pod -n kube-system | grep flannel
```

**措施 4：网络策略审查**：

```bash
# 定期审查网络策略
kubectl get networkpolicy -A

# 确保网络策略不会阻止跨节点通信
```

---

## 4 验证与恢复

### 4.1 验证步骤

**步骤 1：验证防火墙规则**：

```bash
# 检查防火墙规则
sudo ufw status | grep 8472

# 预期输出
8472/udp                     ALLOW       Anywhere
```

**步骤 2：验证跨节点通信**：

```bash
# 测试跨节点通信
kubectl exec -it pod-a -- ping -c 3 10.42.2.10

# 预期输出
PING 10.42.2.10 (10.42.2.10) 56(84) bytes of data.
64 bytes from 10.42.2.10: icmp_seq=1 time=0.234 ms
64 bytes from 10.42.2.10: icmp_seq=2 time=0.256 ms
64 bytes from 10.42.2.10: icmp_seq=3 time=0.245 ms
```

**步骤 3：验证 flannel 状态**：

```bash
# 检查 flannel Pod 状态
kubectl get pod -n kube-system | grep flannel

# 预期输出
kube-flannel-ds-xxx   1/1     Running   0          5d
```

**步骤 4：验证服务可用性**：

```bash
# 测试服务间通信
kubectl exec -it pod-a -- curl http://service-b.default.svc.cluster.local:8080

# 预期输出
{"status":"ok"}
```

### 4.2 恢复确认

**恢复指标**：

- ✅ 防火墙规则：已配置
- ✅ 跨节点通信：成功
- ✅ flannel 状态：正常
- ✅ 服务可用性：正常

**恢复时间**：

- **故障发现**：17:00:00
- **开始排查**：17:00:05
- **根因确认**：17:10:00
- **问题解决**：17:15:00
- **服务恢复**：17:15:05
- **总耗时**：15 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **VXLAN 端口被防火墙阻止**：
   - VXLAN 使用 UDP 端口 8472
   - 防火墙需要开放该端口

2. **CNI 插件配置重要**：
   - CNI 插件配置错误会导致跨节点通信失败
   - 需要正确配置 CNI 插件

3. **网络策略影响通信**：
   - 网络策略可能阻止跨节点通信
   - 需要正确配置网络策略

### 5.2 最佳实践

1. **配置防火墙规则**：
   - 开放 CNI 插件所需端口
   - 使用标准化防火墙规则

2. **CNI 插件监控**：
   - 定期检查 CNI 插件状态
   - 及时处理 CNI 插件故障

3. **网络连通性测试**：
   - 定期测试跨节点通信
   - 及时发现网络问题

4. **网络策略审查**：
   - 定期审查网络策略
   - 确保网络策略不会阻止必要通信

### 5.3 相关文档

- [`../../TECHNICAL/03-networking/cni/cni.md`](../../TECHNICAL/03-networking/cni/cni.md) - CNI 文档
- [`../../TECHNICAL/03-networking/flannel/flannel.md`](../../TECHNICAL/03-networking/flannel/flannel.md) - Flannel 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

## 6 相关文档

- [`../README.md`](README.md) - 故障排查案例集目录
- [`../../TECHNICAL/03-networking/flannel/flannel.md`](../../TECHNICAL/03-networking/flannel/flannel.md) - Flannel 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
