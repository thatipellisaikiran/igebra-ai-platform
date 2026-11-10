import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.security import verify_credentials, create_access_token, DEMO_USERS
from app.models.schemas import (
    LoginRequest,
    UserResponse,
    CitationRef,
    TopicNode,
    SubtopicNode
)

class TestAuthAndModels(unittest.TestCase):
    def test_demo_credentials_student(self):
        user = verify_credentials("student@gapfinder.ai", "student123")
        self.assertIsNotNone(user)
        self.assertEqual(user["role"], "student")
        self.assertEqual(user["full_name"], "Aarav Sharma")

    def test_demo_credentials_teacher(self):
        user = verify_credentials("teacher@gapfinder.ai", "teacher123")
        self.assertIsNotNone(user)
        self.assertEqual(user["role"], "teacher")
        self.assertEqual(user["full_name"], "Dr. Meenakshi Sundaram")

    def test_invalid_credentials(self):
        user = verify_credentials("unknown@gapfinder.ai", "wrongpass")
        self.assertIsNone(user)

    def test_jwt_token_generation(self):
        token = create_access_token({"sub": "usr_std_001", "role": "student"})
        self.assertTrue(isinstance(token, str))
        self.assertGreater(len(token), 20)

    def test_schemas_validation(self):
        citation = CitationRef(
            document_name="notes.pdf",
            section="Section 1",
            page_or_anchor="Page 2"
        )
        self.assertEqual(citation.document_name, "notes.pdf")

        sub = SubtopicNode(
            id="sub_test",
            title="Photosystems",
            past_paper_occurrences=3,
            weightage_category="High",
            current_mastery=0.4,
            status="weak"
        )
        self.assertEqual(sub.id, "sub_test")
        self.assertEqual(sub.status, "weak")

if __name__ == '__main__':
    unittest.main()

