"""nodes/conversation.py — Phase 8"""
import os
from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.6-flash"
SYSTEM_INSTRUCTION = """\
You are Conversacion, a Spanish conversation partner.
Respond in simple Spanish first, then English translation below.
Gently correct mistakes. Show corrections as: ✓ Corrected: "right version"
Keep sentences short and beginner-friendly. Ask natural follow-up questions.
IMPORTANT: If context shows [Student name: X], you already know this — never ask for it again.
"""

def conversation_node(state: dict) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    messages = state.get("messages", [])
    student_name = state.get("student_name")
    words_learned = state.get("words_learned", [])
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
        model=MODEL_NAME, contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
    )
    reply = response.text
    messages.append({"role": "assistant", "content": reply})
    student_name_updated = state.get("student_name")
    lower_msg = state["user_message"].lower()
    for trigger in ["my name is", "i am", "me llamo", "soy", "mi nombre es"]:
        if trigger in lower_msg:
            idx = lower_msg.index(trigger) + len(trigger)
            name_part = state["user_message"][idx:].strip()
            name = name_part.split()[0].strip(".,!?") if name_part else None
            if name:
                student_name_updated = name.capitalize()
            break
    return {**state, "response": reply, "messages": messages,
            "last_agent": "conversation", "student_name": student_name_updated}
