---
name: holdout-groups-smoke
description: >
  Holdout Group Analysis — Smoke Test. Provision a persistent holdout group in PostHog,
  establish baseline metrics for holdout vs treatment populations, and confirm the group
  assignment is stable and uncontaminated.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Holdout group provisioned with stable assignment and baseline metrics captured"
kpis: ["Holdout group size accuracy", "Assignment stability rate", "Baseline metric parity"]
slug: "holdout-groups"
install: "npx gtm-skills add product/retain/holdout-groups"
drills:
  - holdout-group-setup
  - threshold-engine
---

# Holdout Group Analysis — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

A `global-holdout` feature flag is live in PostHog, randomly assigning a fixed percentage of users to the holdout group. Both holdout and treatment PostHog cohorts exist. Baseline metrics for both groups are captured and stored in Attio. Every user resolves to the same group on every evaluation.

## Leading Indicators

- Feature flag created and active in PostHog
- Holdout cohort size within +/-2% of target percentage
- 5 repeated flag evaluations for the same distinct_id all return the same result
- Baseline retention and engagement metrics are within 5% parity between groups

## Instructions

### 1. Determine holdout size and create the holdout group

Run the `holdout-group-setup` drill. This will:
- Calculate the appropriate holdout percentage based on your active user count (default 10%)
- Create the `global-holdout` PostHog feature flag with `ensure_experience_continuity: true`
- Create PostHog cohorts for "Holdout Group" and "Treatment Group (Non-Holdout)"
- Log the `holdout_group_created` event in PostHog

### 2. Verify assignment stability

Using the PostHog feature flag evaluation API, test 10 distinct user IDs. For each, call the evaluation endpoint 5 times. Confirm every call returns the same group assignment. If any user flips between holdout and treatment, the `ensure_experience_continuity` setting is misconfigured — fix it before proceeding.

### 3. Capture baseline metrics

Query PostHog for the last 4 weeks of data, split by holdout vs treatment group. Capture:
- Weekly active users per group
- Primary retention metric (e.g., Week 1, Week 2, Week 4 retention)
- Primary engagement metric (e.g., feature usage frequency, session count)

Store the baseline in Attio as a note on the holdout campaign record.

### 4. Verify baseline parity

Confirm that holdout and treatment groups have comparable metrics at the point of holdout creation. No primary metric should differ by more than 5% between groups. If parity fails, the randomization may be biased — dissolve the holdout, wait 24 hours, and recreate with a fresh flag key.

**Human action required:** Communicate the holdout policy to your team. Any future PostHog experiment MUST include the holdout exclusion filter. Review any currently active experiments and add the filter retroactively.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against: holdout group provisioned with stable assignment and baseline metrics captured. Specifically:
- Holdout flag is active and evaluating correctly
- Holdout cohort size is within +/-2% of target
- Assignment stability is 100% (no user flips)
- Baseline parity is within 5% on all primary metrics

If PASS, proceed to Baseline. If FAIL, diagnose: is the flag misconfigured? Are users not being identified in PostHog? Is the cohort query filtering incorrectly?

## Time Estimate

- 1 hour: determine holdout size and create feature flag + cohorts
- 1 hour: verify assignment stability across test users
- 2 hours: query and analyze baseline metrics, verify parity
- 1 hour: document baseline, communicate policy to team

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, cohorts, event tracking, baseline queries | Free up to 1M feature flag requests/mo ([posthog.com/pricing](https://posthog.com/pricing)) |

## Drills Referenced

- `holdout-group-setup` — provisions the holdout feature flag, creates cohorts, captures baseline
- `threshold-engine` — evaluates pass/fail against the smoke test criteria
