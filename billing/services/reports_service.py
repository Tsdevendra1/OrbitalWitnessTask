import logging

import requests
from fastapi import HTTPException

from billing.constants import BASE_SERVICE_URL
from billing.models import Report

logger = logging.getLogger(__name__)


class ReportService:
    """
    Decision: Use class for fetching reports instead of a normal function. I've seen either approach used in real-world
    applications. I think a class is better here because we might want to add more functionality in the future. In
    addition, it also makes creating mocks for testing easier.
    """

    def __init__(self, base_url: str = BASE_SERVICE_URL) -> None:
        self._base_url = base_url

    def fetch_report(self, report_id: int) -> Report | None:
        try:
            response = requests.get(f"{self._base_url}/reports/{report_id}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return Report(**response.json())
        except Exception as e:
            logger.error(f"Error fetching report {report_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch report {report_id}")
