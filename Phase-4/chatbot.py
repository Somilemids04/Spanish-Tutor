"""
chatbot.py — Phase 4

Thin UI layer. Just handles terminal input/output.
All agent logic lives in agent.py.
All tool logic lives in tools.py.

Run with: python3 phase4/chatbot.py
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from agent import TeacherAgent

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found.")
    sys.exit(1)


def main():
    client = genai.Client(api_key=API_KEY)
    agent = TeacherAgent(client)

    print("=" * 55)
    print("  Spanish Tutor (Phase 4 — Teacher Agent)")
    print("  I now have tools: translate, grammar, vocab, quiz")
    print("  Type 'exit' to quit | 'history' to see chat log")
    print("=" * 55)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Profe: ¡Hasta luego! See you next time!")
            break

        if user_input.lower() == "history":
            print("\n--- Conversation History ---")
            for msg in agent.history:
                if msg.role in ("user", "model"):
                    for part in msg.parts:
                        if hasattr(part, "text") and part.text:
                            role = "You" if msg.role == "user" else "Profe"
                            print(f"{role}: {part.text[:120]}")
            print("----------------------------")
            continue

        if not user_input:
            continue

        try:
            reply = agent.chat(user_input)
        except Exception as e:
            print(f"\n[Error: {e}]")
            continue

        print(f"\nProfe: {reply}")


if __name__ == "__main__":
    main()
