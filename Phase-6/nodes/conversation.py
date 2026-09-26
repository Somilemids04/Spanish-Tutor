"""
nodes/conversation.py — Phase 6

Conversation agent node. Free Spanish practice.
Aware of student name and words learned from shared state.
"""

import os
from google import genai
from google.genai import types
from  state import TutorState

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """\
You are Conversacion, a Spanish conversation partner.
Respond in simple Spanish first, then English translation below.
Gently correct mistakes. Show corrections as: ✓ Corrected: "right version"
Keep sentences short and beginner-friendly. Ask natural follow-up questions.
"""


def conversation_node(state: TutorState) -> TutorState:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    messages = state.get("messages", [])
    student_name = state.get("student_name")
    words_learned = state.get("words_learned", [])

    # Enrich message with context from shared state
    context = state["user_message"]
    if student_name:
        context = f"[Student name: {student_name}] " + context
    if words_learned:
        context += f"\n[Words they know: {', '.join(words_learned[:10])}]"

    messages.append({"role": "user", "content": context})

    contents = [
        types.Content(role=m["role"] if m["role"] != "assistant" else "model",
                      parts=[types.Part(text=m["content"])])
        for m in messages
    ]

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
    )

    reply = response.text
    messages.append({"role": "assistant", "content": reply})

    # Try to extract student name if they introduced themselves.
    student_name_updated = state.get("student_name")
    lower_msg = state["user_message"].lower()
    if "my name is" in lower_msg or "i am" in lower_msg:
        words = state["user_message"].split()
        for i, w in enumerate(words):
            if w.lower() in ("is", "am") and i + 1 < len(words):
                student_name_updated = words[i + 1].strip(".,!?")
                break

    return {
        **state,
        "response": reply,
        "messages": messages,
        "last_agent": "conversation",
        "student_name": student_name_updated,
    }
