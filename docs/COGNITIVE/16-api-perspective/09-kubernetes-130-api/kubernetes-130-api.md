# Kubernetes 1.30+ API 增强详解

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 Kubernetes 1.30+ 核心 API 更新](#11-kubernetes-130-核心-api-更新)
- [2. RuntimeClass 增强](#2-runtimeclass-增强)
  - [2.1 RuntimeClass API 增强](#21-runtimeclass-api-增强)
  - [2.2 RuntimeClass 使用场景](#22-runtimeclass-使用场景)
- [3. HPA 按 Runtime 维度分组](#3-hpa-按-runtime-维度分组)
  - [3.1 HPA Runtime 分组配置](#31-hpa-runtime-分组配置)
  - [3.2 混部场景 HPA 配置](#32-混部场景-hpa-配置)
- [4. ValidatingAdmissionPolicy 稳定版](#4-validatingadmissionpolicy-稳定版)
  - [4.1 ValidatingAdmissionPolicy 配置](#41-validatingadmissionpolicy-配置)
  - [4.2 ValidatingAdmissionPolicyBinding](#42-validatingadmissionpolicybinding)
- [5. CustomResourceDefinition v1.1](#5-customresourcedefinition-v11)
  - [5.1 CRD v1.1 新特性](#51-crd-v11-新特性)
- [6. 实际案例](#6-实际案例)
  - [6.1 案例：支付服务 API 现代化](#61-案例支付服务-api-现代化)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

Kubernetes 1.30+ 在 API 规范方面带来了重要增强，特别是 RuntimeClass 增强、HPA 按
Runtime 维度分组、ValidatingAdmissionPolicy 稳定版等特性，为容器化、沙盒化、WASM
化的 API 设计提供了更好的支持。

### 1.1 Kubernetes 1.30+ 核心 API 更新

| API 特性                          | 版本  | 状态   | 核心内容                       |
| --------------------------------- | ----- | ------ | ------------------------------ |
| **RuntimeClass 增强**             | 1.30+ | GA     | 支持 overhead、scheduling 配置 |
| **HPA Runtime 分组**              | 1.30+ | Beta   | 按 runtimeClassName 维度分组   |
| **ValidatingAdmissionPolicy**     | 1.28+ | Stable | CEL 表达式验证                 |
| **CustomResourceDefinition v1.1** | 1.30+ | GA     | 增强的验证和默认值支持         |

---

## 2. RuntimeClass 增强

### 2.1 RuntimeClass API 增强

**Kubernetes 1.30+ RuntimeClass 完整配置**：

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: wasm
handler: crun
# 新增：overhead 配置
overhead:
  podFixed:
    memory: "64Mi"
    cpu: "50m"
# 新增：scheduling 配置
scheduling:
  nodeSelector:
    wasm-runtime: enabled
  tolerations:
    - key: wasm-workload
      operator: Equal
      value: "true"
      effect: NoSchedule
```

### 2.2 RuntimeClass 使用场景

**场景 1：混部 Linux 容器和 WASM 容器**

```yaml
# Linux 容器 Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: linux-app
spec:
  template:
    spec:
      runtimeClassName: runc # 默认运行时
      containers:
        - name: app
          image: nginx:latest

---
# WASM 容器 Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wasm-app
spec:
  template:
    spec:
      runtimeClassName: wasm # WASM 运行时
      containers:
        - name: app
          image: wasm-app:latest
```

**场景 2：不同沙盒化运行时**

```yaml
# gVisor RuntimeClass
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
overhead:
  podFixed:
    memory: "2Gi"
    cpu: "100m"

---
# Kata Containers RuntimeClass
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: kata
handler: kata
overhead:
  podFixed:
    memory: "512Mi"
    cpu: "200m"
```

---

## 3. HPA 按 Runtime 维度分组

### 3.1 HPA Runtime 分组配置

**Kubernetes 1.30+ HPA 配置**：

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: payment-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      policies:
        - type: Pods
          value: 1
          periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      policies:
        - type: Pods
          value: 2
          periodSeconds: 30
      selectPolicy: Max
```

### 3.2 混部场景 HPA 配置

**Linux 容器和 WASM 容器混部**：

```yaml
# Linux 容器 HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: linux-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: linux-app
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
  # 按 runtimeClassName: runc 分组
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300

---
# WASM 容器 HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: wasm-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: wasm-app
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80 # WASM 容器可以设置更高的利用率
  # 按 runtimeClassName: wasm 分组
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 60 # WASM 容器可以更快缩容
```

---

## 4. ValidatingAdmissionPolicy 稳定版

### 4.1 ValidatingAdmissionPolicy 配置

**Kubernetes 1.28+ 稳定版配置**：

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: api-spec-validation
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
    - expression: "object.spec.lifecycle in ['active', 'deprecated', 'sunset']"
      message: "Lifecycle must be one of: active, deprecated, sunset"
  variables:
    - name: "now"
      expression: "now()"
```

### 4.2 ValidatingAdmissionPolicyBinding

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: api-spec-validation-binding
spec:
  policyName: api-spec-validation
  validationActions: [Deny]
  matchResources:
    namespaceSelector:
      matchLabels:
        api-governance: enabled
```

---

## 5. CustomResourceDefinition v1.1

### 5.1 CRD v1.1 新特性

**默认值支持**：

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
          properties:
            spec:
              type: object
              properties:
                lifecycle:
                  type: string
                  enum: [active, deprecated, sunset]
                  default: active # 默认值
                version:
                  type: string
                  default: "1.0.0" # 默认版本
```

**CEL 表达式验证**：

```yaml
versions:
  - name: v1
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            x-kubernetes-validations:
              - rule: "self.version.matches('^[0-9]+\\.[0-9]+\\.[0-9]+$')"
                message: "Version must be semantic version"
              - rule:
                  "has(self.deprecationPolicy) ?
                  self.deprecationPolicy.sunsetDate > now() : true"
                message: "Sunset date must be in the future"
```

---

## 6. 实际案例

### 6.1 案例：支付服务 API 现代化

**场景**：将支付服务从传统容器迁移到 WASM 容器，并实现混部

**步骤 1：创建 RuntimeClass**

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

**步骤 2：创建 WASM 版本 Deployment**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service-wasm
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-service
      runtime: wasm
  template:
    metadata:
      labels:
        app: payment-service
        runtime: wasm
    spec:
      runtimeClassName: wasm
      containers:
        - name: payment-service
          image: payment-service-wasm:latest
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "200m"
```

**步骤 3：配置 HPA**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: payment-service-wasm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: payment-service-wasm
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 1
          periodSeconds: 30
```

**步骤 4：API 规范 CRD**

```yaml
apiVersion: api.example.com/v1
kind: APIDefinition
metadata:
  name: payment-service-api
spec:
  openapi: "3.1.0"
  version: "2.0.0"
  lifecycle: active
  deprecationPolicy:
    sunsetDate: "2026-12-31"
    replacement: "payment-service-api-v3"
```

---

## 7. 相关文档

- **[容器化 API 规范](../01-containerization-api/containerization-api.md)** -
  Kubernetes CRD API 详解
- **[2025 技术生态](../04-2025-ecosystem/2025-ecosystem.md)** - Kubernetes 1.30+
  生态更新
- **[最佳实践](../08-best-practices/best-practices.md)** - API 规范最佳实践
- **[编排运行时技术规范](../../TECHNICAL/04-orchestration-runtime/orchestration-runtime.md)** -
  RuntimeClass 详细文档
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新**：2025-11-07 **维护者**：项目团队
