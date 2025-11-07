# API 编排规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 编排架构](#11-编排架构)
- [2. 编排模式](#2-编排模式)
  - [2.1 顺序编排](#21-顺序编排)
  - [2.2 并行编排](#22-并行编排)
  - [2.3 条件编排](#23-条件编排)
- [3. 编排引擎](#3-编排引擎)
  - [3.1 工作流定义](#31-工作流定义)
  - [3.2 执行引擎](#32-执行引擎)
- [4. 错误处理](#4-错误处理)
  - [4.1 重试机制](#41-重试机制)
  - [4.2 补偿机制](#42-补偿机制)
- [5. 状态管理](#5-状态管理)
  - [5.1 状态存储](#51-状态存储)
  - [5.2 状态恢复](#52-状态恢复)
- [6. 编排监控](#6-编排监控)
  - [6.1 执行监控](#61-执行监控)
  - [6.2 性能监控](#62-性能监控)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 编排规范定义了 API 在编排场景下的设计和实现，从编排模式到编排引擎，从错误处
理到状态管理。

### 1.1 编排架构

```text
编排定义（Orchestration Definition）
  ↓
编排引擎（Orchestration Engine）
  ↓
API 调用（API Calls）
  ↓
结果聚合（Result Aggregation）
```

---

## 2. 编排模式

### 2.1 顺序编排

**顺序编排配置**：

```yaml
apiVersion: api.example.com/v1
kind: SequentialOrchestration
metadata:
  name: order-processing-orchestration
spec:
  steps:
    - step: 1
      name: "validate_order"
      api: "order-service"
      endpoint: "/api/v1/orders/validate"
      method: "POST"
    - step: 2
      name: "check_inventory"
      api: "inventory-service"
      endpoint: "/api/v1/inventory/check"
      method: "POST"
      dependsOn: ["validate_order"]
    - step: 3
      name: "create_payment"
      api: "payment-service"
      endpoint: "/api/v1/payments"
      method: "POST"
      dependsOn: ["check_inventory"]
```

**顺序编排实现**：

```go
package main

type SequentialOrchestrator struct {
    steps []Step
}

func (o *SequentialOrchestrator) Execute(ctx context.Context) error {
    for _, step := range o.steps {
        if err := o.executeStep(ctx, step); err != nil {
            return err
        }
    }
    return nil
}

func (o *SequentialOrchestrator) executeStep(ctx context.Context, step Step) error {
    result, err := callAPI(ctx, step.API, step.Endpoint, step.Method, step.Input)
    if err != nil {
        return err
    }

    // 存储结果供后续步骤使用
    ctx = context.WithValue(ctx, step.Name, result)
    return nil
}
```

### 2.2 并行编排

**并行编排配置**：

```yaml
apiVersion: api.example.com/v1
kind: ParallelOrchestration
metadata:
  name: order-parallel-orchestration
spec:
  steps:
    - step: 1
      name: "validate_order"
      api: "order-service"
      endpoint: "/api/v1/orders/validate"
    - step: 2
      name: "check_inventory"
      api: "inventory-service"
      endpoint: "/api/v1/inventory/check"
      parallel: true
    - step: 3
      name: "check_payment_method"
      api: "payment-service"
      endpoint: "/api/v1/payment-methods/check"
      parallel: true
```

**并行编排实现**：

```go
package main

import (
    "sync"
    "context"
)

type ParallelOrchestrator struct {
    steps []Step
}

func (o *ParallelOrchestrator) Execute(ctx context.Context) error {
    var wg sync.WaitGroup
    errChan := make(chan error, len(o.steps))

    for _, step := range o.steps {
        if step.Parallel {
            wg.Add(1)
            go func(s Step) {
                defer wg.Done()
                if err := o.executeStep(ctx, s); err != nil {
                    errChan <- err
                }
            }(step)
        } else {
            if err := o.executeStep(ctx, step); err != nil {
                return err
            }
        }
    }

    wg.Wait()
    close(errChan)

    // 检查错误
    for err := range errChan {
        if err != nil {
            return err
        }
    }

    return nil
}
```

### 2.3 条件编排

**条件编排配置**：

```yaml
apiVersion: api.example.com/v1
kind: ConditionalOrchestration
metadata:
  name: order-conditional-orchestration
spec:
  steps:
    - step: 1
      name: "check_order_amount"
      api: "order-service"
      endpoint: "/api/v1/orders/{id}/amount"
    - step: 2
      name: "apply_discount"
      api: "discount-service"
      endpoint: "/api/v1/discounts/apply"
      condition: "step1.amount > 1000"
    - step: 3
      name: "create_payment"
      api: "payment-service"
      endpoint: "/api/v1/payments"
      condition: "always"
```

**条件编排实现**：

```go
package main

import (
    "github.com/antonmedv/expr"
)

type ConditionalOrchestrator struct {
    steps []Step
}

func (o *ConditionalOrchestrator) Execute(ctx context.Context) error {
    results := make(map[string]interface{})

    for _, step := range o.steps {
        // 评估条件
        if step.Condition != "" && step.Condition != "always" {
            program, err := expr.Compile(step.Condition, expr.Env(results))
            if err != nil {
                return err
            }

            output, err := expr.Run(program, results)
            if err != nil {
                return err
            }

            if !output.(bool) {
                continue // 跳过此步骤
            }
        }

        // 执行步骤
        result, err := o.executeStep(ctx, step)
        if err != nil {
            return err
        }

        results[step.Name] = result
    }

    return nil
}
```

---

## 3. 编排引擎

### 3.1 工作流定义

**工作流定义格式**：

```yaml
apiVersion: api.example.com/v1
kind: WorkflowDefinition
metadata:
  name: order-processing-workflow
spec:
  version: "1.0"
  startAt: "validate_order"
  states:
    - name: "validate_order"
      type: "task"
      resource: "order-service"
      next: "check_inventory"
    - name: "check_inventory"
      type: "task"
      resource: "inventory-service"
      next: "create_payment"
    - name: "create_payment"
      type: "task"
      resource: "payment-service"
      end: true
```

### 3.2 执行引擎

**执行引擎实现**：

```go
package main

type WorkflowEngine struct {
    workflows map[string]*WorkflowDefinition
    stateStore StateStore
}

func (e *WorkflowEngine) ExecuteWorkflow(workflowID string, input interface{}) error {
    workflow := e.workflows[workflowID]
    if workflow == nil {
        return fmt.Errorf("workflow not found: %s", workflowID)
    }

    executionID := generateExecutionID()
    execution := &WorkflowExecution{
        ID:        executionID,
        WorkflowID: workflowID,
        Status:    "running",
        Input:     input,
    }

    e.stateStore.SaveExecution(execution)

    // 执行工作流
    return e.executeStates(workflow, execution)
}

func (e *WorkflowEngine) executeStates(workflow *WorkflowDefinition, execution *WorkflowExecution) error {
    currentState := workflow.StartAt

    for {
        state := workflow.GetState(currentState)
        if state == nil {
            break
        }

        // 执行状态
        result, err := e.executeState(state, execution)
        if err != nil {
            execution.Status = "failed"
            e.stateStore.SaveExecution(execution)
            return err
        }

        // 更新执行状态
        execution.CurrentState = currentState
        execution.Results[currentState] = result
        e.stateStore.SaveExecution(execution)

        // 移动到下一个状态
        if state.End {
            break
        }
        currentState = state.Next
    }

    execution.Status = "completed"
    e.stateStore.SaveExecution(execution)
    return nil
}
```

---

## 4. 错误处理

### 4.1 重试机制

**重试机制配置**：

```yaml
apiVersion: api.example.com/v1
kind: RetryPolicy
metadata:
  name: orchestration-retry-policy
spec:
  maxRetries: 3
  backoff:
    strategy: "exponential"
    initialDelay: "1s"
    maxDelay: "10s"
    multiplier: 2
  retryableErrors:
    - "500"
    - "502"
    - "503"
    - "504"
```

### 4.2 补偿机制

**补偿机制实现**：

```go
package main

type CompensationStep struct {
    Name     string
    API      string
    Endpoint string
    Method   string
}

type OrchestrationStep struct {
    Step
    Compensation CompensationStep
}

func (o *Orchestrator) ExecuteWithCompensation(ctx context.Context, steps []OrchestrationStep) error {
    executedSteps := []OrchestrationStep{}

    for _, step := range steps {
        if err := o.executeStep(ctx, step.Step); err != nil {
            // 执行补偿
            return o.compensate(ctx, executedSteps)
        }
        executedSteps = append(executedSteps, step)
    }

    return nil
}

func (o *Orchestrator) compensate(ctx context.Context, steps []OrchestrationStep) error {
    // 逆序执行补偿
    for i := len(steps) - 1; i >= 0; i-- {
        step := steps[i]
        if step.Compensation.Name != "" {
            if err := o.executeStep(ctx, step.Compensation.Step); err != nil {
                return err
            }
        }
    }
    return nil
}
```

---

## 5. 状态管理

### 5.1 状态存储

**状态存储配置**：

```yaml
apiVersion: api.example.com/v1
kind: StateStore
metadata:
  name: orchestration-state-store
spec:
  type: "redis"
  endpoint: "redis:6379"
  ttl: "24h"
  persistence:
    enabled: true
    backend: "postgresql"
```

### 5.2 状态恢复

**状态恢复实现**：

```go
package main

func (e *WorkflowEngine) ResumeWorkflow(executionID string) error {
    execution := e.stateStore.GetExecution(executionID)
    if execution == nil {
        return fmt.Errorf("execution not found: %s", executionID)
    }

    if execution.Status != "running" {
        return fmt.Errorf("execution is not in running state: %s", execution.Status)
    }

    workflow := e.workflows[execution.WorkflowID]
    return e.executeStates(workflow, execution)
}
```

---

## 6. 编排监控

### 6.1 执行监控

**执行监控配置**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: orchestration-execution-metrics
spec:
  groups:
    - name: orchestration_execution
      rules:
        - record: orchestration:workflow_executions_total
          expr: |
            sum(rate(workflow_executions_total[5m])) by (workflow_id, status)
        - record: orchestration:workflow_duration_seconds
          expr: |
            histogram_quantile(0.95, sum(rate(workflow_duration_seconds_bucket[5m])) by (workflow_id, le))
```

### 6.2 性能监控

**性能监控实现**：

```go
package main

type OrchestrationMetrics struct {
    WorkflowID      string
    ExecutionID     string
    StartTime       time.Time
    EndTime         time.Time
    Duration        time.Duration
    StepsExecuted   int
    StepsFailed     int
    TotalAPICalls   int
}

func (e *WorkflowEngine) RecordMetrics(metrics OrchestrationMetrics) {
    // 记录指标
    prometheus.RecordWorkflowExecution(metrics.WorkflowID, metrics.Duration)
    prometheus.RecordWorkflowSteps(metrics.WorkflowID, metrics.StepsExecuted, metrics.StepsFailed)
}
```

---

## 7. 相关文档

- **[API 集成规范](../70-api-integration/api-integration.md)** - API 集成
- **[API 工作流规范](../72-api-workflow/api-workflow.md)** - API 工作流
- **[API 事件驱动规范](../35-api-event-driven/api-event-driven.md)** - 事件驱动
- **[最佳实践](../08-best-practices/best-practices.md)** - 编排最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
