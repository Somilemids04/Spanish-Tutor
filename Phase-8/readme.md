# Phase 8: Quiz and Evaluation

## Objective

Replace the basic quiz agent with a proper quiz engine — structured
questions, difficulty levels, per-topic scoring, wrong answer tracking,
and a detailed evaluation report after every quiz.

---

## What You Learn Here

- How to build a state machine (idle → questioning → evaluating → reporting)
- How to generate structured JSON output from an LLM and parse it
- How to track performance per topic over time
- How to give adaptive feedback based on score

---

## What Changed from Phase 7

| | Phase 7 | Phase 8 |
|---|---|---|
| Quiz logic | One LLM call, no structure | Full quiz engine (quiz_engine.py) |
| Questions | Random, untracked | Structured, 5 per quiz |
| Difficulty | Always same | beginner / intermediate / advanced |
| Scoring | Basic count | Per-topic with percentage |
| Report | None | Full breakdown after every quiz |
| Quiz state | None | State machine tracks progress |

---

## Quiz Commands

```
quiz me                          → beginner quiz on recent words
quiz me on colors                → beginner quiz on colors
quiz intermediate on verbs       → intermediate verb quiz
quiz advanced on grammar         → advanced grammar quiz
```

---

## Folder Structure

```
Phase-8/
├── __init__.py
├── chatbot.py
├── graph.py
├── state.py
├── quiz_engine.py        ← NEW: all quiz logic here
├── progress_tracker.py   ← updated: saves topic_scores
├── data/
│   └── progress.json
└── nodes/
    ├── __init__.py
    ├── supervisor.py
    ├── grammar.py
    ├── vocabulary.py
    ├── quiz.py           ← rewritten: uses quiz_engine
    └── conversation.py
```

---

## Running Phase 8

**Mac/Linux:**
```bash
cd Desktop/Spanish_Tutor
source venv/bin/activate
python3 Phase-8/chatbot.py
```

**Windows:**
```bash
cd Desktop\Spanish_Tutor
venv\Scripts\activate
python Phase-8\chatbot.py
```

---

## Test This Flow

```
You: give me 5 words about animals
You: quiz me on animals
  → 5 structured questions appear one by one
  → Answer each with A/B/C/D
  → Full report appears at end with score + breakdown

You: progress
  → Shows per-topic scores with visual bar
```

---

## What the Report Looks Like

```
================================================
  📊 Quiz Report — Animals (Beginner)
================================================
  Score: 4/5 (80%)  🌟 Excellent!
  You're ready to try intermediate level!

  Question breakdown:
  ✅ Q1: How do you say 'dog' in Spanish?
  ✅ Q2: What does 'gato' mean?
  ❌ Q3: How do you say 'bird'?
      Your answer: C | Correct: B (pájaro)
      💡 'Pájaro' means bird in Spanish.
  ✅ Q4: What is 'pez' in English?
  ✅ Q5: How do you say 'horse'?
================================================
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: phase8` | Run from root: `python3 Phase-8/chatbot.py` |
| Quiz generates wrong questions | Gemini returned bad JSON — retry |
| Quiz stuck after last question | Type anything to trigger report |
| 404 model error | Set `MODEL_NAME = "gemini-2.0-flash"` in all files |

---

## Completion Checklist

- [ ] Quiz generates 5 structured questions
- [ ] Each answer gets immediate correct/wrong feedback
- [ ] Full report shows after quiz with score breakdown
- [ ] `progress` command shows per-topic score bars
- [ ] Topic scores saved to `progress.json`

---

## Phase Status

- [x] Phase 1 — Basic chatbot
- [x] Phase 2 — Conversation memory
- [x] Phase 3 — Intent detection
- [x] Phase 4 — First AI agent
- [x] Phase 5 — Multiple specialized agents
- [x] Phase 6 — Agent orchestration
- [x] Phase 7 — User progress tracking
- [x] Phase 8 — Quiz and evaluation (this phase)
- [ ] Phase 9 — Lesson planning (next)
