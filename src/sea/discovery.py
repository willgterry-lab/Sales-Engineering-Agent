"""Structured MEDDPICC discovery extraction.

The first real agent tool. Takes a discovery-call transcript and returns
a structured MEDDPICCDiscovery object. Uses Claude internally via "forced
tool use" to guarantee the output matches the Pydantic schema.

See sc-fde-concepts-glossary.md for the "structured outputs" concept.
"""

from typing import Literal, Optional

from anthropic import Anthropic
from pydantic import BaseModel, Field


# -----------------------------------------------------------------------------
# Output schema — the contract every transcript extraction must satisfy.
# Each field's `description` is read by Claude when it's deciding what to put
# there, so descriptions matter as much as the field names themselves.
# -----------------------------------------------------------------------------

class MEDDPICCDiscovery(BaseModel):
    """Structured discovery output following the MEDDPICC framework."""

    metrics: list[str] = Field(
        default_factory=list,
        description=(
            "Concrete numbers and KPIs mentioned: budget, spend, headcount, "
            "conversion figures, deadlines. Each as a single short line."
        ),
    )
    economic_buyer: Optional[str] = Field(
        default=None,
        description=(
            "Person with budget authority. Name and/or title. "
            "Null if not yet surfaced on the call."
        ),
    )
    decision_criteria: list[str] = Field(
        default_factory=list,
        description=(
            "What the buyer says matters: features, integrations, methodology, "
            "references, support, performance, deployment shape."
        ),
    )
    decision_process: list[str] = Field(
        default_factory=list,
        description=(
            "Steps required to make the purchase: who signs off, procurement, "
            "InfoSec, legal, board approval, paper-flow timing."
        ),
    )
    identify_pain: list[str] = Field(
        default_factory=list,
        description="The actual problems or pressures the buyer is trying to solve.",
    )
    champion: Optional[str] = Field(
        default=None,
        description=(
            "Name and title of the person inside the account most likely to "
            "advocate internally. Be conservative — only name someone who has "
            "clearly advocated, not just engaged with the conversation. "
            "Null if not yet identified."
        ),
    )
    competition: list[str] = Field(
        default_factory=list,
        description=(
            "Competing products, vendors, or build-in-house alternatives "
            "mentioned by the buyer."
        ),
    )
    paper_process: list[str] = Field(
        default_factory=list,
        description=(
            "Procurement, legal, security, or contractual steps required to close."
        ),
    )
    timeline: Optional[str] = Field(
        default=None,
        description=(
            "When the buyer needs to be signed, onboarded, or seeing value. "
            "Null if not surfaced."
        ),
    )
    summary: str = Field(
        description=(
            "A 2-3 sentence neutral summary of the conversation: who, what, why now."
        ),
    )
    product_fit: Literal["core-only", "measurement-only", "both", "unclear"] = Field(
        description=(
            "Read on Attributary product-line fit. Reason from spend signals "
            "(Core fits ~$10k+/month ad spend; Measurement fits $200k+/month) "
            "and pain shape (Core solves data plumbing and reporting; "
            "Measurement solves incrementality and attribution proof)."
        ),
    )


# -----------------------------------------------------------------------------
# Extraction function — Claude calling Claude with forced tool use.
# -----------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an experienced Solutions Consultant reviewing a sales discovery call transcript. Your job is to extract a structured MEDDPICC summary using the record_discovery tool.

Rules:
- Only record what is actually evidenced in the transcript. Do not invent.
- Use null or empty list for any field not surfaced.
- Be conservative on Champion. Only name someone who has clearly advocated, not just engaged with the conversation.
- For product_fit, reason explicitly from two signals: spend (Attributary Core fits ~$10k+/month ad spend; Measurement fits $200k+/month) and pain shape (Core solves data plumbing and reporting; Measurement solves incrementality and attribution proof). If both signals point both ways, return "both". If neither is clear, return "unclear".
- Be specific. "Reporting takes time" is weak; "10 hours per week of manual reporting work" is useful.
"""


def extract_discovery(
    transcript: str,
    client: Optional[Anthropic] = None,
    model: str = "claude-sonnet-4-6",
) -> MEDDPICCDiscovery:
    """Run extraction on a single transcript.

    Returns a validated MEDDPICCDiscovery object. Raises if the model
    fails to produce a tool_use block (should not happen with tool_choice
    forced).
    """
    client = client or Anthropic()

    # Pydantic generates a JSON Schema that matches Anthropic's tool input_schema format.
    tool_schema = MEDDPICCDiscovery.model_json_schema()

    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        tools=[
            {
                "name": "record_discovery",
                "description": (
                    "Record the structured MEDDPICC summary of the discovery call."
                ),
                "input_schema": tool_schema,
            }
        ],
        # Force the model to call this specific tool. No free-form text allowed.
        # This is the trick that makes structured output reliable.
        tool_choice={"type": "tool", "name": "record_discovery"},
        messages=[
            {"role": "user", "content": f"Discovery transcript:\n\n{transcript}"}
        ],
    )

    # With tool_choice forcing this tool, the response WILL contain a matching
    # tool_use block. We pull its `input` (already a dict) and validate via Pydantic.
    for block in response.content:
        if block.type == "tool_use" and block.name == "record_discovery":
            return MEDDPICCDiscovery.model_validate(block.input)

    raise RuntimeError("Expected a record_discovery tool_use block in the response.")
