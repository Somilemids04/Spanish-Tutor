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