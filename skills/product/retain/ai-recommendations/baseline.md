---
name: ai-recommendations-baseline
description: >
  AI-Powered Recommendations — Baseline Run. Automate the recommendation pipeline
  with n8n to generate and deliver AI suggestions weekly. Track adoption funnels
  in PostHog. Target >=35% adoption and >=12% feature discovery rate at 50+ users.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=35% adoption rate and >=12% net feature discovery rate sustained over 2 weeks at 50+ users"
kpis: ["Recommendation adoption rate", "Feature discovery rate", "Recommendation CTR", "Dismissal rate", "Time to adoption"]
slug: "ai-recommendations"
install: "npx gtm-skills add product/retain/ai-recommendations"
drills:
  - posthog-gtm-events
  - feature-adoption-monitor
---

# AI-Powered Recommendations — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Turn the Smoke-validated recommendation engine into an always-on automated pipeline. n8n generates AI recommendations weekly and delivers them via Intercom (in-app) and Loops (email fallback). Target: >=35% adoption rate and >=12% net feature discovery rate (percentage of users who discover and start using a feature they had never used before) sustained over 2 weeks at 50+ users.

## Leading Indicators

- Weekly pipeline runs without manual intervention for 2 consecutive weeks
- Recommendation CTR holds above 18% across in-app and email channels
- Dismissal rate stays below 35%
- Feature adoption funnel shows clear progression: shown > clicked > adopted
- At least 5 distinct features are recommended per week (no single-feature fixation)
- Email fallback channel produces measurable adoption (not just in-app)

## Instructions

### 1. Configure event tracking

Run the `posthog-gtm-events` drill to formalize the recommendation event taxonomy:

- `recommendation_generated` — AI produced a suggestion for this user; properties: `{user_id, recommendation_id, feature_name, segment, confidence_score}`
- `recommendation_delivered` — suggestion sent via Intercom or Loops; properties: `{recommendation_id, delivery_channel, delivery_timestamp}`
- `recommendation_shown` — user saw the message; properties: `{recommendation_id, view_duration_seconds}`
- `recommendation_clicked` — user clicked the CTA; properties: `{recommendation_id}`
- `recommendation_adopted` — user performed the feature's trigger event within 7 days; properties: `{recommendation_id, days_to_adopt}`
- `recommendation_dismissed` — user closed without clicking; properties: `{recommendation_id, seconds_before_dismiss}`

Build a PostHog funnel: generated > delivered > shown > clicked > adopted. Break down by delivery channel.

### 2. Automate suggestion delivery

Run the the workflow suggestion delivery workflow (see instructions below) drill to build the automated pipeline:

1. Configure an n8n workflow triggered by a weekly cron schedule.
2. The workflow pulls active users from PostHog, filters out users who received a recommendation in the last 7 days or dismissed 3+ consecutive suggestions, and batches them for AI generation.
3. For each eligible user, call the `ai-workflow-recommendation` fundamental with their behavior snapshot and the feature catalog from Smoke.
4. Route delivery: users active in the last 48 hours get Intercom in-app messages; users inactive for 3+ days get Loops transactional emails.
5. Log all `recommendation_generated` and `recommendation_delivered` events to PostHog.

Roll out to 50% of active users via PostHog feature flag (50% treatment, 50% control). This provides a clean measurement of recommendation impact on feature discovery and retention.

### 3. Monitor feature adoption

Run the `feature-adoption-monitor` drill to track whether recommendations actually change behavior:

1. Build a feature adoption dashboard in PostHog tracking: recommendation adoption rate by feature, feature discovery rate (users discovering new features for the first time), and treatment vs. control comparison.
2. Create stalled-user detection: users who clicked a recommendation but did not adopt within 3 days get a follow-up nudge with a more specific tutorial or example.
3. Set alerts for: adoption rate dropping below 25% for 3 consecutive days, or dismissal rate exceeding 50%.

### 4. Evaluate against threshold

After 2 weeks of automated operation, measure:

- **Primary**: adoption rate >=35% AND feature discovery rate >=12% across the treatment group at 50+ users.
- **Secondary**: treatment group shows higher retention and engagement than control group.

If PASS: document the automated pipeline configuration, top-performing features and framings, and channel performance split. Proceed to Scalable.
If FAIL: diagnose by channel (in-app vs email), by feature (which recommendations underperform), and by user segment (are specific cohorts ignoring recommendations). Fix the weakest link and re-run for another 2 weeks.

## Time Estimate

- 4 hours: event taxonomy setup and PostHog funnel configuration
- 4 hours: n8n workflow build and Intercom/Loops template creation
- 2 hours: feature adoption dashboard and alerting setup
- 6 hours: monitoring over 2 weeks, diagnosing issues, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags, cohorts | Free tier: 1M events/mo; Paid: usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic Claude API | Generate personalized recommendations weekly | Sonnet 4.6: $3/$15 per 1M tokens; ~$5-20/mo at 50-200 users — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Intercom | In-app recommendation delivery | Essential: $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Email fallback for inactive users | From $49/mo (up to 5k contacts) — [loops.so/pricing](https://loops.so/pricing) |

**Play-specific cost:** ~$5-20/mo (Claude API for weekly generation at 50-200 users)

## Drills Referenced

- `posthog-gtm-events` — establishes the recommendation event taxonomy and funnels for consistent tracking
- the workflow suggestion delivery workflow (see instructions below) — builds the automated n8n pipeline that generates, filters, routes, and delivers AI recommendations
- `feature-adoption-monitor` — tracks feature discovery rates, identifies stalled users, and triggers follow-up nudges
