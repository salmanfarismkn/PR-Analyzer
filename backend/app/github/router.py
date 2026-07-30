from fastapi import APIRouter

from app.github.schemas import GitHubUser
from app.github.service import GitHubService

router = APIRouter(
    prefix="/github",
    tags=["GitHub"],
)

service = GitHubService()


@router.get("/me")
def get_me():
    return {"status": "ok"}

def get_me() -> GitHubUser:
    return service.get_authenticated_user()