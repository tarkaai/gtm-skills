---
name: referral-program
description: Design, launch, and optimize a customer referral program with tracking and rewards
category: Product
tools:
  - PostHog
  - Loops
  - Intercom
  - Attio
fundamentals:
  - posthog-event-tracking
  - loops-transactional-emails
  - intercom-in-app-messages
  - attio-list-management
---

# Referral Program

This drill sets up a customer referral program from incentive design through launch and optimization. It leverages your happiest customers (identified via NPS or usage data) to drive low-cost, high-quality acquisition.

## Prerequisites

- Product with active, satisfied users (run `nps-feedback-loop` to identify promoters)
- PostHog tracking referral events
- Ability to offer referral incentives (credits, free months, features, or swag)

## Steps

### 1. Design the incentive structure

Choose a referral model that aligns with your product:

- **Two-sided reward**: Both referrer and referee get a benefit (most effective for consumer and prosumer products). Example: "Give a friend 1 month free, get 1 month free."
- **Referrer-only reward**: Credits, premium features, or swag for the referrer. Works for B2B where the referee benefits from the product itself.
- **Tiered rewards**: Escalating rewards as referral count grows (1 referral = sticker, 5 = t-shirt, 10 = free year). Creates gamification.

Keep the incentive simple to explain in one sentence. Complicated programs do not get shared.

### 2. Build the referral mechanism

Create unique referral links or codes per user. Track referral events in PostHog using `posthog-event-tracking`: link shared, link clicked, referee signed up, referee activated, reward unlocked. The tracking chain must be airtight — users will not refer if rewards are not reliably delivered.

### 3. Identify and activate referrers

Using the `attio-list-management` fundamental, pull your promoter list from NPS data and your most active users from PostHog. These are your seed referrers. Do not blast the referral program to everyone — start with users who already love the product. They will convert at higher rates and set social proof.

### 4. Prompt referrals at the right moment

Using `intercom-in-app-messages`, trigger referral prompts at moments of delight:

- After completing a successful workflow
- After a positive NPS response
- After reaching a usage milestone
- After their first month of active use

The prompt should be celebratory: "You've accomplished X — know someone who'd benefit too?"

### 5. Automate the reward fulfillment

Using `loops-transactional-emails`, send automated emails at each step: confirmation when someone uses their link, notification when the referee signs up, reward notification when the referee activates. Make the referrer feel appreciated at every stage. Include a running count of their referrals.

### 6. Measure and optimize

Track the referral funnel: invites sent, clicks, signups, activations, rewards issued. Calculate cost per acquisition via referral and compare to other channels. Benchmark: 10-15% of promoters should refer at least once. If referral rates are low, test the incentive, the prompt timing, or the ease of sharing. Feed high-value referrers into your customer advocacy list.
