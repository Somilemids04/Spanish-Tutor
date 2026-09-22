# Phase 6: Agent Orchestration

## Objective

Give all agents a shared brain. Every agent can now read and write
to a common state — words learned, quiz scores, student name —
so the quiz agent knows what vocabulary was just taught.

---

## What You Learn Here

- What shared state is and why it matters
- How LangGraph works (nodes, edges, conditional routing)
- Why graph-based orchestration beats if/else routing
- How agents hand off context to each other

---

## What Changed from Phase 5

| | Phase 5 | Phase 6 |
|---|---|---|
| Agent memory | Each agent isolated | All agents share one state |
| Routing | Supervisor if/else | LangGraph conditional edges |
| Quiz personalization | Generic questions | Quizzes on words just learned |
| State visibility | Hidden | `status` command shows everything |

---

## New Package: LangGraph

Install before running:
```bash
pip install langgraph
```

Add to `requirements.txt`:
```
google-genai
python-dotenv
langgraph
```

---

## Folder Structure

```
Spanish_Tutor/
└── Phase-6/
    ├── __init__.py         ← makes Phase-6 a Python package
    ├── chatbot.py          ← terminal UI + state management
    ├── graph.py            ← LangGraph workflow definition
    ├── state.py            ← shared state schema
    ├── nodes/
    │   ├── __init__.py
    │   ├── supervisor.py   ← routing node
    │   ├── grammar.py      ← grammar node
    │   ├── vocabulary.py   ← vocabulary node (writes words_learned)
    │   ├── quiz.py         ← quiz node (reads words_learned)
    │   └── conversation.py ← conversation node
    └── README.md
```

---

## Running Phase 6

**Mac/Linux:**
```bash
cd Desktop/Spanish_Tutor
source venv/bin/activate
pip install langgraph
python3 -m  chatbot
```

**Windows:**
```bash
cd Desktop\Spanish_Tutor
venv\Scripts\activate
pip install langgraph
python -m  chatbot
```

> ⚠️ Note: run with `python3 -m  chatbot` not `python3 Phase-6/chatbot.py`
> The `-m` flag is needed for the package imports to work correctly.

---

## Special Commands

| Command | What it does |
|---|---|
| `exit` | Quits and shows quiz score |
| `status` | Shows full shared state (words learned, score, last agent) |

---

## Test This Exact Flow (shows shared state in action)

```
You: give me 5 words about animals
  → Vocabulary Agent teaches: perro, gato, pájaro, pez, caballo

You: status
  → shows words_learned: ['perro', 'gato', 'pájaro', 'pez', 'caballo']

You: quiz me
  → Quiz Agent quizzes on the EXACT words just learned

You: my name is Somil
  → Conversation Agent saves name to shared state

You: status
  → shows student_name: Somil
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: Phase-6` | Use `python3 -m  chatbot` not `python3 Phase-6/chatbot.py` |
| `ModuleNotFoundError: langgraph` | Run `pip install langgraph` with venv active |
| Quiz doesn't use learned words | Type `status` to confirm `words_learned` is populated first |
| 404 model not found | Set `MODEL_NAME = "gemini-3.6-flash"` in all node files |

---

## Completion Checklist

- [ ] `pip install langgraph` succeeded
- [ ] `status` command shows shared state updating across turns
- [ ] Quiz agent uses words from vocabulary session
- [ ] Student name saved after introduction
- [ ] You can explain: nodes, edges, shared state in your own words

---

## Key Concept Before Moving On

LangGraph = a workflow engine for agents.
Shared state = agents talking to each other without direct calls.
This is the foundation of everything from Phase 7 onward —
progress tracking, lesson planning, and long-term memory all
depend on state flowing cleanly between agents.

---

## Phase Status

- [x] Phase 1 — Basic chatbot
- [x] Phase 2 — Conversation memory
- [x] Phase 3 — Intent detection
- [x] Phase 4 — First AI agent
- [x] Phase 5 — Multiple specialized agents
- [x] Phase 6 — Agent orchestration (this phase)
- [ ] Phase 7 — User progress tracking (next)
