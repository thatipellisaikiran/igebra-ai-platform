import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.services.plan_optimizer import plan_optimizer_service
from app.services.topic_mapper import topic_mapper_service
from app.models.schemas import RevisionPlanRequest


class TestPlanOptimizer(unittest.TestCase):
    def setUp(self):
        topic_mapper_service.clear()
        syllabus = (
            "# Biology\n"
            "### Chapter 1: Plant Physiology\n"
            "- Section 1.1: Light Reactions\n"
            "- Section 1.2: Photolysis\n"
            "- Section 1.3: Calvin Cycle\n"
            "- Section 1.4: Glycolysis\n"
            "- Section 1.5: Krebs Cycle\n"
        )
        topic_mapper_service.ingest_syllabus(syllabus, "syllabus.txt")
        subs = topic_mapper_service.get_topic_map().topics[0].subtopics
        topic_mapper_service.update_subtopic_mastery(subs[0].id, 0.20, 1, 5)
        topic_mapper_service.update_subtopic_mastery(subs[2].id, 0.95, 9, 10)

    def tearDown(self):
        topic_mapper_service.clear()

    def test_plan_budget_allocation(self):
        req = RevisionPlanRequest(available_days=5, daily_hours=2.0)
        plan = plan_optimizer_service.create_revision_plan(req)

        self.assertEqual(plan.available_days, 5)
        self.assertEqual(plan.daily_hours, 2.0)
        self.assertEqual(plan.total_budget_hours, 10.0)
        self.assertEqual(len(plan.schedule), 5)
        # Weak topic must be scheduled on Day 1 ahead of strong topic
        self.assertEqual(plan.schedule[0].topic_title, "Section 1.1: Light Reactions")

    def test_plan_adapts_to_budget_changes(self):
        req1 = RevisionPlanRequest(available_days=2, daily_hours=1.5)
        plan1 = plan_optimizer_service.create_revision_plan(req1)
        self.assertEqual(plan1.total_budget_hours, 3.0)
        self.assertEqual(len(plan1.schedule), 2)

        req2 = RevisionPlanRequest(available_days=5, daily_hours=3.0)
        plan2 = plan_optimizer_service.create_revision_plan(req2)
        self.assertEqual(plan2.total_budget_hours, 15.0)
        self.assertEqual(len(plan2.schedule), 5)


if __name__ == '__main__':
    unittest.main()
