---
name: discovery-based-demo-scalable
description: >
  Discovery-Based Demo — Scalable Automation. Scale to 50+ demos per quarter with
  A/B testing of demo structures, automated pain-to-feature effectiveness analysis,
  and a real-time demo performance dashboard. Find the 10x multiplier by identifying
  which demo formats and pain narratives produce the highest close rates.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Scalable Automation"
time: "75 hours over 2 months"
outcome: ">=70% demo-to-nextstep and >=45% demo-to-proposal conversion over 2 months at 50+ demos/quarter volume"
kpis: ["Demo-to-nextstep conversion", "Demo-to-proposal conversion", "Demo personalization score", "Pain-feature effectiveness rate"]
slug: "discovery-based-demo"
install: "npx gtm-skills add sales/aligned/discovery-based-demo"
drills:
  - demo-performance-monitor
  - ab-test-orchestrator
  - demo-prep-automation
---

# Discovery-Based Demo — Scalable Automation

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Outcomes

Maintain >=70% demo-to-nextstep conversion and achieve >=45% demo-to-proposal conversion at scale (50+ demos/quarter). Identify the top 3 pain-to-feature combinations that predict closed deals. Reduce founder demo prep time to <10 minutes per demo via automated prep pipeline.

## Leading Indicators

- Demo prep docs are generated and ready before every scheduled demo with zero manual intervention
- A/B tests on demo structure produce statistically significant winners within 4 weeks
- Pain-feature effectiveness report surfaces clear patterns (some combos convert 2-3x better)
- Demo performance dashboard is checked daily and anomalies are caught within 24 hours
- Follow-up sequence completion rate >90% (no prospect falls through the cracks)

## Instructions

### 1. Deploy the demo performance monitoring system

Run the `demo-performance-monitor` drill to build the always-on monitoring infrastructure:

1. **Full funnel tracking**: Configure PostHog to capture every stage from `discovery_call_completed` through `deal_closed_won` with properties for BANT scores, pains addressed, features shown, and demo duration
2. **Effectiveness dashboard**: Build a PostHog dashboard with panels for funnel conversion rates, pain coverage vs outcome correlation, BANT score vs demo success, recap video engagement, time-to-demo histogram, and weekly demo volume
3. **Automated alerts**: n8n daily cron checks conversion rates against 4-week rolling average. Warning at 15% below baseline. Critical at 30% below baseline. Slack alerts with specific degradation data.
4. **Pain-feature effectiveness report**: Weekly n8n job analyzes which pain-to-feature mappings drive the highest demo-to-nextstep and demo-to-closed-won rates. Ranks all combinations and identifies top 3 winners and bottom 3 losers.

### 2. Run A/B tests on demo structure

Run the `ab-test-orchestrator` drill to test variables that affect demo conversion:

**Test 1: Demo opening structure**
- Control: Start with pain recap from discovery, then show features
- Variant: Start with a 60-second customer story matching the prospect's pain, then show features
- Metric: demo-to-nextstep conversion rate
- Sample: 25 demos per variant

**Test 2: Pain coverage depth**
- Control: Cover 3 pains in 30 minutes (8 min each)
- Variant: Cover 1 pain deeply in 30 minutes (full workflow end-to-end)
- Metric: demo-to-proposal conversion rate
- Sample: 25 demos per variant

**Test 3: Follow-up format**
- Control: Loom recap video + email within 2 hours
- Variant: Personalized one-page PDF summary + email within 2 hours (no video)
- Metric: next-step-to-proposal conversion rate
- Sample: 25 demos per variant

**Test 4: Demo timing**
- Control: Schedule demo within 2-3 days of discovery
- Variant: Schedule demo within 24 hours of discovery
- Metric: demo-to-nextstep conversion rate
- Sample: 25 demos per variant

Use PostHog feature flags to randomly assign prospects to variants. Run each test for a minimum of 50 total demos (25 per variant) before declaring a winner at 95% confidence.

### 3. Scale demo prep automation

Run the `demo-prep-automation` drill with enhancements for scale:

1. **Persona detection**: The agent auto-classifies each prospect into a persona (from Baseline templates) based on discovery transcript. Loads the persona template as the starting point, then personalizes with specific pains.
2. **Feature catalog sync**: Maintain a living feature catalog in Attio. When product ships new features, update the catalog. The agent automatically includes new features in pain-to-feature mapping when relevant.
3. **Historical learning**: The agent queries past demo outcomes from PostHog. When building a prep doc, it checks: "For prospects with similar pains and BANT profile, which demo structure produced the best outcome?" It recommends the winning structure.
4. **Stakeholder prep**: For demos with multiple attendees (detected from Cal.com booking), the agent generates role-specific talking points. The CTO cares about architecture; the VP Sales cares about ROI.

### 4. Build automated demo quality scoring

After each demo, use Fireflies transcript + Claude to auto-score demo quality:

| Dimension | Score 1-5 | How it is measured |
|-----------|-----------|-------------------|
| Pain coverage | Did the rep address all pains from discovery? | Count of discovery pains mentioned in demo transcript |
| Feature relevance | Were shown features connected to stated pains? | Count of explicit pain-to-feature connections |
| Engagement | Did the prospect ask questions and interact? | Count of prospect questions and positive signals |
| ROI delivery | Were quantified ROI estimates shared? | Count of specific numbers/estimates mentioned |
| Close attempt | Did the rep propose a clear next step? | Presence of proposal for next action |

Store scores on the deal in Attio. Correlate demo quality scores with deal outcomes over time. Low-quality demos that still close = the prospect was already convinced (discovery was strong). High-quality demos that do not close = wrong ICP or missing BANT dimension.

### 5. Evaluate at scale

After 2 months with 50+ demos completed:
- Primary: >=70% demo-to-nextstep conversion rate
- Primary: >=45% demo-to-proposal conversion rate
- Secondary: At least 2 A/B tests completed with statistically significant winners
- Secondary: Demo prep time <10 minutes per demo (agent does 90% of work)
- Secondary: Pain-feature effectiveness report identifies clear top 3 and bottom 3 combos

If PASS, proceed to Durable. If FAIL, focus on the lowest-performing funnel stage:
- Discovery-to-demo drop-off: scheduling friction or discovery quality issue
- Demo-to-nextstep drop-off: demo execution or wrong features being shown
- Nextstep-to-proposal drop-off: follow-up sequence or stakeholder blockers

## Time Estimate

- 10 hours: setup (demo-performance-monitor, A/B test framework, enhanced prep automation)
- 5 hours: build demo quality scoring system
- 40 hours: execute 50+ demos over 2 months (30-45 min each, reduced prep)
- 8 hours: review A/B test results and implement winners (weekly)
- 8 hours: weekly funnel review, pain-feature analysis, and optimization
- 4 hours: monthly strategic review of demo playbook
- **Total: ~75 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM -- deal records, demo prep, quality scores, pipeline | Plus $29/user/mo |
| PostHog | Analytics -- funnel tracking, A/B tests, feature flags, dashboards | Free tier (1M events/mo); usage-based after |
| Fireflies | Transcription -- discovery and demo call recording + AI analysis | Business $19/user/mo (API access required for auto-scoring) |
| Cal.com | Scheduling -- demo booking with attendee detection | Free (1 user); Teams $15/user/mo |
| Loom | Video -- recap videos with engagement tracking | Business $12.50/user/mo |
| n8n | Automation -- demo prep pipeline, monitoring, follow-up, reporting | Pro $60/mo cloud (10K executions); or free self-hosted |
| Anthropic API | AI -- BANT extraction, pain mapping, prep docs, quality scoring | ~$2-5/demo (multiple Claude calls per demo) |

**Estimated play-specific cost at Scalable:** ~$150-300/mo (Fireflies Business + Loom Business + n8n Pro + Anthropic API at 50 demos/quarter)

## Drills Referenced

- `demo-performance-monitor` -- always-on monitoring of the discovery-to-demo-to-deal funnel with alerts and effectiveness reports
- `ab-test-orchestrator` -- design, run, and analyze A/B tests on demo structure, timing, and follow-up format
- `demo-prep-automation` -- auto-generate personalized demo prep docs (enhanced with persona detection and historical learning)
