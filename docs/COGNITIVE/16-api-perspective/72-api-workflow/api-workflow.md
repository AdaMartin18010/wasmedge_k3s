# API 工作流规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 工作流架构](#11-工作流架构)
- [2. 工作流定义](#2-工作流定义)
  - [2.1 工作流 DSL](#21-工作流-dsl)
  - [2.2 工作流状态机](#22-工作流状态机)
- [3. 工作流执行](#3-工作流执行)
  - [3.1 执行引擎](#31-执行引擎)
  - [3.2 任务调度](#32-任务调度)
- [4. 工作流状态](#4-工作流状态)
  - [4.1 状态转换](#41-状态转换)
  - [4.2 状态持久化](#42-状态持久化)
- [5. 工作流监控](#5-工作流监控)
  - [5.1 执行监控](#51-执行监控)
  - [5.2 性能监控](#52-性能监控)
- [6. 工作流版本](#6-工作流版本)
  - [6.1 版本管理](#61-版本管理)
  - [6.2 版本迁移](#62-版本迁移)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 工作流规范定义了 API 在工作流场景下的设计和实现，从工作流定义到工作流执行，
从工作流状态到工作流监控。

### 1.1 工作流架构

```text
工作流定义（Workflow Definition）
  ↓
工作流引擎（Workflow Engine）
  ↓
任务执行（Task Execution）
  ↓
状态更新（State Update）
```

---

## 2. 工作流定义

### 2.1 工作流 DSL

**工作流 DSL 定义**：

```yaml
apiVersion: api.example.com/v1
kind: WorkflowDefinition
metadata:
  name: order-processing-workflow
spec:
  version: "1.0"
  description: "Order processing workflow"
  startAt: "validate_order"
  states:
    - name: "validate_order"
      type: "task"
      resource: "arn:aws:lambda:us-east-1:123456789012:function:validate-order"
      timeout: 30
      retry:
        - errorEquals: ["States.ALL"]
          intervalSeconds: 2
          maxAttempts: 3
          backoffRate: 2.0
      next: "check_inventory"

    - name: "check_inventory"
      type: "task"
      resource: "arn:aws:lambda:us-east-1:123456789012:function:check-inventory"
      timeout: 30
      next: "create_payment"

    - name: "create_payment"
      type: "task"
      resource: "arn:aws:lambda:us-east-1:123456789012:function:create-payment"
      timeout: 30
      end: true
```

### 2.2 工作流状态机

**状态机定义**：

```go
package main

type WorkflowState string

const (
    StatePending   WorkflowState = "pending"
    StateRunning   WorkflowState = "running"
    StateCompleted WorkflowState = "completed"
    StateFailed    WorkflowState = "failed"
    StateCancelled WorkflowState = "cancelled"
)

type StateTransition struct {
    From State
    To   State
    Condition func(context interface{}) bool
}

type WorkflowStateMachine struct {
    states      []State
    transitions []StateTransition
    currentState State
}

func (sm *WorkflowStateMachine) Transition(to State, context interface{}) error {
    // 检查转换是否有效
    if !sm.isValidTransition(sm.currentState, to) {
        return fmt.Errorf("invalid transition from %s to %s", sm.currentState, to)
    }

    // 检查条件
    transition := sm.getTransition(sm.currentState, to)
    if transition != nil && transition.Condition != nil {
        if !transition.Condition(context) {
            return fmt.Errorf("transition condition not met")
        }
    }

    // 执行转换
    sm.currentState = to
    return nil
}
```

---

## 3. 工作流执行

### 3.1 执行引擎

**执行引擎实现**：

```go
package main

type WorkflowEngine struct {
    workflows map[string]*WorkflowDefinition
    executor  TaskExecutor
    stateStore StateStore
}

func (e *WorkflowEngine) StartWorkflow(workflowID string, input interface{}) (string, error) {
    workflow := e.workflows[workflowID]
    if workflow == nil {
        return "", fmt.Errorf("workflow not found: %s", workflowID)
    }

    executionID := generateExecutionID()
    execution := &WorkflowExecution{
        ID:         executionID,
        WorkflowID: workflowID,
        Status:     StateRunning,
        Input:      input,
        StartTime:   time.Now(),
    }

    e.stateStore.SaveExecution(execution)

    // 异步执行
    go e.executeWorkflow(execution, workflow)

    return executionID, nil
}

func (e *WorkflowEngine) executeWorkflow(execution *WorkflowExecution, workflow *WorkflowDefinition) {
    currentState := workflow.StartAt

    for {
        state := workflow.GetState(currentState)
        if state == nil {
            break
        }

        // 执行任务
        result, err := e.executor.Execute(state, execution.Input)
        if err != nil {
            execution.Status = StateFailed
            execution.Error = err.Error()
            e.stateStore.SaveExecution(execution)
            return
        }

        // 更新执行状态
        execution.CurrentState = currentState
        execution.Results[currentState] = result
        e.stateStore.SaveExecution(execution)

        // 移动到下一个状态
        if state.End {
            execution.Status = StateCompleted
            execution.EndTime = time.Now()
            e.stateStore.SaveExecution(execution)
            break
        }

        currentState = state.Next
    }
}
```

### 3.2 任务调度

**任务调度实现**：

```go
package main

import (
    "sync"
)

type TaskScheduler struct {
    workers    int
    taskQueue  chan Task
    wg         sync.WaitGroup
}

func NewTaskScheduler(workers int) *TaskScheduler {
    return &TaskScheduler{
        workers:   workers,
        taskQueue: make(chan Task, 100),
    }
}

func (s *TaskScheduler) Start() {
    for i := 0; i < s.workers; i++ {
        s.wg.Add(1)
        go s.worker()
    }
}

func (s *TaskScheduler) worker() {
    defer s.wg.Done()
    for task := range s.taskQueue {
        s.executeTask(task)
    }
}

func (s *TaskScheduler) Schedule(task Task) {
    s.taskQueue <- task
}

func (s *TaskScheduler) executeTask(task Task) {
    // 执行任务
    result, err := task.Execute()
    if err != nil {
        task.OnError(err)
        return
    }
    task.OnSuccess(result)
}
```

---

## 4. 工作流状态

### 4.1 状态转换

**状态转换实现**：

```go
package main

type WorkflowStateManager struct {
    execution *WorkflowExecution
    stateMachine *WorkflowStateMachine
}

func (m *WorkflowStateManager) TransitionTo(state WorkflowState, context interface{}) error {
    return m.stateMachine.Transition(state, context)
}

func (m *WorkflowStateManager) GetCurrentState() WorkflowState {
    return m.execution.Status
}

func (m *WorkflowStateManager) CanTransitionTo(state WorkflowState) bool {
    return m.stateMachine.IsValidTransition(m.execution.Status, state)
}
```

### 4.2 状态持久化

**状态持久化配置**：

```yaml
apiVersion: api.example.com/v1
kind: WorkflowStateStore
metadata:
  name: workflow-state-store
spec:
  type: "postgresql"
  connectionString: "postgresql://user:password@localhost/workflow"
  tableName: "workflow_executions"
  retention: "30d"
```

**状态持久化实现**：

```go
package main

type StateStore interface {
    SaveExecution(execution *WorkflowExecution) error
    GetExecution(executionID string) (*WorkflowExecution, error)
    UpdateExecutionStatus(executionID string, status WorkflowState) error
}

type PostgreSQLStateStore struct {
    db *sql.DB
}

func (s *PostgreSQLStateStore) SaveExecution(execution *WorkflowExecution) error {
    query := `
        INSERT INTO workflow_executions (id, workflow_id, status, input, results, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (id) DO UPDATE SET
            status = $3,
            results = $5,
            updated_at = $7
    `

    _, err := s.db.Exec(query,
        execution.ID,
        execution.WorkflowID,
        execution.Status,
        execution.Input,
        execution.Results,
        execution.StartTime,
        time.Now(),
    )

    return err
}
```

---

## 5. 工作流监控

### 5.1 执行监控

**执行监控配置**：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: workflow-execution-metrics
spec:
  groups:
    - name: workflow_execution
      rules:
        - record: workflow:executions_total
          expr: |
            sum(rate(workflow_executions_total[5m])) by (workflow_id, status)
        - record: workflow:execution_duration_seconds
          expr: |
            histogram_quantile(0.95, sum(rate(workflow_execution_duration_seconds_bucket[5m])) by (workflow_id, le))
```

### 5.2 性能监控

**性能监控实现**：

```go
package main

type WorkflowMetrics struct {
    WorkflowID      string
    ExecutionID     string
    StartTime       time.Time
    EndTime         time.Time
    Duration        time.Duration
    TasksExecuted   int
    TasksFailed     int
}

func (e *WorkflowEngine) RecordMetrics(metrics WorkflowMetrics) {
    // 记录 Prometheus 指标
    prometheus.RecordWorkflowExecution(metrics.WorkflowID, metrics.Duration)
    prometheus.RecordWorkflowTasks(metrics.WorkflowID, metrics.TasksExecuted, metrics.TasksFailed)

    // 记录到日志
    log.Info("Workflow execution completed",
        "workflow_id", metrics.WorkflowID,
        "execution_id", metrics.ExecutionID,
        "duration", metrics.Duration,
        "tasks_executed", metrics.TasksExecuted,
    )
}
```

---

## 6. 工作流版本

### 6.1 版本管理

**版本管理配置**：

```yaml
apiVersion: api.example.com/v1
kind: WorkflowVersion
metadata:
  name: order-processing-workflow-v2
spec:
  workflowID: "order-processing-workflow"
  version: "2.0"
  previousVersion: "1.0"
  changes:
    - type: "added"
      description: "Added payment retry logic"
    - type: "modified"
      description: "Updated inventory check timeout"
  migration:
    strategy: "gradual"
    rolloutPercentage: 10
```

### 6.2 版本迁移

**版本迁移实现**：

```go
package main

func (e *WorkflowEngine) MigrateWorkflow(executionID string, newVersion string) error {
    execution := e.stateStore.GetExecution(executionID)
    if execution == nil {
        return fmt.Errorf("execution not found: %s", executionID)
    }

    oldWorkflow := e.workflows[execution.WorkflowID]
    newWorkflow := e.workflows[newVersion]

    // 迁移状态
    migratedState := migrateState(execution.CurrentState, oldWorkflow, newWorkflow)

    // 更新执行
    execution.WorkflowID = newVersion
    execution.CurrentState = migratedState
    e.stateStore.SaveExecution(execution)

    return nil
}
```

---

## 7. 相关文档

- **[API 编排规范](../71-api-orchestration/api-orchestration.md)** - API 编排
- **[API 集成规范](../70-api-integration/api-integration.md)** - API 集成
- **[API 事件驱动规范](../35-api-event-driven/api-event-driven.md)** - 事件驱动
- **[最佳实践](../08-best-practices/best-practices.md)** - 工作流最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
