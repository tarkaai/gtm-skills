---
name: community-champions-smoke
description: >
  Champion Recognition Program — Smoke Test. Build a community champion scoring
  model from Slack/Discord/forum contribution data, identify your top 10 community
  helpers, and manually validate that at least 3 generate a referral within 7 days
  of personal recognition outreach.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email, Social"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=3 of top 10 scored community champions generate a referral within 7 days of personal recognition outreach"
kpis: ["Champion score distribution", "Top-10 identification accuracy", "Referral conversion from recognition outreach"]
slug: "community-champions"
install: "npx gtm-skills add product/referrals/community-champions"
drills:
  - threshold-engine
---

# Champion Recognition Program — Smoke Test

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Social

## Outcomes

Identify the top 10 community contributors by composite champion score (helpfulness, content creation, consistency, reach, product expertise) and validate that at least 3 generate a referral (share a referral link, introduce a colleague, or recommend the product publicly) within 7 days of personal recognition outreach. This proves that community contribution data can reliably surface users with referral potential, and that recognition motivates sharing.

## Leading Indicators

- Champion scoring model produces a non-uniform distribution (top contributors clearly separate from average community members)
- Manual review of the top 10 confirms they are genuinely helpful members (you recognize their names, they answer questions, they share resources)
- At least 6 of 10 respond to the personal recognition outreach (signals the community relationship is real)
- At least 4 of 10 express willingness to help promote the product even if they have not yet referred

## Instructions

### 1. Build the community champion scoring model

Run the the champion identification scoring workflow (see instructions below) drill to create the composite scoring system:

- Extract community data from Slack, Discord, or forum channels for the trailing 30 days: messages sent, threads participated in, questions answered, reactions received, unique users interacted with
- Weight the 5 scoring dimensions: helpfulness 35%, content creation 25%, consistency 20%, community reach 10%, product expertise 10%
- Compute scores for all community members with at least 3 messages in the last 30 days
- Create the 4 cohorts in PostHog: Champions (>=75), Strong Contributors (50-74), Active Members (25-49), Lurkers (<25)
- Sync the top 10 scored members to an Attio list: "Champion Smoke Test Candidates"

**Important:** At Smoke level, do not automate the scoring pipeline. Run it once manually via API queries and Claude analysis of the results. The goal is to validate the scoring model, not to operationalize it. Pull Slack/Discord data via their APIs, compute scores in a spreadsheet or script, and manually classify members.

### 2. Manually validate the top 10

Review each of the top 10 scored community members:

- Do they answer questions from other members? (Check message history in help channels)
- Do they share resources, guides, or tips? (Check for long-form messages and link sharing)
- Are they consistently active, or did they have one busy week? (Check weekly activity pattern)
- Do other community members mention or tag them for help? (Check mentions)
- Would you want this person publicly representing your product?

If more than 3 of the top 10 do not pass manual validation, the scoring model needs recalibration. Adjust dimension weights and re-run. Document what you changed and why.

**Human action required:** Review the scored list and validate each member. This cannot be automated at Smoke level because you need to build intuition about what a community champion looks like for your specific community.

### 3. Send personal recognition outreach

For each validated champion, send a personal email or DM (not automated, not templated) from a real person on the team:

- Acknowledge their specific contributions: "I noticed you've been helping a lot of people in #support this month — especially your walkthrough on [specific topic] that got a ton of reactions. Thank you."
- Offer a specific recognition: "We'd love to feature you as a community champion. That comes with early feature access and a direct line to our product team."
- Make a specific referral ask that feels natural: choose the approach that fits each champion's profile:
  - Champions who share tutorials: "Know anyone else who'd benefit from the community? Here's a personal invite link."
  - Champions who answer questions: "Your deep knowledge is impressive — would you share [Product] with a colleague who might find it useful?"
  - Champions active on social media: "Would you post about your experience with [Product]? Here's a pre-written tweet you can customize."
- Keep it short. One ask per message. Make the referral action frictionless (provide a one-click link, pre-written post, or shareable invite).

**Human action required:** Write and send 10 personal messages. Track responses in Attio.

### 4. Track responses and evaluate

Over 7 days, log every response and referral action in Attio:

- Response received (yes/no, sentiment, what they said)
- Referral action completed (link shared, colleague introduced, social post made, public recommendation)
- Decline or no response (note the reason if given)

Run the `threshold-engine` drill to evaluate:

- **Pass threshold**: >=3 of the top 10 generate a referral action
- If PASS: the scoring model identifies community members with real referral potential, and recognition motivates sharing. Proceed to Baseline.
- If FAIL but >=6 responded positively: the model is good but the referral ask needs work. Iterate on the ask approach (try a different framing, lower the friction) and re-run.
- If FAIL and <6 responded: the model may be surfacing the wrong people, or the recognition offer is not compelling. Recalibrate scoring weights (maybe helpfulness is not the best predictor; try weighting content creation higher) and re-run.

## Time Estimate

- 2 hours: extract community data and run the scoring model (API queries + score computation)
- 1 hour: manual validation of top 10 community members
- 1 hour: write and send 10 personal recognition messages with referral asks
- 1 hour: 7-day tracking and final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Score storage, cohort creation, referral event tracking | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Store scored members, track outreach and responses | Free tier: 3 seats ([attio.com/pricing](https://attio.com/pricing)) |
| Slack API | Read community messages for scoring | Free (included with Slack workspace) |
| Discord API | Read community messages for scoring | Free (bot token) |

**Estimated play-specific cost at this level:** Free (within free tiers for a manual run of 10 members)

## Drills Referenced

- the champion identification scoring workflow (see instructions below) — builds the composite scoring model from community contribution data (helpfulness, content, consistency, reach, expertise) and syncs scored members to Attio
- `threshold-engine` — evaluates the pass/fail threshold and recommends next action
