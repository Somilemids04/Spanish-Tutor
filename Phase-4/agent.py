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
