# 参考与扩展资源

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
- [2. 架构设计理论](#2-架构设计理论)
- [3. 架构建模](#3-架构建模)
- [4. 接口契约](#4-接口契约)
- [5. 服务网格](#5-服务网格)
- [6. 网络服务网格](#6-网络服务网格)
- [7. 可观测性](#7-可观测性)
- [8. 策略与安全](#8-策略与安全)
- [9. 部署与管理](#9-部署与管理)
- [10. 工作流与编排](#10-工作流与编排)
- [11. 虚拟化与容器化](#11-虚拟化与容器化)
- [12. 沙盒化](#12-沙盒化)
- [13. 资源与章节对应关系](#13-资源与章节对应关系)
- [14. 在线资源](#14-在线资源)
- [15. 社区与会议](#15-社区与会议)

---

## 1. 概述

本文档整理了架构设计、虚拟化、容器化、沙盒化、Service Mesh、OPA 等领域的**参考标
准、框架、工具和资源**，帮助架构师快速找到所需的技术资料和实践指南。

### 1.1 资源分类

- **📚 理论书籍**：架构设计、领域驱动设计等理论书籍
- **📐 建模标准**：C4、ArchiMate、UML 等建模标准
- **🔧 工具框架**：Istio、OPA、OpenTelemetry 等工具框架
- **📖 官方文档**：各项目的官方文档和最佳实践
- **🌐 在线资源**：博客、视频、教程等在线资源

---

## 2. 架构设计理论

### 2.1 经典书籍

| 资源                                                  | 作者             | 说明                       | 适用             |
| ----------------------------------------------------- | ---------------- | -------------------------- | ---------------- |
| **"Composite Architecture"**                          | Martin Fowler    | 说明如何把"组件"组合成系统 | 拆分 & 组合      |
| **"Domain-Driven Design"**                            | Eric Evans       | 领域驱动设计               | 领域边界、聚合根 |
| **"Patterns of Enterprise Application Architecture"** | Martin Fowler    | 常见架构模式               | 组合模式         |
| **"Building Microservices"**                          | Sam Newman       | 微服务架构设计             | 微服务拆分       |
| **"Microservices Patterns"**                          | Chris Richardson | 微服务模式与实践           | 微服务实践       |
| **"Designing Data-Intensive Applications"**           | Martin Kleppmann | 数据密集型应用设计         | 数据层设计       |

### 2.2 在线资源

- **Martin Fowler 博客**：<https://martinfowler.com>
- **DDD 社区**：<https://www.domainlanguage.com>
- **微服务模式**：<https://microservices.io>

---

## 3. 架构建模

### 3.1 建模标准

| 资源               | 说明             | 适用           | 链接                           |
| ------------------ | ---------------- | -------------- | ------------------------------ |
| **C4 Model**       | 层次化架构可视化 | 记录层次与接口 | <https://c4model.com>          |
| **ArchiMate**      | 企业架构建模语言 | 记录、沟通     | <https://archimate.org>        |
| **UML 2.5**        | 统一建模语言     | 记录、沟通     | <https://www.omg.org/spec/UML> |
| **4+1 View Model** | 多视角架构模型   | 多视角分析     | 学术论文                       |

### 3.2 建模工具

| 工具            | 说明           | 适用      | 链接                            |
| --------------- | -------------- | --------- | ------------------------------- |
| **Structurizr** | C4 模型工具    | C4 模型   | <https://structurizr.com>       |
| **Archi**       | ArchiMate 工具 | ArchiMate | <https://www.archimatetool.com> |
| **PlantUML**    | UML 图表生成   | UML 图表  | <https://plantuml.com>          |
| **Draw.io**     | 在线图表工具   | 架构图    | <https://app.diagrams.net>      |

### 3.3 ADR 工具

| 工具          | 说明           | 链接                                  |
| ------------- | -------------- | ------------------------------------- |
| **adr-tools** | ADR 命令行工具 | <https://github.com/npryce/adr-tools> |
| **adr-log**   | ADR 日志生成   | <https://github.com/adr/adr-log>      |

---

## 4. 接口契约

### 4.1 API 描述标准

| 资源                   | 说明              | 适用         | 链接                                             |
| ---------------------- | ----------------- | ------------ | ------------------------------------------------ |
| **OpenAPI**            | REST API 描述标准 | API 契约     | <https://www.openapis.org>                       |
| **gRPC**               | 高性能 RPC 框架   | 强类型接口   | <https://grpc.io>                                |
| **Protobuf**           | 数据序列化格式    | 接口契约     | <https://developers.google.com/protocol-buffers> |
| **GraphQL**            | 查询语言          | 灵活查询接口 | <https://graphql.org>                            |
| **OASIS OpenAPI Spec** | OpenAPI 官方规范  | API 描述标准 | <https://spec.openapis.org/oas/v3.1.0>           |

### 4.2 接口测试工具

| 工具         | 说明         | 链接                      |
| ------------ | ------------ | ------------------------- |
| **Postman**  | API 测试工具 | <https://www.postman.com> |
| **Insomnia** | API 客户端   | <https://insomnia.rest>   |
| **Pact**     | 契约测试工具 | <https://docs.pact.io>    |

---

## 5. 服务网格

### 5.1 Service Mesh 框架

| 资源                    | 说明                 | 适用           | 链接                    |
| ----------------------- | -------------------- | -------------- | ----------------------- |
| **Istio**               | 服务网格             | 流量治理、mTLS | <https://istio.io>      |
| **Linkerd**             | 轻量级服务网格       | 简单易用       | <https://linkerd.io>    |
| **Consul**              | 服务发现和配置       | 服务发现       | <https://www.consul.io> |
| **Kuma**                | 通用服务网格         | 多云、多集群   | <https://kuma.io>       |
| **Cilium Service Mesh** | 基于 eBPF 的服务网格 | 高性能         | <https://cilium.io>     |

### 5.2 相关标准

| 资源          | 说明               | 链接                                                                |
| ------------- | ------------------ | ------------------------------------------------------------------- |
| **Envoy API** | Envoy 代理 API     | <https://www.envoyproxy.io/docs/envoy/latest/api/api>               |
| **xDS 协议**  | Envoy 发现服务协议 | <https://www.envoyproxy.io/docs/envoy/latest/api-docs/xds_protocol> |

---

## 6. 网络服务网格

### 6.1 Network Service Mesh

| 资源                     | 说明             | 链接                                                       |
| ------------------------ | ---------------- | ---------------------------------------------------------- |
| **Network Service Mesh** | 跨域网络服务聚合 | <https://networkservicemesh.io>                            |
| **NSM 文档**             | NSM 官方文档     | <https://networkservicemesh.io/docs>                       |
| **NSM GitHub**           | NSM 源代码       | <https://github.com/networkservicemesh/networkservicemesh> |

---

## 7. 可观测性

### 7.1 可观测性标准

| 资源              | 说明         | 适用     | 链接                             |
| ----------------- | ------------ | -------- | -------------------------------- |
| **OpenTelemetry** | 统一遥测标准 | 统一监控 | <https://opentelemetry.io>       |
| **Prometheus**    | 指标采集     | 指标监控 | <https://prometheus.io>          |
| **Grafana**       | 可视化面板   | 监控展示 | <https://grafana.com>            |
| **Tempo**         | 分布式追踪   | 请求追踪 | <https://grafana.com/docs/tempo> |
| **Jaeger**        | 分布式追踪   | 请求追踪 | <https://www.jaegertracing.io>   |
| **Loki**          | 日志聚合     | 日志收集 | <https://grafana.com/docs/loki>  |

### 7.2 相关标准

| 资源            | 说明                               | 链接                     |
| --------------- | ---------------------------------- | ------------------------ |
| **OpenMetrics** | 指标标准                           | <https://openmetrics.io> |
| **OpenTracing** | 追踪标准（已合并到 OpenTelemetry） | <https://opentracing.io> |

---

## 8. 策略与安全

### 8.1 策略引擎

| 资源                        | 说明                | 适用            | 链接                                             |
| --------------------------- | ------------------- | --------------- | ------------------------------------------------ |
| **OPA (Open Policy Agent)** | 通用策略引擎        | 策略即代码      | <https://www.openpolicyagent.org>                |
| **Gatekeeper**              | Kubernetes 策略引擎 | Kubernetes 策略 | <https://open-policy-agent.github.io/gatekeeper> |
| **Kyverno**                 | Kubernetes 策略引擎 | Kubernetes 策略 | <https://kyverno.io>                             |

### 8.2 安全框架

| 资源                                | 说明                | 链接                                   |
| ----------------------------------- | ------------------- | -------------------------------------- |
| **Cloud-Native Security Framework** | CNCF 云原生安全框架 | <https://github.com/cncf/tag-security> |
| **SPIFFE**                          | 统一身份标识        | <https://spiffe.io>                    |
| **SPIRE**                           | SPIFFE 运行时环境   | <https://spiffe.io/spire>              |

---

## 9. 部署与管理

### 9.1 GitOps 工具

| 资源       | 说明            | 适用   | 链接                                 |
| ---------- | --------------- | ------ | ------------------------------------ |
| **ArgoCD** | GitOps 持续交付 | GitOps | <https://argoproj.github.io/argo-cd> |
| **Flux**   | GitOps 工具     | GitOps | <https://fluxcd.io>                  |
| **Tekton** | CI/CD 流水线    | CI/CD  | <https://tekton.dev>                 |

### 9.2 Kubernetes 管理工具

| 资源              | 说明                | 适用         | 链接                                       |
| ----------------- | ------------------- | ------------ | ------------------------------------------ |
| **Helm**          | Kubernetes 包管理   | K8s 组合     | <https://helm.sh>                          |
| **Kustomize**     | Kubernetes 配置管理 | K8s 组合     | <https://kustomize.io>                     |
| **Argo Rollouts** | 渐进式发布          | 蓝绿、金丝雀 | <https://argoproj.github.io/argo-rollouts> |

### 9.3 Infrastructure as Code

| 资源          | 说明           | 适用       | 链接                       |
| ------------- | -------------- | ---------- | -------------------------- |
| **Terraform** | 基础设施即代码 | 自动化部署 | <https://www.terraform.io> |
| **Pulumi**    | 基础设施即代码 | 自动化部署 | <https://www.pulumi.com>   |
| **Ansible**   | 配置管理       | 自动化部署 | <https://www.ansible.com>  |

### 9.4 CI/CD 工具

| 资源               | 说明  | 适用   | 链接                                  |
| ------------------ | ----- | ------ | ------------------------------------- |
| **GitHub Actions** | CI/CD | 自动化 | <https://github.com/features/actions> |
| **Jenkins**        | CI/CD | 自动化 | <https://www.jenkins.io>              |
| **GitLab CI/CD**   | CI/CD | 自动化 | <https://docs.gitlab.com/ee/ci>       |

---

## 10. 工作流与编排

### 10.1 工作流引擎

| 资源               | 说明       | 适用         | 链接                                        |
| ------------------ | ---------- | ------------ | ------------------------------------------- |
| **Argo Workflows** | 工作流引擎 | 业务流程     | <https://argoproj.github.io/argo-workflows> |
| **Temporal**       | 工作流引擎 | Saga、长事务 | <https://temporal.io>                       |
| **Camunda**        | 工作流引擎 | 业务流程     | <https://camunda.com>                       |

---

## 11. 虚拟化与容器化

### 11.1 虚拟化技术

| 资源               | 说明             | 适用   | 链接                                                                 |
| ------------------ | ---------------- | ------ | -------------------------------------------------------------------- |
| **KVM**            | Linux 内核虚拟化 | 虚拟化 | <https://www.linux-kvm.org>                                          |
| **Xen**            | 虚拟化监控器     | 虚拟化 | <https://xenproject.org>                                             |
| **Hyper-V**        | Windows 虚拟化   | 虚拟化 | <https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows> |
| **VMware vSphere** | 企业虚拟化       | 虚拟化 | <https://www.vmware.com/products/vsphere.html>                       |

### 11.2 容器化技术

| 资源           | 说明                  | 适用       | 链接                     |
| -------------- | --------------------- | ---------- | ------------------------ |
| **Docker**     | 容器平台              | 容器化     | <https://www.docker.com> |
| **Kubernetes** | 容器编排              | 编排       | <https://kubernetes.io>  |
| **containerd** | 容器运行时            | 容器运行时 | <https://containerd.io>  |
| **CRI-O**      | Kubernetes 容器运行时 | 容器运行时 | <https://cri-o.io>       |

### 11.3 容器标准

| 资源                 | 说明           | 链接                                             |
| -------------------- | -------------- | ------------------------------------------------ |
| **OCI Image Spec**   | 容器镜像标准   | <https://github.com/opencontainers/image-spec>   |
| **OCI Runtime Spec** | 容器运行时标准 | <https://github.com/opencontainers/runtime-spec> |
| **CNCF Landscape**   | CNCF 项目全景  | <https://landscape.cncf.io>                      |

---

## 12. 沙盒化

### 12.1 沙盒技术

| 资源                | 说明               | 适用   | 链接                                      |
| ------------------- | ------------------ | ------ | ----------------------------------------- |
| **gVisor**          | 用户态内核         | 沙盒化 | <https://gvisor.dev>                      |
| **Firecracker**     | 轻量级 VMM         | 沙盒化 | <https://firecracker-micrownvm.github.io> |
| **Kata Containers** | VM 容器            | 沙盒化 | <https://katacontainers.io>               |
| **WasmEdge**        | WebAssembly 运行时 | 沙盒化 | <https://wasmedge.org>                    |

### 12.2 安全技术

| 资源         | 说明               | 链接                         |
| ------------ | ------------------ | ---------------------------- |
| **seccomp**  | Linux 系统调用过滤 | Linux man page               |
| **eBPF**     | Linux 内核可编程   | <https://ebpf.io>            |
| **AppArmor** | Linux 安全模块     | <https://apparmor.net>       |
| **SELinux**  | Linux 安全模块     | <https://selinuxproject.org> |

---

## 13. 资源与章节对应关系

### 13.1 架构拆解与组合

| 章节               | 对应资源                                                  |
| ------------------ | --------------------------------------------------------- |
| 5 步拆分与组合流程 | Martin Fowler "Composite Architecture"、DDD by Eric Evans |
| 组合模式           | "Patterns of Enterprise Application Architecture"         |
| 接口契约           | OpenAPI、gRPC、Protobuf                                   |
| 架构建模           | C4 Model、ArchiMate                                       |

### 13.2 Service Mesh 与 NSM

| 章节         | 对应资源                      |
| ------------ | ----------------------------- |
| Service Mesh | Istio、Linkerd、Consul        |
| NSM          | Network Service Mesh 官方文档 |
| 流量治理     | Envoy API、xDS 协议           |

### 13.3 OPA 策略治理

| 章节       | 对应资源                                |
| ---------- | --------------------------------------- |
| OPA 架构   | OPA 官方文档                            |
| 策略即代码 | Gatekeeper、Kyverno                     |
| 安全框架   | Cloud-Native Security Framework、SPIFFE |

### 13.4 动态运维

| 章节     | 对应资源                           |
| -------- | ---------------------------------- |
| GitOps   | ArgoCD、Flux                       |
| 可观测性 | OpenTelemetry、Prometheus、Grafana |
| CI/CD    | GitHub Actions、Jenkins、Tekton    |

### 13.5 虚拟化容器化沙盒化

| 章节   | 对应资源                             |
| ------ | ------------------------------------ |
| 虚拟化 | KVM、Xen、Hyper-V                    |
| 容器化 | Docker、Kubernetes、OCI 标准         |
| 沙盒化 | gVisor、Firecracker、Kata Containers |

---

## 14. 在线资源

### 14.1 博客与文章

- **CNCF Blog**：<https://www.cncf.io/blog>
- **Kubernetes Blog**：<https://kubernetes.io/blog>
- **Istio Blog**：<https://istio.io/latest/news>
- **Martin Fowler Blog**：<https://martinfowler.com>

### 14.2 视频教程

- **Kubernetes 官方教程**：<https://kubernetes.io/docs/tutorials>
- **CNCF 视频库**：<https://www.cncf.io/videos>
- **Istio 官方教程**：<https://istio.io/latest/docs/setup/getting-started>

### 14.3 在线课程

- **Kubernetes 课程**：<https://www.udemy.com/topic/kubernetes>
- **Docker 课程**：<https://www.udemy.com/topic/docker>
- **微服务架构课程**：<https://www.coursera.org>

---

## 15. 社区与会议

### 15.1 开源社区

- **CNCF**：<https://www.cncf.io>
- **Kubernetes 社区**：<https://kubernetes.io/community>
- **Istio 社区**：<https://github.com/istio/community>
- **OPA 社区**：<https://www.openpolicyagent.org/docs/latest>

### 15.2 会议

- **KubeCon +
  CloudNativeCon**：<https://www.cncf.io/kubecon-cloudnativecon-events>
- **IstioCon**：<https://events.istio.io>
- **DockerCon**：<https://www.docker.com/dockercon>

### 15.3 本地用户组

- **Kubernetes 本地用户组**：<https://www.meetup.com/topics/kubernetes>
- **CNCF 本地用户组**：<https://www.cncf.io/local>

---

## 16. 工具推荐

### 16.1 开发工具

| 工具              | 说明       | 链接                             |
| ----------------- | ---------- | -------------------------------- |
| **VS Code**       | 代码编辑器 | <https://code.visualstudio.com>  |
| **IntelliJ IDEA** | Java IDE   | <https://www.jetbrains.com/idea> |
| **GoLand**        | Go IDE     | <https://www.jetbrains.com/go>   |

### 16.2 测试工具

| 工具        | 说明         | 链接                        |
| ----------- | ------------ | --------------------------- |
| **k6**      | 性能测试工具 | <https://k6.io>             |
| **JMeter**  | 负载测试工具 | <https://jmeter.apache.org> |
| **Gatling** | 性能测试工具 | <https://gatling.io>        |

### 16.3 监控工具

| 工具           | 说明       | 链接                           |
| -------------- | ---------- | ------------------------------ |
| **Prometheus** | 指标采集   | <https://prometheus.io>        |
| **Grafana**    | 可视化面板 | <https://grafana.com>          |
| **Jaeger**     | 分布式追踪 | <https://www.jaegertracing.io> |

---

## 16. 学术资源与参考标准

### 16.1 Wikipedia 标准定义

详细内容请参考 [`ACADEMIC-REFERENCES.md`](ACADEMIC-REFERENCES.md) 文档，包含：

- **Von Neumann Architecture**：冯·诺依曼架构标准定义
- **Virtualization**：虚拟化技术标准定义
- **Containerization**：容器化技术标准定义
- **Sandboxing**：沙盒化技术标准定义
- **Service Mesh**：服务网格标准定义
- **OPA**：Open Policy Agent 标准定义

### 16.2 著名大学课程

- **MIT 6.824**：分布式系统课程
- **MIT 6.033**：计算机系统工程课程
- **Stanford CS 244b**：分布式系统课程
- **Stanford CS 140**：操作系统课程
- **CMU 15-445**：数据库系统课程
- **CMU 15-410**：操作系统设计与实现课程
- **UC Berkeley CS 162**：操作系统课程
- **UC Berkeley CS 294**：分布式系统课程

### 16.3 学术论文

- **Xen and the Art of Virtualization** (SOSP 2003)
- **KVM: the Linux Virtual Machine Monitor** (Linux Symposium 2007)
- **In Search of an Understandable Consensus Algorithm** (USENIX ATC 2014)

详细学术资源请参考 [`ACADEMIC-REFERENCES.md`](ACADEMIC-REFERENCES.md)。

---

## 17. 总结

本文档整理了架构设计、虚拟化、容器化、沙盒化、Service Mesh、OPA 等领域的参考资源
，帮助架构师快速找到所需的技术资料和实践指南。

### 17.1 资源使用建议

1. **理论学习**：从经典书籍开始，理解架构设计理论
2. **实践应用**：参考官方文档和最佳实践，应用到实际项目
3. **社区参与**：参与开源社区，获取最新动态和帮助
4. **持续学习**：关注博客、视频、会议，持续学习新技术

### 17.2 资源更新

- 本文档会定期更新，添加最新的资源链接
- 如有遗漏或错误，欢迎提交 Issue 或 PR

---

**参考资源**：

- [架构拆解与组合：5 步流程](./architecture-view/01-decomposition-composition/01-5-step-process.md)
- [分层拆解：9 层架构模型](./architecture-view/01-decomposition-composition/02-layered-decomposition.md)
- [组合模式](./architecture-view/01-decomposition-composition/03-composition-patterns.md)
- [接口与契约](./architecture-view/01-decomposition-composition/04-interfaces-contracts.md)

---

**更新时间**：2025-11-04 **版本**：v1.0 **参考**：`architecture_view.md` 第
190-207 行
