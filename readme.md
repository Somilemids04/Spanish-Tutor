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
| 4 | First AI agent (Teacher Agent) | 🔲 Next |
| 5 | Multiple specialized agents (Grammar, Vocabulary, etc.) | 🔲 |
| 6 | Agent orchestration | 🔲 |
| 7 | User progress tracking | 🔲 |
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
| FastAPI | Phase 4 | Web server for the agent |
| LangChain | Phase 5 | Agent + tool framework |
| LangGraph | Phase 6 | Agent orchestration |
| ChromaDB | Phase 10 | Local vector database (free, no cloud) |
| faster-whisper | Phase 12 | Speech-to-text (runs locally, free) |
| pyttsx3 / Edge TTS | Phase 12 | Text-to-speech (free) |

---

## Folder Structure (full project)

```
spanish-tutor/
├── .env                    # Your API key (never share this)
├── .env.example            # Template showing required variables
├── .gitignore              # Keeps secrets out of git
├── requirements.txt        # All Python dependencies
├── README.md               # This file
│
├── phase1/
│   ├── chatbot.py          # Basic stateless chatbot
│   └── README.md
│
├── phase2/
│   ├── chatbot.py          # Chatbot with conversation memory
│   └── README.md
│
├── phase3/
│   ├── chatbot.py          # Intent-aware chatbot
│   ├── intent.py           # Intent classification module
│   └── README.md
│
├── phase4/                 # Teacher Agent (coming soon)
├── phase5/                 # Multiple agents (coming soon)
├── phase6/                 # Orchestration (coming soon)
├── phase7/                 # Progress tracking (coming soon)
├── phase8/                 # Quiz + evaluation (coming soon)
├── phase9/                 # Lesson planning (coming soon)
├── phase10/                # RAG (coming soon)
├── phase11/                # Long-term memory (coming soon)
├── phase12/                # Voice support (coming soon)
├── phase13/                # Advanced workflows (coming soon)
└── phase14/                # Production deployment (coming soon)
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

### Step 6 — Add your API key

Open `.env` and replace the placeholder:
```
GEMINI_API_KEY=your_actual_key_here
```
Save the file. Never share this or commit it to git.

---

## Running Each Phase

Always run from the `Spanish_Tutor` root folder with `(venv)` active.

**Mac/Linux:**
```bash
python3 phase1/chatbot.py
python3 phase2/chatbot.py
python3 phase3/chatbot.py
```

**Windows:**
```bash
python phase1\chatbot.py
python phase2\chatbot.py
python phase3\chatbot.py
```

Each phase folder has its own README.md with specific instructions.

---

## Gemini Model Reference

If you get a 404 or 503 error, use this model name in all files:

```python
MODEL_NAME = "gemini-2.0-flash"
```

This is the most stable free-tier model for the current SDK version.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `command not found: python` | Use `python3` instead (Mac/Linux) |
| `(venv)` not showing | Run the activate command again |
| `ModuleNotFoundError` | Activate venv first, then `pip install -r requirements.txt` |
| `GEMINI_API_KEY not found` | Check `.env` is in root folder, not inside a phase folder |
| SSL certificate error | Run `pip install --upgrade certifi` |
| 404 model not found | Change model to `gemini-2.0-flash` in the relevant file |
| 503 UNAVAILABLE | Gemini free tier busy — wait 2 min and retry |
| 429 Too Many Requests | Rate limit hit — wait 1 minute |
| Intent always `unknown` | Model name wrong in `intent.py` — set to `gemini-2.0-flash` |

---

## Git Commands (push updates)

```bash
git add .
git commit -m "Phase 3 complete"
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
