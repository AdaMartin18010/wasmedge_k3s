# 电商高并发 Serverless 函数 OPA 策略配置
# 用途：定义电商高并发 Serverless 函数访问控制策略
# 创建日期：2025-11-07

package serverless

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许函数调用的条件
allow if {
    # 请求方法必须是 POST
    input.method == "POST"

    # 请求路径必须是 /api/function
    input.path == "/api/function"

    # 用户角色必须是 user
    input.user.role == "user"

    # 限流检查：剩余请求数 > 0
    input.rate_limit.remaining > 0

    # 用户账户状态必须是 active
    input.user.status == "active"
}

# 允许查询函数状态的条件
allow if {
    input.method == "GET"
    input.path == "/api/status"
    input.user.role == "user"
}

# 允许管理员查询所有函数
allow if {
    input.method == "GET"
    input.path == "/api/all"
    input.user.role == "admin"
}

