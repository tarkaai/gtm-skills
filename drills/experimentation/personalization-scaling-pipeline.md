---
name: personalization-scaling-pipeline
description: Scale personalization from per-segment rules to per-user dynamic adaptation using usage signals, feature flags, and automated variant selection
category: Experimentation
tools:
  - PostHog
  - Intercom
  - Loops
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-feature-flags
  - posthog-experiments
  - posthog-cohorts
  - posthog-custom-events
  - intercom-in-app-messages
  - intercom-user-properties
  - loops-sequences
  - loops-audience
  - attio-custom-attributes
  - attio-lists
  - n8n-workflow-basics
  - n8n-scheduling
  - hypothesis-generation
---

# Personalization Scaling Pipeline

This drill takes the per-segment personalization from the `personalization-rule-engine` and scales it to per-user dynamic adaptation. Instead of 4-6 static segment experiences, the system dynamically adjusts personalization surfaces based on each user's evolving behavior, experiment results, and predicted next-best-action. This is the 10x multiplier: same effort, dramatically more granular personalization.

## Input

- Per-segment personalization running and measured for at least 4 weeks (from `personalization-rule-engine`)
- PostHog experiments enabled
- Engagement scores computed daily (from `engagement-score-computation`)
- Behavioral segments assigned daily (from `user-behavior-segmentation`)
- Anthropic API key for LLM-powered content generation
- At least 500 active users (statistical significance requires volume)

## Steps

### 1. Identify the highest-impact personalization surfaces

Review 4 weeks of personalization event data from PostHog. Rank surfaces by impact:

```sql
SELECT
  properties.surface AS surface,
  properties.segment AS segment,
  count() AS impressions,
  countIf(event = 'personalization_surface_engaged') / countIf(event = 'personalization_surface_shown') AS engagement_rate,
  countIf(event = 'personalization_surface_engaged') AS engagements
FROM events
WHERE event IN ('personalization_surface_shown', 'personalization_surface_engaged')
  AND timestamp > now() - interval 28 day
GROUP BY surface, segment
ORDER BY engagements DESC
```

Focus scaling effort on the top 3 surfaces by engagement volume. Low-engagement surfaces need redesign, not scaling.

### 2. Build per-user feature vectors

Extend the segmentation model to a continuous feature vector per user. Using `posthog-custom-events`, compute daily:

- `engagement_score` (0-100, from engagement-score-computation)
- `behavior_segment` (categorical, from user-behavior-segmentation)
- `primary_workflow` (categorical)
- `feature_breadth` (count of distinct features used in 14 days)
- `collaboration_intensity` (collab actions per active day)
- `session_recency_hours` (hours since last session)
- `personalization_engagement_rate` (personalized surfaces engaged / shown, trailing 14 days)
- `activation_complete` (boolean)
- `plan_type` (free / trial / paid / enterprise)

Store the vector as PostHog person properties and Attio custom attributes (using `attio-custom-attributes`).

### 3. Design the dynamic variant selection engine

Replace static segment-to-variant mapping with a dynamic selection. Using `n8n-workflow-basics`, build a workflow that runs when a user starts a session:

1. **Pull the user's feature vector** from PostHog person properties
2. **Select variants dynamically** based on rules that combine segment + engagement + recency:

```
# Dashboard layout
IF engagement_score >= 80 → "advanced-dashboard" (power tools prominent)
ELIF engagement_score >= 50 AND feature_breadth < 4 → "discovery-dashboard" (highlight unused features)
ELIF engagement_score >= 50 → "standard-dashboard"
ELIF engagement_score < 30 AND session_recency_hours > 168 → "re-engagement-dashboard" (show what they missed)
ELSE → segment-default-dashboard

# CTA variant
IF NOT activation_complete → "activation-cta"
ELIF plan_type = "free" AND engagement_score >= 60 → "upgrade-cta"
ELIF collaboration_intensity = "None" AND feature_breadth >= 3 → "invite-team-cta"
ELIF personalization_engagement_rate < 0.2 → "simplified-cta" (reduce noise)
ELSE → segment-default-cta
```

3. **Set PostHog feature flag overrides** using the PostHog API to assign the selected variant for this user
4. **Log the selection** as `personalization_dynamic_variant_selected` with `{surface, variant, reasoning, feature_vector_snapshot}`

### 4. Launch systematic A/B testing across variants

Using `posthog-experiments`, create experiments for the top 3 surfaces. For each surface:

1. Define the control (current static segment variant) and 2-3 dynamic variants
2. Split traffic: 50% control (static), 50% dynamic selection
3. Primary metric: personalization engagement rate for that surface
4. Secondary metrics: retention at 14 days, feature adoption breadth
5. Run for 2 weeks minimum or until 200+ users per variant
6. Use `hypothesis-generation` to formulate each experiment hypothesis before launching

Document each experiment in Attio: hypothesis, start date, expected duration, success criteria.

### 5. Scale email personalization with LLM generation

Using `loops-sequences` and `loops-audience`, move from 5-6 static segment sequences to dynamically personalized emails:

1. Build an n8n workflow triggered weekly per user
2. Pull the user's feature vector and recent product activity from PostHog
3. Call Anthropic Claude API with a structured prompt:

```
Given this user's product behavior:
- Segment: {segment}
- Engagement score: {score}
- Primary workflow: {workflow}
- Features used this week: {features}
- Features NOT used that similar users love: {recommendations}
- Days since last session: {recency}

Write a single-paragraph email (max 80 words) that:
1. References one specific thing they did this week
2. Suggests one specific next action based on their behavior
3. Includes one concrete benefit of taking that action

Tone: helpful, specific, not salesy. No greetings or sign-offs (those are templated).
```

4. Inject the LLM-generated paragraph into a Loops transactional email template
5. Track opens/clicks per user with `personalization_email_dynamic_opened` and `personalization_email_dynamic_clicked` events

**Guardrail:** Human review the first 50 generated emails before full launch. Set up a Slack notification in n8n that posts a sample of 5 emails daily for ongoing quality monitoring.

### 6. Build the scaling dashboard

Using `posthog-cohorts`, create cohorts for monitoring:

- `personalization-dynamic-active` — users receiving dynamic personalization
- `personalization-static-control` — users on static segment personalization
- `personalization-high-engagement` — users with personalization engagement rate > 50%
- `personalization-low-engagement` — users with rate < 10%

Build a PostHog dashboard comparing:
- Engagement rate: dynamic vs static
- Retention at 7, 14, 30 days: dynamic vs static
- Feature adoption breadth: dynamic vs static
- Churn rate: dynamic vs static

### 7. Implement volume scaling automation

Using `n8n-scheduling`, build workflows that scale without proportional manual effort:

- **Auto-segment refresh:** Daily. Handles 10 users or 10,000 users identically.
- **Dynamic variant selection:** Per-session trigger. Scales with traffic.
- **LLM email generation:** Weekly batch. Process all users in parallel batches of 50.
- **Experiment monitoring:** Daily check. Auto-extend experiments that need more data, auto-conclude experiments that have reached significance.

Set Attio alerts (using `attio-lists`) for: experiment concluded, variant winner found, personalization engagement rate dropped below 30% for any segment.

## Output

- Per-user feature vectors stored in PostHog and Attio
- Dynamic variant selection engine running per-session
- A/B experiments comparing static vs dynamic personalization
- LLM-powered dynamic email personalization
- Scaling dashboard tracking personalization effectiveness
- Automated workflows that handle growing user volume without manual intervention

## Triggers

- Per-session: dynamic variant selection via n8n webhook
- Daily: feature vector computation, experiment monitoring
- Weekly: LLM email batch, personalization performance review
- Monthly: variant rule tuning, experiment portfolio review
