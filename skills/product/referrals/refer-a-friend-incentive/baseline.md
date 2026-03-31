---
name: refer-a-friend-incentive-baseline
description: >
  Referral Rewards Program — Baseline Run. Automate referral link distribution,
  reward fulfillment, and funnel tracking. Run always-on for 2 weeks and validate
  >=12% referral share rate and >=35% referred-user activation rate.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=12% referral share rate AND >=35% referred-user activation rate"
kpis: ["Referral share rate", "Share-to-signup conversion", "Signup-to-activation conversion", "Reward fulfillment rate", "Reward cost per activated referral"]
slug: "refer-a-friend-incentive"
install: "npx gtm-skills add product/referrals/refer-a-friend-incentive"
drills:
  - posthog-gtm-events
  - referral-fulfillment-automation
  - threshold-engine
---

# Referral Rewards Program — Baseline Run

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Automate the full referral lifecycle: link generation, prompt delivery at moments of delight, funnel tracking, reward fulfillment, and milestone notifications. Run always-on for 2 weeks targeting all eligible users (not just the seed group). Validate that >=12% of eligible users share their referral link and >=35% of referred signups activate.

## Leading Indicators

- Referral prompt delivery rate >90% (Intercom messages reaching eligible users)
- Loops referral sequence open rate >40%
- Referral link copy/share events growing day over day for the first 5 days
- At least 10 referral link clicks in the first 3 days
- Reward fulfillment workflow fires successfully on first referral activation (no errors)
- Referred users are reaching the activation milestone within 7 days at a rate comparable to organic users

## Instructions

### 1. Instrument the referral event taxonomy

Run the `posthog-gtm-events` drill to set up the full event taxonomy for the referral program:

- `referral_link_generated` — unique link created for a user
- `referral_prompt_shown` — in-app or email referral prompt delivered
- `referral_link_shared` — user copied or shared their link (with `share_channel` property: email, social, copy, dm)
- `referral_link_clicked` — someone clicked a referral link
- `referral_signup` — new user signed up via referral link
- `referral_activated` — referred user hit the activation milestone
- `referral_reward_issued` — reward applied to referrer and/or referee account

Build the PostHog funnel: `referral_prompt_shown` -> `referral_link_shared` -> `referral_link_clicked` -> `referral_signup` -> `referral_activated` -> `referral_reward_issued`. Save as "Referral Rewards — Baseline Funnel."

Create PostHog cohorts:
- "Referral Eligible" — active users, past activation milestone, 30+ days tenure
- "Active Referrers" — users who shared their referral link in the last 14 days
- "Referred Users" — users who signed up via a referral link

### 2. Automate the referral lifecycle

Run the `referral-fulfillment-automation` drill to build the always-on referral pipeline:

- **Link generation**: n8n workflow generates unique referral codes for all eligible users and stores them in Attio
- **Prompt delivery**: Intercom in-app messages trigger at moments of delight (successful workflow completion, NPS 9-10 response, usage milestone). Loops 3-email sequence enrolls promoters with their referral link.
- **Funnel tracking**: all 7 referral events tracked in PostHog with full attribution chain (referrer_id on every event)
- **Reward fulfillment**: n8n workflow triggered by `referral_activated` verifies the referral, applies the reward via product API, updates Attio, and sends notifications
- **Fraud prevention**: duplicate detection, self-referral blocking, velocity limits (max 10/day per user)

**Human action required:** Verify the reward fulfillment API works correctly by testing with 2-3 manual referrals before going live. Confirm rewards appear in the referrer's account within 24 hours.

### 3. Launch to all eligible users

Roll out the referral program to all eligible users (the "Referral Eligible" PostHog cohort). Do not use a feature flag split at Baseline — the Smoke test already validated the incentive works. The Baseline test validates that the automation works at larger scale.

Monitor the first 48 hours closely:
- Check n8n workflow execution logs for errors
- Verify Intercom prompt delivery rates
- Confirm at least 5 referral links were shared in the first 48 hours
- Verify the first reward fulfillment fires correctly

### 4. Evaluate against threshold

Run the `threshold-engine` drill after 2 weeks:

- **Primary threshold**: >=12% of eligible users shared their referral link
- **Secondary threshold**: >=35% of referred signups activated
- **Guardrail**: reward cost per activated referral is less than the cost of acquiring a user through your next-best channel
- If PASS on all: automation works reliably. Proceed to Scalable.
- If primary PASS but secondary FAIL: referrals are coming in but not converting. Analyze the referee onboarding flow — are referred users seeing their reward context? Is the activation milestone clear?
- If primary FAIL: the automated prompts are less effective than personal outreach. Analyze prompt timing, copy, and channel. Test a different moment of delight or a stronger CTA.

Document: funnel conversion rates at each stage, most effective share channel, average time from referral to activation, reward fulfillment success rate.

## Time Estimate

- 4 hours: instrument referral event taxonomy and build PostHog funnels/cohorts
- 6 hours: build referral fulfillment automation (n8n workflows, Intercom prompts, Loops sequences)
- 2 hours: test the automation end-to-end with manual referrals
- 2 hours: launch monitoring (first 48h) and 2-week threshold evaluation
- 2 hours: analysis and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Referral funnel tracking, cohorts, feature flags | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Referral email sequences, transactional notifications | Free up to 1,000 contacts; $49/mo for up to 5,000 ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app referral prompts at moments of delight | Essential: $29/seat/mo annual ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Attio | Store referral codes, track referrer lists | Free tier: 3 seats ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** $30-80/mo (Loops free or $49/mo if >1,000 contacts; Intercom $29/seat/mo if not already on standard stack)

## Drills Referenced

- `posthog-gtm-events` — defines and instruments the referral event taxonomy and PostHog funnels
- `referral-fulfillment-automation` — automates link generation, prompt delivery, reward fulfillment, fraud prevention, and milestone notifications
- `threshold-engine` — evaluates the pass/fail threshold and recommends next action
