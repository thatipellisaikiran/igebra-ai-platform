import unittest
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.services.rag_engine import RAGEngine


class TestRAGEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RAGEngine()

    def test_starts_empty_without_seed_data(self):
        self.assertEqual(len(self.engine.chunks), 0, "RAG corpus must start empty with no seed data")

    def test_document_indexing(self):
        sample_text = (
            "### Section 2.1: Glycolysis\n"
            "Glycolysis occurs in cytoplasm. 2 ATP net yield.\n\n"
            "### Section 2.2: Fermentation\n"
            "Anaerobic breakdown of pyruvate into ethanol or lactate."
        )
        count = self.engine.index_document("doc_test_01", "test_notes.txt", sample_text, "notes")
        self.assertEqual(count, 2, "Should index 2 sections")

    def test_retrieval_and_citations(self):
        sample_text = (
            "### Section 1.3: Z-Scheme\n"
            "In PS II, excited electrons pass down an electron transport chain to PS I and reduce NADP+."
        )
        self.engine.index_document("doc_test_02", "notes.txt", sample_text, "notes")
        results = self.engine.retrieve("Z-scheme electron transport", top_k=2)
        self.assertGreater(len(results), 0, "Should retrieve relevant chunks for Z-scheme")
        top_chunk = results[0]
        citation = self.engine.build_citation(top_chunk)
        self.assertEqual(citation.document_name, "notes.txt")
        self.assertEqual(citation.section, "Section 1.3: Z-Scheme")


if __name__ == '__main__':
    unittest.main()
