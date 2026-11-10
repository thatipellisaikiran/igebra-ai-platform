from typing import List, Dict
from app.models.schemas import StudentAnswerItem, QuestionEvaluation, QuizSubmissionResponse
from app.services.quiz_service import quiz_service
from app.services.topic_mapper import topic_mapper_service
from app.services.analytics_service import analytics_service


class EvaluatorService:
    def evaluate_quiz(self, quiz_id: str, responses: List[StudentAnswerItem]) -> QuizSubmissionResponse:
        evaluations: List[QuestionEvaluation] = []
        correct_count = 0
        total_questions = len(responses)

        topic_stats: Dict[str, Dict] = {}

        for resp in responses:
            q_data = quiz_service.get_question_by_id(quiz_id, resp.question_id)
            if not q_data:
                continue

            topic_id = q_data["topic_id"]
            topic_name = q_data["topic_name"]
            if topic_id not in topic_stats:
                topic_stats[topic_id] = {"name": topic_name, "correct": 0, "total": 0}
            topic_stats[topic_id]["total"] += 1

            is_correct = (resp.selected_option_idx == q_data["correct_option_idx"])
            user_ans_text = (
                q_data["options"][resp.selected_option_idx]
                if 0 <= resp.selected_option_idx < len(q_data["options"])
                else "None"
            )
            correct_ans_text = q_data["options"][q_data["correct_option_idx"]]

            if is_correct:
                correct_count += 1
                topic_stats[topic_id]["correct"] += 1

            evaluations.append(
                QuestionEvaluation(
                    question_id=resp.question_id,
                    is_correct=is_correct,
                    user_answer=user_ans_text,
                    correct_answer=correct_ans_text,
                    explanation=q_data["explanation"],
                    citation=q_data["citation"],
                )
            )

        topic_scores_pct: Dict[str, float] = {}
        # Update topic mastery scores dynamically
        for tid, stats in topic_stats.items():
            score = stats["correct"] / max(1, stats["total"])
            topic_mapper_service.update_subtopic_mastery(
                tid,
                score,
                correct_count=stats["correct"],
                total_count=stats["total"],
            )
            topic_scores_pct[stats["name"]] = round(score * 100, 1)

        pct = round((correct_count / max(1, total_questions)) * 100, 1) if total_questions > 0 else 0.0

        if evaluations:
            analytics_service.record_attempt(overall_score_pct=pct, topic_scores=topic_scores_pct)

        return QuizSubmissionResponse(
            quiz_id=quiz_id,
            total_questions=total_questions,
            score=correct_count,
            score_percentage=pct,
            evaluations=evaluations,
        )


evaluator_service = EvaluatorService()
