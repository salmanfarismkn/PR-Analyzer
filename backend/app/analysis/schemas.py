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

    added_lines: int

    deleted_lines: int

    total_changes: int