# 供应链管理 OPA 策略配置
# 用途：定义供应链管理访问控制策略
# 创建日期：2025-11-15

package manufacturing.supplychain

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许追踪请求的条件
allow if {
    input.action == "track"
    input.user.role == "authorized_staff"
}

# 允许更新状态（仅限物流公司）
allow if {
    input.action == "update_status"
    input.user.role == "logistics_company"
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role in ["authorized_staff", "logistics_company"]
}
