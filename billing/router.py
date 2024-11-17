import logging

from fastapi import APIRouter

from billing.constants import DEFAULT_BILLING_PARAMETERS
from billing.schemas import UsageResponse
from billing.services.credit_calculation_service import CalculateCreditsService
from billing.services.messages_service import MessageService
from billing.services.reports_service import ReportService
from billing.services.usage_service import UsageService

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["billing"],
)


@router.get("/usage")
def get_usage() -> UsageResponse:
    """
    Decision: I'm not adding authentication for this endpoint but it should be added in a real-world scenario.
    """
    reports_service = ReportService()
    message_service = MessageService()
    # NOTE: Could get parameters for a specific customer here if needed in real-world scenario.
    credit_calculation_service = CalculateCreditsService(DEFAULT_BILLING_PARAMETERS)
    usage_service = UsageService(message_service, reports_service, credit_calculation_service)
    # NOTE: In the real-world scenario could pass a customerid to the get_usage method and only return usage for that
    # customer.
    return usage_service.get_usage()
