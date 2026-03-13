# Slack App Setup

<br/>

## 1. Create Slack App

1. Go to [Slack API](https://api.slack.com/apps)
2. Click **Create New App** → **From scratch**
3. App Name: `QR Bot` (or any name you prefer)
4. Select your Workspace → **Create App**

<br/>

## 2. Configure Bot Token Scopes

Navigate to **OAuth & Permissions** → **Scopes** → **Bot Token Scopes**, and add:

| Scope | Description |
|-------|-------------|
| `chat:write` | Post messages to channels |
| `files:write` | Upload QR code images |
| `channels:read` | View public channel info |
| `groups:read` | View private channel info |
| `groups:write` | Access private channels |
| `incoming-webhook` | Post via incoming webhooks |

<br/>

## 3. Install App to Workspace

1. Navigate to **OAuth & Permissions**
2. Click **Install to Workspace** → **Allow**
3. Copy the **Bot User OAuth Token** (`xoxb-...`)

<br/>

## 4. Invite Bot to Channel

1. Open the channel where you want QR codes to be sent
2. Type `/invite @QR Bot` (or your app name)
3. The bot is now ready to post QR codes to this channel

<br/>

## 5. Configure Environment Variables

Set the Bot Token as an environment variable:

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export API_KEY="your-secret-api-key"  # optional, recommended for production
```

For Kubernetes deployment, create secrets:

```bash
# Create Slack token secret
kubectl create secret generic slack-qr-bot-secret \
  --from-literal=SLACK_BOT_TOKEN=xoxb-your-bot-token \
  -n slack-bots

# Create API key secret
kubectl create secret generic slack-qr-bot-api-key \
  --from-literal=API_KEY=your-secret-api-key \
  -n slack-bots
```

<br/>

## 6. Verify Connection

After starting the service, check the health endpoint:

```bash
curl http://localhost:8080/health
```

Expected response:

```json
{
  "code": 200,
  "message": "Service is healthy",
  "data": {
    "status": "healthy",
    "slack_connection": {
      "connected": true,
      "team": "Your Workspace",
      "user": "qr-bot"
    }
  }
}
```

<br/>

## Troubleshooting

| Error | Solution |
|-------|----------|
| `not_in_channel` | Invite the bot to the channel: `/invite @QR Bot` |
| `invalid_auth` | Check `SLACK_BOT_TOKEN` — must start with `xoxb-` |
| `missing_scope` | Add required scopes in **OAuth & Permissions** and reinstall the app |
| `channel_not_found` | Verify channel name or use channel ID instead |
