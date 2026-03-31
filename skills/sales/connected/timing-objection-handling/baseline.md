---
name: timing-objection-handling-baseline
description: >
  Timing Objection Handling — Baseline Run. First always-on automation: auto-trigger
  root-cause-matched follow-up sequences with cost-of-delay content and urgency assets,
  track response strategy effectiveness across 15-20 timing objections over 2 weeks.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: ">=50% of timing objections result in timeline acceleration or bridging solution acceptance over 2 weeks"
kpis: ["Objection resolution rate", "Timeline acceleration success", "Cost of inaction conversion", "Bridging solution acceptance", "Eventual close rate"]
slug: "timing-objection-handling"
install: "npx gtm-skills add sales/connected/timing-objection-handling"
drills:
  - timing-objection-response
  - timing-objection-follow-up-sequence
  - timing-scorecard-setup
  - posthog-gtm-events
---

# Timing Objection Handling — Baseline Run

> **Stage:** Sales > Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Scale to 15-20 timing objections over 2 weeks with automated follow-up sequences. Prove that root-cause-matched follow-ups with timed urgency assets (cost-of-delay analyses, pilot proposals, reengagement scheduling) produce a sustained >=50% timeline acceleration or bridging acceptance rate.

## Leading Indicators

- Automated follow-up sequences firing within 4 hours of objection logging for all deals with `partially_resolved` or `unresolved` outcomes
- Cost-of-delay analysis generated and delivered for >=60% of timing objections where pain data exists
- Urgency asset engagement rate >=35% (prospect opens cost-of-delay document, pilot proposal, or case study)
- Smokescreen detection rate: >=40% of classified smokescreens confirmed by subsequent conversations
- No deal marked as "lost" without first running the full diagnostic question sequence

## Instructions

### 1. Configure CRM infrastructure

Run the `timing-scorecard-setup` drill to create timeline scoring fields on Attio Deals: `timeline_category`, `target_close_date`, `urgency_drivers`, `timeline_confidence`, `slippage_risk`, `consequence_of_inaction`, `timing_objection_root_cause`, `timing_objection_strategy`, `timing_objection_outcome`. Configure pipeline routing so Immediate deals get daily follow-up cadence, Near-term gets 2-3x/week, and Long-term goes to biweekly nurture.

### 2. Configure event tracking

Run the `posthog-gtm-events` drill to set up comprehensive tracking for the timing objection handling play. Configure these events:

- `timing_objection_received` — fired when any timing objection is logged (manual entry at this level)
- `timing_objection_handled` — fired after response is delivered (from `timing-objection-response` drill)
- `timing_follow_up_sent` — fired for each touch in the follow-up sequence
- `timing_asset_engaged` — fired when prospect opens an urgency asset
- `timing_objection_resolved` — fired when outcome changes to `timeline_accelerated` or `bridging_accepted`
- `deal_closed_won` / `deal_closed_lost` — fired at deal conclusion

Build a PostHog funnel: `timing_objection_received` -> `timing_objection_handled` -> `timing_follow_up_sent` -> `timing_asset_engaged` -> `timing_objection_resolved` -> `deal_closed_won`

### 3. Deploy automated follow-up sequences

Run the `timing-objection-follow-up-sequence` drill to build n8n workflows that auto-trigger when a timing objection outcome is logged as `partially_resolved`, `unresolved`, or `reengagement_scheduled` in Attio. This creates:

- 7 root-cause-specific follow-up sequences (competing_priority, no_urgency, budget_cycle, organizational_change, risk_aversion, smokescreen variants, genuine_constraint)
- Each sequence delivers 2-5 touches over 7-60 days with urgency assets matched to the root cause
- Sequences pause automatically on any prospect reply
- Reply routing: timeline acceleration -> update deal stage; new objection surfaces -> re-classify and route to appropriate play; silence after full sequence -> mark deal stalled with 60-day reminder

Configure Instantly for email delivery (warmed accounts required) or Loops for warmer contacts. Use `instantly-campaign` for cold/warm prospects or `loops-sequences` for existing relationships.

### 4. Handle each objection through the response drill

Continue running the `timing-objection-response` drill for each new timing objection. At this level, the manual steps are the same as Smoke, but the follow-up is now automated:

1. Classify the objection root cause and determine genuine vs smokescreen
2. If confidence >= 5, generate the response and cost-of-delay analysis (where applicable)
3. **Human action required:** Review and deliver the initial response
4. **The follow-up sequence triggers automatically** — no manual follow-up needed
5. Log the outcome when it resolves

Target: 15-20 objections handled over 2 weeks.

### 5. Generate cost-of-delay for high-value deals

For every deal where `total_quantified_pain` exists and root cause is `no_urgency`, `competing_priority`, or `budget_cycle`, ensure a cost-of-delay analysis is generated as part of the `timing-objection-response` drill. The analysis is attached as the primary asset in the follow-up sequence.

**Human action required:** Review each cost-of-delay analysis for accuracy before it is sent. Verify that pain figures match discovery data, calculations are defensible, and the document reads like a helpful analysis (not a pressure tactic).

### 6. Measure and evaluate

At the end of 2 weeks, pull from PostHog:
- Total objections handled
- Acceleration rate (timeline_accelerated + bridging_accepted / total)
- Average days to resolution for resolved objections
- Asset engagement rate (timing_asset_engaged / timing_follow_up_sent)
- Strategy effectiveness: acceleration rate per strategy per root cause
- Smokescreen detection accuracy: how many smokescreen classifications matched the real objection
- Close rate for deals with timing objections vs deals without

Pass criteria: >=50% acceleration or bridging acceptance rate.

If PASS: the automated follow-up system works. Document winning strategies per root cause. Proceed to Scalable.
If FAIL: diagnose the bottleneck:
- Low asset engagement (<25%) -> cost-of-delay analyses or urgency assets are not compelling. Rewrite with more prospect-specific data.
- Low acceleration on `no_urgency` objections -> cost-of-delay is not creating enough urgency. Make compounding factors more concrete.
- High smokescreen rate with low detection accuracy -> diagnostic questions need refinement. Add more direct probing.
- Deals stuck at `reengagement_scheduled` -> reengagement timing or content needs improvement.

## Time Estimate

- 3 hours: configuring Attio timeline fields (timing-scorecard-setup) and PostHog events
- 4 hours: setting up n8n follow-up workflows and email sequences in Instantly/Loops
- 1 hour: reviewing and adjusting cost-of-delay templates
- 4 hours: running timing-objection-response drill on 15-20 deals
- 2 hours: measurement, analysis, and iteration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, timeline fields, objection data, notes | Standard stack (excluded) |
| PostHog | Funnel tracking, event analytics | Standard stack (excluded) |
| n8n | Follow-up workflow automation | Standard stack (excluded) |
| Instantly | Follow-up email delivery | Growth: $47/mo — [pricing](https://instantly.ai/pricing) |
| Anthropic Claude API | Objection classification, cost-of-delay generation, response strategy | ~$5-15/mo at 15-20 objections — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Play-specific cost:** ~$50-65/mo (Instantly + Claude API)

## Drills Referenced

- `timing-objection-response` — classifies each timing objection, determines genuine vs smokescreen, generates cost-of-delay analysis and strategy-matched response
- `timing-objection-follow-up-sequence` — automated multi-touch follow-ups with root-cause-matched urgency assets (cost-of-delay, pilot proposals, reengagement scheduling)
- `timing-scorecard-setup` — creates timeline scoring fields, pipeline routing, and PostHog events for timing qualification in Attio
- `posthog-gtm-events` — configures the full event tracking pipeline for the play
