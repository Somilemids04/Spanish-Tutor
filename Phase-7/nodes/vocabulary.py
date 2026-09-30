"""nodes/vocabulary.py — Phase 7"""
import os, re
from google import genai
from google.genai import types

MODEL_NAME = "gemini-2.0-flash"
SYSTEM_INSTRUCTION = """\
You are Vocabulario, a Spanish vocabulary specialist.
For every word give: Spanish word, pronunciation, English meaning, example sentence.
Group words by theme when possible. Be enthusiastic and encouraging.
At the end of your response, on a new line write:
WORDS_LEARNED: word1, word2, word3
(list only the Spanish words you just taught)
"""

def vocabulary_node(state: dict) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    messages = state.get("messages", [])
    messages.append({"role": "user", "content": state["user_message"]})
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
    words_learned = state.get("words_learned", [])
    match = re.search(r"WORDS_LEARNED:\s*(.+)", reply)
    if match:
        new_words = [w.strip() for w in match.group(1).split(",")]
        words_learned = list(set(words_learned + new_words))
        reply = reply[:match.start()].strip()
    topics = state.get("topics_covered", [])
    topics.append(f"vocabulary: {state['user_message'][:40]}")
    return {**state, "response": reply, "messages": messages, "words_learned": words_learned, "topics_covered": topics, "last_agent": "vocabulary"}
