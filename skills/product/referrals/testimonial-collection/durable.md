---
name: testimonial-collection-durable
description: >
  Systematic Testimonial Collection — Durable Intelligence. Always-on AI agents
  autonomously optimize collection rates, rotate stale inventory, run experiments,
  and maintain testimonial coverage at the local maximum.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained ≥25 testimonials/month with quality ≥4.0 and full segment coverage for 6 months via autonomous optimization"
kpis: ["Collection rate", "Quality score", "Submission rate", "Inventory coverage", "Experiment velocity", "AI lift"]
slug: "testimonial-collection"
install: "npx gtm-skills add product/referrals/testimonial-collection"
drills:
  - autonomous-optimization
  - dashboard-builder
---
# Systematic Testimonial Collection — Durable Intelligence

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes
The testimonial collection pipeline runs autonomously with AI agents detecting metric anomalies, generating improvement hypotheses, running A/B experiments, evaluating results, and auto-implementing winners. The system sustains ≥25 testimonials per month at ≥4.0 average quality with full segment coverage. Weekly optimization briefs report what changed and why. The agent converges when successive experiments produce <2% improvement, indicating the local maximum has been reached.

## Leading Indicators
- Autonomous optimization loop firing on schedule (daily monitor, weekly experiments)
- Experiment win rate ≥30% (at least 1 in 3 experiments produces a statistically significant improvement)
- No health metric in critical status for more than 3 consecutive days
- Inventory freshness ≥30% (testimonials published in the last 90 days as a share of total)
- Testimonial-influenced deal conversion rate measurable and trending up

## Instructions

### 1. Activate the autonomous optimization loop
Run the `autonomous-optimization` drill configured for the testimonial collection play. This is the core loop that makes Durable fundamentally different from Scalable:

**Monitor (daily via n8n cron):**
- Check the 6 testimonial KPIs: collection rate, form open rate, submission rate, quality rate, video willingness, inventory freshness
- Compare last 2 weeks against the 4-week rolling average
- Classify each: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If normal: log to Attio, no action
- If anomaly detected: trigger the Diagnose phase

**Diagnose (triggered by anomaly):**
- Gather context: current request copy, form variant, trigger configuration, segment weighting
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and pipeline context
- Receive 3 ranked hypotheses (e.g., "Request copy has gone stale — rotate to social proof variant," "Short form is now outperforming long form as user base has shifted mobile-heavy," "Enterprise segment is underweighted — increase priority scoring for enterprise candidates")
- Store hypotheses in Attio. If top hypothesis is high-risk (changes affecting >50% of pipeline traffic), send Slack alert for human review and STOP. Otherwise proceed.

**Experiment (triggered by hypothesis acceptance):**
- Take the top-ranked hypothesis
- Use PostHog feature flags to split traffic between control and variant
- Set minimum duration: 7 days or 100+ samples per variant, whichever is longer
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Evaluate (triggered by experiment completion):**
- Pull results from PostHog
- Run `experiment-evaluation`: adopt (implement winner), iterate (new hypothesis building on this result), revert (restore control), or extend (keep running)
- Store the full evaluation in Attio

**Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from adopted changes
- Generate weekly optimization brief: what changed, net impact on KPIs, estimated distance from local maximum, recommended focus for next week
- Post to Slack and store in Attio

**Guardrails:**
- Maximum 1 active experiment at a time
- Auto-revert if primary metric drops >30% during any experiment
- Human approval required for budget changes >20% or targeting changes affecting >50% of traffic
- Maximum 4 experiments per month. If all 4 fail, pause and flag for human strategic review.
- 7-day cooldown after a failed experiment before testing the same variable again

### 2. Activate the testimonial health monitor
Run the `autonomous-optimization` drill to deploy play-specific monitoring that runs alongside the generic optimization loop:

- Daily health check across 6 testimonial-specific metrics (request rate, form open rate, submission rate, quality rate, video willingness, inventory freshness)
- Diagnostic triggers for each declining metric with root-cause analysis
- 4 automated interventions: stale copy rotation, form shortening on abandonment spike, criteria relaxation on low candidate pool, video incentive on video drought
- Weekly testimonial report with pipeline status, inventory gaps, intervention outcomes, and top quotes
- Escalation rules: any metric critical for 5+ days, zero submissions in 2 weeks, or 3+ interventions with no improvement triggers human handoff

### 3. Build the durable intelligence dashboard
Run the `dashboard-builder` drill to create the Durable-level dashboard that goes beyond Scalable's operational view:

- **Optimization loop status**: current phase (monitoring/diagnosing/experimenting/evaluating), active experiment details, days since last experiment
- **Experiment history**: timeline of all experiments with outcomes (adopted/reverted/iterated), cumulative lift from adopted changes
- **Convergence tracker**: trailing 3-experiment average improvement %. When this drops below 2%, the play has reached its local maximum.
- **Testimonial ROI**: testimonials used in sales materials → deals where testimonial was shared → deal outcomes. Calculate testimonial-influenced pipeline and revenue.
- **Inventory lifecycle**: age distribution of active testimonials, upcoming staleness (testimonials approaching 12 months without refresh), segment coverage trending over time
- **Health monitor summary**: 6 metrics with current status, days in current status, and trend arrows

### 4. Evaluate sustainability
Measure against: sustained ≥25 testimonials/month with quality ≥4.0 and full segment coverage for 6 months via autonomous optimization. This level runs continuously. The agent detects convergence when successive experiments produce diminishing returns (<2% improvement for 3 consecutive experiments). At convergence:

1. The testimonial pipeline has reached its local maximum
2. Reduce monitoring frequency from daily to weekly
3. Report: "Testimonial collection is optimized. Current performance: [metrics]. Further gains require strategic changes (new product features generating new use cases, expansion into new verticals, video testimonial program) rather than tactical optimization."

## Time Estimate
- 30 hours: configure autonomous optimization loop (monitor, diagnose, experiment, evaluate, report phases)
- 20 hours: deploy testimonial health monitor with diagnostics and interventions
- 15 hours: build durable intelligence dashboard with ROI tracking and convergence metrics
- 85 hours: ongoing monitoring, experiment review, human approvals for high-risk changes, monthly strategic reviews

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Typeform | Testimonial forms (multiple variants for ongoing experiments) | $50/mo Plus (unlimited responses, logic) |
| PostHog | Feature flags, experiments, anomaly detection, dashboards | Free tier or $0.00045/event beyond 1M |
| n8n | Automation: optimization loop, health monitor, interventions | Self-hosted free or $20/mo cloud |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | ~$10-30/mo based on monitoring frequency |
| Attio | Testimonial inventory, experiment log, optimization history | Included in standard stack |
| Intercom | In-app message variants, automated rotation | Included in standard stack |
| Loops | Email variants, NPS-triggered sequences | Included in standard stack |

**Play-specific cost:** ~$80-100/mo (Typeform Plus + n8n + Anthropic API)
**Agent compute cost:** Variable based on monitoring frequency (~$10-30/mo for daily monitoring with Claude)

## Drills Referenced
- `autonomous-optimization` — the core always-on loop: monitor metrics → detect anomalies → generate hypotheses → run experiments → evaluate results → auto-implement winners. Weekly optimization briefs. Converges at <2% improvement.
- `autonomous-optimization` — play-specific daily health checks, diagnostic triggers, automated interventions for collection pipeline problems, and weekly testimonial reports
- `dashboard-builder` — durable intelligence dashboard with optimization loop status, experiment history, convergence tracking, and testimonial ROI

---

## Pass threshold
**Sustained ≥25 testimonials/month with quality ≥4.0 and full segment coverage for 6 months via autonomous optimization**

This level runs continuously. Review monthly: what experiments improved performance, which segments need attention, whether convergence has been reached.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/referrals/testimonial-collection`_
