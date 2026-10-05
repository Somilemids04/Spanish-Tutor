# Phase 7: User Progress Tracking

## Objective

Save student progress to disk so it survives between sessions.
Words learned, quiz scores, student name — all persist across runs.

---

## What You Learn Here

- What persistence means and why it matters
- How to read/write JSON files in Python
- How to merge saved data back into shared state at startup
- The difference between session memory (RAM) and long-term storage (disk)

---

## What Changed from Phase 6

| | Phase 6 | Phase 7 |
|---|---|---|
| Progress after exit | Lost forever | Saved to JSON file |
| Returning student | Starts from scratch | Picks up where they left off |
| Words learned | Session only | Accumulates across all sessions |
| Quiz history | Session only | All scores saved |
| New file | — | `progress_tracker.py` |
| New folder | — | `data/progress.json` |

---

## Folder Structure

```
Spanish_Tutor/
└── Phase-7/
    ├── __init__.py
    ├── chatbot.py              ← loads/saves progress, runs graph
    ├── graph.py                ← same LangGraph as Phase 6
    ├── state.py                ← same state + session fields
    ├── progress_tracker.py     ← NEW: all file read/write logic
    ├── data/
    │   └── progress.json       ← auto-created on first run
    ├── nodes/
    │   ├── __init__.py
    │   ├── supervisor.py
    │   ├── grammar.py
    │   ├── vocabulary.py
    │   ├── quiz.py
    │   └── conversation.py
    └── README.md
```

---

## Running Phase 7

**Mac/Linux:**
```bash
cd Desktop/Spanish_Tutor
source venv/bin/activate
python3 Phase-7/chatbot.py
```

**Windows:**
```bash
cd Desktop\Spanish_Tutor
venv\Scripts\activate
python Phase-7\chatbot.py
```

---

## Special Commands

| Command | What it does |
|---|---|
| `exit` | Saves session and quits |
| `status` | Shows live shared state |
| `progress` | Shows full progress report across all sessions |

---

## Test This Across Two Sessions

**Session 1:**
```
You: my name is Somil
You: give me 5 words about colors
You: exit        ← saves progress
```

**Session 2 (run again):**
```
  [Progress loaded — welcome back! Sessions: 1]
  Welcome back, Somil!
  Words learned so far: 5

You: progress    ← shows everything from Session 1
You: quiz me     ← quizzes on colors from Session 1
```

---

## What progress.json Looks Like

```json
{
  "student_name": "Somil",
  "total_sessions": 2,
  "words_learned": ["rojo", "azul", "verde", "amarillo", "negro"],
  "topics_covered": ["vocabulary: give me 5 words about colors"],
  "session_quiz_scores": [
    {"correct": 3, "total": 4, "date": "2026-09-22"}
  ],
  "last_seen": "2026-09-22 14:05"
}
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: phase7` | Run from root: `python3 Phase-7/chatbot.py` |
| `progress.json` not created | Run the script and type at least one message |
| Progress not loading | Check `Phase-7/data/progress.json` exists and is valid JSON |
| 404 model not found | Set `MODEL_NAME = "gemini-3.6-flash"` in node files |

---

## Completion Checklist

- [ ] First run creates `Phase-7/data/progress.json`
- [ ] Second run loads name and words from previous session
- [ ] `progress` command shows full report
- [ ] Quiz in session 2 uses words learned in session 1
- [ ] You can explain: session memory vs persistent storage

---

## Key Concept Before Moving On

JSON file = simple persistence. Good for learning.
Limitations: no search, no filtering, slow with large data.
Phase 10 (RAG) + Phase 11 (long-term memory) replace this
with a proper vector database that can search across all progress.

---

## Phase Status

- [x] Phase 1 — Basic chatbot
- [x] Phase 2 — Conversation memory
- [x] Phase 3 — Intent detection
- [x] Phase 4 — First AI agent
- [x] Phase 5 — Multiple specialized agents
- [x] Phase 6 — Agent orchestration
- [x] Phase 7 — User progress tracking (this phase)
- [ ] Phase 8 — Quiz and evaluation (next)
