# 22. 缩写词汇表：全面梳理

## 目录

- [目录](#目录)
- [22.1 文档定位](#221-文档定位)
- [22.2 编排与容器类缩写](#222-编排与容器类缩写)
  - [22.2.1 Kubernetes 相关](#2221-kubernetes-相关)
  - [22.2.2 容器运行时相关](#2222-容器运行时相关)
  - [22.2.3 存储相关](#2223-存储相关)
- [22.3 网络类缩写](#223-网络类缩写)
  - [22.3.1 网络接口与插件](#2231-网络接口与插件)
  - [22.3.2 网络协议](#2232-网络协议)
  - [22.3.3 网络服务](#2233-网络服务)
- [22.4 WebAssembly 类缩写](#224-webassembly-类缩写)
  - [22.4.1 Wasm 核心缩写](#2241-wasm-核心缩写)
  - [22.4.2 Wasm 运行时相关](#2242-wasm-运行时相关)
- [22.5 策略与安全类缩写](#225-策略与安全类缩写)
- [22.6 对象与资源类缩写](#226-对象与资源类缩写)
- [22.7 开发与运维类缩写](#227-开发与运维类缩写)
- [22.8 硬件与平台类缩写](#228-硬件与平台类缩写)
- [22.9 缩写词关系矩阵](#229-缩写词关系矩阵)
  - [22.9.1 编排类关系矩阵](#2291-编排类关系矩阵)
  - [22.9.2 运行时类关系矩阵](#2292-运行时类关系矩阵)
  - [22.9.3 网络类关系矩阵](#2293-网络类关系矩阵)
  - [22.9.4 策略类关系矩阵](#2294-策略类关系矩阵)
- [22.10 缩写词快速检索](#2210-缩写词快速检索)
  - [22.10.1 按字母顺序检索](#22101-按字母顺序检索)
  - [22.10.2 按分类检索](#22102-按分类检索)
- [22.11 参考](#2211-参考)

---

## 22.1 文档定位

本文档全面梳理云原生容器技术栈中所有使用的缩写词，包括完整形式、中文解释、概念关
系、使用场景和相关缩写词，帮助快速理解和查找技术术语。

**文档结构**：

- **编排与容器类缩写**：Kubernetes、容器运行时、存储相关缩写词
- **网络类缩写**：网络接口、协议、服务相关缩写词
- **WebAssembly 类缩写**：Wasm 核心和运行时相关缩写词
- **策略与安全类缩写**：OPA、安全相关缩写词
- **对象与资源类缩写**：Kubernetes 对象相关缩写词
- **开发与运维类缩写**：CI/CD、DevOps 相关缩写词
- **硬件与平台类缩写**：硬件和平台相关缩写词
- **缩写词关系矩阵**：缩写词之间的关联关系
- **缩写词快速检索**：按字母顺序快速查找

## 22.2 编排与容器类缩写

### 22.2.1 Kubernetes 相关

| 缩写                        | 完整形式                          | 中文解释                | 概念关系                  | 使用场景                    | 相关缩写                |
| --------------------------- | --------------------------------- | ----------------------- | ------------------------- | --------------------------- | ----------------------- |
| **K8s**                     | Kubernetes                        | Kubernetes 编排系统     | 容器编排平台              | 集群管理、容器编排          | K3s, CRI, CNI, CSI      |
| **K3s**                     | Kubernetes 轻量版                 | Kubernetes 轻量级版本   | K8s 的轻量版本            | 边缘计算、IoT、资源受限环境 | K8s, containerd         |
| **CRI**                     | Container Runtime Interface       | 容器运行时接口          | Kubernetes 运行时抽象接口 | 容器运行时管理              | containerd, CRI-O, runc |
| **CNI**                     | Container Network Interface       | 容器网络接口            | Kubernetes 网络抽象接口   | 网络插件管理                | Flannel, Calico, Cilium |
| **CSI**                     | Container Storage Interface       | 容器存储接口            | Kubernetes 存储抽象接口   | 存储插件管理                | PV, PVC, StorageClass   |
| **GVR**                     | Group/Version/Resource            | 组/版本/资源            | Kubernetes API 对象标识   | API 对象管理                | API, kubectl            |
| **API**                     | Application Programming Interface | 应用程序编程接口        | 系统间交互接口            | 所有系统交互                | REST, HTTP              |
| **etcd**                    | etcd                              | 分布式键值存储          | Kubernetes 状态存储       | 集群状态存储                | Raft, HA                |
| **kubelet**                 | kubelet                           | Kubernetes 节点代理     | 节点组件                  | Pod 管理、健康检查          | CRI, CNI, CSI           |
| **kube-proxy**              | kube-proxy                        | Kubernetes 网络代理     | 节点组件                  | 服务发现、负载均衡          | Service, iptables, IPVS |
| **kube-api-server**         | Kubernetes API Server             | Kubernetes API 网关     | 控制平面组件              | API 网关、对象验证          | etcd, kubectl           |
| **kube-controller-manager** | Kubernetes Controller Manager     | Kubernetes 控制器管理器 | 控制平面组件              | 控制器逻辑执行              | Controller, ReplicaSet  |
| **kube-scheduler**          | Kubernetes Scheduler              | Kubernetes 调度器       | 控制平面组件              | Pod 调度决策                | Pod, Node               |
| **PV**                      | Persistent Volume                 | 持久化存储卷            | Kubernetes 存储对象       | 数据持久化存储              | PVC, CSI                |
| **PVC**                     | Persistent Volume Claim           | 持久化存储卷声明        | Kubernetes 存储对象       | 存储请求声明                | PV, StorageClass        |
| **HA**                      | High Availability                 | 高可用性                | 系统可用性指标            | 集群高可用部署              | etcd, Raft              |

### 22.2.2 容器运行时相关

| 缩写           | 完整形式                          | 中文解释                 | 概念关系            | 使用场景             | 相关缩写                         |
| -------------- | --------------------------------- | ------------------------ | ------------------- | -------------------- | -------------------------------- |
| **OCI**        | Open Container Initiative         | 开放容器计划             | 容器标准规范组织    | 容器镜像和运行时标准 | OCI Image Spec, OCI Runtime Spec |
| **runc**       | runc                              | OCI 标准容器运行时       | Linux 容器运行时    | Docker 默认运行时    | OCI, containerd                  |
| **crun**       | crun                              | C 实现的 OCI 运行时      | 支持 Wasm 的运行时  | Wasm 容器运行时      | OCI, Wasm, runwasi               |
| **containerd** | containerd                        | 容器运行时守护进程       | 容器运行时管理      | Kubernetes CRI 实现  | CRI, runc, OCI                   |
| **CRI-O**      | Container Runtime Interface - OCI | CRI 的 OCI 实现          | Kubernetes CRI 实现 | 轻量级 CRI 实现      | CRI, OCI                         |
| **runwasi**    | runwasi                           | Wasm shim for containerd | Wasm CRI 集成       | Wasm CRI 支持        | containerd, Wasm, CRI            |
| **shim**       | shim                              | 适配层                   | 容器生命周期管理    | 容器进程管理         | containerd, runc                 |
| **CNM**        | Container Network Model           | Docker 网络模型          | Docker 网络抽象     | Docker 网络管理      | Docker, Network                  |

### 22.2.3 存储相关

| 缩写             | 完整形式            | 中文解释     | 概念关系            | 使用场景          | 相关缩写         |
| ---------------- | ------------------- | ------------ | ------------------- | ----------------- | ---------------- |
| **StorageClass** | StorageClass        | 存储类       | Kubernetes 存储抽象 | 动态存储分配      | PV, PVC, CSI     |
| **OverlayFS**    | Overlay File System | 叠加文件系统 | 容器镜像存储驱动    | Docker 镜像层存储 | Docker, overlay2 |
| **VFS**          | Virtual File System | 虚拟文件系统 | 文件系统抽象层      | 文件系统接口      | Linux            |

## 22.3 网络类缩写

### 22.3.1 网络接口与插件

| 缩写         | 完整形式                        | 中文解释             | 概念关系        | 使用场景              | 相关缩写                 |
| ------------ | ------------------------------- | -------------------- | --------------- | --------------------- | ------------------------ |
| **Flannel**  | Flannel                         | CNI 网络插件         | 简单覆盖网络    | 小型集群网络          | CNI, VXLAN               |
| **Calico**   | Calico                          | CNI 网络插件         | BGP 路由网络    | 大规模集群网络        | CNI, BGP, NetworkPolicy  |
| **Cilium**   | Cilium                          | CNI 网络插件         | eBPF 高性能网络 | 高性能网络和安全      | CNI, eBPF, NetworkPolicy |
| **iptables** | iptables                        | Linux 防火墙工具     | 网络包过滤      | kube-proxy 负载均衡   | kube-proxy, Service      |
| **IPVS**     | IP Virtual Server               | IP 虚拟服务器        | 高性能负载均衡  | kube-proxy 高性能模式 | kube-proxy, Service      |
| **VXLAN**    | Virtual Extensible LAN          | 虚拟可扩展局域网     | 覆盖网络协议    | 跨主机容器网络        | Flannel, CNI             |
| **BGP**      | Border Gateway Protocol         | 边界网关协议         | 路由协议        | Calico 网络路由       | Calico, CNI              |
| **eBPF**     | extended Berkeley Packet Filter | 扩展的伯克利包过滤器 | 内核可编程接口  | Cilium 高性能网络     | Cilium, Linux            |

### 22.3.2 网络协议

| 缩写      | 完整形式                      | 中文解释           | 概念关系        | 使用场景           | 相关缩写             |
| --------- | ----------------------------- | ------------------ | --------------- | ------------------ | -------------------- |
| **HTTP**  | HyperText Transfer Protocol   | 超文本传输协议     | 应用层协议      | Web 服务           | HTTPS, REST          |
| **HTTPS** | HTTP Secure                   | 安全超文本传输协议 | HTTP 的安全版本 | 加密 Web 服务      | HTTP, TLS, SSL       |
| **TCP**   | Transmission Control Protocol | 传输控制协议       | 传输层协议      | 可靠数据传输       | UDP, IP              |
| **UDP**   | User Datagram Protocol        | 用户数据报协议     | 传输层协议      | 快速数据传输       | TCP, IP              |
| **IP**    | Internet Protocol             | 互联网协议         | 网络层协议      | 网络路由           | TCP, UDP, IPv4, IPv6 |
| **DNS**   | Domain Name System            | 域名系统           | 域名解析服务    | 服务发现           | Service, CoreDNS     |
| **TLS**   | Transport Layer Security      | 传输层安全         | 安全传输协议    | 加密通信           | HTTPS, SSL           |
| **SSL**   | Secure Sockets Layer          | 安全套接层         | 安全传输协议    | 加密通信（已弃用） | TLS, HTTPS           |

### 22.3.3 网络服务

| 缩写              | 完整形式      | 中文解释            | 概念关系            | 使用场景           | 相关缩写                          |
| ----------------- | ------------- | ------------------- | ------------------- | ------------------ | --------------------------------- |
| **Service**       | Service       | Kubernetes 服务对象 | 服务抽象            | 服务发现和负载均衡 | ClusterIP, NodePort, LoadBalancer |
| **Ingress**       | Ingress       | Kubernetes 入口对象 | L7 负载均衡         | HTTP/HTTPS 路由    | Ingress Controller, TLS           |
| **ClusterIP**     | Cluster IP    | 集群内部 IP         | Service 类型        | 集群内部服务访问   | Service, kube-proxy               |
| **NodePort**      | Node Port     | 节点端口            | Service 类型        | 节点外部访问       | Service, kube-proxy               |
| **LoadBalancer**  | Load Balancer | 负载均衡器          | Service 类型        | 云平台负载均衡     | Service, Cloud                    |
| **ExternalName**  | External Name | 外部名称            | Service 类型        | 外部服务映射       | Service, DNS                      |
| **CoreDNS**       | CoreDNS       | Kubernetes DNS 服务 | DNS 服务器          | 集群 DNS 解析      | DNS, Service                      |
| **NetworkPolicy** | NetworkPolicy | 网络策略            | Kubernetes 网络策略 | 网络隔离和访问控制 | Calico, Cilium, CNI               |

## 22.4 WebAssembly 类缩写

### 22.4.1 Wasm 核心缩写

| 缩写         | 完整形式                     | 中文解释             | 概念关系          | 使用场景         | 相关缩写           |
| ------------ | ---------------------------- | -------------------- | ----------------- | ---------------- | ------------------ |
| **Wasm**     | WebAssembly                  | Web 汇编             | 字节码格式        | 跨平台字节码执行 | WasmEdge, WASI     |
| **WASI**     | WebAssembly System Interface | WebAssembly 系统接口 | Wasm 系统调用接口 | Wasm 系统调用    | Wasm, WasmEdge     |
| **WASI-NN**  | WASI Neural Network          | WASI 神经网络接口    | Wasm AI 推理接口  | Wasm AI 推理     | Wasm, WasmEdge, AI |
| **WasmEdge** | WasmEdge                     | WebAssembly 运行时   | Wasm 执行引擎     | Wasm 字节码执行  | Wasm, WASI, crun   |
| **WAT**      | WebAssembly Text             | WebAssembly 文本格式 | Wasm 文本表示     | Wasm 开发调试    | Wasm, WAST         |

### 22.4.2 Wasm 运行时相关

| 缩写        | 完整形式 | 中文解释                 | 概念关系           | 使用场景             | 相关缩写              |
| ----------- | -------- | ------------------------ | ------------------ | -------------------- | --------------------- |
| **runwasi** | runwasi  | Wasm shim for containerd | Wasm CRI 集成      | Kubernetes Wasm 支持 | containerd, Wasm, CRI |
| **crun**    | crun     | C 实现的 OCI 运行时      | 支持 Wasm 的运行时 | Wasm 容器运行时      | OCI, Wasm, runwasi    |

## 22.5 策略与安全类缩写

| 缩写           | 完整形式                                 | 中文解释              | 概念关系         | 使用场景            | 相关缩写                  |
| -------------- | ---------------------------------------- | --------------------- | ---------------- | ------------------- | ------------------------- |
| **OPA**        | Open Policy Agent                        | 开放策略代理          | 策略引擎         | 策略即代码          | Rego, Gatekeeper, Kyverno |
| **Rego**       | Rego                                     | OPA 策略语言          | 声明式策略语言   | 策略定义            | OPA, Policy               |
| **OPA-Wasm**   | OPA WebAssembly                          | OPA Wasm 编译版本     | OPA Wasm 编译    | 低延迟策略执行      | OPA, Wasm, Rego           |
| **Gatekeeper** | Gatekeeper                               | Kubernetes 准入控制器 | OPA 的 K8s 集成  | Kubernetes 策略执行 | OPA, Admission Control    |
| **Kyverno**    | Kyverno                                  | Kubernetes 策略引擎   | K8s 原生策略引擎 | Kubernetes 策略管理 | Policy, Kubernetes        |
| **RBAC**       | Role-Based Access Control                | 基于角色的访问控制    | 访问控制模型     | 权限管理            | Kubernetes, API           |
| **TLS**        | Transport Layer Security                 | 传输层安全            | 安全传输协议     | 加密通信            | HTTPS, SSL                |
| **SSL**        | Secure Sockets Layer                     | 安全套接层            | 安全传输协议     | 加密通信（已弃用）  | TLS, HTTPS                |
| **mTLS**       | Mutual TLS                               | 双向 TLS              | 双向认证         | 服务间安全通信      | TLS, Service Mesh         |
| **FIPS**       | Federal Information Processing Standards | 联邦信息处理标准      | 加密标准         | 合规性要求          | Security, Compliance      |

## 22.6 对象与资源类缩写

| 缩写            | 完整形式    | 中文解释                    | 概念关系       | 使用场景       | 相关缩写               |
| --------------- | ----------- | --------------------------- | -------------- | -------------- | ---------------------- |
| **Pod**         | Pod         | Kubernetes Pod 对象         | 最小调度单元   | 容器组运行     | Deployment, ReplicaSet |
| **Deployment**  | Deployment  | Kubernetes Deployment 对象  | 应用部署对象   | 应用部署和管理 | Pod, ReplicaSet        |
| **ReplicaSet**  | ReplicaSet  | Kubernetes ReplicaSet 对象  | Pod 副本集     | Pod 副本管理   | Deployment, Pod        |
| **StatefulSet** | StatefulSet | Kubernetes StatefulSet 对象 | 有状态应用部署 | 有状态应用管理 | Pod, PVC               |
| **DaemonSet**   | DaemonSet   | Kubernetes DaemonSet 对象   | 守护进程集     | 节点级应用部署 | Pod, Node              |
| **ConfigMap**   | ConfigMap   | Kubernetes ConfigMap 对象   | 配置对象       | 应用配置管理   | Pod, Secret            |
| **Secret**      | Secret      | Kubernetes Secret 对象      | 密钥对象       | 敏感信息管理   | Pod, ConfigMap         |
| **Job**         | Job         | Kubernetes Job 对象         | 任务对象       | 一次性任务执行 | Pod, CronJob           |
| **CronJob**     | CronJob     | Kubernetes CronJob 对象     | 定时任务对象   | 定时任务执行   | Job, Pod               |
| **Namespace**   | Namespace   | Kubernetes Namespace 对象   | 命名空间       | 资源隔离       | Pod, Service           |
| **Label**       | Label       | Kubernetes Label            | 标签           | 对象标识和选择 | Selector, Service      |
| **Selector**    | Selector    | Kubernetes Selector         | 选择器         | 对象选择       | Label, Service         |

## 22.7 开发与运维类缩写

| 缩写        | 完整形式                                       | 中文解释              | 概念关系       | 使用场景         | 相关缩写         |
| ----------- | ---------------------------------------------- | --------------------- | -------------- | ---------------- | ---------------- |
| **CI/CD**   | Continuous Integration / Continuous Deployment | 持续集成/持续部署     | DevOps 实践    | 自动化构建和部署 | Git, Docker, K8s |
| **CI**      | Continuous Integration                         | 持续集成              | 自动化构建     | 代码集成测试     | Git, Docker      |
| **CD**      | Continuous Deployment                          | 持续部署              | 自动化部署     | 应用自动部署     | CI, K8s          |
| **DevOps**  | Development and Operations                     | 开发运维              | 软件开发方法   | 开发和运维协作   | CI/CD, Git       |
| **Git**     | Git                                            | 版本控制系统          | 代码版本管理   | 源代码管理       | GitHub, GitLab   |
| **YAML**    | YAML Ain't Markup Language                     | YAML 标记语言         | 配置文件格式   | Kubernetes 配置  | K8s, ConfigMap   |
| **JSON**    | JavaScript Object Notation                     | JSON 数据格式         | 数据交换格式   | API 数据格式     | API, REST        |
| **REST**    | Representational State Transfer                | 表述性状态转移        | API 架构风格   | RESTful API      | API, HTTP        |
| **RESTful** | RESTful                                        | REST 风格             | REST API 实现  | REST API 设计    | REST, API        |
| **API**     | Application Programming Interface              | 应用程序编程接口      | 系统间交互接口 | 所有系统交互     | REST, HTTP       |
| **SDK**     | Software Development Kit                       | 软件开发工具包        | 开发工具集     | 应用开发         | API, Client      |
| **CLI**     | Command Line Interface                         | 命令行接口            | 命令行工具     | 系统管理         | kubectl, docker  |
| **kubectl** | kubectl                                        | Kubernetes 命令行工具 | K8s 管理工具   | Kubernetes 管理  | K8s, API         |

## 22.8 硬件与平台类缩写

| 缩写           | 完整形式                    | 中文解释       | 概念关系         | 使用场景             | 相关缩写           |
| -------------- | --------------------------- | -------------- | ---------------- | -------------------- | ------------------ |
| **CPU**        | Central Processing Unit     | 中央处理器     | 计算机处理器     | 计算资源             | Memory, GPU        |
| **GPU**        | Graphics Processing Unit    | 图形处理器     | 图形计算处理器   | AI 推理、图形计算    | AI, CUDA           |
| **ARM**        | Advanced RISC Machine       | ARM 架构       | 处理器架构       | 边缘设备、移动设备   | IoT, Edge          |
| **x86**        | x86                         | x86 架构       | 处理器架构       | 服务器、PC           | Intel, AMD         |
| **IoT**        | Internet of Things          | 物联网         | 物联网设备       | 边缘计算、IoT 应用   | Edge, K3s          |
| **MEC**        | Multi-access Edge Computing | 多接入边缘计算 | 边缘计算架构     | 5G 边缘计算          | Edge, 5G           |
| **5G**         | 5th Generation              | 第五代移动通信 | 移动通信技术     | 5G 网络              | MEC, Edge          |
| **FaaS**       | Function as a Service       | 函数即服务     | 无服务器计算模型 | Serverless 函数      | Serverless, Lambda |
| **Serverless** | Serverless                  | 无服务器       | 云计算模型       | 按需执行、自动扩缩容 | FaaS, Lambda       |
| **SaaS**       | Software as a Service       | 软件即服务     | 云计算服务模型   | 软件服务提供         | Cloud, Service     |
| **PaaS**       | Platform as a Service       | 平台即服务     | 云计算服务模型   | 平台服务提供         | Cloud, K8s         |
| **IaaS**       | Infrastructure as a Service | 基础设施即服务 | 云计算服务模型   | 基础设施提供         | Cloud, VM          |

## 22.9 缩写词关系矩阵

### 22.9.1 编排类关系矩阵

| 缩写    | 所属层次 | 直接关系                | 间接关系                 | 依赖关系           |
| ------- | -------- | ----------------------- | ------------------------ | ------------------ |
| **K8s** | 编排层   | K3s, CRI, CNI, CSI      | Pod, Service, Deployment | Docker, containerd |
| **K3s** | 编排层   | K8s, containerd         | Pod, Service, CNI        | runc, Flannel      |
| **CRI** | 接口层   | containerd, CRI-O, runc | Pod, kubelet             | OCI                |
| **CNI** | 接口层   | Flannel, Calico, Cilium | Service, NetworkPolicy   | iptables, IPVS     |
| **CSI** | 接口层   | PV, PVC, StorageClass   | Pod, StatefulSet         | Storage            |

### 22.9.2 运行时类关系矩阵

| 缩写           | 所属层次 | 直接关系               | 间接关系       | 依赖关系         |
| -------------- | -------- | ---------------------- | -------------- | ---------------- |
| **OCI**        | 标准层   | runc, crun, containerd | Docker, K8s    | Linux            |
| **runc**       | 运行时层 | OCI, containerd        | Docker, K8s    | Linux, Namespace |
| **containerd** | 运行时层 | CRI, runc, OCI         | K8s, Docker    | Linux            |
| **Wasm**       | 运行时层 | WasmEdge, WASI         | OPA-Wasm, crun | WebAssembly      |
| **WasmEdge**   | 运行时层 | Wasm, WASI, WASI-NN    | runwasi, crun  | WebAssembly      |

### 22.9.3 网络类关系矩阵

| 缩写        | 所属层次 | 直接关系                          | 间接关系               | 依赖关系      |
| ----------- | -------- | --------------------------------- | ---------------------- | ------------- |
| **CNI**     | 接口层   | Flannel, Calico, Cilium           | Service, NetworkPolicy | Linux Network |
| **Service** | 对象层   | ClusterIP, NodePort, LoadBalancer | kube-proxy, DNS        | CNI           |
| **Ingress** | 对象层   | Ingress Controller, TLS           | Service, HTTP          | CNI           |
| **DNS**     | 服务层   | CoreDNS, Service                  | Pod, Namespace         | CNI           |

### 22.9.4 策略类关系矩阵

| 缩写         | 所属层次 | 直接关系                  | 间接关系                  | 依赖关系   |
| ------------ | -------- | ------------------------- | ------------------------- | ---------- |
| **OPA**      | 策略层   | Rego, Gatekeeper, Kyverno | Admission Control, Policy | Kubernetes |
| **Rego**     | 语言层   | OPA, OPA-Wasm             | Policy, Rule              | OPA        |
| **OPA-Wasm** | 策略层   | OPA, Wasm, Rego           | Admission Control         | WasmEdge   |

## 22.10 缩写词快速检索

### 22.10.1 按字母顺序检索

**A**:

- **API**: Application Programming Interface - 应用程序编程接口
- **ARM**: Advanced RISC Machine - ARM 架构

**B**:

- **BGP**: Border Gateway Protocol - 边界网关协议

**C**:

- **Calico**: Calico - CNI 网络插件
- **CD**: Continuous Deployment - 持续部署
- **CI**: Continuous Integration - 持续集成
- **CI/CD**: Continuous Integration / Continuous Deployment - 持续集成/持续部署
- **Cilium**: Cilium - CNI 网络插件
- **CLI**: Command Line Interface - 命令行接口
- **ClusterIP**: Cluster IP - 集群内部 IP
- **CNI**: Container Network Interface - 容器网络接口
- **CNM**: Container Network Model - Docker 网络模型
- **ConfigMap**: ConfigMap - Kubernetes ConfigMap 对象
- **containerd**: containerd - 容器运行时守护进程
- **Controller**: Controller - Kubernetes 控制器
- **CoreDNS**: CoreDNS - Kubernetes DNS 服务
- **CPU**: Central Processing Unit - 中央处理器
- **CRI**: Container Runtime Interface - 容器运行时接口
- **CRI-O**: Container Runtime Interface - OCI - CRI 的 OCI 实现
- **crun**: crun - C 实现的 OCI 运行时
- **CSI**: Container Storage Interface - 容器存储接口
- **CronJob**: CronJob - Kubernetes CronJob 对象

**D**:

- **DaemonSet**: DaemonSet - Kubernetes DaemonSet 对象
- **Deployment**: Deployment - Kubernetes Deployment 对象
- **DevOps**: Development and Operations - 开发运维
- **DNS**: Domain Name System - 域名系统
- **Docker**: Docker - 容器化平台

**E**:

- **eBPF**: extended Berkeley Packet Filter - 扩展的伯克利包过滤器
- **etcd**: etcd - 分布式键值存储
- **ExternalName**: External Name - 外部名称

**F**:

- **FaaS**: Function as a Service - 函数即服务
- **FIPS**: Federal Information Processing Standards - 联邦信息处理标准
- **Flannel**: Flannel - CNI 网络插件

**G**:

- **Gatekeeper**: Gatekeeper - Kubernetes 准入控制器
- **Git**: Git - 版本控制系统
- **GPU**: Graphics Processing Unit - 图形处理器
- **GVR**: Group/Version/Resource - 组/版本/资源

**H**:

- **HA**: High Availability - 高可用性
- **HTTP**: HyperText Transfer Protocol - 超文本传输协议
- **HTTPS**: HTTP Secure - 安全超文本传输协议

**I**:

- **IaaS**: Infrastructure as a Service - 基础设施即服务
- **Ingress**: Ingress - Kubernetes 入口对象
- **IoT**: Internet of Things - 物联网
- **IP**: Internet Protocol - 互联网协议
- **IPVS**: IP Virtual Server - IP 虚拟服务器
- **iptables**: iptables - Linux 防火墙工具

**J**:

- **Job**: Job - Kubernetes Job 对象
- **JSON**: JavaScript Object Notation - JSON 数据格式

**K**:

- **K3s**: Kubernetes 轻量版 - Kubernetes 轻量级版本
- **K8s**: Kubernetes - Kubernetes 编排系统
- **kube-api-server**: Kubernetes API Server - Kubernetes API 网关
- **kube-controller-manager**: Kubernetes Controller Manager - Kubernetes 控制器
  管理器
- **kube-proxy**: kube-proxy - Kubernetes 网络代理
- **kube-scheduler**: Kubernetes Scheduler - Kubernetes 调度器
- **kubelet**: kubelet - Kubernetes 节点代理
- **kubectl**: kubectl - Kubernetes 命令行工具
- **Kyverno**: Kyverno - Kubernetes 策略引擎

**L**:

- **Label**: Label - Kubernetes Label
- **LoadBalancer**: Load Balancer - 负载均衡器

**M**:

- **MEC**: Multi-access Edge Computing - 多接入边缘计算
- **mTLS**: Mutual TLS - 双向 TLS

**N**:

- **Namespace**: Namespace - Kubernetes Namespace 对象
- **NetworkPolicy**: NetworkPolicy - 网络策略
- **NodePort**: Node Port - 节点端口

**O**:

- **OCI**: Open Container Initiative - 开放容器计划
- **OPA**: Open Policy Agent - 开放策略代理
- **OPA-Wasm**: OPA WebAssembly - OPA Wasm 编译版本
- **OverlayFS**: Overlay File System - 叠加文件系统

**P**:

- **PaaS**: Platform as a Service - 平台即服务
- **Pod**: Pod - Kubernetes Pod 对象
- **PVC**: Persistent Volume Claim - 持久化存储卷声明
- **PV**: Persistent Volume - 持久化存储卷

**R**:

- **RBAC**: Role-Based Access Control - 基于角色的访问控制
- **Rego**: Rego - OPA 策略语言
- **ReplicaSet**: ReplicaSet - Kubernetes ReplicaSet 对象
- **REST**: Representational State Transfer - 表述性状态转移
- **RESTful**: RESTful - REST 风格
- **runc**: runc - OCI 标准容器运行时
- **runwasi**: runwasi - Wasm shim for containerd

**S**:

- **SaaS**: Software as a Service - 软件即服务
- **SDK**: Software Development Kit - 软件开发工具包
- **Secret**: Secret - Kubernetes Secret 对象
- **Selector**: Selector - Kubernetes Selector
- **Serverless**: Serverless - 无服务器
- **Service**: Service - Kubernetes 服务对象
- **shim**: shim - 适配层
- **SSL**: Secure Sockets Layer - 安全套接层
- **StatefulSet**: StatefulSet - Kubernetes StatefulSet 对象
- **StorageClass**: StorageClass - 存储类

**T**:

- **TCP**: Transmission Control Protocol - 传输控制协议
- **TLS**: Transport Layer Security - 传输层安全

**U**:

- **UDP**: User Datagram Protocol - 用户数据报协议

**V**:

- **VFS**: Virtual File System - 虚拟文件系统
- **VXLAN**: Virtual Extensible LAN - 虚拟可扩展局域网

**W**:

- **Wasm**: WebAssembly - Web 汇编
- **WasmEdge**: WasmEdge - WebAssembly 运行时
- **WASI**: WebAssembly System Interface - WebAssembly 系统接口
- **WASI-NN**: WASI Neural Network - WASI 神经网络接口
- **WAT**: WebAssembly Text - WebAssembly 文本格式

**X**:

- **x86**: x86 - x86 架构

**Y**:

- **YAML**: YAML Ain't Markup Language - YAML 标记语言

**5**:

- **5G**: 5th Generation - 第五代移动通信

### 22.10.2 按分类检索

**编排类**:

- K8s, K3s, CRI, CNI, CSI, GVR, API, etcd, kubelet, kube-proxy, kube-api-server,
  kube-controller-manager, kube-scheduler, PV, PVC, StorageClass, HA

**运行时类**:

- OCI, runc, crun, containerd, CRI-O, runwasi, shim, CNM

**网络类**:

- CNI, Flannel, Calico, Cilium, iptables, IPVS, VXLAN, BGP, eBPF, Service,
  Ingress, ClusterIP, NodePort, LoadBalancer, ExternalName, CoreDNS, DNS,
  NetworkPolicy, HTTP, HTTPS, TCP, UDP, IP, TLS, SSL, mTLS

**Wasm 类**:

- Wasm, WASI, WASI-NN, WasmEdge, WAT, runwasi, crun

**策略类**:

- OPA, Rego, OPA-Wasm, Gatekeeper, Kyverno, RBAC, FIPS

**对象类**:

- Pod, Deployment, ReplicaSet, StatefulSet, DaemonSet, ConfigMap, Secret, Job,
  CronJob, Namespace, Label, Selector

**开发运维类**:

- CI/CD, CI, CD, DevOps, Git, YAML, JSON, REST, RESTful, API, SDK, CLI, kubectl

**硬件平台类**:

- CPU, GPU, ARM, x86, IoT, MEC, 5G, FaaS, Serverless, SaaS, PaaS, IaaS

## 22.11 参考

- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [Docker 官方文档](https://docs.docker.com/)
- [OCI 规范](https://opencontainers.org/)
- [CNI 规范](https://github.com/containernetworking/cni)
- [CSI 规范](https://kubernetes-csi.github.io/docs/)
- [CRI 规范](https://github.com/kubernetes/cri-api)
- [WasmEdge 文档](https://wasmedge.org/docs/)
- [OPA 文档](https://www.openpolicyagent.org/docs/)
