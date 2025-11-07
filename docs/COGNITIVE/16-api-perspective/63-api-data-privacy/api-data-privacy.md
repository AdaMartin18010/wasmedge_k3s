# API 数据隐私规范

**版本**：v1.0 **最后更新**：2025-11-07 **维护者**：项目团队

## 📑 目录

- [📑 目录](#-目录)
- [1. 概述](#1-概述)
  - [1.1 数据隐私架构](#11-数据隐私架构)
- [2. 隐私法规](#2-隐私法规)
  - [2.1 GDPR](#21-gdpr)
  - [2.2 CCPA](#22-ccpa)
  - [2.3 HIPAA](#23-hipaa)
- [3. 数据分类](#3-数据分类)
  - [3.1 数据敏感度](#31-数据敏感度)
  - [3.2 数据分类标签](#32-数据分类标签)
- [4. 隐私保护](#4-隐私保护)
  - [4.1 数据脱敏](#41-数据脱敏)
  - [4.2 数据加密](#42-数据加密)
  - [4.3 数据匿名化](#43-数据匿名化)
- [5. 用户权利](#5-用户权利)
  - [5.1 数据访问权](#51-数据访问权)
  - [5.2 数据删除权](#52-数据删除权)
  - [5.3 数据可移植权](#53-数据可移植权)
- [6. 隐私合规](#6-隐私合规)
  - [6.1 合规检查](#61-合规检查)
  - [6.2 合规报告](#62-合规报告)
- [7. 相关文档](#7-相关文档)

---

## 1. 概述

API 数据隐私规范定义了 API 在数据隐私场景下的设计和实现，从隐私法规到数据分类，
从隐私保护到用户权利。

### 1.1 数据隐私架构

```text
数据收集（Data Collection）
  ↓
数据分类（Data Classification）
  ↓
隐私保护（Privacy Protection）
  ↓
数据访问（Data Access）
```

---

## 2. 隐私法规

### 2.1 GDPR

**GDPR 合规配置**：

```yaml
apiVersion: api.example.com/v1
kind: GDPRCompliance
metadata:
  name: payment-api-gdpr
spec:
  enabled: true
  dataController: "Example Corp"
  dataProcessor: "Payment Service Provider"
  legalBasis: "consent"
  dataRetention: "7y"
  userRights:
    - right: access
      endpoint: "/api/v1/privacy/data-access"
    - right: deletion
      endpoint: "/api/v1/privacy/data-deletion"
    - right: portability
      endpoint: "/api/v1/privacy/data-export"
  dataProcessing:
    - purpose: "payment processing"
      legalBasis: "contract"
      retention: "7y"
    - purpose: "fraud prevention"
      legalBasis: "legitimate_interest"
      retention: "2y"
```

**GDPR 数据访问实现**：

```go
package main

import (
    "net/http"
    "encoding/json"
)

func HandleDataAccessRequest(w http.ResponseWriter, r *http.Request) {
    userID := getUserIDFromRequest(r)

    data, err := collectUserData(userID)
    if err != nil {
        http.Error(w, "Failed to collect data", http.StatusInternalServerError)
        return
    }

    response := DataAccessResponse{
        UserID: userID,
        Data:   data,
        RequestDate: time.Now(),
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}
```

### 2.2 CCPA

**CCPA 合规配置**：

```yaml
apiVersion: api.example.com/v1
kind: CCPACompliance
metadata:
  name: payment-api-ccpa
spec:
  enabled: true
  businessName: "Example Corp"
  dataCategories:
    - category: "personal_information"
      collected: true
      disclosed: true
      sold: false
    - category: "payment_information"
      collected: true
      disclosed: false
      sold: false
  optOutEndpoint: "/api/v1/privacy/opt-out"
  deletionEndpoint: "/api/v1/privacy/delete"
```

### 2.3 HIPAA

**HIPAA 合规配置**：

```yaml
apiVersion: api.example.com/v1
kind: HIPAACompliance
metadata:
  name: payment-api-hipaa
spec:
  enabled: true
  coveredEntity: "Healthcare Provider"
  businessAssociate: "Payment Processor"
  phiCategories:
    - category: "patient_name"
      encryption: required
      accessLogging: required
    - category: "medical_record_number"
      encryption: required
      accessLogging: required
  safeguards:
    administrative:
      - securityOfficer: required
      - workforceTraining: required
    physical:
      - facilityAccess: required
      - workstationSecurity: required
    technical:
      - accessControl: required
      - auditControls: required
      - integrity: required
```

---

## 3. 数据分类

### 3.1 数据敏感度

**数据敏感度分类**：

```yaml
apiVersion: api.example.com/v1
kind: DataClassification
metadata:
  name: payment-api-data-classification
spec:
  classifications:
    - level: public
      description: "Public data"
      examples: ["product_catalog", "public_pricing"]
    - level: internal
      description: "Internal use only"
      examples: ["employee_id", "internal_notes"]
    - level: confidential
      description: "Confidential data"
      examples: ["customer_email", "order_details"]
    - level: restricted
      description: "Highly sensitive data"
      examples: ["payment_card_number", "ssn", "medical_records"]
```

### 3.2 数据分类标签

**数据分类标签实现**：

```go
package main

type DataClassification string

const (
    ClassificationPublic       DataClassification = "public"
    ClassificationInternal     DataClassification = "internal"
    ClassificationConfidential DataClassification = "confidential"
    ClassificationRestricted   DataClassification = "restricted"
)

type DataField struct {
    Name         string
    Classification DataClassification
    Encryption   bool
    Masking      bool
}

func ClassifyDataField(fieldName string) DataField {
    classification := getClassificationForField(fieldName)
    return DataField{
        Name:          fieldName,
        Classification: classification,
        Encryption:    classification == ClassificationRestricted || classification == ClassificationConfidential,
        Masking:       classification == ClassificationRestricted,
    }
}
```

---

## 4. 隐私保护

### 4.1 数据脱敏

**数据脱敏实现**：

```go
package main

import (
    "strings"
    "regexp"
)

func MaskEmail(email string) string {
    parts := strings.Split(email, "@")
    if len(parts) != 2 {
        return email
    }
    username := parts[0]
    domain := parts[1]

    if len(username) <= 2 {
        return "***@" + domain
    }

    masked := string(username[0]) + "***" + string(username[len(username)-1])
    return masked + "@" + domain
}

func MaskCreditCard(cardNumber string) string {
    if len(cardNumber) < 4 {
        return "****"
    }
    return "****" + cardNumber[len(cardNumber)-4:]
}

func MaskSSN(ssn string) string {
    re := regexp.MustCompile(`^\d{3}-\d{2}-(\d{4})$`)
    return re.ReplaceAllString(ssn, "***-**-$1")
}
```

### 4.2 数据加密

**数据加密配置**：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: data-encryption-config
data:
  encryption.yaml: |
    algorithms:
      at_rest:
        algorithm: AES-256-GCM
        key_rotation: "90d"
      in_transit:
        algorithm: TLS_1.3
        cipher_suites:
          - TLS_AES_256_GCM_SHA384
          - TLS_CHACHA20_POLY1305_SHA256
    key_management:
      provider: vault
      key_path: "secret/data/encryption-keys"
```

### 4.3 数据匿名化

**数据匿名化实现**：

```go
package main

import (
    "crypto/sha256"
    "encoding/hex"
)

func AnonymizeUserID(userID string) string {
    hash := sha256.Sum256([]byte(userID + "salt"))
    return hex.EncodeToString(hash[:])[:16]
}

func AnonymizeIP(ip string) string {
    parts := strings.Split(ip, ".")
    if len(parts) == 4 {
        return parts[0] + "." + parts[1] + ".0.0"
    }
    return ip
}
```

---

## 5. 用户权利

### 5.1 数据访问权

**数据访问权实现**：

```yaml
apiVersion: api.example.com/v1
kind: DataAccessRight
metadata:
  name: payment-api-data-access
spec:
  endpoint: "/api/v1/privacy/data-access"
  method: POST
  requestBody:
    user_id: string
    request_type: "access"
  response:
    user_id: string
    data:
      - category: "personal_information"
        fields: []
      - category: "payment_information"
        fields: []
    request_date: timestamp
```

### 5.2 数据删除权

**数据删除权实现**：

```yaml
apiVersion: api.example.com/v1
kind: DataDeletionRight
metadata:
  name: payment-api-data-deletion
spec:
  endpoint: "/api/v1/privacy/data-deletion"
  method: POST
  requestBody:
    user_id: string
    request_type: "deletion"
    data_categories: []
  response:
    user_id: string
    deletion_status: "pending" | "completed"
    deletion_date: timestamp
```

### 5.3 数据可移植权

**数据可移植权实现**：

```yaml
apiVersion: api.example.com/v1
kind: DataPortabilityRight
metadata:
  name: payment-api-data-portability
spec:
  endpoint: "/api/v1/privacy/data-export"
  method: POST
  requestBody:
    user_id: string
    format: "json" | "csv" | "xml"
  response:
    user_id: string
    export_url: string
    expires_at: timestamp
```

---

## 6. 隐私合规

### 6.1 合规检查

**合规检查配置**：

```yaml
apiVersion: api.example.com/v1
kind: PrivacyComplianceCheck
metadata:
  name: payment-api-compliance-check
spec:
  checks:
    - name: gdpr_compliance
      type: automated
      schedule: "0 0 * * *" # Daily
      rules:
        - rule: "data_retention_policy"
          check: "retention_period <= max_retention"
        - rule: "user_rights_implementation"
          check: "endpoints_exist"
    - name: ccpa_compliance
      type: automated
      schedule: "0 0 * * *" # Daily
      rules:
        - rule: "opt_out_endpoint"
          check: "endpoint_exists"
        - rule: "data_categories_disclosure"
          check: "categories_documented"
```

### 6.2 合规报告

**合规报告生成**：

```yaml
apiVersion: api.example.com/v1
kind: PrivacyComplianceReport
metadata:
  name: payment-api-compliance-report
spec:
  reportType: "gdpr_annual"
  period: "2025-01-01T00:00:00Z/2025-12-31T23:59:59Z"
  sections:
    - section: "data_processing_activities"
    - section: "data_breaches"
    - section: "user_rights_requests"
    - section: "compliance_status"
  output:
    format: "pdf"
    destination: "s3://compliance-reports/gdpr-2025.pdf"
```

---

## 7. 相关文档

- **[API 合规规范](../22-api-compliance/api-compliance.md)** - API 合规
- **[API 安全规范](../11-api-security/api-security.md)** - API 安全
- **[最佳实践](../08-best-practices/best-practices.md)** - 数据隐私最佳实践
- **[API 视角主文档](../../../api_view.md)** ⭐ - API 规范视角的核心论述

**最后更新**：2025-11-07 **维护者**：项目团队
