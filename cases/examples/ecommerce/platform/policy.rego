# 电商平台 OPA 策略配置
# 用途：定义电商平台访问控制策略
# 创建日期：2025-11-15

package ecommerce.platform

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许订单创建请求的条件
allow if {
    input.action == "create_order"
    input.user.role == "customer"
    input.order.amount > 0
    input.order.amount <= 100000
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role == "customer"
}

# 允许管理员操作
allow if {
    input.user.role == "admin"
}

# 拒绝大额订单（需要审批）
deny if {
    input.action == "create_order"
    input.order.amount > 100000
    not input.approval.required
}

