"""
graph.py — Phase 8
Same LangGraph structure, quiz node now uses full quiz engine.
"""

from langgraph.graph import StateGraph, END
from .state import TutorState
from .nodes.supervisor import supervisor_node
from .nodes.grammar import grammar_node
from .nodes.vocabulary import vocabulary_node
from .nodes.quiz import quiz_node
from .nodes.conversation import conversation_node


def route_to_agent(state: TutorState) -> str:
    # If a quiz is active, always route to quiz regardless of supervisor
    if state.get("quiz_active", False):
        return "quiz"
    return state.get("next_agent", "conversation")


def build_graph():
    graph = StateGraph(TutorState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("grammar", grammar_node)
    graph.add_node("vocabulary", vocabulary_node)
    graph.add_node("quiz", quiz_node)
    graph.add_node("conversation", conversation_node)

    graph.set_entry_point("supervisor")

    graph.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "grammar": "grammar",
            "vocabulary": "vocabulary",
            "quiz": "quiz",
            "conversation": "conversation",
        },
    )

    graph.add_edge("grammar", END)
    graph.add_edge("vocabulary", END)
    graph.add_edge("quiz", END)
    graph.add_edge("conversation", END)

    return graph.compile()
