from app.core.config import Settings
from app.github.client import GitHubClient

settings = Settings()


def main() -> None:
    with GitHubClient(
        base_url=settings.github_api_url,
        token=settings.github_token,
    ) as client:
        user = client.get_authenticated_user()
        print(user)


if __name__ == "__main__":
    main()