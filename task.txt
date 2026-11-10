# Hackathon PS 2026

## PS: GapFinder AI (Find What the Student Doesn’t Know)

### Project Description

Students often study everything equally and still miss what they don’t know. Participants build an AI app that takes a student’s syllabus, textbook chapters, notes and past question papers, then finds the student’s weak areas and builds a personalized revision plan. Chat can support the experience, but the main output must be a diagnosis, not just answers.

### Purpose

Most study tools wait for the student to ask a question. A student can’t ask about a gap they don’t know they have. 

### Problem Statement

Given a syllabus, study material and past papers, build an app that:

- Maps questions and topics to the right parts of the syllabus using retrieval.
- Tests the student with generated questions grounded in the source material.
- Identifies weak topics from the student’s answers.
- Produces a prioritized revision plan that updates as the student improves.

### Impact

- Helps students spend time on what they actually don’t know.
- Reduces wasted revision effort before exams.
- Gives teachers a clearer view of where students struggle.
- Makes personalization measurable instead of vague.

### Scope

**Current use cases:** school and college students preparing for exams, competitive exam aspirants, and teachers who want topic-level insight into a class.

**Future scalability:** class-level analytics for teachers, parent progress views, multi-subject support, spaced-repetition reminders, and LMS integration.

### Features Expected

1. **Material upload** for syllabus, notes and past papers (PDF or text).
2. **Topic map** built from the uploaded syllabus.
3. **Diagnostic quiz** generated from the material, with citations to the source section.
4. **Gap report** showing weak, medium and strong topics with reasons.
5. **Personalized revision plan** ordered by priority and available study time.
6. **Explain-this-topic** assistant that answers only from the uploaded material.
7. **Progress dashboard** showing improvement across attempts.
8. **Login** with demo credentials and saved student data.

### AI Features (Mandatory)

- Retrieval-Augmented Generation (RAG) over the student’s own uploaded material, with citations.
- Question generation grounded in retrieved content, not the model’s memory.
- Answer evaluation that explains why an answer is right or wrong.
- Gap analysis that turns quiz results into topic-level weaknesses.
- Plan generation that adapts to the gap report.
- A clear explanation of where retrieval is used, where generation is used, and how the two are kept separate.

## Simplified Version of Problem statement 2:

#### The problem

Students usually revise everything equally. They re-read chapters they already know and still miss the parts they don't. Most study apps only answer questions the student asks. But a student can't ask about something they don't know they're missing.

So the app has to work like a doctor for studying. It shouldn't wait for questions. It should test the student, find what's weak, and give a "treatment plan."

What the app should do (start to finish)

1. The student uploads their study material
- The syllabus (list of topics)
- Textbook chapters and notes
- Past exam papers
1. The app builds a topic map
It reads the syllabus and breaks it into a clear list of topics and subtopics, like a table of contents. It also links each past-paper question to the topic it belongs to. This shows which topics show up most in exams.
2. The app gives the student a diagnostic quiz
- The questions must come from the student's own uploaded material, not from the AI's general knowledge.
- Each question shows where it came from (for example, "Chapter 3, Section 2"). That's the "citation."
1. The app checks the answers and explains them
For each answer, it says right or wrong and why, so the student learns from mistakes.
2. The app produces a gap report (the main output)
It sorts every topic into:
- 🔴 Weak: needs serious work
- 🟡 Medium: partly understood
- 🟢 Strong: already good

Each topic also gets a reason, for example: "You got 3 of 4 questions on photosynthesis wrong, mostly about the light reaction."

1. The app makes a personalized revision plan
- Weakest and most exam-important topics come first.
- It fits the student's available time ("I have 5 days, 2 hours a day").
- When the student takes another quiz and improves, the plan updates itself.
1. "Explain this topic" helper
A chat assistant that explains a topic using only the uploaded material, not outside internet knowledge.
2. Progress dashboard
Shows improvement over time. Example: "Attempt 1: 40% on Algebra, Attempt 3: 75%."
3. Login
Students log in, and their data, quizzes and progress are saved. Demo login details should be ready for judges or testers.

The key idea: "RAG"

The problem statement requires RAG (Retrieval-Augmented Generation). In simple words:

▎ Before the AI answers or makes a question, it first looks up the relevant part of the student's uploaded material, then uses only that to respond.

That's why everything has to show citations. It proves the AI is using the student's book and not making things up.

What matters most

The problem statement says it directly: "the main output must be a diagnosis, not just answers."

A chatbot alone isn't enough. The core loop is:

Upload → Test → Find weak spots → Plan → Re-test → Plan updates

Who it's for

- Students preparing for school, college or competitive exams
- Teachers, who can see which topics a whole class struggles with

Possible later additions (not needed now)

Class-wide reports for teachers, parent views, multiple subjects, revision reminders, and connecting to school systems.