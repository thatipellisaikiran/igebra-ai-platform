from fastapi import APIRouter
from app.models.schemas import GapReportResponse
from app.services.gap_analyzer import gap_analyzer_service

router = APIRouter(prefix="/gap-report", tags=["Diagnostic Gap Report"])

@router.get("/current", response_model=GapReportResponse)
def get_current_gap_report():
    return gap_analyzer_service.generate_gap_report()

