---
name: budget-objection-handling-baseline
description: >
  Budget Objection Handling — Baseline Run. First always-on automation: auto-trigger
  budget navigation follow-up sequences matched to root cause, deliver champion
  enablement assets on a timed cadence, and track navigation effectiveness across
  15-20 budget objections.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=50% of budget objections navigated to resolution with deal value preserved on >=90% of resolved deals over 2 weeks"
kpis: ["Budget navigation success rate", "Deal value preservation rate", "Payment structure acceptance by type", "Champion asset engagement rate", "Days to budget resolution"]
slug: "budget-objection-handling"
install: "npx gtm-skills add sales/proposed/budget-objection-handling"
drills:
  - budget-objection-response
  - pain-based-business-case
  - posthog-gtm-events
---

# Budget Objection Handling — Baseline Run

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Scale to 15-20 budget objections over 2 weeks with automated follow-up sequences. Prove that root-cause-matched follow-ups with budget navigation assets (justification memos, payment structures, cost-of-delay analyses) produce a sustained >=50% navigation success rate with deal value preserved on >=90% of resolved deals.

## Leading Indicators

- Automated follow-up sequences firing within 4 hours of budget objection logging for all deals
- Champion asset engagement rate >=40% (champion opens budget justification memo, downloads payment options, or forwards materials internally)
- Budget justification memo generated for all deals with pain-to-price ratio >=5x
- Deal value preserved (no discount offered) on >=90% of deals where budget was navigated
- Smokescreen detection rate steady or improving from Smoke level

## Instructions

### 1. Configure event tracking

Run the `posthog-gtm-events` drill to set up comprehensive tracking for the budget objection handling play. Configure these events:

- `budget_objection_received` — fired when any budget objection is logged (manual entry at this level)
- `budget_objection_handled` — fired after navigation response is delivered (from `budget-objection-response` drill)
- `budget_follow_up_sent` — fired for each touch in the follow-up sequence
- `budget_asset_engaged` — fired when prospect opens a budget navigation asset
- `budget_asset_forwarded` — fired when the champion forwards the justification memo (detected via email tracking)
- `budget_objection_resolved` — fired when objection outcome changes to resolved
- `deal_closed_won` / `deal_closed_lost` — fired at deal conclusion

Build a PostHog funnel: `budget_objection_received` -> `budget_objection_handled` -> `budget_follow_up_sent` -> `budget_asset_engaged` -> `budget_asset_forwarded` -> `budget_objection_resolved` -> `deal_closed_won`

The critical funnel step unique to budget objections is `budget_asset_forwarded` — when the champion shares the justification memo internally, that is the strongest signal that budget navigation is working.

### 2. Deploy automated follow-up sequences

Run the the budget follow up sequence workflow (see instructions below) drill to build n8n workflows that auto-trigger when a budget objection outcome is logged as `partially_resolved` or `unresolved` in Attio. This creates:

- 5 root-cause-specific sequences (no_allocated_budget, budget_exhausted, wrong_budget_owner, competing_priorities, procurement_friction)
- Each sequence delivers 3-5 touches over 10-30 days with budget navigation assets matched to the root cause
- Sequences are timed to the prospect's budget cycle (budget_exhausted sequences anchor to the next fiscal year)
- Sequences pause automatically on any prospect reply
- Reply routing: positive replies -> update deal stage; new information -> re-classify and re-enter response drill; silence -> mark as budget_stalled with nurture reminder

Configure Instantly for email delivery (warmed accounts required) or Loops for warmer contacts. Use `instantly-campaign` for cold/warm prospects or `loops-sequences` for existing relationships.

### 3. Generate champion enablement materials

For every deal where `pain_to_price_ratio >= 5` and the root cause is `no_allocated_budget`, `budget_exhausted`, or `competing_priorities`, run the `pain-based-business-case` drill. This generates a champion-ready business case using the prospect's own pain data.

Additionally, generate budget-specific materials:
- **Budget justification memo:** One-page document written from the champion's perspective, not the vendor's. Includes: problem statement using the prospect's language, annual cost of the problem, proposed solution cost, ROI and payback period, recommended payment structure.
- **Cost-of-delay analysis:** For each month the prospect delays, calculate: `(annual_quantified_pain / 12) * months_delayed`. Present as: "Every month of delay costs your team ${X}."

**Human action required:** Review each generated document for accuracy before sending. The budget justification memo must read like the champion wrote it — not like a sales pitch.

### 4. Handle each objection through the response drill

Continue running the `budget-objection-response` drill for each new budget objection. At this level:

1. Classify the root cause (including smokescreen detection)
2. Validate the value foundation (pain-to-price ratio)
3. Generate and deliver the initial navigation response with payment structure options
4. **The follow-up sequence triggers automatically** — no manual follow-up needed
5. Champion enablement materials attach to the sequence automatically for qualifying deals
6. Log the outcome when it resolves

Target: 15-20 budget objections handled over 2 weeks.

### 5. Measure and evaluate

At the end of 2 weeks, pull from PostHog:
- Total budget objections handled
- Navigation success rate (resolved / total, excluding smokescreens)
- Deal value preservation rate (deals with no discount / total resolved)
- Payment structure acceptance breakdown (which structures were accepted)
- Champion asset engagement rate (budget_asset_engaged / budget_follow_up_sent)
- Champion asset forward rate (budget_asset_forwarded / budget_asset_engaged) — the key signal
- Average days to budget resolution
- Smokescreen detection rate and accuracy

Pass criteria: >=50% navigation success rate AND deal value preserved on >=90% of resolved deals.

If PASS: automated budget follow-ups work. Proceed to Scalable.
If FAIL: diagnose the bottleneck:
- Low champion engagement (<30%) -> materials are not compelling or not positioned as the champion's own. Rewrite to be more buyer-centric.
- Low preservation rate (<80%) -> sellers are falling back to discounts instead of creative payment structures. Reinforce the framework.
- High smokescreen rate (>40%) -> qualification is weak upstream. Fix discovery before scaling.
- Navigation success below 40% on specific root causes -> the framework for that root cause needs revision.

## Time Estimate

- 4 hours: configuring PostHog events and building the tracking funnel
- 6 hours: setting up n8n follow-up workflows and email sequences
- 3 hours: generating champion enablement materials
- 5 hours: running budget-objection-response drill on 15-20 deals
- 2 hours: measurement, analysis, and iteration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, budget objection data, champion tracking | Standard stack (excluded) |
| PostHog | Funnel tracking, event analytics | Standard stack (excluded) |
| n8n | Follow-up workflow automation | Standard stack (excluded) |
| Instantly | Email sequence delivery for follow-ups | Growth: $47/mo -- [pricing](https://instantly.ai/pricing) |
| Anthropic Claude API | Budget classification, navigation responses, champion materials | ~$8-20/mo at 15-20 objections -- [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Play-specific cost:** ~$55-67/mo (Instantly + Claude API)

## Drills Referenced

- `budget-objection-response` — classifies each budget objection, generates navigation response with payment structures, logs outcome
- the budget follow up sequence workflow (see instructions below) — automated multi-touch follow-up with root-cause-matched budget navigation assets and budget-cycle-aware timing
- `pain-based-business-case` — generates champion-ready business case from pain data for budget justification
- `posthog-gtm-events` — configures the full event tracking pipeline for the play
