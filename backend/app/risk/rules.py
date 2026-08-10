from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from app.analysis.schemas import PullRequestMetrics
from app.risk.thresholds import (
    CHANGE_SIZE_LARGE,
    CHANGE_SIZE_MASSIVE,
    CHANGE_SIZE_MEDIUM,
    CHANGE_SIZE_VERY_LARGE,
    CI_FAILURES_HIGH,
    CI_FAILURES_MEDIUM,
    DATABASE_FILES_HIGH,
    DATABASE_FILES_MEDIUM,
    DEPENDENCY_FILES_HIGH,
    DEPENDENCY_FILES_MEDIUM,
    LARGE_FILE_LARGE,
    LARGE_FILE_MEDIUM,
    LARGE_FILE_VERY_LARGE,
    SECURITY_FILES_HIGH,
    SECURITY_FILES_MEDIUM,
    TEST_RATIO_LOW,
    TEST_RATIO_MEDIUM,
)

@dataclass(frozen=True)
class RiskRule:
    name: str
    category: str
    evaluate: Callable[
        [PullRequestMetrics],
        tuple[int, str] | None,
    ]
    maximum_score: int

def change_size_rule(
    metrics: PullRequestMetrics,
) -> tuple[int, str] | None:

    changes = metrics.total_changes

    if changes >= CHANGE_SIZE_MASSIVE:
        return (
            40,
            f"{changes} lines changed; extremely large PR.",
        )

    if changes >= CHANGE_SIZE_VERY_LARGE:
        return (
            30,
            f"{changes} lines changed; very large PR.",
        )

    if changes >= CHANGE_SIZE_LARGE:
        return (
            20,
            f"{changes} lines changed; large PR.",
        )

    if changes >= CHANGE_SIZE_MEDIUM:
        return (
            10,
            f"{changes} lines changed.",
        )

    return None

def large_file_rule(
    metrics: PullRequestMetrics,
) -> tuple[int, str] | None:

    changes = metrics.largest_file_changes

    if changes >= LARGE_FILE_VERY_LARGE:
        return (
            15,
            f"Largest file contains {changes} line changes.",
        )

    if changes >= LARGE_FILE_LARGE:
        return (
            10,
            f"Largest file contains {changes} line changes.",
        )

    if changes >= LARGE_FILE_MEDIUM:
        return (
            5,
            f"Largest file contains {changes} line changes.",
        )

    return None

def security_rule(
    metrics: PullRequestMetrics,
) -> tuple[int, str] | None:

    count = metrics.security_sensitive_files

    if count >= SECURITY_FILES_HIGH:
        return (
            20,
            f"{count} security-sensitive files modified.",
        )

    if count >= SECURITY_FILES_MEDIUM:
        return (
            12,
            f"{count} security-sensitive file modified.",
        )

    return None

def database_rule(
    metrics: PullRequestMetrics,
) -> tuple[int, str] | None:

    count = metrics.database_files

    if count >= DATABASE_FILES_HIGH:
        return (
            15,
            f"{count} database-related files modified.",
        )

    if count >= DATABASE_FILES_MEDIUM:
        return (
            10,
            f"{count} database-related file modified.",
        )

    return None

def dependency_rule(
    metrics: PullRequestMetrics,
) -> tuple[int, str] | None:

    count = metrics.dependency_files

    if count >= DEPENDENCY_FILES_HIGH:
        return (
            12,
            f"{count} dependency files modified.",
        )

    if count >= DEPENDENCY_FILES_MEDIUM:
        return (
            8,
            f"{count} dependency file modified.",
        )

    return None

def ci_rule(
    metrics: PullRequestMetrics,
) -> tuple[int, str] | None:

    failures = metrics.failed_check_count

    if failures >= CI_FAILURES_HIGH:
        return (
            20,
            f"{failures} CI checks failed.",
        )

    if failures >= CI_FAILURES_MEDIUM:
        return (
            12,
            f"{failures} CI check failed.",
        )

    if metrics.pending_check_count > 0:
        return (
            5,
            f"{metrics.pending_check_count} CI checks are still pending.",
        )

    return None

def test_coverage_rule(
    metrics: PullRequestMetrics,
) -> tuple[int, str] | None:

    if metrics.source_files == 0:
        return None

    ratio = metrics.test_files / metrics.source_files

    if metrics.test_files == 0:
        return (
            20,
            "Source files changed without any test files.",
        )

    if ratio < TEST_RATIO_LOW:
        return (
            15,
            "Very few test files changed relative to source files.",
        )

    if ratio < TEST_RATIO_MEDIUM:
        return (
            8,
            "Test changes are low relative to source changes.",
        )

    return None

def review_rule(
    metrics: PullRequestMetrics,
) -> tuple[int, str] | None:

    if metrics.total_changes >= CHANGE_SIZE_LARGE:

        if metrics.unique_reviewer_count == 0:
            return (
                15,
                "Large PR has no reviewers.",
            )

        if metrics.approved_review_count == 0:
            return (
                10,
                "Large PR has no approved reviews.",
            )

    if metrics.changes_requested_count > 0:
        return (
            8,
            f"{metrics.changes_requested_count} review(s) requested changes.",
        )

    return None

RISK_RULES: tuple[RiskRule, ...] = (
    RiskRule(
        name="Change Size",
        category="code",
        evaluate=change_size_rule,
        maximum_score=40,
    ),
    RiskRule(
        name="Large Individual File",
        category="code",
        evaluate=large_file_rule,
        maximum_score=15,
    ),
    RiskRule(
        name="Security",
        category="security",
        evaluate=security_rule,
        maximum_score=20,
    ),
    RiskRule(
        name="Database",
        category="infrastructure",
        evaluate=database_rule,
        maximum_score=15,
    ),
    RiskRule(
        name="Dependencies",
        category="dependencies",
        evaluate=dependency_rule,
        maximum_score=12,
    ),
    RiskRule(
        name="Testing",
        category="testing",
        evaluate=test_coverage_rule,
        maximum_score=20,
    ),
    RiskRule(
        name="CI",
        category="ci",
        evaluate=ci_rule,
        maximum_score=20,
    ),
    RiskRule(
        name="Reviews",
        category="review",
        evaluate=review_rule,
        maximum_score=15,
    ),
)

RISK_CATEGORIES = (
    "code",
    "security",
    "testing",
    "dependencies",
    "infrastructure",
    "ci",
    "review",
)