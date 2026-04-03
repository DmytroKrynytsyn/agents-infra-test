# agents-infra-test

Two FastAPI microservices deployed on a bare-metal k3s cluster via GitOps.

## How it works

A `git push` triggers GitHub Actions, which builds Docker images and commits the new tag back to `values.yaml`. ArgoCD detects the change and syncs the Helm charts to the cluster. `gateway` is publicly reachable via Traefik ingress; `backend` is internal only.

## Services

- **gateway** — public, exposed at `testapp.local`, calls `backend` internally
- **backend** — internal echo service, no ingress

## Stack

k3s · ArgoCD · Traefik · Helm · GitHub Actions · Docker Hub · FastAPI · uv

## Structure
```
├── gateway/        # source + Dockerfile
├── backend/        # source + Dockerfile
├── helm/           # Helm charts
├── argocd/         # app-of-apps + child apps
└── .github/        # CI workflow
```

## Bootstrap
```bash
kubectl apply -f argocd/app-of-apps.yaml
```

## Test
```bash
curl -k https://testapp.local
curl -k -X POST https://testapp.local/call-backend \
  -H "Content-Type: application/json" \
  -d '{"hello": "world"}'
```

## Secrets required

| Secret | Value |
|---|---|
| `DOCKERHUB_USERNAME` | `dkrinitsyn` |
| `DOCKERHUB_TOKEN` | Docker Hub access token |