"""
lesson_planner.py — Phase 9

Analyzes the student's progress.json and generates a personalized lesson plan.
This is the core intelligence of Phase 9 — it turns raw data into a structured
learning path.

Key idea: a lesson plan is a list of ordered steps. Each step has a type
(vocabulary, grammar, practice, quiz) and a topic chosen based on what the
student needs most.
"""

import json
import os
from datetime import datetime

# ── Topic bank ────────────────────────────────────────────────────────────────
# All topics the tutor knows about, grouped by skill area.
TOPIC_BANK = {
    "vocabulary": [
        "greetings", "numbers", "colors", "family", "food",
        "animals", "body parts", "weather", "clothes", "travel",
    ],
    "grammar": [
        "ser vs estar", "present tense", "past tense", "future tense",
        "subjunctive", "reflexive verbs", "gender and articles",
        "direct object pronouns", "irregular verbs", "commands",
    ],
    "practice": [
        "everyday conversation", "restaurant ordering", "asking directions",
        "shopping", "making plans", "talking about yourself",
    ],
}

# All topics as a flat list for easy lookup
ALL_TOPICS = [t for topics in TOPIC_BANK.values() for t in topics]

PROGRESS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "progress.json"
)


def load_progress() -> dict:
    """Load progress.json, return empty structure if not found."""
    if not os.path.exists(PROGRESS_FILE):
        return {
            "words_learned": [],
            "topics_covered": [],
            "topic_scores": {},
            "quiz_correct": 0,
            "quiz_total": 0,
        }
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)


def _score_for_topic(topic: str, topic_scores: dict) -> float:
    """
    Returns a 0.0–1.0 score for a topic.
    0.0 = never attempted or all wrong
    1.0 = perfect
    """
    if topic not in topic_scores:
        return 0.0
    data = topic_scores[topic]
    total = data.get("total", 0)
    if total == 0:
        return 0.0
    return data.get("correct", 0) / total


def analyze_progress(progress: dict) -> dict:
    """
    Looks at what the student has done and classifies topics into:
    - strong:  scored ≥ 0.8
    - weak:    attempted but scored < 0.5
    - gap:     never covered at all
    - review:  attempted and scored 0.5–0.8 (needs reinforcement)

    Returns a dict with those four lists, plus a recommended_focus string.
    """
    topic_scores = progress.get("topic_scores", {})
    topics_covered = set(progress.get("topics_covered", []))

    strong, weak, review, gap = [], [], [], []

    for topic in ALL_TOPICS:
        score = _score_for_topic(topic, topic_scores)
        if topic not in topics_covered and topic not in topic_scores:
            gap.append(topic)
        elif score >= 0.8:
            strong.append(topic)
        elif score < 0.5:
            weak.append(topic)
        else:
            review.append(topic)

    # Decide focus: weak > gap > review
    if weak:
        recommended_focus = "remediation"
    elif gap:
        recommended_focus = "exploration"
    else:
        recommended_focus = "reinforcement"

    return {
        "strong": strong,
        "weak": weak,
        "review": review,
        "gap": gap,
        "recommended_focus": recommended_focus,
        "words_learned_count": len(progress.get("words_learned", [])),
        "quiz_correct": progress.get("quiz_correct", 0),
        "quiz_total": progress.get("quiz_total", 0),
    }


def generate_lesson_plan(student_name: str = "Student", lesson_count: int = 4) -> dict:
    """
    Generates a personalized lesson plan with `lesson_count` steps.

    Each step is a dict:
        {
            "step": 1,
            "type": "vocabulary" | "grammar" | "practice" | "quiz",
            "topic": "<topic name>",
            "reason": "<why this was chosen>",
            "difficulty": "beginner" | "intermediate" | "advanced",
        }

    Returns the full lesson plan as a dict.
    """
    progress = load_progress()
    analysis = analyze_progress(progress)

    steps = []
    used_topics = set()

    def pick_topic(pool: list) -> str | None:
        for t in pool:
            if t not in used_topics:
                used_topics.add(t)
                return t
        return None

    focus = analysis["recommended_focus"]

    # Determine difficulty from quiz performance
    quiz_total = analysis["quiz_total"]
    quiz_correct = analysis["quiz_correct"]
    if quiz_total == 0:
        difficulty = "beginner"
    elif quiz_total > 0 and (quiz_correct / quiz_total) >= 0.75:
        difficulty = "intermediate"
    else:
        difficulty = "beginner"

    # Build steps based on focus strategy
    for i in range(1, lesson_count + 1):
        step_type = _pick_step_type(i, lesson_count)

        if focus == "remediation" and analysis["weak"]:
            topic = pick_topic(analysis["weak"]) or pick_topic(analysis["gap"]) or pick_topic(analysis["review"])
            reason = f"You struggled with this topic — let's strengthen it."
        elif focus == "exploration" and analysis["gap"]:
            topic = pick_topic(analysis["gap"]) or pick_topic(analysis["review"])
            reason = f"You haven't covered this yet — time to explore!"
        else:
            topic = pick_topic(analysis["review"]) or pick_topic(analysis["gap"])
            reason = f"You've seen this before — let's reinforce it."

        # Final fallback
        if not topic:
            topic = pick_topic(ALL_TOPICS) or "greetings"
            reason = "Continuing your Spanish journey."

        steps.append({
            "step": i,
            "type": step_type,
            "topic": topic,
            "reason": reason,
            "difficulty": difficulty,
        })

    plan = {
        "student_name": student_name,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "focus": focus,
        "difficulty": difficulty,
        "total_steps": lesson_count,
        "steps": steps,
        "analysis_summary": {
            "strong_topics": len(analysis["strong"]),
            "weak_topics": len(analysis["weak"]),
            "new_topics": len(analysis["gap"]),
            "words_learned": analysis["words_learned_count"],
        },
    }
    return plan


def _pick_step_type(step_number: int, total: int) -> str:
    """
    Distributes step types across a lesson for variety.
    Lesson always ends with a quiz to check learning.
    """
    if step_number == total:
        return "quiz"
    if step_number == 1:
        return "vocabulary"
    if step_number == 2:
        return "grammar"
    return "practice"


def format_lesson_plan(plan: dict) -> str:
    """Returns a human-readable summary of the lesson plan."""
    lines = [
        f"\n📚 Personalized Lesson Plan for {plan['student_name']}",
        f"   Generated: {plan['generated_at']}",
        f"   Focus: {plan['focus'].capitalize()} | Difficulty: {plan['difficulty'].capitalize()}",
        f"   Words learned so far: {plan['analysis_summary']['words_learned']}",
        "",
    ]
    for step in plan["steps"]:
        icon = {"vocabulary": "📖", "grammar": "✏️", "practice": "💬", "quiz": "🎯"}.get(step["type"], "•")
        lines.append(
            f"   Step {step['step']}: {icon} {step['type'].capitalize()} — {step['topic']}"
        )
        lines.append(f"            {step['reason']}")
    lines.append("")
    return "\n".join(lines)
