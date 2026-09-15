"""
tools.py — Phase 4

Plain Python functions that the Teacher Agent can call.
NO AI logic here — these are just regular functions.
Gemini decides WHEN to call them. Python runs the actual code.

In later phases these will call real APIs or databases.
For now they return structured data that the agent can use.
"""


def translate_word(word: str, direction: str = "en_to_es") -> dict:
    """
    Translates a word between English and Spanish.

    Args:
        word: the word to translate
        direction: "en_to_es" (English→Spanish) or "es_to_en" (Spanish→English)

    Returns:
        dict with translation, pronunciation, and an example sentence
    """
    # In Phase 10 (RAG) this will query a real dictionary database.
    # For now we return a structured response that guides the LLM.
    return {
        "tool": "translate_word",
        "input_word": word,
        "direction": direction,
        "instruction": (
            f"Provide the {'Spanish' if direction == 'en_to_es' else 'English'} "
            f"translation of '{word}', its phonetic pronunciation, gender if it's a noun, "
            f"and one natural example sentence using it in context."
        ),
    }


def explain_grammar(topic: str) -> dict:
    """
    Returns a grammar explanation request for a specific topic.

    Args:
        topic: the grammar concept to explain (e.g. "ser vs estar", "subjunctive")

    Returns:
        dict with structured instructions for the LLM to explain the topic
    """
    return {
        "tool": "explain_grammar",
        "topic": topic,
        "instruction": (
            f"Explain the Spanish grammar concept: '{topic}'. "
            f"Use simple English. Give 3 short example sentences. "
            f"Highlight the key rule in one sentence. No jargon."
        ),
    }


def get_vocabulary(category: str, count: int = 5) -> dict:
    """
    Returns a vocabulary lesson for a given category.

    Args:
        category: theme of vocabulary (e.g. "colors", "food", "family")
        count: how many words to return (default 5)

    Returns:
        dict instructing the LLM to produce a vocabulary list
    """
    return {
        "tool": "get_vocabulary",
        "category": category,
        "count": count,
        "instruction": (
            f"Give {count} common Spanish words related to '{category}'. "
            f"For each: Spanish word, pronunciation, English meaning, "
            f"and one short example sentence."
        ),
    }


def generate_quiz(topic: str, difficulty: str = "beginner") -> dict:
    """
    Generates a quiz question on a given topic.

    Args:
        topic: what to quiz on (e.g. "numbers", "greetings", "colors")
        difficulty: "beginner", "intermediate", or "advanced"

    Returns:
        dict instructing the LLM to create a quiz question
    """
    return {
        "tool": "generate_quiz",
        "topic": topic,
        "difficulty": difficulty,
        "instruction": (
            f"Create ONE {difficulty}-level Spanish quiz question about '{topic}'. "
            f"Format: question, 4 multiple choice options (A/B/C/D), correct answer, "
            f"and a brief explanation of why it's correct."
        ),
    }


# ── Tool registry ──────────────────────────────────────────────────────────────
# This maps tool names (strings) to actual Python functions.
# The agent uses this to look up and run the right function.
TOOL_REGISTRY = {
    "translate_word": translate_word,
    "explain_grammar": explain_grammar,
    "get_vocabulary": get_vocabulary,
    "generate_quiz": generate_quiz,
}


def run_tool(tool_name: str, tool_args: dict) -> dict:
    """
    Looks up a tool by name and runs it with the given arguments.
    Returns the tool result, or an error dict if tool not found.
    """
    if tool_name not in TOOL_REGISTRY:
        return {"error": f"Unknown tool: {tool_name}"}

    func = TOOL_REGISTRY[tool_name]
    return func(**tool_args)
