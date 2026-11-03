"""
nodes/lesson.py — Phase 9

The Lesson Node drives the student through a personalized lesson plan one step
at a time. It is activated when:
  - The student asks for a lesson / lesson plan
  - lesson_active is already True (mid-lesson continuation)

State machine:
  lesson_active=False  → generate plan, show overview, set step=0, lesson_active=True
  lesson_active=True   → execute current step, advance step
  All steps done       → show completion summary, lesson_active=False
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google import genai
from google.genai import types
from dotenv import load_dotenv

from state import TutorState
from lesson_planner import generate_lesson_plan, format_lesson_plan

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL_NAME = "gemini-2.0-flash"

SYSTEM_INSTRUCTION = """You are Profe, a warm and encouraging Spanish tutor.
You are currently running a structured lesson. Your job is to deliver ONE lesson
step clearly and engagingly. Always:
- State what the step is about
- Teach the concept or vocabulary directly
- Give 2-3 example sentences
- End with a short encouraging message and tell the student to type 'next' to continue
Keep your response focused. This is one step of a multi-step lesson."""


def lesson_node(state: TutorState) -> dict:
    """
    Executes the current lesson step, or starts a new lesson.
    Returns state updates.
    """
    user_msg = state.get("user_message", "").lower().strip()

    # ── Start a new lesson ────────────────────────────────────────────────────
    if not state.get("lesson_active", False):
        student_name = state.get("student_name") or "Student"
        plan = generate_lesson_plan(student_name=student_name, lesson_count=4)
        overview = format_lesson_plan(plan)

        intro = (
            f"¡Vamos a estudiar! I've created a personalized lesson plan for you, "
            f"{student_name}.\n"
            + overview
            + "\nType **'next'** to start Step 1, or **'skip lesson'** to exit."
        )

        return {
            "response": intro,
            "lesson_active": True,
            "lesson_plan": plan,
            "lesson_step": 0,
            "last_agent": "lesson",
        }

    # ── Student wants to exit lesson ──────────────────────────────────────────
    if any(x in user_msg for x in ["skip lesson", "stop lesson", "exit lesson", "cancel lesson"]):
        return {
            "response": "No problem! We'll pick up the lesson another time. What would you like to do instead?",
            "lesson_active": False,
            "lesson_plan": None,
            "lesson_step": 0,
            "last_agent": "lesson",
        }

    plan = state.get("lesson_plan", {})
    steps = plan.get("steps", [])
    current_step = state.get("lesson_step", 0)

    # ── All steps completed ───────────────────────────────────────────────────
    if current_step >= len(steps):
        summary = _completion_summary(plan)
        return {
            "response": summary,
            "lesson_active": False,
            "lesson_plan": None,
            "lesson_step": 0,
            "last_agent": "lesson",
        }

    # ── Execute current step ──────────────────────────────────────────────────
    step = steps[current_step]
    step_response = _execute_step(step, current_step + 1, len(steps))

    next_step = current_step + 1

    # Add topic to covered list
    topics_covered = list(state.get("topics_covered", []))
    if step["topic"] not in topics_covered:
        topics_covered.append(step["topic"])

    return {
        "response": step_response,
        "lesson_step": next_step,
        "topics_covered": topics_covered,
        "last_agent": "lesson",
    }


def _execute_step(step: dict, step_num: int, total_steps: int) -> str:
    """Ask Gemini to deliver one lesson step."""
    step_type = step["type"]
    topic = step["topic"]
    difficulty = step["difficulty"]

    icon = {"vocabulary": "📖", "grammar": "✏️", "practice": "💬", "quiz": "🎯"}.get(step_type, "•")

    prompt = (
        f"[Step {step_num} of {total_steps}] {icon} {step_type.upper()}: {topic}\n\n"
        f"Difficulty: {difficulty}\n"
        f"Reason this was chosen: {step['reason']}\n\n"
        f"Deliver this lesson step. "
        f"{'Give 5 key Spanish words with pronunciation and example sentences.' if step_type == 'vocabulary' else ''}"
        f"{'Explain the grammar rule with 3 example sentences.' if step_type == 'grammar' else ''}"
        f"{'Create a short practice dialogue the student can use.' if step_type == 'practice' else ''}"
        f"{'Create ONE multiple-choice quiz question to test what they just learned.' if step_type == 'quiz' else ''}"
        f"\n\nEnd with: 'Type **next** to continue' (unless this is the last step — then say the lesson is complete)."
    )

    if step_num == total_steps:
        prompt = prompt.replace(
            "Type **next** to continue",
            "¡Felicitaciones! You've reached the end of the lesson!"
        )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            ),
            contents=prompt,
        )
        return response.text or f"Step {step_num}: {step_type} — {topic}"
    except Exception as e:
        return f"[Lesson step error: {e}]\n\nLet's try: {step_type} on {topic}."


def _completion_summary(plan: dict) -> str:
    """Returns a congratulatory lesson-complete message."""
    steps_done = plan.get("total_steps", 0)
    topics = [s["topic"] for s in plan.get("steps", [])]
    topics_str = ", ".join(topics) if topics else "several topics"

    return (
        f"🎉 ¡Excelente trabajo! You've completed your personalized lesson!\n\n"
        f"   In this session you worked on: {topics_str}\n"
        f"   Total steps completed: {steps_done}\n\n"
        f"Your progress has been saved. Type 'lesson' anytime to start a new plan, "
        f"or ask me anything in Spanish!"
    )
