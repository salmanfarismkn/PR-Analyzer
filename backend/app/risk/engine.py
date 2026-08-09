from app.analysis.schemas import PullRequestMetrics
from app.risk.schemas import PullRequestRisk, RiskFactor


class RiskEngine:
    """Deterministic and explainable PR risk calculation."""

    def calculate(
        self,
        pull_request_id: int,
        metrics: PullRequestMetrics,
    ) -> PullRequestRisk:

        factors: list[RiskFactor] = []

        change_size_score = self._change_size_score(metrics)

        if change_size_score > 0:
            factors.append(
                RiskFactor(
                    name="Change Size",
                    score=change_size_score,
                    reason=(
                        f"{metrics.total_changes} lines changed "
                        f"across {metrics.total_files} files."
                    ),
                )
            )

        test_score = self._test_coverage_score(metrics)

        if test_score > 0:
            factors.append(
                RiskFactor(
                    name="Test Coverage",
                    score=test_score,
                    reason=(
                        f"{metrics.source_files} source files changed "
                        f"but only {metrics.test_files} test files changed."
                    ),
                )
            )

        config_score = self._configuration_score(metrics)

        if config_score > 0:
            factors.append(
                RiskFactor(
                    name="Configuration Changes",
                    score=config_score,
                    reason=(
                        f"{metrics.config_files} configuration files "
                        "were modified."
                    ),
                )
            )

        deletion_score = self._deletion_score(metrics)

        if deletion_score > 0:
            factors.append(
                RiskFactor(
                    name="Deleted Files",
                    score=deletion_score,
                    reason=(
                        f"{metrics.deleted_files} files were deleted."
                    ),
                )
            )

        binary_score = self._binary_score(metrics)

        if binary_score > 0:
            factors.append(
                RiskFactor(
                    name="Binary Files",
                    score=binary_score,
                    reason=(
                        f"{metrics.binary_files} binary files "
                        "were modified."
                    ),
                )
            )

        score = min(
            sum(factor.score for factor in factors),
            100,
        )
        security_score = self._security_score(metrics)

        if security_score > 0:
            factors.append(
                RiskFactor(
                    name="Security-Sensitive Changes",
                    score=security_score,
                    reason=(
                        f"{metrics.security_sensitive_files} "
                        "security-sensitive files were modified."
                    ),
                )
            )
        dependency_score = self._dependency_score(metrics)

        if dependency_score > 0:
            factors.append(
                RiskFactor(
                    name="Dependency Changes",
                    score=dependency_score,
                    reason=(
                        f"{metrics.dependency_files} dependency files "
                        "were modified."
                    ),
                )
            )

        ci_score = self._ci_score(metrics)

        if ci_score > 0:
            factors.append(
                RiskFactor(
                    name="CI Failures",
                    score=ci_score,
                    reason=(
                        f"{metrics.failed_check_count} CI checks "
                        "failed."
                    ),
                )
            )

        large_file_score = self._large_file_score(metrics)

        if large_file_score > 0:
            factors.append(
                RiskFactor(
                    name="Large Individual Change",
                    score=large_file_score,
                    reason=(
                        f"The largest modified file contains "
                        f"{metrics.largest_file_changes} line changes."
                    ),
                )
            )
        review_score = self._review_score(metrics)

        if review_score > 0:
            factors.append(
                RiskFactor(
                    name="Review Coverage",
                    score=review_score,
                    reason=(
                        f"{metrics.review_count} reviews from "
                        f"{metrics.unique_reviewer_count} reviewers."
                    ),
                )
            )

        return PullRequestRisk(
            pull_request_id=pull_request_id,
            score=score,
            level=self._risk_level(score),
            factors=factors,
            metrics=metrics,
        )

    @staticmethod
    def _change_size_score(
        metrics: PullRequestMetrics,
    ) -> int:

        changes = metrics.total_changes
        files = metrics.total_files

        score = 0

        if changes > 100:
            score += 10

        if changes > 300:
            score += 10

        if changes > 700:
            score += 15

        if changes > 1500:
            score += 15

        if files > 10:
            score += 5

        if files > 25:
            score += 5

        return min(score, 50)

    @staticmethod
    def _test_coverage_score(
        metrics: PullRequestMetrics,
    ) -> int:

        if metrics.source_files == 0:
            return 0

        if metrics.test_files == 0:
            return 20

        ratio = metrics.test_files / metrics.source_files

        if ratio < 0.25:
            return 15

        if ratio < 0.5:
            return 8

        return 0

    @staticmethod
    def _configuration_score(
        metrics: PullRequestMetrics,
    ) -> int:

        if metrics.config_files >= 3:
            return 15

        if metrics.config_files > 0:
            return 8

        return 0

    @staticmethod
    def _deletion_score(
        metrics: PullRequestMetrics,
    ) -> int:

        if metrics.deleted_files >= 5:
            return 15

        if metrics.deleted_files > 0:
            return 8

        return 0

    @staticmethod
    def _binary_score(
        metrics: PullRequestMetrics,
    ) -> int:

        if metrics.binary_files >= 3:
            return 10

        if metrics.binary_files > 0:
            return 5

        return 0

    @staticmethod
    def _risk_level(score: int) -> str:

        if score >= 70:
            return "high"

        if score >= 40:
            return "medium"

        return "low"

    @staticmethod
    def _security_score(
        metrics: PullRequestMetrics,
    ) -> int:
        if metrics.security_sensitive_files >= 3:
            return 20

        if metrics.security_sensitive_files > 0:
            return 12

        return 0

    @staticmethod
    def _dependency_score(
        metrics: PullRequestMetrics,
    ) -> int:
        if metrics.dependency_files >= 2:
            return 12

        if metrics.dependency_files > 0:
            return 8

        return 0

    @staticmethod
    def _database_score(
        metrics: PullRequestMetrics,
    ) -> int:
        if metrics.database_files >= 3:
            return 15

        if metrics.database_files > 0:
            return 10

        return 0

    @staticmethod
    def _ci_score(
        metrics: PullRequestMetrics,
    ) -> int:

        if metrics.failed_check_count >= 3:
            return 20

        if metrics.failed_check_count > 0:
            return 12

        if metrics.pending_check_count > 0:
            return 5

        return 0

    @staticmethod
    def _large_file_score(
        metrics: PullRequestMetrics,
    ) -> int:
        changes = metrics.largest_file_changes

        if changes > 1000:
            return 15

        if changes > 500:
            return 10

        if changes > 250:
            return 5

        return 0

    @staticmethod
    def _review_score(
        metrics: PullRequestMetrics,
    ) -> int:

        if metrics.total_files == 0:
            return 0

        if metrics.total_changes >= 300:
            if metrics.unique_reviewer_count == 0:
                return 15

            if metrics.approved_review_count == 0:
                return 10

        if metrics.changes_requested_count > 0:
            return 8

        return 0