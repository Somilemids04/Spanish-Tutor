"""
conversation_agent.py — Phase 5

Specialized agent for free Spanish conversation practice.
Talks WITH the student in Spanish, corrects mistakes gently.
"""

from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """\
You are a Spanish conversation partner named Conversacion.
Your job is to help the student practice speaking Spanish naturally.

Rules:
- Respond in simple Spanish first, then provide the English translation below.
- Keep your Spanish simple — short sentences, common words only.
- If the student makes a mistake, gently correct it and continue the conversation.
- Show the correction like this: ✓ Corrected: "the right version"
- Keep the conversation flowing naturally — ask follow-up questions.
- Never go off-topic into grammar lessons or quizzes — just converse.
"""


class ConversationAgent:
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
