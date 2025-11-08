# API 治理规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 API 治理层次](#11-api-治理层次)
  - [1.2 API 治理在 API 规范中的位置](#12-api-治理在-api-规范中的位置)
- [2. 容器化 API 治理](#2-容器化-api-治理)
  - [2.1 Kubernetes Admission Webhook](#21-kubernetes-admission-webhook)
  - [2.2 ValidatingAdmissionPolicy（K8s 1.28+）](#22-validatingadmissionpolicyk8s-128)
- [3. 沙盒化 API 治理](#3-沙盒化-api-治理)
  - [3.1 Seccomp Profile 治理](#31-seccomp-profile-治理)
  - [3.2 AppArmor Profile 治理](#32-apparmor-profile-治理)
- [4. WASM 化 API 治理](#4-wasm-化-api-治理)
  - [4.1 WASI 能力治理](#41-wasi-能力治理)
  - [4.2 WASM 策略插件](#42-wasm-策略插件)
- [5. 服务网格 API 治理](#5-服务网格-api-治理)
  - [5.1 Istio VirtualService](#51-istio-virtualservice)
  - [5.2 DestinationRule](#52-destinationrule)
- [6. 策略即代码（OPA）](#6-策略即代码opa)
  - [6.1 OPA 策略定义](#61-opa-策略定义)
  - [6.2 OPA + Kubernetes](#62-opa--kubernetes)
  - [6.3 OPA-Wasm](#63-opa-wasm)
- [7. API 版本管理](#7-api-版本管理)
  - [7.1 语义化版本](#71-语义化版本)
  - [7.2 API 生命周期管理](#72-api-生命周期管理)
  - [7.3 GitOps 版本管理](#73-gitops-版本管理)
- [8. 形式化定义与理论基础](#8-形式化定义与理论基础)
  - [8.1 API 治理形式化模型](#81-api-治理形式化模型)
  - [8.2 策略执行形式化](#82-策略执行形式化)
  - [8.3 生命周期管理形式化](#83-生命周期管理形式化)
- [9. 相关文档](#9-相关文档)

---

## 1. 概述

API 治理规范定义了 API 生命周期管理、策略执行、版本控制和访问控制的标准化机制，
从 Kubernetes Admission Webhook 到 OPA 策略引擎，再到 WASM 策略插件。本文档基于
形式化方法，提供严格的数学定义和推理论证，分析 API 治理的理论基础和实践方法。

**参考标准**：

- [Kubernetes Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/) -
  Kubernetes 准入控制器
- [OPA Policy Language](https://www.openpolicyagent.org/docs/latest/policy-language/) -
  OPA 策略语言
- [Istio Service Mesh](https://istio.io/latest/docs/) - Istio 服务网格
- [WASM Policy Plugins](https://github.com/proxy-wasm/spec) - WASM 策略插件规范
- [API Governance Best Practices](https://www.gartner.com/en/documents/3889067) -
  API 治理最佳实践

### 1.1 API 治理层次

```text
应用层治理（API Gateway、限流）
  ↓
服务层治理（Service Mesh、mTLS）
  ↓
运行时治理（Admission Webhook、OPA）
  ↓
沙盒层治理（Seccomp、AppArmor）
  ↓
WASM 层治理（WASI 能力、策略插件）
```

### 1.2 API 治理在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API 治理是 Governance 维度的核心：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
                        ↑
                API Governance
```

API 治理在 API 规范中提供：

- **生命周期管理**：API 的创建、更新、废弃和删除
- **策略执行**：Admission Webhook、OPA、Service Mesh 等策略执行机制
- **版本控制**：API 版本管理和兼容性保证
- **访问控制**：RBAC、ABAC 等访问控制机制

---

## 2. 容器化 API 治理

### 2.1 Kubernetes Admission Webhook

**ValidatingAdmissionWebhook**：

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: api-spec-validator
webhooks:
  - name: api-spec-validator.example.com
    rules:
      - apiGroups: ["api.example.com"]
        apiVersions: ["v1"]
        operations: ["CREATE", "UPDATE"]
        resources: ["apidefinitions"]
    clientConfig:
      service:
        namespace: default
        name: api-validator-service
        path: "/validate"
    admissionReviewVersions: ["v1"]
    sideEffects: None
    timeoutSeconds: 5
```

**MutatingAdmissionWebhook**：

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingWebhookConfiguration
metadata:
  name: api-spec-mutator
webhooks:
  - name: api-spec-mutator.example.com
    rules:
      - apiGroups: ["api.example.com"]
        apiVersions: ["v1"]
        operations: ["CREATE"]
        resources: ["apidefinitions"]
    clientConfig:
      service:
        namespace: default
        name: api-mutator-service
        path: "/mutate"
    admissionReviewVersions: ["v1"]
    sideEffects: None
```

### 2.2 ValidatingAdmissionPolicy（K8s 1.28+）

**CEL 表达式验证**：

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: api-spec-policy
spec:
  failurePolicy: Fail
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
  variables:
    - name: "now"
      expression: "now()"
```

---

## 3. 沙盒化 API 治理

### 3.1 Seccomp Profile 治理

**Seccomp Profile CRD**：

```yaml
apiVersion: security-profiles-operator.x-k8s.io/v1alpha1
kind: SeccompProfile
metadata:
  name: payment-service-seccomp
spec:
  defaultAction: SCMP_ACT_ERRNO
  architectures:
    - SCMP_ARCH_X86_64
  syscalls:
    - names:
        - read
        - write
        - open
        - close
      action: SCMP_ACT_ALLOW
```

**Pod 引用 Seccomp Profile**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: payment-service
spec:
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: operator/default/payment-service-seccomp.json
  containers:
    - name: app
      image: payment-service:latest
```

### 3.2 AppArmor Profile 治理

**AppArmor Profile**：

```text
#include <tunables/global>

profile payment-service /usr/bin/payment-service {
    #include <abstractions/base>

    # 允许网络访问
    network tcp,
    network udp,

    # 文件系统访问限制
    /var/lib/payment/** rw,
    /tmp/** rw,

    # 拒绝敏感文件访问
    deny /etc/shadow r,
    deny /etc/passwd r,
}
```

**Pod 使用 AppArmor**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    container.apparmor.security.beta.kubernetes.io/app: localhost/payment-service
spec:
  containers:
    - name: app
      image: payment-service:latest
```

---

## 4. WASM 化 API 治理

### 4.1 WASI 能力治理

**能力最小化原则**：

```wit
// ❌ 错误：暴露过多能力
world insecure-world {
    import wasi:filesystem/filesystem@0.2.0;
    import wasi:network/sockets@0.2.0;
    import wasi:random/random@0.2.0;
}

// ✅ 正确：只导入需要的能力
world secure-world {
    import wasi:http/incoming-handler@0.2.0;
    // 仅 HTTP 能力，无文件系统、网络底层访问
    export handle: func(req: incoming-request) -> response;
}
```

**WasmEdge 能力配置**：

```toml
[wasmtime]
# 允许的能力
allowed_capabilities = [
    "http",
    "keyvalue"
]

# 禁止的能力
denied_capabilities = [
    "filesystem",
    "network"
]
```

### 4.2 WASM 策略插件

**Envoy WASM 过滤器**：

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: wasm-auth-filter
spec:
  workloadSelector:
    labels:
      app: payment-service
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
        listener:
          filterChain:
            filter:
              name: "envoy.filters.network.http_connection_manager"
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.wasm
          typed_config:
            "@type": type.googleapis.com/udpa.type.v1.TypedStruct
            type_url: type.googleapis.com/envoy.extensions.filters.http.wasm.v3.Wasm
            value:
              config:
                name: "auth_wasm_filter"
                root_id: "auth_root"
                vm_config:
                  runtime: "envoy.wasm.runtime.v8"
                  code:
                    local:
                      filename: "/etc/istio/extensions/auth_wasm_filter.wasm"
```

---

## 5. 服务网格 API 治理

### 5.1 Istio VirtualService

**流量路由**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service
spec:
  hosts:
    - payment-service
  http:
    - match:
        - headers:
            version:
              exact: v2
      route:
        - destination:
            host: payment-service
            subset: v2
          weight: 100
    - route:
        - destination:
            host: payment-service
            subset: v1
          weight: 90
        - destination:
            host: payment-service
            subset: v2
          weight: 10
```

**限流配置**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: payment-service
spec:
  hosts:
    - payment-service
  http:
    - route:
        - destination:
            host: payment-service
      fault:
        delay:
          percentage:
            value: 10
          fixedDelay: 5s
      timeout: 10s
```

### 5.2 DestinationRule

**负载均衡策略**：

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service
spec:
  host: payment-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 10
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutiveErrors: 3
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

---

## 6. 策略即代码（OPA）

### 6.1 OPA 策略定义

**Rego 策略示例**：

```rego
package api.authz

default allow = false

# 允许健康检查
allow {
    input.method == "GET"
    input.path == "/health"
}

# 允许支付服务访问支付 API
allow {
    input.method == "POST"
    input.path == "/api/v1/payments"
    input.principal == "payment-service"
    input.claims.role == "payment-writer"
}

# 拒绝未授权访问
deny[msg] {
    not allow
    msg := "Access denied"
}
```

### 6.2 OPA + Kubernetes

**OPA Gatekeeper 策略**：

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg}] {
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required[_]
          not provided[missing]
          msg := sprintf("Missing required label: %v", [missing])
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: must-have-api-version
spec:
  match:
    kinds:
      - apiGroups: ["api.example.com"]
        kinds: ["APIDefinition"]
  parameters:
    labels: ["api-version"]
```

### 6.3 OPA-Wasm

**OPA 策略编译为 WASM**：

```bash
# 编译 Rego 策略为 WASM
opa build -t wasm -e api/authz/allow policy.rego

# 使用 OPA-Wasm
opa eval --format=json --wasm-bundle=bundle.tar.gz 'data.api.authz.allow'
```

---

## 7. API 版本管理

### 7.1 语义化版本

**版本号格式**：`MAJOR.MINOR.PATCH`

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-service-api
spec:
  version: "2.0.0" # 主版本升级
  deprecationPolicy:
    sunsetDate: "2025-12-31"
    replacement: "payment-service-api-v3"
```

### 7.2 API 生命周期管理

**生命周期状态**：

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-service-api
spec:
  lifecycle: deprecated # active | deprecated | sunset
  deprecationPolicy:
    announcementDate: "2025-01-01"
    sunsetDate: "2025-12-31"
    replacement: "payment-service-api-v3"
    migrationGuide: "https://docs.example.com/migration"
```

### 7.3 GitOps 版本管理

**ArgoCD Application**：

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: api-definitions
spec:
  project: default
  source:
    repoURL: https://github.com/example/api-definitions
    targetRevision: main
    path: apis
  destination:
    server: https://kubernetes.default.svc
    namespace: api-governance
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## 8. 形式化定义与理论基础

### 8.1 API 治理形式化模型

**定义 8.1（API 治理）**：API 治理是一个四元组：

```text
API_Governance = ⟨Lifecycle, Policy, Version, Access_Control⟩
```

其中：

- **Lifecycle**：生命周期管理 `Lifecycle: API → State`
- **Policy**：策略执行 `Policy: API × Rule → Decision`
- **Version**：版本管理 `Version: API → Version_Set`
- **Access_Control**：访问控制 `Access_Control: Identity × API → Permission`

**定义 8.2（治理有效性）**：治理有效性是一个函数：

```text
Governance_Effectiveness(API) = f(Policy_Compliance, Version_Consistency, Access_Control_Coverage)
```

其中：

- **Policy_Compliance**：策略遵循度 `[0, 1]`
- **Version_Consistency**：版本一致性 `[0, 1]`
- **Access_Control_Coverage**：访问控制覆盖度 `[0, 1]`

**定理 8.1（治理完备性）**：如果治理有效性为 1，则 API 完全受治理：

```text
Governance_Effectiveness(API) = 1 ⟹ Fully_Governed(API)
```

**证明**：如果策略遵循度、版本一致性和访问控制覆盖度都为 1，则 API 完全受治理。□

### 8.2 策略执行形式化

**定义 8.3（策略）**：策略是一个三元组：

```text
Policy = ⟨Rule, Condition, Action⟩
```

其中：

- **Rule**：规则 `Rule: Expression`
- **Condition**：条件 `Condition: Context → Bool`
- **Action**：动作 `Action: Decision`

**定义 8.4（策略执行）**：策略执行是一个函数：

```text
Execute_Policy: Policy × API × Context → Decision
```

**定理 8.2（策略一致性）**：相同策略在相同上下文中产生相同决策：

```text
Execute_Policy(Policy, API, Context) = Execute_Policy(Policy, API, Context')
```

**证明**：根据定义 8.4，策略执行是确定性的，因此相同策略在相同上下文中产生相同决
策。□

**定义 8.5（策略组合）**：策略组合是一个函数：

```text
Compose_Policies: Policy[] → Policy
```

**定理 8.3（策略组合可结合性）**：策略组合是可结合的：

```text
Compose_Policies(Compose_Policies(P₁, P₂), P₃) = Compose_Policies(P₁, Compose_Policies(P₂, P₃))
```

**证明**：策略组合操作满足结合律，因此可结合。□

### 8.3 生命周期管理形式化

**定义 8.6（API 生命周期）**：API 生命周期是一个状态机：

```text
Lifecycle_States = {Draft, Active, Deprecated, Sunset}
```

**定义 8.7（生命周期转换）**：生命周期转换是一个函数：

```text
Transition: State × Event → State
```

**定理 8.4（生命周期确定性）**：生命周期转换是确定的：

```text
Transition(state, event) = state' ⟹ ∀ state₁ = state: Transition(state₁, event) = state'
```

**证明**：根据定义 8.7，生命周期转换是确定性的，相同状态和事件总是产生相同的新状
态。□

**定义 8.8（版本兼容性）**：版本兼容性是一个函数：

```text
Version_Compatible: Version × Version → Bool
```

**定理 8.5（版本兼容性传递性）**：版本兼容性是传递的：

```text
Version_Compatible(v₁, v₂) ∧ Version_Compatible(v₂, v₃) ⟹ Version_Compatible(v₁, v₃)
```

**证明**：如果 `v₁` 与 `v₂` 兼容，`v₂` 与 `v₃` 兼容，则 `v₁` 与 `v₃` 兼容。□

---

## 9. 相关文档

- **[容器化 API 规范](../01-containerization-api/containerization-api.md)** -
  Kubernetes CRD API 治理
- **[最佳实践](../00-foundation/05-best-practices.md)** - API 治理最佳实践
- **[API 安全规范](../11-api-security/api-security.md)** - API 安全治理
- **[OPA 策略治理](../../ARCHITECTURE/architecture-view/04-opa-policy-governance/)** -
  OPA 详细文档
- **[服务网格技术规范](../../TECHNICAL/19-service-mesh/)** - Service Mesh API 治
  理
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新**：2025-11-07 **维护者**：项目团队
