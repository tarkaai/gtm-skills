---
name: upgrade-prompts-durable
description: >
  In-App Upgrade CTAs — Durable Intelligence. Autonomous optimization loop that
  detects prompt performance changes, generates improvement hypotheses, runs experiments,
  and auto-implements winners to find the local maximum of upgrade prompt revenue.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "20 hours setup + 2 hours/week ongoing"
outcome: "Prompt-attributed MRR sustains or improves for 3+ consecutive months via autonomous optimization"
kpis: ["Monthly prompt-attributed MRR", "Experiment velocity (tests/month)", "Cumulative optimization lift", "Convergence distance", "Prompt fatigue rate"]
slug: "upgrade-prompts"
install: "npx gtm-skills add product/upsell/upgrade-prompts"
drills:
  - autonomous-optimization
  - upgrade-prompt-health-monitor
---

# In-App Upgrade CTAs — Durable Intelligence

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

An AI agent runs the upgrade prompt system autonomously. It monitors prompt performance daily, detects when a trigger type's CTR or conversion declines, generates hypotheses for what to change, runs A/B experiments, evaluates results, and auto-implements winners. Weekly optimization briefs report what changed and why. The system converges toward the local maximum of prompt-attributed revenue and maintains it as user behavior and product features evolve.

## Leading Indicators

- Autonomous experiments running at target velocity of 2-4 per month (confirms the loop is active)
- No manual intervention needed for 4+ consecutive weeks (confirms autonomy)
- Weekly optimization briefs delivered on schedule with actionable content (confirms reporting works)
- Prompt fatigue cohort stable or shrinking (confirms the system is not over-experimenting on users)

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill with these play-specific parameters:

**Primary KPIs to monitor:**
- `upgrade_prompt_clicked / upgrade_prompt_shown` (CTR) per trigger type
- `upgrade_completed / upgrade_prompt_shown` (conversion rate) per trigger type
- Sum of `upgrade_completed.revenue_delta_monthly` (prompt-attributed MRR)

**Anomaly thresholds:**
- Normal: CTR within ±10% of 4-week rolling average
- Plateau: CTR within ±2% for 3+ consecutive weeks
- Drop: CTR declined >20% from 4-week average
- Spike: CTR increased >50% (investigate — could be a bug reducing impressions or a product change driving more trigger events)

**Experiment scope (what the agent can change without human approval):**
- Prompt copy (headline, body text, CTA label)
- Prompt timing (immediate vs delayed, time-of-day)
- Prompt surface (modal vs banner vs tooltip vs inline)
- Email follow-up subject line and send timing
- Segment-specific prompt variants

**Human approval required for:**
- Adding or removing a trigger type
- Changing frequency cap rules (affects all users)
- Changing the upgrade page or pricing (outside this play's scope)
- Any experiment affecting more than 50% of prompt impressions

### 2. Configure the monitoring phase

Using the `autonomous-optimization` drill Phase 1, build an n8n workflow (daily cron, 08:00 UTC) that:

1. Queries PostHog for each trigger type's CTR and conversion rate over the last 7 days
2. Compares against the 4-week rolling average
3. Checks the prompt fatigue cohort size from the `upgrade-prompt-health-monitor` drill
4. Checks revenue attribution trend: is prompt-attributed MRR flat, growing, or declining
5. Classifies the state: normal, plateau, drop, or spike
6. If anomaly detected, triggers Phase 2 (diagnosis)
7. If normal, logs the health check to Attio and moves on

### 3. Configure the diagnosis and experiment phases

Using the `autonomous-optimization` drill Phases 2-4:

**Diagnosis:** When an anomaly is detected, the agent gathers:
- Which trigger type(s) are affected
- The prompt variant currently running for that trigger
- Recent experiment history (what was last changed and when)
- Prompt fatigue cohort growth rate
- Any external factors (product releases, pricing changes, seasonal patterns)

The agent generates 3 ranked hypotheses. Example hypotheses for a CTR drop on feature-gate prompts:
1. "Prompt copy became stale — users have seen the same message too many times. Test a social-proof variant." (low risk)
2. "Prompt timing is wrong — a recent product change moved the feature gate to a different page flow. Adjust trigger location." (medium risk)
3. "Users are experiencing prompt fatigue from cross-trigger exposure. Reduce frequency cap from 7 days to 14 days." (medium risk — affects all users)

**Experiment:** The top hypothesis becomes a PostHog experiment (feature flag with control/variant split). The agent:
- Creates the experiment in PostHog
- Implements the variant (e.g., new prompt copy in Intercom, adjusted timing in n8n)
- Sets minimum duration: 7 days or 200 impressions per variant
- Logs the experiment in Attio with hypothesis, start date, and success criteria

**Evaluation:** When the experiment completes:
- Pull results from PostHog
- If variant wins with ≥95% confidence: adopt the variant, update the live prompt configuration
- If no significant difference: keep the simpler/cheaper variant, log the result, return to monitoring
- If variant loses: revert, log the learning, wait 7-day cooldown before the next experiment on the same trigger

### 4. Configure weekly optimization briefs

Using the `autonomous-optimization` drill Phase 5, the agent generates a weekly brief (every Monday) that includes:

- **This week's metrics:** CTR, conversion rate, and prompt-attributed MRR per trigger type
- **Experiments completed:** hypothesis, result (win/loss/inconclusive), confidence level, impact
- **Experiments in progress:** what is being tested, expected completion date
- **Anomalies detected:** what happened and what action was taken
- **Convergence status:** are successive experiments producing diminishing returns? If 3 consecutive experiments produced <2% improvement, report that this trigger type has likely reached its local maximum
- **Recommendations:** what the agent plans to test next, and any items requiring human decision

Post the brief to Slack and store in Attio as a note on the upgrade-prompts campaign record.

### 5. Maintain the health monitor

The `upgrade-prompt-health-monitor` drill (already deployed from Scalable) continues running in parallel. It provides the data layer that the autonomous optimization loop queries. Ensure:

- Degradation alerts still fire (they serve as a redundant check — the optimization loop also monitors, but the health monitor catches issues the loop might miss during experiment cooldown periods)
- Revenue attribution is accurate (spot-check monthly: does the sum of prompt-attributed upgrades match actual upgrade revenue from billing?)
- Prompt fatigue cohort is reviewed in the weekly brief (the optimization loop should never increase the fatigue rate through over-experimentation)

### 6. Define convergence and steady state

The autonomous optimization loop runs indefinitely. However, it should detect convergence per trigger type:

- **Converged:** 3 consecutive experiments on this trigger type produced <2% improvement. The trigger has reached its local maximum.
- **Action at convergence:** Reduce experiment frequency from continuous to monthly maintenance tests. Reduce monitoring from daily to weekly. Report the converged performance level.
- **Breaking convergence:** If a product change, pricing change, or market shift causes metrics to move >15% from the converged level, re-enter active optimization mode.

When ALL trigger types converge, the play is at its local maximum. The agent reports: "Upgrade prompts optimized. Current performance: [metrics per trigger]. Further gains require strategic changes (new trigger types, pricing restructure, or product changes) rather than tactical optimization."

## Time Estimate

- 8 hours: Configure autonomous optimization loop (n8n workflows for daily monitoring, diagnosis triggers, experiment management)
- 4 hours: Set up hypothesis generation and experiment evaluation prompts for Claude
- 4 hours: Configure weekly brief generation and Slack/Attio delivery
- 2 hours: Define convergence criteria and steady-state monitoring
- 2 hours: End-to-end test of the full loop (simulate an anomaly and verify the loop responds correctly)
- Ongoing: 2 hours/week reviewing weekly briefs and approving high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, anomaly detection, dashboards | Free tier: 1M events/mo + 1M flag requests/mo; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app prompt delivery, Product Tours | Advanced $85/seat/mo + Proactive Support $99/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email follow-up sequences | From $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Optimization loop orchestration (cron, webhooks, API calls) | Self-hosted free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | ~$3-15/1K input tokens depending on model; est. $20-50/mo at 2-4 experiments/mo ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Attio | Campaign record, experiment log, optimization brief storage | From $29/seat/mo ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific monthly cost at Durable:** $200-450/mo (Intercom + Loops + Anthropic API are the main drivers; n8n and PostHog likely within free/low-usage tiers).

## Drills Referenced

- `autonomous-optimization` — the core monitor → diagnose → experiment → evaluate → implement loop that makes Durable fundamentally different from Scalable
- `upgrade-prompt-health-monitor` — provides the per-trigger funnel data, degradation alerts, fatigue cohorts, and revenue attribution that the optimization loop queries
