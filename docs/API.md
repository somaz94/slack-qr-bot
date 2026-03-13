# API Reference

<br/>

## Health Check

<br/>

### GET /health

Check service health and Slack connection status.

#### Response (Healthy)

```json
{
  "code": 200,
  "message": "Service is healthy",
  "data": {
    "status": "healthy",
    "slack_connection": {
      "connected": true,
      "team": "My Workspace",
      "user": "bot",
      "bot_id": "B123456"
    }
  },
  "payLoad": {}
}
```

#### Response (Unhealthy)

```json
{
  "code": 503,
  "message": "Service degraded - Slack connection failed",
  "data": {
    "status": "unhealthy",
    "slack_connection": {
      "connected": false,
      "error": "invalid_auth"
    }
  },
  "payLoad": {}
}
```

| Status Code | Description |
|-------------|-------------|
| 200 | Service is healthy, Slack connected |
| 503 | Service degraded, Slack connection failed |

<br/>

## QR Code Generation

<br/>

### POST /generate-qr

Generate a QR code from an APK URL and send it to a Slack channel.

#### Headers

| Header | Required | Description |
|--------|----------|-------------|
| `X-API-Key` | No* | API authentication key |
| `Content-Type` | Yes | `application/json` |

> \* Required only when `API_KEY` environment variable is set

#### Request Body

```json
{
  "apk_url": "https://example.com/app.apk",
  "channel": "#apk-qr-generator",
  "build_number": "123"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `apk_url` | Yes | APK download URL |
| `channel` | Yes | Slack channel name (`#channel`) or ID (`C0A4WE1RJNR`) |
| `build_number` | No | Build number (displays `latest` if not provided) |

#### Response

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

| Status Code | Description |
|-------------|-------------|
| 200 | QR code sent successfully |
| 400 | Missing required parameters |
| 401 | API key required |
| 403 | Invalid API key |
| 500 | Slack API error |

<br/>

### POST /generate-qr/broadcast

Send QR code to multiple Slack channels.

#### Request Body

```json
{
  "apk_url": "https://example.com/app.apk",
  "channels": ["#channel1", "#channel2", "C0A4WE1RJNR"],
  "build_number": "123"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `apk_url` | Yes | APK download URL |
| `channels` | Yes | Array of channel names or IDs |
| `build_number` | No | Build number |

#### Response

```json
{
  "code": 200,
  "message": "Sent to 2/2 channels",
  "data": {
    "success_count": 2,
    "failed_count": 0,
    "results": [
      { "channel": "#channel1", "status": "success", "file_id": "F123" },
      { "channel": "#channel2", "status": "success", "file_id": "F456" }
    ]
  },
  "payLoad": {}
}
```

<br/>

### POST /generate-qr/custom

Generate a customizable QR code with color and size options.

#### Request Body

```json
{
  "apk_url": "https://example.com/app.apk",
  "channel": "#apk-qr-generator",
  "build_number": "123",
  "qr_options": {
    "box_size": 15,
    "border": 4,
    "fill_color": "#000000",
    "back_color": "#FFFFFF"
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `qr_options.box_size` | No | QR code box size (default: 10) |
| `qr_options.border` | No | QR code border size (default: 4) |
| `qr_options.fill_color` | No | QR code color (default: black) |
| `qr_options.back_color` | No | Background color (default: white) |

<br/>

### POST /generate-qr/broadcast-all

Send QR code to all channels the bot belongs to.

#### Request Body

```json
{
  "apk_url": "https://example.com/app.apk",
  "build_number": "123",
  "qr_options": {
    "box_size": 15
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `apk_url` | Yes | APK download URL |
| `build_number` | No | Build number |
| `qr_options` | No | QR customization options |

<br/>

## Channels

<br/>

### GET /channels

Retrieve list of channels the bot belongs to.

#### Response

```json
{
  "code": 200,
  "message": "Channels retrieved successfully",
  "data": {
    "channels": [
      {
        "id": "C0A4WE1RJNR",
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

## Slack Events

<br/>

### POST /slack/events

Handles Slack Events API callbacks. Responds to URL verification challenges and processes `apk_build` message events automatically.

#### URL Verification

```json
// Request
{ "challenge": "test-token" }

// Response
{ "challenge": "test-token" }
```

#### Message Event

When a message containing `apk_build` and `URL:` is detected, a QR code is automatically generated and sent to the channel.

<br/>

## Swagger UI

Interactive API documentation is available at `/api-docs` when the service is running.
