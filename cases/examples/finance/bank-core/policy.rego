# 银行核心系统 OPA 策略配置
# 用途：定义银行核心系统访问控制策略
# 创建日期：2025-11-15

package bank.core

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许转账请求的条件
allow if {
    input.action == "transfer"
    input.amount <= 1000000
    input.user.role == "authorized"
    input.audit.enabled == true
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role == "authorized"
}

# 拒绝大额转账（需要审批）
deny if {
    input.action == "transfer"
    input.amount > 1000000
    not input.approval.required
}

# 拒绝未授权用户
deny if {
    input.user.role != "authorized"
}
