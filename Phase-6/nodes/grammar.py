"""
nodes/grammar.py — Phase 6

Grammar agent node. Reads shared state, responds to grammar questions,
updates state with the topic covered.
"""

import os
from google import genai
from google.genai import types
from  state import TutorState

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """\
You are Gramatica, a Spanish grammar specialist.
Explain grammar concepts clearly with 3 short examples.
Always show Spanish + English translation for each example.
Be encouraging and beginner-friendly.
"""


def grammar_node(state: TutorState) -> TutorState:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Build messages including history for context.
    messages = state.get("messages", [])
    messages.append({"role": "user", "content": state["user_message"]})

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

    # Update topics covered in shared state.
    topics = state.get("topics_covered", [])
    topics.append(f"grammar: {state['user_message'][:40]}")

    return {
        **state,
        "response": reply,
        "messages": messages,
        "topics_covered": topics,
        "last_agent": "grammar",
    }
