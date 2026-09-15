"""
agent.py — Phase 4 (fixed)

Fixes:
- "Profe: None" bug — properly extracts text from final response
- 400 INVALID_ARGUMENT — cleans up history on failed tool calls
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

TOOL_DECLARATIONS = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="translate_word",
            description="Translates a word between English and Spanish. Use this whenever the student asks how to say something.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "word": types.Schema(type=types.Type.STRING, description="The word or short phrase to translate"),
                    "direction": types.Schema(type=types.Type.STRING, description="'en_to_es' for English to Spanish, 'es_to_en' for Spanish to English"),
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
                    "topic": types.Schema(type=types.Type.STRING, description="The grammar topic to explain"),
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
                    "category": types.Schema(type=types.Type.STRING, description="The vocabulary theme e.g. colors, food, family"),
                    "count": types.Schema(type=types.Type.INTEGER, description="How many words to return. Default is 5."),
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
                    "topic": types.Schema(type=types.Type.STRING, description="What to quiz on e.g. numbers, colors, greetings"),
                    "difficulty": types.Schema(type=types.Type.STRING, description="'beginner', 'intermediate', or 'advanced'"),
                },
                required=["topic"],
            ),
        ),
    ]
)


class TeacherAgent:
    def __init__(self, client: genai.Client):
        self.client = client
        self.history = []

    def _generate(self, contents):
        """Calls Gemini with current contents and returns the response."""
        return self.client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                tools=[TOOL_DECLARATIONS],
            ),
        )

    def _extract_text(self, response) -> str:
        """Safely extracts text from a Gemini response."""
        try:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "text") and part.text:
                    return part.text
        except Exception:
            pass
        return "I'm sorry, I couldn't generate a response. Please try again."

    def chat(self, user_message: str) -> str:
        # Add user message to history
        self.history.append(
            types.Content(role="user", parts=[types.Part(text=user_message)])
        )

        # Step 1 — send to Gemini
        response = self._generate(self.history)
        candidate = response.candidates[0]
        part = candidate.content.parts[0]

        # Step 2 — check for tool call
        if hasattr(part, "function_call") and part.function_call:
            tool_call = part.function_call
            tool_name = tool_call.name
            tool_args = dict(tool_call.args)

            print(f"  [Agent calling tool: {tool_name}({tool_args})]")

            # Run the tool
            tool_result = run_tool(tool_name, tool_args)

            # Add tool call to history
            self.history.append(candidate.content)

            # Add tool result to history
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

            # Step 3 — get final response after tool result
            try:
                final_response = self._generate(self.history)
                final_text = self._extract_text(final_response)


                self.history.append(
                    types.Content(role="model", parts=[types.Part(text=final_text)])
                )
                return final_text

            except Exception as e:
                self.history.pop()
                self.history.pop()
                return f"I had trouble processing that. Could you rephrase? ({e})"

        # No call — plain text response
        plain_text = self._extract_text(response)
        self.history.append(
            types.Content(role="model", parts=[types.Part(text=plain_text)])
        )
        return plain_text