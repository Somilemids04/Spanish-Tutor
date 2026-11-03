"""nodes/grammar.py — Phase 9"""

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

SYSTEM_INSTRUCTION = """You are Profe, an expert Spanish grammar teacher.
Explain grammar concepts clearly. Use simple English. Give 3 short example sentences.
Highlight the key rule. No jargon. Keep it encouraging."""

_history = []


def grammar_node(state: TutorState) -> dict:
    global _history
    user_msg = state.get("user_message", "")

    _history.append({"role": "user", "parts": [{"text": user_msg}]})

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            ),
            contents=_history,
        )
        reply = response.text or "Let me think about that grammar question..."
        _history.append({"role": "model", "parts": [{"text": reply}]})
    except Exception as e:
        reply = f"Grammar error: {e}"
        _history = _history[:-1]

    topics_covered = list(state.get("topics_covered", []))
    if "grammar" not in topics_covered:
        topics_covered.append("grammar")

    return {"response": reply, "topics_covered": topics_covered, "last_agent": "grammar"}
