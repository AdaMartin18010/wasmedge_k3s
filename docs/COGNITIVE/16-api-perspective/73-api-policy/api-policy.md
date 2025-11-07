# API 策略规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 策略架构](#11-策略架构)
- [2. 策略类型](#2-策略类型)
  - [2.1 安全策略](#21-安全策略)
  - [2.2 性能策略](#22-性能策略)
  - [2.3 访问策略](#23-访问策略)
- [3. 策略定义](#3-策略定义)
  - [3.1 策略 DSL](#31-策略-dsl)
  - [3.2 策略规则](#32-策略规则)
- [4. 策略执行](#4-策略执行)
  - [4.1 策略引擎](#41-策略引擎)
  - [4.2 策略评估](#42-策略评估)
- [5. 策略管理](#5-策略管理)
  - [5.1 策略版本](#51-策略版本)
  - [5.2 策略部署](#52-策略部署)
- [6. 策略监控](#6-策略监控)
  - [6.1 策略指标](#61-策略指标)
  - [6.2 策略告警](#62-策略告警)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 策略规范定义了 API 在策略场景下的设计和实现，从策略类型到策略定义，从策略执行到策略管理。

### 1.1 策略架构

```text
策略定义（Policy Definition）
  ↓
策略引擎（Policy Engine）
  ↓
策略评估（Policy Evaluation）
  ↓
策略执行（Policy Enforcement）
```

---

## 2. 策略类型

### 2.1 安全策略

**安全策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: SecurityPolicy
metadata:
  name: payment-api-security-policy
spec:
  rules:
    - name: "require_authentication"
      type: "authentication"
      action: "deny"
      condition: "request.auth == null"
    - name: "rate_limit"
      type: "rate_limit"
      action: "throttle"
      condition: "request.rate > 100"
      limit: 100
      window: "1m"
    - name: "ip_whitelist"
      type: "ip_filter"
      action: "allow"
      condition: "request.ip in whitelist"
```

**安全策略实现**：

```go
package main

type SecurityPolicy struct {
    Rules []SecurityRule
}

type SecurityRule struct {
    Name      string
    Type      string
    Action    string
    Condition func(*Request) bool
}

func (p *SecurityPolicy) Evaluate(req *Request) (bool, string) {
    for _, rule := range p.Rules {
        if rule.Condition(req) {
            if rule.Action == "deny" {
                return false, rule.Name
            }
        }
    }
    return true, ""
}
```

### 2.2 性能策略

**性能策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: PerformancePolicy
metadata:
  name: payment-api-performance-policy
spec:
  rules:
    - name: "max_response_time"
      type: "latency"
      action: "reject"
      threshold: 1000
      unit: "ms"
    - name: "max_payload_size"
      type: "payload"
      action: "reject"
      threshold: 10485760
      unit: "bytes"
    - name: "cache_ttl"
      type: "caching"
      action: "cache"
      ttl: 300
      unit: "seconds"
```

### 2.3 访问策略

**访问策略配置**：

```yaml
apiVersion: api.example.com/v1
kind: AccessPolicy
metadata:
  name: payment-api-access-policy
spec:
  rules:
    - name: "time_based_access"
      type: "time"
      action: "allow"
      schedule:
        - day: "monday-friday"
          time: "09:00-18:00"
    - name: "role_based_access"
      type: "role"
      action: "allow"
      roles: ["admin", "user"]
    - name: "quota_based_access"
      type: "quota"
      action: "throttle"
      quota: 1000
      period: "1h"
```

---

## 3. 策略定义

### 3.1 策略 DSL

**策略 DSL 定义**：

```yaml
apiVersion: api.example.com/v1
kind: PolicyDefinition
metadata:
  name: payment-api-policy-dsl
spec:
  language: "rego"
  policy: |
    package api.policy

    default allow = false

    allow {
        input.method == "GET"
        input.path == ["api", "v1", "payments"]
        input.user.role == "viewer"
    }

    allow {
        input.method == "POST"
        input.path == ["api", "v1", "payments"]
        input.user.role == "user"
        input.body.amount <= input.user.max_amount
    }

    allow {
        input.method == "DELETE"
        input.path == ["api", "v1", "payments"]
        input.user.role == "admin"
    }
```

### 3.2 策略规则

**策略规则实现**：

```go
package main

type PolicyRule struct {
    ID          string
    Name        string
    Type        string
    Condition   string
    Action      string
    Priority    int
    Enabled     bool
}

type PolicyRuleEngine struct {
    rules []PolicyRule
}

func (e *PolicyRuleEngine) Evaluate(req *Request) (bool, string) {
    // 按优先级排序
    sortedRules := e.sortRulesByPriority()

    for _, rule := range sortedRules {
        if !rule.Enabled {
            continue
        }

        if e.evaluateCondition(rule.Condition, req) {
            return e.executeAction(rule.Action, req), rule.Name
        }
    }

    return true, ""
}

func (e *PolicyRuleEngine) evaluateCondition(condition string, req *Request) bool {
    // 解析并评估条件
    // 可以使用表达式引擎如 expr 或 cel
    return true
}
```

---

## 4. 策略执行

### 4.1 策略引擎

**策略引擎实现**：

```go
package main

import (
    "github.com/open-policy-agent/opa/rego"
)

type PolicyEngine struct {
    policies map[string]*rego.PreparedEvalQuery
}

func NewPolicyEngine() *PolicyEngine {
    return &PolicyEngine{
        policies: make(map[string]*rego.PreparedEvalQuery),
    }
}

func (e *PolicyEngine) LoadPolicy(name string, policy string) error {
    query, err := rego.New(
        rego.Query("data.api.policy.allow"),
        rego.Module(name, policy),
    ).PrepareForEval(context.Background())

    if err != nil {
        return err
    }

    e.policies[name] = &query
    return nil
}

func (e *PolicyEngine) Evaluate(name string, input interface{}) (bool, error) {
    query := e.policies[name]
    if query == nil {
        return false, fmt.Errorf("policy not found: %s", name)
    }

    results, err := query.Eval(context.Background(), rego.EvalInput(input))
    if err != nil {
        return false, err
    }

    if len(results) == 0 {
        return false, nil
    }

    return results[0].Expressions[0].Value.(bool), nil
}
```

### 4.2 策略评估

**策略评估实现**：

```go
package main

type PolicyEvaluator struct {
    engine *PolicyEngine
}

func (e *PolicyEvaluator) EvaluateRequest(req *Request) (*PolicyResult, error) {
    input := map[string]interface{}{
        "method": req.Method,
        "path":   req.Path,
        "user": map[string]interface{}{
            "id":   req.UserID,
            "role": req.Role,
        },
        "body": req.Body,
    }

    allowed, err := e.engine.Evaluate("payment-api-policy", input)
    if err != nil {
        return nil, err
    }

    return &PolicyResult{
        Allowed: allowed,
        Reason:  getReason(allowed),
    }, nil
}
```

---

## 5. 策略管理

### 5.1 策略版本

**策略版本管理**：

```yaml
apiVersion: api.example.com/v1
kind: PolicyVersion
metadata:
  name: payment-api-policy-v2
spec:
  policyID: "payment-api-policy"
  version: "2.0"
  previousVersion: "1.0"
  changes:
    - type: "added"
      description: "Added IP whitelist rule"
    - type: "modified"
      description: "Updated rate limit threshold"
  rollout:
    strategy: "gradual"
    percentage: 10
```

### 5.2 策略部署

**策略部署配置**：

```yaml
apiVersion: api.example.com/v1
kind: PolicyDeployment
metadata:
  name: payment-api-policy-deployment
spec:
  policyID: "payment-api-policy"
  version: "2.0"
  targets:
    - endpoint: "payment-service"
      weight: 100
  rollout:
    strategy: "canary"
    steps:
      - step: 1
        percentage: 10
        duration: "5m"
      - step: 2
        percentage: 50
        duration: "10m"
      - step: 3
        percentage: 100
        duration: "0m"
```

---

## 6. 策略监控

### 6.1 策略指标

**策略指标配置**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: policy-metrics
spec:
  groups:
    - name: policy_metrics
      rules:
        - record: policy:evaluations_total
          expr: |
            sum(rate(policy_evaluations_total[5m])) by (policy_id, result)
        - record: policy:evaluation_duration_seconds
          expr: |
            histogram_quantile(0.95, sum(rate(policy_evaluation_duration_seconds_bucket[5m])) by (policy_id, le))
```

### 6.2 策略告警

**策略告警规则**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: policy-alerts
spec:
  groups:
    - name: policy_alerts
      rules:
        - alert: HighPolicyDenialRate
          expr: |
            rate(policy_evaluations_total{result="denied"}[5m]) /
            rate(policy_evaluations_total[5m]) > 0.1
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "High policy denial rate"
            description: "Policy denial rate is {{ $value | humanizePercentage }}"
```

---

## 7. 相关文档

- **[API 治理规范](../13-api-governance/api-governance.md)** - API 治理
- **[API 安全规范](../11-api-security/api-security.md)** - API 安全
- **[API 授权规范](../62-api-authorization/api-authorization.md)** - API 授权
- **[最佳实践](../08-best-practices/best-practices.md)** - 策略最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队

