import os
import pathlib
import anthropic
from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).parent.parent / ".env", override=True)

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=256,
    system=[
        {
            "type": "text",
            "text": "Answer every question in exactly one sentence.",
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[{"role": "user", "content": "What is the capital of France?"}],
)

for block in response.content:
    if block.type == "text":
        print(block.text)
