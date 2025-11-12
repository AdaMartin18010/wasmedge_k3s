# OPA 体系结构：范畴论视角

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 核心思想](#11-核心思想)
- [2 OPA 体系结构](#2-opa-体系结构)
  - [2.1 层次结构](#21-层次结构)
  - [2.2 核心组件](#22-核心组件)
- [3 PDP（Policy Decision Point）](#3-pdppolicy-decision-point)
  - [3.1 PDP 定义](#31-pdp-定义)
  - [3.2 PDP 功能](#32-pdp-功能)
  - [3.3 PDP 接口](#33-pdp-接口)
- [4 PEP（Policy Enforcement Point）](#4-peppolicy-enforcement-point)
  - [4.1 PEP 定义](#41-pep-定义)
  - [4.2 PEP 类型](#42-pep-类型)
  - [4.3 PEP 流程](#43-pep-流程)
- [5 OCP（OPA Control Plane）](#5-ocpopa-control-plane)
  - [5.1 OCP 定义](#51-ocp-定义)
  - [5.2 OCP 功能](#52-ocp-功能)
  - [5.3 OCP API](#53-ocp-api)
- [6 Bundle（策略包）](#6-bundle策略包)
  - [6.1 Bundle 定义](#61-bundle-定义)
  - [6.2 Bundle 结构](#62-bundle-结构)
  - [6.3 Bundle 操作](#63-bundle-操作)
- [7 Decision Log（决策日志）](#7-decision-log决策日志)
  - [7.1 Decision Log 定义](#71-decision-log-定义)
  - [7.2 Decision Log 格式](#72-decision-log-格式)
  - [7.3 Decision Log 集成](#73-decision-log-集成)
- [8 Discovery（发现）](#8-discovery发现)
  - [8.1 Discovery 定义](#81-discovery-定义)
  - [8.2 Discovery 配置](#82-discovery-配置)
- [9 OPA 在层次模型中的定位](#9-opa-在层次模型中的定位)
  - [9.1 各层中的 OPA 角色](#91-各层中的-opa-角色)
- [10 形式化定义](#10-形式化定义)
  - [10.1 OPA 体系结构定义](#101-opa-体系结构定义)
  - [10.2 决策流程定义](#102-决策流程定义)
  - [10.3 Bundle 分发定义](#103-bundle-分发定义)
- [11 总结](#11-总结)

---

## 1 概述

本文档从**范畴论视角**阐述 **OPA 体系结构**，包括 PDP、PEP、OCP 等核心组件。

### 1.1 核心思想

> **OPA 体系结构是一个完整的策略治理系统，通过 PDP、PEP、OCP 等组件实现策略的统
> 一管理、版本化、自动分发和决策审计**

## 2 OPA 体系结构

### 2.1 层次结构

```text
            ┌─────────────────────┐
            │  OPA Control Plane  │
            │ (Centralised)       │
            └─────────────────────┘
                     ▲
             ┌──────────────────┐
             │   Policy Bundles │
             └──────────────────┘
                     ▲
   ┌───────────────────────────────────────┐
   │    OPA (PDP) + PEPs (policy‑agents)   │
   │  (one per service or sidecar)         │
   └───────────────────────────────────────┘
                     ▲
          ┌──────────────────────┐
          │Application/Service   │
          └──────────────────────┘
```

### 2.2 核心组件

| 组件                        | 说明                                                                            | 典型接口                                          |
| --------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------- |
| **PDP**                     | Rego 评估引擎，执行策略、返回 allow/deny                                        | REST / gRPC `decision`                            |
| **PEP**                     | 服务、sidecar 或 Admission Controller 的"前置层"，把请求上下文 `input` 送给 PDP | `opa/decision` API                                |
| **OCP** (OPA Control Plane) | 集中管理 bundle、分发、决策日志、动态配置                                       | REST/HTTP API (`/bundles`, `/logs`, `/discovery`) |
| **Bundle**                  | 一个 Rego policy 包含一组 policy、数据与元数据，Git 版本化                      | `opa bundle create` / `opa bundle push`           |
| **Decision Log**            | 记录每一次 PDP 评估结果（who, what, why)                                        | Log/Prometheus, e.g., `opa.log`                   |
| **Discovery**               | 发现并配置远程 OPA 代理（可跨集群）                                             | `opa discovery` API                               |

## 3 PDP（Policy Decision Point）

### 3.1 PDP 定义

**PDP** 是策略决策点，负责执行策略并返回决策结果。

### 3.2 PDP 功能

- **策略评估**：执行 Rego 策略
- **决策返回**：返回 allow/deny 决策
- **变量绑定**：返回策略匹配的变量绑定

### 3.3 PDP 接口

**REST API**：

```bash
# 决策请求
curl -X POST http://opa:8181/v1/data/mesh/authz/allow \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "attributes": {
        "source": {
          "principal": "spiffe://A/ns/default/sa/frontend"
        },
        "destination": {
          "principal": "spiffe://B/ns/default/sa/order-service"
        },
        "request": {
          "http": {
            "method": "GET",
            "path": "/orders"
          }
        }
      }
    }
  }'
```

**响应**：

```json
{
  "result": true,
  "decision_id": "abc123",
  "metrics": {
    "timer_rego_query_eval_ns": 1234
  }
}
```

## 4 PEP（Policy Enforcement Point）

### 4.1 PEP 定义

**PEP** 是策略执行点，负责将请求上下文传递给 PDP 并执行决策。

### 4.2 PEP 类型

| PEP 类型                 | 说明                            | 典型实现            |
| ------------------------ | ------------------------------- | ------------------- |
| **Service Sidecar**      | 服务侧车中的 PEP                | Istio Envoy         |
| **Admission Controller** | Kubernetes Admission Controller | OPA Gatekeeper      |
| **API Gateway**          | API 网关中的 PEP                | Kong, Istio Gateway |
| **Application**          | 应用内的 PEP                    | OPA SDK             |

### 4.3 PEP 流程

```text
请求
  ↓
PEP 收集上下文
  ↓
PEP 调用 PDP
  ↓
PDP 返回决策
  ↓
PEP 执行决策（allow/deny）
```

## 5 OCP（OPA Control Plane）

### 5.1 OCP 定义

**OCP** 是 OPA 控制平面，负责集中管理策略、分发和决策日志。

### 5.2 OCP 功能

- **Bundle 管理**：管理策略 Bundle
- **Bundle 分发**：将 Bundle 分发到各个 OPA 代理
- **决策日志**：收集和存储决策日志
- **动态配置**：动态配置 OPA 代理

### 5.3 OCP API

**Bundle API**：

```bash
# 获取 Bundle
GET /bundles/bundle-name

# 推送 Bundle
POST /bundles/bundle-name
```

**Decision Log API**：

```bash
# 获取决策日志
GET /logs

# 推送决策日志
POST /logs
```

**Discovery API**：

```bash
# 发现 OPA 代理
GET /discovery
```

## 6 Bundle（策略包）

### 6.1 Bundle 定义

**Bundle** 是一个 Rego policy 包含一组 policy、数据与元数据，Git 版本化。

### 6.2 Bundle 结构

```text
bundle/
├── policies/
│   ├── authz.rego
│   ├── rate-limit.rego
│   └── network-policy.rego
├── data/
│   └── config.json
└── manifest.json
```

### 6.3 Bundle 操作

**创建 Bundle**：

```bash
opa bundle create -o authz.bundle authz.rego
```

**推送 Bundle**：

```bash
opa bundle push authz.bundle
```

**拉取 Bundle**：

```bash
opa bundle pull authz.bundle
```

## 7 Decision Log（决策日志）

### 7.1 Decision Log 定义

**Decision Log** 记录每一次 PDP 评估结果（who, what, why）。

### 7.2 Decision Log 格式

```json
{
  "decision_id": "abc123",
  "timestamp": "2025-11-04T10:00:00Z",
  "input": {
    "attributes": {
      "source": {
        "principal": "spiffe://A/ns/default/sa/frontend"
      },
      "destination": {
        "principal": "spiffe://B/ns/default/sa/order-service"
      }
    }
  },
  "result": true,
  "metrics": {
    "timer_rego_query_eval_ns": 1234
  }
}
```

### 7.3 Decision Log 集成

**Prometheus 集成**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: opa-config
data:
  config.yaml: |
    decision_logs:
      service: prometheus
      reporting:
        max_decisions_per_second: 1000
```

## 8 Discovery（发现）

### 8.1 Discovery 定义

**Discovery** 发现并配置远程 OPA 代理（可跨集群）。

### 8.2 Discovery 配置

```json
{
  "discovery": {
    "name": "my-discovery",
    "service": "http://opa-control-plane:8181",
    "resource": "/v1/discovery"
  }
}
```

## 9 OPA 在层次模型中的定位

### 9.1 各层中的 OPA 角色

| 层级                   | OPA 角色                                         | 典型实现方式                                             | 关键接口             |
| ---------------------- | ------------------------------------------------ | -------------------------------------------------------- | -------------------- |
| **底层 – 虚拟化/硬件** | - 可信根（SGX/TLS） <br> - 策略分配 (谁能跑 VM)  | `KVM → Spiffe`                                           | `opa‑bundle‑vm`      |
| **容器/运行时层**      | - 进程权限、镜像签名 <br> - 资源限制（CPU/内存） | `k8s‑RBAC` + `OPA Gatekeeper`                            | `opa‑bundle‑runtime` |
| **沙盒层**             | - 系统调用过滤 <br> - 细粒度访问控制             | `seccomp‑bpf → OPA`                                      | `opa‑sandbox‑policy` |
| **Mesh/NSM 层**        | - 路由/限流、mTLS、请求/响应验证                 | `Istio/Linkerd sidecar → OPA` <br> `NSM vWire → OPA`     | `opa‑mesh‑policy`    |
| **治理 & 安全层**      | - 统一决策、日志、监控                           | `OPA Control Plane` <br> `Gatekeeper`                    | `opa‑bundle‑global`  |
| **动态运维层**         | - 监控/告警触发策略                              | `Prometheus/Tempo → OPA` <br> `Argo CD` 触发 bundle 更新 | `opa‑decision‑logs`  |

## 10 形式化定义

### 10.1 OPA 体系结构定义

```text
OPA = ⟨PDP, PEP, OCP, Bundle, DecisionLog, Discovery⟩
其中：
- PDP: 策略决策点
- PEP: 策略执行点集合
- OCP: OPA 控制平面
- Bundle: 策略包集合
- DecisionLog: 决策日志
- Discovery: 发现服务
```

### 10.2 决策流程定义

```text
决策流程 D = PEP(input) → PDP(input) → Decision
其中：
- input: 请求上下文
- Decision: {allow, deny, variables}
```

### 10.3 Bundle 分发定义

```text
Bundle 分发 B = OCP(bundle) → PEP₁, PEP₂, ..., PEPₙ
其中：
- bundle: 策略包
- PEPᵢ: 策略执行点
```

## 11 总结

通过**OPA 体系结构**，我们可以：

1. **统一管理**：通过 OCP 统一管理策略
2. **版本化**：通过 Bundle 实现策略版本化
3. **自动分发**：通过 OCP 自动分发策略到各个 PEP
4. **决策审计**：通过 Decision Log 实现决策审计
5. **跨域支持**：通过 Discovery 支持跨集群策略管理

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
2083-2353 行，OPA 体系结构部分
