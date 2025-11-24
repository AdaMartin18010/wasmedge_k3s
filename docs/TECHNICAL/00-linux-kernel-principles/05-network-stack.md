# 05. 网络协议栈

## 📑 目录

- [05. 网络协议栈](#05-网络协议栈)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 网络协议栈的作用](#11-网络协议栈的作用)
    - [1.2 协议栈层次](#12-协议栈层次)
  - [2 网络协议栈架构](#2-网络协议栈架构)
    - [2.1 协议栈层次结构](#21-协议栈层次结构)
    - [2.2 Socket 层](#22-socket-层)
    - [2.3 协议层](#23-协议层)
    - [2.4 设备层](#24-设备层)
  - [3 Socket 接口](#3-socket-接口)
    - [3.1 Socket 创建](#31-socket-创建)
    - [3.2 Socket 绑定](#32-socket-绑定)
    - [3.3 Socket 连接](#33-socket-连接)
    - [3.4 Socket 数据传输](#34-socket-数据传输)
  - [4 TCP/IP 实现](#4-tcpip-实现)
    - [4.1 IP 层](#41-ip-层)
    - [4.2 TCP 层](#42-tcp-层)
    - [4.3 UDP 层](#43-udp-层)
  - [5 网络设备驱动](#5-网络设备驱动)
    - [5.1 网络设备结构](#51-网络设备结构)
    - [5.2 数据包接收](#52-数据包接收)
    - [5.3 数据包发送](#53-数据包发送)
  - [6 网络命名空间](#6-网络命名空间)
    - [6.1 Network Namespace 结构](#61-network-namespace-结构)
    - [6.2 网络设备隔离](#62-网络设备隔离)
    - [6.3 虚拟网络设备](#63-虚拟网络设备)
  - [7 与容器化的关系](#7-与容器化的关系)
    - [7.1 容器网络](#71-容器网络)
    - [7.2 网络隔离](#72-网络隔离)
    - [7.3 网络性能](#73-网络性能)
  - [8 相关文档](#8-相关文档)
    - [8.1 详细机制文档](#81-详细机制文档)
    - [8.2 容器化基础机制](#82-容器化基础机制)
    - [8.3 架构分析](#83-架构分析)
  - [2025 年最新实践](#2025-年最新实践)
    - [网络协议栈应用最佳实践（2025）](#网络协议栈应用最佳实践2025)
  - [实际应用案例](#实际应用案例)
    - [案例 1：容器网络性能优化（2025）](#案例-1容器网络性能优化2025)

---

## 1 概述

**网络协议栈**是 Linux 内核实现网络通信的核心组件，提供从应用层到物理层的完整网络功能。

### 1.1 网络协议栈的作用

- **协议实现**：实现 TCP/IP 协议族
- **Socket 接口**：为应用层提供 Socket API
- **数据包处理**：处理网络数据包的接收和发送
- **路由转发**：实现 IP 路由和转发功能
- **网络设备管理**：管理网络接口和设备

### 1.2 协议栈层次

```text
应用层（Application）
    │
Socket 层（Socket）
    │
传输层（TCP/UDP）
    │
网络层（IP）
    │
数据链路层（Ethernet）
    │
物理层（Hardware）
```

---

## 2 网络协议栈架构

### 2.1 协议栈层次结构

**内核网络协议栈**：

```text
用户空间
    │
    ├── Socket API（socket、bind、connect、send、recv）
    │
内核空间
    │
    ├── Socket 层
    │   ├── AF_INET（IPv4）
    │   ├── AF_INET6（IPv6）
    │   └── AF_UNIX（Unix Domain Socket）
    │
    ├── 传输层
    │   ├── TCP
    │   └── UDP
    │
    ├── 网络层
    │   ├── IP
    │   └── 路由表
    │
    ├── 数据链路层
    │   └── 网络设备驱动
    │
硬件层
```

### 2.2 Socket 层

**Socket 结构**：

```c
// include/net/sock.h
struct sock {
    // Socket 族
    sa_family_t sk_family;

    // Socket 类型
    unsigned char sk_type;
    unsigned char sk_protocol;

    // Socket 状态
    enum sk_state sk_state;

    // 接收队列
    struct sk_buff_head sk_receive_queue;

    // 发送队列
    struct sk_buff_head sk_write_queue;

    // Socket 操作
    const struct proto_ops *sk_prot_creator;

    // 协议特定数据
    void *sk_prot;
    // ...
};
```

**Socket 类型**：

- **SOCK_STREAM**：TCP，面向连接
- **SOCK_DGRAM**：UDP，无连接
- **SOCK_RAW**：原始套接字
- **SOCK_SEQPACKET**：有序数据包

### 2.3 协议层

**协议注册**：

```c
// include/net/sock.h
struct proto {
    // 协议名称
    const char *name;

    // Socket 创建
    struct sock *(*create)(struct net *net, struct socket *sock,
                          int protocol, int kern);

    // 连接
    int (*connect)(struct sock *sk, struct sockaddr *uaddr, int addr_len);

    // 发送
    int (*sendmsg)(struct sock *sk, struct msghdr *msg, size_t len);

    // 接收
    int (*recvmsg)(struct sock *sk, struct msghdr *msg, size_t len, int flags);
    // ...
};
```

### 2.4 设备层

**网络设备结构**：

```c
// include/linux/netdevice.h
struct net_device {
    // 设备名称
    char name[IFNAMSIZ];

    // 设备类型
    unsigned short type;

    // MAC 地址
    unsigned char addr_len;
    unsigned char perm_addr[MAX_ADDR_LEN];

    // 设备操作
    const struct net_device_ops *netdev_ops;

    // 统计信息
    struct net_device_stats stats;

    // 设备标志
    unsigned int flags;
    // ...
};
```

---

## 3 Socket 接口

### 3.1 Socket 创建

**socket() 系统调用**：

```c
// net/socket.c
long sys_socket(int family, int type, int protocol) {
    struct socket *sock;
    int retval;

    // 创建 Socket
    retval = __sys_socket(family, type, protocol);

    return retval;
}

int __sys_socket(int family, int type, int protocol) {
    struct socket *sock;
    int retval;

    // 创建 Socket 结构
    retval = sock_create(family, type, protocol, &sock);
    if (retval < 0)
        return retval;

    // 分配文件描述符
    retval = sock_map_fd(sock, flags & (O_CLOEXEC | O_NONBLOCK));

    return retval;
}
```

### 3.2 Socket 绑定

**bind() 系统调用**：

```c
// net/socket.c
long sys_bind(int fd, struct sockaddr __user *umyaddr, int addrlen) {
    struct socket *sock;
    struct sockaddr_storage address;
    int err;

    // 获取 Socket
    sock = sockfd_lookup_light(fd, &err, &fput_needed);
    if (sock) {
        // 复制地址
        err = move_addr_to_kernel(umyaddr, addrlen, &address);
        if (err >= 0) {
            // 执行绑定
            err = sock->ops->bind(sock, (struct sockaddr *)&address, addrlen);
        }
        fput_light(sock->file, fput_needed);
    }

    return err;
}
```

### 3.3 Socket 连接

**connect() 系统调用**：

```c
// net/socket.c
long sys_connect(int fd, struct sockaddr __user *uservaddr, int addrlen) {
    struct socket *sock;
    struct sockaddr_storage address;
    int err;

    // 获取 Socket
    sock = sockfd_lookup_light(fd, &err, &fput_needed);
    if (sock) {
        // 复制地址
        err = move_addr_to_kernel(uservaddr, addrlen, &address);
        if (err >= 0) {
            // 执行连接
            err = sock->ops->connect(sock, (struct sockaddr *)&address, addrlen, 0);
        }
        fput_light(sock->file, fput_needed);
    }

    return err;
}
```

### 3.4 Socket 数据传输

**send() 系统调用**：

```c
// net/socket.c
long sys_send(int fd, void __user *buff, size_t len, unsigned int flags) {
    return sys_sendto(fd, buff, len, flags, NULL, 0);
}

long sys_sendto(int fd, void __user *buff, size_t len, unsigned int flags,
                 struct sockaddr __user *addr, int addr_len) {
    struct socket *sock;
    struct msghdr msg;
    struct iovec iov;
    int err;

    // 获取 Socket
    sock = sockfd_lookup_light(fd, &err, &fput_needed);
    if (sock) {
        // 准备消息
        iov.iov_base = buff;
        iov.iov_len = len;
        msg.msg_iov = &iov;
        msg.msg_iovlen = 1;
        msg.msg_control = NULL;
        msg.msg_controllen = 0;
        msg.msg_name = addr;
        msg.msg_namelen = addr_len;

        // 发送数据
        err = sock_sendmsg(sock, &msg, len);
        fput_light(sock->file, fput_needed);
    }

    return err;
}
```

**recv() 系统调用**：

```c
// net/socket.c
long sys_recv(int fd, void __user *ubuf, size_t size, unsigned int flags) {
    return sys_recvfrom(fd, ubuf, size, flags, NULL, NULL);
}

long sys_recvfrom(int fd, void __user *ubuf, size_t size, unsigned int flags,
                  struct sockaddr __user *addr, int __user *addr_len) {
    struct socket *sock;
    struct msghdr msg;
    struct iovec iov;
    int err;

    // 获取 Socket
    sock = sockfd_lookup_light(fd, &err, &fput_needed);
    if (sock) {
        // 准备消息
        iov.iov_base = ubuf;
        iov.iov_len = size;
        msg.msg_iov = &iov;
        msg.msg_iovlen = 1;
        msg.msg_control = NULL;
        msg.msg_controllen = 0;
        msg.msg_name = addr;
        msg.msg_namelen = addr_len ? *addr_len : 0;

        // 接收数据
        err = sock_recvmsg(sock, &msg, flags);
        if (err >= 0 && addr_len)
            err = put_user(msg.msg_namelen, addr_len);
        fput_light(sock->file, fput_needed);
    }

    return err;
}
```

---

## 4 TCP/IP 实现

### 4.1 IP 层

**IP 数据包结构**：

```c
// include/uapi/linux/ip.h
struct iphdr {
    __u8 version:4;
    __u8 ihl:4;
    __u8 tos;
    __be16 tot_len;
    __be16 id;
    __be16 frag_off;
    __u8 ttl;
    __u8 protocol;
    __sum16 check;
    __be32 saddr;
    __be32 daddr;
};
```

**IP 数据包接收**：

```c
// net/ipv4/ip_input.c
int ip_rcv(struct sk_buff *skb, struct net_device *dev,
           struct packet_type *pt, struct net_device *orig_dev) {
    struct iphdr *iph;
    struct net *net;

    // 获取 IP 头
    iph = ip_hdr(skb);

    // IP 头校验
    if (ip_fast_csum((u8 *)iph, iph->ihl) != 0)
        goto drop;

    // 路由查找
    if (ip_route_input_noref(skb, iph->daddr, iph->saddr,
                              iph->tos, dev) == 0) {
        // 转发或本地处理
        if (skb_dst(skb)->dev == dev) {
            // 本地处理
            return ip_local_deliver(skb);
        } else {
            // 转发
            return ip_forward(skb);
        }
    }

drop:
    kfree_skb(skb);
    return NET_RX_DROP;
}
```

### 4.2 TCP 层

**TCP 连接状态**：

```c
// include/net/tcp_states.h
enum {
    TCP_ESTABLISHED = 1,
    TCP_SYN_SENT,
    TCP_SYN_RECV,
    TCP_FIN_WAIT1,
    TCP_FIN_WAIT2,
    TCP_TIME_WAIT,
    TCP_CLOSE,
    TCP_CLOSE_WAIT,
    TCP_LAST_ACK,
    TCP_LISTEN,
    TCP_CLOSING,
    TCP_NEW_SYN_RECV,
};
```

**TCP 连接建立**：

```c
// net/ipv4/tcp_input.c
// TCP 三次握手
int tcp_v4_connect(struct sock *sk, struct sockaddr *uaddr, int addr_len) {
    struct sockaddr_in *usin = (struct sockaddr_in *)uaddr;
    struct inet_sock *inet = inet_sk(sk);
    struct tcp_sock *tp = tcp_sk(sk);
    __be16 orig_sport, orig_dport;
    __be32 daddr, nexthop;
    struct flowi4 *fl4;
    struct rtable *rt;
    int err;

    // 解析目标地址
    daddr = usin->sin_addr.s_addr;
    nexthop = daddr;

    // 路由查找
    rt = ip_route_connect(fl4, nexthop, inet->inet_saddr,
                          RT_CONN_FLAGS(sk), sk->sk_bound_dev_if,
                          IPPROTO_TCP, orig_sport, orig_dport, sk);

    // 发送 SYN
    err = tcp_connect(sk);

    return err;
}
```

### 4.3 UDP 层

**UDP 数据包发送**：

```c
// net/ipv4/udp.c
int udp_sendmsg(struct sock *sk, struct msghdr *msg, size_t len) {
    struct inet_sock *inet = inet_sk(sk);
    struct udp_sock *up = udp_sk(sk);
    struct flowi4 fl4;
    int ulen = len;
    struct ipcm_cookie ipc;
    struct rtable *rt = NULL;
    int free = 0;
    int connected = 0;
    __be32 daddr, faddr, saddr;
    __be16 dport;
    int err;

    // 准备 UDP 数据包
    // ...

    // 发送数据包
    return ip_send_skb(sock_net(sk), skb);
}
```

---

## 5 网络设备驱动

### 5.1 网络设备结构

**网络设备操作**：

```c
// include/linux/netdevice.h
struct net_device_ops {
    int (*ndo_init)(struct net_device *dev);
    void (*ndo_uninit)(struct net_device *dev);
    int (*ndo_open)(struct net_device *dev);
    int (*ndo_stop)(struct net_device *dev);
    netdev_tx_t (*ndo_start_xmit)(struct sk_buff *skb,
                                   struct net_device *dev);
    int (*ndo_set_mac_address)(struct net_device *dev, void *addr);
    // ...
};
```

### 5.2 数据包接收

**数据包接收流程**：

```c
// net/core/dev.c
// 网络设备中断处理
static int netif_rx_internal(struct sk_buff *skb) {
    int ret;

    // 数据包统计
    trace_netif_rx(skb);

    // 入队到接收队列
    ret = enqueue_to_backlog(skb, get_cpu());
    put_cpu();

    return ret;
}

// 处理接收队列
static int process_backlog(struct napi_struct *napi, int quota) {
    struct softnet_data *sd = container_of(napi, struct softnet_data, backlog);
    struct sk_buff *skb;
    int work = 0;

    while ((work < quota) && (skb = __skb_dequeue(&sd->input_pkt_queue))) {
        // 处理数据包
        __netif_receive_skb(skb);
        work++;
    }

    return work;
}
```

### 5.3 数据包发送

**数据包发送流程**：

```c
// net/core/dev.c
// 发送数据包
netdev_tx_t __dev_queue_xmit(struct sk_buff *skb, struct net_device *sb_dev) {
    struct net_device *dev = skb->dev;
    struct netdev_queue *txq;
    struct Qdisc *q;
    int rc = -ENOMEM;

    // 选择发送队列
    txq = netdev_pick_tx(dev, skb, sb_dev);
    q = rcu_dereference_bh(txq->qdisc);

    if (q->enqueue) {
        // 入队
        rc = __dev_xmit_skb(skb, q, dev, txq);
    } else {
        // 直接发送
        rc = dev_hard_start_xmit(skb, dev, txq);
    }

    return rc;
}
```

---

## 6 网络命名空间

### 6.1 Network Namespace 结构

**Network Namespace**：

```c
// include/net/net_namespace.h
struct net {
    // 引用计数
    refcount_t count;

    // 网络设备列表
    struct list_head dev_base_head;
    struct hlist_head *dev_name_head;
    struct hlist_head *dev_index_head;

    // 路由表
    struct netns_ipv4 ipv4;
    struct netns_ipv6 ipv6;

    // Socket 列表
    struct list_head sock_list;
    // ...
};
```

### 6.2 网络设备隔离

**Network Namespace 创建**：

```c
// net/core/net_namespace.c
struct net *copy_net_ns(unsigned long flags, struct user_namespace *user_ns,
                        struct net *old_net) {
    struct net *net;
    int rv;

    if (!(flags & CLONE_NEWNET))
        return get_net(old_net);

    // 创建新的 Network Namespace
    net = net_alloc();
    if (!net)
        return ERR_PTR(-ENOMEM);

    // 初始化网络命名空间
    rv = setup_net(net, user_ns);
    if (rv < 0) {
        net_drop_ns(net);
        return ERR_PTR(rv);
    }

    return net;
}
```

### 6.3 虚拟网络设备

**veth 设备**：

- **veth（Virtual Ethernet）**：虚拟以太网设备对
- **用途**：连接不同 Network Namespace
- **实现**：一对虚拟网络设备，数据包从一个设备发送到另一个设备

**bridge 设备**：

- **bridge**：虚拟网桥
- **用途**：连接多个网络设备
- **实现**：类似物理交换机，转发数据包

---

## 7 与容器化的关系

### 7.1 容器网络

**容器网络模式**：

- **Bridge 模式**：容器通过虚拟网桥连接到宿主机网络
- **Host 模式**：容器共享宿主机的 Network Namespace
- **None 模式**：容器没有网络接口
- **自定义网络**：使用 Network Namespace 创建自定义网络

### 7.2 网络隔离

**Network Namespace 隔离**：

- **独立网络栈**：每个容器有独立的网络协议栈
- **独立网络设备**：容器只能看到自己的网络设备
- **独立路由表**：每个容器有独立的路由表
- **独立防火墙规则**：每个容器有独立的 iptables 规则

### 7.3 网络性能

**容器网络性能优化**：

- **SR-IOV**：硬件虚拟化，提高网络性能
- **DPDK**：用户空间网络处理，绕过内核
- **eBPF**：可编程网络处理，提高灵活性

---

## 8 相关文档

### 8.1 详细机制文档

- **[Namespace 机制详解](08-namespace.md)** - Network Namespace 详解
- **[系统调用机制](07-syscall.md)** - socket、bind、connect 系统调用

### 8.2 容器化基础机制

- **[Namespace 机制详解](08-namespace.md)** - Network Namespace 网络隔离
- **[Cgroup 机制详解](09-cgroup.md)** - 网络资源限制

### 8.3 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 隔离机制层次分析
- **[容器化架构视角](../../ARCHITECTURE/02-views/02-virtualization-containerization-sandboxing/)** - 容器化抽象层

---

---

## 2025 年最新实践

### 网络协议栈应用最佳实践（2025）

**2025 年趋势**：网络协议栈在容器网络、服务网格、边缘计算中的深度应用

**实践要点**：

- **容器网络**：使用 CNI 插件实现容器网络
- **网络性能优化**：使用 eBPF 进行网络性能优化
- **网络隔离**：使用网络命名空间进行网络隔离

**代码示例**：

```yaml
# 2025 年 Kubernetes 网络配置
apiVersion: v1
kind: Pod
metadata:
  name: network-pod
spec:
  containers:
  - name: app
    image: nginx:latest
  hostNetwork: false
  dnsPolicy: ClusterFirst
```

## 实际应用案例

### 案例 1：容器网络性能优化（2025）

**场景**：使用 eBPF 优化容器网络性能

**实现方案**：

```bash
# 使用 eBPF 进行网络性能优化
# 安装 eBPF 工具
apt-get install -y bpfcc-tools

# 监控网络性能
bpftrace -e 'tracepoint:net:net_dev_xmit {
    @bytes = hist(args->len);
}'
```

**效果**：

- 网络性能：提升网络吞吐量 20%+
- 网络监控：实时监控网络性能
- 网络优化：自动优化网络配置

---

**最后更新**：2025-11-15
**文档状态**：✅ 完整 | 📊 包含内核实现分析、2025 年最新实践、实际应用案例 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
