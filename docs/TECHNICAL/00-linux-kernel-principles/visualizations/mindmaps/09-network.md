# 网络子系统详细思维导图

## 📑 目录

- [网络子系统详细思维导图](#网络子系统详细思维导图)
  - [📑 目录](#-目录)
  - [1 网络子系统全景](#1-网络子系统全景)
  - [2 Socket 层详细思维导图](#2-socket-层详细思维导图)
  - [3 网络协议栈详细思维导图](#3-网络协议栈详细思维导图)
  - [4 网络设备详细思维导图](#4-网络设备详细思维导图)

---

## 1 网络子系统全景

```mermaid
mindmap
  root((网络子系统))
    Socket 层
      Socket API
        socket()
        bind()
        listen()
        accept()
        connect()
        send/recv
      Socket 类型
        SOCK_STREAM
        SOCK_DGRAM
        SOCK_RAW
        Unix Domain Socket
      Socket 状态
        CLOSED
        LISTEN
        ESTABLISHED
        TIME_WAIT
    网络协议栈
      TCP/IP
        TCP
          可靠传输
          流量控制
          拥塞控制
        UDP
          快速传输
          无连接
        IP
          路由转发
          IP 地址
        ICMP
          控制消息
          ping
      HTTP/HTTPS
        应用层协议
        Web 服务
      gRPC
        RPC 服务
        微服务通信
    网络设备
      物理网卡
        网络接口
        硬件驱动
      虚拟设备
        veth
        bridge
        macvlan
        ipvlan
        vxlan
    网络性能
      零拷贝
        sendfile
        splice
        MSG_ZEROCOPY
      多队列
        RSS
        RPS
        XPS
      TCP 优化
        TCP_NODELAY
        TCP_CORK
        TCP_QUICKACK
    容器化应用
      Network Namespace
        网络隔离
        独立网络栈
        独立路由表
      容器网络
        Bridge 模式
        Host 模式
        Macvlan 模式
        Overlay 网络
```

---

## 2 Socket 层详细思维导图

```mermaid
mindmap
  root((Socket 层))
    Socket 创建
      socket()
        协议族
          AF_INET
          AF_INET6
          AF_UNIX
        Socket 类型
          SOCK_STREAM
          SOCK_DGRAM
          SOCK_RAW
        协议
          IPPROTO_TCP
          IPPROTO_UDP
    Socket 绑定
      bind()
        地址绑定
        IP 地址
        端口号
        权限检查
          CAP_NET_BIND_SERVICE
    Socket 监听
      listen()
        监听队列
        backlog
        SYN 队列
        ACCEPT 队列
    Socket 连接
      connect()
        TCP 三次握手
        连接建立
        超时处理
      accept()
        接受连接
        新 Socket 创建
    Socket 数据传输
      send()
        数据发送
        TCP 发送
        UDP 发送
        零拷贝
      recv()
        数据接收
        TCP 接收
        UDP 接收
        阻塞/非阻塞
    Socket 关闭
      close()
        连接关闭
        TCP 四次挥手
        资源释放
      shutdown()
        部分关闭
        发送关闭
        接收关闭
```

---

## 3 网络协议栈详细思维导图

```mermaid
mindmap
  root((网络协议栈))
    TCP 协议
      可靠传输
        序列号
        确认机制
        重传机制
      流量控制
        滑动窗口
        接收窗口
        发送窗口
      拥塞控制
        慢启动
        拥塞避免
        快速重传
        快速恢复
      连接管理
        三次握手
        四次挥手
        连接状态
    UDP 协议
      无连接
        无状态
        快速传输
      数据报
        数据包
        最大长度
      校验和
        错误检测
    IP 协议
      路由转发
        路由表
        路由查找
        FIB
      分片重组
        IP 分片
        IP 重组
      IP 地址
        IPv4
        IPv6
    ICMP 协议
      控制消息
        ping
        traceroute
      错误报告
        目标不可达
        超时
```

---

## 4 网络设备详细思维导图

```mermaid
mindmap
  root((网络设备))
    物理网卡
      网络接口
        eth0
        enp0s3
      硬件驱动
        网卡驱动
        DMA
        中断处理
      性能
        极高吞吐量
        低延迟
    虚拟设备
      veth
        虚拟以太网对
        容器网络
        性能高
      bridge
        网络桥接
        二层转发
        容器网络
      macvlan
        直接访问
        高性能
        独立 MAC
      ipvlan
        共享 MAC
        高性能
        L2/L3 模式
      vxlan
        跨主机网络
        隧道封装
        Kubernetes CNI
    容器网络模式
      Bridge 模式
        veth + bridge
        标准隔离
        性能高
      Host 模式
        共享 Network Namespace
        性能极高
        无隔离
      Macvlan 模式
        macvlan 设备
        性能极高
        直接访问
      Overlay 模式
        vxlan/tunnel
        跨主机网络
        性能中等
```

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含网络子系统详细思维导图 | 🎯 生产就绪
**维护者**：项目团队
