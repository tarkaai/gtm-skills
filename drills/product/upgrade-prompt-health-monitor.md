---
name: upgrade-prompt-health-monitor
description: Track upgrade prompt performance across trigger types, surfaces, and segments with automated degradation alerts
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-funnels
  - posthog-dashboards
  - posthog-cohorts
  - posthog-custom-events
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-triggers
  - attio-reporting
---

# Upgrade Prompt Health Monitor

This drill builds the measurement and alerting layer for in-app upgrade prompts. It tracks the full prompt-to-upgrade funnel per trigger type (limit proximity, feature gate, growth signal), detects performance degradation, and surfaces which prompt variants and segments are converting or failing.

## Input

- Upgrade prompts deployed via the `upgrade-prompt` drill (at least 1 trigger type live)
- PostHog tracking `upgrade_prompt_shown`, `upgrade_prompt_clicked`, `upgrade_started`, `upgrade_completed` events
- n8n instance for scheduled monitoring
- Attio CRM with expansion deal records

## Steps

### 1. Build the upgrade prompt funnel

Using the `posthog-funnels` fundamental, create a funnel for each trigger type:

```
upgrade_prompt_shown (trigger_type = "limit_proximity")
  -> upgrade_prompt_clicked
    -> upgrade_started
      -> upgrade_completed
```

Create separate funnels for:
- **Limit proximity**: user at 80%+ of a plan limit
- **Feature gate**: user attempted a gated feature
- **Growth signal**: usage volume or team size grew rapidly
- **Time-based**: sustained free usage beyond 30 days

Set conversion window to 7 days (most upgrades happen within 48 hours of prompt, but allow a full week for email follow-up conversions).

Break down each funnel by:
- `plan_current` (free, starter, pro) to see which plans convert
- `prompt_surface` (in-app modal, banner, tooltip, email) to see which delivery method works
- `prompt_variant` (for A/B test tracking)

### 2. Build the upgrade prompt dashboard

Using `posthog-dashboards`, create a dashboard called "Upgrade Prompts — Health":

| Panel | Type | What it shows |
|-------|------|---------------|
| Prompts shown this week | Trend | Daily count of `upgrade_prompt_shown`, broken down by trigger type |
| Prompt CTR by trigger | Bar chart | Click rate per trigger type, current week vs previous 4-week average |
| Upgrade funnel by trigger | Funnel | Full funnel per trigger type (shown -> clicked -> started -> completed) |
| Revenue from prompts | Trend | Sum of `upgrade_completed.revenue_delta` per day |
| Prompt fatigue signal | Trend | Ratio of `upgrade_prompt_dismissed` to `upgrade_prompt_shown` over time; rising ratio = fatigue |
| Segment performance | Table | CTR and conversion by user segment (plan, company size, usage tier) |
| Surface comparison | Bar chart | Conversion rate by prompt surface (in-app vs email vs tooltip) |

Set dashboard subscription to deliver Monday 09:00 to the growth team.

### 3. Create performance cohorts

Using `posthog-cohorts`, create dynamic cohorts:

- **prompt-converted**: Users who completed an upgrade within 7 days of seeing a prompt. Use for revenue attribution.
- **prompt-fatigued**: Users who dismissed 3+ prompts in 14 days without clicking. Suppress further prompts for these users.
- **prompt-high-intent**: Users who clicked a prompt but did not complete the upgrade. Route to a follow-up email or in-app help.
- **prompt-never-shown**: Active users on a free or lower plan who have never seen an upgrade prompt. Potential untapped audience.

### 4. Build degradation detection

Using `posthog-anomaly-detection` and `n8n-scheduling`, create a daily workflow that:

1. Queries PostHog for each trigger type's CTR over the last 7 days
2. Compares against the 4-week rolling average CTR for that trigger type
3. Flags any trigger type where CTR dropped more than 20% from its rolling average
4. Flags if the prompt-fatigued cohort grew more than 15% week-over-week

When a flag fires, the n8n workflow:
- Creates a note on the Attio campaign record for this play using `attio-reporting`
- Sends a Slack notification: "Upgrade prompt CTR for [trigger_type] dropped [X]% vs 4-week avg. Prompt fatigue cohort: [size]."
- If prompt-fatigued cohort exceeds 10% of active free users, recommend pausing prompts for that segment and switching to email-only nudges

### 5. Track prompt suppression and frequency

Using `posthog-custom-events`, log suppression events to prevent over-prompting:

```javascript
posthog.capture('upgrade_prompt_suppressed', {
  reason: 'fatigue_threshold',  // or 'cooldown_period', 'segment_exclusion'
  trigger_type: 'limit_proximity',
  user_prompt_count_30d: promptCount,
  days_since_last_prompt: daysSinceLast
});
```

Monitor the suppression rate. If more than 30% of eligible prompt impressions are being suppressed, the prompt strategy needs redesign (fewer, higher-quality triggers rather than broad coverage).

### 6. Measure revenue attribution

Using `posthog-custom-events`, tag every upgrade completion with its prompt attribution:

```javascript
posthog.capture('upgrade_completed', {
  trigger_type: 'feature_gate',
  prompt_surface: 'in_app_modal',
  prompt_variant: 'v2_social_proof',
  revenue_delta_monthly: mrr_increase,
  days_from_prompt_to_upgrade: daysDiff,
  attributed_to_prompt: wasPromptShownWithin7Days
});
```

Build a PostHog insight: monthly recurring revenue directly attributed to upgrade prompts, broken down by trigger type. This is the single number that justifies the play's existence.

## Output

- Upgrade prompt funnel per trigger type in PostHog
- Health dashboard with 7 panels and weekly delivery
- 4 dynamic cohorts for segmentation and suppression
- Daily degradation detection with Slack + Attio alerting
- Prompt suppression tracking to prevent fatigue
- Revenue attribution per trigger type

## Triggers

Dashboard reviewed weekly. Degradation detection runs daily via n8n cron at 08:00 UTC. Revenue attribution insight updated continuously via PostHog. Re-run full setup when adding new trigger types or prompt surfaces.
