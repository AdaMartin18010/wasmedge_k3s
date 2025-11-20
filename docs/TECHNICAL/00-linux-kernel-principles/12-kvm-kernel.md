# 12. KVM 内核机制

## 📑 目录

- [12. KVM 内核机制](#12-kvm-内核机制)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 KVM 的作用](#11-kvm-的作用)
    - [1.2 KVM 架构](#12-kvm-架构)
  - [2 虚拟化扩展](#2-虚拟化扩展)
    - [2.1 Intel VT-x](#21-intel-vt-x)
    - [2.2 AMD-V](#22-amd-v)
    - [2.3 虚拟化扩展检查](#23-虚拟化扩展检查)
  - [3 KVM 架构](#3-kvm-架构)
    - [3.1 KVM 模块结构](#31-kvm-模块结构)
    - [3.2 /dev/kvm 接口](#32-devkvm-接口)
    - [3.3 VM 数据结构](#33-vm-数据结构)
  - [4 VM 创建与管理](#4-vm-创建与管理)
    - [4.1 VM 创建](#41-vm-创建)
    - [4.2 VCPU 创建](#42-vcpu-创建)
    - [4.3 VM 运行](#43-vm-运行)
  - [5 内存虚拟化](#5-内存虚拟化)
    - [5.1 EPT/NPT](#51-eptnpt)
    - [5.2 内存映射](#52-内存映射)
    - [5.3 内存管理](#53-内存管理)
  - [6 虚拟中断处理](#6-虚拟中断处理)
    - [6.1 中断注入](#61-中断注入)
    - [6.2 中断路由](#62-中断路由)
    - [6.3 虚拟中断控制器](#63-虚拟中断控制器)
  - [7 设备模拟](#7-设备模拟)
    - [7.1 设备模型](#71-设备模型)
    - [7.2 I/O 处理](#72-io-处理)
    - [7.3 设备直通](#73-设备直通)
  - [8 与容器化的关系](#8-与容器化的关系)
    - [8.1 Kata Containers](#81-kata-containers)
    - [8.2 Firecracker](#82-firecracker)
    - [8.3 gVisor](#83-gvisor)
  - [9 相关文档](#9-相关文档)
    - [9.1 详细机制文档](#91-详细机制文档)
    - [9.2 架构分析](#92-架构分析)
    - [9.3 实现细节](#93-实现细节)

---

## 1 概述

**KVM（Kernel-based Virtual Machine）** 是 Linux 内核的虚拟化模块，利用硬件虚拟化扩展（Intel VT-x、AMD-V）提供完整的虚拟化功能。

### 1.1 KVM 的作用

- **CPU 虚拟化**：利用硬件虚拟化扩展实现 CPU 虚拟化
- **内存虚拟化**：使用 EPT/NPT 实现内存虚拟化
- **I/O 虚拟化**：与 QEMU 配合实现设备模拟
- **VM 管理**：提供 VM 创建、运行、管理的接口

### 1.2 KVM 架构

**KVM 架构**：

```
用户空间（QEMU）
    │
    ├── /dev/kvm（KVM 接口）
    │
内核空间（KVM 模块）
    │
    ├── VM 管理
    ├── VCPU 调度
    ├── 内存虚拟化（EPT/NPT）
    └── 中断处理
    │
硬件层（VT-x/AMD-V）
```

---

## 2 虚拟化扩展

### 2.1 Intel VT-x

**Intel VT-x 特性**：

- **VMX（Virtual Machine Extensions）**：CPU 虚拟化扩展
- **VMCS（Virtual Machine Control Structure）**：VM 控制结构
- **EPT（Extended Page Tables）**：扩展页表，内存虚拟化
- **VMX Root/Non-Root 模式**：Hypervisor 和 Guest 模式

**VMCS 结构**：

```c
// arch/x86/include/asm/vmx.h
// VMCS 字段（简化）
struct vmcs {
    u32 revision_id;
    u32 abort;
    // Guest 状态
    u64 guest_rip;
    u64 guest_rsp;
    // Host 状态
    u64 host_rip;
    u64 host_rsp;
    // 控制字段
    u32 pin_based_exec_ctrl;
    u32 cpu_based_exec_ctrl;
    // ...
};
```

### 2.2 AMD-V

**AMD-V 特性**：

- **SVM（Secure Virtual Machine）**：AMD 虚拟化扩展
- **VMCB（Virtual Machine Control Block）**：VM 控制块
- **NPT（Nested Page Tables）**：嵌套页表，内存虚拟化
- **Host/Guest 模式**：Hypervisor 和 Guest 模式

**VMCB 结构**：

```c
// arch/x86/include/asm/svm.h
// VMCB 结构（简化）
struct vmcb {
    struct vmcb_control_area control;
    struct vmcb_save_area save;
};

struct vmcb_control_area {
    u16 intercept_cr_read;
    u16 intercept_cr_write;
    u32 intercept_exceptions;
    // ...
};

struct vmcb_save_area {
    u64 rax;
    u64 rbx;
    u64 rcx;
    u64 rdx;
    // ...
};
```

### 2.3 虚拟化扩展检查

**检查 CPU 虚拟化支持**：

```c
// arch/x86/kvm/x86.c
// 检查 Intel VT-x
static int hardware_setup(void) {
    if (cpu_has_vmx()) {
        // 支持 Intel VT-x
        kvm_x86_ops = &vmx_x86_ops;
        return 0;
    }

    // 检查 AMD-V
    if (cpu_has_svm()) {
        // 支持 AMD-V
        kvm_x86_ops = &svm_x86_ops;
        return 0;
    }

    return -ENODEV;
}
```

---

## 3 KVM 架构

### 3.1 KVM 模块结构

**KVM 模块初始化**：

```c
// virt/kvm/kvm_main.c
static int __init kvm_init(void) {
    int r;
    int cpu;

    // 注册字符设备
    r = misc_register(&kvm_dev);
    if (r) {
        pr_err("kvm: misc device register failed\n");
        return r;
    }

    // 初始化硬件相关代码
    r = kvm_arch_init();
    if (r)
        goto out_unreg;

    // 注册 CPU 热插拔回调
    register_cpu_notifier(&kvm_cpu_notifier);

    return 0;

out_unreg:
    misc_deregister(&kvm_dev);
    return r;
}
```

### 3.2 /dev/kvm 接口

**/dev/kvm 设备文件**：

```c
// virt/kvm/kvm_main.c
static struct miscdevice kvm_dev = {
    KVM_MINOR,
    "kvm",
    &kvm_chardev_ops,
};

static long kvm_dev_ioctl(struct file *filp,
                          unsigned int ioctl, unsigned long arg) {
    long r = -EINVAL;

    switch (ioctl) {
    case KVM_GET_API_VERSION:
        r = KVM_API_VERSION;
        break;
    case KVM_CREATE_VM:
        r = kvm_dev_ioctl_create_vm(arg);
        break;
    case KVM_CHECK_EXTENSION:
        r = kvm_vm_ioctl_check_extension_generic(NULL, arg);
        break;
    case KVM_GET_VCPU_MMAP_SIZE:
        r = PAGE_SIZE;
        break;
    default:
        r = -EINVAL;
    }

    return r;
}
```

**KVM IOCTL 接口**：

- **KVM_CREATE_VM**：创建 VM
- **KVM_CREATE_VCPU**：创建 VCPU
- **KVM_RUN**：运行 VCPU
- **KVM_SET_MEMORY_REGION**：设置内存区域
- **KVM_GET_REGS**：获取寄存器
- **KVM_SET_REGS**：设置寄存器

### 3.3 VM 数据结构

**kvm 结构**：

```c
// include/linux/kvm_host.h
struct kvm {
    spinlock_t mmu_lock;
    struct mutex slots_lock;
    struct mm_struct *mm;
    struct kvm_memslots __rcu *memslots[KVM_ADDRESS_SPACE_NUM];
    struct kvm_vcpu *vcpus[KVM_MAX_VCPUS];
    atomic_t online_vcpus;
    int created_vcpus;
    int last_boosted_vcpu;
    struct list_head vm_list;
    struct mutex lock;
    struct kvm_io_bus __rcu *buses[KVM_NR_BUSES];
    // ...
};
```

**kvm_vcpu 结构**：

```c
// include/linux/kvm_host.h
struct kvm_vcpu {
    struct kvm *kvm;
    int vcpu_id;
    int cpu;
    struct kvm_run *run;
    int guest_mode;
    struct mutex mutex;
    struct kvm_vcpu_arch arch;
    // ...
};
```

---

## 4 VM 创建与管理

### 4.1 VM 创建

**VM 创建流程**：

```c
// virt/kvm/kvm_main.c
static int kvm_dev_ioctl_create_vm(unsigned long type) {
    struct kvm *kvm;
    struct file *file;
    int fd, r;

    // 创建 KVM 结构
    kvm = kvm_create_vm(type);
    if (IS_ERR(kvm))
        return PTR_ERR(kvm);

    // 创建文件描述符
    fd = anon_inode_getfd("kvm-vm", &kvm_vm_fops, kvm, O_RDWR | O_CLOEXEC);
    if (fd < 0) {
        kvm_destroy_vm(kvm);
        return fd;
    }

    return fd;
}

struct kvm *kvm_create_vm(unsigned long type) {
    struct kvm *kvm = kvm_arch_alloc_vm();

    // 初始化内存槽
    r = kvm_init_mmu_notifier(kvm);

    // 初始化其他组件
    r = kvm_arch_init_vm(kvm, type);

    return kvm;
}
```

### 4.2 VCPU 创建

**VCPU 创建流程**：

```c
// virt/kvm/kvm_main.c
static int kvm_vm_ioctl_create_vcpu(struct kvm *kvm, u32 id) {
    struct kvm_vcpu *vcpu;
    int r;

    // 创建 VCPU
    vcpu = kvm_arch_vcpu_create(kvm, id);
    if (IS_ERR(vcpu))
        return PTR_ERR(vcpu);

    // 初始化 VCPU
    r = kvm_arch_vcpu_setup(vcpu);
    if (r)
        goto vcpu_destroy;

    // 添加到 VM
    r = create_vcpu_fd(vcpu);
    if (r < 0)
        goto vcpu_destroy;

    return r;

vcpu_destroy:
    kvm_arch_vcpu_destroy(vcpu);
    return r;
}
```

### 4.3 VM 运行

**VCPU 运行**：

```c
// virt/kvm/kvm_main.c
static int kvm_vcpu_ioctl_run(struct kvm_vcpu *vcpu, struct kvm_run *kvm_run) {
    int r;

    // 设置运行状态
    vcpu->run = kvm_run;

    // 进入 VM 运行循环
    for (;;) {
        // 准备进入 Guest
        if (kvm_vcpu_running(vcpu)) {
            r = vcpu_enter_guest(vcpu);
        } else {
            r = vcpu_block(kvm, vcpu);
        }

        // 处理 VM Exit
        if (r <= 0)
            break;

        // 处理 I/O、中断等
        r = kvm_handle_exit(vcpu);
    }

    return r;
}
```

---

## 5 内存虚拟化

### 5.1 EPT/NPT

**EPT（Extended Page Tables）**：

- **Intel VT-x EPT**：硬件加速的内存虚拟化
- **地址转换**：Guest 虚拟地址 → Guest 物理地址 → Host 物理地址
- **性能优势**：硬件加速，减少软件开销

**EPT 页表结构**：

```c
// arch/x86/kvm/mmu.h
// EPT 页表项
struct ept_pte {
    u64 pfn:52;        // 物理页帧号
    u64 rsvd:11;
    u64 ignore:1;
    u64 w:1;           // 可写
    u64 r:1;           // 可读
    u64 x:1;           // 可执行
    u64 p:1;           // 存在
};
```

### 5.2 内存映射

**内存区域设置**：

```c
// virt/kvm/kvm_main.c
int kvm_vm_ioctl_set_memory_region(struct kvm *kvm,
                                    struct kvm_memory_region *mem) {
    int r;

    // 验证参数
    if (mem->memory_size & (PAGE_SIZE - 1))
        return -EINVAL;

    // 设置内存区域
    r = __kvm_set_memory_region(kvm, mem);

    return r;
}
```

### 5.3 内存管理

**内存槽管理**：

```c
// virt/kvm/kvm_main.c
struct kvm_memslots {
    u64 generation;
    struct kvm_memory_slot memslots[KVM_MEM_SLOTS_NUM];
    atomic_t lru_slot;
    int used_slots;
};
```

---

## 6 虚拟中断处理

### 6.1 中断注入

**中断注入**：

```c
// arch/x86/kvm/x86.c
int kvm_vcpu_ioctl_interrupt(struct kvm_vcpu *vcpu, struct kvm_interrupt *irq) {
    if (irq->irq >= KVM_NR_INTERRUPTS)
        return -EINVAL;

    // 注入中断
    kvm_queue_interrupt(vcpu, irq->irq, false);
    kvm_make_request(KVM_REQ_EVENT, vcpu);

    return 0;
}
```

### 6.2 中断路由

**中断路由**：

```c
// arch/x86/kvm/irq.h
struct kvm_irq_routing_table {
    int chip[KVM_NR_IRQCHIPS][KVM_IRQCHIP_NUM_PINS];
    u32 nr_rt_entries;
    struct kvm_kernel_irq_routing_entry *rt_entries;
    struct kvm_irq_routing_entry entries[];
};
```

### 6.3 虚拟中断控制器

**虚拟中断控制器**：

- **PIC（Programmable Interrupt Controller）**：8259A 兼容
- **IOAPIC（I/O Advanced Programmable Interrupt Controller）**：高级中断控制器
- **LAPIC（Local Advanced Programmable Interrupt Controller）**：本地中断控制器

---

## 7 设备模拟

### 7.1 设备模型

**KVM 与 QEMU 配合**：

- **KVM**：负责 CPU 和内存虚拟化
- **QEMU**：负责设备模拟（网络、存储、USB 等）
- **通信**：通过 `/dev/kvm` 和内存共享

### 7.2 I/O 处理

**I/O 处理流程**：

1. **Guest 执行 I/O 指令**
2. **VM Exit**：触发 VM Exit
3. **KVM 处理**：KVM 识别 I/O 操作
4. **QEMU 处理**：QEMU 模拟设备响应
5. **VM Entry**：返回 Guest

### 7.3 设备直通

**设备直通（Passthrough）**：

- **VFIO（Virtual Function I/O）**：设备直通框架
- **SR-IOV**：单根 I/O 虚拟化
- **性能优势**：接近原生性能

---

## 8 与容器化的关系

### 8.1 Kata Containers

**Kata Containers**：

- **轻量级 VM**：每个容器运行在独立的轻量级 VM 中
- **KVM 支持**：使用 KVM 提供虚拟化
- **安全隔离**：VM 级别的隔离，比容器更安全

### 8.2 Firecracker

**Firecracker**：

- **微 VM**：极小的 VM，启动时间 < 125ms
- **KVM 支持**：基于 KVM 构建
- **应用场景**：Serverless、边缘计算

### 8.3 gVisor

**gVisor**：

- **用户态内核**：在用户空间实现内核功能
- **KVM 可选**：可以使用 KVM 加速
- **安全沙盒**：提供更强的安全隔离

---

## 9 相关文档

### 9.1 详细机制文档

- **[进程与线程](02-process-thread.md)** - 进程调度与 VCPU 调度
- **[虚拟内存管理](03-memory-management.md)** - 内存管理与 EPT/NPT
- **[系统调用机制](07-syscall.md)** - 系统调用与 VM Exit

### 9.2 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 虚拟化层分析
- **[容器化架构视角](../../ARCHITECTURE/02-views/02-virtualization-containerization-sandboxing/)** - 虚拟化抽象层

### 9.3 实现细节

- **[KVM 配置示例](../../ARCHITECTURE/01-implementation/01-virtualization/kvm-setup.md)** - KVM 实际配置
- **[QEMU 配置示例](../../ARCHITECTURE/01-implementation/01-virtualization/qemu-config.md)** - QEMU 配置

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核实现分析 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
