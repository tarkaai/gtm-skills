---
name: win-loss-analysis-scalable
description: >
  Win/Loss Analysis Program — Scalable Automation. Scale interview coverage to >=50% of all
  closed deals, build competitive intelligence from aggregated data, and measure the impact
  of insight-driven changes on win rates.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Direct, Email"
level: "Scalable Automation"
time: "75 hours over 2 months"
outcome: ">=50% interview completion rate and measurable win rate improvement from implemented insights over 2 months"
kpis: ["Interview completion rate", "Win rate trend", "Insight implementation rate", "Impact of changes on metrics"]
slug: "win-loss-analysis"
install: "npx gtm-skills add product/retain/win-loss-analysis"
drills:
  - dashboard-builder
  - threshold-engine
---
# Win/Loss Analysis Program — Scalable Automation

> **Stage:** Product → Retain | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Scale from ad-hoc interviews to a program that covers the majority of closed deals, builds a competitive intelligence database from aggregated data, and creates a measurable feedback loop between buyer insights and win rate improvement.

**Pass threshold:** >=50% interview/survey completion rate across all closed deals AND measurable win rate improvement from implemented insights over 2 months.

## Leading Indicators

- Interview coverage rate trend (should climb from Baseline's ~30% toward 50%+)
- Outreach sequence open/reply rates (optimize subject lines and timing)
- Survey completion rate for non-interview contacts (target: >=15% of those who decline calls)
- Competitive battlecard usage by sales team (are they referencing the insights?)
- Time from insight identified to change implemented (target: <2 weeks for sales/messaging changes)
- Before/after metrics on implemented changes (e.g., win rate on deals where new battle card was used)

## Instructions

### 1. Optimize interview acceptance rate

Analyze Baseline outreach data to improve conversion:

- Pull Loops sequence metrics: open rates, reply rates, booking rates for won vs lost paths
- A/B test outreach subject lines. Test: personalized ("Your feedback on evaluating {Product}") vs curiosity ("One honest question about your decision") vs direct ("20 min for a $25 gift card")
- Test incentives: offer a $25 Amazon gift card or equivalent for completed interviews. Track whether incentivized interviews produce better or worse quality insights.
- Adjust timing: test sending outreach at 3 days, 7 days, and 14 days post-close to find the optimal window
- Implement the changes that produce the highest acceptance rate

### 2. Build the competitive intelligence database

Run the `competitive-intel-aggregation` fundamental (referenced by the the win loss reporting workflow (see instructions below) drill) to build a living competitive database:

- Create the Competitors object in Attio with win/loss rates, strengths, weaknesses, and objection handling
- Process all historical win/loss insights to populate competitor records
- Generate battlecards for competitors with 5+ mentions
- Set up the weekly refresh n8n workflow that updates competitor data from new insights
- Share battlecards with the sales team via Slack and pin to relevant Attio deal views

### 3. Build the win/loss intelligence dashboard

Run the `dashboard-builder` drill to create a dedicated Win/Loss Intelligence dashboard in PostHog:

- **Panel 1:** Interview coverage rate (% of closed deals with completed interview/survey) — line chart, weekly
- **Panel 2:** Win rate trend — line chart, monthly, with annotation markers for when changes were implemented
- **Panel 3:** Top loss reasons — horizontal bar chart, rolling 90 days
- **Panel 4:** Top win reasons — horizontal bar chart, rolling 90 days
- **Panel 5:** Competitor win rates — multi-line chart, monthly, one line per competitor
- **Panel 6:** Insight-to-action velocity — average days from insight identified to change implemented

Set up alerts:
- Win rate drops >10pp month-over-month
- Interview coverage drops below 40%
- A competitor's win rate against you rises above 60%

### 4. Automate monthly reporting

Run the the win loss reporting workflow (see instructions below) drill with the automated scheduling workflow:

- Deploy the n8n cron workflow that generates monthly reports automatically
- Report includes: aggregate metrics, pattern analysis, competitive landscape update, recommended actions, and impact measurement of previously implemented changes
- Report distributed to #sales, #product, and #leadership Slack channels
- Archive each report in Attio for historical reference

### 5. Measure the impact of changes

This is the critical step that separates Scalable from Baseline. For every change implemented based on win/loss insights, track the before/after:

- **Sales process changes:** Compare win rate in the 30 days before vs 30 days after the change. Control for other variables (pipeline quality, deal size).
- **Messaging changes:** Track which deals used the updated messaging (tag in Attio). Compare win rate for deals with new messaging vs deals without.
- **Competitive battlecards:** Tag deals where the battlecard was referenced. Compare win rate against that competitor before and after battlecard deployment.
- **Product changes:** When a feature gap is closed, compare win rate for deals where that feature was a decision factor.

Log impact measurements in PostHog as events: `winloss_change_impact` with properties: change_type, before_metric, after_metric, lift_percentage.

### 6. Scale interview capacity

As deal volume grows, the founder cannot conduct every interview personally:

- Train 1-2 team members on the interview protocol from the the win loss interview pipeline workflow (see instructions below) drill
- Create a shared interview guide document that standardizes questions and probing techniques
- Use Fireflies' team features so all interviewers' recordings flow into the same analysis pipeline
- Implement a rotation: founder handles strategic/large deals, team handles standard deals
- Quality check: review 1 in 5 transcripts to ensure interview quality remains high

**Human action required:** Train interviewers and monitor quality for the first month.

### 7. Evaluate against threshold

Run the `threshold-engine` drill:
- Interview completion rate >=50% of all closed deals
- Measurable win rate improvement from at least one implemented change (statistically meaningful — not just noise)

If PASS: Proceed to Durable. The program is producing measurable business impact.
If FAIL: Diagnose. Low coverage = outreach optimization needed. No measurable impact = either changes are too small, measurement window too short, or insights are not translating to effective changes.

## Time Estimate

- 10 hours: Optimize outreach sequences (A/B tests, incentive testing, timing tests)
- 15 hours: Build competitive intelligence database and battlecards
- 8 hours: Build PostHog dashboard and configure alerts
- 5 hours: Set up automated monthly reporting
- 20 hours: Conduct interviews over 2 months (scaled with team)
- 10 hours: Measure change impact and refine the feedback loop
- 7 hours: Train team, quality checks, process refinement

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal tracking, competitive DB, insight storage | Free (up to 3 users) or Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Cal.com | Interview scheduling | Free tier or Team $12/user/mo — [cal.com](https://cal.com) |
| Fireflies | Interview transcription (multi-user) | Pro $10/mo/seat (2-3 seats) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Typeform | Survey fallback | Basic $25/mo — [typeform.com](https://www.typeform.com) |
| Loops | Automated outreach sequences | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Workflow automation (more workflows) | Pro €60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Dashboards and trend tracking | Free tier (1M events) or $0/mo to start — [posthog.com/pricing](https://posthog.com/pricing) |
| Claude API | Insight extraction + report synthesis | ~$15-30/mo — [anthropic.com](https://console.anthropic.com) |
| Interview incentives | Gift cards for interviewees | ~$25 per interview, est. $250-500/mo |

**Estimated play-specific cost:** ~$200-450/mo (tools + incentives)

## Drills Referenced

- the win loss interview pipeline workflow (see instructions below) — Optimized outreach, scheduling, and recording at scale
- the win loss insight extraction workflow (see instructions below) — Automated AI analysis of every transcript and survey
- the win loss reporting workflow (see instructions below) — Monthly automated reports with trend analysis and recommendations
- `dashboard-builder` — PostHog dashboard for real-time win/loss intelligence
- `threshold-engine` — Evaluates results against the pass threshold
