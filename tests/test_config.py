"""Tests for configuration"""

import os
from src.config import setup_logging, swagger_config, swagger_template


class TestConfig:
    def test_swagger_config_has_specs_route(self):
        assert swagger_config["specs_route"] == "/api-docs"

    def test_swagger_template_info(self):
        assert swagger_template["info"]["title"] == "Slack QR Bot API"
        assert swagger_template["info"]["version"] == "1.0.0"

    def test_swagger_security_definitions(self):
        assert "ApiKeyAuth" in swagger_template["securityDefinitions"]
        assert swagger_template["securityDefinitions"]["ApiKeyAuth"]["type"] == "apiKey"
        assert swagger_template["securityDefinitions"]["ApiKeyAuth"]["name"] == "X-API-Key"

    def test_setup_logging(self):
        setup_logging()
        import logging
        root = logging.getLogger()
        assert root.level == logging.INFO

    def test_api_key_from_env(self, monkeypatch):
        monkeypatch.setenv("API_KEY", "my-secret")
        # Re-import to pick up new value
        import importlib
        import src.config
        importlib.reload(src.config)
        assert src.config.API_KEY == "my-secret"

    def test_rate_limit_enabled_default(self, monkeypatch):
        monkeypatch.setenv("RATE_LIMIT_ENABLED", "true")
        import importlib
        import src.config
        importlib.reload(src.config)
        assert src.config.RATE_LIMIT_ENABLED is True

    def test_rate_limit_disabled(self, monkeypatch):
        monkeypatch.setenv("RATE_LIMIT_ENABLED", "false")
        import importlib
        import src.config
        importlib.reload(src.config)
        assert src.config.RATE_LIMIT_ENABLED is False
