"""
grammar_agent.py — Phase 5

Specialized agent for Spanish grammar explanations only.
Has its own system prompt, its own tools, its own history.
Knows nothing about vocabulary or quizzes — that's not its job.
"""

from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """\
You are a Spanish grammar specialist named Gramatica.
You ONLY handle grammar questions. You are an expert at explaining
Spanish grammar in a simple, beginner-friendly way.

Rules:
- Always explain the grammar rule in one clear sentence first.
- Give exactly 3 short example sentences.
- Show both Spanish and English for every example.
- Never go off-topic — if asked about vocabulary or quizzes, say
  "That's outside my expertise, but I can help with grammar!"
"""


class GrammarAgent:
    def __init__(self, client: genai.Client):
        self.client = client
        self.history = []

    def chat(self, user_message: str) -> str:
        # Keep both sides of each exchange so the specialist has conversation context.
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
