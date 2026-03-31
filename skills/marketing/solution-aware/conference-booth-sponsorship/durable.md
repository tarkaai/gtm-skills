---
name: conference-booth-sponsorship-durable
description: >
  Conference Booth & Sponsorship — Durable Intelligence. Always-on AI agents
  continuously monitor conference program ROI, detect degradation in lead
  quality or conversion rates, generate improvement hypotheses across
  conference selection, booth tactics, and follow-up sequences, run A/B
  experiments, and auto-implement winners. Weekly optimization briefs track
  progress toward the local maximum. Converges when successive experiments
  produce less than 2% improvement.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Durable Intelligence"
time: "120 hours over 12 months"
outcome: "Sustained or improving conference ROI over 12 months. >=80 qualified leads and >=30 meetings per year from 6-8 conferences. Agents detect degradation, diagnose causes, experiment, and auto-implement improvements. Convergence when 3 consecutive experiments produce <2% improvement."
kpis: ["Qualified leads per conference (vs rolling average)", "Cost per meeting (trend)", "Follow-up conversion rate (trend)", "Pipeline per sponsorship dollar (trend)", "Experiment win rate", "Time to convergence"]
slug: "conference-booth-sponsorship"
install: "npx gtm-skills add marketing/solution-aware/conference-booth-sponsorship"
drills:
  - autonomous-optimization
---

# Conference Booth & Sponsorship — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Maintain or improve conference program ROI over 12 months without manual optimization effort
- Detect and respond to degradation (lead quality decline, cost per meeting increase, follow-up fatigue, audience saturation) before they become critical
- Continuously experiment on every lever: conference selection criteria, sponsorship tier, booth demo approach, follow-up timing and format, pre-event targeting
- Find the local maximum — the best achievable conference program performance given your market, audience, and budget
- Generate weekly optimization briefs summarizing what changed, why, and what to try next
- Converge: when 3 consecutive experiments produce <2% improvement, the program is optimized

## Leading Indicators

- Anomaly detection fires within 48 hours of any post-conference metric moving >15% from the 3-conference rolling average
- At least 1 experiment running at all times during the event cycle (the loop never idles until convergence)
- Experiment win rate >30% (not every test wins, but enough do to drive improvement)
- Weekly optimization briefs generated on schedule with actionable recommendations
- No metric declines for 3+ consecutive conferences without an experiment addressing it

## Instructions

### 1. Deploy continuous conference program monitoring

Run the `autonomous-optimization` drill to build the always-on monitoring layer:

- **Post-event automated checks**: 14 days after each conference, the agent runs a full health check — qualified lead rate vs rolling average, cost per meeting vs target, follow-up reply rate by tier, pipeline generated vs sponsorship cost. Alerts fire if any metric falls below critical thresholds (qualified lead rate <12%, cost per meeting >2x rolling average, follow-up reply rate <8%).
- **Cross-conference trend analysis**: After every 2 conferences, compare the latest pair against the rolling average of all previous conferences. Flag any metric declining for 2 consecutive events.
- **Conference post-mortems**: 30 days after each conference (when lagging pipeline data arrives), generate a structured post-mortem: metrics vs targets, what worked, what needs attention, and whether to re-sponsor this conference.
- **Quarterly program reports**: Aggregate all conferences for the quarter. Rank by ROI. Identify patterns in what drives success. Generate sponsorship budget reallocation recommendations.

The monitoring outputs feed directly into the autonomous optimization loop.

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the conference booth program:

**Phase 1 — Monitor (runs weekly via n8n cron, intensifies to daily in the 2 weeks after each conference):**
- Pull conference program KPIs from PostHog: qualified lead rate, cost per meeting, follow-up conversion rate, pipeline per sponsorship dollar
- Compare the latest 2 conferences' metrics against the 3-conference rolling average
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ conferences), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather the current program configuration from Attio: conference selection criteria weights, sponsorship tier strategy, demo track in use, follow-up sequence copy and timing, pre-event outreach template
- Pull metric history from all conferences in PostHog
- Run hypothesis generation with anomaly data + configuration context
- Receive 3 ranked hypotheses. Examples of conference-specific hypotheses:
  - "Qualified lead rate dropped because the last 2 conferences were in a new industry vertical with lower ICP density. Hypothesis: returning to the original vertical will restore qualified lead rates to the rolling average."
  - "Cost per meeting spiked because the sponsorship tier upgrade at the last conference did not produce proportionally more meetings. Hypothesis: downgrading back to mid-tier and investing the savings in pre-event outreach will reduce cost per meeting by 25%."
  - "Follow-up reply rate declining because Tier 2 email copy is stale after 6 conferences. Hypothesis: refreshing email templates with recent case study references will increase reply rate by 10 percentage points."
  - "Pre-event outreach open rate dropped because subject lines have become predictable. Hypothesis: testing a question-based subject line will increase open rate by 15%."
- If top hypothesis has risk = "high" (e.g., dropping a high-cost conference entirely, changing the ICP targeting), send Slack alert for human approval. Otherwise, proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment. Conference-specific experiment types:
  - **Conference selection test**: Sponsor one conference from a new category and compare ROI against the proven conference type
  - **Tier test**: Test mid-tier vs premium-tier at two similar conferences, compare cost per meeting
  - **Follow-up test**: Split leads from one conference — half get the current sequence, half get the variant
  - **Pre-event test**: A/B test outreach copy within the same conference's target list
  - **Demo track test**: Use different demo approaches at consecutive conferences, compare meeting conversion
  - **Timing test**: Send follow-up at variant timing (4 hours vs 12 hours vs 24 hours) — split across leads within one conference
- Set experiment duration: minimum 2 conferences or 6 weeks, whichever is longer (conference cycles are slow)
- Log experiment start in Attio with hypothesis, variants, success criteria, and expected duration

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation: is the improvement statistically significant given conference-level sample sizes?
- Decision:
  - **Adopt**: Winner improves primary metric with sufficient confidence. Update the program configuration. Log the change.
  - **Iterate**: Promising direction but small sample (conference n is inherently low). Extend for 1-2 more conferences.
  - **Revert**: Variant performed worse. Restore the previous approach. Log the failure and the learning.
  - **Extend**: Insufficient data (common with conference-cycle experiments). Run for 2 more events.
- Store the full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected since last brief
  - Experiments in progress (status, preliminary data if available)
  - Experiments completed (decisions, impact)
  - Net metric change from adopted experiments
  - Upcoming conferences and pre-event preparation status
  - Distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 3. Configure conference-specific guardrails

The `autonomous-optimization` drill has standard guardrails. Add these conference-specific constraints:

- **Budget commitment guard**: Conference sponsorships require advance payment. Never commit to a sponsorship costing >$5,000 without human approval. Never exceed the quarterly conference budget by more than 20%.
- **Conference diversity guard**: Never sponsor more than 2 conferences in the same vertical in a single quarter. Test diversity to avoid audience overlap and fatigue.
- **Experiment pacing guard**: Because conferences happen monthly (not daily), experiments take longer. Maximum 2 concurrent experiments. Never test more than 1 variable at the same conference.
- **Relationship guard**: If an experiment involves dropping a conference, consider the relationship impact. Some conference organizers offer loyalty discounts or premium placement to returning sponsors. Flag for human review before dropping any conference with a 2+ year sponsorship history.
- **Lead data guard**: Badge scan data arrives in batches (post-event). Do not evaluate experiments until 14 days after the latest conference in the experiment (full follow-up window).
- **Seasonal guard**: Factor in seasonal conference patterns. Q1 and Q4 tend to have fewer conferences. Do not flag low volume in these quarters as degradation.

### 4. Build the convergence detection system

Track the percentage improvement from each adopted experiment. When 3 consecutive experiments produce <2% improvement on the primary metric (cost per meeting):

1. The conference program is converging — most tactical levers have been optimized
2. Reduce experimentation frequency to 1 experiment per quarter (maintenance mode)
3. Generate a convergence report: "This conference program is optimized at [current metrics]. The best-performing configuration is [conference types, tier, demo approach, follow-up sequence, pre-event strategy]. Further improvement requires strategic changes: entering new geographies, targeting new buyer personas, adding co-marketing partnerships with conference organizers, or shifting from booth-only to booth + speaking slot."

**Human action required:** At convergence, review the report. Decide whether to:
- Accept the local maximum and run the program in maintenance mode
- Reset by expanding to new conference categories or geographies
- Invest in strategic changes (co-hosting, keynote slots, sponsored workshops) that shift the performance ceiling

### 5. Sustain the program over 12 months

Over a 12-month Durable run, the agent:

- Manages a 6-8 conference annual program with automated operations
- Runs 6-12 experiments across all conference variables (paced by the conference cycle)
- Generates 48+ weekly optimization briefs
- Produces quarterly program health reports
- Detects and responds to seasonal patterns, market shifts, and competitive dynamics
- Refreshes the conference scoring model bi-annually based on accumulated ROI data
- Identifies when conference audiences are overlapping (same attendees at multiple events) and recommends diversification
- Tracks lagging indicators: closed-won deals from conference leads, revenue attributed to conference program, LTV of conference-sourced customers

The play is durable when the agent can maintain meetings-per-conference and cost-per-meeting at or above the Scalable benchmark without human optimization effort. Human involvement is limited to: attending conferences, giving demos, and approving high-risk experiments.

## Time Estimate

- Monitoring setup (PostHog dashboards, n8n crons, alert configuration): 6 hours
- Autonomous optimization loop configuration: 4 hours
- Guardrail and convergence detection setup: 3 hours
- Per-conference agent-managed effort (pre-event, enrichment, follow-up, reporting): 5 hours x 8 conferences = 40 hours
- Per-conference human effort (booth attendance, demos): conference attendance time (not counted)
- Experiment design and implementation: 4 hours x 8 experiments = 32 hours
- Weekly brief review: 30 min x 48 weeks = 24 hours
- Quarterly program review: 3 hours x 4 = 12 hours
- **Total: ~120 hours over 12 months** (split: ~80 hours agent, ~40 hours human review/decisions)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Conference scoring + attendee enrichment | $185/mo Launch (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Attio | CRM, conference pipeline, deal tracking, reporting | $29/user/mo Plus — [attio.com](https://attio.com) |
| PostHog | Event tracking, funnels, experiments, anomaly detection | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Automated follow-up nurture | $49/mo (5,000 contacts) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Monitoring crons, optimization loop, pre-event automation | Self-hosted free or Cloud Pro EUR60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Cal.com | Meeting booking | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Loom | Personalized follow-up videos | $12.50/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |
| Anthropic API | Hypothesis generation + experiment evaluation (Claude) | Usage-based ~$15-30/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost at Durable: $400-600/mo + sponsorship costs** (sponsorship budget typically $15,000-40,000/year for a 6-8 conference program)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor conference metrics, diagnose anomalies, generate hypotheses, run experiments across conference selection/booth tactics/follow-up sequences, evaluate results, auto-implement winners, and generate weekly optimization briefs
- `autonomous-optimization` — continuous monitoring with post-event health checks, cross-conference trend analysis, quarterly program reports, and degradation alerts that feed data into the optimization loop
