# Troubleshooting

<br/>

## Authentication Issues

**`401 Unauthorized` error:**
- Verify API key is included in `X-API-Key` header
- Verify header name is exactly `X-API-Key` (case-sensitive)
- Verify API key value matches the Kubernetes Secret

**`403 Forbidden` error:**
- API key value is incorrect
- Restart the pod if the Secret was recently updated

<br/>

## Rate Limiting Issues

**`429 Too Many Requests` error:**
- Requests per minute exceeded for this endpoint
- Retry after waiting 1 minute
- Disable with `RATE_LIMIT_ENABLED=false` in development

See [Configuration Guide](configuration.md#rate-limiting) for per-endpoint limits.

<br/>

## Slack API Issues

**`channel_not_found` error:**
- Verify the bot is invited to the channel: `/invite @bot-name`
- Try using channel ID directly (Channel info → Channel ID at bottom)
- For private channels, verify `groups:read` and `groups:write` scopes are granted

**`not_in_channel` error:**
- The bot needs to be invited to the channel before sending messages
- Run `/invite @your-bot-name` in the target channel

**`invalid_auth` error:**
- Check that `SLACK_BOT_TOKEN` starts with `xoxb-`
- Token may have been revoked — regenerate in Slack App settings

**`missing_scope` error:**
- Add the required scopes in **OAuth & Permissions** and reinstall the app
- See [Slack App Setup](slack-app-setup.md#2-configure-bot-token-scopes) for required scopes

**Slack API temporary failure:**
- Auto retry logic attempts up to 3 times (2s → 4s → 8s wait)
- Check logs if still failing after retries

<br/>

## Kubernetes Issues

**503 Service Unavailable:**
- Check Ingress configuration: `kubectl describe ingress -n slack-bots`
- Verify Service selector matches Pod label: `kubectl get endpoints -n slack-bots`
- Check Pod status: `kubectl get pods -n slack-bots`

**Pod CrashLoopBackOff:**
- Check logs: `kubectl logs -n slack-bots deployment/slack-qr-bot`
- Verify secrets exist: `kubectl get secrets -n slack-bots`
- Verify `SLACK_BOT_TOKEN` is valid

**ImagePullBackOff:**
- Verify image exists: `docker pull somaz940/slack-qr-bot:v0.2.0`
- If using private registry, ensure `imagePullSecrets` are configured

<br/>

## Development Issues

**Tests failing:**
```bash
# Run tests with verbose output
make test

# Check lint errors
make lint
```

**Helm chart issues:**
```bash
# Validate chart
make test-helm

# Debug template rendering
helm template test-release helm/slack-qr-bot/ --debug
```
