# 学习管理系统 OPA 策略配置
# 用途：定义学习管理系统访问控制策略
# 创建日期：2025-11-15

package education.learning

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许学生访问学习内容
allow if {
    input.action == "access_content"
    input.user.role == "student"
    input.course.enrolled == true
}

# 允许教师管理课程
allow if {
    input.action == "manage_course"
    input.user.role == "teacher"
}

# 允许查询请求
allow if {
    input.action == "query"
    input.user.role in ["student", "teacher", "admin"]
}
