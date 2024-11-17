from unittest.mock import Mock, patch

import pytest
import requests
from fastapi import HTTPException

from billing.models import Message
from billing.services.messages_service import MessageService


class TestMessageService:
    @pytest.fixture
    def message_service(self) -> MessageService:
        return MessageService("http://test-service.com")

    @pytest.fixture
    def sample_messages_data(self) -> dict[str, list[dict[str, str | int | None]]]:
        return {
            "messages": [
                {
                    "id": 1,
                    "timestamp": "2024-01-01T00:00:00",
                    "text": "Test message 1",
                },
                {
                    "id": 2,
                    "timestamp": "2024-01-01T00:00:00",
                    "text": "Test message 1",
                    "report_id": None,
                },
                {
                    "id": 3,
                    "timestamp": "2024-01-01T00:00:01",
                    "text": "Test message 2",
                    "report_id": 123,
                },
            ]
        }

    def test_successful_fetch__returns_messages(
        self,
        message_service: MessageService,
        sample_messages_data: dict[str, list[dict[str, str | int | None]]],
    ) -> None:
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_messages_data
            mock_get.return_value = mock_response

            result = message_service.fetch_messages()

            assert isinstance(result, list)
            assert len(result) == 3
            assert all(isinstance(msg, Message) for msg in result)
            assert result[0].id == sample_messages_data["messages"][0]["id"]
            assert result[0].text == sample_messages_data["messages"][0]["text"]
            assert result[0].report_id is None
            assert result[1].report_id is None
            assert result[2].report_id == 123
            mock_get.assert_called_once_with("http://test-service.com/messages/current-period")

    def test_server_error__raises_http_exception(
        self,
        message_service: MessageService,
    ) -> None:
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
            mock_get.return_value = mock_response

            with pytest.raises(HTTPException) as exc_info:
                message_service.fetch_messages()
            assert exc_info.value.status_code == 500
            assert "Failed to fetch messages" in str(exc_info.value.detail)

    # NOTE: Could have added more tests e.g. missing keys etc. but omitted for brevity.
