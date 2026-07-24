from __future__ import annotations
from urllib import response

import httpx
from app.github.schemas import GitHubPullRequest
from app.github.schemas import GitHubUser
from app.github.schemas import GitHubRepository

class GitHubClient:
    """Lightweight client for interacting with the GitHub REST API."""

    def __init__(
        self,
        *,
        base_url: str,
        token: str,
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

    def get_authenticated_user(self) -> GitHubUser:
        """Fetch the currently authenticated GitHub user."""

        response = self._client.get("/user")
        response.raise_for_status()

        return GitHubUser.model_validate(response.json())

    def close(self) -> None:
        """Close the underlying HTTP client."""

        self._client.close()

    def __enter__(self) -> "GitHubClient":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def list_repositories(self) -> list[GitHubRepository]:
        response = self._client.get(
            "/user/repos",
            params={
                "sort": "updated",
                "per_page": 100,
            },
        )
        response.raise_for_status()


        return [
            GitHubRepository.model_validate(repo)
            for repo in response.json()
        ]

    def list_pull_requests(
        self,
        owner: str,
        repository: str,
    ) -> list[GitHubPullRequest]:

        response = self._client.get(
            f"/repos/{owner}/{repository}/pulls",
            params={
                "state": "all",
                "per_page": 100,
            },
        )

        response.raise_for_status()

        return [
            GitHubPullRequest.model_validate(pr)
            for pr in response.json()
        ]