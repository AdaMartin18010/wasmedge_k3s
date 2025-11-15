# 风控系统 OPA 策略配置
# 用途：定义风控系统访问控制策略
# 创建日期：2025-11-15

package risk.control

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许风险评估请求的条件
allow if {
    input.action == "assess"
    input.user.role == "authorized"
    input.transaction.amount > 0
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role == "authorized"
}

# 拒绝高风险交易
deny if {
    input.action == "assess"
    input.risk_score > 0.8
}

# 拒绝未授权用户
deny if {
    input.user.role != "authorized"
}
