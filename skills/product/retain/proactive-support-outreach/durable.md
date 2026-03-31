---
name: proactive-support-outreach-durable
description: >
  Proactive Support Outreach — Durable Intelligence. Autonomous AI agents continuously
  optimize struggle detection, outreach content, and channel routing to find the local
  maximum of proactive retention.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Email, Direct"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving ≥45% engagement and ≥20pp retention lift over 6 months via autonomous optimization"
kpis: ["Outreach engagement rate", "Resolution rate", "30-day retention lift", "Ticket deflection", "Experiment velocity", "Optimization convergence"]
slug: "proactive-support-outreach"
install: "npx gtm-skills add product/retain/proactive-support-outreach"
drills:
  - autonomous-optimization
  - support-churn-correlation
---

# Proactive Support Outreach — Durable Intelligence

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Email, Direct

## Outcomes

Scalable proved the play works at 500+ users/month with tested outreach variants. Durable hands the optimization loop to an autonomous AI agent. The agent monitors the full detection-to-retention pipeline, detects when metrics drift, generates hypotheses for improvement, runs experiments, evaluates results, and auto-implements winners. The play converges on its local maximum — the best possible retention lift given your product, users, and help resources — and maintains it as conditions change.

Success = sustained or improving engagement ≥45% and retention lift ≥20pp over 6 months, with the autonomous optimization loop running without human intervention. The system self-heals when product changes introduce new struggle patterns or when outreach content goes stale.

## Leading Indicators

- Autonomous optimization loop running weekly without errors
- New experiments generated and launched automatically when metrics drift
- Winning experiment variants auto-implemented within 48 hours of reaching significance
- New struggle patterns detected and mapped to help resources without manual intervention
- Weekly optimization briefs showing convergence (successive experiments producing <5% improvement)
- Zero "unmapped workflow" alerts (every detected struggle pattern has an outreach resource)
- Support ticket volume on a sustained downward trend

## Instructions

### 1. Deploy the proactive outreach health monitor

Run the `autonomous-optimization` drill (all 5 steps). This builds the observability layer that the autonomous optimization loop needs:

- PostHog dashboard with 6 panels tracking the full detection-to-retention pipeline
- Daily n8n workflow that checks metrics against rolling averages and fires anomaly alerts
- Weekly health brief generated and posted to Slack with pipeline metrics, workflow resolution breakdown, and optimization recommendations
- Structured signal data stored in Attio for the optimization loop to consume

Validate that the monitor runs cleanly for 1 week before enabling autonomous optimization. Confirm: daily checks fire on schedule, anomaly thresholds are calibrated (not too many false alerts, not too few real alerts), and the weekly brief contains actionable information.

### 2. Deploy autonomous optimization

Run the `autonomous-optimization` drill configured for this play's specific metrics:

**Primary KPIs for the optimization loop:**
- Outreach engagement rate (target: ≥45%)
- Resolution rate (target: ≥40%)
- 30-day retention lift vs. non-outreached (target: ≥20pp)

**Variables the optimizer can experiment on:**
- Outreach message content (framing, length, specificity)
- Outreach channel selection per struggle tier and workflow
- Outreach timing (delay after detection, time of day, day of week)
- Follow-up cadence (number of follow-ups, timing between them)
- In-app message format (tooltip vs. banner vs. card)
- Help content format (text instructions vs. embedded walkthrough vs. video)
- Struggle scoring weights (which signals to weight more/less)
- Struggle tier thresholds (what score cutoffs define moderate/severe/critical)

**Guardrails specific to this play:**
- Never increase outreach frequency beyond 1 per user per 14 days (cooldown is sacred)
- Never remove the "suppress during open ticket" rule
- Never test outreach messages that reference the user's specific errors or session data (privacy boundary — outreach should feel like a proactive tip, not surveillance)
- If negative feedback rate (unsubscribes, complaints, negative replies) exceeds 3% for any variant, auto-revert immediately
- If overall engagement rate drops below 30% during any experiment, auto-revert
- Maximum 1 active experiment at a time (no stacking)

The optimization loop runs Phase 1 (Monitor) daily, Phase 2 (Diagnose) when anomalies are detected, Phase 3 (Experiment) when a hypothesis is generated, Phase 4 (Evaluate) when an experiment completes, and Phase 5 (Report) weekly.

### 3. Connect support data to the optimization loop

Run the `support-churn-correlation` drill to build a continuous feedback loop between support data and proactive outreach:

- Monthly: Recalibrate which support ticket patterns correlate with churn. Feed new signals back into the struggle signal detection workflow (see instructions below) scoring weights.
- Weekly: Analyze new support tickets from users who were proactively outreached. If outreached users still file tickets about the SAME workflow they were helped with, the outreach content is not working for that workflow. The optimization loop should flag this as a priority experiment.
- Weekly: Analyze support tickets from users who were NOT outreached (cooldown-suppressed or below threshold). If these tickets could have been prevented by outreach, consider lowering the detection threshold for that workflow.
- Monthly: Update the struggle-to-help-resource mapping based on new support resolution approaches. When support agents find better ways to resolve common issues, propagate those fixes into the proactive outreach templates.

### 4. Build the self-healing detection layer

The Durable-specific capability: the system automatically adapts when the product changes:

**New struggle pattern detection:**
When the `autonomous-optimization` detects a spike in "unmapped workflow" struggles (users flagged with a `primary_stuck_workflow` that has no help resource mapping), the agent:
1. Extracts the common error messages and failure modes from PostHog
2. Checks if a relevant Intercom help article already exists
3. If yes: adds it to the mapping automatically
4. If no: creates an Attio task to write a help article, and in the meantime, generates a temporary generic help message for that workflow using the Anthropic API

**Stale content detection:**
When the resolution rate for a specific workflow drops below its 4-week average by >20%, the agent:
1. Checks if the linked help article has been updated recently
2. Checks if the product area changed (new deploy, UI change, API change)
3. If the product changed but the help content did not: flags the help resource as stale and creates a task to update it
4. Generates an interim updated outreach message based on the current product state

**Scoring drift correction:**
When the detection precision drops below 50% (too many false positives), the agent:
1. Analyzes which struggle signal types contribute most to false positives
2. Proposes revised scoring weights
3. Runs a 1-week test with the revised weights on a 10% sample
4. If precision improves without recall dropping: adopts the new weights

### 5. Evaluate sustainability

Measure against: sustained or improving ≥45% engagement and ≥20pp retention lift over 6 months.

This level runs continuously. Monthly review:
- Is the optimization loop finding improvements? (experiment win rate, cumulative metric improvement)
- Is the system self-healing? (new struggle patterns getting mapped, stale content getting flagged)
- Are support tickets trending down? (the play's ultimate impact on the support team)
- Is the system converging? (successive experiments producing <2% improvement = local maximum reached)

At convergence:
1. Reduce optimization loop frequency from weekly to biweekly
2. Maintain the health monitor at daily frequency (detect regressions)
3. Report: "Proactive outreach is optimized. Current performance: [engagement rate], [retention lift], [tickets deflected/month]. Further gains require product-level fixes to the highest-struggle workflows, not outreach optimization."

## Time Estimate

- 15 hours: Deploy and validate proactive-outreach-health-monitor
- 20 hours: Deploy and configure autonomous-optimization loop with play-specific guardrails
- 15 hours: Set up support-churn-correlation feedback loop
- 10 hours: Build self-healing detection layer (new pattern detection, stale content detection, scoring drift correction)
- 90 hours: Ongoing monitoring, experiment review, and system maintenance over 6 months (approximately 4 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Struggle detection, experiments, dashboards, session recordings | Free tier: 1M events/mo; Paid: from $0 — https://posthog.com/pricing |
| Intercom | In-app messages, help articles, support ticket data | Starter: $74/mo; Pro varies — https://www.intercom.com/pricing |
| Loops | Triggered outreach emails, A/B variant delivery | Starter: $49/mo — https://loops.so/pricing |
| n8n | Optimization loop scheduling, routing, webhook processing | Cloud: from $24/mo — https://n8n.io/pricing |
| Attio | CRM records, task management, campaign tracking, signal storage | Free tier; Pro: $34/user/mo — https://attio.com/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, content generation | Claude Sonnet: $3/$15 per 1M tokens — https://www.anthropic.com/pricing |

## Drills Referenced

- `autonomous-optimization` — The always-on monitor/diagnose/experiment/evaluate/implement loop that finds the local maximum
- `autonomous-optimization` — Play-specific monitoring of the full detection-to-retention pipeline with daily checks and weekly health briefs
- `support-churn-correlation` — Continuous feedback loop connecting support ticket patterns to struggle detection and outreach effectiveness
