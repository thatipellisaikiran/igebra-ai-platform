from datetime import datetime
from typing import List, Dict
from app.models.schemas import AnalyticsResponse, AttemptHistoryPoint
from app.services.topic_mapper import topic_mapper_service


class AnalyticsService:
    """
    Tracks real student quiz attempts and mastery progression over time.
    Starts empty with zero dummy or seed attempt history.
    """

    def __init__(self):
        self.attempts: List[AttemptHistoryPoint] = []

    def clear(self):
        self.attempts = []

    def record_attempt(self, overall_score_pct: float, topic_scores: Dict[str, float]):
        point = AttemptHistoryPoint(
            attempt_index=len(self.attempts) + 1,
            timestamp=datetime.utcnow().isoformat() + "Z",
            overall_score_pct=overall_score_pct,
            topic_scores=topic_scores,
        )
        self.attempts.append(point)

    def get_progress(self, student_id: str = "usr_std_001") -> AnalyticsResponse:
        if len(self.attempts) >= 2:
            velocity = round(self.attempts[-1].overall_score_pct - self.attempts[0].overall_score_pct, 1)
        elif len(self.attempts) == 1:
            velocity = 0.0
        else:
            velocity = 0.0

        # Derive strongest topic & most critical gap from live topic map
        t_map = topic_mapper_service.get_topic_map()
        tested_subs = [
            sub
            for ch in t_map.topics
            for sub in ch.subtopics
            if sub.status in ("weak", "medium", "strong")
        ]

        if tested_subs:
            strongest = max(tested_subs, key=lambda s: s.current_mastery).title
            weakest = min(tested_subs, key=lambda s: s.current_mastery).title
        else:
            strongest = "No topics tested yet"
            weakest = "No topics tested yet"

        return AnalyticsResponse(
            student_id=student_id,
            attempts_history=self.attempts,
            learning_velocity_pct=velocity,
            strongest_topic=strongest,
            most_critical_gap=weakest,
        )


analytics_service = AnalyticsService()

