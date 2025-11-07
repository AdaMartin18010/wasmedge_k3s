# API 安全测试规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 安全测试架构](#11-安全测试架构)
- [2. 安全测试类型](#2-安全测试类型)
  - [2.1 认证测试](#21-认证测试)
  - [2.2 授权测试](#22-授权测试)
  - [2.3 输入验证测试](#23-输入验证测试)
  - [2.4 注入攻击测试](#24-注入攻击测试)
- [3. OWASP Top 10](#3-owasp-top-10)
  - [3.1 API 安全风险](#31-api-安全风险)
  - [3.2 安全测试用例](#32-安全测试用例)
- [4. 安全扫描工具](#4-安全扫描工具)
  - [4.1 OWASP ZAP](#41-owasp-zap)
  - [4.2 Burp Suite](#42-burp-suite)
  - [4.3 SQLMap](#43-sqlmap)
- [5. 安全测试流程](#5-安全测试流程)
  - [5.1 安全测试计划](#51-安全测试计划)
  - [5.2 安全测试执行](#52-安全测试执行)
  - [5.3 安全测试报告](#53-安全测试报告)
- [6. 安全漏洞修复](#6-安全漏洞修复)
  - [6.1 漏洞分类](#61-漏洞分类)
  - [6.2 修复优先级](#62-修复优先级)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 安全测试规范定义了 API 在安全测试场景下的设计和实现，从安全测试类型到 OWASP
Top 10，从安全扫描工具到安全漏洞修复。

### 1.1 安全测试架构

```text
安全测试工具（Security Testing Tool）
  ↓
API 服务（API Service）
  ↓
安全漏洞检测（Vulnerability Detection）
  ↓
安全测试报告（Security Test Report）
```

---

## 2. 安全测试类型

### 2.1 认证测试

**认证测试用例**：

```yaml
apiVersion: api.example.com/v1
kind: SecurityTest
metadata:
  name: authentication-test
spec:
  type: authentication
  testCases:
    - name: missing_token
      request:
        method: POST
        path: /api/v1/payments
        headers: {}
      expectedStatus: 401
    - name: invalid_token
      request:
        method: POST
        path: /api/v1/payments
        headers:
          Authorization: "Bearer invalid_token"
      expectedStatus: 401
    - name: expired_token
      request:
        method: POST
        path: /api/v1/payments
        headers:
          Authorization: "Bearer expired_token"
      expectedStatus: 401
```

### 2.2 授权测试

**授权测试用例**：

```yaml
apiVersion: api.example.com/v1
kind: SecurityTest
metadata:
  name: authorization-test
spec:
  type: authorization
  testCases:
    - name: unauthorized_access
      request:
        method: DELETE
        path: /api/v1/payments/pay_123
        headers:
          Authorization: "Bearer user_token"
      expectedStatus: 403
    - name: cross_tenant_access
      request:
        method: GET
        path: /api/v1/payments/pay_456
        headers:
          Authorization: "Bearer tenant_a_token"
      expectedStatus: 403
```

### 2.3 输入验证测试

**输入验证测试用例**：

```yaml
apiVersion: api.example.com/v1
kind: SecurityTest
metadata:
  name: input-validation-test
spec:
  type: input_validation
  testCases:
    - name: sql_injection
      request:
        method: POST
        path: /api/v1/payments
        body:
          order_id: "'; DROP TABLE payments; --"
          amount: 10000
      expectedStatus: 400
    - name: xss_attack
      request:
        method: POST
        path: /api/v1/payments
        body:
          order_id: "<script>alert('XSS')</script>"
          amount: 10000
      expectedStatus: 400
    - name: command_injection
      request:
        method: POST
        path: /api/v1/payments
        body:
          order_id: "order_123; rm -rf /"
          amount: 10000
      expectedStatus: 400
```

### 2.4 注入攻击测试

**注入攻击测试**：

```yaml
apiVersion: api.example.com/v1
kind: SecurityTest
metadata:
  name: injection-test
spec:
  type: injection
  testCases:
    - name: sql_injection
      payloads:
        - "'; DROP TABLE payments; --"
        - "' OR '1'='1"
        - "1' UNION SELECT NULL--"
    - name: nosql_injection
      payloads:
        - '{"$ne": null}'
        - '{"$gt": ""}'
        - '{"$where": "this.amount == this.order_id"}'
    - name: command_injection
      payloads:
        - "; rm -rf /"
        - "| cat /etc/passwd"
        - "&& whoami"
```

---

## 3. OWASP Top 10

### 3.1 API 安全风险

**OWASP API Top 10**：

```yaml
apiVersion: api.example.com/v1
kind: OWASPAPISecurity
metadata:
  name: owasp-api-top10
spec:
  risks:
    - id: API1
      name: "Broken Object Level Authorization"
      description:
        "APIs tend to expose endpoints that handle object identifiers"
      severity: HIGH
    - id: API2
      name: "Broken Authentication"
      description: "Authentication mechanisms are often implemented incorrectly"
      severity: HIGH
    - id: API3
      name: "Excessive Data Exposure"
      description: "APIs tend to expose more data than necessary"
      severity: MEDIUM
    - id: API4
      name: "Lack of Resources & Rate Limiting"
      description:
        "APIs often do not impose any restrictions on the size of resources"
      severity: MEDIUM
    - id: API5
      name: "Broken Function Level Authorization"
      description: "Complex access control policies with different hierarchies"
      severity: HIGH
    - id: API6
      name: "Mass Assignment"
      description: "Binding client provided data to data models"
      severity: MEDIUM
    - id: API7
      name: "Security Misconfiguration"
      description:
        "Security misconfiguration is commonly a result of unsecure default
        configurations"
      severity: MEDIUM
    - id: API8
      name: "Injection"
      description: "Injection flaws are common in API code"
      severity: HIGH
    - id: API9
      name: "Improper Assets Management"
      description:
        "APIs tend to expose more endpoints than traditional web applications"
      severity: MEDIUM
    - id: API10
      name: "Insufficient Logging & Monitoring"
      description: "Insufficient logging and monitoring"
      severity: LOW
```

### 3.2 安全测试用例

**OWASP 测试用例**：

```yaml
apiVersion: api.example.com/v1
kind: OWASPTestCases
metadata:
  name: owasp-test-cases
spec:
  testCases:
    - risk: API1
      name: "Test object level authorization"
      test:
        - request:
            method: GET
            path: /api/v1/payments/{payment_id}
            headers:
              Authorization: "Bearer user_a_token"
          payment_id: "pay_b_payment"
          expectedStatus: 403
    - risk: API2
      name: "Test broken authentication"
      test:
        - request:
            method: POST
            path: /api/v1/payments
            headers: {}
          expectedStatus: 401
    - risk: API8
      name: "Test injection attacks"
      test:
        - payload: "'; DROP TABLE payments; --"
          expectedStatus: 400
```

---

## 4. 安全扫描工具

### 4.1 OWASP ZAP

**OWASP ZAP 配置**：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: zap-security-scan
spec:
  template:
    spec:
      containers:
        - name: zap
          image: owasp/zap2docker-stable:latest
          command:
            - zap-baseline.py
            - -t
            - http://payment-service:8080
            - -J
            - zap-report.json
          volumeMounts:
            - name: zap-results
              mountPath: /zap/wrk
      volumes:
        - name: zap-results
          emptyDir: {}
```

### 4.2 Burp Suite

**Burp Suite 配置**：

```yaml
apiVersion: api.example.com/v1
kind: BurpSuiteScan
metadata:
  name: burp-suite-scan
spec:
  target: "http://payment-service:8080"
  scope:
    include:
      - "/api/v1/payments"
    exclude:
      - "/api/v1/health"
  scanTypes:
    - active
    - passive
  reportFormat: html
```

### 4.3 SQLMap

**SQLMap 配置**：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: sqlmap-scan
spec:
  template:
    spec:
      containers:
        - name: sqlmap
          image: paoloo/sqlmap:latest
          command:
            - sqlmap
            - -u
            - "http://payment-service:8080/api/v1/payments?id=1"
            - --batch
            - --level=3
            - --risk=2
```

---

## 5. 安全测试流程

### 5.1 安全测试计划

**安全测试计划**：

```yaml
apiVersion: api.example.com/v1
kind: SecurityTestPlan
metadata:
  name: payment-api-security-test-plan
spec:
  phases:
    - name: planning
      duration: "1w"
      tasks:
        - "Define security requirements"
        - "Identify test scope"
        - "Select testing tools"
    - name: execution
      duration: "2w"
      tasks:
        - "Execute automated scans"
        - "Perform manual testing"
        - "Document vulnerabilities"
    - name: reporting
      duration: "3d"
      tasks:
        - "Generate security report"
        - "Prioritize vulnerabilities"
        - "Create remediation plan"
```

### 5.2 安全测试执行

**安全测试执行**：

```yaml
apiVersion: api.example.com/v1
kind: SecurityTestExecution
metadata:
  name: payment-api-security-test-execution
spec:
  schedule: "weekly"
  tools:
    - name: OWASP ZAP
      enabled: true
      schedule: "daily"
    - name: Burp Suite
      enabled: true
      schedule: "weekly"
    - name: SQLMap
      enabled: true
      schedule: "monthly"
```

### 5.3 安全测试报告

**安全测试报告格式**：

```yaml
apiVersion: api.example.com/v1
kind: SecurityTestReport
metadata:
  name: payment-api-security-report
spec:
  format: sarif
  sections:
    - summary
    - vulnerabilities
    - recommendations
    - remediation
  severityLevels:
    - CRITICAL
    - HIGH
    - MEDIUM
    - LOW
```

---

## 6. 安全漏洞修复

### 6.1 漏洞分类

**漏洞分类**：

```yaml
apiVersion: api.example.com/v1
kind: VulnerabilityClassification
metadata:
  name: vulnerability-classification
spec:
  categories:
    - name: authentication
      examples:
        - "Weak password policy"
        - "Session fixation"
        - "Token leakage"
    - name: authorization
      examples:
        - "Privilege escalation"
        - "Insecure direct object reference"
        - "Missing access control"
    - name: injection
      examples:
        - "SQL injection"
        - "NoSQL injection"
        - "Command injection"
    - name: configuration
      examples:
        - "Default credentials"
        - "Exposed sensitive data"
        - "Missing security headers"
```

### 6.2 修复优先级

**修复优先级**：

```yaml
apiVersion: api.example.com/v1
kind: VulnerabilityRemediation
metadata:
  name: vulnerability-remediation
spec:
  priority:
    CRITICAL:
      sla: "24h"
      examples:
        - "Remote code execution"
        - "SQL injection"
    HIGH:
      sla: "7d"
      examples:
        - "Authentication bypass"
        - "Privilege escalation"
    MEDIUM:
      sla: "30d"
      examples:
        - "Information disclosure"
        - "Weak encryption"
    LOW:
      sla: "90d"
      examples:
        - "Missing security headers"
        - "Verbose error messages"
```

---

## 7. 相关文档

- **[API 安全规范](../11-api-security/api-security.md)** - API 安全
- **[API 安全审计](../28-api-security-audit/api-security-audit.md)** - 安全审计
- **[API 测试规范](../15-api-testing/api-testing.md)** - 安全测试
- **[最佳实践](../08-best-practices/best-practices.md)** - 安全测试最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
