# 推荐系统 OPA 策略配置
# 用途：定义推荐系统访问控制策略
# 创建日期：2025-11-15

package recommendation

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许推荐请求的条件
allow if {
    input.action == "recommend"
    input.user.role == "customer"
    input.user.id != ""
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
