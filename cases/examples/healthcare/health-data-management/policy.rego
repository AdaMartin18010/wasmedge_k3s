# 健康数据管理 OPA 策略配置
# 用途：定义健康数据管理访问控制策略
# 创建日期：2025-11-15

package healthcare.healthdata

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许查询健康数据的条件
allow if {
    input.action == "query"
    input.user.role == "authorized_medical_staff"
    input.patient.consent == true
    input.data_stays_local == true
    input.audit.enabled == true
}

# 拒绝数据外传
deny if {
    input.action == "export"
    input.destination != "local"
}

# 拒绝未授权访问
deny if {
    input.user.role != "authorized_medical_staff"
}
