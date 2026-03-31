---
name: competitive-objection-handling-scalable
description: >
  Competitive Objection Handling — Scalable Automation. A/B test positioning frameworks per
  competitor, automate battlecard refresh from deal outcomes and market monitoring, and build
  proactive competitive prep into every deal before the competitor is mentioned.
stage: "Sales > Aligned"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: ">=50% competitive win rate across all tracked competitors and >=90% battlecard currency score over 2 months"
kpis: ["Competitive win rate by competitor", "Battlecard currency score", "Positioning framework A/B test results", "Proactive competitive prep rate", "Competitive deal velocity"]
slug: "competitive-objection-handling"
install: "npx gtm-skills add sales/aligned/competitive-objection-handling"
drills:
  - competitive-battlecard-assembly
  - ab-test-orchestrator
  - competitive-detection-automation
---

# Competitive Objection Handling — Scalable Automation

> **Stage:** Sales > Aligned | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Find the 10x multiplier for competitive objection handling. A/B test positioning frameworks per competitor to discover the highest-win-rate approach for each one. Automate battlecard refresh so battlecards update themselves from deal outcomes and competitor market changes. Build proactive competitive prep into every deal — brief the seller on likely competitors before the first demo, not after the prospect mentions one.

Target: >= 50% competitive win rate across all tracked competitors and >= 90% battlecard currency (battlecards updated within the last 14 days for all active competitors).

## Leading Indicators

- A/B tests running on positioning frameworks per competitor with statistically significant results
- Battlecards refreshing weekly from new deal data without manual intervention
- Proactive competitive briefs delivered to seller before the demo call for >= 70% of deals
- At least 1 winning framework variant identified per tracked competitor
- Competitive deal velocity (days from competitor detection to close) trending downward
- Detection accuracy (precision + recall) above 90%

## Instructions

### 1. Launch positioning framework A/B tests

Run the `ab-test-orchestrator` drill to test which positioning frameworks work best per competitor. Set up experiments:

**Experiment 1: Framework selection per top competitor**
For your #1 competitor (highest mention count):
- Control: Current default framework for their objection type
- Variant: The second-ranked framework from historical data
- Metric: Competitive win rate for deals against this competitor
- Sample: 10 competitive interactions per variant (minimum)

**Experiment 2: Trap question approach**
- Control: Pain-aligned trap questions (surface gaps related to prospect's pains)
- Variant: Capability-aligned trap questions (surface gaps in product functionality)
- Metric: Prospect engagement after trap question (did they ask a follow-up or acknowledge the gap?)
- Sample: 15 interactions per variant

**Experiment 3: Follow-up timing**
- Control: Follow-up email within 4 hours of competitive call
- Variant: Follow-up email within 1 hour of competitive call (auto-sent with human approval via Slack)
- Metric: Follow-up open rate and deal progression
- Sample: 20 interactions per variant

**Experiment 4: Champion ammunition delivery**
- Control: Send positioning talking points to the seller only
- Variant: Send a champion-ready one-pager that the champion can forward to the buying committee
- Metric: Multi-threaded engagement (did additional stakeholders engage after the competitive objection?)
- Sample: 10 competitive deals per variant

Use PostHog feature flags to randomly assign each competitive interaction to a variant. Log the variant in PostHog event properties.

### 2. Automate battlecard refresh with market monitoring

Extend the `competitive-battlecard-assembly` drill with automated market intelligence:

**Deal-driven refresh (weekly):**
Configure an n8n workflow that runs every Monday:
1. Query Attio for all competitive deals closed in the past 7 days
2. For each competitor involved, pull the deal outcomes and objection data
3. Re-run the battlecard synthesis with all historical + new data
4. Update the Competitor record in Attio
5. If win rate against any competitor changed by > 10 percentage points, send Slack alert

**Market-driven refresh (weekly):**
Set up competitor monitoring via Clay:
1. For each tracked competitor, scrape their changelog, pricing page, and features page weekly
2. Hash content and compare to previous week
3. If changes detected, analyze with Claude: what changed, competitive impact score (1-5)
4. If competitive_impact >= 3, flag the battlecard for update
5. Auto-update the "Recent Changes" section of the battlecard
6. If competitive_impact >= 4, generate a Slack alert: "Competitor {name} made a significant change: {summary}. Battlecard updated. Review and adjust positioning."

**Battlecard currency scoring:**
Calculate weekly for each competitor:
- `currency_score` = (Days since last refresh <= 14 AND last refresh included new deal data) ? 1.0 : decay by 10% per week past due
- Track currency_score in PostHog as `battlecard_currency_updated` event
- Target: >= 0.90 average across all tracked competitors

### 3. Build proactive competitive prep

Don't wait for the prospect to mention a competitor. Predict which competitors are likely and prepare in advance:

Extend `competitive-detection-automation` with proactive prep:
1. When a new deal enters "Demo" or "Proposal" stage, run a competitive likelihood assessment:
   - Industry match: which competitors are strongest in the prospect's industry?
   - Company size match: which competitors target this segment?
   - Tech stack overlap: does the prospect use tools that integrate with a competitor?
   - Historical pattern: which competitors appeared most in similar deals?
2. Rank the top 2 most likely competitors
3. Auto-generate a "Competitive Prep Brief" delivered to the seller 24 hours before the demo:

```markdown
## Competitive Prep Brief — {Company Name}
**Most likely competitors:** {Competitor 1} (75% likelihood), {Competitor 2} (40%)

### If {Competitor 1} comes up:
- Their likely pitch: {based on battlecard}
- Your hinge criterion: {strongest differentiator relevant to this prospect's pains}
- Trap questions to ask: {2-3 questions}
- Supporting asset ready: {link to TCO comparison or case study}

### If {Competitor 2} comes up:
- Their likely pitch: {based on battlecard}
- Your hinge criterion: {strongest differentiator}
- Trap questions: {2-3 questions}
```

4. Track whether the prediction was correct (did the predicted competitor actually come up?)
5. Use prediction accuracy to refine the likelihood model over time

### 4. Scale competitive handling volume

With automated detection, response drafting, and proactive prep in place:
- Every competitive deal gets a battlecard-backed response within 2 hours
- Every demo gets a competitive prep brief 24 hours in advance
- Battlecards refresh weekly from deal data and market monitoring
- A/B tests continuously improve framework selection

The seller's manual involvement per competitive interaction drops to:
- 5 min: review competitive prep brief before demo
- 5 min: review auto-drafted positioning response after detection
- Time on the call itself (already happening)
- 2 min: log the competitive outcome

### 5. Build the competitive performance dashboard

Create a PostHog dashboard for Scalable-level competitive analytics:

- **Win rate by competitor:** Bar chart, updated weekly. Shows which competitors you beat and which beat you.
- **Framework A/B test results:** Table showing control vs variant win rates for each active experiment
- **Battlecard currency:** Gauge per competitor. Green >= 90%, yellow 70-89%, red < 70%.
- **Proactive prep accuracy:** What percentage of predicted competitors actually appeared?
- **Competitive deal velocity:** Average days from competitor detection to close, trend over time
- **Detection accuracy:** Precision and recall trend over time
- **Trap question effectiveness:** Which questions most often led to prospect acknowledging a gap?

### 6. Evaluate against threshold

After 2 months, measure:
- What is the overall competitive win rate? (Target: >= 50%)
- What is the battlecard currency score? (Target: >= 90%)
- Have A/B tests produced at least 1 winning framework variant per top competitor?
- Is proactive competitive prep reaching >= 70% of demos?
- Is competitive deal velocity trending down?

If **PASS**: Framework optimization and automated battlecard management are multiplying competitive effectiveness. Proceed to Durable for autonomous optimization.

If **FAIL**: Focus on the weakest metric:
- Low win rate against specific competitor: Deep-dive into loss reasons. Is the battlecard missing something? Run more deals through discovery to gather intel.
- Low battlecard currency: Check n8n workflow execution logs. Is the refresh pipeline running reliably?
- A/B tests inconclusive: May need more sample size. Extend experiments or focus on your highest-volume competitor.
- Low proactive prep coverage: Check the likelihood model. Are the trigger criteria (deal stage) correct?

## Time Estimate

- A/B test design and setup: 4 hours
- Battlecard automation (deal + market refresh): 6 hours
- Proactive prep system setup: 4 hours
- Competitive calls and interactions (~30 over 2 months): 15 hours
- Dashboard setup: 3 hours
- Weekly A/B test review + battlecard maintenance (8 weeks x 2 hrs): 16 hours
- Competitive prep brief review (30 deals x 10 min): 5 hours
- Threshold evaluation: 2 hours
- **Total: ~65 hours over 2 months** (bulk is call time and weekly reviews; automation handles detection + prep)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, competitor records, battlecards, automated triggers | Plus $29/user/mo; Pro $59/user/mo for advanced automation |
| Fireflies | Auto-transcribe calls for competitive detection | Business $19/user/mo (API access) |
| Claude API (Anthropic) | Competitive scan, positioning generation, battlecard synthesis, market analysis | Sonnet: $3/$15 per M tokens; ~$1-2 per competitive interaction |
| PostHog | Analytics, feature flags, experiments, dashboards | Free tier or usage-based (~$0.00005/event) |
| n8n | Workflow automation (detection, battlecard refresh, proactive prep, scheduling) | Pro $60/mo |
| Clay | Competitor enrichment + market monitoring (web scraping) | Launch $185/mo or Growth $495/mo |

**Estimated play-specific cost at Scalable:** ~$250-450/mo (Fireflies Business + n8n Pro + Clay Launch + Claude API at volume)

## Drills Referenced

- `competitive-battlecard-assembly` — Automated battlecard refresh from deal outcomes and competitor market monitoring
- `ab-test-orchestrator` — Design, run, and evaluate A/B tests on positioning frameworks per competitor
- `competitive-detection-automation` — Extended with proactive competitive prep for upcoming demos
