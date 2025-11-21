# 内核代码示例矩阵

## 📑 目录

- [内核代码示例矩阵](#内核代码示例矩阵)
  - [📑 目录](#-目录)
  - [1 进程管理代码示例](#1-进程管理代码示例)
  - [2 内存管理代码示例](#2-内存管理代码示例)
  - [3 文件系统代码示例](#3-文件系统代码示例)
  - [4 网络子系统代码示例](#4-网络子系统代码示例)
  - [5 容器化机制代码示例](#5-容器化机制代码示例)

---

## 1 进程管理代码示例

### 1.1 创建进程

**系统调用**：`fork()`

**内核实现**：

```c
// kernel/fork.c
SYSCALL_DEFINE0(fork)
{
    struct kernel_clone_args args = {
        .exit_signal = SIGCHLD,
    };
    return kernel_clone(&args);
}

long kernel_clone(struct kernel_clone_args *args)
{
    u64 clone_flags = args->flags;
    struct task_struct *p;

    // 复制进程描述符
    p = copy_process(clone_flags, args->stack, args->stack_size,
                     args->pid, args->tls, args->node);

    if (!IS_ERR(p)) {
        // 唤醒新进程
        wake_up_new_task(p);
        // 返回子进程PID
        return task_pid_vnr(p);
    }
    return PTR_ERR(p);
}
```

**用户空间使用**：

```c
#include <unistd.h>
#include <sys/types.h>

pid_t pid = fork();
if (pid == 0) {
    // 子进程
    printf("Child process: PID=%d\n", getpid());
} else if (pid > 0) {
    // 父进程
    printf("Parent process: Child PID=%d\n", pid);
} else {
    // 错误
    perror("fork");
}
```

---

### 1.2 创建线程

**系统调用**：`clone()`

**内核实现**：

```c
// kernel/fork.c
SYSCALL_DEFINE5(clone, unsigned long, clone_flags, unsigned long, newsp,
                int __user *, parent_tidptr, unsigned long, tls,
                int __user *, child_tidptr)
{
    struct kernel_clone_args args = {
        .flags      = (lower_32_bits(clone_flags) & ~CSIGNAL),
        .pidfd      = parent_tidptr,
        .child_tid  = child_tidptr,
        .parent_tid = parent_tidptr,
        .exit_signal = (lower_32_bits(clone_flags) & CSIGNAL),
        .stack      = newsp,
        .tls        = tls,
    };
    return kernel_clone(&args);
}
```

**用户空间使用**：

```c
#include <pthread.h>

void *thread_func(void *arg) {
    printf("Thread: TID=%ld\n", pthread_self());
    return NULL;
}

pthread_t tid;
pthread_create(&tid, NULL, thread_func, NULL);
pthread_join(tid, NULL);
```

---

## 2 内存管理代码示例

### 2.1 内存映射

**系统调用**：`mmap()`

**内核实现**：

```c
// mm/mmap.c
unsigned long do_mmap(struct file *file, unsigned long addr,
                      unsigned long len, unsigned long prot,
                      unsigned long flags, unsigned long pgoff,
                      unsigned long *populate, struct list_head *uf)
{
    struct mm_struct *mm = current->mm;
    struct vm_area_struct *vma;

    // 查找虚拟地址空间
    addr = get_unmapped_area(file, addr, len, pgoff, flags);
    if (offset_in_page(addr))
        return addr;

    // 创建VMA
    vma = vm_area_alloc(mm);
    vma->vm_start = addr;
    vma->vm_end = addr + len;
    vma->vm_flags = flags;
    vma->vm_page_prot = vm_get_page_prot(flags);

    // 插入VMA到进程地址空间
    vma_link(mm, vma, prev, rb_link, rb_parent);

    return addr;
}
```

**用户空间使用**：

```c
#include <sys/mman.h>

void *addr = mmap(NULL, 4096, PROT_READ | PROT_WRITE,
                  MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
if (addr == MAP_FAILED) {
    perror("mmap");
    return;
}

// 使用映射的内存
memset(addr, 0, 4096);
munmap(addr, 4096);
```

---

### 2.2 内存分配

**内核函数**：`kmalloc()`

**内核实现**：

```c
// mm/slab_common.c
void *kmalloc(size_t size, gfp_t flags)
{
    if (__builtin_constant_p(size)) {
        // 小对象使用Slab分配器
        if (size > KMALLOC_MAX_CACHE_SIZE)
            return kmalloc_large(size, flags);
        return kmalloc_slab(size, flags);
    }
    return __kmalloc(size, flags);
}
```

**内核使用**：

```c
// 分配内存
char *buf = kmalloc(1024, GFP_KERNEL);
if (!buf) {
    printk(KERN_ERR "Memory allocation failed\n");
    return -ENOMEM;
}

// 使用内存
memset(buf, 0, 1024);

// 释放内存
kfree(buf);
```

---

## 3 文件系统代码示例

### 3.1 打开文件

**系统调用**：`open()`

**内核实现**：

```c
// fs/open.c
long do_sys_open(int dfd, const char __user *filename, int flags, umode_t mode)
{
    struct filename *tmp = getname(filename);
    int fd = PTR_ERR(tmp);

    if (!IS_ERR(tmp)) {
        fd = get_unused_fd_flags(flags);
        if (fd >= 0) {
            struct file *f = do_filp_open(dfd, tmp, &op);
            if (IS_ERR(f)) {
                put_unused_fd(fd);
                fd = PTR_ERR(f);
            } else {
                fsnotify_open(f);
                fd_install(fd, f);
            }
        }
        putname(tmp);
    }
    return fd;
}
```

**用户空间使用**：

```c
#include <fcntl.h>

int fd = open("/tmp/test.txt", O_RDWR | O_CREAT, 0644);
if (fd < 0) {
    perror("open");
    return;
}

// 使用文件描述符
write(fd, "Hello", 5);
close(fd);
```

---

## 4 网络子系统代码示例

### 4.1 创建Socket

**系统调用**：`socket()`

**内核实现**：

```c
// net/socket.c
int __sys_socket(int family, int type, int protocol)
{
    struct socket *sock;
    int flags, ret;

    // 创建Socket
    ret = sock_create(family, type, protocol, &sock);
    if (ret < 0)
        return ret;

    // 分配文件描述符
    ret = sock_map_fd(sock, flags & (O_CLOEXEC | O_NONBLOCK));
    if (ret < 0) {
        sock_release(sock);
        return ret;
    }

    return ret;
}
```

**用户空间使用**：

```c
#include <sys/socket.h>
#include <netinet/in.h>

int sockfd = socket(AF_INET, SOCK_STREAM, 0);
if (sockfd < 0) {
    perror("socket");
    return;
}

struct sockaddr_in addr;
addr.sin_family = AF_INET;
addr.sin_port = htons(8080);
addr.sin_addr.s_addr = INADDR_ANY;

bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));
listen(sockfd, 10);
```

---

## 5 容器化机制代码示例

### 5.1 创建PID Namespace

**系统调用**：`clone()` with `CLONE_NEWPID`

**内核实现**：

```c
// kernel/pid_namespace.c
static struct pid_namespace *create_pid_namespace(struct user_namespace *user_ns,
                                                   struct pid_namespace *parent_pid_ns)
{
    struct pid_namespace *ns;
    unsigned int level = parent_pid_ns->level + 1;

    // 分配命名空间
    ns = kmem_cache_zalloc(pid_ns_cachep, GFP_KERNEL);
    if (ns == NULL)
        goto out_free;

    ns->pidmap[0].page = kzalloc(PAGE_SIZE, GFP_KERNEL);
    if (!ns->pidmap[0].page)
        goto out_free;

    ns->pid_cachep = create_pid_cachep(level + 1);
    if (ns->pid_cachep == NULL)
        goto out_free;

    ns->parent = get_pid_ns(parent_pid_ns);
    ns->level = level;
    ns->user_ns = get_user_ns(user_ns);
    ns->pid_allocated = PIDNS_ADDING;

    return ns;
}
```

**用户空间使用**：

```c
#include <sched.h>
#include <unistd.h>

#define STACK_SIZE (1024 * 1024)
static char child_stack[STACK_SIZE];

int child_main(void *arg) {
    printf("Child: PID=%d\n", getpid());
    system("ps aux");
    return 0;
}

int main() {
    printf("Parent: PID=%d\n", getpid());
    clone(child_main, child_stack + STACK_SIZE,
          CLONE_NEWPID | SIGCHLD, NULL);
    wait(NULL);
    return 0;
}
```

---

### 5.2 创建Network Namespace

**系统调用**：`unshare()` with `CLONE_NEWNET`

**内核实现**：

```c
// net/core/net_namespace.c
static __net_init int net_ns_net_init(struct net *net)
{
    // 初始化网络命名空间
    net->dev_base_head = RB_ROOT;
    INIT_LIST_HEAD(&net->dev_name_head);
    INIT_LIST_HEAD(&net->dev_index_head);

    // 初始化协议栈
    setup_net(net, &init_user_ns);

    return 0;
}
```

**用户空间使用**：

```c
#include <sched.h>
#include <sys/socket.h>
#include <linux/if.h>
#include <linux/if_tun.h>

// 创建网络命名空间
unshare(CLONE_NEWNET);

// 创建虚拟网络设备
int tunfd = open("/dev/net/tun", O_RDWR);
struct ifreq ifr;
memset(&ifr, 0, sizeof(ifr));
ifr.ifr_flags = IFF_TUN | IFF_NO_PI;
strcpy(ifr.ifr_name, "tun0");
ioctl(tunfd, TUNSETIFF, &ifr);
```

---

### 5.3 设置Cgroup限制

**Cgroup v2接口**：

```c
// 设置CPU限制
int cgroup_fd = open("/sys/fs/cgroup/cpu/mygroup", O_RDWR);
char cpu_max[] = "50000 100000";  // 50% CPU限制
write(cgroup_fd, cpu_max, sizeof(cpu_max));

// 设置内存限制
int mem_fd = open("/sys/fs/cgroup/memory/mygroup/memory.max", O_WRONLY);
char mem_max[] = "512M";
write(mem_fd, mem_max, sizeof(mem_max));

// 将进程加入Cgroup
int procs_fd = open("/sys/fs/cgroup/mygroup/cgroup.procs", O_WRONLY);
char pid_str[16];
sprintf(pid_str, "%d", getpid());
write(procs_fd, pid_str, strlen(pid_str));
```

**内核实现**：

```c
// kernel/cgroup/cgroup.c
static int cgroup_migrate(struct cgroup *dst_cgrp, struct task_struct *task)
{
    struct cgroup *src_cgrp = task_cgroup_from_root(task, &cgrp_dfl_root);

    // 迁移任务
    cgroup_migrate_execute(&mgctx);

    return 0;
}
```

---

**最后更新**：2025-11-07
**文档状态**：✅ 完整 | 📊 包含内核代码示例矩阵 | 🎯 生产就绪
**维护者**：项目团队
