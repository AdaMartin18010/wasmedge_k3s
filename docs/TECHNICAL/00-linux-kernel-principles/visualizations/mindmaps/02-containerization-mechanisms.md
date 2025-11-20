# 容器化机制思维导图

## 📑 目录

- [容器化机制思维导图](#容器化机制思维导图)
  - [📑 目录](#-目录)
  - [1 容器化机制全景](#1-容器化机制全景)
  - [2 Namespace 机制思维导图](#2-namespace-机制思维导图)
  - [3 Cgroup 机制思维导图](#3-cgroup-机制思维导图)
  - [4 安全机制思维导图](#4-安全机制思维导图)

---

## 1 容器化机制全景

```mermaid
mindmap
  root((容器化机制))
    进程隔离
      Namespace
        PID Namespace
          独立进程树
          init 进程
          进程可见性
        Network Namespace
          独立网络栈
          独立网络设备
          独立路由表
        Mount Namespace
          独立挂载点
          文件系统隔离
        User Namespace
          用户 ID 映射
          权限隔离
        UTS Namespace
          主机名隔离
          域名隔离
        IPC Namespace
          IPC 隔离
          消息队列隔离
    资源限制
      Cgroup
        Cgroup v1
          多层级
          CPU Controller
          Memory Controller
          IO Controller
        Cgroup v2
          统一层级
          统一接口
          改进的控制器
        CPU Controller
          CPU 限制
          CPU 配额
          CPU 共享
        Memory Controller
          内存限制
          内存+交换限制
          内存统计
        IO Controller
          IO 限制
          IO 优先级
    权限控制
      Capabilities
        权限分解
          root 权限分解
          细粒度控制
        主要 Capabilities
          CAP_NET_BIND_SERVICE
          CAP_SYS_ADMIN
          CAP_DAC_OVERRIDE
        Capabilities 集合
          Effective
          Permitted
          Inheritable
      Seccomp
        Strict 模式
          只允许 4 个系统调用
          read/write/exit/sigreturn
        Filter 模式
          BPF 过滤器
          自定义规则
          参数检查
        BPF 过滤器
          BPF 指令
          系统调用过滤
          白名单模式
    安全增强
      LSM
        SELinux
          强制访问控制
          安全上下文
          类型强制
        AppArmor
          基于路径
          配置文件
          学习模式
    容器运行时
      runc
        OCI 标准
        容器创建
        Namespace 设置
        Cgroup 设置
      containerd
        容器管理
        镜像管理
        CRI 接口
      Docker
        镜像构建
        容器管理
        网络管理
```

---

## 2 Namespace 机制思维导图

```mermaid
mindmap
  root((Namespace))
    Namespace 类型
      PID Namespace
        进程隔离
          独立进程树
          init 进程 (PID 1)
          进程可见性
        内核实现
          pid_namespace 结构
          PID 分配
          进程查找
        API
          clone(CLONE_NEWPID)
          setns()
        Docker 应用
          容器进程隔离
          进程树独立
      Network Namespace
        网络隔离
          独立网络栈
          独立网络设备
          独立路由表
          独立防火墙规则
        内核实现
          net 结构
          网络设备列表
          路由表
        API
          clone(CLONE_NEWNET)
          unshare(CLONE_NEWNET)
        Docker 应用
          容器网络
          网络模式
          Bridge/Host/None
      Mount Namespace
        文件系统隔离
          独立挂载点
          挂载操作隔离
          文件系统视图
        内核实现
          mnt_namespace 结构
          挂载点树
        API
          clone(CLONE_NEWNS)
          unshare(CLONE_NEWNS)
        Docker 应用
          容器文件系统
          联合文件系统
          OverlayFS
      User Namespace
        用户隔离
          用户 ID 映射
          权限隔离
          root 权限限制
        内核实现
          user_namespace 结构
          UID/GID 映射
        API
          clone(CLONE_NEWUSER)
        Docker 应用
          非 root 容器
          权限限制
      UTS Namespace
        主机名隔离
          独立主机名
          独立域名
        内核实现
          uts_namespace 结构
        API
          clone(CLONE_NEWUTS)
      IPC Namespace
        IPC 隔离
          消息队列隔离
          共享内存隔离
          信号量隔离
        内核实现
          ipc_namespace 结构
        API
          clone(CLONE_NEWIPC)
    Namespace API
      clone()
        创建新进程
        指定 Namespace 标志
        创建新的 Namespace
      unshare()
        从当前进程分离
        创建新的 Namespace
      setns()
        加入现有 Namespace
        通过文件描述符
    Namespace 数据结构
      nsproxy
        所有 Namespace 的集合
        每个进程一个
      task_struct
        nsproxy 指针
        指向 Namespace 集合
```

---

## 3 Cgroup 机制思维导图

```mermaid
mindmap
  root((Cgroup))
    Cgroup 版本
      Cgroup v1
        多层级结构
          每个控制器独立层级
          复杂的层级关系
        控制器
          CPU Controller
          Memory Controller
          IO Controller
          PIDs Controller
        文件系统接口
          /sys/fs/cgroup/
          每个控制器一个目录
      Cgroup v2
        统一层级
          单一文件系统
          统一的层级结构
        统一接口
          cgroup.controllers
          cgroup.subtree_control
        改进的控制器
          更好的资源管理
          更简单的配置
    CPU Controller
      CPU 限制
        cpu.cfs_quota_us
        cpu.cfs_period_us
      CPU 共享
        cpu.shares
      CPU 统计
        cpu.stat
    Memory Controller
      内存限制
        memory.limit_in_bytes
        memory.memsw.limit_in_bytes
      内存统计
        memory.usage_in_bytes
        memory.max_usage_in_bytes
        memory.stat
      内存回收
        内存压力
        页面回收
        OOM Killer
    IO Controller
      IO 限制
        blkio.throttle.read_bps_device
        blkio.throttle.write_bps_device
      IO 优先级
        blkio.weight
    Cgroup 文件系统
      挂载点
        /sys/fs/cgroup (v1)
        /sys/fs/cgroup/unified (v2)
      控制文件
        cgroup.procs
        cgroup.controllers
        cgroup.subtree_control
    Docker 应用
      资源限制
        --memory
        --cpus
        --device-read-bps
      Kubernetes 应用
        resources.limits
        resources.requests
```

---

## 4 安全机制思维导图

```mermaid
mindmap
  root((安全机制))
    Capabilities
      权限分解
        root 权限分解
          40+ Capabilities
          细粒度控制
        主要 Capabilities
          CAP_NET_BIND_SERVICE
            绑定特权端口
          CAP_SYS_ADMIN
            系统管理权限
          CAP_DAC_OVERRIDE
            绕过文件权限
      Capabilities 集合
        Effective
          当前有效权限
          内核检查使用
        Permitted
          允许的权限上限
          可以获得的权限
        Inheritable
          可继承权限
          传递给子进程
      Docker 应用
        默认移除 Capabilities
        只保留必要权限
        --cap-add/--cap-drop
      Kubernetes 应用
        securityContext.capabilities
        add/drop Capabilities
    Seccomp
      Seccomp 模式
        Strict 模式
          只允许 4 个系统调用
          read/write/exit/sigreturn
        Filter 模式
          BPF 过滤器
          自定义规则
      BPF 过滤器
        BPF 指令
          加载系统调用编号
          比较系统调用
          返回结果
        过滤器编写
          白名单模式
          参数检查
      Docker 应用
        默认 Seccomp 配置
        自定义配置文件
        --security-opt seccomp
      Kubernetes 应用
        seccompProfile
        Localhost 类型
    LSM
      SELinux
        强制访问控制
          基于安全上下文
          类型强制
        安全上下文
          user:role:type:level
        策略配置
          策略规则
          策略文件
        Docker 应用
          --security-opt label
        Kubernetes 应用
          seLinuxOptions
      AppArmor
        基于路径
          文件路径访问控制
          简单易用
        配置文件
          /etc/apparmor.d/
          学习模式
        Docker 应用
          --security-opt apparmor
        Kubernetes 应用
          container.apparmor.security.beta.kubernetes.io
```

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含容器化机制思维导图 | 🎯 生产就绪
**维护者**：项目团队
