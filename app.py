"""Streamlit UI for the Sales Engineering Agent.

Landing page explains the tool. User uploads a discovery transcript
(.md, .txt, .pdf, or .docx). The agent runs and displays results in three tabs.

Run with:
    uv run streamlit run app.py
"""

import io
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
# Global CSS — navy palette, card styles, tab overrides
# ---------------------------------------------------------------------------

NAVY       = "#0f2244"
NAVY_MID   = "#1a3a6e"
NAVY_LIGHT = "#eef2f8"
ACCENT     = "#2563eb"
WHITE      = "#ffffff"

st.markdown(f"""
<style>
  /* ── Layout ── */
  .block-container {{ padding-top: 1.5rem !important; max-width: 1100px; }}
  [data-testid="stAppViewContainer"] {{ background: #f8f9fc; }}

  /* ── Hide Streamlit's auto-anchor icons on custom HTML headings ── */
  [data-testid="stHeadingAnchorLink"] {{ display: none !important; }}
  .hero h1 a, .step-card h4 a, .upload-card h3 a {{ display: none !important; }}

  /* ── Hero banner ── */
  .hero {{
    background: linear-gradient(135deg, {NAVY} 0%, {NAVY_MID} 100%);
    border-radius: 16px;
    padding: 3rem 2.75rem;
    margin-bottom: 2rem;
    color: {WHITE};
    position: relative;
    overflow: hidden;
  }}
  .hero-deco {{
    position: absolute;
    right: -50px;
    bottom: -60px;
    width: 340px;
    height: 340px;
    pointer-events: none;
    z-index: 1;
  }}
  .hero .hero-eyebrow,
  .hero h1,
  .hero p,
  .hero div {{ position: relative; z-index: 2; }}
  .hero-eyebrow {{
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.55);
    margin-bottom: 0.6rem;
  }}
  .hero h1 {{
    color: {WHITE};
    font-size: 2.4rem;
    font-weight: 800;
    margin: 0 0 0.75rem;
    line-height: 1.15;
  }}
  .hero p {{
    color: rgba(255,255,255,0.78);
    font-size: 1.05rem;
    margin: 0;
    max-width: 620px;
    line-height: 1.6;
  }}

  /* ── Step cards ── */
  .steps-grid {{ display: flex; gap: 1rem; margin-bottom: 2rem; }}
  .step-card {{
    flex: 1;
    background: {WHITE};
    border-radius: 12px;
    border-top: 4px solid {NAVY};
    padding: 1.4rem 1.4rem 1.6rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
  }}
  .step-card-top {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.85rem;
  }}
  .step-num {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px; height: 26px;
    background: {NAVY};
    color: {WHITE};
    border-radius: 50%;
    font-size: 0.78rem;
    font-weight: 700;
    flex-shrink: 0;
  }}
  .step-icon {{
    width: 44px; height: 44px;
    background: {NAVY_LIGHT};
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: {NAVY};
    flex-shrink: 0;
  }}
  .step-card h4 {{
    margin: 0 0 0.3rem;
    font-size: 0.95rem;
    font-weight: 700;
    color: {NAVY};
  }}
  .step-card p {{
    margin: 0;
    font-size: 0.85rem;
    color: #4b5563;
    line-height: 1.5;
  }}

  /* ── Upload card (top) + file uploader (bottom) merged into one card ── */
  .upload-card {{
    background: {WHITE};
    border: 2px dashed {NAVY};
    border-bottom: none;
    border-radius: 14px 14px 0 0;
    padding: 1.75rem 2rem 1.25rem;
    margin-bottom: 0;
  }}
  .upload-card h3 {{
    color: {NAVY};
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0 0 0.3rem;
  }}
  .upload-card p {{
    color: #6b7280;
    font-size: 0.88rem;
    margin: 0;
  }}
  /* Remove Streamlit's default gap after the upload-card markdown block */
  .element-container:has(.upload-card) {{
    margin-bottom: 0 !important;
  }}
  /* Style the file uploader as the bottom half of the card */
  [data-testid="stFileUploader"] {{
    background: {WHITE};
    border-left: 2px dashed {NAVY};
    border-right: 2px dashed {NAVY};
    border-bottom: 2px dashed {NAVY};
    border-radius: 0 0 14px 14px;
    padding: 1rem 2rem 1.5rem;
    margin-bottom: 1.5rem;
  }}
  /* Soften the inner dropzone so it reads as nested, not doubled-up */
  [data-testid="stFileUploaderDropzone"] {{
    background: {NAVY_LIGHT} !important;
    border-color: #c7d4e8 !important;
    border-radius: 8px !important;
  }}

  /* ── Badges ── */
  .badge {{
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
  }}
  .badge-navy   {{ background: {NAVY};    color: {WHITE}; }}
  .badge-blue   {{ background: {ACCENT};  color: {WHITE}; }}
  .badge-green  {{ background: #059669;   color: {WHITE}; }}
  .badge-orange {{ background: #d97706;   color: {WHITE}; }}
  .badge-gray   {{ background: #6b7280;   color: {WHITE}; }}

  /* ── Results section header ── */
  .results-header {{
    background: {NAVY};
    border-radius: 10px;
    padding: 0.9rem 1.4rem;
    color: {WHITE};
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 1.25rem;
  }}

  /* ── Discovery field card ── */
  .field-card {{
    background: {WHITE};
    border-left: 4px solid {NAVY};
    border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }}
  .field-label {{
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: {NAVY};
    margin-bottom: 0.35rem;
  }}

  /* ── Case study card ── */
  .cs-card {{
    background: {WHITE};
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    border-top: 4px solid {NAVY};
    padding: 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }}
  .cs-score {{
    float: right;
    background: {NAVY_LIGHT};
    color: {NAVY};
    font-size: 0.78rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
  }}

  /* ── Email card ── */
  .email-card {{
    background: {WHITE};
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    padding: 2rem 2.25rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    white-space: pre-wrap;
    font-size: 0.95rem;
    line-height: 1.7;
    color: #1f2937;
  }}
  .email-subject {{
    font-size: 1.05rem;
    font-weight: 700;
    color: {NAVY};
    padding: 0.75rem 1.2rem;
    background: {NAVY_LIGHT};
    border-radius: 8px;
    margin-bottom: 1.25rem;
  }}

  /* ── Streamlit tab override ── */
  button[data-baseweb="tab"] {{
    font-weight: 600 !important;
    color: #4b5563 !important;
  }}
  button[data-baseweb="tab"][aria-selected="true"] {{
    color: {NAVY} !important;
    border-bottom-color: {NAVY} !important;
  }}

  /* ── Streamlit button ── */
  .stDownloadButton > button {{
    background: {NAVY} !important;
    color: {WHITE} !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.25rem !important;
  }}
  .stDownloadButton > button:hover {{
    background: {NAVY_MID} !important;
  }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Hero banner
# ---------------------------------------------------------------------------

st.markdown(f"""
<div class="hero">
  <div class="hero-eyebrow">Powered by Claude</div>
  <h1>Sales Engineering Agent</h1>
  <p>A Claude-powered agent built for <strong style="color:rgba(255,255,255,0.95)">Attributary</strong>,
  a fictional marketing data platform with two product lines: Core (data pipeline and warehouse connectors)
  and Measurement (marketing mix modelling and incrementality testing).</p>
  <p style="margin-top:0.75rem;">
  Upload a sales discovery call transcript and the agent runs three tools automatically: it extracts
  a structured MEDDPICC analysis, retrieves the most relevant customer case studies from the knowledge base,
  and drafts a tailored follow-up email grounded in both. No invented numbers. No hallucinated references.
  All three artefacts in under 60 seconds.</p>
  <div style="margin-top:1.5rem; padding-top:1.25rem; border-top:1px solid rgba(255,255,255,0.15);
              display:flex; gap:1.5rem; flex-wrap:wrap;">
    <span style="font-size:0.8rem; color:rgba(255,255,255,0.55);">
      Built with &nbsp;
      <strong style="color:rgba(255,255,255,0.85);">Claude API</strong> &nbsp;·&nbsp;
      <strong style="color:rgba(255,255,255,0.85);">Python</strong> &nbsp;·&nbsp;
      <strong style="color:rgba(255,255,255,0.85);">Pydantic</strong> &nbsp;·&nbsp;
      <strong style="color:rgba(255,255,255,0.85);">Streamlit</strong>
    </span>
    <span style="font-size:0.8rem; color:rgba(255,255,255,0.55);">
      Skills demonstrated &nbsp;
      <strong style="color:rgba(255,255,255,0.85);">Tool use</strong> &nbsp;·&nbsp;
      <strong style="color:rgba(255,255,255,0.85);">Structured outputs</strong> &nbsp;·&nbsp;
      <strong style="color:rgba(255,255,255,0.85);">RAG retrieval</strong> &nbsp;·&nbsp;
      <strong style="color:rgba(255,255,255,0.85);">Eval harness</strong>
    </span>
  </div>

  <!-- Decorative blob + icon -->
  <svg class="hero-deco" viewBox="0 0 360 360" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- Blob fill -->
    <path d="M185 28 C255 14 338 68 346 152 C354 236 298 318 214 330 C130 342 52 286 34 202 C16 118 58 38 122 24 C143 18 164 32 185 28 Z"
          fill="rgba(255,255,255,0.07)"/>
    <!-- Offset outline (slightly larger, rotated feel) -->
    <path d="M200 18 C272 4 355 58 361 144 C367 228 310 312 226 326 C142 340 62 282 44 196 C26 110 70 30 136 16 C158 10 178 22 200 18 Z"
          fill="none" stroke="rgba(147,197,253,0.28)" stroke-width="1.5"/>
    <!-- Large magnifying glass icon, centred in blob -->
    <circle cx="168" cy="162" r="58" stroke="rgba(255,255,255,0.16)" stroke-width="14" fill="none"/>
    <line x1="213" y1="207" x2="250" y2="244" stroke="rgba(255,255,255,0.16)" stroke-width="14" stroke-linecap="round"/>
  </svg>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# What you get — three output cards
# ---------------------------------------------------------------------------

st.markdown(f"""
<div style="margin-bottom:0.75rem;">
  <span style="font-size:0.72rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:{NAVY};">
    The outputs
  </span>
  <div style="height:3px; background:{NAVY}; border-radius:2px; margin-top:0.4rem; width:40px;"></div>
</div>
<div class="steps-grid">
  <div class="step-card">
    <div class="step-card-top">
      <div class="step-num">1</div>
      <div class="step-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
      </div>
    </div>
    <h4>Structured discovery</h4>
    <p>Extracts MEDDPICC fields and classifies product-fit (Core vs Measurement) from spend and pain signals in the transcript.</p>
  </div>
  <div class="step-card">
    <div class="step-card-top">
      <div class="step-num">2</div>
      <div class="step-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <ellipse cx="12" cy="5" rx="9" ry="3"/>
          <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
          <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
        </svg>
      </div>
    </div>
    <h4>Case study retrieval</h4>
    <p>Matches the discovery against a knowledge base of customer case studies, filtered and ranked by product line fit.</p>
  </div>
  <div class="step-card">
    <div class="step-card-top">
      <div class="step-num">3</div>
      <div class="step-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="4" width="20" height="16" rx="2"/>
          <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
        </svg>
      </div>
    </div>
    <h4>Follow-up email</h4>
    <p>Drafts a tailored email grounded in the discovery and retrieved case studies. Every figure traces back to the transcript.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# File upload
# ---------------------------------------------------------------------------

st.markdown(f"""
<div class="upload-card">
  <h3>Upload a transcript</h3>
  <p>Accepts .md, .txt, .pdf, or .docx. Paste or export your discovery call notes directly.</p>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Choose file",
    type=["md", "txt", "pdf", "docx"],
    label_visibility="collapsed",
)

if not uploaded:
    st.stop()

# ---------------------------------------------------------------------------
# Parse file by type
# ---------------------------------------------------------------------------

def extract_text(file) -> str:
    name = file.name.lower()
    raw = file.read()

    if name.endswith(".pdf"):
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(raw))
        pages = [p.extract_text() for p in reader.pages if p.extract_text()]
        return "\n\n".join(pages)

    if name.endswith(".docx"):
        from docx import Document
        doc = Document(io.BytesIO(raw))
        return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())

    return raw.decode("utf-8")


transcript = extract_text(uploaded)

if not transcript.strip():
    st.error("Could not extract text from the uploaded file. Please try a different format.")
    st.stop()

st.markdown(
    f'<p style="color:#6b7280; font-size:0.85rem; margin-bottom:1rem;">'
    f'<strong style="color:{NAVY};">{uploaded.name}</strong> &nbsp;·&nbsp; {len(transcript):,} characters extracted</p>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Run agent with live progress
# ---------------------------------------------------------------------------

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
        with _status_container.status(TOOL_LABELS.get(tool_name, tool_name), expanded=False) as s:
            result = inner(tool_name, tool_input)
            s.update(label=TOOL_DONE.get(tool_name, tool_name), state="complete")
        return result
    return verbose_dispatch

_agent_mod._make_dispatch = _make_verbose_dispatch

with st.spinner("Running agent..."):
    try:
        output = run_agent(transcript)
    except Exception as e:
        st.error(f"Agent failed: {type(e).__name__}: {e}")
        st.stop()
    finally:
        _agent_mod._make_dispatch = _original_make_dispatch

_status_container.empty()

st.markdown(
    f'<div style="background:#dcfce7; border:1px solid #86efac; border-radius:8px; '
    f'padding:0.65rem 1rem; color:#166534; font-weight:600; margin-bottom:1.5rem;">'
    f'Agent complete. All three artefacts generated.</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Results — three tabs
# ---------------------------------------------------------------------------

tab_discovery, tab_cases, tab_email = st.tabs(["Discovery", "Case Studies", "Follow-up Email"])

# -- Tab 1: Discovery --------------------------------------------------------

with tab_discovery:
    d = output.discovery

    # Product fit + champion badges
    fit_badge = {
        "core-only":        ("badge-blue",   "Core only"),
        "measurement-only": ("badge-orange",  "Measurement only"),
        "both":             ("badge-green",   "Core + Measurement"),
        "unclear":          ("badge-gray",    "Unclear"),
    }
    fit_cls, fit_label = fit_badge.get(d.product_fit, ("badge-gray", d.product_fit))

    champ = d.champion
    if champ.status == "confirmed":
        champ_html = f'<span class="badge badge-green">Champion confirmed</span> &nbsp; {champ.name}'
    elif champ.status == "forming":
        champ_html = f'<span class="badge badge-orange">Champion forming</span> &nbsp; {champ.name}'
    else:
        champ_html = '<span class="badge badge-gray">No champion identified</span>'

    st.markdown(f"""
    <div style="display:flex; gap:1rem; align-items:center; flex-wrap:wrap; margin-bottom:1.25rem;">
      <span class="badge {fit_cls}">{fit_label}</span>
      {champ_html}
    </div>
    """, unsafe_allow_html=True)

    # Summary
    st.markdown(f"""
    <div class="field-card">
      <div class="field-label">Summary</div>
      <div style="font-size:0.95rem; color:#1f2937; line-height:1.6;">{d.summary}</div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    def field_card(label, items):
        if not items:
            return ""
        if isinstance(items, str):
            body = f'<div style="font-size:0.9rem; color:#1f2937;">{items}</div>'
        else:
            rows = "".join(f'<li style="margin-bottom:0.3rem;">{i}</li>' for i in items)
            body = f'<ul style="margin:0; padding-left:1.2rem; font-size:0.9rem; color:#374151;">{rows}</ul>'
        return f'<div class="field-card"><div class="field-label">{label}</div>{body}</div>'

    with col_left:
        if d.economic_buyer:
            st.markdown(field_card("Economic buyer", d.economic_buyer), unsafe_allow_html=True)
        if d.timeline:
            st.markdown(field_card("Timeline", d.timeline), unsafe_allow_html=True)
        if d.metrics:
            st.markdown(field_card("Metrics", d.metrics), unsafe_allow_html=True)

    with col_right:
        if d.identify_pain:
            st.markdown(field_card("Pain", d.identify_pain), unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        if d.decision_criteria:
            st.markdown(field_card("Decision criteria", d.decision_criteria), unsafe_allow_html=True)
        if d.competition:
            st.markdown(field_card("Competition", d.competition), unsafe_allow_html=True)
    with col4:
        if d.decision_process:
            st.markdown(field_card("Decision process", d.decision_process), unsafe_allow_html=True)
        if d.paper_process:
            st.markdown(field_card("Paper process", d.paper_process), unsafe_allow_html=True)

# -- Tab 2: Case Studies -----------------------------------------------------

with tab_cases:
    if not output.case_studies:
        st.info("No case studies matched.")
    for i, cs in enumerate(output.case_studies, 1):
        reasons_html = "".join(
            f'<li style="margin-bottom:0.25rem; font-size:0.88rem; color:#374151;">{r}</li>'
            for r in cs.match_reasons
        )
        st.markdown(f"""
        <div class="cs-card">
          <div class="cs-score">Score: {cs.score:.0f}</div>
          <div style="font-size:1rem; font-weight:700; color:{NAVY}; margin-bottom:0.5rem;">{i}. {cs.title}</div>
          <div style="font-size:0.75rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase;
                      color:{NAVY}; margin-bottom:0.35rem;">Why retrieved</div>
          <ul style="margin:0 0 0.5rem; padding-left:1.2rem;">{reasons_html}</ul>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("View full case study"):
            st.markdown(cs.content)

# -- Tab 3: Follow-up Email --------------------------------------------------

with tab_email:
    st.markdown(f'<div class="email-subject">Subject: {output.email.subject}</div>', unsafe_allow_html=True)
    # Render body preserving line breaks
    body_html = output.email.body.replace("\n", "<br>")
    st.markdown(f'<div class="email-card">{body_html}</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.download_button(
        label="Download email",
        data=f"Subject: {output.email.subject}\n\n{output.email.body}",
        file_name="followup-email.txt",
        mime="text/plain",
    )
