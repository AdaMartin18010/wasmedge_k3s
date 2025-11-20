# 系统调用思维导图

## 📑 目录

- [系统调用思维导图](#系统调用思维导图)
  - [📑 目录](#-目录)
  - [1 系统调用全景](#1-系统调用全景)
  - [2 进程管理系统调用](#2-进程管理系统调用)
  - [3 内存管理系统调用](#3-内存管理系统调用)
  - [4 文件系统系统调用](#4-文件系统系统调用)
  - [5 网络系统调用](#5-网络系统调用)

---

## 1 系统调用全景

```mermaid
mindmap
  root((系统调用))
    系统调用基础
      系统调用接口
        系统调用编号
          __NR_read
          __NR_write
          __NR_open
        系统调用表
          sys_call_table
          函数指针数组
        参数传递
          x86_64
            rax: 系统调用编号
            rdi/rsi/rdx: 参数
          ARM64
            x8: 系统调用编号
            x0-x5: 参数
      系统调用流程
        用户空间调用
          C 库函数
          syscall() 函数
        进入内核
          syscall 指令
          软中断
        内核处理
          参数检查
          权限检查
          执行操作
        返回用户空间
          sysret/eret
          返回结果
      系统调用性能
        上下文切换开销
          ~100-200 纳秒
        优化技术
          vDSO
          io_uring
    进程管理系统调用
      fork
        创建子进程
        写时复制
        返回子进程 PID
      clone
        创建进程/线程
        Namespace 标志
        共享资源标志
      execve
        加载新程序
        替换地址空间
        参数和环境变量
      exit
        终止进程
        EXIT_ZOMBIE 状态
        通知父进程
      wait/waitpid
        等待子进程
        回收子进程资源
    内存管理系统调用
      mmap
        内存映射
        文件映射
        匿名映射
        共享/私有映射
      munmap
        取消内存映射
        释放虚拟地址空间
      brk/sbrk
        调整堆大小
        内存分配
      mprotect
        修改内存保护
        读/写/执行权限
    文件系统系统调用
      open
        打开文件
        创建文件
        文件标志
      read
        读取文件
        文件描述符
        缓冲区
      write
        写入文件
        文件描述符
        数据缓冲区
      close
        关闭文件
        释放文件描述符
      stat/fstat
        获取文件信息
        inode 信息
        文件大小
      mkdir/rmdir
        创建目录
        删除目录
    网络系统调用
      socket
        创建套接字
        协议族
        套接字类型
      bind
        绑定地址
        IP 地址
        端口号
      connect
        连接服务器
        远程地址
      listen
        监听连接
         backlog
      accept
        接受连接
        返回新套接字
      send/recv
        发送/接收数据
        套接字
        数据缓冲区
      sendto/recvfrom
        发送/接收数据
        UDP 套接字
        目标地址
```

---

## 2 进程管理系统调用

```mermaid
mindmap
  root((进程管理系统调用))
    fork
      功能
        创建子进程
        复制父进程
      实现
        写时复制
        复制进程描述符
      返回值
        父进程: 子进程 PID
        子进程: 0
      使用场景
        多进程程序
        守护进程
    clone
      功能
        创建进程/线程
        灵活的资源共享
      参数
        clone_flags
          CLONE_VM: 共享地址空间
          CLONE_FILES: 共享文件描述符
          CLONE_NEWPID: 新 PID Namespace
          CLONE_NEWNET: 新 Network Namespace
      使用场景
        线程创建
        容器创建
    execve
      功能
        加载新程序
        替换地址空间
      参数
        程序路径
        参数数组
        环境变量
      exec 系列
        execl
        execp
        execv
      使用场景
        程序启动
        脚本执行
    exit
      功能
        终止进程
        释放资源
      进程状态
        EXIT_ZOMBIE
        EXIT_DEAD
      信号
        SIGCHLD 通知父进程
    wait/waitpid
      功能
        等待子进程
        回收资源
      wait
        等待任意子进程
      waitpid
        等待指定子进程
        WNOHANG: 非阻塞
        WUNTRACED: 跟踪子进程
```

---

## 3 内存管理系统调用

```mermaid
mindmap
  root((内存管理系统调用))
    mmap
      功能
        内存映射
        文件映射到内存
      映射类型
        文件映射
          映射文件到内存
          共享映射
          私有映射
        匿名映射
          不关联文件
          堆内存分配
      参数
        addr: 建议地址
        length: 映射长度
        prot: 保护标志
          PROT_READ
          PROT_WRITE
          PROT_EXEC
        flags: 映射标志
          MAP_SHARED
          MAP_PRIVATE
          MAP_ANONYMOUS
        fd: 文件描述符
        offset: 文件偏移
      使用场景
        大文件处理
        共享内存
        内存分配
    munmap
      功能
        取消内存映射
        释放虚拟地址空间
      参数
        addr: 映射地址
        length: 映射长度
    brk/sbrk
      功能
        调整堆大小
        内存分配
      brk
        设置堆结束地址
      sbrk
        增加堆大小
      使用场景
        malloc 底层实现
    mprotect
      功能
        修改内存保护
        改变页面权限
      参数
        addr: 内存地址
        length: 长度
        prot: 新保护标志
      使用场景
        代码保护
        内存安全
```

---

## 4 文件系统系统调用

```mermaid
mindmap
  root((文件系统系统调用))
    文件操作
      open
        功能
          打开/创建文件
          返回文件描述符
        参数
          pathname: 文件路径
          flags: 打开标志
            O_RDONLY
            O_WRONLY
            O_RDWR
            O_CREAT
            O_TRUNC
          mode: 文件权限
        返回值
          文件描述符
          -1 错误
      read
        功能
          读取文件数据
        参数
          fd: 文件描述符
          buf: 缓冲区
          count: 读取字节数
        返回值
          读取的字节数
          0: EOF
          -1: 错误
      write
        功能
          写入文件数据
        参数
          fd: 文件描述符
          buf: 数据缓冲区
          count: 写入字节数
        返回值
          写入的字节数
          -1: 错误
      close
        功能
          关闭文件
          释放文件描述符
        参数
          fd: 文件描述符
    文件信息
      stat/fstat
        功能
          获取文件信息
          inode 信息
        参数
          pathname: 文件路径
          statbuf: 信息缓冲区
        stat 结构
          st_mode: 文件类型和权限
          st_size: 文件大小
          st_mtime: 修改时间
      lstat
        功能
          获取符号链接信息
          不跟随符号链接
    目录操作
      mkdir
        功能
          创建目录
        参数
          pathname: 目录路径
          mode: 目录权限
      rmdir
        功能
          删除空目录
        参数
          pathname: 目录路径
      opendir/readdir
        功能
          打开目录
          读取目录项
```

---

## 5 网络系统调用

```mermaid
mindmap
  root((网络系统调用))
    Socket 创建
      socket
        功能
          创建套接字
          返回文件描述符
        参数
          domain: 协议族
            AF_INET: IPv4
            AF_INET6: IPv6
            AF_UNIX: Unix Domain
          type: 套接字类型
            SOCK_STREAM: TCP
            SOCK_DGRAM: UDP
            SOCK_RAW: 原始套接字
          protocol: 协议
            0: 默认协议
    Socket 绑定
      bind
        功能
          绑定地址
          IP 和端口
        参数
          sockfd: 套接字
          addr: 地址结构
          addrlen: 地址长度
    Socket 连接
      connect
        功能
          连接服务器
          TCP 连接
        参数
          sockfd: 套接字
          addr: 服务器地址
          addrlen: 地址长度
      listen
        功能
          监听连接
          TCP 服务器
        参数
          sockfd: 套接字
          backlog: 连接队列大小
      accept
        功能
          接受连接
          返回新套接字
        参数
          sockfd: 监听套接字
          addr: 客户端地址
          addrlen: 地址长度
    Socket 数据传输
      send/recv
        功能
          发送/接收数据
          TCP 套接字
        参数
          sockfd: 套接字
          buf: 数据缓冲区
          len: 数据长度
          flags: 标志
      sendto/recvfrom
        功能
          发送/接收数据
          UDP 套接字
        参数
          sockfd: 套接字
          buf: 数据缓冲区
          len: 数据长度
          flags: 标志
          dest_addr: 目标地址
          addrlen: 地址长度
```

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含系统调用思维导图 | 🎯 生产就绪
**维护者**：项目团队
