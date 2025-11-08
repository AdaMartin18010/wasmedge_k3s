# 电商高并发 Serverless 函数 Dockerfile
# 用途：构建电商高并发 Serverless 函数镜像
# 创建日期：2025-11-07

FROM scratch

# 复制 Wasm 应用文件
COPY serverless-function.wasm /app.wasm

# 设置入口点
ENTRYPOINT ["/app.wasm"]

