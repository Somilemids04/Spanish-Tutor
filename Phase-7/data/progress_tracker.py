"""
progress_tracker.py — Phase 7

Single responsibility: read and write student progress to disk.
No AI logic here. Just file I/O.

Saves to: Phase-7/data/progress.json
"""

import json
import os
from datetime import datetime
from typing import Optional

# Path to the progress file — relative to project root
PROGRESS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "progress.json"
)

# Default progress structure for a brand new student
DEFAULT_PROGRESS = {
    "student_name": None,
    "total_sessions": 0,
    "words_learned": [],
    "topics_covered": [],
    "session_quiz_scores": [],
    "last_seen": None,
}


def load_progress() -> dict:
    """
    Loads progress from disk.
    If file doesn't exist yet, returns default empty progress.
    Called once at startup.
    """
    if not os.path.exists(PROGRESS_FILE):
        print("  [No progress file found — starting fresh]")
        return DEFAULT_PROGRESS.copy()

    try:
        with open(PROGRESS_FILE, "r") as f:
            data = json.load(f)
        print(f"  [Progress loaded — welcome back! Sessions: {data.get('total_sessions', 0)}]")
        return data
    except (json.JSONDecodeError, IOError):
        print("  [Progress file corrupted — starting fresh]")
        return DEFAULT_PROGRESS.copy()


def save_progress(state: dict) -> None:
    """
    Saves current state to disk after every turn.
    Merges session data with existing progress file.
    Called after every agent response.
    """
    # Build the progress dict from current state
    progress = {
        "student_name": state.get("student_name"),
        "total_sessions": state.get("total_sessions", 1),
        "words_learned": list(set(state.get("words_learned", []))),
        "topics_covered": state.get("topics_covered", []),
        "session_quiz_scores": state.get("session_quiz_scores", []),
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    # Make sure the data directory exists
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)

    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def save_session_end(state: dict) -> None:
    """
    Called when student types 'exit'.
    Saves final quiz score for this session.
    """
    scores = state.get("session_quiz_scores", [])

    if state.get("quiz_total", 0) > 0:
        scores.append({
            "correct": state.get("quiz_correct", 0),
            "total": state.get("quiz_total", 0),
            "date": datetime.now().strftime("%Y-%m-%d"),
        })

    updated_state = {**state, "session_quiz_scores": scores}
    save_progress(updated_state)


def format_progress_summary(progress: dict) -> str:
    """
    Returns a human-readable summary of the student's progress.
    Used by the 'progress' command in the terminal.
    """
    name = progress.get("student_name") or "Student"
    sessions = progress.get("total_sessions", 0)
    words = progress.get("words_learned", [])
    topics = progress.get("topics_covered", [])
    scores = progress.get("session_quiz_scores", [])
    last_seen = progress.get("last_seen", "never")

    lines = [
        f"\n{'='*45}",
        f"  📊 Progress Report — {name}",
        f"{'='*45}",
        f"  Sessions completed : {sessions}",
        f"  Last seen          : {last_seen}",
        f"  Words learned      : {len(words)} total",
    ]

    if words:
        lines.append(f"  Word list          : {', '.join(words[:10])}" +
                     (f" (+{len(words)-10} more)" if len(words) > 10 else ""))

    if topics:
        lines.append(f"  Topics covered     : {len(topics)}")

    if scores:
        avg = sum(s["correct"] for s in scores) / sum(s["total"] for s in scores) * 100
        lines.append(f"  Quiz average       : {avg:.0f}% ({len(scores)} quizzes taken)")

    lines.append(f"{'='*45}")
    return "\n".join(lines)
