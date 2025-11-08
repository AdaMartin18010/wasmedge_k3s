# 快速开始指南

> **创建日期**：2025-11-07 **更新频率**：每月审查 **维护者**：项目团队

---

## 📋 指南概览

本指南为不同角色的读者提供最短路径，帮助您快速找到所需内容。

**阅读时间**：5-10 分钟

---

## 🎯 按角色快速开始

### 👨‍💻 开发者

**目标**：快速上手实践，部署和运行应用

**推荐路径**：

1. **[认知视角](ai_view.md)** →
   [3.3 落地路径：10 分钟跑通"K3s + WasmEdge"](ai_view.md#33-落地路径10-分钟跑通k3s--wasmedge)
2. **[认知视角](ai_view.md)** →
   [4.3 落地路径：10 分钟跑通"K3s + WasmEdge + OPA"准入控制](ai_view.md#43-落地路径10-分钟跑通k3s--wasmedge--opa准入控制)
3. **[安装部署文档](docs/TECHNICAL/05-devops/installation/installation.md)** →
   完整安装指南
4. **[故障排查文档](docs/TECHNICAL/05-devops/troubleshooting/troubleshooting.md)**
   → 常见问题解决

**关键文档**：

- [认知视角](ai_view.md) - 技术演进主线和实践路径
- [安装部署](docs/TECHNICAL/05-devops/installation/installation.md) - 完整安装指
  南
- [故障排查](docs/TECHNICAL/05-devops/troubleshooting/troubleshooting.md) - 常见
  问题解决

**预计时间**：30 分钟上手，1 小时完成部署

---

### 🏗️ 架构师

**目标**：理解技术架构和设计原理，进行技术选型

**推荐路径**：

1. **[认知视角](ai_view.md)** →
   [2.1 理念层：从"货运集装箱"到"声明式宇宙"](ai_view.md#21-理念层从货运集装箱到声明式宇宙)
2. **[架构视角](architecture_view.md)** → 架构拆解与组合原理
3. **[系统视角](system_view.md)** → 7 层 4 域模型和技术选型
4. **[矩阵视角](ai_view.md#7-矩阵视角云原生矩阵力学)** → 云原生矩阵力学模型

**关键文档**：

- [认知视角](ai_view.md) - 技术演进主线和理念层
- [架构视角](architecture_view.md) - 架构拆解与组合
- [系统视角](system_view.md) - 7 层 4 域模型
- [技术-场景矩阵](ai_view.md#6-技术-场景矩阵96-全景) - 9×6 全景矩阵

**预计时间**：2 小时理解架构，1 天完成技术选型

---

### 🔧 运维工程师

**目标**：部署、监控、故障排查和性能优化

**推荐路径**：

1. **[安装部署文档](docs/TECHNICAL/05-devops/installation/installation.md)** →
   完整安装指南
2. **[故障排查文档](docs/TECHNICAL/05-devops/troubleshooting/troubleshooting.md)**
   → 常见问题解决
3. **[eBPF/OTLP 视角](ebpf_otlp_view.md)** → 横纵耦合问题定位模型
4. **[隔离栈文档](docs/TECHNICAL/08-architecture-analysis/isolation-stack/isolation-stack.md)**
   → 五层隔离栈体系

**关键文档**：

- [安装部署](docs/TECHNICAL/05-devops/installation/installation.md) - 完整安装指
  南
- [故障排查](docs/TECHNICAL/05-devops/troubleshooting/troubleshooting.md) - 常见
  问题解决
- [eBPF/OTLP 视角](ebpf_otlp_view.md) - 问题定位模型
- [隔离栈文档](docs/TECHNICAL/08-architecture-analysis/isolation-stack/isolation-stack.md) -
  五层隔离栈体系

**预计时间**：1 小时完成部署，2 小时掌握故障排查

---

### 🔬 研究人员

**目标**：理解理论框架和数学模型，进行深入研究

**推荐路径**：

1. **[认知视角](ai_view.md)** →
   [7. 矩阵视角：云原生矩阵力学](ai_view.md#7-矩阵视角云原生矩阵力学)
2. **[代数视角](algebra_view.md)** → 算子理论和代数结构
3. **[结构视角](structure_view.md)** → 计算-控制-信息三元结构
4. **[形式化理论](docs/COGNITIVE/03-theoretical-perspectives/formal-theory/formal-theory.md)**
   → 结构同构和关系等价

**关键文档**：

- [矩阵视角](ai_view.md#7-矩阵视角云原生矩阵力学) - 云原生矩阵力学模型
- [代数视角](algebra_view.md) - 算子理论和代数结构
- [结构视角](structure_view.md) - 计算-控制-信息三元结构
- [形式化理论](docs/COGNITIVE/03-theoretical-perspectives/formal-theory/formal-theory.md) -
  结构同构和关系等价

**预计时间**：1 天理解理论框架，1 周深入研究

---

## 📚 按主题快速开始

### 技术演进

**目标**：理解技术演进历史和逻辑

**推荐路径**：

1. [认知视角](ai_view.md) →
   [2. Docker → K8s → K3s：容器技术栈演进](ai_view.md#2-docker--k8s--k3s容器技术栈演进)
2. [认知视角](ai_view.md) →
   [2.4 时间轴：技术演进历程](ai_view.md#24-时间轴技术演进历程)
3. [技术社会视角](tech_view.md) →
   [第三部分：基础设施史视角的详细展开](tech_view.md#第三部分基础设施史视角的详细展开)

**关键文档**：

- [认知视角](ai_view.md) - 技术演进主线
- [技术社会视角](tech_view.md) - 基础设施史视角

---

### WasmEdge 集成

**目标**：集成 WasmEdge 到 K3s/K8s

**推荐路径**：

1. [认知视角](ai_view.md) →
   [3. WasmEdge 集成：WebAssembly 作为一等公民](ai_view.md#3-wasmedge-集成webassembly-作为一等公民)
2. [认知视角](ai_view.md) →
   [3.3 落地路径：10 分钟跑通"K3s + WasmEdge"](ai_view.md#33-落地路径10-分钟跑通k3s--wasmedge)
3. [安装部署文档](docs/TECHNICAL/05-devops/installation/installation.md) →
   WasmEdge 安装配置

**关键文档**：

- [认知视角](ai_view.md) - WasmEdge 集成指南
- [安装部署](docs/TECHNICAL/05-devops/installation/installation.md) - WasmEdge
  安装配置

---

### OPA 集成

**目标**：集成 OPA 策略引擎

**推荐路径**：

1. [认知视角](ai_view.md) →
   [4. OPA 集成：策略即代码的轻量级落地](ai_view.md#4-opa-集成策略即代码的轻量级落地)
2. [认知视角](ai_view.md) →
   [4.3 落地路径：10 分钟跑通"K3s + WasmEdge + OPA"准入控制](ai_view.md#43-落地路径10-分钟跑通k3s--wasmedge--opa准入控制)
3. [安装部署文档](docs/TECHNICAL/05-devops/installation/installation.md) → OPA
   Gatekeeper 安装配置

**关键文档**：

- [认知视角](ai_view.md) - OPA 集成指南
- [安装部署](docs/TECHNICAL/05-devops/installation/installation.md) - OPA
  Gatekeeper 安装配置

---

### 问题定位

**目标**：快速定位和解决生产问题

**推荐路径**：

1. [eBPF/OTLP 视角](ebpf_otlp_view.md) → 横纵耦合问题定位模型
2. [隔离栈文档](docs/TECHNICAL/08-architecture-analysis/isolation-stack/isolation-stack.md)
   → 五层隔离栈体系
3. [故障排查文档](docs/TECHNICAL/05-devops/troubleshooting/troubleshooting.md) →
   常见问题解决

**关键文档**：

- [eBPF/OTLP 视角](ebpf_otlp_view.md) - 问题定位模型
- [隔离栈文档](docs/TECHNICAL/08-architecture-analysis/isolation-stack/isolation-stack.md) -
  五层隔离栈体系
- [故障排查](docs/TECHNICAL/05-devops/troubleshooting/troubleshooting.md) - 常见
  问题解决

---

## 🚀 5 分钟快速上手

### 步骤 1：了解核心演进路径（2 分钟）

阅读 [认知视角](ai_view.md) 的 [1. 概述](ai_view.md#1-概述) 部分，了解：

- Docker → K8s → K3s → WasmEdge → OPA 的演进路径
- 每个技术解决的问题和核心价值

### 步骤 2：查看一键安装命令（1 分钟）

查看 [认知视角](ai_view.md) 的
[8.1 2025 年一键安装命令](ai_view.md#81-2025-年一键安装命令) 部分，获取：

- K3s + WasmEdge 一键安装命令
- OPA-Wasm Gatekeeper 安装命令
- 镜像签名和推送命令

### 步骤 3：实践落地路径（2 分钟）

参考 [认知视角](ai_view.md) 的实践路径：

- [3.3 落地路径：10 分钟跑通"K3s + WasmEdge"](ai_view.md#33-落地路径10-分钟跑通k3s--wasmedge)
- [4.3 落地路径：10 分钟跑通"K3s + WasmEdge + OPA"准入控制](ai_view.md#43-落地路径10-分钟跑通k3s--wasmedge--opa准入控制)

---

## 📖 完整学习路径

### 新手路径（2-4 周）

1. **第 1 周**：理解基础概念

   - [认知视角](ai_view.md) →
     [2. Docker → K8s → K3s：容器技术栈演进](ai_view.md#2-docker--k8s--k3s容器技术栈演进)
   - [系统视角](system_view.md) → 7 层 4 域模型

2. **第 2 周**：实践部署

   - [安装部署文档](docs/TECHNICAL/05-devops/installation/installation.md)
   - [故障排查文档](docs/TECHNICAL/05-devops/troubleshooting/troubleshooting.md)

3. **第 3-4 周**：深入理解
   - [架构视角](architecture_view.md)
   - [eBPF/OTLP 视角](ebpf_otlp_view.md)

### 进阶路径（1-2 月）

1. **第 1 个月**：深入架构和理论

   - [架构视角](architecture_view.md)
   - [代数视角](algebra_view.md)
   - [结构视角](structure_view.md)

2. **第 2 个月**：多视角分析
   - [技术社会视角](tech_view.md)
   - [eBPF/OTLP 视角](ebpf_otlp_view.md)
   - [程序设计视角](programming_view.md)

### 专家路径（3-6 月）

1. **第 3-4 个月**：理论深入研究

   - [形式化理论](docs/COGNITIVE/03-theoretical-perspectives/formal-theory/formal-theory.md)
   - [范畴论视角](docs/COGNITIVE/03-theoretical-perspectives/category-theory/category-theory.md)
   - [矩阵视角](docs/COGNITIVE/03-theoretical-perspectives/matrix-perspective/README.md)

2. **第 5-6 个月**：实践和优化
   - [案例研究](docs/ARCHITECTURE/04-applications/case-studies/)
   - [优化实践](docs/TECHNICAL/09-optimization-practices/)

---

## 🔗 相关文档

### 核心视角文档

- [认知视角](ai_view.md) ⭐ - 技术演进主线和实践路径
- [架构视角](architecture_view.md) ⭐ - 架构拆解与组合
- [系统视角](system_view.md) ⭐ - 7 层 4 域模型
- [eBPF/OTLP 视角](ebpf_otlp_view.md) ⭐ - 问题定位模型

### 文档目录

- [文档总览](docs/README.md) - 完整的文档体系说明
- [文档索引](docs/INDEX.md) - 完整文档索引
- [技术参考文档](docs/TECHNICAL/README.md) - 技术规格和实践指南

---

## 📝 更新记录

| 日期       | 更新内容                           | 更新人   |
| ---------- | ---------------------------------- | -------- |
| 2025-11-07 | 创建快速开始指南                   | 项目团队 |
| 2025-11-07 | 更新案例验证完成状态和文档统计信息 | 项目团队 |

---

**最后更新**：2025-11-07 **下次审查**：2025-12-07 **维护者**：项目团队
