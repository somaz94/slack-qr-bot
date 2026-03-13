"""Tests for health check route"""

from unittest.mock import patch
from tests.conftest import parse_response


class TestHealthCheck:
    @patch("src.routes.health.check_slack_connection")
    def test_healthy(self, mock_check, client):
        mock_check.return_value = {
            "connected": True,
            "team": "TestTeam",
            "user": "bot",
            "bot_id": "B123"
        }
        resp = client.get("/health")
        body, code = parse_response(resp)
        assert code == 200
        assert body["message"] == "Service is healthy"
        assert body["data"]["status"] == "healthy"
        assert body["data"]["slack_connection"]["connected"] is True

    @patch("src.routes.health.check_slack_connection")
    def test_unhealthy(self, mock_check, client):
        mock_check.return_value = {
            "connected": False,
            "error": "invalid_auth"
        }
        resp = client.get("/health")
        body, code = parse_response(resp)
        assert code == 503
        assert body["data"]["status"] == "unhealthy"
