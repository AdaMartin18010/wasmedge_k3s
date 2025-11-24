# API 文档生成规范

**版本**：v1.0 **最后更新：2025-11-15 **维护者**：项目团队

## 📑 目录

- [API 文档生成规范](#api-文档生成规范)
  - [📑 目录](#-目录)
  - [1 概述](#1-概述)
    - [1.1 文档生成流程](#11-文档生成流程)
    - [1.2 API 文档在 API 规范中的位置](#12-api-文档在-api-规范中的位置)
  - [2 OpenAPI 文档生成](#2-openapi-文档生成)
    - [2.1 Swagger UI 生成](#21-swagger-ui-生成)
    - [2.2 Redoc 生成](#22-redoc-生成)
  - [3 gRPC 文档生成](#3-grpc-文档生成)
    - [3.1 Protoc 文档生成](#31-protoc-文档生成)
    - [3.2 gRPC-Gateway 文档](#32-grpc-gateway-文档)
  - [4 WIT 文档生成](#4-wit-文档生成)
    - [4.1 WIT 文档生成工具](#41-wit-文档生成工具)
    - [4.2 WIT 组件文档](#42-wit-组件文档)
  - [5 文档即代码](#5-文档即代码)
    - [5.1 GitOps 文档管理](#51-gitops-文档管理)
    - [5.2 CI/CD 文档生成](#52-cicd-文档生成)
  - [6 API 文档版本管理](#6-api-文档版本管理)
    - [6.1 文档版本化](#61-文档版本化)
    - [6.2 文档版本控制](#62-文档版本控制)
  - [7 形式化定义与理论基础](#7-形式化定义与理论基础)
    - [7.1 API 文档形式化模型](#71-api-文档形式化模型)
    - [7.2 文档生成形式化](#72-文档生成形式化)
    - [7.3 文档质量形式化](#73-文档质量形式化)
  - [8 相关文档](#8-相关文档)

---

## 1 概述

API 文档生成规范定义了如何从 API 规范自动生成文档，从 OpenAPI 到 gRPC，从 WIT 到
CRD，实现文档即代码的自动化流程。本文档基于形式化方法，提供严格的数学定义和推理
论证，分析 API 文档生成的理论基础和实践方法。

**参考标准**：

- [OpenAPI Specification](https://swagger.io/specification/) - OpenAPI 规范
- [gRPC Documentation](https://grpc.io/docs/) - gRPC 文档规范
- [WIT Documentation](https://github.com/WebAssembly/component-model/blob/main/design/mvp/WIT.md) -
  WIT 文档规范
- [Docs-as-Code](https://www.writethedocs.org/guide/docs-as-code/) - 文档即代码
  最佳实践
- [API Documentation Best Practices](https://swagger.io/resources/articles/adopting-an-api-first-approach/) -
  API 文档最佳实践

### 1.1 文档生成流程

```text
API 规范（OpenAPI/gRPC/WIT）
  ↓
文档生成工具（Swagger/Protoc/WIT）
  ↓
HTML/PDF/Markdown 文档
  ↓
文档发布（GitHub Pages/ReadTheDocs）
```

### 1.2 API 文档在 API 规范中的位置

根据 API 规范四元组定义（见
[API 规范形式化定义](../00-foundation/01-formalization.md#21-api-规范四元组)）
，API 文档是 IDL 维度的输出：

```text
API_Spec = ⟨IDL, Governance, Observability, Security⟩
            ↑
    API Documentation (output of IDL)
```

API 文档在 API 规范中提供：

- **IDL 文档**：从 OpenAPI、gRPC、WIT 等 IDL 生成的文档
- **API 参考**：API 端点、参数、响应格式的详细说明
- **使用示例**：代码示例和使用场景
- **版本管理**：文档版本与 API 版本同步

---

## 2 OpenAPI 文档生成

### 2.1 Swagger UI 生成

**OpenAPI 3.1 定义**：

```yaml
openapi: 3.1.0
info:
  title: Payment API
  version: 1.0.0
  description: Payment service API documentation
paths:
  /api/v1/payments:
    post:
      summary: Create payment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PaymentRequest"
      responses:
        "201":
          description: Payment created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PaymentResponse"
components:
  schemas:
    PaymentRequest:
      type: object
      required:
        - order_id
        - amount
      properties:
        order_id:
          type: string
        amount:
          type: integer
          minimum: 0
    PaymentResponse:
      type: object
      properties:
        payment_id:
          type: string
        status:
          type: string
```

**Swagger UI 部署**：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: swagger-ui
spec:
  replicas: 1
  selector:
    matchLabels:
      app: swagger-ui
  template:
    metadata:
      labels:
        app: swagger-ui
    spec:
      containers:
        - name: swagger-ui
          image: swaggerapi/swagger-ui:latest
          ports:
            - containerPort: 8080
          env:
            - name: SWAGGER_JSON
              value: /api/openapi.yaml
          volumeMounts:
            - name: openapi
              mountPath: /api
      volumes:
        - name: openapi
          configMap:
            name: openapi-spec
```

### 2.2 Redoc 生成

**Redoc 配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redoc-config
data:
  redoc.yaml: |
    theme:
      colors:
        primary:
          main: "#32329f"
    options:
      nativeScrollbars: true
      hideDownloadButton: false
```

---

## 3 gRPC 文档生成

### 3.1 Protoc 文档生成

**protoc-gen-doc 生成**：

```bash
# 安装 protoc-gen-doc
go install github.com/pseudomuto/protoc-gen-doc/cmd/protoc-gen-doc@latest

# 生成 Markdown 文档
protoc \
  --doc_out=./docs \
  --doc_opt=markdown,api.md \
  payment.proto
```

**生成的文档示例**：

```markdown
# Payment Service

## CreatePayment

Creates a new payment.

**Request**

| Field    | Type   | Description    |
| -------- | ------ | -------------- |
| order_id | string | Order ID       |
| amount   | int64  | Payment amount |

**Response**

| Field      | Type   | Description    |
| ---------- | ------ | -------------- |
| payment_id | string | Payment ID     |
| status     | string | Payment status |
```

### 3.2 gRPC-Gateway 文档

**gRPC-Gateway 注解**：

```protobuf
service PaymentService {
  rpc CreatePayment(CreatePaymentRequest) returns (CreatePaymentResponse) {
    option (google.api.http) = {
      post: "/api/v1/payments"
      body: "*"
    };
    option (grpc.gateway.protoc_gen_openapiv2.options.openapiv2_operation) = {
      summary: "Create payment"
      description: "Creates a new payment"
      tags: "payments"
    };
  }
}
```

---

## 4 WIT 文档生成

### 4.1 WIT 文档生成工具

**wit-doc 生成**：

```bash
# 安装 wit-doc
cargo install wit-doc

# 生成文档
wit-doc generate payment.wit --output docs/
```

**生成的文档示例**：

```markdown
# Payment Service

## Interfaces

### payment@1.0.0

Payment processing interface.

#### Functions

##### create_payment

Creates a new payment.

**Parameters**

- `order_id: string` - Order ID
- `amount: u64` - Payment amount

**Returns**

- `result<payment_id, error>` - Payment ID or error
```

### 4.2 WIT 组件文档

**组件文档结构**：

```wit
/// Payment service component
///
/// This component provides payment processing capabilities.
package example:payment@1.0.0;

/// Payment request
///
/// Contains order ID and amount
type payment-request = record {
    /// Order identifier
    order-id: string,
    /// Payment amount in cents
    amount: u64,
};

/// Payment response
///
/// Contains payment ID and status
type payment-response = record {
    /// Payment identifier
    payment-id: string,
    /// Payment status
    status: string,
};
```

---

## 5 文档即代码

### 5.1 GitOps 文档管理

**ArgoCD Application**：

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: api-docs
spec:
  project: default
  source:
    repoURL: https://github.com/example/api-docs
    targetRevision: main
    path: docs
  destination:
    server: https://kubernetes.default.svc
    namespace: api-docs
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 5.2 CI/CD 文档生成

**GitHub Actions 工作流**：

```yaml
name: Generate API Docs

on:
  push:
    branches: [main]
    paths:
      - "api/**/*.proto"
      - "api/**/*.yaml"
      - "api/**/*.wit"

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Generate OpenAPI docs
        run: |
          swagger-codegen generate \
            -i api/openapi.yaml \
            -l html2 \
            -o docs/openapi

      - name: Generate gRPC docs
        run: |
          protoc --doc_out=docs/grpc \
            --doc_opt=markdown,api.md \
            api/**/*.proto

      - name: Generate WIT docs
        run: |
          wit-doc generate api/**/*.wit --output docs/wit

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

---

## 6 API 文档版本管理

### 6.1 文档版本化

**版本化文档结构**：

```text
docs/
├── v1/
│   ├── openapi.yaml
│   └── index.html
├── v2/
│   ├── openapi.yaml
│   └── index.html
└── latest -> v2
```

### 6.2 文档版本控制

**文档版本 CRD**：

```yaml
apiVersion: api.example.com/v1
kind: APIDocumentation
metadata:
  name: payment-api-docs
spec:
  apiVersion: "1.0.0"
  openapi: "3.1.0"
  lifecycle: active
  deprecationPolicy:
    sunsetDate: "2025-12-31"
    replacement: "payment-api-docs-v2"
```

---

## 7 形式化定义与理论基础

### 7.1 API 文档形式化模型

**定义 7.1（API 文档）**：API 文档是一个三元组：

```text
API_Documentation = ⟨IDL, Generator, Output⟩
```

其中：

- **IDL**：接口定义语言 `IDL: {OpenAPI, gRPC, WIT}`
- **Generator**：文档生成器 `Generator: IDL → Documentation`
- **Output**：文档输出 `Output: {HTML, PDF, Markdown}`

**定义 7.2（文档完整性）**：文档完整性是一个函数：

```text
Documentation_Completeness(Doc) = f(Endpoint_Coverage, Parameter_Coverage, Example_Coverage)
```

其中：

- **Endpoint_Coverage**：端点覆盖度 `[0, 1]`
- **Parameter_Coverage**：参数覆盖度 `[0, 1]`
- **Example_Coverage**：示例覆盖度 `[0, 1]`

**定理 7.1（文档完备性）**：如果文档完整性为 1，则文档完备：

```text
Documentation_Completeness(Doc) = 1 ⟹ Complete(Doc)
```

**证明**：如果端点、参数和示例覆盖度都为 1，则所有 API 元素都有文档，因此文档完
备。□

### 7.2 文档生成形式化

**定义 7.3（文档生成）**：文档生成是一个函数：

```text
Generate_Documentation: IDL × Generator → Documentation
```

**定义 7.4（文档一致性）**：文档与 IDL 一致，当且仅当：

```text
Consistent(Doc, IDL) ⟺ ∀ endpoint ∈ IDL: ∃ doc ∈ Doc: doc.describes(endpoint)
```

**定理 7.2（文档生成一致性）**：生成的文档与 IDL 一致：

```text
Doc = Generate_Documentation(IDL, Generator) ⟹ Consistent(Doc, IDL)
```

**证明**：根据定义 7.3，文档生成器从 IDL 生成文档，因此生成的文档与 IDL 一致。□

**定义 7.5（文档版本同步）**：文档版本与 API 版本同步：

```text
Version_Sync(Doc, API) ⟺ Doc.version = API.version
```

**定理 7.3（版本同步性）**：如果文档版本与 API 版本同步，则文档准确：

```text
Version_Sync(Doc, API) ⟹ Accurate(Doc, API)
```

**证明**：如果文档版本与 API 版本同步，则文档反映当前 API 版本的状态，因此文档准
确。□

### 7.3 文档质量形式化

**定义 7.6（文档质量）**：文档质量是一个函数：

```text
Documentation_Quality(Doc) = f(Completeness, Accuracy, Clarity, Usability)
```

其中：

- **Completeness**：完整性 `[0, 1]`
- **Accuracy**：准确性 `[0, 1]`
- **Clarity**：清晰度 `[0, 1]`
- **Usability**：可用性 `[0, 1]`

**定理 7.4（文档质量最优性）**：文档质量越高，文档越好：

```text
Documentation_Quality(Doc₁) > Documentation_Quality(Doc₂) ⟹ Quality(Doc₁) > Quality(Doc₂)
```

**证明**：根据定义 7.6，文档质量越高，完整性、准确性、清晰度和可用性越高，因此文
档质量越好。□

**定义 7.7（文档可维护性）**：文档可维护性是一个函数：

```text
Maintainability(Doc) = f(Automation_Level, Version_Control, Update_Frequency)
```

**定理 7.5（文档即代码优势）**：文档即代码方法提高可维护性：

```text
Docs_as_Code(Doc) ⟹ Maintainability(Doc) > Manual_Documentation(Doc)
```

**证明**：文档即代码方法使用自动化工具和版本控制，因此可维护性高于手动文档。□

---

## 8 相关文档

- **[容器化 API 规范](../01-containerization-api/containerization-api.md)** -
  Kubernetes CRD API 文档
- **[WASM 化 API 规范](../03-wasm-api/wasm-api.md)** - WIT 文档生成
- **[最佳实践](../00-foundation/05-best-practices.md)** - API 文档最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

---

**最后更新：2025-11-15 **维护者**：项目团队
