# Attributary — Company One-Pager

**Type:** Fixture (reference document for Sales Engineering Agent)
**Version:** v0.1
**Date:** 22 April 2026
**Status:** Fictional. Attributary does not exist. Category inspired by Will's domain experience; all specifics invented.

Everything in this document is either (a) fictional or (b) public category knowledge about marketing data and measurement platforms. No Funnel-specific internal information.

---

## Identity

**Attributary.** A marketing data platform for mid-market and enterprise marketing teams. Two product lines sharing a single data foundation.

**Positioning one-liner.** "One source of truth for every dollar of marketing spend, from raw data ingestion, through AI-powered anomaly detection, to model-based measurement of what actually worked."

**Category.** Marketing data infrastructure plus marketing measurement.

---

## Products

### Core

Data pipeline and warehouse load for marketing data.

**What it does.** Connectors across paid and organic marketing sources (Meta, Google Ads, TikTok, LinkedIn, Amazon Ads, Pinterest, Reddit, TradeDesk, Klaviyo, Braze, Shopify, Stripe, etc.). Normalises platform-specific schemas into a consistent marketing data model. Transforms and pipes out to BI tools, data warehouses (Snowflake, BigQuery, Redshift, Databricks) and data lakes.

**Embedded AI reasoning layer.** Real-time anomaly detection over ingested metrics. Flags when spend, CPC, CTR, CPA or conversion volumes fall outside typical ranges for the account, channel or historical window. Surfaces plain-English explanations and suggested investigation paths, pushed to the Marketing Ops / Analytics Engineering team via in-app notifications and Slack integration. This is the primary differentiator vs. pure-pipe competitors (Fivetran, Supermetrics, Improvado). Core is not just a pipeline; it reasons about the data it moves.

**Buyer map.**

- Champion: Head of Marketing Ops or Head of Analytics Engineering.
- Technical buyer: Head of Data / Analytics Engineering.
- Economic buyer: CMO or CTO, depending on organisation structure.

### Measurement

Model-based measurement of marketing effectiveness.

**What it does.**

- **Marketing Mix Modelling (MMM):** statistical modelling of spend allocation across channels to inform budget decisions.
- **Multi-touch attribution:** journey-level credit allocation across customer touchpoints.
- **Incrementality testing:** causal, experimental measurement of true lift from individual channels and campaigns.

Designed to replace or audit platform-native attribution (Google / Meta reporting) with independently-modelled truth.

**Fed by.** Core data where the customer runs both products. Otherwise a separate ingestion stack the Measurement team builds during onboarding.

**Buyer map.**

- Champion: Head of Growth or CMO.
- Technical buyer: Head of Growth Analytics or Head of Data.
- Economic buyer: CFO on larger deals.

---

## Ideal Customer Profile

Mid-market to enterprise companies running meaningful paid media. Not vertical-locked. Strongest fit in:

- Direct-to-consumer (DTC) brands.
- B2C subscription businesses.
- Retail and marketplaces.
- B2B SaaS companies with strong paid-growth motions.

**Differentiated qualification thresholds by product:**

- **Core.** Minimum roughly **$10,000 per month** in digital ad spend. Companies below this typically haven't outgrown native platform reporting.
- **Measurement.** Minimum **$200,000 per month** in digital ad spend. Below this, model-based measurement is overkill. The cost-to-value ratio doesn't justify it, and the data volume isn't sufficient for MMM to produce stable models.

**What this means for the agent.** A prospect spending $50k/month is a Core prospect. Pitching Measurement to that company loses commercial credibility. One of the agent's core tasks during discovery extraction is reasoning about which product line (or both) a prospect qualifies for, based on spend signals in the transcript.

---

## Pricing

### Core — priced in Flexpoints (consumption-based)

Flexpoints are Attributary's consumption unit. Customers pre-commit to an annual Flexpoint allowance and draw against it based on their data footprint.

- **Connector:** 50 Flexpoints per connector (one connected platform = one connector).
- **Data source:** 5 Flexpoints per source. A "source" is defined as one account times one report type.

**Worked example.** A brand runs Facebook Ads across 30 accounts and needs two report types from each. That's:

- 1 connector (Facebook) = 50 Flexpoints.
- 60 data sources (30 accounts × 2 report types) × 5 Flexpoints each = 300 Flexpoints.
- **Total: 350 Flexpoints for Facebook alone.**

A typical mid-market customer runs 6 to 10 connectors and accumulates several hundred data sources across them.

**Typical deal economics.**

- Average deal: **$1,000 to $2,000 MRR** ($12,000 to $24,000 ARR).
- High end: **$1,000,000+ per year** for large enterprise customers running many connectors across thousands of data sources.

### Measurement — priced by ad spend and number of models

- **Minimum deal size:** $6,000/month ($72,000/year).
- **Upper end:** $1,000,000+/year for large enterprises running many models across markets and product lines.
- Banded on two dimensions: customer digital ad spend and the number of models being maintained.

### Bundles

Multi-product deals are common. Bundling Measurement with a qualifying Core deployment typically unlocks improved entry economics for Measurement versus a standalone deal.

---

## Common objections

These drive the `draft_followup_email` tool's content. Each objection has a canonical positioning response the agent should draw from.

### Core

1. **"We already use Fivetran / Supermetrics."**
   Response: Those tools are pipes. They move data but don't reason about it. Core is a platform: normalised marketing-schema transformations, and an embedded AI reasoning layer that surfaces anomalies in real time. No pure-pipe competitor offers this.

2. **"Our engineering team can build connectors in-house."**
   Response: True, and most teams that try end up owning a brittle pipeline for their first four platforms and abandoning the fifth. Platform APIs break constantly. Meta alone ships breaking changes monthly. Core exists because the build-vs-buy math stops making sense around the third platform.

3. **"BigQuery has native integrations, why add another layer?"**
   Response: BigQuery native integrations give you raw API data: inconsistent schemas, no cross-platform normalisation, no anomaly intelligence. The work between raw platform JSON and usable analytics is where Core earns its price.

### Measurement

1. **"Platform-native attribution (Google / Meta reporting) is good enough."**
   Response: Platform reporting structurally over-credits platform-owned inventory. Meta's attribution tells you Meta worked; Google's tells you Google worked. Independent modelling is the only way to audit true incrementality across the full mix.

2. **"We tried MMM and it was too slow and expensive."**
   Response: Attributary's MMM refreshes on a short cadence (weekly or better), with lower setup effort and an API-first integration path. Not a six-week consulting engagement: an always-on model served back into the channels the marketing team already uses.

3. **"Our CFO doesn't trust attribution models."**
   Response: CFO trust comes from incrementality testing: experimental, causal evidence, not modelled probability. Attributary's incrementality module is designed to produce exactly the finance-grade reports the CFO wants, with defensible methodology.

---

## Competitive context

- **Core competitors:** Fivetran, Supermetrics, Improvado, Adverity, native platform APIs, in-house ETL.
- **Measurement competitors:** Nielsen, Analytic Partners, Meta / Google native attribution, in-house models built on the customer's own warehouse.

**Strategic differentiator.** Attributary is the only vendor that offers a single data foundation feeding both pipeline and measurement. Customers running both products get clean, normalised Core data flowing directly into Measurement models without needing a separate ingestion stack. The AI reasoning layer in Core also feeds confidence signals into Measurement, e.g. "this spike in spend was flagged as anomalous upstream, so MMM attribution for this week should be treated with caution."

---

## Why this matters for the agent

The fixture above is deliberately structured so that individual sections are self-contained for retrieval. When we build `retrieve_case_studies` and `draft_followup_email`, the agent will pull specific chunks: "Core objections," "Measurement buyer map," "Worked example Flexpoints", without needing the rest of the doc. That's intentional.

The per-product qualification thresholds, buyer maps, and objection sets also give the agent real classification work to do during discovery extraction: it must identify which product line (or both) a transcript points to, based on spend signals, role signals, and pain signals. That classification is the single most FDE-flavoured capability in the v1 scope.
