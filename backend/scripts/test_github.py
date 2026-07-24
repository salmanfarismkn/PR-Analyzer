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

        repositories = client.list_repositories()
        print(f"Repositories: {len(repositories)}")

        for repository in repositories:
            print(repository.full_name)

        repositories = client.list_repositories()

        repository = repositories[0]

        print(repository.full_name)

        pull_requests = client.list_pull_requests(
            repository.owner.login,
            repository.name,
        )

        print(f"Total PRs: {len(pull_requests)}")

        for pr in pull_requests:
            print(
                pr.number,
                pr.title,
                pr.state,
            )

if __name__ == "__main__":
    main()
