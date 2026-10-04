import json

from app.services.llm import client
from app.tools.calculator import calculate
from app.tools.file_reader import read_text_file


CALCULATOR_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Perform a basic arithmetic calculation.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number.",
                },
                "b": {
                    "type": "number",
                    "description": "The second number.",
                },
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The arithmetic operation to perform.",
                },
            },
            "required": ["a", "b", "operation"],
        },
    },
}


FILE_READER_TOOL = {
    "type": "function",
    "function": {
        "name": "read_text_file",
        "description": "Read the contents of a UTF-8 text file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the .txt file to read.",
                },
            },
            "required": ["file_path"],
        },
    },
}


TOOLS = [
    CALCULATOR_TOOL,
    FILE_READER_TOOL,
]


def run_agent(user_message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful personal AI assistant. "
                "Use the available tools when they are useful."
            ),
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    assistant_message = response.choices[0].message

    if not assistant_message.tool_calls:
        return assistant_message.content or ""

    messages.append(assistant_message)

    for tool_call in assistant_message.tool_calls:
        print(f"[Agent] Tool selected: {tool_call.function.name}")
        print(f"[Agent] Arguments: {tool_call.function.arguments}")

        arguments = json.loads(tool_call.function.arguments)

        if tool_call.function.name == "calculate":
            result = calculate(
                a=arguments["a"],
                b=arguments["b"],
                operation=arguments["operation"],
            )

        elif tool_call.function.name == "read_text_file":
            result = read_text_file(
                file_path=arguments["file_path"],
            )

        else:
            raise ValueError(
                f"Unknown tool: {tool_call.function.name}"
            )

        print(f"[Tool] Result: {result}")

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            }
        )

    final_response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=TOOLS,
    )

    return final_response.choices[0].message.content or ""
