# 04. VFS 与文件系统

## 📑 目录

- [04. VFS 与文件系统](#04-vfs-与文件系统)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 VFS 的作用](#11-vfs-的作用)
    - [1.2 文件系统层次](#12-文件系统层次)
  - [2 VFS 抽象层](#2-vfs-抽象层)
    - [2.1 VFS 数据结构](#21-vfs-数据结构)
    - [2.2 文件对象（file）](#22-文件对象file)
    - [2.3 目录项（dentry）](#23-目录项dentry)
    - [2.4 inode](#24-inode)
    - [2.5 superblock](#25-superblock)
  - [3 文件操作](#3-文件操作)
    - [3.1 打开文件（open）](#31-打开文件open)
    - [3.2 读取文件（read）](#32-读取文件read)
    - [3.3 写入文件（write）](#33-写入文件write)
    - [3.4 关闭文件（close）](#34-关闭文件close)
  - [4 文件系统类型](#4-文件系统类型)
    - [4.1 ext4 文件系统](#41-ext4-文件系统)
    - [4.2 xfs 文件系统](#42-xfs-文件系统)
    - [4.3 btrfs 文件系统](#43-btrfs-文件系统)
    - [4.4 OverlayFS](#44-overlayfs)
  - [5 文件系统挂载](#5-文件系统挂载)
    - [5.1 挂载流程](#51-挂载流程)
    - [5.2 挂载命名空间](#52-挂载命名空间)
    - [5.3 绑定挂载](#53-绑定挂载)
  - [6 与容器化的关系](#6-与容器化的关系)
    - [6.1 容器文件系统](#61-容器文件系统)
    - [6.2 联合文件系统](#62-联合文件系统)
    - [6.3 文件系统隔离](#63-文件系统隔离)
  - [7 相关文档](#7-相关文档)
    - [7.1 详细机制文档](#71-详细机制文档)
    - [7.2 容器化基础机制](#72-容器化基础机制)
    - [7.3 架构分析](#73-架构分析)

---

## 1 概述

**VFS（Virtual File System）** 是 Linux 内核提供的文件系统抽象层，为上层应用提供统一的文件操作接口，同时支持多种不同的文件系统实现。

### 1.1 VFS 的作用

- **统一接口**：为所有文件系统提供统一的 API
- **文件系统抽象**：隐藏不同文件系统的实现细节
- **性能优化**：提供目录项缓存（dentry cache）、inode 缓存
- **文件系统管理**：管理文件系统的注册、挂载、卸载

### 1.2 文件系统层次

```text
用户空间
    │
    ├── 系统调用（open、read、write）
    │
VFS 抽象层
    │
    ├── 文件系统实现（ext4、xfs、btrfs）
    │
    ├── 块设备层
    │
硬件层（磁盘、SSD）
```

---

## 2 VFS 抽象层

### 2.1 VFS 数据结构

**核心数据结构关系**：

```text
superblock
    └── inode
        └── dentry
            └── file
```

### 2.2 文件对象（file）

**file 结构**：

```c
// include/linux/fs.h
struct file {
    // 文件操作函数
    const struct file_operations *f_op;

    // 关联的 inode
    struct inode *f_inode;

    // 文件位置
    loff_t f_pos;

    // 文件标志
    unsigned int f_flags;
    fmode_t f_mode;

    // 文件描述符
    struct path f_path;

    // 私有数据
    void *private_data;

    // 引用计数
    atomic_long_t f_count;
    // ...
};
```

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
    int (*mmap)(struct file *, struct vm_area_struct *);
    // ...
};
```

### 2.3 目录项（dentry）

**dentry 结构**：

```c
// include/linux/dcache.h
struct dentry {
    // 目录项名称
    struct qstr d_name;

    // 关联的 inode
    struct inode *d_inode;

    // 父目录项
    struct dentry *d_parent;

    // 子目录项列表
    struct list_head d_subdirs;

    // 哈希表
    struct hlist_node d_hash;

    // 引用计数
    unsigned int d_count;

    // 标志
    unsigned int d_flags;
    // ...
};
```

**dentry 缓存**：

- **目的**：加速路径查找
- **结构**：哈希表 + LRU 链表
- **生命周期**：引用计数为 0 时进入 LRU，最终被回收

### 2.4 inode

**inode 结构**：

```c
// include/linux/fs.h
struct inode {
    // inode 编号
    unsigned long i_ino;

    // 文件系统
    struct super_block *i_sb;

    // 文件大小
    loff_t i_size;

    // 访问时间
    struct timespec64 i_atime;
    struct timespec64 i_mtime;
    struct timespec64 i_ctime;

    // 权限
    umode_t i_mode;
    kuid_t i_uid;
    kgid_t i_gid;

    // 文件操作
    const struct inode_operations *i_op;

    // 文件系统特定数据
    void *i_private;
    // ...
};
```

**inode_operations 结构**：

```c
// include/linux/fs.h
struct inode_operations {
    int (*create)(struct inode *, struct dentry *, umode_t, bool);
    struct dentry *(*lookup)(struct inode *, struct dentry *, unsigned int);
    int (*link)(struct dentry *, struct inode *, struct dentry *);
    int (*unlink)(struct inode *, struct dentry *);
    int (*mkdir)(struct inode *, struct dentry *, umode_t);
    int (*rmdir)(struct inode *, struct dentry *);
    // ...
};
```

### 2.5 superblock

**superblock 结构**：

```c
// include/linux/fs.h
struct super_block {
    // 文件系统类型
    struct file_system_type *s_type;

    // 根目录 inode
    struct inode *s_root;

    // 超级块操作
    const struct super_operations *s_op;

    // 块大小
    unsigned long s_blocksize;

    // 文件系统特定数据
    void *s_fs_info;

    // 挂载选项
    struct dentry *s_root;
    // ...
};
```

**super_operations 结构**：

```c
// include/linux/fs.h
struct super_operations {
    struct inode *(*alloc_inode)(struct super_block *sb);
    void (*destroy_inode)(struct inode *);
    void (*dirty_inode)(struct inode *, int flags);
    int (*write_inode)(struct inode *, struct writeback_control *wbc);
    int (*drop_inode)(struct inode *);
    void (*evict_inode)(struct inode *);
    void (*put_super)(struct super_block *);
    int (*sync_fs)(struct super_block *sb, int wait);
    // ...
};
```

---

## 3 文件操作

### 3.1 打开文件（open）

**open() 系统调用流程**：

```c
// fs/open.c
long sys_open(const char __user *filename, int flags, umode_t mode) {
    return do_sys_open(AT_FDCWD, filename, flags, mode);
}

long do_sys_open(int dfd, const char __user *filename, int flags, umode_t mode) {
    struct filename *name = getname(filename);
    int fd = get_unused_fd_flags(flags);

    // 打开文件
    struct file *f = do_filp_open(dfd, name, &op);

    // 安装文件描述符
    fd_install(fd, f);

    return fd;
}
```

**路径查找**：

```c
// fs/namei.c
// 查找路径对应的 dentry
struct dentry *path_lookup(const char *name, unsigned int flags,
                           struct path *path) {
    struct nameidata nd;
    int err;

    // 解析路径
    err = path_init(name, flags, &nd);
    if (err)
        return ERR_PTR(err);

    // 遍历路径
    err = path_walk(name, &nd);
    if (err)
        return ERR_PTR(err);

    *path = nd.path;
    return nd.path.dentry;
}
```

### 3.2 读取文件（read）

**read() 系统调用流程**：

```c
// fs/read_write.c
ssize_t sys_read(unsigned int fd, char __user *buf, size_t count) {
    struct fd f = fdget_pos(fd);
    ssize_t ret = -EBADF;

    if (f.file) {
        loff_t pos = file_pos_read(f.file);
        // 调用文件系统的 read 函数
        ret = vfs_read(f.file, buf, count, &pos);
        file_pos_write(f.file, pos);
        fdput_pos(f);
    }

    return ret;
}

ssize_t vfs_read(struct file *file, char __user *buf, size_t count, loff_t *pos) {
    // 检查文件是否可读
    if (!(file->f_mode & FMODE_READ))
        return -EBADF;

    // 调用文件系统的 read 函数
    if (file->f_op->read)
        return file->f_op->read(file, buf, count, pos);
    else if (file->f_op->read_iter)
        return new_sync_read(file, buf, count, pos);
    else
        return -EINVAL;
}
```

### 3.3 写入文件（write）

**write() 系统调用流程**：

```c
// fs/read_write.c
ssize_t sys_write(unsigned int fd, const char __user *buf, size_t count) {
    struct fd f = fdget_pos(fd);
    ssize_t ret = -EBADF;

    if (f.file) {
        loff_t pos = file_pos_read(f.file);
        // 调用文件系统的 write 函数
        ret = vfs_write(f.file, buf, count, &pos);
        file_pos_write(f.file, pos);
        fdput_pos(f);
    }

    return ret;
}

ssize_t vfs_write(struct file *file, const char __user *buf, size_t count, loff_t *pos) {
    // 检查文件是否可写
    if (!(file->f_mode & FMODE_WRITE))
        return -EBADF;

    // 调用文件系统的 write 函数
    if (file->f_op->write)
        return file->f_op->write(file, buf, count, pos);
    else if (file->f_op->write_iter)
        return new_sync_write(file, buf, count, pos);
    else
        return -EINVAL;
}
```

### 3.4 关闭文件（close）

**close() 系统调用流程**：

```c
// fs/open.c
long sys_close(unsigned int fd) {
    struct file *file;
    struct files_struct *files = current->files;

    // 获取文件对象
    file = fget(fd);
    if (!file)
        return -EBADF;

    // 释放文件描述符
    filp_close(file, files);

    return 0;
}
```

---

## 4 文件系统类型

### 4.1 ext4 文件系统

**ext4 特点**：

- **日志文件系统**：支持日志，提高可靠性
- **大文件支持**：支持最大 16TB 文件
- **大文件系统**：支持最大 1EB 文件系统
- **扩展属性**：支持扩展属性（xattr）
- **延迟分配**：延迟分配磁盘块，提高性能

**ext4 结构**：

```text
Superblock
    ├── Block Group 0
    │   ├── Group Descriptor
    │   ├── Data Block Bitmap
    │   ├── Inode Bitmap
    │   ├── Inode Table
    │   └── Data Blocks
    ├── Block Group 1
    └── ...
```

### 4.2 xfs 文件系统

**xfs 特点**：

- **高性能**：针对大文件和大文件系统优化
- **扩展性**：支持最大 8EB 文件系统
- **日志**：元数据日志，快速恢复
- **分配组**：使用分配组提高并发性能

### 4.3 btrfs 文件系统

**btrfs 特点**：

- **写时复制（CoW）**：支持快照和克隆
- **数据完整性**：校验和、数据去重
- **在线压缩**：支持透明压缩
- **子卷**：支持子卷和快照

### 4.4 OverlayFS

**OverlayFS** 是联合文件系统，用于容器镜像：

**结构**：

```text
Upper Layer（可写层）
    │
Lower Layer（只读层）
    │
Merged（合并视图）
```

**OverlayFS 操作**：

- **读取**：从上层或下层读取
- **写入**：写入上层（Copy-up）
- **删除**：在上层创建白名单文件

**内核实现**：

```c
// fs/overlayfs/super.c
// OverlayFS 挂载
static int ovl_fill_super(struct super_block *sb, void *data, int silent) {
    struct ovl_fs *ofs;

    // 创建 OverlayFS 文件系统
    ofs = ovl_fs_alloc();

    // 解析挂载选项
    err = ovl_parse_opt((char *)data, &ofs->config);

    // 挂载下层文件系统
    err = ovl_mount_lower(ofs);

    // 挂载上层文件系统
    err = ovl_mount_upper(ofs);

    // 设置根目录
    root_dentry = ovl_get_root(sb, upperpath.dentry, lowerpath.dentry);

    return 0;
}
```

---

## 5 文件系统挂载

### 5.1 挂载流程

**mount() 系统调用**：

```c
// fs/namespace.c
long sys_mount(char __user *dev_name, char __user *dir_name,
               char __user *type, unsigned long flags, void __user *data) {
    struct path path;
    int ret;

    // 查找挂载点
    ret = user_path_at(AT_FDCWD, dir_name, LOOKUP_FOLLOW, &path);
    if (ret)
        return ret;

    // 执行挂载
    ret = do_mount(dev_name, dir_name, type, flags, data);

    path_put(&path);
    return ret;
}
```

**挂载数据结构**：

```c
// include/linux/mount.h
struct mount {
    struct hlist_node mnt_hash;
    struct mount *mnt_parent;
    struct dentry *mnt_mountpoint;
    struct vfsmount mnt;
    struct list_head mnt_mounts;
    struct list_head mnt_child;
    struct mnt_namespace *mnt_ns;
    // ...
};
```

### 5.2 挂载命名空间

**Mount Namespace** 提供独立的挂载点视图：

```c
// fs/mount.h
struct mnt_namespace {
    atomic_t count;
    struct ns_common ns;
    struct mount *root;
    struct list_head list;
    // ...
};
```

**Mount Namespace 创建**：

```c
// fs/namespace.c
// 创建新的 Mount Namespace
static struct mnt_namespace *alloc_mnt_ns(struct user_namespace *user_ns) {
    struct mnt_namespace *new_ns;

    new_ns = kmalloc(sizeof(struct mnt_namespace), GFP_KERNEL);
    new_ns->ns.ops = &mntns_operations;
    new_ns->root = NULL;
    INIT_LIST_HEAD(&new_ns->list);

    return new_ns;
}
```

### 5.3 绑定挂载

**绑定挂载（Bind Mount）** 将目录或文件挂载到另一个位置：

```bash
# 绑定挂载目录
mount --bind /source /target

# 绑定挂载文件
mount --bind /source/file /target/file
```

**内核实现**：

```c
// fs/namespace.c
// 绑定挂载
static int do_loopback(struct path *path, const char *old_name) {
    struct path old_path;
    int err;

    // 查找源路径
    err = kern_path(old_name, LOOKUP_FOLLOW, &old_path);
    if (err)
        return err;

    // 创建绑定挂载
    err = path_mount(path, &old_path);

    path_put(&old_path);
    return err;
}
```

---

## 6 与容器化的关系

### 6.1 容器文件系统

**容器文件系统特点**：

- **只读根文件系统**：容器镜像通常是只读的
- **可写层**：容器运行时创建可写层
- **联合挂载**：使用 OverlayFS 等联合文件系统
- **文件系统隔离**：每个容器有独立的文件系统视图

### 6.2 联合文件系统

**容器镜像层结构**：

```text
Container Layer（可写层）
    │
Image Layer 3
    │
Image Layer 2
    │
Image Layer 1（基础镜像）
```

**OverlayFS 在容器中的应用**：

```bash
# Docker 使用 OverlayFS
docker run -it ubuntu:20.04

# 查看挂载信息
mount | grep overlay
overlay on /var/lib/docker/overlay2/... type overlay
```

### 6.3 文件系统隔离

**Mount Namespace 隔离**：

- **独立挂载点**：每个容器有独立的挂载点树
- **挂载操作隔离**：容器内的挂载不影响宿主机
- **文件系统视图**：容器只能看到自己的文件系统

**容器文件系统配置**：

```c
// 创建容器时设置 Mount Namespace
pid_t pid = clone(child_main, stack,
                  CLONE_NEWNS |  // Mount Namespace
                  CLONE_NEWPID | // PID Namespace
                  CLONE_NEWNET | // Network Namespace
                  SIGCHLD,
                  NULL);
```

---

## 7 相关文档

### 7.1 详细机制文档

- **[进程与线程](02-process-thread.md)** - 进程文件系统信息
- **[Namespace 机制详解](08-namespace.md)** - Mount Namespace 详解
- **[系统调用机制](07-syscall.md)** - open、read、write 系统调用

### 7.2 容器化基础机制

- **[Namespace 机制详解](08-namespace.md)** - Mount Namespace 文件系统隔离
- **[Cgroup 机制详解](09-cgroup.md)** - IO 资源限制

### 7.3 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 隔离机制层次分析
- **[容器化架构视角](../../ARCHITECTURE/02-views/02-virtualization-containerization-sandboxing/)** - 容器化抽象层

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核实现分析 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
