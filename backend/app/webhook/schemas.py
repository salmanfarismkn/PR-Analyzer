from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GitHubWebhookRepository(BaseModel):
    id: int
    name: str
    full_name: str
    owner: dict


class GitHubWebhookPullRequest(BaseModel):
    id: int
    number: int

    title: str

    state: str
    merged: bool

    merged_at: datetime | None
    closed_at: datetime | None

    model_config = ConfigDict(
        extra="ignore",
    )


class PullRequestWebhookPayload(BaseModel):
    action: str

    repository: GitHubWebhookRepository
    pull_request: GitHubWebhookPullRequest

    model_config = ConfigDict(
        extra="ignore",
    )