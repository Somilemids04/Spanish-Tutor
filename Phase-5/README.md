# Phase 5: Multiple Specialized Agents

## Objective

Replace the single Teacher Agent with four specialized agents, each
an expert in one domain. A Supervisor routes every message to the
right specialist automatically.

---

## What You Learn Here

- The Supervisor pattern (most common multi-agent architecture)
- Why specialization makes agents better and easier to maintain
- How agents communicate through a coordinator
- How to organize code across multiple files and subfolders

---

## Agents

| Agent | Name | Handles |
|---|---|---|
| Supervisor | — | Routing only, never responds directly |
| Grammar Agent | Gramatica | Grammar rules, conjugation, structure |
| Vocabulary Agent | Vocabulario | Words, translations, themed lists |
| Quiz Agent | Examen | Questions, answers, evaluation |
| Conversation Agent | Conversacion | Free Spanish practice |

---

## What Changed from Phase 4

| | Phase 4 | Phase 5 |
|---|---|---|
| Agents | 1 (does everything) | 4 specialists + 1 supervisor |
| Routing | Tool calls | Supervisor decides |
| Files | 3 | 7 (agents in subfolder) |
| API calls per turn | 1-2 | 2 (route + respond) |

---

## Folder Structure

```
spanish-tutor/
└── Phase-5/
    ├── chatbot.py              ← terminal UI only
    ├── supervisor.py           ← routing logic
    ├── agents/
    │   ├── __init__.py         ← makes agents/ a Python package
    │   ├── grammar_agent.py
    │   ├── vocabulary_agent.py
    │   ├── quiz_agent.py
    │   └── conversation_agent.py
    └── README.md
```

---

## Running Phase 5

**Mac/Linux:**
```bash
cd Desktop/Spanish_Tutor
source venv/bin/activate
python3 Phase-5/chatbot.py
```

**Windows:**
```bash
cd Desktop\Spanish_Tutor
venv\Scripts\activate
python Phase-5\chatbot.py
```

---

## What You See in the Terminal

Every response now shows which agent handled it:

```
You: explain ser vs estar
  [Routed to: Gramatica (Grammar Agent)]

In Spanish, "ser" is used for permanent...

You: quiz me on colors
  [Routed to: Examen (Quiz Agent)]

What color is "rojo"?
A) Blue  B) Red  C) Green  D) Yellow
```

---

## Test It With These Messages

```
You: explain verb conjugation         → Grammar Agent
You: give me words for food           → Vocabulary Agent
You: quiz me on numbers               → Quiz Agent
You: hola como estas                  → Conversation Agent
You: B                                → Quiz Agent (answering a question)
You: how do you say "water"           → Vocabulary Agent
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: supervisor` | Run from root: `python3 Phase-5/chatbot.py` |
| `ModuleNotFoundError: agents` | Same — must run from `Spanish_Tutor` root |
| Always routes to conversation | Rephrase more explicitly e.g. "quiz me" not just "test" |
| 404 model not found | Set `MODEL_NAME = "gemini-3.6-flash"` in all agent files |

---

## Completion Checklist

- [ ] Each message routes to the correct specialist
- [ ] `[Routed to: ...]` label shows the right agent name
- [ ] Quiz agent continues a multi-turn quiz (ask → answer → feedback)
- [ ] You can explain the Supervisor pattern in your own words

---

## Key Concept Before Moving On

The supervisor pattern = a manager who delegates, never does.
Each agent has its own history — they don't share context yet.
Phase 6 (Orchestration) fixes this: agents will share state and
hand off context to each other for more complex workflows.

---

## Phase Status

- [x] Phase 1 — Basic chatbot
- [x] Phase 2 — Conversation memory
- [x] Phase 3 — Intent detection
- [x] Phase 4 — First AI agent
- [x] Phase 5 — Multiple specialized agents (this phase)
- [ ] Phase 6 — Agent orchestration (next)
