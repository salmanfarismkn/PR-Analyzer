from sqlalchemy import func,select
from sqlalchemy.orm import Session

from app.changed_file.models import ChangedFile
from app.analysis.schemas import PullRequestMetrics


class AnalysisService:
    def calculate_metrics(
        self,
        db: Session,
        pull_request_id: int,
    ) -> PullRequestMetrics:
        """
        Deterministically calculate metrics for a pull request
        based on its ChangedFile records.
        """

        files = list(
            db.scalars(
                select(ChangedFile).join(ChangedFile.commit).where(
                    ChangedFile.commit.has(pull_request_id=pull_request_id)
                )
            )
        )

        total_files = len(files)

        # Simple classification rules
        source_files = sum(1 for f in files if f.filename.endswith(".py"))
        test_files = sum(1 for f in files if "test" in f.filename.lower())
        documentation_files = sum(1 for f in files if f.filename.endswith(".md"))
        config_files = sum(1 for f in files if f.filename.endswith((".yml", ".yaml", ".json")))
        binary_files = sum(1 for f in files if f.filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".exe")))

        renamed_files = sum(1 for f in files if f.previous_filename is not None)
        deleted_files = sum(1 for f in files if f.status == "removed")

        added_lines = sum(f.additions for f in files)
        deleted_lines = sum(f.deletions for f in files)
        total_changes = sum(f.changes for f in files)

        return PullRequestMetrics(
            total_files=total_files,
            source_files=source_files,
            test_files=test_files,
            documentation_files=documentation_files,
            config_files=config_files,
            binary_files=binary_files,
            renamed_files=renamed_files,
            deleted_files=deleted_files,
            added_lines=added_lines,
            deleted_lines=deleted_lines,
            total_changes=total_changes,
        )
    def calculate_total_files(self, db: Session, pull_request_id: int) -> int:
        return db.scalar(
            select(func.count(ChangedFile.id))
            .join(ChangedFile.commit)
            .where(ChangedFile.commit.has(pull_request_id=pull_request_id))
        )

    def calculate_added_lines(self, db: Session, pull_request_id: int) -> int:
        return db.scalar(
            select(func.coalesce(func.sum(ChangedFile.additions), 0))
            .join(ChangedFile.commit)
            .where(ChangedFile.commit.has(pull_request_id=pull_request_id))
        )

    def calculate_deleted_lines(self, db: Session, pull_request_id: int) -> int:
        return db.scalar(
            select(func.coalesce(func.sum(ChangedFile.deletions), 0))
            .join(ChangedFile.commit)
            .where(ChangedFile.commit.has(pull_request_id=pull_request_id))
        )

    def calculate_total_changes(self, db: Session, pull_request_id: int) -> int:
        return db.scalar(
            select(func.coalesce(func.sum(ChangedFile.changes), 0))
            .join(ChangedFile.commit)
            .where(ChangedFile.commit.has(pull_request_id=pull_request_id))
        )