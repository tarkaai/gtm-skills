---
name: business-case-development-durable
description: >
  Business Case Development — Durable Intelligence. Autonomous optimization loop detects
  declining approval rates, generates improvement hypotheses, A/B tests business case
  elements, and auto-implements winners. ROI prediction accuracy calibrates continuously
  from closed-deal outcomes.
stage: "Sales > Aligned"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "160 hours over 6 months"
outcome: "Approval rate sustained or improving over 6 months; ROI prediction accuracy ≥70%; autonomous optimization converges (<2% improvement in 3 consecutive experiments)"
kpis: ["Executive approval rate trend", "ROI prediction accuracy", "Time-to-approval trend", "Enterprise win rate", "Autonomous experiment win rate"]
slug: "business-case-development"
install: "npx gtm-skills add sales/aligned/business-case-development"
drills:
  - autonomous-optimization
  - roi-prediction-accuracy
---

# Business Case Development — Durable Intelligence

> **Stage:** Sales → Aligned | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

The business case development process runs autonomously with an always-on optimization loop. The agent detects when approval rates plateau or decline, generates hypotheses for improvement, runs A/B experiments on business case elements, evaluates results, and auto-implements winners. ROI projections continuously calibrate against actual closed-deal outcomes. The system converges toward the local maximum — the best possible approval rate given your market, product, and competitive landscape — and sustains it as conditions change.

## Leading Indicators

- Autonomous optimization fires hypotheses within 24 hours of anomaly detection
- A/B experiments complete within 2 weeks (sufficient deal volume per variant)
- ROI prediction accuracy improves quarter-over-quarter
- Approval rate holds steady despite market or competitive changes
- Experiment win rate exceeds 30% (at least 1 in 3 hypotheses produces a measurable improvement)
- Convergence signal: 3 consecutive experiments produce <2% improvement (local maximum reached)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for business case development. This creates the core always-on agent loop:

**Monitor (daily via n8n cron):**
1. Query PostHog for the business case approval funnel metrics from the last 2 weeks
2. Compare against 4-week rolling average
3. Classify: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If normal → log and continue monitoring
5. If anomaly detected → trigger diagnosis

**Diagnose (triggered by anomaly):**
1. Pull current business case configuration from Attio: template version, persona framing, delivery method, ROI presentation format
2. Pull 8-week metric history from PostHog including segment breakdowns (by industry, deal size, executive persona)
3. Run `hypothesis-generation` with the anomaly context and business-case-specific variables:
   - Hypothesis categories: template structure, ROI framing, strategic alignment depth, risk section approach, delivery format, follow-up cadence, champion enablement materials
4. Receive 3 ranked hypotheses with expected impact
5. If top hypothesis has risk = "high" (e.g., changes the core financial model approach) → send Slack alert for human review
6. If risk = "low" or "medium" → proceed to experiment

**Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using PostHog feature flags
2. Implement the variant: update the auto-generation n8n workflow to produce the variant version for flagged deals
3. Minimum experiment duration: 14 days or 15 cases per variant, whichever is longer
4. Log experiment parameters in Attio: hypothesis, start date, success criteria

**Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation` comparing control vs. variant on approval rate, time-to-approval, and deal progression
3. Decisions:
   - **Adopt**: Update the auto-generation workflow to use the winning variant as the new default. Log the change.
   - **Iterate**: Generate a refined hypothesis building on partial results. Return to Diagnose.
   - **Revert**: Disable the variant, restore control. Log the failure. Return to Monitor.
4. Store the full evaluation in Attio

**Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from adopted changes this week
3. Generate a weekly optimization brief:
   - What changed and why
   - Net impact on approval rate, time-to-approval, win rate
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 2. Deploy business case effectiveness monitoring

Run the `autonomous-optimization` drill to create play-specific monitoring:

**Effectiveness dashboard** tracking:
- Approval funnel: assembled → sent → champion engaged → executive review → approved → won
- Approval rate by industry, deal size, executive persona, alignment score
- Element-level tracking: which business case components (strategic alignment, risk mitigation, specific ROI framing) correlate with approval

**Stall detection alerts:**
- Business case sent > 7 days with no executive review scheduled → alert deal owner
- Approval rate drops > 15% below 12-week average → alert team lead
- Low-ROI case sent (< 200%) → flag for additional discovery

**Element effectiveness tracker:**
After 20+ outcomes, run correlation analysis: which components most strongly predict approval? Feed winning elements into the `autonomous-optimization` loop as high-priority experiment hypotheses.

**Monthly effectiveness report:**
- Total cases delivered, approved, won
- Approval rate and time-to-approval trends (3-month chart)
- Top 3 elements correlated with approval
- Top 3 rejection/stall reasons
- Template and framing recommendations

### 3. Deploy ROI prediction accuracy calibration

Run the `roi-prediction-accuracy` drill to create a continuous feedback loop:

**Monthly measurement cycle (n8n cron):**
1. Query Attio for deals closed ≥90 days ago with ROI models
2. Pull actual customer outcome data from PostHog (feature adoption, usage volume, time savings)
3. Run accuracy scoring: compare projected savings per value driver against annualized actuals
4. Compute:
   - Mean accuracy across all measured deals
   - Systematic bias direction (over- or under-projection)
   - Accuracy by value driver (time savings, cost reduction, revenue increase, risk mitigation)
   - Accuracy trend over time

**Calibration actions:**
- If a value driver is systematically over-projected by >20%, add a discount factor to future ROI models
- If a value driver is under-projected, note it but keep conservative (better to over-deliver)
- If a value driver has no measurement data, either add PostHog tracking or remove from projections
- Feed calibration recommendations into the auto-generation workflow so future ROI models improve automatically

**Accuracy target:** ≥70% mean accuracy across all measured deals by month 6.

### 4. Set Durable guardrails

**Critical guardrails (auto-revert if breached):**
- If approval rate drops >30% during any experiment → auto-revert immediately
- Maximum 1 active experiment at a time per business case element
- Maximum 4 experiments per month. If all 4 fail → pause optimization and alert for human strategic review

**Human approval required for:**
- Changes to the core financial model methodology (NPV calculations, discount rates)
- Changes that affect >50% of auto-generated cases simultaneously
- Any hypothesis flagged as "high risk" by the hypothesis generator

**Cooldown rules:**
- After a failed experiment, wait 7 days before testing the same variable
- After 3 consecutive failures on the same category, escalate to human review of the entire category

**Convergence detection:**
- When 3 consecutive experiments produce <2% improvement → declare convergence
- Reduce monitoring frequency from daily to weekly
- Report: "Business case development has reached its local maximum. Current approval rate: {X}%. Further gains require strategic changes (new markets, product changes, pricing model changes) rather than tactical optimization."

### 5. Continuous strategic adaptation

Even at convergence, the agent monitors for external changes that may shift the local maximum:
- Market shifts: new competitor entering, economic conditions changing approval dynamics
- Product changes: new features that create new value drivers for business cases
- Buyer behavior changes: new executive personas entering the approval chain, changing procurement processes
- Seasonal patterns: budget cycles that affect approval timing

When external change is detected, reset to active monitoring and run a fresh diagnosis cycle.

---

## Time Estimate

- 25 hours: configuring autonomous optimization loop (n8n workflows, PostHog experiments, guardrails)
- 15 hours: setting up business case effectiveness monitoring and stall detection
- 10 hours: configuring ROI prediction accuracy measurement and calibration pipeline
- 80 hours: monitoring, reviewing weekly briefs, approving high-risk experiments over 6 months (~3 hrs/week)
- 30 hours: analyzing monthly reports, calibrating ROI models, updating templates based on experiment results

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal data, experiment tracking, accuracy scores | Standard stack (excluded) |
| PostHog | Analytics — experiments, anomaly detection, dashboards | Standard stack (excluded) |
| n8n | Automation — optimization loop scheduling, alerts, auto-generation | Standard stack (excluded) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, ROI model calibration | ~$30-80/mo at volume ([pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |
| Clay | Continuous stakeholder and initiative enrichment | ~$200-500/mo ([pricing](https://www.clay.com/pricing)) |
| Qwilr (optional) | Interactive business case delivery for A/B testing formats | ~$39-49/user/mo ([pricing](https://qwilr.com/pricing/)) |

**Estimated play-specific cost:** ~$250-600/mo (Clay + Claude API + optional Qwilr)

## Drills Referenced

- `autonomous-optimization` — the core always-on agent loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and generate weekly optimization briefs
- `autonomous-optimization` — play-specific monitoring tracking approval rates, element effectiveness, stall detection, and monthly effectiveness reports
- `roi-prediction-accuracy` — measures projected vs. realized ROI across closed deals, computes model accuracy, and produces calibration recommendations for future projections
