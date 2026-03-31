---
name: calendar-flow-support-durable
description: >
  Calendar booking flow support — Durable Intelligence. Autonomous AI agents manage the
  entire calendar booking funnel: detect conversion anomalies per surface, generate hypotheses
  for why booking rates changed, run A/B experiments on CTA copy and embed configuration,
  auto-implement winners, and produce weekly optimization briefs. The team's only job is
  taking meetings.
stage: "Marketing > SolutionAware"
motion: "LeadCaptureSurface"
channels: "Direct"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Booking completion rate sustained at ≥ 8% for 6 consecutive months with ≥ 75 bookings/mo and ≤ 2 hours/week team involvement"
kpis: ["Monthly booking rate trend (flat or improving over 6 months)", "Monthly bookings (target ≥ 75)", "Show rate trend (target ≥ 80%)", "Cost per booked meeting trend (flat or decreasing)", "Booking-to-opportunity conversion rate (target ≥ 40%)", "Surface health index (% of pages with widget load rate ≥ 95%)"]
slug: "calendar-flow-support"
install: "npx gtm-skills add marketing/solution-aware/calendar-flow-support"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Calendar Booking Flow Support — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** LeadCaptureSurface | **Channels:** Direct

## Outcomes

The calendar booking funnel runs autonomously. AI agents monitor every embedded surface for conversion anomalies, generate hypotheses when rates change, run A/B experiments, auto-implement winners, and produce weekly optimization briefs. The system finds the local maximum for each booking surface and maintains it as traffic patterns, competitor actions, and prospect behavior change over time.

Pass: Booking completion rate ≥ 8% for 6 consecutive months, with ≥ 75 bookings/month, and ≤ 2 hours/week of team involvement (reviewing briefs and taking meetings only).
Fail: Booking rate drops below 6% for 3 consecutive weeks despite automated interventions, or the system requires more than 4 hours/week of manual effort.

## Leading Indicators

- The `autonomous-optimization` loop produces a winning experiment at least once per month for the first 3 months (the system is still finding improvements)
- Surface health index stays above 90% (≥ 90% of pages have widget load rate ≥ 95%)
- No-show recovery rate holds at ≥ 30% (automation catches every missed meeting)
- Mobile booking rate stays within 70% of desktop rate (mobile-specific experiments are working)
- Successive experiments produce diminishing returns after month 4 (convergence toward local maximum — this is the goal)
- Weekly optimization briefs are generated and delivered without human triggering

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured specifically for the calendar booking funnel. This is the core of Durable — an always-on agent that monitors, diagnoses, experiments, and implements.

**Configure the monitoring phase (daily via n8n cron):**

Use the `autonomous-optimization` drill's funnel stages as the primary KPIs for anomaly detection. The agent checks daily:

- Overall booking completion rate (7-day rolling vs 4-week rolling average)
- Per-surface booking rates (each page with an inline embed)
- Widget load rate per surface (technical health)
- Show rate trend
- Booking-to-opportunity conversion rate

Classification thresholds (from `autonomous-optimization`):
- **Normal:** within ±10% of 4-week rolling average
- **Plateau:** within ±2% for 3+ weeks (no improvement, no degradation)
- **Drop:** >20% decline from rolling average
- **Spike:** >50% increase (investigate — could be good or could be bot traffic)

If anomaly detected on any metric or any surface: trigger the diagnosis phase.

**Configure the diagnosis phase (triggered by anomaly):**

The agent gathers context:
1. Pull current embed configuration from Attio campaign record: CTA copy per page, embed placement, form fields, availability window
2. Pull 8-week metric history from PostHog via the `autonomous-optimization` funnel
3. Pull traffic source breakdown: did the anomaly correlate with a traffic source change?
4. Run `hypothesis-generation` with the anomaly data + context

Example hypotheses the agent might generate:
- "Booking rate on the pricing page dropped 25% because the new blog post is sending problem-aware (not solution-aware) traffic to the page. Hypothesis: add an intent qualifier above the calendar embed."
- "Overall timeslot selection rate dropped 18%. Hypothesis: the availability window is stale — team member changed their calendar availability without updating Cal.com."
- "Mobile booking completion rate dropped 30% on comparison pages. Hypothesis: a recent page redesign pushed the embed below the fold on mobile."

Store hypotheses in Attio. If risk = "high" (e.g., removing a booking surface or changing availability for the whole team), send Slack alert and wait for human approval. Otherwise proceed to experiment.

**Configure the experiment phase (triggered by hypothesis acceptance):**

Use PostHog feature flags to split traffic on the affected surface(s). The agent:
1. Creates the variant (e.g., new CTA heading, different embed placement, shorter form)
2. Sets up the PostHog experiment with control vs variant
3. Defines the primary metric (booking completion rate on the affected surface)
4. Sets the experiment duration: minimum 7 days or 200 impressions per variant, whichever is longer
5. Logs the experiment in Attio: hypothesis, start date, expected duration, success criteria

**Configure the evaluation phase (triggered by experiment completion):**

The agent pulls PostHog experiment results and runs `experiment-evaluation`:
- **Adopt:** The variant wins with ≥ 95% statistical significance and the improvement is ≥ 5% relative. Update the live page to use the winning variant. Log the change in Attio with date and impact.
- **Iterate:** Results are inconclusive or the improvement is < 5%. Generate a new hypothesis building on this result. Return to diagnosis.
- **Revert:** The variant performed worse. Disable it, restore control. Log the failure. Return to monitoring.

**Guardrails (enforced by n8n):**
- Maximum 1 active experiment per surface at a time
- If booking rate drops >30% on any surface during an experiment, auto-revert immediately
- If overall booking rate drops below 6% for 2 consecutive weeks, pause all experiments and alert the team
- Maximum 4 experiments per month total. If all 4 fail, pause optimization and flag for human strategic review
- Never experiment on the booking form fields without human approval (form changes affect CRM data quality)

### 2. Build the performance dashboard

Run the `dashboard-builder` drill to create the Durable-level PostHog dashboard:

**Dashboard panels:**
- **Overall booking funnel:** `cta_impression` -> `calendar_widget_loaded` -> `timeslot_selected` -> `meeting_booked` (8-week trend with Scalable baseline line at 8%)
- **Per-surface heatmap:** booking completion rate for each page, color-coded (green ≥ 10%, yellow 6-10%, red < 6%)
- **Surface health index:** widget load rate per page (any page below 95% is flagged red)
- **Mobile vs desktop split:** booking rate by device type, per surface
- **Show rate trend:** 8-week rolling show rate with 80% threshold line
- **Active experiment status:** current test, variant, days running, interim conversion rates
- **No-show recovery funnel:** `noshow_reschedule_sent` -> `meeting_rebooked` rate
- **Booking timing heatmap:** when prospects book (day of week x time of day) to optimize availability
- **Booking-to-opportunity rate:** 8-week trend with 40% threshold line
- **Cost per booked meeting:** monthly trend

**Alerts (via n8n):**
- Any surface drops below 6% booking rate for 3+ consecutive days -> investigate
- Widget load rate drops below 90% on any page -> technical issue, fix immediately
- Overall booking volume drops >30% week-over-week -> investigate traffic source change
- Show rate drops below 70% for 2 consecutive weeks -> review reminder sequence
- No experiments completed in 21+ days -> check if the optimization loop is running

### 3. Deploy the booking-specific monitoring layer

Run the `autonomous-optimization` drill to add the monitoring layer specific to calendar booking funnels. This runs alongside `autonomous-optimization` and provides the play-specific data that feeds the optimization loop.

Configure:
- Daily funnel monitoring with per-surface breakdown
- Weekly surface performance ranking (top 3, bottom 3)
- Booking timing pattern analysis (which days/times are prospects booking? Are there time slots that never get selected?)
- Traffic source attribution (which channels drive the highest-converting traffic to booking surfaces?)

The weekly surface report feeds directly into the `autonomous-optimization` diagnosis phase. If a surface consistently underperforms, the agent either generates an optimization hypothesis or recommends removing the embed from that surface.

### 4. Generate weekly optimization briefs

Build an n8n workflow (configured in `autonomous-optimization` Phase 5) that runs every Monday and delivers:

1. **Status summary:** Total bookings last week, booking rate, comparison to prior 4-week average and Scalable baseline
2. **Surface ranking:** Top 3 and bottom 3 surfaces by booking volume and rate
3. **Experiment update:** What experiment ran, what the result was, what was implemented or reverted
4. **Anomaly report:** Any anomalies detected and how the agent responded
5. **Next week plan:** What the agent plans to test or investigate next
6. **Distance from local maximum:** Are experiments still producing improvements, or has the system converged?

Deliver via Slack to the team. Store in Attio as a campaign note.

**Human action required:** The team reads the weekly brief (5 minutes). If the brief recommends a strategic change (new surface, CTA strategy shift, availability restructure), the team decides. All tactical changes (CTA copy rotation, placement tweaks, availability window adjustments) execute automatically.

### 5. Run monthly deep review

Build an n8n workflow that runs on the 1st of each month:

1. Pull 30-day aggregate metrics across all surfaces
2. Compare to prior month and to the Scalable baseline
3. Rank surfaces by ROI: bookings generated / maintenance effort
4. Identify:
   - Surfaces to keep (high volume, high rate)
   - Surfaces to optimize (high traffic, low rate — opportunity)
   - Surfaces to retire (low traffic, low rate — not worth the embed)
   - New surfaces to test (based on traffic growth on pages without embeds)
5. Calculate: total cost per booked meeting this month, booking-to-opportunity conversion, opportunity-to-revenue attribution if available
6. Flag convergence: if 3 consecutive experiments produced < 2% improvement, the booking funnel has reached its local maximum. Recommend reducing experimentation frequency from weekly to biweekly.

**Human action required:** The team reviews the monthly brief (~15 minutes) and decides on surface additions/retirements and any strategic shifts.

### 6. Sustain for 6 months

The system runs continuously. The agent's responsibilities:
- Monitor all booking surfaces daily for anomalies
- Run the optimization loop: detect -> diagnose -> experiment -> evaluate -> implement
- Generate weekly optimization briefs and monthly deep reviews
- Maintain widget health across all surfaces (fix broken embeds within 4 hours of detection)
- Rotate CTA copy when the agent detects fatigue (declining rates on a specific variant)
- Ensure no-show recovery automation runs reliably
- Detect convergence and reduce optimization intensity when the local maximum is reached

The team's responsibilities:
- Read the weekly Slack brief (5 minutes)
- Take meetings
- Approve strategic changes flagged in the monthly review (~15 minutes/month)
- Review and approve booking form changes if the agent recommends them

### 7. Evaluate sustainability after 6 months

Compute over the full 6-month period:
- Monthly booking rate for each of the 6 months (target: ≥ 8% every month)
- Monthly booking volume for each of the 6 months (target: ≥ 75 every month)
- Booking rate trend (stable, improving, or decaying?)
- Total cost / total bookings = cost per booked meeting
- Total team hours / total bookings = team time per meeting
- Show rate trend
- Booking-to-opportunity conversion rate trend
- Number of A/B experiments run, number that produced significant improvements
- Convergence status: has the system found its local maximum?

- **PASS (≥ 8% rate and ≥ 75 bookings/mo for all 6 months, ≤ 2 hours/week team time):** The play is durable. The calendar booking flow is a self-optimizing conversion engine. Consider: expanding to new surfaces (partner pages, co-marketing content), adding team round-robin via Cal.com Teams, or applying the same pattern to other conversion actions.
- **CONVERGED (rate stable at 8%+ but experiments no longer produce gains):** The local maximum has been found. Reduce the optimization loop from daily to weekly monitoring. Shift experiment resources to other plays. The booking flow is in maintenance mode.
- **DECLINING (rate held for 4+ months then decayed):** Market conditions changed (competitor launched a better booking flow, traffic quality shifted, prospect behavior changed). The agent should detect this via anomaly monitoring and recommend strategic changes: new CTA approaches, different embed formats, or a different conversion surface entirely.
- **FAIL (rate below 6% for 3+ consecutive weeks at any point):** The optimization loop is not adapting fast enough. Diagnose: Are experiments running? Are they targeting the right variables? Is the traffic still solution-aware? Fix the specific broken component or accept that this play requires more manual oversight.

## Time Estimate

- Autonomous optimization loop setup: 16 hours (Month 1)
- Dashboard and alert system: 8 hours (Month 1)
- Booking conversion monitor deployment: 6 hours (Month 1)
- Weekly brief and monthly review workflows: 6 hours (Month 1)
- Setup subtotal: 36 hours
- Weekly agent monitoring and loop execution: 4 hours/week x 24 weeks = 96 hours
- Weekly team time: 30 min/week x 24 weeks = 12 hours
- Monthly team review: 15 min x 6 months = 1.5 hours
- Experiment execution and implementation: 4 hours/month x 6 months = 24 hours
- Ongoing subtotal: ~133.5 hours
- Grand total: ~200 hours over 6 months (170 agent, 14 team, 16 buffer/troubleshooting)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | Inline scheduling embeds, event types, webhooks | Free plan — or Teams $15/user/mo for round-robin ([cal.com/pricing](https://cal.com/pricing)) |
| PostHog | Funnel analytics, A/B experiments, feature flags, anomaly detection, dashboards | Free tier: 1M events/mo; paid ~$0.00005/event beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | CRM — deal lifecycle, experiment log, optimization history | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | All automation: optimization loop, monitoring, alerts, briefs, follow-up | Pro €60/mo or self-host free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | Booking confirmation, no-show recovery, follow-up emails | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Clay | Pre-meeting enrichment | Starter $149/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, brief generation | Usage-based ~$15/1M input tokens ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated monthly cost for Durable:** $250-400/mo depending on team size and event volume

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect metric anomalies per booking surface, generate improvement hypotheses, run A/B experiments via PostHog, evaluate results, auto-implement winners, and produce weekly optimization briefs. Converges when successive experiments produce < 2% improvement.
- `dashboard-builder` — build the Durable PostHog dashboard with per-surface booking rates, experiment status, show rate trends, and cost-per-meeting tracking
- `autonomous-optimization` — play-specific monitoring for the calendar booking funnel: per-surface health checks, booking timing heatmap, traffic source attribution, and weekly surface rankings that feed the optimization loop
