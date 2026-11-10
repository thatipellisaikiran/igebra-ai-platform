from fastapi import APIRouter
from app.models.schemas import DiagnosticQuizResponse, QuizSubmissionRequest, QuizSubmissionResponse
from app.services.quiz_service import quiz_service
from app.services.evaluator import evaluator_service

router = APIRouter(prefix="/quiz", tags=["Diagnostic Quiz"])

@router.get("/diagnostic", response_model=DiagnosticQuizResponse)
def get_diagnostic_quiz(quiz_id: str = "qz_diag_01"):
    return quiz_service.get_diagnostic_quiz(quiz_id=quiz_id)

@router.post("/{quiz_id}/submit", response_model=QuizSubmissionResponse)
def submit_quiz(quiz_id: str, submission: QuizSubmissionRequest):
    return evaluator_service.evaluate_quiz(quiz_id=quiz_id, responses=submission.responses)

