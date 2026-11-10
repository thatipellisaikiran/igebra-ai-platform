from fastapi import APIRouter
from app.models.schemas import ExplainRequest, ExplainResponse
from app.services.explainer import explainer_service

router = APIRouter(prefix="/explain", tags=["Explain-This-Topic Assistant"])

@router.post("", response_model=ExplainResponse)
def explain_topic(request: ExplainRequest):
    return explainer_service.explain_topic(request)

