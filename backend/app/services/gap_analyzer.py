from datetime import datetime
from typing import List
from app.models.schemas import TopicGapItem, GapReportSummary, GapReportResponse
from app.services.topic_mapper import topic_mapper_service


class GapAnalyzerService:
    def generate_gap_report(self, student_id: str = "usr_std_001", student_name: str = "Demo Student") -> GapReportResponse:
        topic_map = topic_mapper_service.get_topic_map()

        weak_list: List[TopicGapItem] = []
        medium_list: List[TopicGapItem] = []
        strong_list: List[TopicGapItem] = []

        total_tested = 0
        sum_scores = 0.0

        for chapter in topic_map.topics:
            for sub in chapter.subtopics:
                if sub.status == "untested":
                    continue

                total_tested += 1
                sum_scores += sub.current_mastery

                stats = topic_mapper_service.topic_eval_stats.get(sub.id)
                accuracy_str = (
                    f"You answered {stats['correct']} of {stats['total']} diagnostic questions correctly."
                    if stats
                    else f"Current diagnostic mastery is {round(sub.current_mastery * 100)}%."
                )

                if sub.status == "weak":
                    reason = f"{accuracy_str} Past exam frequency: {sub.past_paper_occurrences} questions."
                    action = f"Review {chapter.chapter_title} in your uploaded notes and retake a targeted quiz."
                    weak_list.append(
                        TopicGapItem(
                            topic_id=sub.id,
                            title=sub.title,
                            mastery_score=sub.current_mastery,
                            status="weak",
                            badge="🔴 Weak",
                            diagnostic_reason=reason,
                            exam_frequency_weight=round(sub.past_paper_occurrences * 0.15, 2),
                            recommended_action=action,
                        )
                    )
                elif sub.status == "medium":
                    reason = f"{accuracy_str} Partial understanding — needs targeted consolidation."
                    action = "Review key mechanisms and formulas from your uploaded section notes."
                    medium_list.append(
                        TopicGapItem(
                            topic_id=sub.id,
                            title=sub.title,
                            mastery_score=sub.current_mastery,
                            status="medium",
                            badge="🟡 Medium",
                            diagnostic_reason=reason,
                            exam_frequency_weight=round(sub.past_paper_occurrences * 0.12, 2),
                            recommended_action=action,
                        )
                    )
                elif sub.status == "strong":
                    reason = f"{accuracy_str} Solid conceptual accuracy."
                    action = "Maintain mastery with brief periodic recall."
                    strong_list.append(
                        TopicGapItem(
                            topic_id=sub.id,
                            title=sub.title,
                            mastery_score=sub.current_mastery,
                            status="strong",
                            badge="🟢 Strong",
                            diagnostic_reason=reason,
                            exam_frequency_weight=round(sub.past_paper_occurrences * 0.10, 2),
                            recommended_action=action,
                        )
                    )

        overall_pct = round((sum_scores / total_tested) * 100, 1) if total_tested > 0 else 0.0

        summary = GapReportSummary(
            total_topics_analyzed=total_tested,
            weak_count=len(weak_list),
            medium_count=len(medium_list),
            strong_count=len(strong_list),
            overall_preparedness_pct=overall_pct,
        )

        return GapReportResponse(
            student_id=student_id,
            student_name=student_name,
            generated_at=datetime.utcnow().isoformat() + "Z",
            summary=summary,
            weak_topics=weak_list,
            medium_topics=medium_list,
            strong_topics=strong_list,
        )


gap_analyzer_service = GapAnalyzerService()
