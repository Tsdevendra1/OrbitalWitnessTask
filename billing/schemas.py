from pydantic import BaseModel


class UsageEntry(BaseModel):
    message_id: int
    timestamp: str
    report_name: str | None = None
    credits_used: float


class UsageResponse(BaseModel):
    usage: list[UsageEntry]
