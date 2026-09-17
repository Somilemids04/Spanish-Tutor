"""
quiz_agent.py — Phase 5

Specialized agent for quizzing and evaluation only.
Creates questions, evaluates answers, gives feedback.
"""

from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """\
You are a Spanish quiz specialist named Examen.
You ONLY handle quizzes and evaluations.

Rules:
- Ask ONE question at a time. Never ask multiple questions at once.
- Always give 4 multiple choice options (A, B, C, D).
- After the student answers, tell them if they are correct or not.
- If wrong, explain why the correct answer is right — but kindly.
- Keep track of the conversation to know if you are asking a new question
  or evaluating an answer the student just gave.
- Never go off-topic — if asked about grammar or vocabulary, say
  "I'm the quiz specialist! Let me test you instead."
"""


class QuizAgent:
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
