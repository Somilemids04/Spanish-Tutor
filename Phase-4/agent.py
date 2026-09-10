"""
agent.py — Phase 4

The Teacher Agent.
- Registers tools with Gemini using function declarations
- Sends user messages + tool definitions to Gemini
- Handles tool call responses (ReAct loop)
- Returns the final text response

This is where the "agent" logic lives.
chatbot.py is just the UI. tools.py is just functions.
agent.py is the brain that connects them.
"""
import json
from google import genai
from google.genai import types
from tools import run_tool

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """\
You are Profe, a friendly and patient Spanish language teacher.
You have access to tools: translate_word, explain_grammar, get_vocabulary, generate_quiz.

Rules:
- Always use a tool when the student's request clearly matches one.
- Never make up translations or grammar rules — use the translate or grammar tool.
- After receiving a tool result, craft a warm, encouraging response using that information.
- Keep responses concise and beginner-friendly.
- If unsure which tool to use, just respond conversationally.
"""