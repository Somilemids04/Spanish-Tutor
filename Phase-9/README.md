# Phase 9: Lesson Planning

## Objective

Give the AI tutor the ability to **analyze your progress** and generate a
**personalized lesson plan** — a structured, step-by-step study session based
on what you've covered, what you struggle with, and what you haven't seen yet.

---

## What You Learn Here

- How AI systems can use stored data to make personalized decisions
- How to build a multi-step state machine inside a LangGraph node
- How lesson planning differs from simple Q&A (structured vs. reactive)
- How to route a new intent ("lesson") into an existing multi-agent graph

---

## How It Works

```
Student types "lesson"
       ↓
Supervisor detects lesson intent → routes to Lesson Node
       ↓
lesson_planner.py reads progress.json
  - Finds weak topics (scored < 50%)
  - Finds gap topics (never covered)
  - Determines difficulty from quiz history
       ↓
Generates a 4-step plan: Vocabulary → Grammar → Practice → Quiz
       ↓
Shows overview → student types "next" → each step is delivered
       ↓
Completion summary shown → lesson_active = False
```

---

## New Concepts in Phase 9

### Lesson Planner (`lesson_planner.py`)
The brain of Phase 9. It reads `data/progress.json` and classifies every
topic into one of four buckets:

| Bucket | Condition | Strategy |
|--------|-----------|----------|
| strong | score ≥ 80% | Skip for now |
| weak | score < 50% | Prioritize (remediation) |
| review | 50–80% | Reinforce |
| gap | never tried | Explore |

The planner picks topics from weak → gap → review, in that order.

### Lesson State Machine
```
lesson_active = False → generate plan → lesson_active = True, step = 0
lesson_active = True  → execute step N → step = N+1
step >= total_steps   → show completion → lesson_active = False
```

### New State Fields
```python
lesson_active: bool        # True while a lesson is running
lesson_plan: Optional[dict] # the full plan object
lesson_step: int           # which step we're on (0-indexed)
```

---

## Folder Structure

```
Spanish_Tutor/
├── Phase-9/
│   ├── chatbot.py           ← main entry point
│   ├── lesson_planner.py    ← NEW: core lesson intelligence
│   ├── graph.py             ← updated: adds lesson node + routing
│   ├── state.py             ← updated: adds lesson fields
│   ├── progress_tracker.py  ← carried from Phase 7/8
│   ├── __init__.py
│   ├── data/
│   │   └── progress.json    ← auto-created after first session
│   └── nodes/
│       ├── __init__.py
│       ├── lesson.py        ← NEW: lesson execution node
│       ├── supervisor.py    ← updated: routes "lesson" keyword
│       ├── grammar.py
│       ├── vocabulary.py
│       ├── conversation.py
│       └── quiz.py
```

---

## Setup

### Step 1 — Install new dependency (LangGraph)

```bash
pip install -r requirements.txt
```

If `langgraph` isn't installed yet:
```bash
pip install langgraph
```

### Step 2 — Make sure your `.env` is in the root folder

```
Spanish_Tutor/
├── .env    ← GEMINI_API_KEY=your_key_here
```

---

## Running Phase 9

Always run from the **`Spanish_Tutor` root folder** with `(venv)` active.

**Mac/Linux:**
```bash
python3 Phase-9/chatbot.py
```

**Windows:**
```bash
python Phase-9\chatbot.py
```

---

## What to Try

```
You: lesson
  → Profe generates your personalized 4-step lesson plan

You: next
  → Step 1: Vocabulary lesson delivered

You: next
  → Step 2: Grammar lesson delivered

You: next
  → Step 3: Practice dialogue delivered

You: next
  → Step 4: Quiz question (tests what you learned)

You: next
  → 🎉 Lesson complete! Summary shown.
```

### Other commands still work:
```
You: quiz about numbers
You: how do I use ser vs estar?
You: what does "gracias" mean?
You: progress
You: exit
```

---

## Commands Reference

| Command | What happens |
|---------|-------------|
| `lesson` | Generate and start a personalized lesson |
| `next` | Go to the next lesson step |
| `skip lesson` | Exit the lesson early |
| `quiz <topic>` | Start a standalone quiz |
| `progress` | Show your stats summary |
| `history` | Show words learned and topics covered |
| `exit` | Save progress and quit |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: langgraph` | `pip install langgraph` |
| `ModuleNotFoundError: google` | `pip install google-genai` |
| `GEMINI_API_KEY not found` | Check `.env` is in root folder |
| `lesson` generates same plan each time | Normal until you complete quizzes and build a score history |
| 503 error | Gemini free tier busy — wait 2 min and retry |
| 404 model not found | Set `MODEL_NAME = "gemini-2.0-flash"` in all node files |

---

## Completion Checklist

- [ ] Phase 9 runs without errors
- [ ] Type `lesson` → see a personalized 4-step plan
- [ ] Type `next` four times → complete the full lesson
- [ ] Type `lesson` again → see a different plan (based on updated progress)
- [ ] Explain what `lesson_active` does and why it's needed

---

## Key Concept Before Moving On

Phase 9 is where the tutor stops reacting and starts **planning**. Instead of
just answering questions, it now looks at your history and decides what you
need to learn. This is the foundation for Phase 10 (RAG), where the tutor will
pull from a real knowledge base to fill those lesson steps with actual content.

---

## Phase Status

- [x] Phase 1 — Basic chatbot
- [x] Phase 2 — Conversation memory
- [x] Phase 3 — Intent detection
- [x] Phase 4 — First AI agent (Teacher Agent)
- [x] Phase 5 — Multiple specialized agents
- [x] Phase 6 — Agent orchestration (LangGraph)
- [x] Phase 7 — User progress tracking
- [x] Phase 8 — Quiz and evaluation
- [x] Phase 9 — Lesson planning (this phase)
- [ ] Phase 10 — Retrieval-Augmented Generation (RAG)
