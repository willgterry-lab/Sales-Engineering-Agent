# Discovery Call Transcript — Lyridon

**Date:** 20 April 2026
**Duration:** 36 minutes
**Attributary side:** Marcus Hale (AE)
**Lyridon side:** Owen Bradley (VP Marketing Operations), Priya Sharma (Director of Demand Generation)
**Scenario tag:** ambiguous-multi-product

---

**Marcus Hale (Attributary):** Owen, Priya, good to meet you both. Can you hear me alright?

**Owen Bradley (Lyridon):** Loud and clear, thanks Marcus.

**Priya Sharma (Lyridon):** Yep, same.

**Marcus:** Great. So I've got about 40 minutes blocked on my side, I know you've got 30, so we'll be disciplined. Before we start, for my own context, Owen, you run Marketing Operations, Priya you run Demand Gen. Am I right that you both report into the CMO's org but different verticals within it?

**Owen:** Close. I report to Jessica, our CMO, directly. Priya reports to our VP of Marketing Strategy, Ben Nakamura, who also reports to Jessica. So we're peers one level down, different functional remits.

**Marcus:** Got it. And can you give me the very short version of what Lyridon does and where you are as a business? I've done some research but I'd rather hear it from you.

**Priya:** Sure. Lyridon is compliance automation software, we sell into enterprise GRC teams, mostly in regulated industries: financial services, healthcare, large-cap tech. The product automates evidence collection, control monitoring, and audit workflow. We're Series C, closed in late 2024, about 300 employees, $60M ARR last year and we're targeting $85M this year. UK HQ, offices in New York and Austin, customer base split roughly 60/40 between the US and Europe.

**Marcus:** And the marketing shape, budget, team, channel mix?

**Owen:** Marketing is about 40 people under Jessica. Demand gen, which Priya runs, is the largest function. We spend about $4.8M a year on paid, roughly $400k a month averaged, though it's peaky around our virtual event calendar. The big channels are Google Search and PMax, LinkedIn Ads, that's our biggest single line item, 6Sense for ABM intent and orchestration, some Meta and programmatic for brand, a decent influencer line with GRC industry analysts, and we sponsor a couple of flagship industry events.

**Marcus:** Helpful. What prompted the conversation with us? What's the problem that sent you to the form?

**Owen:** I'll start and Priya will jump in. The triggering event, honestly, was our Q1 pipeline review six weeks ago. The review is Jessica, the CRO, Martin Vale, and their direct reports. And we spent the first hour of a 90-minute review arguing about the numbers before we got to any actual strategy. Because our GA4 says one thing about session-to-lead conversion, HubSpot, which is our MAP, reports a different MQL number, Salesforce reports a different SQL and opportunity number, and when you tie that back to what Google Ads and LinkedIn report as leads driven, nothing lines up. So every pipeline review becomes a forensic accounting exercise rather than a strategy conversation. That's the thing I'm trying to kill.

**Priya:** And on my side, there's a separate but related pressure that's actually sharper. In the Q1 board meeting, our CFO, Danny Fielding, raised the question of whether we're over-investing in LinkedIn brand. We've got about $80k a month going to LinkedIn and LinkedIn's own reporting says it's driving a huge pipeline impact, which of course it does because LinkedIn measures itself. We cannot produce a credible read on the incremental pipeline impact of LinkedIn brand versus LinkedIn direct response versus the rest of the mix. Danny has asked for that read by end of Q2. If we can't produce it, he's told Jessica he wants to cut LinkedIn brand by 40% as a default.

**Marcus:** Okay. Two quite distinct problems there. Owen, yours is about unifying the data across GA4, HubSpot, Salesforce, ad platforms, so pipeline reviews start from a shared version of truth. Priya, yours is about incrementality, proving what's actually driving pipeline versus what's just getting last-click credit. Is that the fair split?

**Owen:** That's exactly the split.

**Priya:** Yes.

**Marcus:** Let me probe the first one. Owen, what's in the data stack today and what's missing?

**Owen:** We have Snowflake. We have a data engineering team, four people under our Director of Data, Elena Rojas. They've built dbt models that pull from some sources, Salesforce, HubSpot, our product usage data, into curated tables. The gap is that the ad platform data and the GA4 data aren't reliably in there. Google Ads and LinkedIn in particular, every time Google or LinkedIn change their API, Elena's team has to burn two weeks re-doing the ingestion. So we have a half-built warehouse that works well for CRM and product data but breaks at the advertising boundary. Which is the exact boundary we most need it to work at, because the CLTV-by-channel question depends on joining paid spend data with closed-won revenue in Salesforce.

**Marcus:** That's the Core product in a sentence. We maintain the ad platform connectors, Google Ads, LinkedIn, Meta, 6Sense, GA4, we handle API drift, we land the data in your Snowflake normalised, your dbt layer stays in Elena's hands but stops breaking at the ad-platform boundary. Let me make sure I understand what you'd want it to join against. Salesforce opportunity stages, HubSpot MQL data, and what else?

**Owen:** Salesforce opportunities and closed-won ARR, that's the key one, because that's how we build CLTV. HubSpot for MQLs and SQLs. Product usage data from our internal app, Elena's team has that one solved. And GA4 for top-of-funnel session behaviour. If we could get paid spend joined to all four of those cleanly in Snowflake, that would transform every pipeline review.

**Marcus:** Perfect. That's exactly what Core delivers. And the output of that, CLTV-by-channel, cost-per-pipeline-dollar, cost-per-MQL, cost-per-SQL across segments, that becomes a dashboard you build in Looker or Tableau or whatever's downstream, not something we deliver. Is that right?

**Owen:** Yes. Looker is our BI layer. Once the data is in Snowflake clean, Elena's team is perfectly capable of building the dashboards. The gap has always been upstream of Looker.

**Marcus:** Understood. Now let me take Priya's problem, because this is a different product for us, and I want to be clear about that. Priya, what you're describing, proving incremental pipeline impact of LinkedIn brand specifically, and by extension any channel where last-click attribution is lying to you, that is our Measurement product, not our Core product. MMM plus in-market incrementality testing. That sits on top of the data foundation Owen's building, but it's a separate layer and a separate commercial conversation.

**Priya:** Okay, I was wondering about that. We do need both, don't we.

**Marcus:** Potentially. Let me ask a sharper question so I don't sell you something you don't need. If Owen's Core engagement delivers you a reliable, warehouse-native view of paid spend to pipeline to closed-won revenue by channel, if you have that in September, does that answer Danny's question about LinkedIn brand, or does it not?

**Priya:** It answers part of it. It tells me what LinkedIn brand is getting credit for, last-touch or multi-touch. It doesn't tell me what would happen if I turned LinkedIn brand off. Those are different questions.

**Marcus:** That's exactly right. And the "what would happen if I turned it off" question is Measurement, MMM and incrementality testing. So the honest read from where I sit is that Core is an obvious fit and I'd urge you to do it either way, and Measurement is a probable fit given the CFO pressure Priya just described, but Measurement is a CMO-and-CFO conversation more than a Marketing Ops conversation, and I don't want to assume I can sell Jessica on that on a first call she wasn't in.

**Owen:** That's the right framing. Jessica is the economic buyer above $150k ACV and she'd be the sponsor on Measurement. She's currently focused on the pipeline review problem I'm describing, so Core will resonate with her faster. Measurement would need a separate conversation with her and Danny.

**Marcus:** Very clear. So here's what I'd propose. We scope a Core engagement first. Priya, you stay close to that because the CLTV-by-channel output from Core feeds the Measurement business case later, but Owen leads the Core commercial conversation. In parallel, I'd ask for a separate 45-minute conversation with Jessica and Danny specifically on Measurement, framed around the Q2 board commitment on LinkedIn brand. Two parallel tracks, shared ownership on your side, we wire them together commercially if both close. Does that make sense?

**Priya:** That's the cleanest way to do it, yes.

**Owen:** Agreed. I can get you time with Jessica, probably not Danny on the first meeting, but definitely Jessica. And Jessica can bring Danny when she's ready.

**Marcus:** Perfect. Procurement, what does that look like when the time comes?

**Owen:** We have a proper procurement function, InfoSec review, we'd need SOC 2, DPA review, security questionnaire, data residency discussion. Assume eight weeks from verbal yes to signature on anything above $150k. We have an ISO 27001 requirement too for UK regulated customer data.

**Marcus:** We have all of that documented and ready. Competitive picture, are you talking to anyone else?

**Owen:** We've had a demo with Adverity, similar space but less depth on the B2B ad platforms we care about, particularly 6Sense. We've also seriously considered just putting more budget into Elena's team and building the ad-platform connectors ourselves. That's the internal alternative. It's not a great one, we lose Elena for six months, but it's on the table.

**Marcus:** Very fair. The connector-maintenance argument is usually where we win over build-in-house, because the cost isn't the first build, it's the 18 months of maintenance that follow. Happy to put that in writing in a short memo if it helps Elena's conversation internally.

**Owen:** That would help.

**Marcus:** Last question, what's a realistic timeline on Core?

**Owen:** I'd want to be in evaluation during May, in contract by end of June, onboarding in July, operational for the Q3 pipeline review which is early October. That's the internal clock.

**Marcus:** Workable. Here's what I'll send today, a Core scoping document with the connector list we'd need for your stack, a CLTV-by-channel output example from a similar customer, the build-versus-buy memo for Elena, three reference customers in B2B SaaS with similar Salesforce-plus-HubSpot-plus-paid joining questions, and a proposed agenda for the follow-up working session next week. Separately I'll propose a 45-minute slot for Jessica and, whoever she wants to bring, on Measurement, framed around the board commitment.

**Owen:** Perfect.

**Priya:** Thanks Marcus, much clearer than I expected to come out of this call, honestly.

**Marcus:** Thank you both, speak next week.

---

*End of transcript. Duration: 36:21.*
