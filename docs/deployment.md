# Deployment Guide

<br/>

## Local Development

<br/>

### Prerequisites

- Python 3.12+
- Slack Bot Token ([setup guide](slack-app-setup.md))

<br/>

### Quick Start

```bash
# Create virtualenv and install dependencies
make venv

# Set environment variables
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export API_KEY="your-secret-api-key"

# Run with Flask dev server
make run

# Or run with Gunicorn
make run-gunicorn
```

<br/>

### Run Tests

```bash
make test        # Run tests with coverage
make coverage    # Generate HTML coverage report
make lint        # Run flake8 linter
make test-helm   # Validate Helm chart
```

<br/>

## Docker

<br/>

### Build and Run

```bash
# Build image
make docker-build

# Run as container
make deploy-docker

# Or manually
docker run -d \
  -e SLACK_BOT_TOKEN=xoxb-your-token \
  -e API_KEY=your-secret-key \
  -p 8080:8080 \
  somaz940/slack-qr-bot:v0.2.0

# Smoke test
make deploy-smoke

# Stop and remove
make undeploy-docker
```

<br/>

### Multi-Architecture Build

```bash
# Build and push for linux/amd64 and linux/arm64
make docker-buildx
```

<br/>

## Kubernetes

<br/>

### Prerequisites

- Kubernetes cluster
- kubectl configured

<br/>

### 1. Create Secrets

```bash
# Slack Bot Token
kubectl create secret generic slack-qr-bot-secret \
  --from-literal=SLACK_BOT_TOKEN=xoxb-your-bot-token \
  -n slack-bots

# API Key
kubectl create secret generic slack-qr-bot-api-key \
  --from-literal=API_KEY=your-secret-api-key \
  -n slack-bots

# Container Registry (if using private registry)
kubectl create secret docker-registry harbor-robot-secret \
  --docker-server=your-registry.com \
  --docker-username=robot-user \
  --docker-password=your-password \
  -n slack-bots
```

<br/>

### 2. Deploy

```bash
# Standalone manifests
make deploy-k8s

# Or with Helmfile
cd deploy/helmfile
helmfile -e mgmt apply
```

See [Deploy Examples](../deploy/README.md) for Helmfile details.

<br/>

### 3. Verify

```bash
# Check pod status
kubectl get pods -n slack-bots -l app=slack-qr-bot

# Check logs
make logs

# Health check
kubectl port-forward -n slack-bots svc/slack-qr-bot 8080:80
curl http://localhost:8080/health
```

<br/>

### 4. Operations

```bash
# Restart deployment
make restart

# Tail logs
make logs

# Remove deployment
make undeploy-k8s
```

<br/>

## Helm Chart

### Install from Helm Repository

```bash
helm repo add slack-qr-bot https://somaz94.github.io/slack-qr-bot/helm-repo
helm repo update

helm install my-bot slack-qr-bot/slack-qr-bot \
  -n slack-bots --create-namespace
```

### Install from Local Chart

```bash
helm install my-bot ./helm/slack-qr-bot \
  -f deploy/helmfile/values/mgmt.yaml \
  -n slack-bots --create-namespace
```

### Validate Chart

```bash
make test-helm
```

See [helm/slack-qr-bot/values.yaml](../helm/slack-qr-bot/values.yaml) for all configurable options.
