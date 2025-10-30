# 常见问题

| 现象                     | 根因                                          | 修复                                    |
| ------------------------ | --------------------------------------------- | --------------------------------------- |
| kubectl logs 为空        | crun 未把 wasm stdout 重定向到 cgroup 的 pipe | 升级 crun ≥ 1.8.5                       |
| 镜像拉取失败             | docker hub 将 .wasm 视为 blob 需 token        | 使用 wasm-to-oci 推送至 ghcr/阿里云 ACR |
| 无法解析 DNS             | WASI 预览版网络未完全支持                     | 启用 wasmedge_wasi_socket 插件          |
| HPA 基于 CPU 不触发      | Wasm 时间片小，CPU 采样失真                   | 改用 QPS 或自定义指标（KEDA）           |
| WasmEdge "out of bounds" | 输入 JSON 过大                                | 调大 --max-memory-page 或分段 evaluate  |
| webhook 超时             | 回退到 runc 或 RuntimeClass 不匹配            | 确认 RuntimeClass 及 shim 版本 ≥ 1.8    |
| 政策更新未生效           | Wasm 文件被缓存                               | 使用 ConfigMap 热挂载或监听 inotify     |
