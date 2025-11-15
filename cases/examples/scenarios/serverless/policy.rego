# Serverless 场景 OPA 策略配置
# 用途：定义 Serverless 函数访问控制策略
# 创建日期：2025-11-15

package scenarios.serverless

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许函数调用请求的条件
allow if {
    input.action == "invoke"
    input.user.role == "authorized"
    input.rate_limit.within_limit == true
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role == "authorized"
}

# 拒绝超出速率限制的请求
deny if {
    input.action == "invoke"
    input.rate_limit.within_limit != true
}
