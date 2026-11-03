"""
state.py — Phase 9

TutorState is the single shared object that flows through every node in the
LangGraph graph. Phase 9 adds lesson planning fields on top of Phase 8.
"""

from typing import TypedDict, List, Optional, Dict, Any


class TutorState(TypedDict):
    # ── Core ──────────────────────────────────────────────────────────────────
    user_message: str          # what the student just typed
    next_agent: str            # supervisor's routing decision
    response: str              # what gets printed to the student
    messages: List[dict]       # full conversation history (for each agent's LLM)

    # ── Progress tracking (Phase 7) ───────────────────────────────────────────
    words_learned: List[str]
    topics_covered: List[str]
    quiz_correct: int
    quiz_total: int
    last_agent: Optional[str]
    student_name: Optional[str]

    # ── Quiz state machine (Phase 8) ──────────────────────────────────────────
    quiz_active: bool
    quiz_topic: Optional[str]
    quiz_difficulty: str
    quiz_questions: List[dict]
    quiz_current_index: int
    quiz_answers: List[dict]
    topic_scores: Dict[str, dict]

    # ── Lesson planning (Phase 9) ─────────────────────────────────────────────
    lesson_active: bool         # True while stepping through a lesson plan
    lesson_plan: Optional[dict] # the full plan dict from lesson_planner.py
    lesson_step: int            # index of the current step (0-based)
