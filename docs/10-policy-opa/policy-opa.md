# OPA（策略）

- Rego → wasm：`opa build -t wasm -e '<package/entry>' policy.rego`

## 极简政策示例

```rego
package kubernetes.admission

deny[msg] {
  input.request.kind.kind == "Pod"
  image := input.request.object.spec.containers[_].image
  not startswith(image, "yourhub/")
  msg := sprintf("untrusted image: %v", [image])
}
```

## 编译与镜像

```bash
opa build -t wasm -e 'kubernetes/admission' policy.rego
# 生成 bundle.tar.gz，包含 policy.wasm
```

```dockerfile
FROM scratch
COPY policy.wasm /policy.wasm
```

## 以 WasmEdge 运行（示例 Pod）

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: policy-engine
  labels:
    app: policy-engine
spec:
  runtimeClassName: crun-wasm
  containers:
    - name: opa-wasm
      image: yourhub/admission-wasm:v1
      command: ["wasmedge", "--dir", ".", "/policy.wasm"]
      ports:
        - containerPort: 8080
```
