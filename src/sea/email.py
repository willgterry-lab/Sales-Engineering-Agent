"""Follow-up email drafting tool.

Takes a validated MEDDPICCDiscovery and retrieved case studies, returns a
structured FollowupEmail object via forced tool use.

This is the one tool in the pipeline that calls Claude for generation rather
than extraction. The case studies retrieved by Tool 2 are injected into the
prompt here — that is the grounding step that prevents hallucinated references.
"""

from typing import Optional

from anthropic import Anthropic
from pydantic import BaseModel, Field

from sea.discovery import MEDDPICCDiscovery
from sea.retrieval import RetrievalResult


# -----------------------------------------------------------------------------
# Output schema
# -----------------------------------------------------------------------------

class FollowupEmail(BaseModel):
    """A structured follow-up email from an SC/AE after a discovery call."""

    subject: str = Field(
        description=(
            "Email subject line. Specific to this prospect. References the call "
            "or the primary pain. No generic 'Following up' openers."
        ),
    )
    body: str = Field(
        description=(
            "Full email body as plain text. Paragraphs separated by blank lines. "
            "Signed off as Marcus Hale, Account Executive, Attributary. "
            "No em-dashes anywhere. UK English. "
            "Must cite at least one specific number from the discovery. "
            "Must reference at least one retrieved case study by name with a "
            "specific metric from it. "
            "Must include a clear, single next step."
        ),
    )


# -----------------------------------------------------------------------------
# System prompt
# -----------------------------------------------------------------------------

SYSTEM_PROMPT = """You are Marcus Hale, Account Executive at Attributary, drafting a follow-up email after a sales discovery call. You write on behalf of the Attributary sales team.

Rules:
- No em-dashes anywhere. Replace with commas, full stops, semicolons, or brackets.
- UK English: organise, recognise, specialise, colour, favour.
- Be specific. Use exact numbers from the discovery and exact metrics from the case studies.
- Do not invent numbers, names, or outcomes not present in the inputs.
- Cite retrieved case studies by their customer name and include one concrete metric from each you reference.
- Address the email to the champion if one is identified (confirmed or forming). If none, address to the economic buyer.
- Match tone and urgency to the timeline signal in the discovery.
- One clear next step at the end. No list of three options.
- Keep it under 350 words. Discovery calls warrant a focused note, not a deck.
- Do not use: leverage, spearhead, synergy, robust, seamless, cutting-edge, passionate, results-driven.
"""


# -----------------------------------------------------------------------------
# Prompt builder
# -----------------------------------------------------------------------------

def _build_user_prompt(
    discovery: MEDDPICCDiscovery,
    case_studies: list[RetrievalResult],
) -> str:
    champion_line = (
        f"{discovery.champion.name} ({discovery.champion.status} champion)"
        if discovery.champion.name
        else "no champion identified yet"
    )

    pain_block = "\n".join(f"- {p}" for p in discovery.identify_pain)
    criteria_block = "\n".join(f"- {c}" for c in discovery.decision_criteria)
    metrics_block = "\n".join(f"- {m}" for m in discovery.metrics)
    process_block = "\n".join(f"- {s}" for s in discovery.decision_process)

    case_study_block = ""
    for i, cs in enumerate(case_studies, 1):
        case_study_block += f"\n### Case Study {i}: {cs.title}\n{cs.content}\n"

    return f"""Draft a follow-up email using the discovery summary and retrieved case studies below.

## Discovery summary

Product fit: {discovery.product_fit}
Champion: {champion_line}
Economic buyer: {discovery.economic_buyer or 'not yet identified'}
Timeline: {discovery.timeline or 'not surfaced'}
Summary: {discovery.summary}

### Pain points
{pain_block}

### Key metrics from the call
{metrics_block}

### Decision criteria
{criteria_block}

### Decision process
{process_block}

## Retrieved case studies (ground the email in these — do not invent alternatives)
{case_study_block}
"""


# -----------------------------------------------------------------------------
# Public interface
# -----------------------------------------------------------------------------

def draft_followup_email(
    discovery: MEDDPICCDiscovery,
    case_studies: list[RetrievalResult],
    client: Optional[Anthropic] = None,
    model: str = "claude-sonnet-4-6",
) -> FollowupEmail:
    """Draft a follow-up email grounded in the discovery and retrieved case studies.

    Returns a validated FollowupEmail object. Raises if the model fails to
    produce the expected tool_use block.
    """
    client = client or Anthropic()

    tool_schema = FollowupEmail.model_json_schema()
    user_prompt = _build_user_prompt(discovery, case_studies)

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=[
            {
                "name": "record_email",
                "description": "Record the drafted follow-up email.",
                "input_schema": tool_schema,
            }
        ],
        tool_choice={"type": "tool", "name": "record_email"},
        messages=[{"role": "user", "content": user_prompt}],
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "record_email":
            return FollowupEmail.model_validate(block.input)

    raise RuntimeError("Expected a record_email tool_use block in the response.")
