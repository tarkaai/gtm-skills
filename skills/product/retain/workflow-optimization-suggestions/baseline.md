---
name: workflow-optimization-suggestions-baseline
description: >
  AI Workflow Recommendations — Baseline Run. First always-on automation: n8n pipeline generates and
  delivers behavior-based workflow suggestions weekly to all active users. Validates that acceptance
  rates hold at scale with consistent efficiency improvements.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥25% suggestion acceptance rate AND ≥10% median efficiency improvement across 100+ users over 2 weeks"
kpis: ["Suggestion acceptance rate", "Median workflow time reduction (%)", "Feature discovery rate increase (%)", "Suggestion fatigue rate (dismissals/delivered)"]
slug: "workflow-optimization-suggestions"
install: "npx gtm-skills add product/retain/workflow-optimization-suggestions"
drills:
  - posthog-gtm-events
  - workflow-suggestion-delivery
---

# AI Workflow Recommendations — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

First always-on suggestion pipeline. An n8n workflow runs weekly, analyzes behavior for all active users, generates AI-powered suggestions, and delivers them via Intercom and Loops. Acceptance rate holds at ≥25% across 100+ users and delivered suggestions produce a measurable ≥10% efficiency improvement (faster workflow completion times).

## Leading Indicators

- Suggestion pipeline runs without errors for 2 consecutive weeks
- View rate ≥60% for in-app suggestions, ≥20% for email suggestions
- At least 3 distinct suggestion categories are generated (not all the same type)
- Dismissal rate stays below 30% (no fatigue signal)
- Users who adopt suggestions show faster workflow times within 7 days

## Instructions

### 1. Establish the GTM event taxonomy

Run the `posthog-gtm-events` drill to standardize the event structure for the suggestion system. Define and implement these play-specific events:

```
suggestion_generated    → {user_id, suggestion_id, category, confidence, source_data_age_days}
suggestion_delivered    → {user_id, suggestion_id, category, channel, delivery_trigger}
suggestion_viewed       → {user_id, suggestion_id, view_duration_seconds}
suggestion_clicked      → {user_id, suggestion_id, cta_type}
suggestion_adopted      → {user_id, suggestion_id, adopted_within_days, efficiency_change_pct}
suggestion_dismissed    → {user_id, suggestion_id, dismiss_reason}
```

Build a PostHog funnel: `suggestion_generated → suggestion_delivered → suggestion_viewed → suggestion_clicked → suggestion_adopted`. This is the core measurement for the entire play.

Create a PostHog dashboard with:
- Suggestion funnel conversion rates (updated daily)
- Acceptance rate trend (weekly line chart)
- Top suggestions by adoption rate (table)
- Dismissal rate trend (weekly line chart — watch for upward movement)

### 2. Build the always-on suggestion pipeline

Run the `workflow-suggestion-delivery` drill in full to create the automated pipeline in n8n:

1. **Weekly trigger**: n8n cron fires every Monday at 2 AM
2. **User selection**: Query PostHog for all users active in the last 14 days, excluding:
   - Users who received a suggestion in the last 7 days
   - Users in the first 7 days of their account (still onboarding)
   - Users who dismissed 3+ consecutive suggestions
3. **Behavior analysis**: For each eligible user, call the PostHog API for their last 50 events, feature usage counts, and workflow completion times. Compare against the power user benchmark established at Smoke level.
4. **Suggestion generation**: Call the Claude API via `ai-workflow-recommendation` for each user batch (batch users with similar profiles to save API calls using prompt caching). Generate 1-3 suggestions per user.
5. **Quality filter**: Discard suggestions with confidence = "low". Keep only "medium" and "high" confidence suggestions.
6. **Delivery routing**: For each user:
   - Active in last 24 hours → Intercom in-app message
   - Not active in 3+ days → Loops transactional email
7. **Logging**: Fire `suggestion_generated` and `suggestion_delivered` events to PostHog for every suggestion

### 3. Configure the Intercom and Loops delivery

Using the templates from the `workflow-suggestion-delivery` drill:

**Intercom in-app messages** (for active users):
- Tooltip for efficiency suggestions: trigger when user starts the targeted workflow
- Post for discovery suggestions: show on next session start
- Set frequency cap: 1 suggestion per user per week via PostHog feature flag

**Loops transactional email** (for inactive users):
- Template: personalized subject "A faster way to [workflow]"
- Content: suggestion with quantified benefit + deep link to the feature
- Send only 1 email per user per week

### 4. Monitor pipeline health

For the first 2 weeks, check daily:

- Did the n8n pipeline run without errors?
- How many users received suggestions? (target: 100+ over 2 weeks)
- What is the suggestion category distribution? (should be a mix, not all one type)
- Are there any Intercom delivery failures or Loops bounces?

Fix any pipeline issues within 24 hours. A stalled pipeline produces zero value.

### 5. Measure efficiency impact

For each user who adopts a suggestion, calculate efficiency change:

1. Query their workflow completion times for the 14 days before the suggestion
2. Query their workflow completion times for the 7 days after adoption
3. Calculate: `efficiency_change_pct = (before_median - after_median) / before_median * 100`
4. Fire `suggestion_adopted` event with `{efficiency_change_pct}` as a property
5. Aggregate across all adopters: median efficiency improvement

### 6. Evaluate against threshold

After 2 weeks of the pipeline running, measure:

**Pass threshold: ≥25% acceptance rate AND ≥10% median efficiency improvement**

- Acceptance rate = users who adopted at least 1 suggestion / users who received at least 1 suggestion
- Efficiency improvement = median of all adopters' `efficiency_change_pct` values

If PASS: Document the pipeline configuration, top-performing suggestions, and efficiency benchmarks. Proceed to Scalable.

If FAIL on acceptance rate: Review the suggestion quality. Are suggestions specific enough? Are they timed well? Pull session recordings of users who dismissed suggestions to understand why.

If FAIL on efficiency: The suggestions may be cosmetic rather than impactful. Focus on suggestions that target the largest time gaps between regular users and power users.

## Time Estimate

- 4 hours: set up GTM events, build PostHog dashboard and funnels
- 6 hours: build n8n pipeline, configure Intercom templates, configure Loops template
- 2 hours: test pipeline end-to-end with 5 test users before full launch
- 4 hours: monitor and evaluate over 2 weeks (30 min/day)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Behavior tracking, funnels, cohorts, dashboards | Free tier: 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic Claude API | Generate suggestions for 100+ users weekly | ~$2-5/month at Sonnet 4.6 ([claude.com/pricing](https://claude.com/pricing)) |
| Intercom | In-app suggestion delivery | From $29/seat/month; Proactive Support Plus $99/month for advanced messaging ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email suggestion delivery for inactive users | Free tier: 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Pipeline orchestration (weekly cron, API calls, routing) | Free self-hosted; Cloud from $24/month ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated Baseline cost: ~$30-130/month** (Intercom seat + Loops free tier + n8n cloud + Claude API)

## Drills Referenced

- `posthog-gtm-events` — establish the event taxonomy and build the measurement foundation for suggestion tracking
- `workflow-suggestion-delivery` — build the n8n pipeline, configure Intercom and Loops templates, implement delivery routing and fatigue rules
