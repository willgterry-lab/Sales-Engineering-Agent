"""Demo: extract structured MEDDPICC discovery from a transcript fixture.

What this proves:
- A Pydantic model can serve as the schema for an Anthropic tool.
- "Forced tool use" reliably returns structured data, not free-form text.
- We get a validated Python object out, not a dict we have to inspect by hand.

Run with:
    uv run python scripts/extract_discovery_demo.py
    uv run python scripts/extract_discovery_demo.py fixtures/transcript-02-cirra-insurance.md
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

from sea.discovery import extract_discovery

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TRANSCRIPT = REPO_ROOT / "fixtures" / "transcript-01-bellwether-coffee.md"


if __name__ == "__main__":
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    transcript_path = (REPO_ROOT / path_arg) if path_arg else DEFAULT_TRANSCRIPT

    transcript = transcript_path.read_text(encoding="utf-8")

    print(f"Extracting MEDDPICC from: {transcript_path.name}")
    print(f"Transcript length:        {len(transcript):,} chars")
    print(f"Running extraction (this calls Claude, takes a few seconds)...\n")

    discovery = extract_discovery(transcript)

    print("=" * 60)
    print("RESULT (validated MEDDPICCDiscovery object, serialised to JSON):")
    print("=" * 60)
    print(discovery.model_dump_json(indent=2))
