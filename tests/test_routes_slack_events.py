"""Tests for Slack events route"""

from unittest.mock import patch


class TestSlackEvents:
    def test_url_verification(self, client):
        resp = client.post("/slack/events", json={
            "challenge": "test-challenge-token"
        })
        assert resp.status_code == 200
        assert resp.get_json()["challenge"] == "test-challenge-token"

    @patch("src.routes.slack_events.send_qr_to_slack")
    def test_message_event_with_apk_build(self, mock_send, client):
        mock_send.return_value = {"file": {"id": "F1"}}
        resp = client.post("/slack/events", json={
            "event": {
                "type": "message",
                "text": "apk_build URL: https://example.com/app.apk",
                "channel": "C123"
            }
        })
        assert resp.status_code == 200
        mock_send.assert_called_once_with("C123", "https://example.com/app.apk")

    def test_message_event_without_apk_build(self, client):
        resp = client.post("/slack/events", json={
            "event": {
                "type": "message",
                "text": "hello world",
                "channel": "C123"
            }
        })
        assert resp.status_code == 200

    def test_no_event(self, client):
        resp = client.post("/slack/events", json={"type": "other"})
        assert resp.status_code == 200

    @patch("src.routes.slack_events.send_qr_to_slack")
    def test_event_processing_error(self, mock_send, client):
        mock_send.side_effect = Exception("Slack error")
        resp = client.post("/slack/events", json={
            "event": {
                "type": "message",
                "text": "apk_build URL: https://example.com/app.apk",
                "channel": "C123"
            }
        })
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "ok"

    def test_message_event_apk_build_no_url(self, client):
        resp = client.post("/slack/events", json={
            "event": {
                "type": "message",
                "text": "apk_build without url field",
                "channel": "C123"
            }
        })
        assert resp.status_code == 200

    def test_non_message_event(self, client):
        resp = client.post("/slack/events", json={
            "event": {
                "type": "reaction_added",
                "reaction": "thumbsup"
            }
        })
        assert resp.status_code == 200
