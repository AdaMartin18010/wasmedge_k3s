# 参考资料

## 📑 目录

- [📑 目录](#-目录)
- [📚 核心技术官方文档](#-核心技术官方文档)
  - [Docker](#docker)
  - [Kubernetes](#kubernetes)
  - [K3s](#k3s)
  - [WasmEdge](#wasmedge)
  - [OPA (Open Policy Agent)](#opa-open-policy-agent)
- [🌐 CNCF 生态系统](#-cncf-生态系统)
  - [CNCF 项目](#cncf-项目)
  - [网络技术](#网络技术)
  - [存储技术](#存储技术)
  - [监控与可观测性](#监控与可观测性)
  - [GitOps 和持续交付](#gitops-和持续交付)
  - [Operator 和 CRD](#operator-和-crd)
  - [镜像仓库](#镜像仓库)
  - [升级和迁移](#升级和迁移)
- [📖 书籍和教程](#-书籍和教程)
  - [容器技术](#容器技术)
  - [云原生](#云原生)
- [🎓 在线课程](#-在线课程)
  - [官方培训](#官方培训)
  - [在线平台](#在线平台)
- [📝 博客和文章](#-博客和文章)
  - [官方博客](#官方博客)
  - [技术社区](#技术社区)
- [🔧 工具和资源](#-工具和资源)
  - [命令行工具](#命令行工具)
  - [开发工具](#开发工具)
  - [测试工具](#测试工具)
- [📊 规范和标准](#-规范和标准)
  - [OCI 规范](#oci-规范)
  - [Kubernetes 规范](#kubernetes-规范)
  - [WebAssembly 规范](#webassembly-规范)
- [🎯 最佳实践](#-最佳实践)
  - [官方最佳实践](#官方最佳实践)
  - [社区实践](#社区实践)
- [🔍 研究论文](#-研究论文)
  - [分布式系统](#分布式系统)
  - [容器技术](#容器技术-1)
- [📅 会议和活动](#-会议和活动)
  - [CNCF 活动](#cncf-活动)
- [💡 社区资源](#-社区资源)
  - [GitHub 仓库](#github-仓库)
  - [论坛和社区](#论坛和社区)
- [🔗 相关链接](#-相关链接)
  - [认证](#认证)
  - [报告和白皮书](#报告和白皮书)

---

本文档收集云原生容器技术栈相关的所有外部参考资源。

## 📚 核心技术官方文档

### Docker

- **Docker 官方文档**：<https://docs.docker.com/>
- **Docker Hub**：<https://hub.docker.com/>
- **Docker GitHub**：<https://github.com/docker/docker>
- **OCI Image Spec**：<https://github.com/opencontainers/image-spec>
- **OCI Runtime Spec**：<https://github.com/opencontainers/runtime-spec>

### Kubernetes

- **Kubernetes 官方文档**：<https://kubernetes.io/docs/>
- **Kubernetes GitHub**：<https://github.com/kubernetes/kubernetes>
- **Kubernetes API 参
  考**：<https://kubernetes.io/docs/reference/kubernetes-api/>
- **kubectl 命令参考**：<https://kubernetes.io/docs/reference/kubectl/>
- **CNCF Kubernetes**：<https://www.cncf.io/projects/kubernetes/>

### K3s

- **K3s 官方文档**：<https://docs.k3s.io/>
- **K3s GitHub**：<https://github.com/k3s-io/k3s>
- **K3s 架构设计**：<https://docs.k3s.io/architecture>
- **K3s 安装要求**：<https://docs.k3s.io/installation/requirements>
- **K3s 快速入门**：<https://docs.k3s.io/quick-start>

### WasmEdge

- **WasmEdge 官方文档**：<https://wasmedge.org/docs/>
- **WasmEdge GitHub**：<https://github.com/WasmEdge/WasmEdge>
- **WasmEdge 性能基准**：<https://wasmedge.org/docs/>
- **WASI 标准**：<https://wasi.dev/>
- **WebAssembly 标准**：<https://webassembly.org/>

### OPA (Open Policy Agent)

- **OPA 官方文档**：<https://www.openpolicyagent.org/docs/>
- **OPA GitHub**：<https://github.com/open-policy-agent/opa>
- **OPA Wasm 支持**：<https://www.openpolicyagent.org/docs/latest/wasm/>
- **Rego 语言**：<https://www.openpolicyagent.org/docs/latest/policy-language/>
- **Gatekeeper**：<https://open-policy-agent.github.io/gatekeeper/>

## 🌐 CNCF 生态系统

### CNCF 项目

- **CNCF 项目清单**：<https://www.cncf.io/projects/>
- **CNCF 沙箱项目**：<https://www.cncf.io/sandbox-projects/>
- **CNCF 孵化项目**：<https://www.cncf.io/cncf-projects/>

### 网络技术

- **Flannel**：<https://github.com/flannel-io/flannel>
- **Calico**：<https://projectcalico.docs.tigera.io/>
- **Cilium**：<https://docs.cilium.io/>
- **CoreDNS**：<https://coredns.io/>
- **Traefik**：<https://doc.traefik.io/traefik/>

### 存储技术

- **CSI 规范**：<https://kubernetes-csi.github.io/docs/>
- **Longhorn**：<https://longhorn.io/docs/>
- **Ceph**：<https://docs.ceph.com/>
- **NFS**：<https://kubernetes.io/docs/concepts/storage/volumes/#nfs>

### 监控与可观测性

- **Prometheus**：<https://prometheus.io/docs/>
- **Grafana**：<https://grafana.com/docs/>
- **Loki**：<https://grafana.com/docs/loki/>
- **OpenTelemetry**：<https://opentelemetry.io/docs/>
- **Jaeger**：<https://www.jaegertracing.io/docs/>
- **Fluentd**：<https://docs.fluentd.org/>
- **Fluent Bit**：<https://docs.fluentbit.io/>
- **ELK Stack**：<https://www.elastic.co/guide/>

### GitOps 和持续交付

- **ArgoCD**：<https://argo-cd.readthedocs.io/>
- **Flux**：<https://fluxcd.io/docs/>
- **Helm**：<https://helm.sh/docs/>
- **Kustomize**：<https://kustomize.io/>
- **Tekton**：<https://tekton.dev/docs/>

### Operator 和 CRD

- **Operator SDK**：<https://sdk.operatorframework.io/>
- **Kubebuilder**：<https://book.kubebuilder.io/>
- **Prometheus
  Operator**：<https://github.com/prometheus-operator/prometheus-operator>
- **cert-manager**：<https://cert-manager.io/docs/>

### 镜像仓库

- **Harbor**：<https://goharbor.io/docs/>
- **Docker Registry**：<https://docs.docker.com/registry/>
- **Nexus Repository**：<https://help.sonatype.com/repomanager3>
- **Quay**：<https://access.redhat.com/products/red-hat-quay>
- **Cosign**：<https://github.com/sigstore/cosign>

### 升级和迁移

- **kubeadm**：<https://kubernetes.io/docs/reference/setup-tools/kubeadm/>
- **Velero**：<https://velero.io/docs/>
- **Kompose**：<https://kompose.io/>
- **Sonobuoy**：<https://sonobuoy.io/docs/>

## 📖 书籍和教程

### 容器技术

- **《Docker 实战》**
- **《Kubernetes 权威指南》**
- **《深入剖析 Kubernetes》**

### 云原生

- **《云原生应用架构实践》**
- **《微服务架构设计模式》**
- **《持续交付》**

## 🎓 在线课程

### 官方培训

- **Kubernetes 官方教程**：<https://kubernetes.io/docs/tutorials/>
- **CNCF 培训课程**：<https://www.cncf.io/certification/training/>

### 在线平台

- **Kubernetes 官方互动教
  程**：<https://kubernetes.io/docs/tutorials/kubernetes-basics/>

## 📝 博客和文章

### 官方博客

- **Kubernetes 博客**：<https://kubernetes.io/blog/>
- **CNCF 博客**：<https://www.cncf.io/blog/>
- **Docker 博客**：<https://www.docker.com/blog/>

### 技术社区

- **Medium Kubernetes 专栏**
- **InfoQ 云原生专栏**

## 🔧 工具和资源

### 命令行工具

- **kubectl**：<https://kubernetes.io/docs/reference/kubectl/>
- **k9s**：<https://k9scli.io/>
- **helm**：<https://helm.sh/docs/>
- **kustomize**：<https://kustomize.io/>

### 开发工具

- **VS Code Kubernetes 扩展**
- **IntelliJ Kubernetes 插件**

### 测试工具

- **Sonobuoy**：<https://sonobuoy.io/docs/>
- **kube-bench**：<https://github.com/aquasecurity/kube-bench>
- **kubescape**：<https://kubescape.io/>

## 📊 规范和标准

### OCI 规范

- **OCI Image Specification**：<https://github.com/opencontainers/image-spec>
- **OCI Runtime
  Specification**：<https://github.com/opencontainers/runtime-spec>
- **OCI Distribution
  Specification**：<https://github.com/opencontainers/distribution-spec>

### Kubernetes 规范

- **Kubernetes API 约
  定**：<https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md>
- **CNI 规范**：<https://github.com/containernetworking/cni>
- **CRI 规范**：<https://github.com/kubernetes/cri-api>
- **CSI 规范**：<https://kubernetes-csi.github.io/docs/>

### WebAssembly 规范

- **WebAssembly Core Specification**：<https://webassembly.github.io/spec/core/>
- **WASI**：<https://wasi.dev/>
- **WebAssembly System Interface**：<https://github.com/WebAssembly/WASI>

## 🎯 最佳实践

### 官方最佳实践

- **Kubernetes 最佳实
  践**：<https://kubernetes.io/docs/concepts/cluster-administration/>
- **容器最佳实践**：<https://docs.docker.com/develop/dev-best-practices/>

### 社区实践

- **12-Factor App**：<https://12factor.net/>
- **CNCF Cloud Native Trail
  Map**：<https://raw.githubusercontent.com/cncf/trailmap/master/CNCF_TrailMap_latest.png>

## 🔍 研究论文

### 分布式系统

- **Google Kubernetes 论文**
- **Borg 论文**

### 容器技术

- **Docker 容器技术研究**

## 📅 会议和活动

### CNCF 活动

- **KubeCon +
  CloudNativeCon**：<https://events.linuxfoundation.org/kubecon-cloudnativecon-europe/>
- **CNCF Webinar**

## 💡 社区资源

### GitHub 仓库

- **awesome-kubernetes**：<https://github.com/ramitsurana/awesome-kubernetes>
- **awesome-docker**：<https://github.com/veggiemonk/awesome-docker>
- **awesome-cloud-native**：<https://github.com/rootsongjc/awesome-cloud-native>

### 论坛和社区

- **Kubernetes Slack**：<https://kubernetes.slack.com/>
- **Stack Overflow Kubernetes 标签**
- **Reddit r/kubernetes**

## 🔗 相关链接

### 认证

- **CNCF 认证**：<https://www.cncf.io/certification/>
- **CKA (Certified Kubernetes Administrator)**
- **CKAD (Certified Kubernetes Application Developer)**
- **CKS (Certified Kubernetes Security Specialist)**

### 报告和白皮书

- **CNCF 年度报告**
- **Kubernetes 使用情况报告**

---

**最后更新**：2025-11-07

**维护者**：项目团队
