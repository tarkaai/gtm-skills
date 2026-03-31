---
name: integration-wizard-build
description: Build an AI-guided integration setup wizard using Intercom checklists, contextual bots, and PostHog tracking with automated failure recovery
category: Onboarding
tools:
  - Intercom
  - PostHog
  - n8n
  - Loops
fundamentals:
  - intercom-checklists
  - intercom-bots
  - intercom-in-app-messages
  - intercom-product-tours
  - posthog-custom-events
  - posthog-funnels
  - n8n-triggers
  - n8n-workflow-basics
  - n8n-error-handling
  - loops-transactional
---

# Integration Wizard Build

This drill builds an AI-guided integration setup wizard that walks new users through connecting their critical integrations during onboarding. The wizard uses Intercom checklists for persistent progress tracking, contextual bots for real-time troubleshooting, and n8n workflows for automated failure detection and recovery. The goal is to maximize the percentage of new users who successfully connect at least one integration within their first session.

## Prerequisites

- Intercom installed in your product with Messenger enabled
- PostHog tracking with user identification
- n8n instance with Intercom and PostHog credentials configured
- Loops account for fallback email sequences
- A list of your product's available integrations ranked by: frequency of use, correlation with retention, and setup complexity
- Your product's integration API or webhook system that can emit events when integrations are connected, disconnected, or fail

## Input

- Prioritized list of integrations (top 3-5 that correlate most with activation/retention)
- Integration setup requirements for each (OAuth, API key, webhook URL, etc.)
- Common failure modes per integration (expired tokens, wrong permissions, rate limits)
- Your product's integration status API endpoint or webhook

## Steps

### 1. Rank integrations by activation impact

Query PostHog to determine which integrations correlate most with 30-day retention. Using `posthog-custom-events`, pull:

```
SELECT integration_name,
  COUNT(DISTINCT user_id) as connected_users,
  AVG(CASE WHEN retained_30d THEN 1 ELSE 0 END) as retention_rate
FROM events
WHERE event = 'integration_connected'
GROUP BY integration_name
ORDER BY retention_rate DESC
```

If you lack historical data, rank by: 1) integrations that deliver the product's core value promise, 2) integrations with the simplest setup flow, 3) integrations your ICP is most likely to already use.

Select the top 3 integrations for the wizard. Do not overwhelm users with every possible integration.

### 2. Build the integration checklist in Intercom

Using the `intercom-checklists` fundamental, create a checklist titled "Set up your integrations" with one step per priority integration plus a completion step:

**Step 1: "Connect [Integration 1]"**
- Description: "Connect [Integration 1] to start [specific value]. Takes about 2 minutes."
- Action type: Link to `/settings/integrations/[integration-1]`
- Auto-completion rule: `integration_1_connected` equals `true`

**Step 2: "Connect [Integration 2]"**
- Description: "Connect [Integration 2] to enable [specific value]. Takes about 3 minutes."
- Action type: Link to `/settings/integrations/[integration-2]`
- Auto-completion rule: `integration_2_connected` equals `true`

**Step 3: "Connect [Integration 3]"**
- Description: "Connect [Integration 3] to unlock [specific value]. Takes about 2 minutes."
- Action type: Link to `/settings/integrations/[integration-3]`
- Auto-completion rule: `integration_3_connected` equals `true`

**Step 4: "You're all set"**
- Description: "All integrations connected. Your data is flowing."
- Action type: Link to the main dashboard
- Auto-completion rule: All previous steps complete

Set audience rules: show to users where `signed_up_at` is within the last 14 days AND `integration_wizard_completed` is not `true`.

### 3. Build contextual setup guidance bots

Using the `intercom-bots` fundamental, create a Custom Bot for each integration page:

**Bot trigger:** User lands on `/settings/integrations/[integration-name]` AND has not completed that integration step.

**Bot flow:**
1. "Setting up [Integration]? I can walk you through it step by step."
2. Detect the integration's auth method:
   - OAuth: "Click 'Connect' and authorize access. I'll confirm when it's connected."
   - API key: "You'll need your API key from [Integration]'s settings. Here's how to find it: [link to help article]."
   - Webhook: "Copy this webhook URL and paste it in [Integration]'s settings: [dynamic URL]."
3. After the user attempts setup, check status via the product's integration API
4. If successful: "Connected. [Integration] is now syncing your data. [Checklist step auto-completes]"
5. If failed: Branch to troubleshooting flow (see Step 4)

Use `intercom-product-tours` to create a 3-step guided tour for each integration that highlights: the connect button, the required credentials field, and the success confirmation.

### 4. Build automated failure detection and recovery

Using `n8n-triggers` and `n8n-workflow-basics`, create a webhook workflow that fires on integration failure events from your product:

```
Product Webhook (integration_setup_failed)
  -> Extract: user_id, integration_name, error_type, error_message
  -> Classify error:
     - "auth_expired" -> Send Intercom message: "Your [Integration] token expired. Reconnect here: [link]"
     - "permissions_insufficient" -> Send Intercom message: "We need [specific permission]. Here's how to grant it: [link]"
     - "rate_limited" -> Log and auto-retry in 5 minutes via n8n Wait node
     - "unknown" -> Route to human support via Intercom assignment
  -> Log to PostHog: integration_setup_failed with {integration_name, error_type, retry_count}
  -> Update Intercom user attribute: last_integration_error = error_type
```

Using `n8n-error-handling`, add retry logic: for transient failures (rate limits, timeouts), retry up to 3 times with exponential backoff. For permanent failures (wrong credentials, missing permissions), trigger the Intercom troubleshooting message immediately.

### 5. Build the stalled-user rescue workflow

Using `n8n-workflow-basics` and `n8n-triggers`, create a workflow that detects users who started but did not finish integration setup:

```
n8n Cron (runs every 6 hours)
  -> Query PostHog: users where integration_wizard_started = true
     AND integration_wizard_completed != true
     AND last_active > 1 hour ago (exclude currently active users)
     AND wizard_started_at < 24 hours ago
  -> For each stalled user:
     -> Check which integration step they stalled on
     -> Send contextual Intercom message using intercom-in-app-messages:
        "Looks like you started connecting [Integration] but didn't finish.
         The most common issue is [top error for that integration].
         [Link to resume setup]"
  -> If stalled > 48 hours with no response:
     -> Trigger a Loops transactional email (using loops-transactional) with:
        Subject: "Need help connecting [Integration]?"
        Body: Step-by-step guide for the specific integration they stalled on
        CTA: Deep link to resume setup
```

### 6. Instrument PostHog tracking

Using `posthog-custom-events`, capture these events throughout the wizard:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `integration_wizard_started` | User opens checklist or visits integrations page for first time | `signup_source`, `plan_type`, `persona_type` |
| `integration_step_started` | User clicks a checklist step or visits an integration setup page | `integration_name`, `step_number`, `auth_method` |
| `integration_setup_attempted` | User initiates the connection (clicks Connect, submits API key) | `integration_name`, `auth_method` |
| `integration_setup_succeeded` | Integration successfully connected and verified | `integration_name`, `time_to_connect_seconds`, `attempt_number` |
| `integration_setup_failed` | Integration connection attempt failed | `integration_name`, `error_type`, `error_message`, `attempt_number` |
| `integration_wizard_completed` | User finishes all checklist steps (or 1+ integrations at Smoke) | `integrations_connected`, `total_time_seconds`, `steps_skipped` |
| `integration_wizard_abandoned` | User dismisses checklist and does not return within 48 hours | `last_step_completed`, `integrations_connected` |

### 7. Build the setup funnel in PostHog

Using `posthog-funnels`, create:

**Primary funnel: "Integration Wizard Completion"**
```
integration_wizard_started -> integration_step_started -> integration_setup_attempted
  -> integration_setup_succeeded -> integration_wizard_completed
```
Break down by: `integration_name`, `signup_source`, `plan_type`.

**Failure funnel: "Integration Setup Failures"**
```
integration_setup_attempted -> integration_setup_failed
```
Break down by: `integration_name`, `error_type`. This shows which integrations fail most and why.

**Recovery funnel: "Stalled User Recovery"**
```
integration_wizard_abandoned -> rescue_message_sent -> integration_step_started
  -> integration_setup_succeeded
```
This measures how effective the rescue workflow is.

### 8. Test end-to-end

Before launching to real users:

1. Create a test user account
2. Verify the Intercom checklist appears on first login
3. Click each checklist step and verify it navigates to the correct integration page
4. Complete one integration and verify the checklist step auto-completes
5. Simulate an integration failure and verify the bot delivers the correct troubleshooting message
6. Verify all PostHog events fire correctly in the Live Events view
7. Wait 24+ hours without completing and verify the rescue workflow fires
8. Verify the rescue Intercom message and Loops email arrive with correct content
9. Complete all integrations and verify the wizard completion event fires

Fix any broken steps before proceeding.

## Output

- Intercom checklist guiding users through top 3 integration setups with auto-completion
- Contextual Intercom bots providing step-by-step setup guidance per integration
- Product tours highlighting key UI elements for each integration
- n8n workflow detecting integration failures and triggering contextual recovery messages
- Stalled-user rescue workflow via Intercom and Loops
- Full PostHog event tracking: wizard start, step progress, success, failure, abandonment
- PostHog funnels: completion funnel, failure funnel, recovery funnel

## Triggers

Run once during initial play setup. Re-run when adding new integrations to the wizard or when changing the integration priority ranking.
