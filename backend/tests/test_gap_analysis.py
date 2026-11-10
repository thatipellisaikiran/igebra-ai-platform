import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.services.gap_analyzer import gap_analyzer_service
from app.services.topic_mapper import topic_mapper_service


class TestGapAnalysis(unittest.TestCase):
    def setUp(self):
        topic_mapper_service.clear()
        syllabus = (
            "# Biology\n"
            "### Chapter 1: Photosynthesis\n"
            "- Section 1.1: Light Reactions\n"
            "- Section 1.2: Photolysis\n"
            "- Section 1.3: Calvin Cycle\n"
        )
        topic_mapper_service.ingest_syllabus(syllabus, "syllabus.txt")
        subs = topic_mapper_service.get_topic_map().topics[0].subtopics
        topic_mapper_service.update_subtopic_mastery(subs[0].id, 0.25, 1, 4)
        topic_mapper_service.update_subtopic_mastery(subs[1].id, 0.60, 3, 5)
        topic_mapper_service.update_subtopic_mastery(subs[2].id, 0.90, 9, 10)

    def tearDown(self):
        topic_mapper_service.clear()

    def test_gap_report_structure(self):
        report = gap_analyzer_service.generate_gap_report(student_id="usr_test_01", student_name="Test Student")
        self.assertEqual(report.student_id, "usr_test_01")
        self.assertEqual(report.summary.weak_count, 1)
        self.assertEqual(report.summary.medium_count, 1)
        self.assertEqual(report.summary.strong_count, 1)

        self.assertIn("1 of 4", report.weak_topics[0].diagnostic_reason)
        self.assertIn("🔴", report.weak_topics[0].badge)
        self.assertIn("🟡", report.medium_topics[0].badge)
        self.assertIn("🟢", report.strong_topics[0].badge)


if __name__ == '__main__':
    unittest.main()
