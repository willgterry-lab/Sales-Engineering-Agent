"""Demo: retrieve case studies for each of the three discovery transcripts.

What this proves:
- Product-fit filtering correctly excludes irrelevant case studies.
- Keyword scoring ranks the most contextually relevant study first.
- The retrieval interface returns structured RetrievalResult objects,
  ready for the draft_followup_email tool to consume.

Run with:
    uv run python scripts/retrieve_case_studies_demo.py
    uv run python scripts/retrieve_case_studies_demo.py fixtures/transcript-02-cirra-insurance.md
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

from sea.discovery import extract_discovery
from sea.retrieval import retrieve_case_studies

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TRANSCRIPT = REPO_ROOT / "fixtures" / "transcript-01-bellwether-coffee.md"


if __name__ == "__main__":
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    transcript_path = (REPO_ROOT / path_arg) if path_arg else DEFAULT_TRANSCRIPT

    transcript = transcript_path.read_text(encoding="utf-8")

    print(f"Transcript:   {transcript_path.name}")
    print(f"Extracting discovery (calls Claude)...\n")
    discovery = extract_discovery(transcript)

    print(f"product_fit:  {discovery.product_fit}")
    print(f"champion:     {discovery.champion.status} — {discovery.champion.name}")
    print(f"Retrieving case studies...\n")

    results = retrieve_case_studies(discovery, top_k=2)

    if not results:
        print("No matching case studies found.")
    else:
        for i, result in enumerate(results, 1):
            print(f"{'=' * 60}")
            print(f"RESULT {i}: {result.title}")
            print(f"Score:        {result.score:.0f}")
            print(f"Match reasons:")
            for reason in result.match_reasons:
                print(f"  - {reason}")
            print(f"\nContent preview (first 300 chars):")
            print(result.content[:300].strip())
            print()
