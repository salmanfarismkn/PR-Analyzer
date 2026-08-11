from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.pull_request_sync import (
    PullRequestSyncService,
)
from app.pull_request.models import PullRequest
from app.repository.models import Repository
from app.webhook.schemas import PullRequestWebhookPayload
from app import db


class PullRequestWebhookService:

    def __init__(self) -> None:
        self._sync_service = PullRequestSyncService()

    def process(
        self,
        db: Session,
        payload: PullRequestWebhookPayload,
    ) -> PullRequest | None:

        if payload.action not in {
            "opened",
            "reopened",
            "synchronize",
            "closed",
        }:
            return None

        repository = db.scalar(
            select(Repository).where(
                Repository.owner == payload.repository.owner["login"],
                Repository.name == payload.repository.name,
            )
        )

        if repository is None:
            raise ValueError(
                "Repository from webhook "
                "does not exist locally."
            )

        pull_request = db.scalar(
            select(PullRequest).where(
                PullRequest.github_id
                == payload.pull_request.id
            )
        )

        if pull_request is None:
            pull_request = self._create_pull_request(
                db=db,
                repository=repository,
                payload=payload,
            )
        else:
            self._update_pull_request(
                pull_request=pull_request,
                payload=payload,
            )

        db.commit()
        db.refresh(pull_request)

        if payload.action == "synchronize":
            self._sync_service.sync_pull_request(
                db=db,
                pull_request=pull_request,
            )

        return pull_request

    @staticmethod
    def _create_pull_request(
        db: Session,
        repository: Repository,
        payload: PullRequestWebhookPayload,
    ) -> PullRequest:

        github_pr = payload.pull_request

# Create new PullRequest
        pull_request = PullRequest(
            repository_id=repository.id,
            github_id=github_pr.id,
            number=github_pr.number,
            title=github_pr.title,
            state=github_pr.state,
            author=getattr(github_pr, "author", "unknown"),
            base_branch=getattr(github_pr, "base_branch", "main"),
            head_branch=getattr(github_pr, "head_branch", "unknown"),
            is_draft=getattr(github_pr, "is_draft", False),
            merged=github_pr.merged,
            merged_at=github_pr.merged_at,
            closed_at=github_pr.closed_at,
        )
        db.add(pull_request)


        return pull_request

    @staticmethod
    def _update_pull_request(
        pull_request: PullRequest,
        payload: PullRequestWebhookPayload,
    ) -> None:

# Update existing PullRequest
        github_pr = payload.pull_request

        pull_request.number = github_pr.number
        pull_request.title = github_pr.title
        pull_request.author = getattr(github_pr, "author", "unknown")
        pull_request.base_branch = getattr(github_pr, "base_branch", "main")
        pull_request.head_branch = getattr(github_pr, "head_branch", "unknown")
        pull_request.is_draft = getattr(github_pr, "is_draft", False)
        pull_request.state = github_pr.state
        pull_request.merged = github_pr.merged
        pull_request.merged_at = github_pr.merged_at
        pull_request.closed_at = github_pr.closed_at
