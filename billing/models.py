from decimal import Decimal

from pydantic import BaseModel


class Message(BaseModel):
    id: int
    timestamp: str
    text: str
    report_id: int | None = None


class Report(BaseModel):
    id: int
    name: str
    credit_cost: Decimal
