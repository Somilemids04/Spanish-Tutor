"""
state.py — Phase 8

Adds quiz engine fields to shared state.
"""

from typing import TypedDict, List, Optional, Dict


class TutorState(TypedDict):
    user_message: str
    next_agent: str
    response: str
    messages: List[dict]
    words_learned: List[str]
    topics_covered: List[str]
    last_agent: Optional[str]
    student_name: Optional[str]
    total_sessions: int
    session_quiz_scores: List[dict]
    session_start_word_count: int

    # Phase 8 — Quiz Engine fields
    quiz_active: bool                    # is a quiz currently running?
    quiz_topic: Optional[str]            # current quiz topic
    quiz_difficulty: str                 # beginner / intermediate / advanced
    quiz_questions: List[dict]           # list of question dicts
    quiz_current_index: int              # which question we're on
    quiz_answers: List[dict]             # student answers with correct/wrong
    topic_scores: Dict[str, dict]        # per-topic score tracking
