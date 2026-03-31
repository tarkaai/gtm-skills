---
name: need-assessment-framework-durable
description: >
  Need Assessment Framework — Durable Intelligence. Always-on AI agents autonomously optimize the
  need scoring model, discovery question sequences, and qualification thresholds. The autonomous-optimization
  drill runs the core loop: detect metric anomalies, generate improvement hypotheses, run A/B
  experiments, evaluate results, auto-implement winners. Weekly optimization briefs. Converges when
  successive experiments produce <2% improvement.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving need assessment accuracy (>=80% completion, close rate prediction within 15%) over 6 months with autonomous optimization finding the local maximum of need scoring precision"
kpis: ["Need assessment accuracy (true positive rate)", "Autonomous experiment win rate", "False negative rate", "Close rate prediction accuracy trend", "Need scoring model drift detection", "Cost per qualified lead trend"]
slug: "need-assessment-framework"
install: "npx gtm-skills add sales/qualified/need-assessment-framework"
drills:
  - autonomous-optimization
  - signal-detection
---

# Need Assessment Framework — Durable Intelligence

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Outcomes

The need assessment system runs autonomously, continuously improving itself. An AI agent monitors need scoring metrics, detects when assessment accuracy degrades or market needs shift, generates hypotheses for improvement, runs experiments, and auto-implements winners. The system finds and maintains the local maximum of need scoring precision — the best possible qualification accuracy given your market, ICP, and competitive landscape.

Human involvement is limited to: conducting discovery calls, reviewing weekly optimization briefs, and approving high-risk changes flagged by the agent.

## Leading Indicators

- Autonomous optimization loop is running: anomalies detected, hypotheses generated, experiments launched without human initiation
- Weekly optimization briefs are being delivered on schedule with actionable content
- Need scoring accuracy is stable or improving month-over-month
- False negative rate is trending down (fewer good deals are being incorrectly disqualified due to need assessment)
- Experiments are producing diminishing returns (approaching the local maximum)
- Need category relevance is being maintained — the agent detects when market needs shift and recommends category updates
- Cost per qualified lead is stable at or near its minimum

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the need assessment play. This is the core drill that makes Durable fundamentally different from Scalable. Configure the five phases:

**Phase 1 — Monitor (daily via n8n cron):**
- Use PostHog anomaly detection to check need assessment KPIs daily
- Compare last 2 weeks against 4-week rolling average for:
  - Assessment completion rate (% of opportunities with complete need scoring)
  - Hypothesis accuracy (correlation between pre-call hypothesis and post-call scores)
  - False positive rate (High Need leads that close lost)
  - False negative rate (Low Need leads that later re-engage or close elsewhere)
  - Qualification rate (% meeting minimum threshold)
  - Need category distribution (is one category dominating or dropping off?)
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context: current scoring weights, enrichment provider hit rates, need category definitions, recent experiment results
- Pull 8-week metric history from PostHog
- Run Claude `hypothesis-generation` with the anomaly data
- Receive 3 ranked hypotheses. Examples of need-assessment-specific hypotheses:
  - "The 'reducing operational cost' need category has dropped from 40% Critical to 15% Critical over 6 weeks — market conditions may have shifted priorities toward growth over cost reduction. Recommend redefining this category or replacing with 'accelerating time-to-market.'"
  - "Pre-call hypothesis accuracy for tech companies has degraded from 70% to 45% — LinkedIn job posting data from Clay is returning stale results. Recommend adding a secondary enrichment source for tech stack analysis."
  - "The qualification threshold of 12 is producing a 25% false negative rate — lowering to 10 would capture 18% more true positives with only 5% more false positives."
  - "Discovery question sequence starting with the prospect's strongest predicted need is producing higher rapport but lower information gain — switching to uncertainty-first may improve scoring completeness."
- Store hypotheses in Attio. If top hypothesis is high-risk, alert founder for review.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design experiment using PostHog feature flags
- For scoring changes: split new leads into control (current model) and variant (hypothesis change). Both groups get scored, but only the control model routes deals. After the experiment, compare which model better predicted actual outcomes.
- For need category changes: run both category sets in parallel on new transcripts and compare which produces more discriminating scores
- For threshold changes: split traffic and measure pipeline velocity for each threshold
- For discovery question changes: A/B test question sequences across discovery calls
- Minimum experiment duration: 7 days or 50+ samples per variant

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update the live scoring model/threshold/question sequence. Log the change in Attio.
- If Revert: restore previous configuration. Log the failure.
- If Iterate: generate a refined hypothesis building on the result.

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity for the week
- Generate a weekly need assessment optimization brief:
  - Anomalies detected and their root causes
  - Experiments running and their current status
  - Experiments completed with results (adopted, reverted, or extended)
  - Net change in assessment accuracy this week
  - Need category health: which categories are gaining or losing relevance
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 2. Deploy signal-based need detection

Run the `signal-detection` drill to configure always-on monitoring for need-relevant buying signals:

- **Job posting signals:** Clay monitors for new listings at target accounts that match your need categories. Example: a prospect posting for a "Data Operations Manager" signals "reducing manual data entry" need emerging.
- **Tech stack change signals:** BuiltWith or Wappalyzer detect when a prospect adds, removes, or changes tools in your category — this shifts their need profile.
- **Growth signals:** Funding announcements, headcount surges, new product launches — these create scaling needs that map to your need categories.
- **Competitor signals:** Prospect starts using a competitor (detected via job postings or tech stack) — they have the need, just chose a different solution. Monitor for churn signals from that competitor.
- **Industry shift signals:** Regulatory changes, market downturns, or industry consolidation that would change which of your need categories are Critical vs. Low for entire segments.

When a signal fires, automatically:
1. Check if the account is already in your pipeline
2. If yes: re-run the need hypothesis. If the predicted need profile has changed materially (>3 point total score change), alert the founder and suggest re-discovery
3. If no: create a new deal in Attio, run through the auto-hypothesis pipeline, and route appropriately

### 3. Build durable need intelligence reporting

Run the `autonomous-optimization` drill with Durable-level additions:

- **Scoring model drift dashboard:** Track how the need scoring model's accuracy changes over time. If the model that was 80% accurate in month 1 drops to 60% in month 3, the autonomous optimization loop should have detected and addressed this — if it hasn't, flag for strategic review.
- **Need category evolution tracker:** Which need categories are gaining relevance (more prospects scoring Critical) and which are fading? This is a market intelligence signal — your customers' problems are shifting.
- **Experiment performance tracking:** Cumulative impact of all experiments. How much has the model improved since Scalable level?
- **Market need decay analysis:** Which enrichment signals lose predictive value fastest? This informs which data points need more frequent refresh.
- **Monthly calibration report:** Automated comparison of need scores at assessment time vs. actual deal outcomes (won/lost). Feeds back into the optimization loop.

### 4. Establish guardrails

Configure safety limits in the autonomous optimization loop:

- **Maximum 1 active experiment at a time** for need scoring changes
- **Revert threshold:** If qualification rate drops >30% during an experiment, auto-revert immediately
- **Human approval required for:**
  - Adding or removing a need category (structural scoring change)
  - Lowering the qualification threshold below 10
  - Changing scoring weights such that any single category contributes >40% of the total possible score
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** 7 days between experiments on the same variable
- **Maximum 4 experiments per month.** If all 4 fail, pause optimization and flag for strategic review.

### 5. Monitor for convergence

The optimization loop runs indefinitely. It should detect convergence — when successive experiments produce <2% improvement for 3 consecutive experiments. At convergence:

1. The need scoring model has reached its local maximum for your current market
2. Reduce monitoring frequency from daily to weekly
3. Report to the team: "Need assessment is optimized. Current accuracy: {X}%. Top need categories: {list}. Further gains require strategic changes (new ICP segments, new need categories reflecting market shifts, product changes) rather than scoring formula optimization."
4. Shift the agent's focus to signal detection and market need evolution rather than scoring optimization

### 6. Evaluate sustainability

Measure against: sustained or improving need assessment accuracy (>=80% completion, close rate prediction within 15%) over 6 months with the autonomous optimization loop finding and maintaining the local maximum.

This level runs continuously. Monthly review:
- Is the optimization loop producing value? (Experiments winning, accuracy improving)
- Is the loop converging? (Diminishing returns on experiments)
- Are there market shifts the loop cannot handle? (New competitor, product pivot, economic change shifting buyer needs)
- Are need categories still relevant? (Or has the market moved to different problems)
- Is cost per qualified lead stable?

## Time Estimate

- Autonomous optimization loop setup: 12 hours
- Signal detection configuration: 8 hours
- Reporting and guardrail setup: 6 hours
- Ongoing monitoring and brief review: 4 hours/month (24 hours over 6 months)
- Discovery calls (ongoing): 6 hours/month (36 hours over 6 months)
- Strategic reviews and calibration: 4 hours/month (24 hours over 6 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with need assessment pipeline and experiment logging | Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment + signal monitoring at scale | Growth $495/mo — [clay.com/pricing](https://clay.com/pricing) |
| Instantly | Cold email sequences (auto-optimized) | Hypergrowth $97/mo — [instantly.ai/pricing](https://instantly.ai/pricing) |
| n8n | Automation: optimization loop, reporting, alerts | Pro $60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Fireflies | Call transcription for ongoing discovery calls | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics, experiments, anomaly detection, feature flags | Usage-based, ~$50-200/mo at scale — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, need extraction | ~$50-100/mo at Durable volume — [docs.anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Cal.com | Scheduling | Free — [cal.com/pricing](https://cal.com/pricing) |

**Estimated play-specific cost:** ~$750-1,000/mo (Clay $495 + Instantly $97 + n8n $60 + Fireflies $18 + PostHog ~$50-200 + Anthropic ~$50-100)

## Drills Referenced

- `autonomous-optimization` — the core always-on optimization loop: monitor > diagnose > experiment > evaluate > implement
- `autonomous-optimization` — durable-level dashboards with scoring model drift tracking, need category evolution, experiment impact, and signal decay analysis
- `signal-detection` — always-on monitoring for need-relevant buying signals that trigger re-hypothesis or new lead creation
