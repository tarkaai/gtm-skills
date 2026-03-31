---
name: analyst-consultant-briefings-durable
description: >
  Analyst & Consultant Briefings — Durable Intelligence. Always-on AI agents monitor analyst
  program health, detect metric anomalies, generate improvement hypotheses, run A/B experiments
  on outreach and nurture, and auto-implement winners. Finds the local maximum of analyst-sourced
  pipeline and maintains it as market conditions change.
stage: "Sales > Qualified"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving analyst-sourced referral rate over 6 months; successive optimization experiments produce <2% improvement (local maximum reached)"
kpis: ["Analyst-sourced referrals per month", "Referral-to-meeting conversion rate", "Pipeline value from analyst referrals", "Analyst relationship health (% Healthy)", "Briefing-to-referral ratio", "Optimization experiment win rate"]
slug: "analyst-consultant-briefings"
install: "npx gtm-skills add sales/qualified/analyst-consultant-briefings"
drills:
  - autonomous-optimization
  - analyst-briefing-monitor
---

# Analyst & Consultant Briefings — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

The agent runs the analyst program toward its local maximum — the best possible referral rate and pipeline value given your market, product positioning, and analyst landscape. The shift from Scalable: instead of you monitoring dashboards and deciding what to change, an AI agent continuously detects when metrics plateau or drop, generates hypotheses about what to change, runs controlled experiments, evaluates results, and auto-implements winners. You review weekly optimization briefs and approve high-risk changes. Everything else is autonomous.

**Pass threshold:** Sustained or improving analyst-sourced referral rate over 6 months. The play is converged when 3 consecutive optimization experiments produce <2% improvement — the local maximum has been found.

## Leading Indicators

- Experiment velocity: 2-4 experiments per month (the optimization loop is running)
- Experiment win rate: >=30% of experiments produce measurable improvement
- Time-to-detect anomaly: <24 hours from metric change to hypothesis generation
- Analyst portfolio stability: <10% of analysts moving from Healthy to Cold per quarter
- Referral quality trend: analyst-sourced deals should close at equal or higher rates than other sources

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the analyst briefing program. This creates the core Durable engine:

**Phase 1 — Monitor (daily via n8n cron):**
The agent checks the analyst program's primary KPIs daily using PostHog anomaly detection:
- Briefing request acceptance rate (compare last 2 weeks to 4-week rolling average)
- Referral rate per briefed analyst
- Quarterly update engagement rate (opens, replies)
- Analyst relationship health distribution

Classify each metric: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context from Attio (current analyst list, outreach templates, nurture cadence) and PostHog (8-week metric history). It runs hypothesis generation to produce 3 ranked hypotheses. Examples:
- "Briefing acceptance rate dropped because outreach messaging has become stale — analyst recipients have seen similar language from 3+ vendors this quarter"
- "Referral rate plateaued because quarterly updates lack specificity — analysts are opening but not acting"
- "Tier 3 analyst engagement dropped because two key independents changed coverage areas"

If top hypothesis is high-risk (e.g., changes affecting >50% of the analyst portfolio), send Slack alert for human review and STOP. Otherwise, proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent designs a controlled experiment:
- Create a PostHog feature flag to split the analyst portfolio into control and variant groups
- Implement the variant (e.g., new briefing request subject line, different quarterly update format, adjusted nurture cadence)
- Set experiment duration: minimum 14 days or until 20+ analyst interactions per variant (whichever is longer — analyst populations are smaller than lead populations, so experiments take longer)
- Log experiment start in Attio with hypothesis, start date, and success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent pulls results from PostHog, runs experiment evaluation:
- **Adopt:** Update the live configuration to use the winning variant. Log the change.
- **Iterate:** Generate a new hypothesis building on partial results. Return to Phase 2.
- **Revert:** Disable the variant, restore control. Log the failure.
- **Extend:** If sample size is insufficient (common with analyst populations), extend the experiment.

**Phase 5 — Report (weekly via n8n cron):**
Generate a weekly optimization brief:
- Anomalies detected and actions taken
- Active experiments and preliminary results
- Experiments completed: wins, losses, impact on KPIs
- Net metric change from all adopted changes this period
- Current distance from estimated local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Deploy the analyst briefing monitor

Run the `analyst-briefing-monitor` drill to create the monitoring and reporting layer:

**PostHog dashboard — "Analyst Briefing Program":**
- Briefing pipeline funnel (outreach → scheduled → completed → follow-up → referral)
- Monthly briefing volume with target threshold line
- Referral conversion by analyst tier
- Analyst engagement health over time
- Time-to-briefing by tier
- Pipeline value from analyst referrals

**Alert thresholds:**
- Briefing volume drops >50% month-over-month
- No referrals received in 4 weeks despite active briefings
- Briefing acceptance rate drops below 20%
- Any Priority 1 analyst moves from Healthy to Cold

**Weekly status report (automated):**
Pipeline activity, referral pipeline value, relationship health distribution, and auto-generated action items based on alerts and trends.

**ROI attribution:**
Track cost-per-briefing, briefings-per-referral, referral-to-meeting rate, and analyst-sourced pipeline velocity. These metrics feed directly into the optimization loop.

### 3. Configure guardrails

**Critical guardrails the agent must enforce:**

- **Rate limit:** Maximum 1 active experiment at a time on the analyst program. Never stack experiments — analyst populations are small and changes confound easily.
- **Revert threshold:** If briefing acceptance rate drops >30% during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Changes to briefing document content or structure
  - Changes to quarterly update frequency (moving off the quarterly cadence)
  - Removing any Priority 1 analyst from the portfolio
  - Any experiment the hypothesis generator flags as high-risk
- **Cooldown:** After a failed experiment, wait 14 days before testing a new hypothesis on the same variable (analysts notice inconsistency more than leads do).
- **Maximum experiments per month:** 3 (analyst relationships are high-touch; too many changes erode trust).
- **Never experiment with:** The actual briefing meeting format or the analyst relationship — only outreach, nurture content, and operational elements.

### 4. Maintain the analyst portfolio

While the optimization loop handles tactical improvements, the agent also monitors the strategic health of the analyst portfolio:
- Quarterly: re-run `analyst-target-research` to identify new analysts entering the space
- Detect when analysts change coverage areas or leave firms — update Attio records automatically
- Identify which analysts are generating the highest-value referrals and increase investment in those relationships
- Flag analysts who have been briefed 2+ times with zero referrals for deprioritization review

**Human action required:** Continue conducting briefings personally (this remains human-led). Review the weekly optimization brief. Approve or reject high-risk experiment proposals. Make strategic decisions about portfolio composition based on the agent's recommendations.

### 5. Detect convergence

The agent monitors for convergence: when the analyst program has reached its local maximum. Convergence is detected when:
- 3 consecutive experiments produce <2% improvement on any primary KPI
- Analyst portfolio health is stable (>70% Healthy for 2+ consecutive quarters)
- Referral rate has been within ±5% of peak for 3+ months

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency to 1 per month (maintenance optimization)
3. Report: "The analyst briefing program is optimized. Current referral rate is [X]. Current pipeline from analyst referrals is [$Y/quarter]. Further gains require strategic changes — new market categories, new analyst tiers, or product positioning shifts — rather than tactical optimization."

## Time Estimate

- 20 hours: Initial setup (autonomous optimization loop, monitoring dashboard, alerts, guardrails)
- 10 hours/month: Agent compute for monitoring, hypothesis generation, experiments, reporting
- 4 hours/month: Human time for briefings, weekly brief review, high-risk approvals
- Total over 6 months: ~20 hours setup + ~84 hours ongoing = ~104 hours agent + ~96 hours human

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Analyst portfolio management, referral attribution, experiment logging | Free tier or existing plan — [attio.com](https://attio.com) |
| PostHog | Event tracking, anomaly detection, experiments, dashboards | Free tier (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Optimization loop crons, alert workflows, nurture automation | Free self-hosted or $24/mo cloud — [n8n.io/pricing](https://n8n.io/pricing) |
| Loops | Quarterly update and nurture email sequences | Free tier or $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Claude API | Hypothesis generation, experiment evaluation, report generation, briefing docs | ~$5-15/mo (Sonnet 4.6 for most tasks, Opus 4.6 for complex hypotheses) — [anthropic.com](https://console.anthropic.com) |
| Cal.com | Briefing scheduling | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Clay | Quarterly analyst list refresh | Growth $495/mo or existing plan — [clay.com](https://www.clay.com) |

**Estimated play-specific cost:** $80-170/mo (Loops + Claude API + n8n cloud + Clay credits for quarterly refresh)

## Drills Referenced

- `autonomous-optimization` — The core Durable engine: monitor → diagnose → experiment → evaluate → implement → report
- `analyst-briefing-monitor` — Dashboard, alerts, weekly reports, and ROI attribution for the analyst program
