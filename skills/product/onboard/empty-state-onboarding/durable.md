---
name: empty-state-onboarding-durable
description: >
  Empty State Guidance — Durable Intelligence. AI agent continuously monitors all empty
  state surfaces, detects anomalies and new untreated surfaces, generates improvement
  hypotheses, runs A/B experiments, and auto-implements winners. Sustains or improves
  CTR >=45% over 6 months via autonomous optimization.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Empty state CTR sustained or improving at >=45% over 6 months via autonomous AI optimization"
kpis: ["Empty state CTR (aggregate + per-surface)", "Experiment velocity", "Experiment win rate", "AI-attributed lift", "Convergence status", "Untreated surface detection rate"]
slug: "empty-state-onboarding"
install: "npx gtm-skills add product/onboard/empty-state-onboarding"
drills:
  - autonomous-optimization
---

# Empty State Guidance — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

An always-on AI agent monitors every empty state surface, detects metric anomalies and untreated new surfaces, generates improvement hypotheses, runs A/B experiments autonomously, and auto-implements winners. Weekly optimization briefs track progress toward the local maximum. The play sustains or improves 45%+ aggregate CTR over 6 months without manual intervention beyond reviewing weekly briefs.

## Leading Indicators

- Agent detects anomalies within 24 hours of occurrence (no multi-day blind spots)
- Agent generates hypotheses that produce statistically significant improvements in 25%+ of experiments
- Untreated surfaces from new feature launches are flagged within 7 days of shipping
- Weekly optimization brief is generated on schedule with actionable recommendations
- Convergence detection works: when successive experiments produce <2% improvement, the agent correctly identifies the local maximum

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for empty state metrics:

**Monitor phase (daily):**
- Primary KPI: aggregate empty state CTR across all surfaces
- Secondary KPIs: per-surface CTR, per-persona CTR, template selection rate
- Anomaly detection: compare last 2 weeks against 4-week rolling average
- Classification: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)

**Diagnose phase (triggered by anomaly):**
- Pull the current empty state configuration: which surfaces have which CTA copy, templates, persona variants
- Pull 8-week metric history from PostHog
- Generate 3 ranked hypotheses using Claude. Example hypotheses the agent should explore:
  - "Users from the new acquisition channel have different persona distribution — current templates do not match their use case"
  - "The CTA copy on [surface X] has fatigued after 12 weeks — testing fresh copy will recover 5-10% CTR"
  - "Template [Y] has declined in selection rate — replacing with a template matching current user trends will improve conversion"
  - "Mobile CTR is 15pp below desktop on [surface Z] — the CTA is below the fold on mobile, moving it up will close the gap"

**Experiment phase (triggered by hypothesis acceptance):**
- Use PostHog experiments to split traffic on the target surface
- Minimum 7 days or 100+ users per variant, whichever is longer
- One active experiment per surface at a time (never stack experiments on the same surface)
- Log the experiment in Attio with hypothesis, start date, expected duration, and success criteria

**Evaluate phase (triggered by experiment completion):**
- Pull results from PostHog
- Decision: Adopt (winner improves CTR by 2%+), Iterate (inconclusive, refine hypothesis), Revert (variant lost), Extend (insufficient sample size)
- Auto-implement winners by updating the feature flag configuration

**Report phase (weekly):**
- Generate the weekly optimization brief (see Step 3)

### 2. Deploy the empty state health monitor

Run the `autonomous-optimization` drill to set up:

**Daily health check (8 AM):**
- Query all empty state surface metrics
- Classify each surface as Healthy / Warning / Critical
- Alert on Critical surfaces immediately
- Log all results in Attio

**Weekly untreated surface detection (Monday 7 AM):**
- Compare `page_viewed` routes against known `empty_state_viewed` surfaces
- Flag any route with 50+ unique users and no empty state tracking
- Create a task in Attio for the product team to design the empty state for each flagged surface

**This is what makes Durable different from Scalable:** At Scalable, a human reviews metrics and decides what to test. At Durable, the agent detects the anomaly, proposes the fix, runs the test, evaluates the result, and implements the winner — all autonomously. The human reviews the weekly brief and intervenes only when the agent flags high-risk changes.

### 3. Configure the weekly optimization brief

The agent generates a weekly brief every Monday at 9 AM. Structure:

```
EMPTY STATE OPTIMIZATION BRIEF — WEEK OF [DATE]

OVERALL HEALTH
- Aggregate CTR: [X%] (target: 45%) [UP/DOWN/FLAT vs last week]
- Surfaces monitored: [N]
- Surfaces in Critical status: [N]

AUTONOMOUS ACTIONS THIS WEEK
- Anomalies detected: [N] ([surface names])
- Hypotheses generated: [N]
- Experiments launched: [N]
- Experiments completed: [N]
- Winners implemented: [N] (net CTR impact: [+/-X%])

EXPERIMENT DETAILS
- [Surface A]: Tested [variable]. Result: [winner/loser/inconclusive].
  Lift: [X%], Confidence: [Y%]. Action: [Adopted/Reverted/Extended].

UNTREATED SURFACES
- [Route path] — [N] users/week, no empty state treatment.
  Recommendation: [design priority and template suggestions].

CONVERGENCE STATUS
- Experiments producing >2% improvement: [X of Y] in last 4 weeks
- Status: [Converging / Not converging / Converged]
- If converged: "Further gains require product changes, not empty state optimization."

HUMAN REVIEW NEEDED (if any)
- [Description of high-risk hypothesis awaiting approval]
```

Post the brief to Slack and store in Attio.

### 4. Set up guardrails

Configure these guardrails in the autonomous optimization loop:

- **Revert threshold:** If any surface's CTR drops >30% during an experiment, auto-revert immediately and alert the team.
- **Human approval required for:** Changes to P0 surfaces that affect >50% of traffic. Any hypothesis flagged as "high risk" by the agent (e.g., removing templates, changing the CTA to a different action).
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable on the same surface.
- **Experiment cap:** Maximum 4 experiments per surface per month. If all 4 fail, pause and flag for human strategic review.
- **Overall CTR floor:** If aggregate CTR drops below 40% for 2 consecutive weeks, pause all experiments and alert the team. The priority shifts from optimization to diagnosis.

### 5. Monitor and review monthly

**Human action required (monthly):** Review the accumulated weekly briefs. Assess:
- Is aggregate CTR sustaining above 45%? If declining, check whether the user mix changed or whether specific surfaces degraded.
- Is the agent finding productive experiments? If win rate drops below 25% for 2 consecutive months, the play may be approaching its local maximum.
- Are untreated surfaces getting designed? If the backlog is growing, allocate engineering time to implement new empty state designs.
- Are there strategic changes (new product features, new user personas, new acquisition channels) that require manual empty state redesign rather than incremental optimization?

### 6. Detect convergence

The autonomous optimization loop should detect convergence — when incremental experiments stop producing meaningful improvement. Convergence criteria:
- 3 consecutive experiments produce <2% improvement each
- Aggregate CTR has been within +/-2% for 8 consecutive weeks
- All persona CTR variants are within 5pp of each other

When converged:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment velocity from 2/month to 1/month (maintenance experiments only)
3. Report: "Empty state optimization has converged at [X%] CTR. Current performance is the local maximum. Further improvement requires product changes: new features, new onboarding flows, or changes to the activation metric."

## Time Estimate

- 20 hours: Configure and deploy the autonomous optimization loop (one-time)
- 10 hours: Deploy the empty state health monitor and untreated surface detection (one-time)
- 5 hours: Configure guardrails and the weekly brief template (one-time)
- 8 hours/month: Review weekly briefs, approve high-risk experiments, design new empty states for untreated surfaces (ongoing, ~2h/week)
- Total ongoing: ~48 hours over 6 months for human oversight
- Agent runs continuously: daily monitoring, experiment management, weekly reporting

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, experiments, feature flags, dashboards, session recordings | Paid: ~$0.00005/event; at 500K events/mo ~$25/mo. [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Scheduling optimization loops, health checks, report generation | Pro: ~$60/mo (cloud) for 10K executions. [n8n.io/pricing](https://n8n.io/pricing/) |
| Intercom | In-app messages for persona-targeted empty states | Essential: $29/seat/mo (annual). [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Lifecycle email bridge maintenance | $49/mo for up to 5,000 contacts. [loops.so/pricing](https://loops.so/pricing) |
| Anthropic API | Claude for hypothesis generation and experiment evaluation | ~$15/1M input tokens; ~$75/1M output tokens. Estimated ~$10-20/mo for weekly optimization loop. [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost at this level:** $175-350/mo (PostHog + n8n Pro + Intercom + Loops + Anthropic API)

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor, diagnose, experiment, evaluate, implement, report
- `autonomous-optimization` — play-specific monitoring: per-surface health checks, untreated surface detection, weekly reports
