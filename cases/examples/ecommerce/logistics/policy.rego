# 物流系统 OPA 策略配置
# 用途：定义物流系统访问控制策略
# 创建日期：2025-11-15

package logistics

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许物流追踪请求的条件
allow if {
    input.action == "track"
    input.user.role == "customer"
    input.tracking_number != ""
}

# 允许更新物流状态（仅限物流公司）
allow if {
    input.action == "update_status"
    input.user.role == "logistics_company"
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role == "customer"
}
