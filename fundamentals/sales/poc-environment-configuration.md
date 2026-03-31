---
name: poc-environment-configuration
description: Configure a POC environment with prospect-specific data, integrations, and success tracking instrumentation
tool: Product API / PostHog
difficulty: Advanced
---

# POC Environment Configuration

Configure an existing sandbox or trial environment specifically for a POC engagement: load prospect-relevant data, enable the features being evaluated, instrument success criteria tracking, and connect check-in scheduling.

## When to Use

After a sandbox has been provisioned (via `sandbox-environment-provision`) and POC success criteria have been defined (via `poc-success-criteria-template`). This fundamental bridges the gap between a generic sandbox and a purpose-built POC environment.

## Instructions

### 1. Load the POC success criteria

Pull the POC success criteria JSON from the Attio deal note. Extract:
- Success criteria (the specific tests to run)
- Milestones (the checkpoint schedule)
- Support model (check-in cadence and channel)

### 2. Map criteria to product features

For each success criterion, determine which product features and data are required:

```
POST https://api.anthropic.com/v1/messages
Body:
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1000,
  "messages": [{
    "role": "user",
    "content": "Given these POC success criteria, map each to the product features and sample data needed.\n\nCriteria: {criteria_json}\nAvailable features: {feature_list}\nAvailable sample data personas: {persona_list}\n\nReturn JSON: { \"feature_config\": [\"feature_name\", ...], \"data_requirements\": [{ \"type\": \"...\", \"volume\": \"...\", \"persona\": \"...\" }], \"integration_requirements\": [\"integration_name\", ...] }"
  }]
}
```

### 3. Configure the POC environment

Using the product API or admin tooling:

1. **Enable required features** via feature flags or plan configuration. Disable non-relevant features to reduce noise and focus the evaluation.
2. **Inject criterion-specific data** using `seed-data-injection`. For each success criterion, ensure the sandbox contains data that allows the prospect to test the specific workflow.
3. **Connect integrations** the prospect needs to validate. Use sandbox/test credentials for third-party services.
4. **Create guided paths** in the product (if supported): bookmarks, saved views, or pre-built workflows that align with each milestone.

### 4. Instrument success criteria tracking

For each success criterion, create a PostHog event that fires when the criterion is met:

```javascript
// Example: Criterion "Import 100+ records from CSV"
posthog.capture('poc_criterion_met', {
  deal_id: '{deal_id}',
  criterion_id: 'import_records',
  criterion_name: 'Import 100+ records from CSV',
  priority: 'must-have',
  value_achieved: recordCount,
  target_value: 100,
  met: recordCount >= 100,
  days_into_poc: daysSince(pocStartDate)
});
```

Also instrument milestone achievement:

```javascript
posthog.capture('poc_milestone_achieved', {
  deal_id: '{deal_id}',
  milestone_name: '{milestone_name}',
  milestone_index: 1,
  total_milestones: 5,
  scheduled_day: 2,
  actual_day: daysSince(pocStartDate),
  on_schedule: actualDay <= scheduledDay
});
```

### 5. Schedule check-in touchpoints

Using the Cal.com API (`calcom-booking-links`), generate pre-scheduled check-in links:

- **Kickoff call**: Day 1 (walkthrough, confirm criteria, answer questions)
- **Mid-point review**: Midway through POC (progress check, address blockers)
- **Final review**: Last 2 days (results review, decision discussion)

Store the Cal.com links in the Attio deal record.

### 6. Configure the POC dashboard

Create a deal-specific PostHog dashboard (or filtered view) showing:
- Criteria progress (met/not-met for each criterion)
- Milestone timeline (on-track/behind for each milestone)
- Session activity (login frequency, feature usage)
- Blocker log (errors encountered, help requests)

## Error Handling

- **Feature not available**: If a required feature is not in the product tier, flag this to the deal owner with options (upgrade sandbox tier, provide workaround, adjust criterion).
- **Data injection failure**: Retry once. If persistent, provision with generic data and note the limitation.
- **Integration auth failure**: Log the failure and alert the prospect's technical contact to provide credentials.

## Output

A fully configured POC environment with criterion-specific data, tracking instrumentation for every success criterion and milestone, scheduled check-in calls, and a live progress dashboard.
