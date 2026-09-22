"""
chatbot.py — Phase 6

Terminal UI only. Maintains shared state across turns.
Passes state into LangGraph on every message.

Run with: python3 -m  chatbot
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from  graph import build_graph
from  state import TutorState

load_dotenv()

AGENT_LABELS = {
    "grammar":      "Gramatica (Grammar)",
    "vocabulary":   "Vocabulario (Vocabulary)",
    "quiz":         "Examen (Quiz)",
    "conversation": "Conversacion (Conversation)",
}


def main():
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY not found.")
        sys.exit(1)

    graph = build_graph()

    # Shared state — persists across the entire session
    state: TutorState = {
        "user_message": "",
        "next_agent": "conversation",
        "response": "",
        "messages": [],
        "words_learned": [],
        "topics_covered": [],
        "quiz_correct": 0,
        "quiz_total": 0,
        "last_agent": None,
        "student_name": None,
    }

    print("=" * 60)
    print("  Spanish Tutor (Phase 6 — Agent Orchestration)")
    print("  Agents share context — quiz uses your vocab words!")
    print("  Type 'exit' to quit | 'status' to see shared state")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("exit", "quit"):
            score = f"{state['quiz_correct']}/{state['quiz_total']}" if state['quiz_total'] > 0 else "no quiz taken"
            print(f"\nSupervisor: ¡Hasta luego! Quiz score this session: {score}")
            break

        # Show shared state — great for learning/debugging
        if user_input.lower() == "status":
            print("\n--- Shared State ---")
            print(f"Student name  : {state.get('student_name', 'unknown')}")
            print(f"Words learned : {state.get('words_learned', [])}")
            print(f"Topics covered: {state.get('topics_covered', [])}")
            print(f"Quiz score    : {state.get('quiz_correct', 0)}/{state.get('quiz_total', 0)}")
            print(f"Last agent    : {state.get('last_agent', 'none')}")
            print("--------------------")
            continue

        if not user_input:
            continue

        # Update state with new user message
        state["user_message"] = user_input

        try:
            # Run through LangGraph — state flows through all nodes
            result = graph.invoke(state)
            state = result  # updated state returned after all nodes run

            agent = state.get("last_agent", "unknown")
            label = AGENT_LABELS.get(agent, agent)
            print(f"\n  [Routed to: {label}]")
            print(f"\n{state['response']}")

        except Exception as e:
            print(f"\n[Error: {e}]")
            continue


if __name__ == "__main__":
    main()
