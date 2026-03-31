---
name: pain-discovery-framework-durable
description: >
  Pain Discovery Framework — Durable Intelligence. Always-on AI agents finding the local
  maximum of pain discovery effectiveness. Autonomous optimization loop detects metric
  anomalies, generates hypotheses, runs experiments on question banks and extraction
  prompts, and auto-implements winners. Market-level pain intelligence feeds GTM strategy.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving pain discovery effectiveness (>=70% quantification, >=10x cost) over 6 months via continuous agent-driven question optimization, benchmark refinement, and market adaptation"
kpis: ["Pain quantification rate", "Pain-to-price ratio trend", "Agent experiment win rate", "Business case win rate"]
slug: "pain-discovery-framework"
install: "npx gtm-skills add sales/connected/pain-discovery-framework"
drills:
  - autonomous-optimization
---

# Pain Discovery Framework — Durable Intelligence

> **Stage:** Sales > Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Achieve autonomous optimization of the entire pain discovery system. An always-on agent loop monitors discovery effectiveness, detects when metrics plateau or degrade, generates hypotheses for improvement, runs controlled experiments on question banks, extraction prompts, and business case formats, and auto-implements winners. Market-level pain intelligence feeds ICP refinement, content strategy, and competitive positioning.

Target: Sustained or improving effectiveness (>= 70% quantification rate, >= 10x pain-to-price ratio) over 6 months. Convergence detected when successive experiments produce < 2% improvement.

## Leading Indicators

- Autonomous optimization loop running without human intervention
- Weekly optimization briefs generated and delivered to Slack
- At least 1 experiment running at all times (until convergence)
- Question bank evolving: questions being retired and promoted monthly
- Market-level pain shifts detected before competitors react
- Business case win rate trending upward or stable over 3-month window

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for pain discovery. This creates the always-on monitor -> diagnose -> experiment -> evaluate -> implement cycle.

**Configure the optimization targets:**

| Metric | Data Source | Anomaly Threshold |
|--------|------------|-------------------|
| Pain-to-price ratio (avg) | PostHog | Drop below 8x for 2 weeks = trigger |
| Quantification rate | PostHog | Drop below 55% for 2 weeks = trigger |
| Business case conversion rate | Attio + PostHog | Drop 20% vs 4-week avg = trigger |
| Question surface rate (per question) | Attio | Drop 50% from peak = retire candidate |
| AI extraction recall | Attio (human corrections) | Drop below 75% = prompt tuning needed |

**Configure the experiment space:**

The optimization agent can experiment on these variables (low/medium risk):
- Discovery question ordering within the call prep
- New questions added to the question bank (tested on 10 calls before promotion)
- Pain extraction prompt wording (tested on historical transcripts before going live)
- Quantification prompt anchoring strategies
- Business case format and framing
- Call prep emphasis (which enrichment signals to highlight)

**Human approval required for:**
- Changes to the core ICP definition
- Changes affecting > 50% of active discovery calls simultaneously
- Any experiment the agent flags as "high risk"
- Budget increases for enrichment or tooling

**Guardrails:**
- Maximum 1 active experiment at a time
- Minimum 10 calls per variant before evaluation
- Auto-revert if pain-to-price ratio drops > 30% during an experiment
- Maximum 4 experiments per month; if all fail, pause and flag for human strategic review
- Cooldown: 7 days after a failed experiment before testing the same variable

### 2. Set up pain intelligence reporting

Run the `autonomous-optimization` drill to build the continuous monitoring layer:

**Real-time dashboard panels:**
- Weekly pain-to-price ratio trend (12-week rolling)
- Quantification rate trend with target line
- Pain category distribution over time (stacked area)
- Top 10 pains by frequency and dollar impact
- Win rate: pain-discovered deals vs cold pipeline
- Deal velocity comparison
- Active experiment status and preliminary results

**Anomaly alerts (daily):**
- Pain-to-price ratio below 8x for 2 consecutive weeks
- Quantification rate below 50%
- Business case conversion dropped 20%
- New pain category emerging (frequency > 3 in one week)
- Question effectiveness decaying (surface rate drop > 50%)

**Weekly pain intelligence brief (Monday 8am):**
The agent generates a report covering:
1. Executive summary: what happened, what changed, what to do
2. Key metric changes with explanations
3. Emerging pain patterns (new pains, shifting severity, market trends)
4. Question bank updates: what was retired, promoted, or added experimentally
5. ICP implications from pain segment analysis
6. Recommended experiments for the next optimization cycle
7. Distance from estimated local maximum

Store in Attio. Post to Slack.

### 3. Build market-level pain intelligence

Aggregate pain data across all prospects over 6 months to produce strategic intelligence:

**Pain heat map:** Track which pain categories are growing in severity across your market. If "compliance" pain spikes across segments, your product messaging and content should shift.

**Segment migration:** Detect when new segments develop quantifiable pain. If Series A companies suddenly show 15x pain-to-price ratios (up from 6x), reallocate outbound targeting.

**Competitive signals:** Track whether prospects mention competitors more or less frequently in discovery calls. A spike in competitor mentions in a specific pain category = competitive threat.

**Timing patterns:** Identify quarterly or seasonal patterns in pain urgency. If Q4 budget cycles consistently produce higher quantification rates, front-load discovery call volume in Q3.

**Content feedback loop:** Feed the most common and highest-impact pains into content marketing. If "manual data entry" is the #1 pain across 85% of calls, create a definitive guide, case study, and ROI calculator targeting that specific pain.

### 4. Maintain the question bank as a living system

The question bank evolves continuously at Durable:

**Monthly cycle:**
1. Agent reviews question performance data from `pain-pattern-analysis`
2. Questions with surface_rate < 0.1 for 3 consecutive weeks are retired
3. Experimental questions with surface_rate > 0.3 are promoted to standard
4. 2-3 new experimental questions are generated targeting detected gaps
5. The full question bank is versioned and stored in Attio

**Quarterly review:**
1. Agent generates a "Question Bank Health Report" comparing current vs. 3 months ago
2. Identifies structural shifts: are new pain categories emerging that have no questions?
3. Recommends major question bank overhauls if the market has shifted significantly

**Human action required:** Quarterly review of the Question Bank Health Report. Approve or modify the agent's recommendations for structural changes.

### 5. Detect convergence

The optimization loop runs indefinitely but detects when the play has reached its local maximum:

**Convergence criteria:**
- 3 consecutive experiments produce < 2% improvement on the primary metric (pain-to-price ratio)
- Question bank churn drops below 1 change per month
- Weekly metrics are within +/- 5% of the 4-week rolling average

**At convergence:**
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment cadence from monthly to quarterly
3. Generate a convergence report: "Pain discovery is optimized. Current performance: {metrics}. Further gains require strategic changes (new segments, new product positioning, new competitive dynamics) rather than tactical optimization."
4. Shift agent resources to other plays or to monitoring for market disruptions that break convergence

### 6. Evaluate ongoing sustainability

Monthly review against the Durable threshold:
- Is pain-to-price ratio sustained >= 10x? (Rolling 30-day average)
- Is quantification rate sustained >= 70%?
- Is business case win rate stable or improving?
- Are agent experiments producing at least 1 winner per quarter?

If metrics degrade:
- Check for market shifts (new competitor, regulatory change, economic conditions)
- Check for ICP drift (your best customers are changing)
- Check for question fatigue (prospects hearing the same questions from multiple vendors)
- Run a strategic review — the play may need a fundamental redesign, not optimization

## Time Estimate

- Autonomous optimization setup: 8 hours
- Pain intelligence reporting setup: 6 hours
- Monthly agent oversight and approvals: 4 hours/month x 6 = 24 hours
- Quarterly strategic reviews: 4 hours x 2 = 8 hours
- Discovery calls (ongoing, 15-20/month): ~15 hours/month x 6 = 90 hours
  (call time itself; prep and post-call are fully automated)
- Threshold evaluation (monthly): 1 hour x 6 = 6 hours
- **Total: ~130 hours over 6 months** (bulk is call time; agent overhead is ~4 hrs/month)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, pain data, question bank, intelligence reports | Pro $59/user/mo |
| Fireflies | Auto-transcribe all discovery calls | Business $19/user/mo |
| Claude API (Anthropic) | Pain extraction, quantification, business case, hypothesis generation, experiment evaluation | Sonnet: $3/$15 per M tokens; ~$50-100/mo at volume |
| PostHog | Analytics, anomaly detection, experiments, dashboards | Usage-based; ~$50-100/mo at this volume |
| n8n | All automation: extraction pipeline, optimization loop, reporting, alerts | Pro $60/mo or Business $800/mo |
| Cal.com | Discovery call scheduling | Free or Teams $15/user/mo |
| Clay | Enrichment for call prep + market intelligence | Growth $495/mo |

**Estimated play-specific cost at Durable:** ~$300-600/mo (Fireflies + n8n Pro + Clay Growth + Claude API at volume + PostHog usage). Agent compute (Claude API for the optimization loop) adds ~$50-100/mo.

## Drills Referenced

- `autonomous-optimization` — The core always-on loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners. Weekly optimization briefs.
- `autonomous-optimization` — Continuous dashboards, anomaly alerts, weekly intelligence briefs, market-level pain analysis, question bank health monitoring
