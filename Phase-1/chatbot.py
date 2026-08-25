"""
Phase 1: Basic AI Chatbot for Learning Spanish.
This is the simplest possible version: every message is sent to Gemini
in isolation. There is NO memory of previous turns yet (that's Phase 2).
Run with: python3 /chatbot.py
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Loads GEMINI_API_KEY
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found. Did you create a .env file?")
    sys.exit(1)

# Notice: Behavior comes from the prompt.
SYSTEM_INSTRUCTION = """\
You are a friendly, patient Spanish language tutor named Professor.
Your student is a beginner learning Spanish.

Rules you must follow:
- Always respond primarily in English, but include Spanish vocabulary,
  phrases, or example sentences naturally.
- When you introduce a Spanish word or phrase, also give its pronunciation
  in simple phonetic spelling.
- Keep explanations short and beginner-friendly. Avoid linguistic jargon.
- Be encouraging. Never make the student feel bad about mistakes.
- If the student writes in Spanish, gently correct any mistakes and explain why.
"""

MODEL_NAME = "gemini-2.5-flash" 


def get_tutor_response(client: genai.Client, user_message: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
        ),
    )
    return response.text


def main():
    client = genai.Client(api_key=API_KEY)
    print("=" * 50)
    print("  Spanish Tutor (Phase 1 — no memory yet)")
    print("  Type 'exit' to quit.")
    print("=" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Profe: ¡Hasta luego! (See you later!)")
            break
        
        if not user_input:
            continue

        try:
            reply = get_tutor_response(client, user_input)
        except Exception as e:
            print(f"\n[Error talking to Gemini: {e}]")
            continue
        print(f"\nProfe: {reply}")

if __name__ == "__main__":
    main()
