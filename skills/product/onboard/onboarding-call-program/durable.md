---
name: onboarding-call-program-durable
description: >
  High-Touch Onboarding Calls — Durable Intelligence. Autonomous AI agent continuously
  optimizes the onboarding call program: detects metric anomalies, generates hypotheses,
  runs A/B experiments on call routing and follow-up, evaluates results, and auto-implements
  winners. Converges when successive experiments produce <2% improvement.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Direct"
level: "Durable Intelligence"
time: "20 hours setup + ongoing autonomous operation over 6 months"
outcome: "Sustained ≥75% post-call activation rate over 6 months via autonomous optimization; <2% improvement across 3 consecutive experiments signals convergence"
kpis: ["Post-call 7-day activation rate", "Activation lift vs no-call", "Experiment velocity", "Net metric change from adopted experiments", "Convergence status"]
slug: "onboarding-call-program"
install: "npx gtm-skills add product/onboard/onboarding-call-program"
drills:
  - autonomous-optimization
  - onboarding-health-monitor
---
# High-Touch Onboarding Calls — Durable Intelligence

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Direct

## Outcomes

The AI agent takes over continuous optimization of the onboarding call program. Instead of manually deciding what to test and when, the agent monitors all call program metrics, detects anomalies, generates improvement hypotheses, designs and runs A/B experiments, evaluates results, and auto-implements winners. The human reviews weekly optimization briefs and intervenes only for high-risk changes.

**Pass threshold:** Post-call 7-day activation rate sustained ≥75% over 6 months via autonomous optimization. Convergence reached when 3 consecutive experiments produce <2% improvement, indicating the program has reached its local maximum.

## Leading Indicators

- Autonomous monitoring running daily without errors
- Anomalies detected and diagnosed within 24 hours
- Experiments launching automatically when anomalies surface
- Winners auto-implemented without human intervention (for low/medium risk changes)
- Weekly optimization briefs delivered on schedule
- Net positive metric change from adopted experiments

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to set up the core optimization cycle for the onboarding call program:

**Phase 1 — Monitor (daily via n8n cron):**
- Use PostHog anomaly detection to check all call program KPIs: booking rate, completion rate, activation rate, call score average, activation lift vs no-call, no-show rate
- Compare the last 2 weeks against the 4-week rolling average
- Classify each metric: normal (within 10%), plateau (within 2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If normal: log to Attio, no action
- If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current qualification criteria, invitation copy, call script version, follow-up timing, team member assignments
- Pull 8-week metric history from PostHog
- Run hypothesis generation with the anomaly data + context
- Receive 3 ranked hypotheses with expected impact and risk levels
- If top hypothesis is high risk (e.g., changing qualification criteria affecting >50% of traffic): send alert for human review and STOP
- If low or medium risk: proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Take the top hypothesis
- Design the experiment using PostHog feature flags to split traffic between control (current) and variant (hypothesis change)
- Implement the variant using the appropriate tool:
  - Invitation copy change: update Intercom message or Loops email content
  - Follow-up timing change: adjust n8n workflow delay
  - Qualification criteria change: update PostHog cohort definition
  - Reminder cadence change: adjust Cal.com/Loops reminder sequences
- Set experiment duration: minimum 7 days or 50+ calls per variant, whichever is longer
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation on control vs variant data
- Decision:
  - **Adopt:** Variant wins significantly. Update live configuration. Log the change. Move to Phase 5.
  - **Iterate:** Result inconclusive but promising. Generate a new hypothesis building on this result. Return to Phase 2.
  - **Revert:** Variant loses. Disable variant, restore control. Log the failure. Return to Phase 1.
  - **Extend:** Not enough data yet. Run for another period.
- Store the full evaluation in Attio: decision, confidence level, reasoning, metric impact

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on primary KPIs
  - Current distance from estimated local maximum
  - Recommended focus for next week
  - Whether convergence criteria are approaching
- Post to Slack and store in Attio

### 2. Configure call-program-specific monitoring

Run the `autonomous-optimization` drill to maintain the detailed funnel dashboard and daily anomaly detection built at the Scalable level. Ensure:

- The full funnel dashboard (eligible → invited → booked → completed → activated) is current
- Daily anomaly checks use the thresholds defined at Scalable level
- Weekly performance reports continue generating
- Monthly cohort comparison and ROI analysis runs automatically

The performance monitor feeds anomaly data into the `autonomous-optimization` drill's monitoring phase.

### 3. Deploy onboarding health monitoring

Run the `onboarding-health-monitor` drill to add a second layer of monitoring focused on per-segment health:

- Build a per-persona health dashboard (activation rate by persona, tour completion, email engagement, persona classification distribution)
- Configure daily health checks that compare per-segment metrics against their rolling averages
- Set up cohort drift detection: flag when the profile of new signups shifts significantly (different personas, company sizes, or signup sources)
- Connect health anomalies to the autonomous optimization loop: a per-segment anomaly triggers diagnosis and experimentation specific to that segment

Cohort drift is especially important for onboarding calls: if the user mix changes (e.g., more enterprise signups or a different use case becoming dominant), the call script may need to adapt. The health monitor detects this shift before activation rates drop.

### 4. Set guardrails

Configure the guardrails from the `autonomous-optimization` drill for this specific play:

- **Rate limit:** Maximum 1 active experiment at a time on the call program. Never stack experiments.
- **Revert threshold:** If post-call activation rate drops >20 percentage points at any point during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Qualification criteria changes affecting >50% of eligible users
  - Any change to the call script structure (not just invitation/follow-up copy)
  - Team routing changes that remove a team member from the rotation
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable.
- **Monthly experiment cap:** Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize unmeasured variables:** If a metric lacks PostHog tracking, fix the tracking first.

### 5. Monitor convergence

The autonomous optimization loop runs indefinitely. It should detect convergence -- when successive experiments produce diminishing returns:

- Track the metric impact of each adopted experiment
- If 3 consecutive experiments produce <2% improvement on the primary metric (post-call activation rate), the program has reached its local maximum
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Report: "Onboarding call program is optimized. Current performance: [metrics]. Further gains require strategic changes (new activation milestone, new user segments, product changes) rather than tactical optimization."
  3. The agent continues monitoring for anomalies but stops proactively generating experiments until a metric shifts

### 6. Evaluate sustainability

At 6 months:

1. Post-call 7-day activation rate: has it sustained ≥75% over the full period?
2. Total experiments run, adopted, reverted, and iterated
3. Net metric improvement from all adopted experiments combined
4. Current convergence status: has the program reached its local maximum?
5. ROI: (incremental activations x LTV) vs (all program costs including team time, tool costs, and agent compute)

**Pass:** Activation rate sustained ≥75% over 6 months. At least 6 experiments run. Net metric change is positive.
**Converged:** Activation rate sustained AND 3 consecutive experiments produced <2% improvement. The program has found its local maximum. Shift focus to maintaining and monitoring.

## Time Estimate

- 8 hours: Autonomous optimization loop setup (n8n workflows, PostHog integration, Attio logging)
- 4 hours: Health monitoring and cohort drift detection setup
- 4 hours: Guardrail configuration and testing
- 4 hours: Monthly review and strategic adjustment (30 min/week for 6 months)
- Ongoing: Agent runs autonomously. Human reviews weekly briefs (15 min/week).

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | Team scheduling with round-robin | Teams: $15/user/mo ([cal.com/pricing](https://cal.com/pricing)) |
| Fireflies | Call recording and transcript analysis | Pro: $10/user/mo annually ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| Intercom | In-app messaging (agent-modified) | Essential: $29/seat/mo annually ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email sequences (agent-modified) | $49/mo for 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost:** $90-175/mo (same as Scalable; Durable adds agent compute but does not add new tools)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, weekly briefs
- `autonomous-optimization` — full funnel dashboard, daily anomaly detection, weekly reports, monthly cohort analysis feeding into the optimization loop
- `onboarding-health-monitor` — per-segment health monitoring, cohort drift detection, and anomaly alerts that trigger the optimization loop for segment-specific issues
