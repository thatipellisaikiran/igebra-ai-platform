# API Specification: GapFinder AI REST Interface

This document specifies the RESTful endpoints for the GapFinder AI backend built with FastAPI. All endpoints return and receive JSON payloads.

Base URL: `http://localhost:8000/api`

---

## 1. Authentication Endpoints (`/api/auth`)

### 1.1 Login (Token Generation)
- **POST** `/auth/login`
- **Description**: Authenticate student or teacher credentials and receive a JWT token.
- **Request Body**:
```json
{
  "email": "student@gapfinder.ai",
  "password": "student123"
}
```
- **Response** (`200 OK`):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "usr_std_001",
    "email": "student@gapfinder.ai",
    "full_name": "Demo Student",
    "role": "student"
  }
}
```

### 1.2 Demo Accounts Switcher
- **GET** `/auth/demo-accounts`
- **Description**: List available pre-configured demo personas for hackathon judges and evaluators.
- **Response** (`200 OK`):
```json
[
  {
    "id": "usr_std_001",
    "email": "student@gapfinder.ai",
    "role": "student",
    "label": "Demo Student (Biology Class 12)",
    "password": "student123"
  },
  {
    "id": "usr_tch_001",
    "email": "teacher@gapfinder.ai",
    "role": "teacher",
    "label": "Demo Teacher (Department Lead)",
    "password": "teacher123"
  }
]
```

---

## 2. Material Upload & Ingestion (`/api/materials`)

### 2.1 Upload Study Document
- **POST** `/materials/upload`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: File binary (PDF, TXT, MD)
  - `doc_type`: Enum string (`syllabus` | `notes` | `past_paper`)
  - `subject`: String (e.g., `Biology`)
- **Response** (`201 Created`):
```json
{
  "document_id": "doc_bio_ch3",
  "filename": "chapter_photosynthesis.pdf",
  "doc_type": "notes",
  "chunks_created": 24,
  "status": "indexed",
  "message": "Successfully parsed and vectorized document."
}
```

### 2.2 List Ingested Materials
- **GET** `/materials`
- **Response** (`200 OK`):
```json
[
  {
    "id": "doc_syl_01",
    "filename": "biology_syllabus.txt",
    "doc_type": "syllabus",
    "topics_extracted": 12,
    "uploaded_at": "2026-11-09T10:00:00Z"
  },
  {
    "id": "doc_bio_ch3",
    "filename": "chapter_photosynthesis.pdf",
    "doc_type": "notes",
    "chunks_created": 24,
    "uploaded_at": "2026-11-09T10:05:00Z"
  }
]
```

---

## 3. Topic Map & Exam Weightage (`/api/topic-map`)

### 3.1 Get Topic Hierarchy & Weightage
- **GET** `/topic-map`
- **Response** (`200 OK`):
```json
{
  "subject": "Biology",
  "topics": [
    {
      "id": "top_01",
      "title": "Photosynthesis in Higher Plants",
      "exam_frequency_count": 8,
      "exam_weightage_pct": 28.5,
      "subtopics": [
        {
          "id": "sub_01_01",
          "title": "Light-dependent Reactions (Z-Scheme & Photophosphorylation)",
          "past_paper_occurrences": 5,
          "weightage": "High",
          "current_mastery": 0.35,
          "status": "weak"
        },
        {
          "id": "sub_01_02",
          "title": "Calvin Cycle (C3 and C4 Pathways)",
          "past_paper_occurrences": 3,
          "weightage": "Medium",
          "current_mastery": 0.80,
          "status": "strong"
        }
      ]
    }
  ]
}
```

---

## 4. Grounded Diagnostic Quiz (`/api/quiz`)

### 4.1 Generate Diagnostic Quiz
- **POST** `/quiz/generate`
- **Request Body**:
```json
{
  "topic_ids": ["top_01"],
  "question_count": 5,
  "difficulty": "adaptive"
}
```
- **Response** (`200 OK`):
```json
{
  "quiz_id": "qz_8921b",
  "created_at": "2026-11-09T10:15:00Z",
  "questions": [
    {
      "id": "q_01",
      "topic_id": "sub_01_01",
      "topic_name": "Light Reactions (Photophosphorylation)",
      "question": "What is the primary electron donor for Photosystem II during non-cyclic photophosphorylation?",
      "options": [
        "Plastoquinone",
        "Water (H2O)",
        "Ferredoxin",
        "NADPH"
      ],
      "citation": {
        "document": "chapter_photosynthesis.pdf",
        "section": "Section 3.2 - Splitting of Water",
        "page_reference": "Page 14"
      }
    }
  ]
}
```

### 4.2 Submit Quiz & Evaluate
- **POST** `/quiz/{quiz_id}/submit`
- **Request Body**:
```json
{
  "responses": [
    {
      "question_id": "q_01",
      "selected_option_idx": 0
    }
  ]
}
```
- **Response** (`200 OK`):
```json
{
  "quiz_id": "qz_8921b",
  "total_questions": 5,
  "score": 2,
  "score_percentage": 40.0,
  "evaluations": [
    {
      "question_id": "q_01",
      "is_correct": false,
      "user_answer": "Plastoquinone",
      "correct_answer": "Water (H2O)",
      "explanation": "Incorrect. Water splitting (photolysis) at PS II provides replacement electrons. Plastoquinone functions as an electron carrier down the chain.",
      "citation": "Chapter 3, Section 3.2 (Page 14)"
    }
  ]
}
```

---

## 5. Diagnostic Gap Report (`/api/gap-report`)

### 5.1 Get Diagnostic Gap Summary
- **GET** `/gap-report/current`
- **Response** (`200 OK`):
```json
{
  "student_id": "usr_std_001",
  "assessment_date": "2026-11-09T10:20:00Z",
  "summary": {
    "total_topics_analyzed": 8,
    "weak_count": 3,
    "medium_count": 3,
    "strong_count": 2,
    "overall_preparedness": 52.4
  },
  "categorized_gaps": {
    "weak": [
      {
        "topic_id": "sub_01_01",
        "title": "Light Reactions & Photophosphorylation",
        "mastery_score": 0.25,
        "badge": "🔴 Weak",
        "diagnostic_reason": "You got 3 of 4 questions wrong regarding PS I vs PS II electron flow and water photolysis.",
        "exam_frequency_weight": 0.85
      }
    ],
    "medium": [
      {
        "topic_id": "sub_02_01",
        "title": "Glycolysis and ATP Yield",
        "mastery_score": 0.60,
        "badge": "🟡 Medium",
        "diagnostic_reason": "Understood irreversible steps, but miscalculated net ATP gain under anaerobic conditions.",
        "exam_frequency_weight": 0.70
      }
    ],
    "strong": [
      {
        "topic_id": "sub_01_02",
        "title": "Calvin Cycle (C3 Pathway)",
        "mastery_score": 0.90,
        "badge": "🟢 Strong",
        "diagnostic_reason": "All 4 questions answered correctly, including RuBisCO carboxylation dynamics.",
        "exam_frequency_weight": 0.65
      }
    ]
  }
}
```

---

## 6. Dynamic Personalized Revision Plan (`/api/revision-plan`)

### 6.1 Generate / Re-calculate Revision Plan
- **POST** `/revision-plan/generate`
- **Request Body**:
```json
{
  "available_days": 5,
  "daily_hours": 2.0
}
```
- **Response** (`200 OK`):
```json
{
  "plan_id": "plan_nov_09",
  "total_budget_hours": 10.0,
  "schedule": [
    {
      "day": 1,
      "allocated_hours": 2.0,
      "priority_order": 1,
      "topic_id": "sub_01_01",
      "topic_title": "Light Reactions & Photophosphorylation",
      "status_tag": "🔴 Weak",
      "exam_weight": "High (28% of past exams)",
      "target_actions": [
        "Review Z-scheme diagram in Chapter 3, Section 3.2",
        "Practice 5 targeted diagnostic questions on cyclic photophosphorylation"
      ]
    },
    {
      "day": 2,
      "allocated_hours": 2.0,
      "priority_order": 2,
      "topic_id": "sub_02_01",
      "topic_title": "Glycolysis Substrate-Level Phosphorylation",
      "status_tag": "🟡 Medium",
      "exam_weight": "Medium (18% of past exams)",
      "target_actions": [
        "Review ATP accounting chart in Notes p. 22"
      ]
    }
  ]
}
```

---

## 7. Explain-This-Topic Assistant (`/api/explain`)

### 7.1 Ask Grounded Explanation
- **POST** `/explain`
- **Request Body**:
```json
{
  "topic_id": "sub_01_01",
  "query": "Explain how cyclic photophosphorylation differs from non-cyclic, and why it doesn't produce NADPH."
}
```
- **Response** (`200 OK`):
```json
{
  "topic_id": "sub_01_01",
  "explanation_markdown": "Based on **Chapter 3, Section 3.4**, cyclic photophosphorylation occurs when only Photosystem I (PS I) is functional. The electron excited from P700 is cycled back to PS I through the electron transport chain, driving ATP synthesis via proton gradient. Because electrons do not pass to NADP+ reductase, **no NADPH is formed**, and water is not split, so **no oxygen is released**.",
  "citations": [
    {
      "document": "chapter_photosynthesis.pdf",
      "section": "Section 3.4: Cyclic Photophosphorylation",
      "page": "Page 16",
      "excerpt": "When only PS I is functional, the electron is circulated within the photosystem and the phosphorylation occurs due to cyclic flow of electrons..."
    }
  ]
}
```

---

## 8. Dashboard & Analytics (`/api/analytics`)

### 8.1 Student Progress Over Attempts
- **GET** `/analytics/progress`
- **Response** (`200 OK`):
```json
{
  "student_id": "usr_std_001",
  "attempts_history": [
    {
      "attempt_index": 1,
      "timestamp": "2026-11-07T14:00:00Z",
      "overall_score": 38.0,
      "topic_breakdown": {
        "Light Reactions": 25.0,
        "Calvin Cycle": 60.0
      }
    },
    {
      "attempt_index": 2,
      "timestamp": "2026-11-09T10:15:00Z",
      "overall_score": 55.0,
      "topic_breakdown": {
        "Light Reactions": 50.0,
        "Calvin Cycle": 85.0
      }
    }
  ],
  "learning_velocity": "+17% over last 2 attempts"
}
```

