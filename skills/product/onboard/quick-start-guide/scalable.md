---
name: quick-start-guide-scalable
description: >
  Quick Start Guide — Scalable Automation. Scale the guide to persona-based variants,
  run systematic A/B tests on content and delivery, and deploy continuous health monitoring
  to sustain ≥ 45% completion at 500+ monthly signups.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email, Content"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 45% guide completion rate sustained at 500+ monthly signups with per-persona variants and at least 3 completed A/B tests"
kpis: ["Guide completion rate (target ≥ 45% at scale)", "Per-persona completion rate (target ≥ 40% for every persona)", "A/B test velocity (target ≥ 3 tests in 2 months)", "Cumulative lift from tests (target ≥ 5pp over Baseline)"]
slug: "quick-start-guide"
install: "npx gtm-skills add product/onboard/quick-start-guide"
drills:
  - ab-test-orchestrator
  - onboarding-persona-scaling
  - onboarding-health-monitor
---

# Quick Start Guide — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Content

## Outcomes

The quick-start guide scales from a single guide to persona-specific variants that serve 500+ monthly signups. Automated persona classification routes each new user to the right guide variant. Systematic A/B testing improves content and delivery. Continuous health monitoring detects degradation before it affects activation rates.

Pass: ≥ 45% guide completion rate sustained at 500+ monthly signups, with per-persona variants serving 3+ personas, at least 3 completed A/B tests, and cumulative improvement ≥ 5pp over Baseline.
Fail: Completion rate drops below 40% for 2+ consecutive weeks at scale, or any persona's completion rate falls below 30%, or fewer than 2 A/B tests completed in 2 months.

## Leading Indicators

- Automated persona classification assigns 90%+ of new signups without manual intervention (the classifier is working)
- Per-persona guide completion rates are within 10pp of each other (no persona is dramatically underserved)
- First A/B test reaches statistical significance within 3 weeks (sufficient traffic for testing)
- Health monitoring dashboard shows green across all personas for 7 consecutive days after deployment (the monitoring is stable)
- Guide completion rate does not drop as monthly signup volume increases from Baseline levels to 500+ (the guide scales)

## Instructions

### 1. Build persona-specific guide variants

Run the `onboarding-persona-scaling` drill. Configure it for the quick-start guide:

**Persona discovery:**
Using `posthog-cohorts`, analyze existing guide completion data. Cluster users who completed the guide vs those who abandoned by: role, company size, signup source, and first actions taken. Identify 3-5 distinct persona segments with measurably different guide engagement patterns.

Example personas for a SaaS product:
- `technical_builder`: Engineers who want API docs and integration steps first
- `team_lead`: Managers who want to set up their team and assign roles first
- `solo_creator`: Individual users who want to create their first project immediately
- `marketer`: Marketing users who want to set up tracking and reporting first

**Automated classification:**
Build an n8n workflow using `n8n-triggers` that fires on `signup_completed`:
1. Collect signals: role field from signup, email domain, company size, signup source UTM
2. Apply classification rules to assign `persona_type` property
3. Write `persona_type` to PostHog (via `posthog-custom-events`) and Intercom (via user properties API)
4. Write `persona_confidence` property: "explicit" (user selected role), "inferred" (rules), or "default"

**Per-persona guide content:**
For each persona, create a variant of the quick-start guide that:
- Reorders the milestone steps to match that persona's natural workflow
- Uses examples and screenshots relevant to that persona's use case
- Links to persona-specific features in the CTA for each step
- Has a persona-specific subject line for the email version

Deploy persona variants using PostHog feature flags: `quick-start-guide-persona` with variants per persona type. The flag reads the `persona_type` property to route users.

### 2. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill. Plan a testing roadmap targeting the 3 highest-impact variables:

**Test 1 — Guide format (weeks 1-3):**
- Hypothesis: "If we present the guide as a checklist with progress tracking instead of a linear document, completion rate will increase by 5pp, because checklists create commitment and show progress."
- Control: current linear guide format
- Variant: checklist format with checkmarks and progress bar (deployed via Intercom product tour with step tracking)
- Primary metric: `guide_completed` rate
- Secondary metrics: per-step drop-off, time-to-completion
- Sample size: 200+ per variant

**Test 2 — Delivery timing (weeks 3-5):**
- Hypothesis: "If we show the guide immediately on first login instead of waiting 24 hours for the email, view rate will increase by 10pp, because users are most motivated at signup."
- Control: in-app message on first session + email at 24h
- Variant: auto-open guide on first login (Intercom product tour auto-start) + email at 24h as backup
- Primary metric: `guide_viewed` rate within 3 days
- Secondary metrics: guide_completed rate, guide_abandoned rate

**Test 3 — Stall intervention (weeks 5-7):**
- Hypothesis: "If we send a personalized stall intervention email that references the specific step where the user stopped, re-engagement rate will increase by 15pp vs a generic reminder."
- Control: generic "Complete your setup" email
- Variant: "You left off at Step {N}: {step_name} — here's how to finish" with deep link to that step
- Primary metric: `guide_completed` rate among stalled users (guide_viewed but not guide_completed after 48h)

For each test: use `posthog-experiments` to create the feature flag, calculate required sample size, set the experiment duration, and evaluate using `experiment-evaluation` logic. Never run 2 tests simultaneously on the same user group.

### 3. Deploy continuous health monitoring

Run the `onboarding-health-monitor` drill. Configure monitoring specifically for the quick-start guide:

**Daily monitoring (n8n cron at 08:00 UTC):**
Using `posthog-anomaly-detection`, check daily:
- Overall guide completion rate (7-day rolling) vs 4-week average
- Per-persona guide completion rates
- Per-step drop-off rates
- Email open and click rates for the guide email
- Stall intervention re-engagement rate

Classify each metric: normal (±10%), warning (10-20% below average), critical (>20% below OR below play threshold).

For critical alerts, send to Slack:
```
GUIDE HEALTH ALERT: [persona_type] completion rate dropped to [X%] (expected [Y%])
- Step with highest new drop-off: Step [N] ([step_name])
- Email engagement: [open_rate%] open, [click_rate%] click
- Suggested cause: [step N instruction may be outdated | email delivery issue | persona classifier shifting]
- Recommended action: [review step N content | check Loops delivery | audit classification rules]
```

**Weekly health report (n8n cron, Monday 09:00 UTC):**
Generate a structured report with:
- Total new signups and guide views
- Overall completion rate and trend (up/down/flat)
- Per-persona breakdown: completion rate, time-to-completion, top drop-off step
- A/B test status: active tests, recent results
- Anomalies detected this week and actions taken

Post to Slack and store in Attio as a note on the play record.

**Per-page monitoring:**
Track guide performance by delivery surface (in-app, email, web). If any surface's conversion rate drops > 30% below baseline, alert immediately — it likely indicates a broken link, missing asset, or tracking failure.

### 4. Evaluate against threshold

Measure at the end of 2 months:

- **Guide completion rate at scale:** guide_completed / new signups across all personas, at 500+ monthly signup volume. Target: ≥ 45%.
- **Per-persona completion:** no persona below 40%. If any persona is below 40%, that variant needs a dedicated optimization cycle.
- **A/B test velocity:** at least 3 completed tests with statistically significant results.
- **Cumulative lift:** total improvement in guide completion rate from all adopted test variants vs the original Baseline guide. Target: ≥ 5pp.

- **PASS:** All targets met. Document: persona variants and their performance, test results and adopted changes, monitoring configuration. Proceed to Durable.
- **MARGINAL:** Overall completion ≥ 45% but one persona below 40%, or only 2 tests completed. Focus resources on the underperforming persona or accelerate testing cadence.
- **FAIL:** Overall completion < 45% at scale. Diagnose: Is the persona classifier accurate (check `persona_confidence` distribution)? Are guide variants loading correctly (check PostHog events per variant)? Is the increase in signup volume bringing a different user mix (cohort drift)?

## Time Estimate

- Persona discovery and classification build: 15 hours
- Per-persona guide variant creation: 10 hours
- A/B test design, setup, and monitoring (3 tests): 15 hours
- Health monitoring dashboard and workflow setup: 10 hours
- Ongoing monitoring and optimization (2 months, ~5 hours/week): ~40 hours
- Total: ~60 hours active work over 2 months (with 30 hours overlapping with ongoing monitoring)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, per-persona funnels, anomaly detection | Free 1M events; paid $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Persona classification workflow, health monitoring, stall interventions | Pro €60/mo for 10,000 executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | Per-persona in-app guides, product tours, stall messages | Advanced $85/seat/mo for advanced targeting ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Per-persona email sequences, guide delivery, stall emails | $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost for Scalable:** ~$195 (Intercom Advanced $85 + n8n Pro €60 + Loops $49). PostHog on free tier for most products under 1M events/mo.

## Drills Referenced

- `ab-test-orchestrator` -- design, run, and evaluate A/B tests on guide format, delivery timing, and stall interventions using PostHog feature flags and experiments with statistical rigor
- `onboarding-persona-scaling` -- discover persona segments, build automated classification, create per-persona guide variants, and deploy via feature flags
- `onboarding-health-monitor` -- continuous per-persona health monitoring with daily anomaly detection, weekly reports, and cohort drift detection feeding into optimization
