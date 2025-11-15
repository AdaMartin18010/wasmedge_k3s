# 智能制造 OPA 策略配置
# 用途：定义智能制造访问控制策略
# 创建日期：2025-11-15

package manufacturing.smart

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许本地数据处理
allow if {
    input.action == "process_data"
    input.data_stays_local == true
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role == "authorized_staff"
}

# 拒绝数据外传
deny if {
    input.action == "export"
    input.destination != "local"
}
