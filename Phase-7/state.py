"""
state.py — Phase 7

Same as Phase 6 but adds session tracking fields.
"""

from typing import TypedDict, List, Optional


class TutorState(TypedDict):
    user_message: str
    next_agent: str
    response: str
    messages: List[dict]
    words_learned: List[str]
    topics_covered: List[str]
    quiz_correct: int
    quiz_total: int
    last_agent: Optional[str]
    student_name: Optional[str]

    # NEW in Phase 7
    total_sessions: int                   # how many times student has run the app
    session_quiz_scores: List[dict]       # list of {score, total, date} per session
    session_start_word_count: int         # words known at session start (to track new words this session)
