# 核心概念词典

> **创建日期**：2025-11-15
> **最后更新**：2025-11-15
> **维护者**：项目团队
> **状态**：持续更新

---

## 📑 目录

- [核心概念词典](#核心概念词典)
  - [📑 目录](#-目录)
  - [1. 词典概述](#1-词典概述)
  - [2. 虚拟化相关概念](#2-虚拟化相关概念)
    - [2.1 虚拟化（Virtualization）](#21-虚拟化virtualization)
    - [2.2 全虚拟化（Full Virtualization）](#22-全虚拟化full-virtualization)
    - [2.3 半虚拟化（Paravirtualization）](#23-半虚拟化paravirtualization)
    - [2.4 virtio](#24-virtio)
  - [3. 容器化相关概念](#3-容器化相关概念)
    - [3.1 容器化（Containerization）](#31-容器化containerization)
  - [4. 沙盒化相关概念](#4-沙盒化相关概念)
    - [4.1 沙盒化（Sandboxing）](#41-沙盒化sandboxing)
    - [4.2 gVisor](#42-gvisor)
    - [4.3 Firecracker](#43-firecracker)
    - [4.4 WebAssembly (WASM)](#44-webassembly-wasm)
  - [5. 编排相关概念](#5-编排相关概念)
    - [5.1 Kubernetes (K8s)](#51-kubernetes-k8s)
    - [5.2 K3s](#52-k3s)
  - [6. 运行时相关概念](#6-运行时相关概念)
    - [6.1 WasmEdge](#61-wasmedge)
  - [7. 策略相关概念](#7-策略相关概念)
    - [7.1 OPA (Open Policy Agent)](#71-opa-open-policy-agent)
  - [8. 可观测性相关概念](#8-可观测性相关概念)
    - [8.1 OpenTelemetry (OTLP)](#81-opentelemetry-otlp)
    - [8.2 eBPF](#82-ebpf)
  - [9. 概念关系说明](#9-概念关系说明)
    - [9.1 隔离层次关系](#91-隔离层次关系)
    - [9.2 技术本质差异](#92-技术本质差异)
  - [10. 参考资源](#10-参考资源)
    - [10.1 官方文档](#101-官方文档)
    - [10.2 标准组织](#102-标准组织)
    - [10.3 Wikipedia](#103-wikipedia)

---

## 1. 词典概述

本文档是 **wasmedge_k3s** 项目的**核心概念词典**，统一定义项目中使用的所有核心概念，确保概念定义的一致性和准确性。

**词典目标**：

- ✅ 统一概念定义，避免概念混淆
- ✅ 标注概念定义的来源（Wikipedia、官方文档、学术论文）
- ✅ 明确概念的外延边界
- ✅ 说明概念之间的关系

**词典结构**：

- 按技术领域分类（虚拟化、容器化、沙盒化等）
- 每个概念包含：定义、属性、关系、来源
- 标注概念定义的版本和更新时间

---

## 2. 虚拟化相关概念

### 2.1 虚拟化（Virtualization）

**定义**：通过软件模拟硬件功能，创建多个虚拟环境，每个虚拟环境可以运行独立的操作系统。

**项目定义**：

- 通过 hypervisor 虚拟化的计算单元，携带独立内核状态
- 形式化定义：`Φ: P → V`，物理机到虚拟机的虚拟化映射

**行业标准定义**：

- **Wikipedia**: "Virtualization is the act of creating a virtual (rather than actual) version of something, including virtual computer hardware platforms, storage devices, and computer network resources."
- **VMware**: "Virtualization is the process of creating a software-based, or virtual, representation of something, such as virtual applications, servers, storage and networks."

**属性**：

- 隔离级别：高（独立内核）
- 资源开销：高（128MB+ 内存）
- 启动时间：5-30s
- 兼容性：高（支持多种操作系统）

**关系**：

- 包含：全虚拟化、半虚拟化、硬件辅助虚拟化
- 被包含：L-1 全虚拟化层、L-2 半虚拟化层

**来源**：

- Wikipedia: [Virtualization](https://en.wikipedia.org/wiki/Virtualization)
- VMware: [What is Virtualization?](https://www.vmware.com/solutions/virtualization.html)

**最后更新**：2025-11-15

---

### 2.2 全虚拟化（Full Virtualization）

**定义**：不需要修改 Guest OS 的虚拟化技术，通过硬件辅助（VT-x、AMD-V）或二进制翻译实现。

**项目定义**：

- L-1 全虚拟化层：完整模拟硬件，Guest OS 无需修改

**行业标准定义**：

- **Wikipedia**: "Full virtualization is a virtualization technique used to provide a certain kind of virtual machine environment, namely, one that is a complete simulation of the underlying hardware."

**属性**：

- 隔离级别：最高（独立内核）
- 资源开销：高（128MB+ 内存）
- 启动时间：5-30s
- 兼容性：最高（支持所有操作系统）

**关系**：

- 属于：虚拟化
- 包含：KVM、ESXi、Hyper-V、Xen HVM
- 依赖：L-0 硬件辅助层

**来源**：

- Wikipedia: [Full Virtualization](https://en.wikipedia.org/wiki/Full_virtualization)

**最后更新**：2025-11-15

---

### 2.3 半虚拟化（Paravirtualization）

**定义**：需要修改 Guest OS 内核的虚拟化技术，通过优化的接口提高性能。

**项目定义**：

- L-2 半虚拟化层：Guest 内核需要修改，主动配合 Hypervisor，通过优化的接口提高性能

> **📌 重要说明**：半虚拟化的核心特征是**需要修改 Guest OS 内核**。virtio 虽然是一种半虚拟化 I/O 框架，但它**不需要修改 Guest OS 内核**，只需要安装驱动，因此 virtio 更准确地说是一种**I/O 虚拟化优化技术**，可以在全虚拟化和半虚拟化中使用。

**行业标准定义**：

- **Wikipedia**: "Paravirtualization is a virtualization technique that presents a software interface to virtual machines that is similar, but not identical, to that of the underlying hardware."

**属性**：

- 隔离级别：高（独立内核）
- 资源开销：中（64-128MB 内存）
- 启动时间：3-10s
- 兼容性：中（需要特定的 Guest OS 内核）

**关系**：

- 属于：虚拟化
- 包含：Xen PV、Hyper-V Enlightenment
- 依赖：L-0 硬件辅助层（可选）

**来源**：

- Wikipedia: [Paravirtualization](https://en.wikipedia.org/wiki/Paravirtualization)

**最后更新**：2025-11-15

---

### 2.4 virtio

**定义**：一种半虚拟化 I/O 框架，通过优化的接口提高 I/O 性能。

**项目定义**：

- virtio 是一种**半虚拟化 I/O 框架**，但**不是独立的隔离层次**
- virtio 的核心是 I/O 虚拟化优化技术，可以在全虚拟化（L-1）和半虚拟化（L-2）环境中使用

**行业标准定义**：

- **virtio 标准**: "virtio is a standardized interface for virtual I/O devices, designed to allow efficient (para-virtualized) I/O operations."

**属性**：

- 技术本质：I/O 虚拟化优化技术
- 是否需要修改 Guest OS 内核：否（只需要安装驱动）
- 适用场景：全虚拟化和半虚拟化的 I/O 优化

**关系**：

- 属于：I/O 虚拟化技术
- 可以在：L-1（全虚拟化）和 L-2（半虚拟化）中使用
- 包含：virtio-net、virtio-blk、vhost、vDPA

**来源**：

- virtio 标准文档：<https://docs.oasis-open.org/virtio/virtio/v1.1/csprd01/virtio-v1.1-csprd01.html>

**最后更新**：2025-11-15

---

## 3. 容器化相关概念

### 3.1 容器化（Containerization）

**定义**：在共享操作系统内核的基础上，将应用及其依赖封装，确保环境一致性。

**项目定义**：

- 共享宿主机内核的隔离进程组，仅包含用户态运行时
- 形式化定义：`Ψ: P → C`，物理机到容器的直接映射

**行业标准定义**：

- **Docker**: "A container is a standard unit of software that packages up code and all its dependencies so the application runs quickly and reliably from one computing environment to another."
- **OCI**: "A container is a runtime environment that provides isolation and resource management for applications."

**属性**：

- 隔离级别：中（进程级隔离）
- 资源开销：低（10-50MB 内存）
- 启动时间：1-5s
- 兼容性：高（共享内核）

**关系**：

- 属于：L-3 容器化层
- 包含：runc、containerd、Docker、Podman
- 依赖：Linux Namespace、Cgroup

**来源**：

- Docker: [What is a Container?](https://www.docker.com/resources/what-container/)
- OCI: [Open Container Initiative](https://opencontainers.org/)

**最后更新**：2025-11-15

---

## 4. 沙盒化相关概念

### 4.1 沙盒化（Sandboxing）

**定义**：为应用提供受限的执行环境，增强安全性。

**项目定义**：

- L-4 沙盒化层：在容器或 VM 基础上再增加一层隔离，通过用户态内核或字节码 VM 拦截系统调用

**行业标准定义**：

- **Wikipedia**: "Sandboxing is a security mechanism for separating running programs, usually in an effort to mitigate system failures or software vulnerabilities from spreading."

**属性**：

- 隔离级别：最高（syscall 过滤）
- 资源开销：极低（1-5MB 内存）
- 启动时间：<10ms
- 兼容性：中（需要特定的运行时）

**关系**：

- 属于：L-4 沙盒化层
- 包含：gVisor、Firecracker、WASM、Windows Sandbox

**来源**：

- Wikipedia: [Sandbox (Computer Security)](https://en.wikipedia.org/wiki/Sandbox_(computer_security))

**最后更新**：2025-11-15

---

### 4.2 gVisor

**定义**：Google 开发的用户态内核，在用户空间重新实现 Linux ABI，拦截所有系统调用。

**项目定义**：

- 用户态内核（Userspace Kernel）：在用户空间重新实现 Linux ABI，提供内核级隔离

**行业标准定义**：

- **gVisor 官方文档**: "gVisor is an application kernel, written in Go, that implements a substantial portion of the Linux system call interface."

**属性**：

- 技术本质：用户态内核（Userspace Kernel）
- 隔离机制：在用户空间重新实现 Linux ABI，拦截所有系统调用
- 适用场景：多租户 SaaS、容器安全增强

**关系**：

- 属于：L-4 沙盒化层
- 技术类型：用户态内核
- 包含：Sentry、Gofer、runsc

**来源**：

- gVisor 官方文档：<https://gvisor.dev/docs/>

**最后更新**：2025-11-15

---

### 4.3 Firecracker

**定义**：AWS 开发的轻量级 VMM（Micro-VM），基于 KVM 的极简虚拟机监控程序。

**项目定义**：

- 轻量级 VMM（Micro-VM）：基于 KVM 的极简虚拟机监控程序，提供 VM 级隔离

**行业标准定义**：

- **Firecracker 官方文档**: "Firecracker is an open source virtualization technology that is purpose-built for creating and managing secure, multi-tenant container and function-based services."

**属性**：

- 技术本质：轻量级 VMM（Micro-VM）
- 隔离机制：基于 KVM 的硬件虚拟化
- 适用场景：Serverless、边缘计算

**关系**：

- 属于：L-4 沙盒化层
- 技术类型：轻量级 VMM
- 包含：MicroVM、Jailer、vsock、MMDS

**来源**：

- Firecracker 官方文档：<https://firecracker-microvm.github.io/>

**最后更新**：2025-11-15

---

### 4.4 WebAssembly (WASM)

**定义**：一种低级的字节码格式，设计用于在 Web 浏览器和服务器环境中高效执行。

**项目定义**：

- 字节码运行时（Bytecode Runtime）：基于字节码验证和能力模型，不直接调用系统调用

**行业标准定义**：

- **W3C**: "WebAssembly (abbreviated Wasm) is a binary instruction format for a stack-based virtual machine."

**属性**：

- 技术本质：字节码运行时（Bytecode Runtime）
- 隔离机制：基于字节码验证和能力模型
- 适用场景：边缘计算、插件系统、跨平台应用

**关系**：

- 属于：L-4 沙盒化层
- 技术类型：字节码运行时
- 包含：WasmEdge、Wasmtime、WAMR

**来源**：

- W3C: [WebAssembly Specification](https://webassembly.org/)

**最后更新**：2025-11-15

---

## 5. 编排相关概念

### 5.1 Kubernetes (K8s)

**定义**：开源的容器编排平台，用于自动化部署、扩展和管理容器化应用。

**项目定义**：

- 容器编排平台，提供 Pod、Service、Deployment 等抽象

**行业标准定义**：

- **Kubernetes 官方文档**: "Kubernetes is an open-source system for automating deployment, scaling, and management of containerized applications."

**属性**：

- 类型：容器编排平台
- 功能：自动化部署、扩展、管理
- 适用场景：云原生应用、微服务架构

**关系**：

- 包含：Pod、Service、Deployment、StatefulSet
- 依赖：容器运行时（CRI）、网络插件（CNI）、存储插件（CSI）

**来源**：

- Kubernetes 官方文档：<https://kubernetes.io/docs/>

**最后更新**：2025-11-15

---

### 5.2 K3s

**定义**：轻量级的 Kubernetes 发行版，专为边缘计算和资源受限环境设计。

**项目定义**：

- Kubernetes 轻量级版本，适用于边缘计算、IoT、资源受限环境

**行业标准定义**：

- **K3s 官方文档**: "K3s is a lightweight Kubernetes distribution built for IoT & Edge computing."

**属性**：

- 类型：轻量级 Kubernetes 发行版
- 特点：资源占用小、启动快速、易于部署
- 适用场景：边缘计算、IoT、资源受限环境

**关系**：

- 属于：Kubernetes 发行版
- 兼容：Kubernetes API

**来源**：

- K3s 官方文档：<https://docs.k3s.io/>

**最后更新**：2025-11-15

---

## 6. 运行时相关概念

### 6.1 WasmEdge

**定义**：高性能的 WebAssembly 运行时，专为边缘计算和云原生应用设计。

**项目定义**：

- 云原生 Wasm 运行时，支持 Kubernetes RuntimeClass

**行业标准定义**：

- **WasmEdge 官方文档**: "WasmEdge is a lightweight, high-performance, and extensible WebAssembly runtime for cloud native, edge, and decentralized applications."

**属性**：

- 类型：WebAssembly 运行时
- 特点：高性能、轻量级、可扩展
- 适用场景：边缘计算、云原生应用

**关系**：

- 属于：WebAssembly 运行时
- 支持：WASI、Kubernetes RuntimeClass

**来源**：

- WasmEdge 官方文档：<https://wasmedge.org/docs/>

**最后更新**：2025-11-15

---

## 7. 策略相关概念

### 7.1 OPA (Open Policy Agent)

**定义**：开源的通用策略引擎，用于统一策略决策。

**项目定义**：

- 策略即代码引擎，支持 Rego 策略语言

**行业标准定义**：

- **OPA 官方文档**: "OPA is an open source, general-purpose policy engine that enables unified, context-aware policy enforcement across the entire stack."

**属性**：

- 类型：策略引擎
- 特点：通用、统一、上下文感知
- 适用场景：访问控制、资源配额、合规检查

**关系**：

- 支持：Rego 策略语言、Wasm 策略编译
- 集成：Kubernetes、Gatekeeper

**来源**：

- OPA 官方文档：<https://www.openpolicyagent.org/docs/>

**最后更新**：2025-11-15

---

## 8. 可观测性相关概念

### 8.1 OpenTelemetry (OTLP)

**定义**：开源的观测性框架，提供统一的指标、日志和追踪标准。

**项目定义**：

- 可观测性标准，提供 Metrics、Logging、Tracing 统一接口

**行业标准定义**：

- **OpenTelemetry 官方文档**: "OpenTelemetry is a collection of tools, APIs, and SDKs. Use it to instrument, generate, collect, and export telemetry data (metrics, logs, and traces) to help you analyze your software's performance and behavior."

**属性**：

- 类型：可观测性框架
- 功能：指标、日志、追踪
- 适用场景：分布式系统监控、性能分析

**关系**：

- 支持：OTLP 协议
- 集成：Prometheus、Jaeger、Grafana

**来源**：

- OpenTelemetry 官方文档：<https://opentelemetry.io/docs/>

**最后更新**：2025-11-15

---

### 8.2 eBPF

**定义**：Linux 内核的可编程技术，允许在内核空间运行沙盒程序。

**项目定义**：

- 内核可编程技术，用于网络加速、可观测性、服务网格、安全应用

**行业标准定义**：

- **eBPF 官方文档**: "eBPF is a revolutionary technology with origins in the Linux kernel that can run sandboxed programs in a privileged context such as the operating system kernel."

**属性**：

- 类型：内核可编程技术
- 功能：网络加速、可观测性、安全
- 适用场景：网络监控、性能分析、安全策略

**关系**：

- 支持：内核空间编程
- 集成：Cilium、Falco、BCC

**来源**：

- eBPF 官方文档：<https://ebpf.io/>

**最后更新**：2025-11-15

---

## 9. 概念关系说明

### 9.1 隔离层次关系

**五层隔离栈体系**：

- **L-0 硬件辅助层**：VT-x、AMD-V、SEV、TPM
- **L-1 全虚拟化层**：KVM、ESXi、Hyper-V、Xen HVM
- **L-2 半虚拟化层**：Xen PV、Hyper-V Enlightenment
  - **注意**：virtio 是 I/O 虚拟化优化技术，可以在 L-1 和 L-2 中使用
- **L-3 容器化层**：runc、containerd、Docker、Podman
- **L-4 沙盒化层**：gVisor（用户态内核）、Firecracker（轻量级 VMM）、WASM（字节码运行时）

### 9.2 技术本质差异

**三类沙盒化技术的本质差异**：

| 技术 | 技术本质 | 隔离机制 | 适用场景 |
|------|---------|---------|---------|
| **gVisor** | 用户态内核（Userspace Kernel） | 在用户空间重新实现 Linux ABI | 多租户 SaaS、容器安全增强 |
| **Firecracker** | 轻量级 VMM（Micro-VM） | 基于 KVM 的硬件虚拟化 | Serverless、边缘计算 |
| **WASM** | 字节码运行时（Bytecode Runtime） | 基于字节码验证和能力模型 | 边缘计算、插件系统、跨平台应用 |

---

## 10. 参考资源

### 10.1 官方文档

- **Kubernetes**: <https://kubernetes.io/docs/>
- **K3s**: <https://docs.k3s.io/>
- **WasmEdge**: <https://wasmedge.org/docs/>
- **OPA**: <https://www.openpolicyagent.org/docs/>
- **OpenTelemetry**: <https://opentelemetry.io/docs/>
- **eBPF**: <https://ebpf.io/>
- **gVisor**: <https://gvisor.dev/docs/>
- **Firecracker**: <https://firecracker-microvm.github.io/>

### 10.2 标准组织

- **CNCF**: <https://www.cncf.io/>
- **OCI**: <https://opencontainers.org/>
- **W3C**: <https://www.w3.org/>

### 10.3 Wikipedia

- [Virtualization](https://en.wikipedia.org/wiki/Virtualization)
- [Paravirtualization](https://en.wikipedia.org/wiki/Paravirtualization)
- [Container (Computer Science)](https://en.wikipedia.org/wiki/Container_(computer_science))
- [Sandbox (Computer Security)](https://en.wikipedia.org/wiki/Sandbox_(computer_security))

---

**最后更新**：2025-11-15
**维护者**：项目团队
**状态**：持续更新
