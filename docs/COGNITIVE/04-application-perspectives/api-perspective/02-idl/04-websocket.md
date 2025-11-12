# API WebSocket 规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 WebSocket API 架构](#11-websocket-api-架构)
  - [1.2 API WebSocket 在 API 规范中的位置](#12-api-websocket-在-api-规范中的位置)
- [2 WebSocket 连接](#2-websocket-连接)
  - [2.1 连接建立](#21-连接建立)
  - [2.2 连接管理](#22-连接管理)
- [3 消息协议](#3-消息协议)
  - [3.1 消息格式](#31-消息格式)
  - [3.2 消息类型](#32-消息类型)
- [4 心跳和保活](#4-心跳和保活)
  - [4.1 Ping/Pong 机制](#41-pingpong-机制)
  - [4.2 超时配置](#42-超时配置)
- [5 错误处理](#5-错误处理)
  - [5.1 错误码定义](#51-错误码定义)
  - [5.2 错误恢复](#52-错误恢复)
- [6 性能优化](#6-性能优化)
  - [6.1 连接池](#61-连接池)
  - [6.2 消息压缩](#62-消息压缩)
- [7 形式化定义与理论基础](#7-形式化定义与理论基础)
  - [7.1 API WebSocket 形式化模型](#71-api-websocket-形式化模型)
  - [7.2 连接管理形式化](#72-连接管理形式化)
  - [7.3 消息传输形式化](#73-消息传输形式化)
- [8 相关文档](#8-相关文档)

---

## 1 概述

API WebSocket 规范定义了 API 在 WebSocket 架构下的设计和实现，从连接建立到消息协
议，从心跳保活到性能优化。本文档基于形式化方法，提供严格的数学定义和推理论证，分
析 API WebSocket 的理论基础和实践方法。

**参考标准**：

- [WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455) -
  WebSocket 协议规范
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) -
  WebSocket API
- [Socket.IO](https://socket.io/) - Socket.IO 实时通信
- [WebSocket Best Practices](https://www.websocket.org/aboutwebsocket.html) -
  WebSocket 最佳实践
- [Real-time Communication](https://www.w3.org/TR/websockets/) - W3C WebSocket
  标准

### 1.1 WebSocket API 架构

```text
WebSocket 客户端（Client）
  ↓
WebSocket 服务器（Server）
  ↓
消息路由（Message Router）
  ↓
业务处理（Business Logic）
```

### 1.2 API WebSocket 在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API WebSocket 主要涉及 IDL 和 Observability 维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
            ↑                        ↑
    WebSocket (implementation)
```

API WebSocket 在 API 规范中提供：

- **连接管理**：WebSocket 连接建立和管理
- **消息协议**：消息格式和类型定义
- **心跳保活**：Ping/Pong 机制
- **实时通信**：双向实时数据传输

---

## 2 WebSocket 连接

### 2.1 连接建立

**WebSocket 握手**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: websocket-service
spec:
  hosts:
    - websocket.example.com
  http:
    - match:
        - headers:
            upgrade:
              exact: websocket
      route:
        - destination:
            host: websocket-backend
          weight: 100
```

**Go WebSocket 服务器**：

```go
package main

import (
    "github.com/gorilla/websocket"
    "net/http"
)

var upgrader = websocket.Upgrader{
    CheckOrigin: func(r *http.Request) bool {
        return true
    },
}

func handleWebSocket(w http.ResponseWriter, r *http.Request) {
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        return
    }
    defer conn.Close()

    for {
        messageType, message, err := conn.ReadMessage()
        if err != nil {
            break
        }

        // 处理消息
        response := processMessage(message)

        if err := conn.WriteMessage(messageType, response); err != nil {
            break
        }
    }
}
```

### 2.2 连接管理

**连接管理器**：

```go
type ConnectionManager struct {
    connections map[string]*websocket.Conn
    mutex       sync.RWMutex
}

func (cm *ConnectionManager) AddConnection(id string, conn *websocket.Conn) {
    cm.mutex.Lock()
    defer cm.mutex.Unlock()
    cm.connections[id] = conn
}

func (cm *ConnectionManager) RemoveConnection(id string) {
    cm.mutex.Lock()
    defer cm.mutex.Unlock()
    delete(cm.connections, id)
}

func (cm *ConnectionManager) Broadcast(message []byte) {
    cm.mutex.RLock()
    defer cm.mutex.RUnlock()

    for _, conn := range cm.connections {
        conn.WriteMessage(websocket.TextMessage, message)
    }
}
```

---

## 3 消息协议

### 3.1 消息格式

**JSON 消息格式**：

```json
{
  "type": "payment.created",
  "id": "msg_123",
  "timestamp": "2025-11-07T10:00:00Z",
  "data": {
    "payment_id": "pay_456",
    "order_id": "order_789",
    "amount": 10000,
    "status": "completed"
  }
}
```

**Protobuf 消息格式**：

```protobuf
syntax = "proto3";

package websocket.v1;

message WebSocketMessage {
  string type = 1;
  string id = 2;
  google.protobuf.Timestamp timestamp = 3;
  oneof payload {
    PaymentCreated payment_created = 4;
    PaymentUpdated payment_updated = 5;
  }
}

message PaymentCreated {
  string payment_id = 1;
  string order_id = 2;
  int64 amount = 3;
  string status = 4;
}
```

### 3.2 消息类型

**消息类型定义**：

```yaml
apiVersion: api.example.com/v1
kind: WebSocketMessageType
metadata:
  name: payment-message-types
spec:
  types:
    - name: payment.created
      description: Payment created event
      schema:
        type: object
        properties:
          payment_id:
            type: string
          order_id:
            type: string
          amount:
            type: integer
    - name: payment.updated
      description: Payment updated event
      schema:
        type: object
        properties:
          payment_id:
            type: string
          status:
            type: string
```

---

## 4 心跳和保活

### 4.1 Ping/Pong 机制

**心跳实现**：

```go
func (cm *ConnectionManager) StartHeartbeat(conn *websocket.Conn, interval time.Duration) {
    ticker := time.NewTicker(interval)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            if err := conn.WriteControl(websocket.PingMessage, []byte{}, time.Now().Add(time.Second)); err != nil {
                return
            }
        }
    }
}
```

### 4.2 超时配置

**超时配置**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: websocket-server
spec:
  template:
    spec:
      containers:
        - name: websocket-server
          image: websocket-server:latest
          env:
            - name: WEBSOCKET_READ_TIMEOUT
              value: "60s"
            - name: WEBSOCKET_WRITE_TIMEOUT
              value: "10s"
            - name: WEBSOCKET_PING_INTERVAL
              value: "30s"
```

---

## 5 错误处理

### 5.1 错误码定义

**错误码规范**：

```yaml
apiVersion: api.example.com/v1
kind: WebSocketErrorCode
metadata:
  name: websocket-error-codes
spec:
  codes:
    - code: 1000
      name: NORMAL_CLOSURE
      description: Normal closure
    - code: 1001
      name: GOING_AWAY
      description: Endpoint going away
    - code: 1002
      name: PROTOCOL_ERROR
      description: Protocol error
    - code: 1003
      name: UNSUPPORTED_DATA
      description: Unsupported data type
    - code: 1006
      name: ABNORMAL_CLOSURE
      description: Abnormal closure
    - code: 1007
      name: INVALID_DATA
      description: Invalid payload data
```

### 5.2 错误恢复

**自动重连机制**：

```go
func (c *WebSocketClient) ConnectWithRetry(maxRetries int, backoff time.Duration) error {
    for i := 0; i < maxRetries; i++ {
        if err := c.Connect(); err == nil {
            return nil
        }

        if i < maxRetries-1 {
            time.Sleep(backoff * time.Duration(i+1))
        }
    }

    return fmt.Errorf("failed to connect after %d retries", maxRetries)
}
```

---

## 6 性能优化

### 6.1 连接池

**连接池配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: websocket-dr
spec:
  host: websocket-backend
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 1000
        connectTimeout: "10s"
      http:
        http1MaxPendingRequests: 100
        http2MaxRequests: 100
```

### 6.2 消息压缩

**消息压缩配置**：

```go
var upgrader = websocket.Upgrader{
    EnableCompression: true,
    CompressionLevel: 6, // 1-9, 6 is a good balance
}
```

---

## 7 形式化定义与理论基础

### 7.1 API WebSocket 形式化模型

**定义 7.1（API WebSocket）**：API WebSocket 是一个四元组：

```text
API_WebSocket = ⟨Connection, Message_Protocol, Heartbeat, Router⟩
```

其中：

- **Connection**：WebSocket 连接 `Connection: Client × Server → Connection`
- **Message_Protocol**：消息协议 `Message_Protocol: Message → Format`
- **Heartbeat**：心跳机制 `Heartbeat: Connection → Ping/Pong`
- **Router**：消息路由 `Router: Message → Handler`

**定义 7.2（连接状态）**：连接状态是一个函数：

```text
Connection_State: Connection → {Connecting, Open, Closing, Closed}
```

**定理 7.1（WebSocket 连接可靠性）**：如果连接建立成功，则消息可以传输：

```text
Connection_State(Connection) = Open ⟹ Can_Send(Connection, Message)
```

**证明**：如果连接状态为 Open，则连接已建立，可以发送消息。□

### 7.2 连接管理形式化

**定义 7.3（连接保持）**：连接保持是一个函数：

```text
Keep_Alive: Connection × Timeout → Connection
```

**定义 7.4（心跳间隔）**：心跳间隔是一个函数：

```text
Heartbeat_Interval: Connection → Time
```

**定理 7.2（心跳保活有效性）**：心跳机制保持连接活跃：

```text
Heartbeat(Connection, Interval) ⟹ Connection_State(Connection) = Open
```

**证明**：心跳机制定期发送 Ping/Pong，保持连接活跃，因此连接状态保持 Open。□

### 7.3 消息传输形式化

**定义 7.5（消息传输）**：消息传输是一个函数：

```text
Send_Message: Connection × Message → Result
```

**定义 7.6（消息延迟）**：消息延迟是一个函数：

```text
Message_Latency(Message) = Receive_Time - Send_Time
```

**定理 7.3（WebSocket 实时性）**：WebSocket 提供低延迟实时通信：

```text
Message_Latency(WebSocket) < Message_Latency(HTTP_Polling)
```

**证明**：WebSocket 保持长连接，避免 HTTP 轮询的开销，因此延迟更低。□

---

## 8 相关文档

- **[API 事件驱动架构](../09-architecture/01-api-event-driven.md)** - WebSocket
  事件
- **[API 性能优化](../07-performance/01-api-performance.md)** - WebSocket 性能优
  化
- **[API 微服务架构](../09-architecture/02-api-microservices.md)** - WebSocket
  服务通信
- **[最佳实践](../00-foundation/05-best-practices.md)** - WebSocket 最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
