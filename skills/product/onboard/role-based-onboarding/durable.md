---
name: role-based-onboarding-durable
description: >
  Persona-Based Onboarding — Durable Intelligence. AI agents autonomously monitor per-persona
  activation rates, detect anomalies, generate improvement hypotheses, run A/B experiments, and
  auto-implement winners. Weekly optimization briefs. Converges when successive experiments
  produce <2% improvement.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "80 hours over 6 months"
outcome: "Sustained or improving activation ≥50% across all personas over 6 months via autonomous optimization"
kpis: ["Activation rate by persona", "Experiment velocity", "Cumulative AI lift", "Anomaly detection latency", "Convergence status per persona"]
slug: "role-based-onboarding"
install: "npx gtm-skills add product/onboard/role-based-onboarding"
drills:
  - autonomous-optimization
  - onboarding-health-monitor
---

# Persona-Based Onboarding — Durable Intelligence

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Activation rate sustains or improves ≥50% across all personas over 6 months. An AI agent autonomously runs the detect → diagnose → experiment → evaluate → implement loop. The agent generates weekly optimization briefs summarizing what changed, what improved, and what to focus on next. The agent converges each persona when successive experiments produce <2% improvement, signaling the local maximum has been reached.

## Leading Indicators

- Anomaly detection latency: agent detects metric drops within 24 hours (daily monitoring cycle)
- Experiment velocity: 2-4 experiments completed per month across all personas
- Win rate: ≥40% of experiments produce a statistically significant improvement
- Cumulative AI lift: total activation rate improvement from agent-implemented changes is measurable and growing
- No persona's activation rate drops >20% below its Scalable baseline for more than 2 consecutive weeks without agent intervention
- Convergence: at least one persona reaches local maximum (3 consecutive experiments with <2% improvement)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. Configure the loop for this play:

**Phase 1 — Monitor (daily via n8n cron):**

Build an n8n workflow triggered daily at 08:00 UTC:
1. Use `posthog-anomaly-detection` to check per-persona KPIs: activation rate, tour completion rate, email engagement, time to activation
2. Compare last 2 weeks against 4-week rolling average for each persona independently
3. Classify each persona: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If all personas normal: log to Attio, no action
5. If any persona has an anomaly: trigger Phase 2 for that specific persona

**Phase 2 — Diagnose (triggered by anomaly):**

1. Gather context for the anomalous persona: current tour configuration, email sequence content, classification rules, in-app message triggers
2. Pull 8-week metric history from PostHog for this persona only
3. Run `hypothesis-generation` with the anomaly data + persona context
4. Receive 3 ranked hypotheses. Example hypothesis types for this play:
   - "Tour step 3 has a 45% drop-off — simplify the interaction from 'create and configure' to 'create from template'"
   - "Email 2 open rate dropped 15% — subject line fatigue, test new subject line variant"
   - "Persona classification shifted — 20% more users classified as 'team_lead' but activation stayed flat — check if classification is misassigning solo users"
   - "Time to activation increased 30% — external factor (holiday) or product change broke a tour step"
5. Store hypotheses in Attio
6. If top hypothesis risk = "high": send alert for human review and STOP
7. If risk = "low" or "medium": proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

1. Take the top-ranked hypothesis for the anomalous persona
2. Design the experiment using `posthog-experiments`: create a feature flag splitting that persona's traffic between control and variant
3. Implement the variant:
   - Tour change: create variant tour in Intercom, route via feature flag
   - Email change: create variant sequence in Loops, route via Loops audience segment
   - In-app message change: create variant message in Intercom with targeting rules
   - Classification change: update n8n classification rules for the variant group
4. Set experiment duration: minimum 7 days or until 100+ users per variant, whichever is longer
5. Log experiment start in Attio: hypothesis, persona, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**

1. Pull experiment results from PostHog for the specific persona
2. Run `experiment-evaluation` with control vs variant data
3. Decision:
   - **Adopt**: Variant wins. Update the live configuration: roll the winning tour/email/message to 100% of this persona. Log the change and the metric impact.
   - **Iterate**: Result directionally positive but not significant. Generate a refined hypothesis and return to Phase 2.
   - **Revert**: Variant lost. Disable variant, restore control. Log the failure. Return to Phase 1 monitoring.
   - **Extend**: Insufficient sample size. Keep running for another week.
4. Store the full evaluation in Attio: decision, confidence interval, net metric change, reasoning

**Phase 5 — Report (weekly via n8n cron, Mondays at 09:00 UTC):**

1. Aggregate all optimization activity across all personas for the week
2. Calculate: net metric change from all adopted changes
3. Generate the weekly optimization brief:
   - Per-persona status: normal / optimizing / converged
   - Anomalies detected and how they were handled
   - Experiments: running, completed, adopted, reverted
   - Net activation rate change from agent-implemented improvements
   - Distance from estimated local maximum per persona (based on diminishing returns trend)
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 2. Deploy the onboarding health monitor

Run the `onboarding-health-monitor` drill. This provides the monitoring infrastructure that feeds the autonomous optimization loop:

**Per-persona health dashboard**: Build a PostHog dashboard with activation rate trends, tour completion, email engagement, persona classification distribution, and drop-off heatmap per persona. This is the visual layer that humans use to verify the agent's work.

**Daily health check**: n8n workflow that queries PostHog for per-persona metrics, compares against rolling averages, classifies anomalies, and sends alerts for critical issues. This runs in parallel with the autonomous optimization monitor — it covers metrics the optimization loop does not (like classification drift, which is a systemic issue, not a per-persona experiment).

**Weekly health report**: Structured report with per-persona breakdown, anomalies detected, experiments in flight, and recommended actions. This report complements the optimization brief — the health report covers the full picture while the optimization brief focuses on experiment outcomes.

**Cohort drift detection**: Weekly comparison of this week's signup cohort against historical averages. If the profile of new signups shifts (different persona mix, different signup sources), flag it. Cohort drift means the current onboarding paths may no longer match the incoming users — this requires strategic adjustment, not tactical A/B testing.

### 3. Configure guardrails

Apply the `autonomous-optimization` drill's guardrails to this play:

- **Rate limit**: Maximum 1 active experiment per persona at a time. With 5+ personas, up to 5 experiments can run simultaneously (one each).
- **Revert threshold**: If any persona's activation rate drops >30% during an experiment, auto-revert immediately and alert the team.
- **Human approval required for:**
  - Changes to persona classification rules (affects all new users)
  - Changes to the activation metric definition for any persona
  - Any experiment the hypothesis generator flags as "high risk"
  - Merging or splitting persona segments
- **Cooldown**: After a failed experiment, wait 7 days before testing a new hypothesis on the same variable for the same persona.
- **Monthly cap**: Maximum 4 experiments per persona per month. If all 4 fail for any persona, pause optimization for that persona and flag for human strategic review.
- **Never optimize what is not measured**: If a persona's tour does not have step-level tracking, fix tracking first before running experiments on that tour.

### 4. Monitor for convergence

The agent detects convergence per persona: when 3 consecutive experiments produce <2% improvement, that persona has reached its local maximum. At convergence:

1. Reduce monitoring frequency for that persona from daily to weekly
2. Report: "Persona [X] onboarding is optimized. Current activation rate: [Y%]. Further gains require strategic changes (new activation metric, new channel, product changes) rather than tactical optimization."
3. Shift experiment capacity to non-converged personas

When all personas converge, the play is at its local maximum. The agent maintains monitoring for external changes (product updates, market shifts, cohort drift) that could break convergence.

## Time Estimate

- 12 hours: Setting up the autonomous optimization loop (n8n workflows for all 5 phases)
- 10 hours: Building the onboarding health monitor (dashboard + daily check + weekly report + cohort drift)
- 8 hours: Configuring guardrails and testing the full loop end-to-end
- 50 hours: Ongoing over 6 months — agent runs autonomously, human reviews weekly briefs and handles escalations (~2 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, funnels, dashboards | Free tier: 1M events/mo; ~$50/mo at 2M events ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Product tours + in-app messages (experiment variants) | Essential: $29/seat/mo; Proactive Support Plus: $99/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Email sequence variants per persona | $49/mo for 5K contacts; $149/mo for 20K ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Optimization loop orchestration (daily cron, webhooks) | Standard stack |
| Anthropic API | Hypothesis generation + experiment evaluation via Claude | ~$10-30/mo at 2-4 experiments/month ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Attio | Experiment audit trail, health observations, personas | Standard stack |

**Estimated play-specific cost at this level:** $59-179/mo (Loops $49-149/mo + Anthropic API $10-30/mo; Intercom Proactive Support Plus assumed from Scalable)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect metric anomalies per persona, generate improvement hypotheses, run A/B experiments, evaluate results, auto-implement winners, generate weekly optimization briefs
- `onboarding-health-monitor` — continuous per-persona monitoring with anomaly alerts, cohort drift detection, and weekly health reports feeding the optimization loop
