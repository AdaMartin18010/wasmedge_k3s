# 03. 虚拟内存管理

## 📑 目录

- [03. 虚拟内存管理](#03-虚拟内存管理)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 虚拟内存的作用](#11-虚拟内存的作用)
    - [1.2 虚拟内存的优势](#12-虚拟内存的优势)
  - [2 虚拟地址空间](#2-虚拟地址空间)
    - [2.1 地址空间布局](#21-地址空间布局)
    - [2.2 内存区域（VMA）](#22-内存区域vma)
    - [2.3 地址空间管理](#23-地址空间管理)
  - [3 页表与页表项](#3-页表与页表项)
    - [3.1 页表结构](#31-页表结构)
    - [3.2 页表项（PTE）](#32-页表项pte)
    - [3.3 页表遍历](#33-页表遍历)
    - [3.4 TLB（Translation Lookaside Buffer）](#34-tlbtranslation-lookaside-buffer)
  - [4 物理内存管理](#4-物理内存管理)
    - [4.1 页帧（Page Frame）](#41-页帧page-frame)
    - [4.2 Buddy System](#42-buddy-system)
    - [4.3 Slab Allocator](#43-slab-allocator)
    - [4.4 内存分配接口](#44-内存分配接口)
  - [5 内存映射](#5-内存映射)
    - [5.1 mmap() 系统调用](#51-mmap-系统调用)
    - [5.2 文件映射](#52-文件映射)
    - [5.3 匿名映射](#53-匿名映射)
    - [5.4 共享映射与私有映射](#54-共享映射与私有映射)
  - [6 内存回收](#6-内存回收)
    - [6.1 页面回收机制](#61-页面回收机制)
    - [6.2 交换（Swap）](#62-交换swap)
    - [6.3 内存压缩](#63-内存压缩)
    - [6.4 OOM Killer](#64-oom-killer)
  - [7 与容器化的关系](#7-与容器化的关系)
    - [7.1 容器内存限制](#71-容器内存限制)
    - [7.2 内存统计](#72-内存统计)
    - [7.3 内存回收](#73-内存回收)
  - [8 相关文档](#8-相关文档)
    - [8.1 详细机制文档](#81-详细机制文档)
    - [8.2 容器化基础机制](#82-容器化基础机制)
    - [8.3 架构分析](#83-架构分析)
  - [2025 年最新实践](#2025-年最新实践)
    - [内存管理应用最佳实践（2025）](#内存管理应用最佳实践2025)
  - [实际应用案例](#实际应用案例)
    - [案例 1：容器内存性能优化（2025）](#案例-1容器内存性能优化2025)

---

## 1 概述

**虚拟内存**是 Linux 内核的核心机制之一，为每个进程提供独立的虚拟地址空间，实现内存保护、内存共享和内存管理。

### 1.1 虚拟内存的作用

- **地址空间隔离**：每个进程有独立的虚拟地址空间
- **内存保护**：防止进程访问其他进程的内存
- **内存共享**：多个进程可以共享同一物理页面
- **内存扩展**：通过交换（Swap）扩展可用内存
- **内存管理**：统一管理物理内存和虚拟内存

### 1.2 虚拟内存的优势

- **安全性**：进程无法直接访问物理内存
- **灵活性**：虚拟地址可以映射到任意物理地址
- **效率**：支持按需分页（Demand Paging）
- **共享**：支持内存映射文件、共享库等

---

## 2 虚拟地址空间

### 2.1 地址空间布局

**x86_64 地址空间布局**：

```text
0x00007FFFFFFFFFFF (128TB)
    └── 用户空间（User Space）
        ├── 栈（Stack）- 向下增长
        ├── 内存映射区域（Memory Mapping）
        ├── 堆（Heap）- 向上增长
        ├── BSS 段（未初始化数据）
        ├── 数据段（Data Segment）
        └── 代码段（Text Segment）
0x0000000000000000

0xFFFFFFFFFFFFFFFF
    └── 内核空间（Kernel Space）
        ├── 直接映射区（Direct Mapping）
        ├── vmalloc 区
        ├── 持久映射区
        └── 固定映射区
0xFFFF800000000000
```

**关键区域**：

- **代码段（Text）**：程序代码，只读
- **数据段（Data）**：已初始化全局变量
- **BSS 段**：未初始化全局变量
- **堆（Heap）**：动态分配内存（malloc）
- **栈（Stack）**：局部变量、函数调用
- **内存映射区**：mmap 映射的文件和匿名内存

### 2.2 内存区域（VMA）

内核使用 **VMA（Virtual Memory Area）** 描述虚拟地址空间的连续区域：

```c
// include/linux/mm_types.h
struct vm_area_struct {
    // 虚拟地址范围
    unsigned long vm_start;
    unsigned long vm_end;

    // 关联的进程
    struct mm_struct *vm_mm;

    // 权限标志
    pgprot_t vm_page_prot;
    unsigned long vm_flags;

    // 文件映射
    struct file *vm_file;
    unsigned long vm_pgoff;

    // 操作函数
    const struct vm_operations_struct *vm_ops;

    // 链表和树
    struct rb_node vm_rb;
    struct list_head anon_vma_chain;
    // ...
};
```

**VMA 类型**：

- **代码段 VMA**：可执行、只读
- **数据段 VMA**：可读写
- **堆 VMA**：可读写、可扩展
- **栈 VMA**：可读写、向下增长
- **文件映射 VMA**：映射文件到内存
- **匿名 VMA**：不关联文件（堆、栈）

### 2.3 地址空间管理

**mm_struct 结构**：

```c
// include/linux/mm_types.h
struct mm_struct {
    // 虚拟内存区域列表
    struct vm_area_struct *mmap;
    struct rb_root mm_rb;

    // 页表
    pgd_t *pgd;

    // 内存统计
    unsigned long total_vm;
    unsigned long locked_vm;
    unsigned long pinned_vm;

    // 内存限制
    unsigned long rss;
    unsigned long anon_rss;
    unsigned long file_rss;

    // 内存映射
    struct list_head mmlist;
    // ...
};
```

---

## 3 页表与页表项

### 3.1 页表结构

**x86_64 四级页表**：

```text
虚拟地址：63-48位（未使用）| 47-39位（PML4）| 38-30位（PDPT）| 29-21位（PD）| 20-12位（PT）| 11-0位（Offset）

PML4 (Page Map Level 4)
  └── PDPT (Page Directory Pointer Table)
      └── PD (Page Directory)
          └── PT (Page Table)
              └── Page (4KB)
```

**页表结构**：

```c
// arch/x86/include/asm/pgtable_types.h
typedef struct { unsigned long pte; } pte_t;
typedef struct { unsigned long pmd; } pmd_t;
typedef struct { unsigned long pud; } pud_t;
typedef struct { unsigned long pgd; } pgd_t;
```

### 3.2 页表项（PTE）

**页表项结构（x86_64）**：

```c
// arch/x86/include/asm/pgtable_types.h
// PTE 位定义
#define _PAGE_PRESENT   0x001  // 页面在内存中
#define _PAGE_RW        0x002  // 可写
#define _PAGE_USER      0x004  // 用户空间可访问
#define _PAGE_PWT       0x008  // Page Write Through
#define _PAGE_PCD       0x010  // Page Cache Disable
#define _PAGE_ACCESSED 0x020  // 已访问
#define _PAGE_DIRTY    0x040  // 已修改
#define _PAGE_PSE      0x080  // Page Size Extension
#define _PAGE_GLOBAL   0x100  // 全局页（TLB 不刷新）
```

**页表项操作**：

```c
// mm/pgtable-generic.c
static inline pte_t pte_mkwrite(pte_t pte) {
    return pte_set_flags(pte, _PAGE_RW);
}

static inline pte_t pte_mkdirty(pte_t pte) {
    return pte_set_flags(pte, _PAGE_DIRTY);
}

static inline int pte_present(pte_t pte) {
    return pte_flags(pte) & _PAGE_PRESENT;
}
```

### 3.3 页表遍历

**地址转换流程**：

```c
// arch/x86/mm/pageattr.c
// 虚拟地址到物理地址的转换
static pte_t *walk_page_table(unsigned long addr) {
    pgd_t *pgd;
    pud_t *pud;
    pmd_t *pmd;
    pte_t *pte;

    // 获取页全局目录
    pgd = pgd_offset(current->mm, addr);
    if (pgd_none(*pgd) || pgd_bad(*pgd))
        return NULL;

    // 获取页上级目录
    pud = pud_offset(pgd, addr);
    if (pud_none(*pud) || pud_bad(*pud))
        return NULL;

    // 获取页中间目录
    pmd = pmd_offset(pud, addr);
    if (pmd_none(*pmd) || pmd_bad(*pmd))
        return NULL;

    // 获取页表项
    pte = pte_offset_map(pmd, addr);
    return pte;
}
```

### 3.4 TLB（Translation Lookaside Buffer）

**TLB 作用**：

- **加速地址转换**：缓存虚拟地址到物理地址的映射
- **减少页表访问**：避免每次访问都遍历页表
- **提高性能**：TLB 命中率直接影响性能

**TLB 刷新**：

```c
// arch/x86/include/asm/tlbflush.h
// 刷新当前进程的 TLB
static inline void flush_tlb(void) {
    __flush_tlb();
}

// 刷新指定地址范围的 TLB
static inline void flush_tlb_range(struct vm_area_struct *vma,
                                   unsigned long start, unsigned long end) {
    __flush_tlb_range(vma, start, end);
}
```

---

## 4 物理内存管理

### 4.1 页帧（Page Frame）

**页帧结构**：

```c
// include/linux/mm_types.h
struct page {
    // 页标志
    unsigned long flags;

    // 引用计数
    atomic_t _refcount;

    // 所属的页框号
    unsigned long pfn;

    // 所属的内存区域
    struct zone *zone;

    // 链表
    struct list_head lru;

    // 映射信息
    struct address_space *mapping;
    pgoff_t index;
    // ...
};
```

**页标志**：

```c
// include/linux/page-flags.h
#define PG_locked     0  // 页面被锁定
#define PG_error      1  // 页面错误
#define PG_referenced 2  // 页面被引用
#define PG_uptodate   3  // 页面数据最新
#define PG_dirty      4  // 页面被修改
#define PG_lru        5  // 页面在 LRU 链表上
#define PG_active     6  // 页面活跃
#define PG_slab       7  // 页面属于 slab
// ...
```

### 4.2 Buddy System

**Buddy System** 用于管理物理内存页帧：

```c
// mm/page_alloc.c
// Buddy System 结构
struct free_area {
    struct list_head free_list[MIGRATE_TYPES];
    unsigned long nr_free;
};

struct zone {
    // Buddy System 空闲列表
    struct free_area free_area[MAX_ORDER];
    // ...
};
```

**内存分配**：

```c
// mm/page_alloc.c
// 分配 2^order 个连续页
struct page *__alloc_pages(gfp_t gfp_mask, unsigned int order,
                           struct zonelist *zonelist) {
    struct page *page;

    // 从 Buddy System 分配
    page = get_page_from_freelist(gfp_mask, order, zonelist);

    if (unlikely(!page)) {
        // 内存不足，尝试回收
        page = __alloc_pages_slowpath(gfp_mask, order, zonelist);
    }

    return page;
}
```

**内存释放**：

```c
// mm/page_alloc.c
// 释放页面到 Buddy System
void __free_pages(struct page *page, unsigned int order) {
    if (put_page_testzero(page)) {
        free_the_page(page, order);
    }
}
```

### 4.3 Slab Allocator

**Slab Allocator** 用于分配小对象（小于一页）：

```c
// mm/slab.h
// Slab 缓存
struct kmem_cache {
    // 对象大小
    unsigned int object_size;

    // Slab 列表
    struct list_head slabs_full;
    struct list_head slabs_partial;
    struct list_head slabs_free;

    // 分配函数
    void *(*ctor)(void *obj);
    // ...
};
```

**Slab 分配**：

```c
// mm/slab.c
// 从 Slab 缓存分配对象
void *kmem_cache_alloc(struct kmem_cache *cachep, gfp_t flags) {
    void *ret = slab_alloc(cachep, flags, _RET_IP_);
    return ret;
}

// 释放对象到 Slab 缓存
void kmem_cache_free(struct kmem_cache *cachep, void *objp) {
    slab_free(cachep, objp, _RET_IP_);
}
```

### 4.4 内存分配接口

**内核内存分配函数**：

```c
// include/linux/slab.h
// 分配指定大小的内存（对齐到缓存行）
void *kmalloc(size_t size, gfp_t flags);

// 释放 kmalloc 分配的内存
void kfree(const void *objp);

// 分配虚拟连续但物理不连续的内存
void *vmalloc(unsigned long size);

// 释放 vmalloc 分配的内存
void vfree(const void *addr);

// 分配物理连续的内存
void *kzalloc(size_t size, gfp_t flags);
```

**分配标志（gfp_t）**：

```c
// include/linux/gfp.h
#define __GFP_RECLAIM   0x10u  // 可以回收
#define __GFP_HIGH      0x20u  // 高优先级
#define __GFP_IO        0x40u  // 可以 IO
#define __GFP_FS        0x80u  // 可以文件系统操作
#define __GFP_ZERO      0x8000u // 清零内存
```

---

## 5 内存映射

### 5.1 mmap() 系统调用

**mmap() 接口**：

```c
#include <sys/mman.h>

void *mmap(void *addr, size_t length, int prot, int flags,
           int fd, off_t offset);
```

**参数说明**：

- `addr`：建议的映射地址（通常为 NULL）
- `length`：映射长度
- `prot`：保护标志（PROT_READ、PROT_WRITE、PROT_EXEC）
- `flags`：映射标志（MAP_SHARED、MAP_PRIVATE、MAP_ANONYMOUS）
- `fd`：文件描述符（匿名映射时为 -1）
- `offset`：文件偏移

**内核实现**：

```c
// mm/mmap.c
long sys_mmap(unsigned long addr, unsigned long len,
              unsigned long prot, unsigned long flags,
              unsigned long fd, unsigned long off) {
    struct file *file = NULL;

    // 获取文件对象
    if (!(flags & MAP_ANONYMOUS)) {
        file = fget(fd);
        if (!file)
            return -EBADF;
    }

    // 执行内存映射
    addr = do_mmap(file, addr, len, prot, flags, off);

    if (file)
        fput(file);

    return addr;
}
```

### 5.2 文件映射

**文件映射流程**：

1. **打开文件**：获取文件描述符
2. **创建 VMA**：在内核中创建虚拟内存区域
3. **建立映射**：将文件内容映射到虚拟地址空间
4. **按需加载**：访问时通过缺页异常加载文件内容

**文件映射示例**：

```c
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>

int fd = open("/path/to/file", O_RDONLY);
void *addr = mmap(NULL, 4096, PROT_READ, MAP_SHARED, fd, 0);

// 访问映射的内存
char *data = (char *)addr;
printf("%s\n", data);

// 取消映射
munmap(addr, 4096);
close(fd);
```

### 5.3 匿名映射

**匿名映射**不关联文件，用于：

- **堆内存**：malloc 底层使用匿名映射
- **共享内存**：进程间共享内存
- **大块内存分配**：分配大块连续内存

**匿名映射示例**：

```c
#include <sys/mman.h>

// 分配 1MB 匿名内存
void *addr = mmap(NULL, 1024 * 1024,
                  PROT_READ | PROT_WRITE,
                  MAP_PRIVATE | MAP_ANONYMOUS,
                  -1, 0);

// 使用内存
memset(addr, 0, 1024 * 1024);

// 释放
munmap(addr, 1024 * 1024);
```

### 5.4 共享映射与私有映射

**MAP_SHARED**：

- 多个进程共享同一物理页面
- 修改对所有进程可见
- 用于进程间通信

**MAP_PRIVATE**：

- 写时复制（Copy-on-Write）
- 修改不影响其他进程
- 用于进程私有内存

**写时复制（CoW）流程**：

1. 多个进程映射同一页面（MAP_PRIVATE）
2. 初始共享同一物理页面
3. 某个进程写入时触发缺页异常
4. 内核复制页面，更新页表
5. 进程拥有独立的物理页面

---

## 6 内存回收

### 6.1 页面回收机制

**LRU（Least Recently Used）算法**：

```c
// include/linux/mmzone.h
// LRU 链表
enum lru_list {
    LRU_INACTIVE_ANON = 0,
    LRU_ACTIVE_ANON = 1,
    LRU_INACTIVE_FILE = 2,
    LRU_ACTIVE_FILE = 3,
    LRU_UNEVICTABLE = 4,
    NR_LRU_LISTS
};
```

**页面回收流程**：

1. **扫描 LRU 链表**：从非活跃链表开始
2. **检查页面**：判断页面是否可回收
3. **回收页面**：
   - 脏页：写回磁盘
   - 干净页：直接回收
4. **更新页表**：标记页面不在内存中

### 6.2 交换（Swap）

**交换空间**：

- **交换分区**：独立的磁盘分区
- **交换文件**：普通文件作为交换空间

**交换流程**：

```c
// mm/swap_state.c
// 将页面换出到交换空间
int swap_writepage(struct page *page, struct writeback_control *wbc) {
    struct bio *bio;
    struct swap_info_struct *sis;

    // 获取交换信息
    sis = page_swap_info(page);

    // 创建 BIO 请求
    bio = get_swap_bio(GFP_NOIO, page, sis);

    // 提交写请求
    submit_bio(bio);

    return 0;
}
```

**页面换入**：

```c
// mm/memory.c
// 处理缺页异常，换入页面
static int do_swap_page(struct vm_fault *vmf) {
    struct page *page;
    swp_entry_t entry;

    // 从交换空间读取页面
    entry = pte_to_swp_entry(vmf->orig_pte);
    page = swapin_readahead(entry, GFP_HIGHUSER_MOVABLE,
                            vmf->vma, vmf->address);

    // 建立映射
    do_set_pte(vmf, page);

    return 0;
}
```

### 6.3 内存压缩

**内存压缩（KSM - Kernel Same-page Merging）**：

- 合并相同内容的页面
- 多个进程共享同一物理页面
- 减少内存使用

**内存压缩流程**：

1. **扫描页面**：查找可合并的页面
2. **比较内容**：比较页面内容
3. **合并页面**：将相同页面合并为共享页面
4. **更新页表**：更新所有进程的页表

### 6.4 OOM Killer

**OOM（Out of Memory）Killer**：

当系统内存严重不足时，内核会杀死进程释放内存：

```c
// mm/oom_kill.c
// OOM Killer 选择要杀死的进程
void out_of_memory(struct oom_control *oc) {
    struct task_struct *victim;

    // 选择要杀死的进程
    victim = select_bad_process(oc);

    if (victim) {
        // 杀死进程
        oom_kill_process(oc, victim);
    }
}
```

**OOM 评分**：

- **内存使用**：RSS、Swap 使用量
- **进程优先级**：nice 值
- **运行时间**：长时间运行的进程优先保留
- **子进程数量**：子进程多的进程优先杀死

---

## 7 与容器化的关系

### 7.1 容器内存限制

**Cgroup Memory Controller** 限制容器内存：

```bash
# 设置内存限制为 512MB
echo 536870912 > /sys/fs/cgroup/memory/container1/memory.limit_in_bytes

# 设置内存+交换限制为 1GB
echo 1073741824 > /sys/fs/cgroup/memory/container1/memory.memsw.limit_in_bytes
```

**内核实现**：

```c
// mm/memcontrol.c
// 检查内存限制
static bool mem_cgroup_out_of_memory(struct mem_cgroup *memcg,
                                     const gfp_t gfp_mask,
                                     int order) {
    unsigned long usage = mem_cgroup_usage(memcg);
    unsigned long limit = mem_cgroup_get_limit(memcg);

    if (usage > limit) {
        // 触发 OOM
        return true;
    }

    return false;
}
```

### 7.2 内存统计

**容器内存统计**：

```bash
# 查看容器内存使用
cat /sys/fs/cgroup/memory/container1/memory.usage_in_bytes

# 查看内存峰值
cat /sys/fs/cgroup/memory/container1/memory.max_usage_in_bytes

# 查看内存统计详情
cat /sys/fs/cgroup/memory/container1/memory.stat
```

**统计项**：

- `cache`：页面缓存
- `rss`：常驻内存
- `swap`：交换使用
- `mapped_file`：文件映射内存

### 7.3 内存回收

**容器内存回收**：

- **内存压力**：当容器内存使用接近限制时触发回收
- **页面回收**：回收容器内的非活跃页面
- **交换**：将容器页面换出到交换空间
- **OOM Killer**：容器内 OOM 时杀死容器内进程

**内存回收策略**：

```c
// mm/vmscan.c
// 容器内存回收
static unsigned long mem_cgroup_shrink_node(struct mem_cgroup *memcg,
                                            struct pglist_data *pgdat,
                                            unsigned long nr_to_scan) {
    // 扫描容器内的页面
    // 回收非活跃页面
    return shrink_list(lru_list, nr_to_scan, memcg, pgdat);
}
```

---

## 8 相关文档

### 8.1 详细机制文档

- **[进程与线程](02-process-thread.md)** - 进程地址空间管理
- **[系统调用机制](07-syscall.md)** - mmap、munmap 系统调用
- **[Cgroup 机制详解](09-cgroup.md)** - 内存限制机制

### 8.2 容器化基础机制

- **[Namespace 机制详解](08-namespace.md)** - 进程隔离机制
- **[Cgroup 机制详解](09-cgroup.md)** - 内存资源限制

### 8.3 架构分析

- **[隔离栈分析](../08-architecture-analysis/isolation-stack/)** - 隔离机制层次分析
- **[容器化架构视角](../../ARCHITECTURE/02-views/02-virtualization-containerization-sandboxing/)** - 容器化抽象层

---

---

## 2025 年最新实践

### 内存管理应用最佳实践（2025）

**2025 年趋势**：内存管理在容器内存、云原生内存、边缘内存中的深度应用

**实践要点**：

- **容器内存**：使用 Cgroup v2 进行容器内存管理
- **内存性能优化**：使用内存压缩和内存回收优化内存使用
- **内存隔离**：使用内存命名空间进行内存隔离

**代码示例**：

```yaml
# 2025 年 Kubernetes 内存配置
apiVersion: v1
kind: Pod
metadata:
  name: memory-pod
spec:
  containers:
  - name: app
    image: nginx:latest
    resources:
      requests:
        memory: "128Mi"
      limits:
        memory: "256Mi"
```

## 实际应用案例

### 案例 1：容器内存性能优化（2025）

**场景**：使用 Cgroup v2 优化容器内存管理

**实现方案**：

```bash
# 使用 Cgroup v2 进行内存管理
# 设置内存限制
echo "256M" > /sys/fs/cgroup/memory/memory.limit_in_bytes

# 监控内存使用
cat /sys/fs/cgroup/memory/memory.usage_in_bytes
```

**效果**：

- 内存管理：精确控制容器内存使用
- 内存监控：实时监控内存使用情况
- 内存优化：自动优化内存配置

---

**最后更新**：2025-11-15
**文档状态**：✅ 完整 | 📊 包含内核实现分析、2025 年最新实践、实际应用案例 | 🎯 生产就绪
**维护者**：项目团队

> **📊 2025 年技术趋势参考**：详细技术状态和版本信息请查看
> [27. 2025 年技术趋势汇总](../10-reference-trends/2025-trends/2025-trends.md)
