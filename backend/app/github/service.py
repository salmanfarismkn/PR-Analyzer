from app.core.config import settings
from app.github.client import GitHubClient
from app.github.schemas import GitHubUser


class GitHubService:
    def __init__(self) -> None:
        self._client = GitHubClient(
            base_url=settings.github_api_url,
            token=settings.github_token,
        )

    def get_authenticated_user(self) -> GitHubUser:
        return self._client.get_authenticated_user()