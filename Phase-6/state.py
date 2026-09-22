"""
state.py — Phase 6

Defines the shared state that flows through the entire agent graph.
Every node reads from this state and can write back to it.
This is what allows agents to share context with each other.

Think of it as the "working memory" of the whole system.
"""

from typing import TypedDict, List, Optional


class TutorState(TypedDict):
    """
    The single source of truth shared across all agents.

    LangGraph passes this dict into every node function.
    Each node returns an updated version of it.
    """

    # Current user message
    user_message: str

    # The agent that should handle this message (set by supervisor)
    next_agent: str

    # Final response to show the user
    response: str

    # Running conversation history (role, content pairs)
    messages: List[dict]

    # Words the student has learned this session
    words_learned: List[str]

    # Topics covered this session
    topics_covered: List[str]

    # Current quiz score (correct answers / total questions)
    quiz_correct: int
    quiz_total: int

    # Last agent that responded (so quiz agent knows context)
    last_agent: Optional[str]

    # Student name if they've introduced themselves
    student_name: Optional[str]
