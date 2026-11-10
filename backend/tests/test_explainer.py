import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.services.rag_engine import rag_engine
from app.services.explainer import explainer_service
from app.models.schemas import ExplainRequest


class TestExplainer(unittest.TestCase):
    def setUp(self):
        rag_engine.clear()
        notes = (
            "# Chapter 1: Photosynthesis\n"
            "### Section 1.5: Cyclic and Non-Cyclic Photophosphorylation\n"
            "In stroma lamellae membranes lacking PS II and NADP reductase, cyclic photophosphorylation produces only ATP and no NADPH.\n"
        )
        rag_engine.index_document("doc_ch1", "chapter_photosynthesis.txt", notes, "notes")

    def tearDown(self):
        rag_engine.clear()

    def test_explain_in_syllabus_topic(self):
        req = ExplainRequest(
            topic_id="sub_01_04",
            query="cyclic photophosphorylation stroma lamellae ATP",
        )
        resp = explainer_service.explain_topic(req)
        self.assertTrue(resp.is_grounded_in_material)
        self.assertGreater(len(resp.citations), 0)
        self.assertIn("stroma lamellae", resp.explanation_markdown.lower())
        self.assertEqual(resp.citations[0].document_name, "chapter_photosynthesis.txt")

    def test_explain_out_of_syllabus_guardrail(self):
        req = ExplainRequest(
            topic_id="sub_external",
            query="Calculate the Schwarzschild radius of a Kerr metric black hole singularity.",
        )
        resp = explainer_service.explain_topic(req)
        self.assertFalse(resp.is_grounded_in_material)
        self.assertEqual(len(resp.citations), 0)
        self.assertIn("Out of Scope Notice", resp.explanation_markdown)


if __name__ == '__main__':
    unittest.main()
