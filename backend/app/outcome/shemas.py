from datetime import datetime

from pydantic import BaseModel


class PullRequestOutcomeResponse(BaseModel):
    id: int

    pull_request_id: int

    status: str

    merged_at: datetime | None

    reason: str | None

    observed_at: datetime | None