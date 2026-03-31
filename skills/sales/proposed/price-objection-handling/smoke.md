---
name: price-objection-handling-smoke
description: >
  Price Objection Handling — Smoke Test. Manually diagnose and respond to 5 price
  objections using structured root-cause classification and response frameworks.
  Validate that a systematic approach outperforms ad-hoc responses.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Overcome >=3 out of 5 price objections within 1 week"
kpis: ["Objection overcome rate", "Response framework effectiveness by root cause", "Time from objection to resolution"]
slug: "price-objection-handling"
install: "npx gtm-skills add sales/proposed/price-objection-handling"
drills:
  - price-objection-response
  - threshold-engine
---

# Price Objection Handling — Smoke Test

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that classifying price objections by root cause and applying framework-matched responses produces a measurably higher overcome rate than ad-hoc responses. Target: overcome >=3 out of 5 price objections (prospect advances to next deal stage after objection).

## Leading Indicators

- Root cause classification completed within 24 hours of objection for all 5 objections
- Diagnostic questions asked (not just reactions given) in at least 4 out of 5 objection conversations
- Pain-to-price ratio retrieved from CRM for at least 4 out of 5 deals
- Follow-up with value asset sent within 48 hours for all unresolved objections

## Instructions

### 1. Identify 5 active deals with price objections

Query Attio for deals in the Proposed or Negotiation stage that have received price pushback. If fewer than 5 exist today, include deals expected to reach proposal stage this week.

For each deal, pull from Attio:
- Deal value
- Total quantified pain (from discovery)
- Pain-to-price ratio
- Champion name and role
- Economic buyer name and role (if known)
- Competitor evaluation status

### 2. Run the `price-objection-response` drill for each objection

For each of the 5 deals, execute the `price-objection-response` drill:
1. Classify the objection root cause (no_budget, value_gap, competitor_comparison, sticker_shock, authority_gap, or timing)
2. Validate the pain-to-price ratio — if below 3x, flag this deal as needing deeper discovery before responding
3. Generate a tailored response using the framework mapped to that root cause
4. **Human action required:** Review the generated response, adjust for your voice, and deliver it on the next call or via follow-up email
5. Log the outcome (resolved, partially_resolved, unresolved, escalated, lost) in Attio

Do NOT offer a discount as the first move on any deal. Lead with value reframing, ROI proof, or pain anchoring first.

### 3. Track results in Attio and PostHog

For each objection handled, create an Attio note with:
- Objection quote (prospect's exact words)
- Root cause classification
- Response framework used
- Response delivered (what you actually said/sent)
- Outcome
- Days from objection to resolution (or current status if still open)

Fire PostHog events using the `price-objection-response` drill's event schema: `price_objection_handled` with root_cause, framework_used, outcome, severity, and discount_percentage properties.

### 4. Evaluate against threshold

Run the `threshold-engine` drill at the end of 1 week. The threshold engine queries PostHog for `price_objection_handled` events and checks:
- Total objections handled: must be >= 5
- Objections with outcome = "resolved": must be >= 3
- Average days_to_resolution for resolved objections

If PASS (>=3 resolved): document which frameworks won and which root causes are most common. Proceed to Baseline.
If FAIL (<3 resolved): analyze why. Common failure modes:
- Weak discovery (pain-to-price ratio < 5x on most deals) -> fix discovery before re-running
- Wrong root cause classification (response didn't address actual concern) -> improve diagnostic questions
- No champion to reinforce value internally -> focus on champion development

## Time Estimate

- 1 hour: identifying deals and pulling CRM data
- 3 hours: running the price-objection-response drill 5 times (classify, generate, review, deliver)
- 1 hour: logging outcomes and tracking
- 1 hour: threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, objection logging, notes | Standard stack (excluded from play budget) |
| PostHog | Event tracking for objection outcomes | Standard stack (excluded from play budget) |
| Anthropic Claude API | Objection classification + response generation | ~$0.50-2 for 5 objections at Sonnet 4.6 rates ($3/$15 per M tokens) — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Play-specific cost:** Free (Claude API cost negligible at this volume)

## Drills Referenced

- `price-objection-response` — classifies each objection by root cause, generates a framework-matched response, handles delivery and outcome logging
- `threshold-engine` — evaluates pass/fail against the >=3/5 overcome target at week's end
