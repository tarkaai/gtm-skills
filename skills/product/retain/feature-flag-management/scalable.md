---
name: feature-flag-management-scalable
description: >
  Feature Flag System -- Scalable Automation. Scale flag operations to 500+ concurrent
  flags with automated A/B experimentation, segment-specific rollouts, and flag-driven
  retention experiments.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=85% rollout success rate at 500+ concurrent flags with >=10 flag-based experiments completed"
kpis: ["Rollout success rate at scale", "Concurrent active flags", "Experiment win rate", "Mean time to full rollout", "Rollback rate"]
slug: "feature-flag-management"
install: "npx gtm-skills add product/retain/feature-flag-management"
drills:
  - ab-test-orchestrator
  - feature-readiness-gating
  - flag-rollout-health-monitor
---
# Feature Flag System -- Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes
The flag system handles 500+ concurrent flags without degradation. Flags serve dual purpose: safe rollouts AND experimentation. Segment-specific rollout strategies target features to the right users. 10+ flag-based A/B experiments completed with statistical rigor. Flag health monitoring prevents flag debt from accumulating.

## Leading Indicators
- PostHog feature flag evaluation latency stays under 50ms at 500+ flag volume
- Flag-based experiments reach statistical significance within planned timeframes
- Segment-specific rollouts show higher adoption rates vs uniform rollouts
- Flag debt ratio (stale/active) stays below 25%
- Rollback rate does not increase as flag volume scales

## Instructions

### 1. Scale flag-based experimentation
Run the `ab-test-orchestrator` drill adapted for feature flags. Instead of testing marketing copy, use flags to run product experiments:

For each experiment:
1. Create a PostHog feature flag with multivariate support (control + 1-3 variants)
2. Link the flag to a PostHog experiment with defined primary metric (retention, conversion, engagement) and secondary metrics (error rate, load time as guardrails)
3. Calculate required sample size and set experiment duration
4. Monitor via PostHog experiment results -- do not peek or call winners early
5. When significant: roll winning variant to 100%, archive losing variants

Target: 10+ experiments over 2 months. Track win rate (experiments where a variant beat control). Healthy systems see 20-40% win rate -- lower means hypotheses are weak, higher means you are testing obvious improvements.

### 2. Implement segment-specific rollouts
Run the `feature-readiness-gating` drill to build progressive feature disclosure tied to flags:

- **By user maturity**: Gate advanced features behind flags that only activate for users who have completed prerequisite actions. New users see Core features; power users see everything.
- **By plan tier**: Use PostHog cohorts to target flags by subscription plan. Premium features roll out to paid users first, free tier gets them later (or never).
- **By engagement level**: High-engagement users (top quartile by session frequency) get new features first. They are the best testers -- most likely to exercise edge cases and provide feedback.
- **By geography**: For features with regional compliance implications, roll out region-by-region using cohort-based flag targeting.

Each segment strategy uses PostHog cohorts as the targeting mechanism within the flag's filter configuration.

### 3. Build flag health monitoring at scale
Run the `flag-rollout-health-monitor` drill to maintain system health as flag volume grows:

- Deploy the flag health dashboard tracking: rollout success rate, active flag count, stale flag count, flag debt ratio, per-flag product impact
- Configure weekly health check workflow computing all KPIs
- Set anomaly alerts for: success rate dropping below 80%, active flag count exceeding capacity thresholds, rollback rate spiking
- Enable per-flag product impact tracking -- for every active flag, compare treatment vs control on key metrics using PostHog cohorts

At 500+ flags, manual oversight is impossible. The health monitor is the agent's eyes on the system.

### 4. Implement flag dependencies and conflicts
As flag volume grows, flags interact. Build an n8n workflow that:

1. Maintains a flag dependency graph: "Flag B should not activate unless Flag A is at 100%"
2. Detects flag conflicts: two flags modifying the same UI area should not both be in partial rollout simultaneously
3. Before advancing any flag, checks the dependency graph for conflicts
4. Blocks conflicting rollouts and alerts the flag owners to coordinate

Store the dependency graph as PostHog flag metadata or in a dedicated data store.

### 5. Evaluate against threshold
Measure against: >=85% rollout success rate across 500+ concurrent flags with 10+ experiments completed. If PASS, proceed to Durable. If FAIL, diagnose: is the issue at the flag infrastructure level (latency, evaluation errors) or the process level (poor experiment design, insufficient sample sizes)?

**Human action required:** Review the 10 experiment results. For each winning variant, confirm the metric improvement aligns with a real product improvement, not a measurement artifact.

## Time Estimate
- 15 hours: Set up and run 10+ flag-based experiments via ab-test-orchestrator
- 15 hours: Implement segment-specific rollout strategies with feature-readiness-gating
- 15 hours: Deploy flag health monitoring and tune alert thresholds
- 10 hours: Build flag dependency and conflict detection
- 5 hours: Evaluate results and prepare for Durable

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, cohorts, dashboards | Free tier: 1M events/mo. Growth from $0 with pay-per-use. https://posthog.com/pricing |
| n8n | Workflow automation for health checks and dependency management | Self-hosted free; Cloud from EUR20/mo. https://n8n.io/pricing |
| Intercom | In-app messages for segment-specific feature reveals | Starter $74/mo. https://www.intercom.com/pricing |

## Drills Referenced
- `ab-test-orchestrator` -- runs rigorous A/B experiments using feature flags as the randomization mechanism
- `feature-readiness-gating` -- implements progressive feature disclosure gated by user behavior cohorts
- `flag-rollout-health-monitor` -- monitors system-wide flag health, rollback rates, and flag debt at scale
