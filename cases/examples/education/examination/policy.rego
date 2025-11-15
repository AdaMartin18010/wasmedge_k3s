# 考试系统 OPA 策略配置
# 用途：定义考试系统访问控制策略
# 创建日期：2025-11-15

package education.examination

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许考试请求的条件
allow if {
    input.action == "take_exam"
    input.user.role == "student"
    input.exam.enrolled == true
    input.anti_cheat.enabled == true
}

# 拒绝作弊行为
deny if {
    input.action == "take_exam"
    input.anti_cheat.detected == true
}

# 允许查询请求
allow if {
    input.action == "query"
    input.user.role in ["student", "teacher", "admin"]
}
