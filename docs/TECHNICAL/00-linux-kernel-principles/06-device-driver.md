# 06. 设备驱动模型

## 📑 目录

- [06. 设备驱动模型](#06-设备驱动模型)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 设备驱动的作用](#11-设备驱动的作用)
    - [1.2 设备驱动模型](#12-设备驱动模型)
  - [2 设备模型](#2-设备模型)
    - [2.1 设备（device）](#21-设备device)
    - [2.2 驱动（driver）](#22-驱动driver)
    - [2.3 总线（bus）](#23-总线bus)
    - [2.4 设备类（class）](#24-设备类class)
  - [3 字符设备](#3-字符设备)
    - [3.1 字符设备注册](#31-字符设备注册)
    - [3.2 字符设备操作](#32-字符设备操作)
    - [3.3 设备文件](#33-设备文件)
  - [4 块设备](#4-块设备)
    - [4.1 块设备注册](#41-块设备注册)
    - [4.2 块设备操作](#42-块设备操作)
    - [4.3 请求队列](#43-请求队列)
  - [5 网络设备](#5-网络设备)
    - [5.1 网络设备注册](#51-网络设备注册)
    - [5.2 网络设备操作](#52-网络设备操作)
  - [6 设备树（Device Tree）](#6-设备树device-tree)
    - [6.1 设备树结构](#61-设备树结构)
    - [6.2 设备树解析](#62-设备树解析)
  - [7 与容器化的关系](#7-与容器化的关系)
    - [7.1 设备访问控制](#71-设备访问控制)
    - [7.2 设备命名空间](#72-设备命名空间)
  - [8 相关文档](#8-相关文档)
    - [8.1 详细机制文档](#81-详细机制文档)
    - [8.2 容器化基础机制](#82-容器化基础机制)
    - [8.3 架构分析](#83-架构分析)

---

## 1 概述

**设备驱动**是 Linux 内核与硬件设备交互的接口，负责将硬件设备的功能暴露给用户空间应用程序。

### 1.1 设备驱动的作用

- **硬件抽象**：提供统一的硬件访问接口
- **设备管理**：管理设备的注册、初始化、卸载
- **资源管理**：管理设备的 I/O 端口、中断、DMA
- **设备文件**：通过 `/dev` 目录提供设备访问

### 1.2 设备驱动模型

**Linux 设备驱动模型（LDM）**：

```
用户空间
    │
    ├── 设备文件（/dev/xxx）
    │
内核空间
    │
    ├── 设备类（class）
    │   ├── 字符设备（char）
    │   ├── 块设备（block）
    │   └── 网络设备（net）
    │
    ├── 总线（bus）
    │   ├── PCI
    │   ├── USB
    │   └── Platform
    │
    ├── 设备（device）
    │
    └── 驱动（driver）
```

---

## 2 设备模型

### 2.1 设备（device）

**device 结构**：

```c
// include/linux/device.h
struct device {
    // 设备名称
    const char *init_name;

    // 设备类型
    struct device_type *type;

    // 所属总线
    struct bus_type *bus;

    // 设备驱动
    struct device_driver *driver;

    // 设备类
    struct class *class;

    // 父设备
    struct device *parent;

    // 设备私有数据
    void *driver_data;
    void *platform_data;

    // 设备操作
    const struct dev_pm_ops *pm;
    // ...
};
```

**设备注册**：

```c
// drivers/base/core.c
int device_register(struct device *dev) {
    dev->kobj.kset = devices_kset;
    kobject_init(&dev->kobj, &device_ktype);
    kobj_set_kset_s(dev, get_device_parent(dev));
    kobject_add(&dev->kobj, dev->kobj.parent, NULL);

    // 通知总线
    bus_notify(dev, BUS_NOTIFY_ADD_DEVICE);

    return 0;
}
```

### 2.2 驱动（driver）

**device_driver 结构**：

```c
// include/linux/device/driver.h
struct device_driver {
    // 驱动名称
    const char *name;

    // 所属总线
    struct bus_type *bus;

    // 模块
    struct module *owner;

    // 驱动操作
    int (*probe)(struct device *dev);
    int (*remove)(struct device *dev);
    void (*shutdown)(struct device *dev);
    int (*suspend)(struct device *dev, pm_message_t state);
    int (*resume)(struct device *dev);
    // ...
};
```

**驱动注册**：

```c
// drivers/base/driver.c
int driver_register(struct device_driver *drv) {
    int ret;

    // 注册到总线
    ret = bus_add_driver(drv);
    if (ret)
        return ret;

    // 尝试绑定设备
    driver_attach(drv);

    return 0;
}
```

### 2.3 总线（bus）

**bus_type 结构**：

```c
// include/linux/device/bus.h
struct bus_type {
    // 总线名称
    const char *name;

    // 设备匹配
    int (*match)(struct device *dev, struct device_driver *drv);

    // 设备探测
    int (*probe)(struct device *dev);
    int (*remove)(struct device *dev);

    // 设备列表
    struct subsys_private *p;
    // ...
};
```

**总线注册**：

```c
// drivers/base/bus.c
int bus_register(struct bus_type *bus) {
    int retval;
    struct subsys_private *priv;

    // 分配私有数据
    priv = kzalloc(sizeof(struct subsys_private), GFP_KERNEL);
    bus->p = priv;

    // 注册总线
    retval = kset_register(&bus->p->subsys);

    return retval;
}
```

### 2.4 设备类（class）

**class 结构**：

```c
// include/linux/device/class.h
struct class {
    // 类名称
    const char *name;

    // 类操作
    struct class_attribute *class_attrs;
    const struct attribute_group **dev_groups;

    // 设备列表
    struct kobject *dev_kobj;
    // ...
};
```

**设备类注册**：

```c
// drivers/base/class.c
int __class_register(struct class *cls, struct lock_class_key *key) {
    int error;

    // 注册类
    error = kset_register(&cls->p->subsys);
    if (error)
        return error;

    return 0;
}
```

---

## 3 字符设备

### 3.1 字符设备注册

**字符设备结构**：

```c
// include/linux/cdev.h
struct cdev {
    // 设备操作
    struct kobject kobj;
    struct module *owner;
    const struct file_operations *ops;

    // 设备号
    dev_t dev;
    unsigned int count;
    // ...
};
```

**字符设备注册**：

```c
// fs/char_dev.c
int cdev_add(struct cdev *p, dev_t dev, unsigned count) {
    int error;

    // 初始化字符设备
    p->dev = dev;
    p->count = count;

    // 添加到系统
    error = kobj_map(cdev_map, dev, count, NULL,
                     exact_match, exact_lock, p);
    if (error)
        return error;

    // 添加到设备列表
    kobject_get(&p->kobj);

    return 0;
}
```

### 3.2 字符设备操作

**file_operations 结构**：

```c
// include/linux/fs.h
struct file_operations {
    struct module *owner;
    loff_t (*llseek)(struct file *, loff_t, int);
    ssize_t (*read)(struct file *, char __user *, size_t, loff_t *);
    ssize_t (*write)(struct file *, const char __user *, size_t, loff_t *);
    int (*open)(struct inode *, struct file *);
    int (*release)(struct inode *, struct file *);
    long (*unlocked_ioctl)(struct file *, unsigned int, unsigned long);
    int (*mmap)(struct file *, struct vm_area_struct *);
    // ...
};
```

**字符设备示例**：

```c
// 简单的字符设备驱动
static int mydev_open(struct inode *inode, struct file *file) {
    // 打开设备
    return 0;
}

static ssize_t mydev_read(struct file *file, char __user *buf,
                          size_t count, loff_t *pos) {
    // 读取数据
    return count;
}

static ssize_t mydev_write(struct file *file, const char __user *buf,
                           size_t count, loff_t *pos) {
    // 写入数据
    return count;
}

static const struct file_operations mydev_fops = {
    .owner = THIS_MODULE,
    .open = mydev_open,
    .read = mydev_read,
    .write = mydev_write,
};

static int __init mydev_init(void) {
    int ret;
    dev_t dev;

    // 分配设备号
    ret = alloc_chrdev_region(&dev, 0, 1, "mydev");
    if (ret < 0)
        return ret;

    // 初始化字符设备
    cdev_init(&mydev_cdev, &mydev_fops);
    mydev_cdev.owner = THIS_MODULE;

    // 添加字符设备
    ret = cdev_add(&mydev_cdev, dev, 1);
    if (ret < 0) {
        unregister_chrdev_region(dev, 1);
        return ret;
    }

    return 0;
}
```

### 3.3 设备文件

**设备文件创建**：

```bash
# 创建设备文件
mknod /dev/mydev c 240 0

# 设备文件格式
# c: 字符设备
# 240: 主设备号
# 0: 次设备号
```

**设备文件访问**：

```c
// 用户空间访问设备
int fd = open("/dev/mydev", O_RDWR);
if (fd < 0) {
    perror("open");
    return -1;
}

char buf[1024];
read(fd, buf, sizeof(buf));
write(fd, buf, sizeof(buf));

close(fd);
```

---

## 4 块设备

### 4.1 块设备注册

**块设备结构**：

```c
// include/linux/genhd.h
struct gendisk {
    // 磁盘编号
    int major;
    int first_minor;
    int minors;

    // 磁盘名称
    char disk_name[DISK_NAME_LEN];

    // 块设备操作
    const struct block_device_operations *fops;

    // 请求队列
    struct request_queue *queue;

    // 分区表
    struct disk_part_tbl *part_tbl;
    // ...
};
```

**块设备注册**：

```c
// block/genhd.c
int add_disk(struct gendisk *disk) {
    struct device *ddev = disk_to_dev(disk);
    int ret;

    // 注册设备
    ret = device_add(ddev);
    if (ret)
        return ret;

    // 注册磁盘
    ret = register_disk(disk);
    if (ret) {
        device_del(ddev);
        return ret;
    }

    return 0;
}
```

### 4.2 块设备操作

**block_device_operations 结构**：

```c
// include/linux/blkdev.h
struct block_device_operations {
    int (*open)(struct block_device *, fmode_t);
    void (*release)(struct gendisk *, fmode_t);
    int (*ioctl)(struct block_device *, fmode_t, unsigned, unsigned long);
    int (*compat_ioctl)(struct block_device *, fmode_t, unsigned, unsigned long);
    int (*direct_access)(struct block_device *, sector_t, void **, unsigned long *);
    // ...
};
```

### 4.3 请求队列

**请求队列结构**：

```c
// include/linux/blkdev.h
struct request_queue {
    // 请求列表
    struct list_head queue_head;

    // 请求处理函数
    request_fn_proc *request_fn;
    make_request_fn *make_request_fn;

    // 队列锁
    spinlock_t queue_lock;

    // 队列标志
    unsigned long queue_flags;
    // ...
};
```

**请求处理**：

```c
// block/blk-core.c
// 提交请求
void blk_execute_rq(struct request_queue *q, struct gendisk *bd_disk,
                    struct request *rq, int at_head) {
    // 执行请求
    q->request_fn(q);
}

// 请求完成
void blk_end_request_all(struct request *rq, int error) {
    // 完成请求
    __blk_end_request_all(rq, error);
}
```

---

## 5 网络设备

### 5.1 网络设备注册

**网络设备注册**：

```c
// net/core/dev.c
int register_netdevice(struct net_device *dev) {
    int ret;

    // 初始化网络设备
    ret = dev_init_scheduler(dev);
    if (ret)
        return ret;

    // 添加到设备列表
    ret = netdev_register_kobject(dev);
    if (ret) {
        dev_uninit_scheduler(dev);
        return ret;
    }

    // 通知网络子系统
    call_netdevice_notifiers(NETDEV_REGISTER, dev);

    return 0;
}
```

### 5.2 网络设备操作

**网络设备操作**：

```c
// include/linux/netdevice.h
struct net_device_ops {
    int (*ndo_init)(struct net_device *dev);
    void (*ndo_uninit)(struct net_device *dev);
    int (*ndo_open)(struct net_device *dev);
    int (*ndo_stop)(struct net_device *dev);
    netdev_tx_t (*ndo_start_xmit)(struct sk_buff *skb,
                                   struct net_device *dev);
    int (*ndo_set_mac_address)(struct net_device *dev, void *addr);
    // ...
};
```

---

## 6 设备树（Device Tree）

### 6.1 设备树结构

**设备树（Device Tree）** 用于描述硬件设备，主要用于 ARM 架构：

**设备树示例**：

```dts
/dts-v1/;

/ {
    compatible = "my,board";
    model = "My Board";

    cpus {
        #address-cells = <1>;
        #size-cells = <0>;

        cpu@0 {
            compatible = "arm,cortex-a9";
            reg = <0>;
        };
    };

    memory@0 {
        device_type = "memory";
        reg = <0x0 0x40000000>;
    };

    serial@101f0000 {
        compatible = "arm,pl011";
        reg = <0x101f0000 0x1000>;
        interrupts = <0 1 4>;
    };
};
```

### 6.2 设备树解析

**设备树解析**：

```c
// drivers/of/platform.c
// 从设备树创建平台设备
static int of_platform_bus_create(struct device_node *bus,
                                   const struct of_device_id *matches,
                                   const struct of_dev_auxdata *lookup,
                                   struct device *parent, bool strict) {
    struct device_node *child;
    struct platform_device *dev;
    int rc = 0;

    // 遍历设备树节点
    for_each_child_of_node(bus, child) {
        // 创建平台设备
        dev = of_platform_device_create_pdata(child, NULL, parent);
        if (!dev || !of_match_node(matches, child)) {
            of_node_put(child);
            continue;
        }

        // 递归处理子节点
        rc = of_platform_bus_create(child, matches, lookup, &dev->dev, strict);
        if (rc) {
            of_node_put(child);
            break;
        }
    }

    return rc;
}
```

---

## 7 与容器化的关系

### 7.1 设备访问控制

**容器设备访问**：

- **设备白名单**：容器只能访问允许的设备
- **设备权限**：通过 Capabilities 控制设备访问
- **设备命名空间**：某些设备可以隔离到容器

**Docker 设备访问**：

```bash
# 允许容器访问设备
docker run --device=/dev/sda1 ubuntu:20.04

# 允许容器访问所有设备（危险）
docker run --privileged ubuntu:20.04
```

### 7.2 设备命名空间

**设备命名空间隔离**：

- **设备文件隔离**：容器有独立的 `/dev` 目录
- **设备访问控制**：通过 Cgroup 限制设备访问
- **虚拟设备**：容器可以使用虚拟设备（如 veth、loop）

---

## 8 相关文档

### 8.1 详细机制文档

- **[VFS 与文件系统](04-filesystem.md)** - 设备文件系统
- **[网络协议栈](05-network-stack.md)** - 网络设备驱动

### 8.2 容器化基础机制

- **[Namespace 机制详解](08-namespace.md)** - 设备命名空间
- **[Capabilities 机制](10-capabilities.md)** - 设备访问权限

### 8.3 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 隔离机制层次分析
- **[容器化架构视角](../../ARCHITECTURE/02-views/02-virtualization-containerization-sandboxing/)** - 容器化抽象层

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核实现分析 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
