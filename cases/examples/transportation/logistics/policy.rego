# 智能物流 OPA 策略配置
# 用途：定义智能物流访问控制策略
# 创建日期：2025-11-15

package transportation.logistics

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许物流追踪请求的条件
allow if {
    input.action == "track"
    input.user.role in ["customer", "staff", "admin"]
}

# 允许更新物流状态（仅限物流公司）
allow if {
    input.action == "update_status"
    input.user.role == "logistics_company"
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role in ["customer", "staff", "admin"]
}
