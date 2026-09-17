"""
chatbot.py — Phase 5

Thin UI layer only. All routing logic in supervisor.py.
All agent logic in agents/*.py

Run with: python3 Phase-5/chatbot.py
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from supervisor import Supervisor

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found.")
    sys.exit(1)

# Agent display names shown in terminal
AGENT_LABELS = {
    "grammar":      "Gramatica (Grammar Agent)",
    "vocabulary":   "Vocabulario (Vocabulary Agent)",
    "quiz":         "Examen (Quiz Agent)",
    "conversation": "Conversacion (Conversation Agent)",
}


def main():
    client = genai.Client(api_key=API_KEY)
    supervisor = Supervisor(client)

    print("=" * 58)
    print("  Spanish Tutor (Phase 5 — Multiple Specialized Agents)")
    print("  Specialists: Grammar | Vocabulary | Quiz | Conversation")
    print("  Type 'exit' to quit")
    print("=" * 58)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Supervisor: ¡Hasta luego! See you next time!")
            break

        if not user_input:
            continue

        try:
            agent_name, reply = supervisor.chat(user_input)
            label = AGENT_LABELS.get(agent_name, agent_name)
            print(f"\n  [Routed to: {label}]")
            print(f"\n{reply}")
        except Exception as e:
            print(f"\n[Error: {e}]")
            continue


if __name__ == "__main__":
    main()
