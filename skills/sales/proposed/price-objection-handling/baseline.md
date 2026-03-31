---
name: price-objection-handling-baseline
description: >
  Price Objection Handling — Baseline Run. First always-on automation: auto-trigger
  follow-up sequences matched to objection root cause, deliver value assets on a
  timed cadence, and track response effectiveness across 15-20 objections.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=60% of price objections overcome with <=14 days to close after resolution over 2 weeks"
kpis: ["Objection overcome rate", "Time to objection resolution", "Close rate (objection vs non-objection deals)", "Value asset engagement rate"]
slug: "price-objection-handling"
install: "npx gtm-skills add sales/proposed/price-objection-handling"
drills:
  - price-objection-response
  - objection-follow-up-sequence
  - pain-based-business-case
  - posthog-gtm-events
---

# Price Objection Handling — Baseline Run

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Scale to 15-20 price objections over 2 weeks with automated follow-up sequences. Prove that root-cause-matched follow-ups with timed value asset delivery produce a sustained >=60% overcome rate with resolution within 14 days.

## Leading Indicators

- Automated follow-up sequences firing within 4 hours of objection logging for all deals
- Value asset engagement rate >=40% (prospect opens ROI calculator, business case, or case study)
- Champion-ready business case generated for all deals with pain-to-price ratio >=5x
- No discount offered as first move on any deal

## Instructions

### 1. Configure event tracking

Run the `posthog-gtm-events` drill to set up comprehensive tracking for the price objection handling play. Configure these events:

- `price_objection_received` — fired when any price objection is logged (manual entry at this level)
- `price_objection_handled` — fired after response is delivered (from `price-objection-response` drill)
- `objection_follow_up_sent` — fired for each touch in the follow-up sequence
- `objection_asset_engaged` — fired when prospect opens a value asset
- `objection_resolved` — fired when objection outcome changes to resolved
- `deal_closed_won` / `deal_closed_lost` — fired at deal conclusion

Build a PostHog funnel: `price_objection_received` -> `price_objection_handled` -> `objection_follow_up_sent` -> `objection_asset_engaged` -> `objection_resolved` -> `deal_closed_won`

### 2. Deploy automated follow-up sequences

Run the `objection-follow-up-sequence` drill to build n8n workflows that auto-trigger when an objection outcome is logged as `partially_resolved` or `unresolved` in Attio. This creates:

- 6 root-cause-specific email sequences (no_budget, value_gap, competitor_comparison, sticker_shock, authority_gap, timing)
- Each sequence delivers 3-5 touches over 7-14 days with value assets matched to the root cause
- Sequences pause automatically on any prospect reply
- Reply routing: positive replies -> update deal stage; new objections -> re-classify and re-enter response drill; silence after full sequence -> mark deal as stalled

Configure Instantly for email delivery (warmed accounts required) or Loops for warmer contacts. Use `instantly-campaign` for cold/warm prospects or `loops-sequences` for existing relationships.

### 3. Generate business cases for high-value deals

For every deal where `pain_to_price_ratio >= 5` and the objection root cause is `value_gap` or `no_budget`, run the `pain-based-business-case` drill. This generates a champion-ready ROI document using the prospect's own pain data and quotes.

**Human action required:** Review each generated business case for accuracy before sending. Check that pain quotes are from the actual transcript, cost estimates are defensible, and the document reads like the champion wrote it (not like a vendor pitch).

Attach the business case as the Day 1 asset in the `value_gap` follow-up sequence.

### 4. Handle each objection through the response drill

Continue running the `price-objection-response` drill for each new price objection. At this level, the manual steps are the same as Smoke, but the follow-up is now automated:

1. Classify the objection root cause
2. Validate pain-to-price ratio
3. Generate and deliver the initial response
4. **The follow-up sequence triggers automatically** — no manual follow-up needed
5. Log the outcome when it resolves

Target: 15-20 objections handled over 2 weeks.

### 5. Measure and evaluate

At the end of 2 weeks, pull from PostHog:
- Total objections handled
- Overcome rate (resolved / total)
- Average days to resolution for resolved objections
- Asset engagement rate (objection_asset_engaged / objection_follow_up_sent)
- Close rate for deals with price objections vs deals without
- Framework effectiveness: resolve rate per framework used

Pass criteria: >=60% overcome rate AND average resolution time <=14 days.

If PASS: the automated follow-up system works. Proceed to Scalable.
If FAIL: diagnose the bottleneck:
- Low asset engagement (<30%) -> assets are not compelling or not relevant to root cause. Rewrite.
- Long resolution time (>14 days) -> follow-up cadence too slow or too passive. Tighten timing.
- Low overcome rate on specific root causes -> the response framework for that root cause needs revision.

## Time Estimate

- 4 hours: configuring PostHog events, building the tracking funnel
- 6 hours: setting up n8n follow-up workflows and email sequences in Instantly/Loops
- 2 hours: generating business cases for high-value deals
- 6 hours: running price-objection-response drill on 15-20 deals (faster now with practice)
- 2 hours: measurement, analysis, and iteration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, objection data, notes | Standard stack (excluded) |
| PostHog | Funnel tracking, event analytics | Standard stack (excluded) |
| n8n | Follow-up workflow automation | Standard stack (excluded) |
| Instantly | Email sequence delivery for follow-ups | Growth: $47/mo — [pricing](https://instantly.ai/pricing) |
| Anthropic Claude API | Objection classification, response generation, business case | ~$5-15/mo at 15-20 objections — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Loom (optional) | Video follow-ups for high-value deals | Free (5 min limit) or Business $12.50/mo — [pricing](https://www.loom.com/pricing) |

**Play-specific cost:** ~$50-65/mo (Instantly + Claude API)

## Drills Referenced

- `price-objection-response` — classifies each objection, generates response, logs outcome
- `objection-follow-up-sequence` — automated multi-touch follow-up with root-cause-matched value assets
- `pain-based-business-case` — generates champion-ready business case from pain data for value_gap and no_budget objections
- `posthog-gtm-events` — configures the full event tracking pipeline for the play
