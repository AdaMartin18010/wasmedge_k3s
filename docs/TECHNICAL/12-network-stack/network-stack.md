# 21. 网络技术规格堆栈：全面梳理

## 目录

- [目录](#目录)
- [21.1 文档定位](#211-文档定位)
- [21.2 网络技术栈全景](#212-网络技术栈全景)
  - [21.2.1 网络层次结构](#2121-网络层次结构)
  - [21.2.2 技术组件矩阵](#2122-技术组件矩阵)
  - [21.2.3 技术栈组合](#2123-技术栈组合)
- [21.3 CNI 插件技术规格](#213-cni-插件技术规格)
  - [21.3.1 CNI 规范](#2131-cni-规范)
  - [21.3.2 Flannel 规格](#2132-flannel-规格)
  - [21.3.3 Calico 规格](#2133-calico-规格)
  - [21.3.4 Cilium 规格](#2134-cilium-规格)
  - [21.3.5 CNI 插件对比](#2135-cni-插件对比)
- [21.4 Service 技术规格](#214-service-技术规格)
  - [21.4.1 Service 类型](#2141-service-类型)
  - [21.4.2 ClusterIP 规格](#2142-clusterip-规格)
  - [21.4.3 NodePort 规格](#2143-nodeport-规格)
  - [21.4.4 LoadBalancer 规格](#2144-loadbalancer-规格)
  - [21.4.5 ExternalName 规格](#2145-externalname-规格)
- [21.5 Ingress 技术规格](#215-ingress-技术规格)
  - [21.5.1 Ingress 规范](#2151-ingress-规范)
  - [21.5.2 Nginx Ingress 规格](#2152-nginx-ingress-规格)
  - [21.5.3 Traefik Ingress 规格](#2153-traefik-ingress-规格)
  - [21.5.4 Ingress Controller 对比](#2154-ingress-controller-对比)
- [21.6 网络策略技术规格](#216-网络策略技术规格)
  - [21.6.1 NetworkPolicy 规范](#2161-networkpolicy-规范)
  - [21.6.2 Calico NetworkPolicy 规格](#2162-calico-networkpolicy-规格)
  - [21.6.3 Cilium NetworkPolicy 规格](#2163-cilium-networkpolicy-规格)
  - [21.6.4 网络策略对比](#2164-网络策略对比)
- [21.7 服务发现技术规格](#217-服务发现技术规格)
  - [21.7.1 DNS 服务发现](#2171-dns-服务发现)
  - [21.7.2 CoreDNS 规格](#2172-coredns-规格)
  - [21.7.3 环境变量服务发现](#2173-环境变量服务发现)
  - [21.7.4 服务发现对比](#2174-服务发现对比)
- [21.8 负载均衡技术规格](#218-负载均衡技术规格)
  - [21.8.1 kube-proxy 模式](#2181-kube-proxy-模式)
  - [21.8.2 iptables 模式规格](#2182-iptables-模式规格)
  - [21.8.3 IPVS 模式规格](#2183-ipvs-模式规格)
  - [21.8.4 负载均衡算法](#2184-负载均衡算法)
- [21.9 网络拓扑技术规格](#219-网络拓扑技术规格)
  - [21.9.1 控制平面拓扑](#2191-控制平面拓扑)
  - [21.9.2 数据平面拓扑](#2192-数据平面拓扑)
  - [21.9.3 边缘网络拓扑](#2193-边缘网络拓扑)
  - [21.9.4 混合云网络拓扑](#2194-混合云网络拓扑)
- [21.10 网络性能规格](#2110-网络性能规格)
  - [21.10.1 延迟规格](#21101-延迟规格)
  - [21.10.2 吞吐量规格](#21102-吞吐量规格)
  - [21.10.3 容量规格](#21103-容量规格)
  - [21.10.4 性能对比](#21104-性能对比)
- [21.11 网络协议栈](#2111-网络协议栈)
  - [21.11.1 协议层次](#21111-协议层次)
  - [21.11.2 L2/L3 协议](#21112-l2l3-协议)
  - [21.11.3 L4/L7 协议](#21113-l4l7-协议)
  - [21.11.4 协议栈对比](#21114-协议栈对比)
- [21.12 网络技术栈组合方案](#2112-网络技术栈组合方案)
  - [21.12.1 小规模集群组合](#21121-小规模集群组合)
  - [21.12.2 大规模集群组合](#21122-大规模集群组合)
  - [21.12.3 边缘计算组合](#21123-边缘计算组合)
  - [21.12.4 高性能组合](#21124-高性能组合)
- [21.13 网络接口规范](#2113-网络接口规范)
  - [21.13.1 CNI 接口规范](#21131-cni-接口规范)
  - [21.13.2 Service API 规范](#21132-service-api-规范)
  - [21.13.3 Ingress API 规范](#21133-ingress-api-规范)
- [21.14 参考](#2114-参考)

---

## 21.1 文档定位

本文档全面梳理云原生容器技术栈中的网络技术、规格和堆栈组合方案，包括 CNI 插件
、Service、Ingress、网络策略、服务发现、负载均衡等网络技术的详细规格和技术栈组合
方案。

**文档结构**：

- **网络技术栈全景**：网络层次结构、技术组件矩阵、技术栈组合
- **CNI 插件技术规格**：Flannel、Calico、Cilium 等 CNI 插件的详细规格
- **Service 技术规格**：ClusterIP、NodePort、LoadBalancer 等 Service 类型规格
- **Ingress 技术规格**：Nginx、Traefik 等 Ingress Controller 规格
- **网络策略技术规格**：NetworkPolicy、Calico、Cilium 网络策略规格
- **服务发现技术规格**：DNS、CoreDNS、环境变量等服务发现机制
- **负载均衡技术规格**：kube-proxy 模式、iptables、IPVS、负载均衡算法
- **网络拓扑技术规格**：控制平面、数据平面、边缘网络、混合云网络拓扑
- **网络性能规格**：延迟、吞吐量、容量、性能对比
- **网络协议栈**：协议层次、L2/L3、L4/L7 协议
- **网络技术栈组合方案**：不同场景的网络技术栈组合

## 21.2 网络技术栈全景

### 21.2.1 网络层次结构

**网络层次结构**：

```mermaid
graph TB
    A[应用层] --> B[L7: Ingress]
    B --> C[L4: Service]
    C --> D[L3: CNI]
    D --> E[L2: 网络接口]

    B --> B1[HTTP/HTTPS 路由]
    C --> C1[TCP/UDP 负载均衡]
    D --> D1[IP 路由/Overlay]
    E --> E1[Ethernet/VXLAN]

    style A fill:#e1f5ff
    style E fill:#fff4e1
```

**网络层次定义**：

| 层次   | 定义       | 技术                 | 功能                       |
| ------ | ---------- | -------------------- | -------------------------- |
| **L7** | 应用层     | Ingress、Gateway API | HTTP/HTTPS 路由、SSL 终止  |
| **L4** | 传输层     | Service、kube-proxy  | TCP/UDP 负载均衡、服务发现 |
| **L3** | 网络层     | CNI 插件、路由协议   | IP 路由、网络隔离          |
| **L2** | 数据链路层 | 网络接口、隧道       | 帧传输、VXLAN 封装         |

### 21.2.2 技术组件矩阵

**网络技术组件矩阵**：

| 组件类别     | 技术                 | 定位              | 规格                      |
| ------------ | -------------------- | ----------------- | ------------------------- |
| **CNI 插件** | Flannel              | 简单 Overlay 网络 | VXLAN、支持 < 100 节点    |
| **CNI 插件** | Calico               | 高性能 BGP 网络   | BGP/IPIP、支持 > 500 节点 |
| **CNI 插件** | Cilium               | eBPF 高性能网络   | eBPF、支持 > 1000 节点    |
| **Service**  | ClusterIP            | 集群内部服务      | 虚拟 IP、DNS 解析         |
| **Service**  | NodePort             | 节点端口服务      | 30000-32767 端口范围      |
| **Service**  | LoadBalancer         | 外部负载均衡      | 云平台集成                |
| **Ingress**  | Nginx Ingress        | HTTP 路由         | 高并发、可配置            |
| **Ingress**  | Traefik              | 自动发现路由      | 零配置、自动发现          |
| **网络策略** | NetworkPolicy        | 标准网络策略      | L3/L4 策略                |
| **网络策略** | Calico NetworkPolicy | 增强网络策略      | L3/L4/L7 策略             |
| **网络策略** | Cilium NetworkPolicy | eBPF 网络策略     | L3/L4/L7、高性能          |
| **服务发现** | CoreDNS              | DNS 服务发现      | 集群 DNS、插件支持        |
| **服务发现** | 环境变量             | 环境变量服务发现  | Pod 环境变量注入          |
| **负载均衡** | kube-proxy iptables  | iptables 模式     | 默认模式、规则数多        |
| **负载均衡** | kube-proxy IPVS      | IPVS 模式         | 高性能、大规模集群        |

### 21.2.3 技术栈组合

**网络技术栈组合方案**：

| 场景           | CNI           | Service                | Ingress | 网络策略      | 负载均衡  | 说明     |
| -------------- | ------------- | ---------------------- | ------- | ------------- | --------- | -------- |
| **小规模集群** | Flannel       | ClusterIP              | Traefik | NetworkPolicy | iptables  | 简单易用 |
| **大规模集群** | Calico/Cilium | ClusterIP+LoadBalancer | Nginx   | Calico/Cilium | IPVS      | 高性能   |
| **边缘计算**   | Flannel       | ClusterIP              | Traefik | NetworkPolicy | iptables  | 轻量部署 |
| **高性能集群** | Cilium        | ClusterIP+LoadBalancer | Nginx   | Cilium        | IPVS+eBPF | 极高性能 |

## 21.3 CNI 插件技术规格

### 21.3.1 CNI 规范

**CNI（Container Network Interface）规范**：

**规范版本**：CNI v0.4.0、v1.0.0

**核心接口**：

| 接口      | 定义         | 输入                      | 输出     |
| --------- | ------------ | ------------------------- | -------- |
| **ADD**   | 添加网络接口 | 容器 ID、网络命名空间路径 | 接口配置 |
| **DEL**   | 删除网络接口 | 容器 ID、网络命名空间路径 | 无       |
| **CHECK** | 检查网络接口 | 容器 ID、网络命名空间路径 | 状态     |

**CNI 配置格式**：

```json
{
  "cniVersion": "0.4.0",
  "name": "mynet",
  "type": "bridge",
  "bridge": "cni0",
  "ipam": {
    "type": "host-local",
    "subnet": "10.244.0.0/16"
  }
}
```

**CNI 规范要点**：

- **插件化设计**：CNI 插件独立运行，可替换
- **标准化接口**：统一的 ADD/DEL/CHECK 接口
- **配置驱动**：通过 JSON 配置文件驱动
- **网络命名空间**：支持 Linux 网络命名空间隔离

### 21.3.2 Flannel 规格

**Flannel 技术规格**：

| 规格项         | 规格值              | 说明               |
| -------------- | ------------------- | ------------------ |
| **版本**       | v0.22.0+            | 最新稳定版本       |
| **支持模式**   | VXLAN、host-gw、UDP | 三种网络模式       |
| **IP 分配**    | 每个节点一个子网    | /24 子网（256 IP） |
| **默认网段**   | 10.244.0.0/16       | 可配置             |
| **节点数限制** | < 100 节点          | 推荐规模           |
| **网络策略**   | 支持 NetworkPolicy  | 需要额外组件       |
| **性能**       | 中等                | VXLAN 封装开销     |

**Flannel 架构**：

```mermaid
graph TB
    A[flanneld] --> B[etcd/API Server]
    A --> C[VXLAN Interface]
    C --> D[Pod Network]

    E[CNI Plugin] --> F[flannel-cni]
    F --> C

    style A fill:#e1f5ff
```

**Flannel 模式对比**：

| 模式        | 说明                   | 性能 | 网络要求           |
| ----------- | ---------------------- | ---- | ------------------ |
| **VXLAN**   | 默认模式，封装在 UDP   | 中等 | 无特殊要求         |
| **host-gw** | 主机网关模式，直接路由 | 高   | 节点在同一 L2 网络 |
| **UDP**     | UDP 封装，已弃用       | 低   | 无特殊要求         |

**Flannel 配置示例**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kube-flannel-cfg
  namespace: kube-system
data:
  cni-conf.json: |
    {
      "Network": "10.244.0.0/16",
      "Backend": {
        "Type": "vxlan"
      }
    }
```

### 21.3.3 Calico 规格

**Calico 技术规格**：

| 规格项         | 规格值                 | 说明         |
| -------------- | ---------------------- | ------------ |
| **版本**       | v3.26.0+               | 最新稳定版本 |
| **支持模式**   | BGP、IPIP、VXLAN       | 三种网络模式 |
| **IP 分配**    | IPAM，每个 Pod 一个 IP | IP Pool 管理 |
| **默认网段**   | 192.168.0.0/16         | 可配置       |
| **节点数限制** | > 500 节点             | 大规模集群   |
| **网络策略**   | 原生支持 L3/L4/L7      | 完整网络策略 |
| **性能**       | 高                     | BGP 直接路由 |

**Calico 架构**：

```mermaid
graph TB
    A[calico-node] --> B[BGP Speaker]
    A --> C[Felix]
    A --> D[CNI Plugin]

    B --> E[BGP Peer]
    C --> F[Network Policy]
    D --> G[Pod Network]

    style A fill:#e1f5ff
```

**Calico 模式对比**：

| 模式      | 说明               | 性能 | 网络要求        |
| --------- | ------------------ | ---- | --------------- |
| **BGP**   | 默认模式，BGP 路由 | 高   | 支持 BGP 的网络 |
| **IPIP**  | IP over IP 隧道    | 中高 | 无特殊要求      |
| **VXLAN** | VXLAN 封装         | 中等 | 无特殊要求      |

**Calico 配置示例**：

```yaml
apiVersion: projectcalico.org/v3
kind: IPPool
metadata:
  name: default-pool
spec:
  cidr: 192.168.0.0/16
  ipipMode: Never
  natOutgoing: true
```

### 21.3.4 Cilium 规格

**Cilium 技术规格**：

| 规格项         | 规格值                 | 说明          |
| -------------- | ---------------------- | ------------- |
| **版本**       | v1.14.0+               | 最新稳定版本  |
| **支持模式**   | eBPF、Native Routing   | eBPF 内核加速 |
| **IP 分配**    | IPAM，每个 Pod 一个 IP | IP Pool 管理  |
| **默认网段**   | 10.0.0.0/8             | 可配置        |
| **节点数限制** | > 1000 节点            | 超大规模集群  |
| **网络策略**   | 原生支持 L3/L4/L7      | eBPF 实现     |
| **性能**       | 极高                   | eBPF 内核旁路 |

**Cilium 架构**：

```mermaid
graph TB
    A[cilium-agent] --> B[eBPF Programs]
    A --> C[CNI Plugin]

    B --> D[Kernel Bypass]
    C --> E[Pod Network]

    F[Network Policy] --> B

    style A fill:#e1f5ff
    style B fill:#fff4e1
```

**Cilium 特性**：

| 特性             | 说明              | 优势           |
| ---------------- | ----------------- | -------------- |
| **eBPF**         | 内核旁路，零拷贝  | 极高性能       |
| **L7 策略**      | HTTP/gRPC 策略    | 细粒度控制     |
| **Service Mesh** | 内置 Service Mesh | 无需 Sidecar   |
| **可观测性**     | 内置可观测性      | 网络流量可视化 |

**Cilium 配置示例**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cilium-config
  namespace: kube-system
data:
  enable-bpf-masquerade: "true"
  enable-ipv4: "true"
  ipam: "cluster-pool"
  cluster-pool-ipv4-cidr: "10.0.0.0/8"
```

### 21.3.5 CNI 插件对比

**CNI 插件详细对比**：

| 规格项         | Flannel       | Calico   | Cilium      |
| -------------- | ------------- | -------- | ----------- |
| **复杂度**     | 低            | 中       | 高          |
| **性能**       | 中等          | 高       | 极高        |
| **节点数**     | < 100         | > 500    | > 1000      |
| **网络策略**   | 需要额外组件  | 原生支持 | 原生支持 L7 |
| **路由方式**   | VXLAN Overlay | BGP/IPIP | eBPF 路由   |
| **内存占用**   | ~50MB         | ~100MB   | ~200MB      |
| **CPU 占用**   | 低            | 中       | 中高        |
| **配置难度**   | 简单          | 中等     | 复杂        |
| **社区活跃度** | 高            | 高       | 极高        |
| **生产验证**   | 广泛          | 广泛     | 逐步增加    |

**CNI 插件选择决策树**：

```yaml
CNI 插件选择:
  if 节点数 < 100 and 简单易用: Flannel
  elif 节点数 > 500 and 高性能: Calico
  elif 节点数 > 1000 and 极高性能: Cilium
  elif 需要 L7 策略: Cilium
  elif 需要 BGP 路由: Calico
  else: Flannel（默认）
```

## 21.4 Service 技术规格

### 21.4.1 Service 类型

**Service 类型分类**：

| 类型             | 定义         | 访问方式        | 适用场景           |
| ---------------- | ------------ | --------------- | ------------------ |
| **ClusterIP**    | 集群内部 IP  | ClusterIP       | 集群内部服务       |
| **NodePort**     | 节点端口     | NodeIP:NodePort | 开发测试、简单部署 |
| **LoadBalancer** | 外部负载均衡 | LoadBalancer IP | 生产环境           |
| **ExternalName** | 外部名称映射 | DNS CNAME       | 外部服务映射       |

### 21.4.2 ClusterIP 规格

**ClusterIP Service 规格**：

| 规格项        | 规格值                              | 说明             |
| ------------- | ----------------------------------- | ---------------- |
| **类型**      | ClusterIP                           | 默认类型         |
| **IP 分配**   | 集群内虚拟 IP                       | Service CIDR     |
| **默认 CIDR** | 10.96.0.0/12                        | 可配置           |
| **DNS 解析**  | service.namespace.svc.cluster.local | 集群 DNS         |
| **负载均衡**  | kube-proxy                          | iptables/IPVS    |
| **会话保持**  | SessionAffinity                     | ClientIP         |
| **健康检查**  | Endpoints 检查                      | 自动剔除异常端点 |

**ClusterIP 配置示例**：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 8080
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

### 21.4.3 NodePort 规格

**NodePort Service 规格**：

| 规格项       | 规格值          | 说明          |
| ------------ | --------------- | ------------- |
| **类型**     | NodePort        | 节点端口类型  |
| **端口范围** | 30000-32767     | 默认范围      |
| **访问方式** | NodeIP:NodePort | 任意节点      |
| **外部访问** | 需要开放防火墙  | 端口安全      |
| **负载均衡** | kube-proxy      | iptables/IPVS |

**NodePort 配置示例**：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080
```

### 21.4.4 LoadBalancer 规格

**LoadBalancer Service 规格**：

| 规格项         | 规格值              | 说明             |
| -------------- | ------------------- | ---------------- |
| **类型**       | LoadBalancer        | 外部负载均衡类型 |
| **云平台集成** | 需要云平台支持      | AWS/GCP/Azure    |
| **IP 分配**    | 云平台负载均衡器 IP | 外部 IP          |
| **费用**       | 按使用计费          | 云平台费用       |
| **高可用**     | 云平台保证          | 自动故障转移     |

**LoadBalancer 配置示例**：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-lb
  annotations:
    cloud-provider: aws
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 8080
```

### 21.4.5 ExternalName 规格

**ExternalName Service 规格**：

| 规格项       | 规格值       | 说明         |
| ------------ | ------------ | ------------ |
| **类型**     | ExternalName | 外部名称映射 |
| **DNS 解析** | CNAME 记录   | 外部服务     |
| **用途**     | 外部服务代理 | 数据库、API  |

**ExternalName 配置示例**：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: database.example.com
```

## 21.5 Ingress 技术规格

### 21.5.1 Ingress 规范

**Ingress API 规范**：

**规范版本**：networking.k8s.io/v1

**核心资源**：

| 资源                   | 定义                | 功能       |
| ---------------------- | ------------------- | ---------- |
| **Ingress**            | HTTP/HTTPS 路由规则 | 路由配置   |
| **IngressClass**       | Ingress 控制器类型  | 控制器选择 |
| **Ingress Controller** | 路由执行组件        | 实际路由   |

**Ingress 配置示例**：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

### 21.5.2 Nginx Ingress 规格

**Nginx Ingress Controller 规格**：

| 规格项        | 规格值          | 说明                    |
| ------------- | --------------- | ----------------------- |
| **版本**      | v1.9.0+         | 最新稳定版本            |
| **性能**      | 极高            | 支持高并发              |
| **配置**      | ConfigMap、注解 | 灵活配置                |
| **SSL**       | TLS 终止        | 证书管理                |
| **负载均衡**  | 多种算法        | Round Robin、Least Conn |
| **WebSocket** | 支持            | WebSocket 代理          |

**Nginx Ingress 配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: ingress-nginx
data:
  proxy-connect-timeout: "600"
  proxy-send-timeout: "600"
  proxy-read-timeout: "600"
```

### 21.5.3 Traefik Ingress 规格

**Traefik Ingress Controller 规格**：

| 规格项       | 规格值   | 说明                  |
| ------------ | -------- | --------------------- |
| **版本**     | v3.0.0+  | 最新稳定版本          |
| **性能**     | 高       | 支持中等并发          |
| **配置**     | 自动发现 | 零配置                |
| **SSL**      | 自动证书 | Let's Encrypt         |
| **负载均衡** | 多种算法 | Round Robin、Weighted |

**Traefik 自动发现**：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  annotations:
    traefik.ingress.kubernetes.io/rule-type: PathPrefix
spec:
  selector:
    app: nginx
  ports:
    - port: 80
```

### 21.5.4 Ingress Controller 对比

**Ingress Controller 详细对比**：

| 规格项     | Nginx Ingress  | Traefik  | 说明           |
| ---------- | -------------- | -------- | -------------- |
| **性能**   | 极高           | 高       | Nginx 性能更高 |
| **配置**   | ConfigMap/注解 | 自动发现 | Traefik 零配置 |
| **SSL**    | 手动配置       | 自动证书 | Traefik 自动化 |
| **复杂度** | 高             | 低       | Traefik 更简单 |
| **社区**   | 极高           | 高       | Nginx 更广泛   |

## 21.6 网络策略技术规格

### 21.6.1 NetworkPolicy 规范

**NetworkPolicy API 规范**：

**规范版本**：networking.k8s.io/v1

**核心规则**：

| 规则类型        | 定义       | 功能           |
| --------------- | ---------- | -------------- |
| **podSelector** | Pod 选择器 | 选择目标 Pod   |
| **ingress**     | 入站规则   | 允许的入站流量 |
| **egress**      | 出站规则   | 允许的出站流量 |
| **policyTypes** | 策略类型   | Ingress/Egress |

**NetworkPolicy 配置示例**：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
```

### 21.6.2 Calico NetworkPolicy 规格

**Calico NetworkPolicy 规格**：

| 规格项       | 规格值      | 说明         |
| ------------ | ----------- | ------------ |
| **支持层级** | L3/L4/L7    | 完整网络策略 |
| **规则类型** | 标准 + 扩展 | 更丰富的规则 |
| **性能**     | 高          | BGP 路由优化 |

**Calico NetworkPolicy 扩展**：

```yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: api-policy
spec:
  selector: app == 'api'
  ingress:
    - action: Allow
      source:
        selector: app == 'frontend'
      destination:
        ports:
          - 8080
```

### 21.6.3 Cilium NetworkPolicy 规格

**Cilium NetworkPolicy 规格**：

| 规格项       | 规格值   | 说明         |
| ------------ | -------- | ------------ |
| **支持层级** | L3/L4/L7 | 完整网络策略 |
| **实现方式** | eBPF     | 内核旁路     |
| **性能**     | 极高     | eBPF 零拷贝  |

**Cilium NetworkPolicy L7 规则**：

```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: api-l7-policy
spec:
  endpointSelector:
    matchLabels:
      app: api
  ingress:
    - fromEndpoints:
        - matchLabels:
            app: frontend
      toPorts:
        - ports:
            - port: "8080"
              protocol: TCP
          rules:
            http:
              - method: "GET"
                path: "/api/v1"
```

### 21.6.4 网络策略对比

**网络策略详细对比**：

| 规格项     | NetworkPolicy | Calico | Cilium |
| ---------- | ------------- | ------ | ------ |
| **L3/L4**  | 支持          | 支持   | 支持   |
| **L7**     | 不支持        | 支持   | 支持   |
| **性能**   | 中            | 高     | 极高   |
| **实现**   | iptables      | BGP    | eBPF   |
| **复杂度** | 低            | 中     | 高     |

## 21.7 服务发现技术规格

### 21.7.1 DNS 服务发现

**DNS 服务发现机制**：

**DNS 解析格式**：

| 格式         | 示例                                | 说明       |
| ------------ | ----------------------------------- | ---------- |
| **完整域名** | service.namespace.svc.cluster.local | 完整 FQDN  |
| **短域名**   | service.namespace                   | 命名空间内 |
| **简化名**   | service                             | 同命名空间 |

**DNS 记录类型**：

| 记录类型     | 说明     | 示例                                             |
| ------------ | -------- | ------------------------------------------------ |
| **A 记录**   | IP 地址  | service.namespace.svc.cluster.local -> 10.96.0.1 |
| **SRV 记录** | 服务记录 | \_http.\_tcp.service.namespace.svc.cluster.local |
| **PTR 记录** | 反向解析 | 1.0.96.10.in-addr.arpa                           |

### 21.7.2 CoreDNS 规格

**CoreDNS 技术规格**：

| 规格项   | 规格值       | 说明         |
| -------- | ------------ | ------------ |
| **版本** | v1.11.0+     | 最新稳定版本 |
| **性能** | 高           | 支持高 QPS   |
| **插件** | 丰富插件生态 | 可扩展       |
| **配置** | Corefile     | 灵活配置     |

**CoreDNS 配置示例**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
           lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf {
           max_concurrent 1000
        }
        cache 30
        loop
        reload
        loadbalance
    }
```

### 21.7.3 环境变量服务发现

**环境变量服务发现**：

**环境变量格式**：

| 格式                  | 示例                      | 说明         |
| --------------------- | ------------------------- | ------------ |
| **SERVICE_HOST**      | NGINX_SERVICE_HOST        | Service IP   |
| **SERVICE_PORT**      | NGINX_SERVICE_PORT        | Service 端口 |
| **SERVICE_PORT_HTTP** | NGINX_SERVICE_PORT_80_TCP | 命名端口     |

**环境变量注入**：

```yaml
env:
  - name: NGINX_SERVICE_HOST
    valueFrom:
      fieldRef:
        fieldPath: status.hostIP
```

### 21.7.4 服务发现对比

**服务发现机制对比**：

| 机制         | 优势       | 劣势         | 适用场景 |
| ------------ | ---------- | ------------ | -------- |
| **DNS**      | 标准、灵活 | 延迟略高     | 生产环境 |
| **环境变量** | 零延迟     | 静态、不灵活 | 简单场景 |

## 21.8 负载均衡技术规格

### 21.8.1 kube-proxy 模式

**kube-proxy 模式分类**：

| 模式          | 定义          | 特点       |
| ------------- | ------------- | ---------- |
| **userspace** | 用户空间模式  | 已弃用     |
| **iptables**  | iptables 模式 | 默认模式   |
| **ipvs**      | IPVS 模式     | 高性能模式 |

### 21.8.2 iptables 模式规格

**iptables 模式规格**：

| 规格项       | 规格值         | 说明                |
| ------------ | -------------- | ------------------- |
| **性能**     | 中             | 规则数多时性能下降  |
| **规则数**   | O(n) 增长      | 每个 Service 多规则 |
| **适用场景** | < 1000 Service | 中小规模集群        |

### 21.8.3 IPVS 模式规格

**IPVS 模式规格**：

| 规格项       | 规格值         | 说明           |
| ------------ | -------------- | -------------- |
| **性能**     | 高             | 内核级负载均衡 |
| **规则数**   | O(1) 查找      | 哈希表查找     |
| **适用场景** | > 1000 Service | 大规模集群     |

**IPVS 配置**：

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
networking:
  serviceSubnet: "10.96.0.0/12"
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "ipvs"
```

### 21.8.4 负载均衡算法

**负载均衡算法对比**：

| 算法                     | 定义     | 特点     | 适用场景   |
| ------------------------ | -------- | -------- | ---------- |
| **Round Robin**          | 轮询     | 简单     | 无状态服务 |
| **Least Connections**    | 最少连接 | 均衡负载 | 长连接服务 |
| **IP Hash**              | IP 哈希  | 会话保持 | 有状态服务 |
| **Weighted Round Robin** | 加权轮询 | 性能差异 | 异构节点   |

## 21.9 网络拓扑技术规格

### 21.9.1 控制平面拓扑

**控制平面网络拓扑**：

```mermaid
graph TB
    A[API Server] --> B[etcd]
    A --> C[Controller Manager]
    A --> D[Scheduler]

    E[Node 1] --> A
    F[Node 2] --> A
    G[Node N] --> A

    style A fill:#e1f5ff
```

**控制平面拓扑特点**：

- **星型拓扑**：所有节点连接到 API Server
- **单点故障**：API Server 成为单点
- **高可用方案**：多 API Server + 负载均衡

### 21.9.2 数据平面拓扑

**数据平面网络拓扑**：

```mermaid
graph TB
    A[Pod 1] <--> B[Pod 2]
    A <--> C[Pod 3]
    B <--> C

    D[Node 1] --> A
    E[Node 2] --> B
    F[Node 3] --> C

    style A fill:#fff4e1
```

**数据平面拓扑特点**：

- **网状拓扑**：Pod 间直接通信
- **无 NAT**：Pod 间无 NAT 转换
- **直连通信**：保证低延迟

### 21.9.3 边缘网络拓扑

**边缘网络拓扑**：

```mermaid
graph TB
    A[中心集群] --> B[边缘节点 1]
    A --> C[边缘节点 2]

    B --> D[边缘 Pod]
    C --> E[边缘 Pod]

    style A fill:#e1f5ff
    style B fill:#fff4e1
```

**边缘网络特点**：

- **分层拓扑**：中心-边缘分层
- **网络分区**：接受网络分区
- **本地优先**：边缘本地可用

### 21.9.4 混合云网络拓扑

**混合云网络拓扑**：

```mermaid
graph TB
    A[云集群] <--> B[本地集群]
    A <--> C[边缘集群]

    B --> D[VPN/专线]
    C --> D

    style A fill:#e1f5ff
```

**混合云网络特点**：

- **多集群连接**：VPN/专线连接
- **统一管理**：统一网络策略
- **服务发现**：跨集群服务发现

## 21.10 网络性能规格

### 21.10.1 延迟规格

**网络延迟规格**：

| 场景             | 延迟    | 说明          |
| ---------------- | ------- | ------------- |
| **Pod 间同节点** | < 0.1ms | 本地通信      |
| **Pod 间跨节点** | < 1ms   | 网络通信      |
| **Service 访问** | < 2ms   | 负载均衡开销  |
| **Ingress 访问** | < 5ms   | HTTP 路由开销 |

### 21.10.2 吞吐量规格

**网络吞吐量规格**：

| 场景             | 吞吐量   | 说明            |
| ---------------- | -------- | --------------- |
| **Pod 间带宽**   | 10Gbps   | 节点网络带宽    |
| **Service 吞吐** | 1M QPS   | kube-proxy 吞吐 |
| **Ingress 吞吐** | 100K QPS | HTTP 路由吞吐   |

### 21.10.3 容量规格

**网络容量规格**：

| 资源             | 容量   | 说明          |
| ---------------- | ------ | ------------- |
| **Service 数量** | < 5000 | iptables 模式 |
| **Service 数量** | > 5000 | IPVS 模式     |
| **Ingress 数量** | < 1000 | 推荐规模      |
| **网络策略数量** | < 1000 | 推荐规模      |

### 21.10.4 性能对比

**网络性能详细对比**：

| 指标         | Flannel | Calico | Cilium |
| ------------ | ------- | ------ | ------ |
| **延迟**     | 中      | 低     | 极低   |
| **吞吐量**   | 中      | 高     | 极高   |
| **CPU 占用** | 低      | 中     | 中高   |
| **内存占用** | 低      | 中     | 中高   |

## 21.11 网络协议栈

### 21.11.1 协议层次

**网络协议栈层次**：

| 层次   | 协议            | 功能           |
| ------ | --------------- | -------------- |
| **L7** | HTTP/HTTPS/gRPC | 应用层协议     |
| **L4** | TCP/UDP         | 传输层协议     |
| **L3** | IP/ICMP         | 网络层协议     |
| **L2** | Ethernet/VXLAN  | 数据链路层协议 |

### 21.11.2 L2/L3 协议

**L2/L3 协议对比**：

| 协议         | 层次 | 用途     | 示例     |
| ------------ | ---- | -------- | -------- |
| **Ethernet** | L2   | 帧传输   | 物理网络 |
| **VXLAN**    | L2   | 虚拟网络 | Flannel  |
| **IP**       | L3   | 路由     | 所有网络 |
| **BGP**      | L3   | 路由协议 | Calico   |

### 21.11.3 L4/L7 协议

**L4/L7 协议对比**：

| 协议     | 层次 | 用途       | 示例    |
| -------- | ---- | ---------- | ------- |
| **TCP**  | L4   | 可靠传输   | Service |
| **UDP**  | L4   | 不可靠传输 | DNS     |
| **HTTP** | L7   | Web 协议   | Ingress |
| **gRPC** | L7   | RPC 协议   | 微服务  |

### 21.11.4 协议栈对比

**协议栈实现对比**：

| 实现        | L2    | L3     | L4   | L7   |
| ----------- | ----- | ------ | ---- | ---- |
| **Flannel** | VXLAN | IP     | -    | -    |
| **Calico**  | -     | BGP/IP | -    | 支持 |
| **Cilium**  | eBPF  | eBPF   | eBPF | eBPF |

## 21.12 网络技术栈组合方案

### 21.12.1 小规模集群组合

**小规模集群网络技术栈**：

```yaml
小规模集群网络栈:
  CNI: Flannel (VXLAN)
  Service: ClusterIP + NodePort
  Ingress: Traefik
  网络策略: NetworkPolicy
  负载均衡: kube-proxy iptables
  服务发现: CoreDNS
  说明: 简单易用，配置简单
```

### 21.12.2 大规模集群组合

**大规模集群网络技术栈**：

```yaml
大规模集群网络栈:
  CNI: Calico (BGP) 或 Cilium (eBPF)
  Service: ClusterIP + LoadBalancer
  Ingress: Nginx Ingress
  网络策略: Calico/Cilium NetworkPolicy
  负载均衡: kube-proxy IPVS
  服务发现: CoreDNS
  说明: 高性能，大规模支持
```

### 21.12.3 边缘计算组合

**边缘计算网络技术栈**：

```yaml
边缘计算网络栈:
  CNI: Flannel (host-gw)
  Service: ClusterIP
  Ingress: Traefik
  网络策略: NetworkPolicy
  负载均衡: kube-proxy iptables
  服务发现: CoreDNS
  说明: 轻量部署，本地优先
```

### 21.12.4 高性能组合

**高性能集群网络技术栈**：

```yaml
高性能集群网络栈:
  CNI: Cilium (eBPF)
  Service: ClusterIP + LoadBalancer
  Ingress: Nginx Ingress
  网络策略: Cilium NetworkPolicy (L7)
  负载均衡: Cilium eBPF + IPVS
  服务发现: CoreDNS
  说明: 极高性能，eBPF 内核旁路
```

## 21.13 网络接口规范

### 21.13.1 CNI 接口规范

**CNI 接口规范**：

| 接口      | 定义     | 输入                  | 输出     |
| --------- | -------- | --------------------- | -------- |
| **ADD**   | 添加网络 | 容器 ID、网络命名空间 | 接口配置 |
| **DEL**   | 删除网络 | 容器 ID、网络命名空间 | 无       |
| **CHECK** | 检查网络 | 容器 ID、网络命名空间 | 状态     |

### 21.13.2 Service API 规范

**Service API 规范**：

| API               | 版本 | 功能                       |
| ----------------- | ---- | -------------------------- |
| **Service**       | v1   | 服务发现、负载均衡         |
| **EndpointSlice** | v1   | 端点集合（替代 Endpoints） |

### 21.13.3 Ingress API 规范

**Ingress API 规范**：

| API              | 版本                 | 功能               |
| ---------------- | -------------------- | ------------------ |
| **Ingress**      | networking.k8s.io/v1 | HTTP/HTTPS 路由    |
| **IngressClass** | networking.k8s.io/v1 | Ingress 控制器类型 |

## 21.14 参考

> CNI 规范见 [CNI 规范](https://github.com/containernetworking/cni) Kubernetes
> 网络见
> [Kubernetes 网络](https://kubernetes.io/docs/concepts/services-networking/)
> Service API 见
> [Service API](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/)
> 完整参考列表见 [REFERENCES.md](../REFERENCES.md)
