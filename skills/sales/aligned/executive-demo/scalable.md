---
name: executive-demo-scalable
description: >
  Executive-Focused Demo — Scalable Automation. Scale to 50+ exec demos per quarter
  with A/B testing of demo structures by persona, automated exec engagement scoring,
  and a real-time performance dashboard. Find the 10x multiplier by identifying which
  ROI narratives, demo formats, and follow-up sequences produce the highest close rates
  for each executive persona.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Scalable Automation"
time: "75 hours over 2 months"
outcome: ">=75% exec demo conversion and >=35% faster close time for exec-engaged deals over 2 months at 50+ demos/quarter volume"
kpis: ["Exec demo conversion rate", "Exec engagement score", "Deal velocity by exec engagement", "Demo quality score"]
slug: "executive-demo"
install: "npx gtm-skills add sales/aligned/executive-demo"
drills:
  - dashboard-builder
  - ab-test-orchestrator
---

# Executive-Focused Demo — Scalable Automation

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Maintain >=75% exec demo-to-nextstep conversion and achieve >=35% faster close time for exec-engaged deals at scale (50+ exec demos/quarter). Identify the top ROI narrative and demo structure per persona that predicts closed deals. Reduce exec demo prep time to <10 minutes per demo via fully automated persona-specific prep pipeline.

## Leading Indicators

- Exec demo prep docs are generated and reviewed before every scheduled demo with minimal manual intervention
- A/B tests on demo structure produce statistically significant winners by persona within 6 weeks
- Persona-level conversion analysis surfaces clear patterns (some personas convert 2-3x better with specific framings)
- Exec demo performance dashboard is checked daily and anomalies are caught within 24 hours
- Follow-up sequence completion rate >95% (no exec falls through the cracks)
- Exec engagement scoring predicts deal close probability with >70% accuracy

## Instructions

### 1. Deploy the exec demo performance monitoring system

Run the `dashboard-builder` drill to build the always-on monitoring infrastructure:

1. **Full funnel tracking by persona**: Configure PostHog to capture every stage from `exec_demo_scheduled` through `deal_closed_won` with properties for exec persona, ROI narrative type, demo duration, and sentiment score
2. **Persona effectiveness dashboard**: Build a PostHog dashboard with panels for conversion rates by persona, deal velocity comparison (exec vs non-exec), ROI narrative effectiveness by persona, demo quality scores, multi-exec alignment outcomes, and weekly volume trends
3. **Automated alerts**: n8n daily cron checks per-persona conversion rates against 4-week rolling averages. Warning at 15% below baseline. Critical at 30% below baseline. Slack alerts include which persona degraded and probable cause.
4. **ROI narrative effectiveness report**: Weekly n8n job analyzes which ROI framings (payback period vs market share vs efficiency gain) drive the highest conversion for each persona. Ranks all narrative-persona combinations and identifies top 3 winners and bottom 3 losers.

### 2. Run A/B tests on exec demo structure by persona

Run the `ab-test-orchestrator` drill to test variables that affect exec demo conversion. Segment all tests by exec persona -- a winning structure for CFOs may not work for CTOs.

**Test 1: Demo opening structure**
- Control: Open with pain recap from discovery/research, then show outcomes
- Variant: Open with a 60-second customer story from a peer company in their industry, then show outcomes
- Metric: exec-demo-to-nextstep conversion rate
- Segment by: exec persona
- Sample: 25 exec demos per variant (stratified by persona)

**Test 2: ROI narrative depth**
- Control: Two key numbers with brief framing (e.g., "saves $170K/year, 1-month payback")
- Variant: Full ROI walkthrough with conservative/moderate/optimistic scenarios
- Metric: exec-demo-to-proposal conversion rate
- Segment by: persona (hypothesis: CFOs prefer full walkthrough, CEOs prefer headline numbers)
- Sample: 25 exec demos per variant

**Test 3: Follow-up format**
- Control: Text email with 3 bullet points + Cal.com link within 2 hours
- Variant: Personalized one-page PDF executive summary with embedded ROI chart + Cal.com link within 2 hours
- Metric: nextstep-to-proposal conversion rate
- Sample: 25 exec demos per variant

**Test 4: Multi-exec coordination**
- Control: Independent exec demos (each exec gets their own demo)
- Variant: Unified exec briefing (all execs in one 30-minute session with persona-specific segments)
- Metric: days from first exec demo to proposal request
- Sample: 10 multi-exec deals per variant

Use PostHog feature flags to randomly assign each exec demo to a variant. Run each test for a minimum of 50 total demos (25 per variant) before declaring a winner at 95% confidence. Analyze results by persona -- if a variant wins for CTOs but loses for CFOs, implement persona-specific strategies.

### 3. Scale exec demo prep automation

Run the the exec demo prep workflow (see instructions below) drill with enhancements for scale:

1. **Auto-persona detection**: The agent classifies each exec into a persona from their Attio record and loads the persona template as the starting point. No manual persona assignment needed.
2. **Research freshness check**: Before generating a prep doc, the agent checks if exec research is older than 14 days. If stale, re-run `exec-research-enrichment` before proceeding.
3. **Historical learning**: The agent queries past exec demo outcomes from PostHog. When building a prep doc, it checks: "For execs with this persona and similar company profile, which ROI framing produced the best outcome?" It recommends the winning narrative.
4. **Multi-exec alignment engine**: For deals with multiple exec stakeholders (detected from Attio), the agent generates a stakeholder map showing each exec's persona, priorities, and how to address potential conflicts (e.g., CEO wants investment, CFO wants cost cutting). Proposes a demo sequence that builds internal alignment.
5. **Case study matching**: The agent queries your case study library and auto-selects the most relevant peer proof point for each exec based on their industry, company size, and persona.

### 4. Build exec engagement scoring

Create a composite engagement score for each deal based on exec interaction:

| Signal | Weight | How measured |
|--------|--------|-------------|
| Number of execs engaged | 25% | Count of unique exec_demo_completed events per deal |
| Highest persona seniority | 20% | CEO=5, CFO/CTO=4, VP=3, Director=2 |
| Average sentiment score | 20% | Mean of sentiment_score across all exec demos for this deal |
| Next-step commitment rate | 20% | Percentage of exec demos that yielded next-step commitment |
| Follow-up engagement | 15% | Did execs open/forward the follow-up materials |

Score range: 0-100. Store on the deal in Attio as `exec_engagement_score`.

Correlate exec engagement score with deal outcomes weekly. Hypothesis: deals with score >70 close at 2x+ the rate of deals with score <40. Use this score to prioritize which deals get founder attention.

### 5. Build automated exec demo quality scoring

After each exec demo, use Fireflies transcript + Claude to auto-score quality:

| Dimension | Score 1-5 | How measured |
|-----------|-----------|-------------|
| Strategic framing | Led with business outcomes, not features? | Count of strategic vs tactical statements in first 5 minutes |
| Persona alignment | Language appropriate for the exec's role? | Match between talking points and persona expectations |
| ROI delivery | Quantified ROI estimates presented? | Presence of specific numbers tied to their pains |
| Engagement | Exec asked questions and interacted? | Count of exec questions and positive signals |
| Time discipline | Demo stayed within 15-20 minutes? | Duration check against target |
| Close quality | Clear, specific next step proposed? | Presence of concrete proposal matched to persona |

Store scores on the deal in Attio. Correlate quality scores with outcomes:
- High quality + close = the demo model works
- High quality + no close = wrong ICP or missing BANT dimension (not a demo problem)
- Low quality + close = exec was already convinced (discovery was strong)
- Low quality + no close = demo execution needs improvement for this persona

### 6. Evaluate at scale

After 2 months with 50+ exec demos completed:
- Primary: >=75% exec demo-to-nextstep conversion rate
- Primary: Exec-engaged deals close >=35% faster than non-exec deals
- Secondary: At least 2 A/B tests completed with statistically significant winners
- Secondary: Exec demo prep time <10 minutes per demo
- Secondary: Exec engagement score correlates with close rate at r>0.5
- Secondary: Per-persona conversion analysis identifies clear top and bottom performers

If PASS, proceed to Durable. If FAIL, focus on the lowest-performing funnel stage:
- Scheduling-to-demo drop-off: exec availability is the bottleneck; test async exec briefing formats
- Demo-to-nextstep drop-off: demo execution or wrong ROI framing for the persona
- Nextstep-to-proposal drop-off: follow-up sequence or internal stakeholder blockers; strengthen champion enablement
- Specific persona underperformance: rewrite the persona template and ROI framing for that role

## Time Estimate

- 10 hours: setup (exec-demo-performance-monitor, A/B test framework, enhanced prep automation, engagement scoring)
- 5 hours: build quality scoring system and multi-exec alignment engine
- 40 hours: execute 50+ exec demos over 2 months (20-30 min each with reduced prep)
- 8 hours: review A/B test results and implement per-persona winners (weekly)
- 8 hours: weekly funnel review, persona effectiveness analysis, and optimization
- 4 hours: monthly strategic review of exec demo playbook
- **Total: ~75 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM -- deal records, exec research, engagement scores, persona templates | Plus $29/user/mo |
| PostHog | Analytics -- funnel tracking, A/B tests, feature flags, exec engagement dashboards | Free tier (1M events/mo); usage-based after |
| Fireflies | Transcription -- exec demo call recording + AI quality scoring | Business $19/user/mo (API access required for auto-scoring) |
| Cal.com | Scheduling -- exec demo booking with attendee detection | Free (1 user); Teams $15/user/mo |
| Clay | Enrichment -- exec research, company intelligence, competitive context | Growth $349/mo (12,000 credits for volume research) |
| n8n | Automation -- exec prep pipeline, monitoring, follow-up, reporting | Pro $60/mo cloud (10K executions); or free self-hosted |
| Anthropic API | AI -- persona classification, ROI narratives, quality scoring, case study matching | ~$3-8/exec demo (multiple Claude calls per demo at scale) |

**Estimated play-specific cost at Scalable:** ~$250-500/mo (Fireflies Business + Clay Growth + n8n Pro + Anthropic API at 50 demos/quarter)

## Drills Referenced

- `dashboard-builder` -- always-on monitoring of exec demo funnel with per-persona breakdown, deal velocity impact, and ROI narrative effectiveness reports
- `ab-test-orchestrator` -- design, run, and analyze A/B tests on exec demo structure, ROI depth, follow-up format, and multi-exec coordination
- the exec demo prep workflow (see instructions below) -- auto-generate persona-specific exec demo prep docs (enhanced with historical learning, case study matching, and multi-exec alignment)
