---
name: workspace-setup-flow
description: Build a guided admin workspace setup flow using Intercom Checklists, in-app messages, and lifecycle emails for team product onboarding
category: Onboarding
tools:
  - Intercom
  - Loops
  - PostHog
  - n8n
fundamentals:
  - intercom-checklists
  - intercom-product-tours
  - intercom-in-app-messages
  - intercom-user-properties
  - loops-sequences
  - loops-audience
  - posthog-custom-events
  - posthog-funnels
  - n8n-triggers
  - n8n-workflow-basics
---

# Workspace Setup Flow

This drill builds the admin-specific onboarding path for team products. Admins have fundamentally different goals from end users during onboarding: they configure the workspace (billing, permissions, integrations, team structure) so their team can be productive. This drill creates a multi-channel guided setup flow that drives admins through workspace configuration to the point where they can invite their team.

## Prerequisites

- Intercom installed with Messenger and Checklists enabled
- Loops account configured for transactional and lifecycle emails
- PostHog tracking installed with user identification
- Your product distinguishes admin vs user roles at signup or first login
- Clear definition of what constitutes a "configured workspace" (the admin activation metric)

## Steps

### 1. Define the admin setup milestones

Map the critical path from admin signup to workspace readiness. A workspace is "ready" when the admin has completed enough configuration that inviting team members makes sense. Typical milestones for a team product:

1. `workspace_created` -- admin creates the workspace/organization
2. `profile_configured` -- admin sets company name, logo, timezone
3. `billing_configured` -- admin enters payment method or selects plan
4. `permissions_set` -- admin configures roles and access levels
5. `integration_connected` -- admin connects at least one external tool (SSO, data source, Slack, etc.)
6. `first_team_invite_sent` -- admin invites at least one team member
7. `workspace_ready` -- composite event: milestones 1-5 complete, workspace is configured for team use

Each milestone becomes a tracked PostHog event and an Intercom user attribute for checklist auto-completion.

### 2. Instrument admin setup events in PostHog

Using the `posthog-custom-events` fundamental, track every admin setup action:

```javascript
posthog.capture('workspace_created', {
  workspace_id: workspaceId,
  admin_user_id: userId,
  signup_source: utmSource,
  plan_selected: planName
});

posthog.capture('admin_setup_step_completed', {
  step_name: 'billing_configured',
  step_number: 3,
  total_steps: 6,
  time_since_signup_hours: hoursSinceSignup,
  workspace_id: workspaceId
});

posthog.capture('workspace_ready', {
  workspace_id: workspaceId,
  steps_completed: completedSteps,
  time_to_ready_hours: hoursSinceSignup,
  integrations_connected: integrationList
});
```

Track both individual step completions and the composite `workspace_ready` event.

### 3. Build the admin setup checklist in Intercom

Using the `intercom-checklists` fundamental, create a "Workspace Setup" checklist with these steps:

| Step | Title | Action | Auto-complete trigger |
|------|-------|--------|----------------------|
| 1 | Set up your workspace | Link to /settings/workspace | `workspace_name_set` = true |
| 2 | Add your company details | Link to /settings/profile | `company_profile_completed` = true |
| 3 | Choose your plan | Link to /settings/billing | `billing_configured` = true |
| 4 | Set team permissions | Start tour (permissions tour) | `permissions_configured` = true |
| 5 | Connect your tools | Link to /settings/integrations | `integration_connected` = true |
| 6 | Invite your team | Link to /settings/team | `first_invite_sent` = true |

Set audience rules: show to users where `role` = "admin" AND `workspace_ready` != true AND `signed_up_at` within last 30 days.

Using `intercom-user-properties`, ensure your app sends these attributes to Intercom as the admin completes each step:

```javascript
Intercom('update', {
  billing_configured: true,
  admin_setup_progress: '3/6',
  admin_setup_step_3_completed_at: new Date().toISOString()
});
```

### 4. Build a permissions product tour

Using the `intercom-product-tours` fundamental, create a 4-step interactive tour for the permissions step (the most complex setup action):

1. Highlight the "Roles" section -- explain what roles control
2. Interactive: create a custom role OR select a default template
3. Highlight the "Permissions matrix" -- explain what each permission does
4. Interactive: assign a permission level to the role they just created

This tour auto-launches when the admin clicks "Set team permissions" in the checklist.

### 5. Build stall-point nudges

Using the `intercom-in-app-messages` fundamental, create targeted messages for admins who stall:

- **24 hours, no billing**: "Quick question -- are you evaluating [Product] for your team? We have a 14-day free trial so you can invite your team before committing." CTA: link to billing page.
- **48 hours, no integration**: "Teams that connect [top integration] see [X%] faster setup. Connect in 2 minutes." CTA: link to integrations page.
- **72 hours, no team invite**: "Your workspace is ready. Invite your first teammate to see [Product] in action together." CTA: link to team invite page.

Each message fires once. Dismissed messages do not return.

### 6. Build the admin lifecycle email sequence

Using `loops-sequences` and `loops-audience`, create a 5-email admin setup sequence:

**Email 1 (immediate on workspace creation)**:
- Subject: "[Product] -- your workspace is ready. Here's what to do first."
- Body: Welcome message with a direct link to the setup checklist. One clear next step: "Set up your company profile (takes 2 minutes)."

**Email 2 (24 hours if billing not configured)**:
- Subject: "Quick setup step -- choose your plan"
- Body: Comparison of plan options. Link directly to billing page. Note the free trial period.
- Skip if: billing_configured = true

**Email 3 (48 hours if no integration connected)**:
- Subject: "Connect [top integration] to [Product] -- 2 minutes"
- Body: Step-by-step for the most popular integration. Link directly to integrations page.
- Skip if: integration_connected = true

**Email 4 (Day 4 if no team invite sent)**:
- Subject: "Your team is waiting -- invite them to [Product]"
- Body: Social proof ("Teams of [N]+ see [X%] higher activation"). Direct link to team invite page.
- Skip if: first_invite_sent = true

**Email 5 (Day 7 if workspace not ready)**:
- Subject: "Need help setting up? Let's talk."
- Body: Personal from founder/CSM. Offer a 15-minute setup call. Calendar booking link.
- Skip if: workspace_ready = true

### 7. Build the setup funnel in PostHog

Using the `posthog-funnels` fundamental, create an admin setup funnel:

```
workspace_created
  → profile_configured
  → billing_configured
  → permissions_set
  → integration_connected
  → first_team_invite_sent
  → workspace_ready
```

Break down by: signup source, plan selected, company size, and cohort week. Identify the biggest drop-off step and focus optimization there.

### 8. Wire PostHog events to Loops via n8n

Using `n8n-triggers` and `n8n-workflow-basics`, create an n8n workflow that bridges PostHog admin setup events to Loops contact properties:

```
PostHog Webhook (admin_setup_step_completed)
  → Extract admin email, step_name, step_number
  → PUT to Loops /api/v1/contacts/update with {step_name_completed: true}
  → POST to Loops /api/v1/events/send with {eventName: step_name}
  → Loops sequence uses this to skip already-completed emails
```

Also create a workflow for the `workspace_ready` event that exits the admin from the setup sequence and enrolls them in the "admin ongoing" sequence (tips for managing their team, feature updates, usage reports).

## Output

- Intercom Checklist guiding admins through 6 workspace setup steps with auto-completion
- Permissions product tour for the most complex setup step
- 3 stall-point nudge messages for admins who get stuck
- 5-email admin lifecycle sequence in Loops with behavioral skip logic
- PostHog funnel tracking the full admin setup journey
- n8n workflows bridging PostHog events to Loops and Intercom

## Triggers

Run once during initial play setup. Re-run when adding new setup steps (new integration types, new permission models) or when the setup flow changes.
