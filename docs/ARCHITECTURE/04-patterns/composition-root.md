# Composition Root 模式

## 📑 目录

- [1. 概述](#1-概述)
  - [1.1 核心思想](#11-核心思想)
- [2. 目标与定义](#2-目标与定义)
- [3. 模式结构](#3-模式结构)
  - [3.1 基本结构](#31-基本结构)
  - [3.2 在云原生架构中的应用](#32-在云原生架构中的应用)
- [4. 在云原生架构中的应用](#4-在云原生架构中的应用)
  - [4.1 Kubernetes 中的 Composition Root](#41-kubernetes-中的-composition-root)
  - [4.2 Service Mesh 中的 Composition Root](#42-service-mesh-中的-composition-root)
  - [4.3 OPA 中的 Composition Root](#43-opa-中的-composition-root)
- [5. Composition Root 的优势](#5-composition-root-的优势)
  - [5.1 依赖关系清晰](#51-依赖关系清晰)
  - [5.2 可测试性](#52-可测试性)
  - [5.3 可维护性](#53-可维护性)
- [6. Composition Root 的最佳实践](#6-composition-root-的最佳实践)
  - [6.1 单一入口点](#61-单一入口点)
  - [6.2 延迟创建](#62-延迟创建)
  - [6.3 生命周期管理](#63-生命周期管理)
- [7. 在云原生架构中的实践](#7-在云原生架构中的实践)
  - [7.1 Kubernetes Deployment](#71-kubernetes-deployment)
  - [7.2 Istio VirtualService](#72-istio-virtualservice)
  - [7.3 OPA Policy Bundle](#73-opa-policy-bundle)
- [8. 总结](#8-总结)
  - [核心价值](#核心价值)
  - [一句话归纳](#一句话归纳)
- [9. 参考资源](#9-参考资源)
  - [学术资源](#学术资源)

---

## 1. 概述

本文档详细阐述**Composition Root 模式**在云原生架构中的应用，包括
Kubernetes、Service Mesh、OPA 等场景。

### 1.1 核心思想

> **Composition Root 模式通过在应用程序的单一入口点组合所有依赖关系，确保依赖关
> 系清晰、可测试、可维护**

---

## 2. 目标与定义

**Composition Root** 模式是依赖注入的核心模式，它定义了在应用程序的入口点
（root）组合所有依赖关系的地方。

> **核心思想**：在应用程序的 **单一入口点** 组合所有依赖关系，而不是在应用程序的
> 各个地方分散创建依赖。这样可以确保依赖关系清晰、可测试、可维护。

---

## 3. 模式结构

### 3.1 基本结构

```text
Application Entry Point (Composition Root)
    ├─ 依赖注入容器（DI Container）
    ├─ 注册所有依赖关系
    ├─ 创建对象图
    └─ 启动应用程序
```

### 3.2 在云原生架构中的应用

| 层次       | Composition Root 应用                 | 典型实现           |
| ---------- | ------------------------------------- | ------------------ |
| **应用层** | Spring DI、Guice、Dagger              | Spring Boot、Guice |
| **容器层** | Kubernetes Pod 定义                   | Kubernetes         |
| **网格层** | Istio VirtualService、DestinationRule | Istio              |
| **策略层** | OPA Policy Bundle                     | OPA                |

---

## 4. 在云原生架构中的应用

### 4.1 Kubernetes 中的 Composition Root

在 Kubernetes 中，**Pod 定义** 就是 Composition Root：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: orders-service
spec:
  containers:
    - name: orders
      image: orders:1.0.0
      env:
        - name: DB_HOST
          value: postgres-service
        - name: MESH_ADDR
          value: istio-sidecar
    - name: istio-proxy
      image: istio/proxy:1.21.0
```

**Composition Root 的作用**：

- 定义容器的依赖关系（数据库、Service Mesh）
- 配置环境变量和资源限制
- 注入 sidecar（如 Istio proxy）

### 4.2 Service Mesh 中的 Composition Root

在 Service Mesh 中，**VirtualService** 和 **DestinationRule** 就是 Composition
Root：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: orders
spec:
  hosts:
    - orders
  http:
    - route:
        - destination:
            host: orders
            subset: v1
          weight: 90
        - destination:
            host: orders
            subset: v2
          weight: 10
```

**Composition Root 的作用**：

- 定义服务间的路由规则
- 配置流量分发策略
- 注入策略（如重试、超时、熔断）

### 4.3 OPA 中的 Composition Root

在 OPA 中，**Policy Bundle** 就是 Composition Root：

```rego
package authz

# Composition Root: 定义所有策略规则
default allow = false

allow {
    input.user.role == "admin"
    input.operation == "create"
}
```

**Composition Root 的作用**：

- 定义所有策略规则
- 组合多个策略（如认证、授权、审计）
- 注入策略数据（如用户角色、资源权限）

---

## 5. Composition Root 的优势

### 5.1 依赖关系清晰

**问题**：依赖关系分散在应用程序的各个地方，难以追踪和管理

**解决方案**：在 Composition Root 集中定义所有依赖关系

```text
分散的依赖关系（难以管理）
├─ Service A → DB
├─ Service B → Cache
├─ Service C → Message Queue
└─ ...

集中的依赖关系（易于管理）
└─ Composition Root
    ├─ Service A → DB
    ├─ Service B → Cache
    └─ Service C → Message Queue
```

### 5.2 可测试性

**问题**：依赖关系硬编码，难以进行单元测试

**解决方案**：在 Composition Root 中注入测试依赖

```text
生产环境 Composition Root
└─ Service → Production DB

测试环境 Composition Root
└─ Service → Test DB (Mock)
```

### 5.3 可维护性

**问题**：依赖关系变更需要修改多个地方

**解决方案**：在 Composition Root 中集中管理依赖关系

```text
依赖关系变更
├─ 修改 Composition Root（单一位置）
└─ 自动应用到所有服务
```

---

## 6. Composition Root 的最佳实践

### 6.1 单一入口点

**原则**：在应用程序的单一入口点组合所有依赖关系

```text
Application Entry Point
    ├─ Composition Root
    │   ├─ 注册依赖
    │   ├─ 创建对象图
    │   └─ 启动应用
    └─ Application Logic
```

### 6.2 延迟创建

**原则**：在需要时才创建依赖对象，而不是在启动时创建所有对象

```text
Lazy Composition Root
    ├─ 注册依赖关系（启动时）
    └─ 创建依赖对象（使用时）
```

### 6.3 生命周期管理

**原则**：在 Composition Root 中管理依赖对象的生命周期

```text
Lifecycle Management
    ├─ 创建（启动时）
    ├─ 使用（运行时）
    └─ 销毁（关闭时）
```

---

## 7. 在云原生架构中的实践

### 7.1 Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: orders
          image: orders:1.0.0
          # Composition Root: 定义依赖关系
          env:
            - name: DB_HOST
              valueFrom:
                configMapKeyRef:
                  name: orders-config
                  key: db-host
            - name: MESH_ADDR
              valueFrom:
                serviceAccountKeyRef:
                  name: istio-service-account
                  key: mesh-addr
```

### 7.2 Istio VirtualService

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: orders
spec:
  hosts:
    - orders
  # Composition Root: 定义路由规则
  http:
    - match:
        - headers:
            x-canary:
              exact: "1"
      route:
        - destination:
            host: orders
            subset: v2
          weight: 100
    - route:
        - destination:
            host: orders
            subset: v1
          weight: 90
        - destination:
            host: orders
            subset: v2
          weight: 10
```

### 7.3 OPA Policy Bundle

```rego
package authz

# Composition Root: 定义所有策略规则
default allow = false

# 认证策略
import data.authn.users

# 授权策略
import data.authz.roles

# 审计策略
import data.audit.logs

allow {
    # 组合多个策略
    users[input.user].authenticated
    roles[input.user].allowed[input.operation]
    audit.log(input)
}
```

---

## 8. 总结

### 核心价值

1. **依赖关系清晰**：在单一入口点集中管理依赖关系
2. **可测试性**：易于注入测试依赖
3. **可维护性**：依赖关系变更只需修改单一位置

### 一句话归纳

> **Composition Root 模式通过在应用程序的单一入口点组合所有依赖关系，确保依赖关
> 系清晰、可测试、可维护**。

---

## 9. 参考资源

- **依赖注入**：<https://martinfowler.com/articles/injection.html>
- **Composition Root**：<https://blog.ploeh.dk/2011/07/28/CompositionRoot/>
- **Kubernetes**：<https://kubernetes.io>
- **Istio**：<https://istio.io>
- **OPA**：<https://www.openpolicyagent.org>
- **相关文档**：
  - `architecture-view/08-composition-patterns/04-service-mesh-pattern.md` -
    Service Mesh 模式
  - `architecture-view/04-opa-policy-governance/` - OPA 模式
  - `architecture-view/08-composition-patterns/README.md` - 组合模式概述

### 学术资源

- **[ACADEMIC-REFERENCES.md](../ACADEMIC-REFERENCES.md)** - Wikipedia、大学课程
  、学术论文等学术资源
- **[REFERENCES.md](../REFERENCES.md)** - 参考标准、框架、工具和资源

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md`
Composition Root 模式部分
