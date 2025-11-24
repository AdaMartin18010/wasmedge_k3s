# 调度视角参考资源

> **文档版本**：v1.0 **最后更新：2025-11-15 **维护者**：项目团队

---

## 📑 目录

- [调度视角参考资源](#调度视角参考资源)
  - [📑 目录](#-目录)
  - [1 学术参考](#1-学术参考)
    - [1.1 调度理论](#11-调度理论)
    - [1.2 图论与调度](#12-图论与调度)
    - [1.3 动态系统与调度](#13-动态系统与调度)
    - [1.4 随机过程与调度](#14-随机过程与调度)
    - [1.5 有界系统理论](#15-有界系统理论)
    - [1.6 控制理论](#16-控制理论)
  - [2 实践参考](#2-实践参考)
    - [2.1 Kubernetes 调度器](#21-kubernetes-调度器)
    - [2.2 YARN 调度器](#22-yarn-调度器)
    - [2.3 Mesos 调度器](#23-mesos-调度器)
    - [2.4 其他调度系统](#24-其他调度系统)
  - [3 相关标准](#3-相关标准)
  - [4 在线资源](#4-在线资源)

---

## 1 学术参考

### 1.1 调度理论

**经典教材**：

1. Pinedo, M. L. (2016). _Scheduling: Theory, Algorithms, and Systems_.
   Springer.

   - 调度理论的经典教材，涵盖调度算法的理论基础和实践应用

2. Leung, J. Y. T. (2004). _Handbook of Scheduling: Algorithms, Models, and
   Performance Analysis_. CRC Press.
   - 调度算法的综合手册，包含大量调度算法和性能分析

**重要论文**：

1. Graham, R. L., et al. (1979). "Optimization and approximation in
   deterministic sequencing and scheduling: a survey." _Annals of Discrete
   Mathematics_.

   - 确定性调度问题的优化和近似算法综述

2. Lawler, E. L., et al. (1993). _Sequencing and Scheduling: Algorithms and
   Complexity_. North-Holland.
   - 调度问题的算法和复杂度分析

---

### 1.2 图论与调度

**经典教材**：

1. Bondy, J. A., & Murty, U. S. R. (2008). _Graph Theory_. Springer.

   - 图论的基础教材，涵盖图的基本概念和算法

2. Diestel, R. (2017). _Graph Theory_. Springer.

   - 图论的现代教材，涵盖图的高级主题

3. Cormen, T. H., et al. (2009). _Introduction to Algorithms_. MIT Press.
   - 算法导论，包含图算法的详细分析

**重要论文**：

1. Hopcroft, J. E., & Karp, R. M. (1973). "An n^5/2 algorithm for maximum
   matchings in bipartite graphs." _SIAM Journal on Computing_.

   - 二分图最大匹配的快速算法

2. Edmonds, J., & Karp, R. M. (1972). "Theoretical improvements in algorithmic
   efficiency for network flow problems." _Journal of the ACM_.
   - 网络流问题的理论改进

---

### 1.3 动态系统与调度

**经典教材**：

1. Cassandras, C. G., & Lafortune, S. (2008). _Introduction to Discrete Event
   Systems_. Springer.

   - 离散事件系统导论，适用于调度系统的动态分析

2. Kumar, P. R., & Varaiya, P. (1986). _Stochastic Systems: Estimation,
   Identification, and Adaptive Control_. Prentice-Hall.
   - 随机系统的估计、识别和自适应控制

**重要论文**：

1. Lyapunov, A. M. (1892). "The General Problem of the Stability of Motion."
   - Lyapunov 稳定性理论的奠基性论文

---

### 1.4 随机过程与调度

**经典教材**：

1. Kleinrock, L. (1975). _Queueing Systems, Volume 1: Theory_. Wiley.

   - 排队论的基础教材，适用于调度系统的随机分析

2. Gross, D., & Harris, C. M. (1998). _Fundamentals of Queueing Theory_. Wiley.

   - 排队论基础，包含排队模型的分析方法

3. Ross, S. M. (2014). _Introduction to Probability Models_. Academic Press.
   - 概率模型导论，包含随机过程的基础理论

**重要论文**：

1. Pollaczek, F. (1930). "Über eine Aufgabe der Wahrscheinlichkeitstheorie."
   - Pollaczek-Khintchine 公式的原始论文

---

### 1.5 有界系统理论

**经典教材**：

1. Khalil, H. K. (2002). _Nonlinear Systems_. Prentice-Hall.

   - 非线性系统理论，包含有界性分析

2. Sontag, E. D. (1998). _Mathematical Control Theory: Deterministic Finite
   Dimensional Systems_. Springer.
   - 数学控制理论，包含有界系统的理论分析

---

### 1.6 控制理论

**经典教材**：

1. Åström, K. J., & Murray, R. M. (2008). _Feedback Systems: An Introduction for
   Scientists and Engineers_. Princeton University Press.

   - 反馈系统导论，适用于调度系统的控制分析

2. Franklin, G. F., et al. (2014). _Feedback Control of Dynamic Systems_.
   Pearson.
   - 动态系统的反馈控制

---

## 2 实践参考

### 2.1 Kubernetes 调度器

**官方文档**：

- [Kubernetes 调度器概念](https://kubernetes.io/docs/concepts/scheduling-eviction/)
- [Kubernetes 调度器性能调优](https://kubernetes.io/docs/concepts/scheduling-eviction/scheduler-perf-tuning/)
- [Kubernetes 调度器配置](https://kubernetes.io/docs/reference/scheduling/config/)

**重要资源**：

- [Kubernetes 调度器源码](https://github.com/kubernetes/kubernetes/tree/master/pkg/scheduler)
- [Kubernetes 调度器插件](https://kubernetes.io/docs/reference/scheduling/config/#scheduling-plugins)

---

### 2.2 YARN 调度器

**官方文档**：

- [YARN 调度器概述](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html)
- [Capacity Scheduler](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html)
- [Fair Scheduler](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/FairScheduler.html)

**重要资源**：

- [YARN 调度器源码](https://github.com/apache/hadoop/tree/trunk/hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-resourcemanager/src/main/java/org/apache/hadoop/yarn/server/resourcemanager/scheduler)

---

### 2.3 Mesos 调度器

**官方文档**：

- [Mesos 架构](http://mesos.apache.org/documentation/latest/architecture/)
- [Mesos 调度器](http://mesos.apache.org/documentation/latest/scheduler-http-api/)

**重要资源**：

- [Mesos 调度器源码](https://github.com/apache/mesos/tree/master/src/scheduler)

---

### 2.4 其他调度系统

**Borg/Kubernetes**：

- Verma, A., et al. (2015). "Large-scale cluster management at Google with
  Borg." _EuroSys_.
  - Google Borg 系统的调度设计

**Omega**：

- Schwarzkopf, M., et al. (2013). "Omega: flexible, scalable schedulers for
  large compute clusters." _EuroSys_.
  - Google Omega 系统的调度架构

**Quincy**：

- Isard, M., et al. (2009). "Quincy: fair scheduling for distributed computing
  clusters." _SOSP_.
  - Microsoft Quincy 系统的公平调度

**DRF**：

- Ghodsi, A., et al. (2011). "Dominant Resource Fairness: Fair Allocation of
  Multiple Resource Types." _NSDI_.
  - 主导资源公平（DRF）调度算法

---

## 3 相关标准

**调度相关标准**：

1. **Kubernetes API 标准**：

   - [Kubernetes API 规范](https://kubernetes.io/docs/reference/kubernetes-api/)
   - [调度 API 规范](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#scheduling)

2. **容器运行时标准**：
   - [OCI 运行时规范](https://github.com/opencontainers/runtime-spec)
   - [CRI 接口规范](https://github.com/kubernetes/cri-api)

---

## 4 在线资源

**学术数据库**：

- [ACM Digital Library](https://dl.acm.org/)
- [IEEE Xplore](https://ieeexplore.ieee.org/)
- [Google Scholar](https://scholar.google.com/)

**开源项目**：

- [Kubernetes](https://github.com/kubernetes/kubernetes)
- [Apache YARN](https://github.com/apache/hadoop)
- [Apache Mesos](https://github.com/apache/mesos)

**社区资源**：

- [Kubernetes 社区](https://kubernetes.io/community/)
- [CNCF 调度工作组](https://github.com/cncf/sig-scheduling)

---

**最后更新**：2025-11-15 **维护者**：项目团队
