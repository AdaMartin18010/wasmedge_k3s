# 电商平台 Wasm 应用 Dockerfile
# 用途：构建电商平台 Wasm 应用镜像
# 创建日期：2025-11-15

FROM scratch

# 复制 Wasm 应用文件
COPY ecommerce-platform.wasm /app.wasm

# 设置入口点
ENTRYPOINT ["/app.wasm"]
