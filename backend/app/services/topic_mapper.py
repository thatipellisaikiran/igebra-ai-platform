import re
from typing import List, Dict, Optional
from app.models.schemas import TopicNode, SubtopicNode, TopicMapResponse


class TopicMapperService:
    """
    Dynamically builds the curriculum topic map from uploaded syllabus/notes
    and links past exam paper questions to calculate real exam weightage.
    Starts empty with zero seed or dummy data.
    """

    def __init__(self):
        self.subject: str = "No Syllabus Uploaded Yet"
        self.topics: List[TopicNode] = []
        self.topic_eval_stats: Dict[str, Dict[str, int]] = {}
        self._past_paper_texts: List[str] = []

    def clear(self):
        self.subject = "No Syllabus Uploaded Yet"
        self.topics = []
        self.topic_eval_stats = {}
        self._past_paper_texts = []

    def ingest_syllabus(self, text: str, filename: str = "syllabus"):
        """Parses a syllabus document into chapters and subtopics."""
        lines = text.splitlines()
        subject_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
        if subject_match:
            self.subject = subject_match.group(1).strip()
        elif self.subject == "No Syllabus Uploaded Yet":
            self.subject = filename

        parsed_chapters: List[TopicNode] = []
        current_chapter: Optional[TopicNode] = None
        ch_idx = 0
        sub_idx = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Detect chapter headings (### Chapter..., ## Chapter..., or Chapter N:)
            if re.match(r'^#{2,3}\s+(?!Unit Overview)(.+)$', stripped, re.IGNORECASE) or re.match(r'^Chapter\s+\d+[:.\-]', stripped, re.IGNORECASE):
                title = re.sub(r'^#{1,3}\s+', '', stripped).strip()
                if title.lower().startswith("unit overview"):
                    continue
                ch_idx += 1
                sub_idx = 0
                current_chapter = TopicNode(
                    id=f"top_{ch_idx:02d}",
                    chapter_title=title,
                    exam_frequency_count=0,
                    exam_weightage_pct=0.0,
                    subtopics=[],
                )
                parsed_chapters.append(current_chapter)

            # Detect subtopics (- Section ..., - Topic ..., or numbered items)
            elif re.match(r'^[-*]\s+(.+)$', stripped):
                if current_chapter is None:
                    ch_idx += 1
                    current_chapter = TopicNode(
                        id=f"top_{ch_idx:02d}",
                        chapter_title=self.subject,
                        exam_frequency_count=0,
                        exam_weightage_pct=0.0,
                        subtopics=[],
                    )
                    parsed_chapters.append(current_chapter)

                sub_title = re.sub(r'^[-*]\s+', '', stripped).strip()
                sub_idx += 1
                current_chapter.subtopics.append(
                    SubtopicNode(
                        id=f"sub_{ch_idx:02d}_{sub_idx:02d}",
                        title=sub_title,
                        past_paper_occurrences=0,
                        weightage_category="Low",
                        current_mastery=0.0,
                        status="untested",
                    )
                )

        if parsed_chapters:
            # Merge or replace auto-generated notes topics with authoritative syllabus
            self.topics = parsed_chapters
            for pp_text in self._past_paper_texts:
                self._apply_past_paper_links(pp_text)
            self._recalculate_weightages()

    def ensure_topics_from_notes(self, text: str, filename: str):
        """If notes are uploaded before a syllabus, extract chapters/sections as topics."""
        if self.topics:
            return

        chapter_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
        chapter_title = chapter_match.group(1).strip() if chapter_match else filename
        if self.subject == "No Syllabus Uploaded Yet":
            self.subject = chapter_title

        sections = re.findall(r'^#{2,3}\s+(.+)$', text, flags=re.MULTILINE)
        if not sections:
            sections = [f"{filename} - Core Concepts"]

        subtopics = [
            SubtopicNode(
                id=f"sub_01_{idx + 1:02d}",
                title=sec.strip(),
                past_paper_occurrences=0,
                weightage_category="Low",
                current_mastery=0.0,
                status="untested",
            )
            for idx, sec in enumerate(sections)
        ]

        self.topics = [
            TopicNode(
                id="top_01",
                chapter_title=chapter_title,
                exam_frequency_count=0,
                exam_weightage_pct=0.0,
                subtopics=subtopics,
            )
        ]
        for pp_text in self._past_paper_texts:
            self._apply_past_paper_links(pp_text)
        self._recalculate_weightages()

    def link_past_papers(self, text: str):
        """Stores past paper text and links questions to syllabus subtopics."""
        self._past_paper_texts.append(text)
        if self.topics:
            self._apply_past_paper_links(text)
            self._recalculate_weightages()

    def _apply_past_paper_links(self, text: str):
        """Matches each past-paper question block to the closest subtopic(s)."""
        question_blocks = re.split(r'(?=^Q\d+[\.\):])', text, flags=re.MULTILINE)
        stopwords = {"the", "and", "for", "with", "of", "in", "to", "a", "an", "is", "are", "what", "why", "how", "section", "mapped", "topics"}

        for block in question_blocks:
            block_clean = block.strip()
            if not re.match(r'^Q\d+[\.\):]', block_clean):
                continue

            # Prefer explicit "Mapped Topics:" line if present, else match full question text
            mapped_match = re.search(r'Mapped Topics:\s*(.+)$', block_clean, flags=re.MULTILINE | re.IGNORECASE)
            match_target = mapped_match.group(1) if mapped_match else block_clean
            q_tokens = set(w for w in re.findall(r'\b[a-zA-Z0-9]{3,}\b', match_target.lower()) if w not in stopwords)
            if not q_tokens:
                continue

            best_subs: List[SubtopicNode] = []
            best_overlap = 0

            for ch in self.topics:
                for sub in ch.subtopics:
                    sub_tokens = set(w for w in re.findall(r'\b[a-zA-Z0-9]{3,}\b', sub.title.lower()) if w not in stopwords)
                    overlap = len(q_tokens.intersection(sub_tokens))
                    if overlap > best_overlap:
                        best_overlap = overlap
                        best_subs = [sub]
                    elif overlap == best_overlap and overlap > 0:
                        best_subs.append(sub)

            if best_overlap > 0:
                for sub in best_subs[:2]:
                    sub.past_paper_occurrences += 1

    def _recalculate_weightages(self):
        total_occ = sum(s.past_paper_occurrences for ch in self.topics for s in ch.subtopics)
        max_occ = max((s.past_paper_occurrences for ch in self.topics for s in ch.subtopics), default=0)

        for ch in self.topics:
            ch_occ = sum(s.past_paper_occurrences for s in ch.subtopics)
            ch.exam_frequency_count = ch_occ
            ch.exam_weightage_pct = round((ch_occ / total_occ) * 100, 1) if total_occ > 0 else 0.0

            for s in ch.subtopics:
                if max_occ == 0:
                    s.weightage_category = "Medium"
                elif s.past_paper_occurrences >= max(2, max_occ * 0.6):
                    s.weightage_category = "High"
                elif s.past_paper_occurrences >= 1:
                    s.weightage_category = "Medium"
                else:
                    s.weightage_category = "Low"

    def find_matching_subtopic(self, text: str, section_hint: str = "") -> Optional[SubtopicNode]:
        """Finds the syllabus subtopic most relevant to a chunk of study material."""
        stopwords = {"the", "and", "for", "with", "of", "in", "to", "a", "an", "is", "are", "section", "chapter"}
        query = f"{section_hint} {text[:300]}".lower()
        q_tokens = set(w for w in re.findall(r'\b[a-zA-Z0-9]{3,}\b', query) if w not in stopwords)

        best_sub = None
        best_score = -1

        for ch in self.topics:
            for sub in ch.subtopics:
                sub_tokens = set(w for w in re.findall(r'\b[a-zA-Z0-9]{3,}\b', sub.title.lower()) if w not in stopwords)
                sec_tokens = set(w for w in re.findall(r'\b[a-zA-Z0-9]{3,}\b', section_hint.lower()) if w not in stopwords)
                score = len(sec_tokens.intersection(sub_tokens)) * 3 + len(q_tokens.intersection(sub_tokens))
                if score > best_score:
                    best_score = score
                    best_sub = sub

        return best_sub

    def get_topic_map(self) -> TopicMapResponse:
        total_subtopics = sum(len(ch.subtopics) for ch in self.topics)
        return TopicMapResponse(
            subject=self.subject,
            total_chapters=len(self.topics),
            total_subtopics=total_subtopics,
            topics=self.topics,
        )

    def update_subtopic_mastery(self, topic_id: str, new_score: float, correct_count: int = 0, total_count: int = 0):
        if total_count > 0:
            self.topic_eval_stats[topic_id] = {"correct": correct_count, "total": total_count}

        for topic in self.topics:
            for sub in topic.subtopics:
                if sub.id == topic_id:
                    sub.current_mastery = round(new_score, 2)
                    if new_score < 0.50:
                        sub.status = "weak"
                    elif new_score <= 0.75:
                        sub.status = "medium"
                    else:
                        sub.status = "strong"
                    return


topic_mapper_service = TopicMapperService()
