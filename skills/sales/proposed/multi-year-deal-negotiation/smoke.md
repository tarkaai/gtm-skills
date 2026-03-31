---
name: multi-year-deal-negotiation-smoke
description: >
  Multi-Year Deal Negotiation — Smoke Test. Manually model multi-year deal
  structures for 3-5 active deals, present options, and close at least 1
  multi-year commitment. Validates that your product and market support
  multi-year deal structures before investing in automation.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "10 hours over 2 weeks"
outcome: ">=1 multi-year deal closed (2+ years) with TCV >=1.8x annual deal value within 2 weeks"
kpis: ["Multi-year close rate", "Average contract term (years)", "TCV vs annual ACV ratio", "Anchor-to-close ratio"]
slug: "multi-year-deal-negotiation"
install: "npx gtm-skills add sales/proposed/multi-year-deal-negotiation"
drills:
  - multi-year-deal-modeling
  - threshold-engine
---

# Multi-Year Deal Negotiation — Smoke Test

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that multi-year deal structures work for your product and market. Close at least 1 multi-year deal (2+ year commitment) with a TCV at least 1.8x the annual deal value. This validates that buyers in your market will commit to longer terms in exchange for rate protection and discount, and that the TCV uplift justifies the negotiation effort.

## Leading Indicators

- Deal term options generated for at least 3 deals with quantified pain-to-price ratios
- Comparison documents delivered to at least 3 champions
- At least 2 prospects engage in multi-year negotiation (counter-offer or discussion)
- Negotiation briefs prepared for each deal with walk-away floors defined before presenting
- Concession ladder followed (no jumping to max discount on first pushback)

## Instructions

### 1. Identify 3-5 deals for multi-year proposals

Query Attio for deals currently in the Proposed or Connected stage that meet these criteria:
- ACV >= $10,000 (negotiation overhead must be worth the TCV uplift)
- Pain-to-price ratio >= 5x (buyer needs strong value foundation to commit long-term)
- Champion identified (someone who can circulate the comparison internally)
- No prior multi-year proposal on this deal

If fewer than 3 deals qualify, include deals expected to reach Proposed stage this week. For each deal, pull from Attio: deal value, champion name/role, economic buyer name/role, competitive situation, and budget cycle timing.

### 2. Run the `multi-year-deal-modeling` drill for each deal

For each of the 3-5 qualified deals, execute the `multi-year-deal-modeling` drill:

1. Pull deal context and pain data from Attio
2. Generate 3 multi-year term options (high anchor, target, concession floor)
3. Generate the buyer-facing comparison document
4. Prepare the seller-side negotiation brief with concession ladder
5. Store all outputs in Attio as deal notes

Review each set of generated materials before presenting. Check:
- Are the discount levels within your approved range?
- Is the negotiation brief's walk-away floor acceptable?
- Does the comparison document read as buyer-centric, not vendor sales pitch?

### 3. Present multi-year options to prospects

**Human action required:** Deliver the comparison document to each prospect's champion. Preferred methods (in order of effectiveness):
1. Live walkthrough on a scheduled call — present the options, explain savings, answer questions in real-time
2. Email the comparison document with a note: "Based on our conversations, I put together the contract options for your team. Happy to walk through them."
3. Screen-share the comparison during an existing follow-up call

For each presentation:
- Lead with the highest-TCV option (anchoring)
- Frame discounts as "rate protection" — "this locks your price even if we raise rates next year"
- Never offer additional discount on first pushback — ask a diagnostic question instead: "What would make this work for your budget cycle?"
- Follow the concession ladder from the negotiation brief if the prospect pushes back
- Log the presentation and prospect's initial reaction in Attio

### 4. Handle negotiations and close

For each deal that enters negotiation:
- If prospect counters with different terms: compare against your walk-away floor. If within range, adjust. If below floor, explain the value gap and hold.
- If prospect asks for time: set a clear deadline tied to a business reason ("I can hold this rate through {fiscal year end date}")
- If prospect wants annual instead: log the revert reason. Annual is still a win — capture it.
- If prospect goes dark: follow up at day 3 and day 7, then escalate to a phone call

Log every touchpoint, counter-offer, and concession in Attio with dates and details.

### 5. Track results and evaluate

For each deal, log the outcome in Attio:
- Multi-year closed: record term, final annual price, TCV, discount given, negotiation rounds, and days to close
- Reverted to annual: record why (budget, timing, flexibility concern, decision-maker veto)
- Lost: record loss reason and best offer made

Run the `threshold-engine` drill at the end of 2 weeks. The threshold engine queries Attio for deals with `multi_year_status` = "closed_won" and checks:
- At least 1 multi-year deal closed
- TCV of that deal >= 1.8x the annual deal value
- Discount given <= maximum approved rate

If PASS: document which deal structures won, which presentation method worked best, and which prospect objections came up. Proceed to Baseline.
If FAIL: analyze why. Common failure modes:
- Weak pain data (ratio < 5x) — buyers don't see enough value to commit long-term. Fix discovery.
- Wrong prospects — ACV too low, no budget authority, or wrong timing. Tighten qualification.
- Discount-led negotiation — you anchored on savings instead of value/rate-protection. Reframe.
- No champion to circulate comparison internally — focus on champion development first.

## Time Estimate

- 2 hours: identifying qualified deals, pulling CRM data
- 4 hours: running the deal-modeling drill 3-5 times (generate, review, prepare negotiation brief)
- 3 hours: presenting to prospects, handling negotiation conversations
- 1 hour: logging outcomes, running threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, pain data, negotiation logging, notes | Standard stack (excluded from play budget) |
| PostHog | Event tracking for deal outcomes | Standard stack (excluded from play budget) |
| Anthropic Claude API | Deal term generation + comparison document creation | ~$1-3 for 3-5 deals at Sonnet rates ($3/$15 per M tokens) — [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Play-specific cost:** Free (Claude API cost negligible at this volume)

## Drills Referenced

- `multi-year-deal-modeling` — generates 3 deal term options per prospect, buyer-facing comparison document, and seller-side negotiation brief with concession ladder
- `threshold-engine` — evaluates pass/fail against the >=1 multi-year close target at 2-week mark
