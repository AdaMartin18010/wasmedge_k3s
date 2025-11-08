# 实时对战 Wasm 应用 Dockerfile
# 用途：构建实时对战 Wasm 应用镜像
# 创建日期：2025-11-07

FROM scratch

# 复制 Wasm 应用文件
COPY real-time-battle.wasm /app.wasm

# 复制配置文件
COPY config.json /config.json

# 设置入口点
ENTRYPOINT ["/app.wasm"]

