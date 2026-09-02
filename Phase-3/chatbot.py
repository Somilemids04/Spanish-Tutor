"""
Phase 3: Intent Detection

What's new vs Phase 2:
- Every message is classified by detect_intent() before the tutor responds.
- The detected intent is shown to you in the terminal (so you can see it working).
- The tutor's system prompt is updated per-intent to shape the response style.
- intent.py handles all classification logic — chatbot.py just routes.

Run with: python3 phase3/chatbot.py
"""
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Import our new intent detection module
from intent import detect_intent

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found.")
    sys.exit(1)

MODEL_NAME = "gemini-3.6-flash"

# Base persona — always applied
BASE_SYSTEM_INSTRUCTION = """\
You are a friendly, patient Spanish language tutor named Profe.
Your student is a beginner learning Spanish.
Always respond in English but include Spanish words and phrases naturally.
Give pronunciation in simple phonetic spelling when introducing Spanish words.
Be encouraging. Keep responses concise and beginner-friendly.
"""

# Extra instructions added on top of the base, per detected intent.
# This is how intent shapes the response — not by writing separate functions,
# but by giving the model more specific instructions for each situation.
INTENT_INSTRUCTIONS = {
    "greeting": "The student is greeting you. Greet them warmly in both English and Spanish.",
    "translation": "The student wants a translation. Give the Spanish word/phrase, its pronunciation, and one example sentence.",
    "grammar": "The student has a grammar question. Give a simple, clear explanation with 2-3 short examples. No jargon.",
    "vocabulary": "The student wants new vocabulary. Give 3-5 related words with pronunciation and a short example for each.",
    "practice": "The student wants to practice conversation. Respond naturally in simple Spanish, then provide an English translation below.",
    "quiz": "The student wants to be quizzed. Ask them ONE simple question about Spanish. Wait for their answer.",
    "unknown": "The student said something outside Spanish learning. Gently redirect them back to learning Spanish.",
}

def get_tutor_response(chat, user_message: str, intent: str) -> str:
    """
    Sends user message to the tutor chat session.
    Prepends intent-specific instructions so the response style matches the intent.
    """
    # Combine base instruction + intent-specific instruction
    intent_context = INTENT_INSTRUCTIONS.get(intent, INTENT_INSTRUCTIONS["unknown"])

    # We prepend the intent hint to the user message so the model knows
    # what kind of response is expected — without changing the chat history format
    enriched_message = f"[Student intent: {intent}]\n[Instruction: {intent_context}]\n\nStudent said: {user_message}"

    response = chat.send_message(enriched_message)
    return response.text

def main():
    client = genai.Client(api_key=API_KEY)

    chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=BASE_SYSTEM_INSTRUCTION,
        ),
    )

    print("=" * 55)
    print("  Spanish Tutor (Phase 3 — Intent Detection)")
    print("  I now understand what you are trying to do!")
    print("  Type 'exit' to quit | 'history' to see chat log")
    print("=" * 55)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Profe: ¡Hasta luego! (See you later!)")
            break

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