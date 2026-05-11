# Discovery Call Transcript — Cirra Insurance

**Date:** 16 April 2026
**Duration:** 34 minutes
**Attributary side:** Marcus Hale (AE)
**Cirra side:** Adaeze Okwu (Director of Growth Marketing)
**Scenario tag:** measurement-fit

---

**Marcus Hale (Attributary):** Adaeze, hi. Can you hear me okay?

**Adaeze Okwu (Cirra):** Yeah, all good. I've got 30 minutes, maybe a bit more if we need it. My CMO Rachel might dial in for the last ten, she's keen to be in the loop but has a board prep this morning.

**Marcus:** Brilliant. Before we get into it, you filled in the form and mentioned you'd been looking at MMM options. Is that still the specific need, or has that shifted?

**Adaeze:** It's sharpened, actually. Since I filled in that form two weeks ago, we've had our Q1 board review, and the board has basically told us we have one quarter to prove that our brand investment, which is predominantly linear TV, connected TV, and some influencer, is driving incremental policies. If we can't, they want us to cut that budget by 40% in Q3. So this has moved from a "nice to solve" to a "must solve by end of June" problem.

**Marcus:** Okay, that's very concrete. Thank you. Let me make sure I've got the shape of Cirra right before I ask useful questions. You're a UK-based challenger home insurance business, launched in 2023, direct-to-consumer?

**Adaeze:** That's right. We started with home insurance, we added contents in 2024, and we're about to launch a landlord product in September. We're entirely direct, no broker channel, which is a big part of why this measurement question matters. Every pound of marketing is doing the work of a broker relationship, so we have to be confident the marketing is working.

**Marcus:** Understood. Can you walk me through the paid spend picture, what are you running, roughly, and what's the mix?

**Adaeze:** We're at about £1.5 million a month total marketing spend. Rough breakdown: £600k on linear TV, £200k on connected TV, about £400k across Google Search and PMax, £150k on Meta and TikTok for direct response, £100k on influencer, and the rest on out-of-home and a bit of podcast. We ramped TV in autumn last year and it's the thing nobody can confidently measure.

**Marcus:** And on the digital side, what does your current attribution setup actually tell you?

**Adaeze:** We've got GA4, we pull the raw exports into our Snowflake warehouse. We have a data team, they've built a dbt model that joins GA4 session data with our quote-engine data and our policy-bind data, so we can see the full funnel from anonymous session to paid policy. And that attribution says Google Search is doing basically everything: 65% of policies, last-touch. The problem is we know that can't be right, because when we went dark on Google Search for a weekend as a test in December, policies only dropped 20%. So we're clearly over-crediting search.

**Marcus:** That's a very good intuition test. What's the data team's read on that?

**Adaeze:** They know it's wrong. They've been honest that last-touch GA4-based attribution can't capture upper-funnel work. They actually tried to build an MMM themselves last year, spent about four months on it, and produced something that nobody trusts. The output said TV's incremental ROI was 0.3, which would mean we're setting money on fire, and the CMO looked at it and said "that's impossible because we can see the correlation in quote volume when we have TV on air." So it's been parked. Our data lead, Raj, has been candid that building MMM in-house isn't what his team should be spending time on.

**Marcus:** Right. So the Core side of the house, the data pipeline, the GA4 to Snowflake, the quote and policy data joined in, that's working for you?

**Adaeze:** Yes. I mean, not perfectly: every time Google changes their API or GA4 changes something about how event data looks, the dbt models break and Raj's team loses a week. But the architecture is solid. The warehouse is the source of truth. We don't need more data pipes, we need something on top that answers the question we actually have, which is: where is marketing spend actually driving incremental policies.

**Marcus:** That's very clear and it tells me exactly what shape of Attributary engagement makes sense. Let me be direct: Attributary has two product lines, Core, which is the data platform, the connectors, the warehouse loads, and Measurement, which is MMM plus incrementality testing. Everything you've just described is Measurement. You've got Core largely solved in-house. I wouldn't want to sell you the Core licence, it would be paying for plumbing you've already built. What I'd want to explore with you is Measurement on its own.

**Adaeze:** That's exactly the right read. Raj would be relieved, because he doesn't want someone else's ETL sitting between him and his dbt models. We just need the measurement layer.

**Marcus:** Okay good. So on Measurement specifically, can you tell me what "good" looks like from where you sit? What would the output need to show you, and for whom?

**Adaeze:** The output needs to answer two questions, really. One: for every channel we're running, what is the true incremental contribution to policies bound, not last-touch credit. Two: if I take £100k out of channel X and put it into channel Y, what does the model predict happens to total policies? That's the number the CMO needs to walk into the board with. The secondary thing I'd love, and this is the one I'd use day to day, is being able to design and run incrementality tests on TV and influencer, so we can validate what the MMM is telling us rather than just trusting it.

**Marcus:** Very clear. Both of those things are exactly what Measurement does. MMM refreshed monthly or quarterly, your call, calibrated against incrementality tests you run on the channels where the stakes are highest. Let me ask about stakeholders, who needs to buy into this internally?

**Adaeze:** I own the decision up to a point. Our CMO Rachel signs off on anything above about £50k annual contract value. Above £200k, which I assume we'll be in, it needs CFO sign-off. Our CFO, Danny, is sharp and is actually the person who told the board to put pressure on us to prove TV, so he's not hostile, he just needs to see the methodology. He'll have questions about how the model is specified and whether it's defensible.

**Marcus:** That's useful. Sounds like Danny will want to see the MMM methodology documentation, not just the output. We've got exactly that, we publish our methodology and we can run him through how the models are built.

**Adaeze:** That would be welcome. He's an ex-McKinsey CFO, he's going to probe.

**Marcus:** Understood, we've had that conversation before. What's the process look like beyond sign-off?

**Adaeze:** Procurement is light, but we have a real InfoSec review because we're regulated. The data team would need to walk through your SOC 2, your data-handling, where MMM calibration data sits. That's a couple of weeks. Assume six weeks from verbal yes to signed contract, realistically.

**Marcus:** Good. Competitive picture, who else is in the mix?

**Adaeze:** We've had a conversation with Nielsen. The methodology is trusted but the delivery cycle is quarterly and it's expensive and it's a PowerPoint, not a tool. We want something that refreshes monthly and that Raj can integrate into our warehouse so we can work with the outputs in Looker. We've also, briefly, considered going back to Raj's team and asking them to have another go, but that's a weak option and everyone knows it.

**Marcus:** That's a very common picture in your category. Typically where we win over Nielsen is the refresh cadence and the fact that the model outputs flow back into your warehouse, your team can actually operate on them rather than read them in a deck. And the incrementality testing layer is a material differentiator. Nielsen doesn't help you design in-market tests.

**Adaeze:** That's the thing Rachel most wants, honestly. She wants to design a test next quarter to prove out the connected TV investment. If Measurement comes with test-design support, that's a big unlock.

*Rachel Meyer (CMO, Cirra) joins the call.*

**Rachel Meyer (Cirra):** Sorry I'm late, board prep ran over. What have I missed?

**Adaeze:** I've walked Marcus through the Q3 board commitment and the measurement question. He's clear that we're a Measurement engagement, not a Core one, and he understands the stakeholder picture, you, Danny, InfoSec.

**Rachel:** Good. Marcus, my constraint is very simple: I have one quarter to give the board a defensible, incrementality-validated read on TV, connected TV, and influencer. I need a partner whose methodology I can defend to a CFO who will try to break it. And I need the tool to be something my team can keep running after the first engagement, not a consultancy deliverable that becomes stale the day it lands.

**Marcus:** Very clear. Three things I'd say. One, our methodology is publicly documented and we've taken it through Big Four diligence and similar CFO reviews, we can set Danny up with our head of modelling for an hour and he'll have all the answers he needs. Two, the default product shape is a fully live MMM in your warehouse that your team operates, refreshed on a monthly cadence, not a one-off report. Three, we'll run the first incrementality test on your highest-stakes channel alongside the MMM, sounds like that's connected TV, so you have a clean validation of the model against live data before the board deadline.

**Rachel:** That's the right shape. What does a realistic timeline look like?

**Marcus:** If we can move into a paid POV in May, we'd have the first MMM output and the connected TV incrementality read by late July, which gives you a week or two to land it before the end of Q3.

**Rachel:** That works. Adaeze, let's keep this moving. Marcus, what do you need from us next?

**Marcus:** Three things, a working session next week with Raj to walk through the data we'd need, an introduction to Danny for a 45-minute methodology session, and I'll send over three reference customers, one of whom is in regulated financial services with a similar brand-TV measurement question. Does that work?

**Rachel:** All of that. Thank you. Adaeze will own this from our side, send everything to her.

**Adaeze:** Thanks Marcus, I'll look out for your follow-up.

**Marcus:** Thank you both, speak very soon.

---

*End of transcript. Duration: 34:02.*
