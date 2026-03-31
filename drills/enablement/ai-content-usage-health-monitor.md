---
name: ai-content-usage-health-monitor
description: Track AI content feature adoption, generation quality, and user satisfaction to detect degradation before it impacts retention
category: Enablement
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-cohorts
  - posthog-funnels
  - n8n-scheduling
  - attio-notes
---

# AI Content Usage Health Monitor

This drill builds the monitoring layer for an AI content generation feature embedded in your product. It tracks the full lifecycle from prompt submission through content acceptance to downstream retention impact. Without this drill, you know users are generating content but not whether it is any good or whether it keeps them around.

## Input

- PostHog tracking configured with AI content feature events (see event taxonomy below)
- n8n instance for scheduled monitoring
- Attio for logging health snapshots
- At least 14 days of AI content generation usage data

## Event Taxonomy

Ensure these events are firing in PostHog before proceeding:

```
ai_content_prompt_submitted   — user initiated a generation request
ai_content_generated          — system returned a result
ai_content_accepted           — user accepted/published the generated content (with or without edits)
ai_content_rejected           — user discarded the generated content
ai_content_edited             — user edited the generated content before accepting
ai_content_regenerated        — user requested a new generation for the same prompt
ai_content_feedback_positive  — user gave explicit positive feedback (thumbs up, rating)
ai_content_feedback_negative  — user gave explicit negative feedback (thumbs down, rating)
```

Properties on each event: `user_id`, `content_type` (blog post, email, social, etc.), `prompt_length`, `generation_time_ms`, `model_version`, `template_id` (if using templates).

## Steps

### 1. Build the AI content health dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Daily generation volume | Line chart (7-day trend) | Are more users generating content over time |
| Acceptance rate | Line chart (7-day rolling) | What percentage of generated content is accepted vs rejected |
| Edit rate | Line chart (7-day rolling) | How often users edit before accepting (high edit rate = quality issue) |
| Regeneration rate | Line chart (7-day rolling) | How often users request a second try (high regen = prompt/model issue) |
| Satisfaction score | Line chart (weekly) | Ratio of positive to negative explicit feedback |
| Generation-to-publish funnel | Funnel | prompt_submitted -> generated -> accepted -> published (if applicable) |
| Content type breakdown | Pie chart | Which content types are most generated |
| Retention lift | Comparison chart | 30-day retention of AI content users vs non-users |

### 2. Create health cohorts

Using `posthog-cohorts`, define reusable cohorts:

- **AI Power Users**: 10+ generations in the last 7 days with acceptance rate >60%
- **AI Experimenters**: 1-9 generations in the last 7 days
- **AI Churned**: Used AI content feature in weeks 1-2, zero usage in week 3+
- **AI Frustrated**: 3+ regenerations or rejections in a single session in the last 7 days
- **AI Non-Adopters**: Active product users with zero AI content generations ever

### 3. Build the weekly health check workflow

Using `n8n-scheduling`, create a weekly cron workflow that:

1. Queries PostHog for the trailing 7-day metrics: generation volume, acceptance rate, edit rate, regeneration rate, satisfaction score
2. Compares each metric to the 4-week rolling average
3. Classifies each metric: healthy (within 10% of average), warning (10-25% decline), critical (>25% decline)
4. Logs the health snapshot to Attio using `attio-notes`
5. If any metric is critical, sends an alert to Slack with the specific metric, current value, average value, and percentage change

### 4. Track the retention correlation

Using `posthog-funnels` and `posthog-cohorts`, measure the retention impact:

1. Create two cohorts: users who used AI content in their first 14 days vs users who did not
2. Compare 30-day, 60-day, and 90-day retention between the two groups
3. Track this comparison weekly as a leading indicator
4. If the retention gap between AI users and non-users narrows, the feature's value is eroding
5. If the gap widens, the feature is becoming more sticky

### 5. Monitor content type performance

Break down all metrics by content type. Identify:

- Which content types have the highest acceptance rate (these are working well)
- Which content types have the highest regeneration rate (these need prompt/model improvement)
- Which content types are most correlated with retention (these should be promoted most heavily)

## Output

- AI content health dashboard in PostHog with 8 panels
- 5 reusable health cohorts
- Weekly automated health check with Slack alerts for critical degradation
- Retention correlation tracking (AI users vs non-users)
- Content type performance breakdown

## Triggers

Weekly health check runs via n8n cron every Monday at 9 AM. Dashboard is reviewed weekly. Re-run the full setup when adding new content types, changing AI models, or modifying the feature's UI.
