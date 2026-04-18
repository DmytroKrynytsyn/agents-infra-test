# agents-infra-test

A GitOps-driven microservice setup running on bare-metal k3s. Two FastAPI services, fully automated from `git push` to running pod.

```
git push → build → Docker Hub → ArgoCD → k3s
```

## Services

| Service | Exposed | Role |
|---|---|---|
| gateway | `https://testapp.local` via Envoy Gateway | Public entry point, calls backend |
| backend | cluster-internal only | Echoes requests back |

## Stack

`k3s` · `ArgoCD` · `Envoy Gateway` · `Helm` · `GitHub Actions` · `Docker Hub` · `FastAPI` · `uv`

## How it works

A `git push` triggers GitHub Actions which builds both Docker images in parallel and commits the new timestamp tag back to `helm/*/values.yaml`. ArgoCD detects the change and syncs the Helm charts. The `gateway` service is reachable via Envoy Gateway HTTPRoute over HTTPS; `backend` is only reachable inside the cluster at `agents-infra-test-backend.agents-infra-test.svc.cluster.local`.

ArgoCD uses the [App of Apps](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/) pattern — one parent app manages the child apps for each service.

## Bootstrap

```bash
kubectl apply -f argocd/app-of-apps.yaml
```

## Test

```bash
# add to /etc/hosts: <kserver-ip> testapp.local

curl -k https://testapp.local

curl -k -X POST https://testapp.local/call-backend \
  -H "Content-Type: application/json" \
  -d '{"hello": "world"}'
# → {"echoed": {"hello": "world"}, "from": "agents-infra-test-backend"}
```

## Secrets

| Secret | Value |
|---|---|
| `DOCKERHUB_USERNAME` | `dkrinitsyn` |
| `DOCKERHUB_TOKEN` | Docker Hub access token |