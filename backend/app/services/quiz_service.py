import re
import hashlib
from typing import List, Dict, Optional
from app.models.schemas import QuizQuestion, DiagnosticQuizResponse, CitationRef
from app.services.rag_engine import rag_engine, DocumentChunk
from app.services.topic_mapper import topic_mapper_service


class QuizService:
    """
    Dynamically generates citation-grounded diagnostic quizzes directly from
    uploaded study material chunks stored in the Guarded RAG engine.
    Contains zero hardcoded or seed questions.
    """

    def __init__(self):
        self._quiz_database: Dict[str, Dict] = {}

    def clear(self):
        self._quiz_database = {}

    def _extract_candidate_terms(self, chunks: List[DocumentChunk]) -> List[str]:
        """Collects domain-specific terms/numbers from uploaded chunks to serve as grounded distractors."""
        terms: List[str] = []
        seen = set()
        for ch in chunks:
            # Capitalized domain terms, chemical/bio identifiers, or numeric quantities
            matches = re.findall(
                r'\b(?:\d+\s*(?:ATP|NADPH|NADH|CO2|H2O|O2|nm|turns|molecules)|[A-Z][a-zA-Z0-9\+\-]{3,}(?:\s+[A-Z0-9][a-zA-Z0-9\+\-]+)?)\b',
                ch.text,
            )
            for m in matches:
                cleaned = m.strip()
                if cleaned.lower() not in seen and len(cleaned) >= 3:
                    seen.add(cleaned.lower())
                    terms.append(cleaned)
        return terms

    def _build_question_from_chunk(
        self,
        q_idx: int,
        chunk: DocumentChunk,
        corpus_terms: List[str],
    ) -> Optional[Dict]:
        """Synthesizes a diagnostic MCQ strictly from a single retrieved chunk."""
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', chunk.text) if len(s.strip()) > 35]
        if not sentences:
            return None

        selected_sentence = None
        target_term = None

        # Prefer sentences containing clear factual/quantitative/process terms
        for sent in sentences:
            term_matches = re.findall(
                r'\b(?:\d+\s*(?:ATP|NADPH|NADH|CO2|H2O|O2|nm)|PS\s*I+|P680|P700|RuBisCO|RuBP|NADP\+|NADPH|ATP|pyruvate|glycolysis|chlorophyll\s*a|stroma\s*lamellae|photolysis|Z-scheme|Calvin\s*cycle|Acetyl\s*CoA|Krebs\s*cycle|ubiquinone|oxygen)\b',
                sent,
                flags=re.IGNORECASE,
            )
            if term_matches:
                selected_sentence = sent
                target_term = term_matches[0].strip()
                break

        # Fallback: pick longest informative noun/concept in the first clear sentence
        if not selected_sentence:
            selected_sentence = sentences[0]
            words = [w for w in re.findall(r'\b[a-zA-Z]{6,}\b', selected_sentence)]
            if not words:
                return None
            target_term = max(words, key=len)

        # Build prompt by masking the target term in the grounded statement
        masked = re.sub(re.escape(target_term), "________", selected_sentence, count=1)
        question_text = f"Based on {chunk.section}, complete the statement accurately: \"{masked}\""

        # Select 3 grounded distractors from other terms in the uploaded corpus
        distractors = [t for t in corpus_terms if t.lower() != target_term.lower() and t.lower() not in target_term.lower()][:3]
        fallback_idx = 1
        while len(distractors) < 3:
            candidate = f"Unrelated process variant {fallback_idx}"
            if candidate not in distractors and candidate.lower() != target_term.lower():
                distractors.append(candidate)
            fallback_idx += 1

        # Deterministic rotation for correct option index based on chunk id
        digest = int(hashlib.md5(f"{chunk.chunk_id}_{q_idx}".encode()).hexdigest(), 16)
        correct_idx = digest % 4

        options = list(distractors[:3])
        options.insert(correct_idx, target_term)

        # Match to topic map subtopic
        matched_sub = topic_mapper_service.find_matching_subtopic(chunk.text, chunk.section)
        topic_id = matched_sub.id if matched_sub else f"sec_{q_idx}"
        topic_name = matched_sub.title if matched_sub else chunk.section

        citation = CitationRef(
            document_name=chunk.doc_name,
            section=chunk.section,
            page_or_anchor=chunk.page_ref,
            verbatim_quote=selected_sentence[:180],
        )

        return {
            "id": f"q_{q_idx:02d}",
            "topic_id": topic_id,
            "topic_name": topic_name,
            "question_text": question_text,
            "options": options,
            "correct_option_idx": correct_idx,
            "explanation": f"From {chunk.section} ({chunk.doc_name}): \"{selected_sentence}\"",
            "citation": citation,
        }

    def generate_diagnostic_quiz(self, quiz_id: str = "qz_diag_01", max_questions: int = 5) -> DiagnosticQuizResponse:
        # Prefer notes chunks, fall back to all uploaded chunks
        notes_chunks = [c for c in rag_engine.chunks if c.doc_type == "notes"]
        source_chunks = notes_chunks if notes_chunks else list(rag_engine.chunks)

        if not source_chunks:
            return DiagnosticQuizResponse(
                quiz_id=quiz_id,
                title="No Study Material Uploaded Yet",
                total_questions=0,
                estimated_minutes=0,
                questions=[],
            )

        corpus_terms = self._extract_candidate_terms(source_chunks)
        generated_questions: List[Dict] = []

        for idx, chunk in enumerate(source_chunks, start=1):
            if len(generated_questions) >= max_questions:
                break
            q_dict = self._build_question_from_chunk(len(generated_questions) + 1, chunk, corpus_terms)
            if q_dict:
                generated_questions.append(q_dict)

        self._quiz_database[quiz_id] = {
            "title": f"Diagnostic Assessment: {topic_mapper_service.subject}",
            "estimated_minutes": max(2, len(generated_questions) * 2),
            "questions": generated_questions,
        }

        quiz_questions = [
            QuizQuestion(
                id=q["id"],
                topic_id=q["topic_id"],
                topic_name=q["topic_name"],
                question_text=q["question_text"],
                options=q["options"],
                citation=q["citation"],
            )
            for q in generated_questions
        ]

        return DiagnosticQuizResponse(
            quiz_id=quiz_id,
            title=self._quiz_database[quiz_id]["title"],
            total_questions=len(quiz_questions),
            estimated_minutes=self._quiz_database[quiz_id]["estimated_minutes"],
            questions=quiz_questions,
        )

    def get_diagnostic_quiz(self, quiz_id: str = "qz_diag_01") -> DiagnosticQuizResponse:
        # Always generate fresh from currently indexed uploaded materials
        return self.generate_diagnostic_quiz(quiz_id=quiz_id)

    def get_question_by_id(self, quiz_id: str, question_id: str) -> Optional[Dict]:
        quiz_data = self._quiz_database.get(quiz_id)
        if not quiz_data:
            return None
        for q in quiz_data["questions"]:
            if q["id"] == question_id:
                return q
        return None


quiz_service = QuizService()
