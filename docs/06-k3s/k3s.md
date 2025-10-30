# K3s：轻量级 Kubernetes 架构与实践

本文档深入解析 K3s 的架构设计、裁剪策略和边缘场景最佳实践。

## 定位与优势

### 为什么需要 K3s？

```mermaid
graph LR
    A[Kubernetes] -->|太重| B[边缘场景需求]
    B --> C[K3s]
    C --> D[轻量]
    C --> E[单二进制]
    C --> F[ARM 支持]

    style A fill:#ffe6e6
    style C fill:#e6ffe6
```

### K3s vs Kubernetes

| 维度           | Kubernetes       | K3s                   |
| -------------- | ---------------- | --------------------- |
| **二进制大小** | ~1 GB（多组件）  | ~60 MB（单二进制）    |
| **内存占用**   | ~512 MB 控制平面 | ~250 MB 控制平面      |
| **存储后端**   | 外部 etcd        | sqlite（默认）或 etcd |
| **网络插件**   | 需手动安装       | 内置 flannel          |
| **负载均衡器** | 需手动安装       | 内置 traefik          |
| **适用场景**   | 大规模生产集群   | 边缘、IoT、ARM 设备   |

## 架构设计

### 单二进制架构

```mermaid
graph TB
    A[k3s 二进制] --> B[静态链接组件]
    B --> C[containerd]
    B --> D[flannel]
    B --> E[traefik]
    B --> F[sqlite]
    B --> G[kubelet]
    B --> H[kube-proxy]

    I[manifest 目录] --> A
    A --> J[启动时加载<br/>static pod]

    style A fill:#e1f5ff
    style J fill:#fff4e1
```

### 组件对比

| 组件                         | Kubernetes  | K3s              |
| ---------------------------- | ----------- | ---------------- |
| **kube-api-server**          | ✅ 独立进程 | ✅ 内置          |
| **etcd**                     | ✅ 外部集群 | ✅ sqlite 或外部 |
| **kube-controller-manager**  | ✅ 独立进程 | ✅ 内置          |
| **kube-scheduler**           | ✅ 独立进程 | ✅ 内置          |
| **cloud-controller-manager** | ✅ 独立进程 | ❌ 裁剪          |
| **kubelet**                  | ✅ 节点组件 | ✅ 内置          |
| **kube-proxy**               | ✅ 节点组件 | ✅ 内置          |
| **containerd**               | 外部安装    | ✅ 内置          |
| **CNI 插件**                 | 外部安装    | ✅ 内置 flannel  |
| **Ingress 控制器**           | 外部安装    | ✅ 内置 traefik  |

## 裁剪策略

### 裁剪清单

```mermaid
graph TD
    A[K8s 完整功能] --> B[裁剪 Alpha API]
    A --> C[裁剪云控制器]
    A --> D[裁剪 in-tree 存储驱动]
    A --> E[简化存储后端]

    B --> F[K3s 精简版]
    C --> F
    D --> F
    E --> F

    style A fill:#ffe6e6
    style F fill:#e6ffe6
```

| 裁剪项                       | 原因                     | 影响            |
| ---------------------------- | ------------------------ | --------------- |
| **Alpha API**                | 边缘场景不需要实验性功能 | 减少 API 复杂度 |
| **cloud-controller-manager** | 边缘无云环境             | 减小二进制体积  |
| **in-tree 存储驱动**         | 统一使用 CSI             | 简化维护        |
| **etcd（可选）**             | sqlite 满足边缘需求      | 减小资源占用    |

## 存储后端选择

### 三种存储模式

```mermaid
graph TB
    A[K3s 存储后端] --> B[嵌入式 etcd]
    A --> C[外部 etcd]
    A --> D[外部数据库<br/>MySQL/PostgreSQL]

    B --> E[单节点/小规模]
    C --> F[中等规模<br/>3-5 节点]
    D --> G[大规模<br/>已有数据库]

    style B fill:#e1f5ff
    style D fill:#fff4e1
```

### sqlite vs etcd

| 维度           | sqlite            | etcd              |
| -------------- | ----------------- | ----------------- |
| **安装复杂度** | ✅ 零配置         | ❌ 需独立集群     |
| **资源占用**   | ✅ 极低（单文件） | ❌ 需要 3 节点    |
| **网络依赖**   | ✅ 无网络延迟     | ❌ 网络往返 2ms   |
| **数据一致性** | ✅ 最终一致       | ✅ 强一致（Raft） |
| **高可用**     | ❌ 单点           | ✅ 分布式         |
| **适用场景**   | 边缘、单节点      | 生产集群          |

### 为什么边缘场景选 sqlite？

**技术论证**：

1. **边缘节点常掉电**：sqlite 单文件复制/备份成本最低
2. **网络分区容忍**：本地继续运行，恢复后同步，接受"最终一致"
3. **Pod 密度低**：边缘节点平均 10 Pod/节点，总对象数 ≈1 万，sqlite 单线程足以
4. **资源受限**：ARM 设备内存有限，sqlite 内存占用极低

```mermaid
graph LR
    A[边缘场景] --> B[掉电频繁]
    A --> C[网络不稳定]
    A --> D[资源受限]

    B --> E[sqlite<br/>单文件备份]
    C --> F[本地运行<br/>最终一致]
    D --> G[极低内存占用]

    style E fill:#e6ffe6
    style F fill:#e6ffe6
    style G fill:#e6ffe6
```

## 内置组件

### containerd

- **定位**：容器运行时接口
- **版本**：跟随上游 containerd
- **配置**：自动配置，无需手动管理

### flannel

- **定位**：CNI 网络插件
- **模式**：VXLAN（默认）或 host-gw
- **配置**：自动配置 Pod 网络

### traefik

- **定位**：Ingress 控制器和负载均衡器
- **功能**：自动发现 Service，提供 HTTP/HTTPS 路由
- **配置**：支持注解配置

### metrics-server

- **定位**：资源指标收集
- **功能**：提供 CPU/内存指标，支持 HPA
- **配置**：自动部署

## 高可用架构

### 三种 HA 路径

```mermaid
graph TD
    A[K3s HA 路径] --> B[嵌入式 etcd]
    A --> C[外部 etcd]
    A --> D[外部数据库]

    B --> E[k3s server<br/>--cluster-init]
    C --> F[k3s server<br/>--server]
    D --> G[k3s server<br/>--datastore-endpoint]

    style B fill:#e1f5ff
    style D fill:#fff4e1
```

### HA 配置示例

```bash
# 路径 1：嵌入式 etcd（3 节点）
# 节点 1
k3s server --cluster-init

# 节点 2
k3s server --server https://node1:6443 --token <token>

# 节点 3
k3s server --server https://node1:6443 --token <token>

# 路径 2：外部 etcd
k3s server \
  --datastore-endpoint="etcd" \
  --datastore-cafile=/path/to/ca.pem \
  --datastore-certfile=/path/to/etcd.pem \
  --datastore-keyfile=/path/to/etcd-key.pem

# 路径 3：外部数据库
k3s server \
  --datastore-endpoint="mysql://user:pass@tcp(host:3306)/dbname"
```

## 性能优化

### 为什么 K3s 能支持 1000 节点？

**技术论证**：

1. **控制器精简**：去掉大量 controller 与 alpha API，list-watch 压力下降 40%
2. **本地存储**：sqlite 本地调用延迟 0.1ms，比 etcd 网络往返 2ms 低一个量级
3. **Pod 密度低**：边缘节点平均 10 Pod/节点，总对象数 ≈1 万，sqlite 单线程足以
4. **网络拓扑**：星型拓扑，跨节点 watch 少
5. **内存优化**：控制器精简后，内存常驻 < 250MB，树莓派 4B（4GB）可承受

```mermaid
graph TD
    A[K3s 性能优化] --> B[裁剪控制器]
    A --> C[本地 sqlite]
    A --> D[低 Pod 密度]
    A --> E[星型网络]

    B --> F[减少 40% 压力]
    C --> G[延迟 0.1ms]
    D --> H[对象数 ≈1 万]
    E --> I[减少跨节点 watch]

    style F fill:#e6ffe6
    style G fill:#e6ffe6
```

### 性能基线

| 指标             | 数值      | 说明             |
| ---------------- | --------- | ---------------- |
| **控制平面内存** | < 250 MB  | 树莓派 4B 可承受 |
| **启动时间**     | < 10s     | 单节点           |
| **支持节点数**   | 1000 节点 | 边缘场景         |
| **sqlite 延迟**  | 0.1ms     | 本地调用         |

## 安装与配置

### 单节点安装

```bash
# 快速安装
curl -sfL https://get.k3s.io | sh -

# 带 WasmEdge 支持（2025）
curl -sfL https://get.k3s.io | \
  INSTALL_K3S_VERSION=v1.30.4+k3s1 \
  sh -s - --wasm --write-kubeconfig-mode 644
```

### 多节点安装

```bash
# Server 节点
curl -sfL https://get.k3s.io | K3S_TOKEN=xxx sh -s - server

# Agent 节点
curl -sfL https://get.k3s.io | K3S_TOKEN=xxx \
  K3S_URL=https://server-ip:6443 sh -s - agent
```

### 配置文件位置

| 类型           | 路径                                    | 说明            |
| -------------- | --------------------------------------- | --------------- |
| **kubeconfig** | `/etc/rancher/k3s/k3s.yaml`             | 集群配置文件    |
| **数据目录**   | `/var/lib/rancher/k3s`                  | 集群数据        |
| **manifest**   | `/var/lib/rancher/k3s/server/manifests` | Static pod 清单 |

## 边缘场景实践

### ARM 设备部署

```bash
# 树莓派安装
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--write-kubeconfig-mode 644" sh -

# 检查节点
kubectl get nodes -o wide
```

### 离线部署

```bash
# 1. 在有网络的机器上下载
./k3s-airgap-images-amd64.tar
./k3s

# 2. 传输到目标机器
scp k3s* user@edge-node:/tmp

# 3. 在目标机器上安装
INSTALL_K3S_SKIP_DOWNLOAD=true \
  INSTALL_K3S_AIRGAP_DIR=/tmp \
  /tmp/k3s-install.sh
```

### 资源限制配置

```yaml
# 限制节点资源使用
apiVersion: v1
kind: Node
metadata:
  name: edge-node
spec:
  taints:
    - key: edge
      value: "true"
      effect: NoSchedule
```

## 故障排查

### 常见问题

| 问题             | 原因                 | 解决方案            |
| ---------------- | -------------------- | ------------------- |
| **节点无法加入** | Token 错误或网络不通 | 检查 token 和防火墙 |
| **Pod 无法启动** | 资源不足             | 检查内存和 CPU      |
| **存储问题**     | sqlite 文件损坏      | 备份并恢复          |
| **网络问题**     | flannel 配置错误     | 检查 CNI 配置       |

### 日志位置

```bash
# K3s 日志
journalctl -u k3s -f

# containerd 日志
journalctl -u containerd -f

# kubelet 日志
/var/lib/rancher/k3s/agent/containerd/containerd.log
```

## 参考

- [K3s 官方文档](https://docs.k3s.io/)
- [K3s GitHub](https://github.com/k3s-io/k3s)
- [K3s 快速开始](https://docs.k3s.io/quick-start)

> 更多参考见 [REFERENCES.md](../REFERENCES.md)
