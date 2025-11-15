# 远程医疗 OPA 策略配置
# 用途：定义远程医疗访问控制策略
# 创建日期：2025-11-15

package healthcare.telemedicine

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许视频通话的条件
allow if {
    input.action == "video_call"
    input.user.role == "authorized_medical_staff"
    input.patient.consent == true
    input.data_stays_local == true
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role == "authorized_medical_staff"
}

# 拒绝数据外传
deny if {
    input.action == "data_transfer"
    input.destination != "local"
}
