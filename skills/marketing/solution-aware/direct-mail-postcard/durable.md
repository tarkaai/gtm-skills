---
name: direct-mail-postcard-durable
description: >
  Direct Mail Postcards — Durable Intelligence. AI agents autonomously optimize postcard
  campaigns by detecting metric anomalies, generating improvement hypotheses, running A/B
  experiments, and auto-implementing winners. Finds and maintains the local maximum.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Other"
level: "Durable Intelligence"
time: "20 hours setup + 2 hours/week ongoing over 6 months"
outcome: "Response rate and cost per meeting sustained at or above Scalable baseline for 6 consecutive months; successive optimization experiments produce <2% improvement (convergence)"
kpis: ["Response rate trend", "Cost per meeting trend", "Experiment win rate", "Pipeline generated per month", "Convergence score"]
slug: "direct-mail-postcard"
install: "npx gtm-skills add marketing/solution-aware/direct-mail-postcard"
drills:
  - autonomous-optimization
  - postcard-ab-testing
  - dashboard-builder
---

# Direct Mail Postcards — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Other

## Outcomes

The direct mail channel runs on autopilot with AI agents continuously finding the local maximum. The `autonomous-optimization` drill monitors response rates, cost per meeting, and pipeline generated; when metrics plateau or drop, it generates hypotheses, designs postcard A/B experiments, runs them through the `postcard-ab-testing` drill, evaluates results, and auto-implements winners. The system converges when successive experiments produce less than 2% improvement — meaning the play has reached its optimal performance given current market conditions.

## Leading Indicators

- Weekly optimization loop running without human intervention
- At least 1 experiment running at all times (or convergence declared)
- Response rate stable or improving month-over-month
- Cost per meeting trending flat or down
- Weekly optimization briefs delivered to Slack/email on schedule
- Experiment win rate ≥ 30% (at least 1 in 3 experiments improve the metric)

## Instructions

### 1. Build the direct mail performance dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard with these panels:

**Real-time panels:**
- Postcards sent this week / this month (trend line)
- Delivery rate (delivered / sent) — target ≥ 90%
- Response rate (14-day attributed responses / delivered) — trend line with Scalable baseline marked
- Response breakdown by type (URL visit, email reply, meeting booked) — stacked bar
- Response rate by signal type (job change, funding, hiring, competitor) — compare segments

**Unit economics panels:**
- Cost per postcard (should decrease if Lob tier upgrades with volume)
- Cost per response (trend line)
- Cost per meeting (trend line with $50 target line)
- Pipeline generated per month (bar chart)
- ROI: pipeline generated / total direct mail spend

**Optimization panels:**
- Active experiments (count and description)
- Experiment history (last 10: hypothesis, result, confidence)
- Winning variant adoption log
- Convergence tracker: % improvement from last 3 experiments (converging when <2%)

### 2. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for direct mail. This is the core of Durable — the always-on agent loop that finds and maintains the local maximum.

**Configure the optimization loop with these direct-mail-specific parameters:**

**Monitored KPIs:**
- Primary: Response rate (14-day attributed)
- Secondary: Cost per meeting, pipeline generated per postcard

**Anomaly detection thresholds:**
- Normal: response rate within ±10% of 4-week rolling average
- Plateau: ±2% change for 3+ consecutive weeks
- Drop: >20% decline from 4-week average
- Spike: >50% increase (investigate — may be an outlier or seasonal)

**Hypothesis generation context:** When an anomaly is detected, the agent should consider these optimization variables specific to direct mail:

1. **Copy variables:** Headline framing, body copy length, CTA text, value proposition angle
2. **Design variables:** Postcard size (4x6 vs 6x9), color scheme, image vs. text-heavy, QR code placement
3. **Targeting variables:** Signal type weighting, ICP segment prioritization, company size range, geographic targeting
4. **Timing variables:** Send day of week (to control approximate delivery day), frequency (weekly vs. biweekly), follow-up timing (3 days vs. 5 days after delivery)
5. **Follow-up variables:** Email subject line, email copy, LinkedIn vs. email first, number of follow-up touches

**Experiment execution:** When the optimization loop selects a hypothesis, it runs the `postcard-ab-testing` drill:
1. Creates the variant template in Lob
2. Splits the next send batch into control and treatment
3. Sends both variants
4. Waits for the attribution window (14-21 days)
5. Evaluates results and decides: adopt, iterate, or revert

**Guardrails for direct mail experiments:**
- Never test more than 1 variable at a time
- Minimum 150 postcards per variant per experiment
- Never exceed budget by more than 20% (postcard costs are real money)
- If response rate drops below 2% for 2 consecutive weeks, pause new experiments and alert the founder
- Maximum 2 experiments per month (direct mail response cycles are slow)

### 3. Set up weekly optimization briefs

The `autonomous-optimization` drill generates a weekly brief. Configure it to include direct-mail-specific content:

**Weekly Direct Mail Optimization Brief:**
- Postcards sent/delivered this week
- Response rate this week vs. 4-week average
- Active experiment status (hypothesis, current sample size, preliminary results)
- Last completed experiment (result, confidence, whether adopted)
- Cost per meeting this week
- Pipeline generated this week
- Agent recommendation for next week (continue monitoring, start new experiment, or flag for human review)
- Convergence status: current delta from estimated local maximum

Deliver the brief via Slack and store in Attio as a campaign note.

### 4. Handle convergence

When the optimization loop detects convergence (3 consecutive experiments each producing <2% improvement):

1. Declare the play optimized at its local maximum
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment cadence from 2/month to 1/month (maintenance mode)
4. Generate a convergence report:
   - Final optimized response rate
   - Final cost per meeting
   - Total experiments run and win rate
   - All adopted changes (the accumulated improvements that got you here)
   - Recommendation: "Further gains require strategic changes (new ICP segments, new offer, new channel combinations) rather than tactical optimization"
5. Shift agent focus to monitoring for market changes that might un-converge the play:
   - Competitor starts sending direct mail to the same ICP (dilution)
   - ICP firmographic changes (mergers, layoffs, industry shifts)
   - Seasonal patterns (response rates may vary by quarter)
   - Postage or printing cost increases affecting unit economics

### 5. Continuous market adaptation

Even after convergence, the agent should:
- Monitor for external changes weekly (news, competitor activity, USPS rate changes)
- Re-run the full optimization loop if response rate drops >15% from converged baseline
- Test 1 new hypothesis per month in maintenance mode to detect emerging opportunities
- Refresh prospect lists in Clay — address data goes stale as people change jobs and companies move offices

## Time Estimate

- 8 hours: Dashboard creation and configuration (one-time)
- 8 hours: Autonomous optimization loop configuration and testing (one-time)
- 4 hours: Guardrails, convergence criteria, and brief template setup (one-time)
- 2 hours/week: Review weekly briefs, approve high-risk experiments, strategic adjustments
- Total: ~20 hours setup + 2 hours/week ongoing (~70 hours over 6 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Lob | Print, mail, track postcards at scale | $260-$550/mo + $0.48-$0.51/pc. https://www.lob.com/pricing |
| Clay | Signal detection, enrichment, address sourcing | From $249/mo (Pro). https://www.clay.com/pricing |
| Attio | CRM — contacts, campaigns, experiment logs | Pro from $29/seat/mo. https://attio.com/pricing |
| PostHog | Analytics, experiments, anomaly detection, dashboards | Free up to 1M events/mo. https://posthog.com/pricing |
| n8n | Optimization loop scheduling, webhook processing | Free (self-hosted) or from $24/mo. https://n8n.io/pricing |
| Anthropic API | Hypothesis generation and experiment evaluation (Claude) | Pay per token. ~$10-$30/mo at this usage level. https://www.anthropic.com/pricing |
| Instantly | Follow-up email sequences | From $30/mo. https://instantly.ai/pricing |

**Estimated total monthly cost at 500-1000 postcards/month:**
- Lob: $500-$800/mo (platform + per-piece)
- Clay: ~$249/mo
- Anthropic API: ~$20/mo
- Other tools: ~$150/mo
- **Total: ~$900-$1,250/mo**

## Drills Referenced

- `autonomous-optimization` — The core always-on loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and report weekly
- `postcard-ab-testing` — Execute the A/B experiments proposed by the optimization loop
- `dashboard-builder` — Build the PostHog dashboard for real-time direct mail performance monitoring
