---
name: usage-milestones-scalable
description: >
  Usage Milestone Celebrations — Scalable Automation. Roll out celebrations to 100% of users,
  segment celebrations by persona and usage pattern, A/B test celebration formats and CTA variants,
  and prove the system sustains ≥65% celebration engagement at 500+ users.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥65% celebration engagement rate sustained across 500+ monthly milestone-reaching users"
kpis: ["Celebration engagement rate at scale", "Retention lift by persona", "CTA conversion rate by tier", "Celebration-to-churn ratio"]
slug: "usage-milestones"
install: "npx gtm-skills add product/retain/usage-milestones"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - usage-milestone-rewards
  - feature-adoption-monitor
---

# Usage Milestone Celebrations — Scalable Automation

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Milestone celebrations run at 100% of users with zero manual intervention. Celebrations are segmented by persona so each user gets contextually relevant messaging. A/B tests have optimized celebration format, copy, timing, and CTAs. The system sustains 65%+ engagement across 500+ monthly milestone-reaching users.

## Leading Indicators

- Celebration engagement rate holds steady as user volume scales from Baseline's 100-user test to 500+
- No single persona segment drops below 50% engagement
- At least 2 A/B tests have produced statistically significant improvements
- Churn rate among celebrated users is measurably lower than among users who reached milestones before celebrations existed

## Instructions

### 1. Roll out to 100% of users

Remove the feature flag experiment from Baseline. Enable milestone celebrations for all users. Monitor for 1 week to ensure the infrastructure handles the increased volume:

- Intercom message delivery latency stays under 2 seconds
- Loops email delivery rate stays above 98%
- PostHog event ingestion has no dropped events (check the ingestion dashboard)
- No duplicate celebrations fire for the same user at the same tier

### 2. Segment celebrations by persona

Using PostHog cohorts, define 2-3 user personas based on usage patterns:

- **Power builders**: High action volume, use advanced features, tend to be technical. Celebrate with data: "You have processed 500 workflows — that puts you in the top 5% of users."
- **Steady operators**: Consistent daily usage, moderate volume, value reliability. Celebrate with continuity: "You have logged in 30 days straight. Consistency compounds."
- **Team leaders**: Invite teammates, use collaboration features. Celebrate team impact: "Your team just hit 100 shared projects. Here is what you have built together."

Update the `usage-milestone-rewards` drill celebrations to branch by persona. The in-app message template and email template each get persona-specific copy variants. Use PostHog person properties to assign personas and Intercom user attributes to route to the correct message variant.

### 3. Run systematic A/B tests

Run the `ab-test-orchestrator` drill to test celebration variables in sequence. Test one variable at a time, each for at least 2 weeks or until statistical significance:

**Test 1 — Celebration format:**
- Variant A: text-only congratulations message
- Variant B: animated confetti/badge visual + text
- Metric: engagement rate (click or interact vs. dismiss)

**Test 2 — CTA timing:**
- Variant A: CTA embedded in the celebration message (immediate)
- Variant B: CTA sent as a follow-up email 24 hours later
- Metric: CTA conversion rate

**Test 3 — Social proof:**
- Variant A: standard celebration copy
- Variant B: celebration copy with percentile ranking ("You are in the top 10% of users")
- Metric: post-celebration 7-day retention

**Test 4 — Milestone spacing:**
- Variant A: current milestone ladder (1, 10, 50, 100, 500)
- Variant B: tighter early spacing (1, 5, 15, 50, 100, 500)
- Metric: percentage of users reaching tier 3 within 30 days of signup

Document every test result. Implement winners permanently before starting the next test.

### 4. Build churn prevention around milestones

Run the `churn-prevention` drill with milestone data as a signal source. Add milestone-specific churn signals:

- **Slowing milestone velocity**: User's time between milestones is increasing (e.g., tier 1 to tier 2 took 3 days, tier 2 to tier 3 is on track to take 15+ days). This signals declining engagement.
- **Celebration dismissal streak**: User dismissed or ignored the last 2+ celebrations. This signals fatigue or disengagement.
- **Post-milestone drop**: User hit a milestone but session frequency dropped 50%+ in the following week. The milestone may have represented a "completion" moment rather than a progress moment.

For each signal, configure an automated intervention:
- Slowing velocity: Intercom in-app message highlighting an unused feature relevant to their next milestone
- Dismissal streak: switch to email-only celebrations (less intrusive) and reduce frequency
- Post-milestone drop: personal email with a "what to try next" suggestion tailored to their usage pattern

### 5. Track scale metrics

Run the `feature-adoption-monitor` drill to measure how celebrations drive deeper product usage. Build a PostHog dashboard tracking:

- Monthly milestone-reaching users (target: 500+)
- Celebration engagement rate by persona and tier
- A/B test results timeline
- Retention lift trend (should be stable or improving)
- Churn prevention intervention save rate

Set alerts: engagement rate drops below 60% for any persona, monthly milestone-reaching users drops below 400, or churn rate among celebrated users exceeds uncelebrated baseline.

### 6. Evaluate against threshold

After 2 months, measure: celebration engagement rate across the full user base (500+ milestone-reaching users/month). Target: >=65%.

**PASS** if engagement >=65% at 500+ monthly users. Proceed to Durable.

**FAIL scenarios:**
- Engagement drops as volume scales: infrastructure or targeting issue. Check Intercom delivery rates and PostHog event accuracy at scale.
- Engagement varies wildly by persona: one persona is well-served, others are not. Focus A/B tests on the underperforming persona.
- 500 users not reached: product growth issue, not a celebration issue. Focus on acquisition plays.

## Time Estimate

- 4 hours: roll out to 100%, monitor infrastructure
- 12 hours: build persona segmentation and variant celebrations
- 20 hours: run 4 A/B tests (5 hours setup and analysis each)
- 10 hours: build milestone-based churn prevention signals and interventions
- 8 hours: build dashboard, set alerts, analyze results
- 6 hours: documentation and handoff prep for Durable

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, experiments, cohorts, feature flags | Free tier: 1M events/mo; Growth: $0.00045/event — https://posthog.com/pricing |
| Intercom | Persona-segmented in-app celebrations | Starter: $74/mo; Pro with custom bots: ~$150-300/mo — https://www.intercom.com/pricing |
| Loops | Tier-specific follow-up emails | Starter: $49/mo (5,000 contacts) — https://loops.so/pricing |

## Drills Referenced

- `ab-test-orchestrator` — runs the 4 sequential A/B tests on celebration format, timing, social proof, and spacing
- `churn-prevention` — adds milestone-specific churn signals (slowing velocity, dismissal streaks, post-milestone drops) and automated interventions
- `usage-milestone-rewards` — expands celebrations with persona-specific copy variants
- `feature-adoption-monitor` — measures whether celebrations drive deeper feature discovery at scale
