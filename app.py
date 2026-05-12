"""Streamlit UI for the Sales Engineering Agent.

Landing page explains the tool. User uploads a discovery transcript (.md or .txt).
The agent runs and displays structured results in three tabs.

Run with:
    uv run streamlit run app.py
"""

from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

from sea.agent import run_agent

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Sales Engineering Agent",
    page_icon="🔍",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Landing page
# ---------------------------------------------------------------------------

st.title("Sales Engineering Agent")
st.caption("Powered by Claude")

st.markdown("""
Upload a discovery call transcript and the agent will produce three artefacts automatically:

| Step | Tool | Output |
|------|------|--------|
| 1 | `extract_structured_discovery` | Structured MEDDPICC discovery with product-fit classification |
| 2 | `retrieve_case_studies` | Relevant customer case studies from the knowledge base |
| 3 | `draft_followup_email` | Tailored follow-up email grounded in the discovery and case studies |

The agent is built on the **Attributary** fixture, a fictional multi-product marketing data platform
with two product lines: **Core** (data pipeline, warehouse connectors) and **Measurement** (MMM, incrementality testing).
Product-fit is classified automatically from spend signals in the transcript.
""")

st.divider()

# ---------------------------------------------------------------------------
# File upload
# ---------------------------------------------------------------------------

uploaded = st.file_uploader(
    "Upload a discovery call transcript",
    type=["md", "txt"],
    help="Plain text or Markdown file. The agent expects a transcript of a sales discovery call.",
)

if not uploaded:
    st.info("Upload a transcript above to run the agent.")
    st.stop()

# ---------------------------------------------------------------------------
# Run agent with live progress
# ---------------------------------------------------------------------------

transcript = uploaded.read().decode("utf-8")

st.markdown(f"**File:** {uploaded.name} &nbsp; ({len(transcript):,} characters)")
st.divider()

# Patch the agent's dispatch to report progress into Streamlit status blocks.
import sea.agent as _agent_mod

_original_make_dispatch = _agent_mod._make_dispatch

TOOL_LABELS = {
    "extract_structured_discovery": "Extracting MEDDPICC discovery...",
    "retrieve_case_studies":        "Retrieving case studies...",
    "draft_followup_email":         "Drafting follow-up email...",
}
TOOL_DONE = {
    "extract_structured_discovery": "Discovery extracted",
    "retrieve_case_studies":        "Case studies retrieved",
    "draft_followup_email":         "Email drafted",
}

_status_container = st.empty()

def _make_verbose_dispatch(transcript_inner, state, client, model):
    inner = _original_make_dispatch(transcript_inner, state, client, model)

    def verbose_dispatch(tool_name, tool_input):
        label = TOOL_LABELS.get(tool_name, tool_name)
        done_label = TOOL_DONE.get(tool_name, tool_name)
        with _status_container.status(label, expanded=False) as s:
            result = inner(tool_name, tool_input)
            s.update(label=done_label, state="complete")
        return result

    return verbose_dispatch

_agent_mod._make_dispatch = _make_verbose_dispatch

with st.spinner("Running agent..."):
    try:
        output = run_agent(transcript)
    except Exception as e:
        st.error(f"Agent failed: {e}")
        st.stop()
    finally:
        _agent_mod._make_dispatch = _original_make_dispatch

_status_container.empty()
st.success("Agent complete.")
st.divider()

# ---------------------------------------------------------------------------
# Results — three tabs
# ---------------------------------------------------------------------------

tab_discovery, tab_cases, tab_email = st.tabs(["Discovery", "Case Studies", "Follow-up Email"])

# -- Tab 1: Discovery --------------------------------------------------------

with tab_discovery:
    d = output.discovery

    col1, col2 = st.columns(2)
    with col1:
        fit_colour = {"core-only": "blue", "measurement-only": "orange", "both": "green", "unclear": "red"}
        colour = fit_colour.get(d.product_fit, "gray")
        st.markdown(f"**Product fit:** :{colour}[{d.product_fit}]")

    with col2:
        champ = d.champion
        if champ.status == "confirmed":
            st.markdown(f"**Champion:** :green[confirmed] — {champ.name}")
        elif champ.status == "forming":
            st.markdown(f"**Champion:** :orange[forming] — {champ.name}")
        else:
            st.markdown("**Champion:** :gray[none identified]")

    st.markdown(f"**Summary**\n\n{d.summary}")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        if d.economic_buyer:
            st.markdown(f"**Economic buyer**\n\n{d.economic_buyer}")
        if d.timeline:
            st.markdown(f"**Timeline**\n\n{d.timeline}")
        if d.metrics:
            st.markdown("**Metrics**")
            for m in d.metrics:
                st.markdown(f"- {m}")

    with col_right:
        if d.identify_pain:
            st.markdown("**Pain**")
            for p in d.identify_pain:
                st.markdown(f"- {p}")

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        if d.decision_criteria:
            st.markdown("**Decision criteria**")
            for c in d.decision_criteria:
                st.markdown(f"- {c}")
        if d.competition:
            st.markdown("**Competition**")
            for c in d.competition:
                st.markdown(f"- {c}")
    with col4:
        if d.decision_process:
            st.markdown("**Decision process**")
            for s in d.decision_process:
                st.markdown(f"- {s}")
        if d.paper_process:
            st.markdown("**Paper process**")
            for p in d.paper_process:
                st.markdown(f"- {p}")

# -- Tab 2: Case Studies -----------------------------------------------------

with tab_cases:
    if not output.case_studies:
        st.info("No case studies matched.")
    for i, cs in enumerate(output.case_studies, 1):
        with st.expander(f"{i}. {cs.title}  (score: {cs.score:.0f})", expanded=True):
            st.markdown("**Why this was retrieved**")
            for reason in cs.match_reasons:
                st.markdown(f"- {reason}")
            st.divider()
            st.markdown(cs.content)

# -- Tab 3: Follow-up Email --------------------------------------------------

with tab_email:
    st.markdown(f"### {output.email.subject}")
    st.divider()
    st.markdown(output.email.body)
    st.divider()
    st.download_button(
        label="Download email as .txt",
        data=f"Subject: {output.email.subject}\n\n{output.email.body}",
        file_name="followup-email.txt",
        mime="text/plain",
    )
