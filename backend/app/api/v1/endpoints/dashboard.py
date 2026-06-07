from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.dashboard import DashboardOverview
from app.services.repositories.dashboard_repo import DashboardRepository

router = APIRouter()


@router.get("/projects/{project_id}", response_model=DashboardOverview)
def get_project_dashboard(project_id: int, db: Session = Depends(get_db)) -> DashboardOverview:
    try:
        return DashboardRepository(db).get_project_overview(project_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

