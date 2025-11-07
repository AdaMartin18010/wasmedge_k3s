# API 事件驱动架构规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 事件驱动架构](#11-事件驱动架构)
- [2. 事件架构](#2-事件架构)
  - [2.1 事件定义](#21-事件定义)
  - [2.2 事件总线](#22-事件总线)
- [3. 事件发布](#3-事件发布)
  - [3.1 事件发布 API](#31-事件发布-api)
  - [3.2 事件发布实现](#32-事件发布实现)
- [4. 事件订阅](#4-事件订阅)
  - [4.1 事件订阅配置](#41-事件订阅配置)
  - [4.2 事件处理](#42-事件处理)
- [5. 事件流处理](#5-事件流处理)
  - [5.1 Kafka Streams](#51-kafka-streams)
  - [5.2 Flink 流处理](#52-flink-流处理)
- [6. 事件存储](#6-事件存储)
  - [6.1 事件存储配置](#61-事件存储配置)
  - [6.2 事件查询](#62-事件查询)
- [7. 事件溯源](#7-事件溯源)
  - [7.1 事件溯源模式](#71-事件溯源模式)
  - [7.2 事件重放](#72-事件重放)
- [8. 相关文档](#8-相关文档)

---

## 1. 概述

API 事件驱动架构规范定义了 API 在事件驱动架构下的设计和实现，从事件发布到事件订
阅，从事件流处理到事件存储。

### 1.1 事件驱动架构

```text
事件生产者（Event Producer）
  ↓
事件总线（Event Bus）
  ↓
事件消费者（Event Consumer）
  ↓
事件存储（Event Store）
```

---

## 2. 事件架构

### 2.1 事件定义

**CloudEvents 标准**：

```yaml
apiVersion: api.example.com/v1
kind: EventDefinition
metadata:
  name: payment-created-event
spec:
  type: com.example.payment.created
  source: payment-service
  schema: |
    {
      "type": "object",
      "properties": {
        "payment_id": {"type": "string"},
        "order_id": {"type": "string"},
        "amount": {"type": "number"}
      }
    }
```

### 2.2 事件总线

**Kafka 事件总线**：

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: payment-events
spec:
  partitions: 3
  replicas: 3
  config:
    retention.ms: 604800000
    segment.ms: 86400000
```

---

## 3. 事件发布

### 3.1 事件发布 API

**事件发布端点**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-api-events
spec:
  paths:
    /api/v1/events:
      post:
        summary: Publish event
        requestBody:
          content:
            application/cloudevents+json:
              schema:
                $ref: "#/components/schemas/CloudEvent"
```

### 3.2 事件发布实现

**Go 事件发布**：

```go
package main

import (
    "github.com/cloudevents/sdk-go/v2/event"
    "github.com/cloudevents/sdk-go/v2/protocol/kafka"
)

func publishPaymentCreatedEvent(paymentID, orderID string, amount int64) error {
    e := event.New()
    e.SetType("com.example.payment.created")
    e.SetSource("payment-service")
    e.SetData("application/json", map[string]interface{}{
        "payment_id": paymentID,
        "order_id":   orderID,
        "amount":     amount,
    })

    p, _ := kafka.New(kafka.WithConfigMap(map[string]interface{}{
        "bootstrap.servers": "kafka:9092",
    }))

    return p.Send(context.Background(), e)
}
```

---

## 4. 事件订阅

### 4.1 事件订阅配置

**Kafka Consumer 配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kafka-consumer-config
data:
  consumer.properties: |
    bootstrap.servers=kafka:9092
    group.id=payment-processors
    auto.offset.reset=earliest
    enable.auto.commit=true
```

### 4.2 事件处理

**事件处理实现**：

```go
package main

import (
    "github.com/IBM/sarama"
)

func handlePaymentCreatedEvent(message *sarama.ConsumerMessage) error {
    var event PaymentCreatedEvent
    if err := json.Unmarshal(message.Value, &event); err != nil {
        return err
    }

    // 处理支付创建事件
    return processPaymentCreated(event)
}
```

---

## 5. 事件流处理

### 5.1 Kafka Streams

**Kafka Streams 配置**：

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaStreams
metadata:
  name: payment-streams
spec:
  replicas: 3
  bootstrapServers: kafka:9092
  topics:
    - name: payment-events
      pattern: "payment-.*"
```

### 5.2 Flink 流处理

**Flink Job 配置**：

```yaml
apiVersion: flink.apache.org/v1beta1
kind: FlinkDeployment
metadata:
  name: payment-flink-job
spec:
  image: flink:1.17
  flinkVersion: v1_17
  jobManager:
    resource:
      memory: "2048m"
      cpu: 1
  taskManager:
    resource:
      memory: "2048m"
      cpu: 1
  job:
    jarURI: local:///opt/flink/lib/payment-processor.jar
    parallelism: 3
```

---

## 6. 事件存储

### 6.1 事件存储配置

**EventStore 配置**：

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: eventstore
spec:
  serviceName: eventstore
  replicas: 3
  template:
    spec:
      containers:
        - name: eventstore
          image: eventstore/eventstore:latest
          env:
            - name: EVENTSTORE_CLUSTER_SIZE
              value: "3"
            - name: EVENTSTORE_CLUSTER_GOSSIP_PORT
              value: "2112"
```

### 6.2 事件查询

**事件查询 API**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: event-query-api
spec:
  paths:
    /api/v1/events:
      get:
        summary: Query events
        parameters:
          - name: stream
            in: query
            schema:
              type: string
          - name: from
            in: query
            schema:
              type: integer
          - name: limit
            in: query
            schema:
              type: integer
```

---

## 7. 事件溯源

### 7.1 事件溯源模式

**事件溯源实现**：

```go
package main

type PaymentAggregate struct {
    ID      string
    OrderID string
    Amount  int64
    Status  string
    Events  []Event
}

func (a *PaymentAggregate) ApplyEvent(e Event) {
    switch e.Type {
    case "PaymentCreated":
        a.Status = "created"
    case "PaymentProcessed":
        a.Status = "processed"
    case "PaymentCompleted":
        a.Status = "completed"
    }
    a.Events = append(a.Events, e)
}
```

### 7.2 事件重放

**事件重放配置**：

```yaml
apiVersion: api.example.com/v1
kind: EventReplay
metadata:
  name: payment-replay
spec:
  stream: payment-stream
  from: 0
  to: latest
  handler: payment-aggregate
```

---

## 8. 相关文档

- **[API 生态系统集成](../26-api-ecosystem/api-ecosystem.md)** - 消息队列集成
- **[API 架构设计](../01-containerization-api/containerization-api.md)** - 架构
  模式
- **[最佳实践](../08-best-practices/best-practices.md)** - 事件驱动最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新**：2025-11-07 **维护者**：项目团队
