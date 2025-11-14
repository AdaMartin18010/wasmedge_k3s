# 案例 O-002：OPA 策略评估失败

> **案例编号**：O-002
> **故障类型**：策略评估故障
> **严重程度**：中等
> **创建日期**：2025-11-13
> **最后更新**：2025-11-13

---

## 📑 目录

- [案例 O-002：OPA 策略评估失败](#案例-o-002opa-策略评估失败)
  - [📑 目录](#-目录)
  - [1 问题描述](#1-问题描述)
    - [1.1 故障现象](#11-故障现象)
    - [1.2 环境信息](#12-环境信息)
    - [1.3 影响范围](#13-影响范围)
  - [2 故障排查过程](#2-故障排查过程)
    - [2.1 初步诊断](#21-初步诊断)
    - [2.2 深入排查](#22-深入排查)
    - [2.3 根因分析](#23-根因分析)
  - [3 解决方案](#3-解决方案)
    - [3.1 临时解决方案](#31-临时解决方案)
    - [3.2 永久解决方案](#32-永久解决方案)
    - [3.3 预防措施](#33-预防措施)
  - [4 验证与恢复](#4-验证与恢复)
    - [4.1 验证步骤](#41-验证步骤)
    - [4.2 恢复确认](#42-恢复确认)
  - [5 经验总结](#5-经验总结)
    - [5.1 关键发现](#51-关键发现)
    - [5.2 最佳实践](#52-最佳实践)
    - [5.3 相关文档](#53-相关文档)
  - [6 相关文档](#6-相关文档)

---

## 1 问题描述

### 1.1 故障现象

**主要症状**：

- OPA 策略评估失败
- 日志显示：`Error evaluating policy: rego_parse_error`
- 策略无法正确执行
- 应用部署被拒绝或策略不生效

**错误日志**：

```text
time="2025-11-13T18:00:15Z" level=error msg="Error evaluating policy: rego_parse_error"
time="2025-11-13T18:00:15Z" level=error msg="Policy evaluation failed: invalid syntax"
time="2025-11-13T18:00:15Z" level=error msg="Stack trace: at policy.rego:10:5"
```

**时间线**：

- **18:00:00** - 更新策略
- **18:00:05** - 策略评估开始
- **18:00:10** - 策略评估失败
- **18:00:15** - 应用部署被拒绝

### 1.2 环境信息

**集群信息**：

- **K3s 版本**：v1.30.4+k3s1
- **OPA 版本**：v0.58.0
- **Gatekeeper 版本**：v3.15
- **策略数量**：50+ 条

**策略配置**：

```rego
# policy.rego
package policy

default allow = false

allow {
    input.user.role == "admin"
    input.resource.type == "pod"
    input.action == "create"
    # 语法错误：缺少闭合括号
    input.resource.labels.env == "production"
}
```

**Gatekeeper 配置**：

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
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }
```

### 1.3 影响范围

- **受影响策略**：1 条（policy.rego）
- **受影响服务**：所有依赖该策略的服务
- **业务影响**：应用部署被拒绝，影响生产环境
- **用户影响**：所有依赖该策略的用户

---

## 2 故障排查过程

### 2.1 初步诊断

**步骤 1：检查 OPA 日志**：

```bash
# 检查 OPA 日志
kubectl logs -n gatekeeper-system gatekeeper-controller-manager-xxx --tail=50

# 输出
time="2025-11-13T18:00:15Z" level=error msg="Error evaluating policy: rego_parse_error"
time="2025-11-13T18:00:15Z" level=error msg="Policy evaluation failed: invalid syntax"
```

**步骤 2：检查策略文件**：

```bash
# 检查策略文件
kubectl get configmap -n gatekeeper-system gatekeeper-policy -o yaml

# 输出
apiVersion: v1
kind: ConfigMap
data:
  policy.rego: |
    package policy
    default allow = false
    allow {
        input.user.role == "admin"
        input.resource.type == "pod"
        input.action == "create"
        # 语法错误
        input.resource.labels.env == "production"
    }
```

**步骤 3：测试策略语法**：

```bash
# 使用 opa test 测试策略
opa test policy.rego

# 输出
FAIL: policy.rego:10:5: rego_parse_error: unexpected token: EOF
```

**初步结论**：

- OPA 策略评估失败
- 策略文件存在语法错误
- 需要修复策略语法

### 2.2 深入排查

**步骤 4：检查策略语法**：

```bash
# 使用 opa fmt 格式化策略
opa fmt policy.rego

# 输出
policy.rego:10:5: rego_parse_error: unexpected token: EOF
```

**步骤 5：检查策略结构**：

```bash
# 检查策略结构
opa parse policy.rego

# 输出
1 error occurred: policy.rego:10:5: rego_parse_error: unexpected token: EOF
```

**步骤 6：检查策略依赖**：

```bash
# 检查策略依赖
opa deps policy.rego

# 输出
（无依赖问题）
```

**步骤 7：检查策略测试**：

```bash
# 运行策略测试
opa test policy.rego

# 输出
FAIL: policy.rego:10:5: rego_parse_error: unexpected token: EOF
```

**步骤 8：检查 Gatekeeper 约束**：

```bash
# 检查 Gatekeeper 约束
kubectl get constraints -A

# 输出
NAME                    AGE
k8srequiredlabels-xxx   5d
```

**深入排查结论**：

- 策略文件存在语法错误
- 缺少闭合括号或语法不正确
- 需要修复策略语法

### 2.3 根因分析

**根因 1：策略语法错误**：

- 策略文件存在语法错误
- 缺少闭合括号或语法不正确
- OPA 无法解析策略

**根因 2：策略结构错误**：

- 策略结构可能不正确
- 规则定义可能有问题
- 导致策略评估失败

**根因 3：策略依赖问题**：

- 策略可能依赖不存在的模块
- 导入路径可能错误
- 导致策略评估失败

**根本原因**：

**策略语法错误**：策略文件存在语法错误（缺少闭合括号），导致 OPA 无法解析策略，从而策略评估失败。

---

## 3 解决方案

### 3.1 临时解决方案

**方案 1：禁用问题策略**：

```bash
# 临时禁用问题策略
kubectl delete constraint k8srequiredlabels-xxx -n default
```

**方案 2：回滚到之前版本**：

```bash
# 回滚策略到之前版本
kubectl apply -f policy-previous-version.yaml
```

**方案 3：使用默认策略**：

```yaml
# 使用默认策略
apiVersion: v1
kind: ConfigMap
metadata:
  name: gatekeeper-policy
  namespace: gatekeeper-system
data:
  policy.rego: |
    package policy
    default allow = true
```

**临时方案效果**：

- ✅ 可以快速恢复服务
- ⚠️ 但未解决根本问题
- ⚠️ 可能影响安全性（禁用策略）

### 3.2 永久解决方案

**方案 1：修复策略语法**：

```rego
# 修复后的策略
package policy

default allow = false

allow {
    input.user.role == "admin"
    input.resource.type == "pod"
    input.action == "create"
    input.resource.labels.env == "production"  # 修复语法错误
}
```

**方案 2：验证策略语法**：

```bash
# 使用 opa fmt 格式化策略
opa fmt policy.rego

# 使用 opa test 测试策略
opa test policy.rego

# 使用 opa eval 评估策略
opa eval -d policy.rego -i input.json "data.policy.allow"
```

**方案 3：使用策略模板**：

```yaml
# 使用策略模板
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
          required := input.parameters.labels
          provided := input.review.object.metadata.labels
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }
```

**方案 4：配置策略验证**：

```yaml
# 配置策略验证
apiVersion: v1
kind: ConfigMap
metadata:
  name: gatekeeper-policy-validator
data:
  validate.sh: |
    #!/bin/bash
    opa fmt policy.rego
    opa test policy.rego
    opa eval -d policy.rego -i input.json "data.policy.allow"
```

**永久方案效果**：

- ✅ 解决根本问题
- ✅ 防止问题再次发生
- ✅ 提高系统稳定性

### 3.3 预防措施

**措施 1：策略语法检查**：

```bash
# 配置策略语法检查
opa fmt policy.rego
opa test policy.rego
```

**措施 2：策略版本控制**：

```bash
# 使用 Git 管理策略版本
git add policy.rego
git commit -m "Update policy"
git tag v1.0.0
```

**措施 3：策略测试自动化**：

```yaml
# 配置策略测试 CI/CD
apiVersion: v1
kind: ConfigMap
metadata:
  name: policy-test-pipeline
data:
  test.sh: |
    #!/bin/bash
    opa fmt policy.rego
    opa test policy.rego
    opa eval -d policy.rego -i input.json "data.policy.allow"
```

**措施 4：策略审查流程**：

```bash
# 配置策略审查流程
1. 策略编写
2. 策略语法检查
3. 策略测试
4. 策略审查
5. 策略部署
```

---

## 4 验证与恢复

### 4.1 验证步骤

**步骤 1：验证策略语法**：

```bash
# 检查策略语法
opa fmt policy.rego

# 预期输出
（无错误）
```

**步骤 2：验证策略测试**：

```bash
# 运行策略测试
opa test policy.rego

# 预期输出
PASS: 5/5 tests passed
```

**步骤 3：验证策略评估**：

```bash
# 测试策略评估
opa eval -d policy.rego -i input.json "data.policy.allow"

# 预期输出
{
  "result": [
    {
      "expressions": [
        {
          "value": true,
          "text": "data.policy.allow"
        }
      ]
    }
  ]
}
```

**步骤 4：验证应用部署**：

```bash
# 测试应用部署
kubectl apply -f app-deployment.yaml

# 预期输出
deployment.apps/app-deployment created
```

### 4.2 恢复确认

**恢复指标**：

- ✅ 策略语法：正确
- ✅ 策略测试：通过
- ✅ 策略评估：成功
- ✅ 应用部署：成功

**恢复时间**：

- **故障发现**：18:00:00
- **开始排查**：18:00:05
- **根因确认**：18:05:00
- **问题解决**：18:10:00
- **服务恢复**：18:10:05
- **总耗时**：10 分钟

---

## 5 经验总结

### 5.1 关键发现

1. **策略语法错误导致评估失败**：
   - 策略语法错误会导致 OPA 无法解析策略
   - 需要仔细检查策略语法

2. **策略测试重要**：
   - 策略测试可以发现语法错误
   - 需要定期运行策略测试

3. **策略版本控制重要**：
   - 策略版本控制可以快速回滚
   - 需要使用版本控制系统管理策略

### 5.2 最佳实践

1. **策略语法检查**：
   - 使用 opa fmt 格式化策略
   - 使用 opa test 测试策略

2. **策略版本控制**：
   - 使用 Git 管理策略版本
   - 定期备份策略文件

3. **策略测试自动化**：
   - 配置策略测试 CI/CD
   - 自动发现策略问题

4. **策略审查流程**：
   - 建立策略审查流程
   - 确保策略质量

### 5.3 相关文档

- [`../../TECHNICAL/02-runtime-policy/opa/opa.md`](../../TECHNICAL/02-runtime-policy/opa/opa.md) - OPA 文档
- [`../../TECHNICAL/02-runtime-policy/gatekeeper/gatekeeper.md`](../../TECHNICAL/02-runtime-policy/gatekeeper/gatekeeper.md) - Gatekeeper 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

## 6 相关文档

- [`../README.md`](README.md) - 故障排查案例集目录
- [`../../TECHNICAL/02-runtime-policy/opa/opa.md`](../../TECHNICAL/02-runtime-policy/opa/opa.md) - OPA 文档
- [`../troubleshooting.md`](../troubleshooting.md) - 故障排查指南

---

**最后更新**：2025-11-13
**维护者**：项目团队
**版本**：v1.0
