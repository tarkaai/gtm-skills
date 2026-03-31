---
name: struggle-signal-detection
description: Detect users showing signs of struggle — error spikes, rage clicks, repeated failures, help-seeking behavior — and classify struggle severity for intervention routing
category: Experimentation
tools:
  - PostHog
  - Intercom
  - n8n
  - Attio
fundamentals:
  - posthog-session-recording
  - posthog-user-path-analysis
  - posthog-custom-events
  - posthog-cohorts
  - posthog-anomaly-detection
  - intercom-conversations-export
  - n8n-scheduling
  - n8n-triggers
  - attio-custom-attributes
  - attio-lists
---

# Struggle Signal Detection

This drill builds the detection layer that identifies users who are actively struggling with the product — before they file a support ticket, before they churn, often before they even realize they need help. It captures behavioral signals that indicate confusion, frustration, or blocked progress and outputs scored struggle profiles for downstream outreach.

This is distinct from `usage-drop-detection` (which catches disengagement) and `churn-risk-scoring` (which predicts churn broadly). Struggle detection catches users who are TRYING but FAILING — they are still engaged but having a bad experience.

## Input

- PostHog tracking active with session recording enabled (minimum 14 days of data)
- Intercom connected for support ticket correlation
- n8n instance for scheduled detection runs
- Attio CRM for storing struggle scores and routing

## Steps

### 1. Define struggle signals from product telemetry

Using the `posthog-custom-events` fundamental, ensure these events are tracked. If any are missing, instrument them before proceeding:

**Error signals:**
- `error_displayed` — any user-facing error message. Properties: `error_type`, `error_code`, `page`, `action_attempted`
- `api_error_client` — client-side API call failures. Properties: `endpoint`, `status_code`, `retry_count`
- `validation_failed` — form validation failures. Properties: `form_name`, `field_name`, `error_message`

**Frustration signals:**
- `rage_click` — PostHog auto-captures these if session recording is enabled. 3+ rapid clicks on the same non-interactive element within 2 seconds.
- `dead_click` — clicks on elements that produce no response
- `excessive_page_revisit` — user visits the same page 4+ times in a session without completing the page's intended action

**Help-seeking signals:**
- `help_docs_visited` — user navigated to help center / documentation. Properties: `article_slug`, `search_query`
- `help_search_no_results` — searched help docs and got zero results. Properties: `search_query`
- `intercom_messenger_opened` — opened the support chat widget
- `keyboard_shortcut_help_opened` — opened keyboard shortcut reference (confusion indicator)

**Blocked progress signals:**
- `action_abandoned` — started a multi-step flow but abandoned before completion. Properties: `flow_name`, `step_reached`, `total_steps`
- `repeated_failed_attempt` — attempted the same action 3+ times without success. Properties: `action_name`, `attempt_count`, `last_error`
- `feature_gate_hit` — tried to access a feature behind a paywall or permission gate. Properties: `feature_name`, `gate_type`

### 2. Build the struggle scoring query

Using `posthog-anomaly-detection`, compute a per-user struggle score. The scoring compares each user's recent struggle signals against both their own baseline and the product-wide baseline:

```sql
SELECT
  person_id,
  -- Error density: errors per session in last 7 days
  countIf(event IN ('error_displayed', 'api_error_client', 'validation_failed')
    AND timestamp > now() - interval 7 day) AS errors_7d,
  uniqIf(properties.$session_id,
    timestamp > now() - interval 7 day) AS sessions_7d,
  errors_7d / greatest(sessions_7d, 1) AS error_density,

  -- Rage/dead clicks in last 7 days
  countIf(event IN ('$rageclick', '$dead_click')
    AND timestamp > now() - interval 7 day) AS frustration_clicks_7d,

  -- Help-seeking events in last 7 days
  countIf(event IN ('help_docs_visited', 'help_search_no_results',
    'intercom_messenger_opened')
    AND timestamp > now() - interval 7 day) AS help_seeking_7d,

  -- Abandoned flows in last 7 days
  countIf(event = 'action_abandoned'
    AND timestamp > now() - interval 7 day) AS abandoned_flows_7d,

  -- Repeated failed attempts in last 7 days
  countIf(event = 'repeated_failed_attempt'
    AND timestamp > now() - interval 7 day) AS repeated_failures_7d,

  -- Composite struggle score (0-100)
  least(100,
    (error_density * 15) +
    (frustration_clicks_7d * 5) +
    (help_seeking_7d * 8) +
    (abandoned_flows_7d * 12) +
    (repeated_failures_7d * 15)
  ) AS struggle_score

FROM events
WHERE timestamp > now() - interval 7 day
  AND person_id IS NOT NULL
GROUP BY person_id
HAVING sessions_7d >= 2  -- only score users with real recent activity
ORDER BY struggle_score DESC
```

### 3. Classify struggle tiers

Assign each scored user to a tier based on score and signal pattern:

- **Mild (score 10-25):** Occasional friction. A few errors or one help doc visit. Normal product usage. Do not intervene — log only.
- **Moderate (score 26-50):** Consistent friction. Multiple error types, help-seeking, or 1+ abandoned flow. Route to automated proactive outreach (contextual in-app help or email).
- **Severe (score 51-75):** Active struggle. High error density combined with help-seeking and abandoned flows. Route to targeted outreach with specific assistance for the workflow they are stuck on.
- **Critical (score 76+):** Blocked user. Multiple repeated failures, rage clicks, and/or opened support chat. Route to immediate human-assisted intervention.

Using `posthog-cohorts`, create four dynamic cohorts: `struggle-mild`, `struggle-moderate`, `struggle-severe`, `struggle-critical`. These update automatically as the detection query runs.

### 4. Identify the SPECIFIC struggle context

Scoring alone is not enough for effective outreach. For each moderate+ user, extract what they are struggling WITH:

Using `posthog-user-path-analysis`, trace each struggling user's recent session paths to identify:

1. **The stuck workflow:** What were they trying to accomplish? Map the path: entry point -> steps completed -> failure/abandonment point.
2. **The failure mode:** Are they hitting the same error repeatedly? Trying the wrong approach? Missing a prerequisite step?
3. **The feature area:** Which product area concentrates their struggle? (e.g., integrations, data import, team setup, reporting)

Using `posthog-session-recording`, flag the last 3 sessions of severe/critical users for automated review. Extract: pages visited, errors encountered, time spent on each page (long dwell on simple pages = confusion), and the final action before session end.

Store the struggle context as structured data:

```json
{
  "person_id": "user_123",
  "struggle_score": 68,
  "tier": "severe",
  "primary_stuck_workflow": "data-import",
  "failure_mode": "csv-format-validation",
  "error_messages": ["Invalid date format in column 3", "Missing required field: email"],
  "help_docs_searched": ["csv import", "date format"],
  "sessions_with_struggle": 4,
  "last_struggle_timestamp": "2025-03-28T14:22:00Z"
}
```

### 5. Correlate with support history

Using the `intercom-conversations-export` fundamental, check if the struggling user has existing support tickets:

- **No ticket filed:** Highest priority for proactive outreach. They are struggling silently.
- **Open ticket filed:** Do not send proactive outreach (avoid conflicting channels). Instead, enrich the existing ticket with struggle context so the support agent has behavioral data.
- **Recent ticket resolved:** Check if the struggle signals match the resolved ticket's topic. If yes, the resolution did not work — re-route to a different intervention.

### 6. Store struggle data in the CRM

Using the `attio-custom-attributes` fundamental, add these fields to the contact/company record:

- `struggle_score`: 0-100 numeric
- `struggle_tier`: mild | moderate | severe | critical | none
- `struggle_primary_workflow`: the workflow they are stuck on
- `struggle_failure_mode`: the specific failure pattern
- `struggle_last_detected`: timestamp
- `struggle_consecutive_days`: how many consecutive days struggle was detected
- `struggle_outreach_sent`: boolean (has proactive outreach been triggered)

Using `attio-lists`, maintain a list called "Struggling Users — Active" containing all moderate+ users with their struggle context.

### 7. Build the scheduled detection workflow

Using `n8n-scheduling`, create a workflow that runs every 6 hours:

1. Run the struggle scoring query from Step 2 against PostHog
2. Classify into tiers (Step 3)
3. For moderate+ users, extract struggle context (Step 4)
4. Check support ticket status (Step 5)
5. Update Attio records (Step 6)
6. For users who moved INTO moderate/severe/critical since last run, fire a webhook to the `proactive-outreach-pipeline` drill
7. For users whose struggle resolved (score dropped back below 10), clear the tier and log recovery

Using `n8n-triggers`, add a webhook endpoint for on-demand struggle checks (useful when a support agent wants to check a specific user's struggle profile).

### 8. Track detection accuracy

Using `posthog-custom-events`, log every detection:

```javascript
posthog.capture('struggle_detected', {
  person_id: userId,
  struggle_score: 68,
  struggle_tier: 'severe',
  primary_workflow: 'data-import',
  failure_mode: 'csv-format-validation',
  has_support_ticket: false
});
```

After 30 days, measure:
- Of users flagged severe/critical, what percentage filed a support ticket within 7 days? (validates the signal)
- Of users flagged severe/critical who received NO outreach, what percentage churned within 30 days? (validates the urgency)
- Of users flagged moderate who resolved on their own, what was different about their struggle pattern? (improves tier thresholds)

Target: 50%+ of severe/critical flags should correspond to users who either file a ticket, contact support, or churn within 30 days if not helped.

## Output

- A per-user struggle score computed every 6 hours
- Four PostHog cohorts (mild, moderate, severe, critical) updated automatically
- Structured struggle context (stuck workflow, failure mode, help-seeking behavior) for each flagged user
- Attio records enriched with struggle data for team visibility
- Webhook trigger for downstream proactive outreach
- Detection accuracy tracking via PostHog events

## Triggers

Runs every 6 hours via n8n cron. On-demand via webhook for individual user checks. Recalibrate scoring weights monthly based on correlation with actual support tickets and churn.
