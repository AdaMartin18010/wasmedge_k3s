# 考试系统 Wasm 应用 Dockerfile
# 用途：构建考试系统 Wasm 应用镜像
# 创建日期：2025-11-15

FROM scratch

# 复制 Wasm 应用文件
COPY examination-system.wasm /app.wasm

# 复制 AI 模型文件
COPY anti-cheat-model.wasm /models/anti-cheat-model.wasm

# 设置入口点
ENTRYPOINT ["/app.wasm"]
