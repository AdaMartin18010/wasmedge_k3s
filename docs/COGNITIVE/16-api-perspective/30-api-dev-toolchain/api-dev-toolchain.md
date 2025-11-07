# API 开发工具链规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 工具链流程](#11-工具链流程)
- [2. API 设计工具](#2-api-设计工具)
  - [2.1 OpenAPI 设计工具](#21-openapi-设计工具)
  - [2.2 WIT 设计工具](#22-wit-设计工具)
- [3. 代码生成工具](#3-代码生成工具)
  - [3.1 OpenAPI 代码生成](#31-openapi-代码生成)
  - [3.2 gRPC 代码生成](#32-grpc-代码生成)
  - [3.3 WIT 代码生成](#33-wit-代码生成)
- [4. 测试工具](#4-测试工具)
  - [4.1 API 测试工具](#41-api-测试工具)
  - [4.2 契约测试工具](#42-契约测试工具)
- [5. 文档工具](#5-文档工具)
  - [5.1 API 文档生成](#51-api-文档生成)
  - [5.2 WIT 文档生成](#52-wit-文档生成)
- [6. 部署工具](#6-部署工具)
  - [6.1 Kubernetes 部署](#61-kubernetes-部署)
  - [6.2 GitOps 部署](#62-gitops-部署)
- [7. 监控工具](#7-监控工具)
  - [7.1 指标监控](#71-指标监控)
  - [7.2 日志监控](#72-日志监控)
  - [7.3 追踪监控](#73-追踪监控)
- [8. 相关文档](#8-相关文档)

---

## 1. 概述

API 开发工具链规范定义了 API 开发过程中使用的工具链，从 API 设计到代码生成，从测
试到文档，从部署到监控。

### 1.1 工具链流程

```text
API 设计（OpenAPI Editor、WIT Editor）
  ↓
代码生成（Swagger Codegen、protoc、wit-bindgen）
  ↓
测试（Postman、k6、pact）
  ↓
文档（Swagger UI、Redoc、wit-doc）
  ↓
部署（kubectl、Helm、ArgoCD）
  ↓
监控（Prometheus、Grafana、Jaeger）
```

---

## 2. API 设计工具

### 2.1 OpenAPI 设计工具

**Swagger Editor**：

```yaml
# swagger-editor 配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: swagger-editor
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: swagger-editor
          image: swaggerapi/swagger-editor:latest
          ports:
            - containerPort: 8080
```

**Stoplight Studio**：

```bash
# 安装 Stoplight Studio
npm install -g @stoplight/cli

# 启动 Stoplight Studio
stoplight start
```

### 2.2 WIT 设计工具

**WIT Editor**：

```bash
# 使用 VS Code WIT 扩展
code --install-extension wasm.wit

# 验证 WIT 文件
wit-validate payment.wit
```

---

## 3. 代码生成工具

### 3.1 OpenAPI 代码生成

**Swagger Codegen**：

```bash
# 生成 Go 客户端
swagger-codegen generate \
  -i api/openapi.yaml \
  -l go \
  -o client/go

# 生成 TypeScript 客户端
swagger-codegen generate \
  -i api/openapi.yaml \
  -l typescript-axios \
  -o client/typescript
```

**OpenAPI Generator**：

```bash
# 生成 Rust 服务器
openapi-generator generate \
  -i api/openapi.yaml \
  -g rust-server \
  -o server/rust
```

### 3.2 gRPC 代码生成

**protoc**：

```bash
# 生成 Go 代码
protoc --go_out=. --go-grpc_out=. payment.proto

# 生成 Rust 代码
protoc --rust_out=. payment.proto
```

### 3.3 WIT 代码生成

**wit-bindgen**：

```bash
# 生成 Rust 绑定
wit-bindgen rust \
  --world payment-service \
  --out-dir src/bindings \
  payment.wit
```

---

## 4. 测试工具

### 4.1 API 测试工具

**Postman**：

```json
{
  "info": {
    "name": "Payment API Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create Payment",
      "request": {
        "method": "POST",
        "url": "http://payment-service/api/v1/payments",
        "body": {
          "mode": "raw",
          "raw": "{\"order_id\":\"123\",\"amount\":10000}"
        }
      }
    }
  ]
}
```

**k6**：

```javascript
import http from "k6/http";
import { check } from "k6";

export default function () {
  let res = http.post(
    "http://payment-service/api/v1/payments",
    JSON.stringify({ order_id: "123", amount: 10000 }),
    { headers: { "Content-Type": "application/json" } }
  );
  check(res, {
    "status is 201": (r) => r.status === 201
  });
}
```

### 4.2 契约测试工具

**Pact**：

```javascript
const { Pact } = require("@pact-foundation/pact");

const provider = new Pact({
  consumer: "PaymentClient",
  provider: "PaymentService"
});

describe("Payment API", () => {
  it("creates a payment", () => {
    return provider.addInteraction({
      state: "payment service is available",
      uponReceiving: "a request to create payment",
      withRequest: {
        method: "POST",
        path: "/api/v1/payments",
        body: { order_id: "123", amount: 10000 }
      },
      willRespondWith: {
        status: 201,
        body: { payment_id: "pay_123", status: "created" }
      }
    });
  });
});
```

---

## 5. 文档工具

### 5.1 API 文档生成

**Swagger UI**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: swagger-ui
spec:
  template:
    spec:
      containers:
        - name: swagger-ui
          image: swaggerapi/swagger-ui:latest
          env:
            - name: SWAGGER_JSON
              value: /api/openapi.yaml
```

**Redoc**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redoc
spec:
  template:
    spec:
      containers:
        - name: redoc
          image: redocly/redoc:latest
          env:
            - name: SPEC_URL
              value: http://api-server/openapi.yaml
```

### 5.2 WIT 文档生成

**wit-doc**：

```bash
# 生成 WIT 文档
wit-doc generate payment.wit --output docs/
```

---

## 6. 部署工具

### 6.1 Kubernetes 部署

**kubectl**：

```bash
# 部署 API
kubectl apply -f deployment.yaml

# 查看部署状态
kubectl get deployments

# 查看 Pod 日志
kubectl logs -f deployment/payment-api
```

**Helm**：

```yaml
# Chart.yaml
apiVersion: v2
name: payment-api
version: 1.0.0
description: Payment API Helm Chart

# values.yaml
replicaCount: 3
image:
  repository: payment-api
  tag: latest
service:
  type: ClusterIP
  port: 8080
```

### 6.2 GitOps 部署

**ArgoCD**：

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-api
spec:
  project: default
  source:
    repoURL: https://github.com/example/payment-api
    targetRevision: main
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## 7. 监控工具

### 7.1 指标监控

**Prometheus**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: payment-api-monitor
spec:
  selector:
    matchLabels:
      app: payment-api
  endpoints:
    - port: http
      path: /metrics
```

### 7.2 日志监控

**Loki**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: loki-config
data:
  loki.yaml: |
    auth_enabled: false
    server:
      http_listen_port: 3100
```

### 7.3 追踪监控

**Jaeger**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: jaeger-config
data:
  JAEGER_SERVICE_NAME: payment-api
  JAEGER_AGENT_HOST: jaeger-agent
```

---

## 8. 相关文档

- **[API 文档生成规范](../16-api-documentation/api-documentation.md)** - 文档工
  具使用
- **[API 测试规范](../15-api-testing/api-testing.md)** - 测试工具使用
- **[API 监控告警](../20-api-monitoring/api-monitoring.md)** - 监控工具使用
- **[最佳实践](../08-best-practices/best-practices.md)** - 工具链最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
