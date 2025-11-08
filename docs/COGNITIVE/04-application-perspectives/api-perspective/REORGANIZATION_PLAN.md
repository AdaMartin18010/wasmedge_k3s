# API 规范视角文档集重组方案

**版本**：v2.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📋 重组目标

将 79 个子文件夹重新组织为更合理的分类结构，减少目录层级，提高可维护性和可发现性
。

## 🎯 新的分类方案

### 分类原则

基于 **API 规范四元组** `⟨IDL, Governance, Observability, Security⟩` 和实际使用
场景，将文档分为以下 10 个大类：

### 新的目录结构

```text
docs/COGNITIVE/16-api-perspective/
├── README.md                    # 主索引文档
├── SUMMARY.md                   # 文档总结
│
├── 00-foundation/               # 基础理论（7个文档）
│   ├── 01-formalization.md      # 形式化定义
│   ├── 02-theoretical-foundation.md  # 理论基础
│   ├── 03-comparison-matrix.md  # 对比矩阵
│   ├── 04-api-evolution.md      # API 演进路径
│   ├── 05-best-practices.md     # 最佳实践
│   ├── 06-2025-ecosystem.md     # 2025 技术生态
│   └── 07-case-studies.md       # 实际案例
│
├── 01-runtime/                  # 运行时技术（4个文档）
│   ├── 01-containerization.md   # 容器化 API
│   ├── 02-sandboxing.md         # 沙盒化 API
│   ├── 03-wasm.md               # WASM 化 API
│   └── 04-kubernetes-130.md     # Kubernetes 1.30+ API
│
├── 02-idl/                      # IDL 与协议（5个文档）
│   ├── 01-rest.md               # RESTful API
│   ├── 02-grpc.md               # gRPC API
│   ├── 03-graphql.md            # GraphQL API
│   ├── 04-websocket.md          # WebSocket API
│   └── 05-webhook.md            # Webhook API
│
├── 03-governance/               # 治理与管理（15个文档）
│   ├── 01-api-versioning.md     # 版本管理
│   ├── 02-api-lifecycle.md      # 生命周期
│   ├── 03-api-standardization.md # 标准化
│   ├── 04-api-ecosystem.md      # 生态系统
│   ├── 05-api-governance.md     # 治理规范
│   ├── 06-api-management.md    # API 管理
│   ├── 07-api-design.md         # API 设计
│   ├── 08-api-orchestration.md  # 编排
│   ├── 09-api-workflow.md       # 工作流
│   ├── 10-api-policy.md         # 策略
│   ├── 11-api-discovery.md     # 发现
│   ├── 12-api-catalog.md        # 目录
│   ├── 13-api-proxy.md          # 代理
│   ├── 14-api-transformation.md # 转换
│   └── 15-api-integration.md    # 集成
│
├── 04-observability/            # 可观测性（6个文档）
│   ├── 01-api-observability.md  # 可观测性规范
│   ├── 02-api-logging.md       # 日志
│   ├── 03-api-metrics.md        # 指标
│   ├── 04-api-tracing.md        # 追踪
│   ├── 05-api-monitoring.md     # 监控告警
│   └── 06-api-troubleshooting.md # 故障排查
│
├── 05-security/                 # 安全（7个文档）
│   ├── 01-api-security.md       # 安全规范
│   ├── 02-api-authentication.md # 认证
│   ├── 03-api-authorization.md  # 授权
│   ├── 04-api-data-privacy.md   # 数据隐私
│   ├── 05-api-security-audit.md # 安全审计
│   ├── 06-api-security-testing.md # 安全测试
│   └── 07-api-compliance.md     # 合规性
│
├── 06-quality/                  # 质量保证（8个文档）
│   ├── 01-api-testing.md        # 测试规范
│   ├── 02-api-contract-testing.md # 契约测试
│   ├── 03-api-mocking.md        # Mock 测试
│   ├── 04-api-performance-testing.md # 性能测试
│   ├── 05-api-quality-assurance.md # 质量保证
│   ├── 06-api-benchmarks.md     # 基准测试
│   ├── 07-api-compatibility.md  # 兼容性
│   └── 08-api-deprecation.md    # 废弃策略
│
├── 07-performance/              # 性能优化（3个文档）
│   ├── 01-api-performance.md    # 性能优化规范
│   ├── 02-api-caching.md        # 缓存
│   └── 03-api-cost-optimization.md # 成本优化
│
├── 08-operations/               # 运维运营（8个文档）
│   ├── 01-api-migration.md      # 迁移指南
│   ├── 02-api-monitoring.md     # 监控（与可观测性重复，需合并）
│   ├── 03-api-disaster-recovery.md # 灾难恢复
│   ├── 04-api-multi-region.md   # 多区域部署
│   ├── 05-api-edge-computing.md # 边缘计算
│   ├── 06-api-sla.md            # SLA
│   ├── 07-api-billing.md        # 计费
│   └── 08-api-analytics.md      # 分析
│
├── 09-architecture/             # 架构模式（5个文档）
│   ├── 01-api-event-driven.md   # 事件驱动
│   ├── 02-api-microservices.md  # 微服务
│   ├── 03-api-serverless.md     # 无服务器
│   ├── 04-api-ai-ml.md          # AI/ML 集成
│   └── 05-api-recommendations.md # 推荐系统
│
└── 10-tooling/                  # 工具与平台（7个文档）
    ├── 01-api-dev-toolchain.md  # 开发工具链
    ├── 02-api-documentation.md  # 文档生成
    ├── 03-api-gateway.md        # API 网关
    ├── 04-api-data-validation.md # 数据验证
    ├── 05-api-error-handling.md  # 错误处理
    ├── 06-api-rate-limiting.md   # 限流
    └── 07-api-community.md      # 社区
```

## 📊 重组统计

### 重组前后对比

| 维度               | 重组前 | 重组后 | 变化  |
| ------------------ | ------ | ------ | ----- |
| **顶级目录数**     | 79     | 11     | -86%  |
| **平均每类文档数** | 1      | 6.4    | +540% |
| **目录层级**       | 2 层   | 2 层   | 不变  |
| **可发现性**       | 低     | 高     | 提升  |

### 分类统计

| 分类                 | 文档数 | 说明                |
| -------------------- | ------ | ------------------- |
| **00-foundation**    | 7      | 理论基础和核心概念  |
| **01-runtime**       | 4      | 运行时技术栈        |
| **02-idl**           | 5      | 接口定义语言和协议  |
| **03-governance**    | 15     | 治理和管理相关      |
| **04-observability** | 6      | 可观测性三大支柱    |
| **05-security**      | 7      | 安全相关            |
| **06-quality**       | 8      | 质量保证和测试      |
| **07-performance**   | 3      | 性能优化            |
| **08-operations**    | 8      | 运维和运营          |
| **09-architecture**  | 5      | 架构模式            |
| **10-tooling**       | 7      | 工具和平台          |
| **总计**             | 75     | 不含 README/SUMMARY |

## 🔄 迁移映射表

### 00-foundation/

| 原路径                                                        | 新路径                                       |
| ------------------------------------------------------------- | -------------------------------------------- |
| `07-formalization/formalization.md`                           | `00-foundation/01-formalization.md`          |
| `79-api-theoretical-foundation/api-theoretical-foundation.md` | `00-foundation/02-theoretical-foundation.md` |
| `05-comparison-matrix/comparison-matrix.md`                   | `00-foundation/03-comparison-matrix.md`      |
| `06-api-evolution/api-evolution.md`                           | `00-foundation/04-api-evolution.md`          |
| `08-best-practices/best-practices.md`                         | `00-foundation/05-best-practices.md`         |
| `04-2025-ecosystem/2025-ecosystem.md`                         | `00-foundation/06-2025-ecosystem.md`         |
| `10-case-studies/case-studies.md`                             | `00-foundation/07-case-studies.md`           |

### 01-runtime/

| 原路径                                            | 新路径                              |
| ------------------------------------------------- | ----------------------------------- |
| `01-containerization-api/containerization-api.md` | `01-runtime/01-containerization.md` |
| `02-sandboxing-api/sandboxing-api.md`             | `01-runtime/02-sandboxing.md`       |
| `03-wasm-api/wasm-api.md`                         | `01-runtime/03-wasm.md`             |
| `09-kubernetes-130-api/kubernetes-130-api.md`     | `01-runtime/04-kubernetes-130.md`   |

### 02-idl/

| 原路径                              | 新路径                   |
| ----------------------------------- | ------------------------ |
| `41-api-rest/api-rest.md`           | `02-idl/01-rest.md`      |
| `40-api-grpc/api-grpc.md`           | `02-idl/02-grpc.md`      |
| `39-api-graphql/api-graphql.md`     | `02-idl/03-graphql.md`   |
| `42-api-websocket/api-websocket.md` | `02-idl/04-websocket.md` |
| `43-api-webhook/api-webhook.md`     | `02-idl/05-webhook.md`   |

### 03-governance/

| 原路径                                          | 新路径                                    |
| ----------------------------------------------- | ----------------------------------------- |
| `23-api-versioning/api-versioning.md`           | `03-governance/01-api-versioning.md`      |
| `24-api-lifecycle/api-lifecycle.md`             | `03-governance/02-api-lifecycle.md`       |
| `25-api-standardization/api-standardization.md` | `03-governance/03-api-standardization.md` |
| `26-api-ecosystem/api-ecosystem.md`             | `03-governance/04-api-ecosystem.md`       |
| `13-api-governance/api-governance.md`           | `03-governance/05-api-governance.md`      |
| `58-api-api-management/api-api-management.md`   | `03-governance/06-api-management.md`      |
| `57-api-api-design/api-api-design.md`           | `03-governance/07-api-design.md`          |
| `71-api-orchestration/api-orchestration.md`     | `03-governance/08-api-orchestration.md`   |
| `72-api-workflow/api-workflow.md`               | `03-governance/09-api-workflow.md`        |
| `73-api-policy/api-policy.md`                   | `03-governance/10-api-policy.md`          |
| `75-api-discovery/api-discovery.md`             | `03-governance/11-api-discovery.md`       |
| `76-api-catalog/api-catalog.md`                 | `03-governance/12-api-catalog.md`         |
| `77-api-proxy/api-proxy.md`                     | `03-governance/13-api-proxy.md`           |
| `78-api-transformation/api-transformation.md`   | `03-governance/14-api-transformation.md`  |
| `70-api-integration/api-integration.md`         | `03-governance/15-api-integration.md`     |

### 04-observability/

| 原路径                                              | 新路径                                            |
| --------------------------------------------------- | ------------------------------------------------- |
| `12-api-observability/api-observability.md`         | `04-observability/01-api-observability.md`        |
| `60-api-api-observability/api-api-observability.md` | `04-observability/01-api-observability.md` (合并) |
| `48-api-logging/api-logging.md`                     | `04-observability/02-api-logging.md`              |
| `49-api-metrics/api-metrics.md`                     | `04-observability/03-api-metrics.md`              |
| `50-api-tracing/api-tracing.md`                     | `04-observability/04-api-tracing.md`              |
| `20-api-monitoring/api-monitoring.md`               | `04-observability/05-api-monitoring.md`           |
| `18-api-troubleshooting/api-troubleshooting.md`     | `04-observability/06-api-troubleshooting.md`      |

### 05-security/

| 原路径                                            | 新路径                                   |
| ------------------------------------------------- | ---------------------------------------- |
| `11-api-security/api-security.md`                 | `05-security/01-api-security.md`         |
| `61-api-authentication/api-authentication.md`     | `05-security/02-api-authentication.md`   |
| `62-api-authorization/api-authorization.md`       | `05-security/03-api-authorization.md`    |
| `63-api-data-privacy/api-data-privacy.md`         | `05-security/04-api-data-privacy.md`     |
| `28-api-security-audit/api-security-audit.md`     | `05-security/05-api-security-audit.md`   |
| `54-api-security-testing/api-security-testing.md` | `05-security/06-api-security-testing.md` |
| `22-api-compliance/api-compliance.md`             | `05-security/07-api-compliance.md`       |

### 06-quality/

| 原路径                                                  | 新路径                                     |
| ------------------------------------------------------- | ------------------------------------------ |
| `15-api-testing/api-testing.md`                         | `06-quality/01-api-testing.md`             |
| `51-api-contract-testing/api-contract-testing.md`       | `06-quality/02-api-contract-testing.md`    |
| `52-api-mocking/api-mocking.md`                         | `06-quality/03-api-mocking.md`             |
| `53-api-performance-testing/api-performance-testing.md` | `06-quality/04-api-performance-testing.md` |
| `29-api-quality-assurance/api-quality-assurance.md`     | `06-quality/05-api-quality-assurance.md`   |
| `27-api-benchmarks/api-benchmarks.md`                   | `06-quality/06-api-benchmarks.md`          |
| `56-api-compatibility/api-compatibility.md`             | `06-quality/07-api-compatibility.md`       |
| `55-api-deprecation/api-deprecation.md`                 | `06-quality/08-api-deprecation.md`         |

### 07-performance/

| 原路径                                              | 新路径                                       |
| --------------------------------------------------- | -------------------------------------------- |
| `14-api-performance/api-performance.md`             | `07-performance/01-api-performance.md`       |
| `45-api-caching/api-caching.md`                     | `07-performance/02-api-caching.md`           |
| `21-api-cost-optimization/api-cost-optimization.md` | `07-performance/03-api-cost-optimization.md` |

### 08-operations/

| 原路径                                              | 新路径                                      |
| --------------------------------------------------- | ------------------------------------------- |
| `19-api-migration/api-migration.md`                 | `08-operations/01-api-migration.md`         |
| `32-api-disaster-recovery/api-disaster-recovery.md` | `08-operations/02-api-disaster-recovery.md` |
| `33-api-multi-region/api-multi-region.md`           | `08-operations/03-api-multi-region.md`      |
| `34-api-edge-computing/api-edge-computing.md`       | `08-operations/04-api-edge-computing.md`    |
| `66-api-sla/api-sla.md`                             | `08-operations/05-api-sla.md`               |
| `67-api-billing/api-billing.md`                     | `08-operations/06-api-billing.md`           |
| `68-api-analytics/api-analytics.md`                 | `08-operations/07-api-analytics.md`         |
| `69-api-marketplace/api-marketplace.md`             | `08-operations/08-api-marketplace.md`       |

### 09-architecture/

| 原路径                                          | 新路径                                      |
| ----------------------------------------------- | ------------------------------------------- |
| `35-api-event-driven/api-event-driven.md`       | `09-architecture/01-api-event-driven.md`    |
| `36-api-microservices/api-microservices.md`     | `09-architecture/02-api-microservices.md`   |
| `37-api-serverless/api-serverless.md`           | `09-architecture/03-api-serverless.md`      |
| `38-api-ai-ml/api-ai-ml.md`                     | `09-architecture/04-api-ai-ml.md`           |
| `74-api-recommendations/api-recommendations.md` | `09-architecture/05-api-recommendations.md` |

### 10-tooling/

| 原路径                                                    | 新路径                                      |
| --------------------------------------------------------- | ------------------------------------------- |
| `30-api-dev-toolchain/api-dev-toolchain.md`               | `10-tooling/01-api-dev-toolchain.md`        |
| `16-api-documentation/api-documentation.md`               | `10-tooling/02-api-documentation.md`        |
| `59-api-api-documentation/api-api-documentation.md`       | `10-tooling/02-api-documentation.md` (合并) |
| `17-api-gateway/api-gateway.md`                           | `10-tooling/03-api-gateway.md`              |
| `46-api-data-validation/api-data-validation.md`           | `10-tooling/04-api-data-validation.md`      |
| `47-api-error-handling/api-error-handling.md`             | `10-tooling/05-api-error-handling.md`       |
| `44-api-rate-limiting/api-rate-limiting.md`               | `10-tooling/06-api-rate-limiting.md`        |
| `31-api-community/api-community.md`                       | `10-tooling/07-api-community.md`            |
| `64-api-multi-tenancy/api-multi-tenancy.md`               | `10-tooling/08-api-multi-tenancy.md`        |
| `65-api-internationalization/api-internationalization.md` | `10-tooling/09-api-internationalization.md` |

## 📝 实施步骤

### 阶段一：创建新目录结构

1. 创建 10 个分类目录
2. 在每个分类目录下创建对应的 Markdown 文件

### 阶段二：迁移文档内容

1. 将原文档内容复制到新位置
2. 更新文档内的交叉引用链接
3. 更新文档的"相关文档"部分

### 阶段三：更新索引文档

1. 更新 `README.md` 的目录结构
2. 更新 `SUMMARY.md` 的文档列表
3. 更新 `api_view.md` 中的引用

### 阶段四：清理旧目录

1. 确认所有文档已迁移
2. 删除旧的目录结构
3. 验证所有链接正常工作

## ⚠️ 注意事项

1. **文档合并**：部分文档需要合并（如 `12-api-observability` 和
   `60-api-api-observability`）
2. **链接更新**：所有文档内的交叉引用需要更新路径
3. **向后兼容**：可以考虑创建符号链接或重定向文件
4. **版本控制**：建议在 Git 中创建分支进行重组

## 🎯 重组优势

1. **可发现性提升**：按功能分类，更容易找到相关文档
2. **维护性提升**：相关文档集中管理，便于更新
3. **结构清晰**：10 个分类覆盖所有 API 规范维度
4. **扩展性好**：新文档可以轻松归类到对应分类

---

**最后更新**：2025-11-07 **维护者**：项目团队
