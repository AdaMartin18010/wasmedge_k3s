# 供应链管理 Wasm 应用 Dockerfile
# 用途：构建供应链追踪 Wasm 应用镜像
# 创建日期：2025-11-15

FROM scratch

# 复制 Wasm 应用文件
COPY supply-chain-tracker.wasm /app.wasm

# 设置入口点
ENTRYPOINT ["/app.wasm"]
