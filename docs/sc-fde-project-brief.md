# Sales Engineering Agent — Project Brief

**Version:** v0.1
**Date:** 22 April 2026
**Owner:** Will Terry
**Status:** Scoped — ready to build

## Concept

A multi-step Claude-powered agent that turns a sales discovery-call transcript into the downstream artefacts an SC would normally produce manually: structured discovery (MEDDPICC-style), retrieved case studies grounded in a fixture knowledge base, and a tailored follow-up email.

This is the 12-week upskilling plan's "discovery-call summariser" elevated from a single-shot summariser into a tool-using agent. Same input surface, substantially more interesting architecture.

## Why this shape

It lets one project serve two audiences:

- **AI-native SC / FDE / pre-sales interviews** (primary): Anthropic, Decagon, other pre-IPO AI companies. The demo lands as "an SC using Claude to close the loop between discovery and follow-up."
- **Decagon specifically**: the architecture, conversation to retrieval to tool-using agent to structured artefacts, is the same pattern Decagon deploys for post-support workflows. The bridge narrative is: "I built this for sales, but adapting to a support use case would be days, not weeks." That adaptability is the FDE skill.

## Fixture persona

**Attributary** is a fictional multi-product marketing data and measurement SaaS in the same category as Funnel (not literal Funnel). Full one-pager at `fixtures/attributary-one-pager.md`. Two product lines sharing a single data foundation:

- **Core**: data pipeline and warehouse load. Connectors across paid and organic marketing sources, transformation, normalisation, onward piping to BI tools, data warehouses and data lakes. Includes an embedded AI reasoning layer that flags real-time anomalies in ingested metrics. Champion: Head of Marketing Ops or Analytics Engineering.
- **Measurement**: model-based measurement of marketing spend effectiveness (MMM, multi-touch attribution, incrementality). Champion: Head of Growth or CMO. Economic buyer on larger deals: CFO.

**Differentiated qualification thresholds.** Core: ~$10k/month ad spend minimum. Measurement: $200k/month ad spend minimum. This asymmetry is a deliberate agent-reasoning challenge. The agent must classify which product line a transcript points to based on spend signals.

**Pricing structure.** Core is consumption-based via Flexpoints (50 FP per connector, 5 FP per data source). Measurement is banded by ad spend and number of models, $6k/month minimum. Large enterprises on either product can spend $1m+/year.

**Why this shape.** Will has deep domain fluency here from 2+ years selling Funnel as SC and AE. That compresses the learning surface to the actually-new parts (agent architecture, retrieval, evals). The multi-product split materially raises the interest level of what the agent has to do: classify pain by product line, retrieve per-product case studies, tailor follow-ups to per-product objection sets. This is an active FDE interview talking point, not window-dressing.

**IP guardrails.** Category knowledge from Will's Funnel experience is fair game; non-public Funnel information is not. Specifically:

- Fictional company name, tagline, founding story. Nothing recognisable as Funnel.
- Invented pricing numbers (close to category norms is fine; exact Funnel figures are not).
- Invented customer names in every case study. Never a customer Will actually worked on.
- Rule of thumb: if it's not in a public blog post or G2 listing, don't use it.

Fixture assets produced:

- Company one-pager: positioning, two product lines, ICP, per-product objections, pricing structure.
- Three fake customer case studies across different verticals: at least one single-product and at least one multi-product deal.
- Three sample discovery-call transcripts at varying quality, covering both product lines.

## v1 scope — demoable by end of May 2026

- Agent loop with three tools:
  1. `extract_structured_discovery`: MEDDPICC-style extraction.
  2. `retrieve_case_studies`: RAG over fixture KB.
  3. `draft_followup_email`: tailored, cites retrieved case studies.
- Eval harness of roughly eight golden transcripts, mixing structured checks and Claude-as-judge.
- Streamlit UI showing the agent trace alongside each artefact.
- Public deployment (Railway or Fly).

## v2 scope — June onwards

- `draft_pov_scope` tool.
- `generate_demo_fixtures` tool.
- `log_to_crm`: mock integration simulating customer-system wiring.
- Basic observability: trace logging and run-diff view.

## Tech stack

- Claude API (official Python SDK).
- Python, with Streamlit for UI.
- LanceDB for vector storage (local, zero-infra).
- Cursor as the development environment.
- Railway or Fly for deployment.

## Success criteria for v1

- End-to-end run from paste-transcript to all three artefacts in under 60 seconds.
- Eval harness gives a repeatable quality score across prompt and model changes.
- A non-technical interviewer can follow a four-minute walkthrough.
- A technical interviewer can open the repo and find the agent loop, tool definitions, and evals without searching.

## Risks

- **Scope creep.** The single most likely failure mode. Hard stop at three tools for v1.
- **Weak fixture data.** If the case studies are thin, retrieval looks pointless. The knowledge base needs real effort.
- **Evaluation theatre.** Evals that always pass prove nothing. They must be designed to actually break the agent.

## Open items to resolve before or during Week 1

- ~~Name for the fictional analytics company and product~~: locked: **Attributary** (22 Apr 2026).
- Final deployment target (Railway vs Fly): low stakes, decide at deploy time.
- Confirm LanceDB performance acceptable on 3-case-study corpus.

## Relationship to the upskilling plan

Replaces the "discovery-call summariser" project track. Weekly cadence unchanged: same ~9hrs/week, same Saturday deep blocks. The elevated ambition is absorbed by skipping the simpler v1 and going directly to an agent loop.
