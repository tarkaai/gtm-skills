---
name: power-user-program-smoke
description: >
  Power User Program — Smoke Test. Build a power user scoring model from product
  usage data, identify your top 10% of users, and manually validate that at least
  2 take a concrete advocacy action (testimonial, referral, or review).
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=2 of the top 10 scored users complete an advocacy action within 7 days of personal outreach"
kpis: ["Power user score distribution", "Top-10 identification accuracy", "First advocacy action conversion rate"]
slug: "power-user-program"
install: "npx gtm-skills add product/referrals/power-user-program"
drills:
  - power-user-scoring
  - threshold-engine
---

# Power User Program — Smoke Test

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Identify the top 10% of users by composite power user score and validate that at least 2 of the top 10 take a concrete advocacy action (submit a testimonial, refer a colleague, or leave a public review) within 7 days of personal outreach. This proves that your usage data can reliably surface users with advocacy potential.

## Leading Indicators

- Power user scoring model produces a non-uniform distribution (top users clearly separate from the median)
- Manual review of the top 10 confirms they are genuinely high-value users (you recognize them, they use advanced features, they have been around a while)
- At least 5 of 10 respond to the personal outreach (signals willingness to engage)
- At least 3 of 10 express positive sentiment about the product in their response

## Instructions

### 1. Build the power user scoring model

Run the `power-user-scoring` drill to create the composite scoring system:

- Query PostHog for the 5 scoring dimensions: usage depth, tenure and consistency, collaboration signal, expansion signal, sentiment signal
- Weight the dimensions: depth 30%, tenure 20%, collaboration 20%, expansion 15%, sentiment 15%
- Compute scores for all active users (active in last 30 days)
- Create the 4 cohorts in PostHog: Champions (>=80), Power Users (60-79), Rising Stars (40-59), Standard (<40)
- Sync the top 10 scored users to an Attio list: "Power User Smoke Test Candidates"

**Important:** At Smoke level, do not automate the scoring pipeline. Run it once manually via PostHog queries and Claude analysis of the results. The goal is to validate the model, not to operationalize it.

### 2. Manually validate the top 10

Review each of the top 10 scored users in PostHog and Attio:

- Do they use advanced features? (Check PostHog session recordings or event history)
- Have they been consistently active? (Check weekly session counts over last 3 months)
- Have they collaborated? (Check team invites, shared assets)
- Do they have positive support interactions? (Check Intercom conversation history)
- Would you want this person representing your product publicly?

If more than 3 of the top 10 do not pass manual validation, the scoring model needs recalibration. Adjust dimension weights and re-run. Document what you changed and why.

**Human action required:** Review the scored list and validate each user. This cannot be automated at Smoke level because you need to build intuition about what a "good" power user looks like for your product.

### 3. Send personal outreach to validated users

For each validated power user, send a personal email (not automated, not templated) from a real person on the team:

- Acknowledge their specific usage: "I noticed you've been building [specific thing] with [feature] — impressive work."
- Make a specific ask: choose the easiest advocacy action for each user based on their profile:
  - Users on social media: "Would you share a quick tweet about how you use [product]?"
  - Users who wrote detailed support tickets: "Would you turn that into a 2-paragraph testimonial we could feature?"
  - Users with large teams: "Know a colleague at another company who'd benefit? I'd love to offer them a free trial."
- Keep it short. One ask per email. Make the ask as frictionless as possible (provide a template, a one-click referral link, or a pre-written tweet they can edit).

**Human action required:** Write and send 10 personal emails. Track responses in Attio.

### 4. Track responses and evaluate

Over 7 days, log every response and every advocacy action in Attio:

- Response received (yes/no, sentiment, what they said)
- Advocacy action completed (testimonial submitted, referral sent, review posted)
- Decline or no response (note the reason if given)

Run the `threshold-engine` drill to evaluate:

- **Pass threshold**: >=2 of the top 10 complete an advocacy action
- If PASS: the scoring model identifies users with real advocacy potential. Proceed to Baseline.
- If FAIL but >=5 responded positively: the model is good but the ask needs work. Iterate on the outreach approach and re-run.
- If FAIL and <5 responded: the model may be surfacing the wrong users. Recalibrate scoring weights and re-run.

## Time Estimate

- 2 hours: build and run the scoring model (PostHog queries + cohort creation)
- 1 hour: manual validation of top 10 users
- 1 hour: write and send 10 personal outreach emails
- 1 hour: 7-day tracking and final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage data queries, cohort creation, scoring computation | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Store scored users, track outreach and responses | Free tier: 3 seats ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** Free (within free tiers for a manual run of 10 users)

## Drills Referenced

- `power-user-scoring` — builds the composite scoring model from PostHog usage data and syncs scored users to Attio
- `threshold-engine` — evaluates the pass/fail threshold and recommends next action
