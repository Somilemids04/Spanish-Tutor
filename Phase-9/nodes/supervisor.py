"""
nodes/supervisor.py — Phase 9

Routes the user's message to the correct agent.
Phase 9 adds "lesson" as a valid route.
"""

import json
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

SYSTEM_INSTRUCTION = """You are a routing supervisor for a Spanish tutor app.
Classify the user's message into exactly one of these agents:
- grammar      → grammar questions, verb conjugation, sentence structure
- vocabulary   → word meanings, translations, word lists
- quiz         → user wants to be tested or quizzed
- lesson       → user wants a lesson plan, structured learning, or says 'lesson'
- conversation → general chat, greetings, anything else

Respond with ONLY valid JSON: {"agent": "<name>", "reason": "<one sentence>"}
No markdown, no extra text."""


def supervisor_node(state: TutorState) -> dict:
    user_msg = state.get("user_message", "")

    # Quick keyword shortcuts
    lower = user_msg.lower()
    if any(w in lower for w in ["lesson", "lesson plan", "study plan", "what should i learn"]):
        return {"next_agent": "lesson"}

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.0,
            ),
            contents=user_msg,
        )
        text = response.text.strip()
        # Strip markdown fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        data = json.loads(text)
        agent = data.get("agent", "conversation")
    except Exception:
        agent = "conversation"

    return {"next_agent": agent}
