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
| 7 | User progress tracking | 🔲 Next |
| 8 | Quiz and evaluation | 🔲 |
| 9 | Lesson planning | 🔲 |
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
│   ├── tools.py            # Tool functions (translate, grammar, vocab, quiz)
│   └── README.md
│
├── Phase-5/
│   ├── chatbot.py          # Terminal UI only
│   ├── supervisor.py       # Supervisor routing agent
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── grammar_agent.py
│   │   ├── vocabulary_agent.py
│   │   ├── quiz_agent.py
│   │   └── conversation_agent.py
│   └── README.md
│
├── Phase-6/                
│   ├── __init__.py         # makes it a Python package
│   ├── chatbot.py          # terminal UI + shared state management
│   ├── graph.py            # LangGraph workflow definition
│   ├── state.py            # shared state schema (TutorState)
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── supervisor.py   # routing node
│   │   ├── grammar.py      # grammar node
│   │   ├── vocabulary.py   # vocabulary node (writes words_learned)
│   │   ├── quiz.py         # quiz node (reads words_learned)
│   │   └── conversation.py # conversation node
│   └── README.md
│
├── Phase-7/                # Progress tracking (coming soon)
├── Phase-8/                # Quiz + evaluation (coming soon)
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

Check if you have it:
```
python3 --version
```
If not installed: https://www.python.org/downloads/
During install on Windows, check "Add Python to PATH".

### 2. Get a free Gemini API key

Go to: https://aistudio.google.com/apikey
Sign in with a Google account and generate a key. Free tier is enough for all phases.

---

## First-Time Project Setup (do this once)

### Step 1 — Open your terminal

- **Mac**: Spotlight (Cmd+Space) → type Terminal → Enter
- **Windows**: Start menu → search cmd or PowerShell → Enter

### Step 2 — Navigate to the project

```bash
cd Desktop/Spanish_Tutor
```
Windows: use backslashes `cd Desktop\Spanish_Tutor`

### Step 3 — Create a virtual environment

```bash
python3 -m venv venv
```

### Step 4 — Activate it

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Windows (cmd):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

You will see `(venv)` at the start of your terminal line. ✅

> You must activate every time you open a new terminal.

### Step 5 — Install packages

```bash
pip install -r requirements.txt
```

---

## Running Each Phase

Always run from the `Spanish_Tutor` root folder with `(venv)` active.

**Mac/Linux:**
```bash
python3 Phase-1/chatbot.py
python3 Phase-2/chatbot.py
python3 Phase-3/chatbot.py
python3 Phase-4/chatbot.py
python3 Phase-5/chatbot.py
python3 Phase-6/chatbot.py     # Phase 6 uses relative imports
```

**Windows:**
```bash
python Phase-1\chatbot.py
python Phase-2\chatbot.py
python Phase-3\chatbot.py
python Phase-4\chatbot.py
python Phase-5\chatbot.py
python Phase-6\chatbot.py
```

> ⚠️ Phase 6 Note: If you get `ModuleNotFoundError`, make sure all
> imports inside Phase-6 files use relative imports (e.g. `from .graph import build_graph`)
> not absolute imports (e.g. `from phase6.graph import build_graph`).

---

## Gemini Model Reference

Use this model name in ALL files across ALL phases:

```python
MODEL_NAME = "gemini-3.6-flash"
```

⚠️ Do NOT use `gemini-1.5-flash` or `gemini-2.0-flash` — these either
do not exist or have limited availability on the free tier.

---

## Requirements (install all at once)

```
google-genai
python-dotenv
langgraph
```

Install with:
```bash
pip install -r requirements.txt
```

Or install LangGraph separately when starting Phase 6:
```bash
pip install langgraph
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `command not found: python` | Use `python3` instead (Mac/Linux) |
| `(venv)` not showing | Run the activate command again |
| `ModuleNotFoundError` | Activate venv first, then `pip install -r requirements.txt` |
| `ModuleNotFoundError: agent` or `tools` | Run from root folder, not from inside the phase folder |
| `ModuleNotFoundError: phase6` | Use relative imports inside Phase-6 files (`from .graph import...`) |
| `ModuleNotFoundError: langgraph` | Run `pip install langgraph` with venv active |
| `SyntaxError: invalid decimal literal` | You used `from Phase-6.x import` — use `from .x import` instead |
| `GEMINI_API_KEY not found` | Check `.env` is in root folder, not inside a phase folder |
| SSL certificate error | Run `pip install --upgrade certifi` |
| 404 model not found | Set `MODEL_NAME = "gemini-2.0-flash"` in the relevant file |
| 503 UNAVAILABLE | Gemini free tier busy — wait 2 min and retry |
| 429 Too Many Requests | Rate limit hit — wait 1 minute |
| Intent always `unknown` | Set `MODEL_NAME = "gemini-2.0-flash"` in `Phase-3/intent.py` |
| No such file or directory | Check folder name matches exactly — folders are `Phase-1`, `Phase-2` etc. |

---

## Git Commands

```bash
# First time
git init
git add .
git commit -m "Phase 6 complete"
git remote add origin https://github.com/YOUR_USERNAME/spanish-tutor.git
git branch -M main
git push -u origin main

# Every phase after that
git add .
git commit -m "Phase X complete"
git push
```

---

## How to Think About This Project

Each phase answers one question:

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
