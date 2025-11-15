# 边缘计算场景 OPA 策略配置
# 用途：定义边缘计算服务访问控制策略
# 创建日期：2025-11-15

package scenarios.edgecomputing

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许边缘计算请求的条件
allow if {
    input.action == "edge_compute"
    input.data_stays_local == true
}

# 允许查询请求的条件
allow if {
    input.action == "query"
    input.user.role == "authorized"
}

# 拒绝数据外传
deny if {
    input.action == "export"
    input.destination != "local"
}

