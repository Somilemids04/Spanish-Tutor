"""nodes/quiz.py — Phase 7"""
import os
from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.6-flash"
SYSTEM_INSTRUCTION = """\
You are Examen, a Spanish quiz specialist.
Ask ONE question at a time with 4 multiple choice options (A/B/C/D).
If you know what words the student recently learned, quiz them on those.
After the student answers: say correct/incorrect, explain why, then ask the next question.
Be encouraging even when wrong.
"""

def quiz_node(state: dict) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    messages = state.get("messages", [])
    words_learned = state.get("words_learned", [])
    context_note = ""
    if words_learned:
        context_note = f"\n[Context: Student recently learned: {', '.join(words_learned)}. Quiz on these if possible.]"
    messages.append({"role": "user", "content": state["user_message"] + context_note})
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
    quiz_correct = state.get("quiz_correct", 0)
    quiz_total = state.get("quiz_total", 0)
    lower = reply.lower()
    if "correct" in lower and "incorrect" not in lower:
        quiz_correct += 1
        quiz_total += 1
    elif "incorrect" in lower or "wrong" in lower:
        quiz_total += 1
    return {**state, "response": reply, "messages": messages, "quiz_correct": quiz_correct, "quiz_total": quiz_total, "last_agent": "quiz"}
