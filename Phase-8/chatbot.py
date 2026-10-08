"""
chatbot.py — Phase 8

Adds quiz engine state fields to initial state.
Run with: python3 Phase-8/chatbot.py
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from phase8.graph import build_graph
from phase8.state import TutorState
from phase8.progress_tracker import (
    load_progress,
    save_progress,
    save_session_end,
    format_progress_summary,
)

load_dotenv()

AGENT_LABELS = {
    "grammar":      "Gramatica (Grammar)",
    "vocabulary":   "Vocabulario (Vocabulary)",
    "quiz":         "Examen (Quiz Engine)",
    "conversation": "Conversacion (Conversation)",
}


def main():
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY not found.")
        sys.exit(1)

    graph = build_graph()
    saved = load_progress()
    name = saved.get("student_name")

    state: TutorState = {
        "user_message": "",
        "next_agent": "conversation",
        "response": "",
        "messages": [],
        "words_learned": saved.get("words_learned", []),
        "topics_covered": saved.get("topics_covered", []),
        "last_agent": None,
        "student_name": name,
        "total_sessions": saved.get("total_sessions", 0) + 1,
        "session_quiz_scores": saved.get("session_quiz_scores", []),
        "session_start_word_count": len(saved.get("words_learned", [])),
        # Quiz engine fields
        "quiz_active": False,
        "quiz_topic": None,
        "quiz_difficulty": "beginner",
        "quiz_questions": [],
        "quiz_current_index": 0,
        "quiz_answers": [],
        "topic_scores": saved.get("topic_scores", {}),
    }

    greeting = f"Welcome back, {name}!" if name else "Welcome! I'm your Spanish tutor."

    print("=" * 60)
    print("  Spanish Tutor (Phase 8 — Quiz & Evaluation)")
    print(f"  {greeting}")
    print(f"  Words learned: {len(state['words_learned'])} | Sessions: {state['total_sessions']}")
    print("  Commands: 'exit' | 'status' | 'progress'")
    print("  Quiz: 'quiz me on colors' | 'quiz intermediate on verbs'")
    print("=" * 60)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("exit", "quit"):
            save_session_end(state)
            print(f"\n¡Hasta luego! Progress saved ✅")
            break

        if user_input.lower() == "status":
            print("\n--- Shared State ---")
            print(f"Student       : {state.get('student_name', 'unknown')}")
            print(f"Words learned : {len(state.get('words_learned', []))} words")
            print(f"Quiz active   : {state.get('quiz_active', False)}")
            if state.get("quiz_active"):
                print(f"Quiz topic    : {state.get('quiz_topic')}")
                print(f"Question      : {state.get('quiz_current_index', 0) + 1}/{len(state.get('quiz_questions', []))}")
            print(f"Last agent    : {state.get('last_agent', 'none')}")
            print("--------------------")
            continue

        if user_input.lower() == "progress":
            print(format_progress_summary(state))
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
            save_progress(state)

        except Exception as e:
            print(f"\n[Error: {e}]")
            continue


if __name__ == "__main__":
    main()
