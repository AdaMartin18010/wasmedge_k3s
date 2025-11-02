# 21. 镜像仓库和镜像管理：全面梳理

## 目录

- [目录](#目录)
- [21.1 文档定位](#211-文档定位)
- [21.2 镜像仓库技术栈全景](#212-镜像仓库技术栈全景)
  - [21.2.1 镜像仓库层次结构](#2121-镜像仓库层次结构)
  - [21.2.2 技术组件矩阵](#2122-技术组件矩阵)
  - [21.2.3 技术栈组合](#2123-技术栈组合)
- [21.3 镜像仓库技术规格](#213-镜像仓库技术规格)
  - [21.3.1 Docker Registry 规格](#2131-docker-registry-规格)
  - [21.3.2 Harbor 规格](#2132-harbor-规格)
  - [21.3.3 Nexus Repository 规格](#2133-nexus-repository-规格)
  - [21.3.4 Quay 规格](#2134-quay-规格)
  - [21.3.5 云镜像仓库规格](#2135-云镜像仓库规格)
  - [21.3.6 镜像仓库对比](#2136-镜像仓库对比)
- [21.4 镜像管理技术规格](#214-镜像管理技术规格)
  - [21.4.1 镜像版本管理](#2141-镜像版本管理)
  - [21.4.2 镜像标签策略](#2142-镜像标签策略)
  - [21.4.3 镜像生命周期管理](#2143-镜像生命周期管理)
  - [21.4.4 镜像清理策略](#2144-镜像清理策略)
  - [21.4.5 镜像垃圾回收](#2145-镜像垃圾回收)
- [21.5 镜像安全技术规格](#215-镜像安全技术规格)
  - [21.5.1 镜像扫描](#2151-镜像扫描)
  - [21.5.2 镜像签名](#2152-镜像签名)
  - [21.5.3 镜像验证](#2153-镜像验证)
  - [21.5.4 访问控制](#2154-访问控制)
- [21.6 镜像分发技术规格](#216-镜像分发技术规格)
  - [21.6.1 镜像拉取策略](#2161-镜像拉取策略)
  - [21.6.2 镜像缓存](#2162-镜像缓存)
  - [21.6.3 镜像同步](#2163-镜像同步)
  - [21.6.4 镜像代理](#2164-镜像代理)
- [21.7 镜像仓库技术栈组合方案](#217-镜像仓库技术栈组合方案)
  - [21.7.1 小规模集群组合](#2171-小规模集群组合)
  - [21.7.2 大规模集群组合](#2172-大规模集群组合)
  - [21.7.3 多集群组合](#2173-多集群组合)
  - [21.7.4 边缘计算组合](#2174-边缘计算组合)
- [21.8 镜像管理最佳实践](#218-镜像管理最佳实践)
  - [21.8.1 镜像命名规范](#2181-镜像命名规范)
  - [21.8.2 镜像版本策略](#2182-镜像版本策略)
  - [21.8.3 镜像安全策略](#2183-镜像安全策略)
  - [21.8.4 镜像优化策略](#2184-镜像优化策略)
- [21.9 参考](#219-参考)

---

## 21.1 文档定位

本文档全面梳理云原生容器技术栈中的镜像仓库和镜像管理技术、规格和最佳实践，包括镜
像仓库（Docker Registry、Harbor、Nexus、Quay、云镜像仓库）、镜像版本管理、镜像生
命周期管理、镜像安全、镜像分发等技术。

**文档结构**：

- **镜像仓库技术栈全景**：镜像仓库层次结构、技术组件矩阵、技术栈组合
- **镜像仓库技术规格**：Docker Registry、Harbor、Nexus、Quay、云镜像仓库详细规格
- **镜像管理技术规格**：镜像版本管理、标签策略、生命周期管理、清理策略、垃圾回收
- **镜像安全技术规格**：镜像扫描、镜像签名、镜像验证、访问控制
- **镜像分发技术规格**：镜像拉取策略、镜像缓存、镜像同步、镜像代理
- **镜像仓库技术栈组合方案**：不同场景的镜像仓库技术栈组合
- **镜像管理最佳实践**：镜像命名规范、版本策略、安全策略、优化策略

## 21.2 镜像仓库技术栈全景

### 21.2.1 镜像仓库层次结构

**镜像仓库层次结构**：

```mermaid
graph TB
    A[镜像构建层] --> B[镜像推送]
    B --> C[镜像仓库<br/>Registry]
    C --> D[镜像存储层<br/>Storage Backend]
    C --> E[镜像管理层<br/>Management]

    D --> D1[本地存储<br/>Local Storage]
    D --> D2[对象存储<br/>Object Storage]
    D --> D3[云存储<br/>Cloud Storage]

    E --> E1[版本管理<br/>Versioning]
    E --> E2[生命周期<br/>Lifecycle]
    E --> E3[安全扫描<br/>Security]
    E --> E4[访问控制<br/>Access Control]

    C --> F[镜像拉取层]
    F --> G[镜像缓存<br/>Cache]
    F --> H[镜像代理<br/>Proxy]

    style A fill:#e1f5ff
    style C fill:#fff4e1
    style D fill:#e6ffe6
    style E fill:#ffe6e6
    style F fill:#f0e1ff
```

**镜像仓库层次定义**：

| 层次       | 定义     | 技术                       | 功能               |
| ---------- | -------- | -------------------------- | ------------------ |
| **构建层** | 镜像构建 | Dockerfile、BuildKit       | 镜像构建和推送     |
| **仓库层** | 镜像仓库 | Docker Registry、Harbor    | 镜像存储和管理     |
| **存储层** | 存储后端 | 本地存储、对象存储、云存储 | 实际镜像存储       |
| **管理层** | 镜像管理 | 版本管理、生命周期管理     | 镜像版本和生命周期 |
| **拉取层** | 镜像拉取 | 镜像缓存、镜像代理         | 镜像分发和优化     |

### 21.2.2 技术组件矩阵

**镜像仓库技术组件矩阵**：

| 组件类别     | 技术                  | 定位                 | 成熟度     | 生产验证   |
| ------------ | --------------------- | -------------------- | ---------- | ---------- |
| **镜像仓库** | Docker Registry       | 基础镜像仓库         | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Harbor                | 企业级镜像仓库       | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Nexus Repository      | 多格式仓库（含容器） | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Quay                  | Red Hat 镜像仓库     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | AWS ECR               | AWS 容器镜像仓库     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Azure ACR             | Azure 容器镜像仓库   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | GCP Artifact Registry | GCP 镜像仓库         | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Alibaba ACR           | 阿里云容器镜像仓库   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **镜像扫描** | Trivy                 | 开源镜像扫描工具     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Clair                 | CoreOS 镜像扫描      | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   |
|              | Aqua                  | 商业镜像扫描         | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Snyk                  | 开源安全扫描         | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **镜像签名** | Cosign                | CNCF 镜像签名工具    | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Notary                | Docker 镜像签名      | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   |
| **镜像管理** | Skopeo                | 镜像复制和管理工具   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
|              | Crane                 | Google 镜像管理工具  | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   |

### 21.2.3 技术栈组合

**镜像仓库技术栈组合方案**：

| 场景           | 镜像仓库               | 镜像扫描    | 镜像签名 | 特点               |
| -------------- | ---------------------- | ----------- | -------- | ------------------ |
| **小规模集群** | Docker Registry        | Trivy       | Cosign   | 简单易用、成本低   |
| **企业环境**   | Harbor                 | Trivy/Clair | Cosign   | 功能丰富、安全可靠 |
| **多云环境**   | Harbor + 云仓库        | Trivy       | Cosign   | 混合云支持、安全   |
| **云原生环境** | 云镜像仓库             | 云扫描      | 云签名   | 与云平台深度集成   |
| **边缘计算**   | Docker Registry + 同步 | Trivy       | Cosign   | 轻量级、离线支持   |

## 21.3 镜像仓库技术规格

### 21.3.1 Docker Registry 规格

**Docker Registry 规格**：

**定义**：Docker Registry 是开源的镜像仓库实现，符合 OCI Distribution 规范。

**技术特点**：

- ✅ 符合 OCI Distribution 规范
- ✅ 简单易部署
- ✅ 支持多种存储后端
- ✅ 轻量级
- ⚠️ 功能相对基础

**版本信息**：

- **最新版本**：v2.8.3+（2024）
- **GitHub Stars**：7K+
- **生产验证**：✅ 广泛使用

**存储后端支持**：

- **文件系统**：本地文件系统
- **S3**：AWS S3、MinIO
- **Azure**：Azure Blob Storage
- **GCS**：Google Cloud Storage
- **Swift**：OpenStack Swift

**配置示例**：

```yaml
version: 0.1
storage:
  filesystem:
    rootdirectory: /var/lib/registry
  s3:
    accesskey: YOUR_ACCESS_KEY
    secretkey: YOUR_SECRET_KEY
    region: us-east-1
    bucket: my-registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
```

### 21.3.2 Harbor 规格

**Harbor 规格**：

**定义**：Harbor 是 CNCF 的企业级镜像仓库，提供完整的镜像管理功能。

**技术特点**：

- ✅ 企业级功能
- ✅ 安全扫描集成
- ✅ RBAC 权限管理
- ✅ 镜像复制（多仓库同步）
- ✅ 镜像生命周期管理
- ✅ 与 Kubernetes 集成
- ✅ CNCF 项目

**版本信息**：

- **最新版本**：v2.11.0+（2024）
- **GitHub Stars**：22K+
- **生产验证**：✅ 大规模生产使用
- **CNCF 项目**：✅ 毕业项目

**核心组件**：

1. **Registry**：镜像仓库（Docker Registry）
2. **Core**：核心服务（API、UI）
3. **Job Service**：任务服务（扫描、复制）
4. **Trivy/Clair**：安全扫描
5. **Chart Museum**：Helm Chart 仓库（可选）
6. **Notary**：镜像签名（可选）

**功能特性**：

- ✅ 镜像管理（版本、标签、删除）
- ✅ 安全扫描（CVE 漏洞扫描）
- ✅ 镜像签名（Notary 集成）
- ✅ 镜像复制（多仓库同步）
- ✅ 访问控制（RBAC）
- ✅ 项目管理（多租户）
- ✅ 生命周期管理（自动清理）
- ✅ Webhook 通知

### 21.3.3 Nexus Repository 规格

**Nexus Repository 规格**：

**定义**：Nexus Repository 是 Sonatype 的仓库管理器，支持多种格式
（Maven、Docker、npm 等）。

**技术特点**：

- ✅ 多格式支持（Maven、Docker、npm、PyPI 等）
- ✅ 代理仓库（Proxy Repository）
- ✅ 私有仓库（Hosted Repository）
- ✅ 仓库组（Repository Group）
- ✅ 存储管理
- ⚠️ 商业版功能更丰富

**版本信息**：

- **最新版本**：Nexus 3.65.0+（2024）
- **GitHub Stars**：1K+
- **生产验证**：✅ 企业环境广泛使用

**Docker 仓库类型**：

- **Hosted Repository**：私有仓库
- **Proxy Repository**：代理仓库
- **Repository Group**：仓库组

### 21.3.4 Quay 规格

**Quay 规格**：

**定义**：Quay 是 Red Hat 的企业级镜像仓库。

**技术特点**：

- ✅ 企业级功能
- ✅ 安全扫描（Clair）
- ✅ 镜像签名
- ✅ 镜像复制
- ✅ 访问控制
- ✅ 与 OpenShift 集成
- ⚠️ 商业产品（有开源版本）

**版本信息**：

- **最新版本**：v3.12.0+（2024）
- **GitHub Stars**：2K+
- **生产验证**：✅ Red Hat 环境广泛使用

### 21.3.5 云镜像仓库规格

**云镜像仓库规格**：

**AWS ECR（Elastic Container Registry）**：

**技术特点**：

- ✅ 与 AWS 深度集成
- ✅ 自动镜像扫描
- ✅ IAM 权限控制
- ✅ 生命周期管理
- ✅ 加密存储

**版本信息**：

- **最新版本**：持续更新（2024）
- **生产验证**：✅ AWS 环境广泛使用

**Azure ACR（Azure Container Registry）**：

**技术特点**：

- ✅ 与 Azure 深度集成
- ✅ 自动镜像扫描
- ✅ Azure AD 权限控制
- ✅ 生命周期管理
- ✅ 加密存储

**版本信息**：

- **最新版本**：持续更新（2024）
- **生产验证**：✅ Azure 环境广泛使用

**GCP Artifact Registry**：

**技术特点**：

- ✅ 与 GCP 深度集成
- ✅ 自动镜像扫描
- ✅ IAM 权限控制
- ✅ 生命周期管理
- ✅ 加密存储

**版本信息**：

- **最新版本**：持续更新（2024）
- **生产验证**：✅ GCP 环境广泛使用

**Alibaba ACR**：

**技术特点**：

- ✅ 与阿里云深度集成
- ✅ 自动镜像扫描
- ✅ RAM 权限控制
- ✅ 生命周期管理
- ✅ 加密存储

**版本信息**：

- **最新版本**：持续更新（2024）
- **生产验证**：✅ 阿里云环境广泛使用

### 21.3.6 镜像仓库对比

**镜像仓库对比矩阵**：

| 镜像仓库                  | 定位             | 功能丰富度 | 易用性     | 安全性     | 成熟度     | 推荐场景       |
| ------------------------- | ---------------- | ---------- | ---------- | ---------- | ---------- | -------------- |
| **Docker Registry**       | 基础镜像仓库     | ⭐⭐⭐     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     | ⭐⭐⭐⭐⭐ | 简单场景、开发 |
| **Harbor**                | 企业级镜像仓库   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 企业环境、生产 |
| **Nexus Repository**      | 多格式仓库       | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | 多格式需求     |
| **Quay**                  | Red Hat 镜像仓库 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Red Hat 环境   |
| **AWS ECR**               | AWS 镜像仓库     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | AWS 云原生     |
| **Azure ACR**             | Azure 镜像仓库   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Azure 云原生   |
| **GCP Artifact Registry** | GCP 镜像仓库     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | GCP 云原生     |
| **Alibaba ACR**           | 阿里云镜像仓库   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 阿里云环境     |

## 21.4 镜像管理技术规格

### 21.4.1 镜像版本管理

**镜像版本管理规格**：

**版本策略**：

| 策略           | 说明                | 示例             | 适用场景 |
| -------------- | ------------------- | ---------------- | -------- |
| **语义化版本** | 使用语义化版本号    | `myapp:1.0.0`    | 生产环境 |
| **Git SHA**    | 使用 Git Commit SHA | `myapp:abc123`   | 开发环境 |
| **分支名**     | 使用分支名称        | `myapp:main`     | 持续集成 |
| **日期时间戳** | 使用日期时间戳      | `myapp:20240101` | 临时版本 |

**最佳实践**：

- ✅ 生产环境使用语义化版本
- ✅ 开发环境使用 Git SHA
- ✅ 避免使用 `latest` 标签
- ✅ 支持多版本并存

### 21.4.2 镜像标签策略

**镜像标签策略规格**：

**标签策略**：

- **固定标签**：`v1.0.0`、`v1.1.0`
- **浮动标签**：`latest`、`stable`、`dev`
- **多标签**：同一镜像多个标签（`v1.0.0`、`v1.0`、`v1`、`latest`）

**标签示例**：

```bash
# 构建镜像
docker build -t myapp:v1.0.0 -t myapp:v1.0 -t myapp:v1 -t myapp:latest .

# 推送多标签
docker push myapp:v1.0.0
docker push myapp:v1.0
docker push myapp:v1
docker push myapp:latest
```

### 21.4.3 镜像生命周期管理

**镜像生命周期管理规格**：

**生命周期阶段**：

1. **开发阶段**：频繁构建和推送
2. **测试阶段**：测试和验证
3. **发布阶段**：正式发布版本
4. **归档阶段**：旧版本归档
5. **清理阶段**：删除不再使用的镜像

**生命周期策略**：

- ✅ 保留最近 N 个版本
- ✅ 保留最近 N 天版本
- ✅ 自动删除未使用的镜像
- ✅ 手动归档重要版本

### 21.4.4 镜像清理策略

**镜像清理策略规格**：

**清理规则**：

- **按时间清理**：删除超过 N 天的镜像
- **按数量清理**：只保留最近 N 个版本
- **按使用情况清理**：删除未使用的镜像
- **按标签清理**：删除特定标签的镜像

**Harbor 清理策略示例**：

```yaml
apiVersion: v1
kind: CronJob
metadata:
  name: harbor-cleanup
spec:
  schedule: "0 2 * * *" # 每天凌晨 2 点
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: cleanup
              image: goharbor/harbor-jobservice
              command:
                - /harbor/cleanup.sh
              args:
                - --dry-run=false
                - --keep-days=30
                - --keep-tags=10
```

### 21.4.5 镜像垃圾回收

**镜像垃圾回收规格**：

**垃圾回收策略**：

- ✅ 删除未引用的 Blob
- ✅ 删除未使用的 Manifest
- ✅ 压缩存储空间
- ✅ 定期执行垃圾回收

**Docker Registry 垃圾回收**：

```bash
# 垃圾回收
docker exec registry registry garbage-collect /etc/docker/registry/config.yml

# 预览垃圾回收
docker exec registry registry garbage-collect --dry-run /etc/docker/registry/config.yml
```

**Harbor 垃圾回收**：

- ✅ 通过 Web UI 触发
- ✅ 通过 API 触发
- ✅ 定时任务执行

## 21.5 镜像安全技术规格

### 21.5.1 镜像扫描

**镜像扫描规格**：

**扫描工具**：

| 工具      | 定位         | CVE 数据库 | 性能       | 成熟度     | 推荐场景     |
| --------- | ------------ | ---------- | ---------- | ---------- | ------------ |
| **Trivy** | 开源扫描工具 | ✅         | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 大多数场景   |
| **Clair** | CoreOS 扫描  | ✅         | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   | Harbor 集成  |
| **Aqua**  | 商业扫描     | ✅         | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 企业安全需求 |
| **Snyk**  | 开源扫描     | ✅         | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | 开发环境     |

**Trivy 规格**：

**技术特点**：

- ✅ 快速扫描（< 10s）
- ✅ 支持多种镜像格式（Docker、OCI）
- ✅ 丰富的漏洞数据库
- ✅ CI/CD 集成
- ✅ Kubernetes 集成

**版本信息**：

- **最新版本**：v0.51.0+（2024）
- **GitHub Stars**：20K+
- **生产验证**：✅ 广泛使用

**使用示例**：

```bash
# 扫描镜像
trivy image myapp:v1.0.0

# CI/CD 集成
trivy image --exit-code 1 --severity CRITICAL,HIGH myapp:v1.0.0

# Kubernetes 集成
trivy k8s cluster --report summary
```

### 21.5.2 镜像签名

**镜像签名规格**：

**签名工具**：

| 工具       | 定位            | 标准支持 | 成熟度     | 推荐场景    |
| ---------- | --------------- | -------- | ---------- | ----------- |
| **Cosign** | CNCF 镜像签名   | ✅ OCI   | ⭐⭐⭐⭐⭐ | 云原生环境  |
| **Notary** | Docker 镜像签名 | ⚠️ 旧版  | ⭐⭐⭐⭐   | Docker 环境 |

**Cosign 规格**：

**技术特点**：

- ✅ CNCF 项目
- ✅ OCI 标准支持
- ✅ 与供应链工具集成
- ✅ 多种密钥类型支持

**版本信息**：

- **最新版本**：v2.2.0+（2024）
- **GitHub Stars**：4K+
- **生产验证**：✅ 广泛使用

**使用示例**：

```bash
# 签名镜像
cosign sign --key cosign.key myapp:v1.0.0

# 验证签名
cosign verify --key cosign.pub myapp:v1.0.0

# 密钥对生成
cosign generate-key-pair
```

### 21.5.3 镜像验证

**镜像验证规格**：

**验证策略**：

- ✅ 签名验证（Cosign）
- ✅ 扫描验证（Trivy）
- ✅ 策略验证（OPA、Kyverno）
- ✅ 准入控制（Admission Webhook）

**准入控制示例**：

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: image-validation
webhooks:
  - name: image-validation.example.com
    rules:
      - operations: ["CREATE", "UPDATE"]
        apiGroups: [""]
        apiVersions: ["v1"]
        resources: ["pods"]
    clientConfig:
      service:
        name: image-validator
        namespace: default
        path: /validate
```

### 21.5.4 访问控制

**访问控制规格**：

**访问控制策略**：

- ✅ 基于角色的访问控制（RBAC）
- ✅ 项目级别的访问控制
- ✅ 仓库级别的访问控制
- ✅ 标签级别的访问控制

**Harbor RBAC 示例**：

- **项目管理员**：完全控制项目
- **开发者**：推送和拉取镜像
- **访客**：只读访问

## 21.6 镜像分发技术规格

### 21.6.1 镜像拉取策略

**镜像拉取策略规格**：

**拉取策略**：

| 策略             | 说明             | 适用场景         |
| ---------------- | ---------------- | ---------------- |
| **Always**       | 总是拉取最新镜像 | 开发环境         |
| **IfNotPresent** | 本地不存在时拉取 | 生产环境（推荐） |
| **Never**        | 只使用本地镜像   | 离线环境         |

**配置示例**：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: app
      image: myapp:v1.0.0
      imagePullPolicy: IfNotPresent
```

### 21.6.2 镜像缓存

**镜像缓存规格**：

**缓存策略**：

- ✅ 节点级别缓存
- ✅ 集群级别缓存
- ✅ 代理缓存

**缓存工具**：

- **Docker Layer Caching**：Docker 本地缓存
- **Registry Mirror**：镜像仓库镜像
- **Harbor Proxy Cache**：Harbor 代理缓存

### 21.6.3 镜像同步

**镜像同步规格**：

**同步策略**：

- ✅ 多仓库同步
- ✅ 跨集群同步
- ✅ 边缘节点同步

**Harbor 镜像复制**：

- ✅ 推送模式（Push）
- ✅ 拉取模式（Pull）
- ✅ 定时同步
- ✅ 事件触发同步

### 21.6.4 镜像代理

**镜像代理规格**：

**代理策略**：

- ✅ 代理公共仓库（Docker Hub、gcr.io）
- ✅ 缓存代理
- ✅ 访问控制

**Docker Registry 代理配置**：

```yaml
version: 0.1
proxy:
  remoteurl: https://registry-1.docker.io
  username: YOUR_USERNAME
  password: YOUR_PASSWORD
```

## 21.7 镜像仓库技术栈组合方案

### 21.7.1 小规模集群组合

**小规模集群镜像仓库组合**：

**技术栈**：

- **镜像仓库**：Docker Registry
- **镜像扫描**：Trivy（CI/CD 集成）
- **镜像签名**：Cosign（可选）
- **访问控制**：基础认证

**特点**：

- ✅ 简单易用
- ✅ 资源占用低
- ✅ 成本低

### 21.7.2 大规模集群组合

**大规模集群镜像仓库组合**：

**技术栈**：

- **镜像仓库**：Harbor
- **镜像扫描**：Trivy/Clair（Harbor 集成）
- **镜像签名**：Cosign（Harbor 集成）
- **访问控制**：Harbor RBAC
- **镜像复制**：Harbor 镜像复制

**特点**：

- ✅ 功能丰富
- ✅ 安全可靠
- ✅ 企业级功能

### 21.7.3 多集群组合

**多集群镜像仓库组合**：

**技术栈**：

- **中心仓库**：Harbor
- **边缘仓库**：Docker Registry + Harbor 同步
- **镜像同步**：Harbor 镜像复制
- **镜像扫描**：Trivy
- **镜像签名**：Cosign

**特点**：

- ✅ 多集群管理
- ✅ 镜像同步
- ✅ 边缘支持

### 21.7.4 边缘计算组合

**边缘计算镜像仓库组合**：

**技术栈**：

- **中心仓库**：Harbor
- **边缘仓库**：Docker Registry（轻量级）
- **镜像同步**：Harbor 镜像复制 + 离线同步
- **镜像缓存**：边缘节点缓存
- **镜像扫描**：Trivy（中心）

**特点**：

- ✅ 轻量级部署
- ✅ 离线支持
- ✅ 边缘缓存

## 21.8 镜像管理最佳实践

### 21.8.1 镜像命名规范

**镜像命名规范**：

**命名格式**：

```text
<registry>/<namespace>/<image>:<tag>
```

**命名规则**：

- ✅ 使用小写字母和数字
- ✅ 使用连字符分隔（不使用下划线）
- ✅ 清晰的命名空间
- ✅ 语义化标签

**命名示例**：

```text
registry.example.com/myteam/myapp:v1.0.0
registry.example.com/myteam/myapp:v1.0.0-alpha.1
registry.example.com/myteam/myapp:abc123
```

### 21.8.2 镜像版本策略

**镜像版本策略**：

**版本策略**：

- ✅ 生产环境使用语义化版本（`v1.0.0`）
- ✅ 开发环境使用 Git SHA（`abc123`）
- ✅ 避免使用 `latest` 标签
- ✅ 支持多标签（`v1.0.0`、`v1.0`、`v1`）

### 21.8.3 镜像安全策略

**镜像安全策略**：

**安全策略**：

- ✅ 强制镜像扫描（CI/CD）
- ✅ 强制镜像签名（生产环境）
- ✅ 准入控制（Kubernetes）
- ✅ 定期更新基础镜像
- ✅ 最小权限原则

### 21.8.4 镜像优化策略

**镜像优化策略**：

**优化策略**：

- ✅ 多阶段构建（Multi-stage Build）
- ✅ 使用 .dockerignore
- ✅ 层缓存优化
- ✅ 基础镜像优化（Alpine、Distroless）
- ✅ 镜像压缩

## 21.9 参考

- [Docker Registry 文档](https://docs.docker.com/registry/)
- [Harbor 官方文档](https://goharbor.io/docs/)
- [Trivy 官方文档](https://aquasecurity.github.io/trivy/)
- [Cosign 官方文档](https://docs.sigstore.dev/cosign/)
- [OCI Distribution 规范](https://github.com/opencontainers/distribution-spec)
- [AWS ECR 文档](https://docs.aws.amazon.com/ecr/)
- [Azure ACR 文档](https://docs.microsoft.com/azure/container-registry/)
- [GCP Artifact Registry 文档](https://cloud.google.com/artifact-registry/docs)
