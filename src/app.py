import os
from flask import Flask
from flasgger import Swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .config import (
    swagger_config, swagger_template, RATE_LIMIT_ENABLED,
    RATE_LIMIT_DEFAULT, setup_logging, validate_env
)
from .routes import health_bp, qr_bp, channels_bp, slack_events_bp


def create_app():
    """Flask application factory"""
    # Validate environment variables & setup logging (run at app creation time)
    validate_env()
    setup_logging()

    app = Flask(__name__)

    # Initialize Swagger
    Swagger(app, config=swagger_config, template=swagger_template)

    # Create Rate Limiter and connect to app
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[RATE_LIMIT_DEFAULT] if RATE_LIMIT_ENABLED else [],
        storage_uri="memory://"
    )
    limiter.init_app(app)

    # Register Blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(qr_bp)
    app.register_blueprint(channels_bp)
    app.register_blueprint(slack_events_bp)

    # Apply rate limits
    from .routes.qr import apply_rate_limits
    apply_rate_limits(limiter)

    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
