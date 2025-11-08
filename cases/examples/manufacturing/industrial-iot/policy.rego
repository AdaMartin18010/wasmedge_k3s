# 工业 IoT OPA 策略配置
# 用途：定义工业 IoT 访问控制策略
# 创建日期：2025-11-07

package industrial

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许数据采集的条件
allow if {
    # 请求方法必须是 POST
    input.method == "POST"

    # 请求路径必须是 /api/collect
    input.path == "/api/collect"

    # 设备类型必须是 sensor
    input.device.type == "sensor"

    # 用户角色必须是 operator
    input.user.role == "operator"

    # 用户账户状态必须是 active
    input.user.status == "active"
}

# 允许查询数据的条件
allow if {
    input.method == "GET"
    input.path == "/api/data"
    input.user.role == "operator"
}

# 允许管理员查询所有数据
allow if {
    input.method == "GET"
    input.path == "/api/all"
    input.user.role == "admin"
}

