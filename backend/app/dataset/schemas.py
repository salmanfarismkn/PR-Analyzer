from pydantic import BaseModel


class TrainingExample(BaseModel):
    pull_request_id: int

    additions: int
    deletions: int
    changed_files: int
    commit_count: int

    unique_authors: int
    review_count: int
    unique_reviewers: int
    approvals: int
    change_requests: int

    check_count: int
    successful_checks: int
    failed_checks: int
    pending_checks: int

    is_draft: bool
    age_hours: float

    label: str