"""
nodes/vocabulary.py — Phase 6

Vocabulary agent node. Responds to word/translation requests,
updates shared state with words learned so the quiz agent can use them.
"""

import os
import re
from google import genai
from google.genai import types
from  state import TutorState

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """\
You are Vocabulario, a Spanish vocabulary specialist.
For every word give: Spanish word, pronunciation, English meaning, example sentence.
Group words by theme when possible. Be enthusiastic and encouraging.
At the end of your response, on a new line write:
WORDS_LEARNED: word1, word2, word3
(list only the Spanish words you just taught)
"""


def vocabulary_node(state: TutorState) -> TutorState:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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

    # Extract words learned from the response.
    words_learned = state.get("words_learned", [])
    match = re.search(r"WORDS_LEARNED:\s*(.+)", reply)
    if match:
        new_words = [w.strip() for w in match.group(1).split(",")]
        words_learned = list(set(words_learned + new_words))
        # Remove the WORDS_LEARNED line from the displayed response.
        reply = reply[:match.start()].strip()

    topics = state.get("topics_covered", [])
    topics.append(f"vocabulary: {state['user_message'][:40]}")

    return {
        **state,
        "response": reply,
        "messages": messages,
        "words_learned": words_learned,
        "topics_covered": topics,
        "last_agent": "vocabulary",
    }
