"""Eval harness for the three-tool agent pipeline.

Eight checks across three transcripts, mixing two types:
  - Structured: deterministic assertions on typed output fields.
  - Claude-as-judge: LLM rates quality on a yes/no question with reasoning.

Run with:
    uv run python scripts/run_evals.py

Each check prints PASS or FAIL with a short reason. A total score is printed
at the end. The harness exits with code 1 if any check fails, so it can gate CI.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

import anthropic
from sea.agent import AgentOutput, run_agent

REPO_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Shared client (one instance, re-used across all checks)
# ---------------------------------------------------------------------------
CLIENT = anthropic.Anthropic()


# ---------------------------------------------------------------------------
# Result model
# ---------------------------------------------------------------------------

class EvalResult:
    def __init__(self, name: str, passed: bool, reason: str):
        self.name = name
        self.passed = passed
        self.reason = reason

    def __str__(self):
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.name}\n       {self.reason}"


# ---------------------------------------------------------------------------
# Structured checks — no Claude call, pure Python assertions
# ---------------------------------------------------------------------------

def check_product_fit(output: AgentOutput, expected: str, label: str) -> EvalResult:
    got = output.discovery.product_fit
    passed = got == expected
    return EvalResult(
        name=f"{label}: product_fit == '{expected}'",
        passed=passed,
        reason=f"got '{got}'" if not passed else f"product_fit correctly classified as '{got}'",
    )


def check_no_em_dashes(output: AgentOutput, label: str) -> EvalResult:
    body = output.email.body
    found = "—" in body or " -- " in body
    return EvalResult(
        name=f"{label}: no em-dashes in email",
        passed=not found,
        reason="em-dash found in email body" if found else "clean",
    )


def check_email_cites(output: AgentOutput, substring: str, label: str) -> EvalResult:
    body = output.email.body.lower()
    passed = substring.lower() in body
    return EvalResult(
        name=f"{label}: email cites '{substring}'",
        passed=passed,
        reason=f"'{substring}' not found in email body" if not passed else f"found '{substring}' in email",
    )


# ---------------------------------------------------------------------------
# Claude-as-judge checks — LLM rates a yes/no question, returns reasoning
# ---------------------------------------------------------------------------

JUDGE_SYSTEM = """You are an evaluator for an AI sales agent. You will be given an agent output and a yes/no evaluation question.

Reply in this exact format:
VERDICT: YES
REASON: one sentence explaining your verdict.

or:
VERDICT: NO
REASON: one sentence explaining your verdict.

Be strict. Only answer YES if the evidence is clearly present."""


def claude_judge(question: str, context: str) -> tuple[bool, str]:
    """Ask Claude to evaluate a yes/no question about agent output. Returns (passed, reason)."""
    response = CLIENT.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        system=JUDGE_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": f"Question: {question}\n\nContext:\n{context}",
            }
        ],
    )
    text = response.content[0].text.strip()
    passed = text.upper().startswith("VERDICT: YES")
    reason_line = next((l for l in text.splitlines() if l.upper().startswith("REASON:")), "")
    reason = reason_line[len("REASON:"):].strip() if reason_line else text
    return passed, reason


def check_email_grounded(output: AgentOutput, label: str) -> EvalResult:
    context = (
        f"Discovery summary:\n{output.discovery.summary}\n\n"
        f"Discovery metrics:\n" + "\n".join(output.discovery.metrics) + "\n\n"
        f"Email body:\n{output.email.body}"
    )
    passed, reason = claude_judge(
        question=(
            "Does the email avoid inventing numbers or facts not present in the "
            "discovery summary and metrics? Answer YES if all specific figures in "
            "the email are traceable to the discovery."
        ),
        context=context,
    )
    return EvalResult(name=f"{label}: email is grounded (no invented numbers)", passed=passed, reason=reason)


def check_email_covers_both_products(output: AgentOutput, label: str) -> EvalResult:
    context = (
        f"product_fit: {output.discovery.product_fit}\n\n"
        f"Email body:\n{output.email.body}"
    )
    passed, reason = claude_judge(
        question=(
            "Does the email clearly address both the Core product (data pipeline, "
            "warehouse connectors) and the Measurement product (MMM, incrementality) "
            "as distinct topics, given that product_fit is 'both'?"
        ),
        context=context,
    )
    return EvalResult(
        name=f"{label}: email covers both Core and Measurement", passed=passed, reason=reason
    )


# ---------------------------------------------------------------------------
# Main — run all checks
# ---------------------------------------------------------------------------

TRANSCRIPTS = {
    "bellwether": REPO_ROOT / "fixtures" / "transcript-01-bellwether-coffee.md",
    "cirra":      REPO_ROOT / "fixtures" / "transcript-02-cirra-insurance.md",
    "lyridon":    REPO_ROOT / "fixtures" / "transcript-03-lyridon.md",
}


def main():
    print("Running agent on all three transcripts...\n")
    outputs: dict[str, AgentOutput] = {}
    for name, path in TRANSCRIPTS.items():
        print(f"  {name}...")
        outputs[name] = run_agent(path.read_text(encoding="utf-8"), client=CLIENT)
    print()

    checks: list[EvalResult] = [
        # Structured: product_fit classification
        check_product_fit(outputs["bellwether"], "core-only",         "Bellwether"),
        check_product_fit(outputs["cirra"],      "measurement-only",  "Cirra"),
        check_product_fit(outputs["lyridon"],    "both",              "Lyridon"),
        # Structured: no em-dashes in any email
        check_no_em_dashes(outputs["bellwether"], "Bellwether"),
        check_no_em_dashes(outputs["cirra"],      "Cirra"),
        check_no_em_dashes(outputs["lyridon"],    "Lyridon"),
        # Structured: correct case study cited
        check_email_cites(outputs["bellwether"], "Aurelia Skin",   "Bellwether"),
        check_email_cites(outputs["cirra"],      "Parallax",       "Cirra"),
        # Claude-as-judge: grounding and coverage
        check_email_grounded(outputs["bellwether"],              "Bellwether"),
        check_email_covers_both_products(outputs["lyridon"],     "Lyridon"),
    ]

    print("=" * 60)
    print("EVAL RESULTS")
    print("=" * 60)
    for check in checks:
        print(check)
        print()

    passed = sum(1 for c in checks if c.passed)
    total = len(checks)
    print("=" * 60)
    print(f"SCORE: {passed}/{total}")
    print("=" * 60)

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
