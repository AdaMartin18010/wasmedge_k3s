# 在线游戏边缘渲染 Wasm 应用 Dockerfile
# 用途：构建在线游戏边缘渲染 Wasm 应用镜像
# 创建日期：2025-11-07

FROM scratch

# 复制 Wasm 应用文件
COPY game-renderer.wasm /app.wasm

# 复制游戏资源文件
COPY assets /assets

# 设置入口点
ENTRYPOINT ["/app.wasm"]

