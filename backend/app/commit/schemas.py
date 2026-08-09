from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommitResponse(BaseModel):
    id: int

    pull_request_id: int

    sha: str

    message: str

    author_name: str

    author_email: str

    committed_at: datetime

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class CommitImportSummary(BaseModel):
    imported: int

    skipped: int

    total: int