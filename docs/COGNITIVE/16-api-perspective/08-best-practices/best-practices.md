# API 规范最佳实践

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [1. 概述](#1-概述)
- [2. 容器化 API 最佳实践](#2-容器化-api-最佳实践)
- [3. 沙盒化 API 最佳实践](#3-沙盒化-api-最佳实践)
- [4. WASM 化 API 最佳实践](#4-wasm-化-api-最佳实践)
- [5. API 版本管理最佳实践](#5-api-版本管理最佳实践)
- [6. API 安全最佳实践](#6-api-安全最佳实践)
- [7. API 可观测性最佳实践](#7-api-可观测性最佳实践)
- [8. 相关文档](#8-相关文档)

---

## 1. 概述

本文档提供 API 规范的最佳实践指南，涵盖容器化、沙盒化、WASM 化三大领域的 API 设
计、实现和运维最佳实践。

### 1.1 最佳实践原则

1. **最小权限原则**：API 只暴露必要的接口和能力
2. **版本化策略**：明确的版本管理和兼容性保证
3. **可观测性优先**：API 调用全程可追踪、可监控
4. **安全默认值**：默认启用安全策略，显式放宽
5. **文档驱动**：API 规范即文档，文档即代码

---

## 2. 容器化 API 最佳实践

### 2.1 Kubernetes CRD API 设计最佳实践

### 2.1.1 原则 1：使用 OpenAPI v3 Schema 验证

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: apidefinitions.api.example.com
spec:
  group: api.example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          required: [spec]
          properties:
            spec:
              type: object
              required: [openapi, version]
              properties:
                openapi:
                  type: string
                  pattern: '^3\.[0-9]+\.[0-9]+$'
                version:
                  type: string
                  pattern: '^[0-9]+\.[0-9]+\.[0-9]+$'
                lifecycle:
                  type: string
                  enum: [active, deprecated, sunset]
                  default: active
```

### 2.1.2 原则 2：使用 ValidatingAdmissionPolicy（K8s 1.28+）

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: api-spec-validation
spec:
  matchConstraints:
    resourceRules:
      - apiGroups: ["api.example.com"]
        apiVersions: ["v1"]
        operations: ["CREATE", "UPDATE"]
        resources: ["apidefinitions"]
  validations:
    - expression: "object.spec.openapi != null"
      message: "OpenAPI spec is required"
    - expression: "object.spec.version.matches('^[0-9]+\\.[0-9]+\\.[0-9]+$')"
      message: "Version must be semantic version"
    - expression:
        "has(object.spec.deprecationPolicy) ?
        object.spec.deprecationPolicy.sunsetDate > now() : true"
      message: "Sunset date must be in the future"
```

### 2.2 OCI Runtime Spec 最佳实践

### 2.2.1 原则 1：最小化系统调用

```json
{
  "linux": {
    "syscalls": [
      {
        "names": ["read", "write", "open", "close"],
        "action": "SCMP_ACT_ALLOW"
      },
      {
        "names": ["socket", "connect", "accept"],
        "action": "SCMP_ACT_ALLOW",
        "args": [
          {
            "index": 0,
            "value": 2,
            "op": "SCMP_CMP_EQ"
          }
        ]
      }
    ]
  }
}
```

### 2.2.2 原则 2：资源限制明确

```json
{
  "linux": {
    "resources": {
      "memory": {
        "limit": 536870912,
        "reservation": 268435456
      },
      "cpu": {
        "shares": 1024,
        "quota": 50000,
        "period": 100000
      }
    }
  }
}
```

---

## 3. 沙盒化 API 最佳实践

### 3.1 Seccomp Profile 最佳实践

### 3.1.1 原则 1：白名单模式

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": ["read", "write", "open", "close", "fstat"],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

### 3.1.2 原则 2：参数验证

```json
{
  "syscalls": [
    {
      "names": ["clone"],
      "action": "SCMP_ACT_ALLOW",
      "args": [
        {
          "index": 0,
          "value": 2114060288,
          "valueTwo": 0,
          "op": "SCMP_CMP_MASKED_EQ"
        }
      ]
    }
  ]
}
```

### 3.2 gVisor 配置最佳实践

### 3.2.1 原则 1：最小化 Sentry 开销

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
overhead:
  podFixed:
    memory: "2Gi"
    cpu: "100m"
scheduling:
  nodeSelector:
    runtime: gvisor
  tolerations:
    - key: gvisor-workload
      operator: Equal
      value: "true"
      effect: NoSchedule
```

### 3.2.2 原则 2：网络性能优化

```yaml
# gVisor 网络配置
apiVersion: v1
kind: Pod
metadata:
  name: gvisor-pod
spec:
  runtimeClassName: gvisor
  containers:
    - name: app
      image: app:latest
      # 使用 hostNetwork 减少网络开销（安全场景允许时）
      # hostNetwork: true
```

---

## 4. WASM 化 API 最佳实践

### 4.1 WIT 组件设计最佳实践

### 4.1.1 原则 1：能力最小化

```wit
// ❌ 错误：暴露过多能力
world my-world {
    import wasi:filesystem/filesystem@0.2.0;
    import wasi:network/sockets@0.2.0;
    import wasi:random/random@0.2.0;
    // 不需要的能力也被导入
}

// ✅ 正确：只导入需要的能力
world my-world {
    import wasi:http/incoming-handler@0.2.0;
    // 只导入 HTTP 处理能力
    export handler: func(req: incoming-request) -> response;
}
```

**原则 2：版本化明确**

```wit
// 使用语义化版本
package example:calculator@1.0.0;

// 主版本：不兼容变更
package example:calculator@2.0.0;

// 次版本：向后兼容的新功能
package example:calculator@1.1.0;

// 补丁版本：bug 修复
package example:calculator@1.0.1;
```

### 4.2 WasmEdge 部署最佳实践

**原则 1：使用 OCI 注释（K8s 1.30+）**

```dockerfile
FROM scratch
COPY app.wasm /app.wasm
```

```bash
# 构建时添加 OCI 注释
docker build \
  --annotation "module.wasm.image/variant=compat-smart" \
  -t wasm-app:latest .
```

**原则 2：RuntimeClass 配置**

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: wasm
handler: crun
overhead:
  podFixed:
    memory: "64Mi"
    cpu: "50m"
scheduling:
  nodeSelector:
    wasm-runtime: enabled
```

---

## 5. API 版本管理最佳实践

### 5.1 语义化版本策略

**版本号格式**：`MAJOR.MINOR.PATCH`

- **MAJOR**：不兼容的 API 变更
- **MINOR**：向后兼容的功能新增
- **PATCH**：向后兼容的问题修复

**示例**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-service
spec:
  version: "2.0.0" # 主版本升级，不兼容 v1.x
  deprecationPolicy:
    sunsetDate: "2025-12-31"
    replacement: "payment-service-v3"
```

### 5.2 版本兼容性保证

**原则 1：字段保留策略**

```protobuf
// Protobuf 字段保留
message PaymentRequest {
    string order_id = 1;  // 保留字段，永不删除
    int64 amount = 2;     // 保留字段，永不删除
    // 新字段使用新的字段号
    string currency = 10; // 新增字段
}
```

**原则 2：废弃流程**

```yaml
# OpenAPI 废弃标记
paths:
  /payments/v1:
    post:
      deprecated: true
      x-deprecation-info:
        sunset-date: "2025-12-31"
        replacement: "/payments/v2"
        migration-guide: "https://docs.example.com/migration"
```

---

## 6. API 安全最佳实践

### 6.1 认证最佳实践

**原则 1：使用 SPIFFE/SPIRE**

```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    spiffe.io/spiffe-id: spiffe://example.com/ns/default/sa/payment-service
spec:
  containers:
    - name: app
      image: payment-service:latest
```

**原则 2：mTLS 强制**

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT
```

### 6.2 授权最佳实践

**原则 1：OPA 策略即代码**

```rego
package api.authz

default allow = false

allow {
    input.method == "GET"
    input.path = "/api/v1/health"
}

allow {
    input.method == "POST"
    input.path = "/api/v1/payments"
    input.principal == "payment-service"
    input.claims.role == "payment-writer"
}
```

**原则 2：最小权限原则**

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: payment-service-policy
spec:
  selector:
    matchLabels:
      app: payment-service
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/default/sa/payment-service"]
      to:
        - operation:
            methods: ["POST"]
            paths: ["/api/v1/payments"]
```

---

## 7. API 可观测性最佳实践

### 7.1 OTLP 集成最佳实践

**原则 1：统一使用 OTLP**

```go
// OpenTelemetry SDK 配置
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
)

exporter, _ := otlptracegrpc.New(ctx,
    otlptracegrpc.WithEndpoint("otel-collector:4317"),
    otlptracegrpc.WithInsecure(),
)

tp := trace.NewTracerProvider(
    trace.WithBatcher(exporter),
    trace.WithResource(resource.NewWithAttributes(
        semconv.SchemaURL,
        semconv.ServiceNameKey.String("payment-service"),
    )),
)

otel.SetTracerProvider(tp)
```

**原则 2：Trace 上下文传播**

```go
// HTTP 客户端传播 Trace 上下文
func callDownstream(ctx context.Context, url string) {
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)

    // 自动注入 TraceParent 头
    otel.GetTextMapPropagator().Inject(ctx, propagation.HeaderCarrier(req.Header))

    client.Do(req)
}
```

### 7.2 eBPF 增强可观测性

**原则 1：零侵入追踪**

```c
// eBPF 程序：自动追踪 gRPC 调用
SEC("uprobe/grpc_call")
int trace_grpc_call(struct pt_regs *ctx) {
    struct otlp_span_t span = {
        .trace_id = bpf_get_current_task(),
        .span_id = bpf_ktime_get_ns(),
        .name = "grpc_call",
        .kind = SPAN_KIND_CLIENT
    };

    bpf_perf_event_output(ctx, &events, BPF_F_CURRENT_CPU, &span, sizeof(span));
    return 0;
}
```

**原则 2：采样策略**

```yaml
# OpenTelemetry Collector 采样配置
processors:
  probabilistic_sampler:
    sampling_percentage: 1.0 # 1% 采样
  tail_sampling:
    policies:
      - name: always-sample
        type: always_sample
      - name: latency
        type: latency
        latency:
          threshold_ms: 100 # P99 以上全采样
```

---

## 8. 相关文档

- **[容器化 API 规范](../01-containerization-api/containerization-api.md)** - 容
  器化 API 详解
- **[沙盒化 API 规范](../02-sandboxing-api/sandboxing-api.md)** - 沙盒化 API 详
  解
- **[WASM 化 API 规范](../03-wasm-api/wasm-api.md)** - WASM 化 API 详解
- **[API 演进路径](../06-api-evolution/api-evolution.md)** - API 演进最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新**：2025-11-07 **维护者**：项目团队
