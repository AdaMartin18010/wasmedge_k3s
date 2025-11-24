# API 安全规范

**版本**：v1.0 **最后更新：2025-11-15 **维护者**：项目团队

## 📑 目录

- [API 安全规范](#api-安全规范)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 API 安全层次](#11-api-安全层次)
    - [1.2 API 安全在 API 规范中的位置](#12-api-安全在-api-规范中的位置)
  - [2 容器化 API 安全](#2-容器化-api-安全)
    - [2.1 Kubernetes RBAC API](#21-kubernetes-rbac-api)
    - [2.2 Pod Security Standards](#22-pod-security-standards)
  - [3 沙盒化 API 安全](#3-沙盒化-api-安全)
    - [3.1 Seccomp Profile 安全](#31-seccomp-profile-安全)
    - [3.2 gVisor 安全配置](#32-gvisor-安全配置)
  - [4 WASM 化 API 安全](#4-wasm-化-api-安全)
    - [4.1 WASI 能力令牌模型](#41-wasi-能力令牌模型)
    - [4.2 WasmEdge 安全配置](#42-wasmedge-安全配置)
  - [5 API 安全模型对比](#5-api-安全模型对比)
    - [5.1 安全级别对比](#51-安全级别对比)
    - [5.2 安全策略组合](#52-安全策略组合)
      - [5.2.1 组合 1：容器化 + Seccomp](#521-组合-1容器化--seccomp)
      - [5.2.2 组合 2：gVisor + OPA](#522-组合-2gvisor--opa)
      - [5.2.3 组合 3：WASM + WASI 能力](#523-组合-3wasm--wasi-能力)
  - [6 零信任 API 架构](#6-零信任-api-架构)
    - [6.1 SPIFFE/SPIRE 集成](#61-spiffespire-集成)
    - [6.2 mTLS 强制](#62-mtls-强制)
  - [7 形式化定义与理论基础](#7-形式化定义与理论基础)
    - [7.1 API 安全形式化模型](#71-api-安全形式化模型)
    - [7.2 认证授权形式化](#72-认证授权形式化)
    - [7.3 安全隔离形式化](#73-安全隔离形式化)
  - [8 相关文档](#8-相关文档)

---

## 1 概述

API 安全规范是 API 设计的核心要素，从容器化的 RBAC 到沙盒化的 Seccomp，再到 WASM
的能力令牌模型，提供了不同级别的安全保护。本文档基于形式化方法，提供严格的数学定
义和推理论证，分析 API 安全的理论基础和实践方法。

**参考标准**：

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/) -
  OWASP API 安全 Top 10
- [SPIFFE/SPIRE](https://spiffe.io/) - SPIFFE/SPIRE 规范
- [mTLS](https://datatracker.ietf.org/doc/html/rfc8446) - TLS 1.3 规范
- [WASI Security](https://github.com/WebAssembly/WASI/blob/main/docs/Security.md) -
  WASI 安全模型
- [Kubernetes Security](https://kubernetes.io/docs/concepts/security/) -
  Kubernetes 安全文档

### 1.1 API 安全层次

```text
应用层安全（OAuth2、JWT）
  ↓
服务层安全（mTLS、SPIFFE）
  ↓
运行时安全（Seccomp、AppArmor）
  ↓
沙盒安全（gVisor、Kata）
  ↓
WASM 能力安全（WASI 能力令牌）
```

### 1.2 API 安全在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API 安全是 Security 维度的核心：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
                                               ↑
                                    API Security
```

API 安全在 API 规范中提供：

- **认证机制**：SPIFFE/SPIRE、OAuth2、mTLS 等身份认证
- **授权机制**：RBAC、ABAC、OPA 等权限控制
- **运行时安全**：Seccomp、AppArmor、gVisor 等运行时隔离
- **能力安全**：WASI 能力令牌模型

---

## 2 容器化 API 安全

### 2.1 Kubernetes RBAC API

**Role 定义**：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: api-reader
  namespace: payment
rules:
  - apiGroups: ["api.payment.com"]
    resources: ["apidefinitions"]
    verbs: ["get", "list", "watch"]
```

**RoleBinding**：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: api-reader-binding
  namespace: payment
subjects:
  - kind: ServiceAccount
    name: api-client
    namespace: payment
roleRef:
  kind: Role
  name: api-reader
  apiGroup: rbac.authorization.k8s.io
```

### 2.2 Pod Security Standards

**Restricted Policy**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: app:latest
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
        readOnlyRootFilesystem: true
```

---

## 3 沙盒化 API 安全

### 3.1 Seccomp Profile 安全

**严格 Seccomp Profile**：

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": ["read", "write", "open", "close", "fstat", "lseek"],
      "action": "SCMP_ACT_ALLOW"
    },
    {
      "names": ["exit", "exit_group"],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

### 3.2 gVisor 安全配置

**gVisor RuntimeClass**：

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor-secure
handler: runsc
overhead:
  podFixed:
    memory: "2Gi"
    cpu: "100m"
```

**Pod 配置**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gvisor-pod
spec:
  runtimeClassName: gvisor-secure
  containers:
    - name: app
      image: app:latest
      securityContext:
        capabilities:
          drop:
            - ALL
```

---

## 4 WASM 化 API 安全

### 4.1 WASI 能力令牌模型

**能力最小化原则**：

```wit
// ❌ 错误：暴露过多能力
world insecure-world {
    import wasi:filesystem/filesystem@0.2.0;
    import wasi:network/sockets@0.2.0;
    import wasi:random/random@0.2.0;
    // 不需要的能力也被导入
}

// ✅ 正确：只导入需要的能力
world secure-world {
    import wasi:http/incoming-handler@0.2.0;
    // 仅 HTTP 能力，无文件系统、网络底层访问
    export handle: func(req: incoming-request) -> response;
}
```

### 4.2 WasmEdge 安全配置

**WasmEdge 配置**：

```toml
[wasmtime]
# 内存限制
max_memory_size = 16777216  # 16MB

# 禁用非确定性指令
disallow_non_deterministic = true

# 启用时间限制
timeout = 1000  # 1秒超时
```

---

## 5 API 安全模型对比

### 5.1 安全级别对比

| 安全方案      | 隔离级别     | 性能开销 | 适用场景     |
| ------------- | ------------ | -------- | ------------ |
| **RBAC**      | 应用级       | 低       | 容器化 API   |
| **Seccomp**   | 系统调用级   | <1%      | 容器化 API   |
| **gVisor**    | 用户态内核级 | 10-20%   | 高安全容器化 |
| **Kata**      | 硬件级       | 10-15%   | 极高安全场景 |
| **WASI 能力** | 接口级       | <5%      | WASM API     |

### 5.2 安全策略组合

#### 5.2.1 组合 1：容器化 + Seccomp

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: strict-seccomp.json
  containers:
    - name: app
      securityContext:
        capabilities:
          drop:
            - ALL
```

#### 5.2.2 组合 2：gVisor + OPA

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor-opa
handler: runsc

---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: gvisor-policy
spec:
  selector:
    matchLabels:
      runtime: gvisor
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/default/sa/trusted-service"]
```

#### 5.2.3 组合 3：WASM + WASI 能力

```wit
world secure-api {
    import wasi:http/incoming-handler@0.2.0;
    // 仅 HTTP 能力
    import wasi:keyvalue/readwrite@0.2.0;
    // 仅 Key-Value 存储能力
    // 无文件系统、网络底层访问
    export handle: func(req: incoming-request) -> response;
}
```

---

## 6 零信任 API 架构

### 6.1 SPIFFE/SPIRE 集成

**SPIFFE 身份**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    spiffe.io/spiffe-id: spiffe://example.com/ns/payment/sa/payment-service
spec:
  serviceAccountName: payment-service
  containers:
    - name: app
      image: payment-service:latest
```

**SPIRE 配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: spire-config
data:
  server.conf: |
    server {
        bind_address = "0.0.0.0"
        bind_port = "8081"
        trust_domain = "example.com"
    }
```

### 6.2 mTLS 强制

**Istio PeerAuthentication**：

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: payment
spec:
  mtls:
    mode: STRICT
```

**AuthorizationPolicy**：

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: payment-policy
  namespace: payment
spec:
  selector:
    matchLabels:
      app: payment-service
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/payment/sa/payment-service"]
      to:
        - operation:
            methods: ["POST"]
            paths: ["/api/v1/payments"]
```

---

## 7 形式化定义与理论基础

### 7.1 API 安全形式化模型

**定义 7.1（API 安全）**：API 安全是一个四元组：

```text
API_Security = ⟨Authentication, Authorization, Isolation, Encryption⟩
```

其中：

- **Authentication**：认证机制 `Authentication: Identity → Token`
- **Authorization**：授权机制 `Authorization: Token × Resource → Permission`
- **Isolation**：隔离机制 `Isolation: Process × Process → Bool`
- **Encryption**：加密机制 `Encryption: Data → Encrypted_Data`

**定义 7.2（安全级别）**：安全级别是一个函数：

```text
Security_Level(API) = f(Authentication_Strength, Authorization_Granularity, Isolation_Depth, Encryption_Strength)
```

**定理 7.1（安全级别单调性）**：安全级别越高，API 越安全：

```text
Security_Level(API₁) > Security_Level(API₂) ⟹ Security(API₁) > Security(API₂)
```

**证明**：根据定义 7.2，安全级别越高，认证、授权、隔离和加密强度越高，因此 API
越安全。□

### 7.2 认证授权形式化

**定义 7.3（认证）**：认证是一个函数：

```text
Authenticate: Identity × Credentials → Token | Error
```

**定义 7.4（授权）**：授权是一个函数：

```text
Authorize: Token × Resource × Action → Permission | Denied
```

**定理 7.2（认证授权顺序性）**：授权必须在认证之后：

```text
Authorize(token, resource, action) ≠ Denied ⟹ ∃ identity: Authenticate(identity, creds) = token
```

**证明**：如果授权成功，则必须存在有效的 token，而 token 只能通过认证获得。□

**定义 7.5（最小权限原则）**：最小权限原则要求：

```text
Minimal_Privilege(API) ⟺ ∀ resource, action: Authorize(token, resource, action) = Allow ⟹ Required(resource, action)
```

**定理 7.3（最小权限安全性）**：遵循最小权限原则的 API 更安全：

```text
Minimal_Privilege(API₁) ∧ ¬Minimal_Privilege(API₂) ⟹ Security(API₁) > Security(API₂)
```

**证明**：根据最小权限原则，API₁ 只授予必要的权限，攻击面更小，因此更安全。□

### 7.3 安全隔离形式化

**定义 7.6（隔离）**：隔离是一个函数：

```text
Isolation: Process₁ × Process₂ → Bool
```

其中 `Isolation(p₁, p₂) = true` 表示 `p₁` 和 `p₂` 相互隔离。

**定理 7.4（隔离传递性）**：如果 `p₁` 与 `p₂` 隔离，`p₂` 与 `p₃` 隔离，则 `p₁`
与 `p₃` 隔离：

```text
Isolation(p₁, p₂) ∧ Isolation(p₂, p₃) ⟹ Isolation(p₁, p₃)
```

**证明**：根据隔离的定义，如果 `p₁` 与 `p₂` 隔离，`p₂` 与 `p₃` 隔离，则 `p₁` 无
法访问 `p₂` 的资源，`p₂` 无法访问 `p₃` 的资源，因此 `p₁` 无法访问 `p₃` 的资源，
所以 `p₁` 与 `p₃` 隔离。□

**定义 7.7（安全边界）**：安全边界是一个函数：

```text
Security_Boundary: Process → Resource_Set
```

**定理 7.5（边界隔离性）**：不同安全边界的进程相互隔离：

```text
Security_Boundary(p₁) ∩ Security_Boundary(p₂) = ∅ ⟹ Isolation(p₁, p₂)
```

**证明**：如果两个进程的安全边界不相交，则它们无法访问对方的资源，因此相互隔离
。□

---

## 8 相关文档

- **[沙盒化 API 规范](../02-sandboxing-api/sandboxing-api.md)** - 沙盒化 API 安
  全详解
- **[WASM 化 API 规范](../03-wasm-api/wasm-api.md)** - WASI 能力模型详解
- **[最佳实践](../00-foundation/05-best-practices.md)** - API 安全最佳实践
- **[OPA 策略治理](../../ARCHITECTURE/architecture-view/04-opa-policy-governance/)** -
  OPA 安全策略
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新：2025-11-15 **维护者**：项目团队
