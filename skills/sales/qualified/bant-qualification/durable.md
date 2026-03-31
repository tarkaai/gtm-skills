---
name: bant-qualification-durable
description: >
  BANT Qualification Framework — Durable Intelligence. Always-on AI agents autonomously optimize
  the BANT scoring model, outreach strategy, and qualification thresholds. The autonomous-optimization
  drill runs the core loop: detect metric anomalies, generate improvement hypotheses, run A/B
  experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when
  successive experiments produce <2% improvement.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving qualification accuracy (>=35%) over 6 months with autonomous optimization finding the local maximum of BANT scoring precision"
kpis: ["Qualification accuracy (true positive rate)", "Autonomous experiment win rate", "False negative rate", "Time-to-qualification trend", "Scoring model drift detection", "Cost per qualified lead trend"]
slug: "bant-qualification"
install: "npx gtm-skills add sales/qualified/bant-qualification"
drills:
  - autonomous-optimization
  - bant-qualification-reporting
  - signal-detection
---

# BANT Qualification Framework — Durable Intelligence

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

The BANT qualification system runs autonomously, continuously improving itself. An AI agent monitors qualification metrics, detects when scoring accuracy degrades, generates hypotheses for improvement, runs experiments, and auto-implements winners. The system finds and maintains the local maximum of BANT scoring precision — the best possible qualification rate given your market, ICP, and competitive landscape.

Human involvement is limited to: conducting discovery calls, reviewing weekly optimization briefs, and approving high-risk changes flagged by the agent.

## Leading Indicators

- Autonomous optimization loop is running: anomalies detected, hypotheses generated, experiments launched without human initiation
- Weekly optimization briefs are being delivered on schedule with actionable content
- Scoring accuracy is stable or improving month-over-month
- False negative rate is trending down (fewer good deals are being incorrectly disqualified)
- Experiments are producing diminishing returns (approaching the local maximum)
- Cost per qualified lead is stable at or near its minimum

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the BANT qualification play. This is the core drill that makes Durable fundamentally different from Scalable. Configure the five phases:

**Phase 1 — Monitor (daily via n8n cron):**
- Use PostHog anomaly detection to check BANT qualification KPIs daily
- Compare last 2 weeks against 4-week rolling average for:
  - Qualification rate (% of scored leads reaching composite >=70)
  - Pre-score accuracy (correlation between pre-enrichment and post-call scores)
  - False positive rate (qualified leads that close lost)
  - False negative rate (disqualified leads that re-engage or close elsewhere)
  - Time-to-qualification (days from lead entry to BANT verdict)
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: current scoring weights, enrichment provider hit rates, outreach reply rates, recent experiment results
- Pull 8-week metric history from PostHog
- Run Claude `hypothesis-generation` with the anomaly data
- Receive 3 ranked hypotheses. Examples of BANT-specific hypotheses:
  - "Budget scoring weight is too high — prospects with low budget scores but high need scores are converting at a higher rate than the model predicts"
  - "Authority enrichment accuracy has degraded — LinkedIn title data is stale for 30% of prospects"
  - "Timeline signals from funding rounds are less predictive than job posting signals — swap their weights"
  - "Qualification threshold of 70 is too aggressive — lowering to 65 would capture 12% more true positives with only 3% more false positives"
- Store hypotheses in Attio. If top hypothesis is high-risk, alert founder for review.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design experiment using PostHog feature flags
- For scoring changes: split new leads into control (current model) and variant (hypothesis change). Both groups get scored, but only the control model routes deals. After the experiment, compare which model better predicted actual outcomes.
- For outreach changes: A/B test messaging variants via Instantly
- For threshold changes: split traffic and measure pipeline velocity for each threshold
- Minimum experiment duration: 7 days or 50+ samples per variant

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update the live scoring model/threshold/outreach template. Log the change in Attio.
- If Revert: restore previous configuration. Log the failure.
- If Iterate: generate a refined hypothesis building on the result.

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity for the week
- Generate a weekly BANT optimization brief:
  - Anomalies detected and their root causes
  - Experiments running and their current status
  - Experiments completed with results (adopted, reverted, or extended)
  - Net change in qualification accuracy this week
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 2. Deploy signal-based lead sourcing

Run the `signal-detection` drill to configure always-on monitoring for BANT-relevant buying signals:

- **Budget signals:** Clay monitors for funding announcements, revenue milestones, new budget-relevant job postings (e.g., "Director of Procurement") at target accounts
- **Authority signals:** Job changes at target accounts — new VP/C-suite hires in relevant departments trigger automatic re-scoring
- **Need signals:** Competitor mentions in job postings, tech stack changes detected by BuiltWith, negative reviews of competitors on G2/Capterra
- **Timeline signals:** Contract renewal windows (estimated from competitor adoption dates), fiscal year approaching, regulatory deadlines in their industry

When a signal fires, automatically:
1. Check if the account is already in your pipeline
2. If yes: re-score the deal and alert the founder if the composite score crosses a threshold
3. If no: create a new deal in Attio, run through auto-scoring, and route appropriately

### 3. Build durable qualification reporting

Run the `bant-qualification-reporting` drill with Durable-level additions:

- **Scoring model drift dashboard:** Track how the scoring model's accuracy changes over time. If the model that was 80% accurate in month 1 drops to 65% in month 3, the autonomous optimization loop should have detected and addressed this — if it hasn't, flag for strategic review.
- **Experiment performance tracking:** Cumulative impact of all experiments. How much has the model improved since Scalable level?
- **Market signal decay analysis:** Which enrichment signals lose predictive value fastest? This informs which data points need more frequent refresh.
- **Monthly calibration report:** Automated comparison of BANT scores at qualification time vs. actual deal outcomes (won/lost). Feeds back into the optimization loop.

### 4. Establish guardrails

Configure safety limits in the autonomous optimization loop:

- **Maximum 1 active experiment at a time** for BANT scoring changes
- **Revert threshold:** If qualification rate drops >30% during an experiment, auto-revert immediately
- **Human approval required for:**
  - Changing scoring weights by more than 10 points on any dimension
  - Lowering the qualification threshold below 60
  - Changing the BANT formula structure (e.g., adding/removing a dimension)
- **Cooldown:** 7 days between experiments on the same variable
- **Maximum 4 experiments per month.** If all 4 fail, pause optimization and flag for strategic review.

### 5. Monitor for convergence

The optimization loop runs indefinitely. It should detect convergence — when successive experiments produce <2% improvement for 3 consecutive experiments. At convergence:

1. The BANT scoring model has reached its local maximum for your current market
2. Reduce monitoring frequency from daily to weekly
3. Report to the team: "BANT qualification is optimized. Current accuracy: {X}%. Further gains require strategic changes (new ICP segments, new enrichment providers, product changes) rather than scoring formula optimization."
4. Shift the agent's focus to signal detection and lead sourcing rather than scoring optimization

### 6. Evaluate sustainability

Measure against: sustained or improving qualification accuracy (>=35%) over 6 months with the autonomous optimization loop finding and maintaining the local maximum.

This level runs continuously. Monthly review:
- Is the optimization loop producing value? (Experiments winning, accuracy improving)
- Is the loop converging? (Diminishing returns on experiments)
- Are there market shifts the loop cannot handle? (New competitor, product pivot, economic change)
- Is cost per qualified lead stable?

## Time Estimate

- Autonomous optimization loop setup: 12 hours
- Signal detection configuration: 8 hours
- Reporting and guardrail setup: 6 hours
- Ongoing monitoring and brief review: 4 hours/month (24 hours over 6 months)
- Discovery calls (ongoing): 8 hours/month (48 hours over 6 months)
- Strategic reviews and calibration: 4 hours/month (24 hours over 6 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with BANT pipeline and experiment logging | Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment + signal monitoring at scale | Growth $495/mo — [clay.com/pricing](https://clay.com/pricing) |
| Instantly | Cold email sequences (auto-optimized) | Hypergrowth $97/mo — [instantly.ai/pricing](https://instantly.ai/pricing) |
| n8n | Automation: optimization loop, reporting, alerts | Pro $60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Fireflies | Call transcription for ongoing discovery calls | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics, experiments, anomaly detection, feature flags | Usage-based, ~$50-200/mo at scale — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, BANT extraction | ~$50-100/mo at Durable volume — [docs.anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Cal.com | Scheduling | Free — [cal.com/pricing](https://cal.com/pricing) |

**Estimated play-specific cost:** ~$750-1,000/mo (Clay $495 + Instantly $97 + n8n $60 + Fireflies $18 + PostHog ~$50-200 + Anthropic ~$50-100)

## Drills Referenced

- `autonomous-optimization` — the core always-on optimization loop: monitor > diagnose > experiment > evaluate > implement
- `bant-qualification-reporting` — durable-level dashboards with model drift tracking, experiment impact, and signal decay analysis
- `signal-detection` — always-on monitoring for BANT buying signals that trigger re-scoring or new lead creation
