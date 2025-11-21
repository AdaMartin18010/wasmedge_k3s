# 内核故障排查实战案例矩阵

## 📑 目录

- [内核故障排查实战案例矩阵](#内核故障排查实战案例矩阵)
  - [📑 目录](#-目录)
  - [1 内存问题排查案例](#1-内存问题排查案例)
  - [2 CPU问题排查案例](#2-cpu问题排查案例)
  - [3 I/O问题排查案例](#3-io问题排查案例)
  - [4 网络问题排查案例](#4-网络问题排查案例)

---

## 1 内存问题排查案例

| 问题 | 症状 | 诊断步骤 | 诊断命令 | 根本原因 | 解决方案 | 预防措施 |
|------|------|---------|---------|---------|---------|---------|
| **OOM Killer触发** | 进程被杀死，日志显示OOM | 1. 检查内存使用<br>2. 分析OOM日志<br>3. 检查Cgroup限制 | `dmesg \| grep -i oom`<br>`free -h`<br>`cat /sys/fs/cgroup/memory/.../memory.usage_in_bytes` | 内存不足或Cgroup限制过小 | 1. 增加内存限制<br>2. 优化应用内存使用<br>3. 调整swappiness | Memory Cgroup限制 |
| **内存泄漏** | 内存持续增长，不释放 | 1. 监控内存使用<br>2. 使用kmemleak检测<br>3. 分析内存分配 | `cat /proc/meminfo`<br>`echo scan > /sys/kernel/debug/kmemleak`<br>`valgrind --leak-check=full` | 未释放分配的内存 | 1. 修复内存泄漏<br>2. 添加内存释放<br>3. 使用内存池 | 代码审查、内存检测 |
| **Swap过度使用** | 系统响应慢，I/O等待高 | 1. 检查Swap使用<br>2. 分析内存压力<br>3. 检查swappiness | `free -h`<br>`vmstat 1`<br>`cat /proc/sys/vm/swappiness` | Swap使用过多 | 1. 降低swappiness<br>2. 增加物理内存<br>3. 优化内存使用 | 调整swappiness |
| **内存碎片** | 内存充足但分配失败 | 1. 检查内存碎片<br>2. 分析内存分配<br>3. 检查大页使用 | `cat /proc/buddyinfo`<br>`cat /proc/pagetypeinfo` | 内存碎片化 | 1. 使用大页内存<br>2. 内存压缩<br>3. 重启系统 | 大页内存 |
| **NUMA不平衡** | NUMA系统性能差 | 1. 检查NUMA统计<br>2. 分析内存分布<br>3. 检查CPU绑定 | `numastat`<br>`cat /proc/vmstat \| grep numa` | NUMA内存分配不平衡 | 1. 绑定内存到NUMA节点<br>2. 使用numactl<br>3. 启用NUMA平衡 | NUMA优化 |

**诊断说明**：
- **症状**：问题的表现
- **诊断步骤**：排查步骤
- **诊断命令**：使用的命令
- **根本原因**：问题的根本原因
- **解决方案**：解决方法
- **预防措施**：预防方法

---

## 2 CPU问题排查案例

| 问题 | 症状 | 诊断步骤 | 诊断命令 | 根本原因 | 解决方案 | 预防措施 |
|------|------|---------|---------|---------|---------|---------|
| **CPU 100%使用** | CPU满载，系统响应慢 | 1. 识别热点进程<br>2. 分析CPU使用<br>3. 检查调度 | `top`<br>`perf top`<br>`pidstat -u 1` | 死循环、锁竞争 | 1. 优化算法<br>2. 减少锁竞争<br>3. 并行化 | 性能监控 |
| **CPU负载不均衡** | 部分CPU满载，部分空闲 | 1. 检查CPU负载<br>2. 分析进程分布<br>3. 检查调度域 | `htop`<br>`mpstat -P ALL 1`<br>`cat /proc/schedstat` | 负载不均衡 | 1. 启用负载均衡<br>2. CPU亲和性<br>3. 调整调度域 | 负载均衡 |
| **上下文切换过多** | 系统响应慢，CPU使用高 | 1. 检查上下文切换<br>2. 分析进程数<br>3. 检查调度 | `vmstat 1`<br>`pidstat -w 1`<br>`perf stat -e context-switches` | 进程数过多 | 1. 减少进程数<br>2. CPU亲和性<br>3. 优化调度 | 进程管理 |
| **实时任务延迟** | 实时任务响应慢 | 1. 检查调度策略<br>2. 分析延迟<br>3. 检查中断 | `chrt -p <pid>`<br>`perf sched latency` | 调度策略不当 | 1. 设置实时调度<br>2. 提高优先级<br>3. 绑定CPU | 实时调度 |
| **CPU频率不升** | CPU频率锁定在最低 | 1. 检查频率调节器<br>2. 分析CPU负载<br>3. 检查限制 | `cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor`<br>`cpupower frequency-info` | 频率调节器问题 | 1. 更换调节器<br>2. 检查BIOS设置<br>3. 调整参数 | 频率调节器 |

**诊断说明**：
- **症状**：问题的表现
- **诊断步骤**：排查步骤
- **诊断命令**：使用的命令
- **根本原因**：问题的根本原因
- **解决方案**：解决方法
- **预防措施**：预防方法

---

## 3 I/O问题排查案例

| 问题 | 症状 | 诊断步骤 | 诊断命令 | 根本原因 | 解决方案 | 预防措施 |
|------|------|---------|---------|---------|---------|---------|
| **I/O等待高** | I/O等待时间长，系统响应慢 | 1. 检查I/O等待<br>2. 分析磁盘使用<br>3. 检查I/O调度器 | `iostat -x 1`<br>`iotop`<br>`cat /sys/block/sda/queue/scheduler` | I/O瓶颈 | 1. 更换SSD<br>2. 优化I/O调度器<br>3. 使用多队列 | I/O监控 |
| **磁盘I/O错误** | I/O操作失败，日志错误 | 1. 检查磁盘错误<br>2. 分析I/O错误<br>3. 检查磁盘健康 | `dmesg \| grep -i error`<br>`smartctl -a /dev/sda`<br>`iostat -x 1` | 磁盘故障 | 1. 更换磁盘<br>2. 修复文件系统<br>3. 数据恢复 | 磁盘监控 |
| **文件系统只读** | 文件写入失败 | 1. 检查文件系统状态<br>2. 分析错误日志<br>3. 检查磁盘 | `dmesg \| grep -i readonly`<br>`mount \| grep ro`<br>`fsck -n /dev/sda1` | 文件系统错误 | 1. 修复文件系统<br>2. 检查磁盘<br>3. 恢复数据 | 定期检查 |
| **I/O性能下降** | I/O吞吐量下降 | 1. 检查I/O性能<br>2. 分析I/O模式<br>3. 检查调度器 | `iostat -x 1`<br>`fio --name=test --ioengine=libaio` | I/O调度器不当 | 1. 更换调度器<br>2. 优化I/O参数<br>3. 使用多队列 | I/O优化 |
| **Cgroup I/O限制** | I/O操作被限制 | 1. 检查Cgroup限制<br>2. 分析I/O使用<br>3. 检查限制值 | `cat /sys/fs/cgroup/io/.../io.max`<br>`iostat -x 1` | Cgroup限制过小 | 1. 增加I/O限制<br>2. 优化I/O使用<br>3. 调整限制 | I/O Cgroup |

**诊断说明**：
- **症状**：问题的表现
- **诊断步骤**：排查步骤
- **诊断命令**：使用的命令
- **根本原因**：问题的根本原因
- **解决方案**：解决方法
- **预防措施**：预防方法

---

## 4 网络问题排查案例

| 问题 | 症状 | 诊断步骤 | 诊断命令 | 根本原因 | 解决方案 | 预防措施 |
|------|------|---------|---------|---------|---------|---------|
| **网络丢包** | 网络延迟高，丢包率高 | 1. 检查网络统计<br>2. 分析丢包原因<br>3. 检查网络设备 | `netstat -s`<br>`ethtool -S eth0`<br>`tcpdump -i eth0` | 网络拥塞、驱动问题 | 1. 优化网络配置<br>2. 更新驱动<br>3. 增加缓冲区 | 网络监控 |
| **网络连接失败** | 无法建立连接 | 1. 检查网络配置<br>2. 分析连接错误<br>3. 检查防火墙 | `ip addr show`<br>`ss -tuln`<br>`iptables -L` | 网络配置错误 | 1. 修复网络配置<br>2. 检查防火墙<br>3. 检查路由 | 网络配置 |
| **网络性能差** | 网络吞吐量低 | 1. 检查网络性能<br>2. 分析网络参数<br>3. 检查多队列 | `iperf3 -c <server>`<br>`ethtool -l eth0`<br>`cat /proc/sys/net/core/somaxconn` | 网络参数不当 | 1. 优化网络参数<br>2. 启用多队列<br>3. 使用零拷贝 | 网络优化 |
| **Network Namespace问题** | 容器网络不通 | 1. 检查Namespace<br>2. 分析网络配置<br>3. 检查veth | `ip netns list`<br>`ip netns exec <ns> ip addr`<br>`ip link show` | Namespace配置错误 | 1. 修复Namespace配置<br>2. 检查veth<br>3. 检查路由 | Namespace配置 |
| **TCP连接数过多** | 无法建立新连接 | 1. 检查连接数<br>2. 分析连接状态<br>3. 检查限制 | `ss -s`<br>`cat /proc/sys/net/core/somaxconn`<br>`netstat -an \| grep ESTABLISHED \| wc -l` | 连接数限制 | 1. 增加连接数限制<br>2. 优化连接管理<br>3. 使用连接池 | 连接管理 |

**诊断说明**：
- **症状**：问题的表现
- **诊断步骤**：排查步骤
- **诊断命令**：使用的命令
- **根本原因**：问题的根本原因
- **解决方案**：解决方法
- **预防措施**：预防方法

---

## 5 容器问题排查案例

| 问题 | 症状 | 诊断步骤 | 诊断命令 | 根本原因 | 解决方案 | 预防措施 |
|------|------|---------|---------|---------|---------|---------|
| **容器无法启动** | 容器启动失败 | 1. 检查错误日志<br>2. 分析启动参数<br>3. 检查内核支持 | `docker logs <container>`<br>`dmesg \| tail -100`<br>`uname -r` | Namespace创建失败 | 1. 升级内核<br>2. 检查权限<br>3. 修复配置 | 内核版本检查 |
| **容器资源不足** | 容器性能差 | 1. 检查资源使用<br>2. 分析Cgroup限制<br>3. 检查资源配额 | `docker stats <container>`<br>`cat /sys/fs/cgroup/.../memory.usage_in_bytes` | 资源限制过小 | 1. 增加资源限制<br>2. 优化应用<br>3. 调整配额 | 资源限制 |
| **容器网络不通** | 容器无法访问网络 | 1. 检查Network Namespace<br>2. 分析网络配置<br>3. 检查防火墙 | `docker exec <container> ip addr`<br>`ip netns list`<br>`iptables -L` | Network Namespace问题 | 1. 修复网络配置<br>2. 检查veth<br>3. 检查路由 | 网络配置 |
| **容器权限问题** | 容器操作被拒绝 | 1. 检查Capabilities<br>2. 分析权限需求<br>3. 检查Seccomp | `docker inspect <container> \| grep -i cap`<br>`getcap <file>` | 权限不足 | 1. 添加Capabilities<br>2. 调整Seccomp<br>3. 修复权限 | 权限配置 |
| **容器安全事件** | 安全告警 | 1. 检查审计日志<br>2. 分析安全事件<br>3. 检查安全策略 | `ausearch -m all`<br>`falco`<br>`dmesg \| grep -i seccomp` | 安全策略触发 | 1. 分析安全事件<br>2. 调整策略<br>3. 修复问题 | 安全监控 |

**诊断说明**：
- **症状**：问题的表现
- **诊断步骤**：排查步骤
- **诊断命令**：使用的命令
- **根本原因**：问题的根本原因
- **解决方案**：解决方法
- **预防措施**：预防方法

---

## 6 故障排查工具矩阵

| 工具 | 功能 | 使用场景 | 命令示例 | 输出 | 性能影响 |
|------|------|---------|---------|------|---------|
| **dmesg** | 内核日志 | 查看内核消息 | `dmesg -T \| tail -100` | 内核日志 | 极低 |
| **strace** | 系统调用跟踪 | 跟踪系统调用 | `strace -p <pid>` | 系统调用列表 | 中等 |
| **perf** | 性能分析 | 性能分析 | `perf top`, `perf record` | 性能报告 | 低 |
| **ftrace** | 函数跟踪 | 函数调用跟踪 | `echo function > /sys/kernel/debug/tracing/current_tracer` | 函数跟踪 | 低 |
| **eBPF** | 动态跟踪 | 动态分析 | `bpftrace -e 'tracepoint:syscalls:sys_enter_open'` | 跟踪数据 | 极低 |
| **vmstat** | 系统统计 | 系统资源监控 | `vmstat 1` | 系统统计 | 极低 |
| **iostat** | I/O统计 | I/O性能监控 | `iostat -x 1` | I/O统计 | 极低 |
| **netstat** | 网络统计 | 网络性能监控 | `netstat -s` | 网络统计 | 极低 |
| **tcpdump** | 网络抓包 | 网络分析 | `tcpdump -i eth0 -w capture.pcap` | 网络包 | 中等 |
| **valgrind** | 内存分析 | 内存泄漏检测 | `valgrind --leak-check=full ./app` | 内存报告 | 高 |

**工具说明**：
- **功能**：工具的主要功能
- **使用场景**：适用场景
- **命令示例**：基本使用命令
- **输出**：工具的输出
- **性能影响**：对系统性能的影响

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核故障排查实战案例矩阵 | 🎯 生产就绪
**维护者**：项目团队
