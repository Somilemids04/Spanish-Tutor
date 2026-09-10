"""
agent.py — Phase 4

The Teacher Agent.
- Registers tools with Gemini using function declarations
- Sends user messages + tool definitions to Gemini
- Handles tool call responses (ReAct loop)
- Returns the final text response

This is where the "agent" logic lives.
chatbot.py is just the UI. tools.py is just functions.
agent.py is the brain that connects them.
"""
import json
from google import genai
from google.genai import types
from tools import run_tool

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """\
You are Profe, a friendly and patient Spanish language teacher.
You have access to tools: translate_word, explain_grammar, get_vocabulary, generate_quiz.

Rules:
- Always use a tool when the student's request clearly matches one.
- Never make up translations or grammar rules — use the translate or grammar tool.
- After receiving a tool result, craft a warm, encouraging response using that information.
- Keep responses concise and beginner-friendly.
- If unsure which tool to use, just respond conversationally.
"""

# ── Tool declarations ───────────────────────────────────────────────────────────
# These tell Gemini what tools exist and what arguments they take.
# Gemini reads these descriptions to decide when and how to call each tool.
# Think of this as the "menu" of tools you're giving the agent.
TOOL_DECLARATIONS = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="translate_word",
            description="Translates a word between English and Spanish. Use this whenever the student asks how to say something.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "word": types.Schema(
                        type=types.Type.STRING,
                        description="The word or short phrase to translate"
                    ),
                    "direction": types.Schema(
                        type=types.Type.STRING,
                        description="Translation direction: 'en_to_es' for English to Spanish, 'es_to_en' for Spanish to English"
                    ),
                },
                required=["word"],
            ),
        ),
        types.FunctionDeclaration(
            name="explain_grammar",
            description="Explains a Spanish grammar concept. Use this when the student asks about grammar rules.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "topic": types.Schema(
                        type=types.Type.STRING,
                        description="The grammar topic to explain, e.g. 'ser vs estar', 'verb conjugation', 'gendered nouns'"
                    ),
                },
                required=["topic"],
            ),
        ),
        types.FunctionDeclaration(
            name="get_vocabulary",
            description="Returns vocabulary words for a given category. Use this when the student wants to learn new words.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "category": types.Schema(
                        type=types.Type.STRING,
                        description="The vocabulary theme, e.g. 'colors', 'food', 'family', 'numbers'"
                    ),
                    "count": types.Schema(
                        type=types.Type.INTEGER,
                        description="How many words to return. Default is 5."
                    ),
                },
                required=["category"],
            ),
        ),
        types.FunctionDeclaration(
            name="generate_quiz",
            description="Creates a quiz question for the student. Use this when the student asks to be tested or quizzed.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "topic": types.Schema(
                        type=types.Type.STRING,
                        description="What to quiz on, e.g. 'numbers', 'colors', 'greetings'"
                    ),
                    "difficulty": types.Schema(
                        type=types.Type.STRING,
                        description="Difficulty level: 'beginner', 'intermediate', or 'advanced'"
                    ),
                },
                required=["topic"],
            ),
        ),
    ]
)

class TeacherAgent:
    """
    The Teacher Agent.

    Maintains conversation history and runs the ReAct loop:
    Reason (Gemini decides) → Act (tool called) → Observe (result) → Respond
    """

    def __init__(self, client: genai.Client):
        self.client = client
        self.history = []  # full conversation history (we manage this manually now)

    def chat(self, user_message: str) -> str:
        """
        Processes one user message through the full agent loop.
        Returns the final text response.
        """
        # Add user message to history
        self.history.append(
            types.Content(role="user", parts=[types.Part(text=user_message)])
        )

        # ── Step 1: Send to Gemini with tools ──────────────────────────────────
        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=self.history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                tools=[TOOL_DECLARATIONS],
            ),
        )

        # ── Step 2: Check if Gemini wants to call a tool ───────────────────────
        candidate = response.candidates[0]
        part = candidate.content.parts[0]

        # If it's a function call, run the tool and send result back
        if hasattr(part, "function_call") and part.function_call:
            tool_call = part.function_call
            tool_name = tool_call.name
            tool_args = dict(tool_call.args)

            print(f"  [Agent calling tool: {tool_name}({tool_args})]")

            # Run the actual Python function
            tool_result = run_tool(tool_name, tool_args)

            # Add the agent's tool call to history
            self.history.append(candidate.content)

            # Add tool result to history so Gemini can read it
            self.history.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            function_response=types.FunctionResponse(
                                name=tool_name,
                                response={"result": json.dumps(tool_result)},
                            )
                        )
                    ],
                )
            )

            # ── Step 3: Send tool result back to Gemini for final response ─────
            final_response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=self.history,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    tools=[TOOL_DECLARATIONS],
                ),
            )

            final_text = final_response.text
            # Add final response to history
            self.history.append(
                types.Content(role="model", parts=[types.Part(text=final_text)])
            )
            return final_text

        # No tool call — plain text response
        plain_text = part.text
        self.history.append(
            types.Content(role="model", parts=[types.Part(text=plain_text)])
        )
        return plain_text