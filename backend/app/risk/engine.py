from collections import defaultdict

from app.analysis.schemas import PullRequestMetrics
from app.risk.rules import RISK_RULES, RISK_CATEGORIES
from app.risk.schemas import (
    PullRequestRisk,
    RiskCategory,
    RiskFactor,
)


class RiskEngine:
    """Evaluates deterministic, explainable PR risk rules."""

    def calculate(
        self,
        pull_request_id: int,
        metrics: PullRequestMetrics,
    ) -> PullRequestRisk:

        factors: list[RiskFactor] = []

        for rule in RISK_RULES:
            result = rule.evaluate(metrics)

            if result is None:
                continue

            score, reason = result

            score = min(
                score,
                rule.maximum_score,
            )

            severity = self._factor_severity(score)

            recommendation = self._recommendation(
                category=rule.category,
                name=rule.name,
            )

            factors.append(
                RiskFactor(
                    name=rule.name,
                    category=rule.category,
                    score=score,
                    severity=severity,
                    reason=reason,
                    recommendation=recommendation,
                )
            )

        categories = self._build_categories(factors)

        total_score = min(
            sum(
                category.score
                for category in categories
            ),
            100,
        )
        overall_recommendation = self._overall_recommendation(
            total_score,
        )

        return PullRequestRisk(
            pull_request_id=pull_request_id,
            score=total_score,
            level=self._risk_level(total_score),
            categories=categories,
            factors=factors,
            recommendation=overall_recommendation,
            metrics=metrics,
        )

    @staticmethod
    def _build_categories(
        factors: list[RiskFactor],
    ) -> list[RiskCategory]:

        category_scores: dict[str, int] = defaultdict(int)
        category_factors: dict[str, list[str]] = defaultdict(list)

        for factor in factors:
            category_scores[factor.category] += factor.score
            category_factors[factor.category].append(
                factor.name
            )

        return [
            RiskCategory(
                name=category,
                score=category_scores[category],
                factors=category_factors[category],
            )
            for category in RISK_CATEGORIES
        ]

    @staticmethod
    def _risk_level(score: int) -> str:

        if score >= 70:
            return "high"

        if score >= 40:
            return "medium"

        return "low"

    @staticmethod
    def _factor_severity(score: int) -> str:

        if score >= 15:
            return "high"

        if score >= 8:
            return "medium"

        return "low"

    @staticmethod
    def _recommendation(
        category: str,
        name: str,
    ) -> str:

        recommendations = {
            "Change Size": (
                "Consider splitting this PR into smaller, "
                "independently reviewable changes."
            ),

            "Large Individual File": (
                "Review the large file carefully for hidden "
                "complexity and consider splitting the change."
            ),

            "Security": (
                "Request a security-focused review before merging "
                "and verify authentication and authorization behavior."
            ),

            "Database": (
                "Review migration safety, backward compatibility, "
                "and rollback behavior before merging."
            ),

            "Dependencies": (
                "Review dependency versions, transitive dependencies, "
                "and known security vulnerabilities."
            ),

            "Testing": (
                "Add or update tests covering the modified source "
                "code before merging."
            ),

            "CI": (
                "Investigate failed or pending CI checks before merging."
            ),

            "Reviews": (
                "Obtain sufficient reviewer approval before merging "
                "this change."
            ),
        }

        return recommendations.get(
            name,
            "Review this change carefully before merging.",
        )

    @staticmethod
    def _overall_recommendation(score: int) -> str:

        if score >= 70:
            return (
                "High-risk PR. Require thorough review and "
                "verify CI before merging."
            )

        if score >= 40:
            return (
                "Moderate-risk PR. Review the identified risk "
                "factors carefully before merging."
            )

        return (
            "Low-risk PR. Standard review and CI validation "
            "should be sufficient."
        )