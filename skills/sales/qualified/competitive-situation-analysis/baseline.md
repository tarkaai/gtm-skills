---
name: competitive-situation-analysis-baseline
description: >
  Competitive Situation Assessment — Baseline Run. Always-on competitive discovery pipeline
  that extracts intelligence from every qualification call, builds per-competitor battlecards,
  and delivers tailored positioning responses to deal owners in real time.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "15 hours over 2 weeks"
outcome: "Competitive situation assessed on ≥80% of qualified opportunities over 2 weeks with battlecards built for top 5 competitors"
kpis: ["Competitive discovery rate", "Win rate by competitor", "Battlecard coverage (competitors with 3+ mentions)", "Positioning delivery speed (time from call to battlecard in rep's hands)"]
slug: "competitive-situation-analysis"
install: "npx gtm-skills add sales/qualified/competitive-situation-analysis"
drills:
  - competitive-discovery-call
  - competitive-battlecard-assembly
  - posthog-gtm-events
  - threshold-engine
---

# Competitive Situation Assessment — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Competitive discovery runs automatically on every qualification call. Top 5 competitors have data-backed battlecards built from real deal data. When a competitor is identified in a deal, the deal owner receives a tailored positioning response within 1 hour. Competitive situation is assessed on at least 80% of all qualified opportunities over a 2-week period.

## Leading Indicators

- Fireflies-to-extraction pipeline running without manual intervention
- Competitor mention frequency stabilizing (same competitors appearing across deals, not random noise)
- Battlecards contain actual buyer quotes, not generic positioning
- Deal owners acknowledging battlecard deliveries (Slack reaction or similar)
- Win rate data starting to differentiate by competitor (enough deals to calculate)

## Instructions

### 1. Automate the competitive discovery pipeline

Build an n8n workflow that triggers the `competitive-discovery-call` drill automatically:

1. **Trigger:** Fireflies webhook fires when a new transcript is available
2. **Filter:** Check if the meeting is associated with a deal in Attio's Qualified pipeline stage. Skip internal meetings, customer success calls, etc.
3. **Extract:** Run `call-transcript-competitor-extraction` on the transcript
4. **Store:** Update the Attio deal record with competitive situation data
5. **Route:** If a known competitor is identified, retrieve their battlecard and generate positioning via `competitive-positioning-generation`. Deliver to deal owner via Slack DM.
6. **Log:** Fire PostHog events for every extraction

Test the workflow on 5 calls manually before enabling the automation trigger.

### 2. Build battlecards for top competitors

Run the `competitive-battlecard-assembly` drill for each competitor that appears in 3+ deals from the Smoke test data:

1. **Initialize the Competitors object** in Attio (if not already created in Smoke)
2. **Aggregate deal data** per competitor — wins, losses, objections, buyer quotes, decision criteria
3. **Synthesize battlecards** using Claude — their strengths, their weaknesses, our differentiators, common objections with best responses, trap questions, pricing intel
4. **Enrich with public intelligence** using Clay — company data, pricing page scrape, G2 ratings, recent product changes
5. **Store as structured Competitor records** in Attio with the full battlecard

Target: battlecards for the top 5 competitors by mention frequency. Each battlecard must include at least 3 buyer quotes (from actual deal transcripts, not invented).

### 3. Configure competitive event tracking for Baseline metrics

Extend the PostHog event taxonomy (from Smoke) with Baseline-specific events:

- `battlecard_built` — fired when a new competitor battlecard is created, with `competitor_name`, `deal_count`, `win_rate`
- `battlecard_delivered` — fired when a positioning response is sent to a deal owner, with `deal_id`, `competitor_name`, `delivery_method`
- `competitive_positioning_generated` — fired when Claude generates a positioning response, with `competitor_name`, `positioning_framework`, `deal_value`

Create a PostHog funnel: `competitive_situation_extracted` → `battlecard_delivered` → `deal_won` to measure the competitive intelligence pipeline's impact on win rates.

### 4. Run for 2 weeks and measure

Let the automated pipeline run for 2 full weeks. During this period:

- Monitor the n8n workflow execution log daily for failures
- Spot-check 3 extractions per week against raw transcripts for accuracy
- Track delivery speed: how long between call ending and battlecard reaching the deal owner?
- Note any competitors appearing that lack battlecards — queue them for assembly

**Human action required:** Continue asking competitive discovery questions on calls. The extraction quality depends on prospects disclosing competitive information. Coach the team (or yourself) on the 5 questions from the Smoke test.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate:

- **Primary threshold:** Competitive situation assessed on ≥80% of qualified opportunities over 2 weeks
- **Secondary thresholds:**
  - Battlecards built for all competitors with 3+ deal mentions
  - Positioning delivery within 1 hour of call for known competitors
  - Extraction accuracy ≥85% on spot-checks

If PASS: the competitive intelligence pipeline is running consistently and producing actionable output. Proceed to Scalable.

If FAIL: diagnose:
- Discovery rate < 80%: Either the Fireflies webhook is missing calls (check trigger filter) or transcripts lack competitive content (improve discovery questions)
- Battlecard quality low: Not enough deals per competitor yet. Wait for more data or enrich more aggressively with Clay.
- Delivery speed slow: n8n workflow bottleneck. Check for queue delays or API rate limits.

## Time Estimate

- 3 hours: Build and test the n8n automation workflow
- 5 hours: Build battlecards for top 5 competitors (1 hour each)
- 2 hours: Configure Baseline events and PostHog funnels
- 4 hours: Monitor, spot-check, and iterate over 2 weeks
- 1 hour: Threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Call transcription (always-on) | Pro $10/user/mo annual — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Anthropic Claude API | Extraction + positioning generation | ~$0.05-0.10/call + ~$0.10/positioning response — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Attio | CRM: deals + Competitors object + notes | Included in standard stack — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Event tracking + funnels | Free tier (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Clay | Competitor enrichment for battlecards | Launch $185/mo (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| n8n | Workflow automation | Self-hosted free or Cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost:** ~$50-200/mo (Clay enrichment for battlecard building is the main cost; Fireflies Pro and Claude API are incremental)

## Drills Referenced

- `competitive-discovery-call` — automated competitive extraction from every qualification call
- `competitive-battlecard-assembly` — builds and maintains per-competitor battlecards from deal data
- `posthog-gtm-events` — event taxonomy for competitive tracking
- `threshold-engine` — evaluates pass/fail threshold
