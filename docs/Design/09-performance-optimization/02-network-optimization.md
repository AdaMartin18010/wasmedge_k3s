# 13.2 网络性能优化

> **文档版本**：v1.0 **最后更新**：2025-11-10 **维护者**：项目团队

---

## 📑 目录

- [13.2 网络性能优化](#132-网络性能优化)
  - [📑 目录](#-目录)
  - [概述](#概述)
  - [问题描述](#问题描述)
  - [优化方案对比](#优化方案对比)
  - [API 配置示例](#api-配置示例)
    - [1. SR-IOV 网络直通配置](#1-sr-iov-网络直通配置)
    - [2. DPDK 加速配置](#2-dpdk-加速配置)
    - [3. Multiqueue 配置](#3-multiqueue-配置)
    - [4. HostNetwork 配置](#4-hostnetwork-配置)
  - [相关文档](#相关文档)

---

## 概述

本文档分析网络性能优化的方案和方法，展示如何通过 SR-IOV 直通、DPDK 加速等技术优
化虚拟机网络性能。

## 问题描述

**问题**：虚拟机网络性能相比容器下降 20-30%，如何优化？

**影响**：

- 网络延迟增加
- 吞吐量下降
- 用户体验差

## 优化方案对比

| **方案**        | **实现技术**      | **性能提升** | **适用场景**   |
| --------------- | ----------------- | ------------ | -------------- |
| **SR-IOV 直通** | PCI 设备直通      | 性能+90%     | 高性能网络需求 |
| **DPDK 加速**   | 用户态网络栈      | 性能+60%     | 高吞吐场景     |
| **Multiqueue**  | 多队列 virtio-net | 性能+40%     | 多核 CPU 场景  |
| **HostNetwork** | 共享宿主机网络    | 性能+30%     | 低隔离要求     |

---

## API 配置示例

### 1. SR-IOV 网络直通配置

```yaml
# SR-IOV网络直通配置
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: high-performance-vm
spec:
  template:
    spec:
      domain:
        devices:
          interfaces:
            - name: sriov-net
              sriov: {}
              # SR-IOV网络资源
              resources:
                requests:
                  intel.com/sriov: "1"
      networks:
        - name: sriov-net
          multus:
            networkName: sriov-network
---
# NetworkAttachmentDefinition (SR-IOV)
apiVersion: k8s.cni.cncf.io/v1
kind: NetworkAttachmentDefinition
metadata:
  name: sriov-network
spec:
  config: |
    {
      "type": "sriov",
      "cniVersion": "0.3.1",
      "vlan": 100,
      "ipam": {
        "type": "host-local",
        "subnet": "10.56.0.0/16"
      }
    }
```

### 2. DPDK 加速配置

```yaml
# DPDK 加速配置
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: dpdk-vm
spec:
  template:
    spec:
      domain:
        devices:
          interfaces:
            - name: dpdk-net
              bridge: {}
              # DPDK 加速
              dpdk: {}
      networks:
        - name: dpdk-net
          multus:
            networkName: dpdk-network
```

### 3. Multiqueue 配置

```yaml
# Multiqueue 配置
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: multiqueue-vm
spec:
  template:
    spec:
      domain:
        devices:
          interfaces:
            - name: default
              masquerade: {}
              # Multiqueue
              queueCount: 4
      networks:
        - name: default
          pod: {}
```

### 4. HostNetwork 配置

```yaml
# HostNetwork 配置
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: hostnetwork-vm
spec:
  template:
    spec:
      hostNetwork: true
      domain:
        devices:
          interfaces:
            - name: default
              bridge: {}
      networks:
        - name: default
          pod: {}
```

---

## 相关文档

- [核心功能架构矩阵对比](../01-core-architecture/01-architecture-matrix.md) - 功
  能域对比矩阵
- [虚拟机冷启动优化](../09-performance-optimization/01-cold-start-optimization.md) -
  冷启动优化
- [存储 IO 优化](../09-performance-optimization/03-storage-io-optimization.md) -
  存储 IO 优化

---

**最后更新**：2025-11-10 **维护者**：项目团队
