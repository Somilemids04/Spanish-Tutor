"""
quiz_engine.py — Phase 8

Core quiz logic. Completely separate from the agent.
Responsibilities:
- Generate structured quiz questions via Gemini
- Evaluate student answers
- Track scores per topic
- Generate evaluation reports
- Suggest next difficulty level
"""

import json
import os
from google import genai

MODEL_NAME = "gemini-2.0-flash"


def generate_questions(topic: str, difficulty: str, count: int = 5, words_learned: list = None) -> list:
    """
    Generates a list of structured quiz questions on a topic.
    Returns a list of question dicts.
    """
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    words_context = ""
    if words_learned:
        words_context = f"Focus on these words the student learned: {', '.join(words_learned[:10])}"

    prompt = f"""
Generate {count} Spanish quiz questions about "{topic}" at {difficulty} level.
{words_context}

Return ONLY a valid JSON array, no markdown, no extra text.
Each question must follow this exact format:
{{
    "question": "the question text",
    "options": {{"A": "option1", "B": "option2", "C": "option3", "D": "option4"}},
    "correct": "A",
    "explanation": "why this answer is correct"
}}

Difficulty guide:
- beginner: single words, basic greetings, numbers, colors
- intermediate: verb conjugation, simple sentences, common phrases
- advanced: grammar rules, complex sentences, idioms
"""

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        raw = response.text.strip()

        # Strip markdown if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        questions = json.loads(raw)
        return questions if isinstance(questions, list) else []

    except Exception as e:
        # Fallback single question if generation fails
        return [{
            "question": f"How do you say 'hello' in Spanish?",
            "options": {"A": "Hola", "B": "Gracias", "C": "Adiós", "D": "Por favor"},
            "correct": "A",
            "explanation": "'Hola' means hello in Spanish."
        }]


def evaluate_answer(question: dict, student_answer: str) -> dict:
    """
    Evaluates a student's answer against the correct answer.
    Returns result dict with correct flag and feedback.
    """
    # Normalize the answer — accept "a", "A", or full option text
    answer = student_answer.strip().upper()

    # Handle full text answers — find closest option
    if answer not in ["A", "B", "C", "D"]:
        for key, val in question["options"].items():
            if answer.lower() == val.lower():
                answer = key
                break

    correct = question["correct"].upper()
    is_correct = answer == correct

    return {
        "question": question["question"],
        "student_answer": answer,
        "correct_answer": correct,
        "correct_text": question["options"].get(correct, ""),
        "is_correct": is_correct,
        "explanation": question["explanation"],
    }


def update_topic_scores(topic_scores: dict, topic: str, is_correct: bool) -> dict:
    """
    Updates the per-topic score tracker in shared state.
    """
    if topic not in topic_scores:
        topic_scores[topic] = {"correct": 0, "total": 0}

    topic_scores[topic]["total"] += 1
    if is_correct:
        topic_scores[topic]["correct"] += 1

    return topic_scores


def generate_report(quiz_answers: list, topic: str, difficulty: str, topic_scores: dict) -> str:
    """
    Generates a detailed evaluation report after quiz completion.
    Shows what was right/wrong, topic performance, and next steps.
    """
    if not quiz_answers:
        return "No quiz data to report."

    total = len(quiz_answers)
    correct = sum(1 for a in quiz_answers if a["is_correct"])
    pct = (correct / total * 100) if total > 0 else 0

    # Determine performance level
    if pct >= 80:
        verdict = "🌟 Excellent!"
        suggestion = f"You're ready to try {_next_difficulty(difficulty)} level!"
    elif pct >= 60:
        verdict = "👍 Good job!"
        suggestion = f"A bit more practice on {topic} and you'll be ready for {_next_difficulty(difficulty)}."
    else:
        verdict = "💪 Keep practicing!"
        suggestion = f"Review {topic} vocabulary and try this quiz again."

    lines = [
        f"\n{'='*48}",
        f"  📊 Quiz Report — {topic.title()} ({difficulty.title()})",
        f"{'='*48}",
        f"  Score: {correct}/{total} ({pct:.0f}%)  {verdict}",
        f"  {suggestion}",
        f"\n  Question breakdown:",
    ]

    for i, ans in enumerate(quiz_answers, 1):
        icon = "✅" if ans["is_correct"] else "❌"
        lines.append(f"  {icon} Q{i}: {ans['question'][:50]}")
        if not ans["is_correct"]:
            lines.append(f"      Your answer: {ans['student_answer']} | Correct: {ans['correct_answer']} ({ans['correct_text']})")
            lines.append(f"      💡 {ans['explanation']}")

    # Show all topic scores
    if topic_scores:
        lines.append(f"\n  Topic performance:")
        for t, s in topic_scores.items():
            t_pct = (s["correct"] / s["total"] * 100) if s["total"] > 0 else 0
            lines.append(f"  • {t}: {s['correct']}/{s['total']} ({t_pct:.0f}%)")

    lines.append(f"{'='*48}")
    return "\n".join(lines)


def _next_difficulty(current: str) -> str:
    order = ["beginner", "intermediate", "advanced"]
    idx = order.index(current) if current in order else 0
    return order[min(idx + 1, len(order) - 1)]
