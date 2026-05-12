"""Three-tool agent loop.

Orchestrates extract_structured_discovery -> retrieve_case_studies ->
draft_followup_email in a single Claude-driven loop.

Design notes:
- Claude acts as orchestrator. It decides which tool to call and when.
- The loop maintains a state dict so tools share results without Claude
  shuttling large JSON payloads back and forth.
- Tool schemas are intentionally minimal: tools 2 and 3 take no arguments
  because they read from state, not from Claude's output.
- Max 10 iterations as a safety cap (CLAUDE.md standing rule).
"""

import json
from typing import Optional

from anthropic import Anthropic
from pydantic import BaseModel

from sea.discovery import MEDDPICCDiscovery, extract_discovery
from sea.email import FollowupEmail, draft_followup_email
from sea.retrieval import RetrievalResult, retrieve_case_studies

MAX_ITERATIONS = 10


# -----------------------------------------------------------------------------
# Agent output
# -----------------------------------------------------------------------------

class AgentOutput(BaseModel):
    discovery: MEDDPICCDiscovery
    case_studies: list[RetrievalResult]
    email: FollowupEmail


# -----------------------------------------------------------------------------
# Tool schemas
# The schemas are what Claude sees. Descriptions are the prompt.
# Tools 2 and 3 take no arguments — state is maintained in the loop.
# -----------------------------------------------------------------------------

TOOLS = [
    {
        "name": "extract_structured_discovery",
        "description": (
            "Extract a structured MEDDPICC discovery object from the transcript. "
            "Call this first."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "transcript": {
                    "type": "string",
                    "description": "The full discovery call transcript.",
                }
            },
            "required": ["transcript"],
        },
    },
    {
        "name": "retrieve_case_studies",
        "description": (
            "Retrieve relevant case studies from the knowledge base, using the "
            "discovery extracted in the previous step. Call this second."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "draft_followup_email",
        "description": (
            "Draft a tailored follow-up email grounded in the discovery and "
            "retrieved case studies. Call this third, after both previous tools."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]

SYSTEM_PROMPT = """You are an AI assistant that helps sales teams process discovery call transcripts.

When given a transcript, you must call the three tools in order:
1. extract_structured_discovery — to extract structured MEDDPICC discovery
2. retrieve_case_studies — to find relevant case studies from the knowledge base
3. draft_followup_email — to produce a tailored follow-up email

Call each tool exactly once. Do not skip steps. Do not call them out of order.
After all three tool calls complete, confirm what was produced in one short sentence.
"""


# -----------------------------------------------------------------------------
# Dispatch — maps tool names to Python functions, using shared state
# -----------------------------------------------------------------------------

def _make_dispatch(transcript: str, state: dict, client: Anthropic, model: str):
    """Returns a dispatch function closed over shared state."""

    def dispatch(tool_name: str, tool_input: dict) -> str:
        if tool_name == "extract_structured_discovery":
            discovery = extract_discovery(
                tool_input["transcript"], client=client, model=model
            )
            state["discovery"] = discovery
            return discovery.model_dump_json()

        if tool_name == "retrieve_case_studies":
            if "discovery" not in state:
                return json.dumps({"error": "extract_structured_discovery must run first"})
            results = retrieve_case_studies(state["discovery"], top_k=2)
            state["case_studies"] = results
            return json.dumps([r.model_dump() for r in results])

        if tool_name == "draft_followup_email":
            if "discovery" not in state or "case_studies" not in state:
                return json.dumps({"error": "both prior tools must run first"})
            email = draft_followup_email(
                state["discovery"], state["case_studies"], client=client, model=model
            )
            state["email"] = email
            return email.model_dump_json()

        return json.dumps({"error": f"unknown tool: {tool_name}"})

    return dispatch


# -----------------------------------------------------------------------------
# Agent loop
# -----------------------------------------------------------------------------

def run_agent(
    transcript: str,
    client: Optional[Anthropic] = None,
    model: str = "claude-sonnet-4-6",
) -> AgentOutput:
    """Run the three-tool agent loop on a discovery transcript.

    Returns an AgentOutput with all three artefacts. Raises if the loop
    exceeds MAX_ITERATIONS or if any required artefact is missing at the end.
    """
    client = client or Anthropic()
    state: dict = {}
    dispatch = _make_dispatch(transcript, state, client, model)

    messages = [{"role": "user", "content": f"Process this discovery transcript:\n\n{transcript}"}]

    for iteration in range(MAX_ITERATIONS):
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            break

        # Collect and execute all tool calls in this turn
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = dispatch(block.name, block.input)
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )

        if not tool_results:
            break

        messages.append({"role": "user", "content": tool_results})
    else:
        raise RuntimeError(f"Agent loop exceeded {MAX_ITERATIONS} iterations.")

    missing = [k for k in ("discovery", "case_studies", "email") if k not in state]
    if missing:
        raise RuntimeError(f"Agent loop completed but missing artefacts: {missing}")

    return AgentOutput(
        discovery=state["discovery"],
        case_studies=state["case_studies"],
        email=state["email"],
    )
