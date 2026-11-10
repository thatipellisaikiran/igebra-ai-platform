# System Architecture & Technical Design: GapFinder AI

## 1. High-Level Architecture Overview

GapFinder AI is built on a clean, decoupled client-server architecture designed around a **Retrieval-Augmented Diagnostic Engine**. The architecture explicitly separates **Retrieval** (ground truth extraction from student notes and syllabus) from **Generation** (question authoring, gap diagnostic reasoning, and revision scheduling).

```mermaid
graph TD
    subgraph ClientLayer["Frontend Presentation Layer (React + TypeScript)"]
        UI_Upload["Upload Portal (Syllabus, Notes, Papers)"]
        UI_TopicMap["Topic Map & Exam Weightage Tree"]
        UI_Quiz["Diagnostic Quiz Runner with Citations"]
        UI_Gap["Diagnostic Gap Report (Weak/Med/Strong)"]
        UI_Plan["Adaptive Revision Scheduler"]
        UI_Explain["Explain-This-Topic RAG Chat"]
        UI_Dash["Progress & Mastery Dashboard"]
    end

    subgraph APILayer["FastAPI Gateway & Controller Layer"]
        EP_Auth["/api/auth"]
        EP_Upload["/api/materials/upload"]
        EP_TopicMap["/api/topic-map"]
        EP_Quiz["/api/quiz"]
        EP_Gap["/api/gap-report"]
        EP_Plan["/api/revision-plan"]
        EP_Explain["/api/explain"]
        EP_Analytics["/api/analytics"]
    end

    subgraph ServiceLayer["Core Domain Services"]
        SVC_Parser["Document Parser & Text Extractor"]
        SVC_TopicMapper["Topic Mapper & Past-Paper Linker"]
        SVC_RAG["RAG Engine (Dense + Sparse Hybrid Retriever)"]
        SVC_QuizGen["Citation-Grounded Quiz Generator"]
        SVC_Evaluator["Diagnostic Answer Evaluator"]
        SVC_GapAnalyzer["Gap Scoring & Taxonomy Engine"]
        SVC_PlanOptimizer["Dynamic Revision Plan Optimizer"]
    end

    subgraph StorageLayer["Data & Persistence Layer"]
        DB_Relational["Relational Storage (Users, Quizzes, Progress, Topic Tree)"]
        DB_Vector["Vector Index (Chroma / FAISS - Text Chunks with Citations)"]
        Store_Files["Object / File Storage (Raw Uploaded PDFs / TXT)"]
    end

    UI_Upload --> EP_Upload
    UI_TopicMap --> EP_TopicMap
    UI_Quiz --> EP_Quiz
    UI_Gap --> EP_Gap
    UI_Plan --> EP_Plan
    UI_Explain --> EP_Explain
    UI_Dash --> EP_Analytics

    EP_Upload --> SVC_Parser
    SVC_Parser --> Store_Files
    SVC_Parser --> SVC_RAG
    SVC_RAG --> DB_Vector

    EP_TopicMap --> SVC_TopicMapper
    SVC_TopicMapper --> DB_Relational

    EP_Quiz --> SVC_QuizGen
    SVC_QuizGen --> SVC_RAG
    SVC_QuizGen --> DB_Relational

    EP_Gap --> SVC_Evaluator
    SVC_Evaluator --> SVC_GapAnalyzer
    SVC_GapAnalyzer --> DB_Relational

    EP_Plan --> SVC_PlanOptimizer
    SVC_PlanOptimizer --> DB_Relational

    EP_Explain --> SVC_RAG
```

---

## 2. Separation of Concerns: Retrieval vs. Generation

A critical requirement of the hackathon problem statement is guaranteeing that AI generated content does not hallucinate or use external out-of-syllabus web knowledge.

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant UI as Web Client
    participant API as API Controller
    participant Retriever as RAG Retriever
    participant VectorStore as Vector Database
    participant LLM as Grounded LLM

    Student->>UI: Selects Topic / Starts Diagnostic Test
    UI->>API: POST /api/quiz/generate { topic_id: "T-BIO-02" }
    
    rect rgb(235, 245, 255)
        Note over API,VectorStore: STEP 1: STRICT RETRIEVAL (Deterministic)
        API->>Retriever: Query top chunks for Topic ID with Section Filters
        Retriever->>VectorStore: Vector similarity + metadata filter (doc_type: notes, syllabus)
        VectorStore-->>Retriever: Chunks with Metadata (Doc: Bio_Ch3.pdf, Sec: 3.2, Page: 45)
    end

    rect rgb(255, 243, 230)
        Note over API,LLM: STEP 2: GROUNDED GENERATION (Constrained Synthesis)
        API->>LLM: Prompt = [Strict System Contract] + [Retrieved Context + Citations]
        LLM-->>API: Structured Quiz Items { question, options, correct_idx, citation: "Chapter 3, Sec 3.2, p.45" }
    end

    API->>UI: Returns Diagnostic Quiz with verifiable Citations
    UI->>Student: Displays Questions with Source Citation Pill
```

### Retrieval Layer Duties:
- Deterministic extraction of raw text from PDFs, Markdown, and TXT files.
- Chunking by semantic boundaries (headers, markdown sections, paragraphs) to avoid splitting definitions.
- Tagging chunks with rich metadata: `{ "document_name": "photosynthesis.pdf", "chapter": "Light Reactions", "section": "Photophosphorylation", "page": 14 }`.
- Similarity search restricted to the student's own collection.

### Generation Layer Duties:
- Strictly bound by system instructions: *“Never introduce facts or concepts not found within `<context>`. If the retrieved context is insufficient, return an empty set or request clarification.”*
- Producing structured JSON conforming to schema types with mandatory citation attributes.

---

## 3. End-to-End User Flow & Processing Pipeline

### Phase 1: Material Ingestion & Syllabus Decomposition
1. Student uploads:
   - **Syllabus**: Outlines topics, subtopics, and official learning objectives.
   - **Textbooks / Notes**: Source content for explanations and questions.
   - **Past Exam Papers**: Questions from previous years.
2. The `TopicMapper` parses the syllabus into a hierarchy tree (`Subject -> Chapter -> Topic -> Subtopic`).
3. Past-paper questions are parsed and semantically linked to syllabus nodes to assign an **Exam Frequency / Weightage Score** ($W_{\text{exam}}$).

### Phase 2: Diagnostic Assessment
1. The student triggers a diagnostic test (e.g., across the entire syllabus or a selected unit).
2. For each topic, the `QuizGenerator` retrieves candidate chunks and synthesizes diagnostic questions (Multiple Choice and Conceptual Short Answer).
3. Every generated question has an explicit citation (e.g., `Ref: NCERT Chapter 4, Sec 2.1`).

### Phase 3: Diagnostic Gap Analysis
1. The student submits answers.
2. The `Evaluator` grades answers against source definitions and constructs clear rationales for why options are correct or incorrect.
3. The `GapAnalyzer` computes mastery per subtopic:
   - **Accuracy**: Percentage of correct questions.
   - **Confidence & Error Depth**: Missed conceptual questions carry higher penalty than rote memory misses.
4. Topics are classified into:
   - 🔴 **Weak**: Mastery $< 50\%$ or foundational misconceptions detected.
   - 🟡 **Medium**: Mastery $50\% - 75\%$, partial grasp.
   - 🟢 **Strong**: Mastery $> 75\%$, consistent accuracy.

### Phase 4: Dynamic Revision Plan Formulation
1. Student inputs available revision budget (e.g., 5 days, 2 hours/day = 10 total hours).
2. The `PlanOptimizer` prioritizes topics using the objective function:
   $$\text{Priority Score} = \alpha \cdot (1 - \text{Mastery}) + \beta \cdot \text{Exam Weightage} + \gamma \cdot \text{Prerequisite Urgency}$$
3. Produces a scheduled day-by-day study roadmap focusing first on high-weightage weak areas.

### Phase 5: Targeted "Explain This Topic" & Re-Testing
1. Student clicks on any 🔴 Weak topic to open the **Explain-This-Topic** assistant.
2. The assistant retrieves relevant excerpts from the student's notes and presents a tailored explanation with interactive citations.
3. The student takes a short follow-up micro-quiz on that topic.
4. When score improves, the mastery score updates in real-time, shifting the topic from 🔴 Weak to 🟡 Medium or 🟢 Strong, and automatically reorganizing the revision plan.

---

## 4. Database Entity-Relationship Model

```mermaid
erDiagram
    USER ||--o{ DOCUMENT : uploads
    USER ||--o{ QUIZ_ATTEMPT : takes
    USER ||--o{ REVISION_PLAN : owns

    DOCUMENT ||--o{ DOCUMENT_CHUNK : contains
    
    TOPIC ||--o{ TOPIC : subtopic_of
    TOPIC ||--o{ DOCUMENT_CHUNK : referenced_in
    TOPIC ||--o{ PAST_PAPER_QUESTION : tested_by
    TOPIC ||--o{ QUIZ_QUESTION : generates
    TOPIC ||--o{ TOPIC_MASTERY : tracks

    USER ||--o{ TOPIC_MASTERY : has
    QUIZ_ATTEMPT ||--o{ STUDENT_ANSWER : includes
    QUIZ_QUESTION ||--o{ STUDENT_ANSWER : receives
    REVISION_PLAN ||--o{ PLAN_ITEM : contains
    TOPIC ||--o{ PLAN_ITEM : targets

    USER {
        string id PK
        string email
        string role "student | teacher"
        string full_name
    }

    TOPIC {
        string id PK
        string parent_id FK
        string title
        int depth
        float exam_weightage
    }

    TOPIC_MASTERY {
        string id PK
        string user_id FK
        string topic_id FK
        float mastery_score "0.0 to 1.0"
        string status "weak | medium | strong"
        string diagnosis_reason
        datetime updated_at
    }

    QUIZ_QUESTION {
        string id PK
        string topic_id FK
        string question_text
        json options
        int correct_option_idx
        string explanation
        string citation
        string source_chunk_id
    }
```

