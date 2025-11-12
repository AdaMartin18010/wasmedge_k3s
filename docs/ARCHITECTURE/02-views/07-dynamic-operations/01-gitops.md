# GitOps：持续交付的声明式范式

## 📑 目录

- [📑 目录](#-目录)
- [1 概述](#1-概述)
  - [1.1 核心原则](#11-核心原则)
- [2 GitOps 工作流](#2-gitops-工作流)
  - [2.1 基本流程](#21-基本流程)
  - [2.2 关键组件](#22-关键组件)
- [3 ArgoCD](#3-argocd)
  - [3.1 概述](#31-概述)
  - [3.2 核心概念](#32-核心概念)
    - [3.2.1 Application](#321-application)
    - [3.2.2 ApplicationSet](#322-applicationset)
- [4 Flux](#4-flux)
  - [4.1 概述](#41-概述)
  - [4.2 核心概念](#42-核心概念)
    - [4.2.1 GitRepository](#421-gitrepository)
    - [4.2.2 Kustomization](#422-kustomization)
- [5 GitOps 最佳实践](#5-gitops-最佳实践)
  - [5.1 目录结构](#51-目录结构)
  - [5.2 环境分离](#52-环境分离)
  - [5.3 安全实践](#53-安全实践)
- [6 GitOps 与 CI/CD 集成](#6-gitops-与-cicd-集成)
  - [6.1 传统 CI/CD](#61-传统-cicd)
  - [6.2 GitOps CI/CD](#62-gitops-cicd)
  - [6.3 优势](#63-优势)
- [7 形式化定义](#7-形式化定义)
  - [7.1 GitOps 状态](#71-gitops-状态)
  - [7.2 同步函数](#72-同步函数)
  - [7.3 一致性检查](#73-一致性检查)
- [8 总结](#8-总结)

---

## 1 概述

**GitOps** 是一种使用 Git 作为**单一可信源（Single Source of Truth）**的持续交付
范式，通过声明式配置实现自动化部署和运维。

### 1.1 核心原则

1. **Git 作为真相源**：所有配置和代码都在 Git 中
2. **声明式配置**：使用 YAML/JSON 描述期望状态
3. **自动化同步**：自动检测 Git 变更并同步到集群
4. **可观测性**：所有变更可追溯、可审计

## 2 GitOps 工作流

### 2.1 基本流程

```text
开发 → Git Push → CI Pipeline → 镜像构建 → Git Commit → ArgoCD/Flux → 集群同步
```

### 2.2 关键组件

| 组件            | 作用               | 典型工具                |
| --------------- | ------------------ | ----------------------- |
| **Git 仓库**    | 存储配置和代码     | GitHub, GitLab          |
| **CI Pipeline** | 构建镜像、运行测试 | GitHub Actions, Jenkins |
| **镜像仓库**    | 存储容器镜像       | Docker Hub, Harbor      |
| **GitOps 工具** | 同步 Git 到集群    | ArgoCD, Flux            |
| **Kubernetes**  | 运行应用           | K8s, K3s                |

## 3 ArgoCD

### 3.1 概述

**ArgoCD** 是 CNCF 的 GitOps 持续交付工具，提供：

- **自动同步**：检测 Git 变更并自动同步
- **可视化界面**：查看应用状态和同步历史
- **多集群支持**：管理多个 Kubernetes 集群
- **回滚能力**：快速回滚到之前的版本

### 3.2 核心概念

#### 3.2.1 Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
spec:
  project: default
  source:
    repoURL: https://github.com/example/my-app
    targetRevision: main
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

#### 3.2.2 ApplicationSet

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: my-apps
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            environment: production
  template:
    metadata:
      name: "{{name}}-my-app"
    spec:
      project: default
      source:
        repoURL: https://github.com/example/my-app
        targetRevision: main
        path: k8s
      destination:
        server: "{{server}}"
        namespace: default
```

## 4 Flux

### 4.1 概述

**Flux** 是 CNCF 的另一个 GitOps 工具，提供：

- **自动同步**：检测 Git 变更并自动同步
- **Helm 支持**：支持 Helm charts
- **Kustomize 支持**：支持 Kustomize
- **多租户支持**：支持多租户场景

### 4.2 核心概念

#### 4.2.1 GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1beta1
kind: GitRepository
metadata:
  name: my-app
spec:
  interval: 1m
  url: https://github.com/example/my-app
  ref:
    branch: main
```

#### 4.2.2 Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1beta1
kind: Kustomization
metadata:
  name: my-app
spec:
  interval: 5m
  path: ./k8s
  prune: true
  sourceRef:
    kind: GitRepository
    name: my-app
  validation: client
```

## 5 GitOps 最佳实践

### 5.1 目录结构

```text
my-app/
├── README.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── ...
├── k8s/
│   ├── base/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   └── overlays/
│       ├── dev/
│       │   └── kustomization.yaml
│       └── prod/
│           └── kustomization.yaml
└── helm/
    └── my-app/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
```

### 5.2 环境分离

- **开发环境**：自动同步 main 分支
- **测试环境**：自动同步 test 分支
- **生产环境**：手动审批或自动同步 tagged 版本

### 5.3 安全实践

- **RBAC**：限制 GitOps 工具的权限
- **Sealed Secrets**：加密敏感信息
- **OPA/Gatekeeper**：策略即代码
- **审计日志**：记录所有变更

## 6 GitOps 与 CI/CD 集成

### 6.1 传统 CI/CD

```text
开发 → CI → 构建镜像 → 推送镜像 → 更新部署 → 部署到集群
```

### 6.2 GitOps CI/CD

```text
开发 → CI → 构建镜像 → 推送镜像 → 更新 Git → GitOps 自动同步到集群
```

### 6.3 优势

- **分离关注点**：CI 负责构建，CD 负责部署
- **可追溯性**：所有变更都在 Git 中
- **可回滚性**：快速回滚到之前的版本
- **多环境一致性**：使用相同的配置和流程

## 7 形式化定义

### 7.1 GitOps 状态

```text
GitOps 状态 S = ⟨repo, branch, path, commit⟩
其中：
- repo: Git 仓库 URL
- branch: Git 分支
- path: 配置路径
- commit: Git commit SHA
```

### 7.2 同步函数

```text
同步函数 Sync: S → K8s
其中 Sync(S) 将 Git 配置同步到 Kubernetes 集群
```

### 7.3 一致性检查

```text
一致性检查 Consistent: S × K8s → {true, false}
其中 Consistent(S, k8s) 检查集群状态是否与 Git 一致
```

## 8 总结

GitOps 通过**Git 作为真相源**和**声明式配置**实现了：

1. **自动化部署**：自动检测 Git 变更并同步到集群
2. **可追溯性**：所有变更都在 Git 中，可追溯、可审计
3. **可回滚性**：快速回滚到之前的版本
4. **多环境一致性**：使用相同的配置和流程
5. **分离关注点**：CI 负责构建，CD 负责部署

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第 30
行，GitOps 部分
