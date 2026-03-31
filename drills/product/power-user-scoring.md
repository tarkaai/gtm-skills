---
name: power-user-scoring
description: Build a composite power-user score from product usage data to identify top users most likely to become advocates
category: Product
tools:
  - PostHog
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-funnels
  - attio-lists
  - attio-custom-attributes
---

# Power User Scoring

This drill builds a scoring model that identifies your top users — the ones whose behavior signals deep product investment and advocacy potential. The output is a ranked list of power users in your CRM with composite scores, ready to recruit into an advocacy program.

## Prerequisites

- PostHog tracking core product events for at least 30 days
- Attio configured with contact and company records
- Clear understanding of which product actions correlate with retention and expansion

## Steps

### 1. Define the scoring dimensions

Query PostHog to identify the behaviors that differentiate your most valuable users. Build the composite score from these dimensions, each weighted 0-100:

**Usage depth (weight: 30%)**
Using `posthog-cohorts`, compare users in the top decile of session frequency and feature breadth against the median. Measure:
- Distinct features used in last 30 days
- Advanced feature usage (API, integrations, automations, admin functions)
- Sessions per week (trailing 4 weeks)
- Average session duration

Score formula: `(distinct_features / max_features) * 0.4 + (advanced_feature_count / max_advanced) * 0.3 + (sessions_per_week / 7) * 0.2 + min(avg_session_minutes / 30, 1) * 0.1`

**Tenure and consistency (weight: 20%)**
Using `posthog-custom-events`, calculate:
- Account age in days
- Weekly active weeks out of total weeks (consistency ratio)
- Streak: consecutive weeks with at least 3 sessions

Score formula: `min(account_age_days / 180, 1) * 0.3 + consistency_ratio * 0.5 + min(current_streak_weeks / 12, 1) * 0.2`

**Collaboration signal (weight: 20%)**
Measure team and social behaviors:
- Team members invited
- Shared assets created (shared dashboards, templates, reports)
- Comments or collaboration actions taken

Score formula: `min(teammates_invited / 5, 1) * 0.4 + min(shared_assets / 10, 1) * 0.3 + min(collab_actions_30d / 20, 1) * 0.3`

**Expansion signal (weight: 15%)**
Measure growth trajectory:
- Usage volume month-over-month growth rate
- Feature tier (free, starter, pro, enterprise)
- Approaching plan limits (boolean: at 80%+ of any limit)

Score formula: `min(mom_growth_rate / 0.5, 1) * 0.4 + tier_score * 0.3 + (approaching_limit ? 1 : 0) * 0.3`

**Sentiment signal (weight: 15%)**
Incorporate explicit feedback:
- NPS score (if available, normalize 0-10 to 0-1)
- Support ticket sentiment (positive interactions / total interactions)
- Feature request submissions (signals investment in the product roadmap)

Score formula: `nps_normalized * 0.5 + support_sentiment_ratio * 0.3 + min(feature_requests / 3, 1) * 0.2`

**Composite score**: `depth * 0.30 + tenure * 0.20 + collaboration * 0.20 + expansion * 0.15 + sentiment * 0.15`

### 2. Implement the scoring pipeline

Using `posthog-custom-events`, create a computed person property `power_user_score` that updates daily. Fire an event `power_user_score_computed` with the composite score and all dimension scores as properties:

```javascript
posthog.capture('power_user_score_computed', {
  composite_score: 78,
  depth_score: 85,
  tenure_score: 72,
  collaboration_score: 65,
  expansion_score: 80,
  sentiment_score: 90,
  percentile: 94
});
```

### 3. Create power user cohorts

Using `posthog-cohorts`, define tiered cohorts:

- **Champions** (score >= 80, top ~5%): deepest users, highest advocacy potential
- **Power Users** (score 60-79, top ~15%): strong candidates for program recruitment
- **Rising Stars** (score 40-59): users trending upward, worth nurturing toward power-user status
- **Standard Users** (score < 40): not yet candidates

### 4. Sync scored users to CRM

Using `attio-custom-attributes`, create a `power_user_score` attribute on contacts and a `power_user_tier` attribute (Champion / Power User / Rising Star / Standard). Using `attio-lists`, create a "Power User Candidates" list filtered to score >= 60. This list feeds the advocacy program recruitment pipeline.

### 5. Build the scoring dashboard

Build a PostHog dashboard with:
- Distribution histogram of power user scores (are they normally distributed or bimodal?)
- Tier breakdown: count and percentage in each tier
- Score trend over time: is the population getting more or less engaged?
- Top 20 power users ranked by composite score with dimension breakdown
- Rising Stars with highest month-over-month score increase (these are your acceleration targets)

### 6. Validate and calibrate

Review the top 20 scored users manually. Ask:
- Do these look like your best users? Would you want them as advocates?
- Are any obvious power users missing? If so, a scoring dimension is underweighted.
- Are any low-value users scoring high? If so, a dimension is overweighted.

Adjust weights and re-run until the top 20 matches your intuition. Lock weights and document the calibration.

## Output

- Composite power user score computed daily for all active users
- 4-tier cohort system in PostHog (Champions, Power Users, Rising Stars, Standard)
- Scored user list synced to Attio with tier labels
- Scoring dashboard in PostHog
- Calibrated and documented scoring weights

## Triggers

Run the scoring pipeline daily via n8n cron or PostHog computed properties. Re-calibrate weights quarterly or when the product's core actions change significantly.
