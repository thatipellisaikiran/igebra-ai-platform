import re
from typing import List, Optional
from app.models.schemas import CitationRef


class DocumentChunk:
    def __init__(
        self,
        chunk_id: str,
        doc_id: str,
        doc_name: str,
        doc_type: str,
        chapter: str,
        section: str,
        page_ref: str,
        text: str,
    ):
        self.chunk_id = chunk_id
        self.doc_id = doc_id
        self.doc_name = doc_name
        self.doc_type = doc_type
        self.chapter = chapter
        self.section = section
        self.page_ref = page_ref
        self.text = text
        self.tokens = self._tokenize(text)

    def _tokenize(self, text: str) -> set[str]:
        words = re.findall(r'\b[a-zA-Z0-9_\-]+\b', text.lower())
        return set(words)


class RAGEngine:
    """
    Guarded Retrieval-Augmented Generation Engine.
    Starts empty and deterministically indexes only user-uploaded documents
    with verifiable section and source citations.
    """

    def __init__(self):
        self.chunks: List[DocumentChunk] = []

    def clear(self):
        self.chunks = []

    def index_document(self, doc_id: str, doc_name: str, text: str, doc_type: str) -> int:
        """Parses and chunks uploaded document text into semantic citation-bearing chunks."""
        # Detect chapter title if present
        chapter_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
        chapter_title = chapter_match.group(1).strip() if chapter_match else doc_name

        # Split by section headings like "### Section 1.1: ..." or "## ..." or "### ..."
        sections = re.split(r'(^#{2,3}\s+[^\n]+)', text, flags=re.MULTILINE)
        created_count = 0

        if len(sections) > 1:
            for i in range(1, len(sections), 2):
                heading = sections[i].lstrip('#').strip()
                content = sections[i + 1].strip() if i + 1 < len(sections) else ""
                if content:
                    chunk_id = f"chk_{doc_id}_{created_count + 1}"
                    self.chunks.append(
                        DocumentChunk(
                            chunk_id=chunk_id,
                            doc_id=doc_id,
                            doc_name=doc_name,
                            doc_type=doc_type,
                            chapter=chapter_title,
                            section=heading,
                            page_ref=f"Section {created_count + 1}",
                            text=content[:1200],
                        )
                    )
                    created_count += 1
        else:
            # Fallback to paragraph chunking
            paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if len(p.strip()) > 30]
            if not paragraphs and text.strip():
                paragraphs = [text.strip()]
            for idx, p in enumerate(paragraphs):
                chunk_id = f"chk_{doc_id}_{idx + 1}"
                self.chunks.append(
                    DocumentChunk(
                        chunk_id=chunk_id,
                        doc_id=doc_id,
                        doc_name=doc_name,
                        doc_type=doc_type,
                        chapter=chapter_title,
                        section=f"Part {idx + 1}",
                        page_ref=f"Page {idx + 1}",
                        text=p[:1200],
                    )
                )
                created_count += 1

        return created_count

    def retrieve(self, query: str, top_k: int = 3, section_filter: Optional[str] = None) -> List[DocumentChunk]:
        """
        Retrieves top-k relevant chunks from uploaded materials using keyword overlap.
        """
        if not self.chunks:
            return []

        stopwords = {
            "a", "an", "the", "and", "or", "but", "if", "because", "as", "what", "which",
            "this", "that", "these", "those", "then", "just", "so", "than", "such",
            "is", "was", "are", "were", "be", "been", "being", "have", "has", "had",
            "do", "does", "did", "can", "could", "should", "would", "will", "shall",
            "in", "out", "on", "off", "over", "under", "again", "further", "once",
            "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
            "few", "more", "most", "other", "some", "no", "nor", "not", "only",
            "own", "same", "too", "very", "explain", "describe", "tell", "me", "about",
            "of", "at", "by", "for", "with", "into", "through", "during", "before", "after",
            "above", "below", "to", "from", "up", "down"
        }
        raw_words = re.findall(r'\b[a-zA-Z0-9_\-]+\b', query.lower())
        query_words = set(w for w in raw_words if w not in stopwords)

        if not query_words:
            query_words = set(raw_words)

        scores = []
        for chunk in self.chunks:
            if section_filter and section_filter.lower() not in chunk.section.lower():
                continue
            intersection = query_words.intersection(chunk.tokens)
            if not intersection:
                continue

            score = len(intersection) / max(1, len(query_words))
            section_tokens = set(re.findall(r'\b[a-zA-Z0-9_\-]+\b', chunk.section.lower()))
            if query_words.intersection(section_tokens):
                score += 0.5
            scores.append((score, chunk))

        scores.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scores[:top_k] if score >= 0.15]

    def build_citation(self, chunk: DocumentChunk) -> CitationRef:
        return CitationRef(
            document_name=chunk.doc_name,
            section=chunk.section,
            page_or_anchor=chunk.page_ref,
            verbatim_quote=chunk.text[:160] + ("..." if len(chunk.text) > 160 else ""),
        )


rag_engine = RAGEngine()
