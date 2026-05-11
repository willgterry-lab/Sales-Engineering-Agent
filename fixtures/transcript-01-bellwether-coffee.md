# Discovery Call Transcript — Bellwether Coffee

**Date:** 14 April 2026
**Duration:** 32 minutes
**Attributary side:** Marcus Hale (AE)
**Bellwether side:** Isabelle Harrington (Head of Marketing)
**Scenario tag:** core-fit

---

**Marcus Hale (Attributary):** Isabelle, thanks for making time. Can you hear me okay?

**Isabelle Harrington (Bellwether):** Yeah, crystal clear. Thanks for setting this up. I've got a hard stop at the top of the hour — got a creative review with the agency — so probably 30 minutes if that's alright?

**Marcus:** 30 is perfect. Before we get into it, how did you land on Attributary? I saw you came in through the demo request form, but always curious about the trigger.

**Isabelle:** Honestly? Two of the other DTC people in my Slack group have told me to look at you. One of them — she runs marketing at a skincare brand, I won't name names — said you'd saved her three days a week. That's the bit that got me on the form.

**Marcus:** Nice. Word of mouth is the best kind. So let me make sure I understand the shape of Bellwether before I ask anything useful. You're a DTC coffee subscription, five-ish years old, London HQ — is that roughly right?

**Isabelle:** Yeah. Started in 2021, we're coming up on five years. Subscription is the core of the business — we've got about 40,000 active subscribers across the UK and we launched into the US last year. We do some retail — we're in Waitrose and a handful of independents — but that's maybe 15% of revenue. The rest is D2C.

**Marcus:** And team size on the marketing side?

**Isabelle:** Marketing is me, two performance marketers, a content person, a retention lead, and we've got the founder very involved still. James — he's the CEO — he basically runs brand and creative himself, which is brilliant most of the time and occasionally stressful. We share an agency for paid but most of the execution is in-house.

**Marcus:** Got it. And the friend who put you onto us — she mentioned reporting time. Is that the thing that's actually pinching for you, or is there something underneath that?

**Isabelle:** It's the thing that's pinching. We do a weekly marketing review every Tuesday — James, me, the two performance marketers, retention lead, content lead — and to prepare for that, my team is spending most of Monday morning pulling exports out of Meta, TikTok, Google Ads, GA4, Klaviyo, Amazon, Shopify, and stitching them into a Google Sheet. Then someone charts it, then we argue about whether the numbers are right for 20 minutes at the start of the review before we can get to anything useful.

**Marcus:** How many hours on the Monday, roughly?

**Isabelle:** Between the two performance marketers and me — maybe 10 hours of human time goes into that sheet every Monday. And it's always stale by the time we look at it, because Tuesday 10am it's showing Friday's data at best.

**Marcus:** And the "arguing about whether the numbers are right" — what's actually going on there?

**Isabelle:** A few things. One is TikTok — iOS attribution is a mess, and the numbers TikTok reports in its own dashboard don't match what we see in Shopify for conversions attributed to TikTok campaigns, and then GA4 tells us something different again. So for any given week we've got three numbers for the same channel and we spend half the review arguing about which one to trust. The other is just data freshness. If Meta hasn't finished reporting its Sunday numbers at the time we pull the sheet, you get a weird dip that isn't real, and then we spend the review trying to explain why a channel suddenly looks bad when actually it's just… not finished.

**Marcus:** That's really clear. If I'm hearing you right, the pain isn't "we don't have data" — it's "the data we do have is slow, manual to assemble, and we can't fully trust it." Is that a fair summary?

**Isabelle:** That's exactly it. We've got the data, it's the assembly and trust that's the problem. And my two performance marketers should be running tests and optimising, not being glorified data janitors every Monday.

**Marcus:** What does "trust" look like for you? If you had numbers you could trust, what would that unlock?

**Isabelle:** A few things. One — and this is the one James cares most about — we want to know what our actual blended CAC is, by cohort, week over week. Right now we've got three different CAC numbers depending on who you ask, because Meta, Google and Shopify all tell different stories. Second, we want to be able to A/B test landing pages and creative and measure it properly. At the moment we run tests and then the data's so noisy we can't tell if a winner is real or not. Third — we want to layer in some of our retail data from the Waitrose numbers we get monthly, because at some point we need to see online and retail in one view. That's not urgent though.

**Marcus:** Okay, that's useful. Let me ask about the stack — do you have a warehouse on the Bellwether side?

**Isabelle:** We have BigQuery. We've had it for about 18 months. Our BI analyst — we have one, part-time, his name's Farooq — he set it up and we've got some of our Shopify data flowing in, and some of our Klaviyo data, but it's patchy. Honestly it's there and it works, but most of my team is pulling from source dashboards directly because the warehouse is missing stuff or it's half a day behind. So the warehouse exists but it's not load-bearing for us yet.

**Marcus:** Got it — that's actually a really common pattern, and it's exactly the thing Core is built to fix. The way we'd think about it: every connector you've got live, the data lands in your BigQuery on a daily refresh, normalised, ready to query. TikTok, Meta, Google, Klaviyo, Shopify — all of those are first-class connectors, we handle the API weirdness, and your analyst can actually start building dashboards off a warehouse that's reliable.

**Isabelle:** That's the dream.

**Marcus:** And the anomaly piece — this is the bit that's been getting the most feedback lately — Core has a reasoning layer that watches incoming metrics and flags things that look weird. So say a TikTok ad set suddenly starts spending at 2x its usual CPM — you'd get a flag before Tuesday's review, not during it.

**Isabelle:** That is useful. We had an incident in February where a Meta campaign's frequency capping broke and we overspent by about £18,000 over a weekend before anyone noticed on Monday. That kind of thing would have been caught.

**Marcus:** Exactly that kind of thing. Can I ask what you're spending on paid these days, roughly? It helps me calibrate what the right shape of Attributary looks like for you.

**Isabelle:** We're running about £55k a month on paid in total, across Meta, TikTok, Google, and a smaller piece on Amazon and Pinterest. We'll probably push towards £75k by Q4 as we scale into the US, but that's the current run rate.

**Marcus:** Perfect — that's helpful. One thing I want to be upfront about: Attributary has two product lines. Core — which is the data platform, the connectors, the warehouse loads, the anomaly layer — that's what we've been talking about, and that's absolutely the right fit for you today. We also have a Measurement product that does marketing mix modelling and incrementality testing, but honestly at £55–75k a month, it wouldn't pay back. That's a product that starts to make sense when you're north of £200k a month, so I wouldn't want to sell you something you'd regret in six months.

**Isabelle:** That's really helpful actually. I had seen Measurement on your website and wasn't sure.

**Marcus:** Totally fair. It's a future-state conversation, not a today one. Let me ask about the decision process side — if this conversation goes well, what does the path looks like on your end? Who's involved, how do you usually make a decision like this?

**Isabelle:** So I'd own the decision on the marketing side. James will want to see a demo and probably come in for the numbers conversation — anything above about £20k in annual contract I'd loop him in. We don't have a heavy procurement process, we're small enough that we just do what makes sense. I'd probably want to do some kind of trial or pilot — honestly if I could see the reports running against our actual data for a month before committing, that would be the thing that would make me confident.

**Marcus:** We can absolutely do a structured pilot. Typically that's a 30-day thing where we stand up three or four of your most important connectors, pipe them into your BigQuery, and give you a trial of the anomaly layer on live data. Cost recovery on that pilot if you go ahead afterwards.

**Isabelle:** That's exactly what I'd want.

**Marcus:** Timing — is there any pressure, any event, anything that's making this a now-conversation versus a later-conversation?

**Isabelle:** Two things. One is our Q3 planning — I need to go into the August planning cycle with a plan for how we stop losing Monday mornings to the sheet. If I can't solve that before August, I'll have to hire another analyst, and I'd rather spend that money on tooling. Two is the US scale-up — as we add volume in the US, the manual assembly breaks completely, because now it's Meta US and Meta UK, and the sheet becomes un-manageable. So I've got a window.

**Marcus:** Good to know. So we're looking at something where you'd want to be signed and onboarding in June, realistically, to be operational before the Q3 spend ramp?

**Isabelle:** Yeah, June feels right. May would be better.

**Marcus:** Understood. Last question — and it's an honest one — who else are you looking at? Just so I know how to be useful in the next conversation.

**Isabelle:** We've had a demo with Supermetrics — it's fine, feels more like a reporting tool than a data platform, and doesn't do anything smart with the data. We've also looked at Fivetran as a pure pipeline option, but then Farooq has to build everything on top of it, and I don't have the analyst bandwidth. So you're third in the formal process but first in my head, based on what I've heard from the people I trust.

**Marcus:** That's very fair feedback. Here's what I'd suggest as a next step — let me get our Solutions Engineer on a follow-up with you and Farooq next week, we do a proper working session with your actual data sources, and we sketch out what a pilot would look like. I'll send you three reference customers in the DTC subscription space who'll take a call if you want to pressure-test the experience before you commit. Does that work?

**Isabelle:** That works. Can you also send the Measurement-versus-Core thing in writing? I want to share it with James so he doesn't come into the next meeting confused about which product we're actually buying.

**Marcus:** Will do. I'll send a follow-up today with a one-pager on Core, the product-line explainer, the three reference customers, and a proposed agenda for next week's working session. Thanks Isabelle — good conversation.

**Isabelle:** Thanks Marcus, speak soon.

---

*End of transcript. Duration: 32:14.*
