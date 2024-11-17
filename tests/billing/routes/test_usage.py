from collections.abc import Generator
from unittest.mock import Mock, patch

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from billing.schemas import UsageEntry, UsageResponse
from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestUsageEndpoint:
    endpoint = "/usage"
    @pytest.fixture
    def mock_usage_service(self) -> Generator[Mock, None, None]:
        with patch("billing.router.UsageService") as mock:
            yield mock.return_value

    def test_successful_request__returns_200_with_usage_data(
        self,
        client: TestClient,
        mock_usage_service: Mock,
    ) -> None:
        usage = UsageEntry(
            message_id=1,
            timestamp="2024-01-01T00:00:00",
            report_name="Test report",
            credits_used=10.54,
        )
        usage_response = UsageResponse(usage=[usage])
        mock_usage_service.get_usage.return_value = usage_response

        response = client.get(self.endpoint)

        assert response.status_code == 200
        data = response.json()
        assert "usage" in data
        assert len(data["usage"]) == 1
        assert data["usage"][0]["message_id"] == usage.message_id
        assert data["usage"][0]["timestamp"] == usage.timestamp
        assert data["usage"][0]["report_name"] == usage.report_name
        assert data["usage"][0]["credits_used"] == float(usage.credits_used)

    def test_empty_messages__returns_200_with_empty_usage(
        self,
        client: TestClient,
        mock_usage_service: Mock,
    ) -> None:
        usage_response = UsageResponse(usage=[])
        mock_usage_service.get_usage.return_value = usage_response

        response = client.get(self.endpoint)

        assert response.status_code == 200
        data = response.json()
        assert "usage" in data
        assert len(data["usage"]) == 0

    def test_message_service_error__returns_500(
        self,
        client: TestClient,
        mock_usage_service: Mock,
    ) -> None:
        mock_usage_service.get_usage.side_effect = HTTPException(status_code=500)

        response = client.get(self.endpoint)

        assert response.status_code == 500

    # NOTE: Could add more tests for other error cases (e.g. report service error, calculate credits service error) etc, but omitted for brevity.
