---
name: referral-program-smoke
description: >
  Incentivized Referral Program — Smoke Test. Design a two-sided referral incentive,
  deploy it to your top 20-50 users, and measure whether any signal of organic referral
  behavior exists before investing in automation.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=3 referral links shared AND >=1 referee signs up"
kpis: ["Referral links shared", "Referral link click-through rate", "Referee signups", "Referee activation rate"]
slug: "referral-program"
install: "npx gtm-skills add product/referrals/referral-program"
drills:
  - referral-program
  - posthog-gtm-events
  - threshold-engine
---

# Incentivized Referral Program — Smoke Test

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

At least 3 users share their referral link and at least 1 referee creates an account. This proves that (a) users are willing to refer and (b) the referral mechanic actually produces signups. No automation, no always-on. A single manual run to validate signal.

## Leading Indicators

- Referral prompt open rate >50% (users are seeing the ask)
- At least 10% of prompted users click "share" or copy their referral link
- At least 1 referral link gets clicked by someone other than the referrer
- At least 1 referee begins the signup flow

## Instructions

### 1. Design the referral incentive and mechanism

Run the `referral-program` drill. Focus on steps 1-2: choose a two-sided reward structure (both referrer and referee get a benefit) and build unique referral links per user. Keep the incentive explainable in one sentence. Example: "Give a friend 1 month free, get 1 month free."

**Human action required:** Decide the specific reward. Ensure the reward can be fulfilled manually for this test (no automated reward pipeline needed yet). Approve the referral landing page copy before launch.

### 2. Instrument referral event tracking

Run the `posthog-gtm-events` drill to set up the referral event taxonomy in PostHog. Define and implement these events:

- `referral_link_generated` -- user's unique link is created
- `referral_link_shared` -- user copies or clicks share on their link (properties: `surface`, `share_method`)
- `referral_link_clicked` -- someone visits the referral link (properties: `referrer_id`)
- `referral_signup_started` -- referee begins registration via referral link
- `referral_signup_completed` -- referee creates account via referral link
- `referral_activation_reached` -- referee hits activation milestone
- `referral_reward_issued` -- reward delivered to referrer and/or referee

This event schema persists across all 4 levels. Get it right now.

### 3. Identify and prompt your seed referrers

Run step 3 of the `referral-program` drill. Pull your top 20-50 users by usage data from PostHog (highest session frequency and feature breadth in the last 30 days). Cross-reference with any NPS data: users who scored 9-10 are ideal.

Send each seed referrer a personal Intercom in-app message or Loops email with:
- What the referral program is
- What they and their friend get
- Their unique referral link
- A one-click share button

Do not blast the entire user base. Seed referrers only.

### 4. Observe behavior for 7 days

Monitor PostHog daily for the referral events. Note:
- How many of the 20-50 prompted users shared their link
- How many clicks those links received
- Whether any referee started or completed signup
- Any qualitative feedback (replies to the referral prompt, support tickets, etc.)

### 5. Evaluate against threshold

Run the `threshold-engine` drill. Pass criteria: >=3 referral links shared AND >=1 referee signs up.

- **Pass:** Referral behavior exists. Proceed to Baseline to automate and scale.
- **Marginal pass:** 1-2 links shared but a signup happened. The mechanic works but the prompt needs improvement. Iterate on the referral ask and re-test with a fresh batch of 20-50 users.
- **Fail:** Zero links shared or zero clicks. Diagnose: was the incentive unappealing, was the prompt buried, or was the audience wrong? Redesign the incentive or change the prompt timing and re-run.

## Time Estimate

- 2 hours: incentive design, referral link setup, PostHog event instrumentation
- 1 hour: seed referrer identification and prompt creation
- 1 hour: send prompts and verify events are firing correctly
- 2 hours: daily monitoring over 7 days (15-20 min/day) + threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnel analysis, user identification | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app referral prompt to seed referrers | From $29/seat/mo; Early Stage program up to 90% off ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email referral prompt as backup channel | Free up to 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | Store referrer and referee records | Free up to 3 users ([attio.com](https://attio.com)) |

**Estimated play-specific cost at this level:** $0 (free tiers sufficient for 20-50 user test)

## Drills Referenced

- `referral-program` -- designs incentive structure, builds referral links, identifies seed referrers, crafts referral prompts
- `posthog-gtm-events` -- defines and implements the referral event taxonomy used across all levels
- `threshold-engine` -- evaluates pass/fail against the >=3 shared, >=1 signup threshold
