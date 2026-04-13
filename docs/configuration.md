# Configuration

<br/>

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SLACK_BOT_TOKEN` | Yes | - | Slack Bot OAuth Token (`xoxb-...`) |
| `API_KEY` | No | _(none)_ | API authentication key for external callers |
| `RATE_LIMIT_ENABLED` | No | `true` | Enable/disable rate limiting |
| `PORT` | No | `8080` | Server port |

<br/>

## API Key Authentication

Provides API key-based authentication so only CI/CD pipelines and authorized systems can make calls.

- Authentication via `X-API-Key` header
- Activated when `API_KEY` environment variable is set
- Authentication disabled when not set (development environment)
- Supports all CI/CD tools: Jenkins, GitLab CI, GitHub Actions, etc.

### Generate a Secure API Key

```bash
# Generate 32-byte random key with OpenSSL
openssl rand -base64 32

# Or with Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Kubernetes Secret Setup

```bash
kubectl create secret generic slack-qr-bot-api-key \
  --from-literal=API_KEY=your-api-key \
  -n slack-bots
```

### CI/CD Integration

**Jenkins:**
```groovy
environment {
    SLACK_QR_BOT_API_KEY = credentials('SLACK_QR_BOT_API_KEY')
}
```

**GitLab CI:**
- Settings → CI/CD → Variables
- Key: `SLACK_QR_BOT_API_KEY`, Protected: ✓, Masked: ✓

**GitHub Actions:**
- Settings → Secrets and variables → Actions
- New repository secret: `SLACK_QR_BOT_API_KEY`

<br/>

## Rate Limiting

Prevents excessive requests to ensure service stability.

| Endpoint | Limit | Purpose |
|----------|-------|---------|
| Global default | 10 req/min | General calls |
| `POST /generate-qr` | 20 req/min | Single channel QR generation |
| `POST /generate-qr/custom` | 20 req/min | Custom QR generation |
| `POST /generate-qr/broadcast` | 10 req/min | Multi-channel broadcast |
| `POST /generate-qr/broadcast-all` | 5 req/min | Broadcast to all channels |
| `GET /health` | No limit | Health check |
| `GET /channels` | 10 req/min | List channels |

When rate limit is exceeded, a `429 Too Many Requests` response is returned:
```json
{
  "code": 429,
  "message": "Rate limit exceeded: 20 per 1 minute",
  "data": {},
  "payLoad": {}
}
```

Disable rate limiting for development with `RATE_LIMIT_ENABLED=false`.

<br/>

## Structured JSON Logging

All logs are output in JSON format for easy integration with ELK Stack, Loki, or other log aggregation tools.

```json
{
  "asctime": "2025-12-23 10:30:45",
  "name": "src.app",
  "levelname": "INFO",
  "message": "QR code sent successfully",
  "channel": "apk-qr-generator",
  "file_id": "F07KP4R8E9S"
}
```

### Viewing Logs

```bash
# Kubernetes
kubectl logs -f -n slack-bots deployment/slack-qr-bot
kubectl logs --tail=100 -n slack-bots deployment/slack-qr-bot | jq '.'

# Docker
docker logs -f slack-qr-bot | jq '.'

# Makefile shortcut
make logs
```

<br/>

## Automatic Retry Logic

Automatically retries on temporary Slack API failures using exponential backoff.

- Up to 3 retries (2s → 4s → 8s)
- Applied to: `auth_test`, `conversations_list`, `files_upload_v2`, `get_bot_channels`
- Returns error on permanent failure

<br/>

## CI/CD

### GitHub Actions Workflows

| Workflow | Trigger | Description |
|----------|---------|-------------|
| `test.yml` | Push to main, PRs | Run pytest + flake8 lint |
| `release.yml` | Tag `v*.*.*` | Multi-arch Docker build + GitHub Release |
| `helm-release.yml` | Tag `v*.*.*` | Package and publish Helm chart to gh-pages |
| `changelog-generator.yml` | Push | Auto-update CHANGELOG.md |
| `contributors.yml` | Push | Auto-update CONTRIBUTORS.md |
| `gitlab-mirror.yml` | Push | Mirror to GitLab |

### Version Management

```bash
# Show current version across all files
make version

# Bump version (updates Makefile, Chart.yaml, values.yaml, deployment.yaml, helmfile, README)
make bump-version VERSION=v0.3.0

# Tag and release
git commit -am "chore: bump version to v0.3.0"
git push origin main
git tag v0.3.0 && git push origin v0.3.0
```
