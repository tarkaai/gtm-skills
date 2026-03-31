---
name: self-serve-signup-optimization-baseline
description: >
  Signup Funnel Optimization — Baseline Run. Deploy targeted friction fixes behind feature flags,
  add real-time help triggers, and run always-on conversion monitoring to lift signup CVR.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Website, Product"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: "≥10pp lift in signup CVR over Smoke baseline, sustained for 2+ weeks"
kpis: ["Signup CVR", "Form completion rate", "Form error rate", "Lift vs baseline"]
slug: "self-serve-signup-optimization"
install: "npx gtm-skills add product/onboard/self-serve-signup-optimization"
drills:
  - lead-capture-surface-setup
---

# Signup Funnel Optimization — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Website, Product

## Outcomes

The top 2-3 friction points identified in Smoke are fixed. Each fix is deployed behind a PostHog feature flag with per-variant conversion tracking. An always-on monitoring system alerts when signup CVR degrades. Signup CVR lifts by at least 10 percentage points over the Smoke baseline, sustained for 2+ weeks.

## Leading Indicators

- Feature flag variants showing measurable CVR differences within 7 days
- Form error rate declining as validation improvements take effect
- Intercom help triggers firing for users showing friction signals
- Daily monitoring workflow sending normal/warning/critical status updates
- Zero missed signup regressions (any deployment-caused CVR drop detected within 4 hours)

## Instructions

### 1. Deploy friction fixes

Run the the signup friction reduction workflow (see instructions below) drill. Using the bottleneck analysis from Smoke, implement the top 2-3 fixes (field reduction, OAuth addition, inline validation, mobile optimization, trust signals, or deferred email verification). Each fix goes behind a PostHog feature flag at 50% rollout so you can measure impact per-change.

**Human action required:** Review the proposed changes before deployment. Approve feature flag activation. If the changes involve backend modifications (OAuth integration, email verification deferral), implement those first.

### 2. Optimize the signup surface

Run the `lead-capture-surface-setup` drill to ensure the signup form itself follows best practices: single clear CTA, proper tracking events (cta_impression, cta_clicked, lead_captured), and CRM routing via n8n. If the signup page has multiple CTAs or competing actions, simplify to one primary conversion path.

### 3. Activate always-on monitoring

Run the `cta-conversion-monitor` drill to set up continuous funnel monitoring. This creates:
- Daily n8n cron workflow that checks signup CVR against baseline
- Anomaly detection: Warning at 15% below baseline, Critical at 30% below
- Per-page breakdown showing which signup entry points convert best
- Form abandonment analysis identifying which field causes the most drop-off

### 4. Validate each fix

After each feature flag variant has 200+ users per arm (typically 7-14 days):
- Pull per-variant funnel data from PostHog
- Compare variant CVR to control CVR
- If variant wins with statistical significance: roll to 100%
- If variant loses: revert and investigate
- If inconclusive: extend the test or increase traffic

### 5. Evaluate against threshold

Measure the overall signup CVR after all winning variants are rolled out. Compare to the Smoke baseline. The Baseline level passes when:
- Signup CVR is at least 10 percentage points higher than the Smoke baseline
- The improvement holds for 2+ consecutive weeks
- The monitoring system is running and producing daily status updates

If the 10pp lift is not achieved after deploying all 3 fixes, diagnose which fix had the least impact, revert it, and try the next item on the friction priority list from `signup-funnel-audit`.

## Time Estimate

- 6 hours: Implement and deploy 2-3 friction fixes behind feature flags
- 4 hours: Optimize signup surface and wire CRM routing
- 4 hours: Set up monitoring workflows and anomaly detection
- 14-21 days: Run feature flag experiments (passive monitoring)
- 4 hours: Analyze results, roll out winners, document lift
- 2 hours: Final threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, funnels, session recordings | Free tier: 1M events + 1M flag requests/mo. Paid: usage-based. [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Help triggers for users showing signup friction | Essential: $29/seat/mo. Early-stage startups: up to 90% off year 1. [intercom.com/pricing](https://www.intercom.com/pricing) |
| n8n | Monitoring workflows, webhook routing, daily cron jobs | Community (self-hosted): Free. Cloud Starter: ~$24/mo. [n8n.io/pricing](https://n8n.io/pricing/) |

## Drills Referenced

- the signup friction reduction workflow (see instructions below) — implements targeted fixes for the signup bottleneck behind feature flags with per-variant tracking
- `lead-capture-surface-setup` — optimizes the signup form as a conversion surface with proper tracking and CRM routing
