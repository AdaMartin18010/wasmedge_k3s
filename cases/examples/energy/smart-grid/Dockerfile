# 智能电网 Wasm 应用 Dockerfile
# 用途：构建电力数据处理 Wasm 应用镜像
# 创建日期：2025-11-15

FROM scratch

# 复制 Wasm 应用文件
COPY power-data-processor.wasm /app.wasm

# 设置入口点
ENTRYPOINT ["/app.wasm"]
