import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.services.rag_engine import rag_engine
from app.services.topic_mapper import topic_mapper_service
from app.services.quiz_service import quiz_service
from app.services.evaluator import evaluator_service
from app.services.analytics_service import analytics_service
from app.models.schemas import StudentAnswerItem


class TestQuizAndEvaluator(unittest.TestCase):
    def setUp(self):
        rag_engine.clear()
        topic_mapper_service.clear()
        quiz_service.clear()
        analytics_service.clear()

        notes = (
            "# Chapter 1: Photosynthesis\n"
            "### Section 1.3: Light Reactions\n"
            "In PS II, water photolysis supplies electrons to P680 and releases oxygen.\n\n"
            "### Section 1.6: Calvin Cycle\n"
            "To synthesize one glucose molecule, 6 turns of the Calvin cycle require 18 ATP and 12 NADPH.\n"
        )
        rag_engine.index_document("doc_1", "notes.txt", notes, "notes")
        topic_mapper_service.ensure_topics_from_notes(notes, "notes.txt")

    def tearDown(self):
        rag_engine.clear()
        topic_mapper_service.clear()
        quiz_service.clear()
        analytics_service.clear()

    def test_diagnostic_quiz_generation_from_uploaded_notes(self):
        quiz = quiz_service.get_diagnostic_quiz("qz_diag_01")
        self.assertEqual(quiz.quiz_id, "qz_diag_01")
        self.assertEqual(quiz.total_questions, 2)
        for q in quiz.questions:
            self.assertEqual(len(q.options), 4)
            self.assertEqual(q.citation.document_name, "notes.txt")

    def test_quiz_evaluation_perfect_score(self):
        quiz = quiz_service.get_diagnostic_quiz("qz_diag_01")
        responses = []
        for q in quiz.questions:
            raw_q = quiz_service.get_question_by_id(quiz.quiz_id, q.id)
            responses.append(StudentAnswerItem(question_id=q.id, selected_option_idx=raw_q["correct_option_idx"]))

        result = evaluator_service.evaluate_quiz("qz_diag_01", responses)
        self.assertEqual(result.score, result.total_questions)
        self.assertEqual(result.score_percentage, 100.0)
        self.assertEqual(len(analytics_service.attempts), 1)

    def test_quiz_evaluation_with_mistakes(self):
        quiz = quiz_service.get_diagnostic_quiz("qz_diag_01")
        responses = []
        for q in quiz.questions:
            raw_q = quiz_service.get_question_by_id(quiz.quiz_id, q.id)
            wrong_idx = (raw_q["correct_option_idx"] + 1) % len(raw_q["options"])
            responses.append(StudentAnswerItem(question_id=q.id, selected_option_idx=wrong_idx))

        result = evaluator_service.evaluate_quiz("qz_diag_01", responses)
        self.assertEqual(result.score, 0)
        self.assertEqual(result.score_percentage, 0.0)
        for ev in result.evaluations:
            self.assertFalse(ev.is_correct)
            self.assertTrue(len(ev.explanation) > 0)


if __name__ == '__main__':
    unittest.main()
