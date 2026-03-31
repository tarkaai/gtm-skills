---
name: competitive-objection-handling-durable
description: >
  Competitive Objection Handling — Durable Intelligence. Always-on AI agents finding the local
  maximum of competitive win rates. Autonomous optimization loop detects metric anomalies
  across competitors, generates hypotheses for positioning and battlecard improvements, runs
  experiments, and auto-implements winners. Competitor market monitoring feeds real-time
  battlecard updates.
stage: "Sales > Aligned"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "120 hours over 6 months"
outcome: "Sustained or improving competitive win rate (>=50%) over 6 months via continuous agent-driven battlecard updates, positioning optimization, and competitive market intelligence"
kpis: ["Competitive win rate trend", "Agent experiment win rate", "Battlecard currency score", "Per-competitor positioning effectiveness", "Proactive competitive prep accuracy"]
slug: "competitive-objection-handling"
install: "npx gtm-skills add sales/aligned/competitive-objection-handling"
drills:
  - autonomous-optimization
---

# Competitive Objection Handling — Durable Intelligence

> **Stage:** Sales > Aligned | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Achieve autonomous optimization of the entire competitive objection handling system. An always-on agent loop monitors competitive win rates per competitor, detects when positioning frameworks degrade, generates hypotheses for battlecard and framework improvements, runs controlled experiments, and auto-implements winners. Competitor market monitoring detects product changes, pricing shifts, and positioning moves — triggering battlecard updates before the competitor's changes affect your deals.

Target: Sustained or improving competitive win rate (>= 50%) over 6 months. Convergence detected when successive experiments produce < 2% improvement on the primary metric.

## Leading Indicators

- Autonomous optimization loop running without human intervention
- Weekly competitive intelligence briefs generated and delivered to Slack
- At least 1 positioning experiment running at all times (until convergence)
- Battlecards updating automatically from deal outcomes and market monitoring
- Competitor product/pricing changes detected within 7 days of announcement
- Per-competitor win rate trends stable or improving over 3-month windows
- Proactive competitive prep accuracy improving as the likelihood model learns

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for competitive objection handling. This creates the always-on monitor -> diagnose -> experiment -> evaluate -> implement cycle.

**Configure the optimization targets:**

| Metric | Data Source | Anomaly Threshold |
|--------|------------|-------------------|
| Overall competitive win rate | PostHog | Drop below 45% for 2 weeks = trigger |
| Per-competitor win rate | PostHog + Attio | Any competitor's win rate drops >20% vs 4-week avg = trigger |
| Positioning framework effectiveness | PostHog | Any framework drops 25% from peak win rate = trigger |
| Battlecard currency score | Attio + PostHog | Any competitor's battlecard stale >21 days with active deals = trigger |
| Detection accuracy (recall) | PostHog | Drops below 85% for 2 weeks = trigger |
| Proactive prep accuracy | PostHog | Prediction accuracy drops below 50% = trigger |

**Configure the experiment space:**

The optimization agent can experiment on these variables (low/medium risk):
- Positioning framework selection per competitor (test alternative frameworks)
- Trap question phrasing and ordering
- Follow-up email timing and content
- Champion ammunition format (one-pager vs. talking points vs. comparison matrix)
- Battlecard emphasis (which sections to highlight in competitive prep briefs)
- Proactive prep trigger criteria (deal stage, enrichment signals)
- Detection prompt wording (to improve precision and recall)

**Human approval required for:**
- Changes to the competitive positioning strategy (e.g., switching from "ignore competitor" to "direct comparison" for a specific competitor)
- Changes affecting > 50% of active competitive deals simultaneously
- Any experiment the agent flags as "high risk"
- Publicly shared competitive materials (case studies, comparison pages)

**Guardrails:**
- Maximum 1 active experiment per competitor at a time. Never stack experiments on the same competitor.
- Minimum 8 competitive interactions per variant before evaluation
- Auto-revert if win rate against any competitor drops > 30% during an experiment
- Maximum 4 experiments per month across all competitors; if all fail, pause and flag for strategic review
- Cooldown: 7 days after a failed experiment before testing the same variable on the same competitor
- NEVER auto-generate or send competitive positioning that disparages competitors. All generated content must pass the "respectful competitor" filter.

### 2. Set up competitive intelligence reporting

Run the `autonomous-optimization` drill to build the continuous monitoring layer:

**Real-time dashboard panels:**
- Overall competitive win rate trend (12-week rolling)
- Win rate per competitor (bar chart, updated weekly)
- Positioning framework effectiveness heatmap (framework x competitor x win rate)
- Competitor frequency distribution (who's showing up most in pipeline?)
- Battlecard currency scores per competitor
- Proactive prep accuracy trend
- Time to competitive response trend
- Active experiment status

**Anomaly alerts (daily):**
- Overall competitive win rate below 45% for 2 consecutive weeks
- Any competitor's win rate drops > 20% vs baseline
- New competitor appearing in 3+ deals in one week (emerging threat)
- Framework effectiveness decaying (win rate drop > 25% from peak)
- Battlecard stale for a competitor with active deals
- Competitor product/pricing change detected with impact >= 3

**Weekly competitive intelligence brief (Monday 9 AM):**
The agent generates a report covering:
1. Executive summary: biggest competitive win/threat this week
2. Per-competitor win rate changes with explanations
3. Framework performance rankings (which approach is winning per competitor?)
4. New competitors detected and initial assessment
5. Competitor market changes detected (product launches, pricing shifts, new messaging)
6. Battlecard health: which need refresh, which are current
7. Proactive prep performance: prediction accuracy, coverage rate
8. Active experiments: status, preliminary results
9. Recommended experiments for the next optimization cycle
10. Distance from estimated local maximum

Store in Attio. Post to Slack.

### 3. Build competitive market intelligence

Aggregate competitive data across all deals over 6 months to produce strategic intelligence:

**Competitor threat assessment:** Track which competitors are growing vs shrinking in your pipeline. If Competitor A appears in 40% of deals (up from 20%), your competitive strategy needs to prioritize them.

**Win pattern evolution:** Detect when your winning approaches change. If `pain_alignment` framework used to win 70% against Competitor A but now wins only 45%, something changed — their product improved, their messaging shifted, or your pain story weakened.

**Market positioning shifts:** Track whether competitors are repositioning. If their messaging shifts from "features" to "outcomes" language, they're becoming harder to differentiate on value. If they start undercutting on price, your TCO comparison needs updating.

**Competitive cycle timing:** Identify patterns in when competitive deals spike. If Q4 contract renewals produce more competitive switches, front-load competitive prep in Q3.

**Content feedback loop:** Feed the most effective competitive positioning into content marketing. If the TCO comparison closes 65% of competitive deals against Competitor B, publish a public TCO guide (without naming them) that prospects find during research.

### 4. Maintain battlecards as a living system

At Durable, battlecards evolve continuously:

**Weekly cycle:**
1. Agent reviews all competitive deal outcomes from the past week
2. Battlecards updated with new win/loss patterns and buyer quotes
3. Trap questions refined based on which ones actually surfaced gaps
4. Framework effectiveness rankings updated per competitor
5. Competitor market changes integrated (product launches, pricing changes)

**Monthly cycle:**
1. Agent generates a "Competitive Landscape Report" comparing current vs 3 months ago
2. Identifies structural shifts: are new competitors emerging? Are existing competitors strengthening on previously weak dimensions?
3. Recommends battlecard overhauls for competitors with > 20% win rate change
4. Flags competitors that have become irrelevant (< 2 mentions in 3 months) for archiving

**Human action required:** Monthly review of the Competitive Landscape Report. Approve or modify the agent's recommendations for strategic positioning changes.

### 5. Detect convergence

The optimization loop runs indefinitely but detects when competitive positioning has reached its local maximum:

**Convergence criteria:**
- 3 consecutive experiments produce < 2% improvement on competitive win rate
- Per-competitor battlecard churn drops below 1 substantive change per month
- Weekly competitive metrics within +/- 5% of the 4-week rolling average

**At convergence:**
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment cadence from monthly to quarterly
3. Generate a convergence report: "Competitive positioning is optimized. Current win rate: {rate}% overall. Per-competitor: {breakdown}. Further gains require strategic changes (product differentiation, new market positioning, or competitive features) rather than tactical framework optimization."
4. Maintain market monitoring at full frequency — competitor changes can break convergence at any time
5. Shift optimization agent resources to other plays or to monitoring for competitive disruptions

### 6. Evaluate ongoing sustainability

Monthly review against the Durable threshold:
- Is overall competitive win rate sustained >= 50%? (Rolling 30-day average)
- Is per-competitor win rate stable (no competitor below 35%)?
- Are battlecards current (currency score >= 90%)?
- Is the agent producing at least 1 winning experiment per quarter?
- Is detection accuracy (recall) maintained >= 90%?

If metrics degrade:
- Check for competitor product launches or pricing changes that weren't detected
- Check for new competitors entering the market
- Check for internal changes (new sales team members who need competitive training)
- Check for market shifts (prospect priorities changing, making old battlecards irrelevant)
- Run a strategic review — may need new battlecard research from scratch rather than incremental updates

## Time Estimate

- Autonomous optimization setup: 6 hours
- Competitive intelligence monitoring setup: 6 hours
- Monthly agent oversight and approvals: 3 hours/month x 6 = 18 hours
- Quarterly strategic reviews (Competitive Landscape Report): 3 hours x 2 = 6 hours
- Competitive calls and interactions (ongoing, ~10-15/month): ~10 hours/month x 6 = 60 hours
  (call time itself; detection, prep, and post-call analysis are fully automated)
- Battlecard reviews (monthly check of auto-generated updates): 2 hours/month x 6 = 12 hours
- Threshold evaluation (monthly): 1 hour x 6 = 6 hours
- **Total: ~120 hours over 6 months** (bulk is call time; agent overhead is ~4-5 hrs/month)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, competitor records, battlecards, intelligence reports | Pro $59/user/mo |
| Fireflies | Auto-transcribe all sales calls for competitive detection | Business $19/user/mo |
| Claude API (Anthropic) | Competitive scan, positioning generation, battlecard synthesis, hypothesis generation, experiment evaluation, market analysis | Sonnet: $3/$15 per M tokens; ~$50-100/mo at volume |
| PostHog | Analytics, anomaly detection, experiments, dashboards | Usage-based; ~$50-100/mo at this volume |
| n8n | All automation: detection pipeline, battlecard refresh, optimization loop, market monitoring, reporting | Pro $60/mo or Business $800/mo |
| Clay | Competitor enrichment + market monitoring (web scraping, changelog tracking) | Growth $495/mo |

**Estimated play-specific cost at Durable:** ~$350-650/mo (Fireflies Business + n8n Pro + Clay Growth + Claude API at volume + PostHog usage). Agent compute (Claude API for the optimization loop + market monitoring) adds ~$50-100/mo.

## Drills Referenced

- `autonomous-optimization` — The core always-on loop: monitor competitive metrics, detect anomalies, generate hypotheses, run experiments on positioning frameworks and battlecard content, evaluate results, auto-implement winners. Weekly optimization briefs.
- `autonomous-optimization` — Continuous dashboards, anomaly alerts, competitor market monitoring, weekly competitive intelligence briefs, per-competitor win rate tracking, battlecard health monitoring. Feeds domain-specific metrics and hypotheses into the optimization loop.
