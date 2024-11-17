from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from billing.dataclasses import Credit
from billing.models import Message, Report
from billing.schemas import UsageResponse
from billing.services.credit_calculation_service import CalculateCreditsService
from billing.services.messages_service import MessageService
from billing.services.reports_service import ReportService
from billing.services.usage_service import UsageService


@pytest.fixture
def mock_message_service() -> Mock:
    return Mock(spec=MessageService)


@pytest.fixture
def mock_report_service() -> Mock:
    return Mock(spec=ReportService)


@pytest.fixture
def mock_calculate_credits_service() -> Mock:
    return Mock(spec=CalculateCreditsService)


@pytest.fixture
def usage_service(
    mock_message_service: Mock,
    mock_report_service: Mock,
    mock_calculate_credits_service: Mock,
) -> UsageService:
    return UsageService(
        message_service=mock_message_service,
        report_service=mock_report_service,
        calculate_credits_service=mock_calculate_credits_service,
    )


class TestGetUsage:
    def test_no_messages__returns_empty_usage(
        self,
        usage_service: UsageService,
        mock_message_service: Mock,
    ) -> None:
        mock_message_service.fetch_messages.return_value = []

        result = usage_service.get_usage()

        assert isinstance(result, UsageResponse)
        assert len(result.usage) == 0
        mock_message_service.fetch_messages.assert_called_once()

    def test_message_service_error__raises_http_exception(
        self,
        usage_service: UsageService,
        mock_message_service: Mock,
    ) -> None:
        mock_message_service.fetch_messages.side_effect = HTTPException(status_code=500, detail="Error")

        with pytest.raises(HTTPException):
            usage_service.get_usage()

    def test_message_without_report__returns_calculated_credits(
        self,
        usage_service: UsageService,
        mock_message_service: Mock,
        mock_calculate_credits_service: Mock,
    ) -> None:
        test_message = Message(
            id=1,
            timestamp=datetime.now().isoformat(),
            text="test message",
            report_id=None,
        )
        expected_credits = Credit.from_int(10)
        mock_message_service.fetch_messages.return_value = [test_message]
        mock_calculate_credits_service.calculate_credits.return_value = expected_credits

        result = usage_service.get_usage()

        assert len(result.usage) == 1
        assert result.usage[0].message_id == test_message.id
        assert result.usage[0].timestamp == test_message.timestamp
        assert result.usage[0].report_name is None
        assert result.usage[0].credits_used == expected_credits.amount
        mock_calculate_credits_service.calculate_credits.assert_called_once_with(test_message.text)

    def test_message_with_valid_report__returns_report_credits(
        self,
        usage_service: UsageService,
        mock_message_service: Mock,
        mock_report_service: Mock,
    ) -> None:
        report_id = 123
        test_message = Message(
            id=1,
            timestamp=datetime.now().isoformat(),
            text="test message",
            report_id=report_id,
        )
        test_report = Report(id=report_id, name="Test Report", credit_cost=Decimal("15.5"))
        mock_message_service.fetch_messages.return_value = [test_message]
        mock_report_service.fetch_report.return_value = test_report

        result = usage_service.get_usage()

        assert len(result.usage) == 1
        assert result.usage[0].message_id == test_message.id
        assert result.usage[0].timestamp == test_message.timestamp
        assert result.usage[0].report_name == test_report.name
        assert result.usage[0].credits_used == test_report.credit_cost
        mock_report_service.fetch_report.assert_called_once_with(test_message.report_id)

    def test_message_with_missing_report__returns_calculated_credits(
        self,
        usage_service: UsageService,
        mock_message_service: Mock,
        mock_report_service: Mock,
        mock_calculate_credits_service: Mock,
    ) -> None:
        test_message = Message(
            id=1,
            timestamp=datetime.now().isoformat(),
            text="test message",
            report_id=123,
        )
        expected_credits = Credit.from_int(10)
        mock_message_service.fetch_messages.return_value = [test_message]
        mock_report_service.fetch_report.return_value = None
        mock_calculate_credits_service.calculate_credits.return_value = expected_credits

        result = usage_service.get_usage()

        assert len(result.usage) == 1
        assert result.usage[0].message_id == test_message.id
        assert result.usage[0].timestamp == test_message.timestamp
        assert result.usage[0].report_name is None
        assert result.usage[0].credits_used == expected_credits.amount
        mock_report_service.fetch_report.assert_called_once_with(test_message.report_id)
        mock_calculate_credits_service.calculate_credits.assert_called_once_with(test_message.text)

    def test_report_service_error__raises_http_exception(
        self,
        usage_service: UsageService,
        mock_message_service: Mock,
        mock_report_service: Mock,
    ) -> None:
        test_message = Message(
            id=1,
            timestamp=datetime.now().isoformat(),
            text="test message",
            report_id=123,
        )
        mock_message_service.fetch_messages.return_value = [test_message]
        mock_report_service.fetch_report.side_effect = HTTPException(status_code=500, detail="Error")

        with pytest.raises(HTTPException):
            usage_service.get_usage()
