---
name: stakeholder-mapping-smoke
description: >
  Stakeholder Mapping Framework — Smoke Test. Manually research and classify decision-makers,
  influencers, and blockers in 3 active deals to validate that multi-threaded stakeholder
  mapping produces better deal intelligence than single-threaded selling.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Social, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=3 stakeholders mapped per deal with at least 1 Economic Buyer or Champion identified, for >=3 deals in 1 week"
kpis: ["Stakeholders mapped per deal", "Economic Buyer identification rate", "Champion identification rate", "Gap count per deal"]
slug: "stakeholder-mapping"
install: "npx gtm-skills add sales/connected/stakeholder-mapping"
drills:
  - stakeholder-research
  - threshold-engine
---

# Stakeholder Mapping Framework — Smoke Test

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Social, Email

## Outcomes

Map at least 3 stakeholders (with role classifications) per deal across 3 active deals in 1 week. Each deal must have at least one Economic Buyer or Champion identified. This validates that systematic stakeholder research surfaces contacts and insights that ad-hoc relationship tracking misses.

## Leading Indicators

- Discovery calls yield 2+ new stakeholder names per call when using structured questions
- Org chart research in Clay returns 10+ Director-level contacts per target account
- Stakeholder classifications align with observed behavior (Champions actually advocate, Blockers actually raise objections)
- Deals with mapped stakeholders have clearer next steps than unmapped deals

## Instructions

### 1. Set up CRM stakeholder tracking

Run the the crm pipeline setup workflow (see instructions below) drill if your Attio pipeline is not yet configured. Then create custom attributes on Person records for stakeholder tracking:
- `stakeholder_role` (select: Economic Buyer, Champion, Influencer, Blocker, End User, Gatekeeper)
- `stakeholder_confidence` (select: High, Medium, Low)
- `stakeholder_sentiment` (select: Supportive, Neutral, Opposed, Unknown)
- `engagement_level` (select: Active, Warm, Cold, No Contact)

Also add to Deals: `stakeholder_count` (number), `champion_identified` (checkbox), `economic_buyer_identified` (checkbox).

### 2. Select 3 active deals to map

Choose 3 deals currently at Connected stage or later. Prioritize deals where you have at least one contact but suspect there are more stakeholders involved. Avoid deals that are already well-mapped or about to close.

### 3. Run stakeholder research on each deal

Run the `stakeholder-research` drill for each of the 3 deals. For each deal:

1. List all known contacts from prior calls and emails.
2. Research the org chart. If you have Clay, use the `org-chart-research` fundamental to find 15-20 Director+ people at the company. If not, use LinkedIn search (free or Sales Navigator) to manually find contacts by filtering for the company + Director/VP/C-Suite titles.
3. Classify each person into a buying committee role (Economic Buyer, Champion, Influencer, Blocker, End User, Gatekeeper) using title-based rules first, then AI classification for ambiguous cases.
4. Rate confidence (High/Medium/Low) for each classification.
5. Set sentiment to "Unknown" for contacts you have not interacted with.
6. Store everything in Attio: custom attributes on Person records + a stakeholder map note on the Deal.

**Human action required:** During your next discovery call with each deal, ask targeted stakeholder discovery questions:
- "Who else on your team will be evaluating this?"
- "Who controls the budget for a purchase like this?"
- "Who will be the day-to-day users?"
- "Is there anyone who might have concerns about changing from your current approach?"
- "Walk me through how a purchase decision like this typically gets made at {Company}."

Update the stakeholder map after each call with new names, confirmed roles, and sentiment observations.

### 4. Identify gaps and risks

After mapping all 3 deals, review each for:
- Missing Economic Buyer (cannot close without budget authority)
- Missing Champion (no internal advocate = selling from the outside)
- Unaddressed Blockers (will silently kill the deal if not engaged)
- Single-threading (only 1-2 contacts engaged = fragile deal)

Document gaps as action items: who to find, who to engage, what concerns to address.

### 5. Evaluate against threshold

Run the `threshold-engine` drill. The pass criteria:
- **>=3 stakeholders mapped per deal** for all 3 deals
- **At least 1 Economic Buyer or Champion identified** per deal
- **Classification confidence is Medium or High** for the majority of stakeholders

If PASS: Document the stakeholder research process that worked, note which discovery questions surfaced the most new names, and proceed to Baseline.

If FAIL: Diagnose — was the issue insufficient org chart data (Clay returned few results), weak discovery questions (calls did not surface new names), or wrong deal selection (deals were too early or too small for multi-stakeholder buying)? Adjust and re-run.

## Time Estimate

- CRM setup: 1 hour (one-time)
- Org chart research per deal: 45 minutes (3 deals = 2.25 hours)
- Classification and CRM logging per deal: 30 minutes (3 deals = 1.5 hours)
- Discovery calls: 30 minutes each (built into existing call schedule)
- Gap analysis and threshold evaluation: 1 hour

**Total: ~6 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM for stakeholder tracking and deal management | Free tier (3 users) or Plus at $29/user/mo |
| Clay | Org chart research and people enrichment | Launch at $185/mo (15,000 actions) |
| PostHog | Event tracking for threshold evaluation | Free tier (1M events/mo) |
| LinkedIn | Manual org chart browsing and stakeholder research | Free or Sales Navigator Core at $99.99/mo |

**Estimated monthly cost for this level: $0-29** (Attio free tier + Clay not required for manual research at Smoke scale; LinkedIn free search sufficient for 3 deals)

## Drills Referenced

- `stakeholder-research` — Manual research and classification of all stakeholders in each target account
- the crm pipeline setup workflow (see instructions below) — Configure Attio with stakeholder-specific custom attributes and deal fields
- `threshold-engine` — Evaluate results against pass/fail criteria to determine readiness for Baseline
