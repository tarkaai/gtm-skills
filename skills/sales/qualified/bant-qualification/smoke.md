---
name: bant-qualification-smoke
description: >
  BANT Qualification Framework — Smoke Test. Run BANT qualification manually on a small batch of
  prospects to validate that Budget, Authority, Need, and Timeline scoring produces actionable
  signal for your ICP. Agent helps prep, founder executes discovery calls by hand.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=3 qualified leads (BANT composite score >=70) in 1 week from a batch of 15-20 prospects"
kpis: ["Qualification rate", "Time to qualify per lead", "Discovery call completion rate", "BANT score distribution"]
slug: "bant-qualification"
install: "npx gtm-skills add sales/qualified/bant-qualification"
drills:
  - icp-definition
  - build-prospect-list
  - bant-scorecard-setup
  - bant-discovery-call
  - threshold-engine
---

# BANT Qualification Framework — Smoke Test

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that structured BANT scoring produces meaningful signal. After qualifying 15-20 prospects, at least 3 should score >=70 (Qualified) and have a clear next step booked. The scoring rubric should differentiate between prospects that are ready to buy and those that are not.

## Leading Indicators

- Discovery calls are producing different BANT scores (not all clustering around the same number)
- At least one BANT dimension (Budget, Authority, Need, or Timeline) is consistently weak across prospects — this tells you where your pipeline has a gap
- Qualified prospects are moving forward to demos or proposals, while disqualified ones are not being chased

## Instructions

### 1. Define your ICP and BANT criteria

Run the `icp-definition` drill to document your Ideal Customer Profile. Then extend it with BANT-specific criteria:

- **Budget:** What's the minimum annual budget a prospect should have in your product's category? What funding stage or revenue range correlates with budget availability?
- **Authority:** Which job titles are decision makers vs. influencers for your product? What's the typical buying committee structure?
- **Need:** What are the top 3 pain points your product solves? What triggers indicate a prospect has this need right now?
- **Timeline:** What events create urgency (fiscal year end, contract renewals, new leadership, regulatory deadlines)?

Document these criteria — they feed the scoring rubric in the next step.

### 2. Set up BANT scoring in your CRM

Run the `bant-scorecard-setup` drill to create BANT custom fields on your Attio Deals object. This creates:
- Score fields (0-100) for each BANT dimension
- Status fields (Confirmed/Likely/Unclear/Absent) for each dimension
- Composite score with weighted formula: Budget (25%) + Authority (25%) + Need (30%) + Timeline (20%)
- Qualification verdict: Qualified (>=70), Needs Work (40-69), Disqualified (<40)
- Pipeline stages mapped to BANT outcomes

### 3. Build a small prospect list

Run the `build-prospect-list` drill to source 15-20 contacts matching your ICP. Keep the list small — this is a smoke test. Source from Apollo or Clay, enrich with basic firmographics, and push to Attio. For each prospect, manually estimate initial BANT scores based on what you can see from public data (funding stage, job title, company size, recent news).

### 4. Run discovery calls

**Human action required:** Book and conduct 8-12 discovery calls over the week. Use the `bant-discovery-call` drill for each call:

1. Before each call: review the prospect's pre-enrichment data and generate a BANT question guide focused on the weakest dimensions
2. During the call: work through Budget, Authority, Need, and Timeline questions naturally (do not interrogate — weave them into a genuine conversation about their challenges)
3. After each call: use the transcript to extract BANT signals and update scores in Attio

The `bant-discovery-call` drill handles pre-call prep, Fireflies transcript extraction, LLM-based BANT scoring, and CRM logging.

### 5. Score and evaluate

After completing your calls, review the BANT scores across all prospects. Run the `threshold-engine` drill to evaluate against the pass threshold: >=3 qualified leads (composite score >=70) in 1 week.

Analyze the results:
- What was the overall qualification rate?
- Which BANT dimension was weakest across the pipeline?
- Did the pre-enrichment estimates correlate with post-call scores?
- How long did each qualification take?

If PASS (>=3 qualified), proceed to Baseline. If FAIL, diagnose: are you targeting the wrong ICP (no budget/authority), missing the need (your product doesn't solve their top pain), or poor timing (no urgency)?

## Time Estimate

- ICP definition and BANT criteria: 1 hour
- CRM scorecard setup: 30 minutes
- Prospect list build: 1 hour
- Discovery calls (8-12 at 20-30 min each): 3-4 hours
- Post-call scoring and analysis: 30 minutes

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with BANT custom fields | Free tier (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Call recording and transcription | Free (800 min/mo) or Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Discovery call scheduling | Free (1 user) — [cal.com/pricing](https://cal.com/pricing) |
| Clay | Prospect enrichment | Launch plan $185/mo — [clay.com/pricing](https://clay.com/pricing) |
| PostHog | Event tracking | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost:** $0-18/mo (Fireflies Pro is optional; everything else fits in free tiers for a smoke test)

## Drills Referenced

- `icp-definition` — define ICP and extend with BANT-specific qualification criteria
- `build-prospect-list` — source and enrich 15-20 prospects from Apollo/Clay
- `bant-scorecard-setup` — create BANT scoring infrastructure in Attio
- `bant-discovery-call` — structured discovery call with transcript BANT extraction
- `threshold-engine` — evaluate results against the pass threshold
