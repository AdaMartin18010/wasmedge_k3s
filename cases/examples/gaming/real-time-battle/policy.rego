# 实时对战 OPA 策略配置
# 用途：定义实时对战访问控制策略
# 创建日期：2025-11-07

package gaming

import rego.v1

# 默认拒绝所有请求
default allow = false

# 允许加入对战的条件
allow if {
    # 请求方法必须是 POST
    input.method == "POST"

    # 请求路径必须是 /api/join
    input.path == "/api/join"

    # 用户角色必须是 player
    input.user.role == "player"

    # 游戏状态必须是 waiting
    input.game.status == "waiting"

    # 游戏玩家数量必须小于 10
    count(input.game.players) < 10

    # 用户账户状态必须是 active
    input.user.status == "active"
}

# 允许查询游戏状态的条件
allow if {
    input.method == "GET"
    input.path == "/api/status"
    input.user.role == "player"
    input.game.status in ["waiting", "active"]
}

# 允许管理员查询所有游戏
allow if {
    input.method == "GET"
    input.path == "/api/all"
    input.user.role == "admin"
}

