---
name: onboarding-email-sequence-durable
description: >
  Onboarding email sequence — Durable Intelligence. Agent-driven autonomous
  optimization of onboarding emails: auto-detects performance regressions, generates
  and deploys test hypotheses, refreshes content, and adapts to changing user behavior.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Email"
level: "Durable Intelligence"
time: "4 hours/month over 6 months"
outcome: "Activation rate >= 30% at day 7 sustained over 6 months with autonomous agent maintaining or improving performance without manual intervention"
kpis: ["Activation rate at day 7 (weekly trend)", "Activation rate by segment (monthly)", "Test velocity (tests completed per month)", "Content freshness (days since last email refresh)", "Deliverability score", "Agent intervention count (auto-fixes per month)"]
slug: "onboarding-email-sequence"
install: "npx gtm-skills add product/onboard/onboarding-email-sequence"
drills:
  - dashboard-builder
  - nps-feedback-loop
  - threshold-engine
---

# Onboarding Email Sequence — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Email

## Outcomes

The onboarding email sequence runs autonomously with an AI agent monitoring performance, detecting regressions, generating new test hypotheses, refreshing stale content, and adapting to shifts in user behavior. The human reviews a weekly report and approves major changes. The agent handles everything else. Activation rate >= 30% at day 7 sustained over 6 months.

## Leading Indicators

- Agent detects a regression within 48 hours of it starting (before the weekly report)
- Agent generates at least 2 actionable test hypotheses per month based on data patterns
- Content refresh happens automatically when an email's click rate declines 20%+ from its peak
- Weekly report arrives on time with no gaps — the pipeline is fully reliable
- Activation rate variance stays within +/- 3 percentage points of the 6-month average

## Instructions

### 1. Build the onboarding performance dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard dedicated to onboarding email performance. Include:

- **Activation rate by week:** Line chart showing 7-day activation rate for the treatment group over time. Add a horizontal line at the 30% threshold.
- **Activation rate by segment:** Table showing activation rate for each onboarding track (segments defined at Scalable level). Highlight any segment below 25%.
- **Per-email funnel:** Funnel from `email_sent` > `email_opened` > `email_clicked` > `activation_reached` for each of the 7 emails. Identify the weakest link.
- **Time to activation distribution:** Histogram showing days from signup to activation. The median should be decreasing or stable.
- **A/B test history:** Table of all completed tests with hypothesis, result, and impact on activation rate.
- **Deliverability health:** Bounce rate, spam complaint rate, unsubscribe rate (all should be flat or declining).

Set alerts on this dashboard:
- Activation rate drops below 25% for 3 consecutive days
- Any email step's open rate drops below 30%
- Bounce rate exceeds 2%
- Unsubscribe rate exceeds 0.5%

### 2. Configure the autonomous monitoring agent

Build an n8n workflow (or Claude Code scheduled task) that runs daily and performs:

**Daily health check:**
1. Query PostHog API for yesterday's onboarding metrics: enrollments, sends per step, opens, clicks, milestones, activations
2. Compare each metric to its 30-day rolling average
3. If any metric deviates by more than 15% from the rolling average, flag it as an anomaly
4. For anomalies: generate a diagnosis (what changed? new signup source? product change? seasonal effect?) by cross-referencing with PostHog events and cohort breakdowns
5. If the anomaly is a regression: generate a recommended fix and post it for human review
6. If the anomaly is an improvement: document what likely caused it and whether to double down

**Weekly optimization report:**
Generate a report every Monday with:
- This week vs last week vs 4-week average for all KPIs
- Segment-level performance comparison
- Active and completed A/B tests with results
- Recommended actions ranked by expected impact
- Content staleness check: flag any email that has not been refreshed in 90+ days

### 3. Automate A/B test lifecycle

Build an agent-driven testing loop:

1. **Hypothesis generation:** The agent reviews the per-email funnel data and identifies the weakest email step. It generates a hypothesis: "Email 3 click rate is 4.2% (lowest in the sequence). If we change the CTA from 'Get started' to 'See how [Company Type] uses [Product]' with a specific customer example, click rate will increase by 2+ percentage points."

2. **Test setup:** The agent creates the variant in Loops (new email content), sets up the A/B split in the sequence, and configures PostHog tracking for the new variant.

3. **Monitoring:** The agent checks daily whether the test has reached statistical significance (minimum 200 per variant, 95% confidence). It does NOT call a winner early.

4. **Decision and deployment:** When the test concludes, the agent:
   - If winner: deploys the winning variant to 100% of traffic. Logs the result. Moves to the next test.
   - If no significant difference: keeps the simpler variant. Logs the result. Generates a new hypothesis for a different variable.
   - If loser: reverts immediately. Analyzes why the hypothesis was wrong.

5. **Cadence:** The agent should complete 2-3 tests per month. One test at a time per email step to avoid confounding.

**Human action required:** Review and approve each new test hypothesis before the agent deploys it. The agent posts the hypothesis, expected impact, and test plan. The human approves, modifies, or rejects within 48 hours.

### 4. Automate content refresh

Build an n8n workflow that monitors email content freshness:

1. Track the "birth date" of each email's current content as a variable
2. Every 90 days, or when an email's click rate drops 20%+ from its historical peak, flag it for refresh
3. The agent drafts new content: updated social proof (recent customer examples), refreshed screenshots, current statistics
4. The refresh follows the same structure and tone as the original — it is not a redesign, just updated facts and examples

**Human action required:** Review refreshed email content before deployment. Verify customer examples are accurate and screenshots are current.

### 5. Launch NPS-driven improvements

Run the `nps-feedback-loop` drill with a focus on onboarding-stage users. Deploy an NPS survey at day 14 (after the onboarding sequence completes) via Intercom:

- **Promoters (9-10):** Analyze what they cite as the most helpful part of onboarding. Double down on it.
- **Passives (7-8):** Look for patterns in what they say was missing. These are improvement opportunities for the email sequence.
- **Detractors (0-6):** Investigate whether the email sequence contributed to their dissatisfaction. Were they getting irrelevant emails? Did the CTA lead to a confusing product experience?

Feed NPS insights into the agent's hypothesis generation. If detractors consistently cite "too many emails" as a complaint, test reducing the sequence length. If passives say they "didn't understand what to do," test clearer CTAs and simpler email content.

### 6. Adapt to user behavior shifts

Over 6 months, user behavior changes: new signup sources appear, product features change, competitor landscape shifts. The agent must detect and adapt:

- **New signup source:** When a new `signup_source` value appears with > 50 users and activation rate differs by > 5pp from the average, the agent should recommend a new segment track.
- **Product changes:** When a new feature ships that changes the activation path, the agent flags that the email sequence may reference outdated milestones. Prompt human review.
- **Seasonal patterns:** The agent tracks weekly patterns and adjusts expectations. Holiday periods get different benchmarks than normal periods.

### 7. Monthly human review

Once per month, the human reviews:

1. The agent's weekly reports for the month (10-minute skim)
2. Completed A/B tests and their cumulative impact on activation rate
3. Any proposed sequence changes or new segment tracks
4. NPS trends for onboarding-stage users
5. Approve or modify the agent's plan for next month

Total human time: ~1 hour per month.

## Time Estimate

- 6 hours: Initial setup (dashboard, monitoring agent, test automation pipeline)
- 1 hour/week: Review weekly report (mostly automated — human reviews and approves)
- 2 hours/month: Monthly review and agent plan approval
- Total: ~4 hours/month after initial setup

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Automated email sequences, A/B testing, content delivery | $49/mo+ depending on contact volume. [Pricing](https://loops.so/pricing) |
| PostHog | Dashboards, funnels, cohorts, feature flags, experiments | Free up to 1M events/mo. Usage-based beyond. [Pricing](https://posthog.com/pricing) |
| n8n | Agent workflows, monitoring, alerting, test lifecycle automation | Cloud from €24/mo (Starter) to €60/mo (Pro). Free self-hosted. [Pricing](https://n8n.io/pricing/) |
| Intercom | NPS surveys at day 14, in-app messages for stuck users | From $29/seat/mo (Essential). Early-stage discount available. [Pricing](https://www.intercom.com/pricing) |
| Cal.com | Booking links in help-offer emails | Free for 1 user. [Pricing](https://cal.com/pricing) |

**Estimated monthly cost: $100-200/mo** (Loops $49 + n8n €60 + Intercom $29. PostHog and Cal.com free tier for most volumes.)

## Drills Referenced

- `dashboard-builder` — creates the PostHog dashboard for real-time onboarding email performance visibility
- `nps-feedback-loop` — collects and acts on NPS feedback from users who completed the onboarding sequence
- `threshold-engine` — ongoing evaluation of activation rate against the sustainability threshold
