"""
graph.py — Phase 6

Defines the LangGraph workflow.
Nodes = agent functions
Edges = transitions between agents
Conditional edges = supervisor decides which agent runs next

This replaces the if/else routing from Phase 5 with
a proper graph structure that LangGraph manages.
"""

from langgraph.graph import StateGraph, END
from  state import TutorState
from  nodes.supervisor import supervisor_node
from  nodes.grammar import grammar_node
from  nodes.vocabulary import vocabulary_node
from  nodes.quiz import quiz_node
from  nodes.conversation import conversation_node


def route_to_agent(state: TutorState) -> str:
    """
    Conditional edge function.
    LangGraph calls this after the supervisor node runs.
    Returns the name of the next node to execute.
    """
    return state.get("next_agent", "conversation")


def build_graph() -> StateGraph:
    """
    Builds and compiles the LangGraph agent workflow.

    Graph structure:
    START → supervisor → (grammar | vocabulary | quiz | conversation) → END
    """
    graph = StateGraph(TutorState)

    # Add all nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("grammar", grammar_node)
    graph.add_node("vocabulary", vocabulary_node)
    graph.add_node("quiz", quiz_node)
    graph.add_node("conversation", conversation_node)

    # Entry point — always start at supervisor
    graph.set_entry_point("supervisor")

    # Conditional routing — supervisor decides who goes next
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

    # All specialist agents go to END after responding
    graph.add_edge("grammar", END)
    graph.add_edge("vocabulary", END)
    graph.add_edge("quiz", END)
    graph.add_edge("conversation", END)

    return graph.compile()
