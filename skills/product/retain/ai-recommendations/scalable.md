---
name: ai-recommendations-scalable
description: >
  AI-Powered Recommendations — Scalable Automation. Personalize recommendations
  by behavioral segment using AI clustering. A/B test framing, timing, and channel
  per segment. Target >=35% adoption rate sustained at 500+ users.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=35% adoption rate sustained at 500+ users with segment-specific personalization"
kpis: ["Recommendation adoption rate", "Per-segment adoption rate", "Feature discovery breadth", "Recommendation diversity", "Personalization lift vs uniform"]
slug: "ai-recommendations"
install: "npx gtm-skills add product/retain/ai-recommendations"
drills:
  - ab-test-orchestrator
  - workflow-behavior-analysis
---

# AI-Powered Recommendations — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Scale the recommendation engine from 50-200 users to 500+ without proportional effort. The 10x multiplier is behavioral clustering: instead of generating individual recommendations with generic prompts, group users into behavioral archetypes and apply segment-specific recommendation strategies. Target: >=35% adoption rate sustained at 500+ users with measurable personalization lift over the uniform Baseline approach.

## Leading Indicators

- 4-8 behavioral clusters identified and stable (cluster assignments do not churn >10% week over week)
- Per-segment adoption rates diverge positively from uniform baseline (segments respond differently to tailored strategies)
- Feature discovery breadth increases: users discover 2+ new features per month vs 1 at Baseline
- Recommendation diversity stays above 50% (recommending across the full feature catalog, not fixating)
- A/B tests produce statistically significant winners within 2-3 weeks
- Pipeline processes 500+ users weekly without timeouts or failures

## Instructions

### 1. Analyze user behavior patterns

Run the `workflow-behavior-analysis` drill to map how different users actually work in your product:

1. Build the power-user benchmark: aggregate top 10% of users by feature breadth, average workflow times, and shortcut/automation adoption rate.
2. Run path analysis by segment: new users, regular users, declining users. For each, identify the 3 most common detour sequences (extra steps power users skip) and the 3 features power users rely on that this segment ignores.
3. Detect repeated manual patterns: users who perform the same 3+ step sequence 5+ times per week. These are prime automation recommendation candidates.

### 2. Build the personalization pipeline

Run the the recommendation personalization pipeline workflow (see instructions below) drill:

1. Use `behavior-cluster-computation` to segment users into 4-8 behavioral archetypes. Store cluster assignments as PostHog person properties.
2. For each cluster, define a recommendation strategy: Power Users get pro tips and integrations; Single-Feature Users get complementary features; Explorers get depth guidance; Declining Users get the feature most correlated with retention.
3. Build the n8n automation: weekly cron pulls users, groups by cluster, generates segment-specific recommendations via Claude, filters for quality (confidence >= 0.6), routes to the right delivery channel (Intercom for active users, Loops for inactive), and logs all events.
4. Create segment-specific Intercom message templates: tooltips for Power Users (expert tone), banners for Single-Feature Users (benefit-led), in-app posts for Explorers (quick-win framing), Custom Bots for Declining Users (conversational).

### 3. Run systematic A/B tests

Run the `ab-test-orchestrator` drill to optimize per-segment performance:

1. For each behavioral segment, test 2-3 recommendation strategies. Example tests:
   - Single-Feature Users: "complementary feature" vs "efficiency tip for primary feature"
   - Declining Users: "feature highlight" vs "workflow shortcut" vs "social proof (X users do this)"
2. Test delivery timing per segment: immediate in-session trigger vs next session start vs 24-hour delayed email.
3. Test message framing: quantified benefit ("saves 15 min/week") vs social proof ("80% of power users use this") vs novelty ("new: try this").
4. Use PostHog feature flags to split traffic. Run each test for 2+ weeks or 100+ users per variant per segment. Never stack experiments within a segment.

### 4. Evaluate against threshold

After 2 months of operation at 500+ users:

- **Primary**: adoption rate >=35% across the full user base, sustained for 4 consecutive weeks.
- **Personalization lift**: segment-specific strategies outperform the uniform Baseline approach by >=15% in adoption rate.
- **Breadth**: recommendation diversity stays above 50% (the engine recommends across the full feature catalog).
- **Scale**: pipeline processes the full user base weekly without manual intervention.

If PASS: document winning strategies per segment, optimal delivery timing, and best-performing framings. Freeze the winning configurations. Proceed to Durable.
If FAIL: identify which segments underperform. If 1-2 segments drag down the average, focus A/B testing there. If the pipeline cannot handle volume, optimize n8n batching and Claude API prompt caching. Re-evaluate after 2 more weeks.

## Time Estimate

- 10 hours: behavior analysis and power-user benchmark
- 15 hours: cluster computation, strategy definition, and n8n pipeline build
- 10 hours: segment-specific Intercom and Loops template creation
- 15 hours: A/B test design, setup, and monitoring over 2 months
- 10 hours: performance analysis, iteration, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, experiments, cohorts, path analysis | Free tier: 1M events/mo; Paid: usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic Claude API | Behavioral clustering + segment-specific recommendation generation | Sonnet 4.6: $3/$15 per 1M tokens; ~$20-80/mo at 500+ users (use prompt caching for 90% savings) — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Intercom | Segment-specific in-app messages, Custom Bots, tooltips | Advanced: $85/seat/mo (needed for Custom Bots) — [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Email fallback for inactive users, segment-specific templates | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |

**Play-specific cost:** ~$70-130/mo (Claude API at scale with prompt caching + Loops)

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and analyzes A/B tests on recommendation strategies, timing, and framing per segment
- `workflow-behavior-analysis` — maps user behavior patterns, builds the power-user benchmark, and identifies optimization opportunities
- the recommendation personalization pipeline workflow (see instructions below) — computes behavioral clusters, generates segment-specific recommendations, and automates delivery at scale
