from pydantic import BaseModel


class PullRequestMetrics(BaseModel):
    total_files: int

    source_files: int
    test_files: int
    documentation_files: int
    config_files: int
    binary_files: int

    renamed_files: int
    deleted_files: int

    security_sensitive_files: int
    dependency_files: int
    database_files: int
    ci_files: int

    largest_file_changes: int

    added_lines: int
    deleted_lines: int
    total_changes: int

    review_count: int
    approved_review_count: int
    changes_requested_count: int
    unique_reviewer_count: int

    check_count: int
    successful_check_count: int
    failed_check_count: int
    pending_check_count: int