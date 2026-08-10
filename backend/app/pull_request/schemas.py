from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import List

class PullRequestResponse(BaseModel):
    id: int

    github_id: int

    repository_id: int

    number: int

    title: str

    state: str

    author: str

    base_branch: str

    head_branch: str

    is_draft: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class PullRequestImportSummary(BaseModel):
    repository_id: int
    imported: int = 0
    skipped: int = 0
    total: int = 0
    details: List[dict] = []

class PullRequestSchema(BaseModel):
    id: int
    number: int
    title: str
    state: str
    merged: bool
    merged_at: datetime | None
    closed_at: datetime | None
    repository_id: int

    class Config:
        orm_mode = True