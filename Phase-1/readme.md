# Phase 1: Basic AI Chatbot

## Objective

Build the simplest possible Spanish tutor — you type a message, the AI
responds. No memory, no agents, no tools. Just one API call per message.

---

## What You Learn Here

- How to call an LLM API from Python
- What a system prompt is and why it controls behavior
- Why LLMs are stateless by default
- How to keep API keys safe using `.env`

---

## How It Works

```
You type  →  Python sends message + system prompt to Gemini  →  Gemini replies  →  printed to terminal
```

Every message is sent in isolation. The tutor has zero memory of
previous messages. This is intentional — Phase 2 fixes it.

---

## Folder Structure

```
spanish-tutor/
├── .env                  ← your API key lives here
├── .gitignore
├── requirements.txt
└── phase1/
    └── chatbot.py        ← the entire Phase 1 program
```

---

## Setup (one-time)

### Step 1 — Get a free Gemini API key
Go to https://aistudio.google.com/apikey and generate a key.

### Step 2 — Open your terminal

- **Mac**: Spotlight (Cmd+Space) → Terminal
- **Windows**: Start menu → cmd or PowerShell

### Step 3 — Navigate to the project folder

```bash
cd Desktop/Spanish_Tutor
```

### Step 4 — Create a virtual environment

```bash
python3 -m venv venv
```

### Step 5 — Activate it

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You'll see `(venv)` at the start of your terminal line. ✅

### Step 6 — Install packages

```bash
pip install -r requirements.txt
```

### Step 7 — Add your API key

Open `.env` and replace the placeholder:
```
GEMINI_API_KEY=your_actual_key_here
```

---

## Running Phase 1

Make sure `(venv)` is active, then:

**Mac/Linux:**
```bash
python3 phase1/chatbot.py
```

**Windows:**
```bash
python phase1\chatbot.py
```

You should see:
```
==================================================
  Spanish Tutor (Phase 1 — no memory yet)
  Type 'exit' to quit.
==================================================

You:
```

---

## Test It

Try these messages in order:

```
You: How do you say "thank you" in Spanish?
You: My name is Alex
You: What is my name?          ← it will NOT remember. This is expected.
You: exit
```

The fact that it forgets your name proves the system is stateless.
That's not a bug — it's the core lesson of Phase 1.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `command not found: python` | Use `python3` instead |
| `ModuleNotFoundError` | Activate venv, then run `pip install -r requirements.txt` |
| `GEMINI_API_KEY not found` | Check `.env` is in the root folder, not inside `phase1/` |
| SSL certificate error | Run `pip install --upgrade certifi` |
| 503 error | Gemini free tier overloaded — wait 2 min and retry |

---

## Completion Checklist

- [ ] Script runs without errors
- [ ] Tutor responds in character as a Spanish teacher
- [ ] You confirmed it forgets your name between messages
- [ ] You can explain in your own words why it forgets

---

## Key Concept Before Moving On

The LLM is a pure function: input in, output out, nothing stored.
Every call is completely independent. This is why it forgets.
Phase 2 fixes this by sending the full conversation history every time.

---

## Phase Status

- [x] Phase 1 — Basic chatbot (this phase)
- [ ] Phase 2 — Conversation memory (next)