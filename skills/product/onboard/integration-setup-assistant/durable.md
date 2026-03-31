---
name: integration-setup-assistant-durable
description: >
  Integration Setup Assistant -- Durable Intelligence. Always-on AI agents
  autonomously optimize the integration wizard: detect metric anomalies,
  generate improvement hypotheses, run A/B experiments, evaluate results,
  and auto-implement winners. Converges when successive experiments produce
  <2% improvement.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving >=60% integration completion rate over 6 months via autonomous AI optimization"
kpis: ["Integration completion rate (sustained)", "Experiment velocity (experiments/month)", "AI lift (cumulative improvement from AI-run experiments)", "Time to convergence", "Per-persona completion rate stability"]
slug: "integration-setup-assistant"
install: "npx gtm-skills add product/onboard/integration-setup-assistant"
drills:
  - autonomous-optimization
  - integration-health-monitor
---

# Integration Setup Assistant -- Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Sustained or improving >=60% integration completion rate over 6 months. An AI agent autonomously monitors all integration wizard metrics, detects anomalies, generates hypotheses for improvement, runs controlled A/B experiments, evaluates results, and auto-implements winners. The agent converges on the local maximum -- the best achievable completion rate given current integrations, user mix, and product capabilities. Weekly optimization briefs report what changed and why.

## Leading Indicators

- Autonomous optimization loop running without human intervention for 4+ consecutive weeks
- Experiment velocity: 2-4 experiments completed per month
- Cumulative AI lift: >=5pp improvement over Scalable baseline after 3 months
- Anomaly detection catching issues within 24 hours (no metric drops lasting >1 week undetected)
- Convergence approaching: successive experiments producing <5% improvement (on track for <2% threshold)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the integration wizard. This is the core of Durable -- the drill that makes this level fundamentally different from Scalable. Configure it as follows:

**Phase 1 -- Monitor (daily via n8n cron at 08:00 UTC):**
The agent checks the integration wizard's primary KPIs daily using PostHog:
- Overall wizard completion rate (last 7 days vs 4-week rolling average)
- Per-persona completion rates
- Per-integration success rates
- Rescue recovery rate
- Time to first integration (median)

Classify each metric: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase). If any metric is anomalous, trigger Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**
The agent gathers context from PostHog and Attio:
- Pull the integration wizard's current configuration from Attio: persona definitions, checklist content, bot flows, email sequences, A/B test history
- Pull 8-week metric history from PostHog dashboards
- Run hypothesis generation with the anomaly data + context

The agent generates 3 ranked hypotheses for the anomaly. Example hypotheses for common anomaly types:

*Completion rate drop:*
1. "Checklist step 2 ([Integration]) failure rate spiked 40% -- likely the third-party changed their OAuth flow. Fix: update the auth redirect URL and bot guidance."
2. "New signup cohort has different persona mix -- 60% business_user vs historical 40%. Fix: re-weight integration priority for business_user persona."
3. "Rescue email click rate dropped 50% -- likely email fatigue. Fix: A/B test new subject lines and reduce email frequency."

*Completion rate plateau:*
1. "All high-impact wizard changes have been tested. Test deeper changes: reorder integration priority per persona based on last 30 days of retention data."
2. "Time to connect for [Integration 2] is 3x longer than others. Test: pre-fill configuration fields using enrichment data from signup."
3. "Rescue workflow only reaches users who stall >24h. Test: fire rescue messages at 6h instead of 24h."

Store hypotheses in Attio. If the top hypothesis is flagged "high risk" (affects >50% of users or involves removing an integration), send a Slack alert for human review and STOP.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
The agent designs and runs the experiment:
1. Take the top-ranked hypothesis
2. Create a PostHog experiment: feature flag splits traffic between control and variant
3. Implement the variant:
   - For checklist changes: update Intercom checklist audience rules
   - For bot changes: update Intercom bot flow
   - For email changes: create a variant email in Loops
   - For timing changes: update n8n workflow schedules
   - For integration priority changes: update persona configuration
4. Set experiment duration: minimum 7 days OR 200+ users per variant, whichever is longer
5. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 -- Evaluate (triggered by experiment completion):**
The agent pulls results from PostHog and runs experiment evaluation:
- **Adopt** (statistically significant improvement, p<0.05): update the live configuration to the winning variant. Log the change with effect size and confidence.
- **Iterate** (improvement trend but not significant): generate a new hypothesis building on this result. Return to Phase 2.
- **Revert** (no improvement or negative): disable the variant, restore control. Log the failure. Return to Phase 1.
- **Extend** (promising but insufficient sample): keep running for another cycle.

Store the full evaluation in Attio: decision, confidence interval, reasoning, and configuration change applied.

**Phase 5 -- Report (weekly, Mondays via n8n cron):**
The agent generates a weekly optimization brief:

```
# Integration Wizard Optimization Brief -- Week of [date]

## Summary
- Active experiments: [N]
- Experiments completed this week: [N]
- Decisions: [N adopted, N reverted, N extended]
- Net completion rate change this week: [+/-X pp]

## Current Performance
- Overall completion rate: [X%] (Scalable baseline: [Y%], AI lift: [+Z pp])
- Best persona: [persona] at [rate%]
- Worst persona: [persona] at [rate%]

## Experiment Results
| Experiment | Hypothesis | Result | Decision | Effect |
|-----------|-----------|--------|----------|--------|
| [name]    | [summary] | [+/-X pp, p=Y] | [adopt/revert/extend] | [description] |

## Convergence Status
- Experiments in last 4 weeks: [N]
- Average improvement per experiment: [X pp]
- Convergence: [approaching (<5% avg) / not yet (>5% avg) / converged (<2% for 3 consecutive)]

## Next Steps
- [Queued hypothesis or recommended focus area]
```

Post the brief to Slack and store in Attio.

### 2. Deploy continuous integration health monitoring

Run the `integration-health-monitor` drill to maintain the monitoring infrastructure from Scalable level. At Durable, this drill's anomaly output is the primary input to the autonomous-optimization loop:

- Daily health checks at 08:00 UTC feed anomalies directly to Phase 1 of the optimization loop
- Weekly health reports provide context for Phase 2 hypothesis generation
- Third-party integration change detection triggers immediate triage (not experimentation -- fix the broken integration first, then resume optimization)
- Per-integration failure cohorts provide targeting data for experiments

The health monitor and autonomous optimization loop work together: the monitor detects the problem, the optimizer fixes it.

### 3. Configure guardrails

Set these guardrails for the autonomous optimization loop:

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments.
- **Revert threshold:** If completion rate drops >20% at any point during an experiment, auto-revert immediately and alert the team.
- **Human approval required for:**
  - Removing an integration from any persona's default checklist
  - Changing persona classification logic
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize what is not measured:** If a change requires new PostHog events, implement tracking first (minimum 1 week of baseline data) before running experiments.

### 4. Monitor convergence

The optimization loop runs indefinitely. The agent detects **convergence** when successive experiments produce diminishing returns:

- Track the improvement from each experiment over the last 12 weeks
- If 3 consecutive experiments produce <2% improvement each, the play has reached its local maximum
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment velocity from 2-4/month to 1/month (maintenance experiments)
  3. Generate a convergence report: "Integration wizard has reached its local maximum at [X%] completion rate. Further gains require strategic changes (new integrations, product changes, or new user acquisition channels) rather than tactical optimization of the existing wizard."
  4. Post the convergence report to Slack and store in Attio

Even after convergence, maintain weekly monitoring to detect regressions from external changes (third-party API changes, user mix shifts, product updates).

### 5. Evaluate sustainability

After 6 months, assess the Durable level:

- **Primary metric:** Integration completion rate sustained at >=60% for 6 consecutive months
- **AI lift:** Total improvement attributable to autonomous experiments (sum of adopted experiment effects)
- **Experiment log:** Complete record of every experiment run, its hypothesis, result, and decision
- **Convergence status:** Has the wizard reached its local maximum? If so, at what rate?
- **Operational cost:** Total compute and tool costs for running the optimization loop

If sustained: the play is durable. Continue running the optimization loop at maintenance cadence. Report: "Integration Setup Assistant is operating autonomously. Current completion rate: [X%]. AI lift: [+Y pp]. Convergence: [status]."

If not sustained (rate drops below 60% for 2+ consecutive months despite active optimization): diagnose whether the issue is tactical (fixable via experiments) or strategic (requires product changes, new integrations, or different user acquisition). If strategic, escalate to the product team with specific data and recommendations.

## Time Estimate

- 20 hours: Autonomous optimization loop setup and initial tuning (Step 1)
- 8 hours: Health monitoring deployment and integration (Step 2)
- 4 hours: Guardrail configuration and testing (Step 3)
- 8 hours/month: Monitoring, reviewing weekly briefs, approving high-risk experiments (Steps 4-5)
- Total ongoing: ~8 hours/month for 6 months = 48 hours ongoing + 32 hours setup = ~80 hours active work

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, dashboards, anomaly detection, cohorts | Usage-based: ~$0.00005/event; volume discounts at scale ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Checklists, bots, in-app messages (per-persona variants) | Advanced: $85/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| n8n | Optimization loop scheduling, monitoring workflows, event sync | Cloud Pro: $60/mo ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Loops | Behavioral email sequences (per-persona variants) | Starter: $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | Usage-based: ~$15/1M input tokens, ~$75/1M output tokens ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Estimated play-specific cost at Durable:** ~$200-400/mo (Intercom Advanced + n8n Pro + Loops + Anthropic API for hypothesis generation, ~$10-30/mo at 2-4 experiments/month)

## Drills Referenced

- `autonomous-optimization` -- the core always-on loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- `integration-health-monitor` -- continuous per-integration monitoring with anomaly alerts, weekly reports, and third-party change detection that feeds into the optimization loop
