# Phase 2: Conversation Memory

## Objective

Make the tutor remember everything said in the current session.
Ask "what did I just say?" and it will know.

---

## What You Learn Here

- Why LLMs are stateless and how to work around it
- What a "context window" is
- How conversation history works (roles: user / model)
- Why sending more text costs more tokens

---

## How It Works

The LLM itself has no memory. The trick is simple: every time you send
a message, you also send the **entire conversation history** along with it.
Gemini re-reads the full transcript and responds as if it remembers.

```
Turn 1 → send: ["hi"]
Turn 2 → send: ["hi",  "Hola!",  "what did I say?"]
Turn 3 → send: ["hi",  "Hola!",  "what did I say?",  "You said hi",  ...]
```

The history grows with every turn. The Gemini SDK handles this
automatically via a chat session object.

---

## What Changed from Phase 1

| | Phase 1 | Phase 2 |
|---|---|---|
| API call | `generate_content()` | `chat.send_message()` |
| History | Not sent | Full history sent every turn |
| Memory | None | Full session memory |

Only one meaningful code change — everything else is the same.

---

## Folder Structure

```
spanish-tutor/
├── .env
├── .gitignore
├── requirements.txt
├── phase1/
│   ├── chatbot.py
│   └── README.md
└── phase2/
    ├── chatbot.py        ← new file
    └── README.md         ← this file
```

Phase 1 stays untouched. Each phase is independent.

---

## Running Phase 2

No new packages needed. Just activate venv and run:

**Mac/Linux:**
```bash
cd Desktop/Spanish_Tutor
source venv/bin/activate
python3 phase2/chatbot.py
```

**Windows:**
```bash
cd Desktop\Spanish_Tutor
venv\Scripts\activate
python phase2\chatbot.py
```

You should see:
```
==================================================
  Spanish Tutor (Phase 2 — with memory)
  I will remember everything you tell me!
  Type 'exit' to quit.
  Type 'history' to see the conversation so far.
==================================================

You:
```

---

## Special Commands

| Command | What it does |
|---|---|
| `exit` | Quits the program |
| `history` | Prints the full message list being sent to Gemini |

Use `history` to see exactly what the API receives on every call.
It's the best way to understand how memory actually works under the hood.

---

## Test It With This Exact Sequence

```
You: My name is Alex
You: How do you say "good morning" in Spanish?
You: What is my name?
You: What Spanish word did I just learn?
You: history
```

Expected results:
- It remembers your name ✅
- It remembers "buenos días" ✅
- `history` shows the full growing message list ✅

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Still forgets things | Make sure you're running `phase2/chatbot.py` not `phase1` |
| `(venv)` not showing | Run the activate command again |
| 503 UNAVAILABLE | Gemini free tier busy — wait 2 min and retry |
| 429 Too Many Requests | Rate limit — wait 1 minute |

### If 503 errors keep happening — switch model

In `phase2/chatbot.py`, find line 44 and change:
```python
# from:
MODEL_NAME = "gemini-2.5-flash"

# to:
MODEL_NAME = "gemini-1.5-flash"
```

---

## Completion Checklist

- [ ] Tutor remembers your name across turns
- [ ] Tutor recalls Spanish words learned earlier in the session
- [ ] `history` command shows the growing message list
- [ ] You can explain: "The LLM doesn't really remember — I send the full transcript each time"

---

## Key Concept Before Moving On

Memory here is an illusion — you're just sending more text.
This works fine for short sessions, but has two limits:
1. Cost — more tokens sent = more API usage
2. Context window — there's a maximum amount of text Gemini can read at once

For a learning project this is fine. Phase 11 (long-term memory) solves
this properly using a database instead of sending everything every time.

---

## Phase Status

- [x] Phase 1 — Basic chatbot
- [x] Phase 2 — Conversation memory (this phase)
- [ ] Phase 3 — Intent detection (next)