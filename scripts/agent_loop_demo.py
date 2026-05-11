import datetime
import os
import pathlib
import anthropic
from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).parent.parent / ".env", override=True)

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

TOOLS = [
    {
        "name": "get_current_date",
        "description": "Returns today's date in YYYY-MM-DD format.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    }
]

SYSTEM = [
    {
        "type": "text",
        "text": "You are a helpful assistant. Use tools when appropriate.",
        "cache_control": {"type": "ephemeral"},
    }
]


def get_current_date() -> str:
    return datetime.date.today().isoformat()


def run_loop(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=256,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    return block.text
            return ""

        # Handle tool_use
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if block.name == "get_current_date":
                    result = get_current_date()
                    print(f"[loop] Claude called {block.name}(...) -> '{result}'")
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )

        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    answer = run_loop("What is today's date?")
    print(answer)
