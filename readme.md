# Spanish Tutor — Agentic AI Project

A Spanish language tutor built step-by-step from a simple chatbot to a
voice-enabled AI agent with long-term memory. Built entirely in Python,
100% free to run.

---

## Project Roadmap (14 Phases)

| Phase | Title | Status |
|-------|-------|--------|
| 1 | Basic AI chatbot | ✅ Done |
| 2 | Conversation memory | ✅ Done |
| 3 | Intent detection | ✅ Done |
| 4 | First AI agent (Teacher Agent) | ✅ Done |
| 5 | Multiple specialized agents (Grammar, Vocabulary, etc.) | ✅ Done |
| 6 | Agent orchestration | ✅ Done |
| 7 | User progress tracking | ✅ Done |
| 8 | Quiz and evaluation | ✅ Done |
| 9 | Lesson planning | 🔲 Next |
| 10 | Retrieval-Augmented Generation (RAG) | 🔲 |
| 11 | Long-term memory | 🔲 |
| 12 | Voice support (STT + TTS) | 🔲 |
| 13 | Advanced multi-agent workflows | 🔲 |
| 14 | Production deployment and optimization | 🔲 |

---

## Final Goal

By Phase 14 you will have a fully working:
- 🎙️ Voice-enabled Spanish tutor (speak to it, it speaks back)
- 🧠 Long-term memory (remembers you across sessions)
- 🤖 Multi-agent system (specialized agents for grammar, vocabulary, quizzes)
- 🚀 Production-ready deployment

100% built using free tools and free API tiers.

---

## Tech Stack (introduced gradually per phase)

| Tool | Used From | Purpose |
|------|-----------|---------|
| Python | Phase 1 | Core language |
| Gemini API free tier | Phase 1 | LLM backbone |
| python-dotenv | Phase 1 | Load API keys safely |
| LangGraph | Phase 6 | Agent orchestration + shared state |
| ChromaDB | Phase 10 | Local vector database (free, no cloud) |
| faster-whisper | Phase 12 | Speech-to-text (runs locally, free) |
| pyttsx3 / Edge TTS | Phase 12 | Text-to-speech (free) |

---

## Folder Structure (full project)

```
Spanish_Tutor/
├── .env                    # Your API key (never share this)
├── .env.example            # Template showing required variables
├── .gitignore              # Keeps secrets out of git
├── requirements.txt        # All Python dependencies
├── README.md               # This file
│
├── Phase-1/
│   ├── chatbot.py          # Basic stateless chatbot
│   └── README.md
│
├── Phase-2/
│   ├── chatbot.py          # Chatbot with conversation memory
│   └── README.md
│
├── Phase-3/
│   ├── chatbot.py          # Intent-aware chatbot
│   ├── intent.py           # Intent classification module
│   └── README.md
│
├── Phase-4/
│   ├── chatbot.py          # Terminal UI only
│   ├── agent.py            # Teacher Agent + ReAct loop
│   ├── tools.py            # Tool functions
│   └── README.md
│
├── Phase-5/
│   ├── chatbot.py
│   ├── supervisor.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── grammar_agent.py
│   │   ├── vocabulary_agent.py
│   │   ├── quiz_agent.py
│   │   └── conversation_agent.py
│   └── README.md
│
├── Phase-6/
│   ├── __init__.py
│   ├── chatbot.py
│   ├── graph.py            # LangGraph workflow
│   ├── state.py            # Shared state schema
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── supervisor.py
│   │   ├── grammar.py
│   │   ├── vocabulary.py
│   │   ├── quiz.py
│   │   └── conversation.py
│   └── README.md
│
├── Phase-7/
│   ├── __init__.py
│   ├── chatbot.py
│   ├── graph.py
│   ├── state.py
│   ├── progress_tracker.py # Saves/loads progress to JSON
│   ├── data/
│   │   └── progress.json   # Auto-created on first run
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── supervisor.py
│   │   ├── grammar.py
│   │   ├── vocabulary.py
│   │   ├── quiz.py
│   │   └── conversation.py
│   └── README.md
│
├── Phase-8/
│   ├── __init__.py
│   ├── chatbot.py
│   ├── graph.py
│   ├── state.py
│   ├── quiz_engine.py      # Structured quiz logic + evaluation reports
│   ├── progress_tracker.py # Updated: saves topic_scores
│   ├── data/
│   │   └── progress.json
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── supervisor.py
│   │   ├── grammar.py
│   │   ├── vocabulary.py
│   │   ├── quiz.py         # Rewritten: uses quiz_engine
│   │   └── conversation.py
│   └── README.md
│
├── Phase-9/                # Lesson planning (coming soon)
├── Phase-10/               # RAG (coming soon)
├── Phase-11/               # Long-term memory (coming soon)
├── Phase-12/               # Voice support (coming soon)
├── Phase-13/               # Advanced workflows (coming soon)
└── Phase-14/               # Production deployment (coming soon)
```

---

## Prerequisites (one-time setup)

### 1. Install Python

```
python3 --version
```
If not installed: https://www.python.org/downloads/
During install on Windows, check "Add Python to PATH".

### 2. Get a free Gemini API key

Go to: https://aistudio.google.com/apikey
Free tier is enough for all 14 phases.

---

## First-Time Setup (do this once)

```bash
# Mac/Linux
cd Desktop/Spanish_Tutor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Windows
cd Desktop\Spanish_Tutor
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add your API key to `.env`:
```
GEMINI_API_KEY=your_actual_key_here
```

---

## Running Each Phase

Always run from the `Spanish_Tutor` root with `(venv)` active.

**Mac/Linux:**
```bash
python3 Phase-1/chatbot.py
python3 Phase-2/chatbot.py
python3 Phase-3/chatbot.py
python3 Phase-4/chatbot.py
python3 Phase-5/chatbot.py
python3 Phase-6/chatbot.py
python3 Phase-7/chatbot.py
python3 Phase-8/chatbot.py
```

**Windows:**
```bash
python Phase-1\chatbot.py
python Phase-2\chatbot.py
python Phase-3\chatbot.py
python Phase-4\chatbot.py
python Phase-5\chatbot.py
python Phase-6\chatbot.py
python Phase-7\chatbot.py
python Phase-8\chatbot.py
```

---

## Terminal Commands (Phase 6 onward)

| Command | What it does |
|---|---|
| `exit` | Saves progress and quits |
| `status` | Shows live shared state |
| `progress` | Full progress report with scores |
| `quiz me on [topic]` | Start a quiz (Phase 8+) |
| `quiz intermediate on [topic]` | Quiz with difficulty level |

---

## Gemini Model Reference

Use this in ALL files across ALL phases:
```python
MODEL_NAME = "gemini-2.0-flash"
```

⚠️ Do NOT use `gemini-1.5-flash` or `gemini-3.6-flash`.

---

## Requirements

```
google-genai
python-dotenv
langgraph
```

Install:
```bash
pip install -r requirements.txt
```

LangGraph needed from Phase 6 onward:
```bash
pip install langgraph
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `command not found: python` | Use `python3` (Mac/Linux) |
| `(venv)` not showing | Run activate command again |
| `ModuleNotFoundError` | Activate venv + `pip install -r requirements.txt` |
| `ModuleNotFoundError: phase6/7/8` | Use relative imports inside phase folders |
| `ModuleNotFoundError: langgraph` | `pip install langgraph` |
| `GEMINI_API_KEY not found` | Check `.env` is in root, not inside a phase folder |
| SSL certificate error | `pip install --upgrade certifi` |
| 404 model not found | Set `MODEL_NAME = "gemini-2.0-flash"` |
| 503 UNAVAILABLE | Gemini busy — wait 2 min and retry |
| 429 Too Many Requests | Rate limit — wait 1 minute |
| Quiz stuck mid-session | Type any letter (A/B/C/D) to continue |
| Progress not saving | Make sure `data/` folder exists inside the phase folder |
| Name not recognized | Use English: "my name is X" or Spanish: "me llamo X" |

---

## Git Commands

```bash
# First time
git init
git add .
git commit -m "Phase 8 complete"
git remote add origin https://github.com/YOUR_USERNAME/spanish-tutor.git
git branch -M main
git push -u origin main

# Every phase after
git add .
git commit -m "Phase X complete"
git push
```

---

## How to Think About This Project

| Phase | Core Question |
|-------|--------------|
| 1 | How do I talk to an LLM from Python? |
| 2 | How do I give it memory? |
| 3 | How do I make it understand intent? |
| 4 | What is an AI agent? |
| 5 | How do agents specialize? |
| 6 | How do agents coordinate? |
| 7 | How do I track what a user has learned? |
| 8 | How do I evaluate learning? |
| 9 | How do I plan lessons dynamically? |
| 10 | How do I give the AI access to a knowledge base? |
| 11 | How do I remember things across sessions? |
| 12 | How do I add voice? |
| 13 | How do complex agent workflows work? |
| 14 | How do I ship this for real users? |

Don't skip phases. Each one builds the intuition needed for the next.
