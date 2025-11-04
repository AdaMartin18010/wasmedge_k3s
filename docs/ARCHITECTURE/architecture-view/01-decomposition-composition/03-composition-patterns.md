# 组合模式：让拆分出的组件互联、互操作

## 1. 概述

本文档详细阐述**组合模式**，这是让拆分出的组件能够互联、互操作的关键方法。

### 1.1 核心思想

> **使用成熟的组合模式（Adapter, Facade, Composite, Pipeline, Orchestration,
> Service Mesh 等）把子结构"拼接"成最终的应用**

## 2. 组合模式类型

### 2.1 组合模式概览

| 组合模式                                            | 作用           | 典型技术/工具                                    | 典型案例                       |
| --------------------------------------------------- | -------------- | ------------------------------------------------ | ------------------------------ |
| **Composition Root**                                | 全局依赖注入   | Spring DI, Guice, Dagger, CDI                    | 业务层注入领域服务             |
| **Adapter / Bridge**                                | 跨技术边界     | gRPC + REST, ODBC ↔ JDBC                         | 通过 gRPC 转为 REST 供前端使用 |
| **Facade / Gateway**                                | 聚合多服务     | Netflix Zuul, Kong, Ocelot, Spring Cloud Gateway | 单一入口聚合内部 API           |
| **Composite**                                       | 递归聚合       | Composite pattern, Tree‑structured UI            | 目录树、权限树                 |
| **Pipeline / Orchestrator**                         | 业务流程       | Camunda, Temporal, Argo Workflows                | 长事务、订单处理               |
| **Service Mesh**                                    | 细粒度流量控制 | Istio, Linkerd, Consul                           | 侧车代理、熔断、流量镜像       |
| **Event Bus**                                       | 解耦、异步     | Kafka, NATS, RabbitMQ                            | 订单已完成 → 发送邮件          |
| **Command Query Responsibility Segregation (CQRS)** | 读写分离       | Axon, Lagom                                      | 大量查询读写分离               |
| **Domain Event**                                    | 领域事件       | Axon, EventStore                                 | 订单创建 → 业务服务触发        |
| **Feature Flags**                                   | 代码切换       | LaunchDarkly, Unleash                            | 实验性功能逐步推送             |
| **Infrastructure as Code**                          | 自动化部署     | Terraform, Helm, Pulumi                          | 同步基础设施与代码             |
| **Observability as a Service**                      | 统一监控       | OpenTelemetry Collector, Grafana Loki            | 日志/指标/追踪一体化           |

## 3. Composition Root（组合根）

### 3.1 定义

**Composition Root** 是全局依赖注入的入口点，负责组装所有组件。

### 3.2 典型实现

#### 3.2.1 Spring DI

```java
@Configuration
public class AppConfig {
    @Bean
    public OrderService orderService(OrderRepository repository) {
        return new OrderService(repository);
    }

    @Bean
    public OrderRepository orderRepository(DataSource dataSource) {
        return new JdbcOrderRepository(dataSource);
    }
}
```

#### 3.2.2 Guice

```java
public class AppModule extends AbstractModule {
    @Override
    protected void configure() {
        bind(OrderService.class).to(OrderServiceImpl.class);
        bind(OrderRepository.class).to(JdbcOrderRepository.class);
    }
}
```

### 3.3 形式化定义

```text
CompositionRoot = ⟨components, dependencies, bindings⟩
其中：
- components: 组件集合
- dependencies: 依赖关系
- bindings: 绑定配置
```

## 4. Adapter / Bridge（适配器/桥接）

### 4.1 定义

**Adapter / Bridge** 用于跨技术边界，让不同技术栈的组件能够协作。

### 4.2 典型场景

#### 4.2.1 gRPC ↔ REST

**场景**：前端使用 REST，后端使用 gRPC

**解决方案**：

- **gRPC-Gateway**：将 gRPC 服务暴露为 REST API
- **Envoy**：在 Service Mesh 中自动转换

#### 4.2.2 ODBC ↔ JDBC

**场景**：跨数据库访问

**解决方案**：

- **ODBC-JDBC Bridge**：桥接 ODBC 和 JDBC

### 4.3 形式化定义

```text
Adapter = ⟨source, target, transform⟩
其中：
- source: 源接口
- target: 目标接口
- transform: 转换函数
```

## 5. Facade / Gateway（门面/网关）

### 5.1 定义

**Facade / Gateway** 用于聚合多服务，提供单一入口。

### 5.2 典型场景

#### 5.2.1 API Gateway

**场景**：聚合多个微服务 API

**解决方案**：

- **Kong**：API Gateway
- **Istio Gateway**：服务网格网关
- **Spring Cloud Gateway**：Spring 生态网关

#### 5.2.2 BFF（Backend for Frontend）

**场景**：为不同前端提供定制化 API

**解决方案**：

- **GraphQL**：统一查询接口
- **BFF Service**：前端专用后端服务

### 5.3 形式化定义

```text
Facade = ⟨services, aggregation, interface⟩
其中：
- services: 被聚合的服务集合
- aggregation: 聚合逻辑
- interface: 对外接口
```

## 6. Composite（组合）

### 6.1 定义

**Composite** 用于递归聚合，组织成树状结构。

### 6.2 典型场景

#### 6.2.1 目录树

**场景**：文件系统目录结构

**解决方案**：

- **Composite Pattern**：组合模式
- **Tree Structure**：树形结构

#### 6.2.2 权限树

**场景**：组织权限结构

**解决方案**：

- **RBAC**：基于角色的访问控制
- **权限树**：层次化权限结构

### 6.3 形式化定义

```text
Composite = ⟨components, tree, operations⟩
其中：
- components: 组件集合
- tree: 树形结构
- operations: 操作集合
```

## 7. Pipeline / Orchestrator（流水线/编排）

### 7.1 定义

**Pipeline / Orchestrator** 用于业务流程编排。

### 7.2 典型场景

#### 7.2.1 长事务

**场景**：跨多个服务的长时间事务

**解决方案**：

- **Saga**：分布式事务模式
- **Temporal**：工作流引擎

#### 7.2.2 订单处理

**场景**：订单创建、支付、发货流程

**解决方案**：

- **Argo Workflows**：Kubernetes 工作流
- **Camunda**：业务流程管理

### 7.3 形式化定义

```text
Pipeline = ⟨stages, flow, orchestration⟩
其中：
- stages: 阶段集合
- flow: 流程定义
- orchestration: 编排逻辑
```

## 8. Service Mesh（服务网格）

### 8.1 定义

**Service Mesh** 用于细粒度流量控制，提供侧车代理。

### 8.2 典型场景

#### 8.2.1 微服务通信

**场景**：微服务间通信、熔断、限流

**解决方案**：

- **Istio**：服务网格
- **Linkerd**：轻量级服务网格
- **Consul**：HashiCorp 服务网格

#### 8.2.2 流量镜像

**场景**：将生产流量镜像到测试环境

**解决方案**：

- **Envoy**：云原生代理
- **Istio VirtualService**：虚拟服务配置

### 8.3 形式化定义

```text
ServiceMesh = ⟨sidecars, controlPlane, policies⟩
其中：
- sidecars: 侧车代理集合
- controlPlane: 控制平面
- policies: 策略配置
```

## 9. Event Bus（事件总线）

### 9.1 定义

**Event Bus** 用于解耦、异步通信。

### 9.2 典型场景

#### 9.2.1 订单已完成 → 发送邮件

**场景**：订单完成后异步发送邮件

**解决方案**：

- **Kafka**：分布式消息队列
- **RabbitMQ**：消息队列
- **NATS**：轻量级消息系统

### 9.3 形式化定义

```text
EventBus = ⟨topics, producers, consumers, routing⟩
其中：
- topics: 主题集合
- producers: 生产者集合
- consumers: 消费者集合
- routing: 路由规则
```

## 10. CQRS（命令查询责任分离）

### 10.1 定义

**CQRS** 用于读写分离，提高系统性能。

### 10.2 典型场景

#### 10.2.1 大量查询读写分离

**场景**：读多写少的系统

**解决方案**：

- **Axon**：CQRS 框架
- **Lagom**：响应式微服务框架

### 10.3 形式化定义

```text
CQRS = ⟨command, query, readModel, writeModel⟩
其中：
- command: 命令模型
- query: 查询模型
- readModel: 读模型
- writeModel: 写模型
```

## 11. 组合策略：从微服务到无服务器

| 目标                     | 组合层级        | 典型技术                               | 关键要点                     |
| ------------------------ | --------------- | -------------------------------------- | ---------------------------- |
| **微服务**               | 业务层 + 数据层 | Docker, K8s, Service Mesh              | 每个服务独立部署、独立扩容   |
| **Serverless**           | 业务层          | AWS Lambda, Azure Functions, OpenFaaS  | 按事件自动弹性扩容           |
| **Backend‑for‑Frontend** | API 聚合        | GraphQL, Apollo, Hasura                | 前端只调用单一接口           |
| **Polyglot Persistence** | 数据层          | PostgreSQL, MongoDB, ElasticSearch     | 每种数据模型选最合适存储     |
| **Event‑Sourcing**       | 业务层          | Kafka, EventStore                      | 所有状态由事件重放得到       |
| **Multi‑tenant**         | 应用层          | Istio + namespace, tenant‑aware config | 每租户拥有独立命名空间、限额 |
| **Edge Computing**       | 交付层          | Cloudflare Workers, AWS Greengrass     | 在网络边缘处理请求           |
| **Hybrid Cloud**         | 基础设施层      | Terraform + Crossplane                 | 同一套 IaC 管理公有与私有云  |

## 12. 总结

通过**组合模式**，我们可以：

1. **互联组件**：让拆分出的组件能够相互通信
2. **互操作**：让不同技术栈的组件能够协作
3. **解耦**：通过事件总线、服务网格等解耦组件
4. **聚合**：通过 Facade、Gateway 聚合多个服务
5. **编排**：通过 Pipeline、Orchestrator 编排业务流程

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
76-114 行，组合模式部分
