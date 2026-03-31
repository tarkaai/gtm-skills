---
name: timing-objection-handling-smoke
description: >
  Timing Objection Handling — Smoke Test. Manually diagnose and respond to 5 timing
  objections using structured root-cause classification, smokescreen detection, and
  strategy-matched responses. Validate that a systematic approach accelerates more
  timelines than ad-hoc handling.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=3 out of 5 timing objections result in timeline acceleration or bridging solution acceptance within 1 week"
kpis: ["Timing objection resolution rate", "Timeline acceleration rate", "Cost of inaction presentation impact", "Smokescreen detection accuracy"]
slug: "timing-objection-handling"
install: "npx gtm-skills add sales/connected/timing-objection-handling"
drills:
  - threshold-engine
---

# Timing Objection Handling — Smoke Test

> **Stage:** Sales > Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that classifying timing objections by root cause — and distinguishing genuine constraints from smokescreens — produces a measurably higher timeline acceleration rate than ad-hoc responses. Target: >=3 out of 5 timing objections result in timeline acceleration or bridging solution acceptance (prospect agrees to move forward sooner, accepts a pilot, or commits to a concrete reengagement date).

## Leading Indicators

- Root cause classification completed within 24 hours of objection for all 5 objections
- Smokescreen vs genuine constraint determination made for all 5 objections
- Diagnostic questions asked (not just reactions given) in at least 4 out of 5 conversations
- Cost-of-delay analysis generated and presented for at least 3 out of 5 deals where pain data exists
- Follow-up with urgency asset sent within 48 hours for all unresolved objections

## Instructions

### 1. Identify 5 active deals with timing objections

Query Attio for deals in the Connected stage where the prospect has raised a timing objection ("not the right time", "maybe next quarter", "we're focused on other things", "let's circle back later"). If fewer than 5 exist today, include deals expected to have next calls this week.

For each deal, pull from Attio:
- Deal value
- Total quantified pain (from discovery)
- Pain-to-price ratio
- Timeline category (Immediate, Near-term, Medium-term, Long-term)
- Urgency drivers identified (if any)
- Champion name and role
- Economic buyer engagement status
- Competitor evaluation status

### 2. Run the the timing objection response workflow (see instructions below) drill for each objection

For each of the 5 deals, execute the the timing objection response workflow (see instructions below) drill:

1. Classify the timing objection root cause (competing_priority, no_urgency, budget_cycle, organizational_change, risk_aversion, smokescreen_budget, smokescreen_authority, smokescreen_fit, or genuine_constraint)
2. Determine whether the objection is a genuine constraint or a smokescreen masking a deeper concern (budget, authority, or fit)
3. If classification confidence is below 5, prepare the diagnostic questions and ask them on the next call before proceeding
4. If root cause is `no_urgency`, `competing_priority`, or `budget_cycle` and pain data exists, generate a cost-of-delay analysis showing monthly and cumulative cost of waiting
5. Generate a strategy-matched response (urgency_creation, cost_of_delay, bridging_solution, phased_approach, deferred_start, executive_alignment, reframe_to_pain, or strategic_patience)
6. **Human action required:** Review the generated response and cost-of-delay analysis. Adjust for your voice and relationship context. Deliver on the next call or via follow-up email.
7. Log the outcome in Attio: `timeline_accelerated`, `bridging_accepted`, `reengagement_scheduled`, `partially_resolved`, `unresolved`, or `deal_lost`

Do NOT accept "not the right time" at face value on any deal. Always run diagnostic questions to confirm whether timing is the real blocker. If the objection is a smokescreen, address the underlying concern directly.

### 3. Track results in Attio and PostHog

For each objection handled, create an Attio note with:
- Objection quote (prospect's exact words)
- Root cause classification
- Real constraint vs smokescreen determination
- Strategy used
- Cost-of-delay figures presented (if applicable)
- Response delivered (what you actually said or sent)
- Outcome
- Days from objection to resolution (or current status if still open)

Fire PostHog events: `timing_objection_handled` with root_cause, is_real_constraint, strategy_used, cost_of_delay_presented, and outcome properties.

### 4. Evaluate against threshold

Run the `threshold-engine` drill at the end of 1 week. The threshold engine queries PostHog for `timing_objection_handled` events and checks:
- Total objections handled: must be >= 5
- Objections with outcome `timeline_accelerated` or `bridging_accepted`: must be >= 3
- Smokescreen detection: how many smokescreen classifications were confirmed by the eventual outcome

If PASS (>=3 accelerated or bridging accepted): document which strategies won per root cause, which diagnostic questions surfaced the best information, and whether cost-of-delay presentations correlated with acceleration. Proceed to Baseline.

If FAIL (<3 resolved): analyze why. Common failure modes:
- Weak discovery upstream (no quantified pain, so cost-of-delay analysis has no teeth) -> fix discovery before re-running
- Wrong root cause classification (strategy didn't address actual concern) -> improve diagnostic questions
- No champion to reinforce urgency internally -> focus on champion development
- Genuine constraints where strategic patience was the right answer -> these don't count as failures if reengagement dates are set

## Time Estimate

- 1 hour: identifying deals and pulling CRM data
- 2.5 hours: running the timing-objection-response drill 5 times (classify, generate cost-of-delay, review, deliver)
- 0.5 hours: logging outcomes and tracking
- 1 hour: threshold evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, objection logging, timeline fields, notes | Standard stack (excluded from play budget) |
| PostHog | Event tracking for objection outcomes | Standard stack (excluded from play budget) |
| Anthropic Claude API | Objection classification + cost-of-delay generation + response strategy | ~$0.50-2 for 5 objections at Sonnet 4.6 rates ($3/$15 per M tokens) — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Play-specific cost:** Free (Claude API cost negligible at this volume)

## Drills Referenced

- the timing objection response workflow (see instructions below) — classifies each timing objection by root cause, determines genuine vs smokescreen, generates cost-of-delay analysis, produces a strategy-matched response, and logs outcomes
- `threshold-engine` — evaluates pass/fail against the >=3/5 acceleration target at week's end
