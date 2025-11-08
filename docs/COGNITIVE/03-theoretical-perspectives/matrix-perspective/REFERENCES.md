# 矩阵视角参考链接

## 📑 目录

- [📑 目录](#-目录)
- [1 核心文档](#1-核心文档)
  - [项目内部文档](#项目内部文档)
  - [矩阵视角文档](#矩阵视角文档)
- [2 技术文档](#2-技术文档)
  - [Docker](#docker)
  - [Kubernetes](#kubernetes)
  - [K3s](#k3s)
  - [WasmEdge](#wasmedge)
  - [OPA](#opa)
  - [多租户](#多租户)
- [3 学术资源](#3-学术资源)
  - [矩阵理论](#矩阵理论)
  - [机器学习](#机器学习)
  - [云原生理论](#云原生理论)
- [4 开源项目](#4-开源项目)
  - [核心项目](#核心项目)
  - [相关项目](#相关项目)
- [5 社区资源](#5-社区资源)
  - [CNCF](#cncf)
  - [社区活动](#社区活动)
  - [技术博客](#技术博客)

---

## 1 核心文档

### 项目内部文档

- **[28. 架构框架](../../TECHNICAL/28-architecture-framework/architecture-framework.md)** -
  多维度架构体系与技术规范（技术架构、概念架构、数据架构、业务架构、软件架构、应
  用架构、场景架构）
- **[05. 全局架构设计](../../02-architecture-design/architecture-design/architecture-design.md)** -
  技术组合和架构决策
- **[ai_view.md](../../ai_view.md)** - 核心矩阵内容的原始来源
- **[01. 知识图谱](../../01-core-foundations/knowledge-map/knowledge-map.md)** -
  知识图谱
- **[02. 概览](../../01-core-foundations/overview/overview.md)** - 项目概览
- **[06. 问题-解决方案矩阵](../../02-architecture-design/problem-solution-matrix/problem-solution-matrix.md)** -
  问题解决方案矩阵
- **[07. 形式化理论](../formal-theory/formal-theory.md)** - 形式化理论基础
- **[27. 2025 年技术趋势汇总](../../TECHNICAL/27-2025-trends/2025-trends.md)** -
  最新技术趋势

### 矩阵视角文档

- **[核心概念矩阵](01-core-concepts.md)** - 12 维原子概念向量、6 维场景向量
- **[关系矩阵](02-relation-matrix.md)** - 概念之间的依赖、转换、组合关系
- **[属性矩阵](03-attribute-matrix.md)** - 概念属性在不同场景下的表现
- **[场景变换矩阵](04-scene-transformation.md)** - 场景间的迁移和转换规则
- **[操作变换矩阵](05-operation-transformation.md)** - 各种操作的矩阵表示
- **[技术链矩阵序列](06-tech-chain-sequence.md)** - Docker→K8s→K3s→WasmEdge→OPA→
  多租户的矩阵序列
- **[AI 参数矩阵](07-ai-parameters.md)** - AI 可学习参数矩阵
- **[矩阵运算与应用](08-matrix-operations.md)** - 实际的计算方法和应用场景
- **[实践案例](09-practice-cases.md)** - 边缘计算、Serverless、AI 推理、多租户等
  场景的矩阵分析

## 2 技术文档

### Docker

- [Docker 官方文档](https://docs.docker.com/)
- [OCI 镜像规范](https://github.com/opencontainers/image-spec)
- [BuildKit 文档](https://docs.docker.com/build/buildkit/)

### Kubernetes

- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [Kubernetes API 参考](https://kubernetes.io/docs/reference/kubernetes-api/)
- [Kubernetes 1.30 发布说明](https://kubernetes.io/blog/2024/12/kubernetes-1-30-release-announcement/)

### K3s

- [K3s 官方文档](https://docs.k3s.io/)
- [K3s 1.30 发布说明](https://github.com/k3s-io/k3s/releases/tag/v1.30.4%2Bk3s1)
- [K3s GitHub](https://github.com/k3s-io/k3s)

### WasmEdge

- [WasmEdge 官方文档](https://wasmedge.org/docs/)
- [WasmEdge 0.14 发布说明](https://github.com/WasmEdge/WasmEdge/releases/tag/0.14.0)
- [WasmEdge GitHub](https://github.com/WasmEdge/WasmEdge)

### OPA

- [OPA 官方文档](https://www.openpolicyagent.org/docs/)
- [OPA-Wasm 文档](https://www.openpolicyagent.org/docs/latest/wasm/)
- [Gatekeeper 文档](https://open-policy-agent.github.io/gatekeeper/website/docs/)

### 多租户

- [Capsule 文档](https://clastix.io/docs/)
- [HNC 文档](https://github.com/kubernetes-sigs/hierarchical-namespaces)
- [Cluster-API 文档](https://cluster-api.sigs.k8s.io/)

## 3 学术资源

### 矩阵理论

- [线性代数基础](https://en.wikipedia.org/wiki/Linear_algebra)
- [矩阵运算](<https://en.wikipedia.org/wiki/Matrix_(mathematics)>)
- [张量运算](https://en.wikipedia.org/wiki/Tensor)

### 机器学习

- [梯度下降法](https://en.wikipedia.org/wiki/Gradient_descent)
- [Adam 优化算法](https://en.wikipedia.org/wiki/Stochastic_gradient_descent#Adam)
- [损失函数](https://en.wikipedia.org/wiki/Loss_function)

### 云原生理论

- [CNCF 技术雷达](https://www.cncf.io/reports/)
- [KubeCon 2025 议题](https://www.cncf.io/events/kubecon-cloudnativecon-events/)
- [云原生最佳实践](https://www.cncf.io/reports/)

## 4 开源项目

### 核心项目

- [Docker](https://github.com/docker/docker)
- [Kubernetes](https://github.com/kubernetes/kubernetes)
- [K3s](https://github.com/k3s-io/k3s)
- [WasmEdge](https://github.com/WasmEdge/WasmEdge)
- [OPA](https://github.com/open-policy-agent/opa)
- [Gatekeeper](https://github.com/open-policy-agent/gatekeeper)

### 相关项目

- [crun](https://github.com/containers/crun)
- [containerd-shim-runwasi](https://github.com/containerd/runwasi)
- [Capsule](https://github.com/clastix/capsule)
- [KEDA](https://github.com/kedacore/keda)
- [ArgoCD](https://github.com/argoproj/argo-cd)
- [Flux](https://github.com/fluxcd/flux2)

## 5 社区资源

### CNCF

- [CNCF 官网](https://www.cncf.io/)
- [CNCF 项目](https://www.cncf.io/projects/)
- [CNCF 2025 技术趋势报告](https://www.cncf.io/reports/)

### 社区活动

- [KubeCon 2025](https://www.cncf.io/events/kubecon-cloudnativecon-events/)
- [WasmEdge Meetup](https://github.com/WasmEdge/WasmEdge/discussions)
- [OPA Community](https://www.openpolicyagent.org/community/)

### 技术博客

- [Kubernetes Blog](https://kubernetes.io/blog/)
- [Docker Blog](https://www.docker.com/blog/)
- [CNCF Blog](https://www.cncf.io/blog/)

---

**参考**：

- [参考链接 - 返回目录](../README.md)
- [矩阵视角文档主索引](README.md)
