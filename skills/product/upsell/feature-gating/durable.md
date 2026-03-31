---
name: feature-gating-durable
description: >
  Premium Feature Gating — Durable Intelligence. Autonomous optimization loop that detects
  gate conversion anomalies, generates hypotheses, runs experiments on gate UX and trial
  experiences, and auto-implements winners to sustain and improve upgrade rates across all
  gated features.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving trial-to-upgrade ≥20% and gate-driven MRR growing or stable over 6 months via autonomous optimization"
kpis: ["Trial-to-upgrade rate", "Gate-driven MRR", "Experiment velocity", "Optimization lift", "Gate fatigue index", "Distance from local maximum"]
slug: "feature-gating"
install: "npx gtm-skills add product/upsell/feature-gating"
drills:
  - autonomous-optimization
  - nps-feedback-loop
---

# Premium Feature Gating — Durable Intelligence

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Trial-to-upgrade conversion rate sustained at or above 20% and gate-driven MRR stable or growing for 6 consecutive months. The autonomous optimization loop continuously detects when gate performance changes (conversion drops, fatigue spikes, trial engagement shifts), generates hypotheses for what to adjust, runs A/B experiments on gate UX and trial experiences, and auto-implements winners. Weekly health reports track progress toward the local maximum. When successive experiments produce less than 2% improvement, the gating system has converged and shifts to maintenance mode.

## Leading Indicators

- Anomaly detection catching metric shifts within 24 hours (the monitoring loop is working)
- At least 2 experiments completed per month with documented outcomes
- Winning experiments producing measurable lift (>3% improvement in targeted metric)
- Gate fatigue index stable or declining across all gated features (gates are not wearing out)
- NPS feedback from upgraded users confirms the premium features deliver the value promised by the gates
- New gate-exposed users converting at rates comparable to or better than early cohorts (the system is not just exhausting a fixed pool)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on monitor-diagnose-experiment-evaluate-implement cycle for the feature gating system:

**Monitor (daily via n8n cron):**
- Query PostHog for the gating system's primary KPIs: overall trial-to-upgrade rate, per-feature conversion rates, gate-driven MRR, gate fatigue rate, trial engagement depth, gate dismissal rate
- Compare last 2 weeks against 4-week rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If all metrics normal, log to Attio and take no action
- If any anomaly detected, proceed to diagnosis

**Diagnose (triggered by anomaly):**
- Pull the gating system's current configuration from Attio: active gated features, gate UX variants per feature, trial durations, nurture sequences, segment routing rules, experiment history
- Pull 8-week metric history from PostHog
- Generate 3 ranked hypotheses using Claude. Examples of hypotheses the agent might generate:
  - "Trial-to-upgrade conversion dropped 15% this week because the highest-traffic gate (analytics dashboard) has been showing the same value preview for 8 weeks — test a refreshed preview using the user's own recent data instead of a static screenshot"
  - "Gate fatigue rate spiked 25% in the power-user segment because they encounter 3+ gates per week — test reducing gate frequency to max 1 per week for power users and replacing suppressed gates with email-based trial offers"
  - "Trial engagement is declining for the automation feature because new trial users are not discovering the setup wizard — test adding a PostHog-triggered Intercom product tour that fires on the first login after trial start"
  - "Upgrade rate plateauing across all features because the upgrade CTA links to the pricing page instead of a contextual inline checkout — test an inline upgrade modal that keeps the user in their current workflow"
  - "Free-to-trial conversion for the collaboration feature is 50% lower than other features because the value preview shows a team workspace but free users are solo — test a preview that shows what the user's existing data looks like in the collaborative view"
- Store hypotheses in Attio. If top hypothesis is high-risk (affects >50% of gate-exposed users or requires pricing changes), send Slack alert for human review and stop.

**Experiment (triggered by hypothesis acceptance):**
- Create a PostHog feature flag splitting the affected segment/feature between control (current) and variant (hypothesis change)
- Implement the variant: if the hypothesis targets gate UX, update the gate component's PostHog flag variant; if the hypothesis targets trial nurture, create a Loops sequence variant; if the hypothesis targets timing or frequency, adjust the n8n routing workflow
- Run for minimum 7 days or until 100+ samples per variant
- Log experiment start in Attio: hypothesis, affected feature/segment, start date, expected duration, success criteria

**Evaluate (triggered by experiment completion):**
- Pull results from PostHog experiments API
- Decision tree:
  - **Adopt:** Variant outperforms control with >95% confidence and >3% improvement. Update the live gate configuration. Log the change.
  - **Iterate:** Results inconclusive or marginal. Generate a refined hypothesis building on this result. Return to diagnosis.
  - **Revert:** Variant underperforms control. Disable the variant, restore control. Log the failure. Wait 7 days before testing the same variable.
  - **Extend:** Insufficient sample size. Continue for another period.

**Guardrails:**
- Maximum 1 active experiment per gated feature at a time. Never stack experiments on the same gate.
- If trial-to-upgrade rate drops >30% during any experiment, auto-revert immediately.
- Maximum 4 experiments per month across the gating system. If all 4 fail, pause optimization and flag for human strategic review.
- Never experiment on what is not measured: if a KPI lacks PostHog tracking, fix tracking first.
- Never modify pricing or plan structure autonomously. Gate UX, trial duration, messaging, and timing are fair game. Pricing requires human approval.

### 2. Generate weekly gate health reports

Run the the gate conversion health report workflow (see instructions below) drill to produce a structured weekly brief every Monday:

The report covers:
- **Per-feature gate table:** feature name, gate impressions, preview engagements, trials started, upgrades completed, conversion rate, MRR attributed, trend vs. 4-week average
- **Trial pipeline:** active trials, expected conversions (based on historical engagement-to-conversion correlation), at-risk trials (low engagement), trials expiring this week
- **Experiment outcomes:** what was tested, what happened, what was decided, and net impact on the targeted metric
- **Gate fatigue signals:** features where fatigue is detected for >10% of exposed users, with suppression counts and email-fallback performance
- **Revenue attribution:** total gate-driven MRR this month, month-over-month trend, average revenue per gate-driven upgrade, highest-value gate source
- **AI-generated recommendation:** one specific experiment to run next week, with hypothesis and expected impact
- **Distance from local maximum:** current overall conversion rate vs. estimated ceiling based on diminishing experiment returns

The report is posted to Slack and stored in Attio. "Act"-severity signals (fatigue spikes, conversion drops, trial health deterioration) automatically feed into the optimization loop as the next hypothesis to investigate.

### 3. Close the feedback loop with upgraded users

Run the `nps-feedback-loop` drill targeted specifically at users who upgraded through the feature gating pipeline:

- Survey users 30 days after their gate-driven upgrade: "How valuable has [premium feature] been to your workflow?" (1-10 scale) + "What made you decide to upgrade?" (open text)
- Route responses:
  - **Promoters (9-10):** The gate-to-upgrade experience worked. Ask for a testimonial. Their upgrade story ("I tried [feature] during the trial and immediately saw [benefit]") becomes social proof displayed in gates for other users.
  - **Passives (7-8):** Ask what would make the premium feature a 10. Feed responses to the product team. If the feature is underdelivering relative to what the gate promised, adjust the gate value preview to set more accurate expectations.
  - **Detractors (0-6):** The gate oversold the feature. The user upgraded based on the trial experience but the long-term value did not hold. This is a critical signal: personal outreach, investigate whether the feature needs improvement, and flag for product review. If detractor rate exceeds 15%, consider reducing the gate's aggressiveness for this feature.
- Track NPS by gated feature: if one feature's upgraders score consistently lower, the gate is over-promising relative to sustained value. Tone down that gate's messaging or improve the feature before continuing to push it.

### 4. Detect convergence and shift to maintenance

The optimization loop runs indefinitely until it detects convergence: 3 consecutive experiments producing less than 2% improvement. At convergence:

1. The gating system has found its local maximum for the current feature set, gate UX, trial experiences, and audience composition
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment velocity to 1 per month (maintenance testing for environmental changes: new users behaving differently, competitive landscape shifts, seasonal patterns)
4. Generate a convergence report: "Feature gating optimized. Current trial-to-upgrade rate: [X]%. Gate-driven MRR: [$Y]/mo. Estimated ceiling: [Z]%. Further gains require strategic changes: gating additional features, adjusting pricing tiers, or improving the premium features themselves."
5. Shift agent resources to other plays that have not yet converged

### 5. Continuous evaluation

This level runs continuously. Monthly check-in metrics:
- Is trial-to-upgrade conversion holding at or above 20%?
- Is gate-driven MRR stable or growing?
- Is the optimization loop producing at least 1 experiment per month?
- Are weekly health reports being generated and reviewed?
- Is gate fatigue rate below 15% across all features?

If any metric degrades for 2 consecutive months despite optimization, escalate to human review. The gating system may have hit external limits: the addressable user pool for the current gated features is exhausted, the product's free tier is too generous (users do not feel the need to upgrade), pricing has become uncompetitive, or the premium features have stagnated relative to market expectations. These require strategic intervention, not tactical optimization.

## Time Estimate

- 20 hours: Autonomous optimization loop setup (n8n workflows, PostHog experiment infrastructure, Claude integration for hypothesis generation and evaluation)
- 10 hours: Weekly gate health report automation setup
- 10 hours: NPS feedback loop configuration for gate-driven upgraders
- 110 hours: Ongoing optimization cycles, experiment management, and reporting over 6 months (~4.5 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, funnels, dashboards | Growth from $0.00045/event — https://posthog.com/pricing |
| Intercom | Gate UX variants, in-app upgrade prompts, NPS surveys | ~$150-500/mo at scale — https://www.intercom.com/pricing |
| Loops | Trial nurture sequence variants, upgrade follow-up emails | Starter $49/mo — https://loops.so/pricing |
| n8n | Optimization loop scheduling, trial provisioning, gate routing | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, report summarization | ~$20-50/mo based on usage — https://www.anthropic.com/pricing |
| Attio | Gate campaign records, experiment audit trail, revenue attribution | From $0/mo (free tier) — https://attio.com/pricing |

**Play-specific cost:** ~$250-600/mo (Intercom at scale + Anthropic API usage + PostHog Growth tier)

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate loop that finds the local maximum for gate conversion rates
- the gate conversion health report workflow (see instructions below) — weekly structured report with per-feature gate performance, trial pipeline, revenue attribution, fatigue signals, and recommended next experiment
- `nps-feedback-loop` — collect and act on feedback from gate-driven upgraders to validate that gated features deliver the value the gates promise
