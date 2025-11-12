# API 测试规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 测试金字塔](#11-测试金字塔)
  - [1.2 API 测试在 API 规范中的位置](#12-api-测试在-api-规范中的位置)
- [2 API 契约测试](#2-api-契约测试)
  - [2.1 OpenAPI 契约测试](#21-openapi-契约测试)
  - [2.2 gRPC 契约测试](#22-grpc-契约测试)
  - [2.3 WIT 组件测试](#23-wit-组件测试)
- [3 容器化 API 测试](#3-容器化-api-测试)
  - [3.1 Kubernetes 测试](#31-kubernetes-测试)
  - [3.2 Docker Compose 测试](#32-docker-compose-测试)
- [4 沙盒化 API 测试](#4-沙盒化-api-测试)
  - [4.1 gVisor 测试](#41-gvisor-测试)
  - [4.2 Seccomp 测试](#42-seccomp-测试)
- [5 WASM 化 API 测试](#5-wasm-化-api-测试)
  - [5.1 WasmEdge 测试](#51-wasmedge-测试)
  - [5.2 wasmCloud 测试](#52-wasmcloud-测试)
- [6 集成测试](#6-集成测试)
  - [6.1 服务网格集成测试](#61-服务网格集成测试)
  - [6.2 端到端测试](#62-端到端测试)
- [7 性能测试](#7-性能测试)
  - [7.1 负载测试](#71-负载测试)
  - [7.2 压力测试](#72-压力测试)
- [8 安全测试](#8-安全测试)
  - [8.1 OWASP API 安全测试](#81-owasp-api-安全测试)
  - [8.2 认证授权测试](#82-认证授权测试)
- [9 形式化定义与理论基础](#9-形式化定义与理论基础)
  - [9.1 API 测试形式化模型](#91-api-测试形式化模型)
  - [9.2 测试覆盖度形式化](#92-测试覆盖度形式化)
  - [9.3 测试有效性形式化](#93-测试有效性形式化)
- [10 相关文档](#10-相关文档)

---

## 1 概述

API 测试规范定义了 API 在不同运行时环境下的测试策略和方法，从契约测试到集成测试
，从性能测试到安全测试。本文档基于形式化方法，提供严格的数学定义和推理论证，分析
API 测试的理论基础和实践方法。

**参考标准**：

- [Pact Testing](https://docs.pact.io/) - Pact 契约测试框架
- [OpenAPI Testing](https://swagger.io/specification/) - OpenAPI 测试规范
- [gRPC Testing](https://grpc.io/docs/guides/testing/) - gRPC 测试指南
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) -
  OWASP 测试指南
- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) -
  测试金字塔理论

### 1.1 测试金字塔

```text
E2E 测试（少量）
  ↓
集成测试（中等）
  ↓
单元测试（大量）
  ↓
契约测试（基础）
```

### 1.2 API 测试在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API 测试验证所有四个维度：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
            ↑         ↑            ↑            ↑
    API Testing validates all dimensions
```

API 测试在 API 规范中提供：

- **IDL 测试**：契约测试验证接口定义的正确性
- **Governance 测试**：策略测试验证治理规则的有效性
- **Observability 测试**：可观测性测试验证追踪和监控的完整性
- **Security 测试**：安全测试验证安全机制的有效性

---

## 2 API 契约测试

### 2.1 OpenAPI 契约测试

**Pact 契约测试**：

```javascript
// consumer.test.js
const { Pact } = require("@pact-foundation/pact");

const provider = new Pact({
  consumer: "PaymentClient",
  provider: "PaymentService"
});

describe("Payment API", () => {
  beforeAll(() => provider.setup());
  afterEach(() => provider.verify());
  afterAll(() => provider.finalize());

  it("creates a payment", () => {
    return provider.addInteraction({
      state: "payment service is available",
      uponReceiving: "a request to create payment",
      withRequest: {
        method: "POST",
        path: "/api/v1/payments",
        headers: { "Content-Type": "application/json" },
        body: {
          order_id: "123",
          amount: 10000
        }
      },
      willRespondWith: {
        status: 201,
        headers: { "Content-Type": "application/json" },
        body: {
          payment_id: "pay_123",
          status: "created"
        }
      }
    });
  });
});
```

### 2.2 gRPC 契约测试

**Protobuf 验证**：

```go
func TestPaymentServiceContract(t *testing.T) {
    req := &pb.CreatePaymentRequest{
        OrderId: "123",
        Amount:  10000,
    }

    // 验证请求格式
    if err := req.Validate(); err != nil {
        t.Fatalf("Invalid request: %v", err)
    }

    // 模拟服务调用
    resp, err := mockPaymentService.CreatePayment(context.Background(), req)
    if err != nil {
        t.Fatalf("CreatePayment failed: %v", err)
    }

    // 验证响应格式
    if resp.PaymentId == "" {
        t.Error("PaymentId is empty")
    }
}
```

### 2.3 WIT 组件测试

**WIT 接口测试**：

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use wasi::http::incoming_handler::{IncomingRequest, Response};

    #[test]
    fn test_payment_handler() {
        let handler = PaymentHandler::new();

        let req = IncomingRequest {
            method: "POST".to_string(),
            path: "/api/v1/payments".to_string(),
            headers: vec![],
            body: b"{\"order_id\":\"123\",\"amount\":10000}".to_vec(),
        };

        let resp = handler.handle(req);

        assert_eq!(resp.status, 201);
        assert!(resp.body.len() > 0);
    }
}
```

---

## 3 容器化 API 测试

### 3.1 Kubernetes 测试

**Kind 测试集群**：

```yaml
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

**测试脚本**：

```bash
#!/bin/bash
# 创建测试集群
kind create cluster --config kind-config.yaml

# 部署测试应用
kubectl apply -f test-deployment.yaml

# 等待就绪
kubectl wait --for=condition=ready pod -l app=payment-service --timeout=60s

# 运行测试
kubectl exec -it payment-service-pod -- npm test

# 清理
kind delete cluster
```

### 3.2 Docker Compose 测试

**docker-compose.test.yml**：

```yaml
version: "3.8"
services:
  payment-service:
    image: payment-service:test
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://test:test@postgres:5432/test
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: test
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test

  test-runner:
    image: test-runner:latest
    depends_on:
      - payment-service
    command: npm test
```

---

## 4 沙盒化 API 测试

### 4.1 gVisor 测试

**gVisor 测试配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gvisor-test
spec:
  runtimeClassName: gvisor
  containers:
    - name: test
      image: test-runner:latest
      command: ["/bin/sh", "-c", "npm test"]
      securityContext:
        capabilities:
          drop:
            - ALL
```

### 4.2 Seccomp 测试

**Seccomp Profile 测试**：

```bash
# 测试 Seccomp Profile
docker run --rm \
  --security-opt seccomp=test-seccomp.json \
  test-image \
  npm test
```

**验证系统调用**：

```bash
# 使用 strace 验证系统调用
strace -e trace=all \
  docker run --rm \
  --security-opt seccomp=test-seccomp.json \
  test-image \
  npm test
```

---

## 5 WASM 化 API 测试

### 5.1 WasmEdge 测试

**WasmEdge 测试配置**：

```bash
# 运行 WASM 测试
wasmedge --dir .:. \
  --env TEST_MODE=true \
  payment-service.wasm
```

**WIT 接口测试**：

```rust
#[cfg(test)]
mod tests {
    use wasi::http::incoming_handler::{IncomingRequest, Response};

    #[test]
    fn test_http_handler() {
        let handler = create_handler();

        let req = IncomingRequest {
            method: "GET".to_string(),
            path: "/health".to_string(),
            headers: vec![],
            body: vec![],
        };

        let resp = handler.handle(req);
        assert_eq!(resp.status, 200);
    }
}
```

### 5.2 wasmCloud 测试

**wasmCloud 测试配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: wasmcloud-test-config
data:
  test.yaml: |
    hosts:
      - payment-service-host
    capabilities:
      - http
    tests:
      - name: health_check
        path: /health
        method: GET
        expected_status: 200
```

---

## 6 集成测试

### 6.1 服务网格集成测试

**Istio 集成测试**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service-test
spec:
  hosts:
    - payment-service
  http:
    - match:
        - headers:
            test-mode:
              exact: "true"
      route:
        - destination:
            host: payment-service-test
            subset: test
```

### 6.2 端到端测试

**E2E 测试流程**：

```go
func TestPaymentE2E(t *testing.T) {
    // 1. 创建测试环境
    env := setupTestEnvironment(t)
    defer env.Cleanup()

    // 2. 部署服务
    deployServices(env, []string{"payment-service", "order-service"})

    // 3. 等待服务就绪
    waitForServices(env, []string{"payment-service", "order-service"})

    // 4. 执行测试
    client := NewAPIClient(env.GatewayURL)
    resp, err := client.CreatePayment(&PaymentRequest{
        OrderID: "123",
        Amount:  10000,
    })

    assert.NoError(t, err)
    assert.Equal(t, 201, resp.StatusCode)
}
```

---

## 7 性能测试

### 7.1 负载测试

**K6 负载测试**：

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
  stages: [
    { duration: "30s", target: 100 },
    { duration: "1m", target: 200 },
    { duration: "30s", target: 0 }
  ],
  thresholds: {
    http_req_duration: ["p(95)<100"],
    http_req_failed: ["rate<0.01"]
  }
};

export default function () {
  let res = http.post(
    "http://payment-service/api/v1/payments",
    JSON.stringify({
      order_id: "123",
      amount: 10000
    }),
    {
      headers: { "Content-Type": "application/json" }
    }
  );

  check(res, {
    "status is 201": (r) => r.status === 201
  });

  sleep(1);
}
```

### 7.2 压力测试

**Apache Bench 压力测试**：

```bash
# 1000 请求，并发 10
ab -n 1000 -c 10 \
  -p payment.json \
  -T application/json \
  http://payment-service/api/v1/payments
```

---

## 8 安全测试

### 8.1 OWASP API 安全测试

**注入攻击测试**：

```go
func TestSQLInjection(t *testing.T) {
    testCases := []string{
        "'; DROP TABLE payments; --",
        "1' OR '1'='1",
        "1' UNION SELECT * FROM users --",
    }

    for _, payload := range testCases {
        req := &PaymentRequest{
            OrderID: payload,
            Amount:  10000,
        }

        resp, err := api.CreatePayment(req)
        assert.Error(t, err, "Should reject SQL injection")
        assert.Nil(t, resp)
    }
}
```

### 8.2 认证授权测试

**JWT 测试**：

```go
func TestJWTAuthentication(t *testing.T) {
    // 测试无效 token
    req := httptest.NewRequest("POST", "/api/v1/payments", nil)
    req.Header.Set("Authorization", "Bearer invalid-token")

    resp := httptest.NewRecorder()
    handler.ServeHTTP(resp, req)

    assert.Equal(t, 401, resp.Code)

    // 测试有效 token
    token := generateValidToken()
    req.Header.Set("Authorization", "Bearer "+token)

    resp = httptest.NewRecorder()
    handler.ServeHTTP(resp, req)

    assert.Equal(t, 201, resp.Code)
}
```

---

## 9 形式化定义与理论基础

### 9.1 API 测试形式化模型

**定义 9.1（API 测试）**：API 测试是一个四元组：

```text
API_Test = ⟨Test_Case, Test_Environment, Test_Execution, Test_Result⟩
```

其中：

- **Test_Case**：测试用例 `Test_Case: ⟨Input, Expected_Output, Assertions⟩`
- **Test_Environment**：测试环境 `Test_Environment: {Container, Sandbox, WASM}`
- **Test_Execution**：测试执行 `Test_Execution: Test_Case → Result`
- **Test_Result**：测试结果 `Test_Result: {Pass, Fail, Skip}`

**定义 9.2（测试覆盖度）**：测试覆盖度是一个函数：

```text
Coverage(API) = f(Contract_Coverage, Integration_Coverage, Performance_Coverage, Security_Coverage)
```

其中每个覆盖度 `[0, 1]`。

**定理 9.1（测试覆盖度完备性）**：如果测试覆盖度为 1，则 API 完全测试：

```text
Coverage(API) = 1 ⟹ Fully_Tested(API)
```

**证明**：如果契约、集成、性能和安全覆盖度都为 1，则所有 API 功能都被测试，因此
API 完全测试。□

### 9.2 测试覆盖度形式化

**定义 9.3（契约测试覆盖度）**：契约测试覆盖度是一个函数：

```text
Contract_Coverage(API) = |Tested_Endpoints| / |Total_Endpoints|
```

**定义 9.4（集成测试覆盖度）**：集成测试覆盖度是一个函数：

```text
Integration_Coverage(API) = |Tested_Integrations| / |Total_Integrations|
```

**定理 9.2（测试覆盖度单调性）**：测试覆盖度随测试用例增加而增加：

```text
|Test_Cases₁| < |Test_Cases₂| ⟹ Coverage(API, Test_Cases₁) ≤ Coverage(API, Test_Cases₂)
```

**证明**：测试用例越多，覆盖的端点和场景越多，因此覆盖度越高。□

### 9.3 测试有效性形式化

**定义 9.5（测试有效性）**：测试有效性是一个函数：

```text
Test_Effectiveness(Test) = f(Test_Precision, Test_Recall, Test_Reliability)
```

其中：

- **Test_Precision**：测试精确度 `[0, 1]`
- **Test_Recall**：测试召回率 `[0, 1]`
- **Test_Reliability**：测试可靠性 `[0, 1]`

**定理 9.3（测试有效性最优性）**：测试有效性越高，测试质量越好：

```text
Test_Effectiveness(Test₁) > Test_Effectiveness(Test₂) ⟹ Quality(Test₁) > Quality(Test₂)
```

**证明**：根据定义 9.5，测试有效性越高，精确度、召回率和可靠性越高，因此测试质量
越好。□

**定义 9.6（测试通过率）**：测试通过率是一个函数：

```text
Pass_Rate(Test_Suite) = |Passed_Tests| / |Total_Tests|
```

**定理 9.4（测试通过率与质量）**：测试通过率越高，API 质量越好：

```text
Pass_Rate(Test_Suite) = 1 ⟹ Quality(API) ≥ Threshold
```

**证明**：如果所有测试都通过，则 API 满足所有测试要求，因此质量满足阈值。□

---

## 10 相关文档

- **[最佳实践](../00-foundation/05-best-practices.md)** - API 测试最佳实践
- **[API 性能优化](../14-api-performance/api-performance.md)** - 性能测试
- **[API 安全规范](../11-api-security/api-security.md)** - 安全测试
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新**：2025-11-07 **维护者**：项目团队
