"""Tests for QR code routes"""

from unittest.mock import patch
from tests.conftest import parse_response


class TestGenerateQr:
    @patch("src.decorators.API_KEY", "")
    def test_missing_params(self, client):
        resp = client.post("/generate-qr", json={})
        body, code = parse_response(resp)
        assert code == 400

    @patch("src.decorators.API_KEY", "")
    def test_missing_channel(self, client):
        resp = client.post("/generate-qr", json={
            "apk_url": "https://example.com/app.apk"
        })
        body, code = parse_response(resp)
        assert code == 400

    @patch("src.decorators.API_KEY", "")
    def test_missing_apk_url(self, client):
        resp = client.post("/generate-qr", json={"channel": "#test"})
        body, code = parse_response(resp)
        assert code == 400

    @patch("src.decorators.API_KEY", "")
    @patch("src.routes.qr.send_qr_to_slack")
    def test_success(self, mock_send, client):
        mock_send.return_value = {"file": {"id": "F123"}}
        resp = client.post("/generate-qr", json={
            "apk_url": "https://example.com/app.apk",
            "channel": "#test",
            "build_number": "42"
        })
        data = resp.get_json()
        assert data["success"] is True
        assert data["file_id"] == "F123"

    @patch("src.decorators.API_KEY", "")
    @patch("src.routes.qr.send_qr_to_slack")
    def test_slack_error(self, mock_send, client):
        mock_send.side_effect = Exception("Slack API error")
        resp = client.post("/generate-qr", json={
            "apk_url": "https://example.com/app.apk",
            "channel": "#test"
        })
        assert resp.status_code == 500


class TestBroadcastQr:
    @patch("src.decorators.API_KEY", "")
    def test_missing_params(self, client):
        resp = client.post("/generate-qr/broadcast", json={})
        body, code = parse_response(resp)
        assert code == 400

    @patch("src.decorators.API_KEY", "")
    def test_empty_channels(self, client):
        resp = client.post("/generate-qr/broadcast", json={
            "apk_url": "https://example.com/app.apk",
            "channels": []
        })
        body, code = parse_response(resp)
        assert code == 400

    @patch("src.decorators.API_KEY", "")
    def test_channels_not_list(self, client):
        resp = client.post("/generate-qr/broadcast", json={
            "apk_url": "https://example.com/app.apk",
            "channels": "#single"
        })
        body, code = parse_response(resp)
        assert code == 400

    @patch("src.decorators.API_KEY", "")
    @patch("src.routes.qr.send_qr_to_slack")
    def test_success(self, mock_send, client):
        mock_send.return_value = {"file": {"id": "F123"}}
        resp = client.post("/generate-qr/broadcast", json={
            "apk_url": "https://example.com/app.apk",
            "channels": ["#ch1", "#ch2"]
        })
        body, code = parse_response(resp)
        assert code == 200
        assert body["data"]["success_count"] == 2
        assert body["data"]["failed_count"] == 0

    @patch("src.decorators.API_KEY", "")
    @patch("src.routes.qr.send_qr_to_slack")
    def test_partial_failure(self, mock_send, client):
        mock_send.side_effect = [{"file": {"id": "F1"}}, Exception("fail")]
        resp = client.post("/generate-qr/broadcast", json={
            "apk_url": "https://example.com/app.apk",
            "channels": ["#ch1", "#ch2"]
        })
        body, code = parse_response(resp)
        assert code == 200
        assert body["data"]["success_count"] == 1
        assert body["data"]["failed_count"] == 1


class TestCustomQr:
    @patch("src.decorators.API_KEY", "")
    def test_missing_params(self, client):
        resp = client.post("/generate-qr/custom", json={})
        body, code = parse_response(resp)
        assert code == 400

    @patch("src.decorators.API_KEY", "")
    @patch("src.routes.qr.send_qr_to_slack")
    def test_success(self, mock_send, client):
        mock_send.return_value = {"file": {"id": "F456"}}
        resp = client.post("/generate-qr/custom", json={
            "apk_url": "https://example.com/app.apk",
            "channel": "#test",
            "qr_options": {"box_size": 15, "fill_color": "blue"}
        })
        body, code = parse_response(resp)
        assert code == 200
        assert body["data"]["file_id"] == "F456"

    @patch("src.decorators.API_KEY", "")
    @patch("src.routes.qr.send_qr_to_slack")
    def test_error(self, mock_send, client):
        mock_send.side_effect = Exception("Slack error")
        resp = client.post("/generate-qr/custom", json={
            "apk_url": "https://example.com/app.apk",
            "channel": "#test"
        })
        body, code = parse_response(resp)
        assert code == 500


class TestBroadcastAll:
    @patch("src.decorators.API_KEY", "")
    def test_missing_apk_url(self, client):
        resp = client.post("/generate-qr/broadcast-all", json={})
        body, code = parse_response(resp)
        assert code == 400

    @patch("src.decorators.API_KEY", "")
    @patch("src.routes.qr.get_bot_channels")
    def test_no_channels(self, mock_channels, client):
        mock_channels.return_value = []
        resp = client.post("/generate-qr/broadcast-all", json={
            "apk_url": "https://example.com/app.apk"
        })
        body, code = parse_response(resp)
        assert code == 400

    @patch("src.decorators.API_KEY", "")
    @patch("src.routes.qr.send_qr_to_slack")
    @patch("src.routes.qr.get_bot_channels")
    def test_success(self, mock_channels, mock_send, client):
        mock_channels.return_value = [
            {"id": "C1", "name": "ch1"},
            {"id": "C2", "name": "ch2"}
        ]
        mock_send.return_value = {"file": {"id": "F789"}}
        resp = client.post("/generate-qr/broadcast-all", json={
            "apk_url": "https://example.com/app.apk"
        })
        body, code = parse_response(resp)
        assert code == 200
        assert body["data"]["total_channels"] == 2
        assert body["data"]["success_count"] == 2

    @patch("src.decorators.API_KEY", "")
    @patch("src.routes.qr.get_bot_channels")
    def test_get_channels_error(self, mock_channels, client):
        mock_channels.side_effect = Exception("Slack down")
        resp = client.post("/generate-qr/broadcast-all", json={
            "apk_url": "https://example.com/app.apk"
        })
        body, code = parse_response(resp)
        assert code == 500

    @patch("src.decorators.API_KEY", "")
    @patch("src.routes.qr.send_qr_to_slack")
    @patch("src.routes.qr.get_bot_channels")
    def test_send_partial_failure(self, mock_channels, mock_send, client):
        mock_channels.return_value = [
            {"id": "C1", "name": "ch1"},
            {"id": "C2", "name": "ch2"}
        ]
        mock_send.side_effect = [{"file": {"id": "F1"}}, Exception("fail")]
        resp = client.post("/generate-qr/broadcast-all", json={
            "apk_url": "https://example.com/app.apk"
        })
        body, code = parse_response(resp)
        assert code == 200
        assert body["data"]["success_count"] == 1
        assert body["data"]["failed_count"] == 1
