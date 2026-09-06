from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dataset.service import TrainingDatasetService


router = APIRouter(
    prefix="/dataset",
    tags=["dataset"],
)


@router.get("/training")
def get_training_dataset(
    db: Session = Depends(get_db),
):
    service = TrainingDatasetService()

    return {
        "count": len(
            service.build_dataset(db)
        ),
        "data": service.build_dataset(db),
    }