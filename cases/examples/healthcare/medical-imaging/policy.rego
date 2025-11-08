# 医疗影像处理 OPA 策略配置
# 用途：定义医疗影像处理访问控制策略（数据隐私保护）
# 创建日期：2025-11-07

package medical

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许处理医疗影像的条件
allow if {
    # 请求方法必须是 POST
    input.method == "POST"

    # 请求路径必须是 /api/process
    input.path == "/api/process"

    # 用户角色必须是 doctor
    input.user.role == "doctor"

    # 数据位置必须是本地（不出医院）
    input.data.location == "local"

    # 用户账户状态必须是 active
    input.user.status == "active"
}

# 允许查询处理结果的条件
allow if {
    input.method == "GET"
    input.path == "/api/result"
    input.user.role == "doctor"
    input.data.location == "local"
}

# 允许管理员查询所有记录
allow if {
    input.method == "GET"
    input.path == "/api/records"
    input.user.role == "admin"
    input.data.location == "local"
}

