from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session

from app.core.exceptions import RepositoryAlreadyExistsError
from app.db.session import get_db
from app.repository.schemas import (
    RepositoryCreate,
    RepositoryResponse,
)
from app.repository.service import RepositoryService

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)

# Instantiate the service once
repository_service = RepositoryService()


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
        return repository_service.create(db, payload)
    except RepositoryAlreadyExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[RepositoryResponse],
)
def list_repositories(db: Session = Depends(get_db)):
    return repository_service.list(db)
