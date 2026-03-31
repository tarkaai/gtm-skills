---
name: workflow-optimization-suggestions-scalable
description: >
  AI Workflow Recommendations — Scalable Automation. Personalize suggestions by user segment,
  A/B test suggestion formats and timing, and scale to 500+ users. Find the 10x multiplier
  through segment-specific delivery that lifts acceptance without proportional effort.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥30% acceptance rate across 500+ users with ≥15% median efficiency improvement sustained for 2 months"
kpis: ["Suggestion acceptance rate by segment", "Median workflow time reduction (%)", "Feature discovery breadth increase (%)", "Experiment win rate", "Retention rate for adopters vs. non-adopters"]
slug: "workflow-optimization-suggestions"
install: "npx gtm-skills add product/retain/workflow-optimization-suggestions"
drills:
  - workflow-suggestion-personalization
  - ab-test-orchestrator
---

# AI Workflow Recommendations — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Scale from 100 to 500+ users while improving acceptance rates through personalization. Segment users by behavior maturity and workflow pattern, tailor suggestion content and delivery per segment, and systematically A/B test every variable. The 10x multiplier is personalization: a user who receives a suggestion matched to their usage stage and workflow pattern is 2-3x more likely to adopt it.

## Leading Indicators

- Per-segment acceptance rates are tracked and show differentiation (different segments respond differently)
- At least 2 A/B tests completed with statistically significant results
- Suggestion pipeline scales to 500+ users per week without manual intervention
- Adopter retention rate is measurably higher than non-adopter retention rate (the business case builds)
- Feature discovery rate increases — users are finding and using features they had not used before

## Instructions

### 1. Build user segments for personalization

Run the `workflow-suggestion-personalization` drill to create behavior-based segments:

**Step 1 — Define maturity segments in PostHog:**
- **Beginners** (< 30 days, < 50% feature discovery): create a PostHog cohort with properties `account_age_days < 30 AND feature_discovery_pct < 0.5`
- **Intermediates** (30-90 days, 50-80% feature discovery): `account_age_days BETWEEN 30 AND 90 AND feature_discovery_pct BETWEEN 0.5 AND 0.8`
- **Advanced** (90+ days, 80%+ feature discovery): `account_age_days > 90 AND feature_discovery_pct > 0.8`

**Step 2 — Define workflow pattern segments:**
Use the path analysis data from `workflow-behavior-analysis` to classify each user:
- **Sequential workers**: 80%+ of actions follow a linear pattern (low branch factor in the transition matrix)
- **Explorers**: high branch factor, frequently switch between features
- **Specialists**: 60%+ of actions concentrated in 2-3 features

**Step 3 — Define response segments from Baseline data:**
- **Adopters**: accepted 2+ suggestions historically
- **Browsers**: viewed but adopted < 20% of suggestions
- **Dismissers**: dismissed 50%+ of suggestions received

Write these segment assignments to PostHog person properties via the weekly n8n segmentation pipeline.

### 2. Configure segment-specific suggestions

Update the n8n pipeline to generate different suggestion types per segment:

| Maturity | Pattern | Suggestion Focus |
|----------|---------|-----------------|
| Beginner | Sequential | "Did you know [feature] exists?" — adjacent feature discovery |
| Beginner | Explorer | "Pin [most-used feature] to your sidebar" — reduce navigation time |
| Beginner | Specialist | "Combine [their feature] with [complementary feature]" |
| Intermediate | Sequential | "Use [batch operation] instead of doing [action] one at a time" |
| Intermediate | Explorer | "Create a custom dashboard with your top 5 views" |
| Intermediate | Specialist | "Automate [repeated pattern] with a saved workflow" |
| Advanced | Sequential | "Set up [automation rule] to eliminate [manual step]" |
| Advanced | Explorer | "Build a keyboard shortcut macro for [frequent sequence]" |
| Advanced | Specialist | "Use the API to [integrate their workflow with external tool]" |

For each combination, customize the `ai-workflow-recommendation` prompt to focus on the appropriate suggestion type. Store prompt variants in n8n as separate workflow branches keyed on `{workflow_maturity, workflow_pattern}`.

### 3. Adjust delivery rules per segment

Update the delivery pipeline with segment-specific rules:

- **Adopters**: 2 suggestions per week, prefer in-app tooltip (they respond to just-in-time nudges)
- **Browsers**: 1 suggestion per week, use Intercom Custom Bot (interactive walkthrough > passive message)
- **Dismissers**: 1 suggestion per month, email only, highest confidence suggestions only

Create PostHog feature flags for each frequency tier:
- `suggestion-freq-high` (2/week) → Adopters
- `suggestion-freq-standard` (1/week) → Browsers + new users
- `suggestion-freq-low` (1/month) → Dismissers

### 4. Run systematic A/B tests

Run the `ab-test-orchestrator` drill to test suggestion variables. Run 1 test at a time, 2 weeks each:

**Test 1 — Copy style** (week 1-2):
- Control: quantified benefit ("saves 5 min/day")
- Variant: social proof ("used by 80% of power users")
- Metric: suggestion_clicked rate
- Sample: all Intermediate users (largest segment)

**Test 2 — Delivery timing** (week 3-4):
- Control: next session start
- Variant: triggered when user starts the targeted workflow
- Metric: suggestion_adopted rate
- Sample: all efficiency suggestions

**Test 3 — Suggestion depth** (week 5-6):
- Control: 1-line tooltip
- Variant: 3-step Intercom Custom Bot walkthrough
- Metric: suggestion_adopted rate
- Sample: all discovery suggestions

**Test 4 — Channel for inactive users** (week 7-8):
- Control: email only
- Variant: email + push notification
- Metric: suggestion_viewed rate
- Sample: users inactive 3+ days

After each test, implement the winner permanently. Document the learning: what changed, by how much, and why.

### 5. Build the retention correlation analysis

Using PostHog cohorts, compare:
- **Adopters cohort**: users who adopted 1+ suggestions in the last 60 days
- **Receivers cohort**: users who received suggestions but adopted 0
- **Control cohort**: users who never received suggestions (from the Baseline feature flag holdout)

Measure 30-day and 60-day retention for each cohort. Calculate: `retention_lift = adopter_retention - control_retention`. This is the business case for the play — if adopters retain 15%+ better, the ROI is clear.

Also track: average revenue per user for each cohort. If adopters have higher ARPU (they use more features, which correlates with higher plan tiers), that strengthens the expansion case.

### 6. Evaluate against threshold

After 2 months, measure:

**Pass threshold: ≥30% acceptance rate across 500+ users AND ≥15% median efficiency improvement sustained over 2 months**

- Acceptance rate = unique users who adopted at least 1 suggestion / unique users who received at least 1 suggestion (over the full 2-month period)
- Efficiency improvement = median of all adopters' workflow time reduction percentages
- Check that the rate is sustained: compare month 1 acceptance rate vs. month 2 — must not decline more than 5 percentage points

If PASS: Document segment performance, winning A/B test results, and retention correlation data. Proceed to Durable.

If FAIL on acceptance: Identify the worst-performing segment. Are the suggestions relevant to that segment? Is the delivery channel wrong? Consider dropping the segment temporarily and focusing resources on segments that respond.

If FAIL on efficiency: Review whether adopted suggestions actually changed behavior. Some users may click "try it" but revert to old habits. Track 30-day sustained behavior change, not just first use.

## Time Estimate

- 12 hours: build segments, configure segment-specific suggestion prompts, update n8n pipeline
- 8 hours: configure delivery rules, feature flags, and Intercom templates per segment
- 20 hours: run 4 A/B tests (5 hours each: setup, monitoring, analysis, implementation)
- 8 hours: build retention correlation analysis, dashboard panels
- 12 hours: monitoring and optimization over 2 months (1.5 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Segmentation, experiments, funnels, dashboards, feature flags | Free tier covers most usage; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic Claude API | Segment-specific suggestion generation for 500+ users weekly | ~$10-25/month at Sonnet 4.6 with prompt caching ([claude.com/pricing](https://claude.com/pricing)) |
| Intercom | In-app delivery: tooltips, posts, Custom Bots | $29-85/seat/month; Proactive Support Plus $99/month for Product Tours and Custom Bots ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email suggestion delivery | Free tier to $49/month depending on contact volume ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Pipeline orchestration with segment routing and A/B test implementation | Free self-hosted; Cloud from $24/month ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated Scalable cost: ~$130-300/month** (Intercom with Proactive Support + Loops + n8n + Claude API)

## Drills Referenced

- `workflow-suggestion-personalization` — build behavior-based segments, configure segment-specific prompts, set delivery rules per segment
- `ab-test-orchestrator` — design, run, and analyze A/B tests on suggestion copy, timing, depth, and channel
