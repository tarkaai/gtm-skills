---
name: sandbox-usage-tracking
description: Capture and structure sandbox usage events in PostHog for engagement scoring and sales intelligence
tool: PostHog
difficulty: Config
---

# Sandbox Usage Tracking

Instrument a sandbox environment to capture granular usage events that feed engagement scoring, intervention triggers, and close-rate prediction models.

## When to Use

After provisioning a sandbox via `sandbox-environment-provision`. This fundamental sets up the event taxonomy specific to sandbox evaluation — distinct from general product analytics because the audience is prospects, not customers, and the goal is deal progression, not retention.

## Instructions

### 1. Define the sandbox event taxonomy

All sandbox events follow the naming convention `sandbox_{action}` with standard properties:

| Event | Fires When | Key Properties |
|-------|-----------|----------------|
| `sandbox_provisioned` | Environment is created | `deal_id`, `industry`, `persona`, `sample_data_records` |
| `sandbox_first_login` | Prospect logs in for the first time | `deal_id`, `hours_since_provisioned`, `login_method` |
| `sandbox_session_started` | Any login after first | `deal_id`, `session_number`, `days_since_provisioned` |
| `sandbox_feature_used` | Prospect interacts with a product feature | `deal_id`, `feature_name`, `feature_category`, `is_differentiator` |
| `sandbox_workflow_completed` | Prospect completes a multi-step workflow end-to-end | `deal_id`, `workflow_name`, `steps_completed`, `duration_seconds` |
| `sandbox_data_uploaded` | Prospect uploads their own data | `deal_id`, `data_type`, `record_count` |
| `sandbox_error_encountered` | An error occurs during usage | `deal_id`, `error_type`, `feature_name`, `severity` |
| `sandbox_help_requested` | Prospect clicks help, opens docs, or contacts support | `deal_id`, `help_type`, `context_feature` |
| `sandbox_milestone_achieved` | Prospect completes a success checklist item | `deal_id`, `milestone_name`, `milestone_index`, `total_milestones` |
| `sandbox_expired` | Sandbox reaches expiry date | `deal_id`, `total_sessions`, `total_features_used`, `milestones_completed` |

### 2. Implement event capture

In your product frontend, wrap sandbox-specific tracking:

```javascript
// Detect sandbox context
const isSandbox = window.location.hostname.includes('sandbox-') || currentWorkspace?.sandbox === true;

if (isSandbox) {
  // Enrich every event with sandbox context
  posthog.register({
    sandbox_id: currentWorkspace.sandboxId,
    deal_id: currentWorkspace.dealId,
    prospect_company: currentWorkspace.prospectCompany,
    industry: currentWorkspace.industry,
    days_since_provisioned: daysSince(currentWorkspace.provisionedAt)
  });
}
```

For feature usage tracking, instrument each product area:

```javascript
function trackFeatureUsage(featureName, category, isDifferentiator) {
  posthog.capture('sandbox_feature_used', {
    feature_name: featureName,
    feature_category: category,
    is_differentiator: isDifferentiator,
    session_duration_so_far: getSessionDuration()
  });
}
```

### 3. Build the engagement score

Create a PostHog computed property or n8n workflow that calculates a sandbox engagement score:

| Signal | Points | Max |
|--------|--------|-----|
| First login within 24 hours of provisioning | 10 | 10 |
| Each session after first | 5 | 25 |
| Each unique feature used | 3 | 30 |
| Each differentiator feature used | 5 | 15 |
| Each workflow completed | 8 | 24 |
| Own data uploaded | 15 | 15 |
| Each milestone achieved | 10 | 30 |
| Help requested (positive — shows engagement) | 2 | 6 |
| Error encountered (negative) | -3 | -15 |

**Score ranges**: 0-30 Cold, 31-60 Warm, 61-90 Hot, 91+ Champion.

### 4. Configure real-time alerts

Set up PostHog actions or n8n triggers for sales-critical events:

- **High intent**: `sandbox_data_uploaded` or 3+ `sandbox_workflow_completed` in one session → Slack alert to deal owner: "Prospect is actively evaluating — consider reaching out."
- **Stall signal**: No `sandbox_session_started` for 3+ days after first login → Trigger re-engagement flow.
- **Error risk**: 2+ `sandbox_error_encountered` in one session → Alert support to investigate and deal owner to follow up.
- **Milestone completion**: All milestones achieved → Alert deal owner: "Prospect completed full evaluation — ready for proposal."

### 5. Build the sandbox analytics dashboard

Create a PostHog dashboard with:
- Sandbox provisioning rate (sandboxes created / deals at Connected stage)
- Time to first login (histogram)
- Session count distribution
- Feature usage heatmap (which features get used most)
- Milestone completion funnel
- Engagement score distribution across active sandboxes
- Sandbox-to-proposal conversion by engagement score tier

## Error Handling

- **Missing deal_id**: If a sandbox session fires without a deal_id, log a warning and attempt to resolve via the sandbox_id → deal_id mapping in Attio.
- **Duplicate events**: Use PostHog's deduplication by including a unique event ID for milestone and workflow completion events.
- **Clock skew**: Use server-side timestamps for duration calculations, not client-side.

## Output

A complete sandbox usage event stream in PostHog, an engagement scoring model, real-time sales alerts, and a sandbox analytics dashboard.
