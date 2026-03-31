---
name: invite-flow-setup
description: Build the in-product invite mechanism with contextual triggers, frictionless sharing, and full event tracking
category: Advocacy
tools:
  - PostHog
  - Intercom
  - Loops
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - intercom-in-app-messages
  - intercom-product-tours
  - loops-transactional
  - attio-contacts
  - n8n-workflow-basics
  - n8n-triggers
---

# Invite Flow Setup

This drill builds the complete in-product invite mechanism: the UI surfaces where users invite teammates, the backend that processes invitations, the tracking that measures every step, and the CRM routing that captures invited users as expansion leads.

## Input

- Product with multi-user or team functionality (seats, shared workspaces, collaborative features)
- PostHog tracking installed with user and account identification
- Intercom configured for in-app messaging
- Loops configured for transactional emails
- Attio CRM for contact and deal tracking
- Clear plan structure with seat limits per tier

## Steps

### 1. Map invite entry points

Identify every location in the product where an invite action is natural. Invite surfaces must appear at moments when the user's current task would benefit from a teammate. Entry points ranked by conversion intent:

**High-intent (user is actively trying to collaborate):**
- Team settings / member management page
- "Share" button on any shared resource (project, document, workspace)
- @mention input field when the mentioned person is not on the account
- Permission settings when granting access to a resource

**Medium-intent (user encounters a collaborative feature):**
- Empty team member list during onboarding
- Collaborative feature discovery (comments, shared views, real-time editing)
- Workspace creation flow

**Low-intent (ambient prompts):**
- Dashboard sidebar showing "Invite teammates" with current seat count
- Post-milestone celebration ("You just completed X — invite a colleague to try it too")
- Onboarding checklist item: "Invite your first teammate"

For each entry point, define:
- Trigger condition (what user action or state opens this surface)
- Surface type (inline button, modal, tooltip, banner, checklist item)
- Pre-filled context (what data can be auto-populated to reduce friction)

### 2. Build the invite form

The invite form must be as frictionless as possible. Minimum viable form:

**Required fields:**
- Email address (with multi-email support — paste a comma-separated list)

**Optional but valuable:**
- Role/permission level (dropdown: Admin, Member, Viewer)
- Personal message from the inviter (pre-filled with a default, editable)

**Pre-filled automatically:**
- Inviter name and avatar (shown in the invitation)
- Workspace/team name
- Current project or resource being shared (if invite triggered from a share action)

Implementation via product code. Track form interactions with `posthog-custom-events`:

```javascript
// Invite form opened
posthog.capture('invite_form_opened', {
  account_id: accountId,
  entry_point: 'team_settings',  // | share_button | mention | onboarding_checklist | sidebar
  current_seat_count: currentSeats,
  seat_limit: planSeatLimit,
  seats_remaining: planSeatLimit - currentSeats
});

// Invite sent
posthog.capture('invite_sent', {
  account_id: accountId,
  inviter_user_id: userId,
  invite_count: emailCount,
  entry_point: 'share_button',
  invitee_domain_match: inviteeDomain === companyDomain,  // same company = strong signal
  role_assigned: 'member',
  has_personal_message: !!personalMessage,
  current_seat_count: currentSeats,
  seat_limit: planSeatLimit
});

// Invite form abandoned (opened but not submitted)
posthog.capture('invite_form_abandoned', {
  account_id: accountId,
  entry_point: 'team_settings',
  field_reached: 'email',  // last field the user interacted with
  time_in_form_seconds: timeSpent
});
```

### 3. Build the invitation delivery

Using the `loops-transactional` fundamental, create the invitation email:

**Template: team-invite**
- From: "{{inviterName}} via {{productName}}" (personal sender, not generic)
- Subject: "{{inviterName}} invited you to join {{teamName}} on {{productName}}"
- Body:
  - Personal message from inviter (if provided)
  - What the team is working on (context from the resource or workspace)
  - One-click accept button (large, prominent)
  - What they get: "Join {{teamName}} to [specific value proposition based on product]"
  - Social proof: "{{teamMemberCount}} people are already collaborating"
- Footer: "Not interested? You can ignore this invitation."

**Critical: The accept link must:**
- Pre-authenticate if possible (magic link pattern)
- Pre-fill their email and team assignment
- Drop them directly into the shared workspace/resource, NOT a generic dashboard
- Track: `invite_link_clicked`, `invite_accepted`, `invited_user_first_action`

### 4. Build the acceptance flow

When an invited user clicks the accept link:

1. If they already have an account: add them to the team immediately, redirect to the shared context
2. If they are new: show a minimal signup form (name + password only — email is pre-filled from the invite)
3. After signup: skip the standard onboarding and drop them into the team's workspace with a contextual product tour using `intercom-product-tours`

Track with `posthog-custom-events`:

```javascript
posthog.capture('invite_accepted', {
  account_id: accountId,
  invited_user_id: newUserId,
  inviter_user_id: inviterUserId,
  is_new_user: !existingAccount,
  time_to_accept_hours: hoursSinceInviteSent,
  entry_point_original: originalEntryPoint
});

posthog.capture('invited_user_first_action', {
  account_id: accountId,
  user_id: newUserId,
  action: 'viewed_shared_project',
  time_to_first_action_minutes: minutesSinceAccept,
  was_invited: true
});
```

### 5. Handle invite edge cases

Build handling for these scenarios:

- **Seat limit reached:** If the account has no remaining seats, show the invite form but surface the upgrade path: "Your plan includes {{seatLimit}} seats. Add more seats to invite {{inviteeName}}." Link to the upgrade page. Track `invite_blocked_seat_limit`.
- **Invite already pending:** If the invitee already has a pending invite, show a "Resend" button instead of creating a duplicate. Track `invite_resent`.
- **Invite expired:** Set a 14-day expiration. After expiry, allow the inviter to resend. Track `invite_expired`.
- **Invitee on another account:** If the email belongs to an existing user on a different account, handle the multi-account scenario (either join both accounts or show a choice).
- **Bounce/invalid email:** Detect bounced invite emails via Loops webhook. Notify the inviter: "The invitation to {{email}} could not be delivered." Track `invite_bounced`.

### 6. Wire CRM and automation

Using `n8n-triggers` and `n8n-workflow-basics`, build an n8n workflow:

1. **On invite_sent**: Use `attio-contacts` to create or update the invitee's contact record in Attio. Tag them as "Invited — Pending." Associate with the inviter's company record.
2. **On invite_accepted**: Update the contact status to "Active — Invited User." If this seat addition crosses a tier boundary, create an expansion signal in Attio.
3. **On invite not accepted after 72 hours**: Trigger a reminder email via Loops: "{{inviterName}} is waiting for you to join {{teamName}}."
4. **On invite not accepted after 7 days**: Send the inviter an in-app notification via Intercom: "{{inviteeName}} hasn't accepted yet. Want to resend or try a different email?"

### 7. Build the invite funnel

Using `posthog-funnels`, create the complete invite funnel:

1. `invite_form_opened` — user saw the invite surface
2. `invite_sent` — user submitted at least one email
3. `invite_email_delivered` — Loops confirmed delivery
4. `invite_link_clicked` — invitee clicked the accept link
5. `invite_accepted` — invitee completed signup/join
6. `invited_user_first_action` — invitee took a meaningful action

Break down by: entry_point, inviter_tenure (days since signup), current_seat_count, plan_tier, invitee_domain_match (same company vs external).

## Output

- Invite surfaces at 3+ product entry points with contextual triggers
- Frictionless invite form with multi-email support
- Personalized invitation email via Loops
- Acceptance flow that drops invitees into context (not generic dashboard)
- Edge case handling for seat limits, duplicates, bounces, and expiration
- n8n workflow routing invites to Attio CRM
- PostHog funnel tracking every step from form open to invitee first action

## Triggers

Run once during initial play setup (Smoke level). Re-run when adding new entry points (Scalable level) or when optimizing specific funnel steps based on data.
