---
name: seat-expansion-triggers-baseline
description: >
  Team Growth Upsell — Baseline Run. Automate seat growth signal detection
  and contextual prompt delivery as an always-on system. Validate >=45%
  expansion rate holds over 2 weeks with 50+ prompted accounts.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=45% of prompted accounts add seats over 2 weeks"
kpis: ["Seat expansion rate", "Prompt acceptance rate", "Seats added per conversion", "Time from signal to expansion"]
slug: "seat-expansion-triggers"
install: "npx gtm-skills add product/upsell/seat-expansion-triggers"
drills:
  - seat-growth-signal-detection
  - seat-expansion-prompt-delivery
  - threshold-engine
---

# Team Growth Upsell — Baseline Run

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Turn the Smoke test into an always-on automated system. The signal detection runs every 6 hours, prompt delivery fires automatically when accounts enter the hot tier, and the full funnel is tracked end-to-end. Pass threshold: >=45% of prompted accounts add seats, sustained over a 2-week period with 50+ accounts prompted.

## Leading Indicators

- Signal detection workflow runs on schedule without errors for 3+ consecutive days
- Prompt delivery fires within 1 hour of an account entering the hot tier
- In-app prompts achieve >=30% click-through rate
- Email prompts achieve >=15% click-through rate
- At least 5 accounts add seats in the first week

## Instructions

### 1. Deploy automated signal detection

Run the `seat-growth-signal-detection` drill fully — build the complete n8n workflow that runs every 6 hours:

1. Configure the n8n cron trigger for every 6 hours
2. Add the HogQL query node that scores all accounts against the expansion model
3. Add the tier classification logic (hot >= 40, warm 20-39, watch 15-19)
4. Add the Attio update nodes that write `seat_expansion_score`, `seat_expansion_tier`, `current_seat_count`, `seat_utilization_pct` to each account record
5. Add the webhook trigger node that fires for accounts entering the hot tier
6. Test end-to-end: manually create a test event in PostHog, verify the workflow picks it up on the next run, verify Attio is updated, verify the webhook fires

**Human action required:** Verify the n8n workflow runs successfully for 24 hours before connecting prompt delivery. Check the n8n execution log for errors.

### 2. Deploy automated prompt delivery

Run the `seat-expansion-prompt-delivery` drill fully — build the n8n workflow that receives the webhook from signal detection and delivers contextual prompts:

1. Configure the n8n webhook receiver
2. Add the Attio enrichment node (pull account plan, MRR, previous prompt history)
3. Add the cooldown check (skip if last prompt was within 14 days)
4. Add the routing logic (hot tier: in-app + email for self-serve, add sales deal for high-MRR)
5. Add the Intercom message nodes with the 4 contextual message templates from the drill
6. Add the Loops transactional email nodes with the 3 email templates from the drill
7. Add PostHog event logging for every prompt delivered
8. Test end-to-end: trigger a fake hot-tier webhook, verify the prompt is delivered via the correct channel, verify the PostHog event fires

### 3. Configure the expansion funnel in PostHog

Build a PostHog funnel insight tracking the full path:

1. `seat_expansion_signal_detected` — account shows growth signals
2. `seat_expansion_prompt_shown` — prompt delivered via any channel
3. `seat_expansion_prompt_clicked` — user engaged with the prompt
4. `seats_added` — seats were purchased

Break down by `expansion_tier` and `channel` to identify which signals and delivery channels convert best.

Create a PostHog cohort "Expansion Prompted — No Action" for accounts that received a prompt 7+ days ago but have not added seats. This cohort feeds into the Loops follow-up sequence.

### 4. Launch the 2-email follow-up sequence

Configure the Loops sequence from the `seat-expansion-prompt-delivery` drill:
- Day 0: The initial signal-specific prompt (already sent by the main workflow)
- Day 5: Follow-up for non-converters: "Still thinking about adding seats? Here's how other teams your size use {{productName}}" with social proof and a direct add-seats link

### 5. Evaluate against threshold

Run the `threshold-engine` drill after 2 weeks. Pull the conversion data across all prompted accounts:

- Total accounts prompted: target 50+
- Conversion rate (accounts that added seats / accounts prompted)
- Conversion rate by channel (in-app vs email)
- Conversion rate by signal type (which signals predict expansion best?)
- Average seats added per converting account
- Median time from prompt to seat addition
- Revenue impact: total additional MRR from seat additions

**Pass: >=45% of prompted accounts added seats.** Document the top-performing signal types, channels, and prompt templates. Proceed to Scalable.

**Fail:** If conversion < 45% but signal detection is accurate (hot-tier accounts actually need more seats), the issue is in the prompt. A/B test prompt copy, CTA placement, or timing. If signal detection is inaccurate (hot-tier accounts do not actually need seats), recalibrate the scoring weights. Re-run for another 2-week cycle.

## Time Estimate

- 4 hours: build and test the signal detection n8n workflow
- 4 hours: build and test the prompt delivery n8n workflow
- 2 hours: configure PostHog funnels, cohorts, and the Loops follow-up sequence
- 2 hours: monitor the first week, fix delivery issues
- 4 hours: pull results after 2 weeks, analyze by segment, evaluate threshold

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, signal detection queries, funnel analysis | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Workflow automation for signal detection and prompt delivery | Self-hosted: free; Cloud: from EUR20/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | In-app contextual expansion prompts | From $29/seat/mo; Proactive Support add-on $349/mo for outbound ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Transactional expansion emails and follow-up sequences | Free up to 1,000 contacts; $49/mo for 5,000 ([loops.so/pricing](https://loops.so/pricing)) |

**Play-specific cost:** ~$50-100/mo (Loops paid plan + n8n cloud if not self-hosted)

## Drills Referenced

- `seat-growth-signal-detection` — automated detection of team growth signals, running every 6 hours
- `seat-expansion-prompt-delivery` — contextual prompt routing and delivery via in-app, email, and sales channels
- `threshold-engine` — measure conversion rate against the >=45% pass threshold
