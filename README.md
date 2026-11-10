# GapFinder AI 🎯
### *Find What the Student Doesn’t Know — Intelligent Diagnostic & Revision Engine*

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript%20%7C%20Tailwind-61dafb.svg)](https://react.dev/)
[![RAG](https://img.shields.io/badge/Architecture-Strict%20Retrieval--Augmented%20Generation-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

---

## 📌 Executive Summary

Most study tools and chatbots wait for a student to ask questions. However, **a student cannot ask about a gap they do not know they have**. Revising everything equally leads to wasted revision time on known topics while critical blind spots remain hidden until exam day.

**GapFinder AI** acts as an **academic diagnostician** ("a doctor for studying"):
1. **Ingests & Structures**: Parses uploaded syllabi, textbook notes, and past exam papers.
2. **Maps & Weights**: Constructs a hierarchical Topic Map cross-referenced with past exam frequencies.
3. **Diagnoses (Grounded Testing)**: Generates citation-backed diagnostic quizzes strictly rooted in the student's materials.
4. **Pinpoints Knowledge Gaps**: Classifies topics into **🔴 Weak**, **🟡 Medium**, and **🟢 Strong** with clear diagnostic evidence.
5. **Prescribes (Actionable Treatment Plan)**: Generates a prioritized revision plan customized to the student's available daily study hours.
6. **Grounds Explanations**: Features a strict "Explain This Topic" assistant that answers solely using source citations.
7. **Monitors & Adapts**: Dynamically recalculates the revision trajectory as the student re-tests and masters topics.

---

## 🔄 The Core Learning Loop

```mermaid
flowchart LR
    A[1. Upload Materials<br>Syllabus, Notes, Past Papers] --> B[2. Build Topic Map<br>& Exam Weightage]
    B --> C[3. Diagnostic Quiz<br>Grounded with Citations]
    C --> D[4. Answer Evaluation<br>& Gap Analysis]
    D --> E[5. Gap Report<br>🔴 Weak | 🟡 Med | 🟢 Strong]
    E --> F[6. Dynamic Revision Plan<br>Time-Budgeted & Prioritized]
    F --> G[7. Explain-This-Topic<br>Strict RAG Assistant]
    G --> H[8. Re-Test & Progress]
    H -->|Update Mastery| D
```

---

## 🚀 Key Features

| Feature | Description | Problem Statement Alignment |
| :--- | :--- | :--- |
| **Multi-Source Material Ingestion** | Upload syllabus, lecture notes, textbook chapters, and past papers (PDF, TXT, Markdown). | Ingestion & Structuring |
| **Hierarchical Topic Mapping** | Automatically extracts chapter-topic-subtopic hierarchies and correlates them with past exam frequency. | Topic Weightage Mapping |
| **Citation-Grounded Diagnostic Quiz** | Generates MCQs and conceptual questions referencing specific sections (e.g., `[Chapter 3, Section 2.1]`). | Hallucination-free Testing |
| **Automated Diagnostic Evaluation** | Evaluates student answers, explaining right vs. wrong with reference to source context. | Diagnostic Evaluation |
| **Topic Gap Report** | Categorizes topics into 🔴 Weak, 🟡 Medium, and 🟢 Strong with specific diagnostic rationale. | Core Diagnostic Output |
| **Dynamic Revision Plan** | Prioritizes topics based on gap severity and exam weightage fitted to user daily study hours. | Personalized Revision |
| **Explain-This-Topic Assistant** | Interactive Q&A strictly confined to uploaded material with visible citations. | Retrieval-First Chat |
| **Mastery & Progress Dashboard** | Visualizes historical progress, score trajectory across attempts, and mastery curves. | Class/Student Analytics |
| **Role-Based Demo Authentication** | Pre-configured student and teacher credentials for rapid evaluation. | Demo Ready |

---

## 🧠 AI & RAG Architecture: Separation of Retrieval vs. Generation

To eliminate hallucination and guarantee that the student is tested on their actual curriculum:

1. **Retrieval Boundary**:
   - The document parser breaks materials into semantically coherent chunks annotated with metadata (`document_type`, `chapter`, `section`, `page_number`).
   - Chunks are vectorized and stored in a dense vector store.
   - For any query or topic generation, hybrid search (dense semantic + sparse keyword) retrieves top-$k$ relevant passages.

2. **Generation Boundary**:
   - The LLM is strictly constrained by prompt contracts: *“Rely strictly on the provided context. If an answer or question cannot be formulated from the context, state that it is out of scope.”*
   - Every question and explanation output includes a citation envelope: `{ "citation": "Chapter 4, Page 42", "source_chunk_id": "..." }`.

---

## 📁 Repository Structure

```text
igebra-task/
├── README.md                      # High-level overview and run instructions
├── task.txt                       # Original Hackathon PS specification
├── docs/                          # In-depth architectural & API specifications
│   ├── ARCHITECTURE.md            # System architecture, data flow & diagrams
│   ├── API_SPECIFICATION.md       # Complete REST API documentation
│   ├── RAG_PIPELINE.md            # Chunking, vector search, citations & prompts
│   └── REVISION_ALGORITHM.md      # Topic scoring & time-budget allocation formula
├── backend/                       # FastAPI Python Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI entrypoint and middleware
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py          # App settings and environment variables
│   │   │   └── security.py        # Demo auth & JWT token handling
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py         # Pydantic models for DTOs and validation
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── rag_engine.py      # Vector index, chunking, and strict RAG
│   │   │   ├── topic_mapper.py    # Syllabus parsing & past-paper weightage
│   │   │   ├── quiz_service.py    # Grounded diagnostic quiz generator
│   │   │   ├── evaluator.py       # Answer grading with diagnostic rationale
│   │   │   ├── gap_analyzer.py    # Topic classification (Weak/Medium/Strong)
│   │   │   └── plan_optimizer.py  # Prioritized time-budget revision scheduler
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── auth.py            # Authentication & demo user endpoints
│   │       ├── materials.py       # Document upload and parsing
│   │       ├── topic_map.py       # Syllabus hierarchy & weightage
│   │       ├── quiz.py            # Diagnostic quiz generation & submission
│   │       ├── gap_report.py      # Diagnostic gap analysis
│   │       ├── revision_plan.py   # Personalized revision schedule
│   │       ├── explain.py         # Grounded topic explainer
│   │       └── analytics.py       # Progress and mastery tracking
│   ├── requirements.txt           # Python dependencies
│   └── .env.example               # Environment variables template
├── frontend/                      # React / TypeScript Application
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── App.tsx                # Main application component & routes
│   │   ├── types/
│   │   │   └── index.ts           # TypeScript interfaces matching backend models
│   │   ├── services/
│   │   │   └── api.ts             # API client services
│   │   ├── components/
│   │   │   ├── Navbar.tsx         # Navigation header with demo user switch
│   │   │   ├── UploadZone.tsx     # Drag-and-drop document upload
│   │   │   ├── TopicMapTree.tsx   # Interactive syllabus topic tree & weightage
│   │   │   ├── DiagnosticQuiz.tsx # Quiz view with citation badges & timer
│   │   │   ├── GapReportView.tsx  # Color-coded diagnosis (Weak/Med/Strong)
│   │   │   ├── RevisionPlan.tsx   # Schedule timeline with daily hour controls
│   │   │   ├── ExplainChat.tsx    # Grounded RAG conversational drawer
│   │   │   └── Dashboard.tsx      # Progress trends & mastery metrics
│   │   └── index.css              # Styling & theme definitions
└── sample_data/                   # Curated curriculum sample for testing
    ├── biology_syllabus.txt       # Sample syllabus (Cell Biology, Photosynthesis, Genetics)
    ├── chapter_photosynthesis.txt # Textbook chapter with section headings
    └── past_exam_papers.txt       # Past paper questions with marks
```

---

## ⚡ Quickstart Guide

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```
Backend API will be accessible at: `http://localhost:8000`  
Interactive Swagger docs: `http://localhost:8000/docs`

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend will be available at: `http://localhost:5173`

---

## 🔑 Demo Credentials

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Student** | `student@gapfinder.ai` | `student123` | Take diagnostic test, view gap report, follow revision plan |
| **Teacher / Evaluator** | `teacher@gapfinder.ai` | `teacher123` | Class-level analytics, topic struggle heatmaps, exam alignment |

---

## 🏆 Hackathon Evaluation Checklist

- [x] **Material Upload**: Syllabus, Notes, Past Exam Papers.
- [x] **Topic Map**: Visual hierarchy with past-paper exam weightage.
- [x] **Diagnostic Quiz**: Grounded generation with chapter/section citations.
- [x] **Gap Report**: Weak 🔴 / Medium 🟡 / Strong 🟢 categorization with evidence.
- [x] **Personalized Revision Plan**: Prioritized by gap score and exam importance within study time limit.
- [x] **Explain-This-Topic Assistant**: Strict RAG answering strictly from uploaded material.
- [x] **Progress Tracking**: Historical attempts and mastery progression.
- [x] **Demo Authentication**: Pre-seeded demo credentials.

