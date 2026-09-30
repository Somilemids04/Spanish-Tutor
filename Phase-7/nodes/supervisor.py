"""
nodes/supervisor.py — Phase 7
Same routing logic as Phase 6.
"""

import json
import os
from google import genai
from .state import TutorState

MODEL_NAME = "gemini-2.0-flash"

ROUTING_PROMPT = """\
You are a routing supervisor for a Spanish tutoring app.
Read the student message and current context, then decide which specialist handles it.

Specialists:
- grammar       : grammar rules, conjugation, verb forms, sentence structure
- vocabulary    : new words, translations, themed word lists
- quiz          : testing the student, evaluating answers to questions
- conversation  : free Spanish practice, casual chat, greetings

Return ONLY valid JSON:
{"agent": "specialist_name", "reason": "one short sentence"}

Context clues:
- If student is answering a quiz question (A/B/C/D or short answer) → quiz
- If last_agent was quiz and student gave an answer → quiz
- If unsure → conversation
"""


def supervisor_node(state: TutorState) -> TutorState:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    context = f"""
Student message: {state['user_message']}
Last agent: {state.get('last_agent', 'none')}
Words learned so far: {state.get('words_learned', [])}
Topics covered: {state.get('topics_covered', [])}
Quiz score: {state.get('quiz_correct', 0)}/{state.get('quiz_total', 0)}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"{ROUTING_PROMPT}\n\n{context}",
        )
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        result = json.loads(raw)
        next_agent = result.get("agent", "conversation")
    except Exception:
        next_agent = "conversation"

    return {**state, "next_agent": next_agent}
