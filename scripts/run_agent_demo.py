"""Demo: run the full agent loop on a discovery transcript.

Prints tool call progress as the loop runs, then displays all three artefacts.

Run with:
    uv run python scripts/run_agent_demo.py
    uv run python scripts/run_agent_demo.py fixtures/transcript-02-cirra-insurance.md
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

from sea.agent import run_agent

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TRANSCRIPT = REPO_ROOT / "fixtures" / "transcript-01-bellwether-coffee.md"

TOOL_LABELS = {
    "extract_structured_discovery": "[1/3] extract_structured_discovery",
    "retrieve_case_studies":        "[2/3] retrieve_case_studies",
    "draft_followup_email":         "[3/3] draft_followup_email",
}

if __name__ == "__main__":
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    transcript_path = (REPO_ROOT / path_arg) if path_arg else DEFAULT_TRANSCRIPT

    transcript = transcript_path.read_text(encoding="utf-8")
    print(f"Transcript: {transcript_path.name}")
    print("Running agent loop...\n")

    # Monkey-patch dispatch to print progress without touching agent internals.
    import sea.agent as _agent_mod
    _original_make_dispatch = _agent_mod._make_dispatch

    def _verbose_make_dispatch(transcript, state, client, model):
        inner = _original_make_dispatch(transcript, state, client, model)
        def verbose_dispatch(tool_name, tool_input):
            label = TOOL_LABELS.get(tool_name, tool_name)
            print(f"  {label} called")
            result = inner(tool_name, tool_input)
            print(f"  {label} done")
            return result
        return verbose_dispatch

    _agent_mod._make_dispatch = _verbose_make_dispatch

    output = run_agent(transcript)

    print("\n" + "=" * 60)
    print("DISCOVERY (product_fit + champion)")
    print("=" * 60)
    print(f"product_fit: {output.discovery.product_fit}")
    print(f"champion:    {output.discovery.champion.status} — {output.discovery.champion.name}")

    print("\n" + "=" * 60)
    print("RETRIEVED CASE STUDIES")
    print("=" * 60)
    for cs in output.case_studies:
        print(f"  {cs.title}  (score: {cs.score:.0f})")
        for reason in cs.match_reasons[:1]:
            print(f"    {reason}")

    print("\n" + "=" * 60)
    print(f"FOLLOW-UP EMAIL — {output.email.subject}")
    print("=" * 60)
    print(output.email.body)
