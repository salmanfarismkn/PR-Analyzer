from __future__ import annotations

import re

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.commit.models import Commit
from app.github.service import GitHubService
from app.outcome.revert_models import RevertEvent
from app.pull_request.models import PullRequest


class RevertDetectionService:

    REVERT_SHA_PATTERN = re.compile(
        r"This reverts commit\s+([0-9a-fA-F]{7,40})",
        re.IGNORECASE,
    )

    REVERT_TITLE_PATTERN = re.compile(
        r'^Revert\s+"(?P<title>.+)"',
        re.IGNORECASE,
    )

    def __init__(self) -> None:
        self._github = GitHubService()

    def inspect_commit(
        self,
        db: Session,
        repository_owner: str,
        repository_name: str,
        commit_sha: str,
    ) -> RevertEvent | None:

        commit_data = self._github.get_commit(
            owner=repository_owner,
            repository=repository_name,
            sha=commit_sha,
        )

        github_commit = commit_data.get(
            "commit",
            {},
        )

        message = github_commit.get(
            "message",
            "",
        )

        if not message:
            return None

        original_commit_sha = (
            self._extract_original_sha(message)
        )

        if original_commit_sha is None:
            return None

        original_commit = self._find_original_commit(
            db=db,
            sha=original_commit_sha,
        )

        if original_commit is None:
            return None

        if original_commit.pull_request_id is None:
            return None

        pull_request = db.get(
            PullRequest,
            original_commit.pull_request_id,
        )

        if pull_request is None:
            return None

        existing = db.scalar(
            select(RevertEvent).where(
                RevertEvent.revert_commit_sha
                == commit_sha
            )
        )

        if existing is not None:
            return existing

        event = RevertEvent(
            pull_request_id=pull_request.id,
            revert_commit_sha=commit_sha,
            original_commit_sha=original_commit.sha,
            message=message,
            confidence="high",
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        return event

    @staticmethod
    def _extract_original_sha(
        message: str,
    ) -> str | None:

        match = RevertDetectionService.REVERT_SHA_PATTERN.search(
            message
        )

        if match is None:
            return None

        return match.group(1)

    @staticmethod
    def _find_original_commit(
        db: Session,
        sha: str,
    ) -> Commit | None:

        normalized_sha = sha.strip().lower()

        commit = db.scalar(
            select(Commit).where(
                func.lower(Commit.sha) == normalized_sha
            )
        )

        if commit is not None:
            return commit

        return db.scalar(
            select(Commit).where(
                func.lower(Commit.sha).startswith(normalized_sha)
            )
        )