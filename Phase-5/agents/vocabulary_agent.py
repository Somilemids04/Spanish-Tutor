"""
vocabulary_agent.py — Phase 5

Specialized agent for vocabulary teaching only.
Focuses on word lists, pronunciation, and usage examples.
"""

from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """\
You are a Spanish vocabulary specialist named Vocabulario.
You ONLY handle vocabulary requests — teaching new words, translations,
and word usage.

Rules:
- For every word give: Spanish word, pronunciation in phonetic spelling,
  English meaning, and one short example sentence.
- Group words by theme when possible.
- Be enthusiastic about words — make them memorable.
- Never go off-topic — if asked about grammar or quizzes, say
  "That's outside my expertise, but I can teach you great vocabulary!"
"""


class VocabularyAgent:
    def __init__(self, client: genai.Client):
        self.client = client
        self.history = []

    def chat(self, user_message: str) -> str:
        self.history.append(
            types.Content(role="user", parts=[types.Part(text=user_message)])
        )

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=self.history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
            ),
        )

        reply = response.text
        self.history.append(
            types.Content(role="model", parts=[types.Part(text=reply)])
        )
        return reply
