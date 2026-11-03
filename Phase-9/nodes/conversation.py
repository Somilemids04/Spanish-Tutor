"""nodes/conversation.py — Phase 9"""

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

SYSTEM_INSTRUCTION = """You are Profe, a warm and friendly Spanish tutor.
You chat naturally, answer questions, encourage the student.
If they tell you their name, acknowledge it warmly.
Keep responses concise and conversational."""

_history = []


def conversation_node(state: TutorState) -> dict:
    global _history
    user_msg = state.get("user_message", "")

    # Try to extract student name
    student_name = state.get("student_name")
    student_name_updated = student_name

    lower_msg = user_msg.lower()
    for trigger in ["my name is", "i am", "i'm", "me llamo", "soy", "mi nombre es"]:
        if trigger in lower_msg:
            idx = lower_msg.index(trigger) + len(trigger)
            name_part = user_msg[idx:].strip()
            name = name_part.split()[0].strip(".,!?") if name_part else None
            if name:
                student_name_updated = name.capitalize()
            break

    _history.append({"role": "user", "parts": [{"text": user_msg}]})

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.8,
            ),
            contents=_history,
        )
        reply = response.text or "¡Hola! How can I help you today?"
        _history.append({"role": "model", "parts": [{"text": reply}]})
    except Exception as e:
        reply = f"Conversation error: {e}"
        _history = _history[:-1]

    return {
        "response": reply,
        "student_name": student_name_updated,
        "last_agent": "conversation",
    }
