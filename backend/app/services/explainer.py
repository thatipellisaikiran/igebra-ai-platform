from typing import List
from app.models.schemas import ExplainRequest, ExplainResponse, CitationRef
from app.services.rag_engine import rag_engine

class ExplainerService:
    def explain_topic(self, request: ExplainRequest) -> ExplainResponse:
        retrieved_chunks = rag_engine.retrieve(request.query, top_k=2)

        if not retrieved_chunks:
            return ExplainResponse(
                topic_id=request.topic_id,
                query=request.query,
                explanation_markdown=(
                    "⚠️ **Out of Scope Notice**: This question cannot be answered because the topic is "
                    "not found in your uploaded syllabus or textbook notes. GapFinder AI strictly confines "
                    "its answers to your uploaded materials to prevent exam distraction and hallucination."
                ),
                citations=[],
                is_grounded_in_material=False
            )

        citations: List[CitationRef] = []
        explanation_body = []

        for chunk in retrieved_chunks:
            citations.append(rag_engine.build_citation(chunk))
            explanation_body.append(
                f"**From {chunk.section} ({chunk.page_ref}):**\n\n{chunk.text}\n"
            )

        formatted_explanation = (
            f"### Grounded Diagnostic Explanation\n\n"
            f"Here is the verified explanation directly extracted from your uploaded study materials:\n\n"
            f"{''.join(explanation_body)}\n\n"
            f"> *Note: This explanation is guaranteed to be grounded in `{retrieved_chunks[0].doc_name}`.*"
        )

        return ExplainResponse(
            topic_id=request.topic_id,
            query=request.query,
            explanation_markdown=formatted_explanation,
            citations=citations,
            is_grounded_in_material=True
        )

explainer_service = ExplainerService()

