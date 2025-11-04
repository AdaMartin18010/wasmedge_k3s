# 适配器/桥接模式：跨技术边界

## 1. 概述

**适配器/桥接模式**用于让**不同技术栈**的组件能够无缝协作，实现跨技术边界的组合
。

### 1.1 核心思想

> **让旧系统与新模块无缝衔接，或让不同技术栈的组件能够互操作**

## 2. 适配器模式（Adapter Pattern）

### 2.1 定义

**适配器模式**将一个类的接口转换成客户希望的另一个接口，使原本由于接口不兼容而不
能一起工作的类可以一起工作。

### 2.2 典型场景

#### 2.2.1 gRPC ↔ REST

**场景**：前端使用 REST，后端使用 gRPC

**解决方案**：

- **gRPC-Gateway**：将 gRPC 服务暴露为 REST API
- **Envoy**：在 Service Mesh 中自动转换

**示例**：

```yaml
# gRPC-Gateway 配置
apiVersion: v1
kind: Service
metadata:
  name: grpc-gateway
spec:
  ports:
    - name: http
      port: 8080
      targetPort: 9090
    - name: grpc
      port: 9090
      targetPort: 9090
```

#### 2.2.2 Docker ↔ Kubernetes

**场景**：从 Docker Compose 迁移到 Kubernetes

**解决方案**：

- **Kompose**：将 Docker Compose 转换为 Kubernetes YAML
- **Docker Desktop**：在本地运行 Kubernetes

**示例**：

```bash
# 使用 Kompose 转换
kompose convert
```

### 2.3 形式化定义

```text
适配器 A = ⟨source, target, transform⟩
其中：
- source: 源接口
- target: 目标接口
- transform: 转换函数
```

## 3. 桥接模式（Bridge Pattern）

### 3.1 定义

**桥接模式**将抽象部分与实现部分分离，使它们都可以独立地变化。

### 3.2 典型场景

#### 3.2.1 ODBC ↔ JDBC

**场景**：跨数据库访问

**解决方案**：

- **ODBC**：开放数据库连接标准
- **JDBC**：Java 数据库连接
- **桥接层**：ODBC-JDBC Bridge

#### 3.2.2 容器运行时桥接

**场景**：在不同容器运行时之间切换

**解决方案**：

- **CRI (Container Runtime Interface)**：Kubernetes 容器运行时接口
- **containerd**：实现 CRI 的容器运行时
- **CRI-O**：另一个 CRI 实现

**示例**：

```yaml
# Kubernetes 配置不同的运行时
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: kata
handler: kata
```

### 3.3 形式化定义

```text
桥接 B = ⟨abstraction, implementation, bridge⟩
其中：
- abstraction: 抽象层
- implementation: 实现层
- bridge: 桥接层
```

## 4. Service Mesh 中的适配器

### 4.1 Envoy 适配器

**Envoy** 作为 Service Mesh 的数据平面，提供多种适配器：

- **HTTP → gRPC**：自动转换
- **gRPC → HTTP**：自动转换
- **WebSocket → HTTP**：协议转换
- **TCP → HTTP**：协议升级

### 4.2 Istio 适配器

**Istio** 提供多种适配器：

- **Prometheus**：指标适配器
- **Jaeger**：追踪适配器
- **Fluentd**：日志适配器

### 4.3 示例配置

```yaml
# Istio Adapter 配置
apiVersion: config.istio.io/v1alpha2
kind: adapter
metadata:
  name: prometheus
spec:
  config:
    metrics:
      - name: requests_total
        type: COUNTER
```

## 5. 容器运行时适配器

### 5.1 CRI 适配器

**CRI (Container Runtime Interface)** 是 Kubernetes 的容器运行时接口，提供：

- **containerd**：实现 CRI
- **CRI-O**：另一个 CRI 实现
- **Docker**：通过 containerd 适配

### 5.2 RuntimeClass

**RuntimeClass** 允许在 Pod 级别选择不同的容器运行时：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  runtimeClassName: kata
  containers:
    - name: my-container
      image: my-image
```

## 6. 网络适配器

### 6.1 CNI 适配器

**CNI (Container Network Interface)** 是 Kubernetes 的网络接口，提供：

- **Calico**：网络策略
- **Flannel**：简单网络
- **Cilium**：eBPF 网络

### 6.2 网络桥接

**网络桥接**用于连接不同的网络：

- **VXLAN**：虚拟扩展局域网
- **Geneve**：通用网络虚拟化封装
- **Bridge**：Linux 桥接

## 7. 最佳实践

### 7.1 适配器设计原则

1. **单一职责**：每个适配器只负责一种转换
2. **接口稳定**：适配器接口应该稳定
3. **性能优化**：减少转换开销
4. **错误处理**：优雅处理转换错误

### 7.2 桥接设计原则

1. **抽象与实现分离**：抽象层和实现层应该独立
2. **接口设计**：定义清晰的接口
3. **可扩展性**：支持多种实现
4. **性能考虑**：减少桥接开销

## 8. 总结

适配器/桥接模式通过**跨技术边界**实现了：

1. **无缝集成**：让不同技术栈的组件能够协作
2. **协议转换**：gRPC ↔ REST、HTTP ↔ WebSocket
3. **运行时适配**：容器运行时、网络运行时
4. **Service Mesh 适配**：Envoy、Istio 适配器
5. **可扩展性**：支持多种实现和转换

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
78-92 行，组合模式部分
