---
name: partnerships-warm-intros-durable
description: >
  Partnerships & Warm Intros — Durable Intelligence. Always-on AI agents monitor connector
  performance, score partner relationships, run A/B experiments on ask templates and timing,
  and auto-implement winners. The autonomous-optimization loop finds the local maximum for
  intro volume, conversion rate, and deal value from warm intros.
stage: "Sales > Qualified"
motion: "PartnershipsWarmIntros"
channels: "Other"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving intro volume and meeting rate over 6 months; agents detect anomalies, generate hypotheses, run experiments, and auto-implement winners; converges when successive experiments produce <2% improvement"
kpis: ["Intro requests sent", "Intros received", "Meetings booked from intros", "Request-to-intro rate", "Intro-to-meeting rate", "Pipeline value from warm intros", "Connector portfolio health score", "Experiment win rate"]
slug: "partnerships-warm-intros"
install: "npx gtm-skills add sales/qualified/partnerships-warm-intros"
drills:
  - autonomous-optimization
  - warm-intro-performance-reporting
  - partner-relationship-scoring
---

# Partnerships & Warm Intros — Durable Intelligence

> **Stage:** Sales > Qualified | **Motion:** PartnershipsWarmIntros | **Channels:** Other

## Outcomes

The warm intro pipeline runs autonomously. AI agents monitor every metric, detect when performance changes, generate hypotheses for improvement, run controlled experiments, evaluate results, and implement winners. The `autonomous-optimization` drill is the core engine. Play-specific drills handle connector scoring and partnership reporting.

Pass threshold: **Sustained or improving intro volume and meeting rate over 6 months. Agents detect anomalies, run experiments, and auto-implement winners. Converges when successive experiments produce <2% improvement.**

## Leading Indicators

- Anomaly detection firing correctly (agent catches >90% of real metric changes within 24 hours)
- Experiment velocity (target: 2-3 experiments per month)
- Experiment win rate (target: >40% of experiments produce measurable improvement)
- Connector churn rate (target: <10% of Tier 1/2 connectors go dormant per quarter)
- Week-over-week intro volume stability (target: within +/- 15% of 4-week rolling average)
- Pipeline value per intro trending up or stable

## Instructions

### 1. Build the warm intro performance dashboard and reporting

Run the `warm-intro-performance-reporting` drill to create:

**PostHog Dashboard — "Warm Intros — Durable Performance":**
- Intro requests sent by connector (bar chart, last 30 days)
- Intros received by connector (bar chart, last 30 days)
- Request-to-intro conversion rate by connector (table, sorted descending)
- Meetings booked from intros by connector (bar chart, last 30 days)
- Intro-to-meeting conversion rate by connector (table, sorted descending)
- Full funnel: request -> intro -> meeting -> deal (funnel chart, last 90 days)
- Weekly intro volume trend (line chart, last 6 months)
- Ask template performance: request-to-intro rate by `ask_template_id` (table)

**Weekly automated brief (Friday 3pm via n8n):**
- Total requests, intros, meetings this week vs. 4-week average
- Top and bottom connectors by intro conversion
- Best and worst ask templates
- Recommended actions from `hypothesis-generation`

**Performance alerts:**
- Weekly intro volume drops >30% vs. prior week -> Slack alert
- Any Tier 1 connector goes 30+ days without an intro -> relationship check alert
- Overall request-to-intro rate drops below 25% for 2 weeks -> trigger autonomous optimization investigation
- A new connector delivers first intro within 48 hours -> flag as high-potential

### 2. Score and tier all connectors

Run the `partner-relationship-scoring` drill to establish the connector portfolio:

**Score every connector on 5 dimensions (50-point scale):**
- Response rate (1-10): What % of requests produce intros?
- Intro quality (1-10): What % of intros convert to meetings?
- Deal conversion (1-10): What % of meetings advance past discovery?
- Response speed (1-10): How quickly do they act on requests?
- Volume capacity (1-10): How many intros can they provide per quarter?

**Classify into tiers:**
- Tier 1 (40-50): Elite connectors. Prioritize relationship. Send best targets. Thank proactively.
- Tier 2 (25-39): Good connectors. Reliable with room to improve. Address weakest dimension.
- Tier 3 (10-24): Low-yield connectors. Reduce request frequency. Only send strongest matches.
- Tier 4 (1-9): Ineffective connectors. Stop requesting intros. Move to general network nurture.

**Monthly scoring automation (n8n cron, 1st of each month):**
1. Pull PostHog data for each connector (requests, intros, meetings, deals, response times)
2. Calculate all 5 dimension scores
3. Compute composite score and assign tier
4. Compare to prior month — flag improving and declining connectors
5. Generate monthly connector portfolio report in Attio
6. Feed tier data into the autonomous optimization loop (Tier 1 connectors get higher request priority)

### 3. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the warm intro play:

**Phase 1 — Monitor (daily via n8n cron):**
Use `posthog-anomaly-detection` to check:
- Request-to-intro rate vs. 4-week rolling average
- Intro-to-meeting rate vs. 4-week rolling average
- Weekly intro volume vs. 4-week rolling average
- Connector response rate by tier vs. tier benchmarks

Classify each metric: **normal** (within +/- 10%), **plateau** (within +/- 2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context from Attio: current connector portfolio health, recent request volume, template mix, target quality
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` to produce 3 ranked hypotheses. Examples:
   - "Request-to-intro rate dropped because Template B is being overused with investor connectors who respond better to Template A"
   - "Meeting volume plateau because Tier 1 connectors are being under-asked — increase request frequency for top 5 connectors"
   - "Intro-to-meeting rate spiked because recent targets are better qualified — the Crossbeam overlap filter is working"
4. Store hypotheses in Attio as notes on the partnerships campaign record
5. If top hypothesis is "high risk" (e.g., involves changing approach with Tier 1 connectors), send Slack alert for human review and STOP
6. If "low" or "medium" risk, proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**

Design experiments using `posthog-experiments`:

**Experiment types for this play:**

1. **Ask template A/B test:** Split connectors of the same tier into two groups. Group A gets current best template; Group B gets the variant. Measure request-to-intro rate per group over 2 weeks. Minimum 20 requests per group.

2. **Request timing test:** Test different days-of-week and times for sending intro requests. Split by connector and measure response rate and speed. Run for 4 weeks.

3. **Target selection test:** Test different target prioritization strategies. Group A: highest ICP score first. Group B: highest Crossbeam overlap first. Measure intro-to-meeting rate.

4. **Follow-up cadence test:** Test 3-day vs. 7-day follow-up timing for pending intro requests. Measure whether faster follow-up improves or hurts request-to-intro rate.

5. **Connector re-engagement test:** For Tier 3 connectors, test a "re-activation" approach (personal check-in, updated value prop) vs. standard cadence. Measure if Tier 3 connectors can be upgraded to Tier 2.

Set experiment duration: minimum 14 days or 30+ data points per variant, whichever is longer. Log experiment in Attio: hypothesis, variants, start date, expected duration, success metric.

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation` with control vs. variant data
3. Decision:
   - **Adopt:** Winning variant becomes the new default. Update templates, timing, or targeting in the live workflows. Log the change in Attio.
   - **Iterate:** Generate a new hypothesis building on this result. Return to Phase 2.
   - **Revert:** Disable the variant, restore previous approach. Log the failure. Return to Phase 1 monitoring.
   - **Extend:** Insufficient data. Keep running for another period.
4. Store evaluation (decision, confidence level, reasoning) in Attio

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments active, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on intro volume, conversion rate, and pipeline value
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 4. Guardrails

**Rate limit:** Maximum 1 active experiment at a time. Never stack experiments on the same variable.

**Revert threshold:** If request-to-intro rate drops >30% during an experiment, auto-revert immediately.

**Human approval required for:**
- Any change to Tier 1 connector communication approach
- Any change to the forwardable blurb template (this goes to the target, not just the connector)
- Adding or removing connectors from the Tier 1 list

**Cooldown:** After a failed experiment, wait 7 days before testing the same variable.

**Maximum experiments per month:** 3. If all 3 fail in a month, pause optimization and flag for human strategic review.

**Connector relationship protection:** Never send more than 2 intro requests to any single connector per month. Never ask a Tier 4 connector for intros. Always include a human-reviewed thank-you to connectors whose intros convert to deals.

### 5. Convergence detection

The optimization loop detects convergence when:
- 3 consecutive experiments produce <2% improvement on any metric
- All major variables (templates, timing, targeting, connector mix) have been tested at least twice
- Weekly metrics are stable within +/- 5% for 4+ consecutive weeks

At convergence:
1. Reduce monitoring from daily to weekly
2. Reduce experiment cadence from 2-3/month to 1/month (maintenance experiments)
3. Report: "Warm intro play is optimized. Current performance: {metrics}. Further gains require strategic changes (new connector channels, new market segments, product improvements) rather than tactical optimization."
4. Shift agent effort to connector portfolio expansion (recruiting new Tier 1 connectors to replace any who become dormant)

## Time Estimate

- 20 hours: Build dashboards, scoring system, alerts (month 1)
- 15 hours: Configure autonomous optimization loop with warm-intro-specific experiments (month 1)
- 10 hours/month: Monitor, review experiments, approve changes (months 2-6)
- 5 hours/month: Connector relationship management, human-required actions (months 2-6)
- 10 hours: Convergence analysis, documentation (month 6)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — connector scoring, deal tracking, experiment logging | $29/user/mo Plus ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Analytics — dashboards, funnels, experiments, anomaly detection | Free up to 1M events/mo; usage-based after ([posthog.com/pricing](https://posthog.com/pricing)) |
| Cal.com | Meeting booking with attribution | Free for 1 user; $15/user/mo Teams ([cal.com/pricing](https://cal.com/pricing)) |
| n8n | Automation — optimization loop, scoring crons, alerts, reporting | Free self-hosted; Cloud from ~$24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Crossbeam | Account mapping — ongoing connector discovery | Free tier; Connector from $400/mo ([crossbeam.com/pricing](https://www.crossbeam.com/pricing)) |
| Anthropic API | AI — hypothesis generation, experiment evaluation, brief writing | Usage-based; ~$15/1M input tokens for Claude ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Estimated Durable cost: $50-250/mo** (Attio Plus, n8n self-hosted, PostHog free tier, Crossbeam free tier, Anthropic API ~$10-30/mo for this play's volume)

## Drills Referenced

- `autonomous-optimization` — core optimization loop: monitor -> diagnose -> experiment -> evaluate -> implement
- `warm-intro-performance-reporting` — per-connector dashboards, weekly briefs, performance alerts
- `partner-relationship-scoring` — 5-dimension connector scoring with tier classification and monthly portfolio reports
