# 故障排查矩阵

## 📑 目录

- [故障排查矩阵](#故障排查矩阵)
  - [📑 目录](#-目录)
  - [1 进程问题排查矩阵](#1-进程问题排查矩阵)
  - [2 内存问题排查矩阵](#2-内存问题排查矩阵)
  - [3 文件系统问题排查矩阵](#3-文件系统问题排查矩阵)
  - [4 网络问题排查矩阵](#4-网络问题排查矩阵)
  - [5 容器化问题排查矩阵](#5-容器化问题排查矩阵)
  - [6 综合故障排查流程矩阵](#6-综合故障排查流程矩阵)

---

## 1 进程问题排查矩阵

| 问题 | 症状 | 可能原因 | 检查命令 | 解决方案 | 容器化相关 |
|------|------|---------|---------|---------|-----------|
| **进程无法启动** | 启动失败 | 权限不足 | `ls -l`, `capsh` | 添加 Capabilities | Capabilities 限制 |
| **进程无法启动** | 启动失败 | 系统调用被过滤 | `strace`, `dmesg` | 调整 Seccomp | Seccomp 过滤 |
| **进程卡死** | 无响应 | 死锁 | `ps aux`, `strace -p` | 检查锁、信号量 | IPC Namespace |
| **进程 CPU 高** | CPU 100% | 死循环、计算密集 | `top`, `perf` | 优化算法、限制 CPU | Cgroup CPU |
| **进程内存泄漏** | 内存持续增长 | 未释放内存 | `valgrind`, `/proc/pid/status` | 修复内存泄漏 | Cgroup Memory |
| **进程无法通信** | IPC 失败 | IPC Namespace 隔离 | `ipcs`, `lsns` | 检查 Namespace | IPC Namespace |
| **进程无法看到其他进程** | 进程列表为空 | PID Namespace 隔离 | `ps aux`, `lsns` | 正常现象 | PID Namespace |

**排查工具**：

- **strace**：跟踪系统调用
- **perf**：性能分析
- **valgrind**：内存检查
- **dmesg**：内核日志

---

## 2 内存问题排查矩阵

| 问题 | 症状 | 可能原因 | 检查命令 | 解决方案 | 容器化相关 |
|------|------|---------|---------|---------|-----------|
| **内存不足** | OOM | 内存使用超限 | `free`, `/proc/meminfo` | 增加内存、优化使用 | Cgroup Memory |
| **内存泄漏** | 内存持续增长 | 未释放内存 | `valgrind`, `smem` | 修复内存泄漏 | Cgroup Memory |
| **Swap 使用高** | Swap 频繁 | 内存不足 | `swapon -s`, `vmstat` | 增加内存、调整 swappiness | Cgroup Swap |
| **内存碎片** | 分配失败 | 内存碎片化 | `/proc/buddyinfo` | 内存整理、重启 | 无 |
| **TLB miss 高** | 性能下降 | 页表访问多 | `perf stat` | 使用大页 | 无 |
| **容器内存超限** | 容器被杀死 | Cgroup 限制 | `/sys/fs/cgroup/memory/**` | 增加限制、优化使用 | Cgroup Memory |

**排查工具**：

- **free**：查看内存使用
- **vmstat**：虚拟内存统计
- **valgrind**：内存泄漏检测
- **perf**：性能分析

---

## 3 文件系统问题排查矩阵

| 问题 | 症状 | 可能原因 | 检查命令 | 解决方案 | 容器化相关 |
|------|------|---------|---------|---------|-----------|
| **文件无法打开** | 权限 denied | 权限不足 | `ls -l`, `getcap` | 修改权限、添加 Capabilities | Capabilities |
| **文件无法打开** | 系统调用被过滤 | Seccomp 过滤 | `strace`, `dmesg` | 调整 Seccomp | Seccomp |
| **文件系统只读** | 无法写入 | 只读挂载 | `mount`, `dmesg` | 重新挂载为读写 | Mount Namespace |
| **文件系统空间不足** | No space left | 磁盘空间满 | `df -h`, `du -sh` | 清理空间、扩容 | 无 |
| **inode 耗尽** | No space left | inode 用尽 | `df -i` | 清理文件、增加 inode | 无 |
| **文件系统损坏** | I/O error | 文件系统错误 | `dmesg`, `fsck` | 文件系统检查修复 | 无 |
| **容器文件系统隔离** | 看不到宿主机文件 | Mount Namespace | `lsns`, `mount` | 正常现象 | Mount Namespace |

**排查工具**：

- **df**：查看磁盘空间
- **du**：查看目录大小
- **dmesg**：内核日志
- **fsck**：文件系统检查

---

## 4 网络问题排查矩阵

| 问题 | 症状 | 可能原因 | 检查命令 | 解决方案 | 容器化相关 |
|------|------|---------|---------|---------|-----------|
| **无法绑定端口** | Address already in use | 端口被占用 | `netstat`, `ss` | 更换端口、释放端口 | Network Namespace |
| **无法绑定端口** | Permission denied | 权限不足 | `getcap`, `id` | 添加 CAP_NET_BIND_SERVICE | Capabilities |
| **网络不通** | 连接失败 | Network Namespace 隔离 | `ip addr`, `lsns` | 检查网络配置 | Network Namespace |
| **DNS 解析失败** | 无法解析域名 | DNS 配置错误 | `nslookup`, `/etc/resolv.conf` | 配置 DNS | Network Namespace |
| **网络性能差** | 延迟高、吞吐低 | 网络配置问题 | `iperf`, `ethtool` | 优化网络配置 | 网络模式 |
| **容器间无法通信** | 连接失败 | 网络隔离 | `docker network ls`, `ip route` | 配置容器网络 | Network Namespace |

**排查工具**：

- **netstat/ss**：查看网络连接
- **ip**：网络配置
- **tcpdump**：网络抓包
- **iperf**：网络性能测试

---

## 5 容器化问题排查矩阵

| 问题 | 症状 | 可能原因 | 检查命令 | 解决方案 | 相关机制 |
|------|------|---------|---------|---------|---------|
| **容器无法启动** | 启动失败 | Namespace 创建失败 | `dmesg`, `lsns` | 检查内核支持 | Namespace |
| **容器无法启动** | 启动失败 | Cgroup 配置错误 | `/sys/fs/cgroup/**` | 检查 Cgroup 配置 | Cgroup |
| **容器权限不足** | 操作失败 | Capabilities 限制 | `capsh --print`, `getcap` | 添加必要 Capabilities | Capabilities |
| **容器系统调用被拒绝** | 操作失败 | Seccomp 过滤 | `strace`, `dmesg` | 调整 Seccomp 配置 | Seccomp |
| **容器内存超限** | 容器被杀死 | Cgroup 内存限制 | `/sys/fs/cgroup/memory/**` | 增加内存限制 | Cgroup Memory |
| **容器 CPU 受限** | 性能下降 | Cgroup CPU 限制 | `/sys/fs/cgroup/cpu/**` | 增加 CPU 限制 | Cgroup CPU |
| **容器网络不通** | 连接失败 | Network Namespace 配置 | `ip addr`, `docker network` | 检查网络配置 | Network Namespace |
| **容器文件系统隔离** | 看不到宿主机文件 | Mount Namespace | `mount`, `lsns` | 正常现象 | Mount Namespace |
| **容器进程隔离** | 看不到其他进程 | PID Namespace | `ps aux`, `lsns` | 正常现象 | PID Namespace |

**排查工具**：

- **docker logs**：容器日志
- **dmesg**：内核日志
- **strace**：系统调用跟踪
- **lsns**：查看 Namespace

---

## 6 综合故障排查流程矩阵

| 故障类型 | 第一步 | 第二步 | 第三步 | 第四步 | 第五步 |
|---------|--------|--------|--------|--------|--------|
| **进程问题** | 检查进程状态 | 检查系统调用 | 检查权限 | 检查资源限制 | 检查日志 |
| **内存问题** | 检查内存使用 | 检查 Cgroup 限制 | 检查 Swap | 检查内存泄漏 | 检查 OOM |
| **文件系统问题** | 检查磁盘空间 | 检查权限 | 检查挂载 | 检查文件系统 | 检查日志 |
| **网络问题** | 检查网络配置 | 检查 Network Namespace | 检查防火墙 | 检查 DNS | 检查日志 |
| **容器问题** | 检查容器状态 | 检查 Namespace | 检查 Cgroup | 检查安全机制 | 检查日志 |

**通用排查步骤**：

1. **查看日志**：`dmesg`, `journalctl`, `docker logs`
2. **检查状态**：`ps`, `top`, `free`, `netstat`
3. **跟踪系统调用**：`strace`, `ltrace`
4. **性能分析**：`perf`, `vmstat`, `iostat`
5. **检查配置**：`lsns`, `/sys/fs/cgroup/**`, `getcap`

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含故障排查详细矩阵 | 🎯 生产就绪
**维护者**：项目团队
