---
name: feature-flag-management-baseline
description: >
  Feature Flag System -- Baseline Run. Automate the flag lifecycle: creation via
  webhook, progressive rollout with regression gates, and stale flag cleanup.
  First always-on automation achieving >=90% rollout success rate.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=90% rollout success rate across 10+ flag rollouts with automated regression gates"
kpis: ["Rollout success rate", "Mean time to full rollout", "Rollback rate", "Stale flag count"]
slug: "feature-flag-management"
install: "npx gtm-skills add product/retain/feature-flag-management"
drills:
  - flag-lifecycle-automation
  - threshold-engine
---
# Feature Flag System -- Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes
Automated feature flag lifecycle running always-on via n8n. Flags are created via webhook, advanced through progressive rollout schedules with regression gates, and flagged for cleanup when stale. 10+ flags processed through the system with >=90% reaching 100% rollout without rollback.

## Leading Indicators
- n8n rollout progression workflow fires daily and advances eligible flags
- Regression gates correctly block rollout when treatment group shows metric degradation
- Stale flag cleanup report generates weekly with actionable recommendations
- `flag_rollout_advanced` events fire automatically without manual intervention
- Mean time to full rollout stays within risk-level targets (low: <=7d, medium: <=14d, high: <=28d)

## Instructions

### 1. Build the automated flag lifecycle
Run the `flag-lifecycle-automation` drill to set up:
- **Flag creation workflow**: n8n webhook endpoint that creates PostHog feature flags with standardized metadata (owner, risk level, rollout schedule). Engineering triggers this when a feature is ready for flagged rollout.
- **Progressive rollout schedules**: Three risk-level templates (low/medium/high) that define the percentage stages and timing for each rollout.
- **Daily rollout progression**: n8n cron workflow that checks all active flags against their schedule and advances eligible flags via the PostHog API.
- **Regression gates**: Before each rollout advance, compare treatment vs control group error rates and key metrics over 48 hours. Block the advance if treatment shows >10% higher error rate or >15% lower conversion.
- **Stale flag cleanup**: Weekly n8n workflow that identifies flags at 100% for 14+ days and generates a cleanup report.

### 2. Process 10+ flags through the system
Over the 2-week evaluation period, route all new feature releases through the flag system:
- Create each flag via the webhook endpoint
- Assign appropriate risk levels
- Let the daily cron workflow handle rollout progression
- Monitor regression gates -- when a gate blocks, investigate and resolve the regression before manually unblocking

**Human action required:** Ensure engineering teams create feature flags via the webhook rather than manually in PostHog. Review any flags blocked by regression gates within 24 hours.

### 3. Validate regression gate accuracy
After the first week, audit the regression gates:
- Were any flags blocked that should not have been? (false positives -- gate is too sensitive)
- Were any regressions missed that should have blocked a rollout? (false negatives -- gate is too loose)
- Adjust the thresholds (error rate delta, conversion delta) based on findings

A regression gate that blocks too often creates friction and teams will bypass it. A gate that never blocks provides no safety. Target 5-15% block rate for a healthy system.

### 4. Evaluate against threshold
Run the `threshold-engine` drill. Pass criteria: >=90% rollout success rate (flags reaching 100% without rollback) across 10+ flags processed. If PASS, proceed to Scalable. If FAIL, diagnose: are regressions real (release quality issue) or false positives (gate calibration issue)?

## Time Estimate
- 6 hours: Build and test the flag-lifecycle-automation workflows in n8n
- 2 hours: Configure regression gate thresholds and test with synthetic regressions
- 6 hours: Monitor and support 10+ flags through the automated lifecycle
- 2 hours: Audit regression gate accuracy and evaluate threshold

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, event tracking | Free tier: 1M events/mo, unlimited flags. https://posthog.com/pricing |
| n8n | Workflow automation for rollout progression and cleanup | Self-hosted free; Cloud from EUR20/mo. https://n8n.io/pricing |

## Drills Referenced
- `flag-lifecycle-automation` -- builds the full automated flag creation, rollout, and cleanup pipeline
- `threshold-engine` -- evaluates pass/fail against the 90% rollout success target
