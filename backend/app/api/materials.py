from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import DocumentUploadResponse
from app.services.rag_engine import rag_engine
from app.services.topic_mapper import topic_mapper_service
from app.services.quiz_service import quiz_service
from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/materials", tags=["Study Materials"])

uploaded_documents_metadata: list[dict] = []


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_material(
    file: UploadFile = File(...),
    doc_type: str = Form("notes"),  # syllabus, notes, past_paper
):
    try:
        content_bytes = await file.read()
        text_content = content_bytes.decode("utf-8", errors="ignore")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    if not text_content.strip():
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    doc_id = f"doc_{len(uploaded_documents_metadata) + 1}"
    chunks_count = rag_engine.index_document(
        doc_id=doc_id,
        doc_name=file.filename or f"document_{doc_id}.txt",
        text=text_content,
        doc_type=doc_type,
    )

    if doc_type == "syllabus":
        topic_mapper_service.ingest_syllabus(text_content, file.filename or "syllabus")
    elif doc_type == "notes":
        topic_mapper_service.ensure_topics_from_notes(text_content, file.filename or "notes")
    elif doc_type == "past_paper":
        topic_mapper_service.link_past_papers(text_content)

    meta = {
        "id": doc_id,
        "filename": file.filename,
        "doc_type": doc_type,
        "chunks_created": chunks_count,
        "uploaded_at": datetime.utcnow().isoformat() + "Z",
    }
    uploaded_documents_metadata.append(meta)

    return DocumentUploadResponse(
        document_id=doc_id,
        filename=file.filename or "document",
        doc_type=doc_type,
        chunks_created=chunks_count,
        status="indexed",
        message="Document successfully processed and indexed into Guarded RAG corpus.",
    )


@router.get("")
def list_materials():
    return uploaded_documents_metadata


@router.delete("/reset")
def reset_workspace():
    """Clears all uploaded materials, topic map, quizzes, and attempt history."""
    uploaded_documents_metadata.clear()
    rag_engine.clear()
    topic_mapper_service.clear()
    quiz_service.clear()
    analytics_service.clear()
    return {"status": "cleared"}
