# Sales Engineering Agent — Concepts Glossary

A living reference. Every time we hit a new concept during the build, it lands here with:

- **What it is**: plain English.
- **Why it matters for this project**: the specific role it plays.
- **Interview version**: one or two sentences you can say out loud.

---

## Grounding (and hallucination)

**What it is.** LLMs generate text one token at a time based on patterns from training data. When they lack real information, they fill gaps with plausible-sounding invention. That's *hallucination*. *Grounding* is the practice of giving the model reliable reference material (documents, records, retrieved passages) and instructing it to answer from that material rather than its own recall. Grounding doesn't eliminate hallucination, but it constrains and localises it.

**Why it matters here.** Our agent needs to cite real case studies in its follow-up emails. If we let Claude invent case studies from general knowledge, every email is a liability. The customer names, numbers, and outcomes would all be made up. By building a fixture knowledge base and forcing the agent to retrieve from it, we make the output verifiable.

**Interview version.** "Grounding is how you stop the model making things up. You give it retrieved reference material at runtime and instruct it to answer from that, so the output is traceable back to a source the user can check."

---

## Fixture data

**What it is.** Invented-but-realistic data used to simulate a real customer environment during development and testing. In our project: a fake company, fake case studies, fake discovery transcripts.

**Why it matters here.** We can't build retrieval or evals without something to retrieve and something to evaluate against. Fixtures also let us demo safely: no real customer data, no NDA risk, and we control every variable. For an FDE role specifically, fixture design is the same muscle as scoping a real customer engagement. You're building a mental model of a product, an ICP, and the use cases before you touch code.

**Interview version.** "Before writing any agent code I built the world it operates in: Attributary, a fictional multi-product marketing data platform with per-product ICPs, pricing, case studies and sample discovery calls. That fixture is both the grounding material for retrieval and the ground truth for evals."

---

## Agent loop (and tool use)

**What it is.** An LLM by itself can only read text and write text. It can't fetch a webpage, query a database, or look up a case study. A *tool* is a function in your code that does one specific thing, plus a JSON *schema* describing what it does and what arguments it takes. The *agent loop* is the protocol by which the model uses tools:

1. You send the model a prompt plus a list of available tool schemas.
2. The model decides: answer directly, or request a tool call (returning the tool name and arguments).
3. Your code runs the function and sends the result back as a follow-up message.
4. The model reads the result. It either calls another tool or returns a final answer.
5. Loop until done.

This is the architecture pattern people are pointing at when they say "agentic." The model is not doing anything magical. It chooses which functions to call and in what order. Your code does the actual work.

**Why it matters here.** This is the spine of v1. Three tools (`extract_structured_discovery`, `retrieve_case_studies`, `draft_followup_email`) hang off this loop. Once the loop is working with a trivial tool, swapping in real tools is mechanical: schemas, dispatch entries, Python functions. The demo script `scripts/agent_loop_demo.py` proves the loop works end to end with a one-line tool (`get_current_date`) before any domain logic is wired in.

**Interview version.** "An agent is an LLM that can call functions in your code via a structured loop. The model decides what to do, your code does it, the result comes back, repeat until done. We prove the loop works with a trivial tool first, then swap in the real ones."

---

## Structured outputs (and forced tool use)

**What it is.** Free-form text from an LLM is fine for chat but useless when downstream code needs to operate on the result. *Structured outputs* is the practice of forcing the model to return data that matches a defined schema. With Anthropic's API, in order of reliability:

1. **Forced tool use.** Define a tool whose only job is to "record" the structured object. Set `tool_choice` to that specific tool. The model has no choice but to call it with matching arguments. This is the most reliable pattern.
2. **JSON mode / response format.** Newer feature, simpler API. Tells the model to return JSON.
3. **Free-form text plus parsing.** Prompt the model to write JSON in its response and parse it. Brittle.

The pattern we use: Pydantic model, auto-generate JSON Schema, hand to Claude as a tool, Claude produces matching JSON, Pydantic validates on the way back in. The result is a real typed Python object with validation, not a dict you have to hope is shaped right.

A subtle point worth understanding: in this pattern the tool isn't doing anything real. It doesn't query a database or fetch a webpage. The tool exists purely as a *typed return channel* for the model. This trick is everywhere in production LLM code.

**Why it matters here.** `extract_structured_discovery` produces a `MEDDPICCDiscovery` object that downstream tools (retrieval, follow-up email) depend on. Without a guaranteed schema, every downstream tool would need defensive parsing. Structured outputs are the contract that makes the three-tool pipeline composable.

**Interview version.** "I get structured output by using forced tool use. I define a Pydantic model, hand its JSON Schema to Claude as a tool, set tool_choice to force the model to call it, and validate the result through Pydantic. I get a typed Python object back, not a dict I have to hope is shaped right."

---
