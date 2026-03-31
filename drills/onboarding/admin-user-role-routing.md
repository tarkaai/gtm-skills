---
name: admin-user-role-routing
description: Classify signups as admin or end user at entry point and route them to the correct onboarding path with tracking and CRM sync
category: Onboarding
tools:
  - PostHog
  - Intercom
  - n8n
  - Attio
  - Loops
fundamentals:
  - posthog-custom-events
  - posthog-feature-flags
  - posthog-cohorts
  - intercom-user-properties
  - intercom-checklists
  - n8n-triggers
  - n8n-workflow-basics
  - attio-contacts
  - loops-audience
---

# Admin vs User Role Routing

This drill classifies every new signup as either an admin (workspace creator/configurator) or an end user (team member invited to an existing workspace) and routes them to the appropriate onboarding path. The classification happens at the moment of entry and determines which Intercom checklist, which Loops email sequence, and which PostHog feature flags the user receives.

## Prerequisites

- Your product has distinct admin and user roles (or workspace creator vs invited member)
- PostHog tracking installed with user identification
- Intercom with Checklists and Product Tours configured
- n8n instance for routing automation
- Loops account with separate admin and user email sequences ready

## Steps

### 1. Define classification signals

Determine how to distinguish admins from users at the moment of signup or first login. Common signals:

| Signal | Admin indicator | User indicator |
|--------|----------------|----------------|
| Entry path | Signed up on marketing site, created workspace | Clicked invite link, joined existing workspace |
| Signup URL | `/signup`, `/get-started`, `/pricing` | `/invite/{token}`, `/join/{workspace}` |
| Role selection | Selected "I'm setting this up for my team" | Selected "I was invited by my team" |
| Workspace state | No existing workspace; creates new one | Workspace already exists; joins it |
| Permissions | Assigned owner/admin role by system | Assigned member/user role by system |

The strongest signal is the entry path: workspace creators are admins, invite-link users are end users. If your product has an explicit role selection during signup, use that as the primary signal.

### 2. Instrument the classification event

Using the `posthog-custom-events` fundamental, fire a classification event at the moment the role is determined:

```javascript
posthog.capture('user_role_classified', {
  role: 'admin', // or 'user'
  classification_method: 'entry_path', // or 'role_selection', 'workspace_state'
  workspace_id: workspaceId,
  workspace_is_new: true, // false for invited users
  signup_source: utmSource,
  company_size: companySize // if captured at signup
});

// Set the person property for all future segmentation
posthog.people.set({
  user_role: 'admin',
  workspace_id: workspaceId,
  is_workspace_creator: true
});
```

### 3. Build role-based cohorts in PostHog

Using the `posthog-cohorts` fundamental, create these cohorts:

- **Admins -- Active Setup**: `user_role` = "admin" AND `workspace_ready` != true
- **Admins -- Setup Complete**: `user_role` = "admin" AND `workspace_ready` = true
- **Users -- New**: `user_role` = "user" AND `activation_reached` != true AND `signed_up_at` within last 14 days
- **Users -- Activated**: `user_role` = "user" AND `activation_reached` = true
- **Admins -- Stalled**: `user_role` = "admin" AND `workspace_ready` != true AND `signed_up_at` > 7 days ago

These cohorts drive feature flags, Intercom messaging, and anomaly detection.

### 4. Configure role-based feature flags

Using the `posthog-feature-flags` fundamental, create a feature flag that controls which onboarding experience loads:

```
Flag: onboarding-role-path
Variant "admin": user_role = "admin"
Variant "user": user_role = "user"
Variant "default": fallback for unclassified
```

Your product code checks this flag to determine:
- Which Intercom checklist to display (admin setup checklist vs user getting-started checklist)
- Which dashboard layout to show on first login (admin sees setup overview; user sees workspace activity)
- Which feature set is visible (admin sees settings/billing/team management; user sees workflow tools)

### 5. Wire classification to Intercom

Using `intercom-user-properties`, push the role classification to Intercom immediately after classification:

```javascript
Intercom('update', {
  user_role: 'admin',
  workspace_id: workspaceId,
  is_workspace_creator: true,
  onboarding_path: 'admin_setup'
});
```

This triggers the correct Intercom checklist based on audience rules:
- `user_role` = "admin" shows the "Workspace Setup" checklist (from `workspace-setup-flow` drill)
- `user_role` = "user" shows the "Getting Started" checklist (from `onboarding-flow` drill)

### 6. Wire classification to Loops

Using `n8n-triggers` and `n8n-workflow-basics`, create an n8n workflow triggered by the PostHog `user_role_classified` webhook:

```
PostHog Webhook (user_role_classified)
  → Extract email, role, workspace_id, signup_source
  → POST to Loops /api/v1/contacts/create with {
      email, user_role, workspace_id, signup_source
    }
  → If role = "admin": POST Loops event "admin_signup" (starts admin email sequence)
  → If role = "user": POST Loops event "user_signup" (starts user email sequence)
```

Using `loops-audience`, create two segments:
- "Admin Onboarding" -- contacts where `user_role` = "admin"
- "User Onboarding" -- contacts where `user_role` = "user"

### 7. Sync to CRM

Using `n8n-workflow-basics` and `attio-contacts`, extend the classification workflow to create or update Attio records:

```
→ Use attio-contacts to create Person record with:
    role: admin/user
    workspace_id
    signup_source
    classification_method
  → If admin: also create Company record (if new workspace) with workspace_id
  → If user: link Person to existing Company by workspace_id
```

This ensures the CRM reflects the role split for sales team visibility.

### 8. Handle edge cases

Build logic for these scenarios:

- **Role change**: An end user gets promoted to admin. The app fires a `user_role_changed` event. n8n workflow updates PostHog person property, Intercom attributes, and Loops contact. Intercom shows the admin checklist. Loops enrolls in the admin sequence (skipping steps the user already completed as an end user).
- **Solo user**: Someone signs up, creates a workspace, but never invites anyone. Classify as admin initially. After 14 days with no team invite, fire a `solo_user_detected` event and adjust messaging to focus on solo value rather than team setup.
- **Multiple admins**: Second admin joins an already-configured workspace. Classify as admin but skip workspace setup steps that are already complete. Show a reduced checklist: "Your workspace is set up. Here's what you can configure."

### 9. Build the routing funnel in PostHog

Using `posthog-funnels`, create a routing verification funnel:

```
signup_completed
  → user_role_classified
  → onboarding_path_started (admin_setup OR user_getting_started)
  → first_checklist_step_completed
```

Break down by role to verify: are all signups being classified? Is the classification accurate? Are both paths starting correctly? If `user_role_classified` drops significantly below `signup_completed`, the classification logic has a gap.

## Output

- Every signup classified as admin or user within seconds of account creation
- PostHog person properties and cohorts segmenting by role
- Feature flag routing users to the correct onboarding experience
- Intercom showing the correct checklist per role
- Loops enrolling in the correct email sequence per role
- Attio CRM records reflecting the role classification
- Edge case handling for role changes, solo users, and multi-admin workspaces

## Triggers

Run once during initial play setup. Re-run when adding new roles (e.g., "viewer" role), when changing the classification logic, or when launching new onboarding paths.
