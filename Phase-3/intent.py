"""
intent.py — Phase 3

Single responsibility: detect what the user is trying to do.
Takes raw user text, returns a clean intent label.

Intents supported:
- greeting        : "hola", "hi", "hello"
- translation     : "how do you say X", "what is X in Spanish"
- grammar         : "why is it X", "explain this grammar"
- vocabulary      : "what does X mean", "give me new words"
- practice        : "let's practice", "talk to me in Spanish"
- quiz            : "quiz me", "test me", "ask me a question"
- unknown         : anything that doesn't fit above
"""