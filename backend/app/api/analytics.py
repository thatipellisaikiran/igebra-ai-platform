from fastapi import APIRouter
from app.models.schemas import AnalyticsResponse
from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["Student Analytics"])


@router.get("/progress", response_model=AnalyticsResponse)
def get_student_progress():
    return analytics_service.get_progress()
