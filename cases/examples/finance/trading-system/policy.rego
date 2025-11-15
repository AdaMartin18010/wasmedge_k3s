# 交易系统 OPA 策略配置
# 用途：定义交易系统访问控制策略
# 创建日期：2025-11-15

package finance.trading

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许交易请求的条件
allow if {
    input.action == "trade"
    input.user.role == "authorized_trader"
    input.audit.enabled == true
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role == "authorized_trader"
}

# 拒绝未授权用户
deny if {
    input.user.role != "authorized_trader"
}
