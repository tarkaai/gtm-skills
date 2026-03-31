---
name: outbound-gift-campaigns-smoke
description: >
  Outbound Gift Campaigns — Smoke Test. Send 20 personalized gifts (books, eGift cards,
  or curated items) to high-value solution-aware prospects to test whether physical/digital
  gifting breaks through digital noise and generates meetings.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Smoke Test"
time: "6 hours over 2 weeks"
outcome: "≥ 4 responses (email reply, meeting booked, or LinkedIn reply) from 20 gift recipients within 30 days of delivery"
kpis: ["Response rate", "Meetings booked", "Response quality"]
slug: "outbound-gift-campaigns"
install: "npx gtm-skills add OutboundFounderLed/Marketing/SolutionAware/outbound-gift-campaigns"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---

# Outbound Gift Campaigns — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Direct

## Outcomes

Prove that sending personalized gifts to solution-aware prospects generates ANY signal — an email reply, a meeting booking, or a LinkedIn response. This is a one-shot manual test with 20 recipients. The goal is to validate that gifting as a channel produces higher response rates than cold email alone for your ICP before investing in platforms or automation.

## Leading Indicators

- Gifts successfully delivered (platform tracking shows delivered status)
- At least 1 response within 7 days of delivery
- Responses reference the gift specifically ("thanks for the book", "appreciated the coffee")
- Quality of responses: warm and personal vs. polite but dismissive

## Instructions

### 1. Define your ICP for gift outreach

Run the `icp-definition` drill. Gift campaigns work best for:
- **High-value accounts** where the cost of a $25-75 gift is trivial relative to the deal size (ACV ≥ $10k)
- **Decision makers** at Director+ level who are hard to reach via cold email (inbox saturated)
- **Solution-aware prospects** who already know your category exists — they have the problem and are evaluating options, so a thoughtful gift creates positive brand association at the right moment
- **Companies with physical offices** if sending physical gifts (not required for eGift cards)

For this Smoke test, focus on prospects where you have a clear signal: recent job change into a buyer role, recent funding round, or active evaluation of competitors.

### 2. Build a prospect list of 20 recipients

Run the `build-prospect-list` drill targeting exactly 20 contacts. Quality over quantity at Smoke — pick prospects where you genuinely believe the deal could close. For each contact, enrich with:
- Full name, title, company, email (required)
- Signal type and detail (what triggered this prospect)
- LinkedIn profile URL (for personalization research)
- Physical mailing address (only if sending physical gifts; skip for eGift-only test)

Export to Attio with tag `gift_campaign_smoke_1`.

### 3. Select gifts using AI

For each of the 20 contacts, run the the gift campaign send workflow (see instructions below) drill's AI gift selection step. At Smoke level, you have two viable approaches:

**Approach A — eGift cards via Tremendous (lowest cost, fastest):**
Send $25-50 digital gift cards (coffee, Amazon, or "recipient's choice"). No physical address needed. Delivery is instant. Total cost: $500-$1,000 for 20 gifts. Use `tremendous-send-reward` fundamental.

**Approach B — Books via Sendoso or manual (more personal):**
Select a relevant business book for each prospect based on their role and signal. Books cost $15-30 each. Total cost: $300-$600 + shipping. More memorable than a gift card but requires a mailing address.

**Approach C — Mix (recommended for Smoke):**
Send eGift cards to 10 contacts (fast, no address needed) and books to 10 contacts (where you have addresses). This lets you compare response rates across gift types in a single test.

For each contact, the AI generates a personalized note. Review every note before sending — at Smoke scale (20 contacts), this takes 15 minutes and catches any AI hallucinations about the prospect.

**Human action required:** Review all 20 AI-generated gift selections and personalized notes. Approve, edit, or override each one. The AI provides a starting point; the founder adds the authentic touch.

### 4. Send the gifts

Execute the the gift campaign send workflow (see instructions below) drill:

1. For eGift cards: Call `tremendous-send-reward` for each recipient. Include the personalized note. Track the Tremendous reward ID.
2. For physical gifts: Call `sendoso-send-gift` (or purchase books directly and ship via Amazon/bookshop with a handwritten note). Track the send ID.
3. Log each send in Attio: gift type, value, send date, platform, personalized note.

**Cost estimate for 20 gifts:**
- eGift cards: 20 x $25-50 = $500-$1,000 (no platform fee on Tremendous)
- Books: 20 x $15-30 + shipping = $400-$800
- Mixed: ~$500-$700

### 5. Send a follow-up email 3-5 days after delivery

For each gift recipient, send a short personal email from the founder's address 3-5 days after confirmed delivery (or 3-5 days after send for eGifts):

```
Subject: Quick follow-up on the gift

Hey {{first_name}},

I sent you {{gift_description}} earlier this week — {{one_sentence_why}}.

I've been following {{company}}'s work on {{specific_thing}}, and I think
{{your_product}} could help with {{their_challenge}}.

Would you be open to a 15-minute call this week?

{{your_name}}
```

This is not a cold email sequence. It is a single, personal follow-up that references the gift. Send it manually from your inbox (not via Instantly) to maximize deliverability and warmth.

**Human action required:** Send each follow-up email personally. At 20 contacts, this takes ~30 minutes.

### 6. Monitor responses for 30 days

Track responses across all channels:
- Email replies to the follow-up
- LinkedIn messages or connection acceptances
- Meeting bookings via Cal.com or direct scheduling
- Any inbound that references the gift

Log every response in Attio: response type, date, what they said, and the quality of the response (warm interest, polite acknowledgment, meeting booked, no response).

### 7. Evaluate against threshold

Run the `threshold-engine` drill. Pass threshold: ≥ 4 responses (20% response rate) from 20 gift recipients within 30 days of delivery.

If PASS: Gifting works for your ICP. The response rate likely exceeds cold email by 3-5x. Proceed to Baseline to automate and scale.

If FAIL (1-3 responses): Diagnose:
- Were gifts delivered? Check platform tracking.
- Did recipients open/redeem eGifts? Check Tremendous redemption data.
- Was the follow-up email delivered? Check inbox for bounces.
- Was the gift relevant? Review AI selections — did they match the prospect's situation?
- Was the note generic? Re-read the personalized notes. "Thought you might enjoy this" is not personalization.

If FAIL (0 responses): The channel may not work for your ICP, or the execution was flawed. Try one more iteration with different gift types and deeper personalization before abandoning.

Record qualitative notes: Which gifts got the best reactions? Did anyone mention the gift was surprising or memorable? Did eGifts or physical gifts perform better? This qualitative signal informs Baseline design.

## Time Estimate

- 1 hour: ICP definition and prospect list building
- 1 hour: AI gift selection + human review of 20 selections and notes
- 1 hour: Sending gifts via platform + logging in CRM
- 30 minutes: Writing and sending 20 follow-up emails (3-5 days after delivery)
- 2.5 hours: Response monitoring and evaluation (spread over 4 weeks)
- Total: ~6 hours of active work over a 2-week initial window + 2 more weeks of monitoring

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Tremendous | Send eGift cards (no platform fee) | Free — you pay only the gift card face value. https://www.tremendous.com/pricing |
| Sendoso | Send physical gifts, books, swag | From ~$20,000/yr platform + per-send. https://www.sendoso.com/compare-plans |
| Clay | Enrich prospects with addresses and signals | From $149/mo. https://www.clay.com/pricing |
| Attio | CRM — store contacts, log sends and responses | Free for small teams. https://attio.com/pricing |
| Anthropic API | AI gift selection and note generation | ~$0.10 for 20 selections. https://www.anthropic.com/pricing |

**Estimated total cost for Smoke:** $500-$1,000 (gift value only if using Tremendous; higher if using Sendoso platform)

**Lowest-cost path:** Use Tremendous for $25 eGift cards. Total: $500 + ~$0 platform fees.

## Drills Referenced

- `icp-definition` — Define the ideal customer profile for gift campaign targeting
- `build-prospect-list` — Source and enrich 20 high-value prospects with signal data
- the gift campaign send workflow (see instructions below) — Select gifts via AI, send via platform, and log in CRM
- `threshold-engine` — Evaluate results against the 20% response rate pass threshold
