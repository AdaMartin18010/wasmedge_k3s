# 在线教育平台 OPA 策略配置
# 用途：定义在线教育平台访问控制策略
# 创建日期：2025-11-15

package education.platform

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许学生访问课程
allow if {
    input.action == "access_course"
    input.user.role == "student"
    input.course.enrolled == true
}

# 允许教师管理课程
allow if {
    input.action == "manage_course"
    input.user.role == "teacher"
}

# 允许实时交互（WebSocket）
allow if {
    input.action == "websocket_connect"
    input.user.role == "student"
    input.course.enrolled == true
}

# 允许查询请求
allow if {
    input.action == "query"
    input.user.role in ["student", "teacher", "admin"]
}
