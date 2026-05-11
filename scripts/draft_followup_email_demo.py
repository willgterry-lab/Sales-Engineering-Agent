"""Demo: run the full three-tool pipeline on a discovery transcript.

Extract discovery -> retrieve case studies -> draft follow-up email.

Run with:
    uv run python scripts/draft_followup_email_demo.py
    uv run python scripts/draft_followup_email_demo.py fixtures/transcript-02-cirra-insurance.md
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

from sea.discovery import extract_discovery
from sea.retrieval import retrieve_case_studies
from sea.email import draft_followup_email

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TRANSCRIPT = REPO_ROOT / "fixtures" / "transcript-01-bellwether-coffee.md"


if __name__ == "__main__":
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    transcript_path = (REPO_ROOT / path_arg) if path_arg else DEFAULT_TRANSCRIPT

    transcript = transcript_path.read_text(encoding="utf-8")
    print(f"Transcript: {transcript_path.name}\n")

    print("[1/3] Extracting MEDDPICC discovery...")
    discovery = extract_discovery(transcript)
    print(f"      product_fit: {discovery.product_fit}")
    print(f"      champion:    {discovery.champion.status} — {discovery.champion.name}\n")

    print("[2/3] Retrieving case studies...")
    case_studies = retrieve_case_studies(discovery, top_k=2)
    for cs in case_studies:
        print(f"      {cs.title} (score: {cs.score:.0f})")
    print()

    print("[3/3] Drafting follow-up email...")
    email = draft_followup_email(discovery, case_studies)

    print("\n" + "=" * 60)
    print(f"SUBJECT: {email.subject}")
    print("=" * 60)
    print(email.body)
