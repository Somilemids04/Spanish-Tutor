"""nodes/quiz.py — Phase 9 (carried over from Phase 8)"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google import genai
from google.genai import types
from dotenv import load_dotenv
from state import TutorState

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL_NAME = "gemini-2.0-flash"


def quiz_node(state: TutorState) -> dict:
    """Quiz state machine — generates questions, evaluates answers, reports."""
    user_msg = state.get("user_message", "").strip()
    quiz_active = state.get("quiz_active", False)
    quiz_questions = list(state.get("quiz_questions", []))
    quiz_current_index = state.get("quiz_current_index", 0)
    quiz_answers = list(state.get("quiz_answers", []))
    topic_scores = dict(state.get("topic_scores", {}))
    quiz_topic = state.get("quiz_topic", "general Spanish")
    quiz_difficulty = state.get("quiz_difficulty", "beginner")

    # ── Start a new quiz ──────────────────────────────────────────────────────
    if not quiz_active:
        topic = _extract_topic(user_msg) or "general Spanish"
        questions = _generate_questions(topic, quiz_difficulty, count=3)
        if not questions:
            return {
                "response": "I had trouble generating quiz questions. Please try again.",
                "quiz_active": False,
                "last_agent": "quiz",
            }
        first_q = _format_question(questions[0], 1, len(questions))
        return {
            "response": f"🎯 Quiz time on **{topic}**!\n\n{first_q}",
            "quiz_active": True,
            "quiz_topic": topic,
            "quiz_questions": questions,
            "quiz_current_index": 0,
            "quiz_answers": [],
            "last_agent": "quiz",
        }

    # ── Evaluate current answer ───────────────────────────────────────────────
    if quiz_current_index < len(quiz_questions):
        current_q = quiz_questions[quiz_current_index]
        evaluation = _evaluate_answer(current_q, user_msg)
        quiz_answers.append(evaluation)

        # Update topic scores
        topic = quiz_topic or "general"
        scores = topic_scores.get(topic, {"correct": 0, "total": 0})
        scores["total"] += 1
        if evaluation.get("is_correct"):
            scores["correct"] += 1
        topic_scores[topic] = scores

        next_index = quiz_current_index + 1

        # More questions remaining
        if next_index < len(quiz_questions):
            feedback = "✅ Correct!" if evaluation.get("is_correct") else f"❌ The answer was: {current_q.get('correct_answer', '?')}"
            next_q = _format_question(quiz_questions[next_index], next_index + 1, len(quiz_questions))
            return {
                "response": f"{feedback}\n\n{next_q}",
                "quiz_current_index": next_index,
                "quiz_answers": quiz_answers,
                "topic_scores": topic_scores,
                "quiz_correct": state.get("quiz_correct", 0) + (1 if evaluation.get("is_correct") else 0),
                "quiz_total": state.get("quiz_total", 0) + 1,
                "last_agent": "quiz",
            }

        # Quiz complete
        correct_count = sum(1 for a in quiz_answers if a.get("is_correct"))
        report = _generate_report(quiz_answers, quiz_topic, quiz_difficulty, correct_count, len(quiz_questions))
        return {
            "response": report,
            "quiz_active": False,
            "quiz_questions": [],
            "quiz_current_index": 0,
            "quiz_answers": [],
            "quiz_correct": state.get("quiz_correct", 0) + (1 if evaluation.get("is_correct") else 0),
            "quiz_total": state.get("quiz_total", 0) + 1,
            "topic_scores": topic_scores,
            "last_agent": "quiz",
        }

    return {"response": "Quiz complete! Type 'quiz' to start another.", "quiz_active": False, "last_agent": "quiz"}


def _extract_topic(msg: str) -> str:
    """Try to find a topic in the user's request."""
    lower = msg.lower()
    for keyword in ["about", "on", "for"]:
        if keyword in lower:
            idx = lower.index(keyword) + len(keyword)
            return msg[idx:].strip().rstrip("?!.,").strip()
    return "general Spanish"


def _generate_questions(topic: str, difficulty: str, count: int = 3) -> list:
    prompt = (
        f"Generate {count} {difficulty}-level Spanish quiz questions about '{topic}'.\n"
        "For each question, respond in this exact JSON format:\n"
        '[{"question": "...", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], '
        '"correct_answer": "A", "explanation": "..."}]\n'
        "Return ONLY the JSON array. No markdown."
    )
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(temperature=0.7),
            contents=prompt,
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        import json
        return json.loads(text)
    except Exception:
        return []


def _evaluate_answer(question: dict, student_answer: str) -> dict:
    correct = question.get("correct_answer", "").strip().upper()
    answer = student_answer.strip().upper()
    is_correct = answer == correct or answer.startswith(correct)
    return {
        "question": question.get("question", ""),
        "student_answer": student_answer,
        "correct_answer": correct,
        "is_correct": is_correct,
        "explanation": question.get("explanation", ""),
    }


def _format_question(q: dict, num: int, total: int) -> str:
    options = "\n".join(q.get("options", []))
    return f"**Question {num}/{total}:** {q.get('question', '')}\n\n{options}"


def _generate_report(answers: list, topic: str, difficulty: str, correct: int, total: int) -> str:
    pct = int((correct / total) * 100) if total > 0 else 0
    grade = "🏆 Excellent" if pct >= 80 else "👍 Good" if pct >= 60 else "📚 Keep practicing"
    lines = [
        f"🎯 Quiz Complete! {grade}",
        f"   Topic: {topic} | Difficulty: {difficulty}",
        f"   Score: {correct}/{total} ({pct}%)\n",
    ]
    for i, a in enumerate(answers, 1):
        status = "✅" if a.get("is_correct") else "❌"
        lines.append(f"Q{i}: {status} {a.get('question', '')}")
        if not a.get("is_correct"):
            lines.append(f"   Correct: {a.get('correct_answer')} — {a.get('explanation', '')}")
    lines.append("\nType 'quiz' for another round or ask me anything!")
    return "\n".join(lines)
