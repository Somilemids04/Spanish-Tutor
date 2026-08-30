# Phase 3: Intent Detection

## Objective

Teach the tutor to understand what the user is trying to do before
responding. The system now classifies every message into an intent
label, then shapes its response accordingly.

---

## What You Learn Here

- What intent detection is and why it matters
- How to use an LLM as a classifier (not just a generator)
- How to get structured JSON output from Gemini
- Why splitting code into modules (intent.py) is better than one big file

---

## Intents Supported

| Intent | Example message |
|---|---|
| `greeting` | "hi", "hola", "hello" |
| `translation` | "how do you say cat in Spanish?" |
| `grammar` | "why do adjectives come after nouns?" |
| `vocabulary` | "give me 5 new words" |
| `practice` | "let's have a conversation in Spanish" |
| `quiz` | "quiz me on colors" |
| `unknown` | anything unrelated to Spanish learning |

---

## What Changed from Phase 2

| | Phase 2 | Phase 3 |
|---|---|---|
| Files | 1 (`chatbot.py`) | 2 (`chatbot.py` + `intent.py`) |
| API calls per turn | 1 | 2 (classify → respond) |
| Response style | Same for everything | Shaped by detected intent |

---

## Folder Structure

```
spanish-tutor/
└── phase3/
    ├── chatbot.py    ← main loop + routing
    ├── intent.py     ← classification logic (new)
    └── README.md     ← this file
```

