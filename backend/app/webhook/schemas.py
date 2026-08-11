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

class GitHubWebhookUser(BaseModel):
    login: str
    id: int

    model_config = ConfigDict(
        extra="ignore",
    )


class GitHubPullRequestReview(BaseModel):
    id: int
    user: GitHubWebhookUser

    body: str | None

    state: str

    submitted_at: datetime | None

    html_url: str | None

    model_config = ConfigDict(
        extra="ignore",
    )


class PullRequestReviewWebhookPayload(BaseModel):
    action: str

    repository: GitHubWebhookRepository

    pull_request: GitHubWebhookPullRequest

    review: GitHubPullRequestReview

    model_config = ConfigDict(
        extra="ignore",
    )

class GitHubCheckRunWebhook(BaseModel):
    id: int
    name: str

    status: str
    conclusion: str | None

    details_url: str | None

    started_at: datetime | None
    completed_at: datetime | None

    head_sha: str

    model_config = ConfigDict(
        extra="ignore",
    )


class CheckRunWebhookPayload(BaseModel):
    action: str

    repository: GitHubWebhookRepository

    check_run: GitHubCheckRunWebhook

    model_config = ConfigDict(
        extra="ignore",
    )