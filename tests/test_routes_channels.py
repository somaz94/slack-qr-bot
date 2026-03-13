"""Tests for channels route"""

from unittest.mock import patch
from tests.conftest import parse_response


class TestListChannels:
    @patch("src.routes.channels.get_bot_channels")
    def test_success(self, mock_channels, client):
        mock_channels.return_value = [
            {"id": "C1", "name": "general", "is_private": False, "num_members": 10},
            {"id": "C2", "name": "dev", "is_private": True, "num_members": 5}
        ]
        resp = client.get("/channels")
        body, code = parse_response(resp)
        assert code == 200
        assert body["data"]["count"] == 2
        assert len(body["data"]["channels"]) == 2

    @patch("src.routes.channels.get_bot_channels")
    def test_error(self, mock_channels, client):
        mock_channels.side_effect = Exception("Slack error")
        resp = client.get("/channels")
        body, code = parse_response(resp)
        assert code == 500
