from fastapi import APIRouter
from app.models.schemas import RevisionPlanRequest, RevisionPlanResponse
from app.services.plan_optimizer import plan_optimizer_service

router = APIRouter(prefix="/revision-plan", tags=["Revision Plan"])

@router.post("/generate", response_model=RevisionPlanResponse)
def generate_revision_plan(request: RevisionPlanRequest):
    return plan_optimizer_service.create_revision_plan(request)

@router.get("/current", response_model=RevisionPlanResponse)
def get_current_revision_plan():
    return plan_optimizer_service.create_revision_plan(RevisionPlanRequest(available_days=5, daily_hours=2.0))

