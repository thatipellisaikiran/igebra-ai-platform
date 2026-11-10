from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Authentication
class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    grade: Optional[str] = None
    department: Optional[str] = None
    avatar: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class DemoAccountInfo(BaseModel):
    id: str
    email: str
    role: str
    label: str
    password: str
    description: str

# Documents & Chunks
class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    doc_type: str
    chunks_created: int
    status: str
    message: str

class CitationRef(BaseModel):
    document_name: str
    section: str
    page_or_anchor: str
    verbatim_quote: Optional[str] = None

# Topic Map
class SubtopicNode(BaseModel):
    id: str
    title: str
    past_paper_occurrences: int = 0
    weightage_category: str = "Medium" # High, Medium, Low
    current_mastery: float = 0.50
    status: str = "untested" # weak, medium, strong, untested

class TopicNode(BaseModel):
    id: str
    chapter_title: str
    exam_frequency_count: int
    exam_weightage_pct: float
    subtopics: List[SubtopicNode]

class TopicMapResponse(BaseModel):
    subject: str
    total_chapters: int
    total_subtopics: int
    topics: List[TopicNode]

# Diagnostic Quiz
class QuizQuestion(BaseModel):
    id: str
    topic_id: str
    topic_name: str
    question_text: str
    options: List[str]
    citation: CitationRef

class DiagnosticQuizResponse(BaseModel):
    quiz_id: str
    title: str
    total_questions: int
    estimated_minutes: int
    questions: List[QuizQuestion]

class StudentAnswerItem(BaseModel):
    question_id: str
    selected_option_idx: int

class QuizSubmissionRequest(BaseModel):
    responses: List[StudentAnswerItem]

class QuestionEvaluation(BaseModel):
    question_id: str
    is_correct: bool
    user_answer: str
    correct_answer: str
    explanation: str
    citation: CitationRef

class QuizSubmissionResponse(BaseModel):
    quiz_id: str
    total_questions: int
    score: int
    score_percentage: float
    evaluations: List[QuestionEvaluation]

# Gap Report
class TopicGapItem(BaseModel):
    topic_id: str
    title: str
    mastery_score: float # 0.0 to 1.0
    status: str # weak, medium, strong
    badge: str # 🔴 Weak, 🟡 Medium, 🟢 Strong
    diagnostic_reason: str
    exam_frequency_weight: float
    recommended_action: str

class GapReportSummary(BaseModel):
    total_topics_analyzed: int
    weak_count: int
    medium_count: int
    strong_count: int
    overall_preparedness_pct: float

class GapReportResponse(BaseModel):
    student_id: str
    student_name: str
    generated_at: str
    summary: GapReportSummary
    weak_topics: List[TopicGapItem]
    medium_topics: List[TopicGapItem]
    strong_topics: List[TopicGapItem]

# Revision Plan
class RevisionPlanRequest(BaseModel):
    available_days: int = Field(default=5, ge=1, le=60)
    daily_hours: float = Field(default=2.0, ge=0.5, le=12.0)

class RevisionScheduleItem(BaseModel):
    day: int
    allocated_hours: float
    priority_order: int
    topic_id: str
    topic_title: str
    status_tag: str
    exam_weight_desc: str
    target_actions: List[str]

class RevisionPlanResponse(BaseModel):
    plan_id: str
    available_days: int
    daily_hours: float
    total_budget_hours: float
    schedule: List[RevisionScheduleItem]
    summary_message: str

# Explain This Topic
class ExplainRequest(BaseModel):
    topic_id: str
    query: str

class ExplainResponse(BaseModel):
    topic_id: str
    query: str
    explanation_markdown: str
    citations: List[CitationRef]
    is_grounded_in_material: bool

# Analytics
class AttemptHistoryPoint(BaseModel):
    attempt_index: int
    timestamp: str
    overall_score_pct: float
    topic_scores: Dict[str, float]

class AnalyticsResponse(BaseModel):
    student_id: str
    attempts_history: List[AttemptHistoryPoint]
    learning_velocity_pct: float
    strongest_topic: str
    most_critical_gap: str

