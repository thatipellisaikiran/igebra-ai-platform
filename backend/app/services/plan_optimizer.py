from typing import List
from app.models.schemas import RevisionPlanResponse, RevisionScheduleItem, RevisionPlanRequest
from app.services.topic_mapper import topic_mapper_service


class PlanOptimizerService:
    def create_revision_plan(self, request: RevisionPlanRequest) -> RevisionPlanResponse:
        topic_map = topic_mapper_service.get_topic_map()
        total_budget_hours = request.available_days * request.daily_hours

        candidates = []
        for chapter in topic_map.topics:
            for sub in chapter.subtopics:
                if sub.status == "untested":
                    gap_score = 0.65
                    urgency = 0.8
                    tag = "⚪ Untested"
                elif sub.status == "weak":
                    gap_score = 1.0 - sub.current_mastery
                    urgency = 1.5
                    tag = "🔴 Weak"
                elif sub.status == "medium":
                    gap_score = 1.0 - sub.current_mastery
                    urgency = 1.0
                    tag = "🟡 Medium"
                else:
                    gap_score = 1.0 - sub.current_mastery
                    urgency = 0.2
                    tag = "🟢 Strong"

                exam_weight = min(1.0, sub.past_paper_occurrences / 6.0)
                tps = (0.50 * gap_score) + (0.35 * exam_weight) + (0.15 * urgency)
                candidates.append({
                    "subtopic": sub,
                    "chapter": chapter.chapter_title,
                    "tps": tps,
                    "tag": tag,
                })

        if not candidates:
            return RevisionPlanResponse(
                plan_id="plan_empty",
                available_days=request.available_days,
                daily_hours=request.daily_hours,
                total_budget_hours=total_budget_hours,
                schedule=[],
                summary_message="Upload your syllabus or study notes and take a diagnostic quiz to generate a personalized revision plan.",
            )

        candidates.sort(key=lambda x: x["tps"], reverse=True)

        schedule: List[RevisionScheduleItem] = []
        days_count = request.available_days
        hours_per_day = request.daily_hours
        top_candidates = candidates[:days_count]

        for i, item in enumerate(top_candidates):
            sub = item["subtopic"]
            day_num = i + 1

            actions = [
                f"Review source material in {item['chapter']}",
                f"Focus on key concepts and mechanisms in {sub.title}",
                "Take a follow-up diagnostic quiz to verify gap closure",
            ]

            schedule.append(
                RevisionScheduleItem(
                    day=day_num,
                    allocated_hours=hours_per_day,
                    priority_order=i + 1,
                    topic_id=sub.id,
                    topic_title=sub.title,
                    status_tag=item["tag"],
                    exam_weight_desc=f"{sub.weightage_category} ({sub.past_paper_occurrences} past exam questions)",
                    target_actions=actions,
                )
            )

        summary_msg = (
            f"Optimized {len(schedule)}-day revision schedule totaling "
            f"{len(schedule) * hours_per_day:.1f} study hours (from {total_budget_hours:.1f}h budget)."
        )

        return RevisionPlanResponse(
            plan_id="plan_active",
            available_days=days_count,
            daily_hours=hours_per_day,
            total_budget_hours=total_budget_hours,
            schedule=schedule,
            summary_message=summary_msg,
        )


plan_optimizer_service = PlanOptimizerService()
