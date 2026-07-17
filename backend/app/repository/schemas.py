from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RepositoryCreate(BaseModel):
    github_id: int
    owner: str
    name: str
    description: str | None = None
    default_branch: str = "main"
    is_private: bool


class RepositoryResponse(BaseModel):
    id: int
    github_id: int
    owner: str
    name: str
    description: str | None
    default_branch: str
    is_private: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)