import logging

import requests
from fastapi import HTTPException

from billing.constants import BASE_SERVICE_URL
from billing.models import Message

logger = logging.getLogger(__name__)


class MessageService:
    """
    Decision: Use class for fetching reports instead of a normal function. I've seen either approach used in real-world
    applications. I think a class is better here because we might want to add more functionality in the future. In
    addition, it also makes creating mocks for testing easier.
    """

    def __init__(self, base_url: str = BASE_SERVICE_URL) -> None:
        self._base_url = base_url

    def fetch_messages(self) -> list[Message]:
        try:
            response = requests.get(f"{self._base_url}/messages/current-period")
            response.raise_for_status()
            data = response.json()
            return [Message(**msg) for msg in data["messages"]]
        except Exception as e:
            logger.error(f"Error fetching messages: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch messages")
