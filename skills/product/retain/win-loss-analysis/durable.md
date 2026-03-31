---
name: win-loss-analysis-durable
description: >
  Win/Loss Analysis Program — Durable Intelligence. Always-on AI agents that continuously
  analyze deal outcomes, maintain competitive intelligence, detect strategic shifts, and
  auto-recommend adaptations to sustain or improve win rates over 6+ months.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "140 hours over 6 months"
outcome: "Sustained or improving win rates (>=10% lift in addressable categories) over 6 months via continuous agent-driven insight generation, competitive monitoring, and strategic adaptation"
kpis: ["Win rate trend", "Agent-generated insight quality", "Competitive intelligence accuracy", "Roadmap impact on win rate"]
slug: "win-loss-analysis"
install: "npx gtm-skills add product/retain/win-loss-analysis"
drills:
  - autonomous-optimization
  - dashboard-builder
  - threshold-engine
---
# Win/Loss Analysis Program — Durable Intelligence

> **Stage:** Product → Retain | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

The win/loss analysis program runs continuously with minimal human intervention. AI agents detect strategic shifts in why you win and lose, maintain up-to-date competitive intelligence, and auto-generate recommendations when metrics change. The program is self-correcting: when win rates decline in a segment, the system identifies the cause and proposes specific countermeasures.

**Pass threshold:** Sustained or improving win rates (>=10% lift in addressable categories) over 6 months via continuous agent-driven insight generation, competitive monitoring, and strategic adaptation.

## Leading Indicators

- Interview coverage sustained at >=50% month over month (no decay)
- Time from insight to implemented change (target: <1 week for messaging/sales changes)
- Competitive battlecard freshness (all cards updated within last 30 days)
- Agent recommendation adoption rate (% of agent-suggested changes that get implemented)
- Win rate stability or improvement across all tracked segments
- Correlation between insight-driven changes and measurable win rate lift

## Instructions

### 1. Deploy the continuous monitoring agent

Build an n8n mega-workflow (or set of coordinated workflows) that runs the entire win/loss intelligence loop autonomously:

**Weekly cycle (automated):**
- Monday: Query Attio for all deals closed in the past 7 days. Verify outreach was triggered for each. Flag any gaps (missed deals that didn't get outreach).
- Tuesday: Check interview/survey completion status. Send reminder nudges to contacts who opened but didn't book.
- Wednesday: Process any new transcripts and survey responses through the insight extraction pipeline.
- Thursday: Update the competitive intelligence database with new data points. Regenerate battlecards for any competitor with significant new data.
- Friday: Run a mini-report: this week's interviews, new insights, any alerts. Post to #winloss Slack channel.

**Monthly cycle (automated):**
- Generate the full monthly win/loss report via the the win loss reporting workflow (see instructions below) drill
- Compare current month's metrics to the previous 3 months. Flag any metric that degraded >15%.
- For each degrading metric, use Claude API to generate a root cause hypothesis and 2-3 recommended countermeasures
- Post the monthly report with recommendations to leadership

### 2. Build the strategic drift detector

Create an n8n workflow that detects when the reasons you win or lose are shifting:

- Each month, compare the top 5 win reasons and top 5 loss reasons to the previous quarter's top 5
- If a new reason enters the top 5 (one that was not there before), flag it as an "emerging theme"
- If a previously top-5 reason drops off, flag it as a "resolved theme" (if it was a loss reason you addressed) or "fading strength" (if it was a win reason)
- Use Claude API to analyze the shift: "Our #1 loss reason shifted from 'pricing' to 'missing integrations' over the past quarter. What does this suggest about our market position?"
- Push the strategic drift analysis to PostHog as an event and to Slack

### 3. Automate competitive intelligence updates

Extend the competitive intel system built at Scalable with continuous monitoring:

- Weekly: Regenerate win/loss rates per competitor from the latest data
- Monthly: Use Claude API to generate an updated competitive narrative for each major competitor: "In the past 90 days, we won X and lost Y deals against {Competitor}. The trend is {improving/declining}. Buyers who chose them over us most often cited {reason}. Buyers who chose us over them most often cited {reason}."
- When a competitor's win rate against you changes by >15pp in a quarter, trigger an alert: "Competitive alert: Win rate against {Competitor} dropped from {X}% to {Y}%. Top cited reason: {reason}."
- Auto-update battlecards in Attio with fresh data and quotes

### 4. Build the product feedback pipeline

Connect win/loss insights directly to the product roadmap process:

- Create a filtered Attio view showing all `product-gap` category insights from win/loss analyses, sorted by frequency
- Each month, the agent generates a "Product Impact Report" that lists: which product gaps were cited in lost deals (with deal values), which product strengths drove wins (with deal values), and the estimated revenue impact of closing the top 3 gaps
- Push this report to the product team channel
- Track which product gaps get addressed and measure the win rate impact when they ship (same before/after methodology from Scalable)

### 5. Optimize the interview program continuously

Set up agent-driven optimization of the interview pipeline itself:

- Monthly: Review outreach sequence performance. If acceptance rates decline below 25%, the agent drafts 3 new subject line variants and updates the Loops sequences
- Quarterly: Review interview question effectiveness. Use Claude to analyze which questions consistently produce the highest-quality insights (most actionable, most quoted in reports). Recommend removing low-value questions and adding new ones based on emerging themes.
- Semi-annually: Review incentive effectiveness. Compare insight quality and depth between incentivized and non-incentivized interviews. Adjust incentive strategy.

**Human action required:** Approve interview question changes and incentive adjustments. The agent proposes; a human approves.

### 6. Build the executive intelligence brief

Create a quarterly executive brief that synthesizes 3 months of win/loss intelligence:

Using the the win loss reporting workflow (see instructions below) drill output for each month, plus the strategic drift detector output, generate:

```markdown
# Quarterly Win/Loss Intelligence Brief — {Quarter}

## Executive Summary
{3-sentence summary: win rate trend, biggest competitive shift, highest-impact action taken}

## Win Rate Performance
- Q{N} win rate: {X}% (vs Q{N-1}: {Y}%)
- Win rate by segment: {breakdown}
- Win rate by competitor: {breakdown with trends}

## Strategic Shifts
{What changed in why we win and lose}

## Competitive Landscape
{For each major competitor: position, trend, and recommended response}

## Impact of Actions Taken
| Action | Date Implemented | Before | After | Lift |
|--------|-----------------|--------|-------|------|
| {action} | {date} | {metric} | {metric} | {%} |

## Recommended Strategy Adjustments
1. {Recommendation with data backing}
2. {Recommendation with data backing}
3. {Recommendation with data backing}

## Program Health
- Interview coverage: {X}%
- Insight quality score: {X}/10
- Time to action: {X} days average
```

### 7. Set up self-healing automation

Build resilience into the system:

- If the n8n outreach workflow fails for 3 consecutive deals, pause the workflow and alert the ops team
- If Fireflies fails to join an interview (no transcript within 24 hours of scheduled time), send the contact the Typeform survey as a backup and log the Fireflies failure for investigation
- If Claude API returns errors on insight extraction, queue the transcript for retry (max 3 retries with exponential backoff)
- If interview coverage drops below 40% for 2 consecutive weeks, the agent diagnoses (outreach delivery issue? calendar booking issue? Fireflies failure?) and posts a root cause analysis to Slack

### 8. Evaluate sustainability

This level runs continuously. Evaluate quarterly:
- Is win rate sustained or improving vs 6 months ago? (>=10% lift in at least one addressable category)
- Are the insights still driving real changes? (Track implementation rate of recommendations)
- Is the program's cost justified by the revenue impact? (Calculate: deal value protected or won due to insight-driven changes)
- Is coverage sustained at >=50%? (No decay as team attention moves elsewhere)

If all four pass, the play is durable. If any degrades, diagnose and correct using the agent's own analytical outputs.

## Time Estimate

- 20 hours: Build continuous monitoring agent and weekly/monthly automation workflows
- 15 hours: Build strategic drift detector and competitive auto-updates
- 10 hours: Build product feedback pipeline and revenue impact analysis
- 10 hours: Build executive quarterly brief automation
- 5 hours: Build self-healing automation and error recovery
- 40 hours: Conduct interviews over 6 months (delegated to team, founder reviews quarterly)
- 20 hours: Review agent outputs, approve changes, refine prompts, quality checks
- 20 hours: Monthly report reviews, quarterly strategy sessions, stakeholder alignment

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal tracking, competitive DB, insight storage, reporting | Plus $29/user/mo or Pro $59/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Cal.com | Interview scheduling | Team $12/user/mo — [cal.com](https://cal.com) |
| Fireflies | Interview transcription (multi-user) | Pro $10/mo/seat (2-3 seats) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Typeform | Survey fallback + backup data collection | Plus $50/mo — [typeform.com](https://www.typeform.com) |
| Loops | Automated outreach sequences | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Workflow automation (complex workflows) | Pro €60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Dashboards, trend tracking, alerts | Free tier or Growth — [posthog.com/pricing](https://posthog.com/pricing) |
| Claude API | Insight extraction, synthesis, drift detection, reports | ~$30-60/mo — [anthropic.com](https://console.anthropic.com) |
| Interview incentives | Gift cards for interviewees | ~$25 per interview, est. $250-500/mo |

**Estimated play-specific cost:** ~$300-600/mo (tools + incentives + API usage)

## Drills Referenced

- the win loss interview pipeline workflow (see instructions below) — Self-healing interview pipeline with optimized outreach
- the win loss insight extraction workflow (see instructions below) — Automated AI analysis with quality monitoring
- the win loss reporting workflow (see instructions below) — Monthly automated reports + quarterly executive briefs
- `dashboard-builder` — PostHog dashboard with alerts and trend detection
- `threshold-engine` — Continuous evaluation against sustainability thresholds
