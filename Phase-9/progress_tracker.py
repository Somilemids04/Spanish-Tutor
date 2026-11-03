"""
progress_tracker.py — Phase 9 (carried over from Phase 7/8)

Saves and loads progress.json — the student's persistent record across sessions.
"""

import json
import os
from datetime import datetime

PROGRESS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "progress.json"
)

DEFAULT_PROGRESS = {
    "student_name": None,
    "sessions": 0,
    "words_learned": [],
    "topics_covered": [],
    "quiz_correct": 0,
    "quiz_total": 0,
    "topic_scores": {},
    "last_seen": None,
}


def load_progress() -> dict:
    if not os.path.exists(PROGRESS_FILE):
        return DEFAULT_PROGRESS.copy()
    try:
        with open(PROGRESS_FILE, "r") as f:
            data = json.load(f)
        # Ensure all keys exist (for upgrades from older phases)
        for key, val in DEFAULT_PROGRESS.items():
            if key not in data:
                data[key] = val
        return data
    except Exception:
        return DEFAULT_PROGRESS.copy()


def save_progress(state: dict) -> None:
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    progress = load_progress()

    # Merge state into persistent progress
    if state.get("student_name"):
        progress["student_name"] = state["student_name"]
    if state.get("words_learned"):
        for w in state["words_learned"]:
            if w not in progress["words_learned"]:
                progress["words_learned"].append(w)
    if state.get("topics_covered"):
        for t in state["topics_covered"]:
            if t not in progress["topics_covered"]:
                progress["topics_covered"].append(t)
    if state.get("topic_scores"):
        progress["topic_scores"].update(state["topic_scores"])

    progress["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def save_session_end(state: dict) -> None:
    progress = load_progress()
    progress["sessions"] = progress.get("sessions", 0) + 1
    progress["quiz_correct"] = progress.get("quiz_correct", 0) + state.get("quiz_correct", 0)
    progress["quiz_total"] = progress.get("quiz_total", 0) + state.get("quiz_total", 0)
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def format_progress_summary(progress: dict) -> str:
    name = progress.get("student_name") or "Student"
    sessions = progress.get("sessions", 0)
    words = progress.get("words_learned", [])
    topics = progress.get("topics_covered", [])
    correct = progress.get("quiz_correct", 0)
    total = progress.get("quiz_total", 0)
    pct = f"{int(correct/total*100)}%" if total > 0 else "N/A"

    return (
        f"\n📊 Progress Report for {name}"
        f"\n   Sessions completed : {sessions}"
        f"\n   Words learned      : {len(words)}"
        f"\n   Topics covered     : {len(topics)}"
        f"\n   Quiz accuracy      : {correct}/{total} ({pct})"
        f"\n   Last seen          : {progress.get('last_seen', 'today')}\n"
    )
