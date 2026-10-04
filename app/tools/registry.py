from app.tools.calculator import calculate
from app.tools.file_reader import read_document


TOOL_DEFINITIONS = [
    {
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
    },
    {
        "type": "function",
        "function": {
            "name": "read_document",
            "description": (
                "Read the text content of a TXT, PDF, or DOCX document."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": (
                            "Path to the TXT, PDF, or DOCX document to read."
                        ),
                    },
                },
                "required": ["file_path"],
            },
        },
    },
]


def execute_tool(tool_name: str, arguments: dict):
    if tool_name == "calculate":
        return calculate(
            a=arguments["a"],
            b=arguments["b"],
            operation=arguments["operation"],
        )

    if tool_name == "read_document":
        return read_document(
            file_path=arguments["file_path"],
        )

    raise ValueError(f"Unknown tool: {tool_name}")
