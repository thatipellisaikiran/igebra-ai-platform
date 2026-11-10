export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'student' | 'teacher';
  grade?: string;
  department?: string;
  avatar?: string;
}

export interface CitationRef {
  document_name: string;
  section: string;
  page_or_anchor: string;
  verbatim_quote?: string;
}

export interface SubtopicNode {
  id: string;
  title: string;
  past_paper_occurrences: number;
  weightage_category: 'High' | 'Medium' | 'Low';
  current_mastery: number;
  status: 'weak' | 'medium' | 'strong' | 'untested';
}

export interface TopicNode {
  id: string;
  chapter_title: string;
  exam_frequency_count: number;
  exam_weightage_pct: number;
  subtopics: SubtopicNode[];
}

export interface TopicMapResponse {
  subject: string;
  total_chapters: number;
  total_subtopics: number;
  topics: TopicNode[];
}

export interface QuizQuestion {
  id: string;
  topic_id: string;
  topic_name: string;
  question_text: string;
  options: string[];
  citation: CitationRef;
}

export interface DiagnosticQuizResponse {
  quiz_id: string;
  title: string;
  total_questions: number;
  estimated_minutes: number;
  questions: QuizQuestion[];
}

export interface QuestionEvaluation {
  question_id: string;
  is_correct: boolean;
  user_answer: string;
  correct_answer: string;
  explanation: string;
  citation: CitationRef;
}

export interface QuizSubmissionResponse {
  quiz_id: string;
  total_questions: number;
  score: number;
  score_percentage: number;
  evaluations: QuestionEvaluation[];
}

export interface TopicGapItem {
  topic_id: string;
  title: string;
  mastery_score: number;
  status: 'weak' | 'medium' | 'strong';
  badge: string;
  diagnostic_reason: string;
  exam_frequency_weight: number;
  recommended_action: string;
}

export interface GapReportSummary {
  total_topics_analyzed: number;
  weak_count: number;
  medium_count: number;
  strong_count: number;
  overall_preparedness_pct: number;
}

export interface GapReportResponse {
  student_id: string;
  student_name: string;
  generated_at: string;
  summary: GapReportSummary;
  weak_topics: TopicGapItem[];
  medium_topics: TopicGapItem[];
  strong_topics: TopicGapItem[];
}

export interface RevisionScheduleItem {
  day: number;
  allocated_hours: number;
  priority_order: number;
  topic_id: string;
  topic_title: string;
  status_tag: string;
  exam_weight_desc: string;
  target_actions: string[];
}

export interface RevisionPlanResponse {
  plan_id: string;
  available_days: number;
  daily_hours: number;
  total_budget_hours: number;
  schedule: RevisionScheduleItem[];
  summary_message: string;
}

export interface ExplainResponse {
  topic_id: string;
  query: string;
  explanation_markdown: string;
  citations: CitationRef[];
  is_grounded_in_material: boolean;
}

