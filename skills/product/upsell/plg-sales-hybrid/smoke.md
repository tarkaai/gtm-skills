---
name: plg-sales-hybrid-smoke
description: >
  PLG + Sales-Assist Model — Smoke Test. Instrument product usage signals, build a
  minimal lead capture surface for sales handoff, and validate that at least 10% of
  flagged accounts accept a sales conversation.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Direct"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=10% of flagged accounts accept sales handoff"
kpis: ["Sales-assist accept rate", "PQL signal volume", "Time from signal to handoff"]
slug: "plg-sales-hybrid"
install: "npx gtm-skills add product/upsell/plg-sales-hybrid"
drills:
  - usage-threshold-detection
  - lead-capture-surface-setup
  - threshold-engine
---

# PLG + Sales-Assist Model — Smoke Test

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Direct

## Outcomes

Prove that in-product usage signals can identify accounts ready for a sales conversation, and that a minimal capture surface converts at least 10% of those accounts into accepted handoffs. No automation, no always-on. Agent prepares, human reviews and launches.

## Leading Indicators

- PQL signals firing for at least 5 distinct accounts within the test window
- At least 3 accounts view the lead capture surface after a signal fires
- At least 1 account books or accepts a sales conversation within 3 days of the signal

## Instructions

### 1. Detect accounts approaching plan limits

Run the `usage-threshold-detection` drill. Configure detection for your top 2 metered resources (seats and one other -- API calls, projects, or storage). Set the threshold at 80% consumed. Target a test cohort of 10-20 active accounts on free or starter plans. The drill outputs a list of accounts with urgency tiers (approaching, imminent, critical) stored in Attio.

**Human action required:** Review the detected accounts. Confirm the plan limit data is accurate. Remove any test accounts or internal accounts from the list.

### 2. Build a minimal lead capture surface

Run the `lead-capture-surface-setup` drill. Choose the chat widget surface type (Intercom bot). Configure it to appear only for accounts flagged by the usage threshold detection -- use a PostHog cohort to target the prompt. The bot flow:

1. Trigger: user is in the `usage-imminent` or `usage-critical` PostHog cohort
2. Message: "Looks like your team is growing. Want to explore options for scaling your plan?"
3. If yes: collect their preferred time and route to a Cal.com booking link for a 20-minute call
4. If no: dismiss and log the response

Wire the PostHog events: `plg_capture_shown`, `plg_capture_accepted`, `plg_capture_dismissed`. Route accepted leads to Attio as deals at the "Meeting Requested" stage.

**Human action required:** Review the bot copy and flow before enabling. Test it yourself by triggering the cohort conditions on a test account. Verify the Cal.com link works and the Attio deal gets created.

### 3. Launch and observe for 7 days

Enable the Intercom bot for the flagged cohort. Do not expand beyond the initial 10-20 accounts. Monitor daily in PostHog: how many see the prompt, how many engage, how many accept the handoff.

### 4. Evaluate against threshold

Run the `threshold-engine` drill. Measure: of accounts that saw the lead capture surface, what percentage accepted the sales handoff (booked a call or replied affirmatively)?

- **Pass (>=10% accept rate):** The signal-to-handoff pipeline works. Document which signals drove the most handoffs. Proceed to Baseline.
- **Fail (<10%):** Diagnose: are the wrong accounts being flagged (signal quality), is the prompt copy ineffective (surface quality), or is the timing wrong (users not in buying mode when prompted)? Fix the weakest link and re-run.

## Time Estimate

- 1.5 hours: configure usage threshold detection and verify data accuracy
- 1.5 hours: build the Intercom bot and wire PostHog events + Attio routing
- 0.5 hours: human review and testing
- 1.5 hours: 7-day monitoring and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage tracking, cohorts, event capture | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app chat bot for lead capture | Essential: $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Attio | CRM deal creation for handoff tracking | Standard stack (excluded from play budget) |
| Cal.com | Booking link for sales calls | Free tier available ([cal.com/pricing](https://cal.com/pricing)) |

**Play-specific cost:** Free (within existing Intercom seat and PostHog free tier)

## Drills Referenced

- `usage-threshold-detection` -- detect accounts approaching plan limits and classify urgency
- `lead-capture-surface-setup` -- build the in-product chat widget that captures sales handoff interest
- `threshold-engine` -- evaluate the 10% accept rate pass/fail threshold
