from __future__ import annotations

import httpx


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

    def get_authenticated_user(self) -> dict:
        """Fetch the currently authenticated GitHub user."""

        response = self._client.get("/user")
        response.raise_for_status()

        return response.json()

    def close(self) -> None:
        """Close the underlying HTTP client."""

        self._client.close()

    def __enter__(self) -> "GitHubClient":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()