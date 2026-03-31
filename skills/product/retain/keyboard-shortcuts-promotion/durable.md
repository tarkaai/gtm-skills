---
name: keyboard-shortcuts-promotion-durable
description: >
  Power User Features — Durable Intelligence. Autonomous AI agent monitors shortcut
  adoption metrics, detects anomalies, generates improvement hypotheses, runs A/B
  experiments, and auto-implements winners. Converges when successive experiments
  produce <2% improvement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "20 hours setup + ongoing autonomous operation over 6 months"
outcome: "Shortcut ratio sustained or improving >=25% over 6 months via autonomous optimization; convergence detected when <2% improvement for 3 consecutive experiments"
kpis: ["Shortcut ratio (weekly trend)", "Experiment velocity (experiments completed per month)", "Cumulative AI lift (total improvement from auto-implemented changes)", "Time to convergence (weeks until optimization plateaus)", "Retention delta (shortcut adopters vs non-adopters)"]
slug: "keyboard-shortcuts-promotion"
install: "npx gtm-skills add product/retain/keyboard-shortcuts-promotion"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Power User Features — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

An autonomous AI agent runs the complete shortcut promotion system without human intervention. It monitors all shortcut adoption metrics daily, detects when performance plateaus or drops, generates hypotheses for improvement, designs and runs A/B experiments via PostHog, evaluates results, and auto-implements winners. Weekly optimization briefs summarize what changed and why. The system converges toward the local maximum — the best achievable shortcut adoption rate given the current product, user base, and shortcut set.

## Leading Indicators

- Autonomous monitoring loop firing daily without errors
- Anomalies detected and diagnosed within 24 hours of occurrence
- Experiments launched automatically when hypotheses are generated
- Winners auto-implemented without human intervention (for low/medium risk changes)
- Weekly optimization briefs generated and posted on schedule
- Experiment improvement deltas declining over time (approaching convergence)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to configure the core loop for this play. Adapt it specifically for shortcut promotion:

**Phase 1 — Monitor (daily via n8n cron):**

Configure the anomaly detection to watch these specific metrics:
- Overall shortcut ratio (primary KPI)
- Shortcut ratio by persona segment (technical builder, team lead, casual)
- Hint-to-trial conversion rate
- Hint-to-habitual conversion rate
- Stalled-user percentage
- Shortcut-specific adoption rates for each of the 6-8 promoted shortcuts

Use `posthog-anomaly-detection` to compare last 2 weeks against 4-week rolling average. Classify each metric as normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), or spike (>50% increase).

If any metric triggers an anomaly -> proceed to Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**

The agent gathers context:
1. Pull current shortcut promotion configuration from Attio: active hint copy, timing rules, persona assignments, frequency caps, active interventions
2. Pull 8-week metric history from PostHog dashboards
3. Pull the last 4 experiment results and their outcomes
4. Run `hypothesis-generation` with the anomaly data + context

Example hypotheses the agent might generate:
- "Shortcut ratio plateaued because the hint frequency cap (1/session) is too conservative for high-activity users. Hypothesis: Increase cap to 2/session for users with 10+ sessions/week. Expected impact: +3-5pp shortcut ratio for power segment."
- "Cmd+Enter shortcut adoption dropped 25% because a recent product update changed the submit flow. Hypothesis: Update the hint to reference the new submit location. Expected impact: restore previous adoption rate."
- "Casual user segment shortcut ratio has been flat at 8% for 6 weeks. Hypothesis: Replace tooltip hints with a weekly 'shortcut of the week' Loops email for this segment. Expected impact: +5pp shortcut ratio for casual segment."

If the top hypothesis is high-risk (affects >50% of users or changes a core interaction pattern) -> send Slack alert for human review and STOP. Otherwise, proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

The agent designs the experiment:
1. Creates a PostHog feature flag splitting traffic between control (current) and variant (hypothesis change)
2. Implements the variant: if the hypothesis involves hint copy, update the Intercom message; if it involves timing, adjust the n8n workflow; if it involves a new channel (email), create a new Loops sequence
3. Sets experiment duration: minimum 7 days or 100+ samples per variant, whichever is longer
4. Logs the experiment in Attio: hypothesis, start date, expected duration, success criteria

**Rate limit:** Maximum 1 active experiment at a time. Never stack experiments.

**Phase 4 — Evaluate (triggered by experiment completion):**

The agent evaluates:
1. Pulls experiment results from PostHog
2. Runs `experiment-evaluation` with control vs variant data
3. Decides:
   - **Adopt:** Variant wins with 95% confidence and practical significance (>=3pp improvement on target metric). Auto-implement. Update the live configuration.
   - **Iterate:** Results inconclusive or marginal (<3pp). Generate a refined hypothesis. Return to Phase 2.
   - **Revert:** Variant loses or causes negative secondary effects (retention drop, support ticket increase). Disable variant, restore control. Log the failure.
   - **Extend:** Not enough data yet. Continue for another 7 days.

**Revert threshold:** If shortcut ratio drops >30% at any point during an experiment, auto-revert immediately.

**Phase 5 — Report (weekly via n8n cron):**

Generate a weekly optimization brief:
- Anomalies detected this week and their diagnoses
- Experiments running, completed, or reverted
- Net metric change from adopted changes
- Current shortcut ratio by segment with trend arrows
- Distance from estimated local maximum (based on diminishing returns curve)
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Configure play-specific guardrails

Beyond the standard `autonomous-optimization` guardrails, add these shortcut-specific constraints:

- **Hint annoyance guardrail:** If hint dismissal rate exceeds 80% for any shortcut, auto-disable hints for that shortcut and flag for review. Users are telling you the hint is unwelcome.
- **Retention guardrail:** If the treatment group's 7-day retention drops below the control group's by more than 2pp at any point, pause all experiments and alert the team. The promotion system may be harming retention.
- **Shortcut validity guardrail:** If a product update changes or removes a keyboard shortcut, the agent must detect the change (shortcut usage drops to 0 but mouse usage stays constant) and auto-disable hints for that shortcut within 24 hours.
- **Persona balance guardrail:** Never let optimization for one persona segment degrade another. If improving casual user shortcut ratio causes power user hint dismissal to spike, revert.

### 3. Build the executive shortcut health dashboard

Run the `dashboard-builder` drill to create a comprehensive dashboard for ongoing monitoring:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Shortcut ratio trend (6 months) | Line chart with target line at 25% | Primary health metric, long-term trend |
| Shortcut ratio by persona | Grouped line chart | Per-segment performance divergence |
| Experiment timeline | Gantt-style chart | Visualize experiment cadence and outcomes |
| Cumulative AI lift | Cumulative area chart | Total improvement from all auto-implemented changes |
| Convergence indicator | Gauge chart | Last 3 experiment deltas — approaching convergence if all <2% |
| Time saved (aggregate weekly) | Bar chart | Business value delivered to users |
| Retention delta | Line chart | Shortcut adopters vs non-adopters retention gap |
| Anomaly log | Table | Recent anomalies with status: detected, diagnosed, experimenting, resolved |

Set alerts for:
- Shortcut ratio dropping below 20% (critical — 5pp below target)
- No experiments completed in 3+ weeks (optimization stalled)
- Convergence detected (3 consecutive experiments with <2% improvement)
- Retention delta narrowing (shortcut adoption losing its retention advantage)

### 4. Detect and handle convergence

The autonomous optimization loop runs indefinitely, but it should detect convergence — when the shortcut promotion system has reached its local maximum:

**Convergence criteria:** 3 consecutive experiments produce <2% improvement on the target metric.

When convergence is detected:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment cadence from continuous to monthly spot-checks
3. Generate a convergence report: "Shortcut promotion has reached its local maximum. Current shortcut ratio: X%. Retention delta: Y pp. Total time saved per week: Z hours. Further gains require strategic changes — new shortcuts, product redesign, or fundamentally different promotion mechanisms — rather than tactical optimization."
4. The agent continues monitoring for regressions (metric drops >10% from converged baseline trigger full re-optimization)

### 5. Monthly strategic review

The agent generates a monthly strategic review (distinct from the weekly optimization brief):

- Month-over-month shortcut ratio trend
- Experiments run, adopted, reverted, and their cumulative impact
- Per-shortcut analysis: which shortcuts are fully adopted, which are still gaining, which should be retired from promotion
- Persona segment performance: which segments are optimized, which have room to grow
- Recommendation: continue autonomous optimization, shift focus to a different persona, or declare convergence
- Cost analysis: PostHog events used, Intercom messages sent, n8n workflow executions

**Human action required:** Review the monthly strategic report. Approve or override the agent's recommendation. If the agent recommends adding new shortcuts or changing the shortcut set, that requires a product decision before the agent can act on it.

## Time Estimate

- 8 hours: configure autonomous optimization loop (adapt all 5 phases for shortcut promotion)
- 4 hours: configure play-specific guardrails and anomaly detection rules
- 4 hours: build executive dashboard and convergence detection
- 4 hours: test the full loop end-to-end (trigger an anomaly, verify hypothesis generation, verify experiment creation)
- Ongoing: autonomous operation with weekly briefs and monthly reviews

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards | Usage-based: $0.00005/event; likely $50-200/mo at scale ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Automated in-app messages, updated by experiment results | Essential: $29/seat/mo; Proactive Support Plus if high-volume: $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Stalled-user sequences updated by experiment results | From $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Daily monitoring cron, experiment orchestration, weekly/monthly reporting | Self-hosted: free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, report writing | Claude: ~$15/MTok input, ~$75/MTok output; est. $20-50/mo for this play ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Estimated play-specific cost at this level:** $150-500/mo depending on scale and Intercom plan

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate-report loop that makes Durable fundamentally different; detects metric anomalies, generates improvement hypotheses, runs A/B experiments, auto-implements winners, and produces weekly optimization briefs
- `autonomous-optimization` — ongoing adoption funnel tracking, stalled-user detection, efficiency gain calculations feeding into the optimization loop
- `dashboard-builder` — executive dashboard with convergence indicator, experiment timeline, and retention delta tracking
