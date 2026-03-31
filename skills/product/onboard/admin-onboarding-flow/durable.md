---
name: admin-onboarding-flow-durable
description: >
  Admin vs User Onboarding — Durable Intelligence. Always-on AI agents running the
  autonomous optimization loop: detect anomalies in per-persona onboarding metrics,
  generate improvement hypotheses, run A/B experiments, auto-implement winners, and
  produce weekly optimization briefs. The agent finds and maintains the local maximum
  for both admin setup completion and user activation rates.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "40 hours setup + continuous operation over 6 months"
outcome: "Admin setup completion and user activation rates sustained or improving over 6 months via autonomous AI optimization, with convergence detected when 3 consecutive experiments produce <2% improvement"
kpis: ["Admin setup completion rate (overall + per persona)", "User activation rate (overall + per persona)", "Team invite rate", "Experiment velocity (experiments/month)", "Net metric lift from AI-implemented changes", "Time between anomaly detection and resolution (hours)", "Convergence status per persona"]
slug: "admin-onboarding-flow"
install: "npx gtm-skills add product/onboard/admin-onboarding-flow"
drills:
  - autonomous-optimization
  - onboarding-health-monitor
---

# Admin vs User Onboarding — Durable Intelligence

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

The dual onboarding system runs autonomously. An AI agent monitors all per-persona onboarding metrics daily, detects when any metric plateaus or drops, generates hypotheses for improvement, runs A/B experiments via PostHog, evaluates results, and auto-implements winners. The agent produces weekly optimization briefs summarizing what changed and why. The system converges toward the local maximum -- the best achievable performance given the current product, market, and user mix. Pass threshold: admin setup completion and user activation rates sustained at or above Scalable-level performance for 6 months, with autonomous optimization improving at least one metric by ≥5% over the period.

## Leading Indicators

- Anomaly detection firing within 24 hours of a metric change (not days later)
- Hypothesis generation producing actionable experiments (not vague suggestions)
- At least 2 experiments running per month across all personas
- Experiment win rate ≥30% (not all experiments win, but enough do to drive improvement)
- Weekly optimization briefs delivered on schedule with clear signal (not noise)
- No metric dropping below Scalable thresholds for more than 2 consecutive weeks without an active experiment addressing it
- Convergence detection: agent identifies when further tactical optimization produces diminishing returns

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to build the core agent loop for this play. Configure specifically for admin onboarding:

**Phase 1 -- Monitor (daily via n8n cron):**

The agent checks these metrics daily using PostHog anomaly detection:

| Metric | Play context | Anomaly threshold |
|--------|-------------|-------------------|
| Admin setup completion rate (overall) | Primary admin metric | ±10% from 4-week rolling average |
| Admin setup completion rate (per persona) | SMB, Mid-Market, Enterprise separately | ±15% from per-persona average |
| User activation rate (overall) | Primary user metric | ±10% from 4-week rolling average |
| User activation rate (per persona) | Technical, Non-Technical separately | ±15% from per-persona average |
| Checklist step drop-off rate | Which step has highest abandonment | Any step dropping >20% from baseline |
| Email engagement rate (per path) | Admin and user email sequences | Open rate drops >25% from average |
| Team invite rate | Admin → user conversion | ±15% from 4-week average |
| Persona classification accuracy | % classified vs % defaulting | Default rate exceeds 10% |

Compare last 2 weeks against 4-week rolling average. Classify: normal (within thresholds), plateau (±2% for 3+ weeks), drop (exceeds anomaly threshold), spike (>50% increase -- investigate positive anomaly for replication).

If normal: log to Attio, no action. If anomaly: trigger Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**

The agent gathers context:
- Pull the current persona configurations from Attio (checklist structure, email copy, tour steps, stall nudge timing)
- Pull 8-week metric history from PostHog
- Pull recent experiment results (what was tried, what worked, what failed)
- Identify the specific metric, persona, and step where the anomaly occurred

Run hypothesis generation with this context. The agent generates 3 ranked hypotheses. Examples of play-specific hypotheses:

- "SMB admin setup completion dropped because the new billing step flow (from last week's product update) added friction. Hypothesis: revert to the previous billing step or add a skip option."
- "Technical user activation rate plateaued because the API quickstart tour is too basic for experienced developers. Hypothesis: add an advanced track option that skips beginner content."
- "Enterprise admin setup is slow because SSO configuration requires IT involvement. Hypothesis: add an async SSO setup option where the admin can continue setup and return to SSO later."

If top hypothesis is high risk (affects >50% of users or changes core flow): send alert for human review and STOP. Otherwise: proceed to Phase 3.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**

Design the experiment using PostHog experiments:
- Create a feature flag that splits the affected persona's traffic 50/50
- Control: current configuration. Variant: hypothesis change.
- Primary metric: the anomalous metric (e.g., SMB admin setup completion rate)
- Secondary metrics: adjacent metrics (e.g., time-to-ready, team invite rate) to detect negative spillover
- Duration: minimum 7 days or 100+ samples per variant, whichever is longer

Implement the variant:
- If the hypothesis changes checklist structure: use Intercom audience rules to show the variant checklist to the experiment group
- If the hypothesis changes email copy: create a Loops sequence variant and route via n8n based on PostHog flag
- If the hypothesis changes tour design: create an Intercom Product Tour variant and trigger based on PostHog flag

Log experiment start in Attio: hypothesis, start date, expected duration, success criteria, affected persona.

**Phase 4 -- Evaluate (triggered by experiment completion):**

Pull experiment results from PostHog. Run experiment evaluation:
- **Adopt**: variant wins with 95% confidence AND primary metric improved ≥3% AND no secondary metric degraded >5%. Auto-implement: update the persona's configuration to use the winning variant permanently.
- **Iterate**: variant shows promise but not significant. Generate a refined hypothesis building on this result. Return to Phase 2.
- **Revert**: variant lost or caused secondary metric degradation. Disable variant, restore control. Log the failure with full reasoning. Return to Phase 1 monitoring.
- **Extend**: close to significance but insufficient sample size. Keep running for another period (max 1 additional period).

Store the full evaluation in Attio: decision, confidence level, metric deltas, reasoning, next action.

**Phase 5 -- Report (weekly via n8n cron, Monday 09:00):**

Generate a weekly optimization brief:

```
# Admin Onboarding Optimization Brief — Week of [date]

## Summary
- Anomalies detected: [N] ([list: persona + metric + direction])
- Experiments active: [N] ([list: hypothesis short name + persona + days remaining])
- Experiments completed: [N] ([list: hypothesis + result])
- Net metric change from adopted changes: [+/- X% admin setup, +/- Y% user activation]

## Per-Persona Status
| Persona | Setup/Activation Rate | Trend | Active Experiment | Convergence |
|---------|----------------------|-------|-------------------|-------------|
| SMB Admin | 78% | ↑ | Testing skip-billing flow | No |
| Mid-Market Admin | 72% | → | None | Approaching |
| Enterprise Admin | 65% | ↓ | Testing async-SSO | No |
| Technical User | 68% | → | None | Yes (converged) |
| Non-Technical User | 61% | ↑ | Testing video-first tour | No |

## This Week's Decisions
- [Adopted: SMB admin skip-billing variant → +6pp setup completion]
- [Reverted: Enterprise admin email cadence change → no improvement, slight engagement drop]

## Recommended Focus
- Enterprise admin SSO setup remains the biggest bottleneck. Current experiment testing async flow.
- Non-technical user video-first tour showing early promise — extend 1 more week.

## Distance from Local Maximum
- Estimated convergence: 3 of 5 personas within 5% of estimated ceiling.
- Remaining optimization potential: Enterprise admin + Non-technical user.
```

Post to Slack and store in Attio.

### 2. Deploy the onboarding health monitor

Run the `onboarding-health-monitor` drill to build the continuous per-persona monitoring layer that feeds into the autonomous optimization loop. Configure specifically for admin onboarding:

**Per-persona health dashboard in PostHog:**
- Admin setup completion rate by persona (weekly trend, 12-week window)
- User activation rate by persona (weekly trend, 12-week window)
- Time-to-workspace-ready distribution by admin persona
- Checklist step completion heatmap by persona (which steps, which order, where stalls)
- Email sequence engagement by persona (open, click, unsubscribe)
- Persona classification distribution (monitor for user mix shifts)

**Anomaly thresholds per persona:**
| Metric | Warning | Critical |
|--------|---------|----------|
| Setup/activation rate | 10-20% below 4-week average for 1 week | >20% below OR below play threshold for 2 weeks |
| Checklist/tour completion | 15-25% below average for 1 week | >25% below OR below 40% absolute |
| Email open rate | 20-35% below average for 1 week | >35% below OR below 15% absolute |
| Persona classification default rate | 5-10% | >10% |

**Daily monitoring workflow (n8n, 08:00 UTC):**
Query PostHog for each persona's metrics. Compare to thresholds. Critical anomalies trigger immediate Slack alerts with persona name, metric, current value, expected value, and suggested investigation. Warnings log to Attio. All-healthy logs a status check.

**Weekly health report (n8n, Monday 09:00 UTC):**
Aggregate weekly metrics per persona. Include: total signups, per-persona breakdown, activation rates, anomalies detected, active experiments, and recommended actions. This report provides context for the autonomous optimization brief.

**Cohort drift detection:**
Weekly comparison of this week's signup cohort profile against 4-week historical average. If persona distribution shifts significantly (e.g., enterprise signups suddenly double while SMB drops), flag as cohort drift. Cohort drift means the user mix changed -- optimization should account for the new mix rather than treating it as a performance problem.

### 3. Configure guardrails

**Rate limit:** Maximum 1 active experiment per persona at a time. 5 personas = max 5 concurrent experiments across the play.

**Revert threshold:** If any persona's primary metric (setup completion or activation) drops >30% during an active experiment, auto-revert immediately and alert the team.

**Human approval required for:**
- Changes to the signup flow or workspace creation process
- Changes affecting >50% of all users simultaneously
- Any hypothesis the agent flags as "high risk"
- Budget changes (upgrading tool plans, adding new tools)

**Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable for the same persona.

**Monthly cap:** Maximum 4 experiments per persona per month. If all 4 fail for a persona, pause optimization for that persona and flag for human strategic review.

**Convergence detection:** When 3 consecutive experiments for a persona produce <2% improvement, declare that persona converged. Reduce monitoring from daily to weekly. Report: "This persona's onboarding is optimized. Current performance is [metrics]. Further gains require product changes (new features, pricing changes, onboarding UX redesign) rather than tactical optimization."

### 4. Evaluate sustainability

This level runs continuously for 6 months. Monthly review checkpoints:

**Month 1-2:** Optimization loop running, first experiments completing, weekly briefs flowing. Expected: 1-2 experiments adopted, metrics holding at Scalable levels.

**Month 3-4:** Multiple experiments completed across personas. Expected: at least one persona shows measurable improvement (≥5% over Scalable baseline). Some personas approaching convergence.

**Month 5-6:** Most personas converging. Expected: sustained performance at or above Scalable levels. Agent shifting from active experimentation to monitoring.

Pass criteria for Durable:
- Admin setup completion and user activation rates sustained at or above Scalable-level performance for the full 6 months
- At least one metric improved ≥5% over the Scalable baseline via autonomous optimization
- No metric dropped below Scalable thresholds for more than 2 consecutive weeks without active remediation
- Weekly optimization briefs delivered consistently
- At least 2 personas reached convergence (local maximum found)

If metrics decay despite optimization: the agent diagnoses whether the cause is tactical (fixable via experiments) or strategic (requires product changes, market shift, or user mix change). Strategic causes are escalated to the team with a recommendation.

## Time Estimate

- 16 hours: autonomous optimization loop setup (monitoring workflows, hypothesis generation prompts, experiment automation, evaluation logic, reporting templates)
- 12 hours: onboarding health monitor setup (per-persona dashboard, anomaly thresholds, daily monitoring workflow, weekly health report, cohort drift detection)
- 6 hours: guardrail configuration and testing
- 6 hours: initial calibration (first 2 weeks of running, tuning anomaly thresholds, refining hypothesis generation)
- Ongoing: ~2 hours/week reviewing briefs and approving high-risk experiments (mostly autonomous)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, feature flags, anomaly detection | Growth: ~$100-450/mo based on events + experiments (https://posthog.com/pricing) |
| Intercom | Checklists, product tours, in-app messages (per-persona variants) | Advanced/Expert plan: ~$99-299/seat/mo (https://www.intercom.com/pricing) |
| Loops | Lifecycle email sequences (per-persona variants) | Paid: from $49/mo, scales with contacts (https://loops.so/pricing) |
| n8n | Automation (monitoring crons, experiment orchestration, reporting) | Cloud Pro: ~$50/mo (https://n8n.io/pricing) |
| Anthropic API | Claude Haiku for hypothesis generation and experiment evaluation | Haiku: $1/$5 per M input/output tokens; ~$15-40/mo at this volume (https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Attio | CRM logging of experiments, decisions, and health observations | Pro: $0-34/seat/mo (https://attio.com/pricing) |

**Estimated monthly cost at Durable:** ~$250-900/mo (PostHog $100-450 + Intercom $99-299 + Loops $49-149 + n8n $50 + Anthropic $15-40)

## Drills Referenced

- `autonomous-optimization` — the core always-on agent loop: monitor metrics → detect anomalies → generate hypotheses → run experiments → evaluate results → auto-implement winners → weekly briefs
- `onboarding-health-monitor` — continuous per-persona health monitoring with anomaly alerts, cohort drift detection, and weekly health reports that feed the optimization loop
