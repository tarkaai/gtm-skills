---
name: budget-objection-handling-smoke
description: >
  Budget Objection Handling — Smoke Test. Manually diagnose and respond to 5 budget
  objections using structured root-cause classification, smokescreen detection, and
  budget navigation frameworks. Validate that systematic budget navigation outperforms
  ad-hoc responses.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "Navigate >=3 out of 5 budget objections to a clear next step within 1 week"
kpis: ["Budget navigation success rate", "Smokescreen detection accuracy", "Payment structure acceptance rate", "Days from objection to next step"]
slug: "budget-objection-handling"
install: "npx gtm-skills add sales/proposed/budget-objection-handling"
drills:
  - budget-objection-response
  - threshold-engine
---

# Budget Objection Handling — Smoke Test

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that classifying budget objections by root cause (not just "no budget") and applying navigation-specific responses produces a measurably higher success rate than treating budget objections as price objections. Target: navigate >=3 out of 5 budget objections to a clear next step (prospect advances toward budget approval, accepts a creative payment structure, or connects you to the budget owner).

## Leading Indicators

- Root cause classification completed within 24 hours of objection for all 5 objections
- Smokescreen detection applied to all 5 — at least 1 correctly identified as smokescreen or confirmed genuine
- Diagnostic questions asked (not just responses given) in at least 4 out of 5 conversations
- Payment structure options presented for all deals where root cause is `no_allocated_budget`, `budget_exhausted`, or `competing_priorities`
- Champion asset (budget justification memo) generated for at least 2 deals

## Instructions

### 1. Identify 5 active deals with budget objections

Query Attio for deals in the Proposed or Negotiation stage where the prospect has indicated a budget constraint. Budget objections sound different from price objections:
- Budget: "We don't have budget for this", "That's not in our plan", "I'd need to get finance to approve", "Our budget is committed elsewhere"
- Price (NOT this play): "That's too expensive", "Your competitor is cheaper", "We can't justify that cost"

If fewer than 5 budget objections exist today, include deals expected to reach the proposal stage this week.

For each deal, pull from Attio:
- Deal value
- Total quantified pain (from discovery)
- Pain-to-price ratio
- Champion name and role
- Economic buyer name and role (critical for budget navigation — if unknown, flag it)
- Prospect's fiscal year end (if known)
- Competitive evaluation status

### 2. Run the `budget-objection-response` drill for each objection

For each of the 5 deals:

1. **Classify the root cause** using `budget-objection-classification`. The 6 possible root causes are: `no_allocated_budget`, `budget_exhausted`, `wrong_budget_owner`, `competing_priorities`, `procurement_friction`, `budget_smokescreen`. This is NOT the same taxonomy as price objections.

2. **Detect smokescreens.** If the classifier returns `is_smokescreen: true`, do NOT attempt budget navigation. Instead, re-qualify the deal: is there genuine interest? Is the champion still engaged? What is the real blocker? Log this deal separately.

3. **Validate the value foundation.** If `pain_to_price_ratio < 3`, the budget objection may be harder to navigate because the internal justification story is weak. Flag for additional discovery.

4. **Generate a navigation response** matched to the root cause. For budget-specific objections, the response helps the prospect find or unlock budget — it does NOT try to convince them the product is worth the money (that is price objection territory).

5. **Generate payment structure options** for applicable root causes. Present 2-3 creative structures that preserve deal value (deferred start, quarterly billing, phased rollout, ramp pricing).

6. **Human action required:** Review the generated response and payment options. Adjust for your voice and the specific relationship. Deliver on the next call or via follow-up email.

7. Log the outcome in Attio: `resolved` (budget found/approved), `partially_resolved` (path identified but not yet approved), `unresolved` (no path found), `escalated` (moved to different stakeholder), `smokescreen` (re-qualified as non-budget issue), `lost`.

### 3. Track results in Attio and PostHog

For each objection handled, create an Attio note with:
- Objection quote (prospect's exact words)
- Root cause classification
- Navigation framework used
- Payment structure options presented (if any)
- Payment structure accepted (if any)
- Champion asset generated and sent (yes/no)
- Outcome
- Days from objection to next step (or current status if still open)

Fire PostHog events: `budget_objection_handled` with root_cause, framework_used, outcome, navigability_score, payment_structure_accepted, deal_value_preserved, and was_smokescreen properties.

### 4. Evaluate against threshold

Run the `threshold-engine` drill at the end of 1 week. The threshold engine queries PostHog for `budget_objection_handled` events and checks:
- Total objections handled: must be >= 5
- Objections with outcome = `resolved` or `partially_resolved` with clear next step: must be >= 3
- Smokescreen detection: at least 1 deal correctly classified as smokescreen or confirmed genuine

If PASS (>=3 navigated): document which frameworks won, which root causes are most common, and which payment structures were accepted. Proceed to Baseline.
If FAIL (<3 navigated): analyze why. Common failure modes:
- Weak value foundation (pain-to-price ratio < 5x on most deals) -> fix discovery before re-running
- Wrong root cause classification (navigation didn't address actual constraint) -> improve diagnostic questions
- No economic buyer access (budget owner unknown) -> focus on stakeholder mapping
- High smokescreen rate (>50%) -> the real objection is elsewhere; fix qualification

## Time Estimate

- 1 hour: identifying deals and pulling CRM data
- 3 hours: running the budget-objection-response drill 5 times (classify, generate, review, deliver)
- 1 hour: logging outcomes and tracking
- 1 hour: threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, budget objection logging, notes | Standard stack (excluded from play budget) |
| PostHog | Event tracking for budget navigation outcomes | Standard stack (excluded from play budget) |
| Anthropic Claude API | Budget classification + navigation response + payment structures | ~$1-3 for 5 objections at Sonnet rates ($3/$15 per M tokens) -- [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Play-specific cost:** Free (Claude API cost negligible at this volume)

## Drills Referenced

- `budget-objection-response` — classifies each budget objection by root cause (6-category taxonomy distinct from price objections), detects smokescreens, generates navigation response with payment structure options, handles delivery and outcome logging
- `threshold-engine` — evaluates pass/fail against the >=3/5 navigation target at week's end
