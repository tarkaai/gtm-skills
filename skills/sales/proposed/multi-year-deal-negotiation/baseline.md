---
name: multi-year-deal-negotiation-baseline
description: >
  Multi-Year Deal Negotiation — Baseline Run. First always-on automation:
  auto-generate proposals when deals reach Proposed stage, deliver comparison
  docs, track negotiation events, and measure close rate and TCV across
  all multi-year proposals over 4 weeks.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">=25% close rate on multi-year proposals with average TCV >=1.8x annual ACV across 10+ proposals over 4 weeks"
kpis: ["Multi-year close rate", "Average TCV", "TCV-to-ACV ratio", "Average discount given", "Negotiation rounds per deal"]
slug: "multi-year-deal-negotiation"
install: "npx gtm-skills add sales/proposed/multi-year-deal-negotiation"
drills:
  - multi-year-proposal-automation
  - deal-negotiation-tracking
---

# Multi-Year Deal Negotiation — Baseline Run

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that automated multi-year proposal generation holds the close rate and TCV results from Smoke over a larger volume. Every qualified deal entering the Proposed stage automatically receives a multi-year proposal. Negotiation events are instrumented end-to-end. Target: >=25% close rate on multi-year proposals with average TCV at least 1.8x the annual deal value across 10+ proposals over 4 weeks.

## Leading Indicators

- Automated proposal workflow firing for every qualifying deal (no manual triggers needed)
- All 7 negotiation events tracked in PostHog with consistent properties
- Attio custom attributes populated on every deal in the pipeline
- Negotiation funnel in PostHog showing conversion at each step
- Follow-up sequences executing on schedule (day 3 and day 7 for non-responders)
- Bidirectional sync between Attio and PostHog verified (updates in one appear in the other)

## Instructions

### 1. Deploy the proposal automation workflow

Run the `multi-year-proposal-automation` drill to build the n8n workflow that triggers when a deal enters the Proposed stage:

1. Configure the Attio webhook trigger for deal stage change to "Proposed"
2. Set qualification filters: ACV >= $10,000, pain-to-price ratio >= 5x, champion identified, no prior multi-year proposal
3. Wire up the Anthropic API calls for deal term generation and comparison document creation
4. Configure email delivery: comparison doc sent from the deal owner's email address
5. Set up the follow-up sequence: day 3 nudge, day 7 escalation to human
6. Build response handlers: positive, negative, and counter-offer paths

Test the workflow end-to-end with a test deal before going live:
- Create a test deal in Attio matching all qualification criteria
- Move it to Proposed stage
- Verify: proposal generated, comparison doc created, email drafted (don't send to a real prospect during testing)
- Verify: all PostHog events fired correctly
- Verify: Attio attributes updated

### 2. Instrument negotiation tracking

Run the `deal-negotiation-tracking` drill to set up the full event schema:

1. Create all 7 negotiation events in PostHog with the defined properties
2. Add custom attributes to the Deal object in Attio: `multi_year_status`, `proposed_term_years`, `proposed_discount_pct`, `final_term_years`, `final_discount_pct`, `final_tcv`, `negotiation_rounds`, `concessions_made`, `days_in_negotiation`, `anchor_to_close_ratio`
3. Build the negotiation funnel in PostHog: generated -> sent -> counter_received -> closed_won
4. Build the loss analysis funnel: sent -> closed_lost (breakdown by reason)
5. Create the bidirectional n8n sync between Attio and PostHog
6. Verify computed metrics are calculated on each close event: anchor-to-close ratio, days-in-negotiation, discount-efficiency

### 3. Go live and monitor

Activate the proposal automation workflow. For the first week, monitor closely:
- Check every automated proposal before it sends (add a human approval step in n8n for week 1)
- Verify deal term options are reasonable for each prospect
- Verify comparison documents are accurate and buyer-centric
- Check that follow-up sequences fire on schedule

After week 1, if no issues: remove the human approval step. The workflow runs fully autonomously.

### 4. Handle negotiations (human-in-the-loop)

**Human action required:** When a prospect responds to a multi-year proposal:
- The automation handles logging and alerting
- The founder/seller handles the actual negotiation conversation
- After each conversation, update Attio with: what was discussed, any counter-offers, concessions made, and next steps
- The automation picks up the Attio update and fires the corresponding PostHog events

For this level, negotiation itself stays human-driven. The automation handles proposal generation, delivery, follow-up, and tracking. The human handles the conversations.

### 5. Evaluate against threshold

At the end of 4 weeks, review the PostHog negotiation dashboard:
- Total proposals sent (must be >= 10 for meaningful evaluation)
- Close rate on multi-year proposals (target: >= 25%)
- Average TCV of closed multi-year deals (target: >= 1.8x annual ACV)
- Average discount given (benchmark against Smoke results)
- Negotiation rounds per deal (fewer = better proposal quality)
- Funnel conversion at each step (identify where deals drop off)

If PASS (>= 25% close rate AND >= 1.8x TCV ratio across 10+ proposals):
- Document the working deal structure templates
- Note which segments close best (by ACV, industry, champion seniority)
- Proceed to Scalable

If FAIL:
- If close rate is below 25% but TCV ratio is high: proposals are strong but volume is low. Check qualification criteria — may be too strict.
- If close rate is above 25% but TCV ratio is below 1.8x: too much discounting. Tighten the concession parameters.
- If both are below threshold: diagnose the funnel. Where are deals dropping off? Qualification, proposal quality, delivery timing, or negotiation?

## Time Estimate

- 6 hours: setting up proposal automation (n8n workflow, API integrations, email templates)
- 4 hours: instrumenting negotiation tracking (events, attributes, funnels, sync)
- 2 hours: testing the workflow end-to-end
- 6 hours: monitoring first week, handling negotiations, updating CRM
- 2 hours: weekly check-ins and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal pipeline, negotiation attributes, activity logging | Standard stack (excluded) |
| PostHog | Event tracking, negotiation funnels, deal analytics | Standard stack (excluded) |
| n8n | Proposal automation, follow-up sequences, Attio/PostHog sync | Standard stack (excluded) |
| Anthropic Claude API | Deal term generation + comparison docs (automated) | ~$10-25/mo for 10-30 proposals — [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Instantly | Email delivery for comparison docs and follow-ups | Growth: $30/mo — [pricing](https://instantly.ai/pricing) |

**Play-specific cost:** ~$40-55/mo (Claude API + Instantly)

## Drills Referenced

- `multi-year-proposal-automation` — end-to-end automated flow from deal stage change to proposal delivery with follow-up sequences and response handlers
- `deal-negotiation-tracking` — full event instrumentation for the negotiation lifecycle: 7 events, CRM attributes, funnels, and bidirectional sync
