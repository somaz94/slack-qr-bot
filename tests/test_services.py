"""Tests for QR code generation and Slack services"""

import io
from unittest.mock import patch, MagicMock
from PIL import Image
from slack_sdk.errors import SlackApiError

from src.services import generate_qr_code, check_slack_connection, get_channel_id, get_bot_channels, send_qr_to_slack


class TestGenerateQrCode:
    def test_returns_bytes_io(self):
        result = generate_qr_code("https://example.com")
        assert isinstance(result, io.BytesIO)

    def test_generates_valid_png(self):
        result = generate_qr_code("https://example.com")
        img = Image.open(result)
        assert img.format == "PNG"

    def test_custom_box_size(self):
        small = generate_qr_code("https://example.com", box_size=5)
        large = generate_qr_code("https://example.com", box_size=20)
        small_img = Image.open(small)
        large_img = Image.open(large)
        assert large_img.size[0] > small_img.size[0]

    def test_custom_colors(self):
        result = generate_qr_code(
            "https://example.com",
            fill_color="blue",
            back_color="yellow",
        )
        img = Image.open(result)
        assert img.format == "PNG"


class TestCheckSlackConnection:
    @patch("src.services.slack_client")
    def test_connected(self, mock_client):
        mock_client.auth_test.return_value = {
            "team": "TestTeam",
            "user": "bot",
            "bot_id": "B123"
        }
        result = check_slack_connection()
        assert result["connected"] is True
        assert result["team"] == "TestTeam"

    @patch("src.services.slack_client")
    def test_connection_failed(self, mock_client):
        mock_response = MagicMock()
        mock_response.__getitem__ = MagicMock(return_value="invalid_auth")
        mock_client.auth_test.side_effect = SlackApiError("error", mock_response)
        result = check_slack_connection()
        assert result["connected"] is False
        assert result["error"] == "invalid_auth"


class TestGetChannelId:
    def test_channel_id_direct(self):
        result = get_channel_id("C0A4WE1RJNR")
        assert result == "C0A4WE1RJNR"

    def test_channel_id_with_g_prefix(self):
        result = get_channel_id("G0A4WE1RJNR")
        assert result == "G0A4WE1RJNR"

    @patch("src.services.slack_client")
    def test_channel_name_found(self, mock_client):
        mock_client.conversations_list.return_value = {
            "channels": [
                {"name": "general", "id": "C123"},
                {"name": "test", "id": "C456"}
            ],
            "response_metadata": {"next_cursor": ""}
        }
        result = get_channel_id("#test")
        assert result == "C456"

    @patch("src.services.slack_client")
    def test_channel_name_not_found(self, mock_client):
        mock_client.conversations_list.return_value = {
            "channels": [{"name": "general", "id": "C123"}],
            "response_metadata": {"next_cursor": ""}
        }
        try:
            get_channel_id("#nonexistent")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "not found" in str(e)

    @patch("src.services.slack_client")
    def test_channel_name_pagination(self, mock_client):
        mock_client.conversations_list.side_effect = [
            {
                "channels": [{"name": "general", "id": "C1"}],
                "response_metadata": {"next_cursor": "next123"}
            },
            {
                "channels": [{"name": "target", "id": "C2"}],
                "response_metadata": {"next_cursor": ""}
            }
        ]
        result = get_channel_id("#target")
        assert result == "C2"

    @patch("src.services.slack_client")
    def test_slack_api_error(self, mock_client):
        mock_response = MagicMock()
        mock_response.__getitem__ = MagicMock(return_value="not_authed")
        mock_client.conversations_list.side_effect = SlackApiError("error", mock_response)
        try:
            get_channel_id("#test")
            assert False, "Should have raised SlackApiError"
        except SlackApiError:
            pass


class TestGetBotChannels:
    @patch("src.services.slack_client")
    def test_returns_member_channels(self, mock_client):
        mock_client.conversations_list.return_value = {
            "channels": [
                {"id": "C1", "name": "general", "is_member": True, "is_private": False, "num_members": 10},
                {"id": "C2", "name": "random", "is_member": False, "is_private": False, "num_members": 5},
                {"id": "C3", "name": "dev", "is_member": True, "is_private": True, "num_members": 3},
            ],
            "response_metadata": {"next_cursor": ""}
        }
        result = get_bot_channels()
        assert len(result) == 2
        assert result[0]["name"] == "general"
        assert result[1]["name"] == "dev"
        assert result[1]["is_private"] is True

    @patch("src.services.slack_client")
    def test_slack_api_error(self, mock_client):
        mock_response = MagicMock()
        mock_response.__getitem__ = MagicMock(return_value="not_authed")
        mock_client.conversations_list.side_effect = SlackApiError("error", mock_response)
        try:
            get_bot_channels()
            assert False, "Should have raised SlackApiError"
        except SlackApiError:
            pass


class TestSendQrToSlack:
    @patch("src.services.slack_client")
    def test_success(self, mock_client):
        mock_client.conversations_info.return_value = {
            "channel": {"name": "test", "is_private": False, "is_member": True}
        }
        mock_client.files_upload_v2.return_value = {"file": {"id": "F123"}}
        result = send_qr_to_slack("C0A4WE1RJNR", "https://example.com/app.apk", "42")
        assert result["file"]["id"] == "F123"

    @patch("src.services.slack_client")
    def test_success_with_qr_options(self, mock_client):
        mock_client.conversations_info.return_value = {
            "channel": {"name": "test", "is_private": False, "is_member": True}
        }
        mock_client.files_upload_v2.return_value = {"file": {"id": "F456"}}
        result = send_qr_to_slack(
            "C0A4WE1RJNR", "https://example.com/app.apk", "42",
            qr_options={"box_size": 15, "fill_color": "blue"}
        )
        assert result["file"]["id"] == "F456"

    @patch("src.services.slack_client")
    def test_without_build_number(self, mock_client):
        mock_client.conversations_info.return_value = {
            "channel": {"name": "test", "is_private": False, "is_member": True}
        }
        mock_client.files_upload_v2.return_value = {"file": {"id": "F789"}}
        result = send_qr_to_slack("C0A4WE1RJNR", "https://example.com/app.apk")
        assert result["file"]["id"] == "F789"

    @patch("src.services.slack_client")
    def test_conversations_info_fails_gracefully(self, mock_client):
        mock_response = MagicMock()
        mock_response.__getitem__ = MagicMock(return_value="channel_not_found")
        mock_client.conversations_info.side_effect = SlackApiError("error", mock_response)
        mock_client.files_upload_v2.return_value = {"file": {"id": "F1"}}
        result = send_qr_to_slack("C0A4WE1RJNR", "https://example.com/app.apk")
        assert result["file"]["id"] == "F1"

    @patch("src.services.slack_client")
    def test_upload_fails(self, mock_client):
        mock_client.conversations_info.return_value = {
            "channel": {"name": "test", "is_private": False, "is_member": True}
        }
        mock_response = MagicMock()
        mock_response.__getitem__ = MagicMock(return_value="not_in_channel")
        mock_client.files_upload_v2.side_effect = SlackApiError("error", mock_response)
        try:
            send_qr_to_slack("C0A4WE1RJNR", "https://example.com/app.apk")
            assert False, "Should have raised SlackApiError"
        except SlackApiError:
            pass

    @patch("src.services.get_channel_id")
    @patch("src.services.slack_client")
    def test_channel_lookup_fails(self, mock_client, mock_get_channel):
        mock_get_channel.side_effect = ValueError("Channel not found: bad")
        try:
            send_qr_to_slack("#bad", "https://example.com/app.apk")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
