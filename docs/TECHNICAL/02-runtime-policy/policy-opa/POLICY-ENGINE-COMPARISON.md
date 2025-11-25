# 策略引擎对比分析

> **创建日期**：2025-11-15
> **最后更新**：2025-11-15
> **状态**：已建立
> **维护者**：技术团队

---

## 📋 概述

本文档对比分析 Gatekeeper 和 Kyverno 两种主流 Kubernetes 策略引擎。

---

## 🔄 方案对比

### 核心特性对比

| 特性 | Gatekeeper | Kyverno |
|------|------------|---------|
| **策略语言** | Rego | YAML |
| **学习曲线** | 陡峭 | 平缓 |
| **Kubernetes 集成** | 好 | 最好 |
| **策略类型** | Validate | Validate/Mutate/Generate/VerifyImages |
| **性能** | 中等 | 高 |
| **Wasm 支持** | 无 | v2 支持 |
| **社区活跃度** | 高 | 高 |
| **CNCF 状态** | Graduated | Sandbox |

### 功能特性对比

| 功能 | Gatekeeper | Kyverno |
|------|------------|---------|
| **Validate** | ✅ | ✅ |
| **Mutate** | ❌ | ✅ |
| **Generate** | ❌ | ✅ |
| **VerifyImages** | ❌ | ✅ |
| **审计** | ✅ | ✅ |
| **报告** | ✅ | ✅ |
| **Wasm 支持** | ❌ | ✅ (v2) |

### 性能对比

| 指标 | Gatekeeper | Kyverno |
|------|------------|---------|
| **策略执行延迟** | ~50ms | ~20ms |
| **CPU 占用** | 中等 | 低 |
| **内存占用** | 中等 | 低 |
| **策略复杂度** | 高 | 低 |

---

## 🎯 选型建议

### 选择 Gatekeeper 的场景

- ✅ 需要复杂策略逻辑
- ✅ 团队熟悉 Rego 语言
- ✅ 需要与 OPA 生态集成
- ✅ 需要跨平台策略

### 选择 Kyverno 的场景

- ✅ 追求简单易用
- ✅ 需要 Mutate/Generate 功能
- ✅ 需要镜像验证
- ✅ Kubernetes 原生需求

---

## 📊 详细对比

### 1. 策略编写

#### Gatekeeper

```rego
package k8srequiredlabels

violation[{"msg": msg}] {
    not input.review.object.metadata.labels["app"]
    msg := "All pods must have an 'app' label"
}
```

#### Kyverno

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  rules:
    - name: check-labels
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "All pods must have 'app' label"
        pattern:
          metadata:
            labels:
              app: "?*"
```

### 2. 功能对比

#### Mutate 功能

- **Gatekeeper**：不支持
- **Kyverno**：支持，可以自动修改资源

#### Generate 功能

- **Gatekeeper**：不支持
- **Kyverno**：支持，可以自动生成资源

#### VerifyImages 功能

- **Gatekeeper**：不支持
- **Kyverno**：支持，可以验证镜像签名和漏洞

---

## 💡 最佳实践

### 1. 策略组织

- **Gatekeeper**：使用 ConstraintTemplate 和 Constraint
- **Kyverno**：使用 ClusterPolicy 和 Policy

### 2. 性能优化

- 避免复杂策略
- 使用策略缓存
- 合理设置资源限制

### 3. 安全配置

- 启用镜像验证
- 配置资源限制
- 定期审查策略

---

## 🔗 相关文档

- [OPA 策略引擎](policy-opa.md)
- [Gatekeeper 集成](gatekeeper.md)
- [Kyverno v2](KYVERNO-V2.md)
- [策略即代码最佳实践](../07-security-compliance/security-compliance/security-compliance.md)

---

**最后更新**：2025-11-15
**维护者**：技术团队
