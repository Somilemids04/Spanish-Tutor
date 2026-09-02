"""
intent.py — Phase 3

Single responsibility: detect what the user is trying to do.
Takes raw user text, returns a clean intent label.

Intents supported:
- greeting        : "hola", "hi", "hello"
- translation     : "how do you say X", "what is X in Spanish"
- grammar         : "why is it X", "explain this grammar"
- vocabulary      : "what does X mean", "give me new words"
- practice        : "let's practice", "talk to me in Spanish"
- quiz            : "quiz me", "test me", "ask me a question"
- unknown         : anything that doesn't fit above
"""

import json
from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.6-flash"

# This prompt instructs Gemini to act as a classifier, not a tutor.
# Notice: we ask for JSON only — no explanation, no extra text.
INTENT_DETECTION_PROMPT = """\
You are an intent classifier for a Spanish language learning app.

Given a user message, classify it into EXACTLY ONE of these intents:
- greeting
- translation
- grammar
- vocabulary
- practice
- quiz
- unknown

Rules:
- Return ONLY a valid JSON object, nothing else.
- No explanation, no markdown, no extra text.
- Format: {"intent": "label", "confidence": "high/medium/low"}

Examples:
User: "hi there" → {"intent": "greeting", "confidence": "high"}
User: "how do you say cat in Spanish?" → {"intent": "translation", "confidence": "high"}
User: "why do adjectives come after nouns?" → {"intent": "grammar", "confidence": "high"}
User: "give me 5 new words" → {"intent": "vocabulary", "confidence": "high"}
User: "let's have a conversation in Spanish" → {"intent": "practice", "confidence": "high"}
User: "quiz me on colors" → {"intent": "quiz", "confidence": "high"}
User: "what do you think about pizza?" → {"intent": "unknown", "confidence": "high"}
"""

def detect_intent(client: genai.Client, user_message: str) -> dict:
    """
    Sends user message to Gemini for intent classification.
    Returns a dict like: {"intent": "translation", "confidence": "high"}
    Falls back to {"intent": "unknown", "confidence": "low"} on any error.
    """
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            # We send BOTH the classification instructions AND the user message
            contents=f"{INTENT_DETECTION_PROMPT}\n\nUser message: {user_message}",
        )

        raw = response.text.strip()

        # Strip markdown code fences if Gemini adds them despite instructions
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        result = json.loads(raw)
        return result

    except (json.JSONDecodeError, Exception):
        # Always return a valid dict — never crash the main loop
        return {"intent": "unknown", "confidence": "low"}