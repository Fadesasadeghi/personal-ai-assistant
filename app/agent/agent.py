import json

from app.services.llm import client
from app.tools.registry import TOOL_DEFINITIONS, execute_tool


MODEL = "openai/gpt-oss-120b"


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
        model=MODEL,
        messages=messages,
        tools=TOOL_DEFINITIONS,
        tool_choice="auto",
    )

    assistant_message = response.choices[0].message

    if not assistant_message.tool_calls:
        return assistant_message.content or ""

    messages.append(assistant_message)

    for tool_call in assistant_message.tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print(f"[Agent] Tool selected: {tool_name}")
        print(f"[Agent] Arguments: {arguments}")

        result = execute_tool(tool_name, arguments)

        result_text = str(result)

        print(
            f"[Tool] Result preview: "
            f"{result_text[:500]}"
        )

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result_text,
            }
        )

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOL_DEFINITIONS,
    )

    return final_response.choices[0].message.content or ""
