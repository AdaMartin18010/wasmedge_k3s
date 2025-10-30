# 规划：ai_view 全面拆解与产出目录

- 目标：将 ai_view.md 的主题与子主题结构化，形成可维护的知识库与配套资料。
- 输出：分主题目录 + 主题名文件（非 README）+ 横向规范与清单。

## 目录与文件

- 01-overview/overview.md
- 02-principles/principles.md
- 03-architecture/architecture.md
- 04-docker/docker.md
- 05-kubernetes/kubernetes.md
- 06-k3s/k3s.md
- 07-wasm-edge/wasmedge.md
- 08-orchestration-runtime/orchestration-runtime.md
- 09-oci-supply-chain/oci-supply-chain.md
- 10-policy-opa/policy-opa.md
- 11-edge-serverless/edge-serverless.md
- 12-ai-inference/ai-inference.md
- 13-security-compliance/security-compliance.md
- 14-benchmarks/benchmarks.md
- 15-installation/installation.md
- 16-troubleshooting/troubleshooting.md
- REFERENCES.md
- README.md（docs 总索引）
- assets/

## 填充顺序

1. 01-overview → 02-principles → 03-architecture
2. 04-06 单体与编排差异、K3s 精简点
3. 07-12 WasmEdge 路线、OPA、Edge/Serverless、AI 推理
4. 13 安全合规与签名、14 性能基线
5. 15-16 装配脚本与常见坑

## 统一规范

- Markdown：遵循仓库 .markdownlint.jsonc 与 .prettierrc
- 语法：表格带对齐行、代码块标注语言、标题层级从 `#`
- 引用：每条事实附“来源/时间/版本”，录入 REFERENCES.md 并在文末列出

## 参考登记流程

- 收集：并行检索权威来源（官方发布/Release Notes/文档）
- 登记：在 REFERENCES.md 填 URL/日期/版本，并给出简述
- 标注：在对应章节末尾追加“参考”小节，列出编号
