# 编排与运行时集成

- CRI：containerd ↔ runc/runwasi/crun
- RuntimeClass：按工作负载切换运行时

## RuntimeClass 示例（crun-wasm）

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: crun-wasm
handler: crun
```

## Pod 使用示例

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: wasm-task
spec:
  runtimeClassName: crun-wasm
  containers:
    - name: task
      image: yourhub/app-wasm:v1
```
