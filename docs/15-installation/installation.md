# 安装与最小示例

## 安装 K3s（含 Wasm 支持，占位）

```bash
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.30.4+k3s1 \
  sh -s - --wasm --write-kubeconfig-mode 644
```

## 安装 Gatekeeper（Wasm 引擎示例，占位）

```bash
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm install ge gatekeeper/gatekeeper --set enableExternalData=true \
  --set policyEngine=wasm
```

## 签名与推送 Wasm 策略（占位）

```bash
cosign sign --yes yourhub/policy.wasm
wasm-to-oci push yourhub/policy.wasm yourhub/policy:v1
```

## Hello Wasm Pod（crun）示例

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-wasm
  annotations:
    module.wasm.image/variant: compat-smart
spec:
  runtimeClassName: crun-wasm
  containers:
    - name: app
      image: docker.io/yourhub/hello-wasm:v1
      command: ["hello-wasm.wasm"]
```
