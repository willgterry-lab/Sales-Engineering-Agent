# Sales Engineering Agent

A Claude-powered agent that turns a sales discovery call transcript into three artefacts: structured MEDDPICC discovery, retrieved case studies, and a tailored follow-up email. Built as a portfolio piece for Field/Sales Engineer and Solutions Consultant roles at AI-native companies.

**Live demo:** [sales-engineering-agent-production.up.railway.app](https://sales-engineering-agent-production.up.railway.app)

---

## What it does

Upload a discovery call transcript. The agent runs three tools in sequence and returns:

1. **Structured MEDDPICC discovery** — extracts Metrics, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Identify Pain, Champion, and Competition from the transcript. Also classifies product-line fit (Core, Measurement, or both) based on spend signals. Output is a validated Pydantic schema, not a free-text summary.

2. **Retrieved case studies** — filters and ranks Attributary's case study knowledge base against the discovery object. Hard-filters by product line so a Core-only prospect never receives a Measurement case study. Returns match scores and per-study explanations of why each was retrieved.

3. **Tailored follow-up email** — drafts a post-call email grounded in the discovery and retrieved case studies. Subject line, body, and references all trace back to the transcript. No invented numbers or hallucinated customer names.

All three artefacts are available to download as PDF.

---

## Architecture

```
transcript (text)
       |
       v
  Agent loop (custom Python, max 10 iterations)
       |
       |-- tool 1: extract_structured_discovery
       |       Claude forced-tool-use call
       |       Returns MEDDPICCDiscovery (Pydantic)
       |
       |-- tool 2: retrieve_case_studies
       |       No Claude call. Keyword scoring over fixtures/
       |       Hard-filtered by product_fit from tool 1
       |       Returns list[RetrievalResult]
       |
       `-- tool 3: draft_followup_email
               Claude call, grounded in tool 1 + tool 2 output
               Returns FollowupEmail (Pydantic)
```

**Why a custom loop rather than a framework.** Claude decides which tool to call and in what order. The loop maintains a shared state dict so tools 2 and 3 can read tool 1's output without Claude shuttling large JSON payloads back through the model. Tool schemas are intentionally minimal: tools 2 and 3 declare no input parameters because all their inputs come from state.

**Structured outputs via forced tool use.** Tool 1 uses Claude's forced tool use mode (passing `tool_choice={"type": "tool", "name": "..."}`) to guarantee the response matches the Pydantic schema. This is more reliable than asking Claude to "output JSON" in the system prompt, because the schema is enforced at the API level.

---

## Tech stack

| Layer | Choice |
|---|---|
| LLM | Claude (Anthropic Python SDK) |
| Structured output | Pydantic v2 + forced tool use |
| Retrieval | Keyword scoring (LanceDB vector similarity planned) |
| UI | Streamlit |
| PDF export | fpdf2 |
| Package manager | uv |
| Deployment | Railway (Docker) |

---

## Project structure

```
sales-engineering-agent/
├── app.py                          # Streamlit UI
├── src/sea/
│   ├── agent.py                    # Three-tool agent loop
│   ├── discovery.py                # Tool 1: MEDDPICC extraction + Pydantic schema
│   ├── retrieval.py                # Tool 2: case study retrieval
│   └── email.py                    # Tool 3: follow-up email drafting
├── fixtures/
│   ├── attributary-one-pager.md    # Fictional company context fed to the agent
│   ├── case-study-aurelia-skin.md
│   ├── case-study-parallax-media.md
│   ├── case-study-maison-ysault.md
│   ├── transcript-01-bellwether-coffee.md
│   ├── transcript-02-cirra-insurance.md
│   └── transcript-03-lyridon.md
├── Dockerfile
└── pyproject.toml
```

---

## The Attributary fixture persona

The agent is built around **Attributary**, a fictional multi-product marketing data and measurement SaaS. Using a fictional company avoids surfacing any non-public information from real employers, while the two-product structure creates a genuinely interesting agent reasoning challenge.

**Two product lines, one data foundation:**

- **Core** — data pipeline and warehouse connectors. Joins marketing sources, transforms and normalises, pushes to BI tools and data warehouses. ICP threshold: ~$10k/month ad spend. Champion: Head of Marketing Ops or Analytics Engineering.
- **Measurement** — marketing mix modelling and incrementality testing. Measures true spend effectiveness across channels. ICP threshold: $200k/month ad spend. Champion: Head of Growth or CMO.

The asymmetric qualification thresholds mean the agent must infer product-line fit from spend signals in the transcript rather than taking it as a given input. A prospect spending $50k/month on ads qualifies for Core but not Measurement; one spending $500k/month could be a fit for both. That classification drives which case studies are retrieved and how the email is framed.

**Fixtures included:**

| File | Prospect | Expected fit |
|---|---|---|
| `transcript-01-bellwether-coffee.md` | Bellwether Coffee | Core only |
| `transcript-02-cirra-insurance.md` | Cirra Insurance | Measurement only |
| `transcript-03-lyridon.md` | Lyridon | Core + Measurement |

---

## Running locally

**Prerequisites:** Python 3.10+, [uv](https://docs.astral.sh/uv/), an Anthropic API key.

```bash
git clone https://github.com/willgterry-lab/Sales-Engineering-Agent.git
cd Sales-Engineering-Agent

# Create .env
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# Install dependencies
uv sync

# Run the Streamlit app
uv run streamlit run app.py
```

The app will be available at `http://localhost:8501`. Drop any of the fixture transcripts from `fixtures/` into the uploader to test the full loop.

---

## Key concepts demonstrated

**Tool use and agent loops.** The agent loop is a `while` loop that calls Claude, reads the `stop_reason`, dispatches tool calls, appends results to the message history, and loops until Claude returns `end_turn`. No framework. Each iteration is visible in the code.

**Structured outputs via forced tool use.** Forced tool use means Claude is required to call a specific named tool and cannot produce a plain text response. Combined with a Pydantic schema compiled to JSON Schema, this gives type-safe, validated output from an LLM call.

**RAG retrieval.** Tool 2 does not call Claude. It scores the case study fixtures against the discovery object using keyword overlap and a hard product-line filter derived from tool 1's output. This separation (Claude for extraction and drafting; deterministic code for retrieval) keeps the retrieval step fast, cheap, and auditable. The interface is designed to swap in LanceDB vector similarity without changing the tool contract.

**Prompt grounding.** Tool 3 (email drafting) receives the full discovery object and the retrieved case studies as structured context. The system prompt instructs Claude to cite only figures that appear in those inputs. This is the same grounding pattern used in enterprise RAG deployments to prevent hallucination.

---

## Roadmap

- [ ] Swap keyword retrieval for LanceDB vector similarity
- [ ] Eval harness: eight golden transcripts, structured checks + Claude-as-judge
- [ ] `draft_pov_scope` tool (v2)
- [ ] `generate_demo_fixtures` tool (v2)
- [ ] Trace logging and run-diff observability (v2)

---

## Author

Built by **Will Terry** as part of a portfolio for Field/Sales Engineering and Solutions Consultant roles at AI-native companies.
