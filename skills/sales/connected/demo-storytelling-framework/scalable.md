---
name: demo-storytelling-framework-scalable
description: >
  Demo Storytelling Framework — Scalable Automation. Scale story-driven demos across all opportunities
  with Gong-based engagement analysis, A/B testing of stories and narrative structures, automated story
  refresh, and an intelligence layer that surfaces which stories drive the highest conversion. The 10x
  multiplier is turning engagement data into a feedback loop that continuously improves story selection
  and delivery.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Product"
level: "Scalable Automation"
time: "55 hours over 2 months"
outcome: ">=75% of demos use story-driven prep at scale, demo-to-proposal conversion maintains >=12% lift, and story matching accuracy >=70% (top-matched story correlates with strong engagement) over 2 months"
kpis: ["Storytelling adoption rate at scale", "Demo-to-proposal conversion lift (sustained)", "Story matching accuracy", "Engagement score trend", "Story effectiveness ranking stability"]
slug: "demo-storytelling-framework"
install: "npx gtm-skills add sales/connected/demo-storytelling-framework"
drills:
  - story-intelligence-reporting
  - demo-performance-monitor
  - ab-test-orchestrator
---

# Demo Storytelling Framework — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Product

## Outcomes

Find the 10x multiplier. At Baseline, each demo gets an auto-generated story prep doc. At Scalable, every demo is also analyzed post-delivery — Gong recordings are scored for engagement signals, story effectiveness is ranked weekly, A/B tests compare different stories and narrative structures against each other, and the story matching algorithm improves based on conversion data. The intelligence layer turns every demo into a data point that makes the next demo better.

**Pass threshold:** >=75% of demos use story-driven prep at scale, demo-to-proposal conversion maintains >=12% lift, and story matching accuracy >=70% (top-matched story correlates with strong engagement) over 2 months.

## Leading Indicators

- Gong engagement analysis runs automatically after every demo recording
- Story effectiveness rankings show clear differentiation (top stories 2x+ conversion of bottom stories)
- A/B tests on narrative structure produce statistically significant winners within 4 weeks
- Story matching scores correlate with actual engagement outcomes (high match score = high engagement)
- Story gaps are detected and filled proactively before they affect conversion

## Instructions

### 1. Deploy Story Intelligence Reporting

Run the `story-intelligence-reporting` drill:

- Build the PostHog storytelling dashboard (8 panels: story usage distribution, story-to-conversion funnel, engagement by story, story connection rate, emotional connection rate, match score vs outcome, story gap tracker, weekly volume)
- Configure the weekly story effectiveness ranking workflow in n8n
- Set up degradation alerts: story fatigue (>40% usage), conversion drop (>20% below average), engagement decline (>15% for 2+ weeks), gap expansion (>30% demos flagged)
- Enable the weekly intelligence brief (posted to Slack every Monday)

This creates the data layer. From this point forward, every demo produces intelligence that feeds back into story selection.

### 2. Integrate Gong Engagement Analysis

Connect Gong to the storytelling pipeline:

- Create an n8n workflow triggered when a demo recording is processed in Gong (webhook from Gong or poll Gong API for new recordings)
- For each recorded demo: run `gong-engagement-analysis` to extract storytelling-specific engagement signals: story connection moments, prospect questions about the customer, emotional indicators, and disengagement signals
- Store the engagement scorecard in Attio on the deal record
- Fire the `demo_engagement_scored` PostHog event with all engagement metrics and the `story_id` used

Set up a fallback: if Gong is not available for a demo (e.g., in-person meeting), use manual engagement logging from Baseline as the data source.

### 3. Launch A/B Testing

Run the `ab-test-orchestrator` drill to set up experiments on the storytelling program:

**Experiment 1 — Story Selection (weeks 1-4):**
For prospects in the same ICP segment where you have 2+ applicable stories, randomly assign Story A vs Story B. Measure: demo-to-proposal rate and engagement score. Minimum 15 demos per story before declaring a winner. This tells you which story resonates more with a given segment.

**Experiment 2 — Narrative Structure (weeks 3-6):**
- Control: Standard 4-phase story arc (problem, turning point, solution, results)
- Variant A: Lead with the result, then tell the story backward ("Let me tell you about a company that achieved {result}. Here's how they got there.")
- Variant B: Lead with the customer quote at emotional peak, then contextualize
- Measure: story connection rate and engagement score. Minimum 10 demos per variant.

**Experiment 3 — Closing Bridge (weeks 5-8):**
- Control: Open-ended question ("What would it mean for your team to achieve {result}?")
- Variant: Direct commitment question ("Based on {Customer}'s experience, should we put together a proposal for your team?")
- Measure: next-step commitment rate. Minimum 15 demos per variant.

Log all experiment assignments using PostHog feature flags. Use the `ab-test-orchestrator` to auto-promote winners and start new experiments.

### 4. Build the Story Refresh Pipeline

Create an n8n workflow that maintains story quality at scale:

**Monthly story health check:**
1. Pull story effectiveness rankings from the last 30 days
2. Flag stories where:
   - Engagement scores are declining (3+ week downward trend)
   - The customer has churned or downgraded (check Attio customer status)
   - The story's primary metric is more than 12 months old
   - The product capabilities referenced have changed significantly
3. For flagged stories:
   - If the customer is still active: schedule a refresh call, re-extract the story with updated results
   - If the customer has churned: retire the story immediately
   - If the metric is outdated: reach out for updated numbers or retire

**Automated gap detection:**
1. Pull all demos from the last 30 days where `story_gap_flagged = true`
2. Group by prospect industry and pain theme
3. For the most common gap: trigger the `case-study-creation` process targeting that segment
4. Notify the team: "Story gap detected for {segment}. Recommend creating a case study with a {industry} customer who solved {pain}."

### 5. Feed Engagement Data Back Into Matching

The story matching algorithm from Baseline uses static scoring (industry, size, pain overlap). At Scalable, feed actual outcome data back into the model:

- After 4 weeks of engagement data: calculate the actual conversion rate per story per segment
- Adjust matching weights: if Story A outperforms Story B for fintech prospects despite lower industry match score, the pain overlap dimension should receive higher weight for that segment
- Update the `story-matching-scoring` prompt with historical performance data: "Story X has a {Y}% proposal rate when used with {segment} prospects. Factor this into your scoring."

This creates the feedback loop: demo outcomes improve story matching, which improves demo outcomes.

### 6. Scale Volume

With intelligence and testing running, increase throughput:
- Ensure every demo gets a story-driven prep doc (target: 100% coverage)
- Backfill: for any deals that have demos scheduled but no story prep, run the prep workflow manually
- Track automation rate: % of demos where prep was auto-generated vs manually triggered
- Expand the story library to cover all segments with active pipeline

### 7. Evaluate Against Threshold

After 2 months, measure:
- Storytelling adoption rate: % of demos using story-driven prep at scale (target: >=75%)
- Demo-to-proposal conversion lift: compared to pre-storytelling baseline (target: >=12% sustained improvement)
- Story matching accuracy: % of demos where the AI-selected story produced strong engagement (engagement score >=60 or story connection moment logged) (target: >=70%)
- A/B test results: at least 1 experiment completed with a statistically significant winner
- Story effectiveness ranking: clear differentiation between top and bottom stories

**If all pass:** Proceed to Durable for autonomous optimization of stories, narratives, and matching.
**If adoption holds but conversion regresses:** The stories or narrative structure may be fatiguing. Check story usage distribution for over-reliance on a single story. Run experiments on new narrative approaches.
**If matching accuracy is low:** The scoring model needs recalibration. Compare AI match scores to actual engagement outcomes and adjust dimension weights.

## Time Estimate

- 10 hours: Story intelligence reporting setup (PostHog dashboard, n8n workflows, alerts)
- 6 hours: Gong engagement analysis integration
- 8 hours: A/B test design and orchestrator configuration
- 8 hours: Story refresh pipeline and gap detection automation
- 5 hours: Matching feedback loop implementation
- 8 hours: Daily monitoring and weekly intelligence review (30 min/day x 60 days)
- 5 hours: Experiment analysis, matching recalibration, and threshold evaluation
- 5 hours: Story library expansion and backfill

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal tracking, story library, experiment logging | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Analytics — dashboards, funnels, A/B testing, feature flags | Free up to 1M events, then $0.00005/event — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — intelligence workflows, refresh pipeline, alerts | $24/mo (Starter) or $60/mo (Pro for higher volume) — [n8n.io/pricing](https://n8n.io/pricing) |
| Gong | Conversation intelligence — engagement analysis | $100-150/user/mo (contact sales) — [gong.io/pricing](https://www.gong.io/pricing/) |
| Fireflies | Transcription — discovery calls, story extraction | $18/user/mo (Pro) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Anthropic API | AI — story matching, narrative generation, engagement analysis | Usage-based, ~$10-20/mo at this volume — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** ~$200-400/mo. Primary cost drivers: Gong ($100-150), n8n Pro ($60), Anthropic API (~$20).

## Drills Referenced

- `story-intelligence-reporting` — track story effectiveness, build performance dashboards, generate weekly intelligence briefs, and detect story fatigue and gaps
- `demo-performance-monitor` — monitor the full discovery-to-demo-to-deal funnel and detect conversion degradation patterns
- `ab-test-orchestrator` — run controlled experiments on story selection, narrative structure, and closing techniques
