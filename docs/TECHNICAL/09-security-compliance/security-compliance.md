# 09. 安全与合规：零信任、镜像签名、策略治理

## 📑 目录

- [📑 目录](#-目录)
- [09.1 文档定位](#091-文档定位)
- [09.2 零信任架构](#092-零信任架构)
  - [09.2.1 零信任概念](#0921-零信任概念)
  - [09.2.2 零信任原则](#0922-零信任原则)
  - [09.2.3 零信任实现](#0923-零信任实现)
- [09.3 镜像签名与验证](#093-镜像签名与验证)
  - [09.3.1 镜像签名方案](#0931-镜像签名方案)
  - [09.3.2 签名验证流程](#0932-签名验证流程)
  - [09.3.3 签名场景与决策](#0933-签名场景与决策)
- [09.4 策略治理](#094-策略治理)
  - [09.4.1 OPA 策略治理](#0941-opa-策略治理)
  - [09.4.2 Gatekeeper 集成](#0942-gatekeeper-集成)
  - [09.4.3 Kyverno 集成](#0943-kyverno-集成)
- [09.5 FIPS 与行业合规](#095-fips-与行业合规)
  - [09.5.1 FIPS 合规](#0951-fips-合规)
  - [09.5.2 行业合规要求](#0952-行业合规要求)
  - [09.5.3 合规场景与决策](#0953-合规场景与决策)
- [09.6 数据安全](#096-数据安全)
  - [09.6.1 数据加密](#0961-数据加密)
  - [09.6.2 数据脱敏](#0962-数据脱敏)
  - [09.6.3 OPA-Wasm 数据脱敏](#0963-opa-wasm-数据脱敏)
- [09.7 技术场景分析](#097-技术场景分析)
  - [09.7.1 生产环境安全场景](#0971-生产环境安全场景)
  - [09.7.2 合规场景](#0972-合规场景)
  - [09.7.3 零信任场景](#0973-零信任场景)
- [09.8 决策依据与思路](#098-决策依据与思路)
  - [09.8.1 安全策略决策树](#0981-安全策略决策树)
  - [09.8.2 镜像签名决策树](#0982-镜像签名决策树)
  - [09.8.3 策略治理决策树](#0983-策略治理决策树)
- [09.9 形式化总结](#099-形式化总结)
  - [09.9.1 零信任模型形式化](#0991-零信任模型形式化)
  - [09.9.2 安全策略模型形式化](#0992-安全策略模型形式化)
- [09.10 供应链安全最佳实践](#0910-供应链安全最佳实践)
  - [09.10.1 供应链安全概述](#09101-供应链安全概述)
  - [09.10.2 SBOM（软件物料清单）](#09102-sbom软件物料清单)
  - [09.10.3 依赖项漏洞扫描](#09103-依赖项漏洞扫描)
  - [09.10.4 镜像签名和验证完整流程](#09104-镜像签名和验证完整流程)
  - [09.10.5 Kubernetes 准入控制集成](#09105-kubernetes-准入控制集成)
  - [09.10.6 实际安全案例](#09106-实际安全案例)
    - [案例 1：Log4Shell 漏洞应对](#案例-1log4shell-漏洞应对)
    - [案例 2：供应链攻击防范](#案例-2供应链攻击防范)
    - [案例 3：密钥管理最佳实践](#案例-3密钥管理最佳实践)
  - [09.10.7 安全合规检查清单](#09107-安全合规检查清单)
  - [09.10.8 安全工具集成矩阵](#09108-安全工具集成矩阵)
- [09.11 参考](#0911-参考)
  - [09.11.1 2025 年最新更新（2025-11-06）](#09111-2025-年最新更新2025-11-06)
  - [09.11.2 隔离栈相关文档](#09112-隔离栈相关文档)
  - [09.11.3 安全相关文档](#09113-安全相关文档)
  - [09.11.4 其他相关文档](#09114-其他相关文档)

---

## 09.1 文档定位

本文档深入解析安全与合规场景下的技术方案，包括零信任架构、镜像签名与验证、策略治
理和 FIPS/行业合规的技术原理、实现方式和最佳实践。

**文档结构**：

- **零信任架构**：零信任概念、原则和实现方案
- **镜像签名**：镜像签名方案、验证流程和场景决策
- **策略治理**：OPA、Gatekeeper、Kyverno 的策略治理方案
- **FIPS 合规**：FIPS 合规和行业合规要求
- **数据安全**：数据加密、脱敏和 OPA-Wasm 数据脱敏
- **技术场景**：生产环境、合规、零信任场景的架构设计

## 09.2 零信任架构

### 09.2.1 零信任概念

**定义**：零信任（Zero Trust）是一种安全架构，默认不信任任何实体，需要持续验证。

**核心原则**：

- **永不信任，始终验证**：默认不信任，需要持续验证
- **最小权限**：只授予必要的权限
- **微分段**：网络和资源分段隔离

### 09.2.2 零信任原则

**零信任原则**：

1. **身份验证**：所有实体必须验证身份
2. **设备验证**：所有设备必须验证
3. **网络验证**：所有网络通信必须验证
4. **资源验证**：所有资源访问必须验证

**零信任原则论证**：

- **身份验证**：确保只有授权用户访问
- **设备验证**：确保只有授权设备访问
- **网络验证**：确保网络通信安全
- **资源验证**：确保资源访问安全

### 09.2.3 零信任实现

**零信任实现方案**：

```yaml
零信任实现:
  身份验证: OIDC/OAuth2（用户身份）
  设备验证: 设备证书（设备身份）
  网络验证: mTLS（网络通信）
  资源验证: RBAC + OPA（资源访问）
  优势: 全面验证、最小权限、微分段
```

**零信任实现论证**：

- **身份验证**：使用 OIDC/OAuth2 验证用户身份
- **设备验证**：使用设备证书验证设备身份
- **网络验证**：使用 mTLS 加密网络通信
- **资源验证**：使用 RBAC + OPA 控制资源访问

## 09.3 镜像签名与验证

### 09.3.1 镜像签名方案

**镜像签名方案**：

- **Cosign**：Sigstore 项目的镜像签名工具
- **Notary**：Docker Content Trust 的签名工具
- **自定义签名**：使用自定义签名方案

**镜像签名方案论证**：

- **Cosign**：基于 OCI Artifact，标准签名格式，推荐使用
- **Notary**：Docker 官方工具，但功能有限
- **自定义签名**：灵活但需要自己维护

### 09.3.2 签名验证流程

**签名验证流程**：

```mermaid
graph LR
    A[拉取镜像] --> B[验证签名]
    B --> C{签名有效?}
    C -->|是| D[部署 Pod]
    C -->|否| E[拒绝部署]

    style C fill:#ffe6e6
    style D fill:#e6ffe6
    style E fill:#ffcccc
```

**签名验证流程论证**：

1. **拉取镜像**：从镜像仓库拉取镜像
2. **验证签名**：使用公钥验证镜像签名
3. **准入控制**：通过 Kubernetes 准入控制验证签名
4. **部署决策**：签名有效则部署，无效则拒绝

### 09.3.3 签名场景与决策

**场景 1：生产环境**:

**决策依据**：

- ✅ 必须签名所有镜像
- ✅ 必须验证签名
- ✅ 签名验证失败必须拒绝部署

**决策思路**：

```yaml
生产环境签名策略:
  签名: 必须签名所有镜像（Cosign）
  验证: Kubernetes 准入控制（强制验证）
  失败处理: 签名验证失败必须拒绝部署
  优势: 完整性验证、来源验证、合规要求
```

**场景 2：合规场景**:

**决策依据**：

- ✅ 满足合规要求（如 EO 14028）
- ✅ 完整的签名审计
- ✅ 签名密钥管理

**决策思路**：

```yaml
合规场景签名策略:
  签名: 必须签名所有镜像 + SBOM（Cosign）
  验证: Kubernetes 准入控制（强制验证）
  审计: 完整的签名和验证记录
  密钥管理: Sigstore 密钥管理
  优势: 合规要求、完整审计、密钥管理
```

## 09.4 策略治理

### 09.4.1 OPA 策略治理

**OPA 策略治理**：使用 OPA 定义和执行安全策略。

**策略类型**：

- **准入控制策略**：Kubernetes 准入控制策略
- **授权策略**：API 授权策略
- **数据策略**：数据访问策略

**OPA 策略治理论证**：

- **策略即代码**：策略以代码形式定义，可版本控制
- **通用引擎**：支持多种场景（Kubernetes、API、微服务等）
- **声明式**：使用 Rego 语言，声明式定义策略

### 09.4.2 Gatekeeper 集成

**Gatekeeper**：Kubernetes 准入控制器，使用 OPA 策略。

**Gatekeeper 特点**：

- **准入控制**：Kubernetes 准入控制
- **OPA 集成**：使用 OPA 策略引擎
- **策略模板**：支持策略模板和约束

**Gatekeeper 集成论证**：

- **准入控制**：通过 Kubernetes 准入控制执行策略
- **OPA 集成**：使用 OPA 策略引擎，灵活定义策略
- **策略模板**：支持策略模板，便于复用

### 09.4.3 Kyverno 集成

**Kyverno**：Kubernetes 原生策略引擎，使用 YAML 定义策略。

**Kyverno 特点**：

- **原生集成**：Kubernetes 原生策略引擎
- **YAML 策略**：使用 YAML 定义策略，简单易用
- **策略类型**：支持验证、变更、生成策略

**Kyverno 集成论证**：

- **原生集成**：Kubernetes 原生策略引擎，无需额外组件
- **YAML 策略**：使用 YAML 定义策略，简单易用
- **策略类型**：支持验证、变更、生成策略，功能完整

## 09.5 FIPS 与行业合规

### 09.5.1 FIPS 合规

**FIPS 合规**：FIPS（Federal Information Processing Standards）是美国联邦信息处
理标准。

**FIPS 要求**：

- **加密算法**：使用 FIPS 批准的加密算法
- **随机数生成**：使用 FIPS 批准的随机数生成器
- **密钥管理**：使用 FIPS 批准的密钥管理方案

**FIPS 合规论证**：

- **加密算法**：使用 FIPS 批准的加密算法（如 AES-256）
- **随机数生成**：使用 FIPS 批准的随机数生成器
- **密钥管理**：使用 FIPS 批准的密钥管理方案

### 09.5.2 行业合规要求

**行业合规要求**：

- **HIPAA**：医疗保健行业合规
- **PCI DSS**：支付卡行业合规
- **GDPR**：数据保护合规
- **SOC 2**：服务组织控制合规

**行业合规论证**：

- **HIPAA**：医疗保健数据保护和隐私要求
- **PCI DSS**：支付卡数据安全标准
- **GDPR**：欧盟数据保护法规
- **SOC 2**：服务组织控制标准

### 09.5.3 合规场景与决策

**场景 1：FIPS 合规场景**:

**决策依据**：

- ✅ 必须使用 FIPS 批准的加密算法
- ✅ 必须使用 FIPS 批准的随机数生成器
- ✅ 必须使用 FIPS 批准的密钥管理方案

**决策思路**：

```yaml
FIPS 合规策略:
  加密算法: FIPS 批准算法（AES-256）
  随机数生成: FIPS 批准随机数生成器
  密钥管理: FIPS 批准密钥管理方案
  优势: FIPS 合规、安全性高
```

**场景 2：行业合规场景**:

**决策依据**：

- ✅ 满足行业合规要求（HIPAA、PCI DSS、GDPR、SOC 2）
- ✅ 数据保护和隐私要求
- ✅ 审计和报告要求

**决策思路**：

```yaml
行业合规策略:
  合规标准: HIPAA/PCI DSS/GDPR/SOC 2
  数据保护: 数据加密、访问控制
  审计: 完整的审计日志和报告
  优势: 行业合规、数据保护、审计能力
```

## 09.6 数据安全

### 09.6.1 数据加密

**数据加密方案**：

- **传输加密**：使用 TLS/mTLS 加密数据传输
- **存储加密**：使用加密存储（如加密 Volume）
- **应用加密**：在应用层加密敏感数据

**数据加密论证**：

- **传输加密**：使用 TLS/mTLS 加密数据传输，防止数据泄露
- **存储加密**：使用加密存储，防止存储数据泄露
- **应用加密**：在应用层加密敏感数据，多层防护

### 09.6.2 数据脱敏

**数据脱敏方案**：

- **静态脱敏**：在存储时脱敏数据
- **动态脱敏**：在访问时脱敏数据
- **策略脱敏**：使用策略定义脱敏规则

**数据脱敏论证**：

- **静态脱敏**：在存储时脱敏数据，保护存储数据
- **动态脱敏**：在访问时脱敏数据，保护访问数据
- **策略脱敏**：使用策略定义脱敏规则，灵活控制

### 09.6.3 OPA-Wasm 数据脱敏

> **💡 隔离层次关联**：OPA-Wasm 数据脱敏使用 L-4 沙盒化层的 WASM 运行时
> （WasmEdge）进行快速策略执行。详细的技术解析请参考：
>
> - **[29. 隔离栈](../29-isolation-stack/isolation-stack.md)** - 完整的隔离栈技
>   术解析
> - **[L-4 沙盒化层](../29-isolation-stack/layers/L-4-sandboxing.md)** - WASM 运
>   行时详细文档
> - **[隔离层次对比文档](../29-isolation-stack/layers/isolation-comparison.md)** -
>   WASM 性能对比和安全特点

**OPA-Wasm 数据脱敏**：使用 OPA-Wasm 进行细粒度数据脱敏。

**OPA-Wasm 数据脱敏方案**：

```yaml
OPA-Wasm 数据脱敏:
  策略: Rego 策略（编译到 Wasm）
  执行: WasmEdge（快速执行）
  场景: API 网关、数据访问
  优势: 细粒度控制、快速执行、策略即代码
```

**OPA-Wasm 数据脱敏论证**：

- **细粒度控制**：使用 Rego 策略定义脱敏规则，细粒度控制
- **快速执行**：Wasm 执行快，满足实时脱敏要求
- **策略即代码**：策略以代码形式定义，可版本控制

## 09.7 技术场景分析

### 09.7.1 生产环境安全场景

**场景描述**：生产环境需要全面的安全保护。

**架构挑战**：

1. **镜像安全**：确保镜像未被篡改
2. **访问控制**：控制资源访问
3. **数据安全**：保护敏感数据

**架构决策**：

```yaml
生产环境安全配置:
  镜像签名: Cosign（必须签名所有镜像）
  准入控制: Gatekeeper/Kyverno（强制策略）
  访问控制: RBAC + OPA（细粒度控制）
  数据加密: TLS/mTLS + 加密存储
  优势: 全面安全、多层防护
```

**决策依据**：

- ✅ **镜像安全**：镜像签名确保镜像完整性
- ✅ **访问控制**：准入控制和 RBAC 控制资源访问
- ✅ **数据安全**：数据加密保护敏感数据

### 09.7.2 合规场景

**场景描述**：需要满足合规要求（FIPS、行业合规）。

**架构挑战**：

1. **合规要求**：满足法规要求
2. **审计能力**：提供审计和报告能力
3. **数据保护**：保护敏感数据

**架构决策**：

```yaml
合规场景安全配置:
  FIPS 合规: FIPS 批准加密算法和密钥管理
  行业合规: 满足 HIPAA/PCI DSS/GDPR/SOC 2
  审计: 完整的审计日志和报告
  数据保护: 数据加密、访问控制、数据脱敏
  优势: 合规要求、审计能力、数据保护
```

**决策依据**：

- ✅ **合规要求**：满足 FIPS 和行业合规要求
- ✅ **审计能力**：提供完整的审计日志和报告
- ✅ **数据保护**：数据加密、访问控制、数据脱敏

### 09.7.3 零信任场景

**场景描述**：实现零信任架构，默认不信任，持续验证。

**架构挑战**：

1. **身份验证**：验证所有实体身份
2. **设备验证**：验证所有设备
3. **网络验证**：验证所有网络通信
4. **资源验证**：验证所有资源访问

**架构决策**：

```yaml
零信任场景安全配置:
  身份验证: OIDC/OAuth2（用户身份）
  设备验证: 设备证书（设备身份）
  网络验证: mTLS（网络通信）
  资源验证: RBAC + OPA（资源访问）
  优势: 全面验证、最小权限、微分段
```

**决策依据**：

- ✅ **身份验证**：OIDC/OAuth2 验证用户身份
- ✅ **设备验证**：设备证书验证设备身份
- ✅ **网络验证**：mTLS 加密网络通信
- ✅ **资源验证**：RBAC + OPA 控制资源访问

## 09.8 决策依据与思路

### 09.8.1 安全策略决策树

```yaml
安全策略决策:
  if 生产环境: 镜像签名 + 准入控制 + 数据加密
  elif 合规场景: FIPS 合规 + 行业合规 + 审计
  elif 零信任场景: 身份验证 + 设备验证 + 网络验证 + 资源验证
  else: 基础安全（镜像签名 + 准入控制）
```

### 09.8.2 镜像签名决策树

```yaml
镜像签名决策:
  if 生产环境: 必须签名所有镜像（Cosign）
  elif 合规场景: 必须签名所有镜像 + SBOM（Cosign）
  else: 可选签名（推荐）
```

### 09.8.3 策略治理决策树

```yaml
策略治理决策:
  if 复杂策略: OPA + Gatekeeper（灵活、强大）
  elif 简单策略: Kyverno（简单、易用）
  else: OPA + Gatekeeper（默认、推荐）
```

## 09.9 形式化总结

### 09.9.1 零信任模型形式化

**零信任验证函数**：

$$
ZT(E, D, N, R) = \begin{cases}
\text{allow} & \text{if } \text{verify}(E) \land \text{verify}(D) \land \text{verify}(N) \land \text{verify}(R) \\
\text{deny} & \text{otherwise}
\end{cases}
$$

其中：

- $E$ = 实体（Entity，用户/服务）
- $D$ = 设备（Device）
- $N$ = 网络（Network）
- $R$ = 资源（Resource）

### 09.9.2 安全策略模型形式化

**安全策略函数**：
$$S(P) = \{\text{sign}(P), \text{verify}(P), \text{enforce}(P)\}$$

其中：

- $P$ = 策略（Policy）
- $\text{sign}$ = 签名函数
- $\text{verify}$ = 验证函数
- $\text{enforce}$ = 执行函数

## 09.10 供应链安全最佳实践

### 09.10.1 供应链安全概述

**供应链安全**是指在整个软件供应链中确保代码、镜像、依赖项等的安全性和完整性。

**供应链安全威胁**：

- **依赖项漏洞**：第三方库的安全漏洞
- **镜像篡改**：镜像在传输或存储过程中被篡改
- **恶意代码注入**：在构建过程中注入恶意代码
- **密钥泄露**：构建密钥或访问凭证泄露

### 09.10.2 SBOM（软件物料清单）

**SBOM 定义**：软件物料清单（Software Bill of Materials）记录了软件的所有组件和
依赖项。

**SBOM 生成工具**：

```bash
# 使用 Syft 生成 SBOM
syft docker image myapp:latest -o spdx-json > sbom.json

# 使用 Cosign 签名 SBOM
cosign sign-blob --bundle sbom.json --key cosign.key

# 使用 in-toto 生成完整供应链证明
```

**SBOM 示例**：

```json
{
  "spdxVersion": "SPDX-2.3",
  "name": "myapp-1.0.0",
  "packages": [
    {
      "name": "myapp",
      "version": "1.0.0",
      "supplier": "Organization: MyCompany",
      "dependencies": ["node:16-alpine", "express:4.18.0", "lodash:4.17.21"]
    }
  ]
}
```

### 09.10.3 依赖项漏洞扫描

**漏洞扫描工具**：

```bash
# 使用 Trivy 扫描镜像漏洞
trivy image myapp:latest

# 使用 Grype 扫描漏洞
grype docker:myapp:latest

# 使用 Snyk 扫描依赖项
snyk test --docker myapp:latest
```

**CI/CD 集成示例**：

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  pull_request:
  push:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build image
        run: docker build -t myapp:latest .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: "myapp:latest"
          format: "sarif"
          output: "trivy-results.sarif"

      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: "trivy-results.sarif"

      - name: Generate SBOM
        run: |
          syft docker image myapp:latest -o spdx-json > sbom.json

      - name: Sign SBOM
        run: |
          cosign sign-blob --bundle sbom.json --key cosign.key
```

### 09.10.4 镜像签名和验证完整流程

**完整签名流程**：

```bash
#!/bin/bash
# complete-signing-flow.sh

# 1. 构建镜像
docker build -t myapp:1.0.0 .

# 2. 生成 SBOM
syft docker image myapp:1.0.0 -o spdx-json > sbom.json

# 3. 扫描漏洞
trivy image myapp:1.0.0 --format json > vuln-report.json

# 4. 验证无高危漏洞
if grep -q '"Severity":"CRITICAL"' vuln-report.json; then
    echo "Critical vulnerabilities found, aborting"
    exit 1
fi

# 5. 签名镜像
cosign sign --key cosign.key myapp:1.0.0

# 6. 签名 SBOM
cosign sign-blob --bundle sbom.json --key cosign.key

# 7. 推送镜像和签名
docker push myapp:1.0.0
cosign copy myapp:1.0.0 myregistry.io/myapp:1.0.0

# 8. 推送 SBOM
cosign upload blob --bundle sbom.json myregistry.io/myapp:1.0.0-sbom
```

**验证流程**：

```bash
#!/bin/bash
# verify-image.sh

IMAGE=$1

# 1. 验证镜像签名
if ! cosign verify --key cosign.pub $IMAGE; then
    echo "Image signature verification failed"
    exit 1
fi

# 2. 验证 SBOM 签名
if ! cosign verify-blob --key cosign.pub --bundle sbom.json; then
    echo "SBOM signature verification failed"
    exit 1
fi

# 3. 扫描漏洞
trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE

echo "Image verification passed"
```

### 09.10.5 Kubernetes 准入控制集成

**使用 Gatekeeper 验证镜像签名**：

```yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredimagesignature
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredImageSignature
      validation:
        openAPIV3Schema:
          type: object
          properties:
            key:
              type: string
            images:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredimagesignature

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not check_image_signature(container.image)
          msg := sprintf("Image %v is not signed", [container.image])
        }

        check_image_signature(image) {
          # 调用 cosign verify 验证签名
          # 这里需要集成外部验证服务
        }
---
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
spec:
  match:
    - excludedNamespaces: ["kube-system", "gatekeeper-system"]
  validation:
    traces:
      - userGroups: ["system:serviceaccounts"]
        kind:
          group: ""
          version: "v1"
          kind: "Pod"
```

**使用 Kyverno 验证镜像签名**：

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-image-signature
spec:
  validationFailureAction: enforce
  rules:
    - name: verify-image-signature
      match:
        resources:
          kinds:
            - Pod
      validate:
        message: "All images must be signed"
        pattern:
          spec:
            containers:
              - name: "*"
                image: "myregistry.io/*"
          # 这里需要集成外部验证逻辑
```

### 09.10.6 实际安全案例

#### 案例 1：Log4Shell 漏洞应对

**场景**：2021 年 Log4Shell 漏洞（CVE-2021-44228）影响大量 Java 应用

**应对措施**：

```bash
# 1. 扫描所有镜像中的 Log4j
trivy image --severity CRITICAL myapp:latest | grep log4j

# 2. 生成受影响镜像清单
kubectl get pods --all-namespaces -o json | \
  jq -r '.items[].spec.containers[].image' | \
  sort -u | \
  xargs -I {} trivy image --format json {} | \
  jq -r 'select(.Results[].Vulnerabilities[].VulnerabilityID=="CVE-2021-44228") | .Target'

# 3. 自动更新策略
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: block-log4j-vulnerable-images
spec:
  validationFailureAction: enforce
  rules:
  - name: block-log4j
    match:
      resources:
        kinds:
        - Pod
    validate:
      message: "Images with Log4j vulnerability are not allowed"
      deny:
        conditions:
        - key: "{{ images.containers.*.image }}"
          operator: AnyIn
          value: ["*log4j*"]
```

#### 案例 2：供应链攻击防范

**场景**：防止构建过程中注入恶意代码

**防护措施**：

```yaml
# 1. 使用可信基础镜像
FROM gcr.io/distroless/base:nonroot

# 2. 多阶段构建隔离
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM gcr.io/distroless/nodejs:16
COPY --from=builder /app /app
CMD ["/app/server.js"]

# 3. 构建时扫描
# 在 CI/CD 中集成安全扫描
```

#### 案例 3：密钥管理最佳实践

**场景**：安全地管理镜像签名密钥和访问凭证

**最佳实践**：

```bash
# 1. 使用 Kubernetes Secrets 存储密钥
kubectl create secret generic cosign-key \
  --from-file=cosign.key=cosign.key \
  --from-file=cosign.pub=cosign.pub

# 2. 使用 Sealed Secrets 加密密钥
kubectl create secret generic cosign-key \
  --from-file=cosign.key=cosign.key \
  --dry-run=client -o yaml | \
  kubeseal -o yaml > sealed-secret.yaml

# 3. 使用外部密钥管理服务（如 HashiCorp Vault）
vault kv put secret/cosign-key \
  private_key=@cosign.key \
  public_key=@cosign.pub
```

### 09.10.7 安全合规检查清单

**定期安全检查清单**：

```yaml
供应链安全检查清单:
  镜像安全:
    - [ ] 所有镜像已签名
    - [ ] 签名验证已启用
    - [ ] 定期扫描镜像漏洞
    - [ ] 使用可信基础镜像
    - [ ] 最小化镜像大小和攻击面
  依赖项安全:
    - [ ] 生成 SBOM 清单
    - [ ] 扫描所有依赖项漏洞
    - [ ] 及时更新依赖项
    - [ ] 使用依赖项锁定文件
    - [ ] 审核第三方依赖项
  构建安全:
    - [ ] 使用多阶段构建
    - [ ] 构建过程隔离
    - [ ] 构建日志审计
    - [ ] 构建密钥安全存储
    - [ ] CI/CD 管道安全加固
  运行时安全:
    - [ ] 使用非 root 用户运行
    - [ ] 最小权限原则
    - [ ] 网络策略隔离
    - [ ] 定期安全更新
    - [ ] 运行时安全监控
```

### 09.10.8 安全工具集成矩阵

**安全工具对比**：

| 工具类别       | 工具           | 用途                | 集成方式                   |
| -------------- | -------------- | ------------------- | -------------------------- |
| **镜像签名**   | Cosign         | 镜像签名和验证      | CI/CD、Kubernetes 准入控制 |
| **SBOM 生成**  | Syft           | 生成软件物料清单    | CI/CD                      |
| **漏洞扫描**   | Trivy          | 镜像和文件系统扫描  | CI/CD、Kubernetes Operator |
| **策略治理**   | OPA Gatekeeper | Kubernetes 策略执行 | Kubernetes 准入控制        |
| **密钥管理**   | Sealed Secrets | 密钥加密存储        | Kubernetes Secrets         |
| **运行时安全** | Falco          | 运行时威胁检测      | Kubernetes DaemonSet       |

## 09.11 参考

### 09.11.1 2025 年最新更新（2025-11-06）

- **[27. 2025 趋势 - 2025-11-06 最新更新](../27-2025-trends/2025-trends.md#2714-2025-年-11-月-6-日最新更新)** -
  技术版本更新、生产环境最佳实践、已知问题与解决方案
  - **Sigstore + Cosign CNCF 毕业**：2025 年 7 月成为 CNCF 毕业项目
  - **强制签名**：wasm 模块强制签名写入 Kubernetes 1.30 安全基线
  - **WasmEdge FIPS-140-3 预审**：WasmEdge 沙箱通过 FIPS-140-3 预审
  - **OPA-Wasm 国密支持**：OPA-Wasm 政策支持细粒度字段脱敏，国密 SM4 算法已编译进 wasm
  - **安全更新**：CVE 修复列表和安全建议

**安全与合规最佳实践（2025-11-06）**：

- **镜像签名**：所有镜像必须使用 cosign 签名验证（Sigstore CNCF 毕业）
- **Wasm 模块签名**：wasm 模块强制签名写入 Kubernetes 1.30 安全基线
- **SBOM 要求**：所有镜像必须包含 SBOM（Software Bill of Materials）
- **OPA-Wasm 策略签名**：所有 Wasm 策略模块必须使用 cosign 签名验证
- **国密支持**：OPA-Wasm 支持国密 SM4 算法，满足国内合规要求

### 09.11.2 隔离栈相关文档

- **[29. 隔离栈](../29-isolation-stack/isolation-stack.md)** - 完整的隔离栈技术
  解析，包括安全隔离
- **[L-3 容器化层](../29-isolation-stack/layers/L-3-containerization.md)** - 容
  器安全最佳实践
- **[L-4 沙盒化层](../29-isolation-stack/layers/L-4-sandboxing.md)** - WASM 安全
  特点（OPA-Wasm）
- **[隔离层次对比文档](../29-isolation-stack/layers/isolation-comparison.md)** -
  安全特点对比和技术选型

### 09.11.3 安全相关文档

- **[25. 社区最佳实践](../25-community-best-practices/community-best-practices.md)** -
  安全最佳实践
- **[11. 故障排查](../11-troubleshooting/troubleshooting.md)** - 安全相关故障排
  查
- **[06. OPA 策略](../06-policy-opa/policy-opa.md)** - OPA 策略详细文档

### 09.11.4 其他相关文档

- **[10. 快速参考指南](../../COGNITIVE/10-decision-models/QUICK-REFERENCE.md)** -
  设备访问（USB/PCI/GPU）和内核特性决策快速参考
- **[01. Kubernetes](../01-kubernetes/kubernetes.md)** - Kubernetes 架构与实践

---

**最后更新**：2025-11-06 **维护者**：项目团队
