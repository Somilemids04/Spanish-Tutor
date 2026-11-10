"""
nodes/quiz.py — Phase 8

Completely rewritten. Uses quiz_engine.py for all quiz logic.
Manages quiz state machine:
  idle → generating → questioning → evaluating → reporting → idle
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from quiz_engine import (
    generate_questions,
    evaluate_answer,
    update_topic_scores,
    generate_report,
)


def quiz_node(state: dict) -> dict:
    """
    Quiz state machine:
    - If no quiz active → start one (generate questions)
    - If quiz active → evaluate answer, show next question
    - If quiz done → generate report, reset quiz state
    """
    user_msg = state.get("user_message", "").strip()
    quiz_active = state.get("quiz_active", False)
    questions = state.get("quiz_questions", [])
    current_idx = state.get("quiz_current_index", 0)
    quiz_answers = state.get("quiz_answers", [])
    topic_scores = state.get("topic_scores", {})
    words_learned = state.get("words_learned", [])

    # ── Case 1: No active quiz — start a new one ──────────────────────
    if not quiz_active:
        # Parse topic and difficulty from user message
        topic, difficulty = _parse_quiz_request(user_msg, words_learned)

        print(f"  [Quiz Engine: generating {difficulty} questions on '{topic}'...]")
        questions = generate_questions(topic, difficulty, count=5, words_learned=words_learned)

        if not questions:
            return {**state, "response": "Sorry, I couldn't generate quiz questions. Please try again."}

        # Show first question
        reply = _format_question(questions[0], 1, len(questions))

        return {
            **state,
            "response": reply,
            "quiz_active": True,
            "quiz_topic": topic,
            "quiz_difficulty": difficulty,
            "quiz_questions": questions,
            "quiz_current_index": 0,
            "quiz_answers": [],
            "last_agent": "quiz",
        }

    # ── Case 2: Quiz active — evaluate the student's answer ───────────
    if current_idx < len(questions):
        current_q = questions[current_idx]
        result = evaluate_answer(current_q, user_msg)
        quiz_answers = quiz_answers + [result]

        # Update topic scores
        topic = state.get("quiz_topic", "general")
        topic_scores = update_topic_scores(topic_scores, topic, result["is_correct"])

        # Build feedback message
        if result["is_correct"]:
            feedback = f"✅ Correct! {result['explanation']}"
        else:
            feedback = (
                f"❌ Not quite. The correct answer is {result['correct_answer']}: "
                f"{result['correct_text']}\n💡 {result['explanation']}"
            )

        next_idx = current_idx + 1

        # ── Case 2a: More questions remain ────────────────────────────
        if next_idx < len(questions):
            next_q = _format_question(questions[next_idx], next_idx + 1, len(questions))
            reply = f"{feedback}\n\n{next_q}"

            return {
                **state,
                "response": reply,
                "quiz_current_index": next_idx,
                "quiz_answers": quiz_answers,
                "topic_scores": topic_scores,
                "last_agent": "quiz",
            }

        # ── Case 2b: Quiz complete — generate report ──────────────────
        difficulty = state.get("quiz_difficulty", "beginner")
        report = generate_report(quiz_answers, topic, difficulty, topic_scores)
        reply = f"{feedback}\n{report}\n\nType 'quiz me' to start another quiz!"

        # Save this quiz score to session history
        session_scores = state.get("session_quiz_scores", [])
        correct_count = sum(1 for a in quiz_answers if a["is_correct"])
        session_scores.append({
            "topic": topic,
            "difficulty": difficulty,
            "correct": correct_count,
            "total": len(quiz_answers),
        })

        return {
            **state,
            "response": reply,
            "quiz_active": False,
            "quiz_questions": [],
            "quiz_current_index": 0,
            "quiz_answers": [],
            "topic_scores": topic_scores,
            "session_quiz_scores": session_scores,
            "last_agent": "quiz",
        }

    # Fallback — quiz state is broken, reset
    return {
        **state,
        "response": "Let's start fresh! What topic would you like to be quizzed on?",
        "quiz_active": False,
        "quiz_questions": [],
        "quiz_current_index": 0,
        "quiz_answers": [],
        "last_agent": "quiz",
    }


def _parse_quiz_request(message: str, words_learned: list) -> tuple:
    """Extracts topic and difficulty from user message."""
    msg = message.lower()

    difficulty = "beginner"
    if "intermediate" in msg:
        difficulty = "intermediate"
    elif "advanced" in msg or "hard" in msg:
        difficulty = "advanced"
    elif "easy" in msg or "beginner" in msg:
        difficulty = "beginner"

    # Extract topic
    topics = ["colors", "numbers", "animals", "food", "family",
              "greetings", "verbs", "grammar", "days", "months"]
    topic = "general"
    for t in topics:
        if t in msg:
            topic = t
            break

    # If no topic found but words were learned, quiz on those
    if topic == "general" and words_learned:
        topic = "recently learned words"

    return topic, difficulty


def _format_question(question: dict, number: int, total: int) -> str:
    """Formats a question dict into a readable string."""
    opts = question["options"]
    return (
        f"Question {number}/{total}:\n"
        f"{question['question']}\n\n"
        f"A) {opts['A']}\n"
        f"B) {opts['B']}\n"
        f"C) {opts['C']}\n"
        f"D) {opts['D']}\n\n"
        f"Your answer (A/B/C/D):"
    )
