---
name: sandbox-usage-monitoring
description: Track sandbox engagement patterns, trigger usage-based interventions, and correlate usage with deal outcomes
category: Sales
tools:
  - PostHog
  - Attio
  - Intercom
  - Loops
  - n8n
fundamentals:
  - sandbox-usage-tracking
  - posthog-funnels
  - posthog-cohorts
  - posthog-custom-events
  - posthog-dashboards
  - attio-deals
  - attio-notes
  - intercom-in-app-messages
  - loops-sequences
  - n8n-triggers
  - n8n-workflow-basics
---

# Sandbox Usage Monitoring

This drill builds the always-on monitoring system that watches sandbox usage patterns and triggers appropriate interventions. It sits between provisioning (the `sandbox-provisioning-workflow` drill) and deal progression, converting raw usage data into actionable sales intelligence.

## Input

- PostHog sandbox events flowing (from `sandbox-usage-tracking` fundamental)
- Active sandboxes with deal records in Attio
- Intercom installed in the sandbox product for in-app messaging
- n8n instance for automation

## Steps

### 1. Implement the sandbox event taxonomy

Run the `sandbox-usage-tracking` fundamental to instrument all sandbox-specific events. Verify events are flowing by checking PostHog Live Events for the `sandbox_*` namespace. Confirm each critical event fires correctly:

- `sandbox_first_login`
- `sandbox_session_started`
- `sandbox_feature_used`
- `sandbox_workflow_completed`
- `sandbox_data_uploaded`
- `sandbox_milestone_achieved`

### 2. Build the sandbox engagement funnel

Using `posthog-funnels`, create a funnel tracking the prospect journey through the sandbox:

1. `sandbox_provisioned` (entry)
2. `sandbox_first_login` (activation)
3. `sandbox_feature_used` (exploration, count >= 3 distinct features)
4. `sandbox_workflow_completed` (validation)
5. `sandbox_milestone_achieved` (success, 3+ milestones)

Measure conversion rates between each step. Break down by industry, persona, and deal size to identify which prospect segments engage most deeply.

### 3. Build the engagement scoring pipeline

Create an n8n workflow using `n8n-workflow-basics` that runs every 6 hours:

1. Query PostHog for all sandbox events in the last 6 hours, grouped by `sandbox_id`.
2. Calculate the engagement score per sandbox using the scoring model from `sandbox-usage-tracking`.
3. Write the updated score to Attio on the deal record using `attio-deals`.
4. Compare the current score to the previous score. Flag direction: rising, stable, or declining.

### 4. Configure usage-based interventions

Build n8n workflows triggered by specific usage patterns using `n8n-triggers`:

**Low usage interventions:**
- No login within 48 hours of provisioning → Send reminder email via `loops-sequences` with the walkthrough video link and a "Need help getting started?" message.
- Logged in but used <2 features after first session → Show Intercom in-app message via `intercom-in-app-messages`: "Try [specific feature relevant to their use case] next."
- No session for 5+ days → Send personal email from deal owner: "I noticed you haven't had a chance to explore yet. Want me to walk you through it?"

**High usage interventions:**
- 3+ workflows completed in one session → Slack alert to deal owner: "Prospect is deep in evaluation. Consider reaching out today."
- Own data uploaded → Immediate Slack alert: "Prospect uploaded their own data — high intent signal."
- All milestones completed → Alert deal owner and auto-draft a proposal invitation email.

**Error interventions:**
- 2+ errors in one session → Alert support team to investigate. Send Intercom message: "Looks like you hit a snag. Our team is on it."
- Same error repeated across sessions → Escalate to engineering with sandbox_id for reproduction.

### 5. Build the sandbox analytics dashboard

Using `posthog-dashboards`, create a dashboard with:

- **Provisioning velocity**: Sandboxes created per week, broken down by deal source.
- **Time to first login**: Histogram showing distribution. Target: <24 hours.
- **Session depth**: Average sessions per sandbox, average session duration.
- **Feature usage heatmap**: Which features get used most across all sandboxes.
- **Milestone completion funnel**: Percentage of sandboxes completing each milestone.
- **Engagement score distribution**: Current score distribution across all active sandboxes.
- **Conversion correlation**: Sandbox engagement score vs. deal outcome (won/lost/stalled). This is the key chart — it proves whether sandbox engagement predicts closes.

### 6. Sync sandbox intelligence to CRM

Create an n8n workflow that runs daily and updates each deal in Attio with:

- Current engagement score
- Milestones completed (count and list)
- Last session date
- Total time spent in sandbox
- Features explored (count)
- Risk flag (if declining engagement or approaching expiry with low engagement)

This data powers the deal owner's pipeline review and helps prioritize which prospects need attention.

## Output

- Real-time sandbox engagement scoring in Attio
- Automated usage-based interventions (email, in-app, Slack alerts)
- Sandbox analytics dashboard in PostHog
- Daily CRM sync of sandbox intelligence
- Correlation data between sandbox engagement and deal outcomes

## Triggers

Run continuously once the first sandbox is provisioned. The n8n workflows run on cron schedules (every 6 hours for scoring, daily for CRM sync, real-time for interventions).
