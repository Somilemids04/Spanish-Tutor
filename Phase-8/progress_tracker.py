"""
progress_tracker.py — Phase 8
Same as Phase 7, adds topic_scores to saved data.
"""

import json
import os
from datetime import datetime

PROGRESS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "progress.json"
)

DEFAULT_PROGRESS = {
    "student_name": None,
    "total_sessions": 0,
    "words_learned": [],
    "topics_covered": [],
    "session_quiz_scores": [],
    "topic_scores": {},
    "last_seen": None,
}


def load_progress() -> dict:
    if not os.path.exists(PROGRESS_FILE):
        print("  [No progress file found — starting fresh]")
        return DEFAULT_PROGRESS.copy()
    try:
        with open(PROGRESS_FILE, "r") as f:
            data = json.load(f)
        print(f"  [Progress loaded — welcome back! Sessions: {data.get('total_sessions', 0)}]")
        return data
    except Exception:
        print("  [Progress file corrupted — starting fresh]")
        return DEFAULT_PROGRESS.copy()


def save_progress(state: dict) -> None:
    progress = {
        "student_name": state.get("student_name"),
        "total_sessions": state.get("total_sessions", 1),
        "words_learned": list(set(state.get("words_learned", []))),
        "topics_covered": state.get("topics_covered", []),
        "session_quiz_scores": state.get("session_quiz_scores", []),
        "topic_scores": state.get("topic_scores", {}),
        "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def save_session_end(state: dict) -> None:
    save_progress(state)


def format_progress_summary(state: dict) -> str:
    name = state.get("student_name") or "Student"
    sessions = state.get("total_sessions", 0)
    words = state.get("words_learned", [])
    scores = state.get("session_quiz_scores", [])
    topic_scores = state.get("topic_scores", {})
    last_seen = state.get("last_seen", "this session")

    lines = [
        f"\n{'='*48}",
        f"  📊 Progress Report — {name}",
        f"{'='*48}",
        f"  Sessions completed : {sessions}",
        f"  Last seen          : {last_seen}",
        f"  Words learned      : {len(words)} total",
    ]

    if words:
        preview = ', '.join(words[:8])
        more = f" (+{len(words)-8} more)" if len(words) > 8 else ""
        lines.append(f"  Word list          : {preview}{more}")

    if scores:
        total_correct = sum(s["correct"] for s in scores)
        total_q = sum(s["total"] for s in scores)
        avg = (total_correct / total_q * 100) if total_q > 0 else 0
        lines.append(f"  Quiz average       : {avg:.0f}% across {len(scores)} quizzes")

    if topic_scores:
        lines.append(f"\n  Per-topic scores:")
        for topic, s in topic_scores.items():
            pct = (s["correct"] / s["total"] * 100) if s["total"] > 0 else 0
            bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            lines.append(f"  • {topic:<20} {bar} {pct:.0f}%")

    lines.append(f"{'='*48}")
    return "\n".join(lines)
