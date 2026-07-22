from pydantic import BaseModel


class GitHubUser(BaseModel):
    id: int
    login: str
    name: str | None
    avatar_url: str
    html_url: str
    public_repos: int