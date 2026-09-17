"""
supervisor.py — Phase 5

The Supervisor Agent.
- Never teaches directly
- Reads the user message and decides which specialist to call
- Calls the specialist and returns their response
- Maintains which agent is "active" so multi-turn conversations work

This is the core of the multi-agent pattern.
"""

import json
from google import genai
from google.genai import types

from agents.grammar_agent import GrammarAgent
from agents.vocabulary_agent import VocabularyAgent
from agents.quiz_agent import QuizAgent
from agents.conversation_agent import ConversationAgent

MODEL_NAME = "gemini-3.6-flash"

ROUTING_PROMPT = """\
You are a routing supervisor for a Spanish tutoring app.
Read the student's message and decide which specialist should handle it.

Specialists available:
- grammar       : grammar rules, verb conjugation, sentence structure, ser vs estar
- vocabulary    : new words, translations, word meanings, themed word lists
- quiz          : testing, quizzes, evaluating student answers to questions
- conversation  : free Spanish practice, chatting in Spanish, casual talk

Rules:
- Return ONLY valid JSON, nothing else.
- Format: {"agent": "specialist_name", "reason": "one short sentence"}
- If the student is answering a quiz question, route to: quiz
- If unsure, route to: conversation

Examples:
"how do you say dog?" → {"agent": "vocabulary", "reason": "student wants a translation"}
"explain ser vs estar" → {"agent": "grammar", "reason": "grammar concept question"}
"quiz me on colors" → {"agent": "quiz", "reason": "student wants to be tested"}
"hola como estas" → {"agent": "conversation", "reason": "student is practicing Spanish"}
"B" → {"agent": "quiz", "reason": "student is answering a quiz question"}
"""


class Supervisor:
    def __init__(self, client: genai.Client):
        self.client = client

        # Initialize all specialist agents once
        self.agents = {
            "grammar": GrammarAgent(client),
            "vocabulary": VocabularyAgent(client),
            "quiz": QuizAgent(client),
            "conversation": ConversationAgent(client),
        }

        # Track which agent handled the last message
        # so we can continue multi-turn conversations correctly
        self.active_agent = None

    def _route(self, user_message: str) -> str:
        """
        Asks Gemini which agent should handle this message.
        Returns the agent name as a string.
        """
        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=f"{ROUTING_PROMPT}\n\nStudent message: {user_message}",
            )

            raw = response.text.strip()

            # Strip markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()

            result = json.loads(raw)
            return result.get("agent", "conversation"), result.get("reason", "")

        except Exception:
            return "conversation", "fallback"

    def chat(self, user_message: str) -> tuple[str, str]:
        """
        Routes user message to the right agent and returns their response.
        Returns (agent_name, response_text) so the UI can show who responded.
        """
        agent_name, reason = self._route(user_message)
        self.active_agent = agent_name

        specialist = self.agents[agent_name]
        response = specialist.chat(user_message)

        return agent_name, response
