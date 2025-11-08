# 支付网关 OPA 策略配置
# 用途：定义支付网关访问控制策略
# 创建日期：2025-11-07

package payment

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许支付请求的条件
allow if {
    # 请求方法必须是 POST
    input.method == "POST"

    # 请求路径必须是 /api/payment
    input.path == "/api/payment"

    # 用户角色必须是 customer
    input.user.role == "customer"

    # 支付金额不能超过 10000
    input.amount <= 10000

    # 用户账户状态必须是 active
    input.user.status == "active"
}

# 允许查询请求的条件
allow if {
    input.method == "GET"
    input.path == "/api/payment/status"
    input.user.role == "customer"
}

# 允许管理员查询所有支付记录
allow if {
    input.method == "GET"
    input.path == "/api/payment/records"
    input.user.role == "admin"
}

