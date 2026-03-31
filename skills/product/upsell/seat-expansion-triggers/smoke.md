---
name: seat-expansion-triggers-smoke
description: >
  Team Growth Upsell — Smoke Test. Detect when accounts show team growth
  signals and deliver one contextual seat expansion prompt. Validate that
  the prompt drives seat additions at >=35% rate in a small test group.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=35% of prompted accounts add seats"
kpis: ["Seat expansion rate", "Prompt acceptance rate", "Seats added per conversion"]
slug: "seat-expansion-triggers"
install: "npx gtm-skills add product/upsell/seat-expansion-triggers"
drills:
  - posthog-gtm-events
  - seat-growth-signal-detection
  - threshold-engine
---

# Team Growth Upsell — Smoke Test

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Prove that detecting team growth signals and delivering a contextual seat expansion prompt causes accounts to add seats at a higher rate than unprompted accounts. Pass threshold: >=35% of prompted accounts add at least one seat within 7 days of receiving the prompt.

## Leading Indicators

- Expansion signals are firing in PostHog (proves instrumentation works)
- At least 10 accounts score into the hot or warm tiers within the first 3 days
- Prompt impressions are logged (proves the delivery path works end-to-end)
- At least one account adds seats within 48 hours of receiving a prompt

## Instructions

### 1. Instrument team growth events in PostHog

Run the `posthog-gtm-events` drill to establish the event taxonomy. Then instrument these specific events in your product:

- `team_invite_sent` — fires when a user sends a team invitation
- `team_invite_failed` — fires when an invitation is blocked by seat limit
- `seat_limit_hit` — fires when a user attempts an action blocked by seat count
- `admin_viewed_billing` — fires when an admin visits the billing/seats page
- `seats_added` — fires when seats are actually purchased/added

Each event must include: `account_id`, `user_id`, `current_seat_count`, `seat_limit`, `seats_remaining`.

**Human action required:** A developer must add these tracking calls to the product codebase. Provide them the exact event names, properties, and trigger points. Verify events appear in PostHog Live Events within 24 hours.

### 2. Identify expansion-ready accounts manually

Run the `seat-growth-signal-detection` drill at minimum scale: instead of building the full automated scoring system, run the HogQL query from Step 2 of the drill manually via the PostHog API or MCP. Pull the list of accounts with expansion signals in the last 7 days.

Select 10-20 accounts from the hot tier (score >= 40) as the test group. These are accounts actively hitting seat limits or sending invitations.

### 3. Deliver one contextual prompt per account

For each test account, deliver a single expansion prompt manually:

- If the top signal is `team_invite_failed` or `seat_limit_hit`: send an in-app message via Intercom API referencing the blocked action. Copy: "Your team has reached its {{seatLimit}}-seat limit. Add more seats to bring your colleagues on board." CTA: direct link to seat purchase page.
- If the top signal is `team_invite_sent` or `admin_viewed_billing`: send a transactional email via Loops API. Subject: "Your {{productName}} team is growing." Body: reference their current seat usage, explain what additional seats unlock, include a one-click add-seats link.

Log each prompt delivery as a `seat_expansion_prompt_shown` event in PostHog with: `account_id`, `channel` (in_app or email), `prompt_type` (the triggering signal), `expansion_tier`.

### 4. Measure against threshold

Run the `threshold-engine` drill after 7 days. Pull the conversion data:

- How many of the 10-20 prompted accounts added seats?
- What was the conversion rate (seats_added / prompts_shown)?
- How many seats were added per converting account?
- What was the time from prompt to seat addition?

**Pass: >=35% of prompted accounts added seats.** If pass, document which signal types and channels converted best. Proceed to Baseline.

**Fail:** Diagnose — were the signals accurate (did flagged accounts actually need more seats)? Was the prompt copy clear? Was the add-seats flow frictionless? Fix the weakest link and re-run with 10-20 fresh accounts.

## Time Estimate

- 2 hours: instrument PostHog events and verify they fire
- 1 hour: run the signal detection query and select test accounts
- 1 hour: deliver prompts and configure tracking
- 1 hour: pull results after 7 days and evaluate

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, signal detection queries, funnel measurement | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app expansion prompts | From $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Transactional expansion emails | Free up to 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

**Play-specific cost:** Free (within free tiers at Smoke scale)

## Drills Referenced

- `posthog-gtm-events` — establish the event taxonomy and instrument team growth events
- `seat-growth-signal-detection` — identify which accounts are ready for seat expansion (run manually at Smoke)
- `threshold-engine` — measure conversion rate against the >=35% pass threshold
