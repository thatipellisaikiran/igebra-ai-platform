# Hackathon Judge Demo & Evaluation Walkthrough

This guide provides a step-by-step walkthrough to evaluate all 8 mandatory problem statement features of **GapFinder AI**.

---

## 🎯 Step-by-Step Feature Demonstration

### Step 1: Material Ingestion & Syllabus Parsing (`/api/materials`)
1. Open the UI at `http://localhost:5173` and click on **1. Ingest Materials**.
2. Notice the pre-indexed files:
   - `biology_syllabus.txt`
   - `chapter_photosynthesis.txt`
   - `past_exam_papers.txt`
3. Click **+ Upload Additional Chapter** to see real-time parsing, chunking, and metadata annotation.

---

### Step 2: Syllabus Topic Map & Past Exam Weightage (`/api/topic-map`)
1. Click **2. Topic Map**.
2. Observe how the curriculum is decomposed into:
   - Chapter 1: Photosynthesis in Higher Plants (28.5% exam share)
   - Chapter 2: Cellular Respiration in Plants (22.5% exam share)
3. Note how each subtopic displays its past paper occurrence count (e.g., *Non-Cyclic Z-Scheme* appeared in 6 past exam questions).

---

### Step 3: Citation-Grounded Diagnostic Quiz (`/api/quiz/diagnostic`)
1. Click **3. Diagnostic Quiz**.
2. Notice the citation pill on each question:
   - *Example:* `Citation: Section 1.4: Splitting of Water (Page 4)`
3. Select answers across the 5 diagnostic questions.
4. Click **Submit Answers & Diagnose Gaps**.
5. Observe the instant diagnostic evaluation explaining *why* an answer was correct or incorrect with verbatim quotes from the uploaded text.

---

### Step 4: The Core Diagnosis — Diagnostic Gap Report (`/api/gap-report`)
1. Click **4. Gap Report (Diagnosis)**.
2. Observe how the student's weaknesses are diagnosed:
   - 🔴 **Weak**: Needs serious work (e.g., *Light Reactions & Photophosphorylation* - 25% mastery)
   - 🟡 **Medium**: Partly understood (e.g., *Glycolysis* - 45% mastery)
   - 🟢 **Strong**: Already good (e.g., *Calvin Cycle* - 85% mastery)
3. Read the diagnostic evidence:
   - *"Diagnostic questions showed frequent confusion regarding electron transfer down the Z-scheme. Past exam frequency is 6 questions."*

---

### Step 5: Personalized Adaptive Revision Plan (`/api/revision-plan`)
1. Click **5. Revision Plan**.
2. Adjust the budget slider:
   - Set **Available Days** to `5 Days`
   - Set **Daily Study Time** to `2.0 Hours/day`
3. Click **Recalculate Plan**.
4. Observe how Day 1 and Day 2 prioritize the highest-weightage 🔴 Weak topics first, rather than reviewing everything equally.

---

### Step 6: Strict Guarded RAG Tutor — "Explain-This-Topic" (`/api/explain`)
1. Click **6. Grounded Tutor**.
2. Click one of the preset prompts or ask:
   > *"Why does cyclic photophosphorylation not release oxygen or make NADPH?"*
3. Verify that the answer cites `Section 1.5` and includes the exact textbook excerpt.
4. Try asking an out-of-syllabus question (e.g., *"What is string theory?"*):
   - Notice the guardrail block: GapFinder AI explicitly refuses to answer out-of-syllabus concepts to prevent exam distraction and hallucination.

---

### Step 7: Progress Dashboard & Persona Switcher (`/api/analytics`)
1. Click **7. Progress Dashboard**.
2. View historical attempts showing improvement from Attempt 1 (34%) to Attempt 3 (62%).
3. Click the user icon in the top right to switch from **Aarav Sharma (Student)** to **Dr. Meenakshi Sundaram (Teacher)**.
4. Review class-level analytics and struggle heatmaps.

