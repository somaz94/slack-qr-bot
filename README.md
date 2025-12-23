# Slack QR Bot

A bot that converts APK download URLs into QR codes and automatically sends them to Slack channels.

<br/>

## Example

QR code being sent to a Slack channel:

<img src="img/slack-qr-bot-example.png" alt="Slack QR Bot Example" width="400">

<br/><br/>

## Key Features

- Generate QR code images from APK download links
- Automatically send QR codes to Slack channels
- **Multi-channel broadcast support** 
- **QR code customization** (color, size adjustment) 
- Include build number and download URL information
- Easy invocation via REST API
- **Interactive API documentation via Swagger UI** 
- **Detailed Health Check** (Slack connection status)
- **API Key Authentication** (external call protection)
- **Rate Limiting** (DoS attack prevention)
- **Structured JSON Logging** (ELK/Loki integration)
- **Automatic Retry Logic** (Slack API failure handling)

<br/>

## Security and Stability Features

<br/>

### API Key Authentication
Provides API key-based authentication so only CI/CD pipelines and external systems can make calls.

- Authentication via `X-API-Key` header
- Activated when `API_KEY` environment variable is set
- Authentication disabled when not set (development environment)
- Supports all CI/CD tools: Jenkins, GitLab CI, GitHub Actions, etc.

<br/>

### Rate Limiting
Prevents excessive requests to ensure service stability.

- Default limit: 10 per minute (global)
- QR generation: 20 per minute
- Broadcast: 10 per minute
- Can be disabled with `RATE_LIMIT_ENABLED=false`

<br/>

### Structured JSON Logging
Makes log analysis and monitoring easy in production environments.

- JSON format logging (easy integration with ELK Stack, Loki)
- Includes timestamp, log level, message, context
- Additional metadata like request IP, endpoint

<br/>

### Automatic Retry Logic
Automatically retries on temporary Slack API failures.

- Up to 3 retries (exponential backoff: 2s → 4s → 8s)
- Applied to Slack API calls (`auth_test`, `conversations_list`, `files_upload_v2`)
- Returns error on permanent failure

<br/>

## API Documentation

You can view and test all APIs through Swagger UI:

**Local:** http://localhost:8080/api-docs  
**Production:** http://<your-url>/api-docs

<br/>

## Requirements

<br/>

### Slack App Setup
1. Create a new App at [Slack API](https://api.slack.com/apps)
2. "Create New App" > "From scratch"
3. Add the following Bot Token Scopes in **OAuth & Permissions**:
   - `chat:write` - Send messages
   - `files:write` - Upload files
   - `channels:read` - Read public channel information
   - `groups:read` - Read private channel information
   - `groups:write` - Access private channels
   - `incoming-webhook` 
4. Install app to workspace and copy Bot Token
5. Invite Bot to Slack channel: `/invite @your-bot-name`

<br/>

## Local Development

<br/>

### Run with Docker

```bash
# Build image
docker build -t slack-bot:test .

# Run container (with API key authentication)
docker run -d --name slack-qr-bot \
  -p 8080:8080 \
  -e SLACK_BOT_TOKEN="xoxb-your-token-here" \
  -e API_KEY="your-secret-api-key-here" \
  -e RATE_LIMIT_ENABLED="true" \
  slack-bot:test

# Or run without authentication (for development)
docker run -d --name slack-qr-bot \
  -p 8080:8080 \
  -e SLACK_BOT_TOKEN="xoxb-your-token-here" \
  slack-bot:test

# Check logs (JSON format)
docker logs -f slack-qr-bot
```

<br/>

### Run Directly

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SLACK_BOT_TOKEN="xoxb-your-token-here"
export API_KEY="your-secret-api-key"  # Optional
export RATE_LIMIT_ENABLED="true"      # Optional
export PORT=8080

# Run app
python -m src.app
```

<br/>

## Kubernetes Deployment

```bash
# 1. Create Slack Token Secret (modify token)
kubectl apply -f k8s/slack-token-secret.yaml

# 2. Create API Key Secret (modify API key)
# First, change the API_KEY value in api-key-secret.yaml!
kubectl apply -f k8s/api-key-secret.yaml

# 3. Create Harbor Secret
kubectl apply -f k8s/harbor-robot-secret.yaml

# 4. Deploy
kubectl apply -f k8s/deployment.yaml

# 5. Check status
kubectl get pods -n slack-bots
kubectl get ingress -n slack-bots
```

**⚠️ Important:** Make sure to change the `API_KEY` value in `k8s/api-key-secret.yaml`!

```bash
# Generate secure API key (production)
openssl rand -base64 32

# For internal dev/test environment
# Current key: ${SLACK_QR_BOT_API_KEY}
```

<br/>

### 1. Health Check (Detailed)

Check service status and Slack connection:

```bash
# Without authentication (health check doesn't require auth)
curl http://<slack-bot-url>/health | jq
```

#### Response Example:
```json
{
  "code": 200,
  "message": "Service is healthy",
  "data": {
    "status": "healthy",
    "slack_connection": {
      "connected": true,
      "team": "My Workspace",
      "user": "bot_name",
      "bot_id": "B01234567"
    }
  },
  "payLoad": {}
}
```

<br/>

### 2. List Channels

Retrieve all channels the bot belongs to:

```bash
curl http://<slack-bot-url>/channels | jq
```

#### Response Example:
```json
{
  "code": 200,
  "message": "Channels retrieved successfully",
  "data": {
    "channels": [
      {
        "id": "CXB3GE5D23F",
        "name": "apk-qr-generator",
        "is_private": false,
        "num_members": 5
      }
    ],
    "count": 1
  },
  "payLoad": {}
}
```

<br/>

### 3. Generate and Send QR Code (Basic)

#### Using in Jenkins Pipeline:

```groovy
// Jenkinsfile
stage('Send QR to Slack') {
    steps {
        script {
            sh '''
            curl -X POST http:/<slack-bot-url>/generate-qr \
              -H "Content-Type: application/json" \
              -H "X-API-Key: ${SLACK_QR_BOT_API_KEY}" \
              -d '{
                "channel": "apk-qr-generator",
                "apk_url": "https://example.com/app.apk",
                "build_number": "1.0.0"
              }'
            '''
        }
    }
}
```

#### Or direct curl call:

```bash
# Internal use (current configured key)
curl -X POST http://<slack-bot-url>/generate-qr \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${SLACK_QR_BOT_API_KEY}" \
  -d '{
    "channel": "apk-qr-generator",
    "apk_url": "https://example.com/app.apk",
    "build_number": "1.0.0"
  }'

# Or use different API key
curl -X POST http://<slack-bot-url>/generate-qr \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{
    "channel": "apk-qr-generator",
    "apk_url": "https://example.com/app.apk",
    "build_number": "1.0.0"
  }'
```

#### Parameters:
- `apk_url` (required): APK download URL
- `channel` (required): Slack channel name (`#channel-name`) or channel ID (`C0B3GF7WXGV`)
- `build_number` (optional): Build number (displays "latest" if not provided)

#### Response Example:
```json
{
  "code": 200,
  "message": "QR code sent to Slack",
  "data": {
    "file_id": "F07KP4R8E9S"
  },
  "payLoad": {}
}
```

<br/>

### 4. Multi-channel Broadcast

Send QR code to multiple channels simultaneously:

```bash
curl -X POST http://<slack-bot-url>/generate-qr/broadcast \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{
    "channels": ["apk-qr-generator", "test-channel", "dev-team"],
    "apk_url": "https://example.com/app.apk",
    "build_number": "2.0.1"
  }'
```

#### Parameters:
- `apk_url` (required): APK download URL
- `channels` (required): Array of channel names or IDs
- `build_number` (optional): Build number

#### Response Example:
```json
{
  "code": 200,
  "message": "Sent to 3/3 channels",
  "data": {
    "success_count": 3,
    "failed_count": 0,
    "results": [
      {
        "channel": "apk-qr-generator",
        "status": "success",
        "file_id": "F07KP4R8E9S"
      },
      {
        "channel": "test-channel",
        "status": "success",
        "file_id": "F07KP4R8E9T"
      }
    ]
  },
  "payLoad": {}
}
```

<br/>

### 5. Broadcast to All Channels

Automatically send QR code to all channels the bot belongs to:

```bash
curl -X POST http://<slack-bot-url>/generate-qr/broadcast-all \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{
    "apk_url": "https://example.com/app.apk",
    "build_number": "2.5.0"
  }'
```

#### Parameters:
- `apk_url` (required): APK download URL
- `build_number` (optional): Build number
- `qr_options` (optional): QR customization options

#### Response Example:
```json
{
  "code": 200,
  "message": "Sent to 3/5 channels",
  "data": {
    "total_channels": 5,
    "success_count": 3,
    "failed_count": 2,
    "results": [
      {
        "channel_id": "C0B7XF2WXGZ",
        "channel_name": "apk-qr-generator",
        "status": "success",
        "file_id": "F07KP4R8E9S"
      },
      {
        "channel_id": "C0B5XYZ123",
        "channel_name": "test-channel",
        "status": "failed",
        "error": "not_in_channel"
      }
    ]
  },
  "payLoad": {}
}
```

<br/>

### 6. Generate Custom QR Code

Customize QR code color and size:

```bash
curl -X POST http://<slack-bot-url>/generate-qr/custom \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{
    "channel": "apk-qr-generator",
    "apk_url": "https://example.com/app.apk",
    "build_number": "3.0.0",
    "qr_options": {
      "box_size": 15,
      "border": 4,
      "fill_color": "#FF0000",
      "back_color": "#FFFFFF"
    }
  }'
```

#### Parameters:
- `apk_url` (required): APK download URL
- `channel` (required): Slack channel
- `build_number` (optional): Build number
- `qr_options` (optional): QR code customization options
  - `box_size`: QR code box size (default: 10)
  - `border`: Border size (default: 4)
  - `fill_color`: QR code color (default: "#000000" black)
  - `back_color`: Background color (default: "#FFFFFF" white)

#### Response Example:
```json
{
  "code": 200,
  "message": "Custom QR code sent to Slack",
  "data": {
    "file_id": "F07KP4R8E9S"
  },
  "payLoad": {}
}
```

<br/>

## API Testing

The easiest way to test is using **Swagger UI**:

1. Access http://<slack_web_url>/api-docs in browser
2. **When testing QR generation API:**
   - Click "Authorize" 🔓 button in top-right
   - Enter API Key (e.g., `your-api-key-here`)
   - Click "Authorize" → Auto-applied to all QR endpoints
3. **Health/Channels APIs don't require auth** (no lock 🔒 icon)
4. Select API to test and click "Try it out" button
5. Enter parameters and click "Execute"

#### APIs requiring authentication:
- `/generate-qr` - Single channel QR generation
- `/generate-qr/broadcast` - Multi-channel broadcast
- `/generate-qr/broadcast-all` - Broadcast to all channels
- `/generate-qr/custom` - Custom QR generation

#### APIs not requiring authentication:
- `/health` - Health check
- `/channels` - List channels

You can interactively test all APIs!

<br/>

## Environment Variables

<br/>

### Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `SLACK_BOT_TOKEN` | Slack Bot OAuth Token | `xoxb-...` | Required |
| `API_KEY` | API authentication key (CI/CD only) | `your-api-key-here` (internal) | Optional (recommended) |
| `RATE_LIMIT_ENABLED` | Enable rate limiting | `true` or `false` | Optional (default: true) |
| `PORT` | Server port | `8080` | Optional (default: 8080) |

<br/>

### API Key Setup

#### 1. Generate secure API key:
```bash
# Generate 32-byte random key with OpenSSL
openssl rand -base64 32

# Or with Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 2. Update Kubernetes Secret:
```bash
# Change API_KEY value in k8s/api-key-secret.yaml
kubectl apply -f k8s/api-key-secret.yaml
```

#### 3. Register CI/CD Secrets:

**Jenkins:**
- Jenkins → Credentials → Global → Add Credentials
- Kind: Secret text
- Secret: (enter generated API key)
- ID: `SLACK_QR_BOT_API_KEY`
- Use in Jenkinsfile:
```groovy
environment {
    SLACK_QR_BOT_API_KEY = credentials('SLACK_QR_BOT_API_KEY')
}
```

**GitLab CI:**
- Settings → CI/CD → Variables
- Key: `SLACK_QR_BOT_API_KEY`
- Value: (Input Create API Key)
- Protected: ✓, Masked: ✓

**GitHub Actions:**
- Settings → Secrets and variables → Actions
- New repository secret: `SLACK_QR_BOT_API_KEY`

<br/>

## Rate Limiting Policy

| Endpoint | Limit | Purpose |
|----------|-------|---------||
| Global default | 10 req/min | General calls |
| `POST /generate-qr` | 20 req/min | Single channel QR generation |
| `POST /generate-qr/broadcast` | 10 req/min | Multi-channel broadcast (high load) |
| `POST /generate-qr/broadcast-all` | 5 req/min | Broadcast all channels (very high load) |
| `POST /generate-qr/custom` | 20 req/min | Custom QR generation |
| `GET /health` | No limit | Health check |
| `GET /channels` | 10 req/min | List channels |

**429 Too Many Requests** response when rate limit exceeded:
```json
{
  "code": 429,
  "message": "Rate limit exceeded: 20 per 1 minute",
  "data": {},
  "payLoad": {}
}
```

<br/>

## Viewing Logs

#### JSON format log example:
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

#### View logs in Kubernetes:
```bash
# Real-time logs
kubectl logs -f -n slack-bots deployment/slack-qr-bot

# Last 100 lines
kubectl logs --tail=100 -n slack-bots deployment/slack-qr-bot

# JSON parsing (using jq)
kubectl logs -n slack-bots deployment/slack-qr-bot | jq '.'
```

#### View logs in Docker:
```bash
docker logs -f slack-qr-bot | jq '.'
```

<br/>

## CI/CD

Automatic build in GitLab:

- Automatically builds when files in `src/` folder or `Dockerfile`, `requirements.txt` are changed
- Push image to Harbor Registry: `harbor.somaz.link/library/slack-qr-bot:latest`
- Manual build also available via web UI

Manual deployment after build:
```bash
kubectl rollout restart -n slack-bots deployment/slack-qr-bot
```

<br/>

## Troubleshooting

<br/>

### Authentication Issues

**`401 Unauthorized` error:**
- Verify API key is included in header
- Verify `X-API-Key` header name is correct
- Verify API key value matches Kubernetes Secret

**`403 Forbidden` error:**
- API key value is incorrect
- Pod restart required if Secret was updated

<br/>

### Rate Limiting Issues

**`429 Too Many Requests` error:**
- Requests per minute exceeded
- Retry after waiting 1 minute
- Can disable with `RATE_LIMIT_ENABLED=false` in dev environment

<br/>

### Slack API Issues

**`channel_not_found` error:**
- Verify bot is added to channel: `/invite @bot-name`
- Use channel ID directly (Channel info → Channel ID at bottom)
- For private channels, verify `groups:read`, `groups:write` scopes

**Slack API temporary failure:**
- Auto retry logic attempts up to 3 times (2s → 4s → 8s wait)
- Check logs if still failing after retries

<br/>

### 503 Service Unavailable
- Check Ingress configuration
- Verify Service selector matches Pod label
- Check Pod status: `kubectl get pods -n slack-bots`

<br/>

## Tech Stack

- **Language:** Python 3.14
- **Framework:** Flask 3.0 + Gunicorn
- **Libraries:**
  - `slack-sdk` - Slack API communication
  - `qrcode[pil]` - QR code generation
  - `flasgger` - Swagger API documentation
  - `flask-limiter` - Rate limiting
  - `tenacity` - Retry logic
  - `python-json-logger` - JSON logging
- **Infrastructure:**
  - Docker + Kubernetes
  - GitLab CI + Harbor Registry
  - Ingress (NGINX)

<br/>

## Architecture

```bash
CI/CD Pipeline (Jenkins/GitLab/GitHub)
    ↓ (HTTP POST with X-API-Key)
Ingress (slack-qr-bot.somaz.link)
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

---

## License

This project is licensed under the [MIT License](LICENSE) file for details.