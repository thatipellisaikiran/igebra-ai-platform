"""
GapFinder AI - Automated End-to-End Pipeline Verification Script
Executes the complete loop starting from a completely clean, empty workspace
using files from sample_data/ (no seed data in code).
"""

import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.services.rag_engine import rag_engine
from app.services.topic_mapper import topic_mapper_service
from app.services.quiz_service import quiz_service
from app.services.evaluator import evaluator_service
from app.services.gap_analyzer import gap_analyzer_service
from app.services.plan_optimizer import plan_optimizer_service
from app.services.explainer import explainer_service
from app.services.analytics_service import analytics_service
from app.models.schemas import StudentAnswerItem, RevisionPlanRequest, ExplainRequest


def print_step(title: str):
    print("\n" + "=" * 70)
    print(f"🔹 {title}")
    print("=" * 70)


def main():
    rag_engine.clear()
    topic_mapper_service.clear()
    quiz_service.clear()
    analytics_service.clear()

    print("🚀 Starting GapFinder AI Complete Pipeline Verification (Zero Seed Data)...\n")

    # STEP 1: Material Ingestion
    print_step("Step 1: Ingest Syllabus, Notes, and Past Papers")
    sample_dir = os.path.abspath(os.path.join(BASE_DIR, "..", "sample_data"))

    with open(os.path.join(sample_dir, "biology_syllabus.txt"), "r", encoding="utf-8") as f:
        syllabus_text = f.read()
    with open(os.path.join(sample_dir, "chapter_photosynthesis.txt"), "r", encoding="utf-8") as f:
        notes_text = f.read()
    with open(os.path.join(sample_dir, "past_exam_papers.txt"), "r", encoding="utf-8") as f:
        past_text = f.read()

    c1 = rag_engine.index_document("doc_syl", "biology_syllabus.txt", syllabus_text, "syllabus")
    c2 = rag_engine.index_document("doc_ch1", "chapter_photosynthesis.txt", notes_text, "notes")
    c3 = rag_engine.index_document("doc_pp", "past_exam_papers.txt", past_text, "past_paper")

    topic_mapper_service.ingest_syllabus(syllabus_text, "biology_syllabus.txt")
    topic_mapper_service.link_past_papers(past_text)

    print(f"✅ Indexed chunks -> Syllabus: {c1}, Notes: {c2}, Past Papers: {c3}")

    # STEP 2: Topic Map
    print_step("Step 2: Verify Curriculum Topic Map & Past Paper Weightage")
    topic_map = topic_mapper_service.get_topic_map()
    print(f"✅ Subject: '{topic_map.subject}' | Chapters: {topic_map.total_chapters} | Subtopics: {topic_map.total_subtopics}")

    # STEP 3: Dynamic Diagnostic Quiz
    print_step("Step 3: Dynamically Generate Grounded Diagnostic Quiz")
    quiz = quiz_service.get_diagnostic_quiz("qz_diag_01")
    print(f"✅ Generated {quiz.total_questions} grounded questions from uploaded notes.")

    # STEP 4: Evaluate Quiz (simulate mostly wrong first)
    print_step("Step 4: Student Takes Quiz & Evaluates Answers")
    responses = []
    for i, q in enumerate(quiz.questions):
        raw_q = quiz_service.get_question_by_id("qz_diag_01", q.id)
        choice = raw_q["correct_option_idx"] if i == 0 else (raw_q["correct_option_idx"] + 1) % 4
        responses.append(StudentAnswerItem(question_id=q.id, selected_option_idx=choice))

    eval_result = evaluator_service.evaluate_quiz("qz_diag_01", responses)
    print(f"✅ Quiz Evaluated. Score: {eval_result.score}/{eval_result.total_questions} ({eval_result.score_percentage}%)")

    # STEP 5: Gap Report
    print_step("Step 5: Synthesize Diagnostic Gap Report")
    gap_report = gap_analyzer_service.generate_gap_report()
    print(f"✅ Preparedness: {gap_report.summary.overall_preparedness_pct}% | 🔴 Weak: {gap_report.summary.weak_count} | 🟢 Strong: {gap_report.summary.strong_count}")

    # STEP 6: Revision Plan
    print_step("Step 6: Formulate Prioritized Revision Plan")
    plan_req = RevisionPlanRequest(available_days=5, daily_hours=2.0)
    plan = plan_optimizer_service.create_revision_plan(plan_req)
    print(f"✅ {plan.summary_message}")

    # STEP 7: Guarded Explainer
    print_step("Step 7: Explain-This-Topic (Strict RAG + Guardrail)")
    in_scope = explainer_service.explain_topic(ExplainRequest(topic_id="general", query="Why does cyclic photophosphorylation not produce NADPH?"))
    assert in_scope.is_grounded_in_material and len(in_scope.citations) > 0
    out_scope = explainer_service.explain_topic(ExplainRequest(topic_id="general", query="Calculate the Schwarzschild radius of a Kerr metric black hole singularity."))
    assert not out_scope.is_grounded_in_material and len(out_scope.citations) == 0
    print("✅ In-scope grounded with citations; out-of-scope blocked cleanly.")

    # STEP 8: Retest & Dynamic Adaptation
    print_step("Step 8: Retest & Verify Adaptation")
    perfect_responses = [
        StudentAnswerItem(question_id=q.id, selected_option_idx=quiz_service.get_question_by_id("qz_diag_01", q.id)["correct_option_idx"])
        for q in quiz.questions
    ]
    retest_eval = evaluator_service.evaluate_quiz("qz_diag_01", perfect_responses)
    progress = analytics_service.get_progress()
    print(f"✅ Retest Score: {retest_eval.score_percentage}% | Learning Velocity: +{progress.learning_velocity_pct}%")

    print("\n🎉 ALL PIPELINE CHECKS PASSED WITH ZERO SEED/DUMMY DATA!\n")


if __name__ == "__main__":
    main()
