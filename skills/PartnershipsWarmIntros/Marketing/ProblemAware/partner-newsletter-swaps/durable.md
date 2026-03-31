---
name: partner-newsletter-swaps-durable
description: >
  Partner Newsletter Swaps — Durable Intelligence. Always-on AI agents autonomously optimize
  partner selection, email variant performance, swap cadence, and audience targeting to find
  and maintain the local maximum of the list swap program.
stage: "Marketing > ProblemAware"
motion: "PartnershipsWarmIntros"
channels: "Email"
level: "Durable Intelligence"
time: "Ongoing (~4 hours/month agent oversight)"
outcome: "Sustained >=20 swaps/month, >=800 subscribers/month, >=15 leads/month with <2% month-over-month variance at convergence"
kpis: ["Monthly subscribers from swaps (trending)", "Monthly leads from swaps (trending)", "Experiment win rate", "Subscribers per swap (by partner)", "Cost per lead trend", "Convergence index"]
slug: "partner-newsletter-swaps"
install: "npx gtm-skills add PartnershipsWarmIntros/Marketing/ProblemAware/partner-newsletter-swaps"
drills:
  - autonomous-optimization
  - list-swap-performance-reporting
---
# Partner Newsletter Swaps — Durable Intelligence

> **Stage:** Marketing > ProblemAware | **Motion:** PartnershipsWarmIntros | **Channels:** Email

## Outcomes
- The swap program runs autonomously with the agent managing the optimization cycle
- Sustained >=20 swaps/month, >=800 new subscribers/month, >=15 leads/month
- The agent detects metric anomalies, generates improvement hypotheses, runs A/B experiments, evaluates results, and auto-implements winners
- Performance converges when successive experiments produce <2% improvement — the play has found its local maximum
- Human intervention limited to: approving high-risk changes, reviewing weekly optimization briefs, and strategic direction

## Leading Indicators
- Anomaly detection triggers within 24 hours of a metric shift (no blind spots)
- Hypothesis quality: >=50% of experiments produce a measurable lift
- No metric drops >15% without the agent detecting and diagnosing within 48 hours
- Convergence index: standard deviation of weekly subscriber/lead counts shrinking over time
- Partner portfolio churn: <10% of active partners lost per quarter without replacement

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the list swap program. This drill creates the always-on agent loop:

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check swap KPIs: subscribers per swap, leads per swap, click-to-lead conversion rate, reciprocal balance ratio, partner response rates
- Compare last 2 weeks against the 4-week rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If normal: log to Attio, no action
- If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current partner roster, cadence tiers, email variants in use, recent swap results per partner
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with anomaly data + partner context. Generate 3 ranked hypotheses. Examples:
  - "Subscribers per swap declining because top 3 partners' audiences are saturated at monthly cadence. Hypothesis: reduce these partners to bimonthly and reallocate slots to newer partners."
  - "Click-to-lead conversion dropped 25%. Hypothesis: the curiosity email template has fatigued. Test the question template variant against the current default."
  - "Partner X's last 2 swaps generated 0 leads despite 80+ clicks. Hypothesis: the landing page CTA does not match the email promise. Test a swap-specific landing page."
- Store hypotheses in Attio as notes on the swap program record
- If top hypothesis is high-risk (budget change >20%, audience targeting change affecting >50% of traffic): send Slack alert for human approval. STOP until approved.
- If low/medium risk: proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Use `posthog-experiments` to create a feature flag splitting traffic between control and variant
- Implement the variant change. Experiment types specific to this play:
  - **Email variant test:** Two email templates sent to comparable partners in the same week. Compare click-to-lead rates.
  - **Cadence test:** Change a partner's swap frequency for 2 months. Compare subscribers/month before and after.
  - **Landing page test:** Split swap traffic to two landing pages. Compare lead conversion.
  - **Partner tier test:** Swap a "Volume" partner (high clicks, low conversion) for a new untested partner. Compare leads.
- Set minimum experiment duration: 14 days or 4 swaps per variant, whichever is longer
- Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull results from PostHog
- Run `experiment-evaluation` with control vs variant data
- Decision tree:
  - **Adopt** (variant wins by >=5% with >=90% confidence): Implement the change permanently. Update the master email template library, partner cadence tiers, or landing pages accordingly.
  - **Iterate** (directionally positive but inconclusive): Generate a refined hypothesis. Return to Phase 2.
  - **Revert** (variant loses or neutral): Disable variant, restore control. Log failure. Return to Phase 1. Enforce 7-day cooldown before testing the same variable.
  - **Extend** (insufficient data): Keep running for another cycle.
- Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron, Friday 3pm):**
- Aggregate all optimization activity for the week
- Calculate net metric change from adopted changes
- Generate the weekly optimization brief:
  - Anomalies detected and diagnoses
  - Experiments running, completed, and their outcomes
  - Net impact on subscribers/month and leads/month
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

**Guardrails (enforced by the agent):**
- Maximum 1 active experiment at a time
- Auto-revert if primary metric (leads/month) drops >30% during an experiment
- Human approval required for: partner removal, cadence changes affecting >5 partners, budget increases >20%
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- Cooldown: 7 days after a revert before testing the same variable

### 2. Build the list swap performance monitoring layer

Run the `list-swap-performance-reporting` drill to create the monitoring and reporting infrastructure specific to this play:

1. **PostHog dashboard** ("List Swaps — Partner Performance"):
   - Clicks by partner (bar chart, last 30 days)
   - Meetings by partner (bar chart, last 30 days)
   - Click-to-meeting conversion by partner (table, sorted descending)
   - Clicks over time (trend line, last 90 days)
   - Email variant performance (table, comparing curiosity vs data vs story vs question vs timely)
   - Swap funnel: page visit -> CTA click -> meeting booked (filtered to list-swap traffic)
   - Reciprocal performance: your list's response to each partner's email

2. **Swap performance cohorts:**
   - High-value partners: click-to-meeting rate >5%
   - Volume partners: >50 clicks per swap but low meeting conversion
   - Declining partners: clicks dropped >30% swap-over-swap
   - New partners: first swap in last 30 days
   - Reciprocity imbalanced: net value >3x in either direction

3. **Weekly swap brief** (automated via n8n, Friday 3pm):
   - This week vs 4-week average: clicks, meetings, conversion rate
   - Top partners by meetings generated
   - Anomalies detected with hypotheses
   - Reciprocity check: who owes whom
   - Email variant insights: best subject line, best variant
   - Swap pipeline: active count, scheduled next 2 weeks, partners needing email copy
   - Recommended actions

4. **Per-partner ROI tracker in Attio** (updated weekly by n8n):
   - Total swaps completed, clicks received, meetings generated, click-to-meeting rate
   - Total clicks given (reciprocal), net swap value
   - Best email variant, audience fatigue index, partner reliability score
   - Swap cadence tier, last/next swap dates

5. **Performance alerts:**
   - Partner swap <5 clicks: flag low engagement
   - Partner swap >3 meetings: flag for monthly cadence fast-track
   - Your list unsubscribe rate >0.5% on inbound swap: flag quality issue
   - Total swap meetings drop below Scalable baseline for 2 consecutive weeks: trigger `autonomous-optimization` investigation
   - Email variant >8% CTR: flag as proven template
   - Partner misses scheduled swap: alert for follow-up

### 3. Convergence detection and steady-state operation

The `autonomous-optimization` drill monitors for convergence. The play has reached its local maximum when:
- 3 consecutive experiments produce <2% improvement
- Monthly subscribers and leads are within +/-5% of the trailing 3-month average
- Partner portfolio is stable (churn < replacement rate)

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency from 4/month to 1/month (maintenance experiments)
3. Report: "List swap program optimized. Current performance: [X subscribers/month, Y leads/month]. Further gains require strategic changes: new partner segments, different audience tiers, or product-level changes to the swap offer."
4. Continue running the weekly swap brief and per-partner ROI tracking indefinitely

If market conditions change (new competitor enters, partner landscape shifts, your product repositions), the daily monitoring will detect the metric shift and re-enter the full optimization loop automatically.

---

## Time Estimate
- Autonomous optimization loop setup: 8 hours
- Performance reporting layer build: 6 hours
- Ongoing human oversight: ~4 hours/month (brief review, high-risk approvals, strategic direction)

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, dashboards, cohorts | Growth: $0.00045/event after 1M free (https://posthog.com/pricing) |
| n8n | Optimization loop scheduling, alerting, reporting | Cloud: $24/mo (https://n8n.io/pricing) |
| Attio | Partner CRM, experiment logging, ROI tracking | Plus: $34/user/mo (https://attio.com/pricing) |
| Anthropic (Claude) | Hypothesis generation, experiment evaluation, brief writing | API: ~$15/1M input tokens (https://www.anthropic.com/pricing) |
| Loops | Reciprocal sends, variant testing | Growth: $49/mo (https://loops.so/pricing) |

**Estimated play-specific cost:** ~$100-200/mo + variable agent compute (~$10-30/mo for Claude API calls)

## Drills Referenced
- `autonomous-optimization` — the core always-on loop: monitor metrics -> diagnose anomalies -> generate hypotheses -> run experiments -> evaluate results -> auto-implement winners -> report weekly
- `list-swap-performance-reporting` — play-specific monitoring: per-partner dashboards, swap cohorts, weekly briefs, ROI tracking, and performance alerts that feed the optimization loop
