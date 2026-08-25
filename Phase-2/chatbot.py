"""
Phase 2: Conversation Memory.

Key change from Phase 1:
- We use client.chats.create() which maintains a running history list.
- Every turn, the FULL conversation is sent to Gemini automatically.
- The tutor now remembers everything said in this session.

Run with: python phase2/chatbot.py
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found. Did you create a .env file?")
    sys.exit(1)

SYSTEM_INSTRUCTION = """\
You are a friendly, patient Spanish language tutor named Profe.
Your student is a beginner learning Spanish.

Rules you must follow:
- If you're saying anything in spanish give a translated version of it as well.
- Always respond primarily in English, but include Spanish vocabulary,
  phrases, or example sentences naturally.
- When you introduce a Spanish word or phrase, also give its pronunciation
  in simple phonetic spelling.
- Keep explanations short and beginner-friendly. Avoid linguistic jargon.
- Be encouraging. Never make the student feel bad about mistakes.
- If the student writes in Spanish, gently correct any mistakes and explain why.
- You remember everything the student has told you in this conversation.
  Refer back to earlier context when relevant (e.g. their name, words they 
  already learned, mistakes they made earlier).
"""

MODEL_NAME = "gemini-2.5-flash"


def main():
    client = genai.Client(api_key=API_KEY)

    # --- THE KEY CHANGE FROM PHASE 1 ---
    # Instead of calling client.models.generate_content() each time (stateless),
    # we create a CHAT SESSION. The SDK maintains the history list internally.
    # Every call to chat.send_message() automatically includes full history.
    chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
        ),
    )

    print("=" * 50)
    print("  Spanish Tutor (Phase 2 — with memory)")
    print("  I will remember everything you tell me!")
    print("  Type 'exit' to quit.")
    print("  Type 'history' to see the conversation so far.")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Profe: ¡Hasta luego! (See you later!)")
            break

        # Debug tool: lets you inspect the raw history being sent to Gemini
        if user_input.lower() == "history":
            print("\n--- Conversation History ---")
            for msg in chat.get_history():
                role = "You" if msg.role == "user" else "Profe"
                text = msg.parts[0].text
                print(f"{role}: {text[:120]}{'...' if len(text) > 120 else ''}")
            print("----------------------------")
            continue

        if not user_input:
            continue

        try:
            # send_message() appends user message + model reply to history
            response = chat.send_message(user_input)
        except Exception as e:
            print(f"\n[Error talking to Gemini: {e}]")
            continue

        print(f"\nProfe: {response.text}")


if __name__ == "__main__":
    main()