# Sales Engineering Agent — Claude Working Notes

Persistent context for this project. **Scope: the agent build only.** CV writing, outreach drafts, JD analysis, and interview prep happen in a separate Cowork project, not here.

Read this first, then `docs/sc-fde-project-brief.md` and `docs/sc-fde-concepts-glossary.md` for full project context.

## Project

Will Terry's primary FDE/SC interview portfolio piece. Target audience: Anthropic, Decagon, and other pre-IPO AI-native companies.

A Claude-powered agent that turns a sales discovery-call transcript into three artefacts: structured MEDDPICC discovery, retrieved case studies grounded in a fixture knowledge base, and a tailored follow-up email. Three-tool agent loop, eval harness, Streamlit UI, public deploy by end May 2026.

## Standing rules

1. **No em-dashes anywhere in output.** Hard rule. Replace with full stops, commas, semicolons, or brackets.
2. **Teach concepts as we build.** Will is learning agents, RAG, and evals for the first time. Every meaningful build step needs a plain-English concept layer he can repeat in interviews. New concepts go into the glossary in the same turn they appear.
3. **Progress reports on break, refresher on return.** When Will signals he is stepping away ("dipping out", "back in a few hours"), give a structured progress report covering achievements, current state, and anything to review while away. When he signals he is back, give a refresher with where we left off, pending inputs, and a next-step outline.
4. **UK English.** Organise, optimise, programme, centralise.
5. **No invented metrics or names.** Every number must trace to something Will has told us or to the fixtures. Never round up. Never estimate. Ask if a number is missing.
6. **Attributary fixture IP guardrails.** Category knowledge from Will's Funnel experience is fair game. Non-public Funnel information is not. Fictional company name, invented pricing, invented customer names in every case study.
7. **Tone.** Direct. Cut filler. Short sentences. Avoid leveraged, spearheaded, synergy, robust, passionate, results-driven, dynamic, seamless, cutting-edge, rockstar, ninja, guru, thought leader.

## Current build state

**Tasks complete:**

- Project brief locked at v0.2 (multi-product Attributary persona).
- Fixtures designed: Attributary one-pager, three case studies (Aurelia Skin, Parallax Media, Maison Ysault), three discovery transcripts (Bellwether Coffee, Cirra Insurance, Lyridon). All in `fixtures/`.
- Repo scaffolded with `uv`. Dependencies: `anthropic`, `pydantic`, `python-dotenv`. Working scripts: `scripts/hello_claude.py`, `scripts/agent_loop_demo.py`.

**Task 4 in progress: first real tool, `extract_structured_discovery`.**

- Implemented in `src/sea/discovery.py` using forced tool use with a Pydantic schema.
- Runs via `scripts/extract_discovery_demo.py`. Bellwether passes (returns `core-only`, stable across runs).
- Outstanding: inspect actual extraction JSON for Bellwether; consider revising `champion` field to allow "forming" rather than forcing null-or-named; run against Cirra (expect `measurement-only`) and Lyridon (expect `both`).

**Tasks pending:**

- Tool 2: `retrieve_case_studies`. Keyword match first, then upgrade to LanceDB vector similarity.
- Tool 3: `draft_followup_email`.
- Streamlit UI plus eval harness.
- Deploy on Railway or Fly. README polish. Demo video.

## Architecture decisions

- **Package manager:** `uv`.
- **Vector store:** LanceDB planned for retrieval. Not yet wired up.
- **Model:** `claude-sonnet-4-6` for agent calls. May switch to Haiku for cost on extractor once quality is locked.
- **Structured outputs:** forced tool use with Pydantic schemas. See glossary entry "Structured outputs (and forced tool use)".
- **Agent loop:** custom Python, not a framework. See glossary entry "Agent loop (and tool use)". Dispatches via tool table. Max 10 iterations as safety cap.
