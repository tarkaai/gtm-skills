---
name: usage-limit-sales-upsell-baseline
description: >
  Usage-Based Upsell — Baseline Run. Always-on detection and qualification pipeline
  that surfaces expansion-ready accounts daily, triggers a 4-touch outreach sequence,
  and maintains a live expansion pipeline in Attio over 2 weeks.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email, Direct"
level: "Baseline Run"
time: "22 hours over 2 weeks"
outcome: ">=30% meeting booking rate from qualified accounts and expansion ARR >=10% of base ARR over 2 weeks"
kpis: ["Meeting booking rate from qualified accounts", "Expansion close rate", "Expansion ARR", "Median days from signal to close", "Outreach response rate"]
slug: "usage-limit-sales-upsell"
install: "npx gtm-skills add product/upsell/usage-limit-sales-upsell"
drills:
  - usage-threshold-detection
  - expansion-signal-qualification
  - expansion-outreach-sequence
  - posthog-gtm-events
---

# Usage-Based Upsell — Baseline Run

> **Stage:** Product -> Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Direct

## Outcomes

The first always-on version. A daily detection pipeline identifies accounts near limits, an automated qualification step filters for sales-worthy opportunities, and a multi-touch outreach sequence engages decision-makers with personalized usage data. The system runs continuously for 2 weeks. Results must sustain — not just a one-shot spike from Smoke.

## Leading Indicators

- Detection pipeline runs daily without errors for 14 consecutive days
- Pipeline surfaces at least 5 new qualified accounts per week (sufficient volume)
- Touch 1 email open rate exceeds 50% (the subject line and sender identity resonate)
- Touch 1 reply rate exceeds 15% (the usage data framing is compelling)
- At least 3 expansion meetings booked in the first 2 weeks
- No negative feedback or unsubscribe requests from outreach (the outreach feels helpful)

## Instructions

### 1. Deploy the detection pipeline

Run the `usage-threshold-detection` drill in full automated mode:

1. Configure the plan cap mapping (resource limits per tier) as a JSON config in n8n
2. Build the daily detection workflow in n8n that queries PostHog for accounts at 70%+ of any limit
3. Implement the consumption velocity calculation to project when each account will hit the limit
4. Set up PostHog cohorts: `usage-approaching`, `usage-imminent`, `usage-critical`
5. Configure Attio custom attributes for threshold data storage
6. Activate the daily cron schedule (06:00 UTC)

Verify the pipeline works by comparing first daily run output against your manual Smoke test analysis. Confirm at least 80% overlap — the automated detection should find the same accounts you found manually.

### 2. Deploy automated qualification

Run the `expansion-signal-qualification` drill with automation:

1. Build an n8n workflow that receives the daily detection webhook
2. For each flagged account, pull CRM context from Attio: MRR, plan tier, signup date, support history, existing deals
3. Apply the qualification gates automatically: MRR >= $100, active >= 30 days, no active expansion deal, no critical tickets
4. Compute the expansion qualification score using the signal-based criteria
5. Route Tier 1 (sales-ready, score >= 60) accounts to the outreach sequence
6. Route Tier 2 (watch list, score 30-59) to an Attio list for manual review
7. Log all disqualifications with reasons

**Human action required:** Review the first week's qualification output. Verify the automated scoring is producing reasonable results by spot-checking 5 qualified and 5 disqualified accounts. Adjust scoring thresholds if needed.

### 3. Deploy the outreach sequence

Run the `expansion-outreach-sequence` drill in full automated mode:

1. Create the 4 email templates in Loops with personalization variables: account name, resource name, current count, plan limit, pct used, projected hit date, next tier name, account owner name
2. Build the n8n orchestration workflow: Touch 1 on Day 0, Touch 2 on Day 3 (skip if reply), Touch 3 on Day 7 (skip if reply or meeting), Touch 4 on Day 14 (skip if any engagement)
3. Configure stop conditions: reply detected, meeting booked, self-serve upgrade, deal stage change
4. Create the Cal.com expansion event type linked to Attio deals
5. Set up the in-app message in Intercom for Touch 4
6. Enable full touch logging in Attio per expansion deal

Each outreach email must be sent from the account owner's email address (or founder if no owner). Configure Loops sender identity accordingly. These are sales emails, not marketing emails — reply-to must work.

### 4. Configure event tracking

Run the `posthog-gtm-events` drill to instrument the expansion funnel:

- `expansion_score_computed` — when qualification scores an account
- `expansion_deal_created` — when an expansion deal is opened in Attio
- `expansion_outreach_sent` — when each outreach touch fires
- `expansion_outreach_opened` — email open tracked
- `expansion_outreach_replied` — reply detected
- `expansion_meeting_booked` — Cal.com booking confirmed
- `expansion_deal_closed` — upgrade completed
- `expansion_deal_lost` — deal marked lost with reason

Build a PostHog funnel: `scored -> deal_created -> outreach_sent -> meeting_booked -> deal_closed`. Break down by resource type, MRR band, and outreach touch number.

### 5. Run the pipeline for 2 weeks

Let the full pipeline run for 14 days. Monitor daily for the first week:

- Did detection run? Check n8n execution logs
- How many accounts were detected? Check PostHog cohort sizes
- How many passed qualification? Check Attio "Expansion Pipeline" list
- Did outreach fire correctly? Check Loops delivery reports
- Any replies? Check Loops webhooks and Attio deal activity
- Any meetings booked? Check Cal.com bookings
- Any negative responses? Check Intercom conversations and email replies

Fix pipeline issues immediately. A broken detection pipeline means missed expansion opportunities.

### 6. Manage expansion conversations

**Human action required:** The outreach sequence drives meetings, but the expansion conversation itself is human-led at Baseline. For each meeting:

1. Review the Attio deal context: usage data, signal history, qualification score, outreach history
2. Lead with the customer's growth: "Your usage of {{resource}} tells me your team is getting real value"
3. Present options: next tier, annual commitment, custom bundle
4. Log the outcome in Attio: closed (ARR, new tier), objection (specific reason), deferred (follow-up date)

### 7. Evaluate against threshold

After 2 weeks, measure against the pass threshold: at least 30% meeting booking rate from qualified accounts AND expansion ARR from closed deals is at least 10% of those accounts' base ARR.

Also evaluate:

- Total accounts detected vs. qualified vs. reached (funnel efficiency)
- Meeting booking rate by touch number (which touch drives the most bookings?)
- Close rate from meetings (sales conversation effectiveness)
- Expansion ARR per closed deal (deal size)
- Response sentiment (positive vs. neutral vs. negative — are we annoying anyone?)
- Self-serve conversions during outreach (some accounts may upgrade on their own after Touch 1)
- Pipeline velocity: median days from signal detection to deal close
- Which resource types produce the highest close rate?

If PASS, proceed to Scalable. If FAIL, diagnose the funnel: detection working but qualification too strict (not enough qualified accounts), qualified but outreach not converting (copy or timing problem), meetings but not closing (pricing or value gap). Fix the weakest stage and re-run.

## Time Estimate

- 4 hours: deploy detection pipeline (n8n workflow, PostHog queries, Attio config)
- 4 hours: deploy automated qualification (n8n scoring workflow, Attio integration)
- 4 hours: deploy outreach sequence (Loops templates, n8n orchestration, Cal.com setup, Intercom message)
- 2 hours: configure PostHog event tracking and build funnel
- 4 hours: daily monitoring and managing expansion conversations over 2 weeks
- 4 hours: evaluation, analysis, and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage detection, cohorts, funnel tracking, event analytics | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — expansion deals, qualification, pipeline management | Free up to 3 seats; from $29/seat/mo — [attio.com/pricing](https://attio.com/pricing) |
| Loops | Outreach email sequence (4 templates + personalization) | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Detection scheduling, qualification automation, outreach orchestration | Free self-hosted; Cloud from EUR 24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Intercom | In-app message for Touch 4 | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Cal.com | Expansion meeting booking | Free for individuals; Team from $12/user/mo — [cal.com/pricing](https://cal.com/pricing) |

**Estimated play-specific cost: $80-150/mo** (Loops emails + n8n workflows; PostHog, Attio, Intercom likely already in stack)

## Drills Referenced

- `usage-threshold-detection` — daily pipeline identifying accounts approaching limits, classifying urgency tiers, storing data in Attio
- `expansion-signal-qualification` — automated qualification scoring to filter detected accounts into sales-ready opportunities
- `expansion-outreach-sequence` — 4-touch personalized outreach cadence with stop conditions and CRM logging
- `posthog-gtm-events` — configures the event tracking and funnel measuring the full expansion pipeline
