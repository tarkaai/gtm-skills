---
name: freemium-feature-upsell-durable
description: >
  Freemium to Paid Conversion — Durable Intelligence. Autonomous optimization loop that
  detects conversion anomalies, generates hypotheses, runs experiments on prompt UX, trigger
  thresholds, email sequences, and segment routing, then auto-implements winners to sustain
  and improve free-to-paid conversion rates.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving free-to-paid ≥8% and conversion-driven MRR growing or stable over 6 months via autonomous optimization"
kpis: ["Free-to-paid rate", "Conversion-driven MRR", "Experiment velocity", "Optimization lift", "Prompt fatigue index", "Free user pool health", "Distance from local maximum"]
slug: "freemium-feature-upsell"
install: "npx gtm-skills add product/upsell/freemium-feature-upsell"
drills:
  - autonomous-optimization
  - freemium-conversion-health-report
  - nps-feedback-loop
---

# Freemium to Paid Conversion — Durable Intelligence

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Free-to-paid conversion rate sustained at or above 8% and conversion-driven MRR stable or growing for 6 consecutive months. The autonomous optimization loop continuously detects when conversion performance changes (rate drops, fatigue spikes, cohort velocity shifts, segment imbalances), generates hypotheses for what to adjust, runs A/B experiments on prompt copy, trigger thresholds, email sequences, checkout flow, and segment routing, then auto-implements winners. Weekly health reports track progress toward the local maximum. When 3 successive experiments produce less than 2% improvement, the conversion system has converged and shifts to maintenance mode.

## Leading Indicators

- Anomaly detection catching metric shifts within 24 hours (the monitoring loop is responsive)
- At least 2 experiments completed per month with documented outcomes
- Winning experiments producing measurable lift (>3% improvement in the targeted metric)
- Prompt fatigue index stable or declining across all trigger types (prompts are not wearing out)
- NPS feedback from converted users confirms the paid plan delivers the value promised by the upgrade prompts
- Newer signup cohorts converting at rates comparable to or better than earlier cohorts (the system is not exhausting a fixed pool)
- Free user pool health: active free users growing or stable (the free tier remains attractive for top-of-funnel)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on monitor-diagnose-experiment-evaluate-implement cycle for the freemium conversion system:

**Monitor (daily via n8n cron):**
- Query PostHog for the conversion system's primary KPIs: overall free-to-paid rate, per-trigger conversion rates, per-segment conversion rates, conversion-driven MRR, prompt fatigue rate, email open/click rates, checkout completion rate, free user pool size and activation rate
- Compare last 2 weeks against 4-week rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If all metrics normal, log to Attio and take no action
- If any anomaly detected, proceed to diagnosis

**Diagnose (triggered by anomaly):**
- Pull the conversion system's current configuration from Attio: active trigger types, prompt variants per trigger, email sequences, segment routing rules, suppression thresholds, experiment history
- Pull 8-week metric history from PostHog
- Generate 3 ranked hypotheses using Claude. Examples the agent might generate:
  - "Limit proximity conversion dropped 18% this week because the highest-volume resource (projects) threshold was lowered from 85% to 70% last month, creating prompt fatigue as users see the alert too early — test raising the threshold back to 80% for the approaching tier while keeping imminent at 90%"
  - "Feature gate conversion stalled for the analytics dashboard feature because the locked preview shows a static screenshot that does not match the current UI — test replacing it with a live blurred view of the user's own data"
  - "Time-based email conversion declined because the 30-day trigger is now hitting users who signed up during a recent promotional campaign with lower intent — test extending the time trigger to 45 days for users from paid acquisition channels"
  - "Solo user segment conversion is 40% below team lead segment because the upgrade message focuses on unlimited projects but solo users rarely hit the project limit — test switching solo users to a feature-gate trigger on the automation feature instead"
  - "Checkout completion dropped 12% across all triggers because Stripe recently changed the checkout flow to add a confirm step — test embedding Stripe Elements inline instead of redirecting to Stripe Checkout"
- Store hypotheses in Attio. If the top hypothesis is high-risk (affects >50% of prompted free users or modifies pricing presentation), send Slack alert for human review and stop.

**Experiment (triggered by hypothesis acceptance):**
- Create a PostHog feature flag splitting the affected segment/trigger between control (current) and variant (hypothesis change)
- Implement the variant: if the hypothesis targets prompt UX, update the Intercom message variant; if it targets email, create a Loops sequence variant; if it targets timing or thresholds, adjust the n8n detection workflow parameters; if it targets checkout, modify the Stripe integration
- Run for minimum 7 days or until 100+ samples per variant
- Log experiment start in Attio: hypothesis, affected trigger/segment, start date, expected duration, success criteria

**Evaluate (triggered by experiment completion):**
- Pull results from PostHog experiments API
- Decision tree:
  - **Adopt:** Variant outperforms control with >95% confidence and >3% improvement. Update the live conversion configuration. Log the change.
  - **Iterate:** Results inconclusive or marginal. Generate a refined hypothesis building on this result. Return to diagnosis.
  - **Revert:** Variant underperforms control. Disable the variant, restore control. Log the failure. Wait 7 days before testing the same variable.
  - **Extend:** Insufficient sample size. Continue for another period.

**Guardrails:**
- Maximum 1 active experiment per trigger type at a time. Never stack experiments on the same trigger.
- If free-to-paid rate drops >30% during any experiment, auto-revert immediately.
- Maximum 4 experiments per month across the conversion system. If all 4 fail, pause optimization and flag for human strategic review.
- Never experiment on what is not measured: if a KPI lacks PostHog tracking, fix tracking first.
- Never modify plan pricing or free tier limits autonomously. Prompt copy, trigger thresholds, email content, surface type, and timing are fair game. Pricing and plan structure changes require human approval.

### 2. Generate weekly conversion health reports

Run the `freemium-conversion-health-report` drill to produce a structured weekly brief every Monday:

The report covers:
- **Conversion table:** trigger type, prompts shown, prompts clicked, upgrades started, upgrades completed, conversion rate, MRR attributed, trend vs. 4-week average
- **Cohort analysis:** this week's signup cohort conversion velocity vs. prior 4 cohorts. Are newer users converting faster or slower?
- **Free user pool health:** total free users, active %, activated %, upgrade-ready %, prompt-fatigued %. Trend each metric. If the pool is shrinking, conversion is outpacing acquisition.
- **Segment performance:** conversion rate by user type (solo, team lead, power-free). Which segment is driving revenue growth?
- **Experiment outcomes:** what was tested, what happened, what was decided, net impact on the targeted metric
- **Fatigue signals:** trigger types where fatigue exceeds 15% of exposed users, with suppression counts and email-fallback performance
- **Revenue attribution:** total conversion-driven MRR this month, month-over-month trend, average revenue per conversion, highest-value trigger and segment
- **Recommended action:** one specific experiment to run next week, with hypothesis and expected impact
- **Distance from local maximum:** current overall conversion rate vs. estimated ceiling based on diminishing experiment returns

The report is posted to Slack and stored in Attio. Degradation signals (conversion drops, fatigue spikes, cohort velocity decline) automatically feed into the optimization loop as the next hypothesis to investigate.

### 3. Close the feedback loop with converted users

Run the `nps-feedback-loop` drill targeted at users who converted from free to paid through the upgrade prompt pipeline:

- Survey users 30 days after their conversion: "How valuable has the paid plan been compared to the free tier?" (1-10 scale) + "What feature or capability made you decide to upgrade?" (open text)
- Route responses:
  - **Promoters (9-10):** The upgrade experience worked. Ask for a testimonial. Their conversion story becomes social proof displayed in upgrade prompts for other free users: "[Name] upgraded after hitting the project limit and now manages 200+ projects."
  - **Passives (7-8):** Ask what would make the paid plan a 10. Feed responses to the product team. If the paid plan underdelivers relative to what the prompt promised, adjust prompt copy to set more accurate expectations.
  - **Detractors (0-6):** The prompt oversold the value. The user upgraded but the paid plan did not deliver the expected improvement. Personal outreach, investigate whether the paid tier needs feature improvements. If detractor rate exceeds 15%, reduce prompt aggressiveness for the trigger type that is over-promising.
- Track NPS by trigger type: if users who converted via feature gates score consistently lower than users who converted via limit prompts, the feature gate previews are over-promising relative to the actual feature experience.
- Feed NPS insights into the autonomous optimization loop: low NPS scores for a trigger type become an input signal for the diagnosis phase, potentially generating hypotheses about adjusting that trigger's messaging.

### 4. Detect convergence and shift to maintenance

The optimization loop runs indefinitely until it detects convergence: 3 consecutive experiments producing less than 2% improvement. At convergence:

1. The freemium conversion system has found its local maximum for the current free/paid tier structure, trigger types, prompt UX, email sequences, and audience composition
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment velocity to 1 per month (maintenance testing for environmental changes: new user behavior shifts, competitive landscape changes, seasonal signup patterns)
4. Generate a convergence report: "Freemium conversion optimized. Current free-to-paid rate: [X]%. Conversion-driven MRR: [$Y]/mo. Estimated ceiling: [Z]%. Further gains require strategic changes: adjusting the free tier limits, adding new premium features, modifying pricing, or expanding the free user acquisition funnel."
5. Shift agent resources to other plays that have not yet converged

### 5. Continuous evaluation

This level runs continuously. Monthly check-in metrics:
- Is free-to-paid conversion holding at or above 8%?
- Is conversion-driven MRR stable or growing?
- Is the optimization loop producing at least 1 experiment per month?
- Are weekly health reports being generated and reviewed?
- Is prompt fatigue rate below 15% across all trigger types?
- Is the free user pool healthy (active free users growing or stable)?

If any metric degrades for 2 consecutive months despite optimization, escalate to human review. The conversion system may have hit external limits: the free tier is too generous (users do not feel the need to upgrade), the paid tier does not offer enough differentiation, the free user acquisition channel is declining, pricing has become uncompetitive, or the product's premium features have stagnated relative to market expectations. These require strategic intervention, not tactical optimization.

## Time Estimate

- 16 hours: Autonomous optimization loop setup — n8n workflows for daily monitoring, PostHog experiment infrastructure, Claude integration for hypothesis generation and evaluation, guardrail configuration
- 8 hours: Weekly conversion health report automation — dashboard creation, n8n scheduling, Slack and Attio integration
- 8 hours: NPS feedback loop configuration for converted users — survey deployment, response routing, social proof pipeline
- 88 hours: Ongoing optimization cycles, experiment management, report review, and convergence monitoring over 6 months (~3.5 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, funnels, dashboards | Growth from $0.00045/event — https://posthog.com/pricing |
| Intercom | Prompt variants, in-app upgrade messages, NPS surveys | ~$150-500/mo at scale — https://www.intercom.com/pricing |
| Loops | Email sequence variants, follow-up experiments | Starter $49/mo — https://loops.so/pricing |
| n8n | Optimization loop scheduling, trigger detection, report generation | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, report summarization | ~$20-50/mo based on usage — https://www.anthropic.com/pricing |
| Attio | Campaign records, experiment audit trail, revenue attribution | Free tier — https://attio.com/pricing |

**Play-specific cost:** ~$250-600/mo (Intercom at scale + Anthropic API usage + PostHog Growth tier)

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate loop that finds the local maximum for freemium conversion rates across all trigger types and segments
- `freemium-conversion-health-report` — weekly structured report with per-trigger conversion, cohort analysis, free user pool health, segment performance, fatigue signals, revenue attribution, and recommended next experiment
- `nps-feedback-loop` — collect and act on feedback from converted users to validate that the paid plan delivers the value the upgrade prompts promise
