from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from app.core.exceptions import RepositoryAlreadyExistsError
from app.db.session import get_db
from app.repository.schemas import (
    RepositoryCreate,
    RepositoryResponse,
)
from app.repository.service import (
    create_repository,
    list_repositories,
)

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=HTTPStatus.CREATED,
)
def create(
    payload: RepositoryCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_repository(db, payload)
    except RepositoryAlreadyExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[RepositoryResponse],
)
def list_all(
    db: Session = Depends(get_db),
):
    return list_repositories(db)