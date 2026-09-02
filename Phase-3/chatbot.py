"""
Phase 3: Intent Detection

What's new vs Phase 2:
- Every message is classified by detect_intent() before the tutor responds.
- The detected intent is shown to you in the terminal (so you can see it working).
- The tutor's system prompt is updated per-intent to shape the response style.
- intent.py handles all classification logic — chatbot.py just routes.

Run with: python3 phase3/chatbot.py
"""