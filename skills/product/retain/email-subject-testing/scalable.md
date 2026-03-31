---
name: email-subject-testing-scalable
description: >
  Email Subject-Line A/B Testing — Scalable Automation. Scale subject-line testing to all retention
  email segments with automated variant generation and per-segment optimization, maintaining >=15%
  lift across 500+ recipients.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=15% relative open-rate lift sustained across 500+ recipients per tested email"
kpis: ["Open rate lift by segment", "Click rate by segment", "Test velocity (tests/week)", "Segment coverage (% of retention emails tested)", "Unsubscribe rate"]
slug: "email-subject-testing"
install: "npx gtm-skills add product/retain/email-subject-testing"
drills:
  - email-subject-test-pipeline
  - ab-test-orchestrator
  - email-subject-performance-monitor
  - threshold-engine
---

# Email Subject-Line A/B Testing — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Email

## Outcomes

Scale subject-line A/B testing from individual tests to systematic coverage of all retention emails. Run 2-3 tests per week. Segment tests by user cohort (plan type, usage level, tenure). Achieve >=15% relative open-rate lift sustained across emails with 500+ recipients. Build an automated pipeline that generates variant suggestions, schedules tests, and rolls out winners without manual intervention for each test.

## Leading Indicators

- Test velocity: 2-3 tests completed per week
- Segment coverage: >80% of retention emails have been through at least 1 subject-line test
- Pattern library has 15+ documented results with segment-level insights
- Automated variant generation produces viable suggestions without manual editing >70% of the time
- Open-rate trend line is flat or rising across all retention email categories

## Instructions

### 1. Build segment-aware test scheduling

Extend the `email-subject-test-pipeline` to operate per-segment. Using Loops audience segments (via the `loops-audience` fundamental referenced in the drill), split tests by:

- **Plan type:** Free vs. paid users respond differently to subject-line framing
- **Usage level:** Power users vs. low-usage users have different attention triggers
- **Tenure:** Users in their first 30 days vs. 90+ day users need different language
- **Engagement tier:** Active openers vs. historically low openers

Create an n8n workflow that maintains a test queue: list of untested email + segment combinations. Each week, the workflow picks the 2-3 highest-priority combinations (highest volume, lowest open rate) and triggers the test pipeline.

### 2. Automate variant generation

Run the `ab-test-orchestrator` drill to build a hypothesis-driven testing framework. For each test, the agent:

1. Pulls the current subject line and its open rate from Loops
2. Queries the subject-line pattern library for the winning framing category for this email type + segment combination
3. Generates a variant using the predicted best framing category
4. If no pattern data exists for this combination, defaults to the overall highest-performing framing category

The agent writes the variant subject line directly. **Human action required:** Review and approve variant subject lines for the first 2 weeks. After the agent produces 10+ approved variants without edits, switch to auto-approve with a weekly audit of generated variants.

### 3. Scale monitoring to per-segment reporting

Run the `email-subject-performance-monitor` drill with expanded scope:

- Dashboard panels broken down by segment (plan type, usage level, tenure)
- Per-segment open-rate trend lines with threshold indicators
- Automated alerts when any segment's open rate drops below its 4-week rolling average by >10%
- Weekly brief now includes segment-level insights: "Paid users respond best to direct-value framing; free users respond best to curiosity gaps"

### 4. Build the winner rollout automation

Create an n8n workflow that automates winner rollout:

1. After a test reaches 200+ sends per variant and 48+ hours, pull results from PostHog
2. If one variant wins by >3pp open rate with no unsubscribe rate increase, update the Loops sequence or broadcast template to use the winning subject
3. Log the rollout in the pattern library
4. If the test is a tie (<3pp difference), keep the simpler subject and log the result

This removes manual intervention from the test-evaluate-rollout cycle.

### 5. Evaluate against threshold

Run the `threshold-engine` drill at 2 months. Pass criteria: emails that have been through subject-line testing show >=15% relative open-rate lift sustained across 500+ recipients. Measure across all tested emails, not just the most recent test. If PASS, proceed to Durable. If FAIL, analyze segment-level data to find where lift is weakest and concentrate testing there.

## Time Estimate

- 12 hours: Build segment-aware test scheduling and automated variant generation
- 8 hours: Expand monitoring dashboard to per-segment reporting
- 6 hours: Build winner rollout automation in n8n
- 28 hours: Run 16-20 tests over 2 months (monitoring, reviewing variants, handling edge cases)
- 6 hours: Pattern library analysis and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Send segmented A/B tests, manage sequences | Starter $49/mo (5K contacts); Growth scales with contacts — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Track events, run experiments, build segment dashboards | Free up to 1M events/mo; usage-based pricing above — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Test scheduling, variant generation, winner rollout, weekly briefs | Self-hosted free; Cloud from ~$24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost:** Loops ~$49-149/mo depending on contact count

## Drills Referenced

- `email-subject-test-pipeline` — runs each individual subject-line A/B test, now extended with segment awareness
- `ab-test-orchestrator` — provides the hypothesis framework and automated variant generation
- `email-subject-performance-monitor` — tracks per-segment performance, generates weekly briefs, and fires anomaly alerts
- `threshold-engine` — evaluates pass/fail against the 15% lift at 500+ recipients threshold
