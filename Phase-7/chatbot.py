"""
chatbot.py — Phase 7

Key addition: loads progress at startup, saves after every turn.
Student picks up exactly where they left off.

Run with: python3 Phase-7/chatbot.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from phase7.graph import build_graph
from phase7.state import TutorState
from phase7.progress_tracker import (
    load_progress,
    save_progress,
    save_session_end,
    format_progress_summary,
)

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

    # ── Load saved progress ──────────────────────────────────────────
    saved = load_progress()

    # Merge saved progress into initial state
    state: TutorState = {
        "user_message": "",
        "next_agent": "conversation",
        "response": "",
        "messages": [],                                          # messages reset each session
        "words_learned": saved.get("words_learned", []),        # carried over ✅
        "topics_covered": saved.get("topics_covered", []),      # carried over ✅
        "quiz_correct": 0,                                       # reset each session
        "quiz_total": 0,                                         # reset each session
        "last_agent": None,
        "student_name": saved.get("student_name"),              # carried over ✅
        "total_sessions": saved.get("total_sessions", 0) + 1,  # increment session count
        "session_quiz_scores": saved.get("session_quiz_scores", []),
        "session_start_word_count": len(saved.get("words_learned", [])),
    }

    # Greet returning students by name
    name = state.get("student_name")
    greeting = f"Welcome back, {name}!" if name else "Welcome! I'm your Spanish tutor."

    print("=" * 60)
    print("  Spanish Tutor (Phase 7 — Progress Tracking)")
    print(f"  {greeting}")
    print(f"  Words learned so far: {len(state['words_learned'])}")
    print("  Type 'exit' to quit | 'status' | 'progress' for report")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("exit", "quit"):
            save_session_end(state)
            new_words = len(state["words_learned"]) - state["session_start_word_count"]
            print(f"\nSupervisor: ¡Hasta luego!")
            print(f"  This session: {new_words} new words | Quiz: {state['quiz_correct']}/{state['quiz_total']}")
            print(f"  Progress saved to Phase-7/data/progress.json ✅")
            break

        # Show live shared state
        if user_input.lower() == "status":
            print("\n--- Shared State ---")
            print(f"Student name  : {state.get('student_name', 'unknown')}")
            print(f"Words learned : {state.get('words_learned', [])}")
            print(f"Topics covered: {len(state.get('topics_covered', []))} topics")
            print(f"Quiz score    : {state.get('quiz_correct', 0)}/{state.get('quiz_total', 0)}")
            print(f"Session #     : {state.get('total_sessions', 1)}")
            print(f"Last agent    : {state.get('last_agent', 'none')}")
            print("--------------------")
            continue

        # Show full progress report
        if user_input.lower() == "progress":
            print(format_progress_summary({
                "student_name": state.get("student_name"),
                "total_sessions": state.get("total_sessions", 1),
                "words_learned": state.get("words_learned", []),
                "topics_covered": state.get("topics_covered", []),
                "session_quiz_scores": state.get("session_quiz_scores", []),
                "last_seen": "this session",
            }))
            continue

        if not user_input:
            continue

        state["user_message"] = user_input

        try:
            result = graph.invoke(state)
            state = result

            agent = state.get("last_agent", "unknown")
            label = AGENT_LABELS.get(agent, agent)
            print(f"\n  [Routed to: {label}]")
            print(f"\n{state['response']}")

            # ── Save progress after every turn ───────────────────────
            save_progress(state)

        except Exception as e:
            print(f"\n[Error: {e}]")
            continue


if __name__ == "__main__":
    main()
