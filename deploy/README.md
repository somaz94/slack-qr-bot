# Deploy

This directory contains Kubernetes deployment manifests and Helmfile configuration for `slack-qr-bot`.

<br/>

## Directory Structure

```
deploy/
├── deployment.yaml              # Standalone K8s manifests (Deployment + Service + Ingress)
└── helmfile/
    ├── helmfile.yaml            # Helmfile release configuration
    └── values/
        └── mgmt.yaml            # Values for mgmt environment
```

<br/>

## Prerequisites

Before deploying, create the required Kubernetes secrets:

```bash
# Slack Bot Token
kubectl create secret generic slack-qr-bot-secret \
  --from-literal=SLACK_BOT_TOKEN=xoxb-your-token \
  -n slack-bots

# API Key
kubectl create secret generic slack-qr-bot-api-key \
  --from-literal=API_KEY=your-api-key \
  -n slack-bots
```

See `k8s/` directory for secret template manifests.

<br/>

## Standalone Kubernetes Deployment

Apply the standalone manifest directly with `kubectl`:

```bash
kubectl create namespace slack-bots --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f deploy/deployment.yaml -n slack-bots
```

This creates:
- **Deployment** — 1 replica, `somaz940/slack-qr-bot:v0.2.0`, non-root user (UID 1000), health checks at `/health`
- **Service** — ClusterIP on port 80 → 8080
- **Ingress** — NGINX ingress class (update the host to your domain)

<br/>

## Helmfile Deployment

[Helmfile](https://github.com/helmfile/helmfile) manages Helm releases declaratively.

### Prerequisites

- [Helm](https://helm.sh/docs/intro/install/) v3+
- [Helmfile](https://github.com/helmfile/helmfile#installation)
- Kubernetes cluster access

### Deploy

```bash
cd deploy/helmfile

# Diff before applying
helmfile -e mgmt diff

# Apply
helmfile -e mgmt apply
```

### Environment Values

| File | Description |
|------|-------------|
| `values/mgmt.yaml` | Management environment — Ingress enabled, rate limiting disabled |

Create additional environment files (e.g., `values/prod.yaml`) and reference them in `helmfile.yaml` as needed.

<br/>

## Using the Helm Chart Directly

If you prefer Helm over Helmfile:

```bash
helm repo add slack-qr-bot https://somaz94.github.io/slack-qr-bot/helm-repo
helm repo update

# Install with custom values
helm install my-bot slack-qr-bot/slack-qr-bot \
  -f deploy/helmfile/values/mgmt.yaml \
  -n slack-bots --create-namespace
```

See the [Helm chart values](../helm/slack-qr-bot/values.yaml) for all configurable options.

<br/>

## Version Management

When bumping the project version, the deploy files are updated automatically:

```bash
make bump-version VERSION=v0.3.0
```

This updates the image tag in `deployment.yaml`, chart version in `helmfile.yaml`, and image tag in `values/mgmt.yaml`.
