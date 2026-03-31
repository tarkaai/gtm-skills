---
name: feature-flag-management-smoke
description: >
  Feature Flag System -- Smoke Test. Deploy 5 feature flags with progressive rollout
  conditions in PostHog, execute one full rollout cycle, and validate that the flag
  infrastructure works end-to-end before automating.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "5 flags deployed with at least 1 completing a full rollout cycle (0% to 100%)"
kpis: ["Flags deployed", "Rollout completion rate", "Rollback count"]
slug: "feature-flag-management"
install: "npx gtm-skills add product/retain/feature-flag-management"
drills:
  - posthog-gtm-events
  - threshold-engine
---
# Feature Flag System -- Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes
5 feature flags created and deployed in PostHog. At least 1 flag completes a full rollout cycle from 0% to 100% with no rollback. The agent confirms that flag evaluation, rollout percentage changes, and cohort-based targeting all work via the PostHog API.

## Leading Indicators
- PostHog feature flag API responds correctly to create, read, update operations
- Flag evaluation returns the correct variant for users in and outside the rollout percentage
- `$feature_flag_called` events appear in PostHog when flags are evaluated in the product
- Rollout percentage changes propagate within 60 seconds

## Instructions

### 1. Configure PostHog event tracking for flags
Run the `posthog-gtm-events` drill to set up the base event taxonomy. Add these flag-specific events:
- `flag_created` — properties: flag_key, risk_level, owner, rollout_schedule
- `flag_rollout_advanced` — properties: flag_key, old_percentage, new_percentage
- `flag_rollout_completed` — properties: flag_key, total_days_to_complete
- `flag_rolled_back` — properties: flag_key, rollback_reason, percentage_at_rollback

### 2. Create 5 feature flags via PostHog API
For each flag, use the PostHog API:
```
POST /api/projects/<project_id>/feature_flags/
{
  "key": "{feature-slug}",
  "name": "{Feature Name}",
  "filters": {
    "groups": [{
      "rollout_percentage": 0
    }]
  },
  "active": true
}
```

Create flags across different risk levels to test the range:
- 2 low-risk flags (UI tweaks, copy changes) — start at 5% canary
- 2 medium-risk flags (new features) — start at 2% canary
- 1 high-risk flag (core flow change) — start at 1% canary, internal-only cohort

Log each creation as a `flag_created` event.

### 3. Execute a manual progressive rollout on 1 flag
Choose one low-risk flag. Manually advance it through the low-risk schedule:
- Day 0: Set to 5%. Verify flag evaluates correctly for ~5% of users via PostHog live events.
- Day 1: Advance to 25%. Check `$feature_flag_called` events show ~25% true evaluations.
- Day 3: Advance to 50%. Verify no error rate increase in treatment group.
- Day 5: Advance to 100%. Confirm all users see the feature.

At each stage, use the PostHog API to update:
```
PATCH /api/projects/<project_id>/feature_flags/<flag_id>/
{"filters": {"groups": [{"rollout_percentage": 25}]}}
```

Log each advance as a `flag_rollout_advanced` event.

### 4. Test a rollback
On a second flag, intentionally roll back from a partial rollout:
- Create the flag and advance to 10%
- Simulate a regression: roll back to 0% via the API
- Log `flag_rolled_back` with a reason
- Re-advance the flag to confirm the rollback was clean (no stuck state)

This validates that the rollback mechanism works before you rely on it in automation.

### 5. Test cohort-based targeting
For the high-risk flag, create a PostHog cohort for internal users and target the flag to that cohort only:
```
POST /api/projects/<project_id>/feature_flags/
{
  "key": "high-risk-core-change",
  "filters": {
    "groups": [{
      "properties": [{
        "key": "id",
        "value": <internal-users-cohort-id>,
        "type": "cohort"
      }],
      "rollout_percentage": 100
    }]
  }
}
```

Verify that internal users see the flag and external users do not.

### 6. Evaluate against threshold
Run the `threshold-engine` drill. Pass criteria: 5 flags deployed AND at least 1 completed a full 0%->100% rollout cycle. If PASS, proceed to Baseline. If FAIL, diagnose which API operations did not work and fix before re-running.

**Human action required:** Review the 5 flags in PostHog to confirm they correspond to real features in your product. Verify the SDK is checking these flags in the product code at the correct decision points.

## Time Estimate
- 1 hour: PostHog event setup and flag taxonomy design
- 2 hours: Create 5 flags and execute manual progressive rollout
- 1 hour: Test rollback and cohort targeting
- 1 hour: Verify all events logged correctly and evaluate threshold

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, event tracking, cohorts | Free tier: 1M events/mo, unlimited flags. https://posthog.com/pricing |

## Drills Referenced
- `posthog-gtm-events` -- establishes the event taxonomy for flag lifecycle tracking
- `threshold-engine` -- evaluates pass/fail against the 5-flag deployment target
