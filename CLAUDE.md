# Slack QR Bot - Project Analysis Document

## Project Overview

Slack QR Bot is a Flask-based RESTful API service that converts APK download URLs into QR code images and automatically sends them to Slack channels. It is designed to integrate with CI/CD pipelines for easy distribution and testing of built APK files.

### Key Use Cases
- Mobile app build automation (Jenkins, GitLab CI, GitHub Actions)
- APK distribution to QA teams
- Sharing builds with internal tester groups
- Multi-channel simultaneous distribution

---

## Architecture & Tech Stack

### Tech Stack
- **Language**: Python 3.14
- **Framework**: Flask 3.0.0
- **API Documentation**: Flasgger (Swagger UI)
- **QR Code Generation**: qrcode 7.4.2, Pillow 10.4.0
- **Slack Integration**: slack-sdk 3.26.1
- **Rate Limiting**: flask-limiter 3.5.0
- **Retry Logic**: tenacity 8.2.3
- **Logging**: python-json-logger 2.0.7
- **Web Server**: Gunicorn 21.2.0

### Directory Structure
```bash
slack-qr-bot/
├── src/
│   ├── app.py              # Flask app factory and initialization
│   ├── config.py           # Environment and Swagger configuration
│   ├── decorators.py       # API key authentication decorator
│   ├── services.py         # QR generation and Slack delivery service
│   ├── utils.py            # Utility functions (response formatting, etc.)
│   └── routes/             # API route modules
│       ├── health.py       # Health check endpoint
│       ├── qr.py           # QR code generation/delivery API
│       ├── channels.py     # Slack channel list API
│       └── slack_events.py # Slack event handler
├── k8s/                    # Kubernetes deployment manifests
│   ├── deployment.yaml     # App deployment
│   ├── api-key-secret.yaml # API key secret
│   ├── slack-token-secret.yaml # Slack token secret
│   └── harbor-robot-secret.yaml # Harbor registry secret
├── Dockerfile              # Container image build
├── requirements.txt        # Python dependencies
└── README.md              # User guide
```

---

## Core Features

### 1. QR Code Generation & Delivery
- Convert URLs to QR code images
- Customizable (size, color, border)
- Automatic upload to Slack channels
- Includes build number and download URL info

### 2. API Key Authentication
- `X-API-Key` header-based authentication
- Protects external calls (CI/CD pipeline only)
- Can be disabled in development environments

### 3. Rate Limiting
- Default: 10 req/min (global)
- QR generation: 20 req/min
- Broadcast: 10 req/min
- DoS attack prevention

### 4. Automatic Retry Logic
- Up to 3 retries on Slack API failure
- Exponential backoff: 2s → 4s → 8s
- Uses Tenacity library

### 5. Structured JSON Logging
- JSON format log output
- Easy integration with ELK Stack/Loki
- Includes timestamp, log level, message, context

### 6. Multi-Channel Broadcast
- Simultaneous delivery to multiple Slack channels
- Public/Private channel support
- Per-channel delivery results

### 7. Swagger UI API Documentation
- Interactive API docs
- All endpoints testable
- Access path: `/api-docs`

---

## API Endpoints

### 1. Health Check
```
GET /health
```
- Check Slack connection status
- Response: connection status, team/user info, Bot ID

### 2. QR Code Generation & Delivery
```
POST /generate-qr
Headers: X-API-Key: <your-api-key>
Body: {
  "apk_url": "https://example.com/app.apk",
  "channel": "#apk-qr-generator",
  "build_number": "123"  // optional
}
```

### 3. Slack Channel List
```
GET /channels
Headers: X-API-Key: <your-api-key>
```
- Returns all channels accessible by the bot
- Distinguishes public/private channels

### 4. Multi-Channel Broadcast
```
POST /broadcast-qr
Headers: X-API-Key: <your-api-key>
Body: {
  "apk_url": "https://example.com/app.apk",
  "channels": ["#channel1", "#channel2"],
  "build_number": "123"  // optional
}
```

---

## Environment Variables

### Required
| Variable | Description | Example |
|----------|-------------|---------|
| `SLACK_BOT_TOKEN` | Slack Bot OAuth Token | `xoxb-123456...` |

### Optional
| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | API authentication key (recommended for production) | None (auth disabled) |
| `RATE_LIMIT_ENABLED` | Enable rate limiting | `true` |
| `PORT` | Service port | `8080` |

---

## Security & Reliability

### Authentication
- API key-based authentication prevents unauthorized access
- Managed via environment variables, not exposed in source code

### Rate Limiting
- In-memory storage
- Per-endpoint configuration
- Returns 429 error on excessive requests

### Error Handling
- Structured responses for all errors
- Automatic retry on Slack API failures
- Detailed error logging

### Logging
- Structured in JSON format
- Includes request IP, endpoint, timestamp
- Outputs to stdout in container environments

---

## Deployment

### Docker Local Run
```bash
docker run -d \
  -e SLACK_BOT_TOKEN=xoxb-your-token \
  -e API_KEY=your-secret-key \
  -p 8080:8080 \
  your-registry/slack-qr-bot:latest
```

### Kubernetes Deployment
```bash
# Create secrets
kubectl apply -f k8s/slack-token-secret.yaml
kubectl apply -f k8s/api-key-secret.yaml

# Deploy app
kubectl apply -f k8s/deployment.yaml
```

### Required Kubernetes Secrets
1. **slack-token-secret**: Slack Bot Token
2. **api-key-secret**: API authentication key
3. **harbor-robot-secret**: Harbor registry access (for image pull)

---

## Slack App Setup

### Required Bot Token Scopes
- `chat:write` - Send messages
- `files:write` - Upload files
- `channels:read` - Read public channel info
- `groups:read` - Read private channel info
- `groups:write` - Access private channels
- `incoming-webhook`

### Setup Steps
1. Create a new app at [Slack API](https://api.slack.com/apps)
2. Select "From scratch"
3. Add the scopes above in OAuth & Permissions
4. Install the app to your workspace
5. Copy the Bot Token (starts with `xoxb-`)
6. Invite bot to channel: `/invite @your-bot-name`

---

## Code Module Descriptions

### `src/app.py`
- Uses Flask application factory pattern
- Blueprint registration and Rate Limiter initialization
- Swagger documentation setup

### `src/config.py`
- Environment variable validation (`validate_env()`)
- Swagger template and configuration
- JSON logging setup (`setup_logging()`)

### `src/decorators.py`
- `@require_api_key`: API key authentication decorator
- Header validation and 401/403 response handling

### `src/services.py`
- `generate_qr_code()`: Generate QR code images
- `send_qr_to_slack()`: Upload files via Slack API
- `check_slack_connection()`: Check connection status
- `get_bot_channels()`: Return list of channels accessible by the bot
- Automatic retry logic via Tenacity

### `src/utils.py`
- Standardized response format functions
- `success_response()`, `bad_request()`, `unauthorized()`, etc.

### `src/routes/`
- `health.py`: `/health` health check
- `qr.py`: `/generate-qr`, `/broadcast-qr` QR generation API
- `channels.py`: `/channels` channel list API
- `slack_events.py`: Slack event webhook handler

---

## Testing

### Local Testing
```bash
# Activate Python virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SLACK_BOT_TOKEN=xoxb-your-token
export API_KEY=test-api-key

# Run app
python -m src.app
```

### API Testing (curl)
```bash
# Health Check
curl http://localhost:8080/health

# Generate QR
curl -X POST http://localhost:8080/generate-qr \
  -H "X-API-Key: test-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "apk_url": "https://example.com/app.apk",
    "channel": "#test-channel",
    "build_number": "123"
  }'
```

### Swagger UI Testing
- Visit `http://localhost:8080/api-docs` in your browser
- Test each endpoint interactively

---

## CI/CD Integration Examples

### Jenkins Pipeline
```groovy
stage('Send QR to Slack') {
    steps {
        sh '''
            curl -X POST https://qr-bot.example.com/generate-qr \
                -H "X-API-Key: ${SLACK_QR_API_KEY}" \
                -H "Content-Type: application/json" \
                -d '{
                    "apk_url": "'${APK_URL}'",
                    "channel": "#apk-releases",
                    "build_number": "'${BUILD_NUMBER}'"
                }'
        '''
    }
}
```

### GitLab CI
```yaml
send_qr:
  stage: deploy
  script:
    - |
      curl -X POST $SLACK_QR_BOT_URL/generate-qr \
        -H "X-API-Key: $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
          \"apk_url\": \"$APK_URL\",
          \"channel\": \"#apk-releases\",
          \"build_number\": \"$CI_PIPELINE_IID\"
        }"
```

---

## Troubleshooting

### Slack API Errors
- **Error**: `not_in_channel`
  - **Solution**: Invite the bot to the channel (`/invite @bot-name`)

- **Error**: `invalid_auth`
  - **Solution**: Verify `SLACK_BOT_TOKEN`, ensure it starts with `xoxb-`

### Disable Rate Limiting
```bash
export RATE_LIMIT_ENABLED=false
```

### Check Logs
```bash
# Docker logs
docker logs <container-id>

# Kubernetes logs
kubectl logs -f deployment/slack-qr-bot
```

---
