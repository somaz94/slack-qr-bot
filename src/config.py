"""Swagger API documentation and app configuration"""

import os
import sys
import logging
from pythonjsonlogger import jsonlogger


def validate_env():
    """Validate required environment variables"""
    required_vars = {
        "SLACK_BOT_TOKEN": "Slack Bot OAuth Token (xoxb-...)"
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.environ.get(var):
            missing_vars.append(f"{var}: {description}")
    
    if missing_vars:
        error_msg = "Missing required environment variables:\n" + "\n".join(f"  - {var}" for var in missing_vars)
        logging.error(error_msg)
        print(f"\n❌ {error_msg}\n", file=sys.stderr)
        sys.exit(1)
    
    # Warning for optional environment variables
    optional_vars = {
        "API_KEY": "API authentication key (recommended for production)",
        "RATE_LIMIT_ENABLED": "Enable rate limiting (default: true)"
    }
    
    for var, description in optional_vars.items():
        if not os.environ.get(var):
            logging.warning(f"Optional environment variable not set: {var} - {description}")


# API key configuration
API_KEY = os.environ.get("API_KEY", "")

# Rate limiting configuration
RATE_LIMIT_ENABLED = os.environ.get("RATE_LIMIT_ENABLED", "true").lower() == "true"
RATE_LIMIT_DEFAULT = "10 per minute"  # Default limit: 10 per minute


def setup_logging():
    """Setup JSON logging"""
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    log_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(log_handler)
    root_logger.setLevel(logging.INFO)


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api-docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Slack QR Bot API",
        "description": "API to convert APK download URLs to QR codes and send them to Slack channels",
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "url": "https://github.com/your-repo",
        }
    },
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "ApiKeyAuth": {
            "type": "apiKey",
            "name": "X-API-Key",
            "in": "header",
            "description": "Enter your API key (e.g., somaz-super-user)"
        }
    },
    "tags": [
        {
            "name": "Health",
            "description": "Health check endpoints"
        },
        {
            "name": "QR Code",
            "description": "QR code generation and transmission"
        },
        {
            "name": "Channels",
            "description": "Slack channel management"
        }
    ]
}
