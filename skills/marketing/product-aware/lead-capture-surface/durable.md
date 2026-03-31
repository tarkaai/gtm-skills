---
name: lead-capture-surface-durable
description: >
  Single CTA Lead Capture — Durable Intelligence. Autonomous AI agents manage all lead capture
  surfaces: detect conversion anomalies per page, generate hypotheses for why rates changed,
  run A/B experiments on CTA copy, surface type, and placement, auto-implement winners, and
  produce weekly optimization briefs. The system finds the local maximum for each surface and
  maintains it as traffic patterns and prospect behavior change.
stage: "Marketing > ProductAware"
motion: "LeadCaptureSurface"
channels: "Direct"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Conversion rate sustained at ≥ 5% for 6 consecutive months with ≥ 40 leads/mo and ≤ 2 hours/week team involvement"
kpis: ["Monthly conversion rate trend (flat or improving over 6 months)", "Monthly lead volume (target ≥ 40)", "Best-surface conversion rate (target ≥ 10%)", "Cost per lead trend (flat or decreasing)", "Lead-to-meeting conversion rate (target ≥ 30%)", "Surface health index (% of surfaces with conversion rate ≥ 3%)"]
slug: "lead-capture-surface"
install: "npx gtm-skills add marketing/product-aware/lead-capture-surface"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Single CTA Lead Capture — Durable Intelligence

> **Stage:** Marketing > ProductAware | **Motion:** LeadCaptureSurface | **Channels:** Direct

## Outcomes

The lead capture system runs autonomously. AI agents monitor every surface for conversion anomalies, generate hypotheses when rates change, run A/B experiments, auto-implement winners, and produce weekly optimization briefs. The system finds the local maximum for each lead capture surface and maintains it as traffic patterns, competitor actions, and prospect behavior change over time.

Pass: Conversion rate ≥ 5% for 6 consecutive months, with ≥ 40 leads/month, and ≤ 2 hours/week of team involvement (reviewing briefs only).
Fail: Conversion rate drops below 4% for 3 consecutive weeks despite automated interventions, or the system requires more than 4 hours/week of manual effort.

## Leading Indicators

- The `autonomous-optimization` loop produces a winning experiment at least once per month for the first 3 months (the system is still finding improvements)
- Surface health index stays above 85% (≥ 85% of surfaces maintain conversion rate ≥ 3%)
- Lead-to-meeting conversion rate holds at ≥ 30% (lead quality is maintained while optimizing volume)
- Mobile conversion rate stays within 65% of desktop rate (mobile-specific experiments are working)
- Successive experiments produce diminishing returns after month 4 (convergence toward local maximum -- this is the goal)
- Weekly optimization briefs are generated and delivered without human triggering

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured specifically for the lead capture surface funnel. This is the core of Durable -- an always-on agent that monitors, diagnoses, experiments, and implements.

**Configure the monitoring phase (daily via n8n cron):**

Use the `autonomous-optimization` drill's funnel stages as the primary KPIs for anomaly detection. The agent checks daily:

- Overall conversion rate across all surfaces (7-day rolling vs 4-week rolling average)
- Per-surface conversion rates (each page with a lead capture element)
- CTA click-through rate per surface
- Form/widget completion rate per surface
- Lead-to-meeting conversion rate (lead quality proxy)
- Device split: desktop vs mobile conversion per surface

Classification thresholds (from `autonomous-optimization`):
- **Normal:** within +/- 10% of 4-week rolling average
- **Plateau:** within +/- 2% for 3+ weeks (no improvement, no degradation)
- **Drop:** >20% decline from rolling average
- **Spike:** >50% increase (investigate -- could be good traffic or could be bot submissions)

If anomaly detected on any metric or any surface: trigger the diagnosis phase.

**Configure the diagnosis phase (triggered by anomaly):**

The agent gathers context:
1. Pull current surface configuration from Attio campaign record: CTA copy per page, surface type, form fields, placement
2. Pull 8-week metric history from PostHog via the `autonomous-optimization` funnel
3. Pull traffic source breakdown: did the anomaly correlate with a traffic source change?
4. Pull device breakdown: did the anomaly affect mobile only, desktop only, or both?
5. Run `hypothesis-generation` with the anomaly data + context

Example hypotheses the agent might generate:
- "Conversion rate on the pricing page dropped 22% because a new blog post is sending problem-aware (not product-aware) traffic to the page. Hypothesis: add an intent qualifier question to the form on the pricing page."
- "Form completion rate dropped 30% on the product page. Hypothesis: a recent page redesign pushed the form below the fold on mobile. Test moving the form higher."
- "Overall lead volume increased 40% but lead-to-meeting rate dropped from 35% to 18%. Hypothesis: the shortened form is capturing lower-intent leads. Add back the qualifying question."
- "CTA click-through rate on comparison pages plateaued at 11% for 4 weeks. Hypothesis: visitors have seen the same CTA copy too many times. Test a new headline variant."

Store hypotheses in Attio. If risk = "high" (e.g., removing a surface entirely, changing form fields that affect CRM data, or modifying the primary landing page CTA), send Slack alert and wait for human approval. Otherwise proceed to experiment.

**Configure the experiment phase (triggered by hypothesis acceptance):**

Use PostHog feature flags to split traffic on the affected surface(s). The agent:
1. Creates the variant (e.g., new CTA heading, different surface type, modified form, relocated placement)
2. Sets up the PostHog experiment with control vs variant
3. Defines the primary metric (conversion rate on the affected surface) and secondary metrics (lead-to-meeting rate as a quality guard)
4. Sets the experiment duration: minimum 7 days or 200 impressions per variant, whichever is longer
5. Logs the experiment in Attio: hypothesis, start date, expected duration, success criteria

**Configure the evaluation phase (triggered by experiment completion):**

The agent pulls PostHog experiment results and runs `experiment-evaluation`:
- **Adopt:** The variant wins with ≥ 95% statistical significance and the improvement is ≥ 5% relative. The secondary metric (lead quality) did not decline by more than 10%. Update the live surface to use the winning variant. Log the change in Attio with date and impact.
- **Iterate:** Results are inconclusive or the improvement is < 5%. Generate a new hypothesis building on this result. Return to diagnosis.
- **Revert:** The variant performed worse, or lead quality dropped significantly (lead-to-meeting rate declined >15%). Disable the variant, restore control. Log the failure. Return to monitoring.

**Guardrails (enforced by n8n):**
- Maximum 1 active experiment per surface at a time. Never stack experiments on the same page.
- If conversion rate drops >30% on any surface during an experiment, auto-revert immediately.
- If overall conversion rate drops below 3% for 2 consecutive weeks, pause all experiments and alert the team.
- Maximum 4 experiments per month total across all surfaces. If all 4 fail, pause optimization and flag for human strategic review.
- Never experiment on form fields without human approval (form changes affect CRM data quality and lead routing).
- Always monitor lead quality (lead-to-meeting rate) as a secondary metric. Optimizing conversion rate at the expense of lead quality is a false win.

### 2. Build the performance dashboard

Run the `dashboard-builder` drill to create the Durable-level PostHog dashboard:

**Dashboard panels:**
- **Overall lead capture funnel:** `cta_impression` -> `cta_clicked` -> `lead_captured` (8-week trend with Scalable baseline line at 5%)
- **Per-surface heatmap:** conversion rate for each page, color-coded (green ≥ 6%, yellow 3-6%, red < 3%)
- **Surface health index:** percentage of surfaces maintaining ≥ 3% conversion rate
- **Mobile vs desktop split:** conversion rate by device type, per surface
- **Lead quality trend:** lead-to-meeting conversion rate, 8-week rolling average with 30% threshold line
- **Active experiment status:** current test, variant, days running, interim conversion rates
- **CTA fatigue tracker:** per-surface CTA click-through rate trend over 8 weeks (declining CTR signals copy fatigue)
- **Traffic source quality:** conversion rate by `utm_source` per surface (identifies which sources drive converting traffic)
- **Form abandonment funnel** (for form surfaces): which fields cause drop-off
- **Monthly lead volume:** trend with 40 leads/mo threshold line
- **Cost per lead:** monthly trend

**Alerts (via n8n):**
- Any surface drops below 3% conversion rate for 3+ consecutive days -> investigate
- Overall conversion rate drops below 4% for 2+ consecutive days -> investigate traffic source change
- Lead-to-meeting rate drops below 20% for 2 consecutive weeks -> lead quality issue, review form/surface changes
- CTA click-through rate on any surface declines >25% over 4 weeks -> CTA fatigue, trigger copy rotation experiment
- No experiments completed in 21+ days -> check if the optimization loop is running

### 3. Deploy the lead-capture-specific monitoring layer

Run the `autonomous-optimization` drill to add the monitoring layer specific to lead capture surfaces. This runs alongside `autonomous-optimization` and provides the play-specific data that feeds the optimization loop.

Configure:
- Daily funnel monitoring with per-surface and per-page breakdown
- Weekly surface performance ranking (top 3, bottom 3)
- Form abandonment analysis per surface (for form-based surfaces)
- Device split monitoring: flag any surface where mobile conversion is < 50% of desktop
- Traffic source attribution: which channels drive the highest-converting traffic to each surface

The weekly surface report feeds directly into the `autonomous-optimization` diagnosis phase. If a surface consistently underperforms after 2+ optimization attempts, the agent recommends removing it or testing a completely different surface type on that page.

### 4. Generate weekly optimization briefs

Build an n8n workflow (configured in `autonomous-optimization` Phase 5) that runs every Monday and delivers:

1. **Status summary:** Total leads last week, overall conversion rate, comparison to prior 4-week average and Scalable baseline
2. **Surface ranking:** Top 3 and bottom 3 surfaces by lead volume and conversion rate
3. **Experiment update:** What experiment ran, what the result was, what was implemented or reverted
4. **Lead quality check:** Lead-to-meeting rate this week vs baseline. Any quality concerns?
5. **Anomaly report:** Any anomalies detected and how the agent responded
6. **Next week plan:** What the agent plans to test or investigate next
7. **Distance from local maximum:** Are experiments still producing improvements, or has the system converged?

Deliver via Slack to the team. Store in Attio as a campaign note.

**Human action required:** The team reads the weekly brief (5 minutes). If the brief recommends a strategic change (new page, CTA strategy shift, surface type overhaul), the team decides. All tactical changes (CTA copy rotation, placement tweaks, form field adjustments within approved parameters) execute automatically.

### 5. Run monthly deep review

Build an n8n workflow that runs on the 1st of each month:

1. Pull 30-day aggregate metrics across all surfaces
2. Compare to prior month and to the Scalable baseline
3. Rank surfaces by ROI: leads generated / page traffic volume
4. Identify:
   - Surfaces to keep (high volume, high conversion rate)
   - Surfaces to optimize (high traffic, low conversion -- opportunity)
   - Surfaces to retire (low traffic, low conversion -- not worth maintaining)
   - New surfaces to test (high-traffic pages without lead capture surfaces)
5. Calculate: cost per lead this month, lead-to-meeting conversion, meeting-to-opportunity attribution if available
6. Flag convergence: if 3 consecutive experiments produced < 2% improvement, the lead capture system has reached its local maximum. Recommend reducing experimentation frequency from weekly to biweekly.

**Human action required:** The team reviews the monthly brief (~15 minutes) and decides on surface additions/retirements and any strategic changes.

### 6. Sustain for 6 months

The system runs continuously. The agent's responsibilities:
- Monitor all lead capture surfaces daily for conversion anomalies
- Run the optimization loop: detect -> diagnose -> experiment -> evaluate -> implement
- Generate weekly optimization briefs and monthly deep reviews
- Maintain surface health across all pages (detect and alert on broken forms/widgets within 4 hours)
- Rotate CTA copy when the agent detects fatigue (declining click-through rate on a specific variant for 2+ weeks)
- Monitor lead quality alongside conversion quantity (never sacrifice quality for volume)
- Detect convergence and reduce optimization intensity when the local maximum is reached

The team's responsibilities:
- Read the weekly Slack brief (5 minutes)
- Follow up on captured leads and take meetings
- Approve strategic changes flagged in the monthly review (~15 minutes/month)
- Review and approve form field changes if the agent recommends them

### 7. Evaluate sustainability after 6 months

Compute over the full 6-month period:
- Monthly conversion rate for each of the 6 months (target: ≥ 5% every month)
- Monthly lead volume for each of the 6 months (target: ≥ 40 every month)
- Conversion rate trend (stable, improving, or decaying?)
- Lead-to-meeting conversion rate trend (stable or improving = quality maintained)
- Total cost / total leads = cost per lead
- Total team hours / total leads = team time per lead
- Number of A/B experiments run, number that produced significant improvements
- Convergence status: has the system found its local maximum?
- Surface health index trend: are all surfaces maintaining healthy conversion rates?

- **PASS (≥ 5% rate and ≥ 40 leads/mo for all 6 months, ≤ 2 hours/week team time):** The play is durable. The lead capture system is a self-optimizing conversion engine. Consider: expanding to new channels (partner pages, co-marketing content), adding dynamic surface selection (show different surface types based on visitor behavior), or applying the same pattern to other conversion actions.
- **CONVERGED (rate stable at 5%+ but experiments no longer produce gains):** The local maximum has been found. Reduce the optimization loop from daily to weekly monitoring. Shift experiment resources to other plays. The lead capture system is in maintenance mode.
- **DECLINING (rate held for 4+ months then decayed):** Market conditions changed (prospect behavior shifted, competitor launched a better conversion flow, traffic quality changed). The agent should detect this via anomaly monitoring and recommend strategic changes: new surface types, different page layouts, or a different conversion action entirely.
- **FAIL (rate below 4% for 3+ consecutive weeks at any point):** The optimization loop is not adapting fast enough. Diagnose: Are experiments running? Are they targeting the right variables? Is the traffic still product-aware? Is lead quality being maintained? Fix the specific broken component or accept that this play requires more manual oversight.

## Time Estimate

- Autonomous optimization loop setup: 16 hours (Month 1)
- Dashboard and alert system: 8 hours (Month 1)
- CTA conversion monitor deployment: 6 hours (Month 1)
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
| PostHog | Funnel analytics, A/B experiments, feature flags, anomaly detection, dashboards | Free tier: 1M events/mo; paid ~$0.00005/event beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| Webflow | Landing pages and form surfaces | CMS $23/mo ([webflow.com/pricing](https://webflow.com/pricing)) |
| Cal.com | Inline scheduling embeds (calendar surfaces) | Free plan -- or Teams $15/user/mo ([cal.com/pricing](https://cal.com/pricing)) |
| Tally | Form builder (form surfaces) | Free plan ([tally.so/pricing](https://tally.so/pricing)) |
| Intercom | Chat widget (chat surfaces) | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| Attio | CRM — lead pipeline, experiment log, optimization history | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | All automation: optimization loop, monitoring, alerts, briefs | Pro €60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | Nurture sequences per surface | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, brief generation | Usage-based ~$3/1M input tokens for Sonnet ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated monthly cost for Durable:** $200-350/mo depending on surface count, traffic volume, and Anthropic API usage

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect metric anomalies per lead capture surface, generate improvement hypotheses, run A/B experiments via PostHog, evaluate results, auto-implement winners, and produce weekly optimization briefs. Converges when successive experiments produce < 2% improvement.
- `autonomous-optimization` — play-specific monitoring for lead capture surface funnels: per-page health checks, form abandonment analysis, device split tracking, traffic source attribution, and weekly surface rankings that feed the optimization loop
- `dashboard-builder` — build the Durable PostHog dashboard with per-surface conversion rates, experiment status, lead quality trends, CTA fatigue tracking, and cost-per-lead monitoring
