# 医院信息系统 OPA 策略配置
# 用途：定义医院信息系统访问控制策略
# 创建日期：2025-11-15

package healthcare.his

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许访问患者数据的条件
allow if {
    input.action == "access_patient_data"
    input.user.role == "authorized_medical_staff"
    input.patient.consent == true
    input.audit.enabled == true
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role == "authorized_medical_staff"
}

# 拒绝未授权访问
deny if {
    input.user.role != "authorized_medical_staff"
}

# 拒绝未获得患者同意的访问
deny if {
    input.action == "access_patient_data"
    input.patient.consent != true
}
