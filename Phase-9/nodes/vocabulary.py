"""nodes/vocabulary.py — Phase 9"""

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

SYSTEM_INSTRUCTION = """You are Profe, a Spanish vocabulary teacher.
When teaching words, give: Spanish word, pronunciation, English meaning, example sentence.
At the end of your response, on its own line, write:
WORDS_LEARNED: word1, word2, word3
(list only the Spanish words you taught)"""

_history = []


def vocabulary_node(state: TutorState) -> dict:
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
        reply = response.text or "Here are some Spanish words..."
        _history.append({"role": "model", "parts": [{"text": reply}]})
    except Exception as e:
        reply = f"Vocabulary error: {e}"
        _history = _history[:-1]

    # Extract WORDS_LEARNED tag
    words_learned = list(state.get("words_learned", []))
    if "WORDS_LEARNED:" in reply:
        lines = reply.split("\n")
        display_lines = []
        for line in lines:
            if line.strip().startswith("WORDS_LEARNED:"):
                new_words = [w.strip() for w in line.replace("WORDS_LEARNED:", "").split(",") if w.strip()]
                for w in new_words:
                    if w not in words_learned:
                        words_learned.append(w)
            else:
                display_lines.append(line)
        reply = "\n".join(display_lines).strip()

    topics_covered = list(state.get("topics_covered", []))
    if "vocabulary" not in topics_covered:
        topics_covered.append("vocabulary")

    return {
        "response": reply,
        "words_learned": words_learned,
        "topics_covered": topics_covered,
        "last_agent": "vocabulary",
    }
