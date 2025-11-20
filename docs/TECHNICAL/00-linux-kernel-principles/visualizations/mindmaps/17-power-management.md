# 内核电源管理详细思维导图

## 📑 目录

- [内核电源管理详细思维导图](#内核电源管理详细思维导图)
  - [📑 目录](#-目录)
  - [1 电源管理全景](#1-电源管理全景)
  - [2 CPU 电源管理详细思维导图](#2-cpu-电源管理详细思维导图)
  - [3 设备电源管理详细思维导图](#3-设备电源管理详细思维导图)
  - [4 系统电源管理详细思维导图](#4-系统电源管理详细思维导图)

---

## 1 电源管理全景

```mermaid
mindmap
  root((电源管理))
    CPU 电源管理
      CPU 频率调节
        CPUFreq
        频率调节器
        governors
      CPU 空闲管理
        CPUIdle
        C 状态
        空闲状态
      CPU 热管理
        CPU 温度
        热节流
        动态电压频率调节
    设备电源管理
      设备电源状态
        D0 全功率
        D1/D2 低功率
        D3 关闭
      设备挂起
        挂起设备
        恢复设备
        电源管理接口
      Runtime PM
        运行时电源管理
        自动挂起
        自动恢复
    系统电源管理
      系统挂起
        Suspend to RAM
        Suspend to Disk
        混合挂起
      系统休眠
        Hibernate
        休眠到磁盘
        快速恢复
      ACPI
        ACPI 接口
        电源管理事件
        系统状态
    容器化应用
      容器电源管理
        容器挂起
        容器恢复
        资源限制
```

---

## 2 CPU 电源管理详细思维导图

```mermaid
mindmap
  root((CPU 电源管理))
    CPUFreq
      频率调节器
        performance
          性能模式
          最高频率
        powersave
          省电模式
          最低频率
        ondemand
          按需调节
          动态调节
        conservative
          保守模式
          平滑调节
        schedutil
          调度器驱动
          基于负载
      CPU 频率
        最小频率
        最大频率
        当前频率
      CPU 频率表
        频率列表
        电压表
        频率电压对应
    CPUIdle
      C 状态
        C0 运行
        C1 停止
        C2 深度停止
        C3 深度睡眠
      CPU 空闲
        空闲检测
        空闲进入
        空闲退出
      CPU 热管理
        CPU 温度
        热节流
        动态电压频率调节
```

---

## 3 设备电源管理详细思维导图

```mermaid
mindmap
  root((设备电源管理))
    设备电源状态
      D0
        全功率状态
        设备运行
        最高性能
      D1/D2
        低功率状态
        部分功能
        低功耗
      D3
        关闭状态
        设备关闭
        无功耗
    设备挂起
      挂起设备
        suspend()
        保存状态
        降低功耗
      恢复设备
        resume()
        恢复状态
        恢复功能
      Runtime PM
        运行时电源管理
        自动挂起
        自动恢复
    电源管理接口
      PM 接口
        suspend/resume
        power_on/power_off
        runtime_suspend/runtime_resume
```

---

## 4 系统电源管理详细思维导图

```mermaid
mindmap
  root((系统电源管理))
    系统挂起
      Suspend to RAM
        S3 状态
        内存保持
        快速恢复
      Suspend to Disk
        S4 状态
        保存到磁盘
        完全断电
      混合挂起
        Hybrid Sleep
        内存+磁盘
        双重保护
    系统休眠
      Hibernate
        休眠到磁盘
        完全断电
        快速恢复
      ACPI
        ACPI 接口
        电源管理事件
        系统状态
        电源按钮
    电源管理事件
      电源按钮
        按下事件
        系统响应
      休眠按钮
        休眠事件
        系统休眠
      唤醒事件
        唤醒源
        系统唤醒
```

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核电源管理详细思维导图 | 🎯 生产就绪
**维护者**：项目团队
