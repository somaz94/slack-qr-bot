"""Tests for API key authentication decorator"""

from unittest.mock import patch


class TestRequireApiKey:
    @patch("src.decorators.API_KEY", "test-api-key")
    def test_no_api_key_returns_401(self, client, no_auth_headers):
        resp = client.post("/generate-qr", headers=no_auth_headers, json={
            "apk_url": "https://example.com/app.apk",
            "channel": "#test"
        })
        data = resp.get_json()
        # jsonify(*unauthorized()) returns [body, 401]
        if isinstance(data, list):
            assert data[1] == 401
        else:
            assert resp.status_code == 401

    @patch("src.decorators.API_KEY", "test-api-key")
    def test_invalid_api_key_returns_403(self, client):
        headers = {"X-API-Key": "wrong-key", "Content-Type": "application/json"}
        resp = client.post("/generate-qr", headers=headers, json={
            "apk_url": "https://example.com/app.apk",
            "channel": "#test"
        })
        data = resp.get_json()
        if isinstance(data, list):
            assert data[1] == 403
        else:
            assert resp.status_code == 403

    @patch("src.decorators.API_KEY", "test-api-key")
    @patch("src.routes.qr.send_qr_to_slack")
    def test_valid_api_key_passes(self, mock_send, client):
        mock_send.return_value = {"file": {"id": "F1"}}
        headers = {"X-API-Key": "test-api-key", "Content-Type": "application/json"}
        resp = client.post("/generate-qr", headers=headers, json={
            "apk_url": "https://example.com/app.apk",
            "channel": "#test"
        })
        assert resp.status_code == 200

    @patch("src.decorators.API_KEY", "")
    @patch("src.routes.qr.send_qr_to_slack")
    def test_no_api_key_configured_skips_auth(self, mock_send, client):
        mock_send.return_value = {"file": {"id": "F1"}}
        resp = client.post("/generate-qr", headers={"Content-Type": "application/json"}, json={
            "apk_url": "https://example.com/app.apk",
            "channel": "#test"
        })
        assert resp.status_code == 200
