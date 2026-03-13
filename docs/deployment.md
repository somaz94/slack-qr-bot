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
```

<br/>

## Docker

<br/>

### Build and Run

```bash
# Build image
make docker-build

# Run container
docker run -d \
  -e SLACK_BOT_TOKEN=xoxb-your-token \
  -e API_KEY=your-secret-key \
  -p 8080:8080 \
  somaz940/slack-qr-bot:latest
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
make deploy
```

<br/>

### 3. Verify

```bash
# Check pod status
kubectl get pods -n slack-bots -l app=slack-qr-bot

# Check logs
make logs

# Health check
kubectl port-forward -n slack-bots svc/slack-qr-bot 8080:8080
curl http://localhost:8080/health
```

<br/>

### 4. Operations

```bash
# Restart deployment
make restart

# Tail logs
make logs
```

<br/>

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SLACK_BOT_TOKEN` | Yes | - | Slack Bot OAuth Token (`xoxb-...`) |
| `API_KEY` | No | _(none)_ | API authentication key (recommended for production) |
| `RATE_LIMIT_ENABLED` | No | `true` | Enable rate limiting |
| `PORT` | No | `8080` | Service port |

<br/>

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| Global default | 10/min |
| `/generate-qr` | 20/min |
| `/generate-qr/custom` | 20/min |
| `/generate-qr/broadcast` | 10/min |
| `/generate-qr/broadcast-all` | 5/min |
