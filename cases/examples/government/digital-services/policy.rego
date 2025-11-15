# 数字政务服务 OPA 策略配置
# 用途：定义数字政务服务访问控制策略
# 创建日期：2025-11-15

package government.digital

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许政务服务请求的条件
allow if {
    input.action == "service_request"
    input.user.role == "citizen"
    input.data_encrypted == true
    input.audit.enabled == true
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role == "citizen"
}

# 拒绝未授权访问
deny if {
    input.user.role != "citizen"
}
