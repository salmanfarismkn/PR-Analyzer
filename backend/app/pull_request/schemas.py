from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
    imported: int

    skipped: int

    total: int