# Slack QR Bot

![Top Language](https://img.shields.io/github/languages/top/somaz94/slack-qr-bot?color=blue&logo=python&logoColor=white)
![slack-qr-bot](https://img.shields.io/github/v/tag/somaz94/slack-qr-bot?label=slack-qr-bot&logo=python&logoColor=white)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![Docker Pulls](https://img.shields.io/docker/pulls/somaz940/slack-qr-bot?logo=docker&logoColor=white)
![GitHub Stars](https://img.shields.io/github/stars/somaz94/slack-qr-bot?style=social)

A Slack bot that converts APK download URLs into QR codes and automatically sends them to Slack channels.

<br/>

## Features

![QR Code](https://img.shields.io/badge/QR_Generation-blue?logo=qrcode&logoColor=white)
![Broadcast](https://img.shields.io/badge/Multi--Channel_Broadcast-blue?logo=slack&logoColor=white)
![Custom QR](https://img.shields.io/badge/Custom_QR-green?logo=qrcode&logoColor=white)
![API Key Auth](https://img.shields.io/badge/API_Key_Auth-orange?logo=shield&logoColor=white)
![Rate Limiting](https://img.shields.io/badge/Rate_Limiting-orange?logo=shield&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger_UI-green?logo=swagger&logoColor=white)
![JSON Logging](https://img.shields.io/badge/JSON_Logging-purple?logo=files&logoColor=white)
![Helm](https://img.shields.io/badge/Helm_Chart-0F1689?logo=helm&logoColor=white)
![Health Check](https://img.shields.io/badge/Health_Check-green?logo=files&logoColor=white)

- **QR Code Generation** — Single channel, multi-channel broadcast, broadcast-all, custom colors/size
- **Security** — API key authentication, rate limiting per endpoint, structured JSON logging
- **Reliability** — Automatic retry with exponential backoff (2s → 4s → 8s), detailed health checks
- **Developer Experience** — Swagger UI at `/api-docs`, Helm chart, Helmfile, CI/CD automation

<br/>

## Quick Start

### Docker

```bash
docker run -d --name slack-qr-bot \
  -p 8080:8080 \
  -e SLACK_BOT_TOKEN="xoxb-your-token" \
  -e API_KEY="your-api-key" \
  somaz940/slack-qr-bot:v0.3.0
```

### From Source

```bash
make venv
export SLACK_BOT_TOKEN="xoxb-your-token"
make run
```

### Helm

**Recommended: OCI registry (Helm 3.8+)**

```bash
helm install my-bot oci://ghcr.io/somaz94/charts/slack-qr-bot \
  --version 0.3.0 \
  -n slack-bots --create-namespace
```

**Alternative: classic Helm repo**

```bash
helm repo add slack-qr-bot https://somaz94.github.io/slack-qr-bot/helm-repo
helm repo update
helm install my-bot slack-qr-bot/slack-qr-bot -n slack-bots --create-namespace
```

See [Deployment Guide](docs/deployment.md) for Kubernetes setup and [Deploy Examples](deploy/README.md) for Helmfile configuration.

<br/>

## API Usage

Interactive API docs available at `/api-docs` (Swagger UI). See [API Reference](docs/API.md) for full details.

```bash
# Health check
curl http://localhost:8080/health

# Generate QR and send to Slack
curl -X POST http://localhost:8080/generate-qr \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"channel": "apk-qr-generator", "apk_url": "https://example.com/app.apk", "build_number": "1.0.0"}'

# Multi-channel broadcast
curl -X POST http://localhost:8080/generate-qr/broadcast \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"channels": ["channel1", "channel2"], "apk_url": "https://example.com/app.apk"}'
```

<br/>

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SLACK_BOT_TOKEN` | Yes | - | Slack Bot OAuth Token (`xoxb-...`) |
| `API_KEY` | No | _(none)_ | API key for authentication |
| `RATE_LIMIT_ENABLED` | No | `true` | Enable rate limiting |
| `PORT` | No | `8080` | Server port |

See [Configuration Guide](docs/configuration.md) for API key setup, rate limiting details, logging, and CI/CD integration.

<br/>

## Architecture

```
src/                        # Flask application source
├── app.py                  # App factory + Swagger + rate limiter
├── config.py               # Configuration & logging setup
├── decorators.py           # API key authentication decorator
├── services.py             # Core QR/Slack integration logic
├── utils.py                # Response utilities
└── routes/                 # Flask blueprints
    ├── health.py           # GET /health
    ├── qr.py               # POST /generate-qr (+ broadcast, custom)
    ├── channels.py         # GET /channels
    └── slack_events.py     # POST /slack/events
tests/                      # Pytest test suite
deploy/                     # K8s manifests + Helmfile (see deploy/README.md)
helm/                       # Helm chart (6 templates + 2 examples)
hack/                       # Build/version scripts
k8s/                        # Secret templates
docs/                       # Documentation
.github/workflows/          # CI/CD (10 workflows)
```

```
CI/CD Pipeline (Jenkins/GitLab/GitHub)
    ↓ (HTTP POST with X-API-Key)
Ingress (slack-qr-bot.example.com)
    ↓
Service (slack-qr-bot:8080)
    ↓
Pod (Flask App)
    ├─ Rate Limiter (request limiting)
    ├─ API Key Auth (authentication)
    ├─ JSON Logger (structured logging)
    └─ Tenacity Retry (retry logic)
        ↓
Slack API (QR code upload)
```

<br/>

## Development

```bash
make build            # Create venv and install deps
make test             # Run tests with coverage
make lint             # Run flake8 linter
make docker-build     # Build Docker image
make docker-buildx    # Multi-arch build and push
make test-helm        # Validate Helm chart
make version          # Show version across all files
make help             # Show all available targets
```

<br/>

## Documentation

| Document | Description |
|----------|-------------|
| [API Reference](docs/API.md) | All endpoints, request/response examples, status codes |
| [Configuration Guide](docs/configuration.md) | Environment variables, API key, rate limiting, logging, CI/CD |
| [Deployment Guide](docs/deployment.md) | Local dev, Docker, Kubernetes deployment |
| [Deploy Examples](deploy/README.md) | Standalone K8s manifests, Helmfile configuration |
| [Helm Chart](helm/slack-qr-bot/README.md) | Helm chart configuration reference |
| [Slack App Setup](docs/slack-app-setup.md) | OAuth scopes, bot token, channel setup |
| [Testing Guide](docs/test.md) | Unit tests, Helm tests, smoke tests |
| [Version Guide](docs/version.md) | Version management, bump process, release workflow |
| [Troubleshooting](docs/troubleshooting.md) | Common errors and solutions |

<br/>

## Tech Stack

- **Language:** Python 3.14
- **Framework:** Flask 3.x + Gunicorn
- **Libraries:** slack-sdk, qrcode[pil], flasgger, flask-limiter, tenacity, python-json-logger
- **Infrastructure:** Docker, Kubernetes, Helm, GitHub Actions

<br/>

## Contributing

Issues and pull requests are welcome.

<br/>

## License

This project is licensed under the [Apache License 2.0](LICENSE).
