from sqlalchemy import select
from sqlalchemy.orm import Session

from app.changed_file.models import ChangedFile
from app.github.client import GitHubClient
from app.github.schemas import GitHubChangedFile
from app.core.config import get_settings


class ChangedFileService:
    def __init__(self):
        settings = get_settings()
        self._client = GitHubClient(
            base_url=settings.github_api_url,
            token=settings.github_token,
        )

    def import_changed_files(
        self,
        db: Session,
        owner: str,
        repository: str,
        pull_number: int,
        commit_id: int,
    ) -> list[ChangedFile]:
        """
        Import changed files for a given pull request commit.
        Uses duplicate strategy: if a file already exists for the commit_id + filename,
        update it; otherwise insert a new record.
        """

        github_files: list[GitHubChangedFile] = self._client.list_changed_files(
            owner,
            repository,
            pull_number,
        )

        imported_files: list[ChangedFile] = []

        for gf in github_files:
            # Check if this file already exists for the commit
            existing = db.scalar(
                select(ChangedFile).where(
                    ChangedFile.commit_id == commit_id,
                    ChangedFile.filename == gf.filename,
                )
            )

            if existing:
                # Update existing record
                existing.status = gf.status
                existing.previous_filename = gf.previous_filename
                existing.additions = gf.additions
                existing.deletions = gf.deletions
                existing.changes = gf.changes
                existing.patch = gf.patch
                imported_files.append(existing)
            else:
                # Create new record
                new_file = ChangedFile(
                    commit_id=commit_id,
                    filename=gf.filename,
                    status=gf.status,
                    previous_filename=gf.previous_filename,
                    additions=gf.additions,
                    deletions=gf.deletions,
                    changes=gf.changes,
                    patch=gf.patch,
                )
                db.add(new_file)
                imported_files.append(new_file)

        db.commit()
        return imported_files
