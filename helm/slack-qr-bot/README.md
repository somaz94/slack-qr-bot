# slack-qr-bot Helm Chart

A Helm chart for deploying a Slack QR code bot on Kubernetes.

<br/>

## Prerequisites

- Kubernetes >= 1.16
- Helm >= 3.0
- Pre-created Kubernetes secrets for Slack token and API key

<br/>

## Installation

```bash
# Add the Helm repository
helm repo add slack-qr-bot https://somaz94.github.io/slack-qr-bot/helm-repo
helm repo update

# Install with default values
helm install my-bot slack-qr-bot/slack-qr-bot -n slack-bots --create-namespace

# Install with custom values
helm install my-bot slack-qr-bot/slack-qr-bot -f my-values.yaml -n slack-bots --create-namespace
```

<br/>

## Uninstall

```bash
helm uninstall my-bot -n slack-bots
```

<br/>

## Secret Prerequisites

The chart references existing Kubernetes secrets — it does **not** create them. Create them before installing:

```bash
kubectl create secret generic slack-qr-bot-secret \
  --from-literal=SLACK_BOT_TOKEN=xoxb-your-token \
  -n slack-bots

kubectl create secret generic slack-qr-bot-api-key \
  --from-literal=API_KEY=your-api-key \
  -n slack-bots
```

<br/>

## Configuration

### Image

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.repository` | Container image repository | `somaz940/slack-qr-bot` |
| `image.tag` | Container image tag | `v0.2.0` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `imagePullSecrets` | Image pull secrets | `[]` |

<br/>

### Application

| Parameter | Description | Default |
|-----------|-------------|---------|
| `config.port` | Server port | `8080` |
| `config.rateLimitEnabled` | Enable rate limiting | `false` |

<br/>

### Secrets

| Parameter | Description | Default |
|-----------|-------------|---------|
| `secrets.slackTokenSecretName` | K8s secret name for Slack token | `slack-qr-bot-secret` |
| `secrets.slackTokenKey` | Key within the secret | `SLACK_BOT_TOKEN` |
| `secrets.apiKeySecretName` | K8s secret name for API key | `slack-qr-bot-api-key` |
| `secrets.apiKeyKey` | Key within the secret | `API_KEY` |

<br/>

### Deployment

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `revisionHistoryLimit` | Revision history limit | `3` |
| `nameOverride` | Override chart name | `""` |
| `fullnameOverride` | Override full release name | `""` |
| `podAnnotations` | Pod annotations | `{}` |
| `podLabels` | Extra pod labels | `{}` |
| `nodeSelector` | Node selector | `{}` |
| `tolerations` | Tolerations | `[]` |
| `affinity` | Affinity rules | `{}` |
| `extraEnv` | Extra environment variables | `[]` |

<br/>

### Security

| Parameter | Description | Default |
|-----------|-------------|---------|
| `serviceAccount.create` | Create service account | `true` |
| `serviceAccount.name` | Service account name | `""` |
| `serviceAccount.annotations` | Service account annotations | `{}` |
| `podSecurityContext.runAsNonRoot` | Run as non-root | `true` |
| `podSecurityContext.runAsUser` | Run as user ID | `1000` |
| `podSecurityContext.fsGroup` | FS group ID | `1000` |
| `securityContext.allowPrivilegeEscalation` | Allow privilege escalation | `false` |

<br/>

### Service & Ingress

| Parameter | Description | Default |
|-----------|-------------|---------|
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `80` |
| `service.targetPort` | Target container port | `8080` |
| `service.annotations` | Service annotations | `{}` |
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.className` | Ingress class name | `""` |
| `ingress.annotations` | Ingress annotations | `{}` |
| `ingress.hosts` | Ingress hosts configuration | see `values.yaml` |
| `ingress.tls` | Ingress TLS configuration | `[]` |

<br/>

### Resources & Probes

| Parameter | Description | Default |
|-----------|-------------|---------|
| `resources.requests.cpu` | CPU request | `100m` |
| `resources.requests.memory` | Memory request | `128Mi` |
| `resources.limits.cpu` | CPU limit | `200m` |
| `resources.limits.memory` | Memory limit | `256Mi` |
| `probes.liveness.enabled` | Enable liveness probe | `true` |
| `probes.liveness.path` | Liveness probe path | `/health` |
| `probes.readiness.enabled` | Enable readiness probe | `true` |
| `probes.readiness.path` | Readiness probe path | `/health` |

<br/>

## Examples

See the [examples/](examples/) directory for ready-to-use value files:

| Example | File | Description |
|---------|------|-------------|
| Ingress + TLS | [ingress-tls.yaml](examples/ingress-tls.yaml) | cert-manager TLS termination |
| Production | [production.yaml](examples/production.yaml) | Production-ready (2 replicas, rate limiting, higher resources) |
