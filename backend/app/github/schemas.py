from pydantic import BaseModel
from datetime import datetime

from pydantic import BaseModel

class GitHubOwner(BaseModel):
    id: int
    login: str


class GitHubRepository(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    description: str | None
    default_branch: str
    owner: GitHubOwner

class GitHubUser(BaseModel):
    id: int
    login: str
    name: str | None
    avatar_url: str
    html_url: str
    public_repos: int

class RepositoryImportSummary(BaseModel):
    imported: int
    skipped: int
    total: int


class GitHubPullRequestUser(BaseModel):
    login: str


class GitHubPullRequestBranch(BaseModel):
    ref: str


class GitHubPullRequest(BaseModel):
    id: int
    number: int
    title: str
    state: str
    draft: bool

    user: GitHubPullRequestUser

    base: GitHubPullRequestBranch
    head: GitHubPullRequestBranch

    created_at: datetime
    updated_at: datetime