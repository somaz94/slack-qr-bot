"""Shared test fixtures"""

import os
import pytest

# Set env vars BEFORE any src imports
os.environ.setdefault("SLACK_BOT_TOKEN", "xoxb-test-token")
os.environ.setdefault("API_KEY", "test-api-key")


@pytest.fixture
def app():
    """Create Flask test app"""
    from src.app import create_app
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Create Flask test client"""
    return app.test_client()


@pytest.fixture
def auth_headers():
    """Headers with valid API key"""
    return {"X-API-Key": "test-api-key", "Content-Type": "application/json"}


@pytest.fixture
def no_auth_headers():
    """Headers without API key"""
    return {"Content-Type": "application/json"}


def parse_response(resp):
    """Parse jsonify(*tuple) response which returns [body, code] array"""
    data = resp.get_json()
    if isinstance(data, list) and len(data) == 2:
        return data[0], data[1]
    return data, resp.status_code
