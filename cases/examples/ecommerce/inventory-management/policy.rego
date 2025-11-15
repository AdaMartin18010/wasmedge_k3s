# 库存管理 OPA 策略配置
# 用途：定义库存管理访问控制策略
# 创建日期：2025-11-15

package ecommerce.inventory

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许查询库存
allow if {
    input.action == "query"
    input.user.role in ["customer", "staff", "admin"]
}

# 允许更新库存（仅限管理员）
allow if {
    input.action == "update"
    input.user.role == "admin"
}

# 允许创建库存（仅限管理员）
allow if {
    input.action == "create"
    input.user.role == "admin"
}
