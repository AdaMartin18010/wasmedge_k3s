# 医疗影像处理 Wasm 应用 Dockerfile
# 用途：构建医疗影像处理 Wasm 应用镜像
# 创建日期：2025-11-07

FROM scratch

# 复制 Wasm 应用文件
COPY medical-imaging-ai.wasm /app.wasm

# 复制 AI 模型文件
COPY model.wasm /model.wasm

# 设置入口点
ENTRYPOINT ["/app.wasm"]

