# 11.4 观察者模式：统一事件通知

> **文档版本**：v1.0 **最后更新：2025-11-15 **维护者**：项目团队

---

## 📑 目录

- [11.4 观察者模式：统一事件通知](#114-观察者模式统一事件通知)
  - [📑 目录](#-目录)
  - [概述](#概述)
  - [设计说明](#设计说明)
    - [观察者模式：事件通知系统](#观察者模式事件通知系统)
  - [实现细节](#实现细节)
    - [1. 事件观察者接口](#1-事件观察者接口)
    - [2. 统一事件分发器](#2-统一事件分发器)
    - [3. 事件监听器](#3-事件监听器)
  - [关键技术分析](#关键技术分析)
    - [1. Kubernetes Events](#1-kubernetes-events)
    - [2. Custom Resource Watch](#2-custom-resource-watch)
    - [3. Webhook 通知](#3-webhook-通知)
  - [相关文档](#相关文档)
  - [2025 年最新实践](#2025-年最新实践)
    - [观察者模式最佳实践（2025）](#观察者模式最佳实践2025)
  - [实际应用案例](#实际应用案例)
    - [案例 1：统一事件通知（2025）](#案例-1统一事件通知2025)

---

## 概述

本文档分析观察者模式在统一事件通知中的应用，展示如何通过观察者模式实现容器和虚拟
机的统一事件通知机制。

## 设计说明

**设计**：Kubernetes Events + Custom Resource Watch

### 观察者模式：事件通知系统

```go
// 观察者模式：事件通知系统
type EventObserver interface {
    OnVMCreated(vm *VirtualMachine)
    OnVMDeleted(vm *VirtualMachine)
    OnVMMigrated(vm *VirtualMachine, targetNode string)
    OnQuotaExceeded(namespace string, resource string)
}

// 统一事件分发器
type EventDispatcher struct {
    observers []EventObserver
    eventRecorder record.EventRecorder
}

func (d *EventDispatcher) NotifyVMCreated(vm *VirtualMachine) {
    // 1. 记录K8s Event
    d.eventRecorder.Event(vm, "Normal", "Created", "VM created successfully")

    // 2. 通知所有观察者
    for _, obs := range d.observers {
        obs.OnVMCreated(vm)
    }

    // 3. 触发Webhook（可选）
    d.sendWebhook(vm, "vm.created")
}
```

---

## 实现细节

### 1. 事件观察者接口

```go
// 事件观察者接口
type EventObserver interface {
    OnVMCreated(vm *VirtualMachine)
    OnVMDeleted(vm *VirtualMachine)
    OnVMMigrated(vm *VirtualMachine, targetNode string)
    OnQuotaExceeded(namespace string, resource string)
}

// 监控观察者实现
type MonitoringObserver struct {
    prometheusClient prometheus.Client
}

func (o *MonitoringObserver) OnVMCreated(vm *VirtualMachine) {
    // 记录虚拟机创建指标
    o.prometheusClient.Inc("vm_created_total", map[string]string{
        "namespace": vm.Namespace,
        "name":      vm.Name,
    })
}

func (o *MonitoringObserver) OnVMDeleted(vm *VirtualMachine) {
    // 记录虚拟机删除指标
    o.prometheusClient.Inc("vm_deleted_total", map[string]string{
        "namespace": vm.Namespace,
        "name":      vm.Name,
    })
}

func (o *MonitoringObserver) OnVMMigrated(vm *VirtualMachine, targetNode string) {
    // 记录虚拟机迁移指标
    o.prometheusClient.Inc("vm_migrated_total", map[string]string{
        "namespace":  vm.Namespace,
        "name":       vm.Name,
        "targetNode": targetNode,
    })
}

func (o *MonitoringObserver) OnQuotaExceeded(namespace string, resource string) {
    // 记录配额超限指标
    o.prometheusClient.Inc("quota_exceeded_total", map[string]string{
        "namespace": namespace,
        "resource":  resource,
    })
}

// 日志观察者实现
type LoggingObserver struct {
    logger log.Logger
}

func (o *LoggingObserver) OnVMCreated(vm *VirtualMachine) {
    o.logger.Info("VM created", "namespace", vm.Namespace, "name", vm.Name)
}

func (o *LoggingObserver) OnVMDeleted(vm *VirtualMachine) {
    o.logger.Info("VM deleted", "namespace", vm.Namespace, "name", vm.Name)
}

func (o *LoggingObserver) OnVMMigrated(vm *VirtualMachine, targetNode string) {
    o.logger.Info("VM migrated", "namespace", vm.Namespace, "name", vm.Name, "targetNode", targetNode)
}

func (o *LoggingObserver) OnQuotaExceeded(namespace string, resource string) {
    o.logger.Warn("Quota exceeded", "namespace", namespace, "resource", resource)
}
```

### 2. 统一事件分发器

```go
// 统一事件分发器
type EventDispatcher struct {
    observers     []EventObserver
    eventRecorder record.EventRecorder
    webhookClient webhook.Client
}

func NewEventDispatcher(eventRecorder record.EventRecorder, webhookClient webhook.Client) *EventDispatcher {
    return &EventDispatcher{
        observers:     make([]EventObserver, 0),
        eventRecorder: eventRecorder,
        webhookClient: webhookClient,
    }
}

func (d *EventDispatcher) RegisterObserver(observer EventObserver) {
    d.observers = append(d.observers, observer)
}

func (d *EventDispatcher) NotifyVMCreated(vm *VirtualMachine) {
    // 1. 记录K8s Event
    d.eventRecorder.Event(vm, "Normal", "Created", "VM created successfully")

    // 2. 通知所有观察者
    for _, obs := range d.observers {
        obs.OnVMCreated(vm)
    }

    // 3. 触发Webhook（可选）
    d.sendWebhook(vm, "vm.created")
}

func (d *EventDispatcher) NotifyVMDeleted(vm *VirtualMachine) {
    // 1. 记录K8s Event
    d.eventRecorder.Event(vm, "Normal", "Deleted", "VM deleted successfully")

    // 2. 通知所有观察者
    for _, obs := range d.observers {
        obs.OnVMDeleted(vm)
    }

    // 3. 触发Webhook（可选）
    d.sendWebhook(vm, "vm.deleted")
}

func (d *EventDispatcher) NotifyVMMigrated(vm *VirtualMachine, targetNode string) {
    // 1. 记录K8s Event
    d.eventRecorder.Event(vm, "Normal", "Migrated", fmt.Sprintf("VM migrated to node %s", targetNode))

    // 2. 通知所有观察者
    for _, obs := range d.observers {
        obs.OnVMMigrated(vm, targetNode)
    }

    // 3. 触发Webhook（可选）
    d.sendWebhook(vm, "vm.migrated")
}

func (d *EventDispatcher) NotifyQuotaExceeded(namespace string, resource string) {
    // 1. 记录K8s Event
    d.eventRecorder.Eventf(nil, "Warning", "QuotaExceeded", "Quota exceeded for resource %s in namespace %s", resource, namespace)

    // 2. 通知所有观察者
    for _, obs := range d.observers {
        obs.OnQuotaExceeded(namespace, resource)
    }

    // 3. 触发Webhook（可选）
    d.sendWebhook(nil, "quota.exceeded")
}

func (d *EventDispatcher) sendWebhook(obj interface{}, eventType string) {
    if d.webhookClient == nil {
        return
    }

    payload := map[string]interface{}{
        "type": eventType,
        "object": obj,
        "timestamp": time.Now().Unix(),
    }

    d.webhookClient.Send(payload)
}
```

### 3. 事件监听器

```go
// 事件监听器
type EventListener struct {
    dispatcher *EventDispatcher
    informer   cache.SharedInformer
}

func NewEventListener(dispatcher *EventDispatcher, informer cache.SharedInformer) *EventListener {
    return &EventListener{
        dispatcher: dispatcher,
        informer:   informer,
    }
}

func (l *EventListener) Start(ctx context.Context) error {
    l.informer.AddEventHandler(cache.ResourceEventHandlerFuncs{
        AddFunc: func(obj interface{}) {
            vm := obj.(*VirtualMachine)
            l.dispatcher.NotifyVMCreated(vm)
        },
        UpdateFunc: func(oldObj, newObj interface{}) {
            oldVM := oldObj.(*VirtualMachine)
            newVM := newObj.(*VirtualMachine)

            // 检查是否是迁移事件
            if oldVM.Status.NodeName != newVM.Status.NodeName {
                l.dispatcher.NotifyVMMigrated(newVM, newVM.Status.NodeName)
            }
        },
        DeleteFunc: func(obj interface{}) {
            vm := obj.(*VirtualMachine)
            l.dispatcher.NotifyVMDeleted(vm)
        },
    })

    go l.informer.Run(ctx.Done())

    return nil
}
```

---

## 关键技术分析

### 1. Kubernetes Events

**优势**：

- 统一的事件记录机制
- 支持事件查询和过滤
- 与 Kubernetes 原生事件系统集成

**实现**：

```go
// 使用 Kubernetes EventRecorder
eventRecorder := record.NewEventRecorder(client, scheme)
eventRecorder.Event(vm, "Normal", "Created", "VM created successfully")
```

### 2. Custom Resource Watch

**优势**：

- 实时事件通知
- 支持事件过滤和选择
- 与 Kubernetes Watch API 集成

**实现**：

```go
// 使用 Kubernetes Watch API
watcher, err := client.KubevirtV1().VirtualMachines(namespace).Watch(ctx, metav1.ListOptions{})
for event := range watcher.ResultChan() {
    switch event.Type {
    case watch.Added:
        dispatcher.NotifyVMCreated(event.Object.(*VirtualMachine))
    case watch.Modified:
        dispatcher.NotifyVMUpdated(event.Object.(*VirtualMachine))
    case watch.Deleted:
        dispatcher.NotifyVMDeleted(event.Object.(*VirtualMachine))
    }
}
```

### 3. Webhook 通知

**优势**：

- 支持外部系统集成
- 灵活的事件处理
- 可扩展的事件通知机制

**实现**：

```go
// Webhook 通知
webhookClient := webhook.NewClient(webhookURL)
dispatcher := NewEventDispatcher(eventRecorder, webhookClient)
```

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [声明式 API 设计模式](../07-api-design-patterns/01-declarative-api.md) - 声明
  式 API
- [适配器模式：统一异构运行时](../07-api-design-patterns/02-adapter-pattern.md) -
  适配器模式
- [策略模式：多租户配额策略](../07-api-design-patterns/03-strategy-pattern.md) -
  策略模式
- [监控指标统一采集](../04-operations-monitoring/01-unified-monitoring.md) - 监
  控指标采集

---

## 2025 年最新实践

### 观察者模式最佳实践（2025）

**2025 年趋势**：观察者模式的深度应用

**实践要点**：

- **统一事件通知**：通过观察者模式实现容器和虚拟机的统一事件通知
- **事件观察者**：监控观察者、告警观察者、审计观察者
- **事件分发器**：统一事件分发器管理所有观察者

**代码示例**：

```python
# 2025 年观察者模式应用工具
class EventObserverManager:
    def __init__(self):
        self.observers = []
        self.dispatcher = EventDispatcher()

    def register_observer(self, observer):
        """注册观察者"""
        self.observers.append(observer)
        self.dispatcher.add_observer(observer)

    def notify_event(self, event_type, event_data):
        """通知事件"""
        self.dispatcher.notify(event_type, event_data)
```

## 实际应用案例

### 案例 1：统一事件通知（2025）

**场景**：使用观察者模式实现容器和虚拟机的统一事件通知

**实现方案**：

```yaml
# 事件观察者配置
apiVersion: v1
kind: ConfigMap
metadata:
  name: event-observers
data:
  observers.yaml: |
    - type: monitoring
      endpoint: prometheus:9090
    - type: alerting
      endpoint: alertmanager:9093
    - type: auditing
      endpoint: audit-service:8080
```

**效果**：

- 统一事件通知：通过观察者模式实现容器和虚拟机的统一事件通知
- 事件观察者：监控观察者、告警观察者、审计观察者
- 事件分发器：统一事件分发器管理所有观察者

---

**最后更新**：2025-11-15 **维护者**：项目团队
