from decimal import Decimal
from unittest.mock import Mock, patch

import pytest
import requests
from fastapi import HTTPException
from requests import HTTPError

from billing.models import Report
from billing.services.reports_service import ReportService


class TestReportService:
    @pytest.fixture
    def report_service(self) -> ReportService:
        return ReportService("http://test-service.com")

    @pytest.fixture
    def sample_report_data(self) -> dict[str, str | int]:
        return {
            "id": 123,
            "name": "Test Report",
            "credit_cost": "15.5",
        }

    def test_valid_report_id__returns_report(
        self,
        report_service: ReportService,
        sample_report_data: dict[str, str | int],
    ) -> None:
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = sample_report_data
            mock_get.return_value = mock_response

            result = report_service.fetch_report(123)

            assert isinstance(result, Report)
            assert result.id == sample_report_data["id"]
            assert result.name == sample_report_data["name"]
            assert result.credit_cost == Decimal(sample_report_data["credit_cost"])
            mock_get.assert_called_once_with("http://test-service.com/reports/123")

    def test_nonexistent_report_id__returns_none(
        self,
        report_service: ReportService,
    ) -> None:
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            result = report_service.fetch_report(999)

            assert result is None
            mock_get.assert_called_once_with("http://test-service.com/reports/999")

    def test_server_error__raises_http_exception(
        self,
        report_service: ReportService,
    ) -> None:
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
            mock_get.return_value = mock_response

            with pytest.raises(HTTPException) as exc_info:
                report_service.fetch_report(123)

            assert exc_info.type == HTTPException
            mock_get.assert_called_once_with("http://test-service.com/reports/123")

    # NOTE: Could have added more tests e.g. missing keys etc. but omitted for brevity.
