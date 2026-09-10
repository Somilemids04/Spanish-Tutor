# Phase 4: First AI Agent (Teacher Agent)

## Objective

Build your first real AI Agent — a system that has a goal, a set of
tools it can call, and decides which tool to use on its own.

---

## What You Learn Here

- What makes something an "agent" vs a chatbot
- What function calling / tool use is
- How the ReAct loop works (Reason → Act → Observe → Respond)
- Why we split code into agent.py / tools.py / chatbot.py

---

## The ReAct Loop (core agent pattern)

```
User message
     │
     ▼
Gemini reasons: "I should call translate_word()"
     │
     ▼
Python runs translate_word() → returns result
     │
     ▼
Gemini reads result → writes final response
     │
     ▼
Printed to terminal
```

---

## Tools Available

| Tool | Triggered when student says |
|---|---|
| `translate_word` | "how do you say...", "what is X in Spanish" |
| `explain_grammar` | "why does...", "explain...", "what is the rule for..." |
| `get_vocabulary` | "give me words", "teach me colors/food/family" |
| `generate_quiz` | "quiz me", "test me", "ask me a question" |

---

## What Changed from Phase 3

| | Phase 3 | Phase 4 |
|---|---|---|
| Decision maker | You (if/else routing) | Gemini (agent reasoning) |
| Tools | Prompt instructions | Real Python functions |
| Files | 2 | 3 (agent.py added) |
| API calls per turn | 2 | 1-2 (only calls tool if needed) |

---

## Folder Structure

```
spanish-tutor/
└── phase4/
    ├── chatbot.py    ← terminal UI only
    ├── agent.py      ← agent logic + ReAct loop
    ├── tools.py      ← plain Python tool functions
    └── README.md     ← this file
```

---

## Running Phase 4

**Mac/Linux:**
```bash
cd Desktop/Spanish_Tutor
source venv/bin/activate
python3 phase4/chatbot.py
```

**Windows:**
```bash
cd Desktop\Spanish_Tutor
venv\Scripts\activate
python phase4\chatbot.py
```

---

## What You See in the Terminal

When the agent uses a tool, you'll see it:

```
You: how do you say dog in Spanish?
  [Agent calling tool: translate_word({'word': 'dog', 'direction': 'en_to_es'})]

Profe: Dog in Spanish is "perro" (PEH-rro)...
```

If no tool is needed (e.g. "hello"), the agent responds directly
without calling any tool.

---

## Test It With These Messages

```
You: how do you say "cat" in Spanish?       ← triggers translate_word
You: explain ser vs estar                    ← triggers explain_grammar
You: give me 5 words about food             ← triggers get_vocabulary
You: quiz me on colors                      ← triggers generate_quiz
You: hola, how are you?                     ← no tool, direct response
You: history                                ← shows full conversation
```

Watch the `[Agent calling tool: ...]` line appear (or not) for each message.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: agent` | Run from root: `python3 phase4/chatbot.py` |
| `ModuleNotFoundError: tools` | Same — must run from `Spanish_Tutor` root |
| Tool never called | Rephrase — try "how do you say X in Spanish?" explicitly |
| 404 model not found | `MODEL_NAME = "gemini-3.6-flash"` in `agent.py` |
| 503 / 429 errors | Wait 1-2 minutes, free tier rate limit |

---

## Completion Checklist

- [ ] `[Agent calling tool: ...]` appears for translate/grammar/vocab/quiz requests
- [ ] Agent responds directly (no tool) for greetings and small talk
- [ ] `history` shows the full conversation including tool calls
- [ ] You can explain the ReAct loop in your own words

---

## Key Concept Before Moving On

The agent pattern = give an LLM tools + let it decide.
You no longer write routing logic — the model reasons about what to do.
In Phase 5 the "tools" become entire specialized agents.
That's the jump from one agent to multi-agent.

---

## Phase Status

- [x] Phase 1 — Basic chatbot
- [x] Phase 2 — Conversation memory
- [x] Phase 3 — Intent detection
- [x] Phase 4 — First AI agent (this phase)
- [ ] Phase 5 — Multiple specialized agents (next)
