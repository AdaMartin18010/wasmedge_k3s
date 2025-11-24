# 监控指标统一采集

> **文档版本**：v1.0 **最后更新：2025-11-15 **维护者**：项目团队

---

## 📑 目录

- [监控指标统一采集](#监控指标统一采集)
  - [📑 目录](#-目录)
  - [概述](#概述)
  - [监控指标统一采集矩阵](#监控指标统一采集矩阵)
  - [日志采集架构](#日志采集架构)
    - [容器日志采集](#容器日志采集)
    - [虚拟机日志采集](#虚拟机日志采集)
    - [统一处理](#统一处理)
  - [关键技术分析](#关键技术分析)
    - [1. 节点性能指标](#1-节点性能指标)
    - [2. Pod 性能指标](#2-pod-性能指标)
    - [3. VM GuestOS 指标](#3-vm-guestos-指标)
    - [4. 业务指标](#4-业务指标)
  - [相关文档](#相关文档)
  - [2025 年最新实践](#2025-年最新实践)
    - [统一监控最佳实践（2025）](#统一监控最佳实践2025)
  - [实际应用案例](#实际应用案例)
    - [案例 1：统一指标采集（2025）](#案例-1统一指标采集2025)

---

## 概述

本文档分析虚拟化容器化集群管理 API 中运维监控的同构体系，展示容器和虚拟机如何通
过统一的监控指标采集和日志采集机制实现运维管理。

## 监控指标统一采集矩阵

| **指标类型**   | **容器**       | **虚拟机**    | **采集方式**        | **存储后端** |
| -------------- | -------------- | ------------- | ------------------- | ------------ |
| **节点性能**   | node-exporter  | node-exporter | DaemonSet           | Prometheus   |
| **Pod 性能**   | cAdvisor       | cAdvisor      | kubelet 内置        | Prometheus   |
| **VM GuestOS** | N/A            | Guest Agent   | virt-handler 代理   | Prometheus   |
| **业务指标**   | Custom Metrics | GuestOS 暴露  | 统一 ServiceMonitor | Prometheus   |

---

## 日志采集架构

### 容器日志采集

**Fluentd 收集**：`/var/log/containers`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: kube-system
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      read_from_head true
      <parse>
        @type json
        time_key time
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>

    <match kubernetes.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      logstash_format true
      logstash_prefix kubernetes
    </match>
```

### 虚拟机日志采集

**virt-handler 转发**：GuestOS 串口日志到宿主机

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: kube-system
data:
  fluent.conf: |
    <source>
      @type unix
      path /var/run/kubevirt/virt-handler.sock
      tag virt-launcher.*
      <parse>
        @type json
        time_key time
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>

    <match virt-launcher.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      logstash_format true
      logstash_prefix virt-launcher
    </match>
```

### 统一处理

**同一条 EFK 管道处理**，按 Namespace 和 `app=virt-launcher` 标签区分

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: kube-system
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      read_from_head true
      <parse>
        @type json
        time_key time
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>

    <source>
      @type unix
      path /var/run/kubevirt/virt-handler.sock
      tag virt-launcher.*
      <parse>
        @type json
        time_key time
        time_format %Y-%m-%dT%H:%M:%S.%NZ
      </parse>
    </source>

    <filter kubernetes.** virt-launcher.**>
      @type kubernetes_metadata
      kubernetes_url https://kubernetes.default.svc
      verify_ssl true
    </filter>

    <match kubernetes.** virt-launcher.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      logstash_format true
      logstash_prefix kubernetes
    </match>
```

---

## 关键技术分析

### 1. 节点性能指标

**容器实现**：node-exporter

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      containers:
        - name: node-exporter
          image: prom/node-exporter:latest
          ports:
            - containerPort: 9100
              name: metrics
```

**虚拟机实现**：node-exporter

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      containers:
        - name: node-exporter
          image: prom/node-exporter:latest
          ports:
            - containerPort: 9100
              name: metrics
```

**说明**：

- 容器和虚拟机都使用 node-exporter 采集节点性能指标
- node-exporter 通过 DaemonSet 部署到每个节点
- 节点性能指标统一采集，容器和虚拟机共享同一套监控体系

### 2. Pod 性能指标

**容器实现**：cAdvisor

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test
      image: nginx:alpine
      # cAdvisor 由 kubelet 内置提供
```

**虚拟机实现**：cAdvisor

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    resources:
      requests:
        memory: "1Gi"
        cpu: "1"
    # cAdvisor 由 kubelet 内置提供，监控 virt-launcher Pod
```

**说明**：

- 容器和虚拟机都使用 cAdvisor 采集 Pod 性能指标
- cAdvisor 由 kubelet 内置提供，无需单独部署
- Pod 性能指标统一采集，容器和虚拟机共享同一套监控体系

### 3. VM GuestOS 指标

**容器实现**：N/A

```yaml
# 容器不支持 GuestOS 指标采集
# 容器直接运行在宿主机上，无需 GuestOS 指标
```

**虚拟机实现**：Guest Agent

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
spec:
  domain:
    devices:
      channels:
        - type: unix
          target:
            name: org.qemu.guest_agent.0
          source:
            name: guest-agent
    resources:
      requests:
        memory: "1Gi"
        cpu: "1"
```

**说明**：

- 容器不支持 GuestOS 指标采集，容器直接运行在宿主机上
- 虚拟机通过 Guest Agent 采集 GuestOS 指标
- Guest Agent 通过 virt-handler 代理，统一上报到 Prometheus

### 4. 业务指标

**容器实现**：Custom Metrics

```yaml
apiVersion: v1
kind: Service
metadata:
  name: test-service
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
spec:
  selector:
    app: test
  ports:
    - port: 80
      targetPort: 8080
```

**虚拟机实现**：GuestOS 暴露

```yaml
apiVersion: v1
kind: Service
metadata:
  name: test-vmi-service
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/metrics"
spec:
  selector:
    kubevirt.io/domain: test-vmi
  ports:
    - port: 80
      targetPort: 8080
```

**说明**：

- 容器通过 Custom Metrics 暴露业务指标
- 虚拟机通过 GuestOS 暴露业务指标
- 业务指标统一通过 ServiceMonitor 采集，容器和虚拟机共享同一套监控体系

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [核心设计模式总结](../05-design-patterns/) - 设计模式总结

---

## 2025 年最新实践

### 统一监控最佳实践（2025）

**2025 年趋势**：统一监控的深度优化

**实践要点**：

- **统一指标采集**：容器和虚拟机通过 Prometheus 统一采集指标
- **统一日志采集**：容器和虚拟机通过 EFK Stack 统一采集日志
- **智能监控**：使用 AI 技术进行智能监控和告警

**代码示例**：

```python
# 2025 年统一监控管理工具
class UnifiedMonitoringManager:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.log_collector = LogCollector()
        self.ai_analyzer = AIAnalyzer()

    def collect_metrics(self, workload_type, workload_name):
        """统一采集指标"""
        if workload_type == 'pod':
            return self.metrics_collector.collect_pod_metrics(workload_name)
        elif workload_type == 'vmi':
            return self.metrics_collector.collect_vmi_metrics(workload_name)

    def analyze_metrics(self, metrics):
        """智能分析指标"""
        return self.ai_analyzer.analyze(metrics)
```

## 实际应用案例

### 案例 1：统一指标采集（2025）

**场景**：使用 Prometheus 统一采集容器和虚拟机的指标

**实现方案**：

```yaml
# ServiceMonitor 统一配置
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: unified-metrics
spec:
  selector:
    matchLabels:
      app: test
  endpoints:
    - port: metrics
      path: /metrics
---
# Pod 指标暴露
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
  labels:
    app: test
spec:
  containers:
    - name: test
      image: nginx:alpine
      ports:
        - name: metrics
          containerPort: 8080
---
# VMI 指标暴露
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: test-vmi
  labels:
    app: test
spec:
  domain:
    devices:
      channels:
        - type: unix
          target:
            name: org.qemu.guest_agent.0
```

**效果**：

- 统一指标采集：容器和虚拟机通过 Prometheus 统一采集指标
- 统一存储：指标统一存储在 Prometheus
- 统一查询：通过 PromQL 统一查询指标

---

**最后更新**：2025-11-15 **维护者**：项目团队
