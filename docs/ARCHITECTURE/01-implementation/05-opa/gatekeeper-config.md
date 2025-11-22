# Gatekeeper 配置示例

## 📑 目录

- [Gatekeeper 配置示例](#gatekeeper-配置示例)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 理论基础](#11-理论基础)
  - [2 Gatekeeper 安装配置](#2-gatekeeper-安装配置)
    - [2.1 Helm 安装 Gatekeeper](#21-helm-安装-gatekeeper)
    - [2.2 Gatekeeper 验证安装](#22-gatekeeper-验证安装)
    - [2.3 Gatekeeper 配置](#23-gatekeeper-配置)
  - [3 ConstraintTemplate 示例](#3-constrainttemplate-示例)
    - [3.1 镜像验证 ConstraintTemplate](#31-镜像验证-constrainttemplate)
    - [3.2 资源限制 ConstraintTemplate](#32-资源限制-constrainttemplate)
    - [3.3 标签验证 ConstraintTemplate](#33-标签验证-constrainttemplate)
  - [4 Constraint 示例](#4-constraint-示例)
    - [4.1 镜像验证 Constraint](#41-镜像验证-constraint)
    - [4.2 资源限制 Constraint](#42-资源限制-constraint)
    - [4.3 标签验证 Constraint](#43-标签验证-constraint)
  - [5 相关文档](#5-相关文档)
    - [5.1 理论论证](#51-理论论证)
    - [5.2 架构视角](#52-架构视角)
    - [5.3 技术文档](#53-技术文档)
  - [6 2025 年最新实践](#6-2025-年最新实践)
    - [6.1 Gatekeeper 3.15+ 新特性（2025）](#61-gatekeeper-315-新特性2025)
    - [6.2 OPA-Wasm 策略支持（2025）](#62-opa-wasm-策略支持2025)
    - [6.3 多集群 Gatekeeper 部署（2025）](#63-多集群-gatekeeper-部署2025)
  - [7 实际应用案例](#7-实际应用案例)
    - [案例 1：多租户资源配额策略](#案例-1多租户资源配额策略)
    - [案例 2：镜像安全扫描策略](#案例-2镜像安全扫描策略)
    - [案例 3：标签验证策略](#案例-3标签验证策略)

---

## 1 概述

本文档提供 **Gatekeeper 的实际配置示例**，展示如何通过 Gatekeeper 在 Kubernetes
中实施 OPA 策略。

### 1.1 理论基础

Gatekeeper 配置基于以下理论论证：

- **公理 A5-A8（OPA 公理）**：
  - A5：能力闭包
  - A6：最小权限
  - A7：可证明性
  - A8：版本一致性
- **引理 L3（OPA 确定性）**：OPA 求值过程 ≡ 单调不动点迭代，决策在有限步内唯一且
  可重现

**详细理论论证**：参见 [`../../00-theory/`](../../00-theory/)

---

## 2 Gatekeeper 安装配置

### 2.1 Helm 安装 Gatekeeper

```bash
# 添加 Gatekeeper Helm 仓库
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts

# 安装 Gatekeeper
helm install gatekeeper gatekeeper/gatekeeper \
  --namespace gatekeeper-system \
  --create-namespace
```

### 2.2 Gatekeeper 验证安装

```bash
# 检查 Gatekeeper 组件
kubectl get pods -n gatekeeper-system

# 检查 Gatekeeper CRD
kubectl get crd | grep gatekeeper
```

### 2.3 Gatekeeper 配置

```yaml
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
  namespace: gatekeeper-system
spec:
  match:
    - excludedNamespaces: ["kube-system", "kube-public", "kube-node-lease"]
    - processes: ["*"]
```

---

## 3 ConstraintTemplate 示例

### 3.1 镜像验证 ConstraintTemplate

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredimages
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredImages
      validation:
        openAPIV3Schema:
          type: object
          properties:
            allowedRepos:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredimages

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not starts_with(container.image, allowed_repo)
          allowed_repo := input.parameters.allowedRepos[_]
          msg := sprintf("Image '%v' is not from allowed repositories", [container.image])
        }
```

### 3.2 资源限制 ConstraintTemplate

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredresources
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredResources
      validation:
        openAPIV3Schema:
          type: object
          properties:
            limits:
              type: object
              properties:
                cpu:
                  type: string
                memory:
                  type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredresources

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.resources.limits
          msg := sprintf("Container '%v' must specify resource limits", [container.name])
        }

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          cpu_limit := container.resources.limits.cpu
          cpu_limit > input.parameters.limits.cpu
          msg := sprintf("Container '%v' CPU limit '%v' exceeds maximum '%v'", [container.name, cpu_limit, input.parameters.limits.cpu])
        }
```

### 3.3 标签验证 ConstraintTemplate

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
          required_label := input.parameters.labels[_]
          not input.review.object.metadata.labels[required_label]
          msg := sprintf("Missing required label: %v", [required_label])
        }
```

---

## 4 Constraint 示例

### 4.1 镜像验证 Constraint

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredImages
metadata:
  name: must-have-allowed-repo
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    allowedRepos:
      - "yourhub.com/"
      - "gcr.io/"
```

### 4.2 资源限制 Constraint

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredResources
metadata:
  name: must-have-resource-limits
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    limits:
      cpu: "2"
      memory: "2Gi"
```

### 4.3 标签验证 Constraint

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: must-have-labels
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    labels:
      - "app"
      - "version"
      - "environment"
```

---

## 5 相关文档

### 5.1 理论论证

- **`../../00-theory/01-axioms/A5-A8-opa.md`** - OPA 公理（A5-A8）
- **`../../00-theory/05-lemmas-theorems/L3-opa-determinism.md`** - OPA 确定性引
  理

### 5.2 架构视角

- **`../../02-views/10-quick-views/opa-policy-governance-view.md`** - OPA 策略治
  理架构视角

### 5.3 技术文档

- **`../../../TECHNICAL/02-runtime-policy/policy-opa/policy-opa.md`** - OPA 技术文档

## 6 2025 年最新实践

### 6.1 Gatekeeper 3.15+ 新特性（2025）

**最新版本**：Gatekeeper 3.15+（2025 年）

**新特性**：

- **Wasm 引擎支持**：支持 Wasm 编译的策略
- **性能优化**：策略评估性能提升 50%
- **审计增强**：改进的审计功能

**安装最新版本**：

```bash
# 安装 Gatekeeper 3.15
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm install gatekeeper gatekeeper/gatekeeper \
  --version 3.15.0 \
  --namespace gatekeeper-system \
  --create-namespace
```

### 6.2 OPA-Wasm 策略支持（2025）

**2025 年趋势**：使用 Wasm 编译策略提升性能

**优势**：

- **性能提升**：策略评估性能提升 3-5 倍
- **资源优化**：减少内存占用
- **跨平台**：Wasm 策略可跨平台运行

**配置示例**：

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredimages
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredImages
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredimages
        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not startswith(container.image, "myregistry.com/")
          msg := "Image must come from myregistry.com"
        }
      # 启用 Wasm 编译
      code:
        engine: opa-wasm
```

### 6.3 多集群 Gatekeeper 部署（2025）

**2025 年趋势**：多集群统一策略管理

**配置示例**：

```yaml
# 多集群 Gatekeeper 配置
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
  namespace: gatekeeper-system
spec:
  match:
    - excludedNamespaces: ["kube-system", "kube-public"]
    - processes: ["*"]
  # 多集群同步配置
  sync:
    syncOnly:
      - group: ""
        version: "v1"
        kind: "Namespace"
```

## 7 实际应用案例

### 案例 1：多租户资源配额策略

**场景**：在多租户环境中实施资源配额策略

**实现方案**：

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredresources
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredResources
      validation:
        openAPIV3Schema:
          type: object
          properties:
            limits:
              type: object
              properties:
                cpu:
                  type: string
                memory:
                  type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredresources
        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not container.resources.limits
          msg := "Container must have resource limits"
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredResources
metadata:
  name: must-have-resource-limits
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    limits:
      cpu: "2"
      memory: "2Gi"
```

**效果**：

- 资源控制：确保所有 Pod 有资源限制
- 多租户隔离：每个租户有独立的配额
- 自动拒绝：不符合策略的 Pod 自动拒绝

### 案例 2：镜像安全扫描策略

**场景**：实施镜像安全扫描策略

**实现方案**：

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredimagescan
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredImageScan
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredimagescan
        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          # 检查镜像是否通过安全扫描
          not data.scanned_images[container.image]
          msg := sprintf("Image %v must be scanned", [container.image])
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredImageScan
metadata:
  name: must-scan-images
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
```

**效果**：

- 安全扫描：确保所有镜像通过安全扫描
- 自动拒绝：未扫描的镜像自动拒绝
- 合规性：满足安全合规要求

### 案例 3：标签验证策略

**场景**：实施标签验证策略

**实现方案**：

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
          required := input.parameters.labels[_]
          not input.review.object.metadata.labels[required]
          msg := sprintf("Missing required label: %v", [required])
        }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: must-have-labels
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    labels:
      - "app"
      - "version"
      - "environment"
```

**效果**：

- 标签规范：确保所有资源有必需的标签
- 自动分类：通过标签自动分类资源
- 管理便利：便于资源管理和查询

---

## 8 使用指南

### 8.1 快速开始

**适用场景**：

- Kubernetes 策略即代码
- 多租户资源配额管理
- 安全合规策略实施
- 资源标签和注解验证

**快速步骤**：

1. **安装 Gatekeeper**：

   ```bash
   # 使用 Helm 安装
   helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
   helm install gatekeeper gatekeeper/gatekeeper
   ```

2. **验证安装**：

   ```bash
   # 检查 Gatekeeper 状态
   kubectl get pods -n gatekeeper-system

   # 检查 CRD
   kubectl get crd | grep gatekeeper
   ```

3. **创建第一个策略**：

   ```bash
   # 创建 ConstraintTemplate
   kubectl apply -f constraint-template.yaml

   # 创建 Constraint
   kubectl apply -f constraint.yaml
   ```

### 8.2 使用技巧

#### ConstraintTemplate 编写

**基础结构**：

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
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg}] {
          # Rego 策略逻辑
        }
```

**Rego 策略编写**：

- **输入对象**：`input.review.object` 包含待验证的资源
- **参数访问**：`input.parameters` 包含 Constraint 参数
- **违规报告**：使用 `violation` 数组报告违规

#### Constraint 配置

**匹配规则**：

```yaml
match:
  kinds:
    - apiGroups: [""]
      kinds: ["Pod"]
  namespaces: ["production"]
  excludedNamespaces: ["kube-system"]
```

**参数传递**：

```yaml
parameters:
  labels:
    - "app"
    - "version"
```

#### 策略测试

**Dry-run 模式**：

```bash
# 启用 dry-run 模式（只记录违规，不拒绝）
kubectl patch constrainttemplate k8srequiredlabels \
  --type merge -p '{"spec":{"targets":[{"target":"admission.k8s.gatekeeper.sh","rego":"..."}]}}'
```

**查看违规**：

```bash
# 查看所有违规
kubectl get constraintviolations

# 查看特定 Constraint 的违规
kubectl describe constraint k8srequiredlabels must-have-labels
```

### 8.3 常见问题

**Q1：策略未生效？**

- 检查 ConstraintTemplate 是否创建成功
- 检查 Constraint 的 match 规则是否正确
- 查看 Gatekeeper 日志：`kubectl logs -n gatekeeper-system -l control-plane=controller-manager`

**Q2：策略拒绝所有资源？**

- 检查 Rego 策略逻辑是否正确
- 使用 dry-run 模式测试策略
- 检查 Constraint 的 match 规则是否过于宽泛

**Q3：如何调试 Rego 策略？**

- 使用 OPA Playground 测试 Rego 代码
- 查看 Gatekeeper 审计日志
- 使用 `kubectl get constraintviolations` 查看详细违规信息

### 8.4 实践建议

**多租户资源配额**：

- 使用 ConstraintTemplate 定义资源限制策略
- 为每个租户创建独立的 Constraint
- 参考案例 1 的配置

**镜像安全扫描**：

- 集成镜像扫描工具（如 Trivy、Clair）
- 使用 Constraint 验证镜像扫描状态
- 参考案例 2 的配置

**标签验证**：

- 定义标准标签规范
- 使用 Constraint 强制标签要求
- 参考案例 3 的配置

**策略管理**：

- 使用 GitOps 管理策略配置
- 定期审查和更新策略
- 使用 Policy Library 复用常用策略

**性能考虑**：

- 避免过于复杂的 Rego 策略
- 使用 Constraint 的 match 规则限制作用范围
- 监控 Gatekeeper 的性能指标

---

**更新时间**：2025-11-15 **版本**：v1.2 **状态**：✅ 包含使用指南和 2025 年最新实践
