"""Case study retrieval over the fixture knowledge base.

Stage 1 (this file): keyword scoring. No embeddings, no Claude call.
Stage 2 (future): swap score() for LanceDB vector similarity — same interface,
better recall on indirect matches.

Retrieval pipeline:
  1. Load all case studies from fixtures/.
  2. Hard-filter by product_fit: never return a Measurement case study to a
     core-only prospect or vice versa.
  3. Score eligible studies by keyword overlap between the discovery object
     (pain, competition, summary) and case study text.
  4. Return top-k as RetrievalResult objects.
"""

import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from sea.discovery import MEDDPICCDiscovery

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures"

ProductLine = Literal["core", "measurement"]


# -----------------------------------------------------------------------------
# Data models
# -----------------------------------------------------------------------------

class CaseStudy(BaseModel):
    id: str
    title: str
    content: str
    product_lines: list[ProductLine]


class RetrievalResult(BaseModel):
    case_study_id: str
    title: str
    content: str
    score: float = Field(description="Keyword overlap score. Higher is more relevant.")
    match_reasons: list[str] = Field(
        description="Human-readable explanation of why this case study was selected."
    )


# -----------------------------------------------------------------------------
# Case study registry
# Declares which product lines each fixture case study covers.
# -----------------------------------------------------------------------------

CASE_STUDY_REGISTRY: list[dict] = [
    {
        "id": "aurelia-skin",
        "filename": "case-study-aurelia-skin.md",
        "product_lines": ["core"],
    },
    {
        "id": "parallax-media",
        "filename": "case-study-parallax-media.md",
        "product_lines": ["core", "measurement"],
    },
    {
        "id": "maison-ysault",
        "filename": "case-study-maison-ysault.md",
        "product_lines": ["core", "measurement"],
    },
]


def _load_case_studies() -> list[CaseStudy]:
    studies = []
    for entry in CASE_STUDY_REGISTRY:
        path = FIXTURES_DIR / entry["filename"]
        content = path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else entry["id"]
        studies.append(
            CaseStudy(
                id=entry["id"],
                title=title,
                content=content,
                product_lines=entry["product_lines"],
            )
        )
    return studies


# -----------------------------------------------------------------------------
# Product-fit filter
# -----------------------------------------------------------------------------

def _required_product_lines(product_fit: str) -> set[ProductLine]:
    """Return the set of product lines the prospect qualifies for."""
    if product_fit == "core-only":
        return {"core"}
    if product_fit == "measurement-only":
        return {"measurement"}
    if product_fit == "both":
        return {"core", "measurement"}
    return {"core", "measurement"}  # unclear: don't hard-exclude anything


def _passes_filter(study: CaseStudy, required: set[ProductLine]) -> bool:
    """True if the case study covers at least one required product line."""
    return bool(required.intersection(study.product_lines))


# -----------------------------------------------------------------------------
# Keyword scoring
# -----------------------------------------------------------------------------

def _tokenise(text: str) -> set[str]:
    """Lowercase words, 4+ characters, stripped of punctuation."""
    return {w for w in re.findall(r"[a-z]{4,}", text.lower())}


def _build_query_tokens(discovery: MEDDPICCDiscovery) -> set[str]:
    """Pull signal terms from the discovery object."""
    parts = [
        discovery.summary,
        " ".join(discovery.identify_pain),
        " ".join(discovery.competition),
        " ".join(discovery.decision_criteria),
        discovery.economic_buyer or "",
    ]
    return _tokenise(" ".join(parts))


_STOPWORDS = {
    "that", "this", "with", "from", "have", "they", "their", "will", "been",
    "also", "which", "what", "when", "were", "into", "more", "about", "team",
    "data", "would", "could", "should", "over", "each", "some", "than",
}


def _score(study: CaseStudy, query_tokens: set[str]) -> tuple[float, list[str]]:
    """
    Return (score, match_reasons).

    Score = number of non-stopword query tokens found in the case study text,
    weighted by section. Headline matches count double.
    """
    study_tokens = _tokenise(study.content)
    meaningful_query = query_tokens - _STOPWORDS
    meaningful_study = study_tokens - _STOPWORDS

    hits = meaningful_query & meaningful_study

    # Double-weight terms that appear in the headline (first 200 chars).
    headline_tokens = _tokenise(study.content[:200])
    headline_hits = hits & headline_tokens
    score = len(hits) + len(headline_hits)  # headline hits counted twice

    reasons = []
    if headline_hits:
        reasons.append(f"Headline match on: {', '.join(sorted(headline_hits))}")
    body_only = hits - headline_hits
    if body_only:
        reasons.append(f"Body match on: {', '.join(sorted(body_only))}")

    return float(score), reasons


# -----------------------------------------------------------------------------
# Public interface
# -----------------------------------------------------------------------------

def retrieve_case_studies(
    discovery: MEDDPICCDiscovery,
    top_k: int = 2,
) -> list[RetrievalResult]:
    """Return the top-k most relevant case studies for a given discovery.

    Filters by product_fit first, then ranks by keyword overlap.
    Returns an empty list if no eligible studies score above zero.
    """
    studies = _load_case_studies()
    required = _required_product_lines(discovery.product_fit)
    eligible = [s for s in studies if _passes_filter(s, required)]

    query_tokens = _build_query_tokens(discovery)

    scored: list[tuple[float, list[str], CaseStudy]] = []
    for study in eligible:
        score, reasons = _score(study, query_tokens)
        scored.append((score, reasons, study))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, reasons, study in scored[:top_k]:
        if score == 0:
            continue
        results.append(
            RetrievalResult(
                case_study_id=study.id,
                title=study.title,
                content=study.content,
                score=score,
                match_reasons=reasons if reasons else ["General product-line match"],
            )
        )
    return results
