import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.services.topic_mapper import TopicMapperService


class TestTopicMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = TopicMapperService()

    def test_starts_empty_without_seed_data(self):
        t_map = self.mapper.get_topic_map()
        self.assertEqual(t_map.total_chapters, 0)
        self.assertEqual(t_map.total_subtopics, 0)

    def test_ingest_syllabus_and_link_past_papers(self):
        syllabus = (
            "# Class 12 Biology\n"
            "### Chapter 1: Photosynthesis\n"
            "- Section 1.1: Chloroplast Structure\n"
            "- Section 1.2: Light Reaction and Z-Scheme\n"
        )
        self.mapper.ingest_syllabus(syllabus, "syllabus.txt")

        past_paper = (
            "Q1. [3 Marks] Explain Light Reaction and Z-Scheme.\n"
            "Mapped Topics: Section 1.2: Light Reaction and Z-Scheme\n"
        )
        self.mapper.link_past_papers(past_paper)

        t_map = self.mapper.get_topic_map()
        self.assertEqual(t_map.subject, "Class 12 Biology")
        self.assertEqual(t_map.total_chapters, 1)
        self.assertEqual(t_map.total_subtopics, 2)
        sub2 = t_map.topics[0].subtopics[1]
        self.assertEqual(sub2.past_paper_occurrences, 1)
        self.assertEqual(sub2.status, "untested")

    def test_update_subtopic_mastery(self):
        syllabus = (
            "# Biology\n"
            "### Chapter 1: Photosynthesis\n"
            "- Section 1.1: Chloroplast Structure\n"
        )
        self.mapper.ingest_syllabus(syllabus, "syllabus.txt")
        sub_id = self.mapper.get_topic_map().topics[0].subtopics[0].id

        self.mapper.update_subtopic_mastery(sub_id, 0.30, correct_count=1, total_count=3)
        sub = self.mapper.get_topic_map().topics[0].subtopics[0]
        self.assertEqual(sub.current_mastery, 0.30)
        self.assertEqual(sub.status, "weak")

        self.mapper.update_subtopic_mastery(sub_id, 0.90, correct_count=3, total_count=3)
        self.assertEqual(sub.current_mastery, 0.90)
        self.assertEqual(sub.status, "strong")


if __name__ == '__main__':
    unittest.main()
